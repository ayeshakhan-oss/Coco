"""
Automated Weekly Hiring Pipeline Monitor — Text Version
========================================================
Runs twice weekly (Monday 10:30am, Friday 3pm).
Checks all open positions across Markaz + Gmail + Calendar.
Sends plain-text report with candidate pipeline status.
"""

import os
import sys
import smtplib
import psycopg2
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from scripts.utils.safe_send import safe_sendmail
from scripts.utils.audit_log import log_db_query, log_gmail_read

load_dotenv()

# CONFIG
DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode": "require",
}

TOKEN_GMAIL = os.path.join(os.path.dirname(__file__), "../..", "token_gmail.json")
SCOPES_GMAIL = ["https://www.googleapis.com/auth/gmail.readonly"]

EMAIL_USER = os.getenv("EMAIL_USER", "ayesha.khan@taleemabad.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465

RECIPIENTS_TO = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
RECIPIENTS_CC = ["hiring@taleemabad.com"]

DAYS_FLAG = 3
DAYS_URGENT = 14

# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

def get_open_jobs():
    """Fetch all active job positions."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    query = """
        SELECT j.id, j.job_id, j.title, j.department,
               j.hiring_manager, u.email as hm_email, u.first_name as hm_first_name
        FROM jobs j
        LEFT JOIN users u ON j.hiring_manager = u.id
        WHERE j.job_status = 'Active'
        ORDER BY j.created_at DESC
    """

    cur.execute(query)
    rows = cur.fetchall()
    log_db_query(query, len(rows), "pipeline_monitor_open_jobs")

    jobs = []
    for row in rows:
        jobs.append({
            "id": row[0],
            "job_id": row[1],
            "title": row[2],
            "department": row[3],
            "hm_id": row[4],
            "hm_email": row[5],
            "hm_first_name": row[6],
        })

    conn.close()
    return jobs


def get_candidates_for_job(job_id):
    """Fetch all shortlisted+ candidates for a job."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    query = """
        SELECT a.id, c.first_name, c.last_name, c.email,
               a.status, a.applied_at,
               a.values_interview_result, a.values_interview_date,
               a.gwc_scorecard, a.gwc_interview_date
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = %s
          AND (a.status != 'applied' OR a.values_interview_result IS NOT NULL)
        ORDER BY a.applied_at DESC
    """

    cur.execute(query, (job_id,))
    rows = cur.fetchall()
    log_db_query(query, len(rows), f"pipeline_monitor_job_{job_id}")

    candidates = []
    for row in rows:
        candidates.append({
            "app_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "email": row[3],
            "status": row[4],
            "applied_at": row[5],
            "values_result": row[6],
            "values_date": row[7],
            "gwc_scorecard": row[8],
            "gwc_date": row[9],
        })

    conn.close()
    return candidates

# ═══════════════════════════════════════════════════════════════════════════════
# GMAIL
# ═══════════════════════════════════════════════════════════════════════════════

def get_gmail_service():
    """Authenticate and return Gmail service."""
    creds = Credentials.from_authorized_user_file(TOKEN_GMAIL, SCOPES_GMAIL)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)


def check_values_invite_sent(service, candidate_email):
    """Check if values interview invite was sent to candidate."""
    q = f'to:{candidate_email} subject:(Invitation for Values OR "Zero In")'
    try:
        results = service.users().messages().list(userId="me", q=q, maxResults=1).execute()
        log_gmail_read(q, 1, "check_values_invite")
        msgs = results.get("messages", [])
        return bool(msgs)
    except:
        return False


def check_case_study_sent(service, candidate_email):
    """Check if case study was sent to candidate."""
    q = f'to:{candidate_email} subject:(case study OR KCD assignment)'
    try:
        results = service.users().messages().list(userId="me", q=q, maxResults=1).execute()
        log_gmail_read(q, 1, "check_case_study_sent")
        msgs = results.get("messages", [])
        return bool(msgs)
    except:
        return False


def check_debrief_invite_sent(service, candidate_email):
    """Check if debrief invite was sent to candidate."""
    q = f'to:{candidate_email} subject:(debrief OR GWC discussion)'
    try:
        results = service.users().messages().list(userId="me", q=q, maxResults=1).execute()
        log_gmail_read(q, 1, "check_debrief_invite")
        msgs = results.get("messages", [])
        return bool(msgs)
    except:
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# REPORT BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_report_text(jobs_data):
    """Build plain-text report."""
    now = datetime.now()
    date_str = now.strftime("%A, %d %B %Y")
    day_str = now.strftime("%A")

    report = f"""
HIRING PIPELINE UPDATE — {date_str}
{"=" * 80}

Total Open Positions: {len(jobs_data)}

CANDIDATE STATUS BY POSITION
{"-" * 80}

"""

    for job in jobs_data:
        candidates = job.get("candidates", [])
        urgent_cands = [c for c in candidates if c["urgency"] == "urgent"]
        flagged_cands = [c for c in candidates if c["urgency"] == "flagged"]
        other_cands = [c for c in candidates if c["urgency"] == "normal"]

        report += f"\n{job['title']}\n"
        report += f"Hiring Manager: {job.get('hm_first_name', 'TBD')}\n"
        report += f"Candidates in Pipeline: {len(candidates)}\n"
        report += "-" * 80 + "\n"

        # URGENT first
        if urgent_cands:
            report += "\n[🔴 URGENT — 14+ days stuck]\n"
            for c in urgent_cands:
                report += f"  • {c['first_name']} {c['last_name']} (Days stuck: {c['classification']['days_stuck']})\n"
                report += f"    Stage: {c['classification']['stage']}\n"
                report += f"    Action: {c['classification']['next_action']}\n\n"

        # FLAGGED
        if flagged_cands:
            report += "\n[⚠️ FLAGGED — 3-14 days stuck]\n"
            for c in flagged_cands:
                report += f"  • {c['first_name']} {c['last_name']} (Days stuck: {c['classification']['days_stuck']})\n"
                report += f"    Stage: {c['classification']['stage']}\n"
                report += f"    Action: {c['classification']['next_action']}\n\n"

        # NORMAL
        if other_cands:
            report += f"\n[✓ OK — {len(other_cands)} candidate(s)]\n"
            for c in other_cands:
                report += f"  • {c['first_name']} {c['last_name']} — {c['classification']['stage']}\n"

        report += "\n" + "=" * 80 + "\n"

    report += """
NEXT ACTIONS
{-} — Follow up with shortlisted candidates not yet invited to values interviews
{-} — Send case study assignments to values-passed candidates
{-} — Schedule debriefs with case study submissions
{-} — Make panel decisions for debrief-completed candidates

---
Report compiled by Coco • Hiring Pipeline Monitor
Runs: Monday 10:30am + Friday 3:00pm
""".format("-" * 80, "-" * 80)

    return report

# ═══════════════════════════════════════════════════════════════════════════════
# CLASSIFY & SEND
# ═══════════════════════════════════════════════════════════════════════════════

def classify_candidate(cand):
    """Classify candidate into pipeline stage."""
    now = datetime.now(timezone.utc)
    last_date = cand["applied_at"]
    if cand["values_date"]:
        last_date = cand["values_date"]
    if cand["gwc_date"]:
        last_date = cand["gwc_date"]

    if isinstance(last_date, str):
        last_date = datetime.fromisoformat(last_date.replace("Z", "+00:00"))
    elif last_date and last_date.tzinfo is None:
        last_date = last_date.replace(tzinfo=timezone.utc)

    days_stuck = (now - last_date).days if last_date else 0
    urgency = "urgent" if days_stuck >= DAYS_URGENT else "flagged" if days_stuck >= DAYS_FLAG else "normal"

    # Simplified stage logic
    if cand["values_result"] == "fail":
        stage = "Values Failed"
        action = "Send warm rejection"
    elif cand["values_result"] == "pass":
        if cand["gwc_scorecard"]:
            stage = "Debrief Completed"
            action = "Panel decision pending"
        else:
            stage = "Case Study In"
            action = "Send debrief invite"
    elif cand["status"] == "shortlisted":
        stage = "Shortlisted"
        action = "Send values interview invite"
    else:
        stage = "In Pipeline"
        action = "Monitor progress"

    return {
        "stage": stage,
        "days_stuck": days_stuck,
        "next_action": action,
        "urgency": urgency
    }


def send_report(text):
    """Send the report via email."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Hiring Pipeline Update — {datetime.now().strftime('%A, %d %b %Y')}"
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(RECIPIENTS_TO)
    msg["Cc"] = ", ".join(RECIPIENTS_CC)

    msg.attach(MIMEText(text, "plain"))

    try:
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            all_recipients = RECIPIENTS_TO + RECIPIENTS_CC
            safe_sendmail(server, EMAIL_USER, all_recipients, msg.as_string(), context="hiring_pipeline_monitor_text")
        print("[Send] Report sent successfully")
        return True
    except Exception as e:
        print(f"[Send] Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Run the full pipeline monitor."""
    print(f"[Pipeline Monitor] Starting run at {datetime.now().isoformat()}", flush=True)

    try:
        print("[DB] Fetching open positions...")
        jobs = get_open_jobs()
        print(f"[DB] Found {len(jobs)} open position(s)")

        if not jobs:
            print("[Monitor] No open positions. Exiting.")
            return

        gmail_service = get_gmail_service()
        print("[Auth] Authenticated to Gmail")

        jobs_data = []

        for job in jobs:
            print(f"[Job] Processing {job['title']}")

            candidates = get_candidates_for_job(job["id"])
            print(f"  > {len(candidates)} candidate(s) in pipeline")

            candidates_data = []

            for cand in candidates:
                # Check Gmail status
                values_sent = check_values_invite_sent(gmail_service, cand["email"])
                case_study_sent = check_case_study_sent(gmail_service, cand["email"])
                debrief_sent = check_debrief_invite_sent(gmail_service, cand["email"])

                # For classification, use simplified logic based on DB + Gmail
                if values_sent:
                    if debrief_sent:
                        cand["values_result"] = "pass"
                    elif case_study_sent:
                        cand["values_result"] = "pass"

                classification = classify_candidate(cand)

                candidates_data.append({
                    "first_name": cand["first_name"],
                    "last_name": cand["last_name"],
                    "email": cand["email"],
                    "classification": classification,
                })

            jobs_data.append({
                "id": job["id"],
                "title": job["title"],
                "hm_first_name": job["hm_first_name"],
                "candidates": candidates_data,
            })

        print("[Report] Building text report...")
        text = build_report_text(jobs_data)

        print("[Send] Sending report...")
        success = send_report(text)

        if success:
            print("[Pipeline Monitor] Run completed successfully")
        else:
            print("[Pipeline Monitor] Run completed with send error")

    except Exception as e:
        print(f"[Error] Pipeline monitor failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
