"""Candidate invites: the seven types, and the gates that stop a bad send.

SOURCE OF TRUTH: .claude/skills/06_candidate-invites/SKILL.md and
memory/locked_email_template_interview_invites_FINAL_2026_05_13.md.

The DESIGN is locked and lives in the template. This module owns the rules
about WHO an invite may go to, WHAT may be in its subject, and WHETHER its
booking link has been proven to point at the right thing.

🔴 THE THREE WAYS AN INVITE GOES WRONG, EACH NOW MECHANICAL:

  1. A PILOT THAT REACHES A CANDIDATE. A pilot goes to Ayesha and nobody else,
     with no CC at all (CLAUDE.md Rule 4). `recipients_for` will not build any
     other list for a pilot, and `check_before_send` refuses one.

  2. "[PILOT - ]" LEFT IN A LIVE SUBJECT (CLAUDE.md Rule 7). Refused, because
     the candidate sees the subject line before anything else.

  3. THE WRONG BOOKING LINK. Growth Manager runs as TWO live roles -- Job 39
     Lahore and Job 41 Karachi -- with separate schedules, and
     `scripts/jobs/job39/send_growth_manager_invites_batch.py` sits in the
     job39 folder carrying Job 41 constants. Copying it would silently book a
     Lahore candidate into the Karachi schedule (CLAUDE.md Rule 24). A link is
     therefore not trusted because of where it was found: it is FETCHED, its
     page title read, and a live send refuses until that has happened.

⚠️ The Layer 3 send-time hook is wired but inert (it matches on `tool_name`,
   always literally "Bash"), so nothing outside this module is checking. These
   gates are the only ones that actually run.
"""

from __future__ import annotations

import re
from typing import Optional

# --------------------------------------------------------------------------
# The seven types
# --------------------------------------------------------------------------

VALUES_INTERVIEW = "values_interview"
CASE_STUDY_DEBRIEF = "case_study_debrief"
EXPLORATORY_CALL = "exploratory_call"
WARM_BENCH_OPPORTUNITY = "warm_bench_opportunity"
KEEP_IN_TOUCH = "keep_in_touch"
INTERVIEW_REMINDER = "interview_reminder"
ASSESSMENT_CENTER = "assessment_center"

#: `booking` -- a booking link is required and must be verified before a live
#: send. `reply` -- the candidate replies to confirm; a booking link is wrong
#: for this type. `none` -- no call to arrange at all.
INVITE_TYPES = {
    VALUES_INTERVIEW: {
        "label": "Values Interview Invite",
        "confirm": "booking",
        "note": "Candidate passed screening and is moving to the values round.",
    },
    CASE_STUDY_DEBRIEF: {
        "label": "Case Study Debrief Invite",
        "confirm": "booking",
        "note": "They submitted a case study and it is time to discuss it.",
    },
    EXPLORATORY_CALL: {
        "label": "Exploratory Call Invite",
        "confirm": "booking",
        "note": "An early conversation with no role decision attached.",
    },
    WARM_BENCH_OPPORTUNITY: {
        "label": "Warm Bench Opportunity Invite",
        "confirm": "booking",
        "note": "Somebody held warm for a role that has now opened.",
    },
    KEEP_IN_TOUCH: {
        "label": "Keep-in-Touch Note",
        "confirm": "none",
        # memory/keep_in_touch_note_type_2026_06_19.md
        "note": "Post-conversation warm hold. NO booking button, no promise, "
                "no date.",
    },
    INTERVIEW_REMINDER: {
        "label": "Interview Reminder",
        "confirm": "none",
        # memory/interview_reminder_note_type_2026_07_23.md
        "note": "Day-before nudge for an ALREADY BOOKED interview. Verified "
                "calendar or Gmail data only, never a remembered time.",
    },
    ASSESSMENT_CENTER: {
        "label": "Assessment Center Activity Invite",
        "confirm": "reply",
        # memory/assessment_center_invite_type_2026_07_31.md
        "note": "Onsite full day. Reply to confirm, NO booking link. Venue and "
                "a Maps link only as Ayesha provides them.",
    },
}

#: Every pilot goes here and nowhere else.
PILOT_RECIPIENT = "ayesha.khan@taleemabad.com"

#: The marker a pilot subject may carry and a live subject may never.
PILOT_PREFIX = "[PILOT"
_PILOT_PATTERN = re.compile(r"\[\s*pilot\b", re.I)


class InviteError(ValueError):
    """The invite cannot be sent as configured."""


def requires_booking_link(invite_type: str) -> bool:
    return INVITE_TYPES[invite_type]["confirm"] == "booking"


def forbids_booking_link(invite_type: str) -> bool:
    """Two types are actively wrong with a booking button on them.

    The assessment centre is a full onsite day confirmed by reply, and a
    keep-in-touch note must not imply there is something to book.
    """
    return INVITE_TYPES[invite_type]["confirm"] in ("reply", "none")


def subject_has_pilot_marker(subject: Optional[str]) -> bool:
    return bool(_PILOT_PATTERN.search(subject or ""))


def recipients_for(
    *, live: bool, candidate_email: Optional[str], cc: Optional[list[str]] = None
) -> dict:
    """Who this actually goes to.

    A pilot has ONE recipient and no CC, whatever was configured. That is not a
    filter applied to the live list, it is a different list built from nothing,
    so a CC cannot leak through by being forgotten.
    """
    if not live:
        return {"to": [PILOT_RECIPIENT], "cc": []}
    if not (candidate_email or "").strip():
        raise InviteError("a live invite needs the candidate's email address")
    return {"to": [candidate_email.strip()], "cc": list(cc or [])}


def check_before_send(
    *,
    invite_type: str,
    live: bool,
    subject: str,
    candidate_email: Optional[str],
    booking_url: Optional[str] = None,
    booking_verified_title: Optional[str] = None,
    cc: Optional[list[str]] = None,
) -> list[str]:
    """Every reason this send must not happen. Empty means it may.

    Returns ALL of them rather than the first, so a caller fixes the send once
    instead of discovering problems one at a time.
    """
    problems: list[str] = []

    if invite_type not in INVITE_TYPES:
        raise InviteError(f"unknown invite type {invite_type!r}")
    spec = INVITE_TYPES[invite_type]

    if not (subject or "").strip():
        problems.append("the subject line is empty")

    # Rule 7. The candidate reads the subject before anything else.
    if live and subject_has_pilot_marker(subject):
        problems.append(
            'the subject still carries a "[PILOT" marker, which must never '
            "reach a candidate"
        )
    # A pilot without the marker is allowed -- a threaded pilot must not carry
    # it, because the prefix breaks threading -- so its absence is not an error.

    if live and not (candidate_email or "").strip():
        problems.append("no candidate email address")

    # Rule 4. A pilot is to Ayesha, alone.
    if not live and cc:
        problems.append(
            "a pilot has no CC. It goes to Ayesha and nobody else, so a "
            "candidate cannot receive a draft."
        )

    if spec["confirm"] == "booking":
        if not (booking_url or "").strip():
            problems.append(
                f"{spec['label']} needs a booking link and none is configured"
            )
        elif live and not (booking_verified_title or "").strip():
            # Rule 24. A link is not trusted because of where it was found.
            problems.append(
                "the booking link has not been verified. Fetch it and read its "
                "page title before sending: Growth Manager runs as two roles "
                "with separate schedules, and a link taken from the wrong place "
                "books the candidate into the wrong city."
            )
    elif booking_url and (booking_url or "").strip():
        problems.append(
            f"{spec['label']} must not carry a booking link "
            f"({'the candidate replies to confirm' if spec['confirm'] == 'reply' else 'there is nothing to book'})"
        )

    return problems


# --------------------------------------------------------------------------
# Proving a booking link points where it should
# --------------------------------------------------------------------------

_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def title_of(html: str) -> Optional[str]:
    """The page title, whitespace-collapsed."""
    match = _TITLE.search(html or "")
    if not match:
        return None
    return " ".join(match.group(1).split()) or None


def title_mentions(title: Optional[str], expected: str) -> bool:
    """Whether a verified page title actually matches the role expected.

    Compared on lowercased, whitespace-collapsed text with punctuation
    dropped, because Markaz and Google titles differ in dashes and double
    spaces where the words are the same.
    """
    def norm(s: str) -> str:
        return " ".join(re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower()).split())

    t, e = norm(title), norm(expected)
    if not t or not e:
        return False
    # Every significant word of the expectation must appear in the title.
    words = [w for w in e.split() if len(w) > 2]
    return bool(words) and all(w in t for w in words)
