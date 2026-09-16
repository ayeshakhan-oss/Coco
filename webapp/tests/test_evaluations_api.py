"""Integration tests for the read-only /api/evaluations router (finding 9).

These hit a LIVE database (Nugget's real `public.nugget_screening_*` tables),
so the whole module is skipped when DATABASE_URL isn't available — there is
no way to fake this data, and it isn't Coco's to fixture up. `.env` is loaded
explicitly (mirroring `scripts/screening/read_nugget_screening.py`) because
`webapp.config.Settings` reads `.env` itself without exporting it into
`os.environ`, and the skip guard below only has `os.environ` to check.

Run:  python -m pytest webapp/tests/test_evaluations_api.py -q
"""

from __future__ import annotations

import os

import pytest
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"), reason="needs DATABASE_URL"
)


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
