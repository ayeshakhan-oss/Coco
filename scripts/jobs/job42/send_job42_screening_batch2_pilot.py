# Job 42 SMG supplementary screening report (batch 2, late arrivals) - PILOT to Ayesha ONLY
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

SUBJECT = "[PILOT – ] Supplementary Screening (Batch 2) — Senior Manager Growth (JOB-0042) · 10 late arrivals"

html = open(r"c:\Agent Coco\output\job42\job42_smg_screening_batch2_pilot.html", encoding="utf-8").read()

msg = MIMEMultipart("alternative")
msg["Subject"] = SUBJECT
msg["From"] = SENDER
msg["To"] = ", ".join(RECIPIENTS)
msg.attach(MIMEText(html, "html"))

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(SENDER, PASSWORD)
safe_sendmail(server, SENDER, RECIPIENTS, msg.as_string(),
              context="Job 42 SMG batch-2 supplementary screening report PILOT to Ayesha")
server.quit()
print("PILOT sent to", RECIPIENTS)
