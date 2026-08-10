#!/usr/bin/env python3
"""
Keep-in-Touch Note — Skill 06 candidate-invite family (type #5)

Post-conversation "warm hold": we already spoke with the candidate, the role is
being revisited, and we want them to know they are still in our thinking — WITHOUT
promising a timeline or an outcome.

Two deliberate differences from the other 4 invite types:
  1. NO calendar booking button and NO booking/document links — we are not asking
     the candidate to schedule anything yet.
  2. NON-COMMITTAL copy — no "we will reach out" / hard date. Honest + warm only.

Design is otherwise the LOCKED invite template
(memory/locked_email_template_interview_invites_FINAL_2026_05_13.md).

Pilot sends ONE sample to Ayesha for approval. Live loops CANDIDATES and sends
each person an INDIVIDUAL email (one recipient each — never a shared To/CC that
exposes the group).
"""

import sys
sys.path.insert(0, 'c:/Agent Coco')

from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import os
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# Recipient list — POPULATE with exactly the people the user names.
#   "name"  = first name used in the greeting + subject line
#   "email" = candidate's email address
# Nothing is hardcoded: leave this empty and the script refuses to send.
CANDIDATES = [
    {"name": "Falah", "email": "falah.khan1511@gmail.com"},
    {"name": "Kanooz", "email": "kanoozay@gmail.com"},
    {"name": "Nirmal", "email": "nirmal.khalil28@gmail.com"},
    {"name": "Mushahid", "email": "mushahid.qau514@gmail.com"},
    {"name": "Saadia", "email": "Saadia.academicfora@gmail.com"},
]

ROLE = "Fundraising & Partnerships Manager"

PILOT_MODE = True
PILOT_TO = "ayesha.khan@taleemabad.com"

# Live CC mirrors the Job 32 exploratory-call sends.
LIVE_CC = [
    "ayesha.khan@taleemabad.com",
    "hiring@taleemabad.com",
    "sabeena.abbasi@taleemabad.com",
]

SENDER = "ayesha.khan@taleemabad.com"
LOGO_PATH = "c:/Agent Coco/assets/logo_taleemabad.png"


def subject_for(first_name):
    """Subject (user's pick). Warm, no promise."""
    return f"A Note to Stay Connected — {first_name}"


# ---------------------------------------------------------------------------
# HTML body — LOCKED invite design, button + links removed
# ---------------------------------------------------------------------------
def build_html(first_name):
    return f"""
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #f5f5f5;
            font-family: Georgia, Cambria, "Times New Roman", serif;
        }}
        a {{
            color: #3d63c8;
            text-decoration: underline;
        }}
        p {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 17px;
            line-height: 1.85;
            color: #111111;
            font-weight: 400;
            margin: 0 0 26px 0;
        }}
        strong {{
            font-weight: 700;
        }}
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
                                <!-- Header -->
                                <tr>
                                    <td style="padding:34px 64px 30px 64px; text-align:center;">
                                        <!-- Logo -->
                                        <div style="margin-bottom:16px;">
                                            <img src="cid:taleemabad_logo" alt="Taleemabad" width="34" height="34" style="width:34px; height:auto;">
                                        </div>

                                        <!-- Top Label -->
                                        <div style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:12px; letter-spacing:2.4px; font-weight:500; text-transform:uppercase; color:#3157b7; line-height:1.4; margin:0 0 18px 0;">
                                            TALENT ACQUISITION • KEEPING IN TOUCH
                                        </div>

                                        <!-- Main Heading -->
                                        <h1 style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:24px; line-height:1.2; font-weight:700; color:#3157b7; margin:0 0 10px 0; text-align:center;">
                                            Keeping in Touch
                                        </h1>

                                        <!-- Subtitle -->
                                        <p style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:13px; line-height:1.5; color:#5d73b8; text-align:center; margin:0; font-weight:400;">
                                            An honest note on where things stand
                                        </p>
                                    </td>
                                </tr>

                                <!-- Divider -->
                                <tr>
                                    <td style="border-top:2px solid #4b67d1; height:0; padding:0; margin:0;"></td>
                                </tr>

                                <!-- Body Content -->
                                <tr>
                                    <td style="padding:44px 64px 52px 64px; text-align:left;">
                                        <p style="margin-bottom:30px;">Hi {first_name},</p>

                                        <p>
                                            Thank you again for the conversation we had a few weeks ago about the {ROLE} role. It was a genuine pleasure to learn more about you and the work you care about.
                                        </p>

                                        <p>
                                            I wanted to send a brief, honest note so you are not left wondering where things stand. We are currently revisiting this role, and rather than go quiet while we do, we wanted you to know that our conversation stayed with us and that you are still very much in our thinking.
                                        </p>

                                        <p>
                                            While we cannot put a firm date on it just yet, our hope is to be back in touch sometime in July, once the picture is a little clearer. We simply did not want the wait to read as silence on our end.
                                        </p>

                                        <p>
                                            Thank you for the time you have already shared with us, and for your patience while we work this through.
                                        </p>
                                    </td>
                                </tr>

                                <!-- Signature -->
                                <tr>
                                    <td style="padding:0 64px 52px 64px; text-align:left; font-family:Georgia,Cambria,'Times New Roman',serif;">
                                        <!-- Divider -->
                                        <div style="border-top:1px solid #d9d9d9; margin-top:22px; margin-bottom:28px;"></div>

                                        <!-- Signature Content -->
                                        <p style="font-size:16px; color:#5c5c5c; line-height:1.7; margin:0 0 10px 0; font-weight:400;">Warm regards,</p>

                                        <p style="font-size:18px; font-weight:700; color:#111111; line-height:1.6; margin:0 0 6px 0;">People and Culture Team</p>

                                        <p style="font-size:18px; font-weight:700; color:#2f5fc7; line-height:1.6; margin:0 0 10px 0;">Taleemabad</p>

                                        <p style="font-size:16px; line-height:1.7; color:#2f5fc7; margin:0 0 18px 0;">
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


def build_message(first_name, to_list, cc_list):
    """Build one related MIME message with the logo embedded inline."""
    msg = MIMEMultipart('related')
    msg['Subject'] = subject_for(first_name)
    msg['From'] = SENDER
    msg['To'] = ', '.join(to_list)
    if cc_list:
        msg['Cc'] = ', '.join(cc_list)

    msg_alt = MIMEMultipart('alternative')
    msg.attach(msg_alt)
    msg_alt.attach(MIMEText(build_html(first_name), 'html'))

    try:
        with open(LOGO_PATH, 'rb') as f:
            img_data = f.read()
        img = MIMEImage(img_data, 'png')
        img.add_header('Content-ID', '<taleemabad_logo>')
        img.add_header('Content-Disposition', 'inline', filename=LOGO_PATH.split('/')[-1])
        msg.attach(img)
    except Exception as e:
        print(f"Warning: Could not load {LOGO_PATH}: {e}")

    return msg


def send():
    """Pilot: one sample to Ayesha. Live: an individual email per candidate."""
    load_dotenv()

    if not CANDIDATES:
        print("ERROR: CANDIDATES is empty. Populate it with exactly the people")
        print("       the user named before sending. Nothing was sent.")
        return False

    password = os.getenv("EMAIL_PASSWORD")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, password)

    try:
        if PILOT_MODE:
            # One personalized render per candidate, all to Ayesha only (no CC).
            for c in CANDIDATES:
                to_list = [PILOT_TO]
                cc_list = []
                msg = build_message(c["name"], to_list, cc_list)
                safe_sendmail(
                    smtp_server=server,
                    sender=SENDER,
                    recipients=to_list + cc_list,
                    message=msg.as_string(),
                    context="keep_in_touch_note_pilot",
                )
                print(f"PILOT ({c['name']}) -> {PILOT_TO} | Subject: {subject_for(c['name'])}")
            print(f"All {len(CANDIDATES)} pilot renders sent to {PILOT_TO} (no CC).")
            print("Type: KEEP-IN-TOUCH NOTE (no booking button)")
        else:
            for c in CANDIDATES:
                allow_candidate_addresses([c["email"]])
                to_list = [c["email"]]
                cc_list = LIVE_CC
                msg = build_message(c["name"], to_list, cc_list)
                ctx = "keep_in_touch_note_live_" + c["name"].replace(" ", "_")
                safe_sendmail(
                    smtp_server=server,
                    sender=SENDER,
                    recipients=to_list + cc_list,
                    message=msg.as_string(),
                    context=ctx,
                )
                print(f"LIVE sent to {c['email']} ({c['name']})")
            print(f"Done. {len(CANDIDATES)} individual emails sent.")
        return True
    except Exception as e:
        print("Error: " + str(e))
        return False
    finally:
        server.quit()


if __name__ == '__main__':
    send()
