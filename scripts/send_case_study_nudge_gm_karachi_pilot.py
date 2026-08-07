#!/usr/bin/env python3
"""
Case Study Reminder (gentle nudge) — Growth Manager - Karachi: Muneeb Arif + Waqas Hassan.
Context: Markaz sent both the case study on 2026-08-04 (~6am); 48-hour window passed the
morning of 2026-08-06 with no submission. Ayesha's brief (2026-08-06): "just nudge them,
that its been more than 48 hours, just wanted to check if you're going to submit the case
study, do you need any help/assistance, we're here to support."
Design: locked interview-invite template (FINAL_2026_05_13). No CTA button — reply-to-help flow.
PILOT_MODE=True → each email to Ayesha ONLY, [PILOT - ] prefix.
"""
import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

sys.path.insert(0, r"c:\Agent Coco")
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(r"c:\Agent Coco\.env")

SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")
LOGO_PATH = r"c:\Agent Coco\assets\logo_taleemabad.png"

PILOT_MODE = False
PILOT_TO = "ayesha.khan@taleemabad.com"
LIVE_CC = ["waqas.tanveer@taleemabad.com", "ayesha.khan@taleemabad.com", "hiring@taleemabad.com", "ali.sipra@taleemabad.com"]

POSITION = "Growth Manager - Karachi"

CANDIDATES = [
    {"first": "Muneeb", "full": "Muneeb Arif", "email": "muneebarifkhalid@gmail.com"},
    {"first": "Waqas", "full": "Waqas Hassan", "email": "waqashassan5@hotmail.com"},
]

HTML_TEMPLATE = """
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; padding: 0; background: #f5f5f5; font-family: Georgia, Cambria, "Times New Roman", serif; }
        a { color: #3d63c8; text-decoration: underline; }
        p { font-family: Georgia, Cambria, "Times New Roman", serif; font-size: 17px; line-height: 1.85; color: #111111; font-weight: 400; margin: 0 0 26px 0; }
        strong { font-weight: 700; }
    </style>
</head>
<body>
    <table width="100%" bgcolor="#f5f5f5" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center">
                <table width="calc(100% - 90px)" bgcolor="#e5e7e2" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
                    <tr>
                        <td align="center" style="padding-top:38px; padding-bottom:38px;">
                            <table width="775" bgcolor="#ffffff" cellpadding="0" cellspacing="0" border="0" style="width:775px; max-width:775px; margin:0 auto;">
                                <tr>
                                    <td style="padding:34px 64px 30px 64px; text-align:center;">
                                        <div style="margin-bottom:16px;">
                                            <img src="cid:taleemabad_logo" alt="Taleemabad" width="34" height="34" style="width:34px; height:auto;">
                                        </div>
                                        <div style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:12px; letter-spacing:2.4px; font-weight:500; text-transform:uppercase; color:#3157b7; line-height:1.4; margin:0 0 18px 0;">
                                            TALENT ACQUISITION &bull; CASE STUDY CHECK-IN
                                        </div>
                                        <h1 style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:24px; line-height:1.2; font-weight:700; color:#3157b7; margin:0 0 10px 0; text-align:center;">
                                            Checking In on Your Case Study
                                        </h1>
                                        <p style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:13px; line-height:1.5; color:#5d73b8; text-align:center; margin:0; font-weight:400;">
                                            {position}
                                        </p>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="border-top:2px solid #4b67d1; height:0; padding:0; margin:0;"></td>
                                </tr>
                                <tr>
                                    <td style="padding:44px 64px 52px 64px; text-align:left;">
                                        <p style="margin-bottom:30px;">Hi {first_name},</p>
                                        <p>
                                            I hope you're doing well.
                                        </p>
                                        <p>
                                            We shared the case study for the <strong>{position}</strong> role with you
                                            on Monday. We just wanted to check in, as we haven't received your submission yet.
                                        </p>
                                        <p>
                                            We completely understand that schedules can get busy, so we wanted to see if
                                            you're still planning to submit the case study. If so, we'd appreciate it if
                                            you could let us know when we can expect your submission.
                                        </p>
                                        <p>
                                            If you have any questions, need any clarification, or require a little more
                                            time, please don't hesitate to reply to this email. We're happy to help and
                                            accommodate where we can.
                                        </p>
                                        <p>
                                            We look forward to hearing from you and reading your submission.
                                        </p>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:0 64px 52px 64px; text-align:left; font-family:Georgia,Cambria,'Times New Roman',serif;">
                                        <div style="border-top:1px solid #d9d9d9; margin-top:22px; margin-bottom:28px;"></div>
                                        <p style="font-size:16px; color:#5c5c5c; line-height:1.7; margin:0 0 10px 0; font-weight:400;">Warm regards,</p>
                                        <p style="font-size:18px; font-weight:700; color:#111111; line-height:1.6; margin:0 0 6px 0;">People and Culture Team</p>
                                        <p style="font-size:18px; font-weight:700; color:#2f5fc7; line-height:1.6; margin:0 0 10px 0;">Taleemabad</p>
                                        <p style="font-size:16px; line-height:1.7; color:#2f5fc7; margin:0;">
                                            <a href="mailto:hiring@taleemabad.com" style="color:#2f5fc7; text-decoration:underline;">hiring@taleemabad.com</a> <span style="color:#7d7d7d; margin:0 10px;">|</span> <a href="https://www.taleemabad.com" style="color:#2f5fc7; text-decoration:underline;">www.taleemabad.com</a>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

def build_message(candidate, pilot):
    subject = f"Checking In: Your Case Study for {POSITION} - {candidate['full']}"
    if pilot:
        subject = f"[PILOT - ] {subject}"
    html = (HTML_TEMPLATE
            .replace("{first_name}", candidate["first"])
            .replace("{position}", POSITION))
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = SENDER
    if pilot:
        recipients = [PILOT_TO]
        msg["To"] = PILOT_TO
    else:
        recipients = [candidate["email"]] + LIVE_CC
        msg["To"] = candidate["email"]
        msg["Cc"] = ", ".join(LIVE_CC)
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html, "html"))
    msg.attach(alt)
    with open(LOGO_PATH, "rb") as f:
        img = MIMEImage(f.read(), "png")
    img.add_header("Content-ID", "<taleemabad_logo>")
    img.add_header("Content-Disposition", "inline")
    msg.attach(img)
    return msg, recipients, subject

def main():
    if not PILOT_MODE:
        allow_candidate_addresses([c["email"] for c in CANDIDATES])
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    for c in CANDIDATES:
        msg, recipients, subject = build_message(c, pilot=PILOT_MODE)
        mode = "PILOT" if PILOT_MODE else "LIVE"
        safe_sendmail(server, SENDER, recipients, msg.as_string(),
                      context=f"{mode} case study nudge GM-Karachi -> {c['full']}")
        print(f"{mode} sent: {subject} -> {recipients}")
    server.quit()
    print("DONE")

if __name__ == "__main__":
    main()
