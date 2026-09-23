"""The locked CV-screening rules, and the guard that keeps them separate from
Nugget's technical screening.

Ayesha, 2026-09-15: "cv screening and technical screening are both separate so
you shouldn't mix their sops/rubrics/rules." That is not a style preference --
the two answer different questions against different rubrics, and a CV screen
carrying Nugget's tiers or gates would be presenting one system's judgement
under the other's name. test_cv_screening_borrows_nothing_from_nugget makes it
mechanical.

Run: python -m pytest webapp/tests/test_cv_screening.py -v
"""

from __future__ import annotations

import pytest

from webapp.services import cv_screening as cs
from webapp.services.cv_screening import CVScreeningError

ALL = {c["key"] for c in cs.CRITERIA}

# Long enough to clear MIN_SCREENABLE_WORDS. Tests that are about the retry
# path or the result shape must not also be accidentally testing the
# extraction floor.
A_READABLE_CV = "experience delivering teacher training across districts " * 60
A_JOB_DESCRIPTION = "we need a coach who can run school visits and observations " * 20


def _scores(**over) -> dict:
    base = {k: 3 for k in ALL}
    base.update(over)
    return base


def _evidence(**over) -> dict:
    base = {k: f"line from the CV about {k}" for k in ALL}
    base.update(over)
    return base


def _good_response(**over) -> dict:
    out = {
        "scores": _scores(),
        "evidence": _evidence(),
        "total_experience_years": 8,
        "relevant_experience_years": 3,
        "relevant_experience_note": "three years running school partnerships",
        "strengths": ["ran a partnership pipeline", "wrote the reporting herself"],
        "gaps": ["no government-side experience"],
    }
    out.update(over)
    return out


# --------------------------------------------------------------------------
# The scale, with a real zero (CLAUDE.md Rule 27)
# --------------------------------------------------------------------------


def test_an_all_zero_screen_scores_zero_not_a_floor():
    """The anchor-floor defect in one assertion. On a 1-5 scale with 1 as the
    bottom anchor this would be 20.0, and 20 free points across a cohort is
    what put all 25 RM case studies above the published bar."""
    assert cs.match_percent(_scores(**{k: 0 for k in ALL})) == 0.0


def test_a_perfect_screen_is_one_hundred():
    assert cs.match_percent(_scores(**{k: 5 for k in ALL})) == 100.0


def test_the_weights_sum_to_one_hundred():
    assert sum(c["weight"] for c in cs.CRITERIA) == 100


def test_skills_and_experience_outrank_fit():
    """The SOP ranks skills and experience as TOP priority and fit as
    supporting. Whatever the numbers become, that ordering must hold."""
    by_key = {c["key"]: c for c in cs.CRITERIA}
    assert by_key["skills"]["weight"] == by_key["experience"]["weight"]
    assert by_key["fit"]["weight"] < by_key["skills"]["weight"]
    assert by_key["fit"]["priority"] == "supporting"


def test_validate_scores_rejects_a_bad_shape_or_range():
    with pytest.raises(CVScreeningError):
        cs.validate_scores({"skills": 3})                      # missing keys
    with pytest.raises(CVScreeningError):
        cs.validate_scores(_scores(unexpected_key=3))          # extra key
    with pytest.raises(CVScreeningError):
        cs.validate_scores(_scores(skills=6))                  # out of range
    with pytest.raises(CVScreeningError):
        cs.validate_scores(_scores(skills=2.5))                # not an integer
    with pytest.raises(CVScreeningError):
        cs.validate_scores(_scores(skills=True))               # bool is an int subclass


def test_tier_boundaries_are_inclusive_at_the_bottom():
    assert cs.tier(cs.TIER_SHORTLIST_MIN) == "shortlist"
    assert cs.tier(cs.TIER_SHORTLIST_MIN - 0.01) == "maybe"
    assert cs.tier(cs.TIER_MAYBE_MIN) == "maybe"
    assert cs.tier(cs.TIER_MAYBE_MIN - 0.01) == "no_hire"
    assert cs.tier(0.0) == "no_hire"


# --------------------------------------------------------------------------
# Reading discipline
# --------------------------------------------------------------------------


def test_a_short_cv_is_passed_whole_and_not_marked_truncated():
    text, truncated = cs.cv_for_prompt("x" * 5_000)
    assert len(text) == 5_000 and truncated is False


def test_a_long_cv_is_cut_at_the_limit_never_below_the_floor():
    text, truncated = cs.cv_for_prompt("x" * 90_000)
    assert truncated is True
    assert len(text) == cs.READ_LIMIT
    assert len(text) >= cs.TRUNCATION_FLOOR, (
        "the SOP forbids truncating a CV below 10,000 characters"
    )


def test_the_read_limit_respects_the_sops_own_floor():
    assert cs.READ_LIMIT >= cs.TRUNCATION_FLOOR >= 10_000


# --------------------------------------------------------------------------
# Total vs relevant experience -- the SOP says this three times
# --------------------------------------------------------------------------


def test_relevant_experience_cannot_exceed_total():
    with pytest.raises(CVScreeningError, match="SUBSET"):
        cs._validate_experience(
            {"total_experience_years": 3, "relevant_experience_years": 8,
             "relevant_experience_note": "n"}
        )


def test_both_experience_figures_are_required_separately():
    for missing in ("total_experience_years", "relevant_experience_years"):
        payload = {"total_experience_years": 8, "relevant_experience_years": 3,
                   "relevant_experience_note": "n"}
        del payload[missing]
        with pytest.raises(CVScreeningError, match="separately"):
            cs._validate_experience(payload)


def test_a_negative_experience_figure_is_refused():
    with pytest.raises(CVScreeningError, match="negative"):
        cs._validate_experience(
            {"total_experience_years": -1, "relevant_experience_years": 0,
             "relevant_experience_note": "n"}
        )


def test_the_relevance_note_cannot_be_blank():
    with pytest.raises(CVScreeningError, match="relevant_experience_note"):
        cs._validate_experience(
            {"total_experience_years": 8, "relevant_experience_years": 3,
             "relevant_experience_note": "   "}
        )


def test_equal_total_and_relevant_is_allowed():
    out = cs._validate_experience(
        {"total_experience_years": 4, "relevant_experience_years": 4,
         "relevant_experience_note": "all four years in the same work"}
    )
    assert out["relevant_experience_years"] == 4.0


# --------------------------------------------------------------------------
# Evidence and lists
# --------------------------------------------------------------------------


def test_a_blank_evidence_citation_is_refused():
    with pytest.raises(CVScreeningError, match="blank"):
        cs._validate_evidence(_evidence(skills="   "))


def test_strengths_and_gaps_are_bounded():
    with pytest.raises(CVScreeningError, match="strengths"):
        cs._validate_list({"strengths": ["only one"]}, "strengths", 2, 3)
    with pytest.raises(CVScreeningError, match="strengths"):
        cs._validate_list({"strengths": ["a", "b", "c", "d"]}, "strengths", 2, 3)
    with pytest.raises(CVScreeningError, match="gaps"):
        cs._validate_list({"gaps": []}, "gaps", 1, 2)
    with pytest.raises(CVScreeningError, match="blank"):
        cs._validate_list({"gaps": ["  "]}, "gaps", 1, 2)


# --------------------------------------------------------------------------
# screen_cv: refusals, retry, and who computes the verdict
# --------------------------------------------------------------------------


def test_screen_refuses_without_a_cv():
    """CLAUDE.md Rule 29: 27 CV rejections went out live written from nothing
    but a first name and a role title."""
    with pytest.raises(CVScreeningError, match="no CV text"):
        cs.screen_cv(cv_text="", job_description="JD", candidate_name="A", role="R")
    with pytest.raises(CVScreeningError, match="no CV text"):
        cs.screen_cv(cv_text="   ", job_description="JD", candidate_name="A", role="R")


def test_screen_refuses_a_cv_that_did_not_extract():
    """🔴 Measured against the 16 people actually hired or offered CPD Coach:
    the three thinnest extracted CVs (117, 238 and 296 words) were all returned
    as confident REJECTIONS. Hina Fatima Jafri was hired; her CV extracts to 788
    characters and came back 36% no_hire, and a re-run on the same input gave
    her 6.5 relevant years one time and 0.2 the next, because there was nothing
    to read either time.

    A CV that did not parse is an extraction failure, never a weak candidate --
    the same distinction Nugget's UNUSABLE tier exists for."""
    with pytest.raises(CVScreeningError, match="extraction failure"):
        cs.screen_cv(cv_text="word " * 117, job_description=A_JOB_DESCRIPTION,
                     candidate_name="A", role="R")


def test_the_floor_is_counted_in_words_not_characters():
    """The pypdf letter-spacing defect produced 20,089 characters carrying 15
    words on 12% of one cohort. A character floor waves that straight through."""
    with pytest.raises(CVScreeningError, match="only 1 words"):
        cs.screen_cv(cv_text="x" * 20_089, job_description=A_JOB_DESCRIPTION,
                     candidate_name="A", role="R")


def test_the_screening_floor_sits_far_above_the_is_there_text_floor():
    """cv_text.MIN_USABLE_CHARS asks "is this text at all". It is not, and was
    never meant to be, the bar for screening somebody out."""
    from webapp.services import cv_text as ct

    assert cs.MIN_SCREENABLE_WORDS >= 250
    assert cs.MIN_SCREENABLE_WORDS * 4 > ct.MIN_USABLE_CHARS


def test_a_real_length_cv_is_not_refused(monkeypatch):
    """The median hired candidate's CV extracted to 590 words; the floor must
    not reject an ordinary one."""
    monkeypatch.setattr(cs, "_call_model", lambda **kw: (_good_response(), "m", "sha", False))
    out = cs.screen_cv(cv_text="word " * 590, job_description=A_JOB_DESCRIPTION,
                       candidate_name="A", role="R")
    assert out["tier"] == "maybe"


def test_screen_refuses_without_a_job_description():
    with pytest.raises(CVScreeningError, match="no job description"):
        cs.screen_cv(cv_text=A_READABLE_CV, job_description="", candidate_name="A", role="R")


def test_screen_computes_match_and_tier_in_code_and_ignores_the_models_own(monkeypatch):
    """A model volunteering a 98% match and a shortlist tier must change
    nothing: the numbers come from the scores, through code."""
    response = _good_response(
        scores=_scores(**{k: 1 for k in ALL}),
        match=98.0, tier="shortlist", total=98, recommendation="hire",
    )
    monkeypatch.setattr(cs, "_call_model", lambda **kw: (response, "m", "sha", False))

    out = cs.screen_cv(cv_text=A_READABLE_CV, job_description=A_JOB_DESCRIPTION, candidate_name="A", role="R")
    assert out["match"] == 20.0          # a fifth of every weight, honestly earned
    assert out["tier"] == "no_hire"
    assert "recommendation" not in out
    assert "total" not in out


def test_screen_retries_once_with_a_fresh_call_then_raises(monkeypatch):
    calls = []

    def bad(**kw):
        calls.append(kw)
        return ({"scores": {"skills": 3}}, "m", "sha", False)

    monkeypatch.setattr(cs, "_call_model", bad)
    with pytest.raises(CVScreeningError):
        cs.screen_cv(cv_text=A_READABLE_CV, job_description=A_JOB_DESCRIPTION, candidate_name="A", role="R")
    assert len(calls) == 2, "a malformed response is retried exactly once"


def test_screen_recovers_if_the_second_call_is_well_formed(monkeypatch):
    responses = [({"scores": {"skills": 3}}, "m", "sha", False),
                 (_good_response(), "m", "sha", False)]
    monkeypatch.setattr(cs, "_call_model", lambda **kw: responses.pop(0))
    out = cs.screen_cv(cv_text=A_READABLE_CV, job_description=A_JOB_DESCRIPTION, candidate_name="A", role="R")
    assert out["tier"] == "maybe" and out["match"] == 60.0


def test_unparseable_json_is_wrapped_not_leaked(monkeypatch):
    def boom(**kw):
        raise ValueError("LLM did not return parseable JSON")

    monkeypatch.setattr(cs, "_call_model", boom)
    with pytest.raises(CVScreeningError, match="not parseable JSON"):
        cs.screen_cv(cv_text=A_READABLE_CV, job_description=A_JOB_DESCRIPTION, candidate_name="A", role="R")


def test_the_result_records_what_it_was_built_from(monkeypatch):
    monkeypatch.setattr(
        cs, "_call_model", lambda **kw: (_good_response(), "claude-x", "abc123", True)
    )
    out = cs.screen_cv(
        cv_text=A_READABLE_CV, job_description=A_JOB_DESCRIPTION, candidate_name="A", role="R"
    )
    assert out["cv_chars"] == len(A_READABLE_CV)
    assert out["cv_truncated"] is True
    assert out["model"] == "claude-x"
    assert out["sop_sha256"] == "abc123"


# --------------------------------------------------------------------------
# The separation Ayesha asked for, made mechanical
# --------------------------------------------------------------------------

NUGGET_VOCABULARY = (
    "must_have_skills", "stack_match", "resume_health", "score_pct",
    "tier_reason", "min_resume_health", "min_years", "UNUSABLE", "MANUAL_REVIEW",
)


def test_cv_screening_borrows_nothing_from_nugget():
    """Coco's CV screening and Nugget's technical screening are separate skills
    with separate rubrics. The service must not import Nugget's reader or carry
    its vocabulary, or a CV screen would quietly present one system's judgement
    under the other's name.

    The module docstring names the banned vocabulary in order to ban it, so the
    scan runs over the code below it, not over the header.
    """
    import inspect

    src = inspect.getsource(cs)
    body = src.split('"""', 2)[-1]
    found = [w for w in NUGGET_VOCABULARY if w.lower() in body.lower()]
    assert not found, f"Nugget's rubric vocabulary leaked into CV screening: {found}"
    assert "nugget_reads" not in body, "CV screening must not import Nugget's reader"


def test_cv_screening_uses_cocos_own_three_criteria():
    assert {c["key"] for c in cs.CRITERIA} == {"skills", "experience", "fit"}
    assert set(cs.SCORES) == {0, 1, 2, 3, 4, 5}
