"""The joining email rules, especially the one that would do real harm.

Run: python -m pytest webapp/tests/test_joining_email.py -v

The rules here are Ayesha's, given verbatim, and several were written after a
package took six review rounds. The one that matters most: a VOLUNTEER Fellow
receives the NDA and nothing else. Attaching a contract to an unpaid person
creates an obligation nobody agreed to.
"""

from __future__ import annotations

import pytest

from webapp.services import contracts as spec
from webapp.services import joining_email as je


# --------------------------------------------------------------------------
# Which situations have approved wording
# --------------------------------------------------------------------------


def test_the_five_locked_situations_are_available():
    assert set(je.SITUATIONS) == {
        spec.PAID_FELLOW, spec.VOLUNTEER_FELLOW, spec.FELLOW_TO_PAID,
        spec.PROJECT_HIRE, spec.PERMANENT_HIRE,
    }


@pytest.mark.parametrize("engagement", sorted(je.NO_TEMPLATE))
def test_a_situation_with_no_approved_wording_is_refused(engagement):
    """Inventing the wording is not an option: the templates are locked."""
    with pytest.raises(je.JoiningEmailError, match="no approved joining email"):
        je.situation_for(engagement)


def test_every_situation_names_a_template_that_exists():
    import os

    for key, s in je.SITUATIONS.items():
        path = os.path.join(je.TEMPLATE_DIR, s["template"])
        assert os.path.isfile(path), f"{key} points at a missing template"


def test_a_permanent_hire_is_not_sent_to_a_form_that_does_not_apply():
    """No onboarding form exists for a permanent hire. Only the Fellow and
    NIETE forms exist, and sending someone to the wrong programme's form is
    worse than sending them to none."""
    assert je.SITUATIONS[spec.PERMANENT_HIRE]["onboarding_form"] is None


def test_the_transition_email_carries_no_subject_of_its_own():
    """It is a reply inside the existing thread."""
    assert je.subject_for(spec.FELLOW_TO_PAID, first_name="Ali", role="Coach") is None


def test_the_other_subjects_are_filled_from_the_locked_wording():
    assert je.subject_for(spec.PROJECT_HIRE, first_name="Zia", role="CPD Coach") == (
        "Congratulations Zia on Your Selection as a Coach for the NIETE Project!"
    )
    assert je.subject_for(spec.PAID_FELLOW, first_name="Ali", role="Research") == (
        "Welcome to Taleemabad - Research Fellow"
    )


# --------------------------------------------------------------------------
# 🔴 The package rule
# --------------------------------------------------------------------------


def test_a_volunteer_fellow_with_a_contract_attached_is_refused():
    """The one that would do real harm."""
    problems = je.attachments_ok(
        ["Contract - Ali.pdf", "Fellow NDA - Ali.pdf"], spec.VOLUNTEER_FELLOW)
    assert any("unpaid person" in p for p in problems)


def test_a_volunteer_fellow_with_only_the_nda_is_fine():
    assert je.attachments_ok(["Fellow NDA - Ali.pdf"], spec.VOLUNTEER_FELLOW) == []


def test_a_volunteer_fellow_with_no_nda_is_refused():
    problems = je.attachments_ok(["something.pdf"], spec.VOLUNTEER_FELLOW)
    assert any("must have the NDA" in p for p in problems)


def test_a_transition_email_must_not_carry_a_second_nda():
    """The NDA was signed at the unpaid stage; a second one implies the first
    did not count."""
    problems = je.attachments_ok(
        ["Contract - Ali.pdf", "NDA - Ali.pdf"], spec.FELLOW_TO_PAID)
    assert any("signed at the unpaid stage" in p for p in problems)


def test_a_paid_package_needs_both_documents():
    assert je.attachments_ok(["Contract - Ali.pdf"], spec.PAID_FELLOW)
    assert je.attachments_ok(
        ["Contract - Ali.pdf", "NDA - Ali.pdf"], spec.PAID_FELLOW) == []


@pytest.mark.parametrize("name", ["Contract - Ali.docx", "NDA.doc"])
def test_a_word_attachment_is_refused(name):
    """Candidates receive PDF, never Word."""
    problems = je.attachments_ok([name, "NDA - Ali.pdf"], spec.PAID_FELLOW)
    assert any("never Word" in p for p in problems)


def test_no_attachments_at_all_is_refused():
    assert je.attachments_ok([], spec.PAID_FELLOW)


# --------------------------------------------------------------------------
# The body rules
# --------------------------------------------------------------------------


GOOD = (
    '<p>Hi Zia,</p><p>selected as <b>CPD Coach</b> starting '
    '<b>1st of September 2026</b> at <b>PKR 108,000</b> for <b>4 months</b>. '
    '<a href="https://example.com/form">Click here</a></p>'
)


def test_a_clean_body_passes():
    assert je.check_body(GOOD, compensation="PKR 108,000",
                         start_date="1st of September 2026") == []


def test_a_weekday_in_a_date_is_refused():
    body = GOOD.replace("1st of September 2026", "Monday, 1st of September 2026")
    problems = je.check_body(body, compensation="PKR 108,000",
                             start_date="Monday, 1st of September 2026")
    assert any("weekday" in p for p in problems)


@pytest.mark.parametrize(
    "note",
    [
        "<p>This is a pilot, nothing has gone to the candidate.</p>",
        "<p>Draft for approval before sending.</p>",
        "<p>Open question: is the salary right?</p>",
    ],
)
def test_a_note_to_ayesha_inside_the_body_is_refused(note):
    """The pilot must be identical to what the candidate receives."""
    problems = je.check_body(GOOD + note, compensation="PKR 108,000",
                             start_date="1st of September 2026")
    assert any("identical to what the candidate receives" in p for p in problems)


def test_an_unbolded_compensation_figure_is_refused():
    body = GOOD.replace("<b>PKR 108,000</b>", "PKR 108,000")
    problems = je.check_body(body, compensation="PKR 108,000",
                             start_date="1st of September 2026")
    assert any("not bold" in p and "108,000" in p for p in problems)


def test_an_unbolded_joining_date_is_refused():
    body = GOOD.replace("<b>1st of September 2026</b>", "1st of September 2026")
    problems = je.check_body(body, compensation="PKR 108,000",
                             start_date="1st of September 2026")
    assert any("joining date" in p for p in problems)


def test_a_bare_url_in_the_body_is_refused():
    body = '<p>Fill the form at https://example.com/form please.</p>'
    problems = je.check_body(body, compensation=None, start_date=None)
    assert any("Click here" in p for p in problems)


def test_an_unfilled_template_slot_is_refused():
    problems = je.check_body("<p>Hi {{CANDIDATE_FIRST_NAME}},</p>",
                             compensation=None, start_date=None)
    assert any("did not fill in" in p and "CANDIDATE_FIRST_NAME" in p
               for p in problems)


# --------------------------------------------------------------------------
# Pilot recipients
# --------------------------------------------------------------------------


def test_a_pilot_goes_to_ayesha_alone_whatever_was_configured():
    r = je.recipients_for(live=False, candidate_email="someone@example.com",
                          cc=["hiring@taleemabad.com"])
    assert r == {"to": [je.PILOT_RECIPIENT], "cc": []}
    assert "someone@example.com" not in r["to"] + r["cc"]


def test_a_live_send_keeps_its_cc():
    r = je.recipients_for(live=True, candidate_email="someone@example.com",
                          cc=["hiring@taleemabad.com"])
    assert r["to"] == ["someone@example.com"]
    assert r["cc"] == ["hiring@taleemabad.com"]


def test_a_live_send_without_an_address_raises():
    with pytest.raises(je.JoiningEmailError):
        je.recipients_for(live=True, candidate_email=None)
