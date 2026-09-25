"""HTTP tests for the sourcing router.

The gate into Markaz is the point of this file. It is enforced twice -- in the
service, with a reason a person can read, and by a database CHECK constraint --
and these tests cover the API half. Gate assertions compare dependency
CALLABLES by identity, because every gate `deps._require_role` returns is a
closure named `dep`.

Run: python -m pytest webapp/tests/test_sourcing_router.py -v
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import webapp.deps as deps
import webapp.routers.sourcing as router_mod
from webapp.db import get_db
from webapp.main import app
from webapp.models import SourcedCandidate
from webapp.services import sourcing as src

PREFIX = "/api/sourcing"


def _user(role: str) -> dict:
    return {"id": "appuser-src", "email": f"{role}@example.com", "app_role": role}


def _candidate(**over) -> SourcedCandidate:
    row = SourcedCandidate(
        id="src-1", name="Aa One", organization="TCF",
        linkedin_url="https://pk.linkedin.com/in/aa-one",
        linkedin_slug="aa-one",
        verification_state=src.UNCONFIRMED,
        outreach_state=src.NOT_CONTACTED,
        created_by="test",
    )
    for k, v in over.items():
        setattr(row, k, v)
    return row


class _Result:
    def __init__(self, rows):
        self._rows = rows

    def mappings(self):
        return self

    def all(self):
        return list(self._rows)


class _FakeSession:
    def __init__(self, row=None, existing=None):
        self.row = row
        self.existing = existing or []
        self.committed = False

    def get(self, model, pk):
        return self.row if self.row and self.row.id == pk else None

    def execute(self, stmt, params=None):
        return _Result(self.existing)

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


def _as(role: str, session=None):
    app.dependency_overrides[deps.get_current_user] = lambda: _user(role)
    app.dependency_overrides[get_db] = lambda: session or _FakeSession()


def _dependencies(path: str, method: str) -> set:
    for route in router_mod.router.routes:
        if getattr(route, "path", None) == path and method in (
            getattr(route, "methods", None) or set()
        ):
            return {d.call for d in route.dependant.dependencies if getattr(d, "call", None)}
    raise AssertionError(f"route not found: {method} {path}")


# --------------------------------------------------------------------------
# Gates
# --------------------------------------------------------------------------


def test_recording_a_reply_needs_an_editor():
    found = _dependencies(f"{PREFIX}/{{sourced_id}}", "PATCH")
    assert deps.require_editor in found
    assert deps.require_approver not in found


def test_putting_somebody_into_markaz_needs_an_approver():
    """Recording a reply is an edit. Entering somebody into the hiring
    pipeline is a decision."""
    found = _dependencies(f"{PREFIX}/{{sourced_id}}/push-to-markaz", "POST")
    assert deps.require_approver in found


def test_reading_the_pool_needs_only_a_signed_in_user():
    for path in (f"{PREFIX}/pool", f"{PREFIX}/summary"):
        assert deps.get_current_user in _dependencies(path, "GET")


def test_the_gate_assertion_bites():
    with pytest.raises(AssertionError):
        assert deps.require_approver in _dependencies(f"{PREFIX}/pool", "GET")


def test_an_editor_cannot_push_to_markaz(client):
    _as("editor", _FakeSession(_candidate(outreach_state=src.INTERESTED)))
    r = client.post(f"{PREFIX}/src-1/push-to-markaz", json={"application_id": 1})
    assert r.status_code == 403


# --------------------------------------------------------------------------
# The core rule
# --------------------------------------------------------------------------


def test_nobody_enters_markaz_without_saying_yes(client):
    """The skill's core rule. Refused here with a readable reason, and refused
    again by a database constraint if this ever lets one through."""
    for state in (src.NOT_CONTACTED, src.CONTACTED, src.NO_REPLY,
                  src.REPLIED_NOT_INTERESTED):
        _as("approver", _FakeSession(_candidate(outreach_state=state)))
        r = client.post(f"{PREFIX}/src-1/push-to-markaz", json={"application_id": 1})
        assert r.status_code == 409, state
        assert "confirmed interest" in r.json()["detail"]


def test_somebody_already_in_markaz_is_not_pushed_twice(client):
    _as("approver", _FakeSession(
        _candidate(outreach_state=src.INTERESTED, markaz_application_id=99)))
    r = client.post(f"{PREFIX}/src-1/push-to-markaz", json={"application_id": 1})
    assert r.status_code == 409 and "already in Markaz" in r.json()["detail"]


def test_the_push_refuses_an_application_that_is_not_theirs(client):
    """It records a LINK to a record created by hand. Markaz already holds 298
    duplicate (candidate, job) pairs, and creating more from here would make
    that worse in somebody else's system."""
    _as("approver", _FakeSession(_candidate(outreach_state=src.INTERESTED), existing=[]))
    r = client.post(f"{PREFIX}/src-1/push-to-markaz", json={"application_id": 4321})
    assert r.status_code == 404
    assert "create them there first" in r.json()["detail"]


def test_the_push_names_near_matches_rather_than_guessing(client):
    """Searched by name AND email, because an invitee may exist under an older
    address."""
    _as("approver", _FakeSession(
        _candidate(outreach_state=src.INTERESTED),
        existing=[{"candidate_id": 7, "first_name": "Aa", "last_name": "One",
                   "email": "aa@x.com", "application_id": 555, "job_id": 42}],
    ))
    r = client.post(f"{PREFIX}/src-1/push-to-markaz", json={"application_id": 4321})
    assert r.status_code == 404
    assert "application 555" in r.json()["detail"]


def test_a_matching_application_is_linked(client):
    session = _FakeSession(
        _candidate(outreach_state=src.INTERESTED),
        existing=[{"candidate_id": 7, "first_name": "Aa", "last_name": "One",
                   "email": "aa@x.com", "application_id": 4321, "job_id": 42}],
    )
    _as("approver", session)
    r = client.post(f"{PREFIX}/src-1/push-to-markaz", json={"application_id": 4321})
    assert r.status_code == 200
    assert r.json()["markaz_application_id"] == 4321
    assert session.committed


# --------------------------------------------------------------------------
# Outreach updates
# --------------------------------------------------------------------------


def test_an_unknown_outreach_state_is_refused(client):
    _as("editor", _FakeSession(_candidate()))
    r = client.patch(f"{PREFIX}/src-1", json={"outreach_state": "messaged maybe"})
    assert r.status_code == 400 and "unknown outreach state" in r.json()["detail"]


def test_somebody_in_markaz_cannot_be_moved_off_interested(client):
    """It would break the database constraint, so say why rather than 500."""
    _as("editor", _FakeSession(
        _candidate(outreach_state=src.INTERESTED, markaz_application_id=99)))
    r = client.patch(f"{PREFIX}/src-1", json={"outreach_state": src.NOT_CONTACTED})
    assert r.status_code == 409
    assert "already in Markaz" in r.json()["detail"]


def test_marking_somebody_contacted_stamps_who_and_when(client):
    row = _candidate()
    _as("editor", _FakeSession(row))
    r = client.patch(f"{PREFIX}/src-1", json={"outreach_state": src.CONTACTED})
    assert r.status_code == 200
    assert row.contacted_at is not None and row.contacted_by == "appuser-src"


# --------------------------------------------------------------------------
# What the pool says about itself
# --------------------------------------------------------------------------


def test_a_row_carries_why_it_cannot_enter_markaz(client):
    """So the page can explain it rather than just disabling a button."""
    _as("editor", _FakeSession(_candidate()))
    body = client.patch(f"{PREFIX}/src-1", json={"notes": "x"}).json()
    assert body["blocked_from_markaz"] and "confirmed interest" in body["blocked_from_markaz"]


def test_an_unconfirmed_profile_is_not_reported_as_verified(client):
    _as("editor", _FakeSession(_candidate(verification_state=src.UNCONFIRMED)))
    body = client.patch(f"{PREFIX}/src-1", json={"notes": "x"}).json()
    assert body["is_verified"] is False
    assert body["verification_state"] == src.UNCONFIRMED


def test_a_bad_filter_is_refused_rather_than_silently_ignored(client):
    _as("viewer")
    assert client.get(f"{PREFIX}/pool?outreach_state=nonsense").status_code == 400
    assert client.get(f"{PREFIX}/pool?verification_state=nonsense").status_code == 400
