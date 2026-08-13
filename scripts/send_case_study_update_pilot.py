#!/usr/bin/env python3
"""
Case Study Update - Debrief-Pending Email ("A Quick Update from Our Side")
Skill 01 type #6, added 2026-08-13 at Ayesha's request. Sibling of the Warm Hold
Decision-Pending Update (type #5): same "pending, not decided" family, different
trigger (case study SUBMITTED, debrief decision pending).

Skill file: .claude/skills/01_candidate-communication/case-study-update-email.md
Layout: v8 (Rule 8) imported from scripts/utils/v8_template.py - never inline.

Exemptions (inherited from type #5, sanctioned by Ayesha): no "This is not a yes
for now." opening, dated promise REQUIRED, 800-word minimum does not apply
(target 120-250), and "case study" is permitted candidate-facing language for
this type only (it is the candidate's own deliverable).

DO NOT rename this file to contain warm_bench / gwc / values / rejection - the
send-time hook infers the email type from the filename and would validate this
short note as an 800-word feedback letter and HARD BLOCK it.

First use: Job 42 Senior Manager Growth - the 4 candidates who have submitted
their case study (verified in Markaz + Ayesha's mailbox, 2026-08-13).
PILOT_MODE=True  -> one pilot per candidate to Ayesha ONLY (no CC), [PILOT - ] subject.
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

PILOT_MODE = True                      # flip to False ONLY after Ayesha approves the pilots
PILOT_TO = "ayesha.khan@taleemabad.com"
LIVE_CC = ["ayesha.khan@taleemabad.com", "hiring@taleemabad.com"]

POSITION = "Senior Manager Growth"
# Promised timeline - Ayesha's instruction 2026-08-13 ("early next week").
# GUARDRAIL: if this is going to slip, send a fresh note BEFORE it passes.
UPDATE_BY = "early next week"
BASE_SUBJECT = "A Quick Update from Our Side"

# Job 42 candidates who have SUBMITTED their case study (dual-source verified
# 2026-08-13: Markaz case_study_status='submitted' + mailbox sweep).
CANDIDATES = [
    {"first": "Arshan", "full": "Muhammad Arshan Bilal", "email": "bilalarshan1@gmail.com"},   # app 3884, submitted 7 Aug
    {"first": "Junaid", "full": "Junaid Ali",             "email": "ali.junaid58@gmail.com"},  # app 3992, submitted 9 Aug
    {"first": "Arooj",  "full": "Arooj Khalid",           "email": "aroojkh.545@gmail.com"},   # app 3868, submitted 10 Aug
    {"first": "Yusra",  "full": "Yusra Amjad",            "email": "yusra.amjad16@gmail.com"}, # app 4061, submitted 10 Aug
]

# Sign-off: this family uses "Warmly," (locked with type #5, Ayesha 2026-08-12).
# Content swap only - layout untouched.
FOOTER_WARMLY = FOOTER.replace("Warm regards,", "Warmly,")


def build_body(first_name):
    # 🔒 LOCKED generic template - placeholders only (greeting name / role / timeline).
    return (
        P(f"Hi {first_name},")
        + P("We hope you're doing well.")
        + P(f"Thank you for taking the time to complete and submit your case study for "
            f"the <strong>{POSITION}</strong> position. We know that work takes real time "
            f"and thought alongside everything else you have on, and we are grateful you "
            f"gave it to us.")
        + P(f"We are currently still in the middle of interviews for this role, so we "
            f"wanted to keep you in the loop rather than leave you waiting in silence. We "
            f"expect to share an update with you on the case study debrief interview call by "
            f"<strong>{UPDATE_BY}</strong>.")
        + P("Thank you for your patience and for your continued interest in joining "
            "Taleemabad. We really appreciate the time and effort you have invested in "
            "the process.")
        + FOOTER_WARMLY
    )


def build_message(c, pilot):
    subject = f"[PILOT - {c['full']}] {BASE_SUBJECT}" if pilot else BASE_SUBJECT
    html = wrap(subject_line=BASE_SUBJECT, role=POSITION,
                eyebrow=EYEBROW["case_study_update"], body_html=build_body(c["first"]))
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = SENDER
    if pilot:
        recipients = [PILOT_TO]          # Rule 4: pilots go to Ayesha ONLY, no CC
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
        ctx = (f"PILOT case-study update ({c['full']}, {POSITION}) to Ayesha only"
               if PILOT_MODE
               else f"LIVE case-study update -> {c['full']} ({POSITION})")
        safe_sendmail(server, SENDER, recipients, msg.as_string(), context=ctx)
        print(f"{'PILOT' if PILOT_MODE else 'LIVE'} sent: {subject} -> {recipients[0]}")
    server.quit()
    print(f"DONE - {len(CANDIDATES)} {'pilots to Ayesha' if PILOT_MODE else 'live emails'}.")


if __name__ == "__main__":
    main()
