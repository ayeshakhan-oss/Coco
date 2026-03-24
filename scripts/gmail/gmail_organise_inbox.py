"""
Gmail Inbox Organiser — Taleemabad Talent Acquisition
1. Creates sub-labels under Hiring for all active positions
2. Scans inbox and applies position labels based on subject/content
3. Applies Values Invitation Sent / Case Study Sent where relevant
"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import time

creds   = Credentials.from_authorized_user_file("token_gmail.json")
service = build("gmail", "v1", credentials=creds)

# ── Existing label IDs ─────────────────────────────────────────────────────────
HIRING_ID              = "Label_2013661190210968529"
VALUES_SENT_ID         = "Label_628840849049638343"   # Hiring/Values Invitation Sent
CASE_STUDY_SENT_ID     = "Label_325856810558173157"   # Hiring/Case Study Sent

# ── Positions to create sub-labels for ────────────────────────────────────────
POSITIONS = [
    (10, "Head of Accounts & Finance"),
    (13, "Full Stack Developer"),
    (17, "CPD Coach"),
    (20, "Senior Product Manager"),
    (23, "Program Manager"),
    (24, "Full Stack Lead"),
    (26, "Soul Architect / Conversational UX Designer"),
    (31, "Training Manager"),
    (32, "Fundraising & Partnerships Manager"),
    (33, "Fundraising & Partnerships Lead"),
    (34, "Odoo Developer"),
    (35, "Junior Research Associate – Impact & Policy"),
    (36, "Field Coordinator – Research & Impact Studies"),
]

# ── Extra labels (name, backgroundColor, textColor) ───────────────────────────
EXTRA_LABELS = [
    ("Hiring/Contract Drafting", "#ffad47", "#000000"),   # orange  — in progress
    ("Hiring/Contract Sent",     "#16a766", "#ffffff"),   # green   — done/sent
    ("Hiring/Offer Extended",    "#4a86e8", "#ffffff"),   # blue    — offer stage
    ("Hiring/Onboarding",        "#43d692", "#000000"),   # teal    — new hire
    ("P&C Query",                "#a479e2", "#ffffff"),   # purple  — non-TA
]

# ── Candidate emails we know about (for labelling replies) ───────────────────
JOB35_CANDIDATES = [
    "rameezwasif1@gmail.com", "fatimachohan110@gmail.com",
    "rabiya.baloch.31@gmail.com", "hadiyahshaheen01@gmail.com",
    "hassanzafar8004474@gmail.com", "durenayab349@gmail.com",
    "rahimaomar321@gmail.com", "wasifmehdi550@gmail.com",
    "zeeshanali.gzr55@gmail.com", "mahnoorhasan122@gmail.com",
    "malik_maria99@hotmail.com", "ayeshanadeem2408@gmail.com",
]

JOB36_CANDIDATES = [
    # Top 17 from Job 36 values invite list (from memory)
    "aminabatool", "scheherazade", "faryal", "mariam",
]

# ── Helper: get or create a label (with optional colour) ──────────────────────
def get_or_create_label(name, bg_color=None, text_color=None):
    existing = service.users().labels().list(userId="me").execute().get("labels", [])
    for l in existing:
        if l["name"].lower() == name.lower():
            print(f"  Label exists: {name}")
            return l["id"]
    body = {
        "name": name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show",
    }
    if bg_color:
        body["color"] = {"backgroundColor": bg_color, "textColor": text_color or "#ffffff"}
    result = service.users().labels().create(userId="me", body=body).execute()
    print(f"  Created: {name} [{result['id']}]")
    return result["id"]

# ── Helper: search and label messages ─────────────────────────────────────────
def label_messages(query, label_ids, max_results=100):
    results = service.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()
    messages = results.get("messages", [])
    if not messages:
        return 0
    ids = [m["id"] for m in messages]
    # Batch modify
    service.users().messages().batchModify(
        userId="me",
        body={"ids": ids, "addLabelIds": label_ids}
    ).execute()
    return len(ids)

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Gmail Inbox Organiser — Taleemabad")
    print("=" * 60)

    # Step 1: Create position sub-labels
    print("\n[1] Creating position sub-labels under Hiring...")
    position_labels = {}
    for job_id, title in POSITIONS:
        label_name = f"Hiring/{title}"
        lid = get_or_create_label(label_name)
        position_labels[job_id] = lid
        time.sleep(0.3)  # avoid rate limit

    # Step 2: Apply labels to emails by position keywords
    print("\n[2] Labelling inbox emails by position...")

    label_rules = [
        (10, '"Head of Accounts" OR "Accounts & Finance"'),
        (13, '"Full Stack Developer"'),
        (17, '"CPD Coach"'),
        (20, '"Senior Product Manager"'),
        (23, '"Program Manager"'),
        (24, '"Full Stack Lead"'),
        (26, '"Soul Architect" OR "Conversational UX"'),
        (31, '"Training Manager"'),
        (32, '"Fundraising & Partnerships Manager"'),
        (33, '"Fundraising & Partnerships Lead"'),
        (34, '"Odoo Developer"'),
        (35, '"Junior Research Associate" OR "Impact & Policy"'),
        (36, '"Field Coordinator" OR "Research & Impact Studies"'),
    ]

    total_labelled = 0
    for job_id, query in label_rules:
        lid = position_labels[job_id]
        count = label_messages(query, [lid, HIRING_ID])
        print(f"  Job {job_id}: {count} emails labelled")
        total_labelled += count
        time.sleep(0.3)

    # Step 3: Label Values Invitation Sent emails
    print("\n[3] Labelling Values Invitation emails...")
    vi_query = '"Values Interview" OR "values call" OR "Zero In Call" OR "Book your Interview"'
    vi_count = label_messages(vi_query, [VALUES_SENT_ID, HIRING_ID])
    print(f"  {vi_count} emails labelled as Values Invitation Sent")

    # Step 4: Label Job 35 candidate replies
    print("\n[4] Labelling Job 35 candidate emails...")
    j35_query = " OR ".join(f"from:{e}" for e in JOB35_CANDIDATES)
    j35_count = label_messages(j35_query, [position_labels[35], HIRING_ID])
    j35_query2 = " OR ".join(f"to:{e}" for e in JOB35_CANDIDATES)
    j35_count2 = label_messages(j35_query2, [position_labels[35], HIRING_ID])
    print(f"  {j35_count + j35_count2} Job 35 candidate emails labelled")

    # Step 5: Label screening report emails
    print("\n[5] Labelling screening report emails...")
    report_query = '"Screening Report" OR "screening report"'
    r_count = label_messages(report_query, [HIRING_ID])
    print(f"  {r_count} screening report emails labelled under Hiring")

    # Step 6: Create & apply extra labels (contract, offer, onboarding, P&C)
    print("\n[6] Creating and applying extra labels...")
    extra_ids = {}
    for label_name, bg, fg in EXTRA_LABELS:
        lid = get_or_create_label(label_name, bg, fg)
        extra_ids[label_name] = lid
        time.sleep(0.3)

    extra_rules = [
        ("Hiring/Contract Drafting", '"contract draft" OR "draft the contract" OR "draft contract" OR "draft offer"'),
        ("Hiring/Contract Sent",     '"contract sent" OR "please find the contract" OR "attached contract" OR "employment contract" OR "offer letter attached"'),
        ("Hiring/Offer Extended",    '"offer extended" OR "job offer" OR "pleased to offer" OR "offer letter" OR "verbal offer"'),
        ("Hiring/Onboarding",        '"onboarding" OR "joining date" OR "first day" OR "welcome aboard" OR "orientation" OR "joining formalities"'),
        ("P&C Query",                '"P&C" OR "people and culture" OR "leave policy" OR "payroll" OR "attendance policy" OR "HR policy" OR "employee query"'),
    ]

    extra_count = 0
    for label_name, query in extra_rules:
        lid = extra_ids[label_name]
        apply_ids = [lid, HIRING_ID] if label_name.startswith("Hiring/") else [lid]
        count = label_messages(query, apply_ids)
        print(f"  {label_name}: {count} emails labelled")
        extra_count += count
        time.sleep(0.3)

    print(f"\nDone. Total emails labelled: ~{total_labelled + vi_count + j35_count + j35_count2 + r_count + extra_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
