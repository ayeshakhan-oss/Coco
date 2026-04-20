"""Send Attendance Report — 16 April 2026"""
import os, sys, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
load_dotenv(os.path.join(os.path.dirname(__file__), "../..", ".env"))

from scripts.utils.safe_send import safe_sendmail

# Email config
SENDER_EMAIL = "ayesha.khan@taleemabad.com"
RECIPIENTS = ["ayesha.khan@taleemabad.com"]  # User requested: send to Ayesha only
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Gmail App Password
APP_PASSWORD = os.getenv("EMAIL_PASSWORD")

# PDF path
pdf_path = os.path.join(os.path.dirname(__file__), "Attendance_16Apr2026_I10.pdf")

if not os.path.exists(pdf_path):
    print(f"ERROR: PDF file not found at {pdf_path}")
    sys.exit(1)

# Create message
msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = ", ".join(RECIPIENTS)
msg["Date"] = formatdate(localtime=True)
msg["Subject"] = "I-10 Attendance Report — Thursday, 16 April 2026"

# Email body
body = """Hi Ayesha,

Please find attached the I-10 Head Office Attendance Record for Thursday, 16 April 2026.

SUMMARY:
• Total Active: 84
• Onsite: 47
• On Leave: 6
• WFH Confirmed: 7
• Additional (Non-Payroll): 8
• Flagged: 25

The PDF contains detailed breakdown by category with all names and statuses.

Best,
Coco
Talent Acquisition Agent
"""

msg.attach(MIMEText(body, "plain"))

# Attach PDF
try:
    with open(pdf_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=Attendance_16Apr2026_I10.pdf")
        msg.attach(part)
except FileNotFoundError as e:
    print(f"ERROR: Could not read PDF file: {e}")
    sys.exit(1)

# Send email
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)

    safe_sendmail(
        server,
        SENDER_EMAIL,
        RECIPIENTS,
        msg.as_string(),
        context="attendance_16apr2026"
    )

    server.quit()
    print(f"[SUCCESS] Attendance report sent to: {', '.join(RECIPIENTS)}")
except Exception as e:
    print(f"ERROR sending email: {e}")
    sys.exit(1)
