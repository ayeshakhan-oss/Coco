"""Unit tests for the pure Gmail-matching helpers in gmail_evidence.py.

No network / no Google libs needed — these exercise classification logic only.

Run: python -m pytest webapp/tests/test_gmail_matching.py
"""

from __future__ import annotations

from webapp.services.gmail_evidence import (
    classify_candidate,
    message_recipients,
    norm_email,
    parse_header_addresses,
)


def _msg(to=None, cc=None, bcc=None, internal_ms=1000, mid="<x@taleemabad.com>",
         tid="t1", subject="Update on your application", snippet="Hi"):
    return {
        "to": [norm_email(x) for x in (to or [])],
        "cc": [norm_email(x) for x in (cc or [])],
        "bcc": [norm_email(x) for x in (bcc or [])],
        "internal_ms": internal_ms,
        "message_id": mid,
        "thread_id": tid,
        "subject": subject,
        "snippet": snippet,
    }


def test_parse_header_addresses():
    assert parse_header_addresses("Ali Khan <ali@x.com>, b@y.com") == ["ali@x.com", "b@y.com"]
    assert parse_header_addresses("  CAPS@X.COM ") == ["caps@x.com"]
    assert parse_header_addresses(None) == []
    assert parse_header_addresses("") == []


def test_message_recipients():
    r = message_recipients({"To": "a@x.com", "Cc": "b@y.com, c@z.com"})
    assert r["to"] == ["a@x.com"]
    assert r["cc"] == ["b@y.com", "c@z.com"]
    assert r["bcc"] == []


def test_direct_to_match_is_found():
    ev = classify_candidate("cand@x.com", [_msg(to=["cand@x.com"])], duplicate_email=False)
    assert ev["gmail_status"] == "found"
    assert ev["match_method"] == "recipient_window"
    assert ev["matched_message_id"] == "<x@taleemabad.com>"
    assert ev["gmail_thread_id"] == "t1"
    assert ev["uncertain_reason"] is None


def test_cc_only_match_is_uncertain():
    ev = classify_candidate("cand@x.com", [_msg(to=["other@x.com"], cc=["cand@x.com"])], duplicate_email=False)
    assert ev["gmail_status"] == "uncertain"
    assert "Cc/Bcc" in ev["uncertain_reason"]


def test_no_match_is_none():
    ev = classify_candidate("cand@x.com", [], duplicate_email=False)
    assert ev["gmail_status"] == "none"
    assert ev["matched_message_id"] is None


def test_duplicate_email_is_uncertain_even_with_direct_match():
    ev = classify_candidate("shared@x.com", [_msg(to=["shared@x.com"])], duplicate_email=True)
    assert ev["gmail_status"] == "uncertain"
    assert "shared" in ev["uncertain_reason"]


def test_empty_candidate_email_is_uncertain():
    ev = classify_candidate("", [_msg(to=["x@x.com"])], duplicate_email=False)
    assert ev["gmail_status"] == "uncertain"


def test_picks_most_recent_message():
    older = _msg(to=["cand@x.com"], internal_ms=1000, mid="<old@t.com>")
    newer = _msg(to=["cand@x.com"], internal_ms=5000, mid="<new@t.com>")
    ev = classify_candidate("cand@x.com", [older, newer], duplicate_email=False)
    assert ev["matched_message_id"] == "<new@t.com>"
    assert ev["internal_date"] is not None


def test_case_insensitive_match():
    ev = classify_candidate("Cand@X.com", [_msg(to=["cand@x.com"])], duplicate_email=False)
    assert ev["gmail_status"] == "found"
