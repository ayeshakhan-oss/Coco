"""values_scorecard_drafts.interview_date

Revision ID: 0008_values_draft_interview_date
Revises: 0007_values_replaced_payload
Create Date: 2026-09-17

Ayesha's decision 2026-09-17: `build_markaz_payload`'s `date` field was
silently defaulting to `dt.date.today()` because nothing captured the actual
INTERVIEW date -- a Friday interview submitted the following Monday recorded
Monday in Markaz. This column lets the UI capture the real interview date
(nullable: it is still valid to submit same-day, in which case `submit()`
falls back to today, visibly, in the UI).
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0008_values_draft_interview_date"
down_revision = "0007_values_replaced_payload"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "values_scorecard_drafts",
        sa.Column("interview_date", sa.Date(), nullable=True),
        schema="coco",
    )


def downgrade() -> None:
    op.drop_column("values_scorecard_drafts", "interview_date", schema="coco")
