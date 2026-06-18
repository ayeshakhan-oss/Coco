"""comm_evidence + gmail_sync_runs (Markaz <-> Gmail communication sync)

Revision ID: 0004_gmail_sync
Revises: 0003_roles
Create Date: 2026-06-18

Two new app-owned tables for the Gmail-evidence source-of-truth feature:
- comm_evidence    : per-application Gmail evidence + manual overrides (one row
                     per application; snippet/metadata only, never bodies).
- gmail_sync_runs  : durable audit of each sync + the "last synced" indicator.

Both are added to MANAGED_TABLES in alembic/env.py so autogenerate sees them.
The legacy Talent-Acquisition tables are untouched.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0004_gmail_sync"
down_revision = "0003_roles"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "comm_evidence",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("application_id", sa.Integer(), nullable=False),
        sa.Column("candidate_id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.Integer(), nullable=True),
        sa.Column(
            "gmail_status",
            sa.String(),
            nullable=False,
            server_default="not_checked",
        ),
        sa.Column("match_method", sa.String(), nullable=True),
        sa.Column("matched_message_id", sa.String(), nullable=True),
        sa.Column("gmail_thread_id", sa.String(), nullable=True),
        sa.Column("internal_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("matched_subject", sa.Text(), nullable=True),
        sa.Column("matched_to", sa.Text(), nullable=True),
        sa.Column("matched_snippet", sa.Text(), nullable=True),
        sa.Column("uncertain_reason", sa.Text(), nullable=True),
        sa.Column("marked_sent_by", sa.String(), nullable=True),
        sa.Column("marked_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("marked_sent_reason", sa.Text(), nullable=True),
        sa.Column(
            "ignored", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column("ignored_by", sa.String(), nullable=True),
        sa.Column("ignored_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("checked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(["marked_sent_by"], ["app_users.id"]),
        sa.ForeignKeyConstraint(["ignored_by"], ["app_users.id"]),
        sa.CheckConstraint(
            "gmail_status IN ('not_checked','none','found','uncertain')",
            name="ck_evidence_gmail_status",
        ),
        sa.CheckConstraint(
            "match_method IS NULL OR match_method IN ('message_id','recipient_window','none')",
            name="ck_evidence_match_method",
        ),
    )
    op.create_index(
        "ix_evidence_application_id", "comm_evidence", ["application_id"], unique=True
    )
    op.create_index("ix_evidence_candidate_id", "comm_evidence", ["candidate_id"])
    op.create_index("ix_evidence_gmail_status", "comm_evidence", ["gmail_status"])
    op.create_index(
        "ix_evidence_ignored",
        "comm_evidence",
        ["ignored"],
        postgresql_where=sa.text("ignored"),
    )

    op.create_table(
        "gmail_sync_runs",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("trigger", sa.String(), nullable=False),
        sa.Column("triggered_by", sa.String(), nullable=True),
        sa.Column(
            "full_resync",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "status", sa.String(), nullable=False, server_default="running"
        ),
        sa.Column("query", sa.Text(), nullable=True),
        sa.Column(
            "messages_scanned",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "candidates_evaluated",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "found_count", sa.Integer(), nullable=False, server_default=sa.text("0")
        ),
        sa.Column(
            "uncertain_count",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "none_count", sa.Integer(), nullable=False, server_default=sa.text("0")
        ),
        sa.Column("watermark_before", sa.DateTime(timezone=True), nullable=True),
        sa.Column("watermark_after", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_detail", sa.Text(), nullable=True),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["triggered_by"], ["app_users.id"]),
        sa.CheckConstraint(
            "trigger IN ('scheduled','manual')", name="ck_syncrun_trigger"
        ),
        sa.CheckConstraint(
            "status IN ('running','ok','partial','failed')", name="ck_syncrun_status"
        ),
    )
    op.create_index("ix_syncrun_status", "gmail_sync_runs", ["status"])
    op.create_index("ix_syncrun_started_at", "gmail_sync_runs", ["started_at"])


def downgrade() -> None:
    op.drop_index("ix_syncrun_started_at", table_name="gmail_sync_runs")
    op.drop_index("ix_syncrun_status", table_name="gmail_sync_runs")
    op.drop_table("gmail_sync_runs")
    op.drop_index("ix_evidence_ignored", table_name="comm_evidence")
    op.drop_index("ix_evidence_gmail_status", table_name="comm_evidence")
    op.drop_index("ix_evidence_candidate_id", table_name="comm_evidence")
    op.drop_index("ix_evidence_application_id", table_name="comm_evidence")
    op.drop_table("comm_evidence")
