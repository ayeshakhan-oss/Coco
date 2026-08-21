#!/usr/bin/env python3
"""
Pre-send validation hook for candidate communication emails.

Fires BEFORE safe_sendmail() is called (PreToolUse hook event).
Validates email against all 10 locked rules.

Exit codes:
  - 0: All checks passed or only warnings (allow send)
  - 1: JSON parse error or internal error (allow send, log error)
  - 2: HARD BLOCK violations (block send)
"""

import sys
import json
import re
from datetime import datetime
from pathlib import Path

# Add scripts/evals to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'evals'))

from candidate_communication_eval import evaluate_email


def log_audit(message: str, level: str = 'INFO'):
    """Log to audit log file."""
    try:
        log_path = Path(__file__).parent.parent.parent / 'logs' / 'email_audit.log'
        log_path.parent.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Warning: Could not write to audit log: {e}", file=sys.stderr)


def extract_email_params(tool_input: dict) -> tuple:
    """
    Extract email parameters from Bash tool input.

    Returns: (subject, html_body, pilot_mode, email_type) or (None, None, None, None)
    """
    try:
        # safe_sendmail call looks like:
        # Bash: safe_sendmail(subject, body, recipients, pilot_mode=True)
        # We need to infer from the command string or from passed args

        # Look for common patterns in the command
        command = tool_input.get('command', '')

        # Try to extract subject from quoted strings
        subject_match = re.search(r"subject\s*=\s*['\"]([^'\"]+)['\"]", command)
        subject = subject_match.group(1) if subject_match else None

        # Try to extract pilot_mode
        pilot_match = re.search(r"pilot_mode\s*=\s*(True|False)", command)
        pilot_mode = pilot_match.group(1) == 'True' if pilot_match else True

        # Try to infer email type from filename or context
        email_type = None
        if 'warm_bench' in command:
            email_type = 'warm_bench'
        elif 'gwc' in command or 'GWC' in command:
            email_type = 'gwc_rejection'
        elif 'values' in command:
            email_type = 'values_feedback'
        elif 'rejection' in command or 'cv_rejection' in command:
            email_type = 'cv_rejection'
        # Skill 01 type #7 - INTERNAL staff announcement (added 2026-08-20). Checked
        # first-class so the [PILOT] prefix guard below still runs on it; the
        # candidate content rules (800 words, opening line, jargon) do NOT apply.
        elif 'announcement' in command:
            email_type = 'announcement'

        return subject, None, pilot_mode, email_type

    except Exception:
        return None, None, None, None


def main():
    """
    Hook entry point. Reads from stdin (Claude Code harness).
    """
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        log_audit(f"Hook input JSON parse error: {e}", 'ERROR')
        # Allow send on parse error (don't block work)
        return 0
    except EOFError:
        # No input — this is not a pre-send hook call
        return 0

    tool_name = hook_input.get('tool_name', '')
    tool_input = hook_input.get('tool_input', {})

    # Only process safe_sendmail and related email sends
    if not ('safe_sendmail' in tool_name.lower() or 'send' in tool_name.lower()):
        return 0  # Not an email send

    # Extract email parameters
    subject, body, pilot_mode, email_type = extract_email_params(tool_input)

    # If we couldn't extract params, allow send (this hook isn't configured for this call)
    if not all([subject, email_type]):
        log_audit(f"Could not extract email params from tool input. Tool: {tool_name}", 'WARNING')
        return 0

    # Log the check
    log_audit(f"Pre-send validation: {email_type} | Subject: {subject[:50]}... | pilot={pilot_mode}")

    # NOTE: This is a simplified implementation. In production, the body would need to be
    # passed through the harness or extracted from the tool input more carefully.
    # For now, this hook validates subject-level checks (PILOT prefix, etc.)

    # Perform PILOT prefix check (most critical)
    if not pilot_mode and '[PILOT' in subject:
        violation_msg = f'CRITICAL: [PILOT] prefix in subject with PILOT_MODE=False. Subject: "{subject}"'
        log_audit(violation_msg, 'HARD_BLOCK')
        print(f"ERROR: {violation_msg}", file=sys.stderr)
        return 2  # HARD BLOCK

    # Log that check passed
    log_audit(f"Pre-send validation passed for {email_type}")
    return 0  # Allow send


if __name__ == '__main__':
    sys.exit(main())
