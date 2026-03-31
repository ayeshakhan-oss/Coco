"""
Fetch two reference emails from Gmail - output to UTF-8 file
"""

import os, base64, sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_FILE = "token_gmail.json"

creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())

service = build("gmail", "v1", credentials=creds)

def get_parts(payload):
    parts = []
    def collect(p):
        if "parts" in p:
            for sub in p["parts"]: collect(sub)
        mime = p.get("mimeType", "")
        data = p.get("body", {}).get("data", "")
        if data and mime in ("text/plain", "text/html"):
            text = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            parts.append((mime, text))
    collect(payload)
    return parts

def best_body(payload):
    parts = get_parts(payload)
    # Prefer plain text; if only HTML, strip tags
    for mime, content in parts:
        if mime == "text/plain" and content.strip() and "view this email in" not in content:
            return content
    for mime, content in parts:
        if mime == "text/html":
            return BeautifulSoup(content, "html.parser").get_text(separator="\n")
    return ""

def fetch(query, max_results=1):
    results = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
    messages = results.get("messages", [])
    out = []
    for m in messages:
        msg = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        body = best_body(msg["payload"])
        out.append({
            "subject": headers.get("Subject", ""),
            "from":    headers.get("From", ""),
            "date":    headers.get("Date", ""),
            "body":    body
        })
    return out

lines = []

lines.append("=" * 80)
lines.append("SEARCH 1: Rumi training guide — candidate feedback subjects")
lines.append("=" * 80)
for e in fetch("from:rumi subject:Candidate Feedback Training", max_results=1):
    lines.append(f"Subject : {e['subject']}")
    lines.append(f"From    : {e['from']}")
    lines.append(f"Date    : {e['date']}")
    lines.append(f"Body    :\n{e['body'][:10000]}")
    lines.append("-" * 80)

lines.append("")
lines.append("=" * 80)
lines.append("SEARCH 2: Jawwad to Talal Hassan Khan — The Intercept")
lines.append("=" * 80)
for e in fetch("subject:Intercept Talal", max_results=2):
    lines.append(f"Subject : {e['subject']}")
    lines.append(f"From    : {e['from']}")
    lines.append(f"Date    : {e['date']}")
    lines.append(f"Body    :\n{e['body'][:10000]}")
    lines.append("-" * 80)

# Also try broader search
lines.append("")
lines.append("=" * 80)
lines.append("SEARCH 3: Intercept (broader)")
lines.append("=" * 80)
for e in fetch("subject:Intercept", max_results=3):
    lines.append(f"Subject : {e['subject']}")
    lines.append(f"From    : {e['from']}")
    lines.append(f"Date    : {e['date']}")
    lines.append(f"Body    :\n{e['body'][:6000]}")
    lines.append("-" * 80)

with open("read_emails_output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Done. Output written to read_emails_output.txt")
