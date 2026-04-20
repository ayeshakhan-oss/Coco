#!/usr/bin/env python3
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

subject = f"Soul Architect - Prioritized by PRODUCT THINKING + BUILDER + HUMAN (Tier 1-4) - 2026-04-16"

html_body = """<html><body style="font-family: Georgia, serif; font-size: 14px; color: #1a1a1a; line-height: 1.6; max-width: 700px; margin: auto; background: #f0f4f0; padding: 24px 0;">
<table width="700" cellpadding="0" cellspacing="0" style="background: #ffffff; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 16px;">
  <tr><td style="padding: 32px;">
      <p style="margin: 0 0 16px; font-size: 14px;">Hi Ayesha,</p>
      <p style="margin: 0 0 16px; font-size: 14px; line-height: 1.7;">
        Here's the <strong>Soul Architect slate reorganized by PRODUCT THINKING + BUILDER + HUMAN signals</strong>. 
        51 people reclassified into 4 tiers based on ownership, shipping track record, and human-centered depth.
      </p>
      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">Tiers (START WITH TIER 1)</h3>
      <ul style="margin: 0 0 16px; padding-left: 20px;">
        <li><strong>TIER 1 (Green - 8 people):</strong> Strongest match — Product thinking + shipping track + human depth. Start here.</li>
        <li><strong>TIER 2 (Gold - 11 people):</strong> Strong product + builder OR human signals. Clear ownership history.</li>
        <li><strong>TIER 3 (Orange - 10 people):</strong> Solid product thinking, some builder/human signals.</li>
        <li><strong>TIER 4 (Gray - 24 engineers):</strong> Strong technical execution, product growth potential.</li>
      </ul>
      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">What's Screened For</h3>
      <ul style="margin: 0 0 16px; padding-left: 20px;">
        <li><strong>Product Mindset:</strong> Ownership, tradeoffs, user/outcome focus</li>
        <li><strong>Builder Orientation:</strong> Shipped products, uses tools, executes independently</li>
        <li><strong>Human-Centered:</strong> User research, behavioral understanding, psychology/anthropology background or mindset</li>
        <li><strong>Comfort w/ Ambiguity:</strong> Early-stage, founder, or scrappy execution experience</li>
      </ul>
      <p style="margin: 0 0 12px; font-size: 13px; padding: 12px; background: #f5f5f5; border-left: 4px solid #1565c0; border-radius: 4px;">
        <strong>File attached:</strong> Soul_Architect_PRIORITIZED_ByProductThinking_2026-04-16.xlsx
      </p>
      <p style="margin: 0; font-size: 13px; color: #888;">Warm regards,<br/><strong>Coco</strong><br/>Talent Sourcing Agent | Taleemabad</p>
    </td></tr></table>
</body></html>"""

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = EMAIL_USER
msg["To"] = "ayesha.khan@taleemabad.com"
recipients = ["ayesha.khan@taleemabad.com"]

msg.attach(MIMEText(html_body, "html", "utf-8"))

file_path = "c:\Agent Coco\output\sourcing\Soul_Architect_PRIORITIZED_ByProductThinking_2026-04-16.xlsx"
if os.path.exists(file_path):
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=Soul_Architect_PRIORITIZED_2026-04-16.xlsx')
        msg.attach(part)
else:
    print(f"[ERROR] File not found")
    sys.exit(1)

try:
    allow_candidate_addresses(recipients)
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo()
        s.starttls()
        s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(), context="soul_architect_prioritized")
    print("[SENT] Soul Architect PRIORITIZED sheet sent to ayesha.khan@taleemabad.com")
except Exception as e:
    print(f"[ERROR] {str(e)}")
    sys.exit(1)
