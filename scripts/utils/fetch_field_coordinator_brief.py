"""
Fetch the Field Coordinator decision brief email body sent April 2 2026
"""
import os, sys, base64
sys.path.insert(0, "c:/Agent Coco")

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from scripts.utils.audit_log import log_gmail_read

TOKEN_GMAIL = "c:/Agent Coco/token_gmail.json"
SCOPES_GMAIL = ["https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/gmail.modify"]

def get_creds():
    creds = Credentials.from_authorized_user_file(TOKEN_GMAIL, SCOPES_GMAIL)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

def get_body(payload):
    if "parts" in payload:
        for p in payload["parts"]:
            r = get_body(p)
            if r: return r
    mime = payload.get("mimeType","")
    if mime in ("text/plain","text/html"):
        data = payload.get("body",{}).get("data","")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8","replace")
    return ""

def main():
    service = build("gmail", "v1", credentials=get_creds())

    # Find the Field Coordinator decision brief pilot email
    r = service.users().messages().list(
        userId="me",
        q='subject:"Final Candidates" "Field Coordinator" after:2026/04/01 before:2026/04/04',
        maxResults=5
    ).execute()

    msgs = r.get("messages", [])
    print(f"Found {len(msgs)} matching emails\n")

    for m in msgs:
        msg = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
        hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(f"Subject: {hdrs.get('Subject','')}")
        print(f"From: {hdrs.get('From','')}")
        print(f"Date: {hdrs.get('Date','')}")
        print(f"To: {hdrs.get('To','')}")
        print(f"CC: {hdrs.get('Cc','')}")

        # List attachments
        def list_parts(payload, depth=0):
            mime = payload.get("mimeType","")
            fname = payload.get("filename","")
            if fname:
                print(f"  {'  '*depth}ATTACHMENT: {fname} ({mime})")
            if "parts" in payload:
                for p in payload["parts"]:
                    list_parts(p, depth+1)

        print("Attachments:")
        list_parts(msg["payload"])
        print("---")

    log_gmail_read(query="Final Candidates Field Coordinator April 2026",
                   message_count=len(msgs), context="fetch_field_coordinator_brief")

if __name__ == "__main__":
    main()
