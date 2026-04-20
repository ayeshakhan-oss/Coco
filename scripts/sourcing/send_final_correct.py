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

subject = f"Soul Architect - 22 Product Professionals (Correct URLs) - {datetime.now().strftime('%Y-%m-%d')}"

html_body = """<html><body style="font-family: Georgia, serif; font-size: 14px; color: #1a1a1a;">
<p>Hi Ayesha,</p>
<p>Here's the <strong>Soul Architect slate — 22 mid-level product professionals</strong> with <strong>100% correct working LinkedIn URLs</strong>.</p>
<p>All sourced from verified candidate database. Product roles only. Click links to verify.</p>
<p>When someone confirms interest, tell Coco "[Name] confirmed, add for Soul Architect".</p>
<p>Warm regards,<br/><strong>Coco</strong></p>
</body></html>"""

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = EMAIL_USER
msg["To"] = "ayesha.khan@taleemabad.com"

msg.attach(MIMEText(html_body, "html", "utf-8"))

file_path = r"c:\Agent Coco\output\sourcing\Soul_Architect_FINAL_CORRECT_URLs_2026-04-16.xlsx"
with open(file_path, 'rb') as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename=Soul_Architect_FINAL_CORRECT_URLs_2026-04-16.xlsx')
    msg.attach(part)

allow_candidate_addresses(["ayesha.khan@taleemabad.com"])
with smtplib.SMTP("smtp.gmail.com", 587) as s:
    s.ehlo()
    s.starttls()
    s.login(EMAIL_USER, EMAIL_PASSWORD)
    safe_sendmail(s, EMAIL_USER, ["ayesha.khan@taleemabad.com"], msg.as_string(), context="soul_architect_final_correct")

print("[SENT] Soul Architect 22 candidates with correct LinkedIn URLs")
