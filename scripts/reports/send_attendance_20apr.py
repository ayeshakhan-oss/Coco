#!/usr/bin/env python3
"""Send attendance report for April 20, 2026 to Ayesha."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from dotenv import load_dotenv
from utils.safe_send import safe_sendmail

load_dotenv()

# Configuration
SENDER = "coco@taleemabad.com"
RECIPIENTS = ["ayesha.khan@taleemabad.com"]
SUBJECT = "Attendance Report — I-10 Head Office (20 April 2026)"
PDF_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "Attendance_20Apr2026_I10.pdf")

HTML_BODY = """
<html>
<body style="font-family: Arial, sans-serif;">
<p>Hi Ayesha,</p>
<p>This is today's attendance report.</p>
<br>
<table style="width: 100%; border-collapse: collapse;">
  <tr>
    <td style="padding: 20px; text-align: center; background-color: #f5f5f5;">
      <div style="font-size: 24px; font-weight: bold;">84</div>
      <div style="font-size: 12px;">Total Active</div>
    </td>
    <td style="padding: 20px; text-align: center; background-color: #e8f5e9;">
      <div style="font-size: 24px; font-weight: bold;">52</div>
      <div style="font-size: 12px;">Onsite Today</div>
    </td>
    <td style="padding: 20px; text-align: center; background-color: #ffe0b2;">
      <div style="font-size: 24px; font-weight: bold;">6</div>
      <div style="font-size: 12px;">On Leave</div>
    </td>
    <td style="padding: 20px; text-align: center; background-color: #e3f2fd;">
      <div style="font-size: 24px; font-weight: bold;">12</div>
      <div style="font-size: 12px;">WFH</div>
    </td>
    <td style="padding: 20px; text-align: center; background-color: #f3e5f5;">
      <div style="font-size: 24px; font-weight: bold;">7</div>
      <div style="font-size: 12px;">WFH Confirmed</div>
    </td>
    <td style="padding: 20px; text-align: center; background-color: #f3e5f5;">
      <div style="font-size: 24px; font-weight: bold;">6</div>
      <div style="font-size: 12px;">Additional</div>
    </td>
    <td style="padding: 20px; text-align: center; background-color: #ffebee;">
      <div style="font-size: 24px; font-weight: bold;">1</div>
      <div style="font-size: 12px;">Flagged</div>
    </td>
  </tr>
</table>
</body>
</html>
"""

# Connect to Gmail
SERVER = "smtp.gmail.com"
PORT = 587

try:
    server = smtplib.SMTP(SERVER, PORT)
    server.starttls()
    server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))

    # Create email
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = ", ".join(RECIPIENTS)
    msg["Subject"] = SUBJECT

    # Attach body
    msg.attach(MIMEText(HTML_BODY, "html"))

    # Attach PDF
    with open(PDF_FILE, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(PDF_FILE)}")
    msg.attach(part)

    # Send via safe_sendmail
    safe_sendmail(
        server,
        SENDER,
        RECIPIENTS,
        msg.as_string(),
        context="attendance_report_20apr2026"
    )

    print("[SUCCESS] Attendance report sent to Ayesha")
    server.quit()

except FileNotFoundError:
    print(f"ERROR: PDF file not found at {PDF_FILE}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
