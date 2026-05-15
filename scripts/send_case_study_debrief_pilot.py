#!/usr/bin/env python3
"""
Case Study Debrief Invite — Production template with locked design
Sends to Ayesha for approval before going live
"""

import sys
sys.path.insert(0, 'c:/Agent Coco')

from scripts.utils.safe_send import safe_sendmail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import os
from dotenv import load_dotenv

# Configuration
CANDIDATE_NAME = "Alex Johnson"
POSITION = "Product Designer"
DEBRIEF_LINK = "https://calendar.google.com/calendar/u/0/r/eventedit?text=Case%20Study%20Debrief%20-%20Alex%20Johnson"

PILOT_MODE = True
PILOT_TO = "ayesha.khan@taleemabad.com"

# Email addresses
TO = [PILOT_TO] if PILOT_MODE else ["alex.johnson@example.com"]
CC = [] if PILOT_MODE else ["ayesha.khan@taleemabad.com", "hiring@taleemabad.com"]

SUBJECT = f"Case Study Debrief — {POSITION} — {CANDIDATE_NAME}"

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
        .callout {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 17px;
            line-height: 1.85;
            font-weight: 700;
            color: #3d63c8;
            margin: 26px 0 26px 0;
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
                                            TALENT ACQUISITION • CASE STUDY DEBRIEF
                                        </div>

                                        <!-- Main Heading -->
                                        <h1 style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:24px; line-height:1.2; font-weight:700; color:#3157b7; margin:0 0 10px 0; text-align:center;">
                                            Case Study Debrief
                                        </h1>

                                        <!-- Subtitle -->
                                        <p style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:13px; line-height:1.5; color:#5d73b8; text-align:center; margin:0; font-weight:400;">
                                            {POSITION}
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
                                            Thank you for submitting your case study for the <strong>{POSITION}</strong> role.
                                            We've reviewed your work and would like to invite you for a <strong>30-minute debrief interview</strong>
                                            to discuss your approach, thinking, and the decisions you made.
                                        </p>

                                        <p>
                                            This conversation is an opportunity for us to understand how you think through problems and for you
                                            to learn more about the role and our team. Please come prepared to walk us through your submission
                                            and discuss any questions we might have.
                                        </p>

                                        <!-- CTA Button -->
                                        <div style="text-align:center; margin:40px 0 28px 0;">
                                            <a href="{DEBRIEF_LINK}" style="background:#5b3fc4; color:#ffffff; font-size:16px; font-weight:700; font-family:Georgia,Cambria,'Times New Roman',serif; text-decoration:none; border-radius:7px; padding:14px 34px; display:inline-block; text-align:center;">📅 Schedule Your Debrief</a>
                                        </div>

                                        <p class="button-subtitle">Please book a time that works best for you.</p>

                                        <p>
                                            We look forward to hearing your insights. Let us know if you have any questions beforehand.
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
    """Send case study debrief pilot to Ayesha"""
    load_dotenv()

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
            context="case_study_debrief_invite_pilot"
        )

        server.quit()

        print("Pilot sent to " + TO[0])
        print("Subject: " + SUBJECT)
        print("Candidate: " + CANDIDATE_NAME)
        print("Position: " + POSITION)
        print("Type: CASE STUDY DEBRIEF")
        return True
    except Exception as e:
        print("Error: " + str(e))
        return False

if __name__ == '__main__':
    send_pilot()
