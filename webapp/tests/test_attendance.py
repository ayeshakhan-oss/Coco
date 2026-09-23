"""Daily attendance from Markaz.

The load-bearing tests here are the two that keep the report honest:

  * `test_an_impossible_end_date_never_marks_anyone_absent` -- two real rows in
    Markaz carry end years of 42026 and 20226, and a plain BETWEEN marks those
    people absent for ever. Today that turned 8 genuine absences into 10.
  * `test_the_headline_category_is_not_called_present` -- Markaz records
    absence, not attendance, and a number labelled "onsite" would be read as
    something we cannot see.

Run: python -m pytest webapp/tests/test_attendance.py -v
"""

from __future__ import annotations

import datetime as dt

import pytest

from webapp.services import attendance as att

TODAY = dt.date(2026, 9, 23)


def _person(uid, name, entity="OPL", dept="P&C"):
    return {"user_id": uid, "name": name, "payroll_entity": entity, "department": dept}


def _leave(uid, name, start, end, leave_type="medical", **over):
    row = {"user_id": uid, "name": name, "start_date": start, "end_date": end,
           "leave_type": leave_type, "sub_category": None, "is_half_day": False}
    row.update(over)
    return row


PAYROLL = [_person(1, "Aa One"), _person(2, "Bb Two"), _person(3, "Cc Three"),
           _person(4, "Dd Four", entity="OWT")]


# --------------------------------------------------------------------------
# The corrupt dates
# --------------------------------------------------------------------------


def test_an_impossible_end_date_never_marks_anyone_absent():
    """The exact shapes sitting in Markaz today."""
    for bad_end in ("42026-02-01", "20226-01-02"):
        assert att.date_is_implausible("2026-04-01", bad_end)
        assert att.covers("2026-04-01", bad_end, TODAY) is False


def test_the_two_real_corrupt_rows_are_reported_not_silently_dropped():
    """Somebody has to fix them in Markaz. Dropping them quietly leaves the
    same two people wrong in tomorrow's report too."""
    report = att.build_report(
        on=TODAY, payroll=PAYROLL,
        leave_rows=[
            _leave(1, "Aa One", "2026-04-01", "42026-02-01", "work_from_home"),
            _leave(2, "Bb Two", "2025-12-29", "20226-01-02", "annual"),
        ],
    )
    assert len(report["on_leave"]) == 0
    assert len(report["working_from_home"]) == 0
    assert len(report["needs_correction"]) == 2
    assert all(c["problem"] for c in report["needs_correction"])
    names = {c["name"] for c in report["needs_correction"]}
    assert names == {"Aa One", "Bb Two"}


def test_a_leave_longer_than_any_real_leave_is_flagged():
    assert att.date_is_implausible("2026-01-01", "2026-12-31")
    assert "spans" in att.date_is_implausible("2026-01-01", "2026-12-31")


def test_an_end_before_a_start_is_flagged():
    assert "before it starts" in att.date_is_implausible("2026-09-10", "2026-09-01")


def test_a_three_month_medical_absence_is_allowed():
    """The longest genuine approved leave in the table. The guard must not
    catch it."""
    assert att.date_is_implausible("2026-07-07", "2026-10-07") is None
    assert att.covers("2026-07-07", "2026-10-07", TODAY) is True


def test_an_unparseable_date_is_not_treated_as_open_ended():
    """A missing end date would read as leave with no end, which is worse than
    flagging it."""
    assert att.date_is_implausible("2026-09-01", "not-a-date")
    assert att.covers("2026-09-01", "not-a-date", TODAY) is False


# --------------------------------------------------------------------------
# What the report may claim
# --------------------------------------------------------------------------


def test_the_headline_category_is_not_called_present():
    """Markaz records absence. It cannot tell us somebody walked into the
    office, and a box labelled "onsite" would be read as attendance."""
    assert att.NO_ABSENCE_RECORDED == "no_absence_recorded"
    report = att.build_report(on=TODAY, payroll=PAYROLL, leave_rows=[])
    labels = " ".join(b["label"] for b in att.stat_boxes(report)).lower()
    for forbidden in ("onsite", "present", "in office", "attended"):
        assert forbidden not in labels, f"a box claims {forbidden!r}"


def test_the_caveat_travels_with_every_report():
    report = att.build_report(on=TODAY, payroll=PAYROLL, leave_rows=[])
    assert "not the same as being seen" in report["presence_caveat"]


# --------------------------------------------------------------------------
# Counting
# --------------------------------------------------------------------------


def test_leave_and_wfh_are_counted_separately():
    report = att.build_report(
        on=TODAY, payroll=PAYROLL,
        leave_rows=[
            _leave(1, "Aa One", "2026-09-22", "2026-09-25", "work_from_home"),
            _leave(2, "Bb Two", "2026-09-23", "2026-09-23", "medical"),
        ],
    )
    assert [p["name"] for p in report["working_from_home"]] == ["Aa One"]
    assert [p["name"] for p in report["on_leave"]] == ["Bb Two"]
    assert report["no_absence_recorded"] == 2


def test_the_boxes_account_for_everyone_on_the_payroll():
    report = att.build_report(
        on=TODAY, payroll=PAYROLL,
        leave_rows=[_leave(1, "Aa One", "2026-09-23", "2026-09-23")],
    )
    assert att.boxes_balance(report)
    assert report["total_on_payroll"] == 4


def test_somebody_not_on_this_offices_payroll_cannot_inflate_the_count():
    """NIETE Islamabad is a different site. Its leave must not appear in an
    I-10 report."""
    report = att.build_report(
        on=TODAY, payroll=PAYROLL,
        leave_rows=[_leave(99, "Ee Five", "2026-09-23", "2026-09-23")],
    )
    assert report["on_leave"] == [] and att.boxes_balance(report)


def test_entities_outside_the_requested_office_are_excluded_from_the_roster():
    report = att.build_report(on=TODAY, payroll=PAYROLL + [
        _person(9, "Ff Six", entity="NIETE Islamabad")], leave_rows=[])
    assert report["total_on_payroll"] == 4


def test_two_leave_rows_for_one_person_count_once():
    """A half day and a full day on the same date is still one person away."""
    report = att.build_report(
        on=TODAY, payroll=PAYROLL,
        leave_rows=[
            _leave(1, "Aa One", "2026-09-23", "2026-09-23", is_half_day=True),
            _leave(1, "Aa One", "2026-09-23", "2026-09-23"),
        ],
    )
    assert len(report["on_leave"]) == 1
    assert att.boxes_balance(report)


def test_leave_that_does_not_cover_the_day_is_ignored():
    report = att.build_report(
        on=TODAY, payroll=PAYROLL,
        leave_rows=[_leave(1, "Aa One", "2026-09-01", "2026-09-05")],
    )
    assert report["on_leave"] == []
    assert report["no_absence_recorded"] == 4


def test_the_first_and_last_day_of_leave_both_count():
    for day in ("2026-09-23", "2026-09-25"):
        assert att.covers("2026-09-23", "2026-09-25", dt.date.fromisoformat(day))


# --------------------------------------------------------------------------
# The stat boxes
# --------------------------------------------------------------------------


def test_the_corrections_box_appears_only_when_there_is_something_to_fix():
    clean = att.build_report(on=TODAY, payroll=PAYROLL, leave_rows=[])
    assert all(b["label"] != "Records to fix" for b in att.stat_boxes(clean))

    dirty = att.build_report(on=TODAY, payroll=PAYROLL, leave_rows=[
        _leave(1, "Aa One", "2026-04-01", "42026-02-01")])
    assert any(b["label"] == "Records to fix" for b in att.stat_boxes(dirty))


def test_the_surviving_boxes_keep_the_locked_colours():
    """Three of the template's seven boxes only existed to chase Teams
    announcements. The ones that survive keep their colours."""
    report = att.build_report(on=TODAY, payroll=PAYROLL, leave_rows=[])
    colours = {b["label"]: b["colour"] for b in att.stat_boxes(report)}
    assert colours["No absence recorded"] == "#e8f5e9"   # was "Onsite Today"
    assert colours["On leave"] == "#ffe0b2"
    assert colours["Working from home"] == "#e3f2fd"


def test_corrections_are_outside_the_balance_because_they_count_rows_not_people():
    report = att.build_report(on=TODAY, payroll=PAYROLL, leave_rows=[
        _leave(1, "Aa One", "2026-04-01", "42026-02-01"),
        _leave(1, "Aa One", "2025-12-29", "20226-01-02"),
    ])
    assert len(report["needs_correction"]) == 2
    assert att.boxes_balance(report), "broken rows must not disturb the people count"


def test_a_broken_date_is_reported_in_full_not_truncated():
    """These are the exact values somebody has to correct in Markaz.
    "42026-02-01" trimmed to "42026-02-0" sends them looking for the wrong
    thing, and the valid rows ARE truncated to 10 chars, so it is an easy
    mistake to make."""
    report = att.build_report(on=TODAY, payroll=PAYROLL, leave_rows=[
        _leave(1, "Aa One", "2026-04-01", "42026-02-01", "work_from_home")])
    assert report["needs_correction"][0]["end_date"] == "42026-02-01"
