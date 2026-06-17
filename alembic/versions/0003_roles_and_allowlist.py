"""roles viewer/editor/approver/super_admin + reseed

Revision ID: 0003_roles
Revises: 0002_draft_content
Create Date: 2026-06-18

Expands app_users.app_role to 4 tiers and reseeds the initial team:
ayesha=super_admin, jawwad=approver, aymen=approver. Login is allowlist-only
(enforced in app code: a Google identity must already exist + be active).
"""

from __future__ import annotations

from alembic import op

revision = "0003_roles"
down_revision = "0002_draft_content"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Widen the role CHECK to the 4 tiers.
    op.drop_constraint("ck_app_users_role", "app_users", type_="check")
    op.create_check_constraint(
        "ck_app_users_role",
        "app_users",
        "app_role IN ('viewer','editor','approver','super_admin')",
    )
    op.alter_column("app_users", "app_role", server_default="viewer")

    # Migrate existing data + reseed the team.
    op.execute("UPDATE app_users SET app_role = 'editor' WHERE app_role = 'drafter'")
    op.execute("UPDATE app_users SET app_role = 'super_admin' WHERE email = 'ayesha.khan@taleemabad.com'")
    op.execute("UPDATE app_users SET app_role = 'approver' WHERE email = 'jawwad.ali@taleemabad.com'")
    op.execute(
        """
        INSERT INTO app_users (id, email, first_name, last_name, app_role, active)
        VALUES ('appuser-seed-aymen', 'aymen.abid@taleemabad.com', 'Aymen', 'Abid', 'approver', true)
        ON CONFLICT (email) DO UPDATE SET app_role = 'approver', active = true
        """
    )


def downgrade() -> None:
    op.execute("UPDATE app_users SET app_role = 'approver' WHERE app_role = 'super_admin'")
    op.execute("UPDATE app_users SET app_role = 'drafter' WHERE app_role IN ('editor','viewer')")
    op.drop_constraint("ck_app_users_role", "app_users", type_="check")
    op.create_check_constraint(
        "ck_app_users_role", "app_users", "app_role IN ('drafter','approver')"
    )
    op.alter_column("app_users", "app_role", server_default="drafter")
