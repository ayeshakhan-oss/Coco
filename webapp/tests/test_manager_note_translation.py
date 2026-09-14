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


# --- model fallback -------------------------------------------------------
# ANTHROPIC_MODEL is set by hand on Railway. A typo or a retired id must not
# turn every draft into an empty scaffold: it fails over and says so loudly.

class _FakeMessages:
    def __init__(self, servable):
        self.servable = servable
        self.asked: list[str] = []

    def create(self, *, model, max_tokens, system, messages):
        self.asked.append(model)
        if model not in self.servable:
            raise RuntimeError(
                f"Error code: 404 - {{'type':'error','error':"
                f"{{'type':'not_found_error','message':'model: {model}'}}}}"
            )

        class _Blk:
            type = "text"
            text = '{"rationale": "ok", "sections": [], "title_line": "t"}'

        class _Msg:
            content = [_Blk()]

        return _Msg()


def _drafter_with(servable, configured):
    d = drafting.AnthropicDrafter.__new__(drafting.AnthropicDrafter)
    d.model = configured
    d.degraded_from = None
    d.mode = "api_key"
    d.client = type("C", (), {"messages": _FakeMessages(servable)})()
    return d


def test_a_good_model_is_used_as_is():
    d = _drafter_with({"claude-sonnet-5"}, "claude-sonnet-5")
    d.draft(system="s", user="u", email_type="warm_bench", first_name="A", role="R")
    assert d.client.messages.asked == ["claude-sonnet-5"]
    assert d.model == "claude-sonnet-5"


def test_an_unknown_model_falls_back_and_sticks():
    d = _drafter_with({"claude-haiku-4-5-20251001"}, "claude-sonnet-5-typo")
    d.draft(system="s", user="u", email_type="warm_bench", first_name="A", role="R")
    assert d.client.messages.asked[0] == "claude-sonnet-5-typo"
    assert d.model == "claude-haiku-4-5-20251001", "should stick to what worked"
    d.draft(system="s", user="u", email_type="warm_bench", first_name="A", role="R")
    assert d.client.messages.asked[-1] == "claude-haiku-4-5-20251001"


def test_a_rate_limited_model_falls_back_instead_of_returning_nothing():
    """The real failure, 2026-09-14: ANTHROPIC_MODEL was moved to Sonnet, whose
    quota on this Claude Code subscription token was exhausted while Haiku still
    answered. Every call 429'd, so Ayesha got a 92-word empty scaffold with no
    explanation. A weaker letter that SAYS it is weaker beats no letter."""
    d = _drafter_with({"claude-haiku-4-5-20251001"}, "claude-sonnet-5")
    real = d.client.messages.create

    def _create(**kw):
        if kw["model"] != "claude-haiku-4-5-20251001":
            raise RuntimeError("Error code: 429 - {'type':'rate_limit_error'}")
        return real(**kw)

    d.client.messages.create = _create
    d.draft(system="s", user="u", email_type="warm_bench", first_name="A", role="R")
    assert d.model == "claude-haiku-4-5-20251001"
    assert d.degraded_from == "claude-sonnet-5", "the downgrade must be recorded"


def test_a_real_outage_is_not_swallowed():
    """Only unusable-model and rate-limit errors fall back. An outage, a bad
    request or an auth failure must surface rather than quietly downgrade."""
    d = _drafter_with(set(), "claude-sonnet-5")
    d.client.messages.create = lambda **kw: (_ for _ in ()).throw(
        RuntimeError("Error code: 500 - internal_server_error")
    )
    with pytest.raises(RuntimeError, match="500"):
        d.draft(system="s", user="u", email_type="warm_bench", first_name="A", role="R")


def test_an_undegraded_drafter_records_nothing():
    d = _drafter_with({"claude-sonnet-5"}, "claude-sonnet-5")
    d.draft(system="s", user="u", email_type="warm_bench", first_name="A", role="R")
    assert d.degraded_from is None


# --- the reviewer returns edits, not the whole letter ----------------------
# Reproducing ~1,000 words to change two sentences is a heavy load for a small
# model, and every re-emission risks dropping or mangling something. The drafter
# runs on Haiku whenever the Sonnet quota is out, so the reviewer reads prose and
# returns only the sentences it wants changed.

LETTER = {
    "title_line": "T",
    "greeting": "Dear A,",
    "opening": ["This is not a yes for now.", "You told us about the client."],
    "sections": [{"subhead": None, "paragraphs": [
        "That's the kind of person who holds space for people.",
        "We could not establish direct experience.",
    ]}],
    "ps": "You've proven you can learn hard things.",
}


def test_edits_are_applied_where_they_match():
    edits = [
        {"find": "That's the kind of person who holds space for people.",
         "replace": "What stayed with us was that you carried something for people who were not in the room."},
        {"find": "You've proven you can learn hard things.",
         "replace": "That moment stayed with us, and we wanted to say so plainly before we close."},
    ]
    out, applied, skipped = drafting._apply_edits(LETTER, edits)
    assert (applied, skipped) == (2, 0)
    assert "kind of person" not in out["sections"][0]["paragraphs"][0]
    assert "proven" not in out["ps"]
    # Untouched text must survive byte for byte.
    assert out["opening"] == LETTER["opening"]
    assert out["sections"][0]["paragraphs"][1] == "We could not establish direct experience."


def test_an_edit_that_does_not_match_is_discarded_not_guessed():
    """A fuzzy match would let the reviewer rewrite a sentence it never meant to
    touch. A visible defect beats a silent wrong edit."""
    out, applied, skipped = drafting._apply_edits(
        LETTER, [{"find": "a sentence that is not in the letter", "replace": "x"}])
    assert (applied, skipped) == (0, 1)
    assert out == LETTER


def test_an_ambiguous_edit_is_discarded():
    doubled = {**LETTER, "opening": ["Repeated line.", "Repeated line."],
               "sections": [{"subhead": None, "paragraphs": ["Repeated line."]}]}
    out, applied, skipped = drafting._apply_edits(
        doubled, [{"find": "Repeated line.", "replace": "y"}])
    assert (applied, skipped) == (0, 1)


def test_the_letter_is_handed_over_as_prose_not_json():
    text = drafting._letter_as_text(LETTER)
    assert "Dear A," in text and "P.S. You've proven" in text
    assert "{" not in text and '"paragraphs"' not in text


def test_review_pass_applies_edits_end_to_end():
    class _EditDrafter:
        name = "fake"

        def draft(self, **kw):
            return {"edits": [{
                "find": "That's the kind of person who holds space for people.",
                "replace": "What stayed with us was that you carried something for others.",
                "why": "person-level judgement"}]}

    out, status = drafting._review_pass(
        _EditDrafter(), LETTER, email_type="warm_bench", first_name="A", role="R")
    assert status == "applied"
    assert "kind of person" not in out["sections"][0]["paragraphs"][0]


def test_an_empty_edit_list_is_a_real_answer_not_a_failure():
    class _CleanDrafter:
        name = "fake"

        def draft(self, **kw):
            return {"edits": []}

    out, status = drafting._review_pass(
        _CleanDrafter(), LETTER, email_type="warm_bench", first_name="A", role="R")
    assert status == "skipped"
    assert out == LETTER


def test_the_old_whole_letter_shape_still_works():
    """Belt and braces: a model that answers in the previous contract is honoured."""
    class _OldDrafter:
        name = "fake"

        def draft(self, **kw):
            return {**LETTER, "sections": [{"subhead": None, "paragraphs": ["Rewritten."]}]}

    out, status = drafting._review_pass(
        _OldDrafter(), LETTER, email_type="warm_bench", first_name="A", role="R")
    assert status == "applied"
    assert out["sections"][0]["paragraphs"] == ["Rewritten."]


@pytest.fixture(autouse=True)
def _clear_unusable_models():
    """The unusable-model memo is process-wide by design; isolate it per test."""
    drafting.AnthropicDrafter._unusable.clear()
    yield
    drafting.AnthropicDrafter._unusable.clear()


def test_a_dead_model_is_remembered_across_requests():
    """get_drafter() builds a fresh drafter per request. Without a process-wide
    memo every draft re-probed the rate-limited model and paid the SDK backoff
    again, which is how one generate ran long enough to 502."""
    first = _drafter_with({"claude-haiku-4-5-20251001"}, "claude-sonnet-5")
    first.draft(system="s", user="u", email_type="warm_bench", first_name="A", role="R")
    assert "claude-sonnet-5" in drafting.AnthropicDrafter._unusable

    second = _drafter_with({"claude-haiku-4-5-20251001"}, "claude-sonnet-5")
    # A fresh drafter must not ask the dead model again.
    second.model = "claude-sonnet-5"
    if second.model in drafting.AnthropicDrafter._unusable:
        for c in drafting.AnthropicDrafter._FALLBACK_MODELS:
            if c not in drafting.AnthropicDrafter._unusable:
                second.degraded_from, second.model = second.model, c
                break
    second.draft(system="s", user="u", email_type="warm_bench", first_name="A", role="R")
    assert "claude-sonnet-5" not in second.client.messages.asked, \
        "the second request re-probed a model already known to be dead"
