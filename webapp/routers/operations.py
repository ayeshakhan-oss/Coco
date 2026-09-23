"""Hiring Operations: the daily attendance report, drawn from Markaz.

`webapp/services/attendance.py` holds the rules -- the implausible-date guard,
the categories and the stat boxes. This router is the only code that queries
for them.

🔴 IT READS MARKAZ, NOT TEAMS. The SOP scrapes the Teams "Presence" channel in
   Mission Comms, whose last message is 2026-04-24; the whole team has been
   quiet since 2026-06-21. Absence now lives in Markaz and is current to today.
   See the service docstring.

🔴 IT REPORTS RECORDED ABSENCE, NEVER PRESENCE. A leave system cannot say
   somebody walked into the office, so the headline number is "no absence
   recorded" and every response carries the caveat in full.

Nothing here sends anything. The report is built and shown; sending is a
separate, explicit step (Ayesha, 2026-09-23: "draft and show me, I press
send").
"""

from __future__ import annotations

import datetime as dt
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user
from ..schemas import AttendanceReportOut, DecisionBriefOut, HiringBriefOut
from ..services import attendance as att
from ..services import decision_brief as brief_service
from ..services import hiring_funnel

log = logging.getLogger("webapp.routers.operations")

router = APIRouter(prefix="/api/operations", tags=["operations"])

# The head-office roster. `employee_profiles` is the payroll baseline; the SOP's
# hardcoded 84 was true in April and is 131 today, so it is read live and never
# written down.
_PAYROLL_SQL = text(
    """
    SELECT ep.user_id,
           u.first_name || ' ' || coalesce(u.last_name, '') AS name,
           ep.payroll_entity,
           ep.department,
           ep.job_title
    FROM employee_profiles ep
    JOIN users u ON u.id = ep.user_id
    WHERE ep.payroll_entity IS NOT NULL
    """
)

# Every approved leave row. Deliberately NOT filtered by date in SQL: the
# implausible-date guard lives in the service and has to SEE the broken rows in
# order to report them, and a SQL BETWEEN would silently include the ones with
# impossible end dates anyway.
_LEAVE_SQL = text(
    """
    SELECT lr.user_id,
           u.first_name || ' ' || coalesce(u.last_name, '') AS name,
           lr.leave_type,
           lr.sub_category,
           lr.is_half_day,
           lr.start_date::text AS start_date,
           lr.end_date::text   AS end_date
    FROM leave_requests lr
    JOIN users u ON u.id = lr.user_id
    WHERE lr.status = 'approved'
    """
)

_ENTITIES_SQL = text(
    "SELECT payroll_entity, COUNT(*) AS n FROM employee_profiles "
    "WHERE payroll_entity IS NOT NULL GROUP BY payroll_entity ORDER BY n DESC"
)


@router.get("/attendance/entities")
def list_entities(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Payroll entities and their headcount, so the page can offer the real
    ones rather than a hardcoded list that goes stale."""
    rows = db.execute(_ENTITIES_SQL).mappings().all()
    return {
        "entities": [dict(r) for r in rows],
        "default": list(att.I10_ENTITIES),
    }


@router.get("/attendance", response_model=AttendanceReportOut)
def attendance(
    on: str | None = Query(None, description="ISO date; defaults to today"),
    entities: str | None = Query(
        None, description="Comma-separated payroll entities; defaults to I-10 (OPL, OWT)"
    ),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    if on:
        try:
            day = dt.date.fromisoformat(on)
        except ValueError:
            raise HTTPException(422, f"{on!r} is not a date in YYYY-MM-DD form")
    else:
        day = dt.date.today()

    chosen = (
        tuple(e.strip() for e in entities.split(",") if e.strip())
        if entities else att.I10_ENTITIES
    )
    if not chosen:
        raise HTTPException(422, "no payroll entity selected; nothing to report on")

    payroll = [dict(r) for r in db.execute(_PAYROLL_SQL).mappings()]
    leave = [dict(r) for r in db.execute(_LEAVE_SQL).mappings()]

    report = att.build_report(
        on=day, payroll=payroll, leave_rows=leave, entities=chosen
    )
    if not report["total_on_payroll"]:
        raise HTTPException(
            404,
            f"no one on the payroll for {list(chosen)}. Check the entity names "
            "against /api/operations/attendance/entities.",
        )

    # The categories must account for everyone. If they ever do not, the report
    # is wrong in a way no reader could see, so it refuses rather than showing
    # numbers that do not add up.
    if not att.boxes_balance(report):
        log.error("attendance: boxes do not balance for %s %s", day, chosen)
        raise HTTPException(
            500,
            "The attendance categories do not add up to the payroll total, so "
            "the report would be wrong. This has been logged.",
        )

    return AttendanceReportOut(
        **report,
        stat_boxes=att.stat_boxes(report),
        source="Markaz employee_profiles and approved leave_requests",
    )


# Everything the brief is allowed to claim, for one position.
#
# Joins Markaz to the two app-owned tables, LEFT and filtered on `is_current`,
# so a candidate with no CV screen and no case-study score still appears with
# those fields empty. The brief counts what is missing rather than hiding it.
_BRIEF_SQL = text(
    """
    SELECT a.id                             AS application_id,
           trim(coalesce(c.first_name,'') || ' ' || coalesce(c.last_name,'')) AS name,
           a.status                         AS status,
           a.values_interview_result        AS values_interview_result,
           a.values_scorecard->>'proceedToRightSeat' AS proceed,
           a.values_scorecard->>'finalComments'      AS final_comments,
           a.case_study_status              AS case_study_status,
           a.case_study_submission          AS case_study_submission,
           a.case_study_word_file           AS case_study_word_file,
           a.gwc_interview_result           AS gwc_interview_result,
           a.gwc_interview_date             AS gwc_interview_date,
           (c.resume_data IS NOT NULL AND length(c.resume_data) > 0) AS has_cv,
           cs.tier                          AS cv_screen_tier,
           cs.match                         AS cv_screen_match,
           ev.band                          AS case_study_band,
           ev.total                         AS case_study_total
    FROM applications a
    JOIN candidates c ON c.id = a.candidate_id
    LEFT JOIN coco.cv_screens cs
           ON cs.application_id = a.id AND cs.is_current
    LEFT JOIN coco.case_study_evaluations ev
           ON ev.application_id = a.id
    WHERE a.job_id = :job_id
    ORDER BY a.id
    """
)


@router.get("/decision-brief/{job_id}", response_model=DecisionBriefOut)
def decision_brief(
    job_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """The four-part decision brief for one position.

    Read only, and it never converts an empty Markaz field into a finding: a
    candidate with no debrief on record is reported as having no record, not as
    overdue. What is missing is counted and stated.
    """
    job = db.execute(
        text("SELECT id AS job_pk, title FROM jobs WHERE id = :job_id"),
        {"job_id": job_id},
    ).mappings().first()
    if not job:
        raise HTTPException(404, f"Job {job_id} not found")

    rows = [dict(r) for r in db.execute(_BRIEF_SQL, {"job_id": job_id}).mappings()]
    try:
        brief = brief_service.build_brief(job=dict(job), rows=rows)
    except brief_service.DecisionBriefError as exc:
        raise HTTPException(404, str(exc)) from exc

    # A brief that silently loses a candidate is worse than no brief.
    if not brief_service.everyone_is_accounted_for(brief):
        log.error("decision_brief: groups do not account for every candidate on job %s", job_id)
        raise HTTPException(
            500,
            "The pipeline groups do not account for every candidate, so the "
            "brief would be incomplete. This has been logged.",
        )

    return DecisionBriefOut(**brief, stat_boxes=brief_service.stat_boxes(brief))


# What the mailbox saw, per application, for the funnel's Gmail-derived
# stages. `comm_evidence` is one row per application by construction, so these
# counts are a FLOOR and the service labels them as such.
_FUNNEL_SQL = text(
    """
    SELECT a.id                             AS application_id,
           a.status                         AS status,
           a.values_interview_result        AS values_interview_result,
           a.values_scorecard->>'proceedToRightSeat' AS proceed,
           a.case_study_status              AS case_study_status,
           a.case_study_submission          AS case_study_submission,
           e.matched_subject                AS matched_subject
    FROM applications a
    LEFT JOIN coco.comm_evidence e ON e.application_id = a.id
    WHERE a.job_id = :job_id
    ORDER BY a.id
    """
)

_SYNCED_AT_SQL = text(
    "SELECT max(checked_at)::text AS synced FROM coco.comm_evidence WHERE job_id = :job_id"
)


@router.get("/hiring-brief/{job_id}", response_model=HiringBriefOut)
def hiring_brief(
    job_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """The hiring decision brief: the funnel plus the recommendations.

    The SOP reads the Calendar for bookings. That access is gone, and it turns
    out not to be needed: the booking system emails a confirmation
    ("Appointment booked: ...") and those are already in the synced mailbox
    evidence. Every Gmail-derived count is reported as a floor.
    """
    job = db.execute(
        text("SELECT id AS job_pk, title FROM jobs WHERE id = :job_id"),
        {"job_id": job_id},
    ).mappings().first()
    if not job:
        raise HTTPException(404, f"Job {job_id} not found")

    rows = [dict(r) for r in db.execute(_FUNNEL_SQL, {"job_id": job_id}).mappings()]
    if not rows:
        raise HTTPException(404, f"No applications on {job['title']!r} to brief on")

    synced = db.execute(_SYNCED_AT_SQL, {"job_id": job_id}).scalar()
    funnel = hiring_funnel.build_funnel(
        job=dict(job), rows=rows, evidence_synced_at=synced
    )

    # The recommendations half, from the same job.
    brief_rows = [dict(r) for r in db.execute(_BRIEF_SQL, {"job_id": job_id}).mappings()]
    brief = brief_service.build_brief(job=dict(job), rows=brief_rows)
    if not brief_service.everyone_is_accounted_for(brief):
        log.error("hiring_brief: groups do not account for every candidate on job %s", job_id)
        raise HTTPException(
            500,
            "The pipeline groups do not account for every candidate, so the "
            "brief would be incomplete. This has been logged.",
        )

    return HiringBriefOut(
        **{k: v for k, v in funnel.items() if k != "stages"},
        stages=funnel["stages"],
        inconsistencies=hiring_funnel.narrows_monotonically(funnel),
        brief=DecisionBriefOut(**brief, stat_boxes=brief_service.stat_boxes(brief)),
    )
