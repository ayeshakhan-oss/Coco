#!/usr/bin/env python3
"""
Warm Bench Candidate Interview Invite — CPD Coach
Values + GWC Cleared Candidates for New Positions

PILOT to Ayesha for review
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
from scripts.utils.template_loader import format_interview_invite

load_dotenv()

POSITION = "CPD Coach"
SUBJECT = "A New Opportunity Aligned With Your Profile"
SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")
HIRING_MGR = "abdul.waheed@niete.edu.pk"

BOOKING_LINK = "https://calendar.app.google/YvKqEK16Tax7PGyy5"
JD_LINK = "https://docs.google.com/document/d/1pg58RoVWoVO6WQTlGePJPbW_VLF0GkcYrQeG2Ah6G6s/edit?tab=t.0"
TEAMS_LINK = ""

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets")

INLINE_IMAGES = [
    ("logo_taleemabad", "logo_taleemabad.png"),
    ("logo_facebook", "logo_facebook.png"),
    ("logo_instagram", "logo_instagram.png"),
    ("logo_linkedin", "logo_linkedin.png"),
]

PILOT_RECIPIENT = {
    "email": "ayesha.khan@taleemabad.com",
    "name": "Ayesha"
}


def build_email_html(candidate_name):
    """Build warm bench interview invite HTML using locked template."""

    body_html = f"""<p style="font-family:Georgia,serif; font-size:16px; color:#000000; line-height:1.75; margin:0 0 18px 0; text-align:left;">
              You're one of our <span style="color:#2f4fa2; font-weight:bold;">warm bench candidates</span> — someone we believe is a strong cultural and values fit for Taleemabad. A position has recently opened up in the <span style="color:#2f4fa2; font-weight:bold;">{POSITION}</span> role, and our hiring manager would like to have a <span style="color:#2f4fa2; font-weight:bold;">quick conversation</span> to understand your skills and see if this is the right next step for you.
            </p>

            <p style="font-family:Georgia,serif; font-size:16px; color:#000000; line-height:1.75; margin:0 0 18px 0; text-align:left;">
              This is an informal chat — no formal interview preparation needed. We just want to reconnect and explore if this role is a fit.
            </p>

            <p style="font-family:Georgia,serif; font-size:16px; color:#000000; line-height:1.75; margin:0 0 18px 0; text-align:left;">
              The JD for this position is <a href="{JD_LINK}" style="color:#2f4fa2; text-decoration:none; font-weight:bold;">here</a>, and you can explore more about Taleemabad through the following links:
            </p>

            <table cellpadding="0" cellspacing="0" border="0" style="margin:0 0 18px 0;">
              <tr>
                <td style="padding:8px 0; font-family:Georgia,serif; font-size:16px; color:#000000; line-height:1.75;">
                  • <a href="https://www.youtube.com/watch?v=jb4hWQDNEos" style="color:#2f4fa2; text-decoration:none; font-weight:bold;">Magic of Taleemabad</a>
                </td>
              </tr>
              <tr>
                <td style="padding:8px 0; font-family:Georgia,serif; font-size:16px; color:#000000; line-height:1.75;">
                  • <a href="https://drive.google.com/file/d/1xhITDW5RjYjwKkULfewI1ZPL7iNlI1he/view" style="color:#2f4fa2; text-decoration:none; font-weight:bold;">Impact in a one-minute video</a>
                </td>
              </tr>
            </table>

            <p style="font-family:Georgia,serif; font-size:16px; color:#000000; line-height:1.75; margin:0 0 18px 0; text-align:left;">
              This session will be recorded, and by joining, you consent to being a part of the recorded call.
            </p>

            <p style="font-family:Georgia,serif; font-size:16px; color:#000000; line-height:1.75; margin:0 0 18px 0; text-align:left;">
              Please go through the <a href="https://docs.google.com/document/d/1TBbBAimVX9PxSR6-rT13bLKf38itNdbp5v6EbWuDtkg/edit?tab=t.0" style="color:#2f4fa2; text-decoration:none; font-weight:bold;">interview prep guide</a> to understand the process.
            </p>"""

    return format_interview_invite(
        candidate_name=candidate_name,
        position=POSITION,
        label="PEOPLE & CULTURE • WARM BENCH OPPORTUNITY",
        subtitle="A New Role Aligned With Your Expertise",
        body_html=body_html,
        booking_link=BOOKING_LINK,
        button_text="📅 Lock the Calendar",
        button_subtext="Please lock a slot at your earliest convenience."
    )


def send_pilot(to_email, to_name):
    msg = MIMEMultipart("related")
    msg["From"] = SENDER
    msg["To"] = to_email
    msg["Subject"] = f"{SUBJECT} — {POSITION}"

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(build_email_html(to_name), "html"))
    msg.attach(alt)

    for cid, fname in INLINE_IMAGES:
        with open(os.path.join(ASSETS_DIR, fname), "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", f"<{cid}>")
        img.add_header("Content-Disposition", "inline", filename=fname)
        msg.attach(img)

    recipients = [to_email]
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        safe_sendmail(smtp, SENDER, recipients, msg.as_string(), context='warmBench_invite_pilot')

    print(f"Pilot sent to {to_name} <{to_email}>")


if __name__ == "__main__":
    print("=" * 70)
    print(f"Warm Bench Interview Invite — {POSITION}")
    print("Mode: PILOT to Ayesha")
    print("=" * 70)

    send_pilot(PILOT_RECIPIENT["email"], PILOT_RECIPIENT["name"])
    print("\nReview template. Ready to customize per warm bench candidate.")
    print("=" * 70)
