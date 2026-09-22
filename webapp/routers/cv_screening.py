"""Coco's own CV screening: screen a candidate's CV against their job's JD.

`webapp/services/cv_screening.py` holds the locked rules (the three criteria,
the 0-5 conversion with a real zero, the tiers) and `screen_cv`, which calls the
model and re-validates its response against them.
`webapp/services/job_description.py` turns Markaz's HTML `jobs.description` into
readable text or refuses. `reads.get_cv_evidence` produces the candidate's CV
text or says why it could not. This router is the only code that persists a
screen.

🔒 THIS IS NOT TECHNICAL SCREENING (Ayesha, 2026-09-15: "cv screening and
   technical screening are both separate so you shouldn't mix their
   sops/rubrics/rules"). Nugget's engine is read through
   `routers/evaluations.py` against `public.nugget_screening_*` and is
   READ-ONLY; it has its own rubric, its own P1-P4 tiers and its own gates.
   Nothing in this file reads, writes or imitates it.

Rules enforced here, verbatim rule -> mechanism:

  1. `require_editor` gates screening. Reading a screen needs only a signed-in
     user, exactly like reading a case-study evaluation.
  2. A screen REFUSES rather than degrades. No CV text (422), no readable job
     description (422), no model credential (503). CLAUDE.md Rule 29: 27 CV
     rejections were sent live written from nothing but a first name and a role
     title, because the drafting path accepted empty evidence instead of
     refusing.
  3. The job is read from the APPLICATION's own row, never from a client-supplied
     job id, so a screen cannot be run against a different job's JD.
  4. Re-screening SUPERSEDES. The previous current row for that application is
     flipped to `is_current = False` and given `superseded_by`, in the same
     transaction as the insert. CLAUDE.md Rule 25: a superseded result left live
     somewhere cost three corrections on the RM round.
  5. `match` and `tier` are computed by `cv_screening`, never taken from the
     model, and never recomputed differently by a reader.
"""

from __future__ import annotations

import hashlib
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user, require_editor
from ..models import CVScreen
from ..schemas import (
    CVScreenApplicationOut,
    CVScreenCriterionOut,
    CVScreenJobSummaryOut,
    CVScreenOut,
    CVScreenRequest,
)
from ..services import reads
from ..services.cv_screening import CRITERIA, CVScreeningError, screen_cv
from ..services.drafting import DraftingUnavailable
from ..services.job_description import JobDescriptionUnreadable, to_text

log = logging.getLogger("webapp.routers.cv_screening")

router = APIRouter(prefix="/api/cv-screening", tags=["cv-screening"])


# `jobs.description` is the real JD column. `jobs.jd_text` looks like the
# obvious one and is a trap: across all 32 live jobs on 2026-09-22 it was
# populated on ONE and averaged 211 characters, while `description` was
# populated on 31. See services/job_description.py.
_JOB_SQL = text("SELECT id, title, description FROM jobs WHERE id = :job_id")

_APPLICATIONS_FOR_JOB_SQL = text(
    """
    SELECT a.id                AS application_id,
           a.status            AS status,
           a.created_at        AS applied_at,
           a.custom_answers    AS custom_answers,
           a.canned_answers    AS canned_answers,
           c.first_name        AS first_name,
           c.last_name         AS last_name,
           c.email             AS email,
           (c.resume_data IS NOT NULL AND length(c.resume_data) > 0) AS has_resume
    FROM applications a
    JOIN candidates c ON c.id = a.candidate_id
    WHERE a.job_id = :job_id
    ORDER BY a.created_at DESC NULLS LAST, a.id DESC
    """
)

# Readers MUST filter on is_current, exactly as Nugget's own evals table
# requires: a superseded screen is history, never a live number.
_CURRENT_SCREENS_FOR_JOB_SQL = text(
    "SELECT * FROM coco.cv_screens WHERE job_id = :job_id AND is_current"
)

_SCREENS_FOR_APPLICATION_SQL = text(
    "SELECT * FROM coco.cv_screens WHERE application_id = :application_id "
    "ORDER BY created_at DESC"
)


def _criteria_out() -> list[CVScreenCriterionOut]:
    return [CVScreenCriterionOut(**c) for c in CRITERIA]


def _screen_out(row) -> CVScreenOut:
    """Accepts an ORM CVScreen or a SQL mapping; both carry the same names
    except `model`, which the ORM maps to `model_name` to dodge Pydantic v2's
    protected `model_` namespace."""
    get = (lambda k: getattr(row, k)) if isinstance(row, CVScreen) else row.__getitem__
    model_value = getattr(row, "model_name", None) if isinstance(row, CVScreen) else row["model"]
    return CVScreenOut(
        id=get("id"),
        application_id=get("application_id"),
        job_id=get("job_id"),
        candidate_name=get("candidate_name"),
        role=get("role"),
        scores=get("scores"),
        evidence=get("evidence"),
        strengths=get("strengths"),
        gaps=get("gaps"),
        total_experience_years=get("total_experience_years"),
        relevant_experience_years=get("relevant_experience_years"),
        relevant_experience_note=get("relevant_experience_note"),
        match=get("match"),
        tier=get("tier"),
        model=model_value,
        sop_sha256=get("sop_sha256"),
        jd_sha256=get("jd_sha256"),
        cv_chars=get("cv_chars"),
        cv_truncated=get("cv_truncated"),
        is_current=get("is_current"),
        superseded_by=get("superseded_by"),
        created_by=get("created_by"),
        created_at=get("created_at"),
        criteria=_criteria_out(),
    )


# The SOP requires Expected Salary, City and Relocate captured for every
# candidate. Markaz stores them as free-text Q&A, so they are matched on the
# QUESTION wording and returned as None when no question matches -- never
# inferred from somewhere else, and never guessed.
_PROFILE_FIELDS = {
    "expected_salary": ("expected salary", "salary expectation", "current salary"),
    "city": ("city", "current location", "where are you based", "location"),
    "willing_to_relocate": ("relocate", "relocation", "willing to move"),
}


def _profile_fields(custom_answers, canned_answers) -> dict[str, Optional[str]]:
    pairs: list[tuple[str, str]] = []
    for blob in (custom_answers, canned_answers):
        if isinstance(blob, list):
            for item in blob:
                if isinstance(item, dict):
                    q = item.get("question") or item.get("label") or item.get("title")
                    a = item.get("answer") or item.get("value") or item.get("response")
                    if isinstance(q, str) and a not in (None, ""):
                        pairs.append((q.lower(), str(a).strip()))
        elif isinstance(blob, dict):
            for q, a in blob.items():
                if isinstance(q, str) and a not in (None, ""):
                    pairs.append((q.lower(), str(a).strip()))

    out: dict[str, Optional[str]] = {k: None for k in _PROFILE_FIELDS}
    for field, needles in _PROFILE_FIELDS.items():
        for question, answer in pairs:
            if any(n in question for n in needles):
                out[field] = answer
                break
    return out


@router.get("/criteria", response_model=list[CVScreenCriterionOut])
def get_criteria(user: dict = Depends(get_current_user)):
    """Coco's three criteria and their weights, so the UI renders from the
    service rather than a TypeScript constant that can drift."""
    return _criteria_out()


@router.get("/jobs")
def list_jobs(
    active_only: bool = Query(True),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    return reads.list_jobs(db, active_only=active_only)


@router.get("/jobs/{job_id}/summary", response_model=CVScreenJobSummaryOut)
def job_summary(
    job_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """The four stat boxes of the locked report format. They must sum to the
    total, which the SOP's Common Mistakes table calls out by name."""
    job = db.execute(_JOB_SQL, {"job_id": job_id}).mappings().first()
    if not job:
        raise HTTPException(404, f"Job {job_id} not found")

    total = db.execute(
        text("SELECT COUNT(*) FROM applications WHERE job_id = :job_id"),
        {"job_id": job_id},
    ).scalar_one()

    counts = {"shortlist": 0, "maybe": 0, "no_hire": 0}
    for row in db.execute(_CURRENT_SCREENS_FOR_JOB_SQL, {"job_id": job_id}).mappings():
        counts[row["tier"]] = counts.get(row["tier"], 0) + 1

    jd_chars, jd_error = 0, None
    try:
        jd_chars = len(to_text(job["description"], job_id=job_id))
    except JobDescriptionUnreadable as exc:
        jd_error = str(exc)

    return CVScreenJobSummaryOut(
        job_id=job_id,
        title=job["title"],
        total=total,
        unscreened=total - sum(counts.values()),
        jd_chars=jd_chars,
        jd_error=jd_error,
        **counts,
    )


@router.get("/jobs/{job_id}/applications", response_model=list[CVScreenApplicationOut])
def list_applications(
    job_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    rows = db.execute(_APPLICATIONS_FOR_JOB_SQL, {"job_id": job_id}).mappings().all()
    screens = {
        r["application_id"]: _screen_out(r)
        for r in db.execute(
            _CURRENT_SCREENS_FOR_JOB_SQL, {"job_id": job_id}
        ).mappings()
    }

    out = []
    for r in rows:
        name = " ".join(p for p in (r["first_name"], r["last_name"]) if p).strip()
        out.append(
            CVScreenApplicationOut(
                application_id=r["application_id"],
                candidate_name=name or "(no name on record)",
                email=r["email"],
                status=r["status"],
                applied_at=r["applied_at"],
                cv_available=bool(r["has_resume"]),
                screen=screens.get(r["application_id"]),
                **_profile_fields(r["custom_answers"], r["canned_answers"]),
            )
        )
    return out


@router.get("/screens", response_model=list[CVScreenOut])
def list_screens(
    application_id: int = Query(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Every screen for an application, newest first. A re-screened candidate's
    history stays visible, with `is_current` saying which one is live."""
    rows = db.execute(
        _SCREENS_FOR_APPLICATION_SQL, {"application_id": application_id}
    ).mappings().all()
    return [_screen_out(r) for r in rows]


@router.post("/screen", response_model=CVScreenOut)
def screen(
    body: CVScreenRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    app_row = reads.get_application(db, body.application_id)
    if not app_row:
        raise HTTPException(404, "Application not found")

    # The job comes from the application's own row. A client-supplied job id
    # could screen a candidate against a different role's JD.
    job_id = app_row.get("job_pk")
    if job_id is None:
        raise HTTPException(422, f"Application {body.application_id} has no job on record")

    job = db.execute(_JOB_SQL, {"job_id": job_id}).mappings().first()
    if not job:
        raise HTTPException(404, f"Job {job_id} not found")

    try:
        jd = to_text(job["description"], job_id=job_id)
    except JobDescriptionUnreadable as exc:
        raise HTTPException(422, str(exc)) from exc

    evidence = reads.get_cv_evidence(db, body.application_id)
    cv = evidence.get("cv_text")
    if not cv:
        raise HTTPException(
            422,
            "Cannot screen this candidate: "
            + (evidence.get("cv_error") or "no CV on file")
            + ". A CV screen must be grounded in the candidate's actual CV.",
        )

    candidate_name = " ".join(
        p for p in (app_row.get("first_name"), app_row.get("last_name")) if p
    ).strip() or "the candidate"
    role = (app_row.get("job_title") or job["title"] or "the role").strip()

    try:
        result = screen_cv(
            cv_text=cv, job_description=jd, candidate_name=candidate_name, role=role
        )
    except DraftingUnavailable as exc:
        raise HTTPException(503, f"Screening unavailable: {exc}") from exc
    except CVScreeningError as exc:
        raise HTTPException(422, f"Model returned a malformed screen: {exc}") from exc
    except Exception as exc:
        # An unexpected model/SDK failure is not a predictable input error.
        # The detail is LOGGED, never returned: it can carry SDK internals.
        log.exception(
            "screen: unexpected failure for application %s", body.application_id
        )
        raise HTTPException(
            503,
            "Screening unavailable due to an unexpected error. Try again, or "
            "check the server logs for detail.",
        ) from exc

    row = CVScreen(
        application_id=body.application_id,
        job_id=job_id,
        candidate_name=candidate_name,
        role=role,
        scores=result["scores"],
        evidence=result["evidence"],
        strengths=result["strengths"],
        gaps=result["gaps"],
        total_experience_years=result["total_experience_years"],
        relevant_experience_years=result["relevant_experience_years"],
        relevant_experience_note=result["relevant_experience_note"],
        match=result["match"],
        tier=result["tier"],
        model_name=result["model"],
        sop_sha256=result["sop_sha256"],
        jd_sha256=hashlib.sha256(jd.encode("utf-8")).hexdigest(),
        cv_chars=result["cv_chars"],
        cv_truncated=result["cv_truncated"],
        # Set explicitly rather than left to the column default: the ORM
        # applies that at flush time, so until then the attribute is None
        # and anything reading the object back sees a row that is neither
        # current nor superseded.
        is_current=True,
        created_by=user.get("id") or "",
    )
    db.add(row)
    db.flush()  # assigns row.id, which the superseded rows must point at

    # Rule 25: retire the previous number in the same transaction that creates
    # its replacement, so there is never a moment with two current screens.
    db.execute(
        text(
            "UPDATE coco.cv_screens SET is_current = false, superseded_by = :new_id "
            "WHERE application_id = :application_id AND is_current AND id <> :new_id"
        ),
        {"new_id": row.id, "application_id": body.application_id},
    )
    db.commit()
    db.refresh(row)
    return _screen_out(row)
