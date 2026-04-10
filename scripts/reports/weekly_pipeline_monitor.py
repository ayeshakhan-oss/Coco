"""
Automated Weekly Hiring Pipeline Monitor
=========================================
Runs twice weekly (Monday 10:30am, Friday 3pm).
Checks all open positions across Markaz + Gmail + Calendar.
Flags candidates stuck at pipeline stages.
Sends comprehensive report to Ayesha + Jawwad.
"""

import os
import sys
import json
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

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode": "require",
}

TOKEN_GMAIL = os.path.join(os.path.dirname(__file__), "../..", "token_gmail.json")
TOKEN_CAL = os.path.join(os.path.dirname(__file__), "../..", "token.json")

SCOPES_GMAIL = ["https://www.googleapis.com/auth/gmail.readonly"]
SCOPES_CAL = ["https://www.googleapis.com/auth/calendar.readonly"]

EMAIL_USER = os.getenv("EMAIL_USER", "ayesha.khan@taleemabad.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465

# Recipients
RECIPIENTS_TO = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
RECIPIENTS_CC = ["hiring@taleemabad.com"]

# Escalation thresholds
DAYS_FLAG = 3
DAYS_URGENT = 14

# Color palette (v8+ design, bluish theme)
COLOR_GREEN = "#2e7a4f"  # Taleemabad green
COLOR_BLUE = "#1565c0"   # Primary blue
COLOR_RED = "#c62828"    # Urgent red
COLOR_AMBER = "#f57c00"  # Warning amber
COLOR_GRAY = "#f5f5f5"   # Row background
COLOR_BORDER = "#ddd"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: DATABASE LAYER
# ═══════════════════════════════════════════════════════════════════════════════

def get_open_jobs():
    """Fetch all active job positions with hiring manager emails."""
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
        SELECT a.id, a.candidate_id, c.first_name, c.last_name, c.email,
               a.status, a.applied_at,
               a.values_interview_result, a.values_interview_date, a.values_scorecard,
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
            "candidate_id": row[1],
            "first_name": row[2],
            "last_name": row[3],
            "email": row[4],
            "status": row[5],
            "applied_at": row[6],
            "values_result": row[7],
            "values_date": row[8],
            "values_scorecard": row[9],
            "gwc_scorecard": row[10],
            "gwc_date": row[11],
        })

    conn.close()
    return candidates

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: GMAIL LAYER
# ═══════════════════════════════════════════════════════════════════════════════

def get_gmail_service():
    """Authenticate and return Gmail service."""
    creds = Credentials.from_authorized_user_file(TOKEN_GMAIL, SCOPES_GMAIL)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)


def check_values_invite_sent(service, candidate_email, position_title):
    """Check if values interview invite was sent to candidate. Returns (bool, date_str)."""
    q = f'to:{candidate_email} subject:(Invitation for Values OR "Zero In")'

    try:
        results = service.users().messages().list(userId="me", q=q, maxResults=1).execute()
        log_gmail_read(q, 1, "check_values_invite")

        msgs = results.get("messages", [])
        if msgs:
            return True, ""
        return False, None
    except Exception as e:
        return False, None


def check_case_study_sent(service, candidate_email):
    """Check if case study was sent to candidate."""
    q = f'to:{candidate_email} subject:(case study OR KCD assignment)'

    try:
        results = service.users().messages().list(userId="me", q=q, maxResults=1).execute()
        log_gmail_read(q, 1, "check_case_study_sent")

        msgs = results.get("messages", [])
        return (True, "") if msgs else (False, None)
    except Exception as e:
        return False, None


def check_debrief_invite_sent(service, candidate_email):
    """Check if debrief invite was sent to candidate."""
    q = f'to:{candidate_email} subject:(debrief OR GWC discussion)'

    try:
        results = service.users().messages().list(userId="me", q=q, maxResults=1).execute()
        log_gmail_read(q, 1, "check_debrief_invite")

        msgs = results.get("messages", [])
        return (True, "") if msgs else (False, None)
    except Exception as e:
        return False, None

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: CALENDAR LAYER
# ═══════════════════════════════════════════════════════════════════════════════

def get_calendar_service():
    """Authenticate and return Calendar service."""
    creds = Credentials.from_authorized_user_file(TOKEN_CAL, SCOPES_CAL)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("calendar", "v3", credentials=creds)


def check_values_booked(service, candidate_email):
    """Check if values interview is booked. Returns (bool, start_dt, is_past)."""
    now = datetime.now(timezone.utc)
    past = (now - timedelta(days=60)).isoformat()
    future = (now + timedelta(days=60)).isoformat()

    try:
        results = service.events().list(
            calendarId="primary",
            timeMin=past,
            timeMax=future,
            q="Zero In",
            singleEvents=True,
            maxResults=30
        ).execute()

        events = results.get("items", [])
        for event in events:
            attendees = [a.get("email", "") for a in event.get("attendees", [])]
            if candidate_email in attendees:
                start_dt = event["start"].get("dateTime")
                if start_dt:
                    is_past = datetime.fromisoformat(start_dt.replace("Z", "+00:00")) < now
                    return True, start_dt, is_past
        return False, None, False
    except Exception as e:
        print(f"[Calendar] Error checking values booking for {candidate_email}: {e}")
        return False, None, False


def check_debrief_booked(service, candidate_email):
    """Check if debrief is booked. Returns (bool, start_dt, is_past)."""
    now = datetime.now(timezone.utc)
    past = (now - timedelta(days=60)).isoformat()
    future = (now + timedelta(days=60)).isoformat()

    try:
        results = service.events().list(
            calendarId="primary",
            timeMin=past,
            timeMax=future,
            q="Debrief OR GWC",
            singleEvents=True,
            maxResults=30
        ).execute()

        events = results.get("items", [])
        for event in events:
            attendees = [a.get("email", "") for a in event.get("attendees", [])]
            if candidate_email in attendees:
                start_dt = event["start"].get("dateTime")
                if start_dt:
                    is_past = datetime.fromisoformat(start_dt.replace("Z", "+00:00")) < now
                    return True, start_dt, is_past
        return False, None, False
    except Exception as e:
        print(f"[Calendar] Error checking debrief booking for {candidate_email}: {e}")
        return False, None, False

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: STAGE CLASSIFIER
# ═══════════════════════════════════════════════════════════════════════════════

def classify_candidate(cand, gmail_data, calendar_data):
    """
    Classify candidate into a pipeline stage.
    Returns {stage, days_stuck, next_action, draft_message, urgency}
    """
    now = datetime.now(timezone.utc)

    # Determine last status change date
    last_date = cand["applied_at"]
    if cand["values_date"]:
        last_date = cand["values_date"]
    if cand["gwc_date"]:
        last_date = cand["gwc_date"]

    # Convert to timezone-aware if needed
    if isinstance(last_date, str):
        last_date = datetime.fromisoformat(last_date.replace("Z", "+00:00"))
    elif last_date and last_date.tzinfo is None:
        last_date = last_date.replace(tzinfo=timezone.utc)

    if last_date:
        days_stuck = (now - last_date).days
    else:
        days_stuck = 0

    urgency = "normal"
    if days_stuck >= DAYS_URGENT:
        urgency = "urgent"
    elif days_stuck >= DAYS_FLAG:
        urgency = "flagged"

    # ── Stage classification logic ──

    # Values path
    if cand["values_result"] == "fail":
        return {
            "stage": "Values Failed",
            "days_stuck": days_stuck,
            "next_action": "Send warm rejection",
            "draft_message": None,  # No draft for failed candidates
            "urgency": "normal"
        }

    if cand["values_result"] == "pass":
        # Check if case study sent
        if not gmail_data.get("case_study_sent"):
            return {
                "stage": "Values Pass — No Case Study Sent",
                "days_stuck": days_stuck,
                "next_action": "Send case study assignment",
                "draft_message": draft_case_study_send(cand),
                "urgency": urgency
            }
        else:
            # Case study was sent, check if received
            if not cand["gwc_scorecard"]:
                return {
                    "stage": "Case Study Pending",
                    "days_stuck": days_stuck,
                    "next_action": "Await submission / follow up if overdue",
                    "draft_message": draft_case_study_reminder(cand) if urgency != "normal" else None,
                    "urgency": urgency
                }
            else:
                # Case study received, check debrief
                if not gmail_data.get("debrief_invite_sent"):
                    return {
                        "stage": "Case Study Received — No Debrief Invite",
                        "days_stuck": days_stuck,
                        "next_action": "Send debrief invitation",
                        "draft_message": draft_debrief_invite(cand),
                        "urgency": urgency
                    }
                else:
                    # Debrief invited, check booked
                    if not calendar_data.get("debrief_booked"):
                        return {
                            "stage": "Debrief Invited — Not Booked",
                            "days_stuck": days_stuck,
                            "next_action": "Follow up to book slot",
                            "draft_message": draft_debrief_reminder(cand) if urgency != "normal" else None,
                            "urgency": urgency
                        }
                    else:
                        if calendar_data.get("debrief_past"):
                            return {
                                "stage": "Debrief Completed",
                                "days_stuck": days_stuck,
                                "next_action": "Panel decision pending",
                                "draft_message": None,
                                "urgency": "normal"
                            }
                        else:
                            return {
                                "stage": "Debrief Booked",
                                "days_stuck": days_stuck,
                                "next_action": "Monitor",
                                "draft_message": None,
                                "urgency": "normal"
                            }

    # Values result not yet captured
    if cand["status"] == "shortlisted":
        if not gmail_data.get("values_invite_sent"):
            return {
                "stage": "Shortlisted — No Invite Sent",
                "days_stuck": days_stuck,
                "next_action": "Send values interview invite",
                "draft_message": draft_values_invite(cand),
                "urgency": urgency
            }
        else:
            # Invite sent, check booking
            if not calendar_data.get("values_booked"):
                return {
                    "stage": "Values Invited — Not Booked",
                    "days_stuck": days_stuck,
                    "next_action": "Follow up to book slot",
                    "draft_message": draft_values_reminder(cand) if urgency != "normal" else None,
                    "urgency": urgency
                }
            else:
                if calendar_data.get("values_past"):
                    return {
                        "stage": "Values Completed",
                        "days_stuck": days_stuck,
                        "next_action": "Enter scorecard on Markaz",
                        "draft_message": None,
                        "urgency": "normal"
                    }
                else:
                    return {
                        "stage": "Values Booked",
                        "days_stuck": days_stuck,
                        "next_action": "Monitor",
                        "draft_message": None,
                        "urgency": "normal"
                    }

    # Fallback
    return {
        "stage": "Unknown Stage",
        "days_stuck": days_stuck,
        "next_action": "Review candidate status",
        "draft_message": None,
        "urgency": "normal"
    }


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: DRAFT MESSAGE TEMPLATES
# ═══════════════════════════════════════════════════════════════════════════════

def draft_values_invite(cand):
    """Draft values interview invite message."""
    return {
        "subject": f"Invitation for Values Interview — {cand['first_name']} {cand['last_name']}",
        "body": f"""Hi {cand['first_name']},

Thank you for your application. We've reviewed your profile and would like to invite you to our Values Interview — a conversation where we explore how your values align with ours.

Please pick a time slot that works best for you from the calendar link: [insert link]
Slots available: Mon–Fri, 11am–12pm or 1pm–2pm

Looking forward to connecting with you.

Warm regards,
Ayesha Khan & Team
Taleemabad"""
    }


def draft_values_reminder(cand):
    """Draft values interview reminder message."""
    return {
        "subject": f"[Gentle Reminder] Let's schedule your values interview — {cand['first_name']}",
        "body": f"""Hi {cand['first_name']},

We sent you an invitation for a values interview a few days ago, and we'd love to get it on the calendar.

Could you pick a slot from the calendar link we provided? If those times don't work, please let us know and we can find something that does.

Thanks for your flexibility.

Warm regards,
Ayesha Khan & Team
Taleemabad"""
    }


def draft_case_study_send(cand):
    """Draft case study assignment message."""
    return {
        "subject": f"Your Case Study Assignment — {cand['first_name']} {cand['last_name']}",
        "body": f"""Hi {cand['first_name']},

Great news. You've cleared our values interview, and we'd like to move to the next step: a case study assignment.

Attached is the exercise. Please spend about 1–2 hours on it and send us your response by [DATE].

If you have any questions about the assignment, don't hesitate to reach out.

Looking forward to your work.

Warm regards,
Ayesha Khan & Team
Taleemabad"""
    }


def draft_case_study_reminder(cand):
    """Draft case study reminder message."""
    return {
        "subject": f"[Gentle Reminder] Your Case Study for {cand['first_name']}",
        "body": f"""Hi {cand['first_name']},

We sent you a case study assignment a while ago. We're looking forward to reviewing your work.

If you have questions about the assignment or need more time, please let us know your timeline.

Thanks,

Ayesha Khan & Team
Taleemabad"""
    }


def draft_debrief_invite(cand):
    """Draft debrief invitation message."""
    return {
        "subject": f"Let's Discuss Your Case Study — {cand['first_name']} {cand['last_name']}",
        "body": f"""Hi {cand['first_name']},

Thank you for submitting your case study. We were impressed with your approach and would like to discuss it further in a debrief conversation.

Please pick a time from the calendar link: [insert link]
Slots available: Mon–Fri, 2pm–4pm

Looking forward to hearing your thinking.

Warm regards,
Ayesha Khan & Team
Taleemabad"""
    }


def draft_debrief_reminder(cand):
    """Draft debrief reminder message."""
    return {
        "subject": f"[Reminder] Let's schedule your case study debrief — {cand['first_name']}",
        "body": f"""Hi {cand['first_name']},

We sent you a calendar invite for your case study debrief, and we'd like to get it scheduled.

Could you pick a slot from the link? If you need more time or have questions, please let us know.

Thanks,

Ayesha Khan & Team
Taleemabad"""
    }

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: HTML BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_report_html(jobs_data):
    """Build the full HTML report."""
    now = datetime.now()
    date_str = now.strftime("%d %B %Y")
    day_str = now.strftime("%A")

    total_urgent = sum(1 for j in jobs_data for c in j.get("candidates", []) if c["classification"]["urgency"] == "urgent")
    total_flagged = sum(1 for j in jobs_data for c in j.get("candidates", []) if c["classification"]["urgency"] == "flagged")

    html = f"""<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#f9f9f9;font-family:Arial,sans-serif;">
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#f9f9f9;">
  <tr><td align="center" style="padding:24px 16px;">
    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:900px;">

      <!-- HEADER -->
      <tr>
        <td bgcolor="{COLOR_GREEN}" style="padding:28px 32px;border-radius:8px 8px 0 0;">
          <p style="margin:0;font-size:24px;font-weight:bold;color:#ffffff;">
            Hiring Pipeline Monitor
          </p>
          <p style="margin:4px 0 0 0;font-size:14px;color:#e8f5e9;">
            {day_str}, {date_str} • {len(jobs_data)} open position(s)
          </p>
        </td>
      </tr>

      <!-- STAT BOXES -->
      <tr>
        <td bgcolor="#ffffff" style="padding:20px 32px;border-bottom:1px solid {COLOR_BORDER};">
          <table cellpadding="0" cellspacing="0" border="0" width="100%">
            <tr>
              <td style="text-align:center;padding:0 8px;">
                <p style="margin:0;font-size:28px;font-weight:bold;color:{COLOR_BLUE};">{len(jobs_data)}</p>
                <p style="margin:4px 0 0 0;font-size:12px;color:#666;">Open Positions</p>
              </td>
              <td style="text-align:center;padding:0 8px;border-left:1px solid {COLOR_BORDER};">
                <p style="margin:0;font-size:28px;font-weight:bold;color:{COLOR_RED};">{total_urgent}</p>
                <p style="margin:4px 0 0 0;font-size:12px;color:#666;">🔴 Urgent (14+ days)</p>
              </td>
              <td style="text-align:center;padding:0 8px;border-left:1px solid {COLOR_BORDER};">
                <p style="margin:0;font-size:28px;font-weight:bold;color:{COLOR_AMBER};">{total_flagged}</p>
                <p style="margin:4px 0 0 0;font-size:12px;color:#666;">⚠️ Flagged (3-14 days)</p>
              </td>
            </tr>
          </table>
        </td>
      </tr>

      <!-- JOBS SECTIONS -->
      <tr>
        <td bgcolor="#ffffff" style="padding:24px 32px;">
"""

    # Build per-job sections
    for job in jobs_data:
        candidates = job.get("candidates", [])
        urgent_cands = [c for c in candidates if c["classification"]["urgency"] == "urgent"]
        flagged_cands = [c for c in candidates if c["classification"]["urgency"] == "flagged"]
        other_cands = [c for c in candidates if c["classification"]["urgency"] == "normal"]

        html += f"""
          <!-- JOB: {job['title']} -->
          <p style="margin:0 0 4px 0;font-size:16px;font-weight:bold;color:{COLOR_BLUE};">
            {job['title']}
          </p>
          <p style="margin:0 0 16px 0;font-size:12px;color:#666;">
            Hiring Manager: {job.get('hm_first_name', 'TBD')} • {len(candidates)} candidate(s)
          </p>

          <table cellpadding="0" cellspacing="0" border="0" width="100%"
                 style="border-collapse:collapse;border:1px solid {COLOR_BORDER};margin-bottom:24px;">
            <tr style="background:{COLOR_BLUE};color:#ffffff;">
              <td style="padding:10px;font-weight:bold;border-right:1px solid #fff;">Candidate</td>
              <td style="padding:10px;font-weight:bold;border-right:1px solid #fff;">Stage</td>
              <td style="padding:10px;font-weight:bold;border-right:1px solid #fff;">Days Stuck</td>
              <td style="padding:10px;font-weight:bold;">Next Action</td>
            </tr>
"""

        # Urgent first, then flagged, then normal
        for cand in urgent_cands + flagged_cands + other_cands:
            urgency = cand["classification"]["urgency"]
            badge = "🔴" if urgency == "urgent" else "⚠️" if urgency == "flagged" else ""
            bg = "#ffebee" if urgency == "urgent" else "#fff3e0" if urgency == "flagged" else COLOR_GRAY

            html += f"""
            <tr style="background:{bg};">
              <td style="padding:10px;border-right:1px solid {COLOR_BORDER};">
                <b>{cand['first_name']} {cand['last_name']}</b>
              </td>
              <td style="padding:10px;border-right:1px solid {COLOR_BORDER};">
                {cand['classification']['stage']} {badge}
              </td>
              <td style="padding:10px;border-right:1px solid {COLOR_BORDER};text-align:center;">
                {cand['classification']['days_stuck']}d
              </td>
              <td style="padding:10px;">
                {cand['classification']['next_action']}
              </td>
            </tr>
"""

        html += """
          </table>
"""

    html += """
        </td>
      </tr>

      <!-- DRAFT MESSAGES SECTION -->
      <tr>
        <td bgcolor="#ffffff" style="padding:24px 32px;border-top:2px solid #ddd;">
          <p style="margin:0 0 16px 0;font-size:16px;font-weight:bold;color:{};"><strong>DRAFT MESSAGES</strong></p>
          <p style="margin:0 0 16px 0;font-size:13px;color:#666;">
            Ready for your review. Copy, personalize as needed, and send at your discretion.
          </p>
""".format(COLOR_BLUE)

    # Collect all draft messages
    all_drafts = []
    for job in jobs_data:
        for cand in job.get("candidates", []):
            draft = cand["classification"]["draft_message"]
            if draft:
                all_drafts.append({
                    "name": f"{cand['first_name']} {cand['last_name']}",
                    "job": job["title"],
                    "subject": draft["subject"],
                    "body": draft["body"],
                    "urgency": cand["classification"]["urgency"]
                })

    if all_drafts:
        for draft in all_drafts:
            urgency_label = "🔴 URGENT" if draft["urgency"] == "urgent" else "⚠️ FLAGGED"
            html += f"""
          <div style="background:{COLOR_GRAY};border-left:4px solid {COLOR_BLUE};padding:12px;margin-bottom:16px;">
            <p style="margin:0 0 4px 0;font-size:12px;font-weight:bold;color:#666;">
              {draft['name']} • {draft['job']} • {urgency_label}
            </p>
            <p style="margin:0 0 8px 0;font-size:13px;font-weight:bold;color:#222;">
              Subject: {draft['subject']}
            </p>
            <p style="margin:0;font-size:13px;color:#333;line-height:1.6;white-space:pre-wrap;">
              {draft['body']}
            </p>
          </div>
"""
    else:
        html += f"""
          <p style="margin:0;font-size:13px;color:#999;">
            No candidates in FLAG or URGENT status — no draft messages needed.
          </p>
"""

    # Footer
    html += f"""
        </td>
      </tr>

      <tr>
        <td bgcolor="#f5f5f5" style="padding:16px 32px;text-align:center;border-radius:0 0 8px 8px;font-size:12px;color:#999;">
          <p style="margin:0;">Compiled by Coco • AI Pipeline Monitor</p>
          <p style="margin:4px 0 0 0;">Runs Monday 10:30am + Friday 3pm</p>
        </td>
      </tr>

    </table>
  </td></tr>
</table>
</body>
</html>
"""

    return html

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: SEND
# ═══════════════════════════════════════════════════════════════════════════════

def send_report(html):
    """Send the report via safe_sendmail."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Hiring Pipeline Update — {datetime.now().strftime('%A, %d %b %Y')}"
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(RECIPIENTS_TO)
    msg["Cc"] = ", ".join(RECIPIENTS_CC)

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            all_recipients = RECIPIENTS_TO + RECIPIENTS_CC
            safe_sendmail(server, EMAIL_USER, all_recipients, msg.as_string(), context="hiring_pipeline_monitor")
        print("[Send] Report sent successfully")
        return True
    except Exception as e:
        print(f"[Send] Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9: MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Run the full pipeline monitor."""
    now = datetime.now()
    print(f"[Pipeline Monitor] Starting run at {now.isoformat()}", flush=True)
    sys.stdout.flush()

    try:
        # Get Gmail and Calendar services
        gmail_service = get_gmail_service()
        calendar_service = get_calendar_service()
        print("[Auth] Authenticated to Gmail and Calendar")

        # Get all open jobs
        jobs = get_open_jobs()
        print(f"[DB] Found {len(jobs)} open position(s)")

        if not jobs:
            print("[Monitor] No open positions. Exiting.")
            return

        jobs_data = []

        # Process each job
        for job in jobs:
            print(f"[Job] Processing {job['title']} (ID {job['id']})")

            candidates = get_candidates_for_job(job["id"])
            print(f"  > {len(candidates)} candidate(s) in pipeline")

            candidates_data = []

            for cand in candidates:
                # Gather Gmail data
                values_sent, _ = check_values_invite_sent(gmail_service, cand["email"], job["title"])
                case_study_sent, _ = check_case_study_sent(gmail_service, cand["email"])
                debrief_sent, _ = check_debrief_invite_sent(gmail_service, cand["email"])

                gmail_data = {
                    "values_invite_sent": values_sent,
                    "case_study_sent": case_study_sent,
                    "debrief_invite_sent": debrief_sent,
                }

                # Gather Calendar data
                values_booked, values_dt, values_past = check_values_booked(calendar_service, cand["email"])
                debrief_booked, debrief_dt, debrief_past = check_debrief_booked(calendar_service, cand["email"])

                calendar_data = {
                    "values_booked": values_booked,
                    "values_past": values_past,
                    "debrief_booked": debrief_booked,
                    "debrief_past": debrief_past,
                }

                # Classify
                classification = classify_candidate(cand, gmail_data, calendar_data)

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

        print("[HTML] Building report...", flush=True)
        sys.stdout.flush()
        try:
            html = build_report_html(jobs_data)
            print(f"[HTML] Built report ({len(html)} bytes)", flush=True)
        except Exception as html_err:
            print(f"[HTML Error] {html_err}", flush=True)
            import traceback
            traceback.print_exc()
            raise

        print("[Send] Sending report...", flush=True)
        sys.stdout.flush()
        success = send_report(html)

        if success:
            print("[Pipeline Monitor] Run completed successfully", flush=True)
            sys.stdout.flush()
        else:
            print("[Pipeline Monitor] Run completed with send error", flush=True)
            sys.stdout.flush()

    except Exception as e:
        print(f"[Error] Pipeline monitor failed: {e}", flush=True)
        sys.stdout.flush()
        import traceback
        traceback.print_exc()

        # Send error email to Ayesha only
        try:
            error_html = f"""
<html><body>
<p>Pipeline monitor script encountered an error:</p>
<pre>{str(e)}</pre>
<p>Please investigate.</p>
</body></html>
"""
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "⚠️ Pipeline Monitor Error"
            msg["From"] = EMAIL_USER
            msg["To"] = "ayesha.khan@taleemabad.com"
            msg.attach(MIMEText(error_html, "html"))

            with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                safe_sendmail(server, EMAIL_USER, ["ayesha.khan@taleemabad.com"], msg.as_string(),
                             context="pipeline_monitor_error")
        except Exception as e2:
            print(f"[Error] Could not send error email: {e2}")


if __name__ == "__main__":
    main()
