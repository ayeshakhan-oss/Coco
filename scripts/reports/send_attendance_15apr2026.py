"""Send Attendance Report for 15 April 2026"""
import os
import sys
import smtplib
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
RECIPIENTS = [
    "ayesha.khan@taleemabad.com"
]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Gmail App Password
APP_PASSWORD = os.getenv("EMAIL_PASSWORD")

# PDF path
pdf_path = os.path.join(os.path.dirname(__file__), "..", "..", "output", "Attendance_15Apr2026.pdf")

if not os.path.exists(pdf_path):
    print(f"ERROR: PDF file not found at {pdf_path}")
    sys.exit(1)

# Create message
msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = ", ".join(RECIPIENTS)
msg["Date"] = formatdate(localtime=True)
msg["Subject"] = "I-10 Attendance Report — 15 April 2026 (Wednesday)"

# Email body
body = """Hi Ayesha, Jawwad, and Aymen,

Please see the attendance report for today (15 April 2026) attached.

**Summary:**
• Total Active: 84
• Onsite: 52
• On Leave: 5
• WFH: 1
• WFH Confirmed: 8
• Flagged: 18

Best,
Coco
"""

msg.attach(MIMEText(body, "plain"))

# Attach PDF
try:
    with open(pdf_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=Attendance_15Apr2026.pdf")
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
        context="attendance_15apr2026"
    )

    server.quit()
    print(f"[OK] Attendance report sent to: {', '.join(RECIPIENTS)}")
except Exception as e:
    print(f"ERROR sending email: {e}")
    sys.exit(1)
