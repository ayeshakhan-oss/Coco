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
RECIPIENTS_CC = []

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
    """Fetch all shortlisted+ candidates for a job with full pipeline timeline including communications."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    query = """
        SELECT a.id, a.candidate_id, c.first_name, c.last_name, c.email,
               a.status, a.applied_at,
               a.values_interview_result, a.values_interview_date, a.values_scorecard,
               a.gwc_scorecard, a.gwc_interview_date, a.notes
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
        app_id = row[0]

        # Get communications history for this application
        comm_query = """
            SELECT email_type, sent_at FROM candidate_communications
            WHERE application_id = %s
            ORDER BY sent_at DESC
        """
        cur.execute(comm_query, (app_id,))
        comms = cur.fetchall()

        # Extract sent dates from communications
        values_invite_sent_at = None
        case_study_sent_at = None
        debrief_invite_sent_at = None

        for email_type, sent_at in comms:
            if email_type and "values" in email_type.lower() and not values_invite_sent_at:
                values_invite_sent_at = sent_at
            if email_type and ("case study" in email_type.lower() or "kcd" in email_type.lower()) and not case_study_sent_at:
                case_study_sent_at = sent_at
            if email_type and "debrief" in email_type.lower() and not debrief_invite_sent_at:
                debrief_invite_sent_at = sent_at

        candidates.append({
            "app_id": row[0],
            "candidate_id": row[1],
            "first_name": row[2],
            "last_name": row[3],
            "email": row[4],
            "status": row[5],
            "applied_at": row[6],
            "values_result": row[7],
            "values_interview_date": row[8],
            "values_scorecard": row[9],
            "gwc_scorecard": row[10],
            "gwc_interview_date": row[11],
            "notes": row[12],
            "values_invite_sent_at_markaz": values_invite_sent_at,
            "case_study_sent_at_markaz": case_study_sent_at,
            "debrief_invite_sent_at_markaz": debrief_invite_sent_at,
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


def fetch_all_sent_emails_bulk(service):
    """
    Batch-fetch ALL sent emails (values, case study, debrief) in one pass.
    Returns dict: {email: {type: send_date}}
    Reduces 750 queries to ~3-10 total queries.
    """
    lookup = {}

    # QUERY 1: All values invites
    try:
        print("[Gmail] Fetching all values invites...", flush=True)
        sys.stdout.flush()
        q = 'subject:(Invitation for Values OR "Zero In")'
        results = service.users().messages().list(userId="me", q=q, maxResults=500).execute()
        msg_ids = [m["id"] for m in results.get("messages", [])]
        log_gmail_read(q, len(msg_ids), "batch_fetch_values")

        for msg_id in msg_ids:
            try:
                msg = service.users().messages().get(userId="me", id=msg_id, format="metadata").execute()
                headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
                to_addr = headers.get("To", "").lower()
                send_date = headers.get("Date", "")
                if to_addr:
                    lookup.setdefault(to_addr, {})["values_invite"] = send_date
            except:
                pass
        print(f"[Gmail] Values invites: {len([k for k in lookup.values() if 'values_invite' in k])} recipients", flush=True)
        sys.stdout.flush()
    except Exception as e:
        print(f"[Gmail] Error fetching values invites: {e}", flush=True)

    # QUERY 2: All case study emails
    try:
        print("[Gmail] Fetching all case study assignments...", flush=True)
        sys.stdout.flush()
        q = 'subject:(case study OR KCD assignment)'
        results = service.users().messages().list(userId="me", q=q, maxResults=500).execute()
        msg_ids = [m["id"] for m in results.get("messages", [])]
        log_gmail_read(q, len(msg_ids), "batch_fetch_case_study")

        for msg_id in msg_ids:
            try:
                msg = service.users().messages().get(userId="me", id=msg_id, format="metadata").execute()
                headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
                to_addr = headers.get("To", "").lower()
                send_date = headers.get("Date", "")
                if to_addr:
                    lookup.setdefault(to_addr, {})["case_study"] = send_date
            except:
                pass
        print(f"[Gmail] Case study sent: {len([k for k in lookup.values() if 'case_study' in k])} recipients", flush=True)
        sys.stdout.flush()
    except Exception as e:
        print(f"[Gmail] Error fetching case studies: {e}", flush=True)

    # QUERY 3: All debrief invites
    try:
        print("[Gmail] Fetching all debrief invites...", flush=True)
        sys.stdout.flush()
        q = 'subject:(debrief OR GWC discussion)'
        results = service.users().messages().list(userId="me", q=q, maxResults=500).execute()
        msg_ids = [m["id"] for m in results.get("messages", [])]
        log_gmail_read(q, len(msg_ids), "batch_fetch_debrief")

        for msg_id in msg_ids:
            try:
                msg = service.users().messages().get(userId="me", id=msg_id, format="metadata").execute()
                headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
                to_addr = headers.get("To", "").lower()
                send_date = headers.get("Date", "")
                if to_addr:
                    lookup.setdefault(to_addr, {})["debrief"] = send_date
            except:
                pass
        print(f"[Gmail] Debrief invites: {len([k for k in lookup.values() if 'debrief' in k])} recipients", flush=True)
        sys.stdout.flush()
    except Exception as e:
        print(f"[Gmail] Error fetching debriefs: {e}", flush=True)

    return lookup


def check_values_invite_sent(email_lookup, candidate_email):
    """Check if values invite was sent. Uses pre-fetched lookup."""
    email_lower = candidate_email.lower()
    if email_lower in email_lookup and "values_invite" in email_lookup[email_lower]:
        return True, email_lookup[email_lower]["values_invite"]
    return False, None


def check_case_study_sent(email_lookup, candidate_email):
    """Check if case study was sent. Uses pre-fetched lookup."""
    email_lower = candidate_email.lower()
    if email_lower in email_lookup and "case_study" in email_lookup[email_lower]:
        return True, email_lookup[email_lower]["case_study"]
    return False, None


def check_debrief_invite_sent(email_lookup, candidate_email):
    """Check if debrief invite was sent. Uses pre-fetched lookup."""
    email_lower = candidate_email.lower()
    if email_lower in email_lookup and "debrief" in email_lookup[email_lower]:
        return True, email_lookup[email_lower]["debrief"]
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


def fetch_all_calendar_events(service):
    """Batch-fetch all calendar events. Returns {email: {type: (booked, dt, is_past)}}."""
    lookup = {}
    now = datetime.now(timezone.utc)
    past = (now - timedelta(days=60)).isoformat()
    future = (now + timedelta(days=60)).isoformat()

    # Fetch all values events
    try:
        results = service.events().list(
            calendarId="primary",
            timeMin=past,
            timeMax=future,
            q="Zero In",
            singleEvents=True,
            maxResults=100
        ).execute()

        events = results.get("items", [])
        for event in events:
            attendees = [a.get("email", "").lower() for a in event.get("attendees", [])]
            start_dt = event["start"].get("dateTime")
            if start_dt:
                is_past = datetime.fromisoformat(start_dt.replace("Z", "+00:00")) < now
                for attendee_email in attendees:
                    if attendee_email:
                        lookup.setdefault(attendee_email, {})["values_booked"] = (True, start_dt, is_past)
    except Exception as e:
        print(f"[Calendar] Error fetching values events: {e}")

    # Fetch all debrief events
    try:
        results = service.events().list(
            calendarId="primary",
            timeMin=past,
            timeMax=future,
            q="Debrief OR GWC",
            singleEvents=True,
            maxResults=100
        ).execute()

        events = results.get("items", [])
        for event in events:
            attendees = [a.get("email", "").lower() for a in event.get("attendees", [])]
            start_dt = event["start"].get("dateTime")
            if start_dt:
                is_past = datetime.fromisoformat(start_dt.replace("Z", "+00:00")) < now
                for attendee_email in attendees:
                    if attendee_email:
                        lookup.setdefault(attendee_email, {})["debrief_booked"] = (True, start_dt, is_past)
    except Exception as e:
        print(f"[Calendar] Error fetching debrief events: {e}")

    return lookup


def check_values_booked(calendar_lookup, candidate_email):
    """Check if values interview is booked. Uses pre-fetched calendar lookup."""
    email_lower = candidate_email.lower()
    if email_lower in calendar_lookup and "values_booked" in calendar_lookup[email_lower]:
        return calendar_lookup[email_lower]["values_booked"]
    return False, None, False


def check_debrief_booked(calendar_lookup, candidate_email):
    """Check if debrief is booked. Uses pre-fetched calendar lookup."""
    email_lower = candidate_email.lower()
    if email_lower in calendar_lookup and "debrief_booked" in calendar_lookup[email_lower]:
        return calendar_lookup[email_lower]["debrief_booked"]
    return False, None, False

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: STAGE CLASSIFIER
# ═══════════════════════════════════════════════════════════════════════════════

def classify_candidate(cand, gmail_data, calendar_data):
    """
    Classify candidate following the sequential pipeline flow.
    Cross-verifies Markaz (primary) + Gmail (invites) + Calendar (bookings).
    Returns {stage, days_stuck, next_action, draft_message, urgency, verification_notes}
    """
    now = datetime.now(timezone.utc)

    # Helper: parse date string to datetime
    def parse_date(date_val):
        if not date_val:
            return None
        if isinstance(date_val, str):
            try:
                dt = datetime.fromisoformat(date_val.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except:
                return None
        elif isinstance(date_val, datetime):
            if date_val.tzinfo is None:
                return date_val.replace(tzinfo=timezone.utc)
            return date_val
        return None

    applied_date = parse_date(cand["applied_at"])
    values_invite_sent_date = parse_date(gmail_data.get("values_invite_sent_date"))
    values_interview_date = parse_date(cand["values_interview_date"])
    case_study_sent_date = parse_date(gmail_data.get("case_study_sent_date"))
    debrief_invite_sent_date = parse_date(gmail_data.get("debrief_invite_sent_date"))
    gwc_interview_date = parse_date(cand["gwc_interview_date"])

    # Check if case study was submitted: EVIDENCE is gwc_interview_date (debrief happened, meaning case study was received and discussed)
    case_study_submitted = bool(gwc_interview_date)  # If debrief happened, case study must have been submitted
    case_study_submit_date = gwc_interview_date or case_study_sent_date

    notes = []
    draft_message = None
    action = None
    stage = None
    days_stuck = 0
    urgency = "normal"

    # ══════════════════════════════════════════════════════════════════════════
    # STAGE 1: SHORTLISTED → VALUES INVITE
    # ══════════════════════════════════════════════════════════════════════════

    if cand["status"] == "shortlisted":
        if not gmail_data.get("values_invite_sent"):
            stage = "Shortlisted - No Values Invite"
            action = "Send values interview invite"
            days_stuck = (now - applied_date).days if applied_date else 0
            draft_message = {
                "subject": f"Invitation for the Values Interview for [Position] - {cand['first_name']}",
                "body": f"""Hi {cand['first_name']},

Thank you for your interest in [Position]. We'd like to invite you to participate in our values interview, where we get to know you better beyond your resume.

Please pick a time from this calendar link: [insert link]
Available slots: Mon–Fri, 11am–12pm or 1pm–2pm (2-week window)

Looking forward to meeting you.

Warm regards,
Ayesha Khan
People & Culture
Taleemabad"""
            }
        else:
            # Values invite sent, check if booked
            if not values_interview_date:
                stage = "Values Invite Sent - Not Booked"
                action = "Remind candidate to book calendar slot"
                days_stuck = (now - values_invite_sent_date).days if values_invite_sent_date else 0
                notes.append("Email sent but no calendar booking found")
            elif values_interview_date > now:
                stage = "Values Interview Scheduled"
                action = None
                days_stuck = 0
            else:
                # Interview date is past
                if not cand["values_scorecard"]:
                    stage = "Values Interview Completed - Scorecard Pending"
                    action = "Fill values scorecard"
                    days_stuck = (now - values_interview_date).days if values_interview_date else 0
                    notes.append("Interview completed but scorecard not filled")
                else:
                    # Scorecard filled, check result
                    if cand["values_result"] == "fail":
                        stage = "Values Failed"
                        action = "Send values rejection email"
                        urgency = "normal"
                    elif cand["values_result"] == "pass":
                        # Proceed to Stage 2
                        stage = None  # Will be set in Stage 2

    # ══════════════════════════════════════════════════════════════════════════
    # STAGE 2: VALUES PASS → CASE STUDY
    # ══════════════════════════════════════════════════════════════════════════

    if cand["values_result"] == "pass" and not stage:
        if not gmail_data.get("case_study_sent"):
            stage = "Values Passed - No Case Study"
            action = "Send case study assignment"
            days_stuck = (now - values_interview_date).days if values_interview_date else 0
            draft_message = {
                "subject": f"Case Study Assignment - {cand['first_name']}",
                "body": f"""Hi {cand['first_name']},

Great news. You've cleared our values interview, and we'd like to move to the next step: a case study assignment.

Attached is the exercise. Please spend about 1–2 hours on it and send us your response by [DATE].

If you have any questions about the assignment, don't hesitate to reach out.

Looking forward to your work.

Warm regards,
Ayesha Khan & Team
Taleemabad"""
            }
        else:
            # Case study sent, check if submitted
            if not case_study_submitted:
                days_since_sent = (now - case_study_sent_date).days if case_study_sent_date else 0
                if days_since_sent > 7:
                    stage = "Case Study Overdue"
                    action = "Send reminder to candidate"
                    days_stuck = days_since_sent
                else:
                    stage = "Case Study In Transit"
                    action = None
                    days_stuck = 0
            else:
                # Case study received - check debrief stage (debrief_invite_sent may be in Gmail or Calendar may have the event)
                # EVIDENCE OF DEBRIEF COMPLETION: gwc_interview_date exists

                if gwc_interview_date:
                    # Debrief HAS happened (gwc_interview_date exists)
                    if gwc_interview_date > now:
                        # Debrief is in future (scheduled)
                        stage = "Debrief Scheduled"
                        action = None
                        days_stuck = 0
                    else:
                        # Debrief is in past (completed)
                        if not cand["gwc_scorecard"]:
                            stage = "Debrief Completed - GWC Scorecard Pending"
                            action = "Fill GWC scorecard"
                            days_stuck = (now - gwc_interview_date).days if gwc_interview_date else 0
                        else:
                            stage = "Panel Decision Pending"
                            action = "Make panel decision"
                            days_stuck = 0
                else:
                    # No debrief scheduled yet - check if invite was sent
                    if not gmail_data.get("debrief_invite_sent"):
                        stage = "Case Study Received - No Debrief Invite"
                        action = "Send debrief invite"
                        days_stuck = (now - case_study_submit_date).days if case_study_submit_date else 0
                        draft_message = {
                            "subject": f"Let's Discuss Your Case Study — {cand['first_name']}",
                            "body": f"""Hi {cand['first_name']},

Thank you for submitting your case study. We were impressed with your approach and would like to discuss it further in a debrief conversation.

Please pick a time from the calendar link: [insert link]
Slots available: Mon–Fri, 2pm–4pm

Looking forward to hearing your thinking.

Warm regards,
Ayesha Khan & Team
Taleemabad"""
                        }
                    else:
                        # Debrief invite sent, check if booked
                        if not calendar_data.get("debrief_booked"):
                            days_since_invite = (now - debrief_invite_sent_date).days if debrief_invite_sent_date else 0
                            if days_since_invite > 5:
                                stage = "Debrief Invite Sent - Not Booked (Overdue)"
                                action = "Send reminder email"
                                days_stuck = days_since_invite
                            else:
                                stage = "Awaiting Debrief Booking"
                                action = None
                                days_stuck = 0
                        else:
                            # Calendar booked
                            stage = "Debrief Scheduled"
                            action = None
                            days_stuck = 0

    # ══════════════════════════════════════════════════════════════════════════
    # DEFAULT: Set urgency based on days_stuck
    # ══════════════════════════════════════════════════════════════════════════

    if days_stuck >= DAYS_URGENT:
        urgency = "urgent"
    elif days_stuck >= DAYS_FLAG:
        urgency = "flagged"
    else:
        urgency = "normal"

    return {
        "stage": stage or "Unknown",
        "days_stuck": days_stuck,
        "next_action": action,
        "draft_message": draft_message,
        "urgency": urgency,
        "verification_notes": notes
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
        print("[Auth] Authenticated to Gmail and Calendar", flush=True)
        sys.stdout.flush()

        # Batch-fetch ALL Gmail sends (one-time, for all candidates)
        print("[Gmail] Batch-fetching all sent emails...", flush=True)
        sys.stdout.flush()
        email_lookup = fetch_all_sent_emails_bulk(gmail_service)
        print(f"[Gmail] Indexed {len(email_lookup)} recipient(s)", flush=True)
        sys.stdout.flush()

        # Batch-fetch calendar events (one-time, for all candidates)
        print("[Calendar] Batch-fetching all calendar events...", flush=True)
        sys.stdout.flush()
        calendar_lookup = fetch_all_calendar_events(calendar_service)
        print(f"[Calendar] Indexed {len(calendar_lookup)} attendee(s)", flush=True)
        sys.stdout.flush()

        # Get all open jobs
        jobs = get_open_jobs()
        print(f"[DB] Found {len(jobs)} open position(s)", flush=True)
        sys.stdout.flush()

        if not jobs:
            print("[Monitor] No open positions. Exiting.")
            return

        jobs_data = []

        # Process each job
        for job in jobs:
            print(f"[Job] Processing {job['title']} (ID {job['id']})", flush=True)
            sys.stdout.flush()

            candidates = get_candidates_for_job(job["id"])
            print(f"  > {len(candidates)} candidate(s) in pipeline", flush=True)
            sys.stdout.flush()

            candidates_data = []

            for cand in candidates:
                # SOURCE OF TRUTH: Markaz communications table (not Gmail)
                # Use Markaz first, fall back to Gmail if Markaz doesn't have it
                values_sent_date = cand.get("values_invite_sent_at_markaz")
                case_study_sent_date = cand.get("case_study_sent_at_markaz")
                debrief_sent_date = cand.get("debrief_invite_sent_at_markaz")

                # Fall back to Gmail if Markaz doesn't have the date
                if not values_sent_date:
                    gmail_values_sent, gmail_values_date = check_values_invite_sent(email_lookup, cand["email"])
                    if gmail_values_sent:
                        values_sent_date = gmail_values_date
                if not case_study_sent_date:
                    gmail_case_sent, gmail_case_date = check_case_study_sent(email_lookup, cand["email"])
                    if gmail_case_sent:
                        case_study_sent_date = gmail_case_date
                if not debrief_sent_date:
                    gmail_debrief_sent, gmail_debrief_date = check_debrief_invite_sent(email_lookup, cand["email"])
                    if gmail_debrief_sent:
                        debrief_sent_date = gmail_debrief_date

                gmail_data = {
                    "values_invite_sent": bool(values_sent_date),
                    "values_invite_sent_date": values_sent_date,
                    "case_study_sent": bool(case_study_sent_date),
                    "case_study_sent_date": case_study_sent_date,
                    "debrief_invite_sent": bool(debrief_sent_date),
                    "debrief_invite_sent_date": debrief_sent_date,
                }

                # Gather Calendar data from pre-fetched lookup
                values_booked, values_dt, values_past = check_values_booked(calendar_lookup, cand["email"])
                debrief_booked, debrief_dt, debrief_past = check_debrief_booked(calendar_lookup, cand["email"])

                calendar_data = {
                    "values_booked": values_booked,
                    "values_past": values_past,
                    "debrief_booked": debrief_booked,
                    "debrief_past": debrief_past,
                }

                # Classify using sequential flow
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
