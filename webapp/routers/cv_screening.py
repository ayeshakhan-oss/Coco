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
    CVScreenBatchOut,
    CVScreenBatchRequest,
    CVScreenCriterionOut,
    CVScreenJobSummaryOut,
    CVScreenOut,
    CVScreenRequest,
    CVScreenSkippedOut,
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
           a.applied_at        AS applied_at,
           a.custom_answers    AS custom_answers,
           a.canned_answers    AS canned_answers,
           c.first_name        AS first_name,
           c.last_name         AS last_name,
           c.email             AS email,
           (c.resume_data IS NOT NULL AND length(c.resume_data) > 0) AS has_resume
    FROM applications a
    JOIN candidates c ON c.id = a.candidate_id
    WHERE a.job_id = :job_id
    -- applications has applied_at, NOT created_at. Ordering by a
    -- non-existent column is a 500 on every request, and a fake-session
    -- test cannot see it because the SQL is never executed.
    ORDER BY a.applied_at DESC NULLS LAST, a.id DESC
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
#
# Priority order matters, and each field carries EXCLUDE terms as well as
# match terms. Both were learned from the live data, not guessed:
#
#   * "Are you willing to relocate to another city?" contains both words, so
#     without an order and a claim-once rule the answer "Yes" lands in City.
#   * CPD Coach asks "Willingness to travel in your assigned region (regions
#     may include certain city areas such as Subdivision City...)". A loose
#     "city" match claimed that travel question for 332 of 410 candidates and
#     printed "Yes I am willing to travel" as their city. It is not a city
#     question, and this job HAS no city question -- the location field is
#     "Address".
#
# A field with no matching question stays None. That is the honest answer and
# the SOP's requirement is to CAPTURE what was asked, not to manufacture it.
_PROFILE_FIELDS = (
    ("expected_salary",
     ("expected salary", "salary expectation", "current salary", "salary"),
     ()),
    ("willing_to_relocate",
     ("relocat", "willing to move"),
     ()),
    ("city",
     ("which city", "current city", "city of residence", "your city",
      "current location", "where are you based", "based in", "address"),
     # A travel or relocation question is never a statement of where someone
     # lives, however many times it says the word "city".
     ("travel", "willing", "relocat")),
)


def _answer_pairs(blob) -> list[tuple[str, str]]:
    """Every (question, answer) pair in one of Markaz's answer columns.

    🔴 THE REAL SHAPE IS NESTED. Measured across 800 live applications, the
    ONLY shape either column ever takes is:

        {"1763029445610": {"question": "...", "answer": "..."}}

    a dict keyed by a timestamp id. The flat `{question: answer}` and
    `[{question, answer}]` shapes this function also accepts were my own
    invention and occur zero times; they are kept only as cheap defence if
    Markaz ever changes. An earlier version handled ONLY those two, so it
    returned nothing for every candidate on record while looking correct.
    """
    pairs: list[tuple[str, str]] = []

    def add(question, answer) -> None:
        if isinstance(question, str) and answer not in (None, ""):
            text = str(answer).strip()
            if text:
                pairs.append((question.lower(), text))

    if isinstance(blob, dict):
        for key, value in blob.items():
            if isinstance(value, dict):
                add(value.get("question") or value.get("label"),
                    value.get("answer") or value.get("value"))
            else:
                add(key, value)
    elif isinstance(blob, list):
        for item in blob:
            if isinstance(item, dict):
                add(item.get("question") or item.get("label") or item.get("title"),
                    item.get("answer") or item.get("value") or item.get("response"))
    return pairs


def _profile_fields(custom_answers, canned_answers) -> dict[str, Optional[str]]:
    pairs = _answer_pairs(custom_answers) + _answer_pairs(canned_answers)

    out: dict[str, Optional[str]] = {f: None for f, _, _ in _PROFILE_FIELDS}
    claimed: set[int] = set()
    for field, needles, excludes in _PROFILE_FIELDS:
        for i, (question, answer) in enumerate(pairs):
            if i in claimed or any(x in question for x in excludes):
                continue
            if any(n in question for n in needles):
                out[field] = answer
                claimed.add(i)
                break
    return out


@router.get("/criteria", response_model=list[CVScreenCriterionOut])
def get_criteria(user: dict = Depends(get_current_user)):
    """Coco's three criteria and their weights, so the UI renders from the
    service rather than a TypeScript constant that can drift."""
    return _criteria_out()


@router.get("/jobs")
def list_jobs(
    # Defaults to ALL jobs, not just active ones. Exactly 1 of 32 jobs carries
    # job_status='Active' (CPD Coach); every position anyone actually screens
    # for -- SMG, both Growth Manager roles, Regional Manager -- is 'Closed'.
    # An active-only default showed a one-item dropdown and made the page
    # useless.
    active_only: bool = Query(False),
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


class _Skip(Exception):
    """This candidate cannot be screened, and that is not a failure of the run."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def _job_and_jd(db: Session, job_id: int):
    job = db.execute(_JOB_SQL, {"job_id": job_id}).mappings().first()
    if not job:
        raise HTTPException(404, f"Job {job_id} not found")
    try:
        jd = to_text(job["description"], job_id=job_id)
    except JobDescriptionUnreadable as exc:
        raise HTTPException(422, str(exc)) from exc
    return job, jd, hashlib.sha256(jd.encode("utf-8")).hexdigest()


def _screen_and_store(
    db: Session, application_id: int, *, job_id: int, job, jd: str, jd_sha: str,
    created_by: str,
) -> CVScreen:
    """Screen one application and persist it, superseding any earlier screen.

    Shared by the single-candidate endpoint and the batch runner so the two can
    never drift into scoring the same person differently. Raises `_Skip` for a
    candidate who cannot be screened (no CV, or a CV that did not extract), so a
    batch can record them and carry on instead of aborting.
    """
    app_row = reads.get_application(db, application_id)
    if not app_row:
        raise _Skip("application not found")

    evidence = reads.get_cv_evidence(db, application_id)
    cv = evidence.get("cv_text")
    if not cv:
        raise _Skip(evidence.get("cv_error") or "no CV on file")

    candidate_name = " ".join(
        p for p in (app_row.get("first_name"), app_row.get("last_name")) if p
    ).strip() or "the candidate"
    role = (app_row.get("job_title") or job["title"] or "the role").strip()

    try:
        result = screen_cv(
            cv_text=cv, job_description=jd, candidate_name=candidate_name, role=role
        )
    except CVScreeningError as exc:
        # A CV that did not extract is a document problem, not a weak candidate,
        # and must never be stored as a low score.
        if "extraction failure" in str(exc):
            raise _Skip(str(exc)) from exc
        raise

    row = CVScreen(
        application_id=application_id,
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
        jd_sha256=jd_sha,
        cv_chars=result["cv_chars"],
        cv_truncated=result["cv_truncated"],
        # Set explicitly rather than left to the column default: the ORM applies
        # that at flush time, so until then the attribute is None and anything
        # reading the object back sees a row that is neither current nor
        # superseded.
        is_current=True,
        created_by=created_by,
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
        {"new_id": row.id, "application_id": application_id},
    )
    return row


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

    job, jd, jd_sha = _job_and_jd(db, job_id)

    try:
        row = _screen_and_store(
            db, body.application_id, job_id=job_id, job=job, jd=jd, jd_sha=jd_sha,
            created_by=user.get("id") or "",
        )
    except _Skip as exc:
        raise HTTPException(
            422,
            f"Cannot screen this candidate: {exc.reason}. A CV screen must be "
            "grounded in the candidate's actual CV.",
        ) from exc
    except DraftingUnavailable as exc:
        raise HTTPException(503, f"Screening unavailable: {exc}") from exc
    except CVScreeningError as exc:
        raise HTTPException(422, f"Model returned a malformed screen: {exc}") from exc
    except Exception as exc:
        # An unexpected model/SDK failure is not a predictable input error.
        # The detail is LOGGED, never returned: it can carry SDK internals.
        log.exception("screen: unexpected failure for application %s", body.application_id)
        raise HTTPException(
            503,
            "Screening unavailable due to an unexpected error. Try again, or "
            "check the server logs for detail.",
        ) from exc

    db.commit()
    db.refresh(row)
    return _screen_out(row)


# Applications on a job that still have no current screen, after a cursor.
# The CURSOR is what makes a batch terminate: a candidate whose CV cannot be
# read never gets a screen row, so a "next unscreened" query alone would hand
# back the same person for ever.
_UNSCREENED_AFTER_SQL = text(
    """
    SELECT a.id
    FROM applications a
    WHERE a.job_id = :job_id
      AND a.id > :after
      AND NOT EXISTS (
          SELECT 1 FROM coco.cv_screens s
          WHERE s.application_id = a.id AND s.is_current
      )
    ORDER BY a.id
    LIMIT :limit
    """
)

_UNSCREENED_REMAINING_SQL = text(
    """
    SELECT COUNT(*) FROM applications a
    WHERE a.job_id = :job_id
      AND a.id > :after
      AND NOT EXISTS (
          SELECT 1 FROM coco.cv_screens s
          WHERE s.application_id = a.id AND s.is_current
      )
    """
)


@router.post("/screen-batch", response_model=CVScreenBatchOut)
def screen_batch(
    body: CVScreenBatchRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """Screen the next few unscreened candidates on a job.

    Deliberately a SMALL slice per request rather than a whole position. Each CV
    is a model call of roughly 15 seconds, so a 74-candidate position is about
    20 minutes and a 367-candidate one is over an hour, far past any HTTP
    timeout. The caller loops on `remaining`, which gives real progress instead
    of a request that appears to hang and then dies.

    Every candidate it could not screen is RETURNED, not silently dropped: a CV
    that would not open must be visible as needing a human, never absent.
    """
    job, jd, jd_sha = _job_and_jd(db, body.job_id)
    created_by = user.get("id") or ""
    after = body.after or 0

    ids = [
        r[0] for r in db.execute(
            _UNSCREENED_AFTER_SQL,
            {"job_id": body.job_id, "after": after, "limit": body.limit},
        ).all()
    ]

    screened, skipped = [], []
    for application_id in ids:
        try:
            row = _screen_and_store(
                db, application_id, job_id=body.job_id, job=job, jd=jd,
                jd_sha=jd_sha, created_by=created_by,
            )
            db.commit()
            db.refresh(row)
            screened.append(_screen_out(row))
        except _Skip as exc:
            db.rollback()
            skipped.append(CVScreenSkippedOut(
                application_id=application_id, reason=exc.reason,
            ))
        except DraftingUnavailable as exc:
            # No credential is not a per-candidate problem; stopping the whole
            # batch is the honest response.
            db.rollback()
            raise HTTPException(503, f"Screening unavailable: {exc}") from exc
        except Exception as exc:  # noqa: BLE001
            # One candidate failing must not lose the ones already done.
            db.rollback()
            log.exception("screen_batch: failed on application %s", application_id)
            skipped.append(CVScreenSkippedOut(
                application_id=application_id,
                reason=f"screening failed: {type(exc).__name__}",
            ))

    last = ids[-1] if ids else after
    remaining = db.execute(
        _UNSCREENED_REMAINING_SQL, {"job_id": body.job_id, "after": last}
    ).scalar_one()

    return CVScreenBatchOut(
        job_id=body.job_id,
        screened=screened,
        skipped=skipped,
        last_application_id=last,
        remaining=remaining,
    )
