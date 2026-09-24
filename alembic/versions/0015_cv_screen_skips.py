"""cv_screen_skips (the CVs that could not be read, kept instead of forgotten)

Revision ID: 0015_cv_skips
Revises: 0014_kcd_evaluations
Create Date: 2026-09-24

A candidate whose CV cannot be read never gets a `cv_screens` row -- correctly,
because a screen must be grounded in the candidate's actual CV and a model
asked to judge an empty page still answers (CLAUDE.md Rule 32). But "no row"
and "not looked at yet" were indistinguishable, so the page counted them as
NOT YET SCREENED for ever.

On CPD Coach (job 17) that was 81 of 411. The whole position had in fact been
read: 43 of the 81 have no resume stored in Markaz at all, 26 extract to fewer
than 250 words, and 12 fail extraction outright -- JPEGs, PNGs and legacy .doc
files. Ayesha ran the position twice and then asked why 81 were "still to be
screened", which is exactly what the page told her. Not one of them was work
the screener could do.

So a skip is recorded. The row is DELETED, never superseded, when that
application is successfully screened later -- unlike cv_screens, where history
is the point. A skip is not a result; it is a statement about right now, and a
stale one has no value to anybody.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0015_cv_skips"
down_revision = "0014_kcd_evaluations"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cv_screen_skips",
        sa.Column("id", sa.String(), primary_key=True),
        # One row per application at most: a skip describes the current state
        # of that candidate's CV, so a second attempt replaces the first.
        sa.Column("application_id", sa.Integer(), nullable=False, unique=True),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("candidate_name", sa.Text(), nullable=False),
        # The screener's own words, kept verbatim so the page can say WHY
        # rather than just that something went wrong.
        sa.Column("reason", sa.Text(), nullable=False),
        # A coarse bucket the UI can group and count by, derived from the
        # reason at write time: no_cv / unreadable / too_short.
        sa.Column("kind", sa.Text(), nullable=False),
        # What the file was called in Markaz, which is what somebody chasing a
        # missing CV actually needs to go and look for.
        sa.Column("cv_file_name", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=False, server_default=""),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        schema="coco",
    )
    op.create_index(
        "ix_cv_screen_skip_job_id", "cv_screen_skips", ["job_id"], schema="coco"
    )


def downgrade() -> None:
    op.drop_index("ix_cv_screen_skip_job_id", table_name="cv_screen_skips", schema="coco")
    op.drop_table("cv_screen_skips", schema="coco")
