"""case_study_evaluations (case-study Phase 3: scored evaluation storage)

Revision ID: 0010_case_study_evaluations
Revises: 0009_eval_benchmarks
Create Date: 2026-09-22

A case-study submission scored against an APPROVED `eval_benchmarks` row.
Persists exactly what `case_study_scoring.score_submission` returned -- the
six dimension scores, their evidence citations, any flags, and the total /
band it COMPUTED -- plus which benchmark and which submission sources
actually produced it, so "what was this scored against" is always
answerable from the row alone.

Lives in the `coco` schema from the start -- never `public` -- for the same
reason as comm_evidence, gmail_sync_runs, values_scorecard_drafts and
eval_benchmarks (see 0005/0006/0009): Markaz's Replit per-deploy schema push
prunes `public` tables it doesn't recognise.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0010_case_study_evaluations"
down_revision = "0009_eval_benchmarks"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "case_study_evaluations",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("application_id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column(
            "benchmark_id",
            sa.String(),
            sa.ForeignKey("coco.eval_benchmarks.id"),
            nullable=False,
        ),
        sa.Column("candidate_name", sa.Text(), nullable=False),
        sa.Column("role", sa.Text(), nullable=False),
        sa.Column("scores", postgresql.JSONB(), nullable=False),
        sa.Column("evidence", postgresql.JSONB(), nullable=False),
        sa.Column("flags", postgresql.JSONB(), nullable=False),
        sa.Column("total", sa.Float(), nullable=False),
        sa.Column("band", sa.Text(), nullable=False),
        sa.Column("model", sa.Text(), nullable=False),
        sa.Column("sources", postgresql.JSONB(), nullable=False),
        sa.Column("created_by", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "band IN ('strong_yes','yes','borderline','no','disqualified')",
            name="ck_case_study_evaluation_band",
        ),
        schema="coco",
    )
    op.create_index(
        "ix_case_study_evaluation_application_id",
        "case_study_evaluations",
        ["application_id"],
        schema="coco",
    )
    op.create_index(
        "ix_case_study_evaluation_job_id",
        "case_study_evaluations",
        ["job_id"],
        schema="coco",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_case_study_evaluation_job_id",
        table_name="case_study_evaluations",
        schema="coco",
    )
    op.drop_index(
        "ix_case_study_evaluation_application_id",
        table_name="case_study_evaluations",
        schema="coco",
    )
    op.drop_table("case_study_evaluations", schema="coco")
