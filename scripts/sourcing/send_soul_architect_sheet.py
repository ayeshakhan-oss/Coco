#!/usr/bin/env python3
"""
Send Soul Architect talent sheet (Excel) as email attachment to Ayesha
"""

import os
import sys
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from dotenv import load_dotenv
import importlib.util

# Import safe_send
safe_send_path = os.path.join(os.path.dirname(__file__), "../utils/safe_send.py")
spec = importlib.util.spec_from_file_location("safe_send", safe_send_path)
safe_send = importlib.util.module_from_spec(spec)
spec.loader.exec_module(safe_send)
safe_sendmail = safe_send.safe_sendmail
allow_candidate_addresses = safe_send.allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Email details
subject = f"Soul Architect Sourcing - Mid-Level Talent Sheet (11 Candidates) - {datetime.now().strftime('%Y-%m-%d')}"

html_body = """
<html>
<body style="font-family: Georgia, serif; font-size: 14px; color: #1a1a1a; line-height: 1.6; max-width: 700px; margin: auto; background: #f0f4f0; padding: 24px 0;">

<table width="700" cellpadding="0" cellspacing="0" style="background: #ffffff; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 16px;">
  <tr>
    <td style="padding: 32px;">
      <p style="margin: 0 0 16px; font-size: 14px;">Hi Ayesha,</p>

      <p style="margin: 0 0 16px; font-size: 14px; line-height: 1.7;">
        Here's the <strong>Soul Architect talent slate</strong> — focused on <strong>mid-level professionals with 3-4 years experience</strong>.
        All 11 candidates have verified LinkedIn profiles and are product-focused: Product Designers, APMs, AI Engineers, UX professionals.
      </p>

      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">What's Included in the Sheet</h3>
      <ul style="margin: 0 0 16px; padding-left: 20px;">
        <li><strong>Name</strong> — Full candidate name</li>
        <li><strong>Current Role</strong> — Exact title</li>
        <li><strong>Company</strong> — Current employer</li>
        <li><strong>Location</strong> — City (all Islamabad/Pakistan-based)</li>
        <li><strong>LinkedIn URL</strong> — Direct link to verified profile</li>
        <li><strong>Why Relevant</strong> — Specific experience (3-4 years focus)</li>
      </ul>

      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">Candidate Breakdown</h3>
      <ul style="margin: 0 0 16px; padding-left: 20px;">
        <li><strong>Product Designers:</strong> 5 candidates (4-5 years, SaaS + EdTech + product thinking)</li>
        <li><strong>Product Leaders:</strong> 3 candidates (AI + 10Pearls/Arbisoft product experience)</li>
        <li><strong>AI/ML Engineers:</strong> 1 candidate (ML engineer, product context)</li>
        <li><strong>Product & AI Strategist:</strong> 1 candidate (chatbot + product strategy, consulting)</li>
        <li><strong>Design Leaders:</strong> 1 candidate (Product + Design integration)</li>
      </ul>

      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">Next Steps</h3>
      <ol style="margin: 0 0 16px; padding-left: 20px;">
        <li>Review the attached Excel sheet (scroll right to see all columns)</li>
        <li>Decide which candidates you'd like to reach out to</li>
        <li>Copy their LinkedIn URL and visit their profile</li>
        <li>Send a personalized message via LinkedIn (template available on request)</li>
        <li>When you get confirmed interest: "Name confirmed interest, add for Soul Architect"</li>
        <li>Coco will add them to Markaz with all relevant details</li>
      </ol>

      <p style="margin: 0 0 12px; font-size: 13px; padding: 12px; background: #f5f5f5; border-left: 4px solid #1565c0; border-radius: 4px;">
        <strong>File attached:</strong> Soul_Architect_Mid-Level_Talent_2026-04-16.xlsx
      </p>

      <p style="margin: 0; font-size: 13px; color: #888;">
        Warm regards,<br/>
        <strong>Coco</strong><br/>
        Talent Sourcing Agent | Taleemabad<br/>
        hiring@taleemabad.com
      </p>
    </td>
  </tr>
</table>

<table width="700" cellpadding="0" cellspacing="0" style="background: #ffffff; border-radius: 0 0 8px 8px;">
  <tr>
    <td style="padding: 12px 32px; background: #f5f5f5; font-size: 11px; color: #888; border-radius: 0 0 8px 8px; text-align: center;">
      Soul Architect Sourcing | 11 Mid-Level Verified Profiles | April 16, 2026
    </td>
  </tr>
</table>

</body>
</html>
"""

# Prepare email
msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = EMAIL_USER
msg["To"] = "ayesha.khan@taleemabad.com"

recipients = ["ayesha.khan@taleemabad.com"]

# Attach HTML body
msg.attach(MIMEText(html_body, "html", "utf-8"))

# Attach Excel file
file_path = "c:\Agent Coco\output\sourcing\Soul_Architect_Mid-Level_Talent_2026-04-16.xlsx"
if os.path.exists(file_path):
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= Soul_Architect_Mid-Level_Talent_2026-04-16.xlsx')
        msg.attach(part)
    print(f"[ATTACHED] Excel file: {file_path}")
else:
    print(f"[ERROR] File not found: {file_path}")
    sys.exit(1)

# Send email
try:
    allow_candidate_addresses(recipients)
    
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo()
        s.starttls()
        s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(),
                      context="soul_architect_sourcing_midlevel_sheet")

    print("[SENT] Soul Architect talent sheet sent to ayesha.khan@taleemabad.com")
    print(f"Subject: {subject}")
    print(f"Attachment: Soul_Architect_Mid-Level_Talent_2026-04-16.xlsx")

except Exception as e:
    print(f"[ERROR] Failed to send email: {str(e)}")
    sys.exit(1)
