#!/usr/bin/env python3
"""
Test: Send GWC decision emails as PLAIN TEXT to isolate the issue.
If this works, we know the problem is HTML/MIME structure.
If this doesn't work, the problem is text extraction.
"""
import os, sys, smtplib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from scripts.utils.safe_send import safe_sendmail

load_dotenv()

SENDER = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")

def extract_email_body(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    # Normalize line endings
    content = content.replace("\r\n", "\n")
    lines = content.split("\n")
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("Dear "):
            body_start = i
            break
    body_text = "\n".join(lines[body_start:]).strip()
    return body_text

# Read all 6 drafts
drafts = [
    ("Ali Jawad", "scripts/jobs/hackathon/ali_jawad_warm_800.txt"),
    ("Umair Solangi", "scripts/jobs/hackathon/umair_solangi_warm_800.txt"),
    ("Sultan Muhammad Hamad Sheharyar", "scripts/jobs/hackathon/sultan_sheharyar_warm_800.txt"),
    ("Moaz Nadeem", "scripts/jobs/hackathon/moaz_nadeem_warm_scorecard.txt"),
    ("Alishba Ramzan", "scripts/jobs/hackathon/alishba_ramzan_warm_scorecard.txt"),
    ("Maryam Rafaqat", "scripts/jobs/hackathon/maryam_rafaqat_warm_scorecard.txt"),
]

print("\n=== SENDING GWC DECISION EMAILS - PLAIN TEXT TEST ===\n")

try:
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER, PASSWORD)
    print("[OK] Connected to Gmail SMTP\n")

    for name, filepath in drafts:
        body_text = extract_email_body(filepath)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "[PILOT] Decision of Hackathon - Taleemabad"
        msg["From"] = SENDER
        msg["To"] = "ayesha.khan@taleemabad.com"
        msg["Cc"] = "aymen.abid@taleemabad.com"

        msg.attach(MIMEText(body_text, "plain"))

        safe_sendmail(
            s,
            SENDER,
            ["ayesha.khan@taleemabad.com", "aymen.abid@taleemabad.com"],
            msg.as_string(),
            context=f"hackathon_decision_test_plain_{name.replace(' ', '_')}"
        )
        print(f"[OK] Sent plain text test email for {name} ({len(body_text)} chars)")

    s.quit()
    print(f"\n" + "="*60)
    print(f"Sent 6 plain text test emails to:")
    print(f"  TO: ayesha.khan@taleemabad.com")
    print(f"  CC: aymen.abid@taleemabad.com")
    print(f"="*60)

except Exception as e:
    print(f"[FAILED] {e}")
    import traceback
    traceback.print_exc()
