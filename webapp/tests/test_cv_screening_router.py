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
        self.rollbacks = 0

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

    def rollback(self):
        # Faithful to SQLAlchemy: a rollback discards what was pending. That
        # makes `added` prove ORDER, not just presence -- a skip recorded
        # BEFORE the rollback of the attempt that produced it would be thrown
        # away here and the test would fail, which is the point.
        self.rollbacks += 1
        self.added = []

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


def test_profile_fields_read_the_shape_markaz_actually_uses():
    """🔴 Measured across 800 live applications, the ONLY shape either answers
    column takes is a dict keyed by a timestamp id with {question, answer}
    nested inside. An earlier version of this test used a list of dicts that I
    invented; it passed while the extractor returned nothing for every real
    candidate on record."""
    real = {
        "1763029445610": {"question": "Expected Salary (PKR)", "answer": "250,000"},
        "1763029445611": {"question": "Which city are you currently based in?",
                          "answer": "Lahore"},
        "1763029445612": {"question": "Are you willing to relocate?", "answer": "Yes"},
    }
    assert router_mod._profile_fields(real, {}) == {
        "expected_salary": "250,000",
        "city": "Lahore",
        "willing_to_relocate": "Yes",
    }


def test_a_relocate_question_is_not_read_as_the_candidates_city():
    """"Are you willing to relocate to another city?" contains both words.
    Each question is claimed by at most one field, in priority order, so the
    answer "Yes" can never end up in the City column."""
    blob = {
        "1": {"question": "Are you willing to relocate to another city?", "answer": "Yes"},
        "2": {"question": "Which city do you live in?", "answer": "Karachi"},
    }
    out = router_mod._profile_fields(blob, {})
    assert out["willing_to_relocate"] == "Yes"
    assert out["city"] == "Karachi"


def test_a_travel_question_is_not_read_as_the_candidates_city():
    """The real question text from CPD Coach, verbatim. A loose "city" match
    claimed this travel question for 332 of 410 candidates and printed "Yes I
    am willing to travel" in the City column. That job has no city question at
    all; its location field is "Address"."""
    blob = {
        "1": {"question": "Willingness to travel in your assigned region (regions "
                          "may include certain city areas such as Subdivision City)",
              "answer": "Yes I am willing to travel"},
        "2": {"question": "Address", "answer": "17C, street 46, F-10/4, Islamabad"},
    }
    out = router_mod._profile_fields(blob, {})
    assert out["city"] == "17C, street 46, F-10/4, Islamabad"


def test_a_job_with_no_location_question_reports_none_rather_than_inventing_one():
    blob = {
        "1": {"question": "Willingness to travel in your assigned region (certain "
                          "city areas)", "answer": "Yes"},
        "2": {"question": "Expected Salary", "answer": "150,000"},
    }
    out = router_mod._profile_fields(blob, {})
    assert out["city"] is None
    assert out["expected_salary"] == "150,000"


def test_a_field_nobody_was_asked_about_is_none_not_a_guess():
    out = router_mod._profile_fields({"1": {"question": "Why us?", "answer": "..."}}, {})
    assert out == {"expected_salary": None, "city": None, "willing_to_relocate": None}


def test_both_answer_columns_are_read():
    custom = {"1": {"question": "Expected salary", "answer": "200k"}}
    canned = {"2": {"question": "Current city", "answer": "Islamabad"}}
    out = router_mod._profile_fields(custom, canned)
    assert out["expected_salary"] == "200k" and out["city"] == "Islamabad"


def test_empty_and_missing_columns_are_survivable():
    """263 of 800 applications carry an empty dict rather than null."""
    assert router_mod._profile_fields({}, {})["city"] is None
    assert router_mod._profile_fields(None, None)["city"] is None


def test_a_blank_answer_is_not_an_answer():
    blob = {"1": {"question": "Which city?", "answer": "   "}}
    assert router_mod._profile_fields(blob, {})["city"] is None


def test_the_legacy_shapes_still_parse_if_markaz_ever_changes():
    """Defensive only -- neither shape occurs in the live data today."""
    assert router_mod._profile_fields({"Current city": "Karachi"}, None)["city"] == "Karachi"
    assert router_mod._profile_fields(
        [{"label": "Expected salary", "value": "200k"}], None
    )["expected_salary"] == "200k"


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


# --------------------------------------------------------------------------
# A CV that cannot be read is RECORDED, not forgotten
#
# THE BUG THESE EXIST FOR. A refused candidate gets no `cv_screens` row, which
# is correct: a model asked to judge an empty page still answers. But "could
# not be read" and "not looked at yet" were then the same state to every
# reader, so the page counted refusals as work outstanding for ever.
#
# On CPD Coach that was 81 of 411 -- 43 with no resume stored in Markaz at all,
# 26 extracting to under 250 words, 12 failing outright as JPEGs, PNGs and
# legacy .doc files. The position had been read end to end. Ayesha ran it
# twice and asked why 81 were "still to be screened", which is precisely what
# the page said.
# --------------------------------------------------------------------------


def test_a_skip_is_bucketed_by_what_somebody_would_have_to_do_about_it():
    """`kind` is derived from the reason the refusing code path actually
    produces, so the UI can group without parsing prose."""
    assert router_mod._skip_kind("no resume on file for this candidate") == "no_cv"
    assert router_mod._skip_kind(
        "extracted only 172 words (needs 250+). This is an extraction failure, "
        "not a weak candidate."
    ) == "too_short"
    assert router_mod._skip_kind(
        "could not extract usable text from download.jpg (needs 400+ chars)"
    ) == "unreadable"


def test_the_batch_records_the_skip_instead_of_dropping_it(client, monkeypatch):
    session = _FakeSession({
        "FROM jobs WHERE id": [
            {"id": 39, "title": "Growth Manager",
             "description": "<p>" + ("Real job description text. " * 30) + "</p>"}
        ],
        "SELECT a.id FROM applications": [(4242,)],
    })
    monkeypatch.setattr(router_mod.reads, "get_application", lambda db, i: _application_row())
    monkeypatch.setattr(
        router_mod.reads, "get_cv_evidence",
        lambda db, i: {"cv_text": None,
                       "cv_error": "could not extract usable text from download.jpg",
                       "cv_file_name": "download.jpg"},
    )
    _as("editor", session)
    r = client.post(f"{PREFIX}/screen-batch", json={"job_id": 39, "limit": 1})
    assert r.status_code == 200
    assert [s["application_id"] for s in r.json()["skipped"]] == [4242]

    # The refusal was PERSISTED, with the detail a person chasing the file needs.
    skips = [o for o in session.added if isinstance(o, router_mod.CVScreenSkip)]
    assert len(skips) == 1, "the batch dropped the skip instead of recording it"
    assert skips[0].application_id == 4242
    assert skips[0].kind == "unreadable"
    assert skips[0].cv_file_name == "download.jpg"
    assert skips[0].candidate_name == "Aa Bb"


def test_a_recorded_skip_is_not_offered_as_work_again(client, monkeypatch):
    """Re-reading a JPEG costs real time and changes nothing, so a known
    unreadable CV leaves the run unless somebody asks for it by name."""
    session = _FakeSession({"FROM jobs WHERE id": [
        {"id": 39, "title": "Growth Manager",
         "description": "<p>" + ("Real job description text. " * 30) + "</p>"}
    ]})
    _as("editor", session)
    client.post(f"{PREFIX}/screen-batch", json={"job_id": 39})

    selects = [sql for sql, _ in session.executed if "SELECT a.id FROM applications" in sql]
    assert selects, "the batch never asked for work"
    assert "cv_screen_skips" in selects[0], "a known-unreadable CV is still being handed back"
    assert session.executed[[s for s, _ in session.executed].index(selects[0])][1][
        "retry_skipped"
    ] is False


def test_retry_skipped_is_the_one_way_they_come_back(client, monkeypatch):
    session = _FakeSession({"FROM jobs WHERE id": [
        {"id": 39, "title": "Growth Manager",
         "description": "<p>" + ("Real job description text. " * 30) + "</p>"}
    ]})
    _as("editor", session)
    client.post(f"{PREFIX}/screen-batch", json={"job_id": 39, "retry_skipped": True})

    params = [p for sql, p in session.executed if "SELECT a.id FROM applications" in sql]
    assert params and params[0]["retry_skipped"] is True


def test_a_successful_screen_clears_the_skip(client, monkeypatch):
    """The CV opens after all, so the statement that it could not is no longer
    true. Deleted, not kept: a stale skip would hold the candidate in the
    needs-a-person list for ever."""
    session = _FakeSession({"FROM jobs WHERE id": [
        {"id": 39, "title": "Growth Manager",
         "description": "<p>" + ("Real job description text. " * 30) + "</p>"}
    ]})
    monkeypatch.setattr(router_mod.reads, "get_application", lambda db, i: _application_row())
    monkeypatch.setattr(
        router_mod.reads, "get_cv_evidence",
        lambda db, i: {"cv_text": "word " * 600, "cv_file_name": "cv.pdf"},
    )
    monkeypatch.setattr(router_mod, "screen_cv", lambda **kw: _screen_result())
    _as("editor", session)
    r = client.post(f"{PREFIX}/screen", json={"application_id": 1})
    assert r.status_code == 200

    deletes = [sql for sql, _ in session.executed
               if "DELETE FROM coco.cv_screen_skips" in sql]
    assert deletes, "a successful screen left the old skip standing"


def test_the_summary_does_not_count_unreadable_cvs_as_work_left(client, monkeypatch):
    """411 applications, 330 screened, 81 refused: the position is FINISHED.
    Reporting 81 unscreened is what made a completed run look like a stall."""
    session = _FakeSession({
        "FROM jobs WHERE id": [
            {"id": 17, "title": "CPD Coach",
             "description": "<p>" + ("Real job description text. " * 30) + "</p>"}
        ],
        "SELECT COUNT(*) FROM applications WHERE job_id": [411],
        "FROM coco.cv_screens WHERE job_id": [
            {"tier": "shortlist"}] * 113 + [{"tier": "maybe"}] * 86
        + [{"tier": "no_hire"}] * 131,
        "SELECT COUNT(*) FROM coco.cv_screen_skips": [81],
    })
    _as("viewer", session)
    r = client.get(f"{PREFIX}/jobs/17/summary")
    assert r.status_code == 200
    body = r.json()

    assert body["unreadable"] == 81
    assert body["unscreened"] == 0, "a fully-read position still reports work outstanding"
    # Everyone is still accounted for.
    assert (
        body["shortlist"] + body["maybe"] + body["no_hire"]
        + body["unreadable"] + body["unscreened"]
    ) == body["total"]
