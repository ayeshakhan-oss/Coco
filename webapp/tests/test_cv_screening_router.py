"""HTTP-level tests for the CV-screening router.

Two lessons are baked in here.

1. A gate test that reads the source is not a gate test. `assert
   "require_editor" in src` once matched a MODULE DOCSTRING and passed while
   the route carried the wrong dependency. These assert on
   `route.dependant.dependencies` -- the tree FastAPI actually resolves -- and
   `test_the_gate_bites` proves the assertion fails when the gate is swapped.

2. `TestClient(app)` is built WITHOUT the `with ... as client:` form. Entering
   that context runs the lifespan. webapp/tests/conftest.py now blocks the DDL
   that used to cause, but not running it at all is still the right default for
   a test that has no business booting the app.

Run: python -m pytest webapp/tests/test_cv_screening_router.py -v
"""

from __future__ import annotations

import datetime as dt

import pytest
from fastapi.testclient import TestClient

import webapp.deps as deps
import webapp.routers.cv_screening as router_mod
from webapp.db import get_db
from webapp.main import app

PREFIX = "/api/cv-screening"


def _user(role: str, uid: str = "appuser-cv-test") -> dict:
    return {"id": uid, "email": f"{uid}@example.com", "app_role": role}


class _Result:
    def __init__(self, rows: list[dict]):
        self._rows = rows

    def mappings(self):
        return self

    def all(self):
        return list(self._rows)

    def first(self):
        return self._rows[0] if self._rows else None

    def __iter__(self):
        return iter(self._rows)

    def scalar_one(self):
        return self._rows[0] if self._rows else 0


class _FakeSession:
    """Records every statement so a test can assert WHAT was executed, not
    only what came back."""

    def __init__(self, responses=None):
        self.responses = responses or {}
        self.executed: list[tuple[str, dict]] = []
        self.added: list = []
        self.committed = False
        self.flushed = False

    def execute(self, stmt, params=None):
        sql = " ".join(str(stmt).split())
        self.executed.append((sql, params or {}))
        for needle, rows in self.responses.items():
            if needle in sql:
                return _Result(rows)
        return _Result([])

    def add(self, obj):
        self.added.append(obj)

    def flush(self):
        self.flushed = True
        for obj in self.added:
            if getattr(obj, "id", None) is None:
                obj.id = "cvs-generated-in-flush"

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        pass

    def close(self):
        pass


@pytest.fixture
def client():
    c = TestClient(app)
    try:
        yield c
    finally:
        app.dependency_overrides.clear()


def _as(role: str, session: _FakeSession | None = None):
    app.dependency_overrides[deps.get_current_user] = lambda: _user(role)
    app.dependency_overrides[get_db] = lambda: session or _FakeSession()


# --------------------------------------------------------------------------
# The gates, asserted on the tree FastAPI actually resolves
# --------------------------------------------------------------------------


def _dependencies(path: str, method: str) -> set:
    """The dependency CALLABLES FastAPI resolves for this route.

    Identity, not names. `require_editor`, `require_approver` and
    `require_super_admin` are all closures produced by `deps._require_role`, so
    every one of them is called `dep` -- a name-based assertion cannot tell an
    editor gate from an approver gate and would pass on either. Comparing the
    function object itself is exact.

    Read off `router_mod.router.routes` rather than `app.routes`: this FastAPI
    wraps each included router in an opaque `fastapi.routing._IncludedRouter`
    exposing no `path` or `routes`, so walking the app finds nothing. The tree
    is the same -- `APIRoute.__init__` builds it via `get_dependant()` at
    declaration and `include_router` does not strip it. The behavioural tests
    below drive the full served path as well.
    """
    for route in router_mod.router.routes:
        if getattr(route, "path", None) == path and method in (
            getattr(route, "methods", None) or set()
        ):
            return {d.call for d in route.dependant.dependencies if getattr(d, "call", None)}
    raise AssertionError(f"route not found: {method} {path}")


def test_screening_requires_an_editor():
    assert deps.require_editor in _dependencies(f"{PREFIX}/screen", "POST")


def test_reading_requires_only_a_signed_in_user():
    for path in (f"{PREFIX}/criteria", f"{PREFIX}/jobs", f"{PREFIX}/screens"):
        found = _dependencies(path, "GET")
        assert deps.get_current_user in found
        assert deps.require_editor not in found
        assert deps.require_approver not in found


def test_the_gate_bites():
    """Proof the assertion above is load-bearing: a read route gated only on
    get_current_user must NOT satisfy the editor assertion."""
    with pytest.raises(AssertionError):
        assert deps.require_editor in _dependencies(f"{PREFIX}/jobs", "GET")


def test_the_gates_are_distinguishable_from_each_other():
    """The reason this file compares callables instead of names: every gate
    `deps._require_role` returns is named `dep`, so a name-based assertion
    would report an approver gate as an editor gate."""
    assert deps.require_editor.__name__ == deps.require_approver.__name__ == "dep"
    assert deps.require_editor is not deps.require_approver
    assert deps.require_approver not in _dependencies(f"{PREFIX}/screen", "POST")


def test_a_viewer_is_refused_screening(client):
    _as("viewer")
    r = client.post(f"{PREFIX}/screen", json={"application_id": 1})
    assert r.status_code == 403


def test_an_editor_passes_the_gate_and_reaches_the_body(client):
    """403 would mean the gate; 404 means the gate passed and the handler ran."""
    _as("editor", _FakeSession())
    r = client.post(f"{PREFIX}/screen", json={"application_id": 999999})
    assert r.status_code == 404


# --------------------------------------------------------------------------
# Refusals: the module must never screen on absent evidence
# --------------------------------------------------------------------------


def _application_row(**over):
    row = {
        "id": 1, "job_pk": 39, "first_name": "Aa", "last_name": "Bb",
        "job_title": "Growth Manager",
    }
    row.update(over)
    return row


def test_screening_refuses_when_the_job_description_is_unreadable(client, monkeypatch):
    session = _FakeSession({"FROM jobs WHERE id": [
        {"id": 30, "title": "Hackathon 2026", "description": "<p></p>"}
    ]})
    monkeypatch.setattr(
        router_mod.reads, "get_application", lambda db, i: _application_row(job_pk=30)
    )
    _as("editor", session)
    r = client.post(f"{PREFIX}/screen", json={"application_id": 1})
    assert r.status_code == 422
    assert "readable text" in r.json()["detail"]


def test_screening_refuses_when_the_cv_cannot_be_read(client, monkeypatch):
    """CLAUDE.md Rule 29: 27 CV rejections went out live written from nothing
    but a first name and a role title, because empty evidence was accepted."""
    session = _FakeSession({"FROM jobs WHERE id": [
        {"id": 39, "title": "Growth Manager",
         "description": "<p>" + ("Real job description text. " * 30) + "</p>"}
    ]})
    monkeypatch.setattr(router_mod.reads, "get_application", lambda db, i: _application_row())
    monkeypatch.setattr(
        router_mod.reads, "get_cv_evidence",
        lambda db, i: {"cv_text": None, "cv_error": "no resume on file for this candidate"},
    )
    _as("editor", session)
    r = client.post(f"{PREFIX}/screen", json={"application_id": 1})
    assert r.status_code == 422
    detail = r.json()["detail"]
    assert "no resume on file" in detail
    assert "grounded in the candidate's actual CV" in detail


def test_an_application_with_no_job_is_refused(client, monkeypatch):
    monkeypatch.setattr(
        router_mod.reads, "get_application", lambda db, i: _application_row(job_pk=None)
    )
    _as("editor")
    r = client.post(f"{PREFIX}/screen", json={"application_id": 1})
    assert r.status_code == 422
    assert "no job on record" in r.json()["detail"]


# --------------------------------------------------------------------------
# Supersession (CLAUDE.md Rule 25)
# --------------------------------------------------------------------------


def _screen_result(**over):
    out = {
        "scores": {"skills": 4, "experience": 3, "fit": 3},
        "evidence": {"skills": "a", "experience": "b", "fit": "c"},
        "strengths": ["one", "two"],
        "gaps": ["a gap"],
        "total_experience_years": 8.0,
        "relevant_experience_years": 3.0,
        "relevant_experience_note": "three years on partnerships",
        "match": 68.0,
        "tier": "maybe",
        "model": "claude-x",
        "sop_sha256": "sopsha",
        "cv_chars": 12_000,
        "cv_truncated": False,
    }
    out.update(over)
    return out


def _wire_a_successful_screen(monkeypatch, session):
    monkeypatch.setattr(router_mod.reads, "get_application", lambda db, i: _application_row())
    monkeypatch.setattr(
        router_mod.reads, "get_cv_evidence",
        lambda db, i: {"cv_text": "a real CV" * 500, "cv_error": None},
    )
    monkeypatch.setattr(router_mod, "screen_cv", lambda **kw: _screen_result())


def test_a_new_screen_retires_the_previous_one_before_committing(client, monkeypatch):
    session = _FakeSession({"FROM jobs WHERE id": [
        {"id": 39, "title": "Growth Manager",
         "description": "<p>" + ("Real job description text. " * 30) + "</p>"}
    ]})
    _wire_a_successful_screen(monkeypatch, session)
    _as("editor", session)

    r = client.post(f"{PREFIX}/screen", json={"application_id": 1})
    assert r.status_code == 200, r.text

    updates = [
        (sql, params) for sql, params in session.executed
        if "UPDATE coco.cv_screens" in sql
    ]
    assert len(updates) == 1, "the previous screen must be retired exactly once"
    sql, params = updates[0]
    assert "is_current = false" in sql and "superseded_by = :new_id" in sql
    assert "id <> :new_id" in sql, "the new row must not retire itself"
    assert params["application_id"] == 1
    assert params["new_id"], "the retired rows must point at the replacement"
    assert session.flushed, "the id must be assigned before the UPDATE references it"
    assert session.committed


def test_the_screen_is_persisted_with_what_it_was_built_from(client, monkeypatch):
    session = _FakeSession({"FROM jobs WHERE id": [
        {"id": 39, "title": "Growth Manager",
         "description": "<p>" + ("Real job description text. " * 30) + "</p>"}
    ]})
    _wire_a_successful_screen(monkeypatch, session)
    _as("editor", session)

    assert client.post(f"{PREFIX}/screen", json={"application_id": 1}).status_code == 200
    row = session.added[0]
    assert row.job_id == 39
    assert row.match == 68.0 and row.tier == "maybe"
    assert row.total_experience_years == 8.0 and row.relevant_experience_years == 3.0
    assert row.sop_sha256 == "sopsha"
    assert len(row.jd_sha256) == 64, "the exact JD screened against must be recorded"
    assert row.created_by == "appuser-cv-test"


# --------------------------------------------------------------------------
# Profile fields: captured from the question wording, never guessed
# --------------------------------------------------------------------------


def test_profile_fields_are_matched_on_the_question_text():
    out = router_mod._profile_fields(
        [
            {"question": "What is your Expected Salary?", "answer": "250,000 PKR"},
            {"question": "Which city are you based in?", "answer": "Lahore"},
            {"question": "Are you willing to relocate?", "answer": "Yes"},
        ],
        None,
    )
    assert out == {
        "expected_salary": "250,000 PKR",
        "city": "Lahore",
        "willing_to_relocate": "Yes",
    }


def test_a_field_nobody_was_asked_about_is_none_not_a_guess():
    out = router_mod._profile_fields([{"question": "Why us?", "answer": "..."}], None)
    assert out == {"expected_salary": None, "city": None, "willing_to_relocate": None}


def test_profile_fields_survive_every_shape_markaz_stores():
    assert router_mod._profile_fields(None, None)["city"] is None
    assert router_mod._profile_fields({"Current city": "Karachi"}, None)["city"] == "Karachi"
    assert router_mod._profile_fields(
        [{"label": "Expected salary", "value": "200k"}], None
    )["expected_salary"] == "200k"
    # A blank answer is not an answer.
    assert router_mod._profile_fields([{"question": "City", "answer": ""}], None)["city"] is None


# --------------------------------------------------------------------------
# The criteria the UI renders from
# --------------------------------------------------------------------------


def test_criteria_are_served_from_the_service_not_a_frontend_constant(client):
    _as("viewer")
    r = client.get(f"{PREFIX}/criteria")
    assert r.status_code == 200
    keys = [c["key"] for c in r.json()]
    assert keys == ["skills", "experience", "fit"]
    assert sum(c["weight"] for c in r.json()) == 100
