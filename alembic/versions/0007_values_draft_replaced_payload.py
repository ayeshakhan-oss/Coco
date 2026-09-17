"""values_scorecard_drafts.replaced_payload

Revision ID: 0007_values_replaced_payload
Revises: 0006_values_drafts
Create Date: 2026-09-17

Added for CRITICAL 4 in the task-6 fix pass: `submit()` may now overwrite an
application's EXISTING `public.applications.values_scorecard` when the
caller explicitly passes `overwrite=True`. When that happens, the PRIOR
value is written here so an overwrite never permanently destroys a
human-written scorecard with no trace. NULL on every normal (first-time)
submit.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0007_values_replaced_payload"
down_revision = "0006_values_drafts"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "values_scorecard_drafts",
        sa.Column("replaced_payload", postgresql.JSONB(), nullable=True),
        schema="coco",
    )


def downgrade() -> None:
    op.drop_column("values_scorecard_drafts", "replaced_payload", schema="coco")
