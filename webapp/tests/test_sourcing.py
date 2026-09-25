"""Sourcing: the Markaz gate, verification honesty, and the tenure parser.

Three tests here exist because of things that actually went wrong:

  * `test_nobody_enters_markaz_without_confirmed_interest` -- the skill's core
    rule, which until now was discipline rather than a condition.
  * `test_not_found_is_not_evidence_of_a_fake_person` -- a subagent invented 12
    people and then falsely retracted 6 real ones, and the verifier itself has
    known false negatives.
  * `test_a_connection_count_is_not_years_of_experience` -- the first Band
    classifier read "26 connections" as 8+ years and promoted two people to
    Tier 1 on it.

Run: python -m pytest webapp/tests/test_sourcing.py -v
"""

from __future__ import annotations

import pytest

from webapp.services import sourcing as s


def _row(**over):
    row = {
        "name": "Aa One",
        "organization": "Chemonics International",
        "linkedin_url": "https://pk.linkedin.com/in/aa-one-123",
        "verification_state": s.CONFIRMED,
        "outreach_state": s.NOT_CONTACTED,
        "markaz_application_id": None,
    }
    row.update(over)
    return row


# --------------------------------------------------------------------------
# The Markaz gate
# --------------------------------------------------------------------------


def test_nobody_enters_markaz_without_confirmed_interest():
    """The skill's core rule: "Markaz is ONLY touched after confirmed interest.
    Never speculatively." A sourced person who has not said yes is not an
    applicant, and putting them in the pipeline makes them look like one to
    every report that counts applications."""
    for state in (s.NOT_CONTACTED, s.CONTACTED, s.NO_REPLY, s.REPLIED_NOT_INTERESTED):
        reason = s.may_push_to_markaz(_row(outreach_state=state))
        assert reason and "confirmed interest" in reason, state


def test_somebody_who_said_yes_may_be_pushed():
    assert s.may_push_to_markaz(_row(outreach_state=s.REPLIED_INTERESTED)) is None


def test_a_verified_profile_is_not_by_itself_a_reason_to_push():
    """Verification says the person exists. It says nothing about whether they
    want the job."""
    assert s.may_push_to_markaz(
        _row(verification_state=s.CONFIRMED, outreach_state=s.CONTACTED)
    ) is not None


def test_nobody_is_pushed_twice():
    reason = s.may_push_to_markaz(
        _row(outreach_state=s.REPLIED_INTERESTED, markaz_application_id=4321)
    )
    assert reason == "already in Markaz"


def test_a_row_with_no_name_is_refused():
    reason = s.may_push_to_markaz(_row(outreach_state=s.REPLIED_INTERESTED, name="  "))
    assert reason == "no name on record"


# --------------------------------------------------------------------------
# Verification honesty
# --------------------------------------------------------------------------


def test_not_found_is_not_evidence_of_a_fake_person():
    """Savera Bokhari came back NOT_FOUND while sitting verbatim in the raw
    captures. Nothing may treat this state as proof of invention."""
    assert s.NOT_FOUND in s.VERIFICATION_STATES
    assert s.is_verified(s.NOT_FOUND) is False
    summary = s.summarise([_row(verification_state=s.NOT_FOUND)])
    assert "not evidence they are invented" in summary["caveat"]


def test_only_a_confirmed_profile_counts_as_verified():
    assert s.is_verified(s.CONFIRMED) is True
    for state in (s.UNCONFIRMED, s.NOT_FOUND, s.NO_URL, None):
        assert s.is_verified(state) is False


def test_verification_is_four_states_not_a_boolean():
    """A boolean forces "not confirmed" and "checked and not found" into the
    same bucket, and they mean different things."""
    assert len(s.VERIFICATION_STATES) == 4


def test_an_unknown_state_is_refused_rather_than_stored():
    with pytest.raises(s.SourcingError, match="verification state"):
        s.validate_states("probably real", s.NOT_CONTACTED)
    with pytest.raises(s.SourcingError, match="outreach state"):
        s.validate_states(s.CONFIRMED, "messaged maybe")


# --------------------------------------------------------------------------
# Tenure
# --------------------------------------------------------------------------


def test_a_connection_count_is_not_years_of_experience():
    """Sadaf Gul was classified 8+ years from "26 connections"."""
    assert s.years_from_note("26 connections") is None


def test_a_calendar_year_is_not_years_of_experience():
    """Javaria Abbas was classified 8+ because her post was dated 2023."""
    assert s.years_from_note("post dated 2023") is None
    assert s.years_from_note("joined in 2019") is None


def test_a_hedge_means_we_do_not_know():
    for note in ("likely 4+ years", "approx 5 years", "around 6 years", "unclear"):
        assert s.years_from_note(note) is None, note


def test_an_over_cap_note_is_not_read_as_in_band():
    assert s.years_from_note("MAY EXCEED CAP") is None


def test_a_plain_statement_of_years_is_read():
    assert s.years_from_note("7 years in partnerships") == 7
    assert s.years_from_note("3+ yrs fundraising") == 3
    assert s.years_from_note("10 yr career") == 10


def test_an_absurd_tenure_is_not_believed():
    assert s.years_from_note("99 years") is None


def test_an_empty_note_is_unknown_not_zero():
    assert s.years_from_note(None) is None
    assert s.years_from_note("") is None


# --------------------------------------------------------------------------
# Identity
# --------------------------------------------------------------------------


def test_the_same_person_on_two_country_subdomains_is_one_person():
    a = _row(linkedin_url="https://pk.linkedin.com/in/aa-one-123")
    b = _row(linkedin_url="https://www.linkedin.com/in/AA-One-123/")
    assert s.identity_key(a) == s.identity_key(b)


def test_two_people_with_the_same_name_at_different_orgs_stay_separate():
    a = _row(name="Ali Khan", organization="TCF", linkedin_url=None)
    b = _row(name="Ali Khan", organization="PPAF", linkedin_url=None)
    assert s.identity_key(a) != s.identity_key(b)


def test_a_url_that_is_not_a_profile_yields_no_slug():
    assert s.linkedin_slug("https://linkedin.com/company/tcf") is None
    assert s.linkedin_slug(None) is None


def test_duplicates_are_found_by_slug():
    rows = [
        _row(linkedin_url="https://pk.linkedin.com/in/x"),
        _row(linkedin_url="https://www.linkedin.com/in/X/"),
        _row(linkedin_url="https://pk.linkedin.com/in/y"),
    ]
    dupes = s.find_duplicates(rows)
    assert len(dupes) == 1 and len(next(iter(dupes.values()))) == 2


# --------------------------------------------------------------------------
# Summary
# --------------------------------------------------------------------------


def test_the_summary_keeps_unverified_out_of_the_verified_count():
    rows = [
        _row(verification_state=s.CONFIRMED),
        _row(verification_state=s.UNCONFIRMED),
        _row(verification_state=s.NOT_FOUND),
        _row(verification_state=s.NO_URL),
    ]
    out = s.summarise(rows)
    assert out["verification"][s.CONFIRMED] == 1
    assert out["total"] == 4


def test_ready_for_markaz_counts_only_those_who_said_yes():
    rows = [
        _row(outreach_state=s.REPLIED_INTERESTED),
        _row(outreach_state=s.CONTACTED),
        _row(outreach_state=s.REPLIED_INTERESTED, markaz_application_id=1),
    ]
    out = s.summarise(rows)
    assert out["ready_for_markaz"] == 1
    assert out["in_markaz"] == 1
