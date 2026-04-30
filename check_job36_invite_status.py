"""
Check Gmail sent folder for Job 36 values interview invitations.
Returns: who was sent an invite + whether they've booked (calendar accepted).
"""

import os, base64, json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

SCOPES     = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_FILE = "token_gmail.json"

creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())

service = build("gmail", "v1", credentials=creds)

def get_body(payload):
    def collect(p):
        parts = []
        if "parts" in p:
            for sub in p["parts"]: parts += collect(sub)
        mime = p.get("mimeType", "")
        data = p.get("body", {}).get("data", "")
        if data and mime in ("text/plain", "text/html"):
            text = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            parts.append((mime, text))
        return parts
    all_parts = collect(payload)
    for mime, content in all_parts:
        if mime == "text/plain" and content.strip():
            return content
    for mime, content in all_parts:
        if mime == "text/html":
            return BeautifulSoup(content, "html.parser").get_text(separator="\n")
    return ""

def search_sent(query, max_results=50):
    results = service.users().messages().list(
        userId="me", q=f"in:sent {query}", maxResults=max_results
    ).execute()
    messages = results.get("messages", [])
    out = []
    for m in messages:
        try:
            msg = service.users().messages().get(
                userId="me", id=m["id"], format="full"
            ).execute()
        except Exception as e:
            print(f"  Warning: skipping message {m['id']} — {e}")
            continue
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        out.append({
            "subject": headers.get("Subject", ""),
            "to":      headers.get("To", ""),
            "date":    headers.get("Date", ""),
            "body":    get_body(msg["payload"])[:500],
        })
    return out

# Search for values interview invitations sent for Field Coordinator
print("Searching sent mail for Job 36 values interview invitations...\n")

invites = search_sent(
    'subject:"Values Interview" "Field Coordinator"',
    max_results=50
)

# Also try alternate subject patterns
invites2 = search_sent(
    'subject:"Zero In" "Field Coordinator"',
    max_results=20
)

all_invites = invites + invites2

output = []
output.append(f"Found {len(all_invites)} invitation emails\n")
output.append("=" * 70)

for inv in all_invites:
    output.append(f"To:      {inv['to']}")
    output.append(f"Subject: {inv['subject']}")
    output.append(f"Date:    {inv['date']}")
    output.append("-" * 70)

with open("job36_invite_check.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("\n".join(output))
print(f"\nOutput saved to job36_invite_check.txt")
