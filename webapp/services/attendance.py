"""Daily attendance for the I-10 head office, from Markaz.

SOURCE OF TRUTH for the report's shape:
.claude/skills/03_operations/attendance-reports.md and
memory/attendance_report_complete_template.md.

🔴 THE SOP'S DATA SOURCE NO LONGER EXISTS. It reads presence announcements out
   of the Teams "Presence" channel in Mission Comms. Checked 2026-09-23: that
   channel's last message is 2026-04-24 and the whole team has been quiet since
   2026-06-21. The organisation moved absence into Markaz, where it is live:
   `work_from_home` is a leave type with 360 records (latest yesterday) and
   there were 8 genuine approved absences today. So this reads Markaz, not
   Teams, which is both simpler and current.

🔴 WE CANNOT SEE PRESENCE, ONLY RECORDED ABSENCE. The old report inferred who
   was "onsite" from who had not announced otherwise, and flagged the rest as
   "silent cases". A leave system cannot tell us somebody walked into the
   office. So the headline category is NO_ABSENCE_RECORDED, never "onsite" or
   "present". The wording is the honest claim and it is not decoration: a
   number labelled "onsite" would be read as attendance and it is not.

   That also removes three of the template's seven stat boxes -- "WFH
   Confirmed", "Additional" and "Flagged" only existed because a Teams
   announcement had to be chased and confirmed. An approved WFH request in
   Markaz is already confirmed.

🔴 FOUR LEAVE RECORDS HAVE IMPOSSIBLE DATES. A plain `CURRENT_DATE BETWEEN
   start_date AND end_date` counts those people as absent FOR EVER -- on
   2026-09-23 it reported 10 absences when the true number was 8, a 20% error
   that would have recurred silently every day. Live on 2026-09-24:

     Bushra        annual          start year **0026**
     Bushra        work_from_home  end date **42026-02-01**
     Fatima Khan   work_from_home  start year **2016**
     Moiz Khan     annual          end date **20226-01-02**

   Note that a SQL check on `EXTRACT(YEAR ...)` finds only the two Postgres can
   still parse; checking the date STRING finds all four. They are excluded from
   the counts AND listed for correction, never quietly dropped, because
   somebody has to fix them in Markaz or tomorrow's report is wrong too.
"""

from __future__ import annotations

import datetime as dt
from typing import Iterable, Optional

# The I-10 head office payroll. NIETE Islamabad and NIETE Balochistan are
# separate sites and are not part of this report by default; the caller may ask
# for them explicitly.
I10_ENTITIES = ("OPL", "OWT")

#: Leave types that mean "working, but not from the office".
WFH_TYPES = ("work_from_home",)

#: Nobody is on leave for longer than this. Beyond it the record is a data
#: entry error, not a very long absence. The longest genuine approved leave in
#: the table is a 3-month medical absence, so 180 days is generous.
MAX_PLAUSIBLE_LEAVE_DAYS = 180

#: A year outside this range is a typo, not a date.
MIN_PLAUSIBLE_YEAR = 2020
MAX_PLAUSIBLE_YEAR = 2030

# Categories. NOT the template's seven -- see the module docstring.
ON_LEAVE = "on_leave"
WORKING_FROM_HOME = "working_from_home"
NO_ABSENCE_RECORDED = "no_absence_recorded"
NEEDS_CORRECTION = "needs_correction"

CATEGORIES = (NO_ABSENCE_RECORDED, ON_LEAVE, WORKING_FROM_HOME, NEEDS_CORRECTION)

#: Colours from the locked template, kept for the categories that survived.
CATEGORY_COLOURS = {
    NO_ABSENCE_RECORDED: "#e8f5e9",   # light green, was "Onsite Today"
    ON_LEAVE: "#ffe0b2",              # light orange
    WORKING_FROM_HOME: "#e3f2fd",     # light blue
    NEEDS_CORRECTION: "#ffebee",      # light red, was "Flagged"
}


class AttendanceError(ValueError):
    """The attendance data does not make sense."""


def _as_date(value) -> Optional[dt.date]:
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    text = str(value)[:10]
    try:
        return dt.date.fromisoformat(text)
    except ValueError:
        # An end date of "42026-02-01" does not parse, and must not be treated
        # as a missing date (which would read as open-ended leave).
        return None


def date_is_implausible(start, end) -> Optional[str]:
    """Why this leave record cannot be trusted, or None if it is fine.

    Returns a reason a person can act on, because these rows need correcting in
    Markaz by a human -- suppressing them silently would leave the same two
    people wrong in tomorrow's report too.
    """
    raw_start, raw_end = str(start)[:10], str(end)[:10]
    s, e = _as_date(start), _as_date(end)

    if s is None:
        return f"start date is not a real date ({raw_start})"
    if e is None:
        return f"end date is not a real date ({raw_end})"
    for label, d, raw in (("start", s, raw_start), ("end", e, raw_end)):
        if not MIN_PLAUSIBLE_YEAR <= d.year <= MAX_PLAUSIBLE_YEAR:
            return f"{label} date year {d.year} is not a real year ({raw})"
    if e < s:
        return f"ends ({e}) before it starts ({s})"
    if (e - s).days > MAX_PLAUSIBLE_LEAVE_DAYS:
        return f"spans {(e - s).days} days, longer than any real leave"
    return None


def covers(start, end, on: dt.date) -> bool:
    """True if a PLAUSIBLE leave record covers `on`. An implausible one never
    covers anything -- that is the whole point of the guard."""
    if date_is_implausible(start, end):
        return False
    return _as_date(start) <= on <= _as_date(end)


def categorise(leave_type: Optional[str]) -> str:
    return WORKING_FROM_HOME if (leave_type or "") in WFH_TYPES else ON_LEAVE


def build_report(
    *,
    on: dt.date,
    payroll: Iterable[dt.date],
    leave_rows: Iterable[dict],
    entities: tuple[str, ...] = I10_ENTITIES,
) -> dict:
    """Assemble one day's attendance.

    `payroll` is the head-office roster (one row per person, with `user_id`,
    `name`, `payroll_entity`, `department`). `leave_rows` are APPROVED leave
    requests that might touch `on`.

    Everything is counted from the roster, so a leave record belonging to
    somebody who is not on this office's payroll cannot inflate the numbers.
    """
    roster = {p["user_id"]: p for p in payroll if p.get("payroll_entity") in entities}

    absent: dict[int, dict] = {}
    corrections: list[dict] = []

    for row in leave_rows:
        reason = date_is_implausible(row.get("start_date"), row.get("end_date"))
        if reason:
            # Flagged whether or not they are on this roster: a broken record is
            # worth fixing wherever it sits.
            corrections.append({
                "user_id": row.get("user_id"),
                "name": row.get("name"),
                "leave_type": row.get("leave_type"),
                # NOT truncated to 10 characters like the valid rows below.
                # These are the exact values somebody has to go and correct in
                # Markaz, and "42026-02-01" trimmed to "42026-02-0" sends them
                # looking for the wrong thing.
                "start_date": str(row.get("start_date")),
                "end_date": str(row.get("end_date")),
                "problem": reason,
            })
            continue

        uid = row.get("user_id")
        if uid not in roster or not covers(row["start_date"], row["end_date"], on):
            continue
        # One person, one absence. A half day and a full day on the same date
        # is still one person away.
        if uid not in absent:
            absent[uid] = {
                **roster[uid],
                "category": categorise(row.get("leave_type")),
                "leave_type": row.get("leave_type"),
                "sub_category": row.get("sub_category"),
                "start_date": str(row["start_date"])[:10],
                "end_date": str(row["end_date"])[:10],
                "is_half_day": bool(row.get("is_half_day")),
            }

    on_leave = sorted((p for p in absent.values() if p["category"] == ON_LEAVE),
                      key=lambda p: (p.get("payroll_entity") or "", p.get("name") or ""))
    wfh = sorted((p for p in absent.values() if p["category"] == WORKING_FROM_HOME),
                 key=lambda p: (p.get("payroll_entity") or "", p.get("name") or ""))

    total = len(roster)
    return {
        "date": on.isoformat(),
        "weekday": on.strftime("%A"),
        "entities": list(entities),
        "total_on_payroll": total,
        "on_leave": on_leave,
        "working_from_home": wfh,
        "no_absence_recorded": total - len(on_leave) - len(wfh),
        "needs_correction": sorted(corrections, key=lambda c: str(c.get("name") or "")),
        # Said in full on every response so no reader has to remember it.
        "presence_caveat": (
            "Markaz records absence, not attendance. "
            f"{total - len(on_leave) - len(wfh)} people have no absence recorded "
            "for this date, which is not the same as being seen in the office."
        ),
    }


def stat_boxes(report: dict) -> list[dict]:
    """The stat boxes, in the locked colours, for the categories that survive.

    They MUST sum to the payroll total, which is the check the CV-screening SOP
    calls out by name and which the old attendance template also required.
    `needs_correction` is deliberately outside that sum: it counts broken
    records, not people, and one person can own more than one.
    """
    boxes = [
        {"label": "On payroll", "value": report["total_on_payroll"], "colour": "#f5f5f5"},
        {"label": "No absence recorded", "value": report["no_absence_recorded"],
         "colour": CATEGORY_COLOURS[NO_ABSENCE_RECORDED]},
        {"label": "On leave", "value": len(report["on_leave"]),
         "colour": CATEGORY_COLOURS[ON_LEAVE]},
        {"label": "Working from home", "value": len(report["working_from_home"]),
         "colour": CATEGORY_COLOURS[WORKING_FROM_HOME]},
    ]
    if report["needs_correction"]:
        boxes.append({"label": "Records to fix", "value": len(report["needs_correction"]),
                      "colour": CATEGORY_COLOURS[NEEDS_CORRECTION]})
    return boxes


def boxes_balance(report: dict) -> bool:
    """The three people-categories must account for everyone on the payroll."""
    return (
        report["no_absence_recorded"]
        + len(report["on_leave"])
        + len(report["working_from_home"])
    ) == report["total_on_payroll"]
