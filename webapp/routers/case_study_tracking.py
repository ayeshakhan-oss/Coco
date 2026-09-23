"""Case-study tracking: who submitted, who has not, and what the pool shares.

`webapp/services/case_study_tracking.py` holds the reconciliation rules, the
content-dump flags and the cohort mirror check. `webapp/services/submissions.py`
does the retrieval (mailbox, Drive links, Markaz's file API and its documented
401 wall). This router is the only code that persists a probe.

This is TRACKING, not scoring. `routers/case_studies.py` scores a submission
against a QA'd benchmark and nothing here touches a score.

🔴 THE THING THIS MODULE EXISTS TO PREVENT. Markaz records no case-study SEND
   anywhere: there is no `case_study_sent_at` column, and
   `public.candidate_communications` holds 16 typed rows in the whole table
   while reporting 0 sends against 4 to 17 submissions per job (measured
   2026-09-22 across all 4,509 applications). A tracker built on those fields
   would report "0 sent, 17 submitted" and a reader would conclude the pool had
   never been contacted. So:

     * The submitted side IS trustworthy -- `case_study_status` agrees with the
       evidence columns on all 116 rows that carry it, 0 disagreements -- and is
       read live on every request, straight from `applications`.
     * The sent side comes only from Ayesha's mailbox, costs a network round
       trip per candidate, and is therefore probed on demand and stored.
     * A candidate with no submission and no findable send is
       `no_record_of_a_send`. There is no `not_sent` anywhere in this module.

Rules enforced here, verbatim rule -> mechanism:

  1. `require_editor` gates probing (it reads a mailbox and writes a row).
     Reading the tracker needs only a signed-in user.
  2. A probe REPLACES the previous one for that application: it is a
     measurement, not a judgement. `probed_at` says how fresh it is.
  3. An unreadable submission is recorded as `corpus_error` and never as a
     zero-length corpus, mirroring `cv_text` and `submissions.corpus_for`.
  4. The mirror check runs only over submissions already probed, and says so in
     its own response rather than silently comparing three of eighty.
"""

from __future__ import annotations

import datetime as dt
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user, require_editor
from ..models import CaseStudyProbe
from ..schemas import (
    CaseStudyMirrorPairOut,
    CaseStudyProbeOut,
    CaseStudyProbeRequest,
    CaseStudyTrackingRowOut,
    CaseStudyTrackingSummaryOut,
)
from ..services import case_study_tracking as tracking
from ..services import reads
from ..services.submissions import SubmissionUnreadable, corpus_for

log = logging.getLogger("webapp.routers.case_study_tracking")

router = APIRouter(prefix="/api/case-study-tracking", tags=["case-study-tracking"])

_JOB_SQL = text("SELECT id, title FROM jobs WHERE id = :job_id")

_APPLICATIONS_SQL = text(
    """
    SELECT a.id                       AS application_id,
           a.case_study_submission    AS case_study_submission,
           a.case_study_word_file     AS case_study_word_file,
           a.case_study_excel_file    AS case_study_excel_file,
           a.case_study_video_file    AS case_study_video_file,
           a.case_study_submitted_at  AS case_study_submitted_at,
           a.case_study_status        AS case_study_status,
           c.first_name               AS first_name,
           c.last_name                AS last_name,
           c.email                    AS email
    FROM applications a
    JOIN candidates c ON c.id = a.candidate_id
    WHERE a.job_id = :job_id
    -- applications has applied_at, NOT created_at.
    ORDER BY a.applied_at DESC NULLS LAST, a.id DESC
    """
)

_PROBES_FOR_JOB_SQL = text("SELECT * FROM coco.case_study_probes WHERE job_id = :job_id")


def _name(row) -> str:
    return " ".join(p for p in (row["first_name"], row["last_name"]) if p).strip() or (
        "(no name on record)"
    )


def _probe_out(row) -> CaseStudyProbeOut:
    get = (lambda k: getattr(row, k)) if isinstance(row, CaseStudyProbe) else row.__getitem__
    return CaseStudyProbeOut(
        id=get("id"),
        application_id=get("application_id"),
        job_id=get("job_id"),
        channels=get("channels") or [],
        send_found=get("send_found"),
        send_subject=get("send_subject"),
        send_at=get("send_at"),
        status=get("status"),
        corpus_chars=get("corpus_chars"),
        sources=get("sources") or [],
        corpus_error=get("corpus_error"),
        flags=get("flags") or [],
        completeness=get("completeness") or {},
        probed_by=get("probed_by"),
        probed_at=get("probed_at"),
    )


def _rows_and_probes(db: Session, job_id: int):
    rows = db.execute(_APPLICATIONS_SQL, {"job_id": job_id}).mappings().all()
    probes = {
        p["application_id"]: p
        for p in db.execute(_PROBES_FOR_JOB_SQL, {"job_id": job_id}).mappings()
    }
    return rows, probes


def _status_for(row, probe) -> str:
    """Markaz's columns are read live; the send comes from the probe if there
    is one. `send_found=None` when unprobed, which the service treats as "no
    record" rather than as "no send"."""
    return tracking.submission_status(
        dict(row), send_found=probe["send_found"] if probe else None
    )


@router.get("/jobs/{job_id}", response_model=list[CaseStudyTrackingRowOut])
def tracking_rows(
    job_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    rows, probes = _rows_and_probes(db, job_id)
    out = []
    for r in rows:
        probe = probes.get(r["application_id"])
        out.append(
            CaseStudyTrackingRowOut(
                application_id=r["application_id"],
                candidate_name=_name(r),
                email=r["email"],
                channels=tracking.channels_present(dict(r)),
                submitted_at=r["case_study_submitted_at"],
                markaz_status=r["case_study_status"],
                status=_status_for(r, probe),
                probe=_probe_out(probe) if probe else None,
            )
        )
    return out


@router.get("/jobs/{job_id}/summary", response_model=CaseStudyTrackingSummaryOut)
def summary(
    job_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    job = db.execute(_JOB_SQL, {"job_id": job_id}).mappings().first()
    if not job:
        raise HTTPException(404, f"Job {job_id} not found")

    rows, probes = _rows_and_probes(db, job_id)
    counts = tracking.summarise(
        _status_for(r, probes.get(r["application_id"])) for r in rows
    )
    return CaseStudyTrackingSummaryOut(
        job_id=job_id, title=job["title"], probed=len(probes), **counts
    )


@router.get("/jobs/{job_id}/mirrors", response_model=list[CaseStudyMirrorPairOut])
def mirrors(
    job_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Submissions on this job sharing long verbatim runs.

    Runs only over submissions already probed. A pair is evidence for a person
    to look at, never a verdict: two candidates quoting the same paragraph of
    the assignment are indistinguishable from two sharing an assistant.
    """
    rows, probes = _rows_and_probes(db, job_id)
    names = {r["application_id"]: _name(r) for r in rows}
    corpora = {
        app_id: p["corpus_text"]
        for app_id, p in probes.items()
        if p["corpus_text"]
    }
    return [
        CaseStudyMirrorPairOut(
            **pair,
            candidate_names=[names.get(i, str(i)) for i in pair["application_ids"]],
        )
        for pair in tracking.mirror_pairs(corpora)
    ]


@router.get("/probes", response_model=Optional[CaseStudyProbeOut])
def get_probe(
    application_id: int = Query(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    row = db.execute(
        text("SELECT * FROM coco.case_study_probes WHERE application_id = :a"),
        {"a": application_id},
    ).mappings().first()
    return _probe_out(row) if row else None


@router.post("/probe", response_model=CaseStudyProbeOut)
def probe(
    body: CaseStudyProbeRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """Go and look for one candidate's case study: mailbox, Drive links, Markaz.

    Slow by nature (three network round trips), which is why it is one
    candidate at a time and the result is stored.
    """
    app_row = reads.get_application(db, body.application_id)
    if not app_row:
        raise HTTPException(404, "Application not found")
    job_id = app_row.get("job_pk")
    if job_id is None:
        raise HTTPException(422, f"Application {body.application_id} has no job on record")

    markaz = db.execute(
        text(
            "SELECT a.case_study_submission, a.case_study_word_file, "
            "a.case_study_excel_file, a.case_study_video_file, c.email "
            "FROM applications a JOIN candidates c ON c.id = a.candidate_id "
            "WHERE a.id = :a"
        ),
        {"a": body.application_id},
    ).mappings().first()
    if not markaz:
        raise HTTPException(404, "Application not found")

    channels = tracking.channels_present(dict(markaz))

    # --- The send. Only the mailbox has it. A failure here is NOT fatal: it
    # leaves send_found False, which the status vocabulary already reads as
    # "no record", not as "not sent".
    send = None
    try:
        send = tracking.find_send(markaz["email"])
    except Exception:  # noqa: BLE001 - a mailbox that will not open is not a verdict
        log.exception(
            "probe: mailbox lookup failed for application %s", body.application_id
        )

    # --- The submission itself, only if Markaz says there is one to read.
    corpus_text, corpus_chars, sources, corpus_error = None, 0, [], None
    if channels:
        try:
            corpus = corpus_for(body.application_id, db=db)
            corpus_text = corpus["text"]
            corpus_chars = corpus["chars"]
            sources = corpus["sources"]
        except SubmissionUnreadable as exc:
            # Recorded, never silently treated as an empty submission.
            corpus_error = str(exc)
        except Exception as exc:  # noqa: BLE001
            log.exception(
                "probe: unexpected retrieval failure for application %s",
                body.application_id,
            )
            corpus_error = f"retrieval failed: {type(exc).__name__}"

    flags = tracking.content_dump_flags(corpus_text) if corpus_text else []
    completeness = tracking.completeness(corpus_text or "", body.required_parts)
    status = tracking.submission_status(dict(markaz), send_found=bool(send))

    values = {
        "job_id": job_id,
        "channels": channels,
        "send_found": bool(send),
        "send_subject": send["subject"] if send else None,
        "send_at": send["date"] if send else None,
        "status": status,
        "corpus_chars": corpus_chars,
        "sources": sources,
        "corpus_error": corpus_error,
        "corpus_text": corpus_text,
        "flags": flags,
        "completeness": completeness,
        "probed_by": user.get("id") or "",
    }

    # Set explicitly rather than left to the column's server default: the
    # default only fires on INSERT, so an UPDATE would keep the ORIGINAL
    # probe's timestamp and the row would claim to be fresher than it is --
    # which is the one thing a reader relies on this column for.
    values["probed_at"] = dt.datetime.now(dt.timezone.utc)

    existing = (
        db.query(CaseStudyProbe)
        .filter(CaseStudyProbe.application_id == body.application_id)
        .one_or_none()
    )
    if existing is None:
        row = CaseStudyProbe(application_id=body.application_id, **values)
        db.add(row)
    else:
        # A probe REPLACES the previous one: it is a measurement, not a
        # judgement, so there is no history to retire (unlike CVScreen, where
        # a superseded score must stay visible).
        for key, value in values.items():
            setattr(existing, key, value)
        row = existing
    db.commit()
    db.refresh(row)
    return _probe_out(row)
