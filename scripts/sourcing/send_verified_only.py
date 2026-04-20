#!/usr/bin/env python3
"""Send corrected Soul Architect sheet - VERIFIED ONLY"""

import os, sys, smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from dotenv import load_dotenv
import importlib.util

safe_send_path = os.path.join(os.path.dirname(__file__), "../utils/safe_send.py")
spec = importlib.util.spec_from_file_location("safe_send", safe_send_path)
safe_send = importlib.util.module_from_spec(spec)
spec.loader.exec_module(safe_send)
safe_sendmail = safe_send.safe_sendmail
allow_candidate_addresses = safe_send.allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

subject = f"Soul Architect - 42 Verified Mid-Level Product Professionals (Corrected) - {datetime.now().strftime('%Y-%m-%d')}"

html_body = """
<html>
<body style="font-family: Georgia, serif; font-size: 14px; color: #1a1a1a; line-height: 1.6; max-width: 700px; margin: auto; background: #f0f4f0; padding: 24px 0;">

<table width="700" cellpadding="0" cellspacing="0" style="background: #ffffff; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 16px;">
  <tr>
    <td style="padding: 32px;">
      <p style="margin: 0 0 16px; font-size: 14px;">Hi Ayesha,</p>

      <p style="margin: 0 0 16px; font-size: 14px; line-height: 1.7;">
        Here's the <strong>corrected Soul Architect slate — 42 verified mid-level product professionals</strong> with <strong>working LinkedIn links</strong>.
      </p>

      <p style="margin: 0 0 16px; font-size: 14px;">
        <strong>My apology:</strong> The previous sheet had fabricated LinkedIn URLs for candidates I couldn't verify. This corrected version contains ONLY verified professionals with confirmed, working links.
      </p>

      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">WHAT'S INCLUDED</h3>
      <ul style="margin: 0 0 16px; padding-left: 20px;">
        <li><strong>42 Verified Product Professionals</strong> (maximum 4 years experience)</li>
        <li><strong>Tier 1 (Core):</strong> 8 candidates with strongest signals</li>
        <li><strong>Tier 2 (Strong):</strong> 14 product professionals</li>
        <li><strong>Tier 3 (Engineers):</strong> 20 with product mindset</li>
        <li><strong>ALL verified LinkedIn links</strong> (100% working)</li>
        <li><strong>Product roles only:</strong> PM, Designer, Engineer with product thinking</li>
        <li><strong>Companies:</strong> Arbisoft, 10Pearls, Folio3, Confiz, Xeven, PanaceaLogics, CyMax, Graphiters, GetLicenced, Kollab</li>
      </ul>

      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">NEXT STEPS</h3>
      <ol style="margin: 0 0 16px; padding-left: 20px;">
        <li>Open attached Excel sheet</li>
        <li>Click LinkedIn profiles to verify each person</li>
        <li>Select candidates you want to reach out to</li>
        <li>Draft personalized LinkedIn DMs</li>
        <li>When confirmed: tell Coco "[Name] confirmed, add for Soul Architect"</li>
      </ol>

      <p style="margin: 0 0 12px; font-size: 13px; padding: 12px; background: #f5f5f5; border-left: 4px solid #1565c0; border-radius: 4px;">
        <strong>File attached:</strong> Soul_Architect_VERIFIED_ONLY_2026-04-16.xlsx
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
      Soul Architect Sourcing | 42 Verified Product Professionals | 100% Working LinkedIn Links | April 16, 2026
    </td>
  </tr>
</table>

</body>
</html>
"""

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = EMAIL_USER
msg["To"] = "ayesha.khan@taleemabad.com"

recipients = ["ayesha.khan@taleemabad.com"]

msg.attach(MIMEText(html_body, "html", "utf-8"))

file_path = r"c:\Agent Coco\output\sourcing\Soul_Architect_VERIFIED_ONLY_2026-04-16.xlsx"
if os.path.exists(file_path):
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=Soul_Architect_VERIFIED_ONLY_2026-04-16.xlsx')
        msg.attach(part)
    print(f"[ATTACHED] {file_path}")
else:
    print(f"[ERROR] File not found: {file_path}")
    sys.exit(1)

try:
    allow_candidate_addresses(recipients)

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo()
        s.starttls()
        s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(),
                      context="soul_architect_verified_only_corrected")

    print("[SENT] Corrected Soul Architect sheet (verified only)")
    print(f"Subject: {subject}")
    print(f"Total: 42 verified candidates with working LinkedIn links")

except Exception as e:
    print(f"[ERROR] {str(e)}")
    sys.exit(1)
