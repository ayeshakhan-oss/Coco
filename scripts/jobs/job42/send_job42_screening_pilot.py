# Job 42 (Senior Manager Growth) initial screening report - PILOT to Ayesha ONLY
# Rule: [PILOT - ] subject => TO = ayesha.khan@taleemabad.com ONLY. NO CC. (CLAUDE.md Rule 4)
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

sys.path.insert(0, r"c:\Agent Coco")
from scripts.utils.safe_send import safe_sendmail

load_dotenv(r"c:\Agent Coco\.env")

SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENTS = ["ayesha.khan@taleemabad.com"]  # PILOT: Ayesha only, no CC

SUBJECT = "[PILOT – ] Initial Screening Report — Senior Manager Growth (JOB-0042) · 69 CVs read"

html = open(r"c:\Agent Coco\output\job42\job42_smg_screening_pilot.html", encoding="utf-8").read()

msg = MIMEMultipart("alternative")
msg["Subject"] = SUBJECT
msg["From"] = SENDER
msg["To"] = ", ".join(RECIPIENTS)
msg.attach(MIMEText(html, "html"))

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(SENDER, PASSWORD)
safe_sendmail(server, SENDER, RECIPIENTS, msg.as_string(),
              context="Job 42 SMG initial screening report PILOT to Ayesha")
server.quit()
print("PILOT sent to", RECIPIENTS)
