"""
Identify the 'Shah' Zero In candidate + Huma rebooking
"""
import os, sys, base64
sys.path.insert(0, "c:/Agent Coco")

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from scripts.utils.audit_log import log_gmail_read

TOKEN_GMAIL = "c:/Agent Coco/token_gmail.json"
SCOPES_GMAIL = ["https://www.googleapis.com/auth/gmail.readonly"]

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
            return base64.urlsafe_b64decode(data).decode("utf-8","replace")[:1500]
    return ""

def main():
    service = build("gmail", "v1", credentials=get_creds())

    # Full body of the "Shah" Zero In appointment email
    print("=== SHAH ZERO IN FULL EMAIL ===")
    r = service.users().messages().list(userId="me",
        q="Zero In fundraising Shah Apr 8", maxResults=3).execute()
    for m in r.get("messages",[]):
        msg = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
        hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(f"Subject: {hdrs.get('Subject','')}")
        print(f"From: {hdrs.get('From','')}")
        body = get_body(msg["payload"])
        safe = body.encode("ascii","replace").decode("ascii")
        print(f"Body: {safe[:1500]}")
        print("---")
    log_gmail_read(query="Zero In fundraising Shah Apr 8", message_count=len(r.get("messages",[])), context="fetch_job32_details2")

    # Huma rebooking
    print("\n=== HUMA ZERO IN REBOOKING ===")
    r2 = service.users().messages().list(userId="me",
        q="Zero In fundraising Huma Apr", maxResults=5).execute()
    for m in r2.get("messages",[]):
        msg = service.users().messages().get(userId="me", id=m["id"], format="metadata",
                                              metadataHeaders=["Subject","From","Date"]).execute()
        hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(f"  {hdrs.get('Date','')} | {hdrs.get('From','')} | {hdrs.get('Subject','')}")
    log_gmail_read(query="Zero In fundraising Huma", message_count=len(r2.get("messages",[])), context="fetch_job32_details2")

if __name__ == "__main__":
    main()
