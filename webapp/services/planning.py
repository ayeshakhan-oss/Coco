"""Checking the plan, before the writer ever sees it.

These are the checks the letter-level harness structurally cannot do. It reads
finished prose with regexes, so "used ten stories instead of four", "opened on
the bereavement" and "named a second reason" produce no violation at all: the
loop sees a clean draft and stops. Measured on a real letter that did all three,
the harness returned PASS with zero hard blocks.

On a plan they are arithmetic. Count the slots. Check a flag. Check a list is
empty. No model, no cost, no false positives.

Nothing here is a word list. The point of moving selection into its own stage is
that we stop trying to catch bad judgment by its vocabulary.
"""

from __future__ import annotations

import re
from typing import Optional

# Four is what the offline Opus letter used, and it is the number that separates
# a letter from a transcript. case_study_outcome is higher because its SOP
# requires three or more verbatim anchors from the candidate's own submission,
# which is a different kind of evidence with a different job.
EVIDENCE_CAP = {
    "cv_rejection": 4,
    "values_feedback": 4,
    "warm_bench": 4,
    "gwc_rejection": 4,
    "case_study_outcome": 6,
}
DEFAULT_EVIDENCE_CAP = 4

NARRATIVE_SLOTS = ("opening", "stayed_with_us", "ps")
VALID_SLOTS = NARRATIVE_SLOTS + ("unused",)

# Reasons the planner may give for setting evidence aside. The four safety
# reasons are the ones that must never reach a letter in any wording.
SAFETY_REASONS = ("bereavement", "third_party_death", "medical", "family_crisis")


class PlanRejected(ValueError):
    """The plan broke a rule that re-planning might fix."""


def cap_for(email_type: str) -> int:
    return EVIDENCE_CAP.get(email_type, DEFAULT_EVIDENCE_CAP)


def selected(plan: dict) -> list:
    """The items that will actually reach the writer."""
    return [
        item for item in plan.get("evidence", []) or []
        if isinstance(item, dict) and item.get("slot") in NARRATIVE_SLOTS
    ]


def check_plan(plan: Optional[dict], email_type: str) -> list:
    """Every structural problem with the plan, as a list of reasons.

    An empty list means the plan may go to the writer. Returns ALL problems
    rather than the first, for the same reason the scorecard leak check does:
    reporting one at a time makes a retry loop fix that one and break another.
    """
    if not isinstance(plan, dict):
        return ["the planner did not return an object"]

    problems: list = []
    items = plan.get("evidence")
    if not isinstance(items, list) or not items:
        return ["the plan carries no evidence at all"]

    chosen = selected(plan)
    cap = cap_for(email_type)
    if len(chosen) > cap:
        problems.append(
            f"{len(chosen)} moments selected, and the limit is {cap}. "
            f"A letter that works through everything reads as a transcript."
        )
    if not chosen:
        problems.append("no moments were selected, so there is nothing to write from")

    # Safety. The whole reason selection moved to its own stage.
    for item in items:
        if not isinstance(item, dict):
            problems.append("an evidence item is not an object")
            continue
        if item.get("slot") not in VALID_SLOTS:
            problems.append(
                f"unknown slot {item.get('slot')!r}; expected one of {list(VALID_SLOTS)}"
            )
        if item.get("sensitive") and item.get("slot") in NARRATIVE_SLOTS:
            problems.append(
                f"item {item.get('id')!r} is marked sensitive and must not be used. "
                f"Sensitive material is set aside, not reworded."
            )
        if item.get("slot") in NARRATIVE_SLOTS:
            found = _tragedy_terms(item.get("what_happened") or "")
            if found:
                problems.append(
                    f"item {item.get('id')!r} still narrates {', '.join(found)}. "
                    f"Keep the ACT and strip the event: describe what the "
                    f"candidate did, with no death, illness or crisis in the "
                    f"text. If it cannot be said that way, exclude it."
                )

    # Exactly one opening and at most one P.S., or the letter has no shape.
    for slot, required in (("opening", 1), ("ps", 1)):
        n = sum(1 for i in chosen if i.get("slot") == slot)
        if n != required:
            problems.append(f"{n} items in the {slot!r} slot; expected {required}")

    # Each moment told once. This is what stops the same story appearing in the
    # body and again in the P.S., which no sentence-level repeat check catches.
    ids = [i.get("id") for i in chosen]
    if len(ids) != len(set(ids)):
        problems.append("the same evidence id is used in more than one slot")

    # One gap.
    secondary = plan.get("secondary_concerns")
    if secondary:
        problems.append(
            f"{len(secondary)} secondary concern(s) named. The decision turned on "
            f"one gap, and a second reason reads as a case being built."
        )
    if not (plan.get("central_gap") or "").strip():
        problems.append("no central gap was named")

    # The requirement is explained by describing the work, never the candidate.
    why = (plan.get("why_the_requirement_matters") or "").strip()
    if not why:
        problems.append("no explanation of why the role needs it")
    elif _addresses_the_candidate(why):
        problems.append(
            "the requirement is explained in terms of the candidate ('you', 'your'). "
            "Describe how the work succeeds instead."
        )

    return problems


def _tragedy_terms(text: str) -> list:
    """Bereavement / illness vocabulary inside a selected moment.

    The first live run of the planner proved why this cannot be left to the
    instruction. On the candidate whose letter started all of this, it correctly
    excluded his father's death and then selected, as a strength and marked
    sensitive=false, "when an office boy at the incubation centre was killed,
    you fought the system ... to secure the death benefit for his widow".

    The prompt says the ACT can survive the story. The planner kept the act and
    narrated the death with it, which is the exact thing the rule forbids.

    A word list is the wrong instrument on 1,100 words of prose, and the right
    one here: "what_happened" is a short factual description of something a
    person did, written to a stated instruction, and none of these words belong
    in one. Failing at the plan stage also costs one cheap retry instead of a
    rewrite of a finished letter.

    Both definitions are the harness's own, so there is one place this material
    is described.

    The health terms go through the harness's own check rather than a bare
    match, because they are ALSO ordinary professional vocabulary: we hire
    people who run counselling services, and a bare match fired on 8 of the 103
    sent letters, every one of them about somebody's profession. "Built a
    counselling service for students" is a legitimate thing to select.
    """
    from scripts.evals.candidate_communication_eval import (
        _SENSITIVE_TERMS, check_never_in_a_letter)

    hits = []
    for pattern in _SENSITIVE_TERMS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            hits.append(match.group().lower())

    # Disclosure of someone's own care, as opposed to describing their work.
    passed, _ = check_never_in_a_letter(text, "", "warm_bench")
    if not passed:
        hits.append("a medical or personal disclosure")

    return sorted(set(hits))


def _addresses_the_candidate(text: str) -> bool:
    """Second-person pronouns in the requirement explanation.

    Narrow and literal on purpose: this is a field the planner writes to a
    stated instruction, not free prose, so a pronoun here means the instruction
    was missed rather than that some phrasing slipped through.
    """
    return bool(re.search(r"\b(you|your|yours|you're|you've)\b", text, re.IGNORECASE))


def excluded_sources(plan: dict) -> list:
    """What the planner set aside for safety, for the letter-level check."""
    out = []
    for item in plan.get("excluded", []) or []:
        if isinstance(item, dict) and item.get("reason") in SAFETY_REASONS:
            text = (item.get("source") or "").strip()
            if text:
                out.append(text)
    return out
