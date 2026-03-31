"""
Scan inbox for emails needing a response.
Returns unread emails (excluding automated/sent by Coco).
"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64, email, json, os, sys
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.audit_log import log_gmail_read
from scripts.utils.check_token_expiry import check_all_tokens

check_all_tokens(print_output=True)
creds   = Credentials.from_authorized_user_file("token_gmail.json")
service = build("gmail", "v1", credentials=creds)

SKIP_SENDERS = [
    "ayesha.khan@taleemabad.com",  # self / sent by Coco
    "noreply", "no-reply", "notifications@", "calendar-notification",
    "mailer-daemon", "postmaster", "google.com", "accounts.google.com",
]

def should_skip(sender):
    s = sender.lower()
    return any(skip in s for skip in SKIP_SENDERS)

def get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""

def decode_body(payload):
    """Extract plain text from email payload."""
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")[:500]
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data", "")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")[:500]
    return ""

def scan_unread(max_results=50):
    query = "is:unread in:inbox -from:me"
    results = service.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()
    messages = results.get("messages", [])
    log_gmail_read(query=query, message_count=len(messages), context="gmail_scan_inbox")
    print(f"Found {len(messages)} unread emails in inbox")

    emails_needing_response = []
    for m in messages:
        msg = service.users().messages().get(
            userId="me", id=m["id"], format="full"
        ).execute()
        headers  = msg["payload"].get("headers", [])
        sender   = get_header(headers, "From")
        subject  = get_header(headers, "Subject")
        date_str = get_header(headers, "Date")
        snippet  = msg.get("snippet", "")

        if should_skip(sender):
            continue

        body_preview = decode_body(msg["payload"])

        emails_needing_response.append({
            "id":      m["id"],
            "sender":  sender,
            "subject": subject,
            "date":    date_str,
            "snippet": snippet[:200],
        })

    return emails_needing_response

if __name__ == "__main__":
    emails = scan_unread(50)
    output = json.dumps(emails, indent=2, ensure_ascii=True)
    with open("inbox_scan_results.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(emails, indent=2, ensure_ascii=False))
    print(f"Saved {len(emails)} emails to inbox_scan_results.json")
