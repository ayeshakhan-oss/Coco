"""generate_draft must actually RUN. Nothing exercised the loop until now.

2026-09-15: a multi-part edit aborted halfway, so the loop used a variable
(`repaired_this_attempt`) that was never assigned. 88 tests passed, the deploy
went green, and EVERY regeneration in production returned:

    NameError: name 'repaired_this_attempt' is not defined
    POST /api/communications/generate -> 500

Ayesha clicked Generate on Abdul Wahab's letter and nothing happened. The same
shape as the send-path signature bug: a code path with no test, so a break in it
is invisible until a human hits it.

These tests run the real loop against a scripted drafter. No network.

Run: python -m pytest webapp/tests/test_generate_draft_loop.py
"""

from __future__ import annotations

import pytest

from webapp.services import drafting

SCORECARD = {
    "kind": "values",
    "final_comments": "Strong operator. Could not evidence government relationships.",
    "values": [{"name": "Don't Walk Away", "rating": "+",
                "deep_dive": "Revived a stalled deal by restructuring the quote."}],
}

GOOD_PARA = (
    "There is a moment from your values conversation that the panel kept returning to. "
    "You described a deal that had stalled completely, and you went back to it rather "
    "than letting it go. What stayed with us was the pattern underneath: when something "
    "matters you find what is blocking it and you work the problem. For this role we "
    "needed direct experience inside government systems, and that was the piece we were "
    "not able to establish through our conversations. This is a statement about what we "
    "needed to see, not about what you are able to do."
)


class _ScriptedDrafter:
    """Returns letters, then edits, without touching the network."""

    name = "scripted"

    def __init__(self, paragraphs=6):
        self.paragraphs = paragraphs
        self.draft_calls = 0
        self.review_calls = 0

    def draft(self, *, system, user, email_type, first_name, role,
              prior_violations=None, attempt=0):
        # The reviewer and the translator are told apart by their system prompt.
        if "ONLY THE SENTENCES YOU ARE CHANGING" in system:
            self.review_calls += 1
            return {"edits": []}
        if "translate a hiring manager" in system.lower():
            return {"rationale": "We could not establish government experience."}
        self.draft_calls += 1
        return {
            "title_line": "A Note From Us",
            "greeting": f"Dear {first_name},",
            "opening": ["This is not a yes for now.", GOOD_PARA],
            "sections": [{"subhead": None, "paragraphs": [GOOD_PARA] * self.paragraphs}],
            "ps": "That moment stayed with us.",
        }


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    drafting._NOTE_CACHE.clear()
    yield
    drafting._NOTE_CACHE.clear()


def test_generate_draft_runs_end_to_end(monkeypatch):
    """The regression: this raised NameError before the loop ever finished."""
    d = _ScriptedDrafter()
    monkeypatch.setattr(drafting, "get_drafter", lambda: d)
    out = drafting.generate_draft(
        scorecard=SCORECARD, first_name="Abdul", role="Growth Manager - Lahore",
        app_id=None, email_type="warm_bench",
    )
    assert out is not None
    assert out["body_html"], "no letter was rendered"
    assert out["eval"]["word_count"] > 0
    assert d.draft_calls >= 1


def test_a_clean_first_draft_does_not_retry(monkeypatch):
    d = _ScriptedDrafter()
    monkeypatch.setattr(drafting, "get_drafter", lambda: d)
    out = drafting.generate_draft(
        scorecard=SCORECARD, first_name="Abdul", role="Growth Manager - Lahore",
        app_id=None, email_type="warm_bench",
    )
    if not [v for v in out["eval"]["violations"] if v["severity"] == "HARD_BLOCK"]:
        assert out["attempts"] == 1, "a clean draft must not be redrafted"


def test_a_blocked_draft_is_REPAIRED_not_redrafted(monkeypatch):
    """Attempts 2+ must edit the letter we have. A fresh draft each time is how
    the loop used to diverge: three attempts, three different defects."""
    class _AlwaysBlocked(_ScriptedDrafter):
        def draft(self, *, system, user, email_type, first_name, role,
                  prior_violations=None, attempt=0):
            if "ONLY THE SENTENCES YOU ARE CHANGING" in system:
                self.review_calls += 1
                return {"edits": []}
            if "translate a hiring manager" in system.lower():
                return {"rationale": "clean rationale"}
            self.draft_calls += 1
            return {
                "title_line": "A Note From Us",
                "greeting": f"Dear {first_name},",
                # Too short: guarantees a word-count HARD_BLOCK every time.
                "opening": ["This is not a yes for now."],
                "sections": [{"subhead": None, "paragraphs": ["Short."]}],
                "ps": "",
            }

    d = _AlwaysBlocked()
    monkeypatch.setattr(drafting, "get_drafter", lambda: d)
    out = drafting.generate_draft(
        scorecard=SCORECARD, first_name="Abdul", role="Growth Manager - Lahore",
        app_id=None, email_type="warm_bench",
    )
    assert out["eval"]["violations"], "a short letter must fail the word count"
    # The letter is drafted ONCE; later attempts go through the repair path.
    assert d.draft_calls == 1, (
        f"attempts 2+ redrafted instead of repairing (draft_calls={d.draft_calls})"
    )
    assert out.get("retries_exhausted") is True


def test_a_dead_model_yields_a_scaffold_not_a_crash(monkeypatch):
    class _Dead:
        name = "dead"

        def draft(self, **kw):
            raise RuntimeError("Error code: 500 - upstream")

    monkeypatch.setattr(drafting, "get_drafter", lambda: _Dead())
    out = drafting.generate_draft(
        scorecard=SCORECARD, first_name="Abdul", role="Growth Manager - Lahore",
        app_id=None, email_type="warm_bench",
    )
    assert out is not None
    assert out["drafter_used"].startswith("unavailable")
