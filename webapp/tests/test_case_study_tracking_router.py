"""HTTP-level tests for the case-study tracking router.

The load-bearing tests here are the ones that keep the module honest about what
it cannot see. Markaz records no case-study SEND, so a probe that finds nothing
must never harden into "not sent", and a re-probe must actually advance
`probed_at` -- a stale timestamp claiming freshness is the one thing a reader
relies on this table for.

Gate assertions compare dependency CALLABLES by identity, not names: every gate
`deps._require_role` returns is a closure called `dep`, so a name-based check
cannot tell an editor gate from an approver gate.

Run: python -m pytest webapp/tests/test_case_study_tracking_router.py -v
"""

from __future__ import annotations

import datetime as dt

import pytest
from fastapi.testclient import TestClient

import webapp.deps as deps
import webapp.routers.case_study_tracking as router_mod
from webapp.db import get_db
from webapp.main import app
from webapp.models import CaseStudyProbe
from webapp.services import case_study_tracking as tracking

PREFIX = "/api/case-study-tracking"


def _user(role: str, uid: str = "appuser-cst-test") -> dict:
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

    def __iter__(self):
        return iter(self._rows)


class _Query:
    def __init__(self, result):
        self._result = result

    def filter(self, *a, **kw):
        return self

    def one_or_none(self):
        return self._result


class _FakeSession:
    def __init__(self, responses=None, existing_probe=None):
        self.responses = responses or {}
        self.executed = []
        self.added = []
        self.existing_probe = existing_probe
        self.committed = False

    def execute(self, stmt, params=None):
        sql = " ".join(str(stmt).split())
        self.executed.append((sql, params or {}))
        for needle, rows in self.responses.items():
            if needle in sql:
                return _Result(rows)
        return _Result([])

    def query(self, *a, **kw):
        return _Query(self.existing_probe)

    def add(self, obj):
        self.added.append(obj)
        if getattr(obj, "id", None) is None:
            obj.id = "csp-generated"

    def flush(self):
        pass

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


def test_probing_requires_an_editor():
    found = _dependencies(f"{PREFIX}/probe", "POST")
    assert deps.require_editor in found
    assert deps.require_approver not in found


def test_reading_the_tracker_requires_only_a_signed_in_user():
    for path in (f"{PREFIX}/jobs/{{job_id}}", f"{PREFIX}/jobs/{{job_id}}/summary",
                 f"{PREFIX}/jobs/{{job_id}}/mirrors", f"{PREFIX}/probes"):
        found = _dependencies(path, "GET")
        assert deps.get_current_user in found, path
        assert deps.require_editor not in found, path


def test_the_gate_assertion_bites():
    with pytest.raises(AssertionError):
        assert deps.require_editor in _dependencies(f"{PREFIX}/probes", "GET")


def test_a_viewer_cannot_probe(client):
    _as("viewer")
    assert client.post(f"{PREFIX}/probe", json={"application_id": 1}).status_code == 403


# --------------------------------------------------------------------------
# The Rule 18 behaviour, end to end
# --------------------------------------------------------------------------


def _app_rows(**over):
    row = {
        "application_id": 1,
        "case_study_submission": None,
        "case_study_word_file": None,
        "case_study_excel_file": None,
        "case_study_video_file": None,
        "case_study_submitted_at": None,
        "case_study_status": None,
        "first_name": "Aa",
        "last_name": "Bb",
        "email": "aa@example.com",
    }
    row.update(over)
    return [row]


def test_an_unprobed_candidate_with_no_submission_is_not_reported_as_unsent(client):
    session = _FakeSession({"FROM applications a JOIN candidates": _app_rows()})
    _as("viewer", session)
    rows = client.get(f"{PREFIX}/jobs/42").json()
    assert rows[0]["status"] == tracking.NO_RECORD_OF_A_SEND
    assert rows[0]["probe"] is None


def test_the_summary_reports_the_caveat_as_a_number(client):
    session = _FakeSession({
        "FROM applications a JOIN candidates": _app_rows() + _app_rows(
            application_id=2, case_study_word_file="/uploads/x.docx"
        ),
        "FROM jobs WHERE id": [{"id": 42, "title": "Senior Manager Growth"}],
    })
    _as("viewer", session)
    body = client.get(f"{PREFIX}/jobs/42/summary").json()
    assert body["total"] == 2
    assert body["no_record_of_a_send"] == 1
    assert body["unproven_absence"] == 1
    assert body["submitted_without_send_record"] == 1
    assert "not_sent" not in body


def test_markaz_columns_are_read_live_not_from_the_probe(client):
    """A submission that arrived after the last probe must show immediately."""
    session = _FakeSession({
        "FROM applications a JOIN candidates": _app_rows(
            case_study_submission="https://drive.google.com/x"
        ),
    })
    _as("viewer", session)
    rows = client.get(f"{PREFIX}/jobs/42").json()
    assert rows[0]["channels"] == ["submission_text"]


# --------------------------------------------------------------------------
# Probing
# --------------------------------------------------------------------------


def _wire_probe(monkeypatch, *, send=None, corpus=None, unreadable=None, boom=None):
    monkeypatch.setattr(
        router_mod.reads, "get_application",
        lambda db, i: {"id": i, "job_pk": 42, "first_name": "Aa", "last_name": "Bb"},
    )
    monkeypatch.setattr(router_mod.tracking, "find_send", lambda email: send)

    def corpus_for(app_id, db=None):
        if boom:
            raise boom
        if unreadable:
            raise router_mod.SubmissionUnreadable(unreadable)
        return corpus

    monkeypatch.setattr(router_mod, "corpus_for", corpus_for)


_MARKAZ = {
    "case_study_submission": "https://drive.google.com/x",
    "case_study_word_file": None,
    "case_study_excel_file": None,
    "case_study_video_file": None,
    "email": "aa@example.com",
}


def _probe_session(existing=None, markaz=None):
    return _FakeSession(
        {"SELECT a.case_study_submission": [markaz or _MARKAZ]},
        existing_probe=existing,
    )


def test_a_probe_that_finds_no_send_records_no_record_never_not_sent(client, monkeypatch):
    session = _probe_session()
    _wire_probe(monkeypatch, send=None, corpus={
        "text": "a real submission " * 50, "chars": 900, "sources": ["Drive link"]
    })
    _as("editor", session)
    body = client.post(f"{PREFIX}/probe", json={"application_id": 1}).json()
    assert body["send_found"] is False
    assert body["status"] == tracking.SUBMITTED_WITHOUT_SEND_RECORD


def test_a_found_send_is_recorded_with_the_message_that_evidenced_it(client, monkeypatch):
    when = dt.datetime(2026, 8, 24, 9, 30, tzinfo=dt.timezone.utc)
    session = _probe_session(markaz={**_MARKAZ, "case_study_submission": None})
    _wire_probe(monkeypatch, send={"subject": "Your Case Study | Growth Manager", "date": when})
    _as("editor", session)
    body = client.post(f"{PREFIX}/probe", json={"application_id": 1}).json()
    assert body["send_found"] is True
    assert body["send_subject"] == "Your Case Study | Growth Manager"
    assert body["status"] == tracking.AWAITING


def test_a_mailbox_failure_is_not_fatal_and_is_not_read_as_not_sent(client, monkeypatch):
    """A mailbox that will not open tells us nothing about the candidate."""
    session = _probe_session(markaz={**_MARKAZ, "case_study_submission": None})
    _wire_probe(monkeypatch)
    monkeypatch.setattr(
        router_mod.tracking, "find_send",
        lambda email: (_ for _ in ()).throw(OSError("IMAP down")),
    )
    _as("editor", session)
    r = client.post(f"{PREFIX}/probe", json={"application_id": 1})
    assert r.status_code == 200
    assert r.json()["status"] == tracking.NO_RECORD_OF_A_SEND


def test_an_unreadable_submission_is_recorded_as_an_error_not_an_empty_corpus(
    client, monkeypatch
):
    session = _probe_session()
    _wire_probe(monkeypatch, unreadable="the Drive link resolved to the SPA shell")
    _as("editor", session)
    body = client.post(f"{PREFIX}/probe", json={"application_id": 1}).json()
    assert body["corpus_error"] == "the Drive link resolved to the SPA shell"
    assert body["corpus_chars"] == 0
    assert body["flags"] == []


def test_an_unexpected_retrieval_failure_is_caught_and_named(client, monkeypatch):
    session = _probe_session()
    _wire_probe(monkeypatch, boom=RuntimeError("something odd"))
    _as("editor", session)
    body = client.post(f"{PREFIX}/probe", json={"application_id": 1}).json()
    assert body["corpus_error"] == "retrieval failed: RuntimeError"


def test_retrieval_is_skipped_entirely_when_markaz_holds_nothing(client, monkeypatch):
    """Three network round trips for a candidate with no submission is waste."""
    called = []
    session = _probe_session(markaz={**_MARKAZ, "case_study_submission": None})
    _wire_probe(monkeypatch)
    monkeypatch.setattr(
        router_mod, "corpus_for",
        lambda app_id, db=None: called.append(app_id) or {"text": "", "chars": 0, "sources": []},
    )
    _as("editor", session)
    client.post(f"{PREFIX}/probe", json={"application_id": 1})
    assert called == [], "corpus_for must not run when there is nothing to read"


def test_flags_are_raised_from_the_submission_text(client, monkeypatch):
    session = _probe_session()
    _wire_probe(monkeypatch, corpus={
        "text": "Certainly! Here is a comprehensive analysis. " * 20,
        "chars": 900, "sources": ["Gmail attachment"],
    })
    _as("editor", session)
    body = client.post(f"{PREFIX}/probe", json={"application_id": 1}).json()
    assert "assistant_voice" in {f["flag"] for f in body["flags"]}
    assert all(f["meaning"] for f in body["flags"])


def test_completeness_is_unknown_unless_required_parts_are_supplied(client, monkeypatch):
    session = _probe_session()
    _wire_probe(monkeypatch, corpus={"text": "x " * 500, "chars": 1000, "sources": []})
    _as("editor", session)

    body = client.post(f"{PREFIX}/probe", json={"application_id": 1}).json()
    assert body["completeness"]["known"] is False

    body = client.post(
        f"{PREFIX}/probe",
        json={"application_id": 1, "required_parts": ["Market sizing"]},
    ).json()
    assert body["completeness"]["known"] is True
    assert body["completeness"]["missing"] == ["Market sizing"]


# --------------------------------------------------------------------------
# The upsert, and the timestamp a reader trusts
# --------------------------------------------------------------------------


def test_a_reprobe_replaces_the_row_rather_than_adding_a_second(client, monkeypatch):
    existing = CaseStudyProbe(
        id="csp-existing", application_id=1, job_id=42, channels=[],
        send_found=False, status=tracking.NO_RECORD_OF_A_SEND, corpus_chars=0,
        sources=[], flags=[], completeness={}, probed_by="someone",
        probed_at=dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc),
    )
    session = _probe_session(existing=existing)
    _wire_probe(monkeypatch, corpus={"text": "y " * 500, "chars": 1000, "sources": ["Drive"]})
    _as("editor", session)

    r = client.post(f"{PREFIX}/probe", json={"application_id": 1})
    assert r.status_code == 200
    assert session.added == [], "a re-probe must update, not insert a duplicate"
    assert existing.corpus_chars == 1000


def test_a_reprobe_advances_probed_at(client, monkeypatch):
    """The bug this catches: the column's server default only fires on INSERT,
    so an UPDATE that relies on it keeps the ORIGINAL timestamp and the row
    claims to be fresher than it is."""
    stale = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
    existing = CaseStudyProbe(
        id="csp-existing", application_id=1, job_id=42, channels=[],
        send_found=False, status=tracking.NO_RECORD_OF_A_SEND, corpus_chars=0,
        sources=[], flags=[], completeness={}, probed_by="someone", probed_at=stale,
    )
    session = _probe_session(existing=existing)
    _wire_probe(monkeypatch, corpus={"text": "y " * 500, "chars": 1000, "sources": []})
    _as("editor", session)

    client.post(f"{PREFIX}/probe", json={"application_id": 1})
    assert existing.probed_at > stale, "probed_at did not advance on a re-probe"


# --------------------------------------------------------------------------
# Mirrors
# --------------------------------------------------------------------------

_SHARED = (
    "the pipeline supports one hundred and eight partners in year one which is "
    "below the target of one hundred and fifty schools across the region "
    "requiring an additional forty two partnerships to close the gap entirely"
)


def test_mirrors_name_the_candidates_and_show_the_shared_text(client):
    session = _FakeSession({
        "FROM applications a JOIN candidates": (
            _app_rows(application_id=1, first_name="Aa", last_name="One")
            + _app_rows(application_id=2, first_name="Bb", last_name="Two")
        ),
        "FROM coco.case_study_probes WHERE job_id": [
            {"application_id": 1, "corpus_text": "opening one. " + _SHARED},
            {"application_id": 2, "corpus_text": "opening two. " + _SHARED},
        ],
    })
    _as("viewer", session)
    pairs = client.get(f"{PREFIX}/jobs/42/mirrors").json()
    assert len(pairs) == 1
    assert pairs[0]["candidate_names"] == ["Aa One", "Bb Two"]
    assert pairs[0]["examples"]
    # No verdict, no cause.
    assert "cause" not in pairs[0] and "verdict" not in pairs[0]


def test_mirrors_over_an_unprobed_job_are_empty_rather_than_wrong(client):
    session = _FakeSession({"FROM applications a JOIN candidates": _app_rows()})
    _as("viewer", session)
    assert client.get(f"{PREFIX}/jobs/42/mirrors").json() == []
