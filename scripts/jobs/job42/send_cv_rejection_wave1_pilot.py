# -*- coding: utf-8 -*-
"""Job 42 CV-rejection WAVE 1 — PILOT to Ayesha ONLY (3 archetype emails).
Rule 4: [PILOT – ] subject => TO = ayesha.khan@taleemabad.com ONLY. NO CC.
Feedback widget appended at marker; logo embedded via v8 attach_logo."""
import os, sys, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

sys.path.insert(0, r"c:\Agent Coco")
from scripts.utils.safe_send import safe_sendmail
from scripts.utils.v8_template import attach_logo
from scripts.utils.feedback_widget import feedback_widget

load_dotenv(r"c:\Agent Coco\.env")
SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENTS = ["ayesha.khan@taleemabad.com"]  # PILOT: Ayesha only, no CC

ROLE = "Senior Manager Growth"
WAVE = [
    (3986, "Adnan Riaz", "What 300 negotiations told us about your craft",
     r"c:\Agent Coco\output\job42\rejection_emails\3986_Adnan_Riaz.html"),
    (4023, "Muhammad Naeem Ayubi", "Twenty-eight years of institutional selling, read closely",
     r"c:\Agent Coco\output\job42\rejection_emails\4023_Muhammad_Naeem_Ayubi.html"),
    (4053, "Wasib Javed", "Fifty-seven percent of a region's revenue, and an honest constraint",
     r"c:\Agent Coco\output\job42\rejection_emails\4053_Wasib_Javed.html"),
]

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(SENDER, PASSWORD)

for app_id, name, subject, path in WAVE:
    html = open(path, encoding="utf-8").read()
    html = html.replace("<!-- FEEDBACK_WIDGET_HERE -->",
                        feedback_widget(name, ROLE, app_id, "Application Feedback"))
    msg = MIMEMultipart("related")
    msg["Subject"] = f"[PILOT – {name}] {subject}"
    msg["From"] = SENDER
    msg["To"] = ", ".join(RECIPIENTS)
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html, "html"))
    msg.attach(alt)
    attach_logo(msg)
    safe_sendmail(server, SENDER, RECIPIENTS, msg.as_string(),
                  context=f"Job 42 CV-rejection wave-1 PILOT ({name}) to Ayesha")
    print("PILOT sent:", name)

server.quit()
print("Wave 1 pilot complete:", len(WAVE), "emails to", RECIPIENTS)
