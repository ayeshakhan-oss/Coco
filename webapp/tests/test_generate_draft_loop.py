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


GOOD_PLAN = {
    "central_gap": "A record of moving a senior official from interest to commitment.",
    "why_the_requirement_matters": (
        "What carries the final step is rarely the analysis. It is the "
        "relationship that was in place before the ask was made."
    ),
    "secondary_concerns": [],
    "evidence": [
        {"id": "e1", "slot": "opening", "sensitive": False, "rank": 1,
         "what_happened": "Asked for more time on a nine district rollout plan."},
        {"id": "e2", "slot": "stayed_with_us", "sensitive": False, "rank": 2,
         "what_happened": "Carried a national incubation programme for four years."},
        {"id": "e3", "slot": "ps", "sensitive": False, "rank": 3,
         "what_happened": "Let the startup portal feasibility work go."},
        {"id": "e4", "slot": "unused", "sensitive": True, "rank": 4,
         "what_happened": "Sat with a dying parent in intensive care."},
    ],
    "excluded": [{"source": "values.dont_walk_away.deepDive", "reason": "bereavement"}],
}


class _ScriptedDrafter:
    """Returns letters, then edits, without touching the network."""

    name = "scripted"

    def __init__(self, paragraphs=6):
        self.paragraphs = paragraphs
        self.draft_calls = 0
        self.review_calls = 0
        self.plan_calls = 0
        self.stages: list = []
        self.write_user = None

    def draft(self, *, system, user, email_type, first_name, role,
              prior_violations=None, attempt=0):
        # Every stage is told apart by its system prompt. A stage this stub does
        # not recognise falls through to "return a letter", which is how the
        # planner silently got served a full letter JSON and counted as a draft
        # call the first time it was added. Keep the discriminators exhaustive.
        if "ONLY THE SENTENCES YOU ARE CHANGING" in system:
            self.stages.append("review")
            self.review_calls += 1
            return {"edits": []}
        if "ADD NEW PARAGRAPHS ONLY" in system:
            self.stages.append("expand")
            return {"additions": []}
        if "translate a hiring manager" in system.lower():
            self.stages.append("translate")
            return {"rationale": "We could not establish government experience."}
        if "You are NOT writing it" in system:
            self.stages.append("plan")
            self.plan_calls += 1
            return GOOD_PLAN
        self.stages.append("write")
        self.write_user = user
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
            if "ADD NEW PARAGRAPHS ONLY" in system:
                # An expander that adds nothing: the letter stays short.
                return {"additions": []}
            if "translate a hiring manager" in system.lower():
                return {"rationale": "clean rationale"}
            if "You are NOT writing it" in system:
                self.plan_calls += 1
                return GOOD_PLAN
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


ROLE_PARA = (
    "For this role, much of the work happens alongside teachers in their own "
    "classrooms, over many months, and the progress is slow and easy to miss. "
    "What we needed to see was a record of carrying that kind of work through "
    "to the point where it holds without us in the room. That matters to us "
    "because the people who depend on this role are teachers who have been "
    "promised support before, and the trust is built only by staying with them. "
    "This is the standard we hold the role to, and it is where our decision "
    "landed."
)


def test_a_short_draft_is_EXPANDED_past_the_floor(monkeypatch):
    """2026-10-05: every warm bench after the planning stage came out under 800
    (751, 778, 519), and the sentence-repair retries could never add the
    missing words. A short draft must now be lengthened, not handed back."""
    class _Short(_ScriptedDrafter):
        expand_calls = 0
        expand_user = None

        def draft(self, *, system, user, email_type, first_name, role,
                  prior_violations=None, attempt=0):
            if "ADD NEW PARAGRAPHS ONLY" in system:
                self.expand_calls += 1
                self.expand_user = user
                return {"additions": [{"section": 2, "paragraph": ROLE_PARA}] * 6}
            return super().draft(system=system, user=user, email_type=email_type,
                                 first_name=first_name, role=role,
                                 prior_violations=prior_violations, attempt=attempt)

    d = _Short(paragraphs=2)
    monkeypatch.setattr(drafting, "get_drafter", lambda: d)
    out = drafting.generate_draft(
        scorecard=SCORECARD, first_name="Abdul", role="Growth Manager - Lahore",
        app_id=None, email_type="warm_bench",
    )
    rules = [v["rule"] for v in out["eval"]["violations"] if v["severity"] == "HARD_BLOCK"]
    assert d.expand_calls >= 1, "a short draft was never expanded"
    assert not any(r.startswith("Word count minimum") for r in rules), (
        f"still short after expansion: {out['eval']['word_count']} words"
    )
    assert d.draft_calls == 1, "expansion must lengthen the letter, not redraft it"
    # The expander works from the plan's gap, never from the excluded evidence.
    assert "intensive care" not in d.expand_user
    assert GOOD_PLAN["central_gap"] in d.expand_user


def test_expand_pass_keeps_every_existing_sentence():
    content = {
        "greeting": "Dear Abdul,",
        "opening": ["This is not a yes for now.", "First."],
        "sections": [{"subhead": None, "paragraphs": ["A."]},
                     {"subhead": None, "paragraphs": ["B."]},
                     {"subhead": None, "paragraphs": ["Close."]}],
        "ps": "P.",
    }

    class _D:
        def draft(self, **kw):
            return {"additions": [{"section": 2, "paragraph": "New one."},
                                  {"section": 99, "paragraph": "Clamped."},
                                  {"section": 1, "paragraph": "  "},
                                  {"section": 1, "paragraph": "When you spoke, it was right."},
                                  {"section": 1, "paragraph": "Your answer was clear."}]}

    out, status = drafting._expand_pass(_D(), content, email_type="warm_bench",
                                        first_name="Abdul", role="R", plan=None,
                                        words_needed=300)
    assert status == "applied"
    assert out["sections"][0]["paragraphs"] == ["A."]
    # Section 99 is clamped to the last NON-closing section.
    assert out["sections"][1]["paragraphs"] == ["B.", "New one.", "Clamped."]
    assert out["sections"][2]["paragraphs"] == ["Close."], "the close was touched"
    assert content["sections"][1]["paragraphs"] == ["B."], "input was mutated"


def test_expand_pass_drops_any_paragraph_about_the_candidate():
    """The expander never saw the interview. On Haiku it wrote "you described
    it as a sustained relationship", which she never said."""
    content = {"greeting": "Dear A,", "opening": ["This is not a yes for now."],
               "sections": [{"subhead": None, "paragraphs": ["A."]},
                            {"subhead": None, "paragraphs": ["Close."]}], "ps": ""}

    class _D:
        def draft(self, **kw):
            return {"additions": [{"section": 1, "paragraph": "You described it well."},
                                  {"section": 1, "paragraph": "We know YOU'RE capable."}]}

    out, status = drafting._expand_pass(_D(), content, email_type="warm_bench",
                                        first_name="A", role="R", plan=None,
                                        words_needed=300)
    assert status == "skipped"
    assert out is content


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


# ---------------------------------------------------------------------------
# THE PLANNING STAGE
#
# The point of planning is not that the writer is told to leave things out. It
# is that the things it must leave out are NOT IN ITS INPUT. A rule can be
# euphemised around - a real letter got a bereavement past every sensitive-word
# pattern we own by calling it "a moment of profound loss" - and an absent fact
# cannot.
# ---------------------------------------------------------------------------

def test_the_writer_is_given_the_plan_and_not_the_excluded_material(monkeypatch):
    d = _ScriptedDrafter()
    monkeypatch.setattr(drafting, "get_drafter", lambda: d)
    drafting.generate_draft(
        scorecard=SCORECARD, first_name="Abdul", role="Growth Manager - Lahore",
        app_id=None, email_type="warm_bench",
    )

    assert d.plan_calls == 1, "the plan stage did not run"
    assert d.write_user, "the writer was never called"

    # Every selected moment reached the writer.
    for item in GOOD_PLAN["evidence"]:
        if item["slot"] != "unused":
            assert item["what_happened"] in d.write_user, (
                f"selected moment missing from the writer's prompt: {item['id']}"
            )

    # The sensitive one did not, in any form.
    assert "intensive care" not in d.write_user
    assert "dying parent" not in d.write_user

    # Nor did the raw scorecard evidence the plan was distilled from.
    assert "restructuring the quote" not in d.write_user, (
        "the plan must REPLACE the raw evidence, not sit alongside it"
    )

    # The single gap and its role-side justification did.
    assert GOOD_PLAN["central_gap"] in d.write_user
    assert "relationship that was in place" in d.write_user


def test_the_stages_run_in_order(monkeypatch):
    d = _ScriptedDrafter()
    monkeypatch.setattr(drafting, "get_drafter", lambda: d)
    drafting.generate_draft(
        scorecard=SCORECARD, first_name="Abdul", role="Growth Manager - Lahore",
        app_id=None, email_type="warm_bench",
    )
    ordered = [s for s in d.stages if s in ("plan", "write")]
    assert ordered[:2] == ["plan", "write"], (
        f"planning must precede writing, got {d.stages}"
    )


def test_a_rejected_plan_is_retried_once_then_the_letter_is_written_anyway(monkeypatch):
    """Never refuse, never write unplanned in silence. Say so on the draft.

    A letter written from the full evidence is what we shipped for months and
    beats no letter. But whoever reads this draft has to know that the step
    which keeps a bereavement out of a rejection did not run.
    """
    class _BadPlanner(_ScriptedDrafter):
        def draft(self, *, system, user, email_type, first_name, role,
                  prior_violations=None, attempt=0):
            if "You are NOT writing it" in system:
                self.plan_calls += 1
                return {"evidence": [], "central_gap": ""}   # unusable
            return super().draft(
                system=system, user=user, email_type=email_type,
                first_name=first_name, role=role,
                prior_violations=prior_violations, attempt=attempt)

    d = _BadPlanner()
    monkeypatch.setattr(drafting, "get_drafter", lambda: d)
    out = drafting.generate_draft(
        scorecard=SCORECARD, first_name="Abdul", role="Growth Manager - Lahore",
        app_id=None, email_type="warm_bench",
    )

    assert d.plan_calls == 2, "the planner should get exactly one retry"
    assert d.draft_calls >= 1, "the letter must still be written"
    rules = [v["rule"] for v in out["eval"]["violations"]]
    assert "Evidence was not planned" in rules, (
        "writing unplanned must be visible on the draft, not silent"
    )
    assert "plan" not in out


def test_planning_can_be_switched_off(monkeypatch):
    """The Railway escape hatch: back to one writer call without a redeploy."""
    from webapp import config

    d = _ScriptedDrafter()
    monkeypatch.setattr(drafting, "get_drafter", lambda: d)
    settings = config.get_settings()
    monkeypatch.setattr(settings, "draft_planning_enabled", False)
    drafting.generate_draft(
        scorecard=SCORECARD, first_name="Abdul", role="Growth Manager - Lahore",
        app_id=None, email_type="warm_bench",
    )
    assert d.plan_calls == 0
    assert d.draft_calls >= 1
    assert "restructuring the quote" in d.write_user, (
        "with planning off the writer should see the raw scorecard evidence again"
    )
