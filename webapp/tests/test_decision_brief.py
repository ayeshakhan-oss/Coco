"""Assembling a decision brief.

The load-bearing tests are the ones that stop the brief asserting things it
cannot see. Markaz records no debrief verdict for anybody on Job 42 and no
case-study score, so the easy mistakes are calling that OVERDUE (a claim about
the candidate) or printing a blank where a number should be.

Run: python -m pytest webapp/tests/test_decision_brief.py -v
"""

from __future__ import annotations

import datetime as dt

import pytest

from webapp.services import decision_brief as db

TODAY = dt.date(2026, 9, 24)
JOB = {"job_pk": 42, "title": "Senior Manager Growth"}


def _row(app_id=1, **over):
    row = {
        "application_id": app_id,
        "name": f"Cand {app_id}",
        "has_cv": True,
        "status": "shortlisted",
        "values_interview_result": None,
        "proceed": None,
        "final_comments": None,
        "case_study_status": None,
        "case_study_submission": None,
        "case_study_word_file": None,
        "case_study_band": None,
        "case_study_total": None,
        "cv_screen_tier": None,
        "cv_screen_match": None,
        "gwc_interview_result": None,
        "gwc_interview_date": None,
    }
    row.update(over)
    return row


# --------------------------------------------------------------------------
# What the brief may NOT claim
# --------------------------------------------------------------------------


def test_no_debrief_on_record_is_not_called_overdue():
    """OVERDUE is a claim about the candidate. Markaz holds no debrief verdict
    for anybody on Job 42, and labelling all of them late would invent a delay
    (CLAUDE.md Rule 18: no record is never no event)."""
    assert db.debrief_verdict(_row(), today=TODAY) == db.NOT_RECORDED
    assert db.NOT_RECORDED not in (
        db.PANEL_DECISION, db.DEBRIEF_CONFIRMED, db.DEBRIEF_SCHEDULED, db.OVERDUE)


def test_overdue_needs_a_date_to_be_late_against():
    past = _row(gwc_interview_date="2026-09-01")
    future = _row(gwc_interview_date="2026-10-01")
    assert db.debrief_verdict(past, today=TODAY) == db.OVERDUE
    assert db.debrief_verdict(future, today=TODAY) == db.DEBRIEF_SCHEDULED


def test_a_recorded_result_is_a_confirmed_debrief():
    for result in ("pass", "fail", "strong_pass"):
        assert db.debrief_verdict(_row(gwc_interview_result=result), today=TODAY) == (
            db.DEBRIEF_CONFIRMED)


def test_an_unparseable_debrief_date_is_not_read_as_overdue():
    assert db.debrief_verdict(_row(gwc_interview_date="soon"), today=TODAY) == db.NOT_RECORDED


def test_the_caveat_travels_with_the_brief():
    brief = db.build_brief(job=JOB, rows=[_row()], today=TODAY)
    assert "statement about our records" in brief["evidence_caveat"]


def test_what_is_missing_is_counted_not_left_blank():
    brief = db.build_brief(job=JOB, rows=[
        _row(1, proceed="Yes", case_study_status="submitted"),
        _row(2, has_cv=False),
    ], today=TODAY)
    assert brief["not_recorded"]["debrief_verdicts"] == 2
    assert brief["not_recorded"]["case_study_scores"] == 1
    assert brief["not_recorded"]["missing_cv"] == 1


# --------------------------------------------------------------------------
# Values: two sources that can disagree
# --------------------------------------------------------------------------


def test_the_scorecard_beats_the_status_column():
    """`proceedToRightSeat` is what the interviewer filled in; the column is
    derived and has been wrong before."""
    row = _row(proceed="Yes", values_interview_result="fail")
    assert db._passed_values(row) is True


def test_a_disagreement_is_surfaced_not_silently_resolved():
    row = _row(proceed="Yes", values_interview_result="fail")
    note = db.values_disagreement(row)
    assert note and "scorecard is used" in note


def test_agreement_raises_nothing():
    assert db.values_disagreement(_row(proceed="Yes", values_interview_result="pass")) is None


def test_no_values_interview_is_none_not_false():
    """None means "not interviewed". False means "interviewed and did not
    pass". Collapsing them puts people in the wrong pipeline group."""
    assert db._passed_values(_row()) is None
    assert db._passed_values(_row(values_interview_result="fail")) is False


# --------------------------------------------------------------------------
# The five groups
# --------------------------------------------------------------------------


def test_every_candidate_lands_in_exactly_one_group():
    rows = [
        _row(1, proceed="Yes"),
        _row(2, proceed="No"),
        _row(3, case_study_status="submitted"),
        _row(4, status="shortlisted"),
        _row(5, status="rejected"),
    ]
    brief = db.build_brief(job=JOB, rows=rows, today=TODAY)
    assert db.everyone_is_accounted_for(brief)
    assert sum(len(g["people"]) for g in brief["groups"]) == 5


def test_the_groups_are_the_sops_five_in_its_order():
    brief = db.build_brief(job=JOB, rows=[_row()], today=TODAY)
    assert [g["key"] for g in brief["groups"]] == list(db.GROUPS)
    assert len(db.GROUPS) == 5


def test_values_out_and_values_pass_are_separated():
    brief = db.build_brief(job=JOB, rows=[
        _row(1, proceed="Yes"), _row(2, proceed="No")], today=TODAY)
    by_key = {g["key"]: g["people"] for g in brief["groups"]}
    assert [p["application_id"] for p in by_key[db.VALUES_PASS_PENDING]] == [1]
    assert [p["application_id"] for p in by_key[db.VALUES_OUT]] == [2]


def test_a_shortlisted_candidate_with_nothing_submitted_is_awaiting_not_rejected():
    brief = db.build_brief(job=JOB, rows=[_row(1, status="shortlisted")], today=TODAY)
    by_key = {g["key"]: g["people"] for g in brief["groups"]}
    assert len(by_key[db.AWAITING_SUBMISSION]) == 1
    assert by_key[db.NOT_INTERVIEWED] == []


# --------------------------------------------------------------------------
# Leading candidates
# --------------------------------------------------------------------------


def test_leading_requires_both_a_values_pass_and_a_submission():
    brief = db.build_brief(job=JOB, rows=[
        _row(1, proceed="Yes", case_study_status="submitted"),
        _row(2, proceed="Yes"),                       # no submission
        _row(3, case_study_status="submitted"),       # no values interview
    ], today=TODAY)
    assert [p["application_id"] for p in brief["leading"]] == [1]


def test_leading_is_ordered_by_the_case_study_then_the_cv_screen():
    brief = db.build_brief(job=JOB, rows=[
        _row(1, proceed="Yes", case_study_status="submitted", case_study_total=62),
        _row(2, proceed="Yes", case_study_status="submitted", case_study_total=81),
        _row(3, proceed="Yes", case_study_status="submitted", cv_screen_match=90),
    ], today=TODAY)
    assert [p["application_id"] for p in brief["leading"]] == [2, 1, 3]


def test_leading_is_not_capped_at_a_fixed_number():
    """CLAUDE.md Rule 17: never force a fixed shortlist size. If five are
    strong, the brief shows five."""
    rows = [_row(i, proceed="Yes", case_study_status="submitted") for i in range(1, 6)]
    brief = db.build_brief(job=JOB, rows=rows, today=TODAY)
    assert len(brief["leading"]) == 5


# --------------------------------------------------------------------------
# CV links
# --------------------------------------------------------------------------


def test_every_person_carries_a_cv_link():
    """The SOP calls this non-negotiable. Served from Markaz, so no manual
    Drive upload stands between the brief and a working link."""
    brief = db.build_brief(job=JOB, rows=[_row(1), _row(2)], today=TODAY)
    everyone = [p for g in brief["groups"] for p in g["people"]]
    assert everyone and all(p["cv_url"] == db.cv_url(p["application_id"]) for p in everyone)


def test_a_candidate_with_no_cv_on_file_is_flagged_rather_than_linked_to_nothing():
    brief = db.build_brief(job=JOB, rows=[_row(1, has_cv=False)], today=TODAY)
    person = brief["groups"][0]["people"][0] if brief["groups"][0]["people"] else None
    person = person or next(p for g in brief["groups"] for p in g["people"])
    assert person["has_cv"] is False
    assert brief["not_recorded"]["missing_cv"] == 1


# --------------------------------------------------------------------------
# Refusals and boxes
# --------------------------------------------------------------------------


def test_a_job_with_no_applications_is_refused():
    with pytest.raises(db.DecisionBriefError, match="nothing to brief on"):
        db.build_brief(job=JOB, rows=[], today=TODAY)


def test_the_four_stat_boxes_are_the_sops_four():
    brief = db.build_brief(job=JOB, rows=[_row()], today=TODAY)
    assert [b["label"] for b in db.stat_boxes(brief)] == [
        "Applications", "Values interviews", "Shortlisted", "Leading"]


def test_the_debrief_schedule_holds_only_people_with_a_date():
    brief = db.build_brief(job=JOB, rows=[
        _row(1, gwc_interview_date="2026-10-01"), _row(2)], today=TODAY)
    assert [p["application_id"] for p in brief["debrief_schedule"]] == [1]


def test_an_unrankable_leading_list_says_so_rather_than_implying_an_order():
    """On Job 42 all 17 leading candidates have no case-study score and no CV
    screen. Presenting them in id order would read as a ranking."""
    brief = db.build_brief(job=JOB, rows=[
        _row(i, proceed="Yes", case_study_status="submitted") for i in (1, 2, 3)
    ], today=TODAY)
    assert brief["leading_note"] and "not ranked" in brief["leading_note"]


def test_a_fully_ranked_list_carries_no_note():
    brief = db.build_brief(job=JOB, rows=[
        _row(1, proceed="Yes", case_study_status="submitted", case_study_total=80),
        _row(2, proceed="Yes", case_study_status="submitted", case_study_total=60),
    ], today=TODAY)
    assert brief["leading_note"] is None


def test_a_partly_ranked_list_says_who_is_unscored():
    brief = db.build_brief(job=JOB, rows=[
        _row(1, proceed="Yes", case_study_status="submitted", case_study_total=80),
        _row(2, proceed="Yes", case_study_status="submitted"),
    ], today=TODAY)
    assert "not on merit" in brief["leading_note"]
