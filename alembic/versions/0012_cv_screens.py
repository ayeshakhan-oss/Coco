"""cv_screens (Candidate Evaluation: Coco's own CV screening)

Revision ID: 0012_cv_screens
Revises: 0011_benchmark_qa_gate
Create Date: 2026-09-22

One candidate's CV screened against one job description, using Coco's own three
criteria (skills / experience / fit) on a 0-5 scale with a real zero.

This is NOT Nugget's technical screening. That engine writes to
`public.nugget_screening_evals`, is owned by another agent, and is read-only to
us. The two never share a table, a rubric or a tier vocabulary: Coco's tiers are
shortlist / maybe / no_hire, never P1-P4 (Ayesha, 2026-09-15).

Lives in the `coco` schema from the start -- never `public` -- for the same
reason as comm_evidence, gmail_sync_runs, values_scorecard_drafts,
eval_benchmarks and case_study_evaluations (see 0005/0006/0009/0010): Markaz's
Replit per-deploy schema push prunes `public` tables it doesn't recognise.

Note the revision id is short. `alembic_version.version_num` is varchar(32) and
0011's original 49-character id could never be stamped (see
webapp/tests/test_migration_revision_ids.py, which now guards every migration).
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0012_cv_screens"
down_revision = "0011_benchmark_qa_gate"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cv_screens",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("application_id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("candidate_name", sa.Text(), nullable=False),
        sa.Column("role", sa.Text(), nullable=False),
        sa.Column("scores", postgresql.JSONB(), nullable=False),
        sa.Column("evidence", postgresql.JSONB(), nullable=False),
        sa.Column("strengths", postgresql.JSONB(), nullable=False),
        sa.Column("gaps", postgresql.JSONB(), nullable=False),
        # Two figures, never one: conflating total with relevant experience is
        # the SOP's own named mistake.
        sa.Column("total_experience_years", sa.Float(), nullable=False),
        sa.Column("relevant_experience_years", sa.Float(), nullable=False),
        sa.Column("relevant_experience_note", sa.Text(), nullable=False),
        sa.Column("match", sa.Float(), nullable=False),
        sa.Column("tier", sa.Text(), nullable=False),
        sa.Column("model", sa.Text(), nullable=False),
        sa.Column("sop_sha256", sa.Text(), nullable=False),
        sa.Column("jd_sha256", sa.Text(), nullable=False),
        sa.Column("cv_chars", sa.Integer(), nullable=False),
        sa.Column(
            "cv_truncated", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        # Re-screening supersedes rather than duplicates, so a stale number can
        # never be read back as live (CLAUDE.md Rule 25).
        sa.Column(
            "is_current", sa.Boolean(), nullable=False, server_default=sa.true()
        ),
        sa.Column("superseded_by", sa.String(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "tier IN ('shortlist','maybe','no_hire')",
            name="ck_cv_screen_tier",
        ),
        sa.CheckConstraint(
            "relevant_experience_years <= total_experience_years",
            name="ck_cv_screen_relevant_within_total",
        ),
        sa.CheckConstraint(
            "(is_current AND superseded_by IS NULL) OR "
            "(NOT is_current AND superseded_by IS NOT NULL)",
            name="ck_cv_screen_supersession_is_coherent",
        ),
        schema="coco",
    )
    op.create_index(
        "ix_cv_screen_application_id", "cv_screens", ["application_id"], schema="coco"
    )
    op.create_index("ix_cv_screen_job_id", "cv_screens", ["job_id"], schema="coco")


def downgrade() -> None:
    op.drop_index("ix_cv_screen_job_id", table_name="cv_screens", schema="coco")
    op.drop_index(
        "ix_cv_screen_application_id", table_name="cv_screens", schema="coco"
    )
    op.drop_table("cv_screens", schema="coco")
