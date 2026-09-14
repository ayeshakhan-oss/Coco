"""The hiring manager's blunt note must never reach the writer verbatim.

Why this file exists (2026-09-14, app 3869): the drafter was handed the
manager's private note as its evidence and the send gate then forbade it from
reusing any four consecutive content words of it. That instruction cannot
converge. Each retry wrote a WHOLE NEW LETTER that avoided the single phrase it
had been told about and echoed a different one instead:

    attempt 1  "one government adjacent example"   -> HARD BLOCK
    attempt 2  "remote night shift job"            -> HARD BLOCK

Two hard blocks in front of Ayesha, on two separate letters, for the same
structural reason. The fix is that the writer no longer reads the note at all.

The property under test is the safety one: when translation FAILS, the field is
dropped, never passed through raw. A silent fallback to the raw note would
reinstate the exact bug.

Run: python -m pytest webapp/tests/test_manager_note_translation.py
"""

from __future__ import annotations

import pytest

from webapp.services import drafting

RAW_NOTE = (
    "Motivation reads circumstantial, wants out of a remote night-shift job, "
    "more than mission-driven. His one government-adjacent example does not "
    "translate to education bureaucracy."
)

CLEAN = (
    "We were not able to understand what was drawing this candidate toward our "
    "particular mission as clearly as we needed to. For this position we also "
    "needed direct familiarity with how public education systems operate day to "
    "day, and we could not establish enough of that through the process."
)


@pytest.fixture(autouse=True)
def _clear_translation_cache():
    """Translations are cached per (note, role) so regenerating a draft costs no
    extra model call. Without this fixture the cache leaks between tests and a
    failure case silently reads an earlier test's successful translation, which
    is exactly what happened when the cache was first added."""
    drafting._NOTE_CACHE.clear()
    yield
    drafting._NOTE_CACHE.clear()


class _FakeDrafter:
    """Returns a scripted translation, or raises, without touching the network."""

    name = "fake"

    def __init__(self, result=None, *, explode=False):
        self.result = result
        self.explode = explode
        self.calls = 0

    def draft(self, *, system, user, email_type, first_name, role,
              prior_violations=None, attempt=0):
        self.calls += 1
        if self.explode:
            raise RuntimeError("model unreachable")
        return {"rationale": self.result}


def test_leak_detector_sees_a_four_word_echo():
    assert drafting._leaks_from("your one government adjacent example was thin", RAW_NOTE)
    assert not drafting._leaks_from(CLEAN, RAW_NOTE)


def test_a_clean_translation_replaces_the_raw_note():
    sc = {"final_comments": RAW_NOTE, "values": [{"name": "X", "rating": "+"}]}
    out, warnings = drafting._soften_manager_notes(
        _FakeDrafter(CLEAN), sc, role="Growth Manager"
    )
    assert out["final_comments"] == CLEAN
    assert RAW_NOTE not in out["final_comments"]
    assert warnings == []


def test_a_failed_translation_DROPS_the_note_and_never_passes_it_raw():
    """The property that matters. Falling back to the raw note would put the
    manager's wording back in front of the writer and the leak would return."""
    sc = {"final_comments": RAW_NOTE, "values": [{"name": "X", "rating": "+"}]}
    out, warnings = drafting._soften_manager_notes(
        _FakeDrafter(explode=True), sc, role="Growth Manager"
    )
    assert "final_comments" not in out, "the raw note survived a failed translation"
    assert warnings == ["final_comments"]


def test_a_translation_that_still_echoes_is_rejected_then_dropped():
    """Two attempts, both echoing -> treated as a failure, so the note is
    dropped rather than handed over."""
    echoing = "He wants out of a remote night-shift job."
    fake = _FakeDrafter(echoing)
    sc = {"additional_comments": RAW_NOTE, "competencies": [{"name": "c", "score": 7}]}
    out, warnings = drafting._soften_manager_notes(fake, sc, role="Growth Manager")
    assert fake.calls == 2, "should retry once before giving up"
    assert "additional_comments" not in out
    assert warnings == ["additional_comments"]


def test_warm_bench_softens_both_scorecards():
    sc = {
        "kind": "values_and_gwc",
        "values": {"final_comments": RAW_NOTE, "values": []},
        "gwc": {"additional_comments": RAW_NOTE, "competencies": []},
    }
    out, warnings = drafting._soften_manager_notes(
        _FakeDrafter(CLEAN), sc, role="Growth Manager"
    )
    assert out["values"]["final_comments"] == CLEAN
    assert out["gwc"]["additional_comments"] == CLEAN
    assert warnings == []


def test_the_candidates_own_stories_are_never_touched():
    """deep_dive / curve_ball / micro_case record what the CANDIDATE said. They
    are what make the letter personal, the leakage gate never covered them, and
    softening them would strip the letter of its evidence."""
    story = "I had put in my blood and sweat in this project."
    sc = {
        "final_comments": RAW_NOTE,
        "values": [{"name": "Hard Things", "rating": "+", "deep_dive": story,
                    "curve_ball": story, "micro_case": story}],
    }
    out, _ = drafting._soften_manager_notes(_FakeDrafter(CLEAN), sc, role="GM")
    v = out["values"][0]
    assert v["deep_dive"] == story
    assert v["curve_ball"] == story
    assert v["micro_case"] == story


@pytest.mark.parametrize("empty", [None, "", "   "])
def test_an_absent_note_costs_no_model_call(empty):
    fake = _FakeDrafter(CLEAN)
    sc = {"final_comments": empty, "values": []}
    out, warnings = drafting._soften_manager_notes(fake, sc, role="GM")
    assert fake.calls == 0
    assert warnings == []


def test_a_second_draft_reuses_the_cached_translation():
    """Regenerating must not re-pay for the translation. The drafting credential
    is rate limited, and every 429 costs a dropped note and a thinner letter."""
    fake = _FakeDrafter(CLEAN)
    sc = {"final_comments": RAW_NOTE, "values": []}
    first, _ = drafting._soften_manager_notes(fake, sc, role="Growth Manager")
    second, _ = drafting._soften_manager_notes(fake, sc, role="Growth Manager")
    assert fake.calls == 1, "the second draft called the model again"
    assert first["final_comments"] == second["final_comments"] == CLEAN


def test_the_cache_is_keyed_by_role_too():
    fake = _FakeDrafter(CLEAN)
    sc = {"final_comments": RAW_NOTE, "values": []}
    drafting._soften_manager_notes(fake, sc, role="Growth Manager")
    drafting._soften_manager_notes(fake, sc, role="Senior Manager Growth")
    assert fake.calls == 2, "a different role must get its own translation"
