"""
check_token_expiry.py — Coco Token Health Monitor
==================================================
Checks all OAuth token files for expiry / revocation.
Run manually or call check_all_tokens() at session start.

Usage:
    python scripts/utils/check_token_expiry.py
"""

import os
import json
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

TOKEN_FILES = [
    "token.json",
    "token_gmail.json",
    "token_gmail_labels.json",
    "token_sheets.json",
]

WARN_WITHIN_DAYS = 3  # warn if token expires within this many days


def check_token(filepath: str) -> dict:
    result = {"file": os.path.basename(filepath), "status": "unknown", "detail": ""}

    if not os.path.exists(filepath):
        result["status"] = "MISSING"
        result["detail"] = "File not found"
        return result

    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        result["status"] = "UNREADABLE"
        result["detail"] = str(e)
        return result

    # Check for revocation marker
    if data.get("invalid") or data.get("revoked"):
        result["status"] = "REVOKED"
        result["detail"] = "Token marked invalid/revoked"
        return result

    # Check expiry timestamp
    expiry_str = data.get("expiry") or data.get("token_expiry")
    if expiry_str:
        try:
            # Handle both ISO format and epoch
            if isinstance(expiry_str, (int, float)):
                expiry = datetime.fromtimestamp(expiry_str, tz=timezone.utc)
            else:
                expiry = datetime.fromisoformat(expiry_str.replace("Z", "+00:00"))

            now = datetime.now(tz=timezone.utc)
            delta = expiry - now
            days_left = delta.total_seconds() / 86400

            if days_left < 0:
                result["status"] = "EXPIRED"
                result["detail"] = f"Expired {abs(days_left):.1f} days ago"
            elif days_left < WARN_WITHIN_DAYS:
                result["status"] = "EXPIRING_SOON"
                result["detail"] = f"Expires in {days_left:.1f} days ({expiry.strftime('%Y-%m-%d %H:%M')} UTC)"
            else:
                result["status"] = "OK"
                result["detail"] = f"Valid for {days_left:.1f} days"
        except Exception as e:
            result["status"] = "PARSE_ERROR"
            result["detail"] = f"Could not parse expiry: {e}"
    else:
        # No expiry field — likely a refresh token (long-lived)
        if data.get("refresh_token") or data.get("token"):
            result["status"] = "OK"
            result["detail"] = "Refresh token present, no expiry field (long-lived)"
        else:
            result["status"] = "INCOMPLETE"
            result["detail"] = "No token or expiry field found"

    # Check Gmail scopes if present
    scopes = data.get("scopes") or data.get("scope", "")
    if scopes:
        if isinstance(scopes, list):
            scopes_str = " ".join(scopes)
        else:
            scopes_str = str(scopes)
        result["scopes"] = scopes_str

    return result


def check_all_tokens(print_output: bool = True) -> list:
    results = []
    for fname in TOKEN_FILES:
        fpath = os.path.join(ROOT, fname)
        r = check_token(fpath)
        results.append(r)

        if print_output:
            icon = {"OK": "[OK]", "MISSING": "[--]", "EXPIRED": "[!!]",
                    "EXPIRING_SOON": "[!]", "REVOKED": "[!!]"}.get(r["status"], "[?]")
            print(f"  {icon} {r['file']:35s} {r['status']:15s} {r['detail']}")
            if "scopes" in r:
                print(f"       scopes: {r['scopes'][:120]}")

    # Summary
    bad = [r for r in results if r["status"] not in ("OK",)]
    if bad and print_output:
        print(f"\n  WARNING: {len(bad)} token(s) need attention.")
        for r in bad:
            print(f"    - {r['file']}: {r['status']} — {r['detail']}")

    return results


if __name__ == "__main__":
    print("Coco Token Health Check")
    print("-" * 60)
    check_all_tokens()
