#!/usr/bin/env python3
"""
Case Study Debrief Invites - Regional Manager (INTERNAL round), 2026-09-07.
Skill 06 type #2. Locked invite design (FINAL_2026_05_13). Body copy cloned VERBATIM from
the SMG batch-2 live send (2026-08-31) with ONE substitution: that batch linked a video
walkthrough of the role, this one links the RM job description, because that is the
artefact that exists for this role.

Ayesha's brief 2026-09-07: invite the 17 who scored at or above the published 70% bar on
the strict re-mark of the internal case study round. Booking link supplied by her in chat.

VERIFIED before drafting:
  - The 17 are every candidate at or above 70 on the strict re-mark (strict_scores.json,
    all 25 scored). Below the line and NOT invited: Muhammad Salman 65, Javeria Nayyab 64,
    Toseef ur Rehman 63, Sana Nawaz 63, Hafsa Bashir 62, Areej Noshad 60, Khadija Akbar 59,
    Rida Abbas 56.
  - Emails pulled from the submission roster and confirmed against the From address on each
    person's own submission email. All 17 present, all @niete.edu.pk.
  - NO debrief invite has ever been sent to any of the 17 (per-recipient IMAP scan of
    ayesha.khan@ Sent Mail since 01-Aug-2026, run 2026-09-07): zero sent items to any of
    them, debrief-related or otherwise.
  - NAME EVIDENCE checked against each person's own From display name (CLAUDE.md Rule 22).
    16 of 17 match the held name exactly. One conflict:
      * We hold "Syed Ateeb Ali"; he signs himself "Ateeb Ali" on all 10 of his own emails.
        Syed is a patronymic rather than part of the name he uses, so the GREETING is
        "Hi Ateeb," while the subject line keeps the full formal name.
        >>> FLAGGED TO AYESHA - confirm before live. <<<
  - BOOKING_LINK supplied directly by Ayesha 2026-09-07 in chat. NOT reused from the SMG
    batches (batch 1 was we2Xc2uoYA1x3c1s9, batch 2 VXJ1qxddrMVakeFAA) - CLAUDE.md Rule 22
    requires a fresh link per batch or these 17 land in the wrong calendar.
  - JD_LINK is the same Google Doc sent to all staff in the internal announcement on
    2026-08-20 (scripts/send_internal_announcement_pilot.py), so "revisit" is accurate -
    they have all seen it.

DELIBERATELY NOT STATED (Ayesha has not supplied these; nothing is invented):
  - No duration. No panel names. No booking deadline. The locked copy says "at your
    earliest convenience", which needs none of them.

TONE NOTE: this batch spans scores of 100 down to exactly 70. Every email is byte-identical
except the first name and the subject, so nothing in it hints at a ranking.

PILOT_MODE=True -> all 17 emails to Ayesha ONLY, [PILOT - ] prefix, NO CC (CLAUDE.md Rule 4).
"""
import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

sys.path.insert(0, r"c:\Agent Coco")
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(r"c:\Agent Coco\.env")

SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")
LOGO_PATH = r"c:\Agent Coco\assets\logo_taleemabad.png"

PILOT_MODE = False  # LIVE - Ayesha approved 2026-09-07 ("go llive")
PILOT_TO = "ayesha.khan@taleemabad.com"
# CC list given verbatim by Ayesha 2026-09-07 for THIS internal round. Note it is NOT the
# SMG debrief list - Waqas is out, and Asma and Bilal (NIETE) are in. Bare names resolved
# only where the address is already established in confirmed prior use; the two niete.edu.pk
# addresses were supplied by her in full, not inferred (CLAUDE.md Rule 20 - never resolve a
# bare first name from the repo).
LIVE_CC = ["ali.sipra@taleemabad.com",
           "asma.zaheer@niete.edu.pk",
           "bilal@niete.edu.pk",
           "hiring@taleemabad.com",
           "ayesha.khan@taleemabad.com"]

POSITION = "Regional Manager"
BOOKING_LINK = "https://calendar.app.google/w8WJ3GEmVNYUQztL8"  # supplied by Ayesha 2026-09-07
JD_LINK = ("https://docs.google.com/document/d/"
           "1Jdj6RIxt64hnKh9duXVdLCasy5BlTTxJOBe4pY1vy7A/edit?usp=sharing")

# Score in the comment is for the audit trail only - it never appears in the email.
CANDIDATES = [
    {"first": "Ateeb",     "full": "Syed Ateeb Ali",  "email": "ateeb.ali@niete.edu.pk"},        # 100 RM-17
    {"first": "Danish",    "full": "Danish Iqbal",    "email": "danish.iqbal@niete.edu.pk"},     # 100 RM-09
    {"first": "Moiz",      "full": "Moiz Khan",       "email": "moiz.khan@niete.edu.pk"},        #  95 RM-24
    {"first": "Warda",     "full": "Warda Kiani",     "email": "warda.kiani@niete.edu.pk"},      #  92 RM-13
    {"first": "Meerab",    "full": "Meerab Din",      "email": "meerab.din@niete.edu.pk"},       #  89 RM-15
    {"first": "Mubasher",  "full": "Mubasher Irfan",  "email": "mubasher.irfan@niete.edu.pk"},   #  85 RM-22
    {"first": "Eysha",     "full": "Eysha Qadeer",    "email": "eysha.qadeer@niete.edu.pk"},     #  83 RM-02
    {"first": "Bushra",    "full": "Bushra Karim",    "email": "bushra.karim@niete.edu.pk"},     #  81 RM-08
    {"first": "Imran",     "full": "Muhammad Imran",  "email": "imran@niete.edu.pk"},            #  80 RM-03
    {"first": "Ashas",     "full": "Ashas Khan",      "email": "ashas.khan@niete.edu.pk"},       #  75 RM-23
    {"first": "Fakhr",     "full": "Fakhr Ul Islam",  "email": "fakhr.islam@niete.edu.pk"},      #  75 RM-06
    {"first": "Shafaq",    "full": "Shafaq Tahir",    "email": "shafaq.tahir@niete.edu.pk"},     #  74 RM-04
    {"first": "Maroof",    "full": "Maroof Anwar",    "email": "maroof.anwar@niete.edu.pk"},     #  72 RM-10
    {"first": "Saman",     "full": "Saman Zahoor",    "email": "saman.zahoor@niete.edu.pk"},     #  72 RM-05
    {"first": "Misbah",    "full": "Misbah Iqbal",    "email": "misbah.iqbal@niete.edu.pk"},     #  70 RM-25
    {"first": "Saba",      "full": "Saba Kokab",      "email": "saba.kokab@niete.edu.pk"},       #  70 RM-19
    {"first": "Waleed",    "full": "Waleed Abdullah", "email": "waleed.abdullah@niete.edu.pk"},  #  70 RM-16
]

HTML_TEMPLATE = """
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; padding: 0; background: #f5f5f5; font-family: Georgia, Cambria, "Times New Roman", serif; }
        a { color: #3d63c8; text-decoration: underline; }
        p { font-family: Georgia, Cambria, "Times New Roman", serif; font-size: 17px; line-height: 1.85; color: #111111; font-weight: 400; margin: 0 0 26px 0; }
        strong { font-weight: 700; }
        .callout { font-family: Georgia, Cambria, "Times New Roman", serif; font-size: 17px; line-height: 1.85; font-weight: 700; color: #3d63c8; margin: 26px 0 26px 0; }
        .button-subtitle { font-family: Georgia, Cambria, "Times New Roman", serif; font-size: 16px; line-height: 1.6; color: #111111; text-align: center; margin: 18px 0 0 0; }
    </style>
</head>
<body>
    <table width="100%" bgcolor="#f5f5f5" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center">
                <table width="calc(100% - 90px)" bgcolor="#e5e7e2" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
                    <tr>
                        <td align="center" style="padding-top:38px; padding-bottom:38px;">
                            <table width="775" bgcolor="#ffffff" cellpadding="0" cellspacing="0" border="0" style="width:775px; max-width:775px; margin:0 auto;">
                                <tr>
                                    <td style="padding:34px 64px 30px 64px; text-align:center;">
                                        <div style="margin-bottom:16px;">
                                            <img src="cid:taleemabad_logo" alt="Taleemabad" width="34" height="34" style="width:34px; height:auto;">
                                        </div>
                                        <div style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:12px; letter-spacing:2.4px; font-weight:500; text-transform:uppercase; color:#3157b7; line-height:1.4; margin:0 0 18px 0;">
                                            TALENT ACQUISITION &bull; CASE STUDY DEBRIEF
                                        </div>
                                        <h1 style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:24px; line-height:1.2; font-weight:700; color:#3157b7; margin:0 0 10px 0; text-align:center;">
                                            Invitation for the Case Study Debrief
                                        </h1>
                                        <p style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:13px; line-height:1.5; color:#5d73b8; text-align:center; margin:0; font-weight:400;">
                                            {position}
                                        </p>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="border-top:2px solid #4b67d1; height:0; padding:0; margin:0;"></td>
                                </tr>
                                <tr>
                                    <td style="padding:44px 64px 52px 64px; text-align:left;">
                                        <p style="margin-bottom:30px;">Hi {first_name},</p>
                                        <p>
                                            Thank you for completing and submitting the case study for the
                                            <strong>{position}</strong> role. We appreciate the time and thought
                                            you put into it.
                                        </p>
                                        <p>
                                            As the next step, we would like to invite you to a
                                            <strong>case study debrief conversation</strong> with our team. In this
                                            session, we will walk through your submission together - your approach,
                                            your thinking, and the choices you made - and you'll also get a chance
                                            to hear our questions and share anything you'd add.
                                        </p>
                                        <p>
                                            To help you prepare, you may find it useful to revisit the
                                            <a href="{jd_link}">role description</a> before we speak.
                                        </p>
                                        <p class="callout">
                                            This session will be recorded. By joining, you consent to being part of the recorded call.
                                        </p>
                                        <p>
                                            Please book a slot using the button below. If none of the available times
                                            work for you, simply reply to this email and we will figure something out together.
                                        </p>
                                        <div style="text-align:center; margin:40px 0 28px 0;">
                                            <a href="{booking_link}" style="background:#5b3fc4; color:#ffffff; font-size:16px; font-weight:700; font-family:Georgia,Cambria,'Times New Roman',serif; text-decoration:none; border-radius:7px; padding:14px 34px; display:inline-block; text-align:center;">&#128197; Schedule Your Debrief</a>
                                        </div>
                                        <p class="button-subtitle">Please book a slot at your earliest convenience.</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:0 64px 52px 64px; text-align:left; font-family:Georgia,Cambria,'Times New Roman',serif;">
                                        <div style="border-top:1px solid #d9d9d9; margin-top:22px; margin-bottom:28px;"></div>
                                        <p style="font-size:16px; color:#5c5c5c; line-height:1.7; margin:0 0 10px 0; font-weight:400;">Warm regards,</p>
                                        <p style="font-size:18px; font-weight:700; color:#111111; line-height:1.6; margin:0 0 6px 0;">People and Culture Team</p>
                                        <p style="font-size:18px; font-weight:700; color:#2f5fc7; line-height:1.6; margin:0 0 10px 0;">Taleemabad</p>
                                        <p style="font-size:16px; line-height:1.7; color:#2f5fc7; margin:0;">
                                            <a href="mailto:hiring@taleemabad.com" style="color:#2f5fc7; text-decoration:underline;">hiring@taleemabad.com</a> <span style="color:#7d7d7d; margin:0 10px;">|</span> <a href="https://www.taleemabad.com" style="color:#2f5fc7; text-decoration:underline;">www.taleemabad.com</a>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""


def build_message(candidate, pilot):
    subject = f"Case Study Debrief Invitation for {POSITION} - {candidate['full']}"
    if pilot:
        subject = f"[PILOT - ] {subject}"
    html = (HTML_TEMPLATE
            .replace("{first_name}", candidate["first"])
            .replace("{position}", POSITION)
            .replace("{booking_link}", BOOKING_LINK)
            .replace("{jd_link}", JD_LINK))
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = SENDER
    if pilot:
        recipients = [PILOT_TO]
        msg["To"] = PILOT_TO
    else:
        recipients = [candidate["email"]] + LIVE_CC
        msg["To"] = candidate["email"]
        msg["Cc"] = ", ".join(LIVE_CC)
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html, "html"))
    msg.attach(alt)
    with open(LOGO_PATH, "rb") as f:
        img = MIMEImage(f.read(), "png")
    img.add_header("Content-ID", "<taleemabad_logo>")
    img.add_header("Content-Disposition", "inline")
    msg.attach(img)
    return msg, recipients, subject


def main():
    if not BOOKING_LINK.startswith("https://calendar.app.google/"):
        sys.exit("BLOCKED: BOOKING_LINK is not a real Google Calendar booking link. "
                 "Never fabricate or reuse a link across batches.")
    if not JD_LINK.startswith("https://docs.google.com/"):
        sys.exit("BLOCKED: JD_LINK is not set.")
    if PILOT_MODE and "[PILOT" not in build_message(CANDIDATES[0], True)[2]:
        sys.exit("BLOCKED: pilot prefix missing.")
    if not PILOT_MODE:
        allow_candidate_addresses([c["email"] for c in CANDIDATES])
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    for c in CANDIDATES:
        msg, recipients, subject = build_message(c, pilot=PILOT_MODE)
        mode = "PILOT" if PILOT_MODE else "LIVE"
        safe_sendmail(server, SENDER, recipients, msg.as_string(),
                      context=f"{mode} case study debrief invite RM internal -> {c['full']}")
        print(f"{mode} sent: {subject} -> {recipients}")
    server.quit()
    print(f"DONE - {len(CANDIDATES)} {'pilot' if PILOT_MODE else 'live'} emails")


if __name__ == "__main__":
    main()
