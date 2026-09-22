"""The conftest DDL guard must actually stop a test run writing to production.

A gate that has only ever passed proves nothing (CLAUDE.md Rule 25), so these
tests do not merely check the predicate: the last one runs the exact pattern
that caused the 2026-09-22 incident -- `with TestClient(app)`, which triggers
`webapp.main.lifespan` and its `ensure_app_tables()` + `create_all()` self-heal
-- against a production-shaped DATABASE_URL, and asserts the DDL was refused.

Run: python -m pytest webapp/tests/test_ddl_guard.py -v
"""

from __future__ import annotations

import os

import pytest

import webapp.db as db_mod
from webapp.tests.ddl_guard import ALLOW_ENV, BLOCKED_DDL, ddl_is_allowed

PROD_SHAPED_URL = "postgresql://u:p@ep-example-pooler.eu-central-1.aws.neon.tech/db"


def test_the_predicate_blocks_a_real_database_and_allows_a_scratch_one():
    assert ddl_is_allowed("sqlite:///:memory:") is True
    assert ddl_is_allowed("sqlite+pysqlite:///./scratch.db") is True
    assert ddl_is_allowed(PROD_SHAPED_URL) is False
    assert ddl_is_allowed("postgresql+psycopg://u:p@host/db") is False
    # No database configured is not ours to swallow: get_engine() still raises.
    assert ddl_is_allowed(None) is True
    assert ddl_is_allowed("") is True


def test_the_opt_out_works_so_a_deliberate_test_database_is_still_usable(monkeypatch):
    monkeypatch.setenv(ALLOW_ENV, "1")
    assert ddl_is_allowed(PROD_SHAPED_URL) is True


def test_the_guard_is_actually_installed_on_the_module_every_call_site_imports():
    """All six callers do `from ..db import ensure_app_tables` inside a function
    body, so they resolve this attribute at call time. If it is the unpatched
    original, none of them are covered."""
    assert db_mod.ensure_app_tables.__name__ == "guarded_ensure_app_tables", (
        "conftest's session fixture did not patch webapp.db.ensure_app_tables; "
        "every DDL path is unguarded"
    )


def _reset_engine() -> None:
    """The lifespan builds an Engine from whatever DATABASE_URL is set. Drop it
    so a fake URL cannot leak into any test that runs later in this session."""
    db_mod._engine = None
    db_mod._SessionLocal = None


def test_the_lifespan_that_caused_the_incident_is_now_refused(monkeypatch):
    """`with TestClient(app)` runs the startup self-heal. Before the guard this
    created coco.eval_benchmarks and coco.case_study_evaluations in the LIVE
    database from a local test run. It must now be blocked."""
    from fastapi.testclient import TestClient

    from webapp.config import get_settings

    monkeypatch.setenv("DATABASE_URL", PROD_SHAPED_URL)
    monkeypatch.setenv("AUTH_DEV_BYPASS", "true")
    get_settings.cache_clear()
    _reset_engine()

    before = len(BLOCKED_DDL)
    try:
        from webapp.main import app

        with TestClient(app) as c:
            assert c.get("/healthz").status_code == 200
    finally:
        get_settings.cache_clear()
        _reset_engine()

    blocked = BLOCKED_DDL[before:]
    ops = {op for op, _ in blocked}

    assert "ensure_app_tables" in ops, (
        "the lifespan self-heal reached ensure_app_tables() unguarded -- it would "
        f"have issued CREATE SCHEMA / CREATE TABLE against {PROD_SHAPED_URL}"
    )
    assert "create_all" in ops, (
        "the lifespan's Base.metadata.create_all() ran unguarded against a "
        "production-shaped database URL"
    )
    # Both records point at the database we refused to touch. The create_all
    # record is SQLAlchemy's own str(url), which MASKS the password -- so the
    # blocked-DDL log can never leak a credential into a test report.
    assert all("ep-example-pooler" in url for _, url in blocked), blocked
    assert not any(":p@" in url for op, url in blocked if op == "create_all"), (
        "a database password was recorded verbatim in BLOCKED_DDL"
    )
