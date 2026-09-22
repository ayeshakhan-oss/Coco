"""HTTP-level tests for the case-study router (Task 6), mirroring
webapp/tests/test_values_scoring_http.py's TestClient + app.dependency_overrides
pattern -- see that file's docstring for why route-FUNCTION tests (in
test_case_study_scoring.py) are not enough on their own: they call the route
function directly with a hand-built user dict, bypassing FastAPI's dependency
resolution entirely, so a route whose `Depends(...)` was quietly swapped for
the wrong gate would still pass every one of those tests.

These tests close that gap: a REAL request is routed, FastAPI resolves the
REAL dependant tree (`require_editor`/`require_approver` -> `get_current_user`),
and only the identity of `get_current_user` is swapped out via
`app.dependency_overrides`. `require_editor`, `require_approver`, and each
route's own role check all run for real.

No live database anywhere in this file: `get_db` is overridden with the same
in-memory `_FakeCaseStudySession` used by the direct route-function tests in
`test_case_study_scoring.py`, imported from there rather than reimplemented.

`TestClient(app)` is built WITHOUT the `with ... as client:` context-manager
form on purpose, for the same reason as test_values_scoring_http.py: entering
that context runs `webapp.main.lifespan`, whose startup self-heal calls
`Base.metadata.create_all()` against `settings.database_url` if one happens to
be configured in the environment running the tests -- a real DB touch this
file must never risk.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import webapp.deps as deps
import webapp.routers.case_studies as router_mod
from webapp.db import get_db
from webapp.main import app
from webapp.models import EvalBenchmark
from webapp.tests.test_case_study_scoring import (
    _all,
    _fake_case_study_app_row,
    _good_evidence,
    _FakeCaseStudySession,
)

PREFIX = "/api/case-studies"


def _user(role: str, uid: str = "appuser-http-test") -> dict:
    return {"id": uid, "email": f"{uid}@example.com", "app_role": role}


@pytest.fixture
def client():
    """A plain (no-lifespan) TestClient. `dependency_overrides` is cleared in
    teardown unconditionally, so an override set by one test can never leak
    into the next regardless of how that test exits (pass, fail, or raise)."""
    c = TestClient(app)
    try:
        yield c
    finally:
        app.dependency_overrides.clear()


def _override_user(role: str) -> None:
    app.dependency_overrides[deps.get_current_user] = lambda: _user(role)


def _override_db(fake_session) -> None:
    def _fake_get_db():
        yield fake_session

    app.dependency_overrides[get_db] = _fake_get_db


# ---------------------------------------------------------------------------
# Real 403s for the wrong role, through the real dependency graph.
# ---------------------------------------------------------------------------


def test_viewer_is_rejected_from_create_benchmark(client):
    _override_user("viewer")
    _override_db(_FakeCaseStudySession())
    r = client.post(f"{PREFIX}/benchmarks", json={"job_id": 7, "title": "t", "body": "the case text"})
    assert r.status_code == 403


def test_viewer_is_rejected_from_approve_benchmark(client):
    _override_user("viewer")
    _override_db(_FakeCaseStudySession())
    r = client.post(f"{PREFIX}/benchmarks/benchmark-1/approve")
    assert r.status_code == 403


def test_viewer_is_rejected_from_score(client):
    _override_user("viewer")
    _override_db(_FakeCaseStudySession())
    r = client.post(f"{PREFIX}/score", json={"application_id": 555})
    assert r.status_code == 403


def test_viewer_is_rejected_from_get_evaluation(client):
    _override_user("viewer")
    _override_db(_FakeCaseStudySession())
    r = client.get(f"{PREFIX}/evaluations/cse-1")
    assert r.status_code == 403


def test_editor_is_rejected_from_approve_benchmark(client):
    """The gate this file exists to protect: an editor can create a
    benchmark and score against an already-approved one, but must never be
    able to APPROVE one -- that is Ayesha's deliberate approver-only bar
    (router docstring rule 1), the same shape as Phase 2's approver-only
    submit gate on values scorecards."""
    _override_user("editor")
    db = _FakeCaseStudySession()
    db._store["benchmark-1"] = EvalBenchmark(
        id="benchmark-1", job_id=7, kind="case_study", title="t", body="b",
        created_by="appuser-editor", status="draft",
    )
    _override_db(db)
    r = client.post(f"{PREFIX}/benchmarks/benchmark-1/approve")
    assert r.status_code == 403


def test_editor_passes_the_create_benchmark_gate(client):
    _override_user("editor")
    _override_db(_FakeCaseStudySession())
    r = client.post(f"{PREFIX}/benchmarks", json={"job_id": 7, "title": "t", "body": "the case text"})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "draft"
    assert body["qa_approved_at"] is None


def test_approver_passes_the_approve_gate(client):
    _override_user("approver")
    db = _FakeCaseStudySession()
    db._store["benchmark-http-1"] = EvalBenchmark(
        id="benchmark-http-1", job_id=7, kind="case_study", title="t", body="b",
        created_by="appuser-editor", status="draft",
    )
    _override_db(db)
    r = client.post(f"{PREFIX}/benchmarks/benchmark-http-1/approve")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "approved"
    assert body["qa_approved_by"] is not None
    assert body["qa_approved_at"] is not None


def test_approver_can_still_reach_the_lower_editor_gate_on_score(client, monkeypatch):
    """approver outranks editor (webapp/deps.py ROLE_LEVEL), so it must also
    clear `require_editor` on /score and GET /evaluations/{id} -- a route
    gated on `require_approver` is a stricter bar, never a different,
    incompatible one."""
    _override_user("approver")
    monkeypatch.setattr(
        router_mod.reads, "get_application", lambda db, app_id: _fake_case_study_app_row(app_id)
    )
    monkeypatch.setattr(
        router_mod, "corpus_for",
        lambda app_id, *, db=None: {
            "text": "submission text " * 50, "sources": ["Gmail attachment: case.docx"],
            "chars": 800, "usable": True,
        },
    )
    monkeypatch.setattr(
        router_mod, "score_submission",
        lambda **kw: {
            "scores": _all(4), "evidence": _good_evidence(), "flags": [],
            "total": 80.0, "band": "strong_yes", "model": "test-model",
        },
    )
    db = _FakeCaseStudySession()
    db.approved_benchmark_row = {"id": "benchmark-approved-http", "body": "the answer key"}
    _override_db(db)

    r = client.post(f"{PREFIX}/score", json={"application_id": 555})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 80.0
    assert body["band"] == "strong_yes"
    assert body["benchmark_id"] == "benchmark-approved-http"


def test_approver_can_read_an_evaluation(client):
    _override_user("approver")
    db = _FakeCaseStudySession()
    from webapp.models import CaseStudyEvaluation

    db._store["cse-http-1"] = CaseStudyEvaluation(
        id="cse-http-1", application_id=555, job_id=7, benchmark_id="benchmark-1",
        candidate_name="Zara Khan", role="Growth Manager",
        scores=_all(3), evidence=_good_evidence(), flags=[],
        total=60.0, band="yes", model_name="test-model",
        sources=["Gmail attachment: case.docx"], created_by="appuser-editor",
    )
    _override_db(db)
    r = client.get(f"{PREFIX}/evaluations/cse-http-1")
    assert r.status_code == 200
    assert r.json()["id"] == "cse-http-1"


# ---------------------------------------------------------------------------
# RULE 0, through a REAL request -- not just the route-function test in
# test_case_study_scoring.py.
# ---------------------------------------------------------------------------


def test_score_409s_through_real_http_when_no_approved_benchmark_exists(client, monkeypatch):
    _override_user("editor")
    monkeypatch.setattr(
        router_mod.reads, "get_application", lambda db, app_id: _fake_case_study_app_row(app_id)
    )
    db = _FakeCaseStudySession()
    db.approved_benchmark_row = None
    _override_db(db)

    r = client.post(f"{PREFIX}/score", json={"application_id": 555})
    assert r.status_code == 409
    assert "Rule 0" in r.json()["detail"]


def test_score_409s_through_real_http_for_a_draft_only_benchmark(client, monkeypatch):
    """Same real-request proof for the draft-invisibility case."""
    _override_user("editor")
    monkeypatch.setattr(
        router_mod.reads, "get_application", lambda db, app_id: _fake_case_study_app_row(app_id)
    )
    db = _FakeCaseStudySession()
    db._store["benchmark-draft-http"] = EvalBenchmark(
        id="benchmark-draft-http", job_id=7, kind="case_study", title="t", body="b",
        created_by="x", status="draft",
    )
    _override_db(db)

    r = client.post(f"{PREFIX}/score", json={"application_id": 555})
    assert r.status_code == 409


def test_get_benchmark_body_never_leaks_through_a_score_409(client, monkeypatch):
    """Belt-and-suspenders: a 409 response must never accidentally include a
    draft benchmark's body text (it hasn't been QA'd -- nothing about it
    should be user-visible yet beyond its existence)."""
    _override_user("editor")
    monkeypatch.setattr(
        router_mod.reads, "get_application", lambda db, app_id: _fake_case_study_app_row(app_id)
    )
    db = _FakeCaseStudySession()
    db._store["benchmark-secret"] = EvalBenchmark(
        id="benchmark-secret", job_id=7, kind="case_study", title="t",
        body="UNAPPROVED SENSITIVE ANSWER KEY TEXT", created_by="x", status="draft",
    )
    _override_db(db)

    r = client.post(f"{PREFIX}/score", json={"application_id": 555})
    assert r.status_code == 409
    assert "UNAPPROVED SENSITIVE ANSWER KEY TEXT" not in r.text
