"""Read endpoints that drive the dashboard: the candidate queue (by bucket),
queue stats, application detail, scorecards, and the job filter list."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
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
    "awaiting_scorecard",
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
    active_only: bool = Query(True),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return reads.list_jobs(db, active_only=active_only)
