"""Read endpoints that drive the dashboard: the candidate queue (by bucket),
queue stats, application detail, scorecards, and the job filter list."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user
from ..schemas import (
    ApplicationDetail,
    JobItem,
    PositionSummary,
    QueueRow,
    QueueStats,
    ScorecardResponse,
)
from ..services import reads
from ..services.scorecard import (
    normalize_comm_history,
    normalize_gwc_scorecard,
    normalize_values_scorecard,
)

router = APIRouter(prefix="/api", tags=["candidates"])

_BUCKETS = {
    "all",
    "relevant",
    "scored",
    "needs_comms",
    "high_priority",
    "already_sent",
    "needs_review",
    "in_progress",
    "sent",
    "shortlisted",
    "interview_scheduled",
    "case_study",
    "awaiting_scorecard",
    "ignored",
}


@router.get("/candidates", response_model=list[QueueRow])
def list_candidates(
    status_filter: str = Query("relevant", alias="status"),
    job_pk: Optional[int] = Query(None, alias="job"),
    q: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    if status_filter not in _BUCKETS:
        raise HTTPException(400, f"Invalid status filter. One of: {sorted(_BUCKETS)}")
    return reads.list_queue(
        db, bucket=status_filter, job_pk=job_pk, q=q, limit=limit, offset=offset
    )


@router.get("/candidates/stats", response_model=QueueStats)
def candidate_stats(
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return reads.queue_stats(db)


@router.get("/positions", response_model=list[PositionSummary])
def positions(
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return reads.positions_summary(db)


@router.get("/candidates/{application_id}", response_model=ApplicationDetail)
def candidate_detail(
    application_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    row = reads.get_application(db, application_id)
    if not row:
        raise HTTPException(404, "Application not found")
    row["comm_history"] = normalize_comm_history(row.pop("communication_history", None))
    return row


@router.get("/candidates/{application_id}/scorecard", response_model=ScorecardResponse)
def candidate_scorecard(
    application_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    raw = reads.get_scorecards_raw(db, application_id)
    if raw is None:
        raise HTTPException(404, "Application not found")
    return {
        "application_id": application_id,
        "values": normalize_values_scorecard(raw.get("values_scorecard")),
        "gwc": normalize_gwc_scorecard(raw.get("gwc_scorecard")),
    }


@router.get("/jobs", response_model=list[JobItem])
def list_jobs(
    # All positions, not just active ones. Only CPD Coach is 'Active', so this
    # picker (Case Study Scoring's benchmark job selector) showed one job.
    active_only: bool = Query(False),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return reads.list_jobs(db, active_only=active_only)


# The CV itself, so a candidate's name can be a link to it.
#
# The decision-brief SOP requires EVERY candidate name to be hyperlinked to
# their CV, and calls it non-negotiable. It assumes the CV has been uploaded to
# Google Drive by hand first. Serving it straight out of Markaz removes that
# step entirely: the bytes are already in `candidates.resume_data`, and the link
# is behind the same Google sign-in as the rest of the app, so a brief forwarded
# to a hiring manager shows them the CV and shows a stranger nothing.
_CV_SQL = text(
    """
    SELECT c.resume_data, c.resume_mime_type, c.resume_file_name,
           c.first_name, c.last_name
    FROM applications a
    JOIN candidates c ON c.id = a.candidate_id
    WHERE a.id = :application_id
    """
)


@router.get("/candidates/{application_id}/cv")
def candidate_cv(
    application_id: int,
    download: bool = Query(False, description="Force a download instead of inline"),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Stream this candidate's CV as it was uploaded.

    Markaz stores it base64-encoded in a TEXT column. The stored
    `resume_mime_type` is unreliable -- a .docx labelled application/pdf is
    common -- so the real file signature decides what is sent, the same sniffing
    `cv_text.extract` does before choosing a parser.
    """
    import base64
    import binascii
    import re as _re

    from fastapi.responses import Response

    row = db.execute(_CV_SQL, {"application_id": application_id}).mappings().first()
    if not row:
        raise HTTPException(404, "Application not found")
    if not row["resume_data"]:
        raise HTTPException(404, "No CV on file for this candidate")

    try:
        raw = base64.b64decode(_re.sub(r"\s+", "", row["resume_data"]), validate=False)
    except (binascii.Error, ValueError) as exc:
        raise HTTPException(422, f"The stored CV is not valid base64: {exc}") from exc

    # Sniff, never trust the recorded mime type.
    if raw[:5] == b"%PDF-":
        media, ext = "application/pdf", "pdf"
    elif raw[:2] == b"PK":
        media, ext = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "docx",
        )
    else:
        media, ext = "application/octet-stream", "bin"

    name = " ".join(p for p in (row["first_name"], row["last_name"]) if p).strip()
    safe = _re.sub(r"[^A-Za-z0-9 _-]", "", name) or f"application-{application_id}"
    disposition = "attachment" if download else "inline"
    return Response(
        content=raw,
        media_type=media,
        headers={
            "Content-Disposition": f'{disposition}; filename="CV - {safe}.{ext}"',
            # A CV is personal data. Never let a shared cache hold it.
            "Cache-Control": "private, no-store",
        },
    )
