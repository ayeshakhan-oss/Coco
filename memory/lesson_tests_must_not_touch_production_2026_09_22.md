---
name: Running pytest could create tables in PRODUCTION (2026-09-22)
description: "coco.eval_benchmarks and coco.case_study_evaluations appeared in the live database created by a test run, not a migration, which is how alembic and the real schema drifted twice in one day. Six paths reach ensure_app_tables(), one of them the READ path. conftest.py now blocks DDL against any non-SQLite database. Also: the integration suite had been silently dead on a 2.5s probe against a 3.4-7.4s connect, because a skip that always fires is a deleted test that still shows in the count."
type: feedback
---

# A test run must never issue DDL against a real database (2026-09-22)

## What happened

`coco.eval_benchmarks` and `coco.case_study_evaluations` existed in **production**
before any migration created them. They were created by `Base.metadata.create_all()`
running inside a local `pytest` process pointed at the live `DATABASE_URL`. That is
why alembic said `0008` while the tables of `0009`/`0010` already existed, and why
`alembic upgrade head` then failed on a `CREATE TABLE` and advanced nothing.

Nothing was damaged: `create_all` only adds missing tables, never drops or alters.
But a developer running the suite on a feature branch would have created that
branch's half-finished tables in the live database.

## Why the existing defence was not one

Two test modules already avoided it, with a comment:

> `TestClient(app)` is built WITHOUT the `with ... as client:` context-manager form
> on purpose ... entering that context runs `webapp.main.lifespan`, whose startup
> self-heal calls `Base.metadata.create_all()`.

That is a note asking future authors to remember something, and it is also
**incomplete**: the lifespan is one of **six** paths to `ensure_app_tables()`.

```
webapp/main.py:47              scheduler
webapp/main.py:79              lifespan
webapp/routers/gmail_sync.py   an endpoint
webapp/services/evidence.py    error path
webapp/services/gmail_evidence.py
webapp/services/reads.py:45    THE READ PATH  <- self-heals when a query hits a missing table
```

## The fix, and why it works

All six do `from ..db import ensure_app_tables` **inside a function body**, so they
resolve the attribute at call time. Patching it on `webapp.db` intercepts every one.

`webapp/tests/conftest.py` holds an autouse session fixture that wraps
`ensure_app_tables` and `Base.metadata.create_all`. DDL is allowed against **SQLite**
or under an explicit `COCO_ALLOW_TEST_DDL=1`; everything else is **skipped and
counted**, never executed.

**Skipping, not raising, is deliberate.** `reads.py` and `evidence.py` reach that code
only on an error path, and raising there would turn a protected read into a 500 and
fail the live read-only integration suite.

`create_all`'s guard judges **the engine actually passed in**, not the configured
`DATABASE_URL`, so a test that builds its own SQLite engine is unaffected.

## Three things this cost me, worth keeping

**1. pytest loads `conftest.py` under its own module identity.** `from
webapp.tests.conftest import BLOCKED_DDL` builds a **second copy** of the module with
its own empty list. My first proof test failed while the guard was working perfectly
and logging both blocks. Shared state between a conftest and a test belongs in a
**normal module** (`webapp/tests/ddl_guard.py`), not in conftest.

**2. The proof must run the thing that broke.**
`test_ddl_guard.py::test_the_lifespan_that_caused_the_incident_is_now_refused` runs
the exact `with TestClient(app)` pattern against a production-shaped URL and asserts
both operations were refused. A guard that has only ever passed proves nothing.

**3. SQLAlchemy's `str(url)` masks the password**, so the blocked-DDL log can never
leak a credential into a test report. Asserted rather than assumed.

## The second defect, found on the way

`test_evaluations_api.py` bounded its reachability probe at **2.5s**. A cold connect
to Neon from this machine takes **3.4 to 7.4s**. The suite was not flaky, it was
**silently dead**: all 9 tests skipped on every local run reporting *"the database
did not respond"*, while the database was reachable the whole time. At a 20s ceiling
they ran and passed against live data for the first time.

🔑 **A skip that always fires is a deleted test that still shows up in the count.**
The budget is a ceiling, not a cost: `probe.join()` returns as soon as the connection
succeeds, so only a genuinely offline run waits it out.

## Connectivity, corrected

Repo memory says port 5432 is blocked from this machine. It is **intermittent**, not
blocked: a socket probe connected twice (3.4s, 7.4s) and the 9 integration tests ran
against production for 7 minutes, while `psycopg` minutes later reported *"Network is
unreachable"* for both A records and then a DNS failure. So:

- **alembic cannot be relied on locally.** Apply migrations over the Neon HTTPS
  `/sql` endpoint (`reference_neon_https_sql_workaround_2026_08_05.md`, in the user-level memory directory rather than this repo).
- **But a local test run CAN reach production**, which is exactly why the guard
  above is needed rather than merely tidy.

See [candidate_evaluation_all_six_subskills_2026_09_23.md](candidate_evaluation_all_six_subskills_2026_09_23.md).
