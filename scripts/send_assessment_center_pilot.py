#!/usr/bin/env python3
"""
Assessment Center Activity Invite — Skill 06, invite type #7 (added 2026-07-31)
Onsite full-day assessment invite. Locked interview-invite design (FINAL 2026-05-13).
Sends pilot to Ayesha for approval before going live.
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
CANDIDATE_NAME = "Sarah Mitchell"   # sample for pilot; replace per candidate for live
CANDIDATE_FIRST = "Sarah"
POSITION = "CPD Coach"
ACTIVITY_DATE = "Thursday, August 6, 2026"
START_TIME = "10:30 AM"
END_TIME = "5:00 PM"
CONFIRM_BY_DATE = "Monday, August 3, 2026"  # calendar invitation goes out by this day to confirmed candidates
VENUE_ADDRESS = "Service Rd W, Sector H-9/1, Islamabad, 44000, Pakistan"
VENUE_MAP_LINK = "https://maps.app.goo.gl/wmSUN8BKUBkhaeYA8"

PILOT_MODE = True
PILOT_TO = "ayesha.khan@taleemabad.com"

# Email addresses — PILOT: Ayesha ONLY, no CC (locked rule 2026-06-08)
TO = [PILOT_TO] if PILOT_MODE else ["candidate.email@example.com"]
CC = [] if PILOT_MODE else ["ayesha.khan@taleemabad.com", "hiring@taleemabad.com"]

BASE_SUBJECT = f"Invitation to the Assessment Center Activity for {POSITION} - {CANDIDATE_NAME}"
SUBJECT = f"[PILOT – ] {BASE_SUBJECT}" if PILOT_MODE else BASE_SUBJECT

# HTML Email Body — LOCKED DESIGN (locked_email_template_interview_invites_FINAL_2026_05_13.md)
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
                                            TALENT ACQUISITION • ASSESSMENT CENTER ACTIVITY
                                        </div>

                                        <!-- Main Heading -->
                                        <h1 style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:24px; line-height:1.2; font-weight:700; color:#3157b7; margin:0 0 10px 0; text-align:center;">
                                            Invitation to Our Assessment Center Activity
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
                                        <p style="margin-bottom:30px;">Hi {CANDIDATE_FIRST},</p>

                                        <p>
                                            Congratulations on making it to the next stage of our recruitment
                                            process! We're excited to invite you to our Assessment Center Activity.
                                        </p>

                                        <p>
                                            This will be an onsite activity taking place on <strong>{ACTIVITY_DATE}</strong>,
                                            starting promptly at <strong>{START_TIME}</strong> and continuing until
                                            <strong>{END_TIME}</strong>. We kindly request that you arrive on time so you
                                            can fully participate in the day's activities.
                                        </p>

                                        <p>
                                            <strong>Venue:</strong> {VENUE_ADDRESS} — <a href="{VENUE_MAP_LINK}">view on Google Maps</a>.
                                        </p>

                                        <p>
                                            If you're joining us from outside Islamabad, please let us know by
                                            replying to this email so we can coordinate accordingly.
                                        </p>

                                        <p>
                                            To confirm your attendance, kindly reply to this email with your
                                            acknowledgement. We will send the Google Calendar invitation by
                                            <strong>{CONFIRM_BY_DATE}</strong> to the candidates who have confirmed.
                                        </p>

                                        <p style="margin-bottom:0;">
                                            We look forward to meeting you and wish you the very best for this stage
                                            of the process. If you have any questions, please feel free to reach out.
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

                                        <p style="font-size:16px; font-weight:700; line-height:1.7; margin:0 0 4px 0;">
                                            <a href="https://www.linkedin.com/in/ayesha-raza-khan-386668177/" style="color:#2f5fc7; text-decoration:underline;">Ayesha Raza Khan</a>
                                        </p>
                                        <p style="font-size:16px; line-height:1.7; color:#111111; margin:0;">
                                            03354288844
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

def send_pilot():
    """Send Assessment Center Activity invite (pilot to Ayesha)"""
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
            context="assessment_center_invite_pilot"
        )

        server.quit()

        print("Pilot sent to " + TO[0])
        print("Subject: " + SUBJECT)
        print("Candidate: " + CANDIDATE_NAME)
        print("Position: " + POSITION)
        print("Type: ASSESSMENT CENTER ACTIVITY")
        return True
    except Exception as e:
        print("Error: " + str(e))
        return False

if __name__ == '__main__':
    send_pilot()
