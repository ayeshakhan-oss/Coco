"""Unit tests for the pure status-derivation functions in reads.py.

These encode the SAME precedence as the SQL `displayed` CTE. They are the
regression guard for the rule: a candidate is only ever "Sent" via an app-sent
comm, a Gmail `found` match, or a manual override — never from Markaz alone;
ambiguous Gmail evidence is always "Needs Review"; needs-comms + >7 days + no
evidence is "High Priority".

Run:  python -m pytest webapp/tests/test_status_derivation.py
"""

from __future__ import annotations

import itertools

from webapp.services.reads import (
    compute_comm_required,
    compute_is_high_priority,
    derive_display_status,
    infer_required_email_type,
)


# ── comm_required + email-type inference ─────────────────────────────────────

def test_comm_required_statuses():
    assert compute_comm_required("rejected") is True
    assert compute_comm_required("warm_bench") is True
    assert compute_comm_required("consider_other_roles") is True
    for s in ("new", "applied", "shortlisted", "offer", "hired", "P2", "gwc_scheduled", None):
        assert compute_comm_required(s) is False


def test_required_email_type_inference():
    # Rejected: gwc beats values beats CV-stage.
    assert infer_required_email_type("rejected", values_filled=True, gwc_filled=True) == "gwc_rejection"
    assert infer_required_email_type("rejected", values_filled=False, gwc_filled=True) == "gwc_rejection"
    assert infer_required_email_type("rejected", values_filled=True, gwc_filled=False) == "values_feedback"
    assert infer_required_email_type("rejected", values_filled=False, gwc_filled=False) == "cv_rejection"
    # Warm bench.
    assert infer_required_email_type("warm_bench", False, False) == "warm_bench"
    assert infer_required_email_type("consider_other_roles", False, False) == "warm_bench"
    # Not required -> None.
    assert infer_required_email_type("new", True, True) is None
    assert infer_required_email_type("shortlisted", False, False) is None


# ── derive_display_status precedence ─────────────────────────────────────────

def _d(**kw):
    base = dict(
        sent_count=0,
        active_count=0,
        gmail_status="not_checked",
        manual_marked=False,
        comm_required=False,
        is_high_priority=False,
    )
    base.update(kw)
    return derive_display_status(**base)


def test_app_sent_is_sent_regardless_of_everything():
    assert _d(sent_count=1) == "sent"
    # Sent wins even over uncertain gmail / high priority inputs.
    assert _d(sent_count=1, gmail_status="uncertain", comm_required=True, is_high_priority=True) == "sent"


def test_manual_override_is_sent():
    assert _d(manual_marked=True) == "sent"
    assert _d(manual_marked=True, comm_required=True, is_high_priority=True) == "sent"


def test_gmail_found_is_sent_only_when_comms_required():
    # External evidence = "Sent" ONLY for a candidate who needs a rejection/feedback.
    # For a not-yet-decided candidate a found email is an interview invite, so they
    # stay in their pipeline stage (default status -> awaiting_scorecard).
    assert _d(gmail_status="found", comm_required=True) == "sent"
    assert _d(gmail_status="found", comm_required=False) == "awaiting_scorecard"


def test_markaz_log_counts_as_sent_only_when_comms_required():
    # A logged Markaz communication is evidence of a rejection ONLY if one was due.
    assert _d(markaz_comms=2, comm_required=True, is_high_priority=True) == "sent"
    # Markaz log on a not-decided candidate is an invite -> NOT "sent".
    assert _d(markaz_comms=1, comm_required=False) == "awaiting_scorecard"
    # No Markaz log + comm required + no other evidence -> still needs comms.
    assert _d(markaz_comms=0, comm_required=True) == "needs_comms"


def test_gmail_uncertain_is_needs_review_only_when_comms_required():
    assert _d(gmail_status="uncertain", comm_required=True) == "needs_review"
    assert _d(gmail_status="uncertain", comm_required=True, is_high_priority=True) == "needs_review"
    # Ambiguous match on a not-decided candidate -> still their pipeline stage.
    assert _d(gmail_status="uncertain", comm_required=False) == "awaiting_scorecard"


def test_pipeline_stage_is_mirrored_from_markaz():
    # Not-yet-decided candidates show their Markaz stage, never "Sent" (an invite
    # in Gmail/Markaz must not flip them to Sent).
    assert _d(status="shortlisted") == "shortlisted"
    assert _d(status="shortlisted", gmail_status="found") == "shortlisted"
    assert _d(status="shortlisted", markaz_comms=1) == "shortlisted"
    assert _d(status="gwc_scheduled") == "interview_scheduled"
    assert _d(status="case_study_sent") == "case_study"
    # But a real app-send/manual mark still wins (they truly were sent something).
    assert _d(status="shortlisted", sent_count=1) == "sent"


def test_in_progress():
    assert _d(active_count=1) == "in_progress"
    assert _d(active_count=2, comm_required=True, is_high_priority=True) == "in_progress"


def test_high_priority_and_needs_comms():
    assert _d(comm_required=True, is_high_priority=True) == "high_priority"
    assert _d(comm_required=True, is_high_priority=False) == "needs_comms"


def test_ignored_leaves_the_action_queues():
    # Ignored dismisses a candidate out of needs_comms / high_priority.
    assert _d(ignored=True, comm_required=True, is_high_priority=True) == 'ignored'
    assert _d(ignored=True, comm_required=True) == 'ignored'
    assert _d(ignored=True, gmail_status='uncertain', comm_required=True) == 'ignored'
    # A real app-send always wins over ignore (they WERE contacted).
    assert _d(ignored=True, sent_count=1) == 'sent'
    # Markaz/Gmail evidence beats ignore only when a rejection was actually due.
    assert _d(ignored=True, markaz_comms=1, comm_required=True) == 'sent'
    assert _d(ignored=True, markaz_comms=1, comm_required=False) == 'ignored'


def test_awaiting_scorecard_default():
    assert _d() == "awaiting_scorecard"
    assert _d(comm_required=False, is_high_priority=False) == "awaiting_scorecard"


def test_never_sent_from_markaz_alone():
    """comm_required (a Markaz signal) without any evidence is NEVER 'sent'."""
    for hp in (True, False):
        out = _d(comm_required=True, is_high_priority=hp)
        assert out in ("needs_comms", "high_priority")
        assert out != "sent"


def test_full_cross_product_is_valid_and_consistent():
    """Every combination yields a known status; 'sent' implies real evidence."""
    valid = {"sent", "needs_review", "in_progress", "high_priority", "needs_comms", "awaiting_scorecard"}
    for sent_count, active_count, gmail, manual, req, hp in itertools.product(
        (0, 1), (0, 1), ("not_checked", "none", "found", "uncertain"), (False, True), (False, True), (False, True)
    ):
        out = derive_display_status(
            sent_count=sent_count,
            active_count=active_count,
            gmail_status=gmail,
            manual_marked=manual,
            comm_required=req,
            is_high_priority=hp,
        )
        assert out in valid
        if out == "sent":
            assert sent_count > 0 or manual or gmail == "found"


# ── is_high_priority gating ──────────────────────────────────────────────────

def _hp(**kw):
    base = dict(
        comm_required=True,
        active_count=0,
        sent_count=0,
        manual_marked=False,
        gmail_status="not_checked",
        ignored=False,
        days_waiting=30,
    )
    base.update(kw)
    return compute_is_high_priority(**base)


def test_high_priority_requires_all_conditions():
    assert _hp() is True  # comm_required, no evidence, >7d, not ignored
    assert _hp(days_waiting=7) is False  # not strictly > 7
    assert _hp(days_waiting=8) is True
    assert _hp(comm_required=False) is False
    assert _hp(active_count=1) is False  # in progress
    assert _hp(sent_count=1) is False  # already sent
    assert _hp(manual_marked=True) is False  # manually marked
    assert _hp(gmail_status="found") is False  # has evidence
    assert _hp(gmail_status="uncertain") is False  # needs review, not high priority
    assert _hp(ignored=True) is False  # dismissed
    assert _hp(days_waiting=None) is False  # no clock
    assert _hp(markaz_comms=1) is False  # a Markaz email exists -> communicated
