"""The non-negotiable values-scoring rules, tested without an LLM or a database.

PASS is zero minuses AND at most two plus-minuses. Everything else is OUT. This is
computed in code and never left to a model, so it is tested exhaustively here.
"""

from __future__ import annotations

import itertools

import pytest
from fastapi import HTTPException

from webapp.services.values_scoring import (
    MARKAZ_KEYS,
    NOT_OBSERVED,
    RATINGS,
    VALUE_NAMES,
    ValuesScorecardError,
    build_markaz_payload,
    tally,
    validate_markaz_payload,
    validate_values,
    verdict,
)


# --------------------------------------------------------------------------
# Task 5: the model call. These monkeypatch _call_model, so no network call is
# ever made here.
# --------------------------------------------------------------------------


def test_verdict_is_computed_not_taken_from_the_model(monkeypatch):
    """A model that claims PASS on a scorecard containing a minus must not win."""
    from webapp.services import values_scoring as vs

    payload = {
        "values": [
            {"name": n, "deepDive": "d", "curveBall": "c", "microCase": "m", "rating": r}
            for n, r in zip(vs.VALUE_NAMES, ["+", "+", "+", "+", "+", "-"])
        ],
        "verdict": "PASS",          # the model lying
        "gwc": {"gets_it": "Yes", "wants_it": "Yes", "capacity": "Yes"},
    }
    monkeypatch.setattr(vs, "_call_model", lambda **kw: (payload, "test-model"))

    out = vs.score_transcript(transcript="x" * 3000, candidate_name="A", role="R")
    assert out["verdict"] == "OUT"      # computed from the ratings
    assert out["gwc"] is None           # GWC only for a PASS


def test_short_transcript_is_refused():
    from webapp.services.values_scoring import TranscriptTooShort, score_transcript

    with pytest.raises(TranscriptTooShort):
        score_transcript(transcript="too short", candidate_name="A", role="R")


def test_malformed_model_response_is_not_silently_repaired(monkeypatch):
    from webapp.services import values_scoring as vs

    bad = {"values": [{"name": "Don't Walk Away", "deepDive": "d",
                       "curveBall": "c", "microCase": "m", "rating": "+"}]}
    monkeypatch.setattr(vs, "_call_model", lambda **kw: (bad, "test-model"))
    with pytest.raises(vs.ValuesScorecardError):
        vs.score_transcript(transcript="x" * 3000, candidate_name="A", role="R")


def test_a_response_that_is_not_parseable_json_is_retried(monkeypatch):
    """_call_model can raise a plain ValueError (drafting._parse_json's "LLM
    did not return parseable JSON") before any ValuesScorecardError territory
    is reached. That must be retried exactly like a wrong-shape response."""
    from webapp.services import values_scoring as vs

    good = {
        "values": [
            {"name": n, "deepDive": "d", "curveBall": "c", "microCase": "m", "rating": "+"}
            for n in vs.VALUE_NAMES
        ],
    }
    calls = []

    def flaky(**kw):
        calls.append(kw)
        if len(calls) == 1:
            raise ValueError("Expecting value: line 1 column 1")
        return good, "test-model"

    monkeypatch.setattr(vs, "_call_model", flaky)
    out = vs.score_transcript(transcript="x" * 3000, candidate_name="A", role="R")
    assert out["verdict"] == "PASS"
    assert len(calls) == 2


def test_json_parse_failure_on_both_attempts_raises_scorecard_error_not_bare_value_error(monkeypatch):
    """Two consecutive parse failures must still surface as a single,
    handleable exception type, never a bare ValueError escaping the function."""
    from webapp.services import values_scoring as vs

    calls = []

    def always_broken(**kw):
        calls.append(kw)
        raise ValueError("Expecting value: line 1 column 1")

    monkeypatch.setattr(vs, "_call_model", always_broken)
    with pytest.raises(vs.ValuesScorecardError) as excinfo:
        vs.score_transcript(transcript="x" * 3000, candidate_name="A", role="R")
    assert type(excinfo.value) is vs.ValuesScorecardError
    assert len(calls) == 2


def _values(ratings):
    return [
        {"name": n, "deepDive": "d", "curveBall": "c", "microCase": "m", "rating": r}
        for n, r in zip(VALUE_NAMES, ratings)
    ]


def test_canonical_names_and_ratings():
    assert VALUE_NAMES == (
        "Don't Walk Away from Hard Things",
        "All for One & One for All",
        "Continuously Improve Our Craft",
        "Have Courageous Conversations",
        "Don't Hold On Too Tight",
        "Practice Joy",
    )
    assert RATINGS == ("+", "+/-", "-")


def test_verdict_exhaustively_over_every_possible_scorecard():
    # All 3^6 = 729 combinations. The rule must hold for every one.
    for combo in itertools.product(RATINGS, repeat=6):
        got = verdict(list(combo))
        minuses = combo.count("-")
        plus_minuses = combo.count("+/-")
        expected = "PASS" if (minuses == 0 and plus_minuses <= 2) else "OUT"
        assert got == expected, f"{combo}: got {got}, expected {expected}"


def test_verdict_named_cases():
    assert verdict(["+"] * 6) == "PASS"
    assert verdict(["+", "+", "+", "+", "+", "+/-"]) == "PASS"
    assert verdict(["+", "+", "+", "+", "+/-", "+/-"]) == "PASS"
    # Three plus-minuses is OUT even with no minus.
    assert verdict(["+", "+", "+", "+/-", "+/-", "+/-"]) == "OUT"
    # A single minus is OUT regardless of everything else.
    assert verdict(["+", "+", "+", "+", "+", "-"]) == "OUT"


def test_tally():
    assert tally(["+", "+", "+/-", "-", "+", "+/-"]) == {"plus": 3, "plus_minus": 2, "minus": 1}


def test_validate_rejects_wrong_shape():
    with pytest.raises(ValuesScorecardError):
        validate_values(_values(["+"] * 5)[:5])            # only five values
    with pytest.raises(ValuesScorecardError):
        bad = _values(["+"] * 6); bad[0]["name"] = "Don't Walk Away"
        validate_values(bad)                                # the OLD skill-file name
    with pytest.raises(ValuesScorecardError):
        bad = _values(["+"] * 6); bad[2], bad[3] = bad[3], bad[2]
        validate_values(bad)                                # out of canonical order
    with pytest.raises(ValuesScorecardError):
        bad = _values(["+"] * 6); bad[1]["rating"] = "++"
        validate_values(bad)                                # invalid rating token
    with pytest.raises(ValuesScorecardError):
        bad = _values(["+"] * 6); bad[4]["curveBall"] = "   "
        validate_values(bad)                                # blank evidence


def test_validate_accepts_the_not_observed_sentinel():
    ok = _values(["+"] * 6)
    ok[3]["curveBall"] = NOT_OBSERVED
    validate_values(ok)  # must not raise


def _ok_values():
    return [
        {"name": n, "deepDive": "d", "curveBall": "c", "microCase": "m", "rating": "+"}
        for n in VALUE_NAMES
    ]


def test_payload_shape_matches_the_live_records():
    p = build_markaz_payload(
        candidate_name="Muhammad Junaid",
        host="Ayesha Khan",
        values=_ok_values(),
        final_comments="PASS - 6(+) / 0(+/-) / 0(-)",
        proceed=True,
        date="Aug 14, 2026",
    )
    assert set(p) == MARKAZ_KEYS
    assert p["candidateName"] == "Muhammad Junaid"
    assert p["noteTaker"] == "Coco (AI P&C Assistant)"
    assert p["date"] == "Aug 14, 2026"
    # The live records store a STRING, not a boolean. 215 of 219.
    assert p["proceedToRightSeat"] == "Yes"
    assert isinstance(p["proceedToRightSeat"], str)
    assert [v["name"] for v in p["values"]] == list(VALUE_NAMES)


def test_proceed_false_is_the_string_no():
    p = build_markaz_payload(
        candidate_name="X", host="Ayesha Khan", values=_ok_values(),
        final_comments="OUT", proceed=False,
    )
    assert p["proceedToRightSeat"] == "No"


def test_payload_rejects_a_boolean_proceed_value():
    p = build_markaz_payload(
        candidate_name="X", host="Ayesha Khan", values=_ok_values(),
        final_comments="PASS", proceed=True,
    )
    p["proceedToRightSeat"] = True          # the shape the old skill file documented
    with pytest.raises(ValuesScorecardError):
        validate_markaz_payload(p)


def test_payload_rejects_extra_or_missing_keys():
    p = build_markaz_payload(
        candidate_name="X", host="Ayesha Khan", values=_ok_values(),
        final_comments="PASS", proceed=True,
    )
    with pytest.raises(ValuesScorecardError):
        validate_markaz_payload({**p, "extra": 1})
    with pytest.raises(ValuesScorecardError):
        validate_markaz_payload({k: v for k, v in p.items() if k != "noteTaker"})


def test_draft_table_lives_in_the_coco_schema():
    """public is inside Markaz's Replit schema-push blast radius; coco is not."""
    from webapp.models import ValuesScorecardDraft

    assert ValuesScorecardDraft.__table__.schema == "coco"


# --------------------------------------------------------------------------
# Task 6: the router. generate/read/edit are exercised directly against the
# route functions with a fake, in-memory Session (no live database, no real
# model call) -- these are unit tests of the router's own logic, not
# integration tests. submit() is deliberately never exercised against a real
# DATABASE_URL in this test file: it is the only code in the app that writes
# to Markaz's public.applications, and that write is verified by a human, not
# by CI. See task-6-brief.md.
# --------------------------------------------------------------------------


def test_submit_requires_approver_and_generate_requires_editor():
    from webapp.main import app

    def _routes():
        out = []
        def walk(rs):
            for r in rs:
                if hasattr(r, "path"):
                    out.append(r)
                elif hasattr(r, "original_router"):
                    walk(r.original_router.routes)
        walk(app.routes)
        return out

    paths = {r.path for r in _routes()}
    assert "/api/values-scorecards/generate" in paths
    assert "/api/values-scorecards/{draft_id}" in paths
    assert "/api/values-scorecards/{draft_id}/submit" in paths

    import webapp.routers.values_scorecards as m
    src = open(m.__file__, encoding="utf-8").read()
    # The submit endpoint must be gated on approver, not on any signed-in user.
    assert "require_approver" in src
    submit_block = src.split("def submit")[1]
    assert "get_current_user" not in submit_block


def test_submit_sql_touches_only_the_values_scorecard_column():
    """public.applications is Markaz's table. The UPDATE inside submit() must
    touch ONLY values_scorecard for the one target row -- never another
    column, never an INSERT, never a DELETE."""
    import webapp.routers.values_scorecards as m

    src = open(m.__file__, encoding="utf-8").read()
    submit_block = src.split("def submit")[1]
    # Qualified as public.applications (Minor 7) -- not the bare,
    # search_path-dependent name.
    assert "UPDATE public.applications SET values_scorecard" in submit_block
    assert "INSERT INTO" not in submit_block
    assert "DELETE FROM" not in submit_block
    for forbidden in (
        "values_interview_result", "values_interview_score",
        "values_interview_date", "values_interviewer_name",
    ):
        assert forbidden not in submit_block


# ---- Fakes for exercising the route functions directly ----------------


class _FakeResult:
    """Stands in for whatever a real SQLAlchemy `Result` needs to support at
    each of submit()'s call sites: `.rowcount` for the two UPDATEs,
    `.mappings().first()` for the `public.applications` read, `.scalar()`
    for the stale-duplicate lookup."""

    def __init__(self, rowcount=0, mapping_row=None, scalar_value=None):
        self.rowcount = rowcount
        self._mapping_row = mapping_row
        self._scalar_value = scalar_value

    def mappings(self):
        return self

    def first(self):
        return self._mapping_row

    def scalar(self):
        return self._scalar_value


class _FakeSession:
    """A minimal stand-in for a SQLAlchemy Session. No network, no engine.

    submit() now runs several distinct statements in one transaction (the
    conditional status flip, a `public.applications` read, an optional
    stale-duplicate lookup, the final UPDATE) -- `execute()` dispatches on a
    substring of the SQL text so each test can configure just the piece it
    cares about. Defaults reproduce the "happy path, no duplicates, no
    existing Markaz scorecard" case so tests written before submit() grew
    these extra checks keep working with no per-test setup.
    """

    def __init__(self):
        self.committed = 0
        self.rolled_back = 0
        self.execute_calls = []
        # Governs the conditional `SET status = 'submitted'` UPDATE.
        self.flip_rowcount = 1
        # Governs the final `UPDATE public.applications` write.
        self.execute_rowcount = 1
        # The CURRENT public.applications row read before the write. None
        # candidate_id/job_id skips the stale-duplicate check; None
        # values_scorecard skips the overwrite-refusal check.
        self.applications_row = {
            "values_scorecard": None, "candidate_id": None, "job_id": None,
        }
        # The id of the newest application sharing the target's
        # (candidate_id, job_id) pair. None (or equal to the draft's own
        # application_id) means "the target already is the newest."
        self.newer_application_id = None
        self._store = {}

    def add(self, obj):
        self._store[getattr(obj, "id", None)] = obj

    def commit(self):
        self.committed += 1

    def rollback(self):
        self.rolled_back += 1

    def refresh(self, obj):
        pass

    def get(self, model, id_):
        return self._store.get(id_)

    def execute(self, stmt, params=None):
        sql = str(stmt)
        self.execute_calls.append((sql, params))
        if "SET status = 'submitted'" in sql:
            return _FakeResult(rowcount=self.flip_rowcount)
        if "SELECT values_scorecard, candidate_id, job_id" in sql:
            return _FakeResult(mapping_row=self.applications_row)
        if "ORDER BY updated_at DESC LIMIT 1" in sql:
            return _FakeResult(scalar_value=self.newer_application_id)
        if "UPDATE public.applications SET values_scorecard" in sql:
            return _FakeResult(rowcount=self.execute_rowcount)
        return _FakeResult(rowcount=self.execute_rowcount)


def _fake_app_row(application_id=101):
    return {
        "application_id": application_id,
        "candidate_id": 55,
        "first_name": "Amina",
        "last_name": "Raza",
        "job_title": "Growth Manager",
        "job_pk": 7,
    }


def _make_draft(**overrides):
    from webapp.models import ValuesScorecardDraft

    defaults = dict(
        id="vsd-test",
        application_id=101,
        candidate_name="Amina Raza",
        host="Ayesha Khan",
        transcript_sha256="abc123",
        values_json=_ok_values(),
        final_comments="PASS - 6(+) / 0(+/-) / 0(-)",
        proceed=True,
        gwc={"gets_it": "Yes", "wants_it": "Yes", "capacity": "Yes"},
        status="draft",
        model_name="test-model",
        created_by="appuser-editor",
    )
    defaults.update(overrides)
    return ValuesScorecardDraft(**defaults)


def test_generate_builds_draft_with_computed_verdict_and_proceed(monkeypatch):
    import hashlib

    import webapp.routers.values_scorecards as router_mod
    from webapp.schemas import ValuesScorecardGenerateRequest

    monkeypatch.setattr(
        router_mod.reads, "get_application", lambda db, app_id: _fake_app_row(app_id)
    )
    scored = {
        "values": _ok_values(),
        "gwc": {"gets_it": "Yes", "wants_it": "Yes", "capacity": "Yes"},
        "tally": {"plus": 6, "plus_minus": 0, "minus": 0},
        "verdict": "PASS",
        "model": "test-model",
    }
    monkeypatch.setattr(router_mod, "score_transcript", lambda **kw: scored)

    db = _FakeSession()
    transcript = "x" * 3000
    body = ValuesScorecardGenerateRequest(
        application_id=101, transcript=transcript, host="Ayesha Khan"
    )
    out = router_mod.generate(body, db, {"id": "appuser-editor"})

    assert out["candidate_name"] == "Amina Raza"          # first + last from the application
    assert out["verdict"] == "PASS"                        # computed, matches the scored verdict
    assert out["proceed"] is True                           # default: proceed follows PASS
    assert out["final_comments"] == "PASS - 6(+) / 0(+/-) / 0(-)"
    assert out["status"] == "draft"
    assert out["transcript_sha256"] == hashlib.sha256(transcript.encode("utf-8")).hexdigest()
    assert db.committed == 1


def test_generate_refuses_a_short_transcript(monkeypatch):
    import webapp.routers.values_scorecards as router_mod
    from webapp.schemas import ValuesScorecardGenerateRequest

    monkeypatch.setattr(
        router_mod.reads, "get_application", lambda db, app_id: _fake_app_row(app_id)
    )

    def _raise(**kw):
        raise router_mod.TranscriptTooShort("transcript is too short")

    monkeypatch.setattr(router_mod, "score_transcript", _raise)

    db = _FakeSession()
    body = ValuesScorecardGenerateRequest(application_id=101, transcript="too short", host="Ayesha Khan")
    with pytest.raises(HTTPException) as exc:
        router_mod.generate(body, db, {"id": "appuser-editor"})
    assert exc.value.status_code == 422


def test_edit_recomputes_verdict_and_drops_gwc_when_the_new_verdict_is_out():
    import webapp.routers.values_scorecards as router_mod
    from webapp.schemas import ValuesScorecardEdit

    draft = _make_draft(id="vsd-1")
    db = _FakeSession()
    db._store["vsd-1"] = draft

    edited = _values(["+", "+", "+", "+", "+", "-"])  # one minus -> OUT
    out = router_mod.edit_draft("vsd-1", ValuesScorecardEdit(values=edited), db, {"id": "appuser-editor"})

    assert out["verdict"] == "OUT"
    assert out["gwc"] is None       # GWC dropped, never a back door around a failing round
    assert out["proceed"] is False  # follows the recomputed verdict
    assert db.committed == 1


def test_edit_refuses_a_draft_that_is_already_submitted():
    import webapp.routers.values_scorecards as router_mod
    from webapp.schemas import ValuesScorecardEdit

    draft = _make_draft(id="vsd-2", status="submitted")
    db = _FakeSession()
    db._store["vsd-2"] = draft

    with pytest.raises(HTTPException) as exc:
        router_mod.edit_draft("vsd-2", ValuesScorecardEdit(final_comments="x"), db, {"id": "appuser-editor"})
    assert exc.value.status_code == 409


def test_submit_writes_the_payload_and_marks_the_draft_submitted():
    import webapp.routers.values_scorecards as router_mod

    draft = _make_draft(id="vsd-3", application_id=202, candidate_name="Bilal Tariq")
    db = _FakeSession()
    db._store["vsd-3"] = draft
    db.execute_rowcount = 1

    out = router_mod.submit("vsd-3", db=db, user={"id": "appuser-approver"})

    assert out["status"] == "submitted"
    assert out["approved_by"] == "appuser-approver"
    assert out["approved_at"] is not None
    assert out["submitted_at"] is not None
    assert out["markaz_payload"]["candidateName"] == "Bilal Tariq"
    assert db.committed == 1
    assert db.rolled_back == 0

    # submit() now runs the conditional status flip, a public.applications
    # read (Critical 4/5), and the final write -- the LAST call is the write,
    # and it targets exactly one application_id, qualified as public.applications.
    sql_text, params = db.execute_calls[-1]
    assert "UPDATE public.applications" in sql_text
    assert "values_scorecard" in sql_text
    assert params["app_id"] == 202
    # And the FIRST call is the atomic status-flip guard (Critical 1).
    assert "SET status = 'submitted'" in db.execute_calls[0][0]


def test_submit_rolls_back_and_raises_if_the_row_count_is_not_exactly_one():
    import webapp.routers.values_scorecards as router_mod

    draft = _make_draft(id="vsd-4", application_id=303)
    db = _FakeSession()
    db._store["vsd-4"] = draft
    db.execute_rowcount = 0  # simulate a row that no longer matches

    with pytest.raises(HTTPException) as exc:
        router_mod.submit("vsd-4", db=db, user={"id": "appuser-approver"})
    assert exc.value.status_code == 500
    assert db.rolled_back == 1
    assert db.committed == 0
    assert draft.status == "draft"      # never mutated on a failed write
    assert draft.markaz_payload is None


def test_submit_refuses_a_second_submission_without_writing_again():
    import webapp.routers.values_scorecards as router_mod

    draft = _make_draft(id="vsd-5", application_id=404, status="submitted")
    db = _FakeSession()
    db._store["vsd-5"] = draft

    with pytest.raises(HTTPException) as exc:
        router_mod.submit("vsd-5", db=db, user={"id": "appuser-approver"})
    assert exc.value.status_code == 409
    assert len(db.execute_calls) == 0  # a double-click must never re-attempt the write


def test_submit_logs_the_payload_verbatim_before_the_final_write(monkeypatch):
    """The log line must immediately precede the WRITE, not the earlier reads
    (the conditional status flip, the public.applications lookup)."""
    import webapp.routers.values_scorecards as router_mod

    order = []

    class _TracingLogger:
        def info(self, *args, **kwargs):
            order.append("log")

    def _tag(sql: str) -> str:
        if "SET status = 'submitted'" in sql:
            return "execute:flip"
        if "SELECT values_scorecard" in sql:
            return "execute:read_application"
        if "ORDER BY updated_at" in sql:
            return "execute:duplicate_check"
        if "UPDATE public.applications" in sql:
            return "execute:write"
        return "execute:other"

    class _TracingSession(_FakeSession):
        def execute(self, stmt, params=None):
            result = super().execute(stmt, params)
            order.append(_tag(str(stmt)))
            return result

    monkeypatch.setattr(router_mod, "log", _TracingLogger())

    draft = _make_draft(id="vsd-6", application_id=505)
    db = _TracingSession()
    db._store["vsd-6"] = draft

    router_mod.submit("vsd-6", db=db, user={"id": "appuser-approver"})

    assert order[-2:] == ["log", "execute:write"]
    assert order.count("log") == 1


# --------------------------------------------------------------------------
# Task-6 fix pass (2026-09-17): the write-path criticals + the duplicate-
# application trap. Same _FakeSession, configured per test to surface the
# specific condition each fix addresses.
# --------------------------------------------------------------------------


def test_submit_rejects_a_concurrent_double_click_via_the_atomic_flip():
    """The guard is the conditional UPDATE itself, not a prior read: if it
    matches zero rows (a concurrent request already flipped it, or won a
    row-lock race), submit must 409 and touch nothing else."""
    import webapp.routers.values_scorecards as router_mod

    draft = _make_draft(id="vsd-7", application_id=606)
    db = _FakeSession()
    db._store["vsd-7"] = draft
    db.flip_rowcount = 0  # simulates a concurrent request that won the race

    with pytest.raises(HTTPException) as exc:
        router_mod.submit("vsd-7", db=db, user={"id": "appuser-approver"})
    assert exc.value.status_code == 409
    assert len(db.execute_calls) == 1           # only the flip was attempted
    assert draft.status == "draft"               # in-memory draft untouched
    assert draft.markaz_payload is None


def test_submit_clamps_proceed_false_on_an_out_verdict_even_if_stored_true():
    """A draft can end up with proceed=True stored against ratings that are
    actually OUT. submit() must never let that become a permanent 'Yes' in
    Markaz -- re-derive it from the current ratings, defensively, again."""
    import webapp.routers.values_scorecards as router_mod

    out_values = _values(["+", "+", "+", "+", "+", "-"])  # one minus -> OUT
    draft = _make_draft(id="vsd-8", application_id=707, values_json=out_values, proceed=True)
    db = _FakeSession()
    db._store["vsd-8"] = draft

    out = router_mod.submit("vsd-8", db=db, user={"id": "appuser-approver"})

    assert out["markaz_payload"]["proceedToRightSeat"] == "No"
    assert out["proceed"] is False
    assert draft.proceed is False


def test_submit_recomputes_final_comments_from_current_ratings():
    """final_comments must never assert a verdict/tally that disagrees with
    the CURRENT ratings, even when the stored string is stale."""
    import webapp.routers.values_scorecards as router_mod

    out_values = _values(["+", "+", "+", "+", "+", "-"])  # one minus -> OUT
    draft = _make_draft(
        id="vsd-9", application_id=808, values_json=out_values, proceed=True,
        final_comments="PASS - 6(+) / 0(+/-) / 0(-)",  # stale
    )
    db = _FakeSession()
    db._store["vsd-9"] = draft

    out = router_mod.submit("vsd-9", db=db, user={"id": "appuser-approver"})

    assert out["markaz_payload"]["finalComments"] == "OUT - 5(+) / 0(+/-) / 1(-)"
    assert out["final_comments"] == "OUT - 5(+) / 0(+/-) / 1(-)"


def test_submit_refuses_to_overwrite_an_existing_markaz_scorecard():
    import webapp.routers.values_scorecards as router_mod

    draft = _make_draft(id="vsd-10", application_id=909)
    db = _FakeSession()
    db._store["vsd-10"] = draft
    db.applications_row = {
        "values_scorecard": {"candidateName": "Someone Else"},
        "candidate_id": None, "job_id": None,
    }

    with pytest.raises(HTTPException) as exc:
        router_mod.submit("vsd-10", db=db, user={"id": "appuser-approver"})
    assert exc.value.status_code == 409
    assert "909" in exc.value.detail
    assert not any(
        "UPDATE public.applications SET values_scorecard" in sql
        for sql, _ in db.execute_calls
    )
    assert draft.status == "draft"


def test_submit_overwrite_flag_replaces_and_preserves_the_prior_payload():
    import webapp.routers.values_scorecards as router_mod
    from webapp.schemas import ValuesScorecardSubmitRequest

    draft = _make_draft(id="vsd-11", application_id=1010, candidate_name="Zara Iqbal")
    db = _FakeSession()
    db._store["vsd-11"] = draft
    prior = {"candidateName": "Someone Else", "finalComments": "an old human-written scorecard"}
    db.applications_row = {"values_scorecard": prior, "candidate_id": None, "job_id": None}

    out = router_mod.submit(
        "vsd-11", body=ValuesScorecardSubmitRequest(overwrite=True),
        db=db, user={"id": "appuser-approver"},
    )

    assert out["status"] == "submitted"
    assert out["markaz_payload"]["candidateName"] == "Zara Iqbal"
    assert out["replaced_payload"] == prior
    assert draft.replaced_payload == prior


def test_submit_refuses_a_stale_duplicate_application():
    """Markaz's UI displays the most recently updated application for a
    (candidate_id, job_id) pair. Writing to an older duplicate of the same
    pair must be refused, naming the newer id -- never silently redirected."""
    import webapp.routers.values_scorecards as router_mod

    draft = _make_draft(id="vsd-12", application_id=1111)
    db = _FakeSession()
    db._store["vsd-12"] = draft
    db.applications_row = {"values_scorecard": None, "candidate_id": 55, "job_id": 7}
    db.newer_application_id = 2708  # a newer duplicate exists

    with pytest.raises(HTTPException) as exc:
        router_mod.submit("vsd-12", db=db, user={"id": "appuser-approver"})
    assert exc.value.status_code == 409
    assert "2708" in exc.value.detail
    assert draft.status == "draft"


def test_submit_proceeds_when_the_target_is_already_the_newest_duplicate():
    import webapp.routers.values_scorecards as router_mod

    draft = _make_draft(id="vsd-13", application_id=1212)
    db = _FakeSession()
    db._store["vsd-13"] = draft
    db.applications_row = {"values_scorecard": None, "candidate_id": 55, "job_id": 7}
    db.newer_application_id = 1212  # the target IS the newest

    out = router_mod.submit("vsd-13", db=db, user={"id": "appuser-approver"})
    assert out["status"] == "submitted"


def test_submit_skips_the_duplicate_check_when_ids_are_null():
    import webapp.routers.values_scorecards as router_mod

    draft = _make_draft(id="vsd-14", application_id=1313)
    db = _FakeSession()
    db._store["vsd-14"] = draft
    db.applications_row = {"values_scorecard": None, "candidate_id": None, "job_id": None}
    db.newer_application_id = 9999  # would be a hit, but must never be checked

    out = router_mod.submit("vsd-14", db=db, user={"id": "appuser-approver"})
    assert out["status"] == "submitted"
    assert not any("ORDER BY updated_at" in sql for sql, _ in db.execute_calls)


def test_submit_stores_approved_by_as_id_and_email():
    import webapp.routers.values_scorecards as router_mod

    draft = _make_draft(id="vsd-15", application_id=1414)
    db = _FakeSession()
    db._store["vsd-15"] = draft

    out = router_mod.submit(
        "vsd-15", db=db,
        user={"id": "appuser-approver", "email": "ayesha.khan@taleemabad.com"},
    )
    assert out["approved_by"] == "appuser-approver ayesha.khan@taleemabad.com"


def test_edit_raises_422_not_500_on_a_bad_rating_token():
    """A predictable input error (a bad rating token) must return 422 with
    the message, never escape as an uncaught 500."""
    import webapp.routers.values_scorecards as router_mod
    from webapp.schemas import ValuesScorecardEdit

    draft = _make_draft(id="vsd-16")
    db = _FakeSession()
    db._store["vsd-16"] = draft

    bad_values = _values(["+"] * 6)
    bad_values[2]["rating"] = "++"  # not one of the RATINGS tokens
    with pytest.raises(HTTPException) as exc:
        router_mod.edit_draft(
            "vsd-16", ValuesScorecardEdit(values=bad_values), db, {"id": "appuser-editor"}
        )
    assert exc.value.status_code == 422


def test_edit_raises_422_on_blank_evidence():
    import webapp.routers.values_scorecards as router_mod
    from webapp.schemas import ValuesScorecardEdit

    draft = _make_draft(id="vsd-17")
    db = _FakeSession()
    db._store["vsd-17"] = draft

    bad_values = _values(["+"] * 6)
    bad_values[4]["curveBall"] = "   "
    with pytest.raises(HTTPException) as exc:
        router_mod.edit_draft(
            "vsd-17", ValuesScorecardEdit(values=bad_values), db, {"id": "appuser-editor"}
        )
    assert exc.value.status_code == 422


def test_generate_maps_an_unexpected_model_failure_to_503_not_500(monkeypatch):
    import webapp.routers.values_scorecards as router_mod
    from webapp.schemas import ValuesScorecardGenerateRequest

    monkeypatch.setattr(
        router_mod.reads, "get_application", lambda db, app_id: _fake_app_row(app_id)
    )

    def _boom(**kw):
        raise RuntimeError("connection reset")

    monkeypatch.setattr(router_mod, "score_transcript", _boom)

    db = _FakeSession()
    body = ValuesScorecardGenerateRequest(
        application_id=101, transcript="x" * 3000, host="Ayesha Khan"
    )
    with pytest.raises(HTTPException) as exc:
        router_mod.generate(body, db, {"id": "appuser-editor"})
    assert exc.value.status_code == 503


def test_edit_refuses_client_proceed_true_on_an_out_scorecard():
    """An editor (below the approver gate) must never be able to force
    proceed=True on a scorecard the locked rule already failed."""
    import webapp.routers.values_scorecards as router_mod
    from webapp.schemas import ValuesScorecardEdit

    draft = _make_draft(id="vsd-18")
    db = _FakeSession()
    db._store["vsd-18"] = draft

    edited = _values(["+", "+", "+", "+", "+", "-"])  # one minus -> OUT
    out = router_mod.edit_draft(
        "vsd-18", ValuesScorecardEdit(values=edited, proceed=True), db, {"id": "appuser-editor"}
    )
    assert out["verdict"] == "OUT"
    assert out["proceed"] is False  # the client's proceed=True is ignored


def test_edit_allows_client_proceed_false_on_a_passing_verdict():
    """A client MAY set proceed=False even when the verdict is PASS (e.g. a
    GWC failure) -- only forcing True on a failing verdict is blocked."""
    import webapp.routers.values_scorecards as router_mod
    from webapp.schemas import ValuesScorecardEdit

    draft = _make_draft(id="vsd-19")  # PASS by default
    db = _FakeSession()
    db._store["vsd-19"] = draft

    out = router_mod.edit_draft(
        "vsd-19", ValuesScorecardEdit(proceed=False), db, {"id": "appuser-editor"}
    )
    assert out["verdict"] == "PASS"
    assert out["proceed"] is False


def test_get_draft_requires_editor_not_a_bare_signed_in_user():
    import webapp.routers.values_scorecards as m

    src = open(m.__file__, encoding="utf-8").read()
    get_block = src.split("def get_draft")[1].split("def edit_draft")[0]
    assert "require_editor" in get_block
    # Not imported (a draft carries the candidate's name plus verbatim
    # interview evidence -- Controller Ruling 9). Check the import line and
    # every dependency wiring, not the module docstring's own mention of it.
    assert "get_current_user" not in m.get_draft.__globals__
    assert "Depends(get_current_user)" not in src


def test_recompute_final_comments_keeps_narrative_after_the_prefix():
    from webapp.services.values_scoring import recompute_final_comments

    out = recompute_final_comments(
        ["+", "+", "+", "+", "+", "-"],
        "PASS - 6(+) / 0(+/-) / 0(-) - strong across the board",
    )
    assert out == "OUT - 5(+) / 0(+/-) / 1(-) - strong across the board"


def test_recompute_final_comments_prepends_when_no_prior_prefix():
    from webapp.services.values_scoring import recompute_final_comments

    out = recompute_final_comments(["+"] * 6, "a freeform note with no prefix")
    assert out == "PASS - 6(+) / 0(+/-) / 0(-) - a freeform note with no prefix"
