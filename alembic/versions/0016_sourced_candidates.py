"""sourced_candidates (Talent Sourcing: the pool, outreach and the Markaz gate)

Revision ID: 0016_sourced_candidates
Revises: 0015_cv_skips
Create Date: 2026-09-25

A passive candidate found by sourcing, and what has happened to them since.

The skill's 3-layer web search stays in Claude Code: it drives a LOCAL headless
browser against a SearXNG instance that answers an anti-bot proof-of-work, and
the built-in web search is effectively blind to Pakistani LinkedIn. Everything
downstream -- the pool, who was contacted, who replied, who may enter Markaz --
lives here.

🔴 `ck_sourced_markaz_needs_confirmed_interest` IS THE SKILL'S CORE RULE AS A
   CONSTRAINT. "Markaz is ONLY touched after confirmed interest. Never
   speculatively." It is now impossible to record a Markaz application against
   somebody who has not said yes, even through a bug. A sourced person who has
   not agreed is not an applicant, and putting them in the pipeline makes them
   look like one to every report that counts applications.

🔴 Verification is FOUR states rather than a boolean, because on 2026-09-08 a
   subagent invented twelve people with plausible LinkedIn slugs and then
   FALSELY RETRACTED six real ones. `not_found` means the check did not come
   back and is NOT evidence of invention -- the verifier has known false
   negatives. A boolean would collapse that into "unverified" and lose it.

`years` is nullable on purpose, with `years_note` keeping the original text:
the first Band classifier read "26 connections" as 8+ years of experience.

Lives in the `coco` schema -- never `public`.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0016_sourced_candidates"
down_revision = "0015_cv_skips"
branch_labels = None
depends_on = None

VERIFICATION = ("confirmed", "unconfirmed", "not_found", "no_url")
OUTREACH = (
    "not_contacted", "contacted", "replied_interested",
    "replied_not_interested", "no_reply",
)


def upgrade() -> None:
    op.create_table(
        "sourced_candidates",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("organization", sa.Text(), nullable=True),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("location", sa.Text(), nullable=True),
        sa.Column("linkedin_url", sa.Text(), nullable=True),
        # The identifying part, lowercased: country subdomains vary for one
        # person, so the slug identifies them and the URL does not.
        sa.Column("linkedin_slug", sa.Text(), nullable=True),
        sa.Column("years", sa.Integer(), nullable=True),
        sa.Column("years_note", sa.Text(), nullable=True),
        sa.Column("verification_state", sa.Text(), nullable=False),
        sa.Column("verification_note", sa.Text(), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("tier", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Text(), nullable=True),
        sa.Column("outreach_state", sa.Text(), nullable=False),
        sa.Column("contacted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("contacted_by", sa.Text(), nullable=True),
        sa.Column("reply_note", sa.Text(), nullable=True),
        sa.Column("markaz_application_id", sa.Integer(), nullable=True),
        sa.Column("pushed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("pushed_by", sa.Text(), nullable=True),
        sa.Column("job_id", sa.Integer(), nullable=True),
        sa.Column("role_label", sa.Text(), nullable=True),
        sa.Column("source", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "verification_state IN (" + ",".join(f"'{v}'" for v in VERIFICATION) + ")",
            name="ck_sourced_verification_state",
        ),
        sa.CheckConstraint(
            "outreach_state IN (" + ",".join(f"'{v}'" for v in OUTREACH) + ")",
            name="ck_sourced_outreach_state",
        ),
        sa.CheckConstraint(
            "markaz_application_id IS NULL OR outreach_state = 'replied_interested'",
            name="ck_sourced_markaz_needs_confirmed_interest",
        ),
        schema="coco",
    )
    op.create_index(
        "ix_sourced_candidate_slug", "sourced_candidates", ["linkedin_slug"], schema="coco"
    )
    op.create_index(
        "ix_sourced_candidate_job_id", "sourced_candidates", ["job_id"], schema="coco"
    )
    op.create_index(
        "ix_sourced_candidate_outreach", "sourced_candidates", ["outreach_state"],
        schema="coco",
    )


def downgrade() -> None:
    for name in (
        "ix_sourced_candidate_outreach",
        "ix_sourced_candidate_job_id",
        "ix_sourced_candidate_slug",
    ):
        op.drop_index(name, table_name="sourced_candidates", schema="coco")
    op.drop_table("sourced_candidates", schema="coco")
