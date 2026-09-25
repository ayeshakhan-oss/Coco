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
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
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

# Values-scorecard draft enum (see ValuesScorecardDraft below).
VALUES_DRAFT_STATUSES = ("draft", "submitted")

# Eval-benchmark status enum (see EvalBenchmark below). Rule 0 of the case-study
# rubric: the benchmark must be written and QA'd before any submission is read.
EVAL_BENCHMARK_STATUSES = ("draft", "approved", "retired")

# Case-study evaluation band enum (see CaseStudyEvaluation below) -- matches
# webapp.services.case_study_scoring.band()'s return values exactly.
CASE_STUDY_EVALUATION_BANDS = ("strong_yes", "yes", "borderline", "no", "disqualified")

# Coco's own CV-screening tiers (Skill 02, cv-screening.md). Deliberately NOT
# Nugget's P1-P4: that is a separate skill with a separate rubric.
CV_SCREEN_TIERS = ("shortlist", "maybe", "no_hire")

# Imported from the service rather than restated, so the CHECK constraint and
# the reconciliation logic cannot drift. There is deliberately no 'not_sent':
# Markaz records no case-study send, so we can never assert one did not happen.
from .services.case_study_tracking import STATUSES as CASE_STUDY_PROBE_STATUSES  # noqa: E402
from .services.kcd_evaluation import VERDICTS as KCD_VERDICTS  # noqa: E402
from .services.sourcing import OUTREACH_STATES, VERIFICATION_STATES  # noqa: E402


def _appuser_id() -> str:
    return "appuser-" + uuid4().hex


def _comm_id() -> str:
    return "comm-" + uuid4().hex


def _evidence_id() -> str:
    return "ev-" + uuid4().hex


def _syncrun_id() -> str:
    return "sync-" + uuid4().hex


def _values_draft_id() -> str:
    return "vsd-" + uuid4().hex


def _benchmark_id() -> str:
    return "benchmark-" + uuid4().hex


def _evaluation_id() -> str:
    return "cse-" + uuid4().hex


def _cv_screen_id() -> str:
    return "cvs-" + uuid4().hex


def _cv_screen_skip_id() -> str:
    return "cvk-" + uuid4().hex


def _case_study_probe_id() -> str:
    return "csp-" + uuid4().hex


def _kcd_evaluation_id() -> str:
    return "kcd-" + uuid4().hex


def _sourced_candidate_id() -> str:
    return "src-" + uuid4().hex


def _invite_link_id() -> str:
    return "ilnk-" + uuid4().hex


def _invite_send_id() -> str:
    return "isnd-" + uuid4().hex


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
        # Live in a dedicated `coco` schema so Markaz's Replit per-deploy schema
        # push (which prunes unknown `public` tables) can't drop them. See
        # docs/RAILWAY_DEPLOYMENT_LESSONS.md + the 2026-06-30 root-cause memo.
        {"schema": "coco"},
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
        {"schema": "coco"},  # see CommEvidence — protected from Markaz's schema push
    )


class ValuesScorecardDraft(Base):
    """A values-interview scorecard DRAFT — reviewed by a human before it is
    ever written to Markaz. `webapp/services/values_scoring.py` holds the pure
    scoring rules and the Markaz payload shape; this table is where a scored
    draft lives between "the model scored it" and "a human approved + submitted
    it", plus the durable record of what was actually submitted.

    We deliberately store only a SHA-256 of the interview transcript, not the
    transcript itself: the transcript is interview content about a named
    person and does not need a second home once it has been scored. The hash
    is enough to tell whether a re-score used the same input.
    """

    __tablename__ = "values_scorecard_drafts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_values_draft_id)

    application_id: Mapped[int] = mapped_column(Integer, nullable=False)
    candidate_name: Mapped[str] = mapped_column(Text, nullable=False)
    host: Mapped[str] = mapped_column(Text, nullable=False)

    # The actual interview date, captured in the UI -- NEVER the date the
    # scorecard happens to be submitted. Nullable: still valid to submit
    # same-day, in which case submit() falls back to today (visibly, in the
    # UI, not silently). See migration 0008.
    interview_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    transcript_sha256: Mapped[str] = mapped_column(Text, nullable=False)

    # Column is named "values" to match the Markaz payload key
    # (build_markaz_payload's "values" list of per-value ratings). Mapped to a
    # differently-named Python attribute: "values" is a builtin dict method
    # name and shadows SQLAlchemy's (deprecated) Query.values(), so we keep it
    # out of the attribute namespace even though a standalone declarative
    # smoke test showed no actual collision on this Base.
    values_json: Mapped[dict] = mapped_column("values", JSONB, nullable=False)

    final_comments: Mapped[str] = mapped_column(Text, nullable=False)
    proceed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # The Get/Want/Capacity scorecard, when this draft is part of a warm-bench
    # evaluation that also carries a GWC interview. Absent for a values-only pass.
    gwc: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    status: Mapped[str] = mapped_column(
        Text, nullable=False, default="draft", server_default="draft"
    )

    # Column is named "model" to record which model scored the draft. Mapped to
    # a differently-named Python attribute for the same reason as "values"
    # above: "model" collides with Pydantic v2's `model_`-prefixed protected
    # namespace on any schema that later wraps this row (e.g. `model_config`,
    # `model_validate`), even though it is not reserved on the SQLAlchemy side.
    model_name: Mapped[str] = mapped_column("model", Text, nullable=False)

    created_by: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    approved_by: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    approved_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    submitted_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # The exact payload handed to Markaz at submit time (see
    # build_markaz_payload), kept for audit even though it is reconstructable
    # from the other columns.
    markaz_payload: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # The PRIOR `applications.values_scorecard` value, when submit() was
    # called with overwrite=True against an application that already had a
    # human-written scorecard. NULL on every normal (first-time) submit.
    # Never let an overwrite destroy the only copy of what it replaced.
    replaced_payload: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "status IN ('draft','submitted')", name="ck_values_draft_status"
        ),
        Index("ix_values_draft_application_id", "application_id"),
        # Live in a dedicated `coco` schema so Markaz's Replit per-deploy schema
        # push (which prunes unknown `public` tables) can't drop them. See
        # docs/RAILWAY_DEPLOYMENT_LESSONS.md + the 2026-06-30 root-cause memo.
        {"schema": "coco"},
    )


class EvalBenchmark(Base):
    """The answer key a case-study run is scored against, written and QA'd
    BEFORE any submission is opened.

    Rule 0 of the case-study rubric: scoring calibrates to whoever is read
    first, so reading a submission before the benchmark exists (or before it
    has been QA'd) anchors the whole pool. `qa_approved_at` / `qa_approved_by`
    make that discipline mechanical: a scoring run can require this row to be
    `status = 'approved'` with both fields set before it will start.

    The benchmark carries NO candidate names or responses -- it calibrates to
    the case, not the cohort, or it stops being reusable for the next round
    (CLAUDE.md Rule 17).
    """

    __tablename__ = "eval_benchmarks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_benchmark_id)

    job_id: Mapped[int] = mapped_column(Integer, nullable=False)
    kind: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    # Where the benchmark's source material lives (e.g. a Drive doc or a repo
    # path), for provenance. Not required: a benchmark can be authored directly.
    source_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_by: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # The QA gate. Both stay NULL until a human other than the author has read
    # the benchmark and approved it -- that is what "approved" in status means.
    qa_approved_by: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    qa_approved_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    status: Mapped[str] = mapped_column(
        Text, nullable=False, default="draft", server_default="draft"
    )

    __table_args__ = (
        CheckConstraint(
            "status IN (" + ",".join(f"'{s}'" for s in EVAL_BENCHMARK_STATUSES) + ")",
            name="ck_eval_benchmark_status",
        ),
        # The plan's own wording for Rule 0 is "a benchmark row with
        # qa_approved_at set" -- not just status='approved'. Without this,
        # an approved-but-null-qa_approved_at row was structurally possible
        # even though approve_benchmark() never actually writes one; the
        # scoring gate's SQL (_APPROVED_BENCHMARK_FOR_JOB_SQL) now also
        # filters on qa_approved_at IS NOT NULL, so the two cannot diverge.
        # Added in migration 0011 (this table predates it, from 0009).
        CheckConstraint(
            "status <> 'approved' OR qa_approved_at IS NOT NULL",
            name="ck_eval_benchmark_approved_has_qa_approved_at",
        ),
        Index("ix_eval_benchmark_job_id", "job_id"),
        # Same reasoning as ValuesScorecardDraft above: `coco`, never `public`.
        {"schema": "coco"},
    )


class CaseStudyEvaluation(Base):
    """A case-study submission scored against an APPROVED `EvalBenchmark`.

    Persists exactly what `case_study_scoring.score_submission` returned -- the
    six dimension scores, their evidence citations, any flags, and the total /
    band it COMPUTED (never recomputed differently by a later reader) -- plus
    which benchmark and which submission sources actually produced it, so
    "what was this scored against" is always answerable from the row alone,
    the same audit reasoning `ValuesScorecardDraft.transcript_sha256` exists
    for.

    `webapp/routers/case_studies.py` is the only code that writes this table;
    Rule 0 of the rubric (benchmark written and QA'd before any submission is
    read) is enforced there, before this row is ever created -- there is no
    row here that was not scored against a benchmark carrying
    `status = 'approved'` at the time of scoring.
    """

    __tablename__ = "case_study_evaluations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_evaluation_id)

    application_id: Mapped[int] = mapped_column(Integer, nullable=False)
    job_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # The SPECIFIC benchmark row actually used -- never just "the job's
    # benchmark", since a job can carry more than one over time (a draft, a
    # retired prior version, a later revision).
    benchmark_id: Mapped[str] = mapped_column(
        String, ForeignKey("coco.eval_benchmarks.id"), nullable=False
    )

    candidate_name: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)

    scores: Mapped[dict] = mapped_column(JSONB, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSONB, nullable=False)
    flags: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    band: Mapped[str] = mapped_column(Text, nullable=False)

    # Column is named "model" (which model actually scored this) but mapped to
    # a differently-named Python attribute -- same reason as
    # ValuesScorecardDraft.model_name: "model" collides with Pydantic v2's
    # `model_`-prefixed protected namespace on any schema that wraps this row.
    model_name: Mapped[str] = mapped_column("model", Text, nullable=False)

    # Every provenance origin submissions.corpus_for() actually read (a Gmail
    # attachment, a Drive link, ...) -- so a report's method note can say
    # exactly what was verified, mirroring corpus_for's own `sources` field.
    sources: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # Which revision of the (mutable, unversioned)
    # `.claude/skills/02_candidate-evaluation/case-study-scoring-rubric.md`
    # actually produced this score -- an anchor edit between two rounds makes
    # them scored on different scales, and without this a row cannot say
    # which one it was (see webapp/prompts/case_study_prompt.rubric_sha256).
    # Same audit reasoning as ValuesScorecardDraft.transcript_sha256.
    rubric_sha256: Mapped[str] = mapped_column(Text, nullable=False)

    # How much submission text was actually scored (len() of the exact
    # corpus string handed to the model) -- previously unanswerable from a
    # persisted row.
    corpus_chars: Mapped[int] = mapped_column(Integer, nullable=False)

    created_by: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "band IN (" + ",".join(f"'{b}'" for b in CASE_STUDY_EVALUATION_BANDS) + ")",
            name="ck_case_study_evaluation_band",
        ),
        Index("ix_case_study_evaluation_application_id", "application_id"),
        Index("ix_case_study_evaluation_job_id", "job_id"),
        # Same reasoning as ValuesScorecardDraft/EvalBenchmark: `coco`, never
        # `public` (Markaz's Replit per-deploy schema push prunes tables it
        # doesn't recognise there).
        {"schema": "coco"},
    )


class CVScreen(Base):
    """One candidate's CV screened against one job description.

    Persists exactly what `cv_screening.screen_cv` returned -- the three
    criterion scores, their citations, the strengths and gaps, the two
    experience figures kept separate, and the match / tier it COMPUTED -- plus
    which CV and which job description actually produced it, so "what was this
    screened against" is answerable from the row alone.

    🔒 This is Coco's OWN CV screening. Nugget's technical screening lives in
       `public.nugget_screening_evals`, is owned by another agent, and is read
       through services/nugget_reads.py. The two never share a table, a rubric
       or a tier vocabulary (Ayesha, 2026-09-15).

    Re-screening SUPERSEDES rather than duplicates. A second screen of the same
    application flips the previous row's `is_current` to False and records the
    new row's id in `superseded_by`, so a stale number can never be read back
    as live -- the gap CLAUDE.md Rule 25 records as costing three corrections
    on the RM round, where a superseded mean stayed live in a sheet tab, a Doc
    and a PDF after the report had moved on. Readers MUST filter on
    `is_current`, exactly as Nugget's own evals table requires.
    """

    __tablename__ = "cv_screens"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_cv_screen_id)

    application_id: Mapped[int] = mapped_column(Integer, nullable=False)
    job_id: Mapped[int] = mapped_column(Integer, nullable=False)

    candidate_name: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)

    scores: Mapped[dict] = mapped_column(JSONB, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSONB, nullable=False)
    strengths: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    gaps: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # Two figures, never one. Conflating them is the SOP's own named mistake:
    # "5 years" reads as five relevant years when it may be five total and one
    # relevant.
    total_experience_years: Mapped[float] = mapped_column(Float, nullable=False)
    relevant_experience_years: Mapped[float] = mapped_column(Float, nullable=False)
    relevant_experience_note: Mapped[str] = mapped_column(Text, nullable=False)

    match: Mapped[float] = mapped_column(Float, nullable=False)
    tier: Mapped[str] = mapped_column(Text, nullable=False)

    # Named "model" in the database but mapped to a differently-named Python
    # attribute: "model" collides with Pydantic v2's protected `model_`
    # namespace on any schema wrapping this row.
    model_name: Mapped[str] = mapped_column("model", Text, nullable=False)

    # Which revision of cv-screening.md produced this screen, and which job
    # description it was screened against. A JD is edited between rounds, and
    # without this a row cannot say which wording it was judged on.
    sop_sha256: Mapped[str] = mapped_column(Text, nullable=False)
    jd_sha256: Mapped[str] = mapped_column(Text, nullable=False)

    # How much CV text was actually read, and whether it had to be cut. The SOP
    # forbids truncating below 10,000 characters, so a reader can check.
    cv_chars: Mapped[int] = mapped_column(Integer, nullable=False)
    cv_truncated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    superseded_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_by: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "tier IN (" + ",".join(f"'{t}'" for t in CV_SCREEN_TIERS) + ")",
            name="ck_cv_screen_tier",
        ),
        CheckConstraint(
            "relevant_experience_years <= total_experience_years",
            name="ck_cv_screen_relevant_within_total",
        ),
        # A superseded row must name its replacement, and a current row must
        # not: the two fields cannot disagree about which number is live.
        CheckConstraint(
            "(is_current AND superseded_by IS NULL) OR "
            "(NOT is_current AND superseded_by IS NOT NULL)",
            name="ck_cv_screen_supersession_is_coherent",
        ),
        Index("ix_cv_screen_application_id", "application_id"),
        Index("ix_cv_screen_job_id", "job_id"),
        # `coco`, never `public`: Markaz's Replit per-deploy schema push prunes
        # tables it does not recognise there.
        {"schema": "coco"},
    )


# The three reasons a CV cannot be screened, in the order the screener meets
# them. `kind` is derived from the reason text at write time so the UI can
# group and count without parsing prose.
CV_SKIP_KINDS = ("no_cv", "unreadable", "too_short")


class CVScreenSkip(Base):
    """A candidate whose CV could not be read, kept instead of forgotten.

    🔴 THIS IS NOT A LOW SCORE, AND MUST NEVER BECOME ONE. A CV that will not
    open is a document problem needing a human; a model asked to judge an empty
    page still answers, which is why `cv_screening` REFUSES below 250 words
    rather than scoring what it could not read (CLAUDE.md Rule 32).

    It exists because refusing silently is its own defect. A refused candidate
    gets no `cv_screens` row, so "could not be read" and "not looked at yet"
    were the same state to every reader, and the page counted them as unscreened
    for ever. On CPD Coach that was 81 of 411 -- 43 with no resume stored at
    all, 26 extracting to under 250 words, 12 failing outright as JPEGs, PNGs
    and legacy .doc files -- and it read as a screener that kept stopping.

    A skip is DELETED, never superseded, once that application screens
    successfully. CVScreen keeps its history because a retired score still says
    what we once believed; a skip says only what is true right now, and a stale
    one is worth nothing to anybody.
    """

    __tablename__ = "cv_screen_skips"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_cv_screen_skip_id)

    # Unique: a skip is the current state of one candidate's CV, so a second
    # attempt replaces the first rather than stacking up.
    application_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    job_id: Mapped[int] = mapped_column(Integer, nullable=False)
    candidate_name: Mapped[str] = mapped_column(Text, nullable=False)

    # The screener's own words, verbatim, so the page can say WHY.
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    kind: Mapped[str] = mapped_column(Text, nullable=False)

    # What the file was called in Markaz: what somebody chasing a missing CV
    # actually needs in order to go and look for it.
    cv_file_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_by: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "kind IN (" + ",".join(f"'{k}'" for k in CV_SKIP_KINDS) + ")",
            name="ck_cv_screen_skip_kind",
        ),
        Index("ix_cv_screen_skip_job_id", "job_id"),
        {"schema": "coco"},
    )


class CaseStudyProbe(Base):
    """The last time we went and LOOKED for one candidate's case study.

    A measurement, not a judgement, so there is one row per application and a
    new probe overwrites it -- unlike CVScreen, where an old score must be
    retired rather than replaced. `probed_at` is how a reader knows whether to
    trust it.

    It exists because looking is expensive: the mailbox, the candidate's Drive
    links and Markaz's own file API are three network round trips per
    candidate, which cannot happen inside a page load for a job with eighty
    applicants.

    🔴 `send_found = False` DOES NOT MEAN NOT SENT. Markaz records no
       case-study send anywhere (no `case_study_sent_at` column, and
       `candidate_communications` carries 16 typed rows in total while
       reporting 0 sends against 4-17 submissions per job), so a send is only
       ever visible in Ayesha's mailbox. A probe that finds nothing means our
       records are silent. `case_study_tracking.submission_status` encodes
       this: the status is NO_RECORD_OF_A_SEND, and there is deliberately no
       "not_sent".
    """

    __tablename__ = "case_study_probes"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_case_study_probe_id)

    # One row per application: a probe replaces the previous one. The unique
    # constraint is NAMED in __table_args__ rather than declared with
    # unique=True, which produces an unnamed constraint that Postgres names
    # itself and a later migration cannot refer to.
    application_id: Mapped[int] = mapped_column(Integer, nullable=False)
    job_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # What Markaz holds: the subset of CHANNELS that carried something.
    channels: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # What the mailbox holds. `send_found=False` is "we could not find one".
    send_found: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    send_subject: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    send_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    status: Mapped[str] = mapped_column(Text, nullable=False)

    # What reading the submission produced. `corpus_error` is set, and the rest
    # left empty, when the submission exists but could not be read -- the same
    # refuse-rather-than-degrade shape as CVScreen and cv_text.
    corpus_chars: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sources: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    corpus_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # The assembled submission text itself. Stored, rather than re-fetched,
    # because the mirror check is a COHORT check: it compares every
    # submission on a job against every other, and re-assembling each one
    # costs three network round trips. More importantly, a mirror finding
    # has to show the shared text -- a flag a human cannot check is an
    # accusation -- and hashes alone cannot. Internal evaluation data,
    # never sent anywhere; the original stays in Markaz and Drive.
    corpus_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    flags: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    completeness: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    probed_by: Mapped[str] = mapped_column(Text, nullable=False)
    probed_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "status IN (" + ",".join(f"'{s}'" for s in CASE_STUDY_PROBE_STATUSES) + ")",
            name="ck_case_study_probe_status",
        ),
        # A send we claim to have found must say which message it was.
        CheckConstraint(
            "(NOT send_found) OR (send_subject IS NOT NULL AND send_at IS NOT NULL)",
            name="ck_case_study_probe_send_is_evidenced",
        ),
        UniqueConstraint("application_id", name="uq_case_study_probe_application_id"),
        Index("ix_case_study_probe_job_id", "job_id"),
        {"schema": "coco"},
    )


class KCDEvaluation(Base):
    """One case study evaluated on the Knowledge / Capacity / Design framework.

    A HUMAN evaluation with the rules enforced, not a model score. The SOP
    requires reading the assignment, the raw datasets and an ideal answer
    before opening a single submission, and the app has none of those; a model
    scoring without them would produce exactly the ungrounded output Rule 29
    exists to prevent. `case_study_evaluations` is the model-scored,
    benchmark-anchored table and is a different thing.

    What this table guarantees, because the rules are in
    `services/kcd_evaluation.py` and mirrored as CHECK constraints here:

      * the scale runs 0 to 5 in half steps WITH A REAL ZERO (CLAUDE.md
        Rule 27), not the SOP's 1-to-5 floor;
      * a CONDITIONAL verdict cannot exist without its condition, which the
        SOP's own Common Mistakes table names as making it unactionable;
      * an incomplete submission is marked as such and is never ranked against
        a complete one (`kcd_evaluation.rank_results` does the splitting);
      * advancement to GWC is the SOP's 60%, held in one constant rather than
        restated in prose.

    Re-evaluating SUPERSEDES rather than duplicates, like `CVScreen` and unlike
    `CaseStudyProbe`: this is a judgement, so the old number must stay visible
    and marked, never silently overwritten (CLAUDE.md Rule 25).

    🔒 "KCD" is internal. Anything that leaves the team says "case study".
    """

    __tablename__ = "kcd_evaluations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_kcd_evaluation_id)

    application_id: Mapped[int] = mapped_column(Integer, nullable=False)
    job_id: Mapped[int] = mapped_column(Integer, nullable=False)
    candidate_name: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)

    scores: Mapped[dict] = mapped_column(JSONB, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSONB, nullable=False)
    # A role-specific framework may override the default weights. Null means
    # the defaults in kcd_evaluation.DIMENSIONS were used, and storing which
    # is the only way a later reader can reproduce the total.
    weights: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Which dimensions were capped and under which of the SOP's two rules.
    caps_applied: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    total: Mapped[float] = mapped_column(Float, nullable=False)
    verdict: Mapped[str] = mapped_column(Text, nullable=False)
    condition: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    advances_to_gwc: Mapped[bool] = mapped_column(Boolean, nullable=False)

    incomplete: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    missing_parts: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # The SOP's three integrity checks: content dump, mirror problem,
    # foundational misread. Signals for a human, each with its evidence.
    integrity_flags: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # The SOP's cross-check: aligned within 5 points, flag above 10.
    second_evaluator: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    second_total: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    superseded_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_by: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "verdict IN (" + ",".join(f"'{v}'" for v in KCD_VERDICTS) + ")",
            name="ck_kcd_verdict",
        ),
        # The SOP's rule, at the database level: a conditional with no
        # condition is a hedge, not a decision.
        CheckConstraint(
            "verdict <> 'conditional' OR (condition IS NOT NULL AND btrim(condition) <> '')",
            name="ck_kcd_conditional_states_its_condition",
        ),
        CheckConstraint("total >= 0 AND total <= 100", name="ck_kcd_total_range"),
        CheckConstraint(
            "(is_current AND superseded_by IS NULL) OR "
            "(NOT is_current AND superseded_by IS NOT NULL)",
            name="ck_kcd_supersession_is_coherent",
        ),
        Index("ix_kcd_evaluation_application_id", "application_id"),
        Index("ix_kcd_evaluation_job_id", "job_id"),
        {"schema": "coco"},
    )


class SourcedCandidate(Base):
    """A passive candidate found by sourcing, and what has happened to them.

    The 3-layer web search stays in Claude Code (it drives a local headless
    browser against a SearXNG instance answering an anti-bot proof-of-work, and
    the built-in search is blind to Pakistani LinkedIn). This table owns
    everything downstream: the pool, who has been contacted, who replied, and
    who may be put into Markaz.

    🔴 THE CORE RULE IS A DATABASE CONSTRAINT, not a convention. "Markaz is ONLY
       touched after confirmed interest. Never speculatively."
       `ck_sourced_markaz_needs_confirmed_interest` makes it impossible to
       record a Markaz application against somebody who has not said yes, even
       through a bug. A sourced person who has not agreed is not an applicant,
       and putting them in the pipeline makes them look like one to every
       report that counts applications.

    🔴 VERIFICATION IS FOUR STATES, NEVER A BOOLEAN. On 2026-09-08 a subagent
       invented twelve people with plausible LinkedIn slugs and then falsely
       retracted six real ones. `not_found` means the check did not come back;
       it is NOT evidence of invention, because the verifier has known false
       negatives. A boolean would force that into "unverified" and lose the
       distinction.

    `years` is nullable ON PURPOSE and `years_note` keeps the original text. A
    column that admits it does not know beats one that quietly invents a
    number: the first Band classifier read "26 connections" as 8+ years.
    """

    __tablename__ = "sourced_candidates"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_sourced_candidate_id)

    name: Mapped[str] = mapped_column(Text, nullable=False)
    organization: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    linkedin_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # The identifying part, lowercased. Country subdomains vary for one person
    # (pk.linkedin.com vs www.linkedin.com), so the slug identifies them and
    # the URL does not.
    linkedin_slug: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    years_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    verification_state: Mapped[str] = mapped_column(Text, nullable=False)
    verification_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    verified_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    tier: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    outreach_state: Mapped[str] = mapped_column(Text, nullable=False)
    contacted_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    contacted_by: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reply_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Set ONLY after confirmed interest -- see the CHECK constraint below.
    markaz_application_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    pushed_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    pushed_by: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Which role they were sourced for, and where the row came from.
    job_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    role_label: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_by: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "verification_state IN ("
            + ",".join(f"'{v}'" for v in VERIFICATION_STATES) + ")",
            name="ck_sourced_verification_state",
        ),
        CheckConstraint(
            "outreach_state IN (" + ",".join(f"'{v}'" for v in OUTREACH_STATES) + ")",
            name="ck_sourced_outreach_state",
        ),
        # The core rule, at the database level.
        CheckConstraint(
            "markaz_application_id IS NULL "
            "OR outreach_state = 'replied_interested'",
            name="ck_sourced_markaz_needs_confirmed_interest",
        ),
        Index("ix_sourced_candidate_slug", "linkedin_slug"),
        Index("ix_sourced_candidate_job_id", "job_id"),
        Index("ix_sourced_candidate_outreach", "outreach_state"),
        {"schema": "coco"},
    )


class InviteLink(Base):
    """The booking / JD links for one invite type, and PROOF of where they go.

    🔴 THIS TABLE EXISTS BECAUSE A REPO CONSTANT IS NOT EVIDENCE. Growth Manager
       runs as two live roles, Job 39 Lahore and Job 41 Karachi, with separate
       JDs and separate booking schedules.
       `scripts/jobs/job39/send_growth_manager_invites_batch.py` sits in the
       job39 folder and its constants are Job 41 / Karachi; copying it for a
       Lahore candidate books them into the Karachi schedule and nothing
       complains (CLAUDE.md Rule 24).

    So `verified_title` is the title the page ACTUALLY returned when somebody
    fetched it, `verified_at` is when, and a live send refuses while they are
    null. `expected_title` is what the role should be, so the fetched title is
    compared against something rather than merely stored.

    A row with a `job_id` beats the type-level default. That is how two cities
    keep two schedules without either inheriting the other's.
    """

    __tablename__ = "invite_links"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_invite_link_id)
    job_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    invite_type: Mapped[str] = mapped_column(Text, nullable=False)
    label: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    booking_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    jd_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    prep_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    expected_title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    verified_title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    verified_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    verified_by: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    verify_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    cc_list: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("uq_invite_links_job_type", "job_id", "invite_type",
              unique=True, postgresql_where=text("job_id IS NOT NULL")),
        Index("uq_invite_links_default_type", "invite_type",
              unique=True, postgresql_where=text("job_id IS NULL")),
        {"schema": "coco"},
    )


class InviteSend(Base):
    """One invite that actually left, pilot or live.

    🔴 `uq_invite_sends_live_once` IS THE BATCH DISCIPLINE AS A CONSTRAINT. The
       rule from 2026-08-24 is to scan Sent Mail per recipient for the invite's
       own subject BEFORE drafting and again AFTER sending, because a send
       loop's console output reports what it TRIED, not what left, and catches
       neither a duplicate nor a silent omission. Postgres now refuses a second
       live invite of the same type to the same application.

    Pilots sit outside that index on purpose: a pilot is redrafted and re-sent
    to Ayesha as many times as it takes.

    `booking_url` and `booking_verified_title` are copied in at send time, so
    editing the configuration later cannot rewrite history about which
    schedule somebody was actually booked into.
    """

    __tablename__ = "invite_sends"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_invite_send_id)
    application_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    candidate_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    job_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    invite_type: Mapped[str] = mapped_column(Text, nullable=False)
    candidate_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    to_address: Mapped[str] = mapped_column(Text, nullable=False)
    cc_list: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    body_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_live: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    booking_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    booking_verified_title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    sent_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    sent_by: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("uq_invite_sends_live_once", "application_id", "invite_type",
              unique=True,
              postgresql_where=text("is_live AND application_id IS NOT NULL")),
        Index("ix_invite_sends_sent_at", "sent_at"),
        {"schema": "coco"},
    )
