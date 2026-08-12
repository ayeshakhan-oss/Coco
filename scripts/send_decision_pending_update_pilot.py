#!/usr/bin/env python3
"""
Warm Hold — Decision-Pending Update ("A Quick Note from Our Side")
Skill 01 type #5, added 2026-08-12. Locked generic template (Ayesha's wording,
approved 2026-08-12) — placeholders only: [Candidate Name]/[Role Name]/[Day/Date].
Layout: v8 (Rule 8) imported from scripts/utils/v8_template.py.

First use: CPD Coach (Job 17) assessment-center candidates, 2026-08-12.
PILOT_MODE=True -> one pilot per candidate to Ayesha ONLY (no CC),
subject "[PILOT - Name] A Quick Note from Our Side".
PILOT_MODE=False -> individual live emails, CC ayesha + hiring@, clean subject.
"""
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

sys.path.insert(0, r"c:\Agent Coco")
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
from scripts.utils.v8_template import P, FOOTER, wrap, attach_logo, EYEBROW

load_dotenv(r"c:\Agent Coco\.env")
SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")

PILOT_MODE = False  # Ayesha approved live send 2026-08-12
PILOT_TO = "ayesha.khan@taleemabad.com"
LIVE_CC = ["ayesha.khan@taleemabad.com", "bilal@niete.edu.pk",
           "hiring@taleemabad.com", "ali.sipra@taleemabad.com"]  # per Ayesha 2026-08-12

POSITION = "CPD Coach"
UPDATE_BY = "Friday, August 21, 2026"   # confirm with Ayesha before live - promised date
BASE_SUBJECT = "A Quick Note from Our Side"

# Assessment-center (6 Aug) candidates chosen by Ayesha 2026-08-12
CANDIDATES = [
    {"first": "Hajra",   "full": "Hajra Sajjad",    "email": "hajra2357@gmail.com"},
    {"first": "Iram",    "full": "Iram Nisar",      "email": "iram.nisar@gmail.com"},
    {"first": "Misbah",  "full": "Misbah Kokab",    "email": "misbah_kokab@yahoo.com"},
    {"first": "Naima",   "full": "Naima Javed",     "email": "naimajaved89@gmail.com"},
    {"first": "Samra",   "full": "Samra Nazeer",    "email": "samranazeer89@gmail.com"},
    {"first": "Wasima",  "full": "Wasima Naz",      "email": "nazwasima666@gmail.com"},
    {"first": "Yumna",   "full": "Yumna Sohail",    "email": "yumna.sohail99@gmail.com"},
    {"first": "Zunaira", "full": "Zunaira Anum",    "email": "zunairaanum72@gmail.com"},
    {"first": "Namal",   "full": "Namal Javaid",    "email": "namal.javaid16@gmail.com"},
]

# Sign-off: Ayesha's locked template uses "Warmly," (2026-08-12) - content swap only,
# layout untouched.
FOOTER_WARMLY = FOOTER.replace("Warm regards,", "Warmly,")


def build_body(first_name):
    # 🔒 LOCKED generic template - Ayesha's wording verbatim, placeholders only.
    return (
        P(f"Hi {first_name},")
        + P("We hope you're doing well.")
        + P(f"Thank you again for taking the time to interview with us for the "
            f"<strong>{POSITION}</strong> position. It was great getting to know more "
            f"about your experience and background.")
        + P(f"We're currently wrapping up a few internal discussions and consolidating "
            f"feedback from the interview process before we make a final decision. We "
            f"wanted to keep you in the loop and let you know that we expect to share "
            f"an update with you by <strong>{UPDATE_BY}</strong>.")
        + P("Thank you for your patience and for your continued interest in joining "
            "Taleemabad. We really appreciate the time and effort you've invested in "
            "the process.")
        + FOOTER_WARMLY
    )


def build_message(c, pilot):
    subject = f"[PILOT - {c['full']}] {BASE_SUBJECT}" if pilot else BASE_SUBJECT
    html = wrap(subject_line=BASE_SUBJECT, role=POSITION,
                eyebrow=EYEBROW["warm_hold"], body_html=build_body(c["first"]))
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = SENDER
    if pilot:
        recipients = [PILOT_TO]
        msg["To"] = PILOT_TO
    else:
        recipients = [c["email"]] + LIVE_CC
        msg["To"] = c["email"]
        msg["Cc"] = ", ".join(LIVE_CC)
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html, "html"))
    msg.attach(alt)
    attach_logo(msg)
    return msg, recipients, subject


def main():
    if not PILOT_MODE:
        allow_candidate_addresses([c["email"] for c in CANDIDATES])
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    for c in CANDIDATES:
        msg, recipients, subject = build_message(c, pilot=PILOT_MODE)
        ctx = ("PILOT warm-hold decision-pending update "
               f"({c['full']}, CPD Coach) to Ayesha only" if PILOT_MODE
               else f"LIVE warm-hold decision-pending update -> {c['full']} (CPD Coach)")
        safe_sendmail(server, SENDER, recipients, msg.as_string(), context=ctx)
        print(f"{'PILOT' if PILOT_MODE else 'LIVE'} sent: {subject} -> {recipients[0]}")
    server.quit()
    print(f"DONE - {len(CANDIDATES)} {'pilots to Ayesha' if PILOT_MODE else 'live emails'}.")


if __name__ == "__main__":
    main()
