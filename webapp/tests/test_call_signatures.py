"""Every cross-module call in the draft/send path must actually be callable.

The regression (2026-09-14): adding `scorecard_text=` to the evaluate_email call
sites also added it to the `sending.send_communication(...)` call, which did not
accept it. Nothing failed until Ayesha pressed Send pilot and got:

    502: Send failed: send_communication() got an unexpected keyword argument
    'scorecard_text'

The unit tests all passed, because none of them call the send path. A signature
mismatch is invisible to a test suite that never makes the call.

Run: python -m pytest webapp/tests/test_call_signatures.py
"""

from __future__ import annotations

import ast
import inspect
import os

from webapp.services import sending
from scripts.evals.candidate_communication_eval import evaluate_email

ROUTER = os.path.join(os.path.dirname(__file__), "..", "routers", "communications.py")


def _kwargs_passed_to(func_name: str) -> set[str]:
    """Every keyword the router passes to `func_name`, read from the source."""
    with open(ROUTER, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    found: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", None)
        if name == func_name:
            found.update(kw.arg for kw in node.keywords if kw.arg)
    return found


def test_router_only_passes_kwargs_send_communication_accepts():
    passed = _kwargs_passed_to("send_communication")
    accepted = set(inspect.signature(sending.send_communication).parameters)
    assert passed, "no send_communication call found in the router"
    assert passed <= accepted, (
        "router passes kwargs send_communication does not accept: "
        f"{sorted(passed - accepted)}"
    )


def test_router_only_passes_kwargs_evaluate_email_accepts():
    passed = _kwargs_passed_to("evaluate_email")
    accepted = set(inspect.signature(evaluate_email).parameters)
    assert passed, "no evaluate_email call found in the router"
    assert passed <= accepted, (
        "router passes kwargs evaluate_email does not accept: "
        f"{sorted(passed - accepted)}"
    )


def test_send_communication_forwards_the_evidence_to_the_gate():
    """Both corpora must reach the send-time check, or the gate is weaker than
    the draft-time one and a letter can pass on its way out."""
    src = inspect.getsource(sending.send_communication)
    assert "cv_corpus=cv_corpus" in src
    assert "scorecard_text=scorecard_text" in src
