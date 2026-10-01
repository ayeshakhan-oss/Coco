"""The contract package send: PDFs only, pilot to Ayesha, approver for live.

Run: python -m pytest webapp/tests/test_contract_send.py -v

A candidate must never receive an editable contract, and a pilot must never
reach anybody but Ayesha. Both are checked here against a transport that
records instead of delivering.
"""

from __future__ import annotations

import pytest

from webapp import deps
from webapp.routers import contracts as router_mod
from webapp.services import joining_email as je
from webapp.services import sending

PDF = b"%PDF-1.4 pretend"


def _dependencies(path: str, method: str) -> set:
    for route in router_mod.router.routes:
        if getattr(route, "path", None) == path and method in (
            getattr(route, "methods", None) or set()
        ):
            return {d.call for d in route.dependant.dependencies if getattr(d, "call", None)}
    raise AssertionError(f"route not found: {method} {path}")


# --------------------------------------------------------------------------
# Who can reach it
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path,method",
    [("/api/contracts/package", "POST"), ("/api/contracts/send", "POST"),
     ("/api/contracts/people", "GET"), ("/api/contracts/prefill", "GET")],
)
def test_everything_touching_a_contract_needs_at_least_an_editor(path, method):
    """These carry a CNIC and a salary."""
    assert deps.require_editor in _dependencies(path, method)


def test_the_live_send_is_gated_in_the_body_not_on_the_route():
    """One route serves pilot and live, so the pilot stays open to an editor
    and goes through exactly the code that builds the live email."""
    import inspect

    src = inspect.getsource(router_mod.send_package)
    assert "approver" in src and "live" in src
    assert deps.require_approver not in _dependencies("/api/contracts/send", "POST")


def test_the_pilot_and_the_live_email_are_built_by_one_function():
    """A pilot assembled separately proves nothing about the live send."""
    import inspect

    assert "_build_package" in inspect.getsource(router_mod.send_package)
    assert "_build_package" in inspect.getsource(router_mod.preview_package)


def test_the_preview_never_returns_the_attachment_bytes():
    """The PDFs carry a CNIC and a salary and must not sit in a JSON response
    a browser caches."""
    import inspect

    src = inspect.getsource(router_mod.preview_package)
    assert "size_bytes" in src
    assert '"bytes"' not in src.split("return")[1]


# --------------------------------------------------------------------------
# The send boundary
# --------------------------------------------------------------------------


def test_a_pilot_goes_to_ayesha_alone_with_the_attachments():
    tx = sending.CaptureTransport()
    result = sending.send_joining_email(
        subject="Welcome to Taleemabad - Research Fellow",
        html="<p>Hi Ali,</p>",
        attachments=[("Contract - Ali.pdf", PDF), ("Fellow NDA - Ali.pdf", PDF)],
        to=[je.PILOT_RECIPIENT], cc=[], live=False,
        context="test_pilot", transport=tx,
    )
    assert result["to"] == [je.PILOT_RECIPIENT]
    assert result["cc"] == []
    assert tx.sent[0]["recipients"] == [je.PILOT_RECIPIENT]
    assert len(result["attachments"]) == 2


@pytest.mark.parametrize("name", ["Contract - Ali.docx", "NDA.doc", "notes.txt"])
def test_a_non_pdf_attachment_is_refused(name):
    """A candidate must never receive an editable contract."""
    tx = sending.CaptureTransport()
    with pytest.raises(ValueError, match="never Word|not a PDF"):
        sending.send_joining_email(
            subject="x", html="<p>x</p>", attachments=[(name, PDF)],
            to=["a@b.com"], cc=[], live=False, context="t", transport=tx)
    assert tx.sent == []


def test_a_pdf_filename_hiding_something_else_is_refused():
    """The extension is not evidence. The bytes are."""
    tx = sending.CaptureTransport()
    with pytest.raises(ValueError, match="does not contain a PDF"):
        sending.send_joining_email(
            subject="x", html="<p>x</p>",
            attachments=[("Contract - Ali.pdf", b"PK\x03\x04 this is a docx")],
            to=["a@b.com"], cc=[], live=False, context="t", transport=tx)
    assert tx.sent == []


def test_a_send_with_no_recipient_is_refused():
    tx = sending.CaptureTransport()
    with pytest.raises(ValueError, match="needs a recipient"):
        sending.send_joining_email(
            subject="x", html="<p>x</p>", attachments=[("a.pdf", PDF)],
            to=[], cc=[], live=False, context="t", transport=tx)


def test_a_live_send_passes_the_candidate_through_the_allow_list():
    import inspect

    src = inspect.getsource(sending.send_joining_email)
    assert "allow_candidate_addresses" in src
    assert "if live:" in src, "and only for a live send, never for a pilot"


def test_the_feedback_letter_harness_is_not_run_on_a_joining_email():
    """It validates 800-word decision letters and would block every one."""
    import inspect

    body = inspect.getsource(sending.send_joining_email).split('"""')[2]
    assert "evaluate_email" not in body
