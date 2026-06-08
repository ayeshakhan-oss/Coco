#!/usr/bin/env python3
"""
Test: Values Interview Invite — Dummy candidate to Ayesha for design verification
"""

import sys
sys.path.insert(0, 'c:/Agent Coco')

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv

# Load credentials
load_dotenv()
SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")

# Test Configuration
CANDIDATE_NAME = "Test Candidate"
POSITION = "Soul Architect"
JD_LINK = "https://docs.google.com/document/d/1abc123/edit"
PREP_GUIDE_LINK = "https://docs.google.com/document/d/2def456/edit"
BOOKING_LINK = "https://calendar.google.com/calendar/u/0/r/eventedit?text=Values+Interview"

TO = ["ayesha.khan@taleemabad.com"]
SUBJECT = f"[TEST] Values Interview Invite — {CANDIDATE_NAME} for {POSITION}"

# HTML Email Body — Locked Design
HTML_BODY = f"""
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #f3f4f6;
            font-family: Georgia, Cambria, "Times New Roman", serif;
        }}
        a {{
            color: #4169E1;
            text-decoration: none;
            font-weight: bold;
        }}
        p {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 16px;
            line-height: 1.75;
            color: #000000;
            margin: 0 0 18px 0;
        }}
        .header-label {{
            font-family: Arial, sans-serif;
            font-size: 12px;
            letter-spacing: 2px;
            color: #4b6cb7;
            font-weight: bold;
            text-transform: uppercase;
            text-align: center;
            margin: 0 0 24px 0;
        }}
        .title {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 28px;
            font-weight: bold;
            color: #4169E1;
            line-height: 1.3;
            text-align: center;
            margin: 0 0 10px 0;
        }}
        .subtitle {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 15px;
            color: #5a6ea8;
            line-height: 1.4;
            text-align: center;
            margin: 0 0 32px 0;
        }}
        .divider {{
            height: 1px;
            background: #4169E1;
            margin: 30px 0 50px 0;
        }}
        .greeting {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 20px;
            font-weight: bold;
            color: #4169E1;
            line-height: 1.3;
            margin: 0 0 18px 0;
        }}
        .callout {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 16px;
            font-weight: bold;
            color: #4169E1;
            margin: 18px 0 18px 0;
        }}
    </style>
</head>
<body>
    <table width="100%" bgcolor="#f3f4f6" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center" style="padding: 60px 0;">
                <table width="620" bgcolor="#ffffff" cellpadding="0" cellspacing="0" border="0" style="border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
                    <tr>
                        <td align="center" style="padding: 60px 70px 0 70px;">
                            <!-- LOGO -->
                            <img src="cid:taleemabad_logo" width="48" height="48" style="display: block; margin: 0 auto 24px auto;">

                            <!-- HEADER LABEL -->
                            <div class="header-label">PEOPLE & CULTURE • VALUES INTERVIEW</div>

                            <!-- TITLE -->
                            <div class="title">{POSITION}</div>

                            <!-- SUBTITLE -->
                            <div class="subtitle">Interview Opportunity</div>

                            <!-- DIVIDER -->
                            <div class="divider"></div>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding: 0 70px;">
                            <!-- GREETING -->
                            <div class="greeting">Hi {CANDIDATE_NAME},</div>

                            <!-- BODY -->
                            <p>Thank you for your interest in the {POSITION} role at Taleemabad. We're excited to move forward with the next stage of our interview process.</p>

                            <p>We'd like to invite you to a <strong>45-minute values conversation</strong> with our People & Culture team. This is an opportunity for us to learn more about your values, motivations, and how you approach collaboration.</p>

                            <p><span class="callout">This session will be recorded.</span></p>

                            <p>To help you prepare, we've put together a <a href="{PREP_GUIDE_LINK}">brief guide</a> with some background and questions we typically explore. Feel free to review it, but there's no need to over-prepare — we're interested in authentic conversation.</p>

                            <p>Please use the calendar link below to book a time that works for you:</p>

                            <p style="text-align: center; margin: 30px 0;">
                                <a href="{BOOKING_LINK}" style="display: inline-block; background: #4169E1; color: white; padding: 12px 30px; border-radius: 4px; text-decoration: none; font-weight: bold;">📅 Book your Interview</a>
                            </p>

                            <p>If you have any questions or need to reschedule, please don't hesitate to reach out.</p>

                            <p>We look forward to speaking with you soon.</p>

                            <!-- SIGNATURE -->
                            <p style="margin: 40px 0 0 0; border-top: 1px solid #d0d0d0; padding-top: 20px; font-size: 14px;">
                                <strong>People & Culture Team</strong><br/>
                                Taleemabad
                            </p>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding: 0 70px 60px 70px;"></td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

# Create email message
msg = MIMEMultipart("related")
msg["Subject"] = SUBJECT
msg["From"] = SENDER
msg["To"] = ", ".join(TO)

# Attach HTML body
msg_alternative = MIMEMultipart("alternative")
msg.attach(msg_alternative)
msg_alternative.attach(MIMEText(HTML_BODY, "html"))

# Attach logo image (CID embedding)
try:
    with open("c:/Agent Coco/assets/logo_taleemabad.png", "rb") as logo_file:
        logo_img = MIMEImage(logo_file.read())
        logo_img.add_header("Content-ID", "<taleemabad_logo>")
        logo_img.add_header("Content-Disposition", "inline")
        msg.attach(logo_img)
        print("[OK] Logo embedded successfully")
except Exception as e:
    print(f"[WARN] Logo embedding failed: {e}")

# Send email
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    server.sendmail(SENDER, TO, msg.as_string())
    server.quit()
    print(f"[OK] Test email sent to {TO[0]}")
    print(f"  Subject: {SUBJECT}")
    print(f"  Candidate: {CANDIDATE_NAME}")
    print(f"  Position: {POSITION}")
except Exception as e:
    print(f"[ERROR] Email send failed: {e}")
