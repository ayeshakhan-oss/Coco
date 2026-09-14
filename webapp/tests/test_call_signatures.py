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


# --- Every gate gets the same evidence -------------------------------------
# A second regression of the same shape (2026-09-14, comm-b0e84207): four of the
# five evaluate_email call sites were handed `scorecard_text`; the one inside
# generate_draft was not. The leakage check stands down when it gets no
# scorecard, so the draft stored eval_passed=true with zero violations, and the
# letter hard-blocked only at Send — after the drafter and the review pass had
# both lost their chance to repair it. A gate that runs late is a gate that
# reaches Ayesha.

_EVIDENCE_KWARGS = {"cv_corpus", "scorecard_text", "candidate_name", "role"}

_WEBAPP = os.path.join(os.path.dirname(__file__), "..")
_GATE_FILES = [
    os.path.join(_WEBAPP, "routers", "communications.py"),
    os.path.join(_WEBAPP, "services", "drafting.py"),
    os.path.join(_WEBAPP, "services", "sending.py"),
]


def _evaluate_email_calls():
    """(file, lineno, {kwargs}) for every evaluate_email call in the app."""
    out = []
    for path in _GATE_FILES:
        with open(path, encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            fn = node.func
            name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", None)
            if name == "evaluate_email":
                out.append(
                    (os.path.basename(path), node.lineno,
                     {kw.arg for kw in node.keywords if kw.arg})
                )
    return out


def test_every_gate_is_handed_the_same_evidence():
    calls = _evaluate_email_calls()
    assert len(calls) >= 5, f"expected every gate to be found, got {calls}"
    starved = [
        (f, line, sorted(_EVIDENCE_KWARGS - kwargs))
        for f, line, kwargs in calls
        if _EVIDENCE_KWARGS - kwargs
    ]
    assert not starved, (
        "these evaluate_email gates are missing evidence, so they check less "
        f"than the others and a letter passes one stage to block at the next: {starved}"
    )


def test_generate_draft_accepts_and_uses_the_scorecard():
    from webapp.services import drafting

    assert "scorecard_text" in inspect.signature(drafting.generate_draft).parameters
    assert "scorecard_text=scorecard_text" in inspect.getsource(drafting.generate_draft)
    assert "scorecard_text=" in _kwargs_passed_to("generate_draft") or (
        "scorecard_text" in _kwargs_passed_to("generate_draft")
    ), "the generate endpoint must pass the scorecard to the drafter's gate"
