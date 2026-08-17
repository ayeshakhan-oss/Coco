#!/usr/bin/env python3
"""
Case Study Debrief Invites — Growth Manager - Karachi, batch of 3 (2026-08-17).
Skill 06 type #2. Locked invite design (FINAL_2026_05_13). Cloned verbatim from the
approved Waqas Hassan send of 2026-08-07 — only the candidate list changed.

Ayesha's brief 2026-08-17: send debrief invites to Muneeb, Marzia/Merzia and Huda.

VERIFIED before drafting:
  - All three submitted their case study (Markaz applications 3869 / 3819 / 3803).
  - No debrief invite has ever been sent to any of them (IMAP scan of Ayesha's mailbox,
    01-Aug onward: only Waqas Hassan has a GM-Karachi debrief invite).
  - Huda and Marzia each have a *Zero In Call* booking in the calendar (10 Aug / 13 Aug)
    — that is NOT a debrief. Muneeb has no booking of any kind.
  - BOOKING_LINK is the same appointment schedule used for the 7 Aug GM debriefs,
    extracted from the live Waqas Hassan email — not fabricated.
  - Markaz spells her "Marzia Hasnain"; her own email signs "Merzia". Greeting uses
    "Marzia" per Markaz; flag at pilot review if she prefers Merzia.

PILOT_MODE=True -> every email to Ayesha ONLY with [PILOT - ] prefix.
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

PILOT_MODE = False
PILOT_TO = "ayesha.khan@taleemabad.com"
LIVE_CC = ["waqas.tanveer@taleemabad.com", "ayesha.khan@taleemabad.com", "hiring@taleemabad.com", "ali.sipra@taleemabad.com", "zeest.qureshi@taleemabad.com"]

POSITION = "Growth Manager - Karachi"
BOOKING_LINK = "https://calendar.app.google/SzQgacaWQqnLEQ449"  # same GM-debrief schedule Ayesha provided 2026-08-07 — confirm at pilot review

CANDIDATES = [
    {"first": "Muneeb", "full": "Muneeb Arif", "email": "muneebarifkhalid@gmail.com"},
    {"first": "Marzia", "full": "Marzia Hasnain", "email": "merzia.hasnain99@gmail.com"},
    {"first": "Huda", "full": "Huda Shaikh", "email": "hudashaikh8080@gmail.com"},
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
            .replace("{booking_link}", BOOKING_LINK))
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
    if "PASTE_AYESHA_CALENDAR_LINK" in BOOKING_LINK or not BOOKING_LINK.startswith("https://"):
        sys.exit("BLOCKED: BOOKING_LINK is not set. Paste Ayesha's real Google Calendar link before sending. Never fabricate links.")
    if not PILOT_MODE:
        allow_candidate_addresses([c["email"] for c in CANDIDATES])
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    for c in CANDIDATES:
        msg, recipients, subject = build_message(c, pilot=PILOT_MODE)
        mode = "PILOT" if PILOT_MODE else "LIVE"
        safe_sendmail(server, SENDER, recipients, msg.as_string(),
                      context=f"{mode} case study debrief invite GM-Karachi -> {c['full']}")
        print(f"{mode} sent: {subject} -> {recipients}")
    server.quit()
    print("DONE")

if __name__ == "__main__":
    main()
