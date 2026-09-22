"""eval_benchmarks approved-implies-qa'd gate + case_study_evaluations rubric/corpus provenance

Revision ID: 0011_eval_benchmark_qa_gate_and_rubric_provenance
Revises: 0010_case_study_evaluations
Create Date: 2026-09-22

Two review fixes from the case-study Phase 3 final review, landed together
because both close the same gap: "which answer key, and which rubric text,
produced this score" must always be answerable from the rows alone.

1. `coco.eval_benchmarks`: the plan defines Rule 0 as "a benchmark row with
   `qa_approved_at` set" -- but 0009's CHECK constraint only ever
   constrained `status`, so an `approved` row with a NULL `qa_approved_at`
   was structurally possible in the database even though
   `approve_benchmark()` never actually writes one. This adds a CHECK that
   makes that divergence impossible at the database level, not just by
   convention: `status <> 'approved' OR qa_approved_at IS NOT NULL`.
   `webapp/routers/case_studies.py`'s `_APPROVED_BENCHMARK_FOR_JOB_SQL` gets
   the matching `AND qa_approved_at IS NOT NULL` in the same code change, so
   the two cannot drift apart.

2. `coco.case_study_evaluations`: `rubric_sha256` records which revision of
   the (mutable, unversioned)
   `.claude/skills/02_candidate-evaluation/case-study-scoring-rubric.md`
   file actually produced this score -- the same audit reasoning as
   `values_scorecard_drafts.transcript_sha256` (0006). Two evaluations
   scored before and after an anchor edit to that file were otherwise
   indistinguishable in the database. `corpus_chars` records how much
   submission text was actually scored, previously unanswerable from a
   persisted row.

Both new columns on `case_study_evaluations` carry a `server_default` purely
so this ALTER is safe to run even if the table already holds rows (every
row written by the app from this point on always supplies a real value via
the ORM insert; the default only ever matters for a pre-existing row) --
this could not be verified against production from this machine (port 5432
is blocked here; production migrations run via `railway run`), so the
column is defensive rather than a claim that the table is known-empty.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# NOTE: alembic_version.version_num is varchar(32). This id was originally
# "0011_eval_benchmark_qa_gate_and_rubric_provenance" (49 chars), which made the
# migration impossible to stamp. Keep every revision id at 32 characters or fewer.
revision = "0011_benchmark_qa_gate"
down_revision = "0010_case_study_evaluations"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_eval_benchmark_approved_has_qa_approved_at",
        "eval_benchmarks",
        "status <> 'approved' OR qa_approved_at IS NOT NULL",
        schema="coco",
    )
    op.add_column(
        "case_study_evaluations",
        sa.Column("rubric_sha256", sa.Text(), nullable=False, server_default=""),
        schema="coco",
    )
    op.add_column(
        "case_study_evaluations",
        sa.Column("corpus_chars", sa.Integer(), nullable=False, server_default="0"),
        schema="coco",
    )
    # The defaults above exist only to make the ALTER safe against any
    # pre-existing row; going forward every insert supplies a real value, so
    # drop the server-side default rather than let it mask a future ORM bug
    # that forgets to pass one.
    op.alter_column("case_study_evaluations", "rubric_sha256", server_default=None, schema="coco")
    op.alter_column("case_study_evaluations", "corpus_chars", server_default=None, schema="coco")


def downgrade() -> None:
    op.drop_column("case_study_evaluations", "corpus_chars", schema="coco")
    op.drop_column("case_study_evaluations", "rubric_sha256", schema="coco")
    op.drop_constraint(
        "ck_eval_benchmark_approved_has_qa_approved_at",
        "eval_benchmarks",
        schema="coco",
        type_="check",
    )
