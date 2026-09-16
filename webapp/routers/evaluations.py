"""Read-only endpoints over Nugget's screening results.

🔒 These tables belong to Nugget (Aymen Abid's agent). This router exposes GET
only; there is deliberately no write path. See
.claude/skills/02_candidate-evaluation/technical-screening.md.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user
from ..schemas import EvaluationDetail, EvaluationRow, EvaluationSummary, ScreenedJob
from ..services import nugget_reads

router = APIRouter(prefix="/api/evaluations", tags=["evaluations"])


@router.get("/jobs", response_model=list[ScreenedJob])
def screened_jobs(
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return nugget_reads.list_screened_jobs(db)


@router.get("/jobs/{job_id}/summary", response_model=EvaluationSummary)
def job_summary(
    job_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return nugget_reads.job_summary(db, job_id)


@router.get("/jobs/{job_id}/candidates", response_model=list[EvaluationRow])
def job_candidates(
    job_id: int,
    tier: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    if tier is not None and not nugget_reads.is_valid_tier(tier):
        raise HTTPException(400, f"Invalid tier. One of: {list(nugget_reads.TIER_ORDER)}")
    return nugget_reads.candidates_for_job(db, job_id, tier=tier, limit=limit, offset=offset)


@router.get("/applications/{application_id}", response_model=EvaluationDetail)
def application_evaluation(
    application_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    row = nugget_reads.evaluation_for_application(db, application_id)
    if not row:
        raise HTTPException(404, "No current screening evaluation for this application")
    return row
