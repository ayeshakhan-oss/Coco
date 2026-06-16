"""Alembic environment for the Coco webapp.

Manages ONLY the two app-owned tables (app_users, communications). The legacy
Talent-Acquisition tables are excluded from autogenerate so Alembic never tries
to drop or alter them.

Connection URL comes from webapp settings (DATABASE_URL). For offline SQL
generation (`alembic upgrade head --sql`) a placeholder URL is used when
DATABASE_URL is unset, so DDL can be reviewed without a live database.
"""

from __future__ import annotations

import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Make `import webapp...` resolve when alembic runs from the repo root.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from webapp.config import get_settings  # noqa: E402
from webapp.db import Base, _normalize_url  # noqa: E402
import webapp.models  # noqa: E402,F401  (registers tables on Base.metadata)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Tables this Alembic environment is allowed to manage.
MANAGED_TABLES = {"app_users", "communications"}

_PLACEHOLDER_OFFLINE_URL = "postgresql+psycopg://user:pass@localhost:5432/neondb"


def _get_url() -> str:
    settings = get_settings()
    if settings.database_url:
        return _normalize_url(settings.database_url)
    # No DB configured — only valid for offline `--sql` rendering.
    return _PLACEHOLDER_OFFLINE_URL


def include_object(obj, name, type_, reflected, compare_to):
    if type_ == "table":
        return name in MANAGED_TABLES
    return True


def run_migrations_offline() -> None:
    context.configure(
        url=_get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    settings = get_settings()
    if not settings.database_url:
        raise RuntimeError(
            "DATABASE_URL is not set — refusing to run migrations against the "
            "localhost placeholder. Set DATABASE_URL in the environment."
        )
    section = config.get_section(config.config_ini_section, {})
    section["sqlalchemy.url"] = _normalize_url(settings.database_url)
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
