"""The hiring funnel.

The patterns here were derived from the 1,210 real subject lines in
coco.comm_evidence, so the tests use those subjects verbatim. The load-bearing
ones are that a stage with no matching email reports "not visible" rather than
0, and that a debrief booking is not mistaken for a values booking.

Run: python -m pytest webapp/tests/test_hiring_funnel.py -v
"""

from __future__ import annotations

from webapp.services import hiring_funnel as hf

JOB = {"job_pk": 42, "title": "Senior Manager Growth"}


def _row(app_id=1, **over):
    row = {
        "application_id": app_id,
        "status": None,
        "values_interview_result": None,
        "proceed": None,
        "case_study_status": None,
        "case_study_submission": None,
        "matched_subject": None,
    }
    row.update(over)
    return row


def _stage(funnel, key):
    return next(s for s in funnel["stages"] if s["key"] == key)


# --------------------------------------------------------------------------
# Classifying real subjects
# --------------------------------------------------------------------------


def test_the_real_booking_subjects_are_recognised():
    """Verbatim from coco.comm_evidence."""
    assert hf.classify_subject(
        "Appointment booked: Zero In Call For Senior Growth Manager (Fahad Ali) @ Mon Aug 4"
    ) == hf.VALUES_BOOKED
    assert hf.classify_subject(
        "Appointment booked: Case Study Debrief - Senior Manager Growth (Umar Zahid) @ Tue"
    ) == hf.DEBRIEF_BOOKED
    assert hf.classify_subject(
        "Lets proceed with the Case Study for Senior Manager Growth - Muhammad"
    ) == hf.CASE_STUDY_SENT


def test_a_debrief_booking_is_not_read_as_a_values_booking():
    """It contains "Appointment booked" AND "case study". Order matters."""
    s = "Appointment booked: Case Study Debrief - Senior Manager Growth (Name) @ Wed"
    assert hf.classify_subject(s) == hf.DEBRIEF_BOOKED


def test_outcome_subjects_are_recognised_in_their_several_forms():
    for subject in (
        "Your Application for Junior Research Associate, Impact & Policy",
        "Your CPD Coach Application Update",
        "Update on Application Outcome",
        "Application Update - Growth Manager Role",
        "Offer Letter Junior Research Associate - Impact & Policy - at Taleemabad",
    ):
        assert hf.classify_subject(subject) == hf.OUTCOME_SENT, subject


def test_double_spaces_do_not_defeat_the_matching():
    """Markaz subjects carry them (CLAUDE.md Rule 18)."""
    assert hf.classify_subject(
        "Appointment  booked:  Zero  In  Call  For  Growth  Manager (Name)"
    ) == hf.VALUES_BOOKED


def test_an_unrelated_subject_classifies_as_nothing():
    assert hf.classify_subject("Re: lunch") is None
    assert hf.classify_subject("") is None
    assert hf.classify_subject(None) is None


# --------------------------------------------------------------------------
# What the funnel may claim
# --------------------------------------------------------------------------


def test_a_stage_with_no_matching_email_is_not_visible_rather_than_zero():
    """0 reads as "nobody was sent one". The truth is we did not recognise
    an email, which is a statement about our matching."""
    funnel = hf.build_funnel(job=JOB, rows=[_row()])
    booked = _stage(funnel, hf.VALUES_BOOKED)
    assert booked["count"] is None
    assert booked["source"] == hf.UNAVAILABLE
    assert "not that none was sent" in booked["note"]


def test_gmail_counts_are_marked_as_a_floor_and_markaz_counts_are_not():
    funnel = hf.build_funnel(job=JOB, rows=[
        _row(1, matched_subject="Appointment booked: Zero In Call For X (A)"),
        _row(2, proceed="Yes"),
    ])
    assert _stage(funnel, hf.VALUES_BOOKED)["is_floor"] is True
    assert _stage(funnel, hf.VALUES_PASSED)["is_floor"] is False
    assert _stage(funnel, hf.VALUES_PASSED)["source"] == hf.MARKAZ


def test_the_caveat_explains_why_gmail_is_a_floor():
    funnel = hf.build_funnel(job=JOB, rows=[_row()])
    assert "one message per candidate" in funnel["caveat"]


# --------------------------------------------------------------------------
# Counting from Markaz
# --------------------------------------------------------------------------


def test_values_passed_reads_the_scorecard_and_the_column():
    funnel = hf.build_funnel(job=JOB, rows=[
        _row(1, proceed="Yes"),
        _row(2, values_interview_result="pass"),
        _row(3, proceed="No"),
    ])
    assert _stage(funnel, hf.VALUES_PASSED)["count"] == 2
    assert _stage(funnel, hf.VALUES_DONE)["count"] == 3


def test_a_submitted_case_study_counts_from_either_column():
    funnel = hf.build_funnel(job=JOB, rows=[
        _row(1, case_study_status="submitted"),
        _row(2, case_study_submission="https://drive/x"),
        _row(3),
    ])
    assert _stage(funnel, hf.CASE_STUDY_SUBMITTED)["count"] == 2


def test_one_candidate_is_counted_once_per_stage_however_many_emails():
    funnel = hf.build_funnel(job=JOB, rows=[
        _row(1, matched_subject="Appointment booked: Zero In Call For X (A)"),
        _row(1, matched_subject="Appointment booked: Zero In Call For X (A)"),
    ])
    assert _stage(funnel, hf.VALUES_BOOKED)["count"] == 1


# --------------------------------------------------------------------------
# The funnel should narrow
# --------------------------------------------------------------------------


def test_a_funnel_that_widens_is_reported():
    """More people cleared values than were shortlisted means one of the two
    numbers is wrong. Better said out loud than left for a reader to notice."""
    funnel = hf.build_funnel(job=JOB, rows=[
        _row(i, proceed="Yes", status="rejected") for i in range(1, 4)
    ])
    # 3 cleared values but the shortlisted count also picks them up, so this
    # particular shape is consistent; force a widening instead.
    funnel["stages"] = [
        {"key": hf.SHORTLISTED, "title": "a", "count": 2, "source": hf.MARKAZ,
         "is_floor": False, "note": None},
        {"key": hf.VALUES_PASSED, "title": "b", "count": 5, "source": hf.MARKAZ,
         "is_floor": False, "note": None},
    ]
    problems = hf.narrows_monotonically(funnel)
    assert problems and "higher than" in problems[0]


def test_a_gmail_floor_rising_above_an_exact_count_is_not_reported():
    """A floor exceeding an exact count says nothing, because the floor is
    measuring a different thing."""
    funnel = {"stages": [
        {"key": hf.SHORTLISTED, "title": "a", "count": 2, "source": hf.MARKAZ,
         "is_floor": False, "note": None},
        {"key": hf.VALUES_BOOKED, "title": "b", "count": 9, "source": hf.GMAIL,
         "is_floor": True, "note": None},
    ]}
    assert hf.narrows_monotonically(funnel) == []


def test_a_healthy_funnel_reports_nothing():
    funnel = {"stages": [
        {"key": hf.SHORTLISTED, "title": "a", "count": 10, "source": hf.MARKAZ,
         "is_floor": False, "note": None},
        {"key": hf.VALUES_PASSED, "title": "b", "count": 4, "source": hf.MARKAZ,
         "is_floor": False, "note": None},
    ]}
    assert hf.narrows_monotonically(funnel) == []


def test_every_stage_is_present_in_order():
    funnel = hf.build_funnel(job=JOB, rows=[_row()])
    assert [s["key"] for s in funnel["stages"]] == list(hf.STAGES)
