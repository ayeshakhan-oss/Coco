# -*- coding: utf-8 -*-
"""Job 42 CV-rejection batches 01-04 (40 candidates) — PILOT to Ayesha ONLY.
Rule 4: [PILOT – ] subject => TO = ayesha.khan@taleemabad.com ONLY. NO CC.
Subjects parsed from each draft's header slot; widget appended; logo embedded."""
import os, sys, re, json, glob, time, smtplib
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
SKIP = {3986, 4023, 4053}  # wave-1, already piloted

rec = json.load(open(r"c:\Agent Coco\output\job42\rejection_email_recipients.json", encoding="utf-8"))
names = {r["app_id"]: r["name"] for r in rec["recipients"]}

files = sorted(glob.glob(r"c:\Agent Coco\output\job42\rejection_emails\*.html"))
queue = []
for f in files:
    app_id = int(os.path.basename(f).split("_")[0])
    if app_id in SKIP:
        continue
    html = open(f, encoding="utf-8").read()
    m = re.search(r'font-size:17px;\s*font-weight:bold;color:#1565c0;line-height:1\.4;">\s*(.*?)\s*</p>', html, re.S)
    subject = re.sub(r"\s+", " ", m.group(1)).replace("&amp;", "&") if m else None
    assert subject and "[" not in subject, f"bad subject in {f}"
    queue.append((app_id, names[app_id], subject, f, html))

assert len(queue) == 40, f"expected 40, got {len(queue)}"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(SENDER, PASSWORD)
sent = 0
for app_id, name, subject, path, html in queue:
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
                  context=f"Job 42 CV-rejection batch01-04 PILOT ({name}, app {app_id}) to Ayesha")
    sent += 1
    time.sleep(1.2)

server.quit()
print(f"PILOTS SENT: {sent}/40 to {RECIPIENTS}")
