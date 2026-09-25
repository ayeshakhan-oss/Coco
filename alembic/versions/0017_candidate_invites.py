"""invite_links + invite_sends (Skill 06: Candidate Invites)

Revision ID: 0017_candidate_invites
Revises: 0016_sourced_candidates
Create Date: 2026-09-25

Two tables, each one a lesson made mechanical.

🔴 `invite_links` EXISTS BECAUSE A LINK IN A REPO CONSTANT IS NOT EVIDENCE.
   Growth Manager runs as TWO live roles -- Job 39 Lahore and Job 41 Karachi --
   with separate JDs and separate booking schedules, and
   `scripts/jobs/job39/send_growth_manager_invites_batch.py` sits in the job39
   folder carrying Job 41 / Karachi constants. Copying it for a Lahore
   candidate books them into the Karachi schedule and nothing complains
   (CLAUDE.md Rule 24). Here a link is configuration, per job and per type, and
   it carries `verified_title` / `verified_at`: the title the page ACTUALLY
   returned when somebody fetched it. A live send refuses while those are null.

🔴 `invite_sends` EXISTS BECAUSE A SEND LOOP CANNOT SEE ITS OWN OMISSIONS.
   The batch discipline from 2026-08-24 is an IMAP scan of Sent Mail for the
   invite's own subject BEFORE drafting (proves nobody already got it) and
   again AFTER sending (proves exactly one each), because a loop's console
   output reports what it TRIED, not what left. `uq_invite_sends_live_once` is
   that scan as a constraint: one live invite of one type per application,
   enforced by Postgres. Pilots are excluded from it -- a pilot is redrafted
   and re-sent to Ayesha as often as it takes.

Both live in the `coco` schema. A Coco table in `public` is dropped by
Markaz/Replit (memory/root_cause_markaz_replit_drops_coco_tables_2026_06_30.md).
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0017_candidate_invites"
down_revision = "0016_sourced_candidates"
branch_labels = None
depends_on = None

SCHEMA = "coco"


def upgrade() -> None:
    op.create_table(
        "invite_links",
        sa.Column("id", sa.String(), primary_key=True),
        # Null job_id = a default for that type across jobs. A job-specific row
        # always wins, which is how Lahore and Karachi keep separate schedules.
        sa.Column("job_id", sa.Integer(), nullable=True),
        sa.Column("invite_type", sa.Text(), nullable=False),
        sa.Column("label", sa.Text(), nullable=True),
        sa.Column("booking_url", sa.Text(), nullable=True),
        sa.Column("jd_url", sa.Text(), nullable=True),
        sa.Column("prep_url", sa.Text(), nullable=True),
        # What the role is expected to be, so a fetched title can be compared
        # against something rather than merely recorded.
        sa.Column("expected_title", sa.Text(), nullable=True),
        # The title the page actually returned, and when. Null means unproven.
        sa.Column("verified_title", sa.Text(), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("verified_by", sa.Text(), nullable=True),
        sa.Column("verify_error", sa.Text(), nullable=True),
        sa.Column("cc_list", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.text("now()"), nullable=False),
        schema=SCHEMA,
    )
    # One configuration per (job, type). A second row for the same pair is how
    # two different booking links for one role end up both looking correct.
    op.create_index(
        "uq_invite_links_job_type",
        "invite_links", ["job_id", "invite_type"],
        unique=True, schema=SCHEMA,
        postgresql_where=sa.text("job_id IS NOT NULL"),
    )
    op.create_index(
        "uq_invite_links_default_type",
        "invite_links", ["invite_type"],
        unique=True, schema=SCHEMA,
        postgresql_where=sa.text("job_id IS NULL"),
    )

    op.create_table(
        "invite_sends",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("application_id", sa.Integer(), nullable=True),
        sa.Column("candidate_id", sa.Integer(), nullable=True),
        sa.Column("job_id", sa.Integer(), nullable=True),
        sa.Column("invite_type", sa.Text(), nullable=False),
        sa.Column("candidate_name", sa.Text(), nullable=True),
        # Recorded as sent, not as configured: the pilot recipient is Ayesha and
        # the row must say so, or a pilot reads later like a candidate send.
        sa.Column("to_address", sa.Text(), nullable=False),
        sa.Column("cc_list", postgresql.JSONB(), nullable=True),
        sa.Column("subject", sa.Text(), nullable=False),
        sa.Column("body_html", sa.Text(), nullable=True),
        sa.Column("is_live", sa.Boolean(), nullable=False,
                  server_default=sa.text("false")),
        # The link as it stood at send time, so a later config edit cannot
        # rewrite history about which schedule somebody was booked into.
        sa.Column("booking_url", sa.Text(), nullable=True),
        sa.Column("booking_verified_title", sa.Text(), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True),
                  server_default=sa.text("now()"), nullable=False),
        sa.Column("sent_by", sa.Text(), nullable=True),
        schema=SCHEMA,
    )
    # THE DUPLICATE-SEND GUARD. One live invite of one type per application.
    # Pilots are deliberately outside it.
    op.create_index(
        "uq_invite_sends_live_once",
        "invite_sends", ["application_id", "invite_type"],
        unique=True, schema=SCHEMA,
        postgresql_where=sa.text("is_live AND application_id IS NOT NULL"),
    )
    op.create_index(
        "ix_invite_sends_sent_at", "invite_sends", ["sent_at"], schema=SCHEMA
    )


def downgrade() -> None:
    op.drop_index("ix_invite_sends_sent_at", "invite_sends", schema=SCHEMA)
    op.drop_index("uq_invite_sends_live_once", "invite_sends", schema=SCHEMA)
    op.drop_table("invite_sends", schema=SCHEMA)
    op.drop_index("uq_invite_links_default_type", "invite_links", schema=SCHEMA)
    op.drop_index("uq_invite_links_job_type", "invite_links", schema=SCHEMA)
    op.drop_table("invite_links", schema=SCHEMA)
