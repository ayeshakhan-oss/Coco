"""eval_benchmarks (case-study Phase 3: benchmark storage)

Revision ID: 0009_eval_benchmarks
Revises: 0008_values_draft_interview_date
Create Date: 2026-09-22

The answer key a case-study run is scored against, written and QA'd BEFORE
any submission is opened. Rule 0 of the case-study rubric: scoring calibrates
to whoever is read first, so reading a submission before the benchmark
exists (or before it has been QA'd) anchors the whole pool. `qa_approved_by`
/ `qa_approved_at` make that discipline mechanical -- a scoring run can
require this row to be `status = 'approved'` with both fields set before it
will start.

Lives in the `coco` schema from the start -- never `public` -- for the same
reason as comm_evidence, gmail_sync_runs and values_scorecard_drafts (see
0005/0006): Markaz's Replit per-deploy schema push prunes `public` tables it
doesn't recognise.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0009_eval_benchmarks"
down_revision = "0008_values_draft_interview_date"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS coco")
    op.create_table(
        "eval_benchmarks",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("source_path", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("qa_approved_by", sa.Text(), nullable=True),
        sa.Column("qa_approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "status", sa.Text(), nullable=False, server_default="draft"
        ),
        sa.CheckConstraint(
            "status IN ('draft','approved','retired')", name="ck_eval_benchmark_status"
        ),
        schema="coco",
    )
    op.create_index(
        "ix_eval_benchmark_job_id",
        "eval_benchmarks",
        ["job_id"],
        schema="coco",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_eval_benchmark_job_id",
        table_name="eval_benchmarks",
        schema="coco",
    )
    op.drop_table("eval_benchmarks", schema="coco")
