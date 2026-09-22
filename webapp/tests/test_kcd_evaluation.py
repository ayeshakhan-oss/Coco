"""The locked KCD evaluation rules.

Two tests here exist because the SOP and CLAUDE.md disagree, and the code had
to choose:

  * `test_the_scale_has_a_real_zero` -- the SOP anchors at 1 and reserves 0 for
    "not submitted". Rule 27 forbids exactly that floor.
  * `test_an_incomplete_submission_is_never_ranked_above_a_complete_one` -- the
    structural answer to what the SOP was actually worried about when it wrote
    that floor.

Run: python -m pytest webapp/tests/test_kcd_evaluation.py -v
"""

from __future__ import annotations

import pytest

from webapp.services import kcd_evaluation as k
from webapp.services.kcd_evaluation import KCDEvaluationError

ALL = {d["key"] for d in k.DIMENSIONS}


def _scores(**over) -> dict:
    base = {key: 3.0 for key in ALL}
    base.update(over)
    return base


# --------------------------------------------------------------------------
# The scale
# --------------------------------------------------------------------------


def test_the_scale_has_a_real_zero():
    """The SOP says "1 = Absent or fundamentally wrong" and reserves 0 for a
    missing submission. That is a 20% floor under every dimension, which is
    the defect CLAUDE.md Rule 27 records as putting all 25 RM case studies
    above a published bar. On this scale an empty answer scores 0."""
    assert 0.0 in k.SCORES
    assert k.weighted_total(_scores(**{key: 0.0 for key in ALL})) == 0.0


def test_a_perfect_evaluation_is_one_hundred():
    assert k.weighted_total(_scores(**{key: 5.0 for key in ALL})) == 100.0


def test_half_steps_are_required_by_the_sop_and_accepted():
    """"Use fractional scores (4.5, 3.5) for candidates between whole
    numbers." Whole numbers only compress differences the SOP calls
    meaningful."""
    assert 4.5 in k.SCORES and 3.5 in k.SCORES
    total = k.weighted_total(_scores(knowledge=4.5))
    assert total != k.weighted_total(_scores(knowledge=4.0))
    assert total != k.weighted_total(_scores(knowledge=5.0))


def test_a_quarter_step_is_refused():
    with pytest.raises(KCDEvaluationError, match="whole or half step"):
        k.validate_scores(_scores(knowledge=4.25))


def test_the_weights_sum_to_one_hundred():
    assert sum(d["weight"] for d in k.DIMENSIONS) == 100


def test_validate_rejects_a_bad_shape_or_range():
    with pytest.raises(KCDEvaluationError):
        k.validate_scores({"knowledge": 3.0})
    with pytest.raises(KCDEvaluationError):
        k.validate_scores(_scores(extra=3.0))
    with pytest.raises(KCDEvaluationError):
        k.validate_scores(_scores(knowledge=5.5))
    with pytest.raises(KCDEvaluationError):
        k.validate_scores(_scores(knowledge=True))


def test_a_role_specific_framework_may_supply_its_own_weights():
    weights = {"knowledge": 50, "capacity": 30, "design": 20}
    assert k.weighted_total(_scores(**{key: 5.0 for key in ALL}), weights) == 100.0
    assert k.weighted_total(_scores(knowledge=5.0, capacity=0.0, design=0.0), weights) == 50.0


def test_weights_that_do_not_sum_to_one_hundred_are_refused():
    with pytest.raises(KCDEvaluationError, match="sum to 100"):
        k.weighted_total(_scores(), {"knowledge": 50, "capacity": 30, "design": 5})
    with pytest.raises(KCDEvaluationError, match="cover exactly"):
        k.weighted_total(_scores(), {"knowledge": 100})


# --------------------------------------------------------------------------
# Verdicts and the GWC gate
# --------------------------------------------------------------------------


def test_verdict_bands_match_the_sop_exactly():
    assert k.verdict(85.0) == k.STRONG_HIRE
    assert k.verdict(84.99) == k.HIRE
    assert k.verdict(70.0) == k.HIRE
    assert k.verdict(69.99) == k.CONDITIONAL
    assert k.verdict(55.0) == k.CONDITIONAL
    assert k.verdict(54.99) == k.BORDERLINE
    assert k.verdict(40.0) == k.BORDERLINE
    assert k.verdict(39.99) == k.NOT_RECOMMENDED
    assert k.verdict(0.0) == k.NOT_RECOMMENDED


def test_the_gwc_threshold_is_sixty_and_lives_in_one_place():
    assert k.GWC_ADVANCEMENT_THRESHOLD == 60.0
    assert k.advances_to_gwc(60.0) is True
    assert k.advances_to_gwc(59.99) is False


def test_the_gwc_gate_is_not_the_same_line_as_a_hire_verdict():
    """A CONDITIONAL candidate at 62 advances to GWC. Collapsing the two would
    quietly raise the advancement bar from 60 to 70."""
    assert k.verdict(62.0) == k.CONDITIONAL
    assert k.advances_to_gwc(62.0) is True


def test_a_conditional_verdict_must_state_its_condition():
    """The SOP's own Common Mistakes table: a CONDITIONAL with no condition is
    not actionable."""
    with pytest.raises(KCDEvaluationError, match="must state its condition"):
        k.validate_conditional(k.CONDITIONAL, None)
    with pytest.raises(KCDEvaluationError, match="must state its condition"):
        k.validate_conditional(k.CONDITIONAL, "   ")
    k.validate_conditional(k.CONDITIONAL, "Evidence they have run a field team before.")


def test_other_verdicts_do_not_need_a_condition():
    for v in (k.STRONG_HIRE, k.HIRE, k.BORDERLINE, k.NOT_RECOMMENDED):
        k.validate_conditional(v, None)


# --------------------------------------------------------------------------
# Caps
# --------------------------------------------------------------------------


def test_a_cap_lowers_a_score_above_it():
    out = k.apply_caps(_scores(knowledge=5.0), insight_without_evidence=["knowledge"])
    assert out["knowledge"] == k.CAP_INSIGHT_WITHOUT_EVIDENCE


def test_a_cap_is_a_ceiling_and_never_raises_a_score():
    """Hafsa Bashir was rejected live at 62.0 and recalibrated to 72.0 on her
    own appeal, partly because a question was marked BELOW its own cap. A cap
    can only lower."""
    out = k.apply_caps(_scores(knowledge=1.5), insight_without_evidence=["knowledge"])
    assert out["knowledge"] == 1.5


def test_both_caps_can_apply_to_different_dimensions():
    out = k.apply_caps(
        _scores(knowledge=5.0, capacity=4.5, design=5.0),
        insight_without_evidence=["knowledge"],
        evidence_without_interpretation=["capacity"],
    )
    assert out["knowledge"] == 3.0 and out["capacity"] == 3.0 and out["design"] == 5.0


def test_capping_an_unknown_dimension_is_refused():
    with pytest.raises(KCDEvaluationError, match="unknown dimension"):
        k.apply_caps(_scores(), insight_without_evidence=["nonsense"])


def test_applying_no_caps_changes_nothing():
    scores = _scores(knowledge=4.5)
    assert k.apply_caps(scores) == scores


# --------------------------------------------------------------------------
# Incomplete submissions
# --------------------------------------------------------------------------


def _result(name, total, incomplete=False):
    return {"candidate": name, "total": total, "incomplete": incomplete}


def test_an_incomplete_submission_is_never_ranked_above_a_complete_one():
    """The SOP: excluded from the main ranking entirely, never ranked above a
    full submission. A single list sorted by total would break that the first
    time a strong partial outscored a weak complete one -- so the two never
    share a list."""
    out = k.rank_results([
        _result("strong partial", 82.0, incomplete=True),
        _result("weak complete", 41.0),
    ])
    assert [r["candidate"] for r in out["ranked"]] == ["weak complete"]
    assert [r["candidate"] for r in out["incomplete"]] == ["strong partial"]


def test_the_ranking_is_ordered_and_the_incomplete_section_is_too():
    out = k.rank_results([
        _result("b", 70.0), _result("a", 88.0), _result("c", 55.0),
        _result("p", 40.0, True), _result("q", 60.0, True),
    ])
    assert [r["candidate"] for r in out["ranked"]] == ["a", "b", "c"]
    assert [r["candidate"] for r in out["incomplete"]] == ["q", "p"]


def test_a_cohort_with_no_incomplete_submissions_carries_no_note():
    out = k.rank_results([_result("a", 88.0)])
    assert out["incomplete"] == [] and out["note"] is None


def test_the_note_says_the_scores_are_floors():
    out = k.rank_results([_result("p", 52.0, True)])
    assert "floors" in out["note"]


def test_an_incomplete_score_is_rendered_with_its_asterisk_and_caveat():
    rendered = k.format_incomplete_score(52.0)
    assert rendered.startswith("52.0%*")
    assert "floor" in rendered and "not a capability read" in rendered


def test_ranking_refuses_a_result_that_does_not_say_whether_it_is_complete():
    with pytest.raises(KCDEvaluationError, match="'total' and 'incomplete'"):
        k.rank_results([{"candidate": "a", "total": 70.0}])


# --------------------------------------------------------------------------
# Cross-check with Noah
# --------------------------------------------------------------------------


def test_scores_within_five_points_are_aligned():
    assert k.cross_check(72.0, 68.0)["status"] == "aligned"
    assert k.cross_check(72.0, 67.0)["status"] == "aligned"


def test_scores_more_than_ten_apart_are_flagged_before_anything_goes_out():
    out = k.cross_check(82.0, 70.0)
    assert out["status"] == "divergent"
    assert out["delta"] == 12.0
    assert "before anything goes out" in out["note"]


def test_the_gap_the_sop_leaves_unnamed_is_reported_not_rounded_away():
    """Between 5 and 10 the SOP says nothing. Rounding it into 'aligned' would
    invent a permission it never gave."""
    out = k.cross_check(80.0, 72.0)
    assert out["status"] == "review"
    assert out["delta"] == 8.0


def test_no_second_evaluation_says_so_rather_than_claiming_agreement():
    out = k.cross_check(72.0, None)
    assert out["status"] == "not_available" and out["delta"] is None


# --------------------------------------------------------------------------
# What the module deliberately does not do
# --------------------------------------------------------------------------


def test_kcd_is_an_internal_name_and_the_module_says_so():
    """memory/feedback_terminology.md, Ayesha 2026-04-02: always call it "case
    study" to candidates and to hiring managers. KCD is internal only."""
    import inspect

    assert "case study" in inspect.getsource(k).lower()
