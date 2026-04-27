#!/usr/bin/env python3
"""
CPD Coach Values Interview Invite - Pilot to Ayesha
"""

import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = 'C:/Users/Dell/Downloads/token.json'
creds = Credentials.from_authorized_user_file(TOKEN_FILE, [
    'https://www.googleapis.com/auth/gmail.send'
])
service = build('gmail', 'v1', credentials=creds)

html_body = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Georgia, serif; background-color: #f9f9f9; margin: 0; padding: 0; }
        .container { max-width: 600px; margin: 0 auto; background-color: white; }
        .header { background-color: white; padding: 20px; text-align: center; border-bottom: 3px solid #2E5090; }
        .logo { font-size: 16px; font-weight: bold; color: #333; margin-bottom: 15px; }
        .header-line { color: #2E5090; font-size: 13px; letter-spacing: 1px; margin-bottom: 10px; }
        .position-title { color: #2E5090; font-size: 32px; font-weight: bold; margin: 15px 0; line-height: 1.2; }
        .subtitle { color: #555; font-size: 14px; margin: 0 0 20px 0; }
        .blue-line { height: 3px; background-color: #2E5090; margin: 0; }
        .content { padding: 30px 25px; }
        .content p { font-family: Georgia, serif; font-size: 14px; line-height: 1.6; text-align: justify; color: #333; margin: 0 0 15px 0; }
        .cta-button { display: inline-block; background-color: #2E5090; color: white; padding: 12px 25px; text-decoration: none; border-radius: 4px; font-size: 14px; margin-top: 15px; }
        .footer { padding: 20px 25px; background-color: #f5f5f5; font-size: 12px; color: #777; text-align: center; border-top: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Taleemabad</div>
            <div class="header-line">VALUES INTERVIEW INVITATION</div>
            <div class="position-title">CPD Coach</div>
            <div class="subtitle">Taleemabad Program</div>
        </div>
        <div class="blue-line"></div>

        <div class="content">
            <p>Dear Candidate,</p>

            <p>We are excited to invite you to the values interview stage for the CPD Coach position at Taleemabad. Your application stood out to us, and we would like to learn more about your values, work style, and fit with our organization.</p>

            <p>The values interview is a conversation between you and our team about how your personal values align with Taleemabad's mission. We are looking to understand your motivations, your approach to working with teachers, and how you navigate complex educational challenges.</p>

            <p>This is not a technical interview. Instead, we want to have an authentic conversation about what drives you as an educator and a professional.</p>

            <p>Please select a time that works best for you from the calendar below:</p>

            <p style="text-align: center; margin: 25px 0;">
                <a href="https://calendar.app.google/YvKqEK16Tax7PGyy5" class="cta-button">Book Your Interview Slot</a>
            </p>

            <p>If you have any questions about the interview format or need to reschedule, please reach out to us directly.</p>

            <p>We look forward to speaking with you.</p>

            <p>Best regards,<br>
            Taleemabad Talent Acquisition Team</p>
        </div>

        <div class="footer">
            <p>Taleemabad Consulting. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

def send_pilot():
    """Send pilot invite to Ayesha for review."""

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'CPD Coach Values Interview Invite Template - Pilot'
    msg['From'] = 'Taleemabad Markaz Hiring <hiring@taleemabad.com>'
    msg['To'] = 'ayesha.khan@taleemabad.com'

    msg.attach(MIMEText(html_body, 'html'))

    try:
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        result = service.users().messages().send(userId='me', body={'raw': raw}).execute()

        print(f"\nPilot sent to Ayesha for review.")
        print(f"Message ID: {result['id']}")
        print("Template ready for use with candidate names.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    send_pilot()
