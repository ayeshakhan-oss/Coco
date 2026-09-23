"""The hiring funnel for one position: how many reached each stage.

SOURCE OF TRUTH: .claude/skills/03_operations/hiring-decision-brief.md, a
10-step SOP that counts shortlisted, values invites sent, bookings, completed
calls, pass/fail, case studies sent, debrief invites and debrief bookings.

🔴 THE SOP READS THE CALENDAR FOR BOOKINGS, AND THE CALENDAR IS GONE. The
   OAuth client behind the only token carrying a calendar scope was deleted, so
   it cannot refresh (memory, re-verified 2026-08-29). It turns out not to
   matter: the booking system emails a confirmation, and those land in the
   mailbox the app already syncs. Real subjects from `coco.comm_evidence`:

     "Appointment booked: Zero In Call For Senior Growth Manager (Name) @ ..."
     "Appointment booked: Case Study Debrief - Senior Manager Growth (Name) @ ..."
     "Lets proceed with the Case Study for Senior Manager Growth - Name"

   So bookings are visible without the Calendar at all.

🔴 EVERY GMAIL-DERIVED COUNT IS A FLOOR, NEVER A TOTAL, for two reasons that
   both had to be measured rather than assumed:

     1. `comm_evidence` holds ONE ROW PER APPLICATION (a unique constraint) and
        keeps only the most recent matching message. A candidate who was
        invited, booked and then rejected shows only the rejection.
     2. Classification is subject matching. A reworded subject is invisible to
        it, and Markaz's own subjects carry double spaces (CLAUDE.md Rule 18).

   So the funnel reports "at least N" and names its source per stage. A count
   that cannot be established is None, which the page renders as "not visible"
   -- never 0, which would read as "nobody".
"""

from __future__ import annotations

import re
from typing import Iterable, Optional

# Stages in funnel order.
SHORTLISTED = "shortlisted"
VALUES_BOOKED = "values_booked"
VALUES_DONE = "values_done"
VALUES_PASSED = "values_passed"
CASE_STUDY_SENT = "case_study_sent"
CASE_STUDY_SUBMITTED = "case_study_submitted"
DEBRIEF_BOOKED = "debrief_booked"
OUTCOME_SENT = "outcome_sent"

STAGE_TITLES = {
    SHORTLISTED: "Shortlisted from CV screening",
    VALUES_BOOKED: "Values interview booked",
    VALUES_DONE: "Values interview held",
    VALUES_PASSED: "Cleared the values interview",
    CASE_STUDY_SENT: "Case study sent",
    CASE_STUDY_SUBMITTED: "Case study submitted",
    DEBRIEF_BOOKED: "Case study debrief booked",
    OUTCOME_SENT: "Outcome communicated",
}
STAGES = tuple(STAGE_TITLES)

# Where each number comes from, shown next to it so a reader knows how much to
# trust it. Markaz is authoritative; Gmail is a floor.
MARKAZ = "Markaz"
GMAIL = "Gmail (at least)"
UNAVAILABLE = "not visible"

# Patterns derived from the 1,210 real subjects in coco.comm_evidence on
# 2026-09-24, not invented. Matched against a whitespace-normalised,
# lowercased subject, because Markaz subjects carry double spaces.
_BOOKED_VALUES = re.compile(r"appointment booked:.*\bzero.?in call\b")
_BOOKED_DEBRIEF = re.compile(r"appointment booked:.*\b(case study )?debrief\b")
_CASE_STUDY_SENT = re.compile(r"\b(let'?s |lets )?proceed with the case study\b")
_OUTCOME = re.compile(
    r"\b(application update|update on (your )?application"
    r"|your application for|application outcome|offer letter"
    r"|application - |application update)\b"
)


def normalise(subject: Optional[str]) -> str:
    """Lowercased, whitespace-collapsed. Markaz subjects carry double spaces
    ("Growth  Manager"), which defeat a plain substring test."""
    return " ".join((subject or "").split()).lower()


def classify_subject(subject: Optional[str]) -> Optional[str]:
    """Which stage this email is evidence of, or None.

    Order matters: an "Appointment booked" for a debrief also contains the
    words "case study", so the booking patterns are tested first.
    """
    s = normalise(subject)
    if not s:
        return None
    if _BOOKED_DEBRIEF.search(s):
        return DEBRIEF_BOOKED
    if _BOOKED_VALUES.search(s):
        return VALUES_BOOKED
    if _CASE_STUDY_SENT.search(s):
        return CASE_STUDY_SENT
    if _OUTCOME.search(s):
        return OUTCOME_SENT
    return None


def build_funnel(
    *,
    job: dict,
    rows: Iterable[dict],
    evidence_synced_at: Optional[str] = None,
) -> dict:
    """Counts per stage, each with its source and whether it is a floor."""
    rows = list(rows)

    from_gmail: dict[str, set[int]] = {s: set() for s in STAGES}
    for r in rows:
        stage = classify_subject(r.get("matched_subject"))
        if stage:
            from_gmail[stage].add(r["application_id"])

    shortlisted = sum(
        1 for r in rows
        if (r.get("status") or "") in ("shortlisted", "case_study_sent", "hired", "offer")
        or r.get("values_interview_result") or r.get("proceed")
    )
    values_done = sum(1 for r in rows if r.get("proceed") or r.get("values_interview_result"))
    values_passed = sum(
        1 for r in rows
        if (r.get("proceed") or "").strip().lower() == "yes"
        or (r.get("values_interview_result") or "").strip().lower() in ("pass", "strong_pass")
    )
    submitted = sum(
        1 for r in rows
        if (r.get("case_study_status") or "").strip()
        or (r.get("case_study_submission") or "").strip()
    )

    def stage(key, count, source, floor=False, note=None):
        return {
            "key": key, "title": STAGE_TITLES[key], "count": count,
            "source": source, "is_floor": floor, "note": note,
        }

    stages = [
        stage(SHORTLISTED, shortlisted, MARKAZ),
        stage(VALUES_BOOKED, len(from_gmail[VALUES_BOOKED]) or None, GMAIL, floor=True,
              note="from booking confirmation emails"),
        stage(VALUES_DONE, values_done, MARKAZ,
              note="a scorecard exists, so the call happened"),
        stage(VALUES_PASSED, values_passed, MARKAZ),
        stage(CASE_STUDY_SENT, len(from_gmail[CASE_STUDY_SENT]) or None, GMAIL, floor=True),
        stage(CASE_STUDY_SUBMITTED, submitted, MARKAZ),
        stage(DEBRIEF_BOOKED, len(from_gmail[DEBRIEF_BOOKED]) or None, GMAIL, floor=True,
              note="from booking confirmation emails"),
        stage(OUTCOME_SENT, len(from_gmail[OUTCOME_SENT]) or None, GMAIL, floor=True),
    ]
    for s in stages:
        if s["count"] is None:
            s["source"] = UNAVAILABLE
            s["note"] = (
                "no matching email found. That means none was recognised, not "
                "that none was sent."
            )

    return {
        "job_id": job.get("job_pk") or job.get("id"),
        "job_title": job.get("title"),
        "total_applications": len(rows),
        "stages": stages,
        "evidence_synced_at": evidence_synced_at,
        "caveat": (
            "Markaz counts are exact. Gmail counts are a floor: the evidence "
            "table keeps one message per candidate, so somebody invited, booked "
            "and later rejected shows only the rejection, and a reworded "
            "subject line is invisible to the matching."
        ),
    }


def narrows_monotonically(funnel: dict) -> list[str]:
    """Stages where the count went UP from the stage before it.

    A funnel should narrow. Where it widens, one of the two numbers is wrong or
    the two are measuring different things, and that is worth showing rather
    than leaving for a reader to spot. Gmail floors are skipped, because a
    floor rising above an exact count says nothing.
    """
    problems, previous, previous_title = [], None, None
    for s in funnel["stages"]:
        if s["count"] is None or s["is_floor"]:
            continue
        if previous is not None and s["count"] > previous:
            problems.append(
                f"{s['title']} ({s['count']}) is higher than "
                f"{previous_title} ({previous})"
            )
        previous, previous_title = s["count"], s["title"]
    return problems
