"""The CV-grounding gate: every concrete particular in a CV-stage rejection must
come from the candidate's own application.

Encodes Skill 01 (01_candidate-rejections.md):
  Step 2  "Only use observations from actual CV text."
  Rule 5  "every strength and gap must be tied to actual CV text ... Never make
           up observations."
  Rule 7  "Never assume data - if not in CV, state 'Not mentioned in your CV'."

The case that made this necessary is `test_the_lahore_market_claim_is_blocked`:
a letter sent live on 2026-07-08 praised a candidate's familiarity with a market
his CV never mentions.

Run: python -m pytest webapp/tests/test_cv_grounding.py
"""

from __future__ import annotations

from scripts.evals.candidate_communication_eval import (
    check_cv_grounding,
    check_cv_particulars,
)

CV = """
Umer Rafi. Marketing Communication Growth. Pakistan.
B2B growth, marketing and communications professional with 10+ years across
SaaS and tech-services companies, spanning content strategy, brand, PR, demand
generation, and go-to-market. Built the editorial calendar and ran paid media
for two product launches. Managed a team of 3.
"""


def _check(body, **kw):
    """The invented-particulars WARNING (check_cv_particulars). Separate from the
    hard block, which asks the opposite question: did the letter engage with the
    CV at all? See the tests at the bottom of this file."""
    kw.setdefault("candidate_name", "Muhammad Umer Rafi")
    kw.setdefault("role", "Growth Manager")
    return check_cv_particulars(body, "cv_rejection", CV, **kw)


def test_the_lahore_market_claim_is_blocked():
    """The real 2026-07-08 sentence. His CV contains no 'Lahore'."""
    body = ("<p>What came through clearly was your familiarity with the Lahore "
            "market specifically.</p>")
    passed, detail = _check(body)
    assert passed is False
    assert "lahore" in detail.lower()


def test_a_letter_built_from_the_cv_passes():
    body = ("<p>Your application shows ten years across SaaS and tech-services, "
            "with real depth in content strategy and demand generation. You "
            "managed a team of 3 and ran paid media for two product launches.</p>")
    passed, detail = _check(body)
    assert passed is True, detail


def test_a_city_in_the_role_title_is_not_a_claim_about_the_candidate():
    """'Growth Manager - Lahore' means the ROLE is in Lahore. Naming the role's
    own city is not a claim about the person, so it must not block."""
    body = "<p>Thank you for applying for the Growth Manager role in Lahore.</p>"
    passed, detail = _check(body, role="Growth Manager - Lahore")
    assert passed is True, detail


def test_ungrounded_figures_are_blocked():
    body = "<p>Your application describes 12 years of growth leadership.</p>"
    passed, detail = _check(body)
    assert passed is False
    assert "12" in detail


def test_figures_present_in_the_cv_pass():
    body = "<p>Your application describes 10 years across SaaS.</p>"
    passed, detail = _check(body)
    assert passed is True, detail


def test_quotes_must_be_verbatim():
    body = ('<p>You wrote that you were a "world-class growth operator" in your '
            "application.</p>")
    passed, detail = _check(body)
    assert passed is False
    assert "verbatim" in detail


def test_sentence_openers_are_not_treated_as_claims():
    """Capitalised sentence-initial words carry no information about anyone."""
    body = ("<p>Did your application show this? Yes, in places.</p>\n"
            "<p>Here is what we would suggest next.</p>")
    passed, detail = _check(body)
    assert passed is True, detail


def test_possessives_and_contractions_are_normalised():
    body = "<p>Taleemabad's work in Pakistan's public schools. We'd welcome it.</p>"
    passed, detail = _check(body)
    assert passed is True, detail


def test_gate_stands_down_with_no_corpus():
    """A hand-written letter evaluated from the CLI has no corpus; neither check
    may block on an absence (generation refuses separately)."""
    assert check_cv_grounding("<p>Anything at all.</p>", "cv_rejection", None)[0] is True
    assert check_cv_particulars("<p>Anything about Lahore.</p>", "cv_rejection", None)[0] is True


def test_gate_only_applies_to_cv_rejections():
    body = "<p>During our conversation you spoke about the Lahore market.</p>"
    assert check_cv_grounding(body, "values_feedback", CV)[0] is True
    assert check_cv_particulars(body, "values_feedback", CV)[0] is True


# --- the POSITIVE requirement: did the letter engage with the CV at all? ------
#
# This is the half that matters for the incident. The 27 letters sent live
# contained no fabricated proper nouns to catch - they were generic prose about
# people whose CVs were never opened.

GENERIC = """
<p>Your application showed real clarity about what this kind of work involves.
You have taken on complex challenges and stayed engaged in environments that
demanded both strategic thinking and hands-on execution. That is real, and it
matters to us.</p>
<p>What we look for at this stage is evidence that someone has built and held
a pipeline on their own, and the written application did not make that visible
to us. These are not dealbreakers, they are specifics that would have helped us
move forward with confidence.</p>
"""


# The production default is min_anchors=25, calibrated on 800+ word letters
# against full CVs. These fixtures are a few lines each, so they pass an explicit
# scaled-down threshold; the calibration itself is verified by
# scripts/evals/calibrate_cv_grounding.py against the two real corpora.
SCALED = 4


def test_a_generic_letter_is_blocked_even_with_nothing_fabricated():
    """The incident shape: nothing invented, nothing grounded either."""
    passed, detail = check_cv_grounding(
        GENERIC, "cv_rejection", CV, min_anchors=SCALED,
        candidate_name="Muhammad Umer Rafi", role="Growth Manager")
    assert passed is False
    assert "generic" in detail


def test_a_letter_that_engages_with_the_cv_passes():
    body = """
    <p>Your application describes ten years across SaaS and tech-services, with
    depth in content strategy, brand and demand generation.</p>
    <p>You ran paid media for two product launches and built the editorial
    calendar, and you managed a team of 3. Where the application left us
    uncertain was public relations against the growth targets this role carries.</p>
    """
    passed, detail = check_cv_grounding(
        body, "cv_rejection", CV, min_anchors=SCALED,
        candidate_name="Muhammad Umer Rafi", role="Growth Manager")
    assert passed is True, detail


def test_the_positive_check_does_not_apply_to_other_types():
    passed, _ = check_cv_grounding(GENERIC, "warm_bench", CV, min_anchors=SCALED)
    assert passed is True
