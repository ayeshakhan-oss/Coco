"""Send attendance report to Ayesha"""
import os
import sys
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from dotenv import load_dotenv
from scripts.utils.safe_send import safe_sendmail

load_dotenv(os.path.join(os.path.dirname(__file__), "../..", ".env"))

# Create email
msg = MIMEMultipart()
msg['Subject'] = 'I-10 Attendance Report — Tuesday, 14 April 2026'
msg['From'] = 'coco@taleemabad.com'
msg['To'] = 'ayesha.khan@taleemabad.com'

body = "Hi Ayesha,\n\nAttached: I-10 Head Office Attendance Report for Tuesday, 14 April 2026.\n\nCompiled by Coco"
msg.attach(MIMEText(body, 'plain'))

# Attach PDF
pdf_path = os.path.join(os.path.dirname(__file__), "..", "..", "output", "Attendance_14Apr2026.pdf")
with open(pdf_path, 'rb') as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f'attachment; filename="Attendance_14Apr2026.pdf"')
msg.attach(part)

# Send via safe_send
EMAIL_USER = os.getenv("EMAIL_USER", "ayesha.khan@taleemabad.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL_USER, EMAIL_PASSWORD)

safe_sendmail(
    server,
    EMAIL_USER,
    ["ayesha.khan@taleemabad.com"],
    msg.as_string(),
    context="attendance_14apr2026"
)

server.quit()
print("✓ Attendance report sent to Ayesha")
