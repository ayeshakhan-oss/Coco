#!/usr/bin/env python3
"""
Send live case study invite emails to candidates with CC list
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "utils"))
from safe_send import safe_sendmail, allow_candidate_addresses
from dotenv import load_dotenv

# Load .env
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

# Configuration
SENDER = os.getenv("EMAIL_USER")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("EMAIL_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("EMAIL_PORT", 587))
LOGO_PATH = r"c:\Agent Coco\assets\logo_taleemabad.png"

# CC recipients
CC_RECIPIENTS = [
    "fahad.rao@taleemabad.com",
    "hiring@taleemabad.com",
    "ayesha.khan@taleemabad.com"
]

# Candidates
CANDIDATES = [
    {"name": "Subtain Ali", "email": "dhanial.subtain2011@gmail.com"},
    {"name": "Altamash Mumtaz", "email": "altamash_mumtaz@hotmail.com"},
]

def create_html_content(candidate_name):
    """Generate HTML content for a specific candidate"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ margin: 0; padding: 40px 20px; background-color: #f5f5f5; font-family: Georgia, Cambria, serif; }}
        .container {{ max-width: 700px; margin: 0 auto; background: #ffffff; padding: 60px 50px; }}
        .logo {{ text-align: center; margin-bottom: 40px; }}
        .logo img {{ display: block; margin: 0 auto; width: 48px; height: 48px; border-radius: 0; }}
        .title {{ text-align: center; font-family: Georgia, serif; font-size: 32px; font-weight: bold; color: #1565C0; line-height: 1.4; margin: 0 0 15px 0; }}
        .subtitle {{ text-align: center; font-family: Georgia, serif; font-size: 16px; font-style: italic; color: #1565C0; line-height: 1.5; margin: 0 0 30px 0; }}
        .divider {{ height: 2px; background-color: #1565C0; margin: 30px 0 40px 0; }}
        .body {{ font-family: Georgia, serif; font-size: 15px; color: #333; line-height: 1.75; text-align: left; }}
        .body p {{ margin: 0 0 18px 0; }}
        .greeting {{ font-weight: normal; margin-bottom: 18px; }}
        a {{ color: #1565C0; text-decoration: none; }}
        .signature {{ margin-top: 40px; padding-top: 15px; border-top: 1px solid #ddd; font-size: 14px; color: #666; font-family: Georgia, serif; }}
        .signature-name {{ font-weight: bold; color: #333; margin: 5px 0 0 0; font-size: 14px; }}
        .signature-company {{ font-weight: bold; color: #1565C0; margin: 0; font-size: 14px; }}
        .signature-coco {{ font-size: 13px; color: #888; margin: 10px 0 0 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="cid:logo_taleemabad" alt="Taleemabad" />
        </div>

        <div class="title">{candidate_name}, We're Moving Forward</div>
        <div class="subtitle">Your next step in the interview process</div>

        <div class="divider"></div>

        <div class="body">
            <p class="greeting">Hi {candidate_name},</p>

            <p>We hope you're doing well.</p>

            <p>We're delighted to share that you've successfully cleared our Values Round, congratulations! We genuinely enjoyed our conversations with you and are excited to continue moving forward together.</p>

            <p>As a next step, we'll be sharing a case study with you next week. We're currently completing values interviews with a few other candidates and expect to wrap those up by the end of this week. Once that process is complete, we'll send the case study to all candidates who have successfully cleared the Values Round.</p>

            <p>Thank you for your patience and continued interest in Taleemabad. We're looking forward to the next stage of the process and to learning more about how you approach the challenge ahead.</p>
        </div>

        <div class="signature">
            Warm regards,<br />
            <div class="signature-name">People and Culture Team</div>
            <div class="signature-company">Taleemabad</div>
            <br />
            <a href="mailto:hiring@taleemabad.com">hiring@taleemabad.com</a> | <a href="http://www.taleemabad.com">www.taleemabad.com</a>
            <br /><br />
            <div class="signature-coco">Sent on behalf of Talent Acquisition Team by Coco</div>
        </div>
    </div>
</body>
</html>"""

def send_live(candidate_name, candidate_email):
    """Send live email to one candidate with CC list"""
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER, SENDER_PASSWORD)

        # Allow candidate email for safe_sendmail bouncer
        allow_candidate_addresses([candidate_email])

        # Create message with related content (for embedded images)
        msg = MIMEMultipart("related")
        msg["Subject"] = f"Your Next Step: Case Study Round at Taleemabad"
        msg["From"] = SENDER
        msg["To"] = candidate_email
        msg["Cc"] = ", ".join(CC_RECIPIENTS)

        # Attach HTML
        msg_alternative = MIMEMultipart("alternative")
        msg.attach(msg_alternative)
        html_content = create_html_content(candidate_name)
        msg_alternative.attach(MIMEText(html_content, "html"))

        # Attach logo image with Content-ID
        if os.path.exists(LOGO_PATH):
            with open(LOGO_PATH, "rb") as attachment:
                img_part = MIMEImage(attachment.read(), name=os.path.basename(LOGO_PATH))
                img_part.add_header("Content-ID", "<logo_taleemabad>")
                img_part.add_header("Content-Disposition", "inline", filename=os.path.basename(LOGO_PATH))
                msg.attach(img_part)

        # Combine TO and CC for sending
        all_recipients = [candidate_email] + CC_RECIPIENTS

        # Send via safe_sendmail
        safe_sendmail(
            server,
            SENDER,
            all_recipients,
            msg.as_string(),
            context=f"case_study_invite_live_{candidate_name.replace(' ', '_')}"
        )

        server.quit()
        print(f"LIVE EMAIL SENT: {candidate_name} ({candidate_email})")
        print(f"  CC: {', '.join(CC_RECIPIENTS)}")
        return True

    except Exception as e:
        print(f"ERROR ({candidate_name}): {str(e)}")
        return False

if __name__ == "__main__":
    print("Sending live case study invite emails...\n")

    for candidate in CANDIDATES:
        send_live(candidate["name"], candidate["email"])
        print()

    print("All live emails sent.")
