#!/usr/bin/env python3
"""
Internal Announcement Email (Skill 01 type #7, added 2026-08-20 at Ayesha's request)
====================================================================================
Broadcast to TALEEMABAD STAFF. This is NOT candidate communication: the audience is
internal colleagues, so the candidate rules (800-word minimum, "This is not a yes for
now.", the no-names ban, the jargon ban, the feedback widget) do not apply.

Skill file: .claude/skills/01_candidate-communication/internal-announcement-email.md
Layout:     v8 (Rule 8) imported from scripts/utils/v8_template.py - never inline.

Still enforced: no em dashes, collective voice, safe_sendmail(), pilot to Ayesha first,
clean subject on live sends, no fabricated facts.

DO NOT rename this file to contain warm_bench / gwc / values / rejection - the send-time
hook infers the email type from the filename and would validate this notice as an
800-word candidate feedback letter and HARD BLOCK it.

First use: Regional Manager (RM) internal opening. Body copy written by Ayesha
2026-08-20 and used verbatim except for one em dash, which the no-em-dash rule
converts to a period.

PILOT_MODE=True  -> one pilot to Ayesha ONLY (no CC), [PILOT - ] subject.
PILOT_MODE=False -> live send to RECIPIENTS, clean subject.
"""
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

sys.path.insert(0, r"c:\Agent Coco")
from scripts.utils.safe_send import safe_sendmail
from scripts.utils.v8_template import P, PL, UL, FOOTER, wrap, attach_logo, EYEBROW, BLUE

load_dotenv(r"c:\Agent Coco\.env")
SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")

PILOT_MODE = False        # Ayesha approved live send 2026-08-20 ("looks good. we can go live")

PILOT_TO = "ayesha.khan@taleemabad.com"

# Live recipients supplied by Ayesha 2026-08-20. Never guess a distribution list:
# "bilal" was ambiguous in her message and she confirmed bilal@niete.edu.pk explicitly.
RECIPIENTS = ["all@niete.edu.pk"]
LIVE_CC = [
    "ali.sipra@taleemabad.com",
    "hiring@taleemabad.com",
    "ayesha.khan@taleemabad.com",
    "bilal@niete.edu.pk",
    "asma.zaheer@niete.edu.pk",
]

ROLE = "Regional Manager (RM)"
SUBJECT = "An Internal Opportunity: Regional Manager"
# Single deadline for resume + completed case study. Ayesha 2026-08-20: the case study
# now ships WITH the announcement (self-assess), so the old two-stage flow (resume first,
# case study after screening, 5 working days) collapses into one date. Thursday 27th is
# exactly 5 working days from tomorrow: Fri 21, Mon 24, Tue 25, Wed 26, Thu 27.
DEADLINE = "Thursday, 27th August at 1:00 PM"
JD_URL = ("https://docs.google.com/document/d/"
          "1Jdj6RIxt64hnKh9duXVdLCasy5BlTTxJOBe4pY1vy7A/edit?usp=sharing")
CASE_STUDY_URL = ("https://docs.google.com/document/d/"
                  "15YVgih8s6gItnO0fFSD2C3OBADpCQLmF3rfwvJWHWBQ/edit?usp=sharing")


def buttons():
    """Two centered links, JD and case study. v8 blue; no new palette. Stacks on
    narrow screens because each cell is its own row on mobile widths."""
    def btn(url, label, solid=True):
        if solid:
            style = (f"display:inline-block;padding:12px 26px;background:{BLUE};"
                     "color:#ffffff;border:1px solid " + BLUE + ";")
        else:
            style = (f"display:inline-block;padding:12px 26px;background:#ffffff;"
                     f"color:{BLUE};border:1px solid {BLUE};")
        return (f'<a href="{url}" style="{style}font-family:Georgia,serif;font-size:14px;'
                'text-decoration:none;border-radius:6px;margin:5px 6px;">' + label + '</a>')
    return (
        '<table width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 26px 0;">'
        '<tr><td align="center">'
        + btn(JD_URL, "Read the Job Description", solid=True)
        + btn(CASE_STUDY_URL, "Open the Case Study", solid=False)
        + '</td></tr></table>'
    )


def build_body():
    # Copy by Ayesha, 2026-08-20. Verbatim except: the em dash in "Don't count yourself
    # out - take the shot!" is converted to a period per the no-em-dash rule.
    return (
        PL("Hi everyone,")
        + P("We&rsquo;ve got an exciting opportunity opening up, and we&rsquo;re bringing "
            "it to our own people first. We&rsquo;re looking for our next "
            f"<strong>{ROLE}</strong>, and if you&rsquo;ve been thinking about taking on a "
            "new challenge, stepping into a bigger role, or simply testing yourself, this "
            "might just be your sign to go for it.")
        + PL("<strong>Here&rsquo;s what you need to know:</strong>")
        + UL([
            "<strong>Role:</strong> Regional Manager (RM)",
            "<strong>Minimum Experience:</strong> 2 years",
            "<strong>Employment Type:</strong> Contractual",
            "<strong>Contract Until:</strong> 31st December 2026",
        ])
        + buttons()
        + PL("<strong>Who can apply?</strong>")
        + PL("You&rsquo;re eligible to throw your hat in the ring if you:")
        + UL([
            "Have completed at least 90 days with the organization",
            "Are not currently on probation",
            "Have at least 2 years of experience in Relationship Management",
        ])
        + PL("<strong>Interested? Here&rsquo;s what happens next:</strong>")
        + P("Check yourself against the criteria above, and if you meet them, go straight "
            "ahead. The case study is linked here as well, so there is no waiting on us to "
            "send it to you.")
        + P(f"Reply to this email with your <strong>updated resume</strong> and your "
            f"<strong>completed case study</strong> by <strong>{DEADLINE}</strong>. "
            "Submissions that meet the 70% benchmark will move forward in the process.")
        + P("Know this role is for you? Go for it. Not completely sure but think you could "
            "be a fit? Don&rsquo;t count yourself out. Take the shot.")
        + PL("We&rsquo;re excited to see who steps up for the challenge.")
        + FOOTER
    )


def build_message(pilot):
    subject = f"[PILOT - ] {SUBJECT}" if pilot else SUBJECT
    html = wrap(subject_line=SUBJECT, role=ROLE,
                eyebrow=EYEBROW["announcement"], body_html=build_body())
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = SENDER
    if pilot:
        recipients = [PILOT_TO]           # Rule 4: pilots go to Ayesha ONLY, no CC
        msg["To"] = PILOT_TO
    else:
        recipients = list(RECIPIENTS) + LIVE_CC
        msg["To"] = ", ".join(RECIPIENTS)
        msg["Cc"] = ", ".join(LIVE_CC)
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html, "html"))
    msg.attach(alt)
    attach_logo(msg)
    return msg, recipients, subject


def main():
    if not PILOT_MODE and not RECIPIENTS:
        raise SystemExit("RECIPIENTS is empty. Ayesha must supply the staff list before "
                         "a live send. Refusing to guess a distribution list.")
    msg, recipients, subject = build_message(pilot=PILOT_MODE)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    ctx = (f"PILOT internal announcement ({ROLE}) to Ayesha only" if PILOT_MODE
           else f"LIVE internal announcement ({ROLE}) -> {len(recipients)} staff")
    safe_sendmail(server, SENDER, recipients, msg.as_string(), context=ctx)
    server.quit()
    print(f"{'PILOT' if PILOT_MODE else 'LIVE'} sent: {subject} -> {recipients}")


if __name__ == "__main__":
    main()
