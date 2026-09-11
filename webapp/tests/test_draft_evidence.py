"""Evidence-sourcing guards for AI drafting.

The regression these encode (2026-09-11, application 3867): a CV-stage rejection
was generated from an EMPTY values scorecard. The drafter was handed six value
names and nothing else, and produced 1,000 words of specific claims about a CV
it had never seen, plus a recital of our internal values at the candidate.

Two rules follow, and both are tested here:
  1. Evidence is sourced per type and never mixed. A cv_rejection is grounded in
     the candidate's own application material; the values scorecard is not
     passed to it at all.
  2. Empty evidence raises MissingEvidence. It never degrades to a prompt that
     lets the model write from nothing.

Run: python -m pytest webapp/tests/test_draft_evidence.py
"""

from __future__ import annotations

import pytest

from webapp.prompts.draft_prompt import (
    MissingEvidence,
    _gwc_is_empty,
    _values_is_empty,
    build_user_prompt,
)
from webapp.services import cv_text

# The real shape of application 3867's scorecard: saved, never filled in.
EMPTY_VALUES = {
    "kind": "values",
    "final_comments": "",
    "proceed_to_right_seat": "Yes",
    "values": [
        {"name": "Don't Walk Away from Hard Things", "rating": "", "deep_dive": "",
         "curve_ball": "", "micro_case": ""},
        {"name": "Have Courageous Conversations", "rating": "", "deep_dive": "",
         "curve_ball": "", "micro_case": ""},
    ],
}

FILLED_VALUES = {
    "kind": "values",
    "final_comments": "Strong on ownership, thin on conflict.",
    "proceed_to_right_seat": "No",
    "values": [
        {"name": "Have Courageous Conversations", "rating": "Needs work",
         "deep_dive": "Described avoiding a peer conflict for two quarters.",
         "curve_ball": "", "micro_case": ""},
    ],
}

CV_TEXT = (
    "ASMA KHAN\nGrowth Manager, Lahore\n\nEXPERIENCE\n"
    "Led paid acquisition for a 40-person edtech, growing enrolments from 300 to "
    "2,400 a term over eighteen months. Built the reporting stack from scratch in "
    "SQL and Looker. Managed a team of four across content and performance. "
    "Ran the school-partnerships pilot in Punjab, signing eleven schools in the "
    "first quarter and writing the onboarding playbook the team still uses.\n"
    "EDUCATION\nBSc Economics, LUMS.\n"
) * 2

GOOD_CV_EVIDENCE = {
    "cv_text": CV_TEXT,
    "cv_error": None,
    "cv_file_name": "asma-khan-cv.pdf",
    "cover_letter": "I have followed Taleemabad's work in public schools for two years.",
    "custom_answers": {"Expected salary": "PKR 450,000", "City": "Lahore"},
    "canned_answers": None,
    "linkedin_url": "https://linkedin.com/in/example",
    "portfolio_url": None,
}


def _prompt(**kw):
    base = dict(scorecard=None, first_name="Asma", role="Growth Manager",
                email_type="cv_rejection", cv_evidence=GOOD_CV_EVIDENCE)
    base.update(kw)
    return build_user_prompt(**base)


# --- 1. cv_rejection is grounded in the candidate's own material --------------

def test_cv_rejection_prompt_carries_the_cv_text():
    out = _prompt()
    assert "asma-khan-cv.pdf" in out
    assert "school-partnerships pilot in Punjab" in out
    assert "PKR 450,000" in out
    assert "I have followed Taleemabad's work" in out


def test_cv_rejection_never_receives_values_evidence():
    """Even if a values scorecard is handed in, it must not reach the prompt."""
    out = _prompt(scorecard=FILLED_VALUES)
    assert "Courageous Conversations" not in out
    assert "avoiding a peer conflict" not in out
    assert "Strong on ownership" not in out


def test_cv_rejection_prompt_forbids_naming_internal_values():
    out = _prompt()
    assert "Do not name or allude to our internal values" in out


# --- 2. empty evidence refuses ------------------------------------------------

def test_empty_values_scorecard_is_detected():
    assert _values_is_empty(EMPTY_VALUES) is True
    assert _values_is_empty(FILLED_VALUES) is False


def test_values_feedback_refuses_on_empty_scorecard():
    with pytest.raises(MissingEvidence, match="values scorecard .* is empty"):
        build_user_prompt(scorecard=EMPTY_VALUES, first_name="Jawwad",
                          role="Senior Manager Growth", email_type="values_feedback")


def test_values_feedback_drafts_on_a_filled_scorecard():
    out = build_user_prompt(scorecard=FILLED_VALUES, first_name="Jawwad",
                            role="Senior Manager Growth", email_type="values_feedback")
    assert "avoiding a peer conflict" in out


def test_cv_rejection_refuses_with_no_cv():
    ev = dict(GOOD_CV_EVIDENCE, cv_text=None, cv_error="no resume on file")
    with pytest.raises(MissingEvidence, match="no resume on file"):
        _prompt(cv_evidence=ev)


def test_cv_rejection_refuses_on_a_too_short_cv():
    ev = dict(GOOD_CV_EVIDENCE, cv_text="Asma Khan. Growth.", cv_error=None)
    with pytest.raises(MissingEvidence, match="characters of CV text"):
        _prompt(cv_evidence=ev)


def test_cv_rejection_refuses_when_no_evidence_was_loaded_at_all():
    with pytest.raises(MissingEvidence):
        _prompt(cv_evidence=None)


def test_interview_type_refuses_when_no_scorecard_exists():
    with pytest.raises(MissingEvidence, match="no scorecard exists"):
        build_user_prompt(scorecard=None, first_name="Asma", role="Growth Manager",
                          email_type="gwc_rejection")


def test_empty_gwc_scorecard_is_detected():
    assert _gwc_is_empty({"kind": "gwc", "competencies": [{"name": "Gets it", "score": None}]})
    assert not _gwc_is_empty({"kind": "gwc", "final_mark": "No"})


# --- 3. CV extraction ---------------------------------------------------------

def test_extract_refuses_empty_resume():
    with pytest.raises(cv_text.CVUnreadable, match="no resume on file"):
        cv_text.extract(None)


def test_extract_refuses_unparseable_bytes():
    import base64
    junk = base64.b64encode(b"not a document" * 50).decode()
    with pytest.raises(cv_text.CVUnreadable):
        cv_text.extract(junk, mime_type="application/pdf", file_name="x.pdf")
