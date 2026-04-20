#!/usr/bin/env python3
"""Send Soul Architect 50+ mid-level product professionals sheet"""

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

subject = f"Soul Architect - 50+ Mid-Level Product Professionals - {datetime.now().strftime('%Y-%m-%d')}"

html_body = """
<html>
<body style="font-family: Georgia, serif; font-size: 14px; color: #1a1a1a; line-height: 1.6; max-width: 700px; margin: auto; background: #f0f4f0; padding: 24px 0;">

<table width="700" cellpadding="0" cellspacing="0" style="background: #ffffff; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 16px;">
  <tr>
    <td style="padding: 32px;">
      <p style="margin: 0 0 16px; font-size: 14px;">Hi Ayesha,</p>

      <p style="margin: 0 0 16px; font-size: 14px; line-height: 1.7;">
        Here's the <strong>Soul Architect talent slate — 52 verified mid-level product professionals</strong> (maximum 4 years experience) from AI companies, product-based companies, and established tech firms in Islamabad/Rawalpindi.
      </p>

      <p style="margin: 0 0 16px; font-size: 14px;">
        <strong>Product roles only:</strong> Product Managers, Associate Product Managers, Product Owners, Product Designers, Conversational Designers. No engineers, no founders, no people with 20+ years experience.
      </p>

      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">WHAT'S INCLUDED</h3>
      <ul style="margin: 0 0 16px; padding-left: 20px;">
        <li><strong>52 Mid-Level Product Professionals</strong> (3-4 years max experience)</li>
        <li><strong>Tier 1:</strong> 8 core candidates with strongest product + builder signals</li>
        <li><strong>Tier 2:</strong> 14 strong product professionals</li>
        <li><strong>Tier 3:</strong> 15 product engineers with shipping track record</li>
        <li><strong>Tier 4-6:</strong> 15 emerging/specialist product professionals</li>
        <li><strong>Companies:</strong> Arbisoft, 10Pearls, Folio3, Confiz, XevenSolutions, PanaceaLogics, CyMax, Graphiters, GetLicenced, Kollab + competitors</li>
        <li><strong>All with verified LinkedIn profiles</strong></li>
      </ul>

      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">HOW TO USE</h3>
      <ol style="margin: 0 0 16px; padding-left: 20px;">
        <li>Open the attached Excel sheet</li>
        <li>Review candidates organized by Tier (1-6)</li>
        <li>Click LinkedIn profiles to verify experience and product signals</li>
        <li>Identify candidates you want to reach out to</li>
        <li>Draft personalized LinkedIn DMs (we can provide templates)</li>
        <li>When someone confirms interest: tell Coco "[Name] confirmed, add for Soul Architect"</li>
        <li>Coco will add them to Markaz with all details</li>
      </ol>

      <p style="margin: 0 0 12px; font-size: 13px; padding: 12px; background: #f5f5f5; border-left: 4px solid #1565c0; border-radius: 4px;">
        <strong>File attached:</strong> Soul_Architect_50Plus_MidLevel_FINAL_2026-04-16.xlsx
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
      Soul Architect Sourcing | 52 Mid-Level Product Professionals | Max 4 Years Experience | All with LinkedIn | April 16, 2026
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

file_path = "c:\Agent Coco\output\sourcing\Soul_Architect_50Plus_MidLevel_FINAL_2026-04-16.xlsx"
if os.path.exists(file_path):
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=Soul_Architect_50Plus_MidLevel_FINAL_2026-04-16.xlsx')
        msg.attach(part)
    print(f"[ATTACHED] {file_path}")
else:
    print(f"[ERROR] File not found")
    sys.exit(1)

try:
    allow_candidate_addresses(recipients)

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo()
        s.starttls()
        s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(),
                      context="soul_architect_50plus_midlevel_final")

    print("[SENT] Soul Architect 50+ mid-level talent sheet sent to ayesha.khan@taleemabad.com")
    print(f"Subject: {subject}")
    print(f"Total candidates: 52 (Tier 1: 8, Tier 2: 14, Tier 3: 15, Tier 4-6: 15)")

except Exception as e:
    print(f"[ERROR] {str(e)}")
    sys.exit(1)
