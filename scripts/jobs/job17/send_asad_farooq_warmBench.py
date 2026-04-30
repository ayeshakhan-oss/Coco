#!/usr/bin/env python3
"""
Warm Bench Candidate Interview Invite — CPD Coach
Asad Farooq (ID 102)

WORKFLOW:
  1. Run with PILOT_MODE = True  --> sends to Ayesha for review
  2. On approval, set PILOT_MODE = False and run again --> sends to Asad
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

load_dotenv()

# ── CONFIG ────────────────────────────────────────────────────────────────────
PILOT_MODE = False  # True = Ayesha only; False = Asad Farooq

POSITION = "CPD Coach"
SUBJECT = "A New Opportunity Aligned With Your Profile"
SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")
HIRING_MGR = "abdul.waheed@niete.edu.pk"
CC_LIST = [
    "hiring@taleemabad.com",
    HIRING_MGR,
]

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

# ── CANDIDATES ────────────────────────────────────────────────────────────────
PILOT_RECIPIENT = {
    "email": "ayesha.khan@taleemabad.com",
    "name": "Ayesha"
}

CANDIDATE = {
    "name": "Asad Farooq",
    "email": "masad.malik59@gmail.com"
}

# ── EMAIL: BUILD HTML ─────────────────────────────────────────────────────────
def build_email_html(candidate_name):
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0; padding:0; background-color:#f3f4f6; font-family:Georgia,serif;">

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#f3f4f6;">
  <tr>
    <td align="center" style="padding:60px 0;">
      <table cellpadding="0" cellspacing="0" border="0" width="620" style="background-color:#ffffff; border-radius:8px; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

        <!-- Logo -->
        <tr>
          <td align="center" style="padding:60px 70px 24px 70px;">
            <img src="cid:logo_taleemabad" width="48" height="48" alt="Taleemabad" style="display:block;border:0;">
          </td>
        </tr>

        <!-- Top Label -->
        <tr>
          <td align="center" style="padding:0 70px 24px 70px;">
            <p style="font-family:Arial,sans-serif; font-size:12px; color:#4b6cb7; letter-spacing:2px; font-weight:bold; margin:0; text-transform:uppercase;">
              PEOPLE & CULTURE • WARM BENCH OPPORTUNITY
            </p>
          </td>
        </tr>

        <!-- Main Title -->
        <tr>
          <td align="center" style="padding:0 70px 10px 70px;">
            <h1 style="font-family:Georgia,serif; font-size:28px; font-weight:bold; color:#2f4fa2; margin:0; line-height:1.3;">
              {POSITION}
            </h1>
          </td>
        </tr>

        <!-- Subtitle -->
        <tr>
          <td align="center" style="padding:0 70px 32px 70px;">
            <p style="font-family:Georgia,serif; font-size:15px; color:#5a6ea8; margin:0; line-height:1.4;">
              A New Role Aligned With Your Expertise
            </p>
          </td>
        </tr>

        <!-- Divider -->
        <tr>
          <td style="padding:30px 70px 50px 70px;">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td style="height:1px; background-color:#2f4fa2;"></td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Body Content -->
        <tr>
          <td style="padding:0 70px 50px 70px;">

            <p style="font-family:Georgia,serif; font-size:20px; color:#2f4fa2; font-weight:bold; margin:0 0 18px 0; line-height:1.3;">
              Hi {candidate_name},
            </p>

            <p style="font-family:Georgia,serif; font-size:16px; color:#000000; line-height:1.75; margin:0 0 18px 0; text-align:left;">
              You're one of our <span style="color:#2f4fa2; font-weight:bold;">warm bench candidates</span> — someone we believe is a strong cultural and values fit for Taleemabad. A position has recently opened up in the <span style="color:#2f4fa2; font-weight:bold;">{POSITION}</span> role, and our hiring manager would like to have a <span style="color:#2f4fa2; font-weight:bold;">quick conversation</span> to understand your skills and see if this is the right next step for you.
            </p>

            <p style="font-family:Georgia,serif; font-size:16px; color:#000000; line-height:1.75; margin:0 0 18px 0; text-align:left;">
              This is an informal chat — no formal interview preparation needed. We just want to reconnect and explore if this role is a fit.
            </p>

            <p style="font-family:Georgia,serif; font-size:16px; color:#000000; line-height:1.75; margin:0 0 18px 0; text-align:left;">
              The JD for this position is <a href="{JD_LINK}" style="color:#2f4fa2; text-decoration:none; font-weight:bold;">here</a>, and you can explore more about Taleemabad through the following links:
            </p>

            <!-- Links -->
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
            </p>

            <p style="font-family:Georgia,serif; font-size:16px; color:#000000; line-height:1.75; margin:0 0 40px 0; text-align:left;">
              Let us know if you need anything ahead of the conversation.
            </p>

          </td>
        </tr>

        <!-- Button -->
        <tr>
          <td align="center" style="padding:0 70px 50px 70px;">
            <table cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td bgcolor="#2f4fa2" style="border-radius:4px; padding:14px 32px;">
                  <a href="{BOOKING_LINK}" style="color:#ffffff; font-size:15px; font-weight:bold; text-decoration:none; font-family:Georgia,serif; display:block;">
                    📅 Lock the Calendar
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <tr>
          <td align="center" style="padding:0 70px 60px 70px;">
            <p style="font-family:Georgia,serif; font-size:14px; color:#5a6ea8; margin:0; line-height:1.5;">
              Please lock a slot at your earliest convenience.
            </p>
          </td>
        </tr>

        <!-- Footer Divider -->
        <tr>
          <td style="padding:0 70px;">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td style="height:1px; background-color:#e8e8e8;"></td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="padding:50px 70px 60px 70px;">

            <p style="font-family:Georgia,serif; font-size:14px; color:#5a6ea8; margin:0 0 20px 0; line-height:1.6;">
              Feel free to connect with us on our socials to get a sense of our culture:
            </p>

            <table cellpadding="0" cellspacing="0" border="0" style="margin:0 0 24px 0;">
              <tr>
                <td style="padding-right:16px;" valign="middle">
                  <a href="https://taleemabad.com" style="text-decoration:none;">
                    <img src="cid:logo_taleemabad" width="32" height="48" alt="Taleemabad" style="display:block;border:0;">
                  </a>
                </td>
                <td style="padding-right:12px;" valign="middle">
                  <a href="https://www.facebook.com/taleemabad" style="text-decoration:none;">
                    <img src="cid:logo_facebook" width="36" height="36" alt="Facebook" style="display:block;border:0;border-radius:4px;">
                  </a>
                </td>
                <td style="padding-right:12px;" valign="middle">
                  <a href="https://www.instagram.com/taleemabad" style="text-decoration:none;">
                    <img src="cid:logo_instagram" width="36" height="36" alt="Instagram" style="display:block;border:0;border-radius:4px;">
                  </a>
                </td>
                <td valign="middle">
                  <a href="https://www.linkedin.com/company/taleemabad" style="text-decoration:none;">
                    <img src="cid:logo_linkedin" width="36" height="36" alt="LinkedIn" style="display:block;border:0;border-radius:4px;">
                  </a>
                </td>
              </tr>
            </table>

            <p style="font-family:Georgia,serif; font-size:16px; color:#000000; font-weight:bold; margin:0 0 6px 0; line-height:1.4;">
              See you soon,
            </p>
            <p style="font-family:Georgia,serif; font-size:16px; color:#000000; margin:0 0 16px 0; line-height:1.4;">
              Team Taleemabad
            </p>
            <p style="font-family:Georgia,serif; font-size:13px; color:#5a6ea8; margin:0; line-height:1.4;">
              Coco – AI Assistant Taleemabad
            </p>

          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>

</body>
</html>"""
    return html


# ── EMAIL: SEND ───────────────────────────────────────────────────────────────
def send_invite(to_email, to_name, cc_list=None):
    msg = MIMEMultipart("related")
    msg["From"] = SENDER
    msg["To"] = to_email
    msg["Subject"] = f"{SUBJECT} — {POSITION}"
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(build_email_html(to_name), "html"))
    msg.attach(alt)

    for cid, fname in INLINE_IMAGES:
        with open(os.path.join(ASSETS_DIR, fname), "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", f"<{cid}>")
        img.add_header("Content-Disposition", "inline", filename=fname)
        msg.attach(img)

    recipients = [to_email] + (cc_list or [])
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        allow_candidate_addresses(recipients if isinstance(recipients, list) else [recipients])
        safe_sendmail(smtp, SENDER, recipients, msg.as_string(), context='asad_farooq_warmBench_invite')

    cc_str = f" (CC: {', '.join(cc_list)})" if cc_list else ""
    print(f"Sent to {to_name} <{to_email}>{cc_str}")


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print(f"Job 17 — CPD Coach | Warm Bench Invite — Asad Farooq")
    print(f"Mode: {'PILOT (Ayesha only)' if PILOT_MODE else 'LIVE (Asad Farooq)'}")
    print("=" * 60)

    if PILOT_MODE:
        send_invite(PILOT_RECIPIENT["email"], PILOT_RECIPIENT["name"])
        print(f"\nPilot sent to Ayesha. Review then set PILOT_MODE = False to send to {CANDIDATE['name']}.")
    else:
        send_invite(CANDIDATE["email"], CANDIDATE["name"], cc_list=CC_LIST)
        print(f"\nLive sent to {CANDIDATE['name']} <{CANDIDATE['email']}>")

    print("=" * 60)


if __name__ == "__main__":
    main()
