"""
Check current Zero In call schedule for Fundraising & Partnerships Manager
"""
import os, sys, base64
sys.path.insert(0, "c:/Agent Coco")

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from scripts.utils.audit_log import log_gmail_read

TOKEN_GMAIL = "c:/Agent Coco/token_gmail.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_creds():
    creds = Credentials.from_authorized_user_file(TOKEN_GMAIL, SCOPES)
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
            return base64.urlsafe_b64decode(data).decode("utf-8","replace")[:600]
    return ""

def main():
    service = build("gmail", "v1", credentials=get_creds())

    # All Zero In bookings, acceptances, declines for Fundraising
    print("=== ALL ZERO IN ACTIVITY — FUNDRAISING & PARTNERSHIPS ===\n")
    queries = [
        '"Zero In Call for Fundraising" (booked OR Accepted OR Declined OR canceled)',
    ]
    for q in queries:
        r = service.users().messages().list(userId="me", q=q, maxResults=50).execute()
        msgs = r.get("messages", [])
        print(f"Found {len(msgs)} messages\n")
        for m in msgs:
            msg = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
            hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
            subj = hdrs.get("Subject","")
            frm  = hdrs.get("From","")
            date = hdrs.get("Date","")
            body = get_body(msg["payload"])
            # Extract candidate name and date from subject
            safe_body = body[:300].encode("ascii","replace").decode("ascii")
            print(f"  [{date[:16]}] {frm.split('<')[0].strip()}")
            print(f"  {subj}")
            if safe_body.strip():
                print(f"  >> {safe_body[:200].strip()}")
            print()
        log_gmail_read(query=q, message_count=len(msgs), context="fetch_job32_zeroin_status")

if __name__ == "__main__":
    main()
