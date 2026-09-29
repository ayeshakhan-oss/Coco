"""Reading an offer thread: the counter case, and everything that is not pay.

Run: python -m pytest webapp/tests/test_offer_evidence.py -v

THE CASE THIS IS BUILT AROUND. Mariam and Hafiza both countered their offers
and the agreed figure was NOT the one in the first offer letter (CLAUDE.md
Rule 19). Anything that reads the first match and stops would have put the
wrong salary in two of the last handful of contracts. So the thread is read
to the end, the latest figure wins, and a disagreement is reported rather than
resolved quietly.
"""

from __future__ import annotations

import pytest

from webapp.services import offer_evidence as oe


# --------------------------------------------------------------------------
# Amounts
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Gross Salary PKR 150,000 per month", 150_000),
        ("Total Earnings Rs. 220,000/- inclusive of tax", 220_000),
        ("a monthly figure of 95,000 PKR", 95_000),
        ("Basic Salary: PKR 60,000", 60_000),
        ("Rs 1,250,000 annually", 1_250_000),
    ],
)
def test_a_salary_is_found_however_it_is_written(text, expected):
    found = oe.find_amounts(text)
    assert found and found[0]["amount"] == expected


def test_a_number_with_no_currency_is_not_a_salary():
    """A bare number in a sentence about reach is not pay."""
    assert oe.find_amounts("we reached 150,000 students last year") == []


@pytest.mark.parametrize(
    "text",
    [
        "the project budget is PKR 4,000,000",
        "total funding of Rs. 900,000 from the grant",
        "reimbursement of PKR 12,000 for travel",
        "we served 250,000 beneficiaries at a cost of PKR 300,000",
    ],
)
def test_money_that_is_plainly_not_pay_is_ignored(text):
    assert oe.find_amounts(text) == [], text


def test_amounts_are_labelled_by_what_precedes_them():
    text = (
        "Base Salary: PKR 60,000\n"
        "Medical Allowance: PKR 15,000\n"
        "Other Allowance: PKR 25,000\n"
        "Total Earnings PKR 100,000 per month inclusive of tax"
    )
    got = {a["label"]: a["amount"] for a in oe.find_amounts(text)}
    assert got == {"base": 60_000, "medical": 15_000, "other": 25_000, "total": 100_000}


def test_an_implausible_amount_is_rejected():
    assert oe.find_amounts("PKR 12") == []
    assert oe.find_amounts("PKR 99,000,000") == []


def test_every_amount_carries_the_sentence_it_came_from():
    found = oe.find_amounts("Your gross salary will be PKR 150,000 per month.")
    assert "gross salary" in found[0]["context"]


# --------------------------------------------------------------------------
# Dates
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text,iso",
    [
        ("starting 1st October 2026", "2026-10-01"),
        ("commencing 01 October 2026", "2026-10-01"),
        ("your first day is October 1, 2026", "2026-10-01"),
        ("effective 2026-10-01", "2026-10-01"),
        ("joining on 15 Dec 2026", "2026-12-15"),
    ],
)
def test_a_start_date_is_found_and_recognised(text, iso):
    found = oe.find_dates(text)
    assert found, text
    assert found[0]["date"] == iso
    assert found[0]["kind"] == "start"


def test_an_end_date_is_told_apart_from_a_start_date():
    found = oe.find_dates(
        "The contract runs from 1 October 2026 until 31 March 2027.")
    kinds = {f["kind"]: f["date"] for f in found}
    assert kinds.get("start") == "2026-10-01"
    assert kinds.get("end") == "2027-03-31"


def test_an_impossible_date_is_not_returned():
    assert oe.find_dates("31 February 2026") == []
    assert oe.find_dates("1 January 1998") == []


def test_a_date_with_no_cue_word_is_left_unknown():
    found = oe.find_dates("We met on 4 July 2026 to discuss.")
    assert found and found[0]["kind"] == "unknown"


# --------------------------------------------------------------------------
# A whole thread, including the counter
# --------------------------------------------------------------------------


OFFER = {
    "from_me": True, "date": "2026-08-01T10:00:00Z",
    "subject": "Congratulations on Your Selection as a Coach",
    "body": "We are delighted to offer you the role. Total Earnings PKR 120,000 "
            "per month inclusive of tax, commencing 1 September 2026.",
}
COUNTER = {
    "from_me": False, "date": "2026-08-02T09:00:00Z",
    "subject": "Re: Congratulations on Your Selection as a Coach",
    "body": "Thank you so much. Would it be possible to reconsider the figure? "
            "I was hoping for something closer to PKR 140,000.",
}
AGREED = {
    "from_me": True, "date": "2026-08-03T16:00:00Z",
    "subject": "Re: Congratulations on Your Selection as a Coach",
    "body": "Happy to confirm. Total Earnings PKR 135,000 per month inclusive "
            "of tax, commencing 1 September 2026 until 31 March 2027.",
}


def test_the_agreed_figure_wins_not_the_first_offer():
    """The whole point. Reading the first message gives 120,000, which is the
    wrong number and the exact Mariam/Hafiza failure."""
    result = oe.read_thread([OFFER, COUNTER, AGREED])
    assert result["proposed"]["total"]["amount"] == 135_000


def test_the_order_of_the_messages_does_not_change_the_answer():
    """Gmail does not hand them back in order."""
    result = oe.read_thread([AGREED, OFFER, COUNTER])
    assert result["proposed"]["total"]["amount"] == 135_000


def test_a_disagreement_in_the_thread_is_reported():
    result = oe.read_thread([OFFER, COUNTER, AGREED])
    text = " ".join(result["warnings"])
    assert "more than one total figure" in text
    assert "120,000" in text and "135,000" in text


def test_a_candidate_counter_is_called_out_by_name():
    result = oe.read_thread([OFFER, COUNTER, AGREED])
    assert result["counters"], "the counter message was not noticed"
    assert any("countered" in w for w in result["warnings"])


def test_our_own_message_is_never_mistaken_for_a_counter():
    """Only the candidate can counter. We negotiate in our own words too."""
    ours = dict(OFFER, body="We can revise this if needed.")
    assert oe.read_thread([ours])["counters"] == []


def test_the_dates_come_through_with_the_salary():
    result = oe.read_thread([OFFER, COUNTER, AGREED])
    assert result["proposed"]["start_date"]["date"] == "2026-09-01"
    assert result["proposed"]["end_date"]["date"] == "2027-03-31"


def test_a_thread_with_no_salary_says_so_rather_than_guessing():
    quiet = {"from_me": True, "date": "2026-08-01T10:00:00Z",
             "subject": "Welcome", "body": "Looking forward to having you."}
    result = oe.read_thread([quiet])
    assert result["proposed"]["total"] is None
    assert any("No salary figure" in w for w in result["warnings"])


def test_an_empty_thread_does_not_raise():
    result = oe.read_thread([])
    assert result["messages_read"] == 0
    assert result["proposed"]["total"] is None


def test_every_proposed_value_says_where_it_came_from():
    """A figure with no source is a figure nobody can check."""
    result = oe.read_thread([OFFER, COUNTER, AGREED])
    for key in ("total", "start_date", "end_date"):
        value = result["proposed"][key]
        assert value and value["source"]["subject"], key
        assert value["source"]["date"], key


def test_the_breakdown_is_picked_up_when_the_letter_gives_one():
    letter = {
        "from_me": True, "date": "2026-08-01T10:00:00Z", "subject": "Offer",
        "body": "Base Salary: PKR 60,000\nMedical: PKR 15,000\n"
                "Others: PKR 25,000\nTotal Earnings PKR 100,000 per month",
    }
    p = oe.read_thread([letter])["proposed"]
    assert p["base"]["amount"] == 60_000
    assert p["medical"]["amount"] == 15_000
    assert p["other"]["amount"] == 25_000
    assert p["total"]["amount"] == 100_000


# --------------------------------------------------------------------------
# Two gaps found by running this against REAL threads
# --------------------------------------------------------------------------

# Both of these came from Ayesha's actual mailbox on 2026-09-29, not invented.


def test_a_divergent_unlabelled_figure_is_reported():
    """Mariam's real thread. The only figure carrying the word "total" was the
    FIRST offer at 116,000; 118,000, 130,000 and 145,000 were discussed later
    without that word. The same-label check stayed silent and the page would
    have shown 116,000 as settled."""
    thread = [
        {"from_me": True, "date": "2026-08-19T10:00:00Z", "subject": "Congratulations Mariam",
         "body": "Total Earnings PKR 116,000 per month inclusive of tax."},
        {"from_me": False, "date": "2026-08-20T10:00:00Z", "subject": "Re: Congratulations Mariam",
         "body": "Thank you. Would it be possible to reconsider? I was hoping for PKR 145,000."},
        {"from_me": True, "date": "2026-08-21T10:00:00Z", "subject": "Re: Congratulations Mariam",
         "body": "We can stretch to PKR 130,000."},
    ]
    result = oe.read_thread(thread)
    assert result["proposed"]["total"]["amount"] == 116_000  # the only labelled one
    text = " ".join(result["warnings"])
    assert "not the one shown" in text
    assert "130,000" in text and "145,000" in text


def test_a_breakdown_bigger_than_the_total_is_refused_as_readable():
    """Hafiza's real thread yields base 135,000 against total 108,000. One of
    them is read from the wrong place and neither may be copied unchecked."""
    thread = [
        {"from_me": True, "date": "2026-08-19T10:00:00Z", "subject": "Offer Letter CPD Coach",
         "body": "Basic Salary PKR 135,000"},
        {"from_me": True, "date": "2026-09-08T10:00:00Z", "subject": "Re: Congratulations Hafiza",
         "body": "Total Earnings PKR 108,000 per month."},
    ]
    warnings = " ".join(oe.read_thread(thread)["warnings"])
    assert "larger than the total" in warnings


def test_parts_that_do_not_add_up_are_reported():
    thread = [{
        "from_me": True, "date": "2026-08-01T10:00:00Z", "subject": "Offer",
        "body": "Base Salary: PKR 60,000\nMedical: PKR 15,000\n"
                "Total Earnings PKR 100,000 per month",
    }]
    warnings = " ".join(oe.read_thread(thread)["warnings"])
    assert "add up to" in warnings


def test_a_clean_consistent_offer_raises_nothing():
    """The other half: a straightforward thread must not be cluttered with
    warnings, or nobody will read them when they matter."""
    thread = [{
        "from_me": True, "date": "2026-09-07T10:00:00Z",
        "subject": "Congratulations Zia on Your Selection",
        "body": "Total Earnings PKR 108,000 per month inclusive of tax, "
                "commencing 7 September 2026 until 31 December 2026.",
    }]
    result = oe.read_thread(thread)
    assert result["proposed"]["total"]["amount"] == 108_000
    assert result["warnings"] == [], result["warnings"]
