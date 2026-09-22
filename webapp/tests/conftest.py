"""A test run must never issue DDL against a real database.

`webapp.db.ensure_app_tables()` and the lifespan's `Base.metadata.create_all()`
are production self-heal paths: a Neon restore or branch-swap can drop the
app-owned tables while leaving `alembic_version` stamped, so `alembic upgrade`
is a no-op and every read 500s (docs/RAILWAY_DEPLOYMENT_LESSONS.md, incident
2026-06-20). They are idempotent and correct in production and must stay.

Under pytest they are a hazard. On 2026-09-22 `coco.eval_benchmarks` and
`coco.case_study_evaluations` appeared in PRODUCTION created by a local test
run rather than by any migration, which is how alembic and the real schema
drifted apart twice in one day. Nothing was damaged, but a developer running
`pytest` on a feature branch would create that branch's half-finished tables
in the live database.

Two test modules already try to avoid this by constructing `TestClient(app)`
without the `with ...` form, so the lifespan never runs. That is not a guard:

  * it is a comment asking future authors to remember something, and
  * the lifespan is only one of SIX paths to `ensure_app_tables()`. One of the
    others is the READ path (`services/reads.py:45`), which self-heals when a
    query fails on a missing table.

All six call sites import `ensure_app_tables` LOCALLY inside a function body,
so patching the attribute on `webapp.db` intercepts every one of them. That is
what this fixture does, plus the single direct `Base.metadata.create_all` in
the lifespan.

DDL is allowed against SQLite (a scratch database), and against anything at all
when `COCO_ALLOW_TEST_DDL=1` is set deliberately. Everything else is skipped and
counted in `BLOCKED_DDL`, never executed. Skipping is the right failure mode
rather than raising: `reads.py` and `evidence.py` only reach this code on an
error path, and raising there would turn a protected read into a 500 and fail
the live read-only integration suite in `test_evaluations_api.py`.
"""

from __future__ import annotations

import logging

import pytest

import webapp.db as db_mod
from webapp.tests.ddl_guard import ALLOW_ENV, BLOCKED_DDL, bind_url, ddl_is_allowed

_log = logging.getLogger("coco.tests.ddl_guard")


@pytest.fixture(autouse=True, scope="session")
def block_ddl_against_a_real_database():
    from webapp.config import get_settings

    real_ensure = db_mod.ensure_app_tables
    real_create_all = db_mod.Base.metadata.create_all

    def guarded_ensure_app_tables(*args, **kwargs):
        url = get_settings().database_url
        if ddl_is_allowed(url):
            return real_ensure(*args, **kwargs)
        BLOCKED_DDL.append(("ensure_app_tables", url or ""))
        _log.warning(
            "BLOCKED ensure_app_tables() during a test run: it would have issued "
            "DDL against a non-test database. Set %s=1 only if that is genuinely "
            "what you want.",
            ALLOW_ENV,
        )
        return None

    def guarded_create_all(bind=None, *args, **kwargs):
        # Judge the engine actually passed in, not the configured DATABASE_URL:
        # a test that builds its own SQLite engine is doing nothing wrong.
        url = bind_url(bind) if bind is not None else get_settings().database_url
        if ddl_is_allowed(url):
            return real_create_all(bind, *args, **kwargs)
        BLOCKED_DDL.append(("create_all", url or ""))
        _log.warning(
            "BLOCKED Base.metadata.create_all() during a test run: it would have "
            "created app-owned tables in a non-test database.",
        )
        return None

    db_mod.ensure_app_tables = guarded_ensure_app_tables
    db_mod.Base.metadata.create_all = guarded_create_all
    try:
        yield
    finally:
        db_mod.ensure_app_tables = real_ensure
        db_mod.Base.metadata.create_all = real_create_all
