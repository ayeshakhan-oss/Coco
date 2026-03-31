"""
Check Gmail for Field Coordinator (Job 36) case study submissions.
Searches for emails from known candidates + any case study subject lines.
"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from scripts.utils.audit_log import log_gmail_read
from scripts.utils.check_token_expiry import check_all_tokens

check_all_tokens(print_output=True)
creds = Credentials.from_authorized_user_file("token_gmail.json")
service = build("gmail", "v1", credentials=creds)

# All candidates sent the case study (confirmed via Markaz Candidate Communications)
# DB status is NOT reliable — some remain 'shortlisted' even after case study was sent
KNOWN_CANDIDATES = [
    {"name": "Scheherazade Noor", "email": "noorscheherazade@gmail.com"},
    {"name": "Jalal Ud Din",      "email": "jalalsaraikhan@gmail.com"},
    {"name": "Amina Batool",      "email": "aminabatool2000@gmail.com"},
    {"name": "Maria Karim",       "email": "mariakarim1013@gmail.com"},
    {"name": "Usman Ahmed Khan",  "email": "usmanumar646@gmail.com"},
]

def get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""

def has_attachments(payload):
    for part in payload.get("parts", []):
        if part.get("filename") and part["filename"].strip():
            return True, part["filename"]
    return False, None

def search_gmail(query):
    results = service.users().messages().list(userId="me", q=query, maxResults=20).execute()
    msgs = results.get("messages", [])
    log_gmail_read(query=query, message_count=len(msgs), context="check_job36_case_study_submissions")
    return msgs

found = []

# Search by each known candidate's email
for candidate in KNOWN_CANDIDATES:
    query = f"from:{candidate['email']}"
    messages = search_gmail(query)
    for m in messages:
        msg = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
        headers = msg["payload"].get("headers", [])
        subject = get_header(headers, "Subject")
        date    = get_header(headers, "Date")
        snippet = msg.get("snippet", "")[:200]
        has_att, filename = has_attachments(msg["payload"])

        found.append({
            "candidate": candidate["name"],
            "from":      candidate["email"],
            "subject":   subject,
            "date":      date,
            "has_attachment": has_att,
            "attachment_name": filename or "none",
            "snippet":   snippet,
            "source":    "known candidate search"
        })

# Also search broadly for case study subject lines for this role
broad_queries = [
    "subject:case study field coordinator",
    "subject:case study research",
    "subject:case study submission",
]
for query in broad_queries:
    messages = search_gmail(query)
    for m in messages:
        msg = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
        headers  = msg["payload"].get("headers", [])
        sender   = get_header(headers, "From")
        subject  = get_header(headers, "Subject")
        date     = get_header(headers, "Date")
        snippet  = msg.get("snippet", "")[:200]
        has_att, filename = has_attachments(msg["payload"])

        # Skip if already captured from known candidate search
        already = any(r["from"] in sender for r in found)
        if not already:
            found.append({
                "candidate": "UNKNOWN — not in Markaz DB",
                "from":      sender,
                "subject":   subject,
                "date":      date,
                "has_attachment": has_att,
                "attachment_name": filename or "none",
                "snippet":   snippet,
                "source":    f"broad search: {query}"
            })

def safe(s):
    return s.encode("ascii", errors="replace").decode("ascii") if s else ""

print(f"\n=== FIELD COORDINATOR (JOB 36) - GMAIL CASE STUDY SCAN ===")
print(f"Total emails found: {len(found)}\n")
for i, r in enumerate(found, 1):
    print(f"[{i}] {safe(r['candidate'])}")
    print(f"    From:       {safe(r['from'])}")
    print(f"    Subject:    {safe(r['subject'])}")
    print(f"    Date:       {safe(r['date'])}")
    print(f"    Attachment: {safe(r['attachment_name'])}")
    print(f"    Snippet:    {safe(r['snippet'][:120])}")
    print(f"    Source:     {safe(r['source'])}")
    print()

with open("job36_case_study_gmail_check.json", "w", encoding="utf-8") as f:
    json.dump(found, f, indent=2, ensure_ascii=False)
print("Saved to job36_case_study_gmail_check.json")
