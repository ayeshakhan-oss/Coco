"""CRUD for the app-owned communications table (draft lifecycle)."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Communication


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def create_draft(
    db: Session,
    *,
    application_id: Optional[int],
    candidate_id: int,
    job_id: Optional[int],
    email_type: str,
    title_line: str,
    role_title: str,
    body_html: str,
    draft_content: Optional[dict],
    word_count: int,
    eval_result: dict,
    eval_passed: bool,
    created_by: Optional[str],
) -> Communication:
    comm = Communication(
        application_id=application_id,
        candidate_id=candidate_id,
        job_id=job_id,
        email_type=email_type,
        subject=title_line,
        title_line=title_line,
        role_title=role_title,
        body_html=body_html,
        draft_content=draft_content,
        status="draft",
        word_count=word_count,
        eval_result=eval_result,
        eval_passed=eval_passed,
        created_by=created_by,
    )
    db.add(comm)
    db.commit()
    db.refresh(comm)
    return comm


def get(db: Session, comm_id: str) -> Optional[Communication]:
    return db.get(Communication, comm_id)


def update_content(
    db: Session,
    comm: Communication,
    *,
    body_html: str,
    draft_content: Optional[dict],
    title_line: str,
    role_title: Optional[str],
    word_count: int,
    eval_result: dict,
    eval_passed: bool,
) -> Communication:
    comm.body_html = body_html
    if draft_content is not None:
        comm.draft_content = draft_content
    comm.title_line = title_line
    comm.subject = title_line
    if role_title is not None:
        comm.role_title = role_title
    comm.word_count = word_count
    comm.eval_result = eval_result
    comm.eval_passed = eval_passed
    comm.updated_at = _utcnow()
    db.commit()
    db.refresh(comm)
    return comm


def submit(db: Session, comm: Communication) -> Communication:
    comm.status = "in_review"
    comm.submitted_at = _utcnow()
    comm.updated_at = _utcnow()
    db.commit()
    db.refresh(comm)
    return comm


def approve(db: Session, comm: Communication, approver_id: Optional[str]) -> Communication:
    comm.status = "approved"
    comm.approved_by = approver_id
    comm.approved_at = _utcnow()
    comm.updated_at = _utcnow()
    db.commit()
    db.refresh(comm)
    return comm


def request_changes(db: Session, comm: Communication) -> Communication:
    comm.status = "draft"
    comm.updated_at = _utcnow()
    db.commit()
    db.refresh(comm)
    return comm


def mark_sent(
    db: Session,
    comm: Communication,
    *,
    sent_to: list[str],
    message_id: str,
    rendered_html: str,
    mode: str = "live",
) -> Communication:
    comm.status = "sent"
    comm.mode = mode
    comm.sent_to = sent_to
    comm.message_id = message_id
    comm.rendered_html = rendered_html
    comm.sent_at = _utcnow()
    comm.updated_at = _utcnow()
    db.commit()
    db.refresh(comm)
    return comm


def mark_failed(db: Session, comm: Communication, error: str) -> Communication:
    comm.status = "failed"
    comm.error_detail = error[:2000]
    comm.updated_at = _utcnow()
    db.commit()
    db.refresh(comm)
    return comm


def list_communications(
    db: Session,
    *,
    status: Optional[str] = None,
    candidate_id: Optional[int] = None,
    created_by: Optional[str] = None,
    limit: int = 100,
) -> list[Communication]:
    stmt = select(Communication)
    if status:
        stmt = stmt.where(Communication.status == status)
    if candidate_id is not None:
        stmt = stmt.where(Communication.candidate_id == candidate_id)
    if created_by:
        stmt = stmt.where(Communication.created_by == created_by)
    stmt = stmt.order_by(Communication.updated_at.desc()).limit(limit)
    return list(db.execute(stmt).scalars().all())
