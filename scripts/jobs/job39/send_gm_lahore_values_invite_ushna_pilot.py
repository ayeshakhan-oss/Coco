#!/usr/bin/env python3
"""
Values Interview Invite — Growth Manager - Lahore (JOB-0039) — Ushna Fawad.

Design is LOCKED: HTML lifted unchanged from
scripts/send_growth_manager_values_invite_pilot.py (the 8 Jul 2026 GM-Lahore
batch that went live). ONLY the candidate and the position label differ.

Links verified live 2026-08-24 by fetching each URL and reading its <title>:
  JD      -> "Growth Manager Lahore - Google Drive"
  PREP    -> "Interview Prep Guide - Google Docs"
  BOOKING -> "Zero in Call for Growth Manager Lahore"   <- Lahore schedule, not Karachi

Candidate verified in Markaz (Neon HTTPS SQL API, MCP was down):
  candidate 3349 · application 4141 · job 39 "Growth Manager - Lahore"
  applied 2026-08-13 · status 'new' · Lahore-based (DHA Phase 8)

PILOT (default): ayesha.khan@taleemabad.com ONLY, no CC, [PILOT - ] subject.
LIVE  (--live) : TO Ushna, CC the list the 8 Jul GM-Lahore batch used.
"""

import os
import sys
import smtplib
import argparse

sys.path.insert(0, "c:/Agent Coco")

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
POSITION = "Growth Manager - Lahore"

JD_LINK         = "https://drive.google.com/file/d/1ui-Y_jTr9xEkTHM3KH85q0ZvA16VreJJ/view?usp=sharing"
PREP_GUIDE_LINK = "https://docs.google.com/document/d/1TBbBAimVX9PxSR6-rT13bLKf38itNdbp5v6EbWuDtkg/edit?tab=t.0"
BOOKING_LINK    = "https://calendar.app.google/WMdp99dVmqPuuMvp9"
IMPACT_LINK     = "https://impact-microsite.vercel.app/"

CANDIDATE = {
    "first": "Ushna",
    "full":  "Ushna Fawad",
    "email": "ushna.fawad@gmail.com",   # Markaz candidate 3349
}

SENDER   = "ayesha.khan@taleemabad.com"
PILOT_TO = "ayesha.khan@taleemabad.com"
# Same CC list the 8 Jul 2026 GM-Lahore values invites carried.
LIVE_CC  = ["ayesha.khan@taleemabad.com", "hiring@taleemabad.com",
            "waqas.tanveer@taleemabad.com"]

LOGO_PATH = "c:/Agent Coco/assets/logo_taleemabad.png"


# ---------------------------------------------------------------------------
# HTML body (LOCKED design — do not alter structure, colours, fonts, spacing)
# ---------------------------------------------------------------------------
def build_html(first_name):
    return f"""
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #f5f5f5;
            font-family: Georgia, Cambria, "Times New Roman", serif;
        }}
        a {{
            color: #3d63c8;
            text-decoration: underline;
        }}
        p {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 17px;
            line-height: 1.85;
            color: #111111;
            font-weight: 400;
            margin: 0 0 26px 0;
        }}
        strong {{
            font-weight: 700;
        }}
        ul {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            margin: 0 0 26px 0;
            padding-left: 50px;
        }}
        li {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 17px;
            line-height: 1.85;
            color: #111111;
        }}
        .callout {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 17px;
            line-height: 1.85;
            font-weight: 700;
            color: #3d63c8;
            margin: 26px 0 26px 0;
        }}
        .button-subtitle {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 16px;
            line-height: 1.6;
            color: #111111;
            text-align: center;
            margin: 18px 0 0 0;
        }}
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
                                <!-- Header -->
                                <tr>
                                    <td style="padding:34px 64px 30px 64px; text-align:center;">
                                        <!-- Logo -->
                                        <div style="margin-bottom:16px;">
                                            <img src="cid:taleemabad_logo" alt="Taleemabad" width="34" height="34" style="width:34px; height:auto;">
                                        </div>

                                        <!-- Top Label -->
                                        <div style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:12px; letter-spacing:2.4px; font-weight:500; text-transform:uppercase; color:#3157b7; line-height:1.4; margin:0 0 18px 0;">
                                            TALENT ACQUISITION &bull; VALUES INTERVIEW
                                        </div>

                                        <!-- Main Heading -->
                                        <h1 style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:24px; line-height:1.2; font-weight:700; color:#3157b7; margin:0 0 10px 0; text-align:center;">
                                            Invitation for the Values Interview
                                        </h1>

                                        <!-- Subtitle -->
                                        <p style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:13px; line-height:1.5; color:#5d73b8; text-align:center; margin:0; font-weight:400;">
                                            {POSITION}
                                        </p>
                                    </td>
                                </tr>

                                <!-- Divider -->
                                <tr>
                                    <td style="border-top:2px solid #4b67d1; height:0; padding:0; margin:0;"></td>
                                </tr>

                                <!-- Body Content -->
                                <tr>
                                    <td style="padding:44px 64px 52px 64px; text-align:left;">
                                        <p style="margin-bottom:30px;">Hi {first_name},</p>

                                        <p>
                                            Thank you for your interest in the <strong>{POSITION}</strong>
                                            role at Taleemabad. We have reviewed your application and would like to
                                            invite you for a <strong>45-minute values conversation</strong>
                                            with our team, to learn more about you and how your persona aligns with the way we work.
                                        </p>

                                        <p>
                                            A short video walkthrough of the <strong>{POSITION}</strong> JD is
                                            <a href="{JD_LINK}">available here</a>. You can also explore more about
                                            Taleemabad and our work:
                                        </p>

                                        <ul>
                                            <li><a href="{IMPACT_LINK}">10 Years Of Impact - Taleemabad</a></li>
                                        </ul>

                                        <p>
                                            Please go through the <a href="{PREP_GUIDE_LINK}">interview prep guide</a> to understand what to expect from
                                            this conversation.
                                        </p>

                                        <p class="callout">
                                            This session will be recorded. By joining, you consent to being part of the recorded call.
                                        </p>

                                        <p>
                                            Let us know if you have any questions ahead of the interview. We look forward to speaking with you.
                                        </p>

                                        <!-- CTA Button -->
                                        <div style="text-align:center; margin:40px 0 28px 0;">
                                            <a href="{BOOKING_LINK}" style="background:#5b3fc4; color:#ffffff; font-size:16px; font-weight:700; font-family:Georgia,Cambria,'Times New Roman',serif; text-decoration:none; border-radius:7px; padding:14px 34px; display:inline-block; text-align:center;">&#128197; Book your Interview</a>
                                        </div>

                                        <p class="button-subtitle">Please book a slot at your earliest convenience.</p>
                                    </td>
                                </tr>

                                <!-- Signature -->
                                <tr>
                                    <td style="padding:0 64px 52px 64px; text-align:left; font-family:Georgia,Cambria,'Times New Roman',serif;">
                                        <!-- Divider -->
                                        <div style="border-top:1px solid #d9d9d9; margin-top:22px; margin-bottom:28px;"></div>

                                        <!-- Signature Content -->
                                        <p style="font-size:16px; color:#5c5c5c; line-height:1.7; margin:0 0 10px 0; font-weight:400;">Warm regards,</p>

                                        <p style="font-size:18px; font-weight:700; color:#111111; line-height:1.6; margin:0 0 6px 0;">People and Culture Team</p>

                                        <p style="font-size:18px; font-weight:700; color:#2f5fc7; line-height:1.6; margin:0 0 10px 0;">Taleemabad</p>

                                        <p style="font-size:16px; line-height:1.7; color:#2f5fc7; margin:0 0 18px 0;">
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


def send_one(server, to_list, cc_list, subject, pilot):
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = ", ".join(to_list)
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    alt = MIMEMultipart("alternative")
    msg.attach(alt)
    alt.attach(MIMEText(build_html(CANDIDATE["first"]), "html", "utf-8"))

    # CID-embedded logo (34px, centered) — required by the locked design.
    with open(LOGO_PATH, "rb") as f:
        img = MIMEImage(f.read(), "png")
    img.add_header("Content-ID", "<taleemabad_logo>")
    img.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
    msg.attach(img)

    recipients = to_list + cc_list
    allow_candidate_addresses(recipients)
    safe_sendmail(
        server, SENDER, recipients, msg.as_string(),
        context="gm_lahore_values_invite_ushna_" + ("pilot" if pilot else "live"),
    )
    return recipients


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="send to the candidate")
    args = ap.parse_args()
    pilot = not args.live

    load_dotenv(r"c:\Agent Coco\.env")

    if pilot:
        subject = (f"[PILOT - ] Invitation for the Values Interview for "
                   f"{POSITION} - {CANDIDATE['full']}")
        to_list, cc_list = [PILOT_TO], []
    else:
        subject = (f"Invitation for the Values Interview for "
                   f"{POSITION} - {CANDIDATE['full']}")
        to_list, cc_list = [CANDIDATE["email"]], LIVE_CC

    print(f"Mode: {'PILOT (Ayesha only)' if pilot else 'LIVE'}")
    print(f"Subject: {subject}")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, os.getenv("EMAIL_PASSWORD"))
    rec = send_one(server, to_list, cc_list, subject, pilot)
    server.quit()

    print(f"Sent to: {', '.join(rec)}")


if __name__ == "__main__":
    main()
