"""Single import surface for the reused, LOCKED candidate-communication logic.

These modules live under scripts/ and are the SINGLE SOURCE OF TRUTH for the
v8 email layout, the validation harness (7 HARD-BLOCK + 4 WARNING rules), and
the recipient-allowlist send bouncer. The webapp imports them HERE and never
reimplements them, so the locked design and rules cannot drift.

The container ships the full repo tree and sets PYTHONPATH=/app. For local/dev
runs we also insert the repo root onto sys.path so `from scripts...` resolves
regardless of the current working directory.
"""

from __future__ import annotations

import os
import sys


def _ensure_repo_root_on_path() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(here)  # repo root = parent of webapp/
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)


_ensure_repo_root_on_path()

# v8 locked email layout
from scripts.utils.v8_template import (  # noqa: E402
    H,
    SUB,
    P,
    PS,
    FOOTER,
    EYEBROW,
    LOGO_PATH,
    wrap,
    attach_logo,
)

# In-email candidate feedback widget
from scripts.utils.feedback_widget import feedback_widget  # noqa: E402

# Recipient-allowlist send bouncer + audit log
from scripts.utils.safe_send import (  # noqa: E402
    safe_sendmail,
    guard_and_log_api_send,
    allow_candidate_addresses,
    SecurityError,
)

# Validation harness — authoritative quality gate
from scripts.evals.candidate_communication_eval import (  # noqa: E402
    evaluate_email,
    SECTION_HEADINGS,
)

# Email types the harness/templates support.
EMAIL_TYPES = ("cv_rejection", "values_feedback", "warm_bench", "gwc_rejection")

__all__ = [
    "H",
    "SUB",
    "P",
    "PS",
    "FOOTER",
    "EYEBROW",
    "LOGO_PATH",
    "wrap",
    "attach_logo",
    "feedback_widget",
    "safe_sendmail",
    "guard_and_log_api_send",
    "allow_candidate_addresses",
    "SecurityError",
    "evaluate_email",
    "SECTION_HEADINGS",
    "EMAIL_TYPES",
]
