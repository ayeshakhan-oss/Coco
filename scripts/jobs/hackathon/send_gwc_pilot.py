#!/usr/bin/env python3
"""
Send GWC rejection email drafts to Ayesha and Aymen for pilot review.
"""

import os, sys, smtplib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scripts.utils.safe_send import safe_sendmail

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Read all 6 drafts
drafts = [
    ('Ali Jawad', 'scripts/jobs/hackathon/ali_jawad_warm_800.txt'),
    ('Umair Solangi', 'scripts/jobs/hackathon/umair_solangi_warm_800.txt'),
    ('Sultan Muhammad Hamad Sheharyar', 'scripts/jobs/hackathon/sultan_sheharyar_warm_800.txt'),
    ('Moaz Nadeem', 'scripts/jobs/hackathon/moaz_nadeem_warm_scorecard.txt'),
    ('Alishba Ramzan', 'scripts/jobs/hackathon/alishba_ramzan_warm_scorecard.txt'),
    ('Maryam Rafaqat', 'scripts/jobs/hackathon/maryam_rafaqat_warm_scorecard.txt'),
]

# Build email body
body = """Hi Ayesha and Aymen,

Here are the 6 GWC rejection email drafts for Hackathon 2026 candidates. Please review for tone, authenticity, and accuracy.

All emails use:
- Matched tone per candidate (frustrated/disappointed/concerned/warm/honest)
- Specific quotes from actual interviews
- No em dashes (SOP compliant)
- Verified - zero fabrication

Ready to send to candidates once you give the go-ahead.

---

"""

# Add all 6 drafts
for name, filepath in drafts:
    with open(filepath, 'r') as f:
        content = f.read()
    body += f"\n{'='*80}\n{content}\n{'='*80}\n"

# Create email
msg = MIMEMultipart("alternative")
msg["From"]    = EMAIL_USER
msg["To"]      = "ayesha.khan@taleemabad.com"
msg["Cc"]      = "aymen.abid@taleemabad.com"
msg["Subject"] = "PILOT: Hackathon 2026 GWC Rejection Emails (6 candidates) - Review & Approve"

msg.attach(MIMEText(body, "plain", "utf-8"))

# Send via SMTP with safe_sendmail
recipients = ["ayesha.khan@taleemabad.com", "aymen.abid@taleemabad.com"]
with smtplib.SMTP("smtp.gmail.com", 587) as s:
    s.ehlo()
    s.starttls()
    s.login(EMAIL_USER, EMAIL_PASSWORD)
    safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(),
                  context="hackathon_gwc_rejection_pilot")

print("[✓] Pilot sent to Ayesha Khan and Aymen Abid")
print("  TO: ayesha.khan@taleemabad.com")
print("  CC: aymen.abid@taleemabad.com")
print("  Subject: PILOT: Hackathon 2026 GWC Rejection Emails (6 candidates) - Review & Approve")
