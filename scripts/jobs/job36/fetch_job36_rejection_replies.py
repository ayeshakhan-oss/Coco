"""
Fetch candidate replies to Job 36 rejection emails.
Searches Gmail for 'Re: Your Application for Field Coordinator' replies.
Prints full body of each reply for quote extraction.
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64, json

creds   = Credentials.from_authorized_user_file("token_gmail.json")
service = build("gmail", "v1", credentials=creds)

QUERY = 'subject:"Your Application for Field Coordinator" in:inbox'

def get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""

def decode_body(payload):
    """Recursively extract plain text from email payload."""
    mime = payload.get("mimeType", "")
    if mime == "text/plain":
        data = payload.get("body", {}).get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    if "parts" in payload:
        for part in payload["parts"]:
            result = decode_body(part)
            if result:
                return result
    return ""

results = service.users().messages().list(
    userId="me", q=QUERY, maxResults=50
).execute()

messages = results.get("messages", [])
print(f"Found {len(messages)} matching emails\n{'='*60}")

replies = []
for m in messages:
    msg = service.users().messages().get(
        userId="me", id=m["id"], format="full"
    ).execute()
    headers = msg["payload"].get("headers", [])
    sender  = get_header(headers, "From")
    subject = get_header(headers, "Subject")
    date    = get_header(headers, "Date")
    body    = decode_body(msg["payload"])

    # skip emails sent by Coco / Ayesha
    if "ayesha.khan@taleemabad.com" in sender.lower():
        continue

    replies.append({
        "sender":  sender,
        "subject": subject,
        "date":    date,
        "body":    body[:2000]
    })

print(f"Candidate replies found: {len(replies)}\n")
for i, r in enumerate(replies, 1):
    print(f"--- Reply {i} ---")
    print(f"From:    {r['sender']}")
    print(f"Subject: {r['subject']}")
    print(f"Date:    {r['date']}")
    print(f"Body:\n{r['body']}")
    print()

with open("job36_rejection_replies.json", "w", encoding="utf-8") as f:
    json.dump(replies, f, indent=2, ensure_ascii=False)
print("Saved to job36_rejection_replies.json")
