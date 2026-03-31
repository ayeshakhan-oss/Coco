"""
Job 36 — Field Coordinator, Research & Impact Studies
Case Study Debrief Invitation — LIVE SEND
Recipients: Scheherazade Noor, Maria Karim, Amina Batool,
            Usman Ahmed Khan, Asad Farooq, Jalal Ud Din
CC: hiring@taleemabad.com, ayesha.khan@taleemabad.com, jawwad.ali@taleemabad.com
Design: v8 (white bg, blue header, CID logo, purple CTA button)
"""

import os, smtplib, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

SENDER   = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
CC       = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]

POSITION        = "Field Coordinator \u2013 Research & Impact Studies"
SCHEDULING_LINK = "https://calendar.app.google/e7SmSYxxEYnaQcgr7"
SUBJECT         = f"Invitation to Case Study Debrief - {POSITION}"

LOGO_PATH = os.path.join(os.path.dirname(__file__), "../../..", "assets", "logo_taleemabad.png")
with open(LOGO_PATH, "rb") as f:
    LOGO_BYTES = f.read()

CANDIDATES = [
    {"first_name": "Scheherazade", "email": "noorscheherazade@gmail.com"},
    {"first_name": "Maria",        "email": "mariakarim1013@gmail.com"},
    {"first_name": "Amina",        "email": "aminabatool2000@gmail.com"},
    {"first_name": "Usman",        "email": "usmanumar646@gmail.com"},
    {"first_name": "Asad",         "email": "masad.malik59@gmail.com"},
    {"first_name": "Jalal",        "email": "jalalsaraikhan@gmail.com"},
]

# ── COLOURS ────────────────────────────────────────────────────────────────────
DARK   = "#1a1a1a"
BLUE   = "#1565c0"
PURPLE = "#4f46e5"
WHITE  = "#ffffff"
BG     = "#f0f4f0"
MID    = "#555555"
RULE   = "#e0e0e0"


def build_html(first_name):
    header = f"""
<table width="100%" cellpadding="0" cellspacing="0"
       style="border-radius:8px 8px 0 0;overflow:hidden;
              border-bottom:2px solid {BLUE};">
  <tr>
    <td align="center" bgcolor="{WHITE}"
        style="background-color:{WHITE};padding:28px 40px 22px 40px;">
      <img src="cid:taleemabad_logo" height="38" alt="Taleemabad"
           style="display:block;margin:0 auto 14px auto;">
      <p style="margin:0;font-family:Georgia,serif;font-size:11px;
                color:{BLUE};letter-spacing:2px;text-transform:uppercase;">
        People &amp; Culture &nbsp;&bull;&nbsp; Next Round Invitation
      </p>
      <p style="margin:10px 0 4px 0;font-family:Georgia,serif;font-size:17px;
                font-weight:bold;color:{BLUE};line-height:1.4;">
        Invitation to Case Study Debrief
      </p>
      <p style="margin:0;font-family:Georgia,serif;font-size:12px;color:#5c85c7;">
        {POSITION}
      </p>
    </td>
  </tr>
</table>"""

    body = f"""
    <p style="margin:0 0 20px 0;">Hi {first_name},</p>

    <p style="margin:0 0 18px 0;">
      Congratulations on making it to the next stage of the process. We have really enjoyed
      getting to know your work so far.
    </p>

    <p style="margin:0 0 18px 0;">
      This email is an invitation to the third round, where we will be debriefing the case
      study you recently submitted. In this conversation, you will have the chance to interact
      directly with the hiring manager for the role.
    </p>

    <p style="margin:0 0 18px 0;">
      The goal of this round is to better understand your thinking, approach, and strengths
      through your case study, while also giving you the opportunity to get a clearer sense
      of the role, the team, and how we work at Taleemabad.
    </p>

    <p style="margin:0 0 8px 0;">
      Please pick a time that works best for you using the link below:
    </p>

    <table width="100%" cellpadding="0" cellspacing="0" style="margin:28px 0;">
      <tr>
        <td align="center">
          <a href="{SCHEDULING_LINK}"
             style="display:inline-block;background:{PURPLE};color:{WHITE};
                    font-family:Arial,sans-serif;font-size:14px;font-weight:bold;
                    padding:14px 36px;border-radius:6px;text-decoration:none;
                    letter-spacing:0.3px;">
            Book Your Slot
          </a>
        </td>
      </tr>
    </table>

    <p style="margin:0 0 32px 0;">
      We are genuinely looking forward to this conversation and learning more about you.
    </p>

    <table width="100%" cellpadding="0" cellspacing="0"
           style="margin-top:40px;border-top:1px solid {RULE};padding-top:20px;">
      <tr>
        <td style="font-family:Georgia,serif;font-size:13px;color:{MID};line-height:1.9;">
          Warm regards,<br>
          <strong style="color:{DARK};">People and Culture Team</strong><br>
          <strong style="color:{BLUE};">Taleemabad</strong><br>
          <a href="mailto:hiring@taleemabad.com"
             style="color:{BLUE};text-decoration:none;">hiring@taleemabad.com</a>
          &nbsp;|&nbsp;
          <a href="http://www.taleemabad.com"
             style="color:{BLUE};text-decoration:none;">www.taleemabad.com</a><br>
          <span style="font-size:12px;color:#aaa;margin-top:4px;display:block;">
            Sent on behalf of Talent Acquisition Team by Coco
          </span>
        </td>
      </tr>
    </table>"""

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background-color:{BG};">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background-color:{BG};padding:32px 0;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0"
             style="max-width:620px;border-radius:8px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);">
        <tr><td>{header}</td></tr>
        <tr>
          <td style="background:{WHITE};padding:40px 52px 48px 52px;
                     border-radius:0 0 8px 8px;
                     font-family:Georgia,serif;font-size:15px;
                     line-height:1.8;color:{DARK};">
            {body}
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


def send_one(candidate):
    html = build_html(candidate["first_name"])

    msg = MIMEMultipart("related")
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html, "html"))
    msg.attach(alt)

    logo = MIMEImage(LOGO_BYTES, "png")
    logo.add_header("Content-ID", "<taleemabad_logo>")
    logo.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
    msg.attach(logo)

    to_addr = candidate["email"]
    msg["From"]    = SENDER
    msg["To"]      = to_addr
    msg["CC"]      = ", ".join(CC)
    msg["Subject"] = SUBJECT

    all_recipients = [to_addr] + CC
    allow_candidate_addresses([to_addr])

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER, PASSWORD)
        safe_sendmail(server, SENDER, all_recipients, msg.as_string(),
                      context=f"job36_debrief_{candidate['first_name']}")


if __name__ == "__main__":
    for c in CANDIDATES:
        send_one(c)
    print("\nAll done.")
