"""HTTP-level tests for the KCD evaluation router.

The load-bearing ones are the refusals: the verdict and the total are computed
here and never accepted from the client, a CONDITIONAL cannot be stored without
its condition, every score needs evidence behind it, and an incomplete
submission never shares a list with a complete one.

Gate assertions compare dependency CALLABLES by identity: every gate
`deps._require_role` returns is a closure called `dep`.

Run: python -m pytest webapp/tests/test_kcd_evaluations_router.py -v
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import webapp.deps as deps
import webapp.routers.kcd_evaluations as router_mod
from webapp.db import get_db
from webapp.main import app
from webapp.services import kcd_evaluation as kcd

PREFIX = "/api/kcd-evaluations"


def _user(role: str, uid: str = "appuser-kcd-test") -> dict:
    return {"id": uid, "email": f"{uid}@example.com", "app_role": role}


class _Result:
    def __init__(self, rows):
        self._rows = rows

    def mappings(self):
        return self

    def all(self):
        return list(self._rows)

    def first(self):
        return self._rows[0] if self._rows else None


class _FakeSession:
    def __init__(self, responses=None):
        self.responses = responses or {}
        self.executed = []
        self.added = []
        self.committed = False

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
        for obj in self.added:
            if getattr(obj, "id", None) is None:
                obj.id = "kcd-generated"

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


def _body(**over):
    payload = {
        "application_id": 1,
        "scores": {"knowledge": 4.0, "capacity": 3.5, "design": 4.0},
        "evidence": {
            "knowledge": "cited the enrolment column by name in E2",
            "capacity": "worked the margin backwards without prompting",
            "design": "named what the plan costs in month three",
        },
    }
    payload.update(over)
    return payload


def _wire(monkeypatch):
    monkeypatch.setattr(
        router_mod.reads, "get_application",
        lambda db, i: {"id": i, "job_pk": 42, "first_name": "Aa", "last_name": "Bb",
                       "job_title": "Senior Manager Growth"},
    )


# --------------------------------------------------------------------------
# Gates
# --------------------------------------------------------------------------


def test_writing_an_evaluation_requires_an_editor():
    found = _dependencies(f"{PREFIX}/evaluations", "POST")
    assert deps.require_editor in found
    assert deps.require_approver not in found


def test_reading_requires_only_a_signed_in_user():
    for path, method in (
        (f"{PREFIX}/framework", "GET"),
        (f"{PREFIX}/evaluations", "GET"),
        (f"{PREFIX}/jobs/{{job_id}}/cohort", "GET"),
    ):
        found = _dependencies(path, method)
        assert deps.get_current_user in found, path
        assert deps.require_editor not in found, path


def test_the_gate_assertion_bites():
    with pytest.raises(AssertionError):
        assert deps.require_editor in _dependencies(f"{PREFIX}/framework", "GET")


def test_a_viewer_cannot_write_an_evaluation(client):
    _as("viewer")
    assert client.post(f"{PREFIX}/evaluations", json=_body()).status_code == 403


# --------------------------------------------------------------------------
# The framework the UI renders from
# --------------------------------------------------------------------------


def test_the_framework_is_served_from_the_service(client):
    _as("viewer")
    body = client.get(f"{PREFIX}/framework").json()
    assert [d["key"] for d in body["dimensions"]] == ["knowledge", "capacity", "design"]
    assert body["gwc_threshold"] == 60.0
    assert 0.0 in body["scores"] and 4.5 in body["scores"]
    assert "not_sent" not in body["verdicts"]


def test_the_scale_offered_to_the_ui_has_a_real_zero(client):
    """If the form only offers 1 to 5, the floor comes back through the UI
    however careful the service is."""
    _as("viewer")
    assert min(client.get(f"{PREFIX}/framework").json()["scores"]) == 0.0


# --------------------------------------------------------------------------
# Who computes the verdict
# --------------------------------------------------------------------------


def test_the_total_and_verdict_are_computed_not_taken_from_the_client(client, monkeypatch):
    _wire(monkeypatch)
    session = _FakeSession()
    _as("editor", session)
    body = client.post(
        f"{PREFIX}/evaluations",
        json=_body(
            scores={"knowledge": 1.0, "capacity": 1.0, "design": 1.0},
            total=99.0, verdict="strong_hire", advances_to_gwc=True,
        ),
    ).json()
    assert body["total"] == 20.0
    assert body["verdict"] == kcd.NOT_RECOMMENDED
    assert body["advances_to_gwc"] is False


def test_caps_are_applied_before_the_total(client, monkeypatch):
    _wire(monkeypatch)
    _as("editor", _FakeSession())
    body = client.post(
        f"{PREFIX}/evaluations",
        json=_body(
            scores={"knowledge": 5.0, "capacity": 5.0, "design": 5.0},
            caps={"insight_without_evidence": ["knowledge"],
                  "evidence_without_interpretation": []},
        ),
    ).json()
    assert body["scores"]["knowledge"] == 3.0
    assert body["total"] < 100.0
    assert body["caps_applied"]["insight_without_evidence"] == ["knowledge"]


def test_a_cap_never_raises_a_score_through_the_api(client, monkeypatch):
    _wire(monkeypatch)
    _as("editor", _FakeSession())
    body = client.post(
        f"{PREFIX}/evaluations",
        json=_body(
            scores={"knowledge": 1.0, "capacity": 3.0, "design": 3.0},
            caps={"insight_without_evidence": ["knowledge"],
                  "evidence_without_interpretation": []},
        ),
    ).json()
    assert body["scores"]["knowledge"] == 1.0


# --------------------------------------------------------------------------
# Refusals
# --------------------------------------------------------------------------


def test_a_conditional_verdict_without_its_condition_is_refused(client, monkeypatch):
    _wire(monkeypatch)
    _as("editor", _FakeSession())
    r = client.post(
        f"{PREFIX}/evaluations",
        json=_body(scores={"knowledge": 3.0, "capacity": 3.0, "design": 3.0}),
    )
    assert r.status_code == 422
    assert "must state its condition" in r.json()["detail"]


def test_the_same_scores_are_accepted_once_the_condition_is_given(client, monkeypatch):
    _wire(monkeypatch)
    _as("editor", _FakeSession())
    r = client.post(
        f"{PREFIX}/evaluations",
        json=_body(
            scores={"knowledge": 3.0, "capacity": 3.0, "design": 3.0},
            condition="Evidence they have run a field team before.",
        ),
    )
    assert r.status_code == 200
    assert r.json()["verdict"] == kcd.CONDITIONAL
    assert r.json()["condition"].startswith("Evidence they have run")


def test_a_condition_on_a_non_conditional_verdict_is_dropped(client, monkeypatch):
    """Noise on a HIRE. Kept only where it means something."""
    _wire(monkeypatch)
    _as("editor", _FakeSession())
    body = client.post(
        f"{PREFIX}/evaluations",
        json=_body(condition="irrelevant here"),
    ).json()
    assert body["verdict"] == kcd.HIRE
    assert body["condition"] is None


def test_a_score_with_no_evidence_behind_it_is_refused(client, monkeypatch):
    _wire(monkeypatch)
    _as("editor", _FakeSession())
    r = client.post(
        f"{PREFIX}/evaluations",
        json=_body(evidence={"knowledge": "cited E2", "capacity": "  ", "design": "x"}),
    )
    assert r.status_code == 422
    assert "capacity" in r.json()["detail"]


def test_a_quarter_step_score_is_refused(client, monkeypatch):
    _wire(monkeypatch)
    _as("editor", _FakeSession())
    r = client.post(
        f"{PREFIX}/evaluations",
        json=_body(scores={"knowledge": 4.25, "capacity": 4.0, "design": 4.0}),
    )
    assert r.status_code == 422
    assert "whole or half step" in r.json()["detail"]


def test_an_application_with_no_job_is_refused(client, monkeypatch):
    monkeypatch.setattr(
        router_mod.reads, "get_application",
        lambda db, i: {"id": i, "job_pk": None, "first_name": "Aa", "last_name": "Bb"},
    )
    _as("editor", _FakeSession())
    r = client.post(f"{PREFIX}/evaluations", json=_body())
    assert r.status_code == 422 and "no job on record" in r.json()["detail"]


# --------------------------------------------------------------------------
# Supersession and the cohort split
# --------------------------------------------------------------------------


def test_a_new_evaluation_retires_the_previous_one(client, monkeypatch):
    _wire(monkeypatch)
    session = _FakeSession()
    _as("editor", session)
    assert client.post(f"{PREFIX}/evaluations", json=_body()).status_code == 200

    updates = [
        (sql, p) for sql, p in session.executed if "UPDATE coco.kcd_evaluations" in sql
    ]
    assert len(updates) == 1
    sql, params = updates[0]
    assert "is_current = false" in sql and "id <> :new_id" in sql
    assert params["application_id"] == 1 and params["new_id"]
    assert session.committed


def _stored(app_id, total, incomplete=False):
    return {
        "id": f"kcd-{app_id}", "application_id": app_id, "job_id": 42,
        "candidate_name": f"Cand {app_id}", "role": "SMG",
        "scores": {"knowledge": 4.0, "capacity": 4.0, "design": 4.0},
        "evidence": {"knowledge": "a", "capacity": "b", "design": "c"},
        "weights": None, "caps_applied": {}, "total": total,
        "verdict": kcd.verdict(total), "condition": None,
        "advances_to_gwc": kcd.advances_to_gwc(total), "incomplete": incomplete,
        "missing_parts": [], "integrity_flags": [], "second_evaluator": None,
        "second_total": None, "is_current": True, "superseded_by": None,
        "created_by": "u", "created_at": None,
    }


def test_the_cohort_never_ranks_an_incomplete_above_a_complete(client):
    session = _FakeSession({
        "FROM coco.kcd_evaluations WHERE job_id": [
            _stored(1, 82.0, incomplete=True),
            _stored(2, 41.0),
        ]
    })
    _as("viewer", session)
    body = client.get(f"{PREFIX}/jobs/42/cohort").json()
    assert [e["application_id"] for e in body["ranked"]] == [2]
    assert [e["application_id"] for e in body["incomplete"]] == [1]
    assert "floors" in body["note"]


def test_an_incomplete_score_is_rendered_with_its_caveat(client):
    session = _FakeSession({
        "FROM coco.kcd_evaluations WHERE job_id": [_stored(1, 52.0, incomplete=True)]
    })
    _as("viewer", session)
    body = client.get(f"{PREFIX}/jobs/42/cohort").json()
    display = body["incomplete"][0]["display_score"]
    assert display.startswith("52.0%*") and "not a capability read" in display
    assert body["ranked"][0]["display_score"] if body["ranked"] else True


def test_the_cohort_counts_who_advances_and_excludes_incomplete_ones(client):
    session = _FakeSession({
        "FROM coco.kcd_evaluations WHERE job_id": [
            _stored(1, 72.0), _stored(2, 61.0), _stored(3, 55.0),
            _stored(4, 90.0, incomplete=True),
        ]
    })
    _as("viewer", session)
    body = client.get(f"{PREFIX}/jobs/42/cohort").json()
    assert body["gwc_threshold"] == 60.0
    assert body["advancing"] == 2, "an incomplete submission does not advance"


def test_the_cross_check_is_reported_on_every_evaluation(client):
    row = _stored(1, 82.0)
    row.update(second_evaluator="Noah", second_total=70.0)
    session = _FakeSession({"FROM coco.kcd_evaluations WHERE job_id": [row]})
    _as("viewer", session)
    cc = client.get(f"{PREFIX}/jobs/42/cohort").json()["ranked"][0]["cross_check"]
    assert cc["status"] == "divergent" and cc["delta"] == 12.0
