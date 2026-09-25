"""contract_masters + contract_builds (Skill 07: contract drafting)

Revision ID: 0018_contract_masters
Revises: 0017_candidate_invites
Create Date: 2026-09-25

🔴 THE MASTERS LIVE HERE RATHER THAN IN GIT. `Contracts\\` is gitignored and
   stays that way: these are approved legal documents and a commit is
   permanent. They are uploaded once through the app and stored as bytes in
   this table, so the repository never carries them and a master can be
   replaced without a deploy.

🔴 `contract_builds` DELIBERATELY DOES NOT STORE THE GENERATED DOCUMENT. A
   filled contract contains a CNIC, a salary and a home address. The built
   file is streamed straight to the person who asked for it and never written
   down; this table keeps only who built what, for whom, and whether the
   validator passed. That is enough to answer "was a contract issued for this
   person" without turning the database into a store of identity documents.

   For the same reason `field_values` is NOT a column. The values ARE the PII.

Lives in the `coco` schema — never `public`, which Markaz's Replit push drops.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0018_contract_masters"
down_revision = "0017_candidate_invites"
branch_labels = None
depends_on = None

SCHEMA = "coco"


def upgrade() -> None:
    op.create_table(
        "contract_masters",
        sa.Column("id", sa.String(), primary_key=True),
        # The path as TEMPLATE_MAP names it, e.g.
        # "Fellow/Template - NDA Fellow Employee.docx". One row per master, and
        # the same file legitimately backs several (entity, doc_type) pairs.
        sa.Column("rel_path", sa.Text(), nullable=False),
        sa.Column("filename", sa.Text(), nullable=False),
        sa.Column("content", sa.LargeBinary(), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        # Identifies the exact master a document was built from, so a later
        # "which version produced this contract" has an answer.
        sa.Column("sha256", sa.String(64), nullable=False),
        # How many highlighted fill fields it carried when uploaded. A changed
        # count on re-upload is the signal that the master was re-issued.
        sa.Column("field_count", sa.Integer(), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(timezone=True),
                  server_default=sa.text("now()"), nullable=False),
        sa.Column("uploaded_by", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        schema=SCHEMA,
    )
    # One current master per path. Replacing one is an update, not a second row
    # that leaves two plausible versions of a legal document in play.
    op.create_index(
        "uq_contract_masters_rel_path", "contract_masters", ["rel_path"],
        unique=True, schema=SCHEMA,
    )

    op.create_table(
        "contract_builds",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("entity", sa.Text(), nullable=False),
        sa.Column("engagement", sa.Text(), nullable=False),
        sa.Column("doc_type", sa.Text(), nullable=False),
        sa.Column("master_sha256", sa.String(64), nullable=True),
        # A name is unavoidable to answer "did we issue this person a
        # contract". Nothing else about them is kept.
        sa.Column("person_name", sa.Text(), nullable=True),
        sa.Column("candidate_id", sa.Integer(), nullable=True),
        sa.Column("application_id", sa.Integer(), nullable=True),
        sa.Column("validator_passed", sa.Boolean(), nullable=True),
        sa.Column("validator_report", sa.Text(), nullable=True),
        sa.Column("built_at", sa.DateTime(timezone=True),
                  server_default=sa.text("now()"), nullable=False),
        sa.Column("built_by", sa.Text(), nullable=True),
        schema=SCHEMA,
    )
    op.create_index(
        "ix_contract_builds_built_at", "contract_builds", ["built_at"], schema=SCHEMA
    )


def downgrade() -> None:
    op.drop_index("ix_contract_builds_built_at", "contract_builds", schema=SCHEMA)
    op.drop_table("contract_builds", schema=SCHEMA)
    op.drop_index("uq_contract_masters_rel_path", "contract_masters", schema=SCHEMA)
    op.drop_table("contract_masters", schema=SCHEMA)
