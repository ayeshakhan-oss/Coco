#!/usr/bin/env python3
"""
CPD Coach Values Interview Invites - Pilot
Send to Ayesha for review
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))
from safe_send import safe_sendmail

load_dotenv()

# Candidates
CANDIDATES = [
    {
        'name': 'Yumna Sohail',
        'email': 'yumna.sohail99@gmail.com'
    },
    {
        'name': 'Namal Javaid',
        'email': 'namal.javaid16@gmail.com'
    },
    {
        'name': 'Rosheen Naeem',
        'email': 'rosheen.naeem@gmail.com'
    }
]

# Job details
POSITION = "CPD Coach"
JD_LINK = "https://docs.google.com/document/d/1pg58RoVWoVO6WQTlGePJPbW_VLF0GkcYrQeG2Ah6G6s/edit?tab=t.0"
BOOKING_LINK = "https://calendar.app.google/Bn6wZHZbQFfC5kDU7"

# Pilot mode
PILOT_MODE = True
PILOT_TO = "ayesha.khan@taleemabad.com"

# Load real Taleemabad logo
logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo_taleemabad.png')
with open(logo_path, 'rb') as f:
    logo_data = f.read()

# Email template
def generate_html(candidate_name):
    return """
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body, p, div, a, span {
            font-family: Georgia, Cambria, "Times New Roman", serif;
            color: #000000;
        }
    </style>
</head>
<body style="margin: 0; padding: 60px 0; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" bgcolor="#f5f5f5">
        <tr>
            <td align="center">
                <table width="620" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
                    <!-- Logo -->
                    <tr>
                        <td align="center" style="padding: 60px 0 24px 0;">
                            <img src="cid:taleemabad_logo" width="48" height="48" style="display: block;">
                        </td>
                    </tr>

                    <!-- Header Label -->
                    <tr>
                        <td align="center" style="padding: 0 70px; font-size: 12px; letter-spacing: 2px; font-weight: bold; color: #4b6cb7; text-transform: uppercase;">
                            PEOPLE &amp; CULTURE • VALUES INTERVIEW
                        </td>
                    </tr>

                    <!-- Title -->
                    <tr>
                        <td align="center" style="padding: 24px 70px 10px; font-size: 28px; font-weight: bold; color: #4169E1; line-height: 1.3;">
                            """ + POSITION + """
                        </td>
                    </tr>

                    <!-- Subtitle -->
                    <tr>
                        <td align="center" style="padding: 0 70px 32px; font-size: 15px; color: #5a6ea8; line-height: 1.4;">
                            A Conversation About Values &amp; Culture Fit
                        </td>
                    </tr>

                    <!-- Divider -->
                    <tr>
                        <td style="padding: 30px 70px 50px; border-top: 1px solid #4169E1;"></td>
                    </tr>

                    <!-- Body Content -->
                    <tr>
                        <td style="padding: 0 70px 40px; font-size: 16px; color: #000000; line-height: 1.75;">
                            <p style="margin: 0 0 18px 0; font-size: 20px; font-weight: bold; color: #4169E1;">Hi """ + candidate_name + """,</p>

                            <p style="margin: 0 0 18px 0;">Thank you for your interest in the """ + POSITION + """ role at Taleemabad. We're impressed with your background and would like to move forward to the next stage of our process.</p>

                            <p style="margin: 0 0 18px 0;">We'd like to invite you to a <strong>45-minute values interview</strong> with our team. This is a conversation where we'll get to know you better and explore how your values and work style align with our culture and mission.</p>

                            <p style="margin: 0 0 18px 0;">Before we meet, we recommend reviewing the <a href=\"""" + JD_LINK + """\" style=\"color: #4169E1; text-decoration: none; font-weight: bold;\">role description</a> to familiarize yourself with the position.</p>

                            <p style="margin: 0 0 18px 0;\"><strong>Please note:</strong> This session will be recorded so we can refer back to it as we evaluate fit.</p>

                            <p style="margin: 0 0 24px 0;\">Use the button below to book your preferred time:</p>
                        </td>
                    </tr>

                    <!-- CTA Button -->
                    <tr>
                        <td align="center" style="padding: 0 70px 40px;">
                            <table cellpadding="0" cellspacing="0">
                                <tr>
                                    <td align="center" bgcolor="#5b3fc4" style="border-radius: 7px; padding: 14px 32px;">
                                        <a href=\"""" + BOOKING_LINK + """\" style=\"color: #ffffff; text-decoration: none; font-size: 16px; font-weight: bold; font-family: Georgia, serif; display: inline-block;\">Book Your Interview</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Additional Info -->
                    <tr>
                        <td style="padding: 0 70px 50px; font-size: 16px; color: #000000; line-height: 1.75;">
                            <p style="margin: 0 0 18px 0;\">If you have any questions or need to reschedule, please don't hesitate to reach out.</p>

                            <p style="margin: 0 0 0 0;\">We look forward to speaking with you soon!</p>
                        </td>
                    </tr>

                    <!-- Signature -->
                    <tr>
                        <td style="padding: 40px 70px 60px; border-top: 1px solid #d0d0d0; font-size: 16px; color: #000000; line-height: 1.75;">
                            <p style="margin: 0 0 12px 0; font-weight: bold;\">Warm regards,</p>
                            <p style="margin: 0 0 0 0;\"><strong>Ayesha Khan</strong><br>People &amp; Culture<br>Taleemabad</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

# Send pilots
try:
    PASSWORD = os.getenv("EMAIL_PASSWORD")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("ayesha.khan@taleemabad.com", PASSWORD)

    for candidate in CANDIDATES:
        msg = MIMEMultipart('alternative')
        subject = "[PILOT – ] Values Interview Invite: " + candidate['name'] + " – " + POSITION
        msg['Subject'] = subject
        msg['From'] = "ayesha.khan@taleemabad.com"
        msg['To'] = PILOT_TO

        html_content = generate_html(candidate['name'])
        msg.attach(MIMEText(html_content, 'html'))

        # Attach logo
        img = MIMEImage(logo_data, 'png')
        img.add_header('Content-ID', '<taleemabad_logo>')
        img.add_header('Content-Disposition', 'inline')
        msg.attach(img)

        # Send
        safe_sendmail(
            server,
            "ayesha.khan@taleemabad.com",
            [PILOT_TO],
            msg.as_string(),
            context="cpd_coach_values_interview_pilot_" + candidate['name'].lower().replace(' ', '_')
        )

        print(f"[SUCCESS] Pilot sent for {candidate['name']}")

    server.quit()
    print(f"\n[COMPLETE] All 3 pilots sent to {PILOT_TO}")

except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)
