"""
Fetch full email threads for Mizhgan reschedule + Shah Zero In call
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
    """Extract plain text or HTML body from email payload."""
    if "parts" in payload:
        for p in payload["parts"]:
            result = get_body(p)
            if result:
                return result
    mime = payload.get("mimeType","")
    if mime in ("text/plain","text/html"):
        data = payload.get("body",{}).get("data","")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")[:2000]
    return ""

def fetch_thread(service, thread_id):
    t = service.users().threads().get(userId="me", id=thread_id, format="full").execute()
    for msg in t.get("messages",[]):
        hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(f"\n  From: {hdrs.get('From','')}")
        print(f"  Date: {hdrs.get('Date','')}")
        print(f"  Subject: {hdrs.get('Subject','')}")
        body = get_body(msg["payload"])
        # Print first 600 chars of body
        if body:
            print(f"  Body: {body[:600].strip()}")

def main():
    service = build("gmail", "v1", credentials=get_creds())

    # 1. Mizhgan reschedule thread
    print("\n=== MIZHGAN RESCHEDULE THREAD ===")
    r = service.users().messages().list(userId="me", q="mizhgan kirmani reschedule", maxResults=5).execute()
    for m in r.get("messages",[]):
        msg = service.users().messages().get(userId="me", id=m["id"], format="metadata",
                                              metadataHeaders=["Subject","From","Date","To"]).execute()
        hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(f"  Subject: {hdrs.get('Subject','')}")
        print(f"  From: {hdrs.get('From','')}")
        print(f"  Date: {hdrs.get('Date','')}")
    log_gmail_read(query="mizhgan kirmani reschedule", message_count=len(r.get("messages",[])), context="fetch_job32_details")

    # Full thread on Mizhgan debrief (most recent email)
    r2 = service.users().messages().list(userId="me", q="mizhgan kirmani debrief", maxResults=3).execute()
    msgs = r2.get("messages",[])
    if msgs:
        msg = service.users().messages().get(userId="me", id=msgs[0]["id"], format="full").execute()
        hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(f"\nLatest Mizhgan debrief email:")
        print(f"  Subject: {hdrs.get('Subject','')}")
        print(f"  From: {hdrs.get('From','')}")
        body = get_body(msg["payload"])
        safe_body = body[:800].strip().encode("ascii","replace").decode("ascii")
        print(f"  Body excerpt: {safe_body}")
    log_gmail_read(query="mizhgan kirmani debrief", message_count=len(msgs), context="fetch_job32_details")

    # 2. "Shah" Zero In call
    print("\n\n=== SHAH ZERO IN CALL ===")
    r3 = service.users().messages().list(userId="me",
           q="Zero In fundraising partnerships Shah", maxResults=5).execute()
    for m in r3.get("messages",[]):
        msg = service.users().messages().get(userId="me", id=m["id"], format="metadata",
                                              metadataHeaders=["Subject","From","Date","To"]).execute()
        hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(f"  Subject: {hdrs.get('Subject','')}")
        print(f"  From: {hdrs.get('From','')}")
        print(f"  Date: {hdrs.get('Date','')}")
    log_gmail_read(query="Zero In fundraising Shah", message_count=len(r3.get("messages",[])), context="fetch_job32_details")

    # 3. Hamdan GWC — any notes/outcome
    print("\n\n=== HAMDAN GWC OUTCOME ===")
    r4 = service.users().messages().list(userId="me", q="hamdan ahmad gwc OR debrief OR zero in", maxResults=5).execute()
    for m in r4.get("messages",[]):
        msg = service.users().messages().get(userId="me", id=m["id"], format="metadata",
                                              metadataHeaders=["Subject","From","Date","To"]).execute()
        hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(f"  Subject: {hdrs.get('Subject','')}")
        print(f"  From: {hdrs.get('From','')}")
        print(f"  Date: {hdrs.get('Date','')}")
    log_gmail_read(query="hamdan ahmad gwc debrief", message_count=len(r4.get("messages",[])), context="fetch_job32_details")

    # 4. Check for any Huma Mumtaz Zero In rebook
    print("\n\n=== HUMA MUMTAZ STATUS ===")
    r5 = service.users().messages().list(userId="me", q="Huma Mumtaz OR huma.mumtaz3 fundraising", maxResults=5).execute()
    for m in r5.get("messages",[]):
        msg = service.users().messages().get(userId="me", id=m["id"], format="metadata",
                                              metadataHeaders=["Subject","From","Date","To"]).execute()
        hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(f"  Subject: {hdrs.get('Subject','')}")
        print(f"  From: {hdrs.get('From','')}")
        print(f"  Date: {hdrs.get('Date','')}")
    log_gmail_read(query="Huma Mumtaz fundraising", message_count=len(r5.get("messages",[])), context="fetch_job32_details")

if __name__ == "__main__":
    main()
