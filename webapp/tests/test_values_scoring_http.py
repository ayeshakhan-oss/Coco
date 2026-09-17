"""HTTP-level tests for the values-scorecard router (Task 6 test-quality fix).

Every test in `test_values_scoring.py` that exercises `generate`/`get_draft`/
`edit_draft`/`submit` calls the route FUNCTION directly with a hand-made
`{"id": ...}` user dict, bypassing FastAPI's dependency resolution entirely.
That is deliberate and documented there (fast, no-DB unit tests of the
router's own logic) -- but it also means NO test in this project has ever
sent a real HTTP request through the real dependency graph and checked the
status code a wrong role actually gets back. A route whose `Depends(...)`
was quietly swapped for the wrong gate would still pass every test in that
file, because the fake `user` dict is handed straight to the function body
and the `Depends(require_approver)` declaration is never evaluated at all.

These tests close that gap with `TestClient` + `app.dependency_overrides`:
a real request is routed, FastAPI resolves the real dependant tree
(`require_editor`/`require_approver` -> `get_current_user`), and only the
identity of `get_current_user` is swapped out. `require_editor`,
`require_approver`, and the route's role check itself all run for real.

No live database anywhere in this file: `get_db` is overridden with the
same in-memory `_FakeSession` used by the direct route-function tests in
`test_values_scoring.py`, imported from there rather than reimplemented, so
nothing here opens a real connection, writes to `public.applications`, or
needs `DATABASE_URL` to be set.

`TestClient(app)` is built WITHOUT the `with ... as client:` context-manager
form on purpose. Entering that context runs `webapp.main.lifespan`, whose
startup self-heal calls `Base.metadata.create_all()` against
`settings.database_url` if one happens to be configured in the environment
running the tests -- a real DB touch this file must never risk. A bare
`TestClient(app)` serves requests without ever running that lifespan (see
`/healthz` returning fine under the same construction, no DB required).
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import webapp.deps as deps
from webapp.db import get_db
from webapp.main import app
from webapp.tests.test_values_scoring import _FakeSession, _make_draft

PREFIX = "/api/values-scorecards"


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
# B) real 403s for the wrong role, through the real dependency graph.
# ---------------------------------------------------------------------------


def test_viewer_is_rejected_from_generate(client):
    _override_user("viewer")
    _override_db(_FakeSession())
    r = client.post(
        f"{PREFIX}/generate",
        json={"application_id": 101, "transcript": "x" * 3000, "host": "Ayesha Khan"},
    )
    assert r.status_code == 403


def test_viewer_is_rejected_from_get_draft(client):
    _override_user("viewer")
    db = _FakeSession()
    db._store["vsd-http-1"] = _make_draft(id="vsd-http-1")
    _override_db(db)
    r = client.get(f"{PREFIX}/vsd-http-1")
    assert r.status_code == 403


def test_viewer_is_rejected_from_edit_draft(client):
    _override_user("viewer")
    db = _FakeSession()
    db._store["vsd-http-2"] = _make_draft(id="vsd-http-2")
    _override_db(db)
    r = client.patch(f"{PREFIX}/vsd-http-2", json={"final_comments": "x"})
    assert r.status_code == 403


def test_viewer_is_rejected_from_submit(client):
    _override_user("viewer")
    db = _FakeSession()
    db._store["vsd-http-3"] = _make_draft(id="vsd-http-3")
    _override_db(db)
    r = client.post(f"{PREFIX}/vsd-http-3/submit")
    assert r.status_code == 403


def test_editor_is_rejected_from_submit(client):
    """The gate this whole file exists to protect: an editor can generate,
    read, and edit a draft, but must never be able to submit it -- that is
    Ayesha's deliberate approver-only bar for writing a permanent Markaz
    hiring record (router docstring rule 1)."""
    _override_user("editor")
    db = _FakeSession()
    db._store["vsd-http-4"] = _make_draft(id="vsd-http-4")
    _override_db(db)
    r = client.post(f"{PREFIX}/vsd-http-4/submit")
    assert r.status_code == 403


def test_approver_passes_the_submit_gate(client):
    _override_user("approver")
    db = _FakeSession()
    db._store["vsd-http-5"] = _make_draft(id="vsd-http-5", application_id=9001)
    _override_db(db)
    r = client.post(f"{PREFIX}/vsd-http-5/submit")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "submitted"
    assert body["markaz_payload"]["candidateName"] == "Amina Raza"
    assert db.committed == 1
    assert db.rolled_back == 0


def test_approver_can_still_reach_the_lower_editor_gate(client):
    """approver outranks editor (webapp/deps.py ROLE_LEVEL), so it must also
    clear `require_editor` on generate/get/patch -- a route gated on
    `require_approver` is a stricter bar, never a different, incompatible
    one."""
    _override_user("approver")
    db = _FakeSession()
    db._store["vsd-http-6"] = _make_draft(id="vsd-http-6")
    _override_db(db)
    r = client.get(f"{PREFIX}/vsd-http-6")
    assert r.status_code == 200
    assert r.json()["id"] == "vsd-http-6"


# ---------------------------------------------------------------------------
# C) the `overwrite` flag through REAL request-body parsing (TestClient),
# not a hand-built ValuesScorecardSubmitRequest(...) instance.
# ---------------------------------------------------------------------------


def test_submit_with_no_body_at_all_still_refuses_an_existing_scorecard(client):
    """The route's default is `ValuesScorecardSubmitRequest()` (overwrite
    defaults to False) so a plain POST with no JSON body at all -- the
    common case, no client sends a body for a normal submit -- must still be
    parsed as overwrite=False, not error out on a missing body."""
    _override_user("approver")
    db = _FakeSession()
    db._store["vsd-http-7"] = _make_draft(id="vsd-http-7", application_id=9002)
    db.applications_row = {
        "values_scorecard": {"candidateName": "Someone Else"},
        "candidate_id": None,
        "job_id": None,
    }
    _override_db(db)
    r = client.post(f"{PREFIX}/vsd-http-7/submit")
    assert r.status_code == 409
    assert "9002" in r.json()["detail"]
    assert db.committed == 0


def test_submit_with_overwrite_false_explicit_in_the_body_still_refuses(client):
    _override_user("approver")
    db = _FakeSession()
    db._store["vsd-http-8"] = _make_draft(id="vsd-http-8", application_id=9003)
    db.applications_row = {
        "values_scorecard": {"candidateName": "Someone Else"},
        "candidate_id": None,
        "job_id": None,
    }
    _override_db(db)
    r = client.post(f"{PREFIX}/vsd-http-8/submit", json={"overwrite": False})
    assert r.status_code == 409
    assert db.committed == 0


def test_submit_with_overwrite_true_replaces_and_preserves_the_prior_payload(client):
    """The one path that must actually succeed once an existing Markaz
    scorecard is found: `overwrite: true`, parsed from a real JSON body
    through FastAPI's own Pydantic model, not constructed in Python and
    passed straight to the function."""
    _override_user("approver")
    db = _FakeSession()
    db._store["vsd-http-9"] = _make_draft(
        id="vsd-http-9", application_id=9004, candidate_name="Zara Iqbal"
    )
    prior = {"candidateName": "Someone Else", "finalComments": "an old human-written scorecard"}
    db.applications_row = {"values_scorecard": prior, "candidate_id": None, "job_id": None}
    _override_db(db)
    r = client.post(f"{PREFIX}/vsd-http-9/submit", json={"overwrite": True})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "submitted"
    assert body["markaz_payload"]["candidateName"] == "Zara Iqbal"
    assert body["replaced_payload"] == prior
    assert db.committed == 1


def test_submit_overwrite_flag_rejects_a_non_boolean_value(client):
    """Real Pydantic request parsing (the thing this section exists to
    exercise) also means a body FastAPI itself refuses is exercised, not
    just the two accepted values."""
    _override_user("approver")
    db = _FakeSession()
    db._store["vsd-http-10"] = _make_draft(id="vsd-http-10", application_id=9005)
    _override_db(db)
    r = client.post(f"{PREFIX}/vsd-http-10/submit", json={"overwrite": "yes please"})
    assert r.status_code == 422
    assert db.committed == 0
