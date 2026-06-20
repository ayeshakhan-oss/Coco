"""Pydantic response schemas for the API."""

from __future__ import annotations

import datetime as dt
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class _Base(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)


class CurrentUserOut(_Base):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    app_role: str


class UserOut(_Base):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    app_role: str
    active: bool
    last_login_at: Optional[dt.datetime] = None
    created_at: Optional[dt.datetime] = None


class UserCreate(_Base):
    email: str
    app_role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(_Base):
    app_role: Optional[str] = None
    active: Optional[bool] = None


class JobItem(_Base):
    job_pk: int
    job_code: Optional[str] = None
    title: Optional[str] = None
    job_status: Optional[str] = None
    department: Optional[str] = None


class QueueRow(_Base):
    application_id: int
    candidate_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    job_pk: Optional[int] = None
    job_code: Optional[str] = None
    job_title: Optional[str] = None
    job_status: Optional[str] = None
    status: Optional[str] = None
    values_filled: bool = False
    gwc_filled: bool = False
    values_interview_result: Optional[str] = None
    scorecard_date: Optional[dt.datetime] = None
    interviewer: Optional[str] = None
    sent_count: int = 0
    active_count: int = 0
    last_sent_at: Optional[dt.datetime] = None
    prior_platform_comms: int = 0
    bucket: str
    # Markaz <-> Gmail communication-sync dimensions (Phase 1+).
    applied_at: Optional[dt.datetime] = None
    days_waiting: Optional[int] = None
    gmail_status: str = "not_checked"
    comm_required: bool = False
    required_email_type: Optional[str] = None
    is_high_priority: bool = False
    has_evidence: bool = False
    manual_marked: bool = False
    ignored: bool = False
    display_status: Optional[str] = None


class QueueStats(_Base):
    needs_comms: int
    high_priority: int = 0
    in_progress: int
    sent: int
    needs_review: int = 0
    awaiting_scorecard: int
    ignored: int = 0
    scored: int
    total: int
    total_applications: int = 0
    total_candidates: int = 0
    open_positions: int = 0


class PositionSummary(_Base):
    job_pk: int
    job_code: Optional[str] = None
    job_title: Optional[str] = None
    needs_comms: int
    high_priority: int = 0
    in_progress: int
    sent: int
    needs_review: int = 0
    awaiting_scorecard: int = 0
    scored: int
    total: int = 0
    last_gmail_sync_at: Optional[dt.datetime] = None


class ScorecardValueItem(_Base):
    name: str
    rating: str = ""
    deep_dive: str = ""
    curve_ball: str = ""
    micro_case: str = ""


class ScorecardResponse(_Base):
    application_id: int
    values: Optional[dict[str, Any]] = None  # normalized values scorecard
    gwc: Optional[dict[str, Any]] = None  # normalized gwc scorecard


class CommHistoryItem(_Base):
    sent_at: Optional[str] = None
    sent_by: Optional[str] = None
    status: Optional[str] = None
    subject: Optional[str] = None
    template_name: Optional[str] = None
    recipient_email: Optional[str] = None
    cc_emails: list[str] = []
    source: str = "markaz"


class EvalViolation(_Base):
    rule: str
    severity: str
    detail: str


class EvalResult(_Base):
    passed: bool
    word_count: int
    violations: list[EvalViolation] = []


class GenerateRequest(_Base):
    application_id: int
    email_type: str
    role_title: Optional[str] = None


class DraftUpdate(_Base):
    # Structured content edited in the section editor; the body HTML is rendered
    # from this server-side (so the locked v8 layout can't drift).
    title_line: str
    role_title: Optional[str] = None
    content: dict[str, Any]


class CommunicationOut(_Base):
    id: str
    application_id: Optional[int] = None
    candidate_id: int
    job_id: Optional[int] = None
    email_type: str
    subject: Optional[str] = None
    title_line: Optional[str] = None
    role_title: Optional[str] = None
    body_html: Optional[str] = None
    draft_content: Optional[dict[str, Any]] = None
    status: str
    mode: Optional[str] = None
    word_count: Optional[int] = None
    eval_result: Optional[dict[str, Any]] = None
    eval_passed: Optional[bool] = None
    sent_to: Optional[list[str]] = None
    message_id: Optional[str] = None
    error_detail: Optional[str] = None
    created_by: Optional[str] = None
    approved_by: Optional[str] = None
    created_at: Optional[dt.datetime] = None
    updated_at: Optional[dt.datetime] = None
    submitted_at: Optional[dt.datetime] = None
    approved_at: Optional[dt.datetime] = None
    sent_at: Optional[dt.datetime] = None


class GenerateResponse(_Base):
    communication: CommunicationOut
    eval: EvalResult
    attempts: int
    drafter_used: str


class SendRequest(_Base):
    mode: str = "pilot"  # 'pilot' | 'live'


class SendResponse(_Base):
    communication: CommunicationOut
    mode: str
    subject: str
    recipients: list[str]
    message_id: Optional[str] = None


class ApplicationDetail(_Base):
    application_id: int
    candidate_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    job_pk: Optional[int] = None
    job_code: Optional[str] = None
    job_title: Optional[str] = None
    job_status: Optional[str] = None
    status: Optional[str] = None
    stage: Optional[str] = None
    values_filled: bool = False
    gwc_filled: bool = False
    values_interview_result: Optional[str] = None
    values_interview_date: Optional[dt.datetime] = None
    values_interviewer_name: Optional[str] = None
    gwc_interview_result: Optional[str] = None
    gwc_interview_date: Optional[dt.datetime] = None
    gwc_interviewer_name: Optional[str] = None
    comm_history: list[CommHistoryItem] = []
    # Markaz <-> Gmail communication-sync dimensions + evidence (Phase 1+).
    applied_at: Optional[dt.datetime] = None
    days_waiting: Optional[int] = None
    comm_required: bool = False
    required_email_type: Optional[str] = None
    is_high_priority: bool = False
    has_evidence: bool = False
    manual_marked: bool = False
    ignored: bool = False
    display_status: Optional[str] = None
    gmail_status: str = "not_checked"
    gmail_match: Optional["GmailMatch"] = None


class GmailMatch(_Base):
    """The Gmail Sent evidence for one application (drives 'View Gmail match')."""
    gmail_status: str = "not_checked"
    match_method: Optional[str] = None
    matched_message_id: Optional[str] = None
    gmail_thread_id: Optional[str] = None
    internal_date: Optional[dt.datetime] = None
    matched_subject: Optional[str] = None
    matched_to: Optional[str] = None
    matched_snippet: Optional[str] = None
    uncertain_reason: Optional[str] = None
    marked_sent_at: Optional[dt.datetime] = None
    marked_sent_by: Optional[str] = None
    marked_sent_reason: Optional[str] = None
    ignored: bool = False
    ignored_at: Optional[dt.datetime] = None
    checked_at: Optional[dt.datetime] = None


class GmailSyncStatusOut(_Base):
    last_sync_at: Optional[dt.datetime] = None
    status: Optional[str] = None
    trigger: Optional[str] = None
    messages_scanned: Optional[int] = None
    candidates_evaluated: Optional[int] = None
    found_count: Optional[int] = None
    uncertain_count: Optional[int] = None
    none_count: Optional[int] = None
    started_at: Optional[dt.datetime] = None
    finished_at: Optional[dt.datetime] = None
    error_detail: Optional[str] = None


class MarkSentRequest(_Base):
    reason: Optional[str] = None


class IgnoreRequest(_Base):
    ignored: bool = True


class BulkMarkSentRequest(_Base):
    application_ids: list[int]
    reason: Optional[str] = None


class BulkIgnoreRequest(_Base):
    application_ids: list[int]
    ignored: bool = True


class BulkResult(_Base):
    updated: int


class TimelineItem(_Base):
    source: str  # 'markaz' | 'gmail' | 'coco'
    ts: Optional[str] = None
    subject: Optional[str] = None
    actor: Optional[str] = None
    snippet: Optional[str] = None
    link: Optional[str] = None


# Resolve the forward reference (GmailMatch is defined after ApplicationDetail).
ApplicationDetail.model_rebuild()
