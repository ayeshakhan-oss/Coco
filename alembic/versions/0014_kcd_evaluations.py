"""kcd_evaluations (Candidate Evaluation: Knowledge / Capacity / Design)

Revision ID: 0014_kcd_evaluations
Revises: 0013_case_study_probes
Create Date: 2026-09-22

One case study evaluated on the Knowledge / Capacity / Design framework. A
HUMAN evaluation with the rules enforced, not a model score: the SOP requires
reading the assignment, the raw datasets and an ideal answer before opening a
submission, and the app has none of those. `case_study_evaluations` is the
model-scored, benchmark-anchored table and is a different thing.

Two of the CHECK constraints below encode rules that were previously prose:

  * `ck_kcd_conditional_states_its_condition` -- the SOP's own Common Mistakes
    table says a CONDITIONAL verdict with no stated condition is not
    actionable. It is now impossible to store one.
  * `ck_kcd_supersession_is_coherent` -- a re-evaluation retires the previous
    row rather than overwriting it (CLAUDE.md Rule 25), and the two fields
    cannot disagree about which number is live.

The scale itself (0 to 5 in half steps, with a real zero rather than the SOP's
1-to-5 floor, per CLAUDE.md Rule 27) is enforced in
webapp/services/kcd_evaluation.py, which is the only writer.

Lives in the `coco` schema -- never `public`.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0014_kcd_evaluations"
down_revision = "0013_case_study_probes"
branch_labels = None
depends_on = None

VERDICTS = ("strong_hire", "hire", "conditional", "borderline", "not_recommended")


def upgrade() -> None:
    op.create_table(
        "kcd_evaluations",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("application_id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("candidate_name", sa.Text(), nullable=False),
        sa.Column("role", sa.Text(), nullable=False),
        sa.Column("scores", postgresql.JSONB(), nullable=False),
        sa.Column("evidence", postgresql.JSONB(), nullable=False),
        # Null means the defaults were used. Storing which is the only way a
        # later reader can reproduce the total.
        sa.Column("weights", postgresql.JSONB(), nullable=True),
        sa.Column("caps_applied", postgresql.JSONB(), nullable=False),
        sa.Column("total", sa.Float(), nullable=False),
        sa.Column("verdict", sa.Text(), nullable=False),
        sa.Column("condition", sa.Text(), nullable=True),
        sa.Column("advances_to_gwc", sa.Boolean(), nullable=False),
        sa.Column(
            "incomplete", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column("missing_parts", postgresql.JSONB(), nullable=False),
        sa.Column("integrity_flags", postgresql.JSONB(), nullable=False),
        sa.Column("second_evaluator", sa.Text(), nullable=True),
        sa.Column("second_total", sa.Float(), nullable=True),
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
            "verdict IN (" + ",".join(f"'{v}'" for v in VERDICTS) + ")",
            name="ck_kcd_verdict",
        ),
        sa.CheckConstraint(
            "verdict <> 'conditional' OR "
            "(condition IS NOT NULL AND btrim(condition) <> '')",
            name="ck_kcd_conditional_states_its_condition",
        ),
        sa.CheckConstraint("total >= 0 AND total <= 100", name="ck_kcd_total_range"),
        sa.CheckConstraint(
            "(is_current AND superseded_by IS NULL) OR "
            "(NOT is_current AND superseded_by IS NOT NULL)",
            name="ck_kcd_supersession_is_coherent",
        ),
        schema="coco",
    )
    op.create_index(
        "ix_kcd_evaluation_application_id",
        "kcd_evaluations",
        ["application_id"],
        schema="coco",
    )
    op.create_index(
        "ix_kcd_evaluation_job_id", "kcd_evaluations", ["job_id"], schema="coco"
    )


def downgrade() -> None:
    op.drop_index("ix_kcd_evaluation_job_id", table_name="kcd_evaluations", schema="coco")
    op.drop_index(
        "ix_kcd_evaluation_application_id", table_name="kcd_evaluations", schema="coco"
    )
    op.drop_table("kcd_evaluations", schema="coco")
