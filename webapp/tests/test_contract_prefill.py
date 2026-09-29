"""Filling a contract from what we know, without inventing anything.

Run: python -m pytest webapp/tests/test_contract_prefill.py -v

THE BUG THIS CAUGHT ON ITS FIRST REAL RUN. The NIETE master has a field called
"EMPLOYER NAME DESIGNATION". A plain `\\bname\\b` rule matched it as the
employee's name and filled it with the CANDIDATE's name, into the signature
block where the signing officer belongs. Found against the real master, not in
theory, and the employer rule now runs first.
"""

from __future__ import annotations

import datetime as dt
import pathlib

import pytest

from webapp.services import contract_prefill as pre
from webapp.services import contracts as spec
from webapp.services import offer_evidence as oe

REPO = pathlib.Path(__file__).resolve().parents[2]
NIETE = REPO / "Contracts" / "NIETE" / "NIETE - Project-based Employment Contract.docx"
NDA = REPO / "Contracts" / "Promotion" / "Template - NDA Full Time Permanent Employee.docx"

MARKAZ = {
    "legal_name": "Marzia Hasnain Khandwala",
    "markaz_name": "Marzia Hasnain",
    "cnic": "42101-1234567-8",
    "position": "Growth Manager - Karachi",
    "hiring_manager": "Waqas Tanveer",
}

OFFER_BODY = (
    "Base Salary: PKR 60,000\nMedical: PKR 18,000\nOthers: PKR 30,000\n"
    "Total Earnings PKR 108,000 per month, commencing 7 September 2026 "
    "until 31 December 2026."
)


def _groups(path: pathlib.Path):
    if not path.is_file():
        pytest.skip(f"master not on this machine: {path.name}")
    return spec.group_fields(spec.discover_fields(path.read_bytes()))


def _offer(body: str = OFFER_BODY):
    return oe.read_thread([{
        "from_me": True, "date": "2026-09-07T10:00:00Z",
        "subject": "Congratulations", "body": body,
    }])


#: "not given" has to be distinguishable from "explicitly no offer thread",
#: or a test asking for no offer silently gets the default one.
_DEFAULT = object()


def _fill(path=NIETE, markaz=_DEFAULT, offer=_DEFAULT):
    return pre.build_prefill(
        groups=_groups(path),
        markaz=MARKAZ if markaz is _DEFAULT else markaz,
        offer=_offer() if offer is _DEFAULT else offer,
        today=dt.date(2026, 9, 29),
    )


# --------------------------------------------------------------------------
# 🔴 The signature block
# --------------------------------------------------------------------------


def test_the_employer_field_never_gets_the_candidates_name():
    """The bug. "EMPLOYER NAME DESIGNATION" is the signing officer, not the
    person being hired."""
    result = _fill()
    assert "EMPLOYER NAME DESIGNATION" not in result["values"]
    assert "EMPLOYER NAME DESIGNATION" in result["still_needed"]


def test_the_employer_rule_is_checked_before_the_name_rule():
    assert pre.meaning_of("EMPLOYER NAME DESIGNATION") == "employer"
    assert pre.meaning_of("EMPLOYEE'S NAME") == "legal_name"


# --------------------------------------------------------------------------
# The legal name
# --------------------------------------------------------------------------


def test_the_legal_name_they_typed_beats_the_name_stored_in_markaz():
    """8 of the 17 who have submitted the form typed a different name."""
    result = _fill()
    assert result["values"]["EMPLOYEE'S NAME"] == "Marzia Hasnain Khandwala"
    assert "differs from the name stored in Markaz" in result["sources"]["EMPLOYEE'S NAME"]


def test_without_a_submitted_form_the_stored_name_is_used_and_flagged():
    markaz = dict(MARKAZ, legal_name=None)
    result = _fill(markaz=markaz)
    assert result["values"]["EMPLOYEE'S NAME"] == "Marzia Hasnain"
    assert "NOT submitted" in result["sources"]["EMPLOYEE'S NAME"]


# --------------------------------------------------------------------------
# The term: two fields written the same way
# --------------------------------------------------------------------------


def test_the_term_start_and_end_are_told_apart_by_the_word_before_them():
    """Both are written "DATE, MONTH, YEAR". Only "from" and "to" distinguish
    them, and matching anywhere in the preceding text finds "from" in both."""
    values = _fill()["values"]
    assert values["DATE, MONTH, YEAR"] == "7th September 2026"
    assert values["DATE, MONTH , YEAR"] == "31st December 2026"


def test_the_duration_is_worked_out_from_the_term_not_read_separately():
    """A contract whose duration disagrees with its own dates is worse than
    one with the duration left blank."""
    result = _fill()
    duration = next(v for k, v in result["values"].items() if " to " in str(v))
    assert duration == "7th September 2026 to 31st December 2026"
    assert "cannot disagree" in " ".join(result["sources"].values())


def test_no_date_ever_names_the_weekday():
    """joining-emails rule 3."""
    days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
            "Saturday", "Sunday")
    blob = " ".join(str(v) for v in _fill()["values"].values())
    assert not any(d in blob for d in days), blob


# --------------------------------------------------------------------------
# The money lines
# --------------------------------------------------------------------------


def test_a_money_field_gets_the_number_only():
    """The master already prints "PKR" in front, so writing "PKR 108,000" into
    it produces "Total Earnings PKR PKR 108,000" on a real contract."""
    values = _fill()["values"]
    money = {k: v for k, v in values.items()
             if str(v).replace(",", "").isdigit()}
    assert money, "no money field was filled"
    for value in money.values():
        assert "PKR" not in str(value)
    assert "108,000" in money.values()


def test_the_breakdown_lines_each_get_their_own_figure():
    values = _fill()["values"]
    filled = {str(v) for v in values.values()}
    for amount in ("108,000", "60,000", "18,000", "30,000"):
        assert amount in filled, amount


def test_a_salary_says_it_is_the_field_most_worth_checking():
    result = _fill()
    money_sources = [s for k, s in result["sources"].items()
                     if str(result["values"][k]).replace(",", "").isdigit()]
    assert money_sources
    assert all("counter" in s for s in money_sources)


# --------------------------------------------------------------------------
# Nothing is invented
# --------------------------------------------------------------------------


def test_with_no_offer_thread_no_salary_or_dates_are_filled():
    result = _fill(offer=None)
    blob = " ".join(str(v) for v in result["values"].values())
    assert "108,000" not in blob
    assert "September 2026" not in blob or "29th September 2026" in blob


def test_a_field_with_nothing_to_go_on_stays_empty():
    """An opaque placeholder with no words before it is left blank rather than
    filled with something plausible."""
    result = _fill()
    assert result["still_needed"], "everything was filled, which cannot be right"


def test_every_filled_field_carries_a_source():
    result = _fill()
    for key in result["values"]:
        assert result["sources"].get(key), f"{key} was filled with no source"


def test_the_nda_fills_completely_because_it_asks_for_nothing_else():
    result = _fill(path=NDA)
    assert result["still_needed"] == [], result["still_needed"]
    assert result["filled"] == result["total_fields"] == 3


def test_the_caveat_always_travels_with_the_result():
    assert "proposal" in _fill()["caveat"]


def test_warnings_from_the_offer_thread_are_carried_through():
    """A countered offer must not lose its warning on the way to the page."""
    countered = oe.read_thread([
        {"from_me": True, "date": "2026-08-01T10:00:00Z", "subject": "Offer",
         "body": "Total Earnings PKR 116,000 per month."},
        {"from_me": False, "date": "2026-08-02T10:00:00Z", "subject": "Re: Offer",
         "body": "Would it be possible to reconsider? I was hoping for PKR 145,000."},
    ])
    result = _fill(offer=countered)
    assert any("negotiation" in w or "not the one shown" in w
               for w in result["warnings"]), result["warnings"]
