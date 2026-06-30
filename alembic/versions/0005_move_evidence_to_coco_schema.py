"""Move comm_evidence + gmail_sync_runs into a dedicated `coco` schema

Revision ID: 0005_coco_schema
Revises: 0004_gmail_sync
Create Date: 2026-06-30

Root cause (found 2026-06-30): Markaz is hosted on Replit, and Replit's
per-deploy schema push prunes `public` tables it doesn't recognise — which
repeatedly dropped Coco's `comm_evidence` + `gmail_sync_runs` (added in 0004),
blanking the dashboard. Replit's own `_system` schema survives every deploy, so
moving Coco's evidence tables into a dedicated `coco` schema takes them out of
that blast radius. Cross-schema reads/joins to `public` (applications,
candidates, app_users) keep working natively; all SQL references are qualified
as `coco.<table>` in the app.

Idempotent: handles a fresh upgrade (0004 made them in public -> move to coco),
a DB where the app already self-healed them into coco (drop the public orphans),
or a partial state.
"""

from __future__ import annotations

from alembic import op

revision = "0005_coco_schema"
down_revision = "0004_gmail_sync"
branch_labels = None
depends_on = None

_TABLES = ("comm_evidence", "gmail_sync_runs")


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS coco")
    for t in _TABLES:
        # If it exists in public AND coco doesn't have it yet -> move it (keeps
        # data + indexes). If both exist -> drop the public orphan. If only coco
        # exists -> nothing to do.
        op.execute(
            f"""
            DO $$
            BEGIN
              IF to_regclass('public.{t}') IS NOT NULL
                 AND to_regclass('coco.{t}') IS NULL THEN
                EXECUTE 'ALTER TABLE public.{t} SET SCHEMA coco';
              ELSIF to_regclass('public.{t}') IS NOT NULL
                 AND to_regclass('coco.{t}') IS NOT NULL THEN
                EXECUTE 'DROP TABLE public.{t} CASCADE';
              END IF;
            END $$;
            """
        )


def downgrade() -> None:
    for t in _TABLES:
        op.execute(
            f"""
            DO $$
            BEGIN
              IF to_regclass('coco.{t}') IS NOT NULL
                 AND to_regclass('public.{t}') IS NULL THEN
                EXECUTE 'ALTER TABLE coco.{t} SET SCHEMA public';
              END IF;
            END $$;
            """
        )
    # Leave the (now empty) coco schema in place; dropping it is not safe to assume.
