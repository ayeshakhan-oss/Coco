"""
Fetch Job 32 context: Gmail threads + Calendar events for GWC/debrief calls
"""
import os, sys, json, base64
sys.path.insert(0, "c:/Agent Coco")

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_CAL   = "c:/Agent Coco/token.json"
TOKEN_GMAIL = "c:/Agent Coco/token_gmail.json"

SCOPES_CAL   = ["https://www.googleapis.com/auth/calendar.readonly"]
SCOPES_GMAIL = ["https://www.googleapis.com/auth/gmail.readonly"]

from scripts.utils.audit_log import log_gmail_read

def get_creds(token_path, scopes):
    creds = Credentials.from_authorized_user_file(token_path, scopes)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

# ── GMAIL ──────────────────────────────────────────────────────────────────────
def search_gmail():
    creds = get_creds(TOKEN_GMAIL, SCOPES_GMAIL)
    service = build("gmail", "v1", credentials=creds)

    queries = [
        "subject:fundraising GWC",
        "subject:Zero In job32",
        "subject:Zero In fundraising",
        "mizhgan kirmani",
        "zain ul abideen",
        "hamdan ahmad",
        "fundraising partnerships manager debrief",
        "fundraising partnerships manager gwc",
    ]

    print("\n=== GMAIL SEARCH ===")
    for q in queries:
        results = service.users().messages().list(userId="me", q=q, maxResults=5).execute()
        msgs = results.get("messages", [])
        if msgs:
            print(f"\nQuery: {q!r} — {len(msgs)} result(s)")
            for m in msgs[:3]:
                msg = service.users().messages().get(userId="me", id=m["id"],
                                                      format="metadata",
                                                      metadataHeaders=["Subject","From","Date","To"]).execute()
                hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
                print(f"  Subject: {hdrs.get('Subject','')}")
                print(f"  From: {hdrs.get('From','')}")
                print(f"  Date: {hdrs.get('Date','')}")
                log_gmail_read(
                    query=q,
                    message_count=len(msgs),
                    context="fetch_job32_context"
                )
        else:
            print(f"Query: {q!r} — no results")

# ── CALENDAR ───────────────────────────────────────────────────────────────────
def search_calendar():
    creds = get_creds(TOKEN_CAL, SCOPES_CAL)
    service = build("calendar", "v3", credentials=creds)

    from datetime import datetime, timezone, timedelta
    now  = datetime.now(timezone.utc)
    past = (now - timedelta(days=60)).isoformat()
    future = (now + timedelta(days=60)).isoformat()

    print("\n=== CALENDAR SEARCH ===")
    events_result = service.events().list(
        calendarId="primary",
        timeMin=past,
        timeMax=future,
        maxResults=50,
        singleEvents=True,
        orderBy="startTime",
        q="Zero In"
    ).execute()
    events = events_result.get("items", [])
    print(f"\n'Zero In' events ({len(events)} found):")
    for e in events:
        start = e["start"].get("dateTime", e["start"].get("date",""))
        print(f"  {start} | {e.get('summary','')} | {[a.get('email','') for a in e.get('attendees',[])[:5]]}")

    # Also search for fundraising/Zain/Mizhgan/Hamdan
    for q in ["fundraising", "Zain", "Mizhgan", "Hamdan", "GWC"]:
        r2 = service.events().list(
            calendarId="primary",
            timeMin=past,
            timeMax=future,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
            q=q
        ).execute()
        evs = r2.get("items", [])
        if evs:
            print(f"\nCalendar query {q!r} — {len(evs)} result(s):")
            for e in evs:
                start = e["start"].get("dateTime", e["start"].get("date",""))
                print(f"  {start} | {e.get('summary','')} | attendees: {[a.get('email','') for a in e.get('attendees',[])[:5]]}")

if __name__ == "__main__":
    search_gmail()
    search_calendar()
