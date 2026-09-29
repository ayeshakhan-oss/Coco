"""One-time setup: mint (or reuse) a Gmail token for Coco's webapp and print the
authorized-user JSON to paste into Railway as GMAIL_OAUTH_TOKEN_JSON.

Scopes: gmail.readonly (the Markaz<->Gmail evidence sync) + gmail.send (so the
webapp can send candidate emails from ayesha.khan@ over HTTPS — required because
Railway blocks outbound SMTP) + drive.file (contract attachments must be PDF and
Drive is the only converter; `drive.file` reaches ONLY files this app creates,
never anything already in her Drive). A token missing any of these is NOT
reused; the consent window re-opens to add what is missing.

Run locally (Ayesha's machine, signed into ayesha.khan@taleemabad.com):

    python scripts/auth/setup_gmail_sync_token.py

Behavior:
  1. If .claude/config/token_gmail.json already has a readonly refresh token that
     works, it's reused (no new consent prompt).
  2. Otherwise a browser consent window opens for the gmail.readonly scope.
  3. Either way it verifies the mailbox identity and prints the JSON for Railway.
"""

from __future__ import annotations

import json
import os
import sys

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",  # evidence sync (read Sent/inbox)
    "https://www.googleapis.com/auth/gmail.send",       # send candidate emails from the webapp
    # 🔒 drive.FILE, never plain `drive`. Contract attachments must be PDF and
    # never .docx (Skill 07 joining-emails rule 10, harness-blocked), and Drive
    # is the only converter available. `drive.file` grants access ONLY to files
    # this app itself creates — it uploads the .docx, converts, downloads the
    # PDF and deletes the temporary copy. It cannot see, read or change
    # anything already in Ayesha's Drive. The broad `drive` scope on
    # token_sheets_broad.json stays local and off the server.
    "https://www.googleapis.com/auth/drive.file",
]
TOKEN_PATH = os.path.join(".claude", "config", "token_gmail.json")
CLIENT_SECRETS = os.path.join("data", "credentials.json")
EXPECTED_MAILBOX = "ayesha.khan@taleemabad.com"


def _verify(creds) -> str:
    from googleapiclient.discovery import build

    svc = build("gmail", "v1", credentials=creds, cache_discovery=False)
    profile = svc.users().getProfile(userId="me").execute()
    return profile.get("emailAddress", "")


def _load_existing():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    if not os.path.exists(TOKEN_PATH):
        return None
    try:
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    except Exception:
        return None
    if not creds.refresh_token:
        return None
    # Force a fresh consent if the saved token doesn't already include EVERY
    # scope we need (e.g. an older readonly-only token can't send).
    try:
        if not creds.has_scopes(SCOPES):
            return None
    except Exception:
        return None
    try:
        if not creds.valid and creds.expired:
            creds.refresh(Request())
        return creds
    except Exception:
        return None


def _consent():
    from google_auth_oauthlib.flow import InstalledAppFlow

    if not os.path.exists(CLIENT_SECRETS):
        sys.exit(f"Missing OAuth client secrets at {CLIENT_SECRETS}. Cannot run consent flow.")
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
    # access_type=offline + prompt=consent guarantees a refresh_token.
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        f.write(creds.to_json())
    return creds


def main() -> None:
    creds = _load_existing()
    if creds:
        print(f"Reusing existing readonly token at {TOKEN_PATH}.")
    else:
        print("No reusable token found — opening consent for gmail.readonly...")
        creds = _consent()

    mailbox = _verify(creds)
    print(f"\nToken is valid. Mailbox: {mailbox}")
    if mailbox.lower() != EXPECTED_MAILBOX:
        print(f"  WARNING: expected {EXPECTED_MAILBOX}. Make sure you consented with the right account.")

    print("\n" + "=" * 70)
    print("Paste the following as the Railway env var  GMAIL_OAUTH_TOKEN_JSON")
    print("(single line, keep it SECRET — it grants read + SEND on the mailbox):")
    print("=" * 70)
    # Compact single-line JSON for the env var.
    print(json.dumps(json.loads(creds.to_json())))
    print("=" * 70)


if __name__ == "__main__":
    main()
