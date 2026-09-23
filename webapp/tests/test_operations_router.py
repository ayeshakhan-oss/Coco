"""HTTP tests for the Hiring Operations attendance endpoint.

The report is read-only and gated on a signed-in user: it contains staff leave,
which is more sensitive than anything else the app shows, but it is also the
thing the whole P&C team needs daily, so it sits behind sign-in rather than
behind editor.

Run: python -m pytest webapp/tests/test_operations_router.py -v
"""

from __future__ import annotations

import datetime as dt

import pytest
from fastapi.testclient import TestClient

import webapp.deps as deps
import webapp.routers.operations as router_mod
from webapp.db import get_db
from webapp.main import app

PREFIX = "/api/operations"
TODAY = dt.date.today().isoformat()


def _user(role: str = "viewer") -> dict:
    return {"id": "appuser-ops", "email": "ops@example.com", "app_role": role}


class _Result:
    def __init__(self, rows):
        self._rows = rows

    def mappings(self):
        return self

    def all(self):
        return list(self._rows)

    def __iter__(self):
        return iter(self._rows)


class _FakeSession:
    def __init__(self, payroll=None, leave=None):
        self.payroll = payroll if payroll is not None else _PAYROLL
        self.leave = leave if leave is not None else []

    def execute(self, stmt, params=None):
        sql = " ".join(str(stmt).split())
        if "employee_profiles ep" in sql and "GROUP BY" not in sql:
            return _Result(self.payroll)
        if "leave_requests" in sql:
            return _Result(self.leave)
        if "GROUP BY payroll_entity" in sql:
            return _Result([{"payroll_entity": "OPL", "n": 104},
                            {"payroll_entity": "OWT", "n": 27}])
        return _Result([])

    def close(self):
        pass


def _p(uid, name, entity="OPL"):
    return {"user_id": uid, "name": name, "payroll_entity": entity,
            "department": "P&C", "job_title": "Manager"}


_PAYROLL = [_p(1, "Aa One"), _p(2, "Bb Two"), _p(3, "Cc Three", "OWT"),
            _p(9, "Ff Six", "NIETE Islamabad")]


@pytest.fixture
def client():
    c = TestClient(app)
    try:
        yield c
    finally:
        app.dependency_overrides.clear()


def _as(role="viewer", session=None):
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


def test_the_report_needs_a_signed_in_user():
    for path in (f"{PREFIX}/attendance", f"{PREFIX}/attendance/entities"):
        found = _dependencies(path, "GET")
        assert deps.get_current_user in found, path


def test_the_report_writes_nothing():
    """Ayesha, 2026-09-23: draft and show, she presses send. Nothing in
    Operations sends or stores on its own."""
    methods = {m for r in router_mod.router.routes for m in (getattr(r, "methods", None) or set())}
    assert methods <= {"GET", "HEAD"}, f"Operations exposes a write method: {methods}"


# --------------------------------------------------------------------------
# The report
# --------------------------------------------------------------------------


def test_todays_report_counts_only_the_head_office(client):
    _as(session=_FakeSession())
    body = client.get(f"{PREFIX}/attendance").json()
    assert body["total_on_payroll"] == 3          # OPL 2 + OWT 1, not NIETE
    assert body["entities"] == ["OPL", "OWT"]
    assert body["no_absence_recorded"] == 3


def test_the_boxes_account_for_everyone(client):
    _as(session=_FakeSession(leave=[{
        "user_id": 1, "name": "Aa One", "leave_type": "medical",
        "sub_category": None, "is_half_day": False,
        "start_date": TODAY, "end_date": TODAY}]))
    body = client.get(f"{PREFIX}/attendance").json()
    people = (body["no_absence_recorded"] + len(body["on_leave"])
              + len(body["working_from_home"]))
    assert people == body["total_on_payroll"]


def test_no_box_claims_somebody_was_present(client):
    """Markaz records absence. A box labelled "onsite" would be read as
    attendance, which is not something we can see."""
    _as(session=_FakeSession())
    body = client.get(f"{PREFIX}/attendance").json()
    labels = " ".join(b["label"] for b in body["stat_boxes"]).lower()
    for forbidden in ("onsite", "present", "attended", "in office"):
        assert forbidden not in labels
    assert "not the same as being seen" in body["presence_caveat"]


def test_a_broken_leave_record_is_surfaced_not_silently_dropped(client):
    """Four of these sit in Markaz right now. Excluding them quietly leaves
    tomorrow's report wrong too."""
    _as(session=_FakeSession(leave=[{
        "user_id": 1, "name": "Aa One", "leave_type": "work_from_home",
        "sub_category": None, "is_half_day": False,
        "start_date": "2026-04-01", "end_date": "42026-02-01"}]))
    body = client.get(f"{PREFIX}/attendance").json()
    assert len(body["needs_correction"]) == 1
    fix = body["needs_correction"][0]
    assert fix["end_date"] == "42026-02-01", "the value to correct must be shown in full"
    assert fix["problem"]
    assert len(body["working_from_home"]) == 0


def test_wfh_and_leave_are_separate_categories(client):
    _as(session=_FakeSession(leave=[
        {"user_id": 1, "name": "Aa One", "leave_type": "work_from_home",
         "sub_category": "wfh", "is_half_day": False,
         "start_date": TODAY, "end_date": TODAY},
        {"user_id": 2, "name": "Bb Two", "leave_type": "medical",
         "sub_category": None, "is_half_day": False,
         "start_date": TODAY, "end_date": TODAY},
    ]))
    body = client.get(f"{PREFIX}/attendance").json()
    assert [p["name"] for p in body["working_from_home"]] == ["Aa One"]
    assert [p["name"] for p in body["on_leave"]] == ["Bb Two"]


# --------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------


def test_a_past_date_can_be_asked_for(client):
    _as(session=_FakeSession())
    body = client.get(f"{PREFIX}/attendance?on=2026-09-01").json()
    assert body["date"] == "2026-09-01"
    assert body["weekday"] == "Tuesday"


def test_a_date_that_is_not_a_date_is_refused(client):
    _as(session=_FakeSession())
    r = client.get(f"{PREFIX}/attendance?on=last-tuesday")
    assert r.status_code == 422 and "not a date" in r.json()["detail"]


def test_entities_can_be_chosen(client):
    _as(session=_FakeSession())
    body = client.get(f"{PREFIX}/attendance?entities=NIETE%20Islamabad").json()
    assert body["total_on_payroll"] == 1
    assert body["entities"] == ["NIETE Islamabad"]


def test_an_entity_nobody_is_on_is_refused_rather_than_reported_as_zero(client):
    """A report saying 0 on payroll reads as "nobody came in", not as "you
    asked for a name that does not exist"."""
    _as(session=_FakeSession())
    r = client.get(f"{PREFIX}/attendance?entities=Nonesuch")
    assert r.status_code == 404 and "no one on the payroll" in r.json()["detail"]


def test_an_empty_entity_list_is_refused(client):
    _as(session=_FakeSession())
    assert client.get(f"{PREFIX}/attendance?entities=%20,%20").status_code == 422


def test_the_entities_endpoint_offers_the_real_ones(client):
    """The SOP hardcoded a payroll of 84, which was true in April and is 131
    now. The page reads the list rather than carrying a copy."""
    _as(session=_FakeSession())
    body = client.get(f"{PREFIX}/attendance/entities").json()
    assert body["default"] == ["OPL", "OWT"]
    assert {e["payroll_entity"] for e in body["entities"]} == {"OPL", "OWT"}
