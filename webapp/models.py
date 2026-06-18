"""App-owned ORM models.

Only TWO tables are owned by this app: `app_users` (SSO identity + RBAC) and
`communications` (the draft -> review -> approve -> send lifecycle, and the
durable record of what was sent — replacing log-file parsing).

The existing Talent-Acquisition tables (candidates, applications, jobs, users)
are READ-ONLY from this app and are NOT mapped here; we query them with
parameterized SQL in the read services.
"""

from __future__ import annotations

import datetime as dt
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base

EMAIL_TYPES = ("cv_rejection", "values_feedback", "warm_bench", "gwc_rejection")
COMM_STATUSES = ("draft", "in_review", "approved", "sent", "failed")
COMM_MODES = ("pilot", "live")
APP_ROLES = ("drafter", "approver")

# Gmail-evidence enums (used by the Markaz <-> Gmail sync feature).
GMAIL_STATUSES = ("not_checked", "none", "found", "uncertain")
MATCH_METHODS = ("message_id", "recipient_window", "none")
SYNC_TRIGGERS = ("scheduled", "manual")
SYNC_STATUSES = ("running", "ok", "partial", "failed")


def _appuser_id() -> str:
    return "appuser-" + uuid4().hex


def _comm_id() -> str:
    return "comm-" + uuid4().hex


def _evidence_id() -> str:
    return "ev-" + uuid4().hex


def _syncrun_id() -> str:
    return "sync-" + uuid4().hex


class AppUser(Base):
    __tablename__ = "app_users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_appuser_id)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    google_sub: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    app_role: Mapped[str] = mapped_column(
        String, nullable=False, default="viewer", server_default="viewer"
    )
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    last_login_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "email LIKE '%@taleemabad.com'", name="ck_app_users_email_domain"
        ),
        CheckConstraint(
            "app_role IN ('viewer','editor','approver','super_admin')",
            name="ck_app_users_role",
        ),
    )


class Communication(Base):
    __tablename__ = "communications"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_comm_id)

    # Links into the read-only TA tables (no DB-level FK to those, by design).
    application_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    candidate_id: Mapped[int] = mapped_column(Integer, nullable=False)
    job_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    email_type: Mapped[str] = mapped_column(String, nullable=False)

    # Content. body_html is the INNER body passed to wrap() — stored so we can
    # deterministically re-wrap + re-evaluate. rendered_html is the full sent
    # document, archived only when status='sent'. subject is always the CLEAN
    # subject; the [PILOT - name] prefix is applied at send time, never stored.
    subject: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    title_line: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    role_title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    body_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rendered_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Structured content (title_line/greeting/opening/sections/ps) so the editor
    # can edit section-by-section; body_html is rendered from this.
    draft_content: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    status: Mapped[str] = mapped_column(
        String, nullable=False, default="draft", server_default="draft"
    )
    mode: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    word_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    eval_result: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    eval_passed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    sent_to: Mapped[Optional[list[str]]] = mapped_column(ARRAY(Text), nullable=True)
    message_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    error_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_by: Mapped[Optional[str]] = mapped_column(
        ForeignKey("app_users.id"), nullable=True
    )
    approved_by: Mapped[Optional[str]] = mapped_column(
        ForeignKey("app_users.id"), nullable=True
    )

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    submitted_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    approved_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    sent_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "email_type IN ('cv_rejection','values_feedback','warm_bench','gwc_rejection')",
            name="ck_comm_email_type",
        ),
        CheckConstraint(
            "status IN ('draft','in_review','approved','sent','failed')",
            name="ck_comm_status",
        ),
        CheckConstraint(
            "mode IS NULL OR mode IN ('pilot','live')", name="ck_comm_mode"
        ),
        Index("ix_comm_candidate_id", "candidate_id"),
        Index("ix_comm_application_id", "application_id"),
        Index("ix_comm_job_id", "job_id"),
        Index("ix_comm_status", "status"),
        Index("ix_comm_email_type", "email_type"),
        Index("ix_comm_app_type", "application_id", "email_type"),
        # Fast "has a sent comm of this type?" lookups for the queue buckets.
        Index(
            "ix_comm_sent_app_type",
            "application_id",
            "email_type",
            postgresql_where=text("status = 'sent'"),
        ),
    )


class CommEvidence(Base):
    """Per-application communication evidence + manual overrides.

    One row per application. Holds the result of cross-referencing Gmail's Sent
    mailbox (read-only), plus human overrides (manual "mark sent", "ignore").
    The send pipeline NEVER writes here and this module never imports it — the
    Gmail feature is strictly read-only and isolated from `safe_send`.

    Completion (display "Sent") is only ever reached via an app-sent
    `communications` row, a Gmail `found` match, or a manual override here —
    never from a Markaz status alone.
    """

    __tablename__ = "comm_evidence"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_evidence_id)

    application_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    candidate_id: Mapped[int] = mapped_column(Integer, nullable=False)
    job_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Gmail evidence (read-only). Snippet/metadata only — never the full body.
    gmail_status: Mapped[str] = mapped_column(
        String, nullable=False, default="not_checked", server_default="not_checked"
    )
    match_method: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    matched_message_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    gmail_thread_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    internal_date: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    matched_subject: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    matched_to: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    matched_snippet: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    uncertain_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Manual override: a human attests this candidate was communicated with
    # outside Coco. This is NOT a send and never touches the eval gate.
    marked_sent_by: Mapped[Optional[str]] = mapped_column(
        ForeignKey("app_users.id"), nullable=True
    )
    marked_sent_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    marked_sent_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Reversible "ignore" for shortlisted-but-never-scheduled candidates.
    ignored: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    ignored_by: Mapped[Optional[str]] = mapped_column(
        ForeignKey("app_users.id"), nullable=True
    )
    ignored_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    checked_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "gmail_status IN ('not_checked','none','found','uncertain')",
            name="ck_evidence_gmail_status",
        ),
        CheckConstraint(
            "match_method IS NULL OR match_method IN ('message_id','recipient_window','none')",
            name="ck_evidence_match_method",
        ),
        Index("ix_evidence_application_id", "application_id", unique=True),
        Index("ix_evidence_candidate_id", "candidate_id"),
        Index("ix_evidence_gmail_status", "gmail_status"),
        Index("ix_evidence_ignored", "ignored", postgresql_where=text("ignored")),
    )


class GmailSyncRun(Base):
    """One row per Gmail sync run — the durable audit + 'last synced' source.

    `logs/read_audit.log` is ephemeral on Railway; this table is the source of
    truth for sync history and the dashboard's "last synced" indicator.
    """

    __tablename__ = "gmail_sync_runs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_syncrun_id)

    trigger: Mapped[str] = mapped_column(String, nullable=False)
    triggered_by: Mapped[Optional[str]] = mapped_column(
        ForeignKey("app_users.id"), nullable=True
    )
    full_resync: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    status: Mapped[str] = mapped_column(
        String, nullable=False, default="running", server_default="running"
    )
    query: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    messages_scanned: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    candidates_evaluated: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    found_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    uncertain_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    none_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    watermark_before: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    watermark_after: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    finished_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "trigger IN ('scheduled','manual')", name="ck_syncrun_trigger"
        ),
        CheckConstraint(
            "status IN ('running','ok','partial','failed')", name="ck_syncrun_status"
        ),
        Index("ix_syncrun_status", "status"),
        Index("ix_syncrun_started_at", "started_at"),
    )
