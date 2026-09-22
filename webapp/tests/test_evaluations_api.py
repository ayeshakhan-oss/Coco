"""Integration tests for the read-only /api/evaluations router (finding 9).

These hit a LIVE database (Nugget's real `public.nugget_screening_*` tables),
so the whole module is skipped when DATABASE_URL isn't available — there is
no way to fake this data, and it isn't Coco's to fixture up. `.env` is loaded
explicitly (mirroring `scripts/screening/read_nugget_screening.py`) because
`webapp.config.Settings` reads `.env` itself without exporting it into
`os.environ`, and the skip guard below only has `os.environ` to check.

`DATABASE_URL` being SET is not the same as the database being REACHABLE. From
this machine, port 5432 is routed through a slow/blocked path (TCP connects
only after ~10-14s per attempt instead of failing fast — see
memory/reference_neon_https_sql_workaround_2026_08_05.md), and this module
opens many such connections (one per test, plus TestClient app startup), which
used to inflate a 1.6s full-suite run to ~414s. The skip guard below runs a
short, BOUNDED raw-socket connect (a couple of seconds) before deciding to run
this module at all, so a slow/blocked path skips fast instead of the whole
module hanging through real (multi-second-per-attempt) connection retries.
Wherever the DB connects quickly (e.g. Railway, or any network with a fast
path to Neon), this still runs normally.

Run:  python -m pytest webapp/tests/test_evaluations_api.py -q
"""

from __future__ import annotations

import os
import socket
import threading
from urllib.parse import urlsplit

import pytest
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

_DATABASE_URL = os.environ.get("DATABASE_URL")
_CONNECT_TIMEOUT_SECONDS = 2.5


def _database_reachable(url: str) -> bool:
    """A bounded, best-effort TCP reachability probe (NOT a full Postgres
    handshake, which the blocked network path here can spend 10+ seconds on
    per attempt even when it eventually succeeds). Any failure — DNS, refused,
    or simply too slow to be worth it in a unit-test run — means "skip".

    `socket.create_connection`'s own `timeout=` only bounds the connect() call,
    NOT the getaddrinfo()/DNS resolution that happens first — and on this
    machine DNS resolution for the Neon hostname alone routinely takes 8-14s,
    so a bare `timeout=` here does not actually bound wall-clock time. The
    probe therefore runs in a DAEMON thread with its own `join(timeout=...)`:
    if it hasn't reported back within the budget, this returns False
    immediately and the daemon thread is abandoned (it cannot block process
    exit), rather than the whole test collection waiting on a slow resolver.
    """
    try:
        parts = urlsplit(url)
        host = parts.hostname
        if not host:
            return False
        port = parts.port or 5432
    except ValueError:
        return False

    outcome: dict[str, bool] = {}

    def _attempt() -> None:
        try:
            with socket.create_connection((host, port), timeout=_CONNECT_TIMEOUT_SECONDS):
                outcome["ok"] = True
        except OSError:
            outcome["ok"] = False

    probe = threading.Thread(target=_attempt, daemon=True)
    probe.start()
    probe.join(timeout=_CONNECT_TIMEOUT_SECONDS)
    return outcome.get("ok", False)


_SKIP_REASON = "needs DATABASE_URL"
if _DATABASE_URL and not _database_reachable(_DATABASE_URL):
    _SKIP_REASON = "DATABASE_URL is set but the database did not respond within " \
        f"{_CONNECT_TIMEOUT_SECONDS}s from this machine — skipping rather than " \
        "hanging through slow/blocked-path connection retries"
    _DATABASE_URL = None

pytestmark = pytest.mark.skipif(not _DATABASE_URL, reason=_SKIP_REASON)


@pytest.fixture(scope="module")
def client():
    """A TestClient with auth forced on for just this module.

    The checked-in `.env` ships `AUTH_DEV_BYPASS=false` (real Google SSO is
    required by default, even in development), so every one of these
    endpoints would 401 without a session cookie. `get_settings()` is
    `lru_cache`d, so flipping the env var alone isn't enough once some other
    test in the same process has already triggered a Settings() build with
    the old value — clear the cache after setting the var, and restore both
    afterwards so this override can't leak into any test file that happens
    to run later in the same session.
    """
    had_var = "AUTH_DEV_BYPASS" in os.environ
    old_value = os.environ.get("AUTH_DEV_BYPASS")
    os.environ["AUTH_DEV_BYPASS"] = "true"

    from webapp.config import get_settings

    get_settings.cache_clear()

    from fastapi.testclient import TestClient

    from webapp.main import app

    with TestClient(app) as c:
        yield c

    if had_var:
        os.environ["AUTH_DEV_BYPASS"] = old_value  # type: ignore[assignment]
    else:
        os.environ.pop("AUTH_DEV_BYPASS", None)
    get_settings.cache_clear()


@pytest.fixture(scope="module")
def db_session():
    """A direct DB session, for tests that need to read a raw column (not
    exposed through any /api/evaluations response) rather than go through
    the read-only router. Module-scoped and closed at teardown, same as the
    `client` fixture above; both talk to the same live DATABASE_URL this
    module is skipped without."""
    from webapp.db import get_sessionmaker

    SessionLocal = get_sessionmaker()
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Job 38 (AI Engineer Lead) and job 13 (Full Stack Developer) are real,
# already-screened jobs in the shared database (confirmed via
# `python scripts/screening/read_nugget_screening.py --list`). Job 38's P4
# tier is a known, stable count (378) at the time these tests were written.
JOB_WITH_P4 = 38
JOB_WITH_MANUAL_REVIEW = 13


def test_jobs_endpoint_lists_screened_jobs(client):
    r = client.get("/api/evaluations/jobs")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)
    assert any(j["job_id"] == JOB_WITH_P4 for j in body)


def test_job_summary_endpoint_includes_unscored_count(client):
    r = client.get(f"/api/evaluations/jobs/{JOB_WITH_MANUAL_REVIEW}/summary")
    assert r.status_code == 200
    body = r.json()
    for key in ("tiers", "scored", "unusable", "unscored", "total"):
        assert key in body
    # Finding 5: MANUAL_REVIEW rows count toward `scored` (unchanged meaning)
    # but must also show up in the new `unscored` count.
    manual_review = next(
        (t for t in body["tiers"] if t["tier"] == "MANUAL_REVIEW"), None
    )
    if manual_review is not None:
        assert manual_review["is_unscored"] is True
        assert body["unscored"] >= manual_review["n"]


def test_job_candidates_endpoint_returns_paged_object_with_total(client):
    r = client.get(
        f"/api/evaluations/jobs/{JOB_WITH_P4}/candidates", params={"tier": "P4"}
    )
    assert r.status_code == 200
    body = r.json()
    # Finding 3: response shape changed from a bare list to {rows, total}.
    assert set(body.keys()) == {"rows", "total"}
    assert isinstance(body["rows"], list)
    assert body["total"] == 378
    assert len(body["rows"]) <= 100  # default page size, well under the total


def test_job_candidates_bogus_tier_is_400(client):
    r = client.get(
        f"/api/evaluations/jobs/{JOB_WITH_P4}/candidates", params={"tier": "BOGUS"}
    )
    assert r.status_code == 400


def test_job_candidates_negative_limit_is_422_not_500(client):
    # Finding 2: `limit` had no lower bound, so `?limit=-1` used to reach
    # Postgres as `LIMIT -1` (SQLSTATE 2201W) and surface as an unhandled 500.
    r = client.get(
        f"/api/evaluations/jobs/{JOB_WITH_P4}/candidates", params={"limit": -1}
    )
    assert r.status_code == 422


def test_job_candidates_over_max_limit_is_still_422(client):
    # Pre-existing upper bound (le=500); confirms fix 2 didn't loosen it.
    r = client.get(
        f"/api/evaluations/jobs/{JOB_WITH_P4}/candidates", params={"limit": 501}
    )
    assert r.status_code == 422


def test_application_evaluation_missing_application_is_404(client):
    r = client.get("/api/evaluations/applications/999999999")
    assert r.status_code == 404


def test_application_evaluation_found_drops_raw_rubric_internals(client):
    # Finding 7: dimension_scores/hard_filter_flags have no frontend consumer
    # and are dropped from the response. Pull a real application id off the
    # candidates list rather than hardcoding one.
    listing = client.get(
        f"/api/evaluations/jobs/{JOB_WITH_MANUAL_REVIEW}/candidates",
        params={"limit": 1},
    )
    assert listing.status_code == 200
    rows = listing.json()["rows"]
    if not rows:
        pytest.skip(f"job {JOB_WITH_MANUAL_REVIEW} has no current evals to fetch")

    app_id = rows[0]["application_id"]
    r = client.get(f"/api/evaluations/applications/{app_id}")
    assert r.status_code == 200
    body = r.json()
    assert "dimension_scores" not in body
    assert "hard_filter_flags" not in body


def test_our_payload_shape_matches_a_real_markaz_scorecard(db_session):
    """Pull a real scorecard and assert our validator accepts it unchanged.

    If Markaz's shape ever drifts, this fails and tells us before we write a
    scorecard nobody can see.
    """
    from sqlalchemy import text

    from webapp.services.values_scoring import validate_markaz_payload

    row = db_session.execute(
        text(
            "SELECT values_scorecard FROM public.applications "
            "WHERE jsonb_typeof(values_scorecard) = 'object' "
            "AND jsonb_typeof(values_scorecard->'values') = 'array' "
            "AND jsonb_array_length(values_scorecard->'values') = 6 "
            "AND jsonb_typeof(values_scorecard->'proceedToRightSeat') = 'string' "
            "ORDER BY id DESC LIMIT 1"
        )
    ).scalar()
    assert row, "no real scorecard found to compare against"
    validate_markaz_payload(row)
