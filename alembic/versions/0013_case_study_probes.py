"""case_study_probes (Candidate Evaluation: case-study tracking)

Revision ID: 0013_case_study_probes
Revises: 0012_cv_screens
Create Date: 2026-09-22

The last time we went and LOOKED for one candidate's case study: what Markaz
holds, whether a send is findable in the mailbox, and what reading the
submission produced. One row per application, replaced by a later probe --
a measurement, not a judgement.

🔴 `send_found = false` does not mean "not sent". Markaz records no case-study
   send anywhere: there is no `case_study_sent_at` column, and
   `public.candidate_communications` holds 16 typed rows in the whole table
   while reporting 0 sends against 4-17 submissions per job (measured
   2026-09-22). A send is only visible in Ayesha's mailbox, so a probe that
   finds nothing means our records are silent. The status vocabulary has no
   "not_sent" for exactly that reason.

Lives in the `coco` schema -- never `public` -- like every other app-owned
table: Markaz's Replit per-deploy schema push prunes `public` tables it does
not recognise.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0013_case_study_probes"
down_revision = "0012_cv_screens"
branch_labels = None
depends_on = None

STATUSES = ("submitted", "awaiting", "no_record_of_a_send", "submitted_without_send_record")


def upgrade() -> None:
    op.create_table(
        "case_study_probes",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("application_id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("channels", postgresql.JSONB(), nullable=False),
        sa.Column(
            "send_found", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column("send_subject", sa.Text(), nullable=True),
        sa.Column("send_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("corpus_chars", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("sources", postgresql.JSONB(), nullable=False),
        sa.Column("corpus_error", sa.Text(), nullable=True),
        # Stored so the cohort-level mirror check can run without three
        # network round trips per candidate, and so a mirror finding can
        # show the shared text rather than only assert it.
        sa.Column("corpus_text", sa.Text(), nullable=True),
        sa.Column("flags", postgresql.JSONB(), nullable=False),
        sa.Column("completeness", postgresql.JSONB(), nullable=False),
        sa.Column("probed_by", sa.Text(), nullable=False),
        sa.Column(
            "probed_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "status IN (" + ",".join(f"'{s}'" for s in STATUSES) + ")",
            name="ck_case_study_probe_status",
        ),
        # A send we claim to have found must say which message it was.
        sa.CheckConstraint(
            "(NOT send_found) OR (send_subject IS NOT NULL AND send_at IS NOT NULL)",
            name="ck_case_study_probe_send_is_evidenced",
        ),
        sa.UniqueConstraint(
            "application_id", name="uq_case_study_probe_application_id"
        ),
        schema="coco",
    )
    op.create_index(
        "ix_case_study_probe_job_id", "case_study_probes", ["job_id"], schema="coco"
    )


def downgrade() -> None:
    op.drop_index(
        "ix_case_study_probe_job_id", table_name="case_study_probes", schema="coco"
    )
    op.drop_table("case_study_probes", schema="coco")
