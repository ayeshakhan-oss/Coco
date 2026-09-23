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
from ..schemas import AttendanceReportOut
from ..services import attendance as att

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
