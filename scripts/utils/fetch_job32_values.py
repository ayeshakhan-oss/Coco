"""
Fetch all values call (Zero In) status for Job 32 candidates
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
            return base64.urlsafe_b64decode(data).decode("utf-8","replace")[:1000]
    return ""

def main():
    service = build("gmail", "v1", credentials=get_creds())

    # All Zero In invites sent for Job 32
    print("=== ALL ZERO IN INVITES SENT FOR JOB 32 ===")
    r = service.users().messages().list(userId="me",
        q="subject:\"Invitation for the Values Interview for Fundraising\"", maxResults=20).execute()
    for m in r.get("messages",[]):
        msg = service.users().messages().get(userId="me", id=m["id"], format="metadata",
              metadataHeaders=["Subject","From","Date","To"]).execute()
        hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(f"  {hdrs.get('Date','')} | To: {hdrs.get('To','')} | {hdrs.get('Subject','')}")
    log_gmail_read(query="Values Interview invites Fundraising", message_count=len(r.get("messages",[])), context="fetch_job32_values")

    # All Zero In booking confirmations
    print("\n=== ALL ZERO IN BOOKINGS (Fundraising) ===")
    r2 = service.users().messages().list(userId="me",
        q="\"Zero In Call for Fundraising\" (Appointment booked OR Accepted OR Declined)", maxResults=20).execute()
    for m in r2.get("messages",[]):
        msg = service.users().messages().get(userId="me", id=m["id"], format="metadata",
              metadataHeaders=["Subject","From","Date","To"]).execute()
        hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(f"  {hdrs.get('Date','')} | From: {hdrs.get('From','')} | {hdrs.get('Subject','')}")
    log_gmail_read(query="Zero In bookings Fundraising", message_count=len(r2.get("messages",[])), context="fetch_job32_values")

    # Check for any values pass/outcome emails for job 32 candidates
    print("\n=== VALUES OUTCOMES / PIPELINE PROGRESSION ===")
    for name in ["Mizhgan", "Zain", "Hamdan", "Huma Mumtaz", "Shahzad"]:
        r3 = service.users().messages().list(userId="me",
            q=f"{name} fundraising (values OR zero in OR passed OR GWC OR case study)", maxResults=5).execute()
        msgs = r3.get("messages",[])
        if msgs:
            print(f"\n  {name} ({len(msgs)} results):")
            for m in msgs[:3]:
                msg = service.users().messages().get(userId="me", id=m["id"], format="metadata",
                      metadataHeaders=["Subject","From","Date"]).execute()
                hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
                print(f"    {hdrs.get('Date','')} | {hdrs.get('From','')} | {hdrs.get('Subject','')}")
        log_gmail_read(query=f"{name} fundraising values pipeline", message_count=len(msgs), context="fetch_job32_values")

if __name__ == "__main__":
    main()
