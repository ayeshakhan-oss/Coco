#!/usr/bin/env python3
"""
Dummy interview invite pilot — demonstrates locked template format
Sends to Ayesha for visual review
"""

import sys
sys.path.insert(0, 'c:/Agent Coco')

from scripts.utils.safe_send import safe_sendmail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import base64
import os

# Configuration
CANDIDATE_NAME = "Sarah Mitchell"
POSITION = "CPD Coach"
STAGE_NAME = "WARM BENCH OPPORTUNITY"
BOOKING_LINK = "https://calendar.google.com/calendar/u/0/r/eventedit?text=Interview%20-%20Sarah%20Mitchell"
JD_LINK = "https://docs.google.com/document/d/dummy-jd-link"
TEAMS_LINK = "https://teams.microsoft.com/dummy"

PILOT_MODE = True
PILOT_TO = "ayesha.khan@taleemabad.com"

# Email addresses
TO = [PILOT_TO] if PILOT_MODE else ["sarah.mitchell@example.com"]
CC = [] if PILOT_MODE else ["ayesha.khan@taleemabad.com", "hiring@taleemabad.com"]

SUBJECT = f"A New Opportunity Aligned With Your Profile — {POSITION}"

# HTML Email Body
HTML_BODY = f"""
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: Georgia, serif;
            background-color: #f3f4f6;
            margin: 0;
            padding: 0;
        }}
        .wrapper {{
            background-color: #f3f4f6;
            padding: 60px 0;
            text-align: center;
        }}
        .card {{
            background-color: #ffffff;
            max-width: 620px;
            margin: 0 auto;
            padding: 60px 70px;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
            text-align: left;
        }}
        .logo {{
            text-align: center;
            margin-bottom: 24px;
        }}
        .logo img {{
            width: 48px;
            height: 48px;
        }}
        .header-label {{
            text-align: center;
            font-family: Arial, sans-serif;
            font-size: 12px;
            letter-spacing: 2px;
            color: #4169E1;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 24px;
        }}
        .title {{
            text-align: center;
            font-family: Georgia, serif;
            font-size: 28px;
            font-weight: bold;
            color: #4169E1;
            line-height: 1.3;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            font-family: Georgia, serif;
            font-size: 15px;
            color: #4169E1;
            line-height: 1.4;
            margin-bottom: 32px;
        }}
        .divider {{
            height: 1px;
            background-color: #4169E1;
            margin: 30px 0 50px 0;
        }}
        .greeting {{
            font-family: Georgia, serif;
            font-size: 20px;
            font-weight: bold;
            color: #4169E1;
            line-height: 1.3;
            margin-bottom: 18px;
        }}
        .body-text {{
            font-family: Georgia, serif;
            font-size: 16px;
            color: #000000;
            line-height: 1.75;
            margin-bottom: 18px;
            text-align: left;
        }}
        a {{
            color: #4169E1;
            text-decoration: none;
            font-weight: bold;
        }}
        .cta-button {{
            text-align: center;
            margin: 40px 0 50px 0;
        }}
        .cta-button a {{
            display: inline-block;
            background-color: #663399;
            color: #ffffff;
            font-family: Georgia, serif;
            font-size: 15px;
            font-weight: bold;
            padding: 14px 32px;
            border-radius: 4px;
            text-decoration: none;
        }}
        .button-subtitle {{
            text-align: center;
            font-family: Georgia, serif;
            font-size: 14px;
            color: #4169E1;
            margin: 0 70px 60px 70px;
        }}
        .footer-divider {{
            height: 1px;
            background-color: #e8e8e8;
            margin: 0;
        }}
        .footer {{
            padding: 50px 70px 60px 70px;
            font-family: Georgia, serif;
            color: #4169E1;
            font-size: 14px;
        }}
        .social-row {{
            margin-bottom: 24px;
            text-align: center;
        }}
        .social-row img {{
            margin-right: 12px;
            border-radius: 4px;
            height: 36px;
        }}
        .closing {{
            margin-top: 20px;
            font-family: Georgia, serif;
        }}
        .closing-see {{
            font-size: 16px;
            font-weight: bold;
            color: #000000;
            margin: 0 0 6px 0;
        }}
        .closing-team {{
            font-size: 16px;
            color: #000000;
            margin: 0 0 16px 0;
        }}
        .closing-coco {{
            font-size: 13px;
            color: #5a6ea8;
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="card">
            <!-- Logo -->
            <div class="logo">
                <img src="cid:taleemabad_logo" alt="Taleemabad" width="48" height="48" style="width: 48px; height: 48px;">
            </div>

            <!-- Header Label -->
            <div class="header-label">PEOPLE & CULTURE • {STAGE_NAME}</div>

            <!-- Title -->
            <div class="title">{POSITION}</div>

            <!-- Subtitle -->
            <div class="subtitle">A New Role Aligned With Your Expertise</div>

            <!-- Divider -->
            <div class="divider"></div>

            <!-- Greeting -->
            <div class="greeting">Hi {CANDIDATE_NAME},</div>

            <!-- Body -->
            <div class="body-text">
                You're one of our warm bench candidates, and we're excited about a new {POSITION} role that just opened up. This is a perfect fit for your background, and we'd love to have a quick, informal conversation with you to explore if this role aligns with your career goals.
            </div>

            <div class="body-text">
                This will be a casual chat—no prep needed. We simply want to reconnect and understand how your skills match this new opportunity.
            </div>

            <div class="body-text">
                You can review the job description <a href="{JD_LINK}">here</a>, and explore more about Taleemabad and our impact through these resources:
            </div>

            <div class="body-text">
                • <a href="https://www.youtube.com/watch?v=example">The Magic of Taleemabad</a><br>
                • <a href="https://drive.google.com/example">Our Impact in One Minute</a>
            </div>

            <div class="body-text">
                <strong>Please note:</strong> This session will be recorded, and by joining, you consent to being part of the recorded call. You can also review our <a href="https://docs.google.com/document/d/example">interview prep guide</a> to get a sense of our process.
            </div>

            <div class="body-text">
                Let us know if you need anything ahead of the conversation. Looking forward to hearing from you!
            </div>

            <!-- CTA Button -->
            <div class="cta-button">
                <a href="{BOOKING_LINK}">📅 Lock the Calendar</a>
            </div>

            <!-- Button Subtitle -->
            <div class="button-subtitle">Please lock a slot at your earliest convenience.</div>

            <!-- Footer Divider -->
            <div class="footer-divider"></div>

            <!-- Footer -->
            <div class="footer">
                <div style="margin-bottom: 20px;">Feel free to connect with us on our socials to get a sense of our culture:</div>

                <div class="social-row">
                    <img src="cid:taleemabad_icon" alt="Taleemabad" width="32" height="48" style="width: 32px; height: 48px; margin-right: 16px;">
                    <img src="cid:facebook_icon" alt="Facebook" width="36" height="36" style="width: 36px; height: 36px;">
                    <img src="cid:instagram_icon" alt="Instagram" width="36" height="36" style="width: 36px; height: 36px;">
                    <img src="cid:linkedin_icon" alt="LinkedIn" width="36" height="36" style="width: 36px; height: 36px;">
                </div>

                <div class="closing">
                    <div class="closing-see">See you soon,</div>
                    <div class="closing-team">Team Taleemabad</div>
                    <div class="closing-coco">Coco – AI Assistant Taleemabad</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

def send_pilot():
    """Send dummy pilot to Ayesha"""
    import smtplib
    from dotenv import load_dotenv

    load_dotenv()

    try:
        # Create message
        msg = MIMEMultipart('related')
        msg['Subject'] = SUBJECT
        msg['From'] = 'ayesha.khan@taleemabad.com'
        msg['To'] = ', '.join(TO)
        if CC:
            msg['Cc'] = ', '.join(CC)

        # Attach HTML
        msg_alt = MIMEMultipart('alternative')
        msg.attach(msg_alt)
        msg_alt.attach(MIMEText(HTML_BODY, 'html'))

        # Load real CID-embedded logos from assets
        logo_files = {
            'taleemabad_logo': 'c:/Agent Coco/assets/logo_taleemabad.png',
            'taleemabad_icon': 'c:/Agent Coco/assets/logo_taleemabad.png',
            'facebook_icon': 'c:/Agent Coco/assets/logo_facebook.png',
            'instagram_icon': 'c:/Agent Coco/assets/logo_instagram.png',
            'linkedin_icon': 'c:/Agent Coco/assets/logo_linkedin.png',
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

        # Connect and send via safe_sendmail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        password = os.getenv("EMAIL_PASSWORD")
        server.login("ayesha.khan@taleemabad.com", password)

        safe_sendmail(
            smtp_server=server,
            sender="ayesha.khan@taleemabad.com",
            recipients=TO + CC,
            message=msg.as_string(),
            context="dummy_interview_invite_pilot"
        )

        server.quit()

        print("Pilot sent to " + TO[0])
        print("Subject: " + SUBJECT)
        print("Candidate: " + CANDIDATE_NAME + " (dummy)")
        print("Position: " + POSITION)
        return True
    except Exception as e:
        print("Error: " + str(e))
        return False

if __name__ == '__main__':
    send_pilot()
