#!/usr/bin/env python3
"""
Send Fundraising & Partnerships Manager Screening Report Excel to user
"""
import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
from utils.safe_send import safe_sendmail

# Config
SENDER = os.getenv("EMAIL_USER")
GMAIL_PASS = os.getenv("EMAIL_PASSWORD")
RECIPIENT = "ayesha.khan@taleemabad.com"
EXCEL_FILE = os.path.join(
    os.path.dirname(__file__),
    "reports",
    "Fundraising_Partnerships_Manager_Screening.xlsx"
)

def send_screening_report():
    """Send the Excel screening report to user"""

    if not os.path.exists(EXCEL_FILE):
        print(f"ERROR: File not found: {EXCEL_FILE}")
        sys.exit(1)

    # Create message
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = "Fundraising & Partnerships Manager — Screening Report (Excel)"

    # Body
    body = """Hi Zeshan,

Attached is the Fundraising & Partnerships Manager screening report in Excel format.

Contents:
- Screening Summary: All 10 assessed candidates with scores and verdicts
- Dimension Scores: 7-dimension evaluation heatmap
- Next Steps: 5 recommended actions

Report Date: 05 March 2026
Total Applications: 64 | Assessed: 48 | Shortlisted: 5

Best,
Coco
Taleemabad Talent Acquisition Agent
"""

    msg.attach(MIMEText(body, "plain"))

    # Attach Excel file
    with open(EXCEL_FILE, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {os.path.basename(EXCEL_FILE)}",
    )
    msg.attach(part)

    # Send
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER, GMAIL_PASS)

        # Use safe_sendmail
        safe_sendmail(
            server,
            SENDER,
            [RECIPIENT],
            msg.as_string(),
            context="screening_report_fundraising_partnerships"
        )

        server.quit()
        print(f"SUCCESS: Report sent to {RECIPIENT}")

    except Exception as e:
        print(f"ERROR sending email: {e}")
        sys.exit(1)

if __name__ == "__main__":
    send_screening_report()
