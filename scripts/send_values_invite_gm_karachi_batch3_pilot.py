#!/usr/bin/env python3
"""
Values Interview Invite — Growth Manager - Karachi, Batch 3 (2026-08-12).
Format: exact reuse of the previous live GM-Karachi values invite (sent 2026-07-26 to Muneeb Arif),
fetched from Gmail — locked invite design FINAL_2026_05_13. One change per locked rule
2026-07-29: the "Sent on behalf of Talent Acquisition Team by Coco" footer line is REMOVED.

PILOT_MODE=True → ONE sample email to Ayesha ONLY (no CC), subject prefixed [PILOT - ].
PILOT_MODE=False → individual live email per candidate, CC per previous live send.
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

PILOT_MODE = False  # Ayesha approved live send 2026-08-12
PILOT_TO = "ayesha.khan@taleemabad.com"
LIVE_CC = ["waqas.tanveer@taleemabad.com", "ayesha.khan@taleemabad.com", "hiring@taleemabad.com", "ali.sipra@taleemabad.com"]

POSITION = "Growth Manager - Karachi"
JD_LINK = "https://drive.google.com/file/d/17LAZRojac420zA_SKpny7MRfPUAFLjgr/view"
IMPACT_LINK = "https://impact-microsite.vercel.app/"
PREP_GUIDE_LINK = "https://docs.google.com/document/d/1TBbBAimVX9PxSR6-rT13bLKf38itNdbp5v6EbWuDtkg/edit?tab=t.0"
BOOKING_LINK = "https://calendar.google.com/calendar/u/0/appointments/schedules/AcZssZ0hJDcEaQ96plihTTdsSbAqFlNOtyzXk1kizSqFZGXDYUhvKaQiu3uCeQvl0byy3_bvvyq-YDuP"

# Shortlisted on job 41 (2026-08-12, Ayesha's verdict on the new-batch screening) with
# no values interview and no prior comms (verified: Markaz comm history + Ayesha's mailbox
# via read-only IMAP, both empty except the application-received notification).
CANDIDATES = [
    {"first": "Khizran", "full": "Khizran Zehra Baloch", "email": "khizranzehra@gmail.com"},   # app 4065
    {"first": "Zubair", "full": "Syed Zubair Ali", "email": "syedzubairi@hotmail.com"},        # app 4113
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
        ul { font-family: Georgia, Cambria, "Times New Roman", serif; margin: 0 0 26px 0; padding-left: 50px; }
        li { font-family: Georgia, Cambria, "Times New Roman", serif; font-size: 17px; line-height: 1.85; color: #111111; }
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
                                            TALENT ACQUISITION &bull; VALUES INTERVIEW
                                        </div>
                                        <h1 style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:24px; line-height:1.2; font-weight:700; color:#3157b7; margin:0 0 10px 0; text-align:center;">
                                            Invitation for the Values Interview
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
                                            Thank you for your interest in the <strong>{position}</strong>
                                            role at Taleemabad. We have reviewed your application and would like to
                                            invite you for a <strong>45-minute values conversation</strong>
                                            with our team, to learn more about you and how your persona aligns with Taleemabad values.
                                        </p>
                                        <p>
                                            The JD for this position is <a href="{jd_link}">available here</a>. You can also explore more about
                                            Taleemabad and our work:
                                        </p>
                                        <ul>
                                            <li><a href="{impact_link}">10 Years Of Impact - Taleemabad</a></li>
                                        </ul>
                                        <p>
                                            Please go through the <a href="{prep_link}">interview prep guide</a> to understand what to expect from
                                            this conversation.
                                        </p>
                                        <p class="callout">
                                            This session will be recorded. By joining, you consent to being part of the recorded call.
                                        </p>
                                        <p>
                                            Let us know if you have any questions ahead of the interview. We look forward to speaking with you.
                                        </p>
                                        <div style="text-align:center; margin:40px 0 28px 0;">
                                            <a href="{booking_link}" style="background:#5b3fc4; color:#ffffff; font-size:16px; font-weight:700; font-family:Georgia,Cambria,'Times New Roman',serif; text-decoration:none; border-radius:7px; padding:14px 34px; display:inline-block; text-align:center;">&#128197; Book your Interview</a>
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
    subject = f"Values Interview for {POSITION} - {candidate['full']}"
    if pilot:
        subject = f"[PILOT - ] {subject}"
    html = (HTML_TEMPLATE
            .replace("{first_name}", candidate["first"])
            .replace("{position}", POSITION)
            .replace("{jd_link}", JD_LINK)
            .replace("{impact_link}", IMPACT_LINK)
            .replace("{prep_link}", PREP_GUIDE_LINK)
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
    if not PILOT_MODE:
        allow_candidate_addresses([c["email"] for c in CANDIDATES])
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    if PILOT_MODE:
        for c in CANDIDATES:
            msg, recipients, subject = build_message(c, pilot=True)
            safe_sendmail(server, SENDER, recipients, msg.as_string(),
                          context=f"PILOT values invite GM-Karachi batch3 ({c['full']}) to Ayesha only")
            print(f"PILOT sent to {recipients}: {subject}")
        print(f"All {len(CANDIDATES)} pilots sent to Ayesha only.")
    else:
        for c in CANDIDATES:
            msg, recipients, subject = build_message(c, pilot=False)
            safe_sendmail(server, SENDER, recipients, msg.as_string(),
                          context=f"LIVE values invite GM-Karachi batch3 -> {c['full']}")
            print(f"LIVE sent: {subject} -> {c['email']}")
    server.quit()
    print("DONE")

if __name__ == "__main__":
    main()
