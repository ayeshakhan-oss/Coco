"""initial: app_users + communications

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-15

Creates the two app-owned tables and seeds the initial approvers. The legacy
Talent-Acquisition tables are untouched.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "app_users",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("google_sub", sa.String(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("app_role", sa.String(), nullable=False, server_default="drafter"),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("email", name="uq_app_users_email"),
        sa.UniqueConstraint("google_sub", name="uq_app_users_google_sub"),
        sa.CheckConstraint(
            "email LIKE '%@taleemabad.com'", name="ck_app_users_email_domain"
        ),
        sa.CheckConstraint(
            "app_role IN ('drafter','approver')", name="ck_app_users_role"
        ),
    )

    op.create_table(
        "communications",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("application_id", sa.Integer(), nullable=True),
        sa.Column("candidate_id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.Integer(), nullable=True),
        sa.Column("email_type", sa.String(), nullable=False),
        sa.Column("subject", sa.Text(), nullable=True),
        sa.Column("title_line", sa.Text(), nullable=True),
        sa.Column("role_title", sa.Text(), nullable=True),
        sa.Column("body_html", sa.Text(), nullable=True),
        sa.Column("rendered_html", sa.Text(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="draft"),
        sa.Column("mode", sa.String(), nullable=True),
        sa.Column("word_count", sa.Integer(), nullable=True),
        sa.Column("eval_result", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("eval_passed", sa.Boolean(), nullable=True),
        sa.Column("sent_to", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column("message_id", sa.String(), nullable=True),
        sa.Column("error_detail", sa.Text(), nullable=True),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column("approved_by", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"], ["app_users.id"], name="fk_comm_created_by"
        ),
        sa.ForeignKeyConstraint(
            ["approved_by"], ["app_users.id"], name="fk_comm_approved_by"
        ),
        sa.CheckConstraint(
            "email_type IN ('cv_rejection','values_feedback','warm_bench','gwc_rejection')",
            name="ck_comm_email_type",
        ),
        sa.CheckConstraint(
            "status IN ('draft','in_review','approved','sent','failed')",
            name="ck_comm_status",
        ),
        sa.CheckConstraint(
            "mode IS NULL OR mode IN ('pilot','live')", name="ck_comm_mode"
        ),
    )

    op.create_index("ix_comm_candidate_id", "communications", ["candidate_id"])
    op.create_index("ix_comm_application_id", "communications", ["application_id"])
    op.create_index("ix_comm_job_id", "communications", ["job_id"])
    op.create_index("ix_comm_status", "communications", ["status"])
    op.create_index("ix_comm_email_type", "communications", ["email_type"])
    op.create_index(
        "ix_comm_app_type", "communications", ["application_id", "email_type"]
    )
    op.create_index(
        "ix_comm_sent_app_type",
        "communications",
        ["application_id", "email_type"],
        postgresql_where=sa.text("status = 'sent'"),
    )

    # Seed initial approvers. (Table is newly created, so plain inserts are safe.)
    app_users = sa.table(
        "app_users",
        sa.column("id", sa.String),
        sa.column("email", sa.String),
        sa.column("first_name", sa.String),
        sa.column("last_name", sa.String),
        sa.column("app_role", sa.String),
        sa.column("active", sa.Boolean),
    )
    op.bulk_insert(
        app_users,
        [
            {
                "id": "appuser-seed-ayesha",
                "email": "ayesha.khan@taleemabad.com",
                "first_name": "Ayesha",
                "last_name": "Khan",
                "app_role": "approver",
                "active": True,
            },
            {
                "id": "appuser-seed-jawwad",
                "email": "jawwad.ali@taleemabad.com",
                "first_name": "Jawwad",
                "last_name": "Ali",
                "app_role": "approver",
                "active": True,
            },
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_comm_sent_app_type", table_name="communications")
    op.drop_index("ix_comm_app_type", table_name="communications")
    op.drop_index("ix_comm_email_type", table_name="communications")
    op.drop_index("ix_comm_status", table_name="communications")
    op.drop_index("ix_comm_job_id", table_name="communications")
    op.drop_index("ix_comm_application_id", table_name="communications")
    op.drop_index("ix_comm_candidate_id", table_name="communications")
    op.drop_table("communications")
    op.drop_table("app_users")
