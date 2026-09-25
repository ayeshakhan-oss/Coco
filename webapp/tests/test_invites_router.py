"""Who can reach the invite endpoints, and what happens at the send boundary.

Run: python -m pytest webapp/tests/test_invites_router.py -v

This router puts email in front of candidates, so "which role can send live"
has to be answered by the dependency tree FastAPI actually resolves, and the
send boundary has to be checked with a transport that records instead of
delivering.
"""

from __future__ import annotations

import pytest

from webapp import deps
from webapp.routers import invites as router_mod
from webapp.services import invite_render as rnd
from webapp.services import invites as inv
from webapp.services import sending


def _dependencies(path: str, method: str) -> set:
    """The dependency CALLABLES for a route, compared by identity.

    `require_editor` and `require_approver` are both closures produced by
    `deps._require_role` and both are named `dep`, so a name-based assertion
    would pass on either one.
    """
    for route in router_mod.router.routes:
        if getattr(route, "path", None) == path and method in (
            getattr(route, "methods", None) or set()
        ):
            return {d.call for d in route.dependant.dependencies if getattr(d, "call", None)}
    raise AssertionError(f"route not found: {method} {path}")


WRITE_ROUTES = [
    ("/api/invites/links", "POST"),
    ("/api/invites/links/{link_id}/verify", "POST"),
    ("/api/invites/send", "POST"),
]

READ_ROUTES = [
    ("/api/invites/types", "GET"),
    ("/api/invites/links", "GET"),
    ("/api/invites/sends", "GET"),
    ("/api/invites/preview", "POST"),
]


@pytest.mark.parametrize("path,method", WRITE_ROUTES)
def test_write_routes_require_at_least_an_editor(path, method):
    assert deps.require_editor in _dependencies(path, method), (
        f"{method} {path} changes what candidates receive and must be gated"
    )


@pytest.mark.parametrize("path,method", READ_ROUTES)
def test_read_routes_require_a_signed_in_user(path, method):
    found = _dependencies(path, method)
    assert deps.get_current_user in found or deps.require_editor in found


def test_the_gate_assertion_bites():
    """Without this, a bug in `_dependencies` would make every test above pass
    while checking nothing."""
    assert deps.require_editor not in _dependencies("/api/invites/types", "GET")


def test_a_live_send_is_gated_inside_the_handler_not_on_the_route():
    """One route serves both a pilot and a live send, because a pilot must
    stay available to an editor. The approver check therefore has to be in the
    body, and this asserts it is actually there."""
    import inspect

    src = inspect.getsource(router_mod.send)
    assert "body.live" in src and "approver" in src
    # And it is not merely on the route, which would block editors piloting.
    assert deps.require_approver not in _dependencies("/api/invites/send", "POST")


def test_the_send_log_row_is_written_before_the_email_leaves():
    """The duplicate guard is a unique index. If the row were written after
    the send, a duplicate would go out and only then fail to record, which is
    backwards for a guard whose job is to stop a second copy reaching a
    candidate."""
    import inspect

    src = inspect.getsource(router_mod.send)
    flush_at = src.index("db.flush()")
    send_at = src.index("sending.send_invite")
    assert flush_at < send_at, "the log row must be flushed before the send"


# --------------------------------------------------------------------------
# The send boundary, with a transport that records instead of delivering
# --------------------------------------------------------------------------


def _ctx(invite_type="values_interview"):
    return dict(
        first_name="Ushna", full_name="Ushna Tariq",
        position="Growth Manager - Lahore",
        jd_url="https://drive.google.com/file/d/jd/view",
        prep_url="https://docs.google.com/document/d/prep",
        booking_url="https://calendar.google.com/appointments/lahore",
    )


def test_send_invite_delivers_a_pilot_to_ayesha_alone():
    tx = sending.CaptureTransport()
    result = sending.send_invite(
        invite_type="values_interview",
        subject="Values Interview for Growth Manager - Lahore",
        body_html=rnd.render("values_interview", _ctx()),
        live=False,
        candidate_email="candidate@example.com",
        cc=["hiring@taleemabad.com"],
        booking_url="https://calendar.google.com/appointments/lahore",
        context="test_pilot",
        transport=tx,
    )
    assert result["to"] == [inv.PILOT_RECIPIENT]
    assert result["cc"] == []
    assert tx.sent[0]["recipients"] == [inv.PILOT_RECIPIENT]
    # The candidate's own address reached no part of the pilot.
    assert "candidate@example.com" not in tx.sent[0]["recipients"]


def test_send_invite_refuses_a_live_subject_carrying_the_pilot_marker():
    tx = sending.CaptureTransport()
    with pytest.raises(sending.SendBlocked) as exc:
        sending.send_invite(
            invite_type="values_interview",
            subject="[PILOT - ] Values Interview for Growth Manager",
            body_html=rnd.render("values_interview", _ctx()),
            live=True,
            candidate_email="candidate@example.com",
            booking_url="https://calendar.google.com/appointments/lahore",
            booking_verified_title="Zero in Call for Growth Manager Lahore",
            context="test_live",
            transport=tx,
        )
    assert any("[PILOT" in v["message"] for v in exc.value.violations)
    assert tx.sent == [], "nothing may leave when the gate blocks"


def test_send_invite_refuses_a_live_send_with_no_address():
    tx = sending.CaptureTransport()
    with pytest.raises(sending.SendBlocked):
        sending.send_invite(
            invite_type="values_interview", subject="Values Interview",
            body_html="<html></html>", live=True, candidate_email=None,
            context="test", transport=tx,
        )
    assert tx.sent == []


def test_send_invite_does_not_run_the_feedback_letter_harness():
    """An invite is a 200-word note. `evaluate_email` validates 800-word
    decision letters, and running it here would hard block every invite for
    failing rules never written for this kind of email."""
    import inspect

    src = inspect.getsource(sending.send_invite)
    assert "evaluate_email" not in src.split('"""')[2], (
        "the feedback-letter harness must not run on invites"
    )


def test_a_live_send_passes_the_candidate_through_the_allow_list():
    """`safe_sendmail` refuses external addresses unless they were explicitly
    allowed first, so a live invite must call `allow_candidate_addresses`."""
    import inspect

    src = inspect.getsource(sending.send_invite)
    assert "allow_candidate_addresses" in src
    assert "if live:" in src, "and only for a live send, never for a pilot"
