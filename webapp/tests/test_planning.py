"""The plan gates, proved against deliberately broken plans.

A gate that has only ever passed proves nothing, so every check here is shown
failing on the shape it exists to catch, and the good plan is shown passing all
of them at once.

The good plan below is the one the offline Opus letter implicitly used for
Salman Tariq (Growth Manager Lahore): four moments, the bereavement and the
colleague's death and the therapy disclosure all set aside, one gap.

Run: python -m pytest webapp/tests/test_planning.py
"""

from __future__ import annotations

import copy

import pytest

from webapp.services import planning


GOOD = {
    "central_gap": (
        "A record of carrying a relationship with a senior government official "
        "to the point where they committed."
    ),
    "why_the_requirement_matters": (
        "What carries the final step is rarely the strength of the analysis. It "
        "is the relationship that was already in place before the ask was made."
    ),
    "secondary_concerns": [],
    "evidence": [
        {"id": "e1", "slot": "opening", "sensitive": False, "rank": 1,
         "what_happened": "Asked for more time when the director wanted a nine "
                          "district rollout plan by the next morning."},
        {"id": "e2", "slot": "stayed_with_us", "sensitive": False, "rank": 2,
         "what_happened": "Carried a national incubation programme for four years "
                          "through shifting sites, to completion."},
        {"id": "e3", "slot": "stayed_with_us", "sensitive": False, "rank": 3,
         "what_happened": "Argued for the team's promotions ahead of his own, and "
                          "his did not come through that year."},
        {"id": "e4", "slot": "ps", "sensitive": False, "rank": 4,
         "what_happened": "Let the Punjab Startup Portal feasibility work go when "
                          "leadership judged it was not the priority."},
        {"id": "e5", "slot": "unused", "sensitive": False, "rank": 5,
         "what_happened": "Completed a six week bootcamp with a delegation to Turkey."},
        {"id": "e6", "slot": "unused", "sensitive": True, "rank": 6,
         "what_happened": "Sat with his father in intensive care for 25 days."},
    ],
    "excluded": [
        {"source": "values.dont_walk_away.deepDive", "reason": "bereavement"},
        {"source": "values.all_for_one.deepDive", "reason": "third_party_death"},
        {"source": "values.courageous.deepDive", "reason": "medical"},
    ],
}


def _broken(**changes):
    plan = copy.deepcopy(GOOD)
    plan.update(changes)
    return plan


def test_the_good_plan_passes_every_gate():
    assert planning.check_plan(GOOD, "warm_bench") == []


def test_four_is_the_cap_and_a_fifth_is_caught():
    plan = copy.deepcopy(GOOD)
    plan["evidence"][4]["slot"] = "stayed_with_us"   # promote the unused one
    problems = planning.check_plan(plan, "warm_bench")
    assert any("limit is 4" in p for p in problems), problems


def test_case_study_outcome_may_carry_more():
    """Its SOP needs three or more verbatim anchors; four would be a squeeze."""
    plan = copy.deepcopy(GOOD)
    plan["evidence"][4]["slot"] = "stayed_with_us"
    assert planning.check_plan(plan, "case_study_outcome") == []


def test_sensitive_material_cannot_be_given_a_slot():
    """The failure this whole stage exists for: the bereavement reaching the letter."""
    plan = copy.deepcopy(GOOD)
    plan["evidence"][5]["slot"] = "opening"
    problems = planning.check_plan(plan, "warm_bench")
    assert any("sensitive" in p for p in problems), problems


def test_sensitivity_is_checked_on_the_item_not_the_wording():
    """Euphemising the text does not help, because the flag is what is read.

    'A moment of profound loss' defeated every sensitive-word pattern we own and
    still opened a real letter. Here the same euphemised text is still blocked,
    because the judgement was made on the evidence rather than on the prose.
    """
    plan = copy.deepcopy(GOOD)
    plan["evidence"][5]["slot"] = "opening"
    plan["evidence"][5]["what_happened"] = "Spoke about a moment of profound loss."
    assert any("sensitive" in p for p in planning.check_plan(plan, "warm_bench"))


def test_a_second_reason_is_caught():
    problems = planning.check_plan(
        _broken(secondary_concerns=["has never closed a paid pilot"]), "warm_bench")
    assert any("secondary concern" in p for p in problems), problems


def test_a_missing_central_gap_is_caught():
    assert any("central gap" in p
               for p in planning.check_plan(_broken(central_gap="  "), "warm_bench"))


def test_the_requirement_may_not_be_explained_through_the_candidate():
    problems = planning.check_plan(_broken(
        why_the_requirement_matters=(
            "Someone arriving without your experience spends a year learning "
            "what the room already knows."
        )), "warm_bench")
    assert any("in terms of the candidate" in p for p in problems), problems


def test_one_opening_and_one_ps_are_required():
    plan = copy.deepcopy(GOOD)
    plan["evidence"][3]["slot"] = "stayed_with_us"       # lose the P.S.
    assert any("'ps' slot" in p for p in planning.check_plan(plan, "warm_bench"))

    plan = copy.deepcopy(GOOD)
    plan["evidence"][1]["slot"] = "opening"              # two openings
    assert any("'opening' slot" in p for p in planning.check_plan(plan, "warm_bench"))


def test_the_same_moment_cannot_fill_two_slots():
    """The body-and-then-the-P.S. duplication no sentence-level check catches."""
    plan = copy.deepcopy(GOOD)
    plan["evidence"][3]["id"] = "e2"
    assert any("more than one slot" in p
               for p in planning.check_plan(plan, "warm_bench"))


def test_an_unknown_slot_is_caught():
    plan = copy.deepcopy(GOOD)
    plan["evidence"][1]["slot"] = "conclusion"
    assert any("unknown slot" in p for p in planning.check_plan(plan, "warm_bench"))


@pytest.mark.parametrize("plan", [None, "not a dict", {}, {"evidence": []}])
def test_a_malformed_plan_is_rejected_not_trusted(plan):
    assert planning.check_plan(plan, "warm_bench")


def test_every_problem_is_reported_not_just_the_first():
    """Reporting one at a time makes a retry fix that one and break another."""
    plan = _broken(secondary_concerns=["a second reason"], central_gap="")
    plan["evidence"][5]["slot"] = "opening"
    assert len(planning.check_plan(plan, "warm_bench")) >= 3


def test_excluded_safety_sources_are_surfaced_for_the_letter_check():
    assert set(planning.excluded_sources(GOOD)) == {
        "values.dont_walk_away.deepDive",
        "values.all_for_one.deepDive",
        "values.courageous.deepDive",
    }


def test_a_non_safety_exclusion_is_not_surfaced():
    """'Not decision relevant' is a judgement call, not a thing we must police."""
    plan = _broken(excluded=[
        {"source": "values.craft.deepDive", "reason": "not_decision_relevant"}])
    assert planning.excluded_sources(plan) == []


def test_a_selected_moment_may_not_narrate_a_death():
    """The first LIVE planner run produced exactly this, on Haiku, for app 3656.

    It correctly excluded the candidate's father's death, then selected as a
    strength, with sensitive=false: "When an office boy at the incubation centre
    was killed, you fought the system ... to secure the death benefit for his
    widow". Keeping the act is not permission to narrate the event.
    """
    plan = copy.deepcopy(GOOD)
    plan["evidence"][2]["what_happened"] = (
        "When an office boy at the incubation centre was killed, he fought the "
        "system to secure the death benefit for his widow."
    )
    problems = planning.check_plan(plan, "warm_bench")
    assert any("narrates" in p for p in problems), problems


def test_the_same_act_with_the_tragedy_stripped_passes():
    """Rule 31's sanctioned form. The act survives; the death does not."""
    plan = copy.deepcopy(GOOD)
    plan["evidence"][2]["what_happened"] = (
        "Went against his own organisation so a colleague's family received "
        "what they were owed, when it would have been easier if nobody had asked."
    )
    assert planning.check_plan(plan, "warm_bench") == []


@pytest.mark.parametrize("text", [
    "Sat with his father in intensive care for 25 days.",
    "Spoke about starting therapy that year.",
    "Described the funeral he organised for a colleague.",
    "Described his diagnosis and the months after it.",
])
def test_bereavement_and_medical_vocabulary_is_caught_in_any_selected_moment(text):
    plan = copy.deepcopy(GOOD)
    plan["evidence"][1]["what_happened"] = text
    assert any("narrates" in p for p in planning.check_plan(plan, "warm_bench"))


@pytest.mark.parametrize("text", [
    "Built a counselling service for students at three schools.",
    "Ran the mental health programme for a district education office.",
    "Led career counselling for final year students.",
])
def test_someones_PROFESSION_is_not_mistaken_for_a_disclosure(text):
    """The calibration this reuses exists for exactly these.

    We hire people who run counselling and mental-health programmes. A bare
    keyword match fired on 8 of the 103 sent letters, every one about somebody's
    job. Blocking these would make the planner unable to select the very work a
    candidate was hired to talk about.
    """
    plan = copy.deepcopy(GOOD)
    plan["evidence"][1]["what_happened"] = text
    assert planning.check_plan(plan, "warm_bench") == []


def test_the_health_check_is_deliberately_conservative():
    """Documents the boundary rather than pretending it is not there.

    The health split needs a disclosure verb, so "Talked about his diagnosis"
    passes where "Described his diagnosis" is caught. Widening it means
    re-measuring against the 103 sent letters, which is the discipline every
    other pattern in that harness carries. Recorded here so the next person
    meets the limit in a test instead of in a letter.
    """
    plan = copy.deepcopy(GOOD)
    plan["evidence"][1]["what_happened"] = "Talked about his diagnosis afterwards."
    assert planning.check_plan(plan, "warm_bench") == []


def test_an_excluded_item_may_still_describe_what_it_is():
    """Only SELECTED moments are scanned. The planner has to be able to say what
    it set aside, or 'excluded' becomes unreadable to a human checking it."""
    plan = copy.deepcopy(GOOD)
    plan["evidence"][5]["what_happened"] = "Sat with his dying father in intensive care."
    plan["evidence"][5]["slot"] = "unused"
    assert planning.check_plan(plan, "warm_bench") == []
