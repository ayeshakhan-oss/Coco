"""values_scorecard_drafts (values-scoring Phase 2: draft storage)

Revision ID: 0006_values_drafts
Revises: 0005_coco_schema
Create Date: 2026-09-17

A values-interview scorecard DRAFT, reviewed by a human before it is ever
written to Markaz. Lives in the `coco` schema from the start — never `public`
— for the same reason as comm_evidence + gmail_sync_runs (see 0005): Markaz's
Replit per-deploy schema push prunes `public` tables it doesn't recognise.

Stores only a SHA-256 of the interview transcript, not the transcript itself:
the transcript is interview content about a named person and does not need a
second home once it has been scored. The hash is enough to tell whether a
re-score used the same input.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0006_values_drafts"
down_revision = "0005_coco_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS coco")
    op.create_table(
        "values_scorecard_drafts",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("application_id", sa.Integer(), nullable=False),
        sa.Column("candidate_name", sa.Text(), nullable=False),
        sa.Column("host", sa.Text(), nullable=False),
        sa.Column("transcript_sha256", sa.Text(), nullable=False),
        sa.Column("values", postgresql.JSONB(), nullable=False),
        sa.Column("final_comments", sa.Text(), nullable=False),
        sa.Column("proceed", sa.Boolean(), nullable=False),
        sa.Column("gwc", postgresql.JSONB(), nullable=True),
        sa.Column(
            "status", sa.Text(), nullable=False, server_default="draft"
        ),
        sa.Column("model", sa.Text(), nullable=False),
        sa.Column("created_by", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("approved_by", sa.Text(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("markaz_payload", postgresql.JSONB(), nullable=True),
        sa.CheckConstraint(
            "status IN ('draft','submitted')", name="ck_values_draft_status"
        ),
        schema="coco",
    )
    op.create_index(
        "ix_values_draft_application_id",
        "values_scorecard_drafts",
        ["application_id"],
        schema="coco",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_values_draft_application_id",
        table_name="values_scorecard_drafts",
        schema="coco",
    )
    op.drop_table("values_scorecard_drafts", schema="coco")
