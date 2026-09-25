"""The rules that turn dimension scores into a tier.

Run: python -m pytest webapp/tests/test_tech_tiering.py -v

These are the judgement calls. Everything else in technical screening is
plumbing; this is where a candidate is placed, and where a subtle mistake is
invisible until someone audits a whole cohort.
"""

from __future__ import annotations

import pytest

from webapp.services import rubric_drafting, tech_tiering as t

# Job 13's live shape, reduced to what tiering reads.
RUBRIC = {
    "max_score": 100,
    "dimensions": [
        {"key": "must_have_skills", "weight": 8, "core": True},
        {"key": "responsibility_alignment", "weight": 5, "core": True},
        {"key": "stack_match", "weight": 4, "core": True},
        {"key": "technical_breadth", "weight": 2, "core": False},
        {"key": "experience_depth", "weight": 1, "core": False},
    ],
    "thresholds": {
        "p1": 85, "p2": 70, "p3": 50, "basis": "absolute",
        "gates": {
            "p1": {"min_dimension": {"must_have_skills": 4, "stack_match": 3}},
            "p2": {"min_dimension": {"must_have_skills": 2}},
        },
    },
    "hard_filters": [
        {"key": "onsite_location", "label": "On-site: Islamabad",
         "action": "reject", "on_unknown": "flag"},
        {"key": "university_tier", "label": "University",
         "action": "flag", "on_unknown": "flag"},
    ],
    "manual_review_rules": {"min_resume_chars": 500, "min_resume_health": 60},
}

WEIGHT_TOTAL = sum(d["weight"] for d in RUBRIC["dimensions"]) * 5  # 100


def _score(**raw):
    dims, total, max_score = t.score_dimensions(RUBRIC, raw)
    pct = t.score_percent(total, max_score, weight_total=WEIGHT_TOTAL)
    return dims, pct


# --------------------------------------------------------------------------
# The bottom of the scale
# --------------------------------------------------------------------------


def test_a_candidate_who_evidences_nothing_scores_zero():
    """🔴 THE ANCHOR FLOOR. Coco's RM round put all 25 case studies above a
    published 70% bar because its anchors started at 1, which floors every
    dimension at a fifth of its weight. A rubric whose zero is real must be
    able to return an actual zero."""
    _, pct = _score(must_have_skills=0, responsibility_alignment=0,
                    stack_match=0, technical_breadth=0, experience_depth=0)
    assert pct == 0.0


def test_a_perfect_candidate_scores_one_hundred():
    _, pct = _score(must_have_skills=5, responsibility_alignment=5,
                    stack_match=5, technical_breadth=5, experience_depth=5)
    assert pct == 100.0


def test_weights_actually_weight():
    """5 on the heaviest dimension must beat 5 on the lightest."""
    _, heavy = _score(must_have_skills=5, responsibility_alignment=0,
                      stack_match=0, technical_breadth=0, experience_depth=0)
    _, light = _score(must_have_skills=0, responsibility_alignment=0,
                      stack_match=0, technical_breadth=0, experience_depth=5)
    assert heavy > light
    assert heavy == 40.0 and light == 5.0


def test_a_missing_dimension_raises_rather_than_scoring_zero():
    """An unanswered dimension is a malformed response. Defaulting it to 0
    would be indistinguishable from a candidate who genuinely lacks the
    skill, and would quietly push people down a tier."""
    with pytest.raises(t.TieringError, match="stack_match"):
        t.score_dimensions(RUBRIC, {"must_have_skills": 5,
                                    "responsibility_alignment": 5,
                                    "technical_breadth": 5,
                                    "experience_depth": 5})


@pytest.mark.parametrize("bad", [6, -1, "five", None])
def test_a_score_outside_zero_to_five_raises(bad):
    with pytest.raises(t.TieringError):
        t.score_dimensions(RUBRIC, {
            "must_have_skills": bad, "responsibility_alignment": 3,
            "stack_match": 3, "technical_breadth": 3, "experience_depth": 3})


# --------------------------------------------------------------------------
# Thresholds and gates
# --------------------------------------------------------------------------


def test_a_strong_aggregate_cannot_mask_a_critical_weakness():
    """🔴 THE WHOLE POINT OF A GATE. This candidate scores 88%, above the P1
    bar of 85, but has stack_match 2 against a gate requiring 3. They must NOT
    be P1, and the reason must say which dimension blocked it."""
    dims, pct = _score(must_have_skills=5, responsibility_alignment=5,
                       stack_match=2, technical_breadth=5, experience_depth=5)
    assert pct >= 85
    tier, reason = t.assign_tier(rubric=RUBRIC, dimension_scores=dims, pct=pct)
    assert tier != "P1"
    assert "stack match" in reason.lower()


def test_meeting_the_bar_and_the_gate_gives_the_tier():
    dims, pct = _score(must_have_skills=5, responsibility_alignment=5,
                       stack_match=4, technical_breadth=4, experience_depth=4)
    tier, reason = t.assign_tier(rubric=RUBRIC, dimension_scores=dims, pct=pct)
    assert tier == "P1"
    assert "85" in reason


def test_below_every_bar_is_p4():
    dims, pct = _score(must_have_skills=1, responsibility_alignment=1,
                       stack_match=1, technical_breadth=1, experience_depth=1)
    tier, _ = t.assign_tier(rubric=RUBRIC, dimension_scores=dims, pct=pct)
    assert tier == "P4"


def test_the_tier_reason_is_written_for_a_person():
    dims, pct = _score(must_have_skills=3, responsibility_alignment=3,
                       stack_match=3, technical_breadth=3, experience_depth=3)
    _, reason = t.assign_tier(rubric=RUBRIC, dimension_scores=dims, pct=pct)
    assert reason.endswith(".")
    assert "%" in reason


# --------------------------------------------------------------------------
# Hard filters: the protective wording, as behaviour
# --------------------------------------------------------------------------


def test_silence_in_a_cv_never_rejects():
    """🔴 "Report a hard filter as unknown when the CV is silent. Silence is
    not a refusal, and it must never read as one." A CV that says nothing
    about relocating must not be rejected for it."""
    flags, reject = t.evaluate_hard_filters(RUBRIC, {"onsite_location": "unknown"})
    assert reject is None
    assert [f["result"] for f in flags if f["key"] == "onsite_location"] == ["unknown"]


def test_a_missing_filter_verdict_is_treated_as_unknown_not_as_failure():
    flags, reject = t.evaluate_hard_filters(RUBRIC, {})
    assert reject is None
    assert all(f["result"] == "unknown" for f in flags)


def test_an_explicit_refusal_does_reject():
    _, reject = t.evaluate_hard_filters(RUBRIC, {"onsite_location": "fail"})
    assert reject == "On-site: Islamabad"


def test_a_flag_filter_never_changes_the_tier():
    """University tier: never fail on this. The SOP calls it a tie-breaker
    between comparable candidates and nothing more, so even an explicit fail
    on a `flag` filter must leave the tier alone."""
    _, reject = t.evaluate_hard_filters(RUBRIC, {"university_tier": "fail"})
    assert reject is None


def test_a_rejecting_filter_places_p4_and_explains_itself():
    dims, pct = _score(must_have_skills=5, responsibility_alignment=5,
                       stack_match=5, technical_breadth=5, experience_depth=5)
    tier, reason = t.assign_tier(rubric=RUBRIC, dimension_scores=dims, pct=pct,
                                 hard_filter_reject="On-site: Islamabad")
    assert tier == "P4"
    assert "On-site: Islamabad" in reason


# --------------------------------------------------------------------------
# Resume health: an unreadable CV is never a weak candidate
# --------------------------------------------------------------------------


def test_an_empty_extraction_is_unusable():
    health, issues = t.resume_health("")
    assert health == 0 and issues
    assert t.route_unscorable(health=health, chars=0,
                              rules=RUBRIC["manual_review_rules"])[0] == "UNUSABLE"


def test_the_letter_spacing_defect_is_caught():
    """🔴 pypdf can produce a 20,089-character CV containing 15 real words.
    Every character-count check passes it. Counting words does not."""
    spaced = " ".join(["a" * 40] * 60)  # 2,400 chars, 60 absurd "words"
    health, issues = t.resume_health(spaced)
    assert health < 60
    assert any("word length" in i for i in issues)


def test_a_short_but_real_cv_goes_to_manual_review_not_to_a_low_score():
    """🔴 MANUAL_REVIEW and UNUSABLE are never rejections and never zeros.
    They mean a person has to open the document."""
    short = " ".join(["experience"] * 40)
    health, _ = t.resume_health(short)
    routed = t.route_unscorable(health=health, chars=len(short),
                                rules=RUBRIC["manual_review_rules"])
    assert routed is not None
    assert routed[0] in t.UNSCORED_TIERS
    assert "person" in routed[1]


def test_a_healthy_cv_is_scored_normally():
    good = " ".join(["delivered"] * 400)
    health, _ = t.resume_health(good)
    assert health >= 60
    assert t.route_unscorable(health=health, chars=len(good),
                              rules=RUBRIC["manual_review_rules"]) is None


def test_health_is_not_flattered_by_length_alone():
    """A live Nugget evaluation carries resume_health 85.5 on 21 extracted
    characters. Length is not health."""
    health, _ = t.resume_health("Ali Khan, Engineer.")
    assert health == 0


# --------------------------------------------------------------------------
# The draft validator
# --------------------------------------------------------------------------


def _draft(**over):
    dim = {
        "key": "must_have_skills", "label": "Must-have skills", "weight": 8,
        "core": True,
        "anchors": {str(i): f"anchor {i}" for i in range(6)},
        "look_for": ["x"], "common_gaps": ["y"],
    }
    base = {
        "title": "Full Stack Developer", "seniority": "mid", "min_years": 3,
        "dimensions": [dict(dim), dict(dim, key="stack_match", core=True, weight=4),
                       dict(dim, key="breadth", core=False, weight=2)],
        "hard_filters": [],
        "thresholds": {"p1": 85, "p2": 70, "p3": 50},
    }
    base.update(over)
    return base


def test_a_draft_missing_its_zero_anchor_is_rejected():
    """🔴 The single most important check in the validator. A rubric whose
    anchors start at 1 floors every candidate at a fifth of every weight, and
    it looks completely normal in a rendered rubric."""
    d = _draft()
    d["dimensions"][0]["anchors"].pop("0")
    with pytest.raises(rubric_drafting.RubricDraftError, match="anchors"):
        rubric_drafting.validate_draft(d)


def test_a_valid_draft_passes():
    out = rubric_drafting.validate_draft(_draft())
    assert len(out["dimensions"]) == 3
    assert out["max_score"] == 100
    assert all(str(i) in out["dimensions"][0]["anchors"] for i in range(6))


def test_a_university_filter_can_never_reject():
    d = _draft(hard_filters=[{"key": "university_tier", "label": "University",
                              "rule": "tie-breaker only", "action": "reject"}])
    out = rubric_drafting.validate_draft(d)
    assert out["hard_filters"][0]["action"] == "flag"


def test_thresholds_must_descend():
    with pytest.raises(rubric_drafting.RubricDraftError, match="descend"):
        rubric_drafting.validate_draft(_draft(thresholds={"p1": 50, "p2": 70, "p3": 85}))


def test_a_gate_naming_a_non_core_dimension_is_dropped():
    """A gate that names a dimension which is not core never fires. Shipping it
    would look like a safeguard and be none."""
    d = _draft(thresholds={"p1": 85, "p2": 70, "p3": 50,
                           "gates": {"p1": {"min_dimension": {"breadth": 4}}}})
    out = rubric_drafting.validate_draft(d)
    assert out["thresholds"]["gates"]["p1"]["min_dimension"] == {}


def test_the_composed_scoring_prompt_carries_every_anchor():
    """The stored system_prompt IS the scoring contract: the engine reads it
    back per candidate and never reconstructs it. A dropped anchor would be
    silent."""
    draft = rubric_drafting.validate_draft(_draft(hard_filters=[
        {"key": "onsite_location", "label": "On-site: Islamabad",
         "rule": "Report fail only where the candidate says they will not "
                 "work there.", "action": "reject", "on_unknown": "flag"},
    ]))
    prompt = rubric_drafting.compose_system_prompt(
        draft=draft, job_title="Full Stack Developer", department="Engineering",
        location="Islamabad", job_description="Build things.",
    )
    for dim in draft["dimensions"]:
        assert f"[key: {dim['key']}]" in prompt
        for score in range(6):
            assert dim["anchors"][str(score)] in prompt
    assert "An absent skill scores 0" in prompt
    assert "Silence is not a refusal" in prompt
    assert "scoring a document, not ranking a person" in prompt
    assert "—" not in prompt, "no em dashes in a prompt whose output may reach a letter"
