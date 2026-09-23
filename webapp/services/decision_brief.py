"""Assemble a decision brief for one position.

SOURCE OF TRUTH: .claude/skills/03_operations/decision-briefs.md -- four parts
(header and stat boxes, leading candidates, pipeline summary in five groups,
debrief schedule), four exact verdict labels, and every candidate name linked to
their CV.

🔴 THE BRIEF'S CORE EVIDENCE IS NOT ALL IN MARKAZ, AND THE GAPS MUST SHOW.
   Measured on Job 42 (Senior Manager Growth, 185 applicants) on 2026-09-24:

     values_interview_result   18 recorded
     values_scorecard          18 recorded, with proceedToRightSeat
     case_study_status         17 recorded
     case_study_score           0 recorded
     gwc_interview_result       0 recorded
     gwc_interview_date         0 recorded

   Case-study scores and debrief verdicts are simply not written down anywhere
   machine-readable; they live in Ayesha's head, her mailbox, and the reports
   she has sent. CLAUDE.md Rule 18 is the same lesson from the other side:
   "Not Started" in Markaz means NO RECORD, never NO EVENT.

   So this module never converts an empty field into a finding. A candidate
   with no debrief record is NOT_RECORDED, which is a statement about our
   records, and never OVERDUE, which is a statement about them. The SOP's
   OVERDUE label is still produced, but only where there is a date to be late
   against.

🔴 EVERY NAME LINKS TO A CV, and the link is served by this app out of Markaz
   (`GET /api/candidates/{id}/cv`) rather than requiring a manual upload to
   Drive first. It sits behind the same Google sign-in as everything else.
"""

from __future__ import annotations

import datetime as dt
from typing import Iterable, Optional

# The SOP's four labels, exactly. Plus one it does not have and needs.
PANEL_DECISION = "PANEL DECISION"
DEBRIEF_CONFIRMED = "DEBRIEF CONFIRMED"
DEBRIEF_SCHEDULED = "DEBRIEF SCHEDULED"
OVERDUE = "OVERDUE"
#: 🔴 NOT in the SOP, and required. Markaz records no debrief for anybody, and
#: calling that OVERDUE would assert a delay we cannot see. This says what is
#: true: there is no record.
NOT_RECORDED = "NO DEBRIEF RECORDED"

VERDICT_LABELS = (
    PANEL_DECISION, DEBRIEF_CONFIRMED, DEBRIEF_SCHEDULED, OVERDUE, NOT_RECORDED,
)

# The five pipeline groups, in the SOP's order.
VALUES_PASS_PENDING = "values_pass_debrief_pending"
VALUES_OUT = "values_out"
CASE_STUDY_OUT = "case_study_out"
AWAITING_SUBMISSION = "awaiting_submission"
NOT_INTERVIEWED = "not_interviewed"

GROUP_TITLES = {
    VALUES_PASS_PENDING: "Values pass, debrief pending",
    VALUES_OUT: "Values interview not passed",
    CASE_STUDY_OUT: "Did not advance after the case study",
    AWAITING_SUBMISSION: "Case study sent, nothing submitted yet",
    NOT_INTERVIEWED: "Not interviewed",
}
GROUPS = tuple(GROUP_TITLES)


class DecisionBriefError(ValueError):
    """The brief cannot be assembled from what is on record."""


def cv_url(application_id: int) -> str:
    """Where a candidate's name points. Served by this app from Markaz, so no
    manual Drive upload stands between a brief and a working link."""
    return f"/api/candidates/{application_id}/cv"


def _passed_values(row: dict) -> Optional[bool]:
    """True, False, or None for "no values interview on record".

    Two sources and they can disagree: the `values_interview_result` column and
    `proceedToRightSeat` inside the scorecard JSON. The SCORECARD wins, because
    it is what the interviewer actually filled in, and a disagreement is
    surfaced rather than silently resolved.
    """
    proceed = (row.get("proceed") or "").strip().lower()
    if proceed in ("yes", "no"):
        return proceed == "yes"
    result = (row.get("values_interview_result") or "").strip().lower()
    if result in ("pass", "strong_pass"):
        return True
    if result == "fail":
        return False
    return None


def values_disagreement(row: dict) -> Optional[str]:
    """The column and the scorecard saying different things is worth showing."""
    proceed = (row.get("proceed") or "").strip().lower()
    result = (row.get("values_interview_result") or "").strip().lower()
    if not proceed or not result:
        return None
    from_card = proceed == "yes"
    from_column = result in ("pass", "strong_pass")
    if from_card != from_column:
        return (
            f"the scorecard says proceed={proceed!r} but the status column says "
            f"{result!r}; the scorecard is used"
        )
    return None


def debrief_verdict(row: dict, *, today: Optional[dt.date] = None) -> str:
    """One of the SOP's labels, or NOT_RECORDED.

    Never OVERDUE on an absence. A candidate is only late if there is a date to
    be late against.
    """
    today = today or dt.date.today()
    result = (row.get("gwc_interview_result") or "").strip().lower()
    if result in ("pass", "strong_pass", "fail"):
        return DEBRIEF_CONFIRMED

    raw = row.get("gwc_interview_date")
    if raw:
        when = str(raw)[:10]
        try:
            booked = dt.date.fromisoformat(when)
        except ValueError:
            return NOT_RECORDED
        return OVERDUE if booked < today else DEBRIEF_SCHEDULED

    return NOT_RECORDED


def _submitted_case_study(row: dict) -> bool:
    return bool(
        (row.get("case_study_status") or "").strip()
        or (row.get("case_study_submission") or "").strip()
        or (row.get("case_study_word_file") or "").strip()
    )


def group_for(row: dict) -> str:
    """Which of the SOP's five pipeline groups this candidate belongs in."""
    passed = _passed_values(row)

    if passed is False:
        return VALUES_OUT
    if passed is True:
        return VALUES_PASS_PENDING
    # No values interview on record from here down.
    if _submitted_case_study(row):
        return CASE_STUDY_OUT
    if (row.get("status") or "") in ("shortlisted", "case_study_sent"):
        return AWAITING_SUBMISSION
    return NOT_INTERVIEWED


def build_brief(
    *,
    job: dict,
    rows: Iterable[dict],
    today: Optional[dt.date] = None,
) -> dict:
    """The four parts, from whatever is genuinely on record."""
    today = today or dt.date.today()
    rows = list(rows)
    if not rows:
        raise DecisionBriefError(
            f"no applications on {job.get('title') or 'this job'}, so there is "
            "nothing to brief on"
        )

    people, groups = [], {g: [] for g in GROUPS}
    for r in rows:
        person = {
            "application_id": r["application_id"],
            "name": r.get("name") or "(no name on record)",
            "cv_url": cv_url(r["application_id"]),
            "has_cv": bool(r.get("has_cv")),
            "status": r.get("status"),
            "passed_values": _passed_values(r),
            "values_disagreement": values_disagreement(r),
            "values_comments": (r.get("final_comments") or "").strip() or None,
            "submitted_case_study": _submitted_case_study(r),
            "case_study_band": r.get("case_study_band"),
            "case_study_total": r.get("case_study_total"),
            "cv_screen_tier": r.get("cv_screen_tier"),
            "cv_screen_match": r.get("cv_screen_match"),
            "debrief_verdict": debrief_verdict(r, today=today),
            "debrief_date": str(r["gwc_interview_date"])[:10] if r.get("gwc_interview_date") else None,
            "group": group_for(r),
        }
        people.append(person)
        groups[person["group"]].append(person)

    # Leading candidates: passed values AND submitted a case study. Ordered by
    # the case-study total where we have one, then the CV screen. Deliberately
    # NOT a cut-off -- the SOP asks for the strongest recommendations, and a
    # position with three good candidates should show three.
    leading = sorted(
        (p for p in people
         if p["passed_values"] is True and p["submitted_case_study"]),
        key=lambda p: (-(p["case_study_total"] or 0), -(p["cv_screen_match"] or 0)),
    )

    # If nothing can separate them, say so rather than let the order read as a
    # ranking. On Job 42 all 17 leading candidates have no case-study score and
    # no CV screen, so the list is a set, not an order.
    rankable = sum(
        1 for p in leading
        if p["case_study_total"] is not None or p["cv_screen_match"] is not None
    )
    if leading and rankable == 0:
        leading_note = (
            f"These {len(leading)} are not ranked. Nobody here has a case-study "
            "score or a CV screen on record, so there is nothing to order them "
            "by. Scoring the case studies would sharpen this section."
        )
    elif leading and rankable < len(leading):
        leading_note = (
            f"{len(leading) - rankable} of these {len(leading)} have no score on "
            "record and sit at the bottom of the order for that reason, not on merit."
        )
    else:
        leading_note = None

    interviewed = [p for p in people if p["passed_values"] is not None]
    missing_cv = [p for p in people if not p["has_cv"]]

    return {
        "job_id": job.get("job_pk") or job.get("id"),
        "job_title": job.get("title"),
        "generated_on": today.isoformat(),
        "total_applications": len(people),
        "values_interviews": len(interviewed),
        "shortlisted": sum(1 for p in people if (p["status"] or "") == "shortlisted"),
        "leading": leading,
        "leading_note": leading_note,
        "groups": [
            {"key": g, "title": GROUP_TITLES[g], "people": groups[g]} for g in GROUPS
        ],
        "debrief_schedule": sorted(
            (p for p in people if p["debrief_date"]),
            key=lambda p: p["debrief_date"] or "",
        ),
        # Said out loud rather than left for a reader to infer from blanks.
        "not_recorded": {
            "debrief_verdicts": sum(
                1 for p in people if p["debrief_verdict"] == NOT_RECORDED
            ),
            "case_study_scores": sum(
                1 for p in people if p["submitted_case_study"] and p["case_study_total"] is None
            ),
            "missing_cv": len(missing_cv),
        },
        "evidence_caveat": (
            "Case-study scores and debrief verdicts are not recorded in Markaz. "
            "Where this brief says a debrief is not recorded, that is a "
            "statement about our records and not about the candidate."
        ),
    }


def stat_boxes(brief: dict) -> list[dict]:
    """The SOP's four boxes, in its colours."""
    return [
        {"label": "Applications", "value": brief["total_applications"], "colour": "#fdecea"},
        {"label": "Values interviews", "value": brief["values_interviews"], "colour": "#e3f2fd"},
        {"label": "Shortlisted", "value": brief["shortlisted"], "colour": "#fff3e0"},
        {"label": "Leading", "value": len(brief["leading"]), "colour": "#f5f5f5"},
    ]


def everyone_is_accounted_for(brief: dict) -> bool:
    """The five groups must contain every application exactly once. A brief
    that quietly loses a candidate is worse than no brief."""
    counted = sum(len(g["people"]) for g in brief["groups"])
    return counted == brief["total_applications"]
