#!/usr/bin/env python3
"""
Values Interview Invite — Head of Accounts and Finance (DUMMY/PILOT)
Uses LOCKED FINAL template (2026-05-13)
"""

import os
import sys
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

# Setup paths
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from utils.safe_send import safe_sendmail, allow_candidate_addresses

# Load environment
load_dotenv(dotenv_path=os.path.join(Path(__file__).parent.parent, ".env"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Configuration
POSITION = "Head of Accounts and Finance"
CANDIDATE_NAME = "Subtain Ali"
CANDIDATE_EMAIL = "dhanial.subtain2011@gmail.com"
CALENDAR_LINK = "https://calendar.app.google/wCuouLGPCfoBKUUGA"
JD_LINK = "https://docs.google.com/document/d/1Raz3aRTdmR7ICatqud9UJXrE8ja-E2rwI5jV0WTXL-A/edit?usp=sharing"
PREP_GUIDE_LINK = "https://docs.google.com/document/d/dummy-prep-guide"

# Email content (HTML) — EXACT LOCKED TEMPLATE (2026-05-13)
html_body = f"""
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
        ul {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            margin: 0 0 26px 0;
            padding-left: 50px;
        }}
        li {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 17px;
            line-height: 1.85;
            color: #111111;
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
        .signature-warm {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 16px;
            color: #5c5c5c;
            line-height: 1.7;
            margin-bottom: 10px;
            font-weight: 400;
        }}
        .signature-team {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 18px;
            font-weight: 700;
            color: #111111;
            line-height: 1.6;
            margin-bottom: 6px;
        }}
        .signature-org {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 18px;
            font-weight: 700;
            color: #2f5fc7;
            line-height: 1.6;
            margin-bottom: 10px;
        }}
        .signature-contact {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 16px;
            line-height: 1.7;
            color: #2f5fc7;
        }}
        .signature-footer {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 15px;
            line-height: 1.7;
            color: #9a9a9a;
            margin-top: 18px;
            font-weight: 400;
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
                                            TALENT ACQUISITION • VALUES INTERVIEW
                                        </div>

                                        <!-- Main Heading -->
                                        <h1 style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:24px; line-height:1.2; font-weight:700; color:#3157b7; margin:0 0 10px 0; text-align:center;">
                                            Invitation for the Values Interview
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
                                            Thank you for your interest in the <strong>{POSITION}</strong>
                                            role at Taleemabad. We have reviewed your application and would like to
                                            invite you for a <strong>45-minute values conversation</strong>
                                            with our team, to learn more about you and how your persona aligns with the way we work.
                                        </p>

                                        <p>
                                            The JD for this position is <a href="{JD_LINK}">available here</a>. You can also explore more about
                                            Taleemabad and our work:
                                        </p>

                                        <ul>
                                            <li><a href="https://impact-microsite.vercel.app/">10 Years Of Impact - Taleemabad</a></li>
                                        </ul>

                                        <p>
                                            Please go through the <a href="{PREP_GUIDE_LINK}">interview prep guide</a> to understand what to expect from
                                            this conversation. The prep guide contains information on Taleemabad's values, the role,
                                            and what we'll be discussing.
                                        </p>

                                        <p class="callout">
                                            Please note: Conversations will be recorded for internal use only.
                                        </p>

                                        <p>
                                            We look forward to learning more about you. If you have any questions in the meantime, please feel free to reach out.
                                        </p>

                                        <!-- CTA Button -->
                                        <div style="text-align:center; margin:40px 0 28px 0;">
                                            <a href="{CALENDAR_LINK}" style="background:#5b3fc4; color:#ffffff; font-family:Georgia,Cambria,'Times New Roman',serif; font-size:16px; font-weight:700; padding:14px 34px; border-radius:7px; text-decoration:none; display:inline-block;">
                                                Lock Your Interview Slot
                                            </a>
                                        </div>

                                        <div class="button-subtitle">
                                            Please select a time at your earliest convenience.
                                        </div>
                                    </td>
                                </tr>

                                <!-- Signature Section -->
                                <tr>
                                    <td style="padding:10px 64px 18px 64px; text-align:left; border-top:1px solid #d9d9d9; margin-top:22px;">
                                        <div class="signature-warm">Warm regards,</div>
                                        <div class="signature-team">People and Culture Team</div>
                                        <div class="signature-org">Taleemabad</div>
                                        <div class="signature-contact">
                                            <a href="mailto:ayesha.khan@taleemabad.com" style="color:#2f5fc7; text-decoration:underline;">ayesha.khan@taleemabad.com</a>
                                            |
                                            <a href="https://taleemabad.com" style="color:#2f5fc7; text-decoration:underline;">taleemabad.com</a>
                                        </div>
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

def main():
    # Build message with related for CID-embedded images
    msg = MIMEMultipart("related")
    msg["Subject"] = f"Invitation for the Values Interview - {POSITION}"
    msg["From"] = EMAIL_USER
    msg["To"] = CANDIDATE_EMAIL
    msg["Cc"] = "ayesha.khan@taleemabad.com, hiring@taleemabad.com, fahad.rao@taleemabad.com"

    # Attach HTML as alternative
    msg_alt = MIMEMultipart("alternative")
    msg.attach(msg_alt)
    msg_alt.attach(MIMEText(html_body, "html", "utf-8"))

    # Embed logo
    logo_path = "c:/Agent Coco/assets/logo_taleemabad.png"
    try:
        with open(logo_path, "rb") as f:
            img_data = f.read()
        img = MIMEImage(img_data, "png")
        img.add_header("Content-ID", "<taleemabad_logo>")
        img.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
        msg.attach(img)
    except Exception as e:
        print(f"Warning: Could not load logo: {e}")

    # Send via SMTP with safe_sendmail
    recipients = [CANDIDATE_EMAIL, "ayesha.khan@taleemabad.com", "hiring@taleemabad.com", "fahad.rao@taleemabad.com"]

    # Approve candidate address
    allow_candidate_addresses([CANDIDATE_EMAIL])

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo()
        s.starttls()
        s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(
            s,
            EMAIL_USER,
            recipients,
            msg.as_string(),
            context="values_interview_invite_head_of_accounts_finance_altamash_mumtaz"
        )

    print(f"[SENT] Live email sent!")
    print(f"   Position: {POSITION}")
    print(f"   Candidate: {CANDIDATE_NAME}")
    print(f"   To: {CANDIDATE_EMAIL}")
    print(f"   CC: ayesha.khan@taleemabad.com, hiring@taleemabad.com, fahad.rao@taleemabad.com")
    print(f"   Template: LOCKED FINAL (2026-05-13) + CID-embedded logo")

if __name__ == "__main__":
    main()
