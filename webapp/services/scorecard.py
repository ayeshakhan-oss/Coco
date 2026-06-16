"""Normalize the two scorecard JSON shapes stored in applications.

values_scorecard and gwc_scorecard have DIFFERENT shapes (confirmed against the
live DB):

  values_scorecard = {date, host, noteTaker, candidateName, finalComments,
                      proceedToRightSeat, values:[{name,rating,deepDive,
                      curveBall,microCase}]}

  gwc_scorecard    = {name, peer, hiringManager, finalMark, recordingLink,
                      additionalComments, getIt/wantIt/capacityToDoIt:
                      {question1..3}, competencies:[{name,score,weight}]}

These functions flatten both into snake_case views the API/UI can render
uniformly. They are pure (no DB), so they unit-test in isolation.
"""

from __future__ import annotations

from typing import Optional


def normalize_values_scorecard(data: Optional[dict]) -> Optional[dict]:
    if not data:
        return None
    values = []
    for v in data.get("values") or []:
        values.append(
            {
                "name": v.get("name", "") or "",
                "rating": v.get("rating", "") or "",
                "deep_dive": v.get("deepDive", "") or "",
                "curve_ball": v.get("curveBall", "") or "",
                "micro_case": v.get("microCase", "") or "",
            }
        )
    return {
        "kind": "values",
        "candidate_name": data.get("candidateName", "") or "",
        "host": data.get("host", "") or "",
        "note_taker": data.get("noteTaker", "") or "",
        "date": data.get("date", "") or "",
        "proceed_to_right_seat": data.get("proceedToRightSeat", "") or "",
        "final_comments": data.get("finalComments", "") or "",
        "values": values,
    }


def normalize_gwc_scorecard(data: Optional[dict]) -> Optional[dict]:
    if not data:
        return None
    comps = []
    for c in data.get("competencies") or []:
        comps.append(
            {
                "name": c.get("name", "") or "",
                "score": c.get("score"),
                "weight": c.get("weight"),
            }
        )
    return {
        "kind": "gwc",
        "candidate_name": data.get("name", "") or "",
        "hiring_manager": data.get("hiringManager", "") or "",
        "final_mark": data.get("finalMark", "") or "",
        "get_it": data.get("getIt", {}) or {},
        "want_it": data.get("wantIt", {}) or {},
        "capacity_to_do_it": data.get("capacityToDoIt", {}) or {},
        "competencies": comps,
        "recording_link": data.get("recordingLink", "") or "",
        "additional_comments": data.get("additionalComments", "") or "",
    }


def normalize_comm_history(arr: Optional[list]) -> list:
    """Flatten the applications.communication_history jsonb (Markaz platform's
    own email record) into a uniform list for the History view / dedupe context."""
    out = []
    for item in arr or []:
        if not isinstance(item, dict):
            continue
        out.append(
            {
                "sent_at": item.get("sentAt"),
                "sent_by": item.get("sentBy"),
                "status": item.get("status"),
                "subject": item.get("subject"),
                "template_name": item.get("templateName"),
                "recipient_email": item.get("recipientEmail"),
                "cc_emails": item.get("ccEmails", []) or [],
                "source": "markaz",
            }
        )
    return out
