"""
Gmail Label Organiser — Taleemabad Talent Acquisition
Creates label hierarchy, labels existing emails, sets up filters for future emails.

Requires re-auth with broader scopes (modify + labels + settings).
Delete token_gmail_labels.json to force re-auth.
"""

import os, json, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Broader scopes needed for this script
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.settings.basic",
]

CREDS_FILE = "credentials.json"
TOKEN_FILE = "token_gmail_labels.json"

# ── Auth ──────────────────────────────────────────────────────────────────────

creds = None
if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())

service = build("gmail", "v1", credentials=creds)

# ── Label definitions ─────────────────────────────────────────────────────────

LABEL_TREE = {
    "Feedback": {
        "color": {"backgroundColor": "#16a766", "textColor": "#ffffff"},
        "children": {
            "Feedback/Initial Screening Feedback": {"color": {"backgroundColor": "#16a766", "textColor": "#ffffff"}},
            "Feedback/Values Call Feedback":       {"color": {"backgroundColor": "#16a766", "textColor": "#ffffff"}},
            "Feedback/GWC Not Cleared Feedback":   {"color": {"backgroundColor": "#285bac", "textColor": "#ffffff"}},
            "Feedback/Warm Bench":                 {"color": {"backgroundColor": "#4986e7", "textColor": "#ffffff"}},
        }
    },
    "Pilot": {
        "color": {"backgroundColor": "#e66550", "textColor": "#ffffff"},
        "children": {
            "Pilot/Screening Report (Pilot)":   {"color": {"backgroundColor": "#e66550", "textColor": "#ffffff"}},
            "Pilot/Values Invite (Pilot)":      {"color": {"backgroundColor": "#e66550", "textColor": "#ffffff"}},
            "Pilot/Values Feedback (Pilot)":    {"color": {"backgroundColor": "#e66550", "textColor": "#ffffff"}},
            "Pilot/Rejection Email (Pilot)":    {"color": {"backgroundColor": "#e66550", "textColor": "#ffffff"}},
        }
    },
    "Screening Analysis Reports": {
        "color": {"backgroundColor": "#8e63ce", "textColor": "#ffffff"},
        "children": {}
    },
}

# ── Create / fetch labels ─────────────────────────────────────────────────────

def get_existing_labels():
    result = service.users().labels().list(userId="me").execute()
    return {l["name"]: l["id"] for l in result.get("labels", [])}

def create_label(name, color):
    body = {
        "name": name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show",
        "color": color,
    }
    try:
        result = service.users().labels().create(userId="me", body=body).execute()
        print(f"  Created: {name}")
        return result["id"]
    except Exception as e:
        print(f"  Error creating {name}: {e}")
        return None

def ensure_labels():
    existing = get_existing_labels()
    label_ids = {}

    for parent, cfg in LABEL_TREE.items():
        if parent not in existing:
            lid = create_label(parent, cfg["color"])
        else:
            lid = existing[parent]
            print(f"  Exists:  {parent}")
        label_ids[parent] = lid

        for child, ccfg in cfg.get("children", {}).items():
            if child not in existing:
                clid = create_label(child, ccfg["color"])
            else:
                clid = existing[child]
                print(f"  Exists:  {child}")
            label_ids[child] = clid

    return label_ids

# ── Search and label messages ─────────────────────────────────────────────────

def search_messages(query, max_results=200):
    results = service.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()
    return [m["id"] for m in results.get("messages", [])]

def apply_label(message_ids, label_id, label_name):
    if not message_ids:
        print(f"  No messages found for: {label_name}")
        return
    # Gmail batch modify — up to 1000 at once
    chunks = [message_ids[i:i+100] for i in range(0, len(message_ids), 100)]
    total = 0
    for chunk in chunks:
        service.users().messages().batchModify(
            userId="me",
            body={"ids": chunk, "addLabelIds": [label_id]}
        ).execute()
        total += len(chunk)
        time.sleep(0.3)
    print(f"  Labelled {total} messages -> {label_name}")

# ── Email search queries per label ────────────────────────────────────────────

def build_label_queries():
    return {

        # ── FEEDBACK ────────────────────────────────────────────────────────

        "Feedback/Initial Screening Feedback": [
            'subject:"Your Application for Field Coordinator, Research & Impact Studies"',
            'subject:"Your Application for" -subject:"Invitation" -subject:"Pilot" -subject:"Zero In"',
        ],

        "Feedback/Values Call Feedback": [
            'subject:"Sehri, Iftari"',
            'subject:"Punjab handover"',
            'subject:"Values Interview Feedback" -subject:"PILOT" -subject:"[PILOT"',
        ],

        "Feedback/GWC Not Cleared Feedback": [
            'subject:"GWC" "feedback" -subject:"PILOT"',
            'subject:"GWC Not Cleared"',
        ],

        "Feedback/Warm Bench": [
            'subject:"warm bench" -subject:"PILOT"',
            'subject:"Keeping you in our pipeline"',
        ],

        # ── PILOT ────────────────────────────────────────────────────────────

        "Pilot/Screening Report (Pilot)": [
            'subject:"[PILOT]" "Rejection Drafts"',
            'subject:"[PILOT v2]" "Rejection Drafts"',
            'subject:"Screening Report" "PILOT"',
            'subject:"[PILOT] Job"',
        ],

        "Pilot/Values Invite (Pilot)": [
            'subject:"[PILOT]" "Values Interview"',
            'subject:"Invitation for the Values Interview" "PILOT"',
        ],

        "Pilot/Values Feedback (Pilot)": [
            'subject:"[PILOT" "Values Interview Feedback"',
            'subject:"[PILOT REVIEW]" "Values Interview Feedback"',
            'subject:"[PILOT v2]" "Values Interview Feedback"',
            'subject:"Sehri, Iftari" to:ayesha.khan@taleemabad.com',
            'subject:"Punjab handover" to:ayesha.khan@taleemabad.com',
        ],

        "Pilot/Rejection Email (Pilot)": [
            'subject:"[PILOT]" "Rejection"',
            'subject:"[PILOT v2]" "Rejection"',
            'subject:"Your Application for Field Coordinator" to:ayesha.khan@taleemabad.com',
        ],

        # ── SCREENING ANALYSIS REPORTS ───────────────────────────────────────

        "Screening Analysis Reports": [
            'subject:"Screening Report- Fundraising"',
            'subject:"Screening Report- Field Coordinator"',
            'subject:"Screening Report- Junior Research"',
            'subject:"Screening Report-" -subject:"PILOT"',
            'has:attachment filename:pdf subject:"Screening Report"',
        ],
    }

# ── Gmail filters for future emails ───────────────────────────────────────────

def create_filter(criteria_query, label_id, label_name):
    body = {
        "criteria": {"query": criteria_query},
        "action": {
            "addLabelIds": [label_id],
            "removeLabelIds": [],
        }
    }
    try:
        service.users().settings().filters().create(
            userId="me", body=body
        ).execute()
        print(f"  Filter created for: {label_name}")
    except Exception as e:
        if "already exists" in str(e).lower() or "409" in str(e):
            print(f"  Filter already exists: {label_name}")
        else:
            print(f"  Filter error ({label_name}): {e}")

FILTER_RULES = [
    # Feedback
    ('subject:"Your Application for Field Coordinator"',       "Feedback/Initial Screening Feedback"),
    ('subject:"Your Application for" -subject:"Invitation"',  "Feedback/Initial Screening Feedback"),
    ('subject:"Values Interview Feedback" -subject:"PILOT"',  "Feedback/Values Call Feedback"),
    ('subject:"GWC Not Cleared"',                             "Feedback/GWC Not Cleared Feedback"),
    ('subject:"Keeping you in our pipeline"',                 "Feedback/Warm Bench"),
    # Pilot
    ('subject:"[PILOT" "Rejection"',                          "Pilot/Rejection Email (Pilot)"),
    ('subject:"[PILOT" "Values Interview Feedback"',          "Pilot/Values Feedback (Pilot)"),
    ('subject:"[PILOT" "Values Interview"',                   "Pilot/Values Invite (Pilot)"),
    ('subject:"[PILOT" "Screening Report"',                   "Pilot/Screening Report (Pilot)"),
    # Screening Reports
    ('subject:"Screening Report-" has:attachment',            "Screening Analysis Reports"),
]

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("\n=== Creating labels ===")
    label_ids = ensure_labels()

    print("\n=== Labelling existing emails ===")
    queries = build_label_queries()
    labelled_total = 0

    for label_name, query_list in queries.items():
        lid = label_ids.get(label_name)
        if not lid:
            print(f"  Skipping {label_name} — label ID not found")
            continue

        all_ids = set()
        for q in query_list:
            ids = search_messages(q)
            all_ids.update(ids)
            time.sleep(0.2)

        apply_label(list(all_ids), lid, label_name)
        labelled_total += len(all_ids)

    print(f"\nTotal messages labelled: {labelled_total}")

    print("\n=== Setting up filters for future emails ===")
    for query, label_name in FILTER_RULES:
        lid = label_ids.get(label_name)
        if lid:
            create_filter(query, lid, label_name)
            time.sleep(0.2)

    print("\nDone. Your Gmail is organised.")
    print("Labels created:")
    for name in label_ids:
        print(f"  {name}")

if __name__ == "__main__":
    main()
