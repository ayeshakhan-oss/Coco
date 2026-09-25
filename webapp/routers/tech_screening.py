"""The technical screening wizard: pick a job, review the rubric, check the
pool and cost, confirm, then run.

🔒 THIS ROUTER WRITES TO NUGGET'S TABLES. Until 2026-09-25 Coco was read-only
against `public.nugget_screening_*`; the owner lifted that so runs can be
launched from Railway instead of depending on a desktop worker. Every write
goes through `services.nugget_writes`, which executes only statements declared
as module-level constants. `/api/evaluations` stays read-only and is unchanged.

THIS IS NOT COCO'S CV SCREENING. That is a separate system with its own
criteria and its own shortlist/maybe/no_hire vocabulary, and the two must never
share a rubric or a tier (Ayesha, 2026-09-15). Technical roles are tiered
P1-P4 against Nugget's rubric; `/api/cv-screening` is untouched by this file.
"""

from __future__ import annotations

import logging
import os
import socket
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user, require_editor
from ..schemas import (
    TechCreateRunRequest, TechJobOut, TechModelOut, TechPlanOut,
    TechPlanRequest, TechRubricDraftRequest, TechRubricPublishRequest,
    TechRubricStepOut, TechRunOut, TechWorkOut, TechWorkRequest,
)
from ..services import (
    job_description, nugget_writes, pricing, rubric_drafting, screening_runs,
)
from ..services.drafting import DraftingUnavailable

log = logging.getLogger("webapp.tech_screening")

router = APIRouter(prefix="/api/tech-screening", tags=["tech-screening"])


def _worker_id() -> str:
    """Who claimed an item. Nugget's own workers identify as
    `HOST:PID:RANDOM`; keeping the shape means a mixed run stays readable in
    `claimed_by` whoever executed it."""
    return f"{socket.gethostname()}:{os.getpid()}:{uuid.uuid4().hex[:8]}"


# Jobs with their rubric and screening state. Markaz's tables are always in
# `public`; only the nugget_screening_* tables follow NUGGET_SCHEMA.
_JOBS_SQL = """
SELECT j.id AS job_pk, j.job_id AS job_code, j.title, j.department, j.job_status,
       COUNT(DISTINCT a.id) AS applications
FROM public.jobs j
LEFT JOIN public.applications a ON a.job_id = j.id
GROUP BY j.id, j.job_id, j.title, j.department, j.job_status
ORDER BY (j.job_status = 'Active') DESC, j.title
"""


def _rubric_state(db: Session) -> dict:
    sql = f"""
    SELECT r.job_id, r.version,
           COUNT(*) FILTER (WHERE e.id IS NOT NULL) AS scored
    FROM {nugget_writes.schema()}.nugget_screening_rubrics r
    LEFT JOIN {nugget_writes.schema()}.nugget_screening_evals e
           ON e.job_id = r.job_id AND e.is_current AND e.status = 'scored'
    WHERE r.status = 'active'
    GROUP BY r.job_id, r.version
    """
    return {r["job_id"]: r for r in db.execute(text(sql)).mappings()}


def _live_runs(db: Session) -> dict:
    sql = f"""
    SELECT job_id, id, status FROM {nugget_writes.schema()}.nugget_screening_runs
    WHERE status IN ('planning', 'queued', 'running', 'paused')
    """
    return {r["job_id"]: r for r in db.execute(text(sql)).mappings()}


@router.get("/jobs", response_model=list[TechJobOut])
def jobs(db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    """Step 1. Every position, live first.

    Deliberately NOT filtered to active jobs: exactly 1 of 32 is `Active`, and
    defaulting to active-only once made every job picker in the app a
    one-item dropdown (CLAUDE.md Rule 32).
    """
    rubrics = _rubric_state(db)
    runs = _live_runs(db)
    out = []
    for row in db.execute(text(_JOBS_SQL)).mappings():
        rubric = rubrics.get(row["job_pk"])
        run = runs.get(row["job_pk"])
        out.append({
            **dict(row),
            "has_rubric": rubric is not None,
            "rubric_version": rubric["version"] if rubric else None,
            "scored": int(rubric["scored"]) if rubric else 0,
            "live_run_id": str(run["id"]) if run else None,
            "live_run_status": run["status"] if run else None,
        })
    return out


@router.get("/models", response_model=list[TechModelOut])
def models(_user: dict = Depends(get_current_user)):
    return pricing.price_table()


@router.get("/jobs/{job_id}/rubric", response_model=TechRubricStepOut)
def job_rubric(
    job_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """Step 2. The published rubric, or why one cannot be drafted yet."""
    meta = db.execute(
        text("SELECT title, department, description FROM public.jobs WHERE id = :id"),
        {"id": job_id},
    ).mappings().first()
    if not meta:
        raise HTTPException(404, "No such job")

    rubric = screening_runs.active_rubric(db, job_id)
    blocked = None
    if rubric is None:
        try:
            job_description.to_text(meta["description"])
        except job_description.JobDescriptionUnreadable as exc:
            blocked = (
                f"This job has no readable description, so a rubric cannot be "
                f"drafted from it: {exc}"
            )
    return {
        "job_id": job_id,
        "job_title": meta["title"],
        "department": meta["department"],
        "jd_source": "neon_description",
        "rubric": screening_runs.rubric_summary(rubric),
        "blocked_reason": blocked,
    }


@router.post("/rubric/draft")
def draft_rubric(
    body: TechRubricDraftRequest,
    db: Session = Depends(get_db),
    _user: dict = Depends(require_editor),
):
    """Draft a rubric from the job description. WRITES NOTHING.

    The draft comes back for a person to read. A rubric decides how every
    applicant to this role is judged, so it is published by a separate,
    deliberate call.
    """
    meta = db.execute(
        text("SELECT title, department, description FROM public.jobs WHERE id = :id"),
        {"id": body.job_id},
    ).mappings().first()
    if not meta:
        raise HTTPException(404, "No such job")
    try:
        jd = job_description.to_text(meta["description"])
    except job_description.JobDescriptionUnreadable as exc:
        raise HTTPException(422, str(exc)) from exc

    try:
        draft = rubric_drafting.draft_rubric(
            job_title=meta["title"], department=meta["department"],
            location=None, job_description=jd,
        )
    except DraftingUnavailable as exc:
        raise HTTPException(503, str(exc)) from exc
    except rubric_drafting.RubricDraftError as exc:
        raise HTTPException(422, f"The drafted rubric was rejected: {exc}") from exc
    return {"job_id": body.job_id, "draft": draft}


@router.post("/rubric")
def publish_rubric(
    body: TechRubricPublishRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """Publish a reviewed draft as the job's active rubric.

    Archiving the previous version and inserting the new one happen in ONE
    transaction: `uq_nsr_active_per_job` forbids two active rows, and doing it
    in two would leave the job with no rubric at all if the second failed.
    """
    try:
        draft = rubric_drafting.validate_draft(body.draft)
    except rubric_drafting.RubricDraftError as exc:
        raise HTTPException(422, str(exc)) from exc

    for field in ("system_prompt", "output_schema", "jd_snapshot"):
        if not body.draft.get(field):
            raise HTTPException(
                422,
                f"the draft is missing {field}: publish the draft returned by "
                "/rubric/draft rather than a hand-built object",
            )
        draft[field] = body.draft[field]
    draft["drafted_by_model"] = body.draft.get("drafted_by_model")
    draft["jd_source"] = body.draft.get("jd_source", "neon_description")

    try:
        result = screening_runs.publish_rubric(
            db, job_id=body.job_id, draft=draft, created_by=user["email"],
        )
    except Exception:
        db.rollback()
        raise
    db.commit()
    return {"job_id": body.job_id, **result}


@router.post("/runs/plan", response_model=TechPlanOut)
def plan(
    body: TechPlanRequest,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """Step 3. Who gets screened and what it costs. Reads only."""
    if body.model not in pricing.known_models():
        raise HTTPException(422, f"unknown model {body.model!r}")
    try:
        result = screening_runs.plan_run(
            db, job_id=body.job_id, mode=body.mode, since_days=body.since_days,
            max_candidates=body.max_candidates, model=body.model,
            use_batch=body.use_batch,
        )
    except screening_runs.NoActiveRubric as exc:
        raise HTTPException(409, str(exc)) from exc
    except screening_runs.RunError as exc:
        raise HTTPException(422, str(exc)) from exc

    live = screening_runs.live_run_for_job(db, body.job_id)
    result["live_run_id"] = str(live["id"]) if live else None
    return result


@router.post("/runs")
def create_run(
    body: TechCreateRunRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """Step 4. Create the run and its items in one transaction."""
    if body.model not in pricing.known_models():
        raise HTTPException(422, f"unknown model {body.model!r}")
    if body.effort not in screening_runs.EFFORTS:
        raise HTTPException(422, f"unknown effort {body.effort!r}")
    try:
        plan_result = screening_runs.plan_run(
            db, job_id=body.job_id, mode=body.mode, since_days=body.since_days,
            max_candidates=body.max_candidates, model=body.model,
            use_batch=body.use_batch,
        )
        run_id = screening_runs.create_run(
            db, job_id=body.job_id, plan=plan_result, requested_by=user["email"],
            effort=body.effort, cost_cap_usd=body.cost_cap_usd,
        )
    except screening_runs.RunConflict as exc:
        db.rollback()
        raise HTTPException(409, str(exc)) from exc
    except screening_runs.NoActiveRubric as exc:
        db.rollback()
        raise HTTPException(409, str(exc)) from exc
    except screening_runs.RunError as exc:
        db.rollback()
        raise HTTPException(422, str(exc)) from exc
    except Exception:
        db.rollback()
        raise
    db.commit()
    return {"run_id": run_id, "job_id": body.job_id,
            "total_items": plan_result["people"]}


@router.get("/runs/{run_id}", response_model=TechRunOut)
def get_run(
    run_id: str,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    run = screening_runs.get_run(db, run_id)
    if not run:
        raise HTTPException(404, "No such run")
    return screening_runs.run_progress(run, db=db)


@router.get("/jobs/{job_id}/runs", response_model=list[TechRunOut])
def job_runs(
    job_id: int,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    out = []
    for row in screening_runs.runs_for_job(db, job_id, limit=limit):
        full = screening_runs.get_run(db, row["id"])
        if full:
            out.append(screening_runs.run_progress(full, db=db))
    return out


@router.post("/runs/{run_id}/work", response_model=TechWorkOut)
def work(
    run_id: str,
    body: TechWorkRequest,
    db: Session = Depends(get_db),
    _user: dict = Depends(require_editor),
):
    """One slice of a run: reap stuck items, claim a few, score them.

    The browser loops on `remaining`. Each candidate commits as it finishes, so
    a request lost to a redeploy costs one slice, and the reaper returns
    whatever it had claimed.
    """
    try:
        return screening_runs.work(
            db, run_id=run_id, worker=_worker_id(), limit=body.limit,
        )
    except DraftingUnavailable as exc:
        db.rollback()
        raise HTTPException(503, str(exc)) from exc
    except screening_runs.RunError as exc:
        db.rollback()
        raise HTTPException(422, str(exc)) from exc
    except Exception:
        db.rollback()
        raise


@router.post("/runs/{run_id}/cancel", response_model=TechRunOut)
def cancel_run(
    run_id: str,
    db: Session = Depends(get_db),
    _user: dict = Depends(require_editor),
):
    run = screening_runs.get_run(db, run_id)
    if not run:
        raise HTTPException(404, "No such run")
    try:
        screening_runs.request_cancel(db, run_id)
    except Exception:
        db.rollback()
        raise
    db.commit()
    return screening_runs.run_progress(screening_runs.get_run(db, run_id), db=db)
