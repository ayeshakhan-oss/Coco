#!/usr/bin/env python3
"""
Exploratory Call Invite — Production template with locked design
For candidates who don't match current openings but are interesting
Sends to Ayesha for approval before going live
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

# Configuration
CANDIDATE_NAME = "Falah Khan"
BOOKING_LINK = "https://calendar.app.google/r1Rj1b1UMiAqonDs5"
DOCUMENT_LINK = "https://drive.google.com/file/d/1VV_gcRRBpt8LtYeILsRzAF320D4jP-Kv/view?usp=sharing"

PILOT_MODE = False
PILOT_TO = "ayesha.khan@taleemabad.com"

# Email addresses
TO = [PILOT_TO] if PILOT_MODE else ["falah.khan1511@gmail.com"]
CC = [] if PILOT_MODE else ["ayesha.khan@taleemabad.com", "hiring@taleemabad.com", "sabeena.abbasi@taleemabad.com"]

SUBJECT = f"Let's Chat — {CANDIDATE_NAME}"

# HTML Email Body — LOCKED DESIGN
HTML_BODY = f"""
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
        .button-subtitle {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 16px;
            line-height: 1.6;
            color: #111111;
            text-align: center;
            margin: 18px 0 0 0;
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
                                            TALENT ACQUISITION • EXPLORATORY CALL
                                        </div>

                                        <!-- Main Heading -->
                                        <h1 style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:24px; line-height:1.2; font-weight:700; color:#3157b7; margin:0 0 10px 0; text-align:center;">
                                            Let's Chat
                                        </h1>

                                        <!-- Subtitle -->
                                        <p style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:13px; line-height:1.5; color:#5d73b8; text-align:center; margin:0; font-weight:400;">
                                            An opportunity to explore a potential fit
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
                                        <p style="margin-bottom:30px;">Hi {CANDIDATE_NAME},</p>

                                        <p>
                                            Thank you for expressing your interest when we reached out to connect, we really appreciate your openness to having a conversation with us.
                                        </p>

                                        <p>
                                            We'd love to invite you for a short exploratory conversation with the Taleemabad team. The call would be around 30 minutes and would primarily be an opportunity for us to understand your experience, skills, and aspirations better, while also giving you a chance to learn more about Taleemabad, the work we're building, and the kind of challenges we're solving.
                                        </p>

                                        <p>
                                            We're approaching this as an open conversation, and while there may not be a specific role tied to it immediately, we genuinely hope that somewhere down the line there could be an opportunity for us to work together.
                                        </p>

                                        <p>
                                            I'm also attaching <a href="{DOCUMENT_LINK}">Fundraising & Partnerships Overview</a> for additional context ahead of the conversation.
                                        </p>

                                        <!-- CTA Button -->
                                        <div style="text-align:center; margin:40px 0 28px 0;">
                                            <a href="{BOOKING_LINK}" style="background:#5b3fc4; color:#ffffff; font-size:16px; font-weight:700; font-family:Georgia,Cambria,'Times New Roman',serif; text-decoration:none; border-radius:7px; padding:14px 34px; display:inline-block; text-align:center;">📅 Let's Chat</a>
                                        </div>

                                        <p class="button-subtitle">Pick a time that works for you.</p>

                                        <p>
                                            Looking forward to connecting.
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

                                        <p style="font-size:15px; line-height:1.7; color:#9a9a9a; margin:0; font-weight:400;">Sent on behalf of Talent Acquisition Team by Coco</p>
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

def send_pilot():
    """Send exploratory call invite"""
    load_dotenv()

    # Whitelist candidate address for bouncer (if live send)
    if not PILOT_MODE:
        allow_candidate_addresses(TO)

    try:
        msg = MIMEMultipart('related')
        msg['Subject'] = SUBJECT
        msg['From'] = 'ayesha.khan@taleemabad.com'
        msg['To'] = ', '.join(TO)
        if CC:
            msg['Cc'] = ', '.join(CC)

        msg_alt = MIMEMultipart('alternative')
        msg.attach(msg_alt)
        msg_alt.attach(MIMEText(HTML_BODY, 'html'))

        logo_files = {
            'taleemabad_logo': 'c:/Agent Coco/assets/logo_taleemabad.png',
        }

        for cid, filepath in logo_files.items():
            try:
                with open(filepath, 'rb') as f:
                    img_data = f.read()
                img = MIMEImage(img_data, 'png')
                img.add_header('Content-ID', f'<{cid}>')
                img.add_header('Content-Disposition', 'inline', filename=filepath.split('/')[-1])
                msg.attach(img)
            except Exception as e:
                print(f"Warning: Could not load {filepath}: {e}")

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        password = os.getenv("EMAIL_PASSWORD")
        server.login("ayesha.khan@taleemabad.com", password)

        safe_sendmail(
            smtp_server=server,
            sender="ayesha.khan@taleemabad.com",
            recipients=TO + CC,
            message=msg.as_string(),
            context="exploratory_call_invite_pilot"
        )

        server.quit()

        print("Pilot sent to " + TO[0])
        print("Subject: " + SUBJECT)
        print("Candidate: " + CANDIDATE_NAME)
        print("Type: EXPLORATORY CALL")
        return True
    except Exception as e:
        print("Error: " + str(e))
        return False

if __name__ == '__main__':
    send_pilot()
