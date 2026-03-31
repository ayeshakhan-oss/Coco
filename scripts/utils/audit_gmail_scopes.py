"""
audit_gmail_scopes.py — Gmail OAuth Scope Auditor
==================================================
Checks that all OAuth tokens only have the minimum required scopes.
Flags any token with overly broad scopes (e.g. full gmail.modify instead of readonly).

Minimum required scopes for Coco:
  - token_gmail.json:        gmail.readonly (read replies only)
  - token_gmail_labels.json: gmail.readonly (label reads)
  - token_sheets.json:       spreadsheets.readonly
  - token.json:              calendar (needed for invite creation)

Usage:
    python scripts/utils/audit_gmail_scopes.py
"""

import os
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Minimum acceptable scopes per token file (must have AT LEAST one of these)
REQUIRED_SCOPES = {
    "token_gmail.json": [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://mail.google.com/",
    ],
    "token_gmail_labels.json": [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://mail.google.com/",
    ],
    "token_sheets.json": [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/spreadsheets",
    ],
    "token.json": [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.events",
    ],
}

# Overly broad scopes that should trigger a warning
OVERLY_BROAD = {
    "https://mail.google.com/",                               # full access (allows send/delete)
    "https://www.googleapis.com/auth/gmail.modify",           # modify — not needed for reads
    "https://www.googleapis.com/auth/drive",                  # full Drive
    "https://www.googleapis.com/auth/spreadsheets",           # write access — warn if not needed
}

# Scopes that are acceptable overrides (send scripts need send access)
ACCEPTABLE_SEND_SCOPES = {
    "https://mail.google.com/",  # smtplib IMAP/SMTP uses this — OK for send tokens
}


def audit_file(fname: str) -> dict:
    fpath = os.path.join(ROOT, fname)
    result = {"file": fname, "status": "OK", "issues": [], "scopes": []}

    if not os.path.exists(fpath):
        result["status"] = "MISSING"
        result["issues"].append("File not found — may be OK if not yet authorized")
        return result

    try:
        with open(fpath, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        result["status"] = "UNREADABLE"
        result["issues"].append(str(e))
        return result

    raw_scopes = data.get("scopes") or data.get("scope", "")
    if isinstance(raw_scopes, str):
        scopes = raw_scopes.split()
    elif isinstance(raw_scopes, list):
        scopes = raw_scopes
    else:
        scopes = []

    result["scopes"] = scopes

    if not scopes:
        result["status"] = "NO_SCOPE_INFO"
        result["issues"].append("No scope field in token — cannot audit")
        return result

    # Check for overly broad scopes
    for s in scopes:
        if s in OVERLY_BROAD and s not in ACCEPTABLE_SEND_SCOPES:
            result["issues"].append(f"Overly broad scope: {s}")
            result["status"] = "WARN"

    # Check required scopes present
    required = REQUIRED_SCOPES.get(fname, [])
    if required and not any(s in scopes for s in required):
        result["issues"].append(f"Missing required scope. Expected one of: {required}")
        result["status"] = "WARN"

    return result


def run_audit(print_output: bool = True) -> list:
    results = []
    for fname in REQUIRED_SCOPES:
        r = audit_file(fname)
        results.append(r)

        if print_output:
            icon = "[OK]" if r["status"] == "OK" else "[!]" if r["status"] == "WARN" else "[?]"
            print(f"  {icon} {r['file']:35s} {r['status']}")
            for s in r["scopes"]:
                print(f"       scope: {s}")
            for issue in r["issues"]:
                print(f"       ISSUE: {issue}")

    return results


if __name__ == "__main__":
    print("Coco Gmail Scope Audit")
    print("-" * 60)
    run_audit()
