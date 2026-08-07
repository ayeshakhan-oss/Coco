"""
Job 42 — Senior Manager Growth (JOB-0042)
Values Interview Invitation — 10 shortlisted candidates.

Design: reference implementation scripts/jobs/job32/send_job32_values_invite.py (locked Skill 06 invite design).
Only content changed: position, video JD link, booking link, candidates.

WORKFLOW:
  1. Run with PILOT_MODE = True  --> sends ALL 10 personalized invites to Ayesha ONLY
     (subjects prefixed "[PILOT – ]", no CC — CLAUDE.md Rule 4).
  2. On approval, set PILOT_MODE = False and run again --> sends to the 10 candidates
     (prefix stripped — Rule 7: never "[PILOT – ]" in live emails).
"""

import os
import smtplib
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))


# ── CONFIG ────────────────────────────────────────────────────────────────────
PILOT_MODE  = False  # batch 3 pilots approved by Ayesha 2026-08-07 (standard CC confirmed) --> LIVE

POSITION    = "Senior Manager Growth"
SENDER      = "ayesha.khan@taleemabad.com"
PASSWORD    = os.getenv("EMAIL_PASSWORD")
CC_STANDARD = [
    "ayesha.khan@taleemabad.com",
    "hiring@taleemabad.com",
    "waqas.tanveer@taleemabad.com",  # hiring manager, Job 42 (verified in Markaz users)
    "ali.sipra@taleemabad.com",
]

PILOT_TO = "ayesha.khan@taleemabad.com"

BOOKING_LINK    = "https://calendar.app.google/4coXoLsZNKwJvdAAA"
JD_LINK         = "https://drive.google.com/file/d/1zwWEzeaiud7Y_nMnLjBP-6-ebYHCRrBQ/view?usp=sharing"  # video JD
PREP_GUIDE_LINK = "https://docs.google.com/document/d/1TBbBAimVX9PxSR6-rT13bLKf38itNdbp5v6EbWuDtkg/edit?tab=t.0"

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets")

INLINE_IMAGES = [
    ("logo_taleemabad", "logo_taleemabad.png"),
]

# ── CANDIDATES (10 shortlisted — names/emails verified from Markaz) ───────────
CANDIDATES = [
    {"greet": "Murtaza", "name": "Murtaza Hassan",         "email": "murtaza.hassan0700@gmail.com"},
    {"greet": "Arshan",  "name": "Muhammad Arshan Bilal",  "email": "bilalarshan1@gmail.com"},
    {"greet": "Shakeel", "name": "Muhammad Shakeel Ahmad", "email": "shakeel.rtp@gmail.com"},
    {"greet": "Umar",    "name": "Umar Zahid",             "email": "umarzahid07@gmail.com"},
    {"greet": "Shahmir", "name": "Shahmir Hashmat",        "email": "shahmirhashmat1999@gmail.com"},
    {"greet": "Fahad",   "name": "Fahad Ali",              "email": "fahadalikhoso0@gmail.com"},
    {"greet": "Zeshan",  "name": "Muhammad Zeshan",        "email": "xeshan.nawaz@gmail.com"},
    {"greet": "Salman",  "name": "Salman Ahmad",           "email": "zedef@hotmail.com"},
    {"greet": "Ali",     "name": "Ali Ahmed",              "email": "aliahmed209@gmail.com"},
    {"greet": "Hina",    "name": "Hina Rehman",            "email": "hinarehman1794@gmail.com"},
    # Batch sent live 2026-08-05. Rimsha added after Ayesha reinstated her the same day:
    {"greet": "Rimsha",  "name": "Rimsha Taj",             "email": "rimsha-taj@live.com"},
    # Batch 3 (2026-08-07, per Ayesha in chat) — NOT yet on Markaz; records to be created later:
    {"greet": "Yusra",   "name": "Yusra Wahid",            "email": "yusra.wahid12@gmail.com"},
    {"greet": "Basit",   "name": "Basit Hussain",          "email": "syed.basit89@gmail.com"},
    {"greet": "Imran",   "name": "Imran Mehmood Choudhry", "email": "imranchoudhry@gmail.com"},
    {"greet": "Furqan",  "name": "Furqan Afzal",           "email": "fafzal98@gmail.com"},
    # Late add per Ayesha in chat, 2026-08-07 (approved batch-3 template):
    {"greet": "Irfan",   "name": "Irfan Siddiqui",         "email": "irfanmsiddiqui@outlook.com"},
]

# Send only to candidates in this list (empty = all). Used to add late approvals
# without re-emailing the already-invited batch.
ONLY = ["Irfan Siddiqui"]


# ── EMAIL: BUILD HTML (design identical to job32 reference) ───────────────────
def build_email_html(greet_name, booking_url):

    booking_block = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin:28px 0 8px 0;">
  <tr>
    <td align="center">
      <table cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td bgcolor="#5b3fa6" style="border-radius:6px; padding:13px 32px;">
            <a href="{booking_url}"
               style="color:#ffffff; font-size:15px; font-weight:bold;
                      text-decoration:none; font-family:Georgia,serif;">
              &#128197;&nbsp; Book your Interview
            </a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td align="center"
        style="font-family:Georgia,serif; font-size:13px; color:#888888;
               padding:8px 0 0 0;">
      Please book a slot at your earliest convenience.
    </td>
  </tr>
</table>"""

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background-color:#f0f4f0;">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background-color:#f0f4f0;padding:32px 0;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0"
             style="max-width:620px;border-radius:8px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);">

        <!-- ── Header ── -->
        <tr>
          <td>
            <table width="100%" cellpadding="0" cellspacing="0"
                   style="border-radius:8px 8px 0 0;overflow:hidden;
                          border-bottom:2px solid #1565c0;">
              <tr>
                <td align="center" bgcolor="#ffffff"
                    style="background-color:#ffffff;padding:28px 40px 22px 40px;">
                  <img src="cid:logo_taleemabad" height="38" alt="Taleemabad"
                       style="display:block;margin:0 auto 14px auto;">
                  <p style="margin:0;font-family:Georgia,serif;font-size:11px;
                            color:#1565c0;letter-spacing:2px;text-transform:uppercase;">
                    Talent Acquisition &nbsp;&bull;&nbsp; Values Interview
                  </p>
                  <p style="margin:10px 0 4px 0;font-family:Georgia,serif;font-size:17px;
                            font-weight:bold;color:#1565c0;line-height:1.4;">
                    Invitation for the Values Interview
                  </p>
                  <p style="margin:0;font-family:Georgia,serif;font-size:12px;color:#5c85c7;">
                    {POSITION}
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ── Body ── -->
        <tr>
          <td style="background:#ffffff;padding:40px 52px 48px 52px;
                     border-radius:0 0 8px 8px;
                     font-family:Georgia,serif;font-size:15px;
                     line-height:1.8;color:#1a1a1a;">

            <p style="margin:0 0 18px 0;text-align:justify;">Hi {greet_name},</p>

            <p style="margin:0 0 18px 0;text-align:justify;">
              Thank you for your interest in the <strong>{POSITION}</strong> role at
              Taleemabad. We have reviewed your application and would like to invite you
              for a <strong>45-minute values conversation</strong> with our team, to learn
              more about you and how your persona aligns with the way we work.
            </p>

            <p style="margin:0 0 18px 0;text-align:justify;">
              The video JD for this position is
              <a href="{JD_LINK}" style="color:#1565c0;">available here</a>.
              You can also explore more about Taleemabad and our work:
            </p>

            <ul style="margin:0 0 18px 0;padding-left:22px;line-height:1.8;">
              <li style="margin-bottom:6px;">
                <a href="https://impact-microsite.vercel.app/" style="color:#1565c0;">
                  10 Years Of Impact - Taleemabad
                </a>
              </li>
            </ul>

            <p style="margin:0 0 18px 0;text-align:justify;">
              Please go through the
              <a href="{PREP_GUIDE_LINK}"
                 style="color:#1565c0;">interview prep guide</a>
              to understand what to expect from this conversation.
            </p>

            <p style="margin:0 0 18px 0;font-weight:bold;color:#1565c0;text-align:justify;">
              This session will be recorded. By joining, you consent to being part of
              the recorded call.
            </p>

            <p style="margin:0 0 8px 0;text-align:justify;">
              Let us know if you have any questions ahead of the interview. We look
              forward to speaking with you.
            </p>

            {booking_block}

            <!-- ── Footer ── -->
            <table width="100%" cellpadding="0" cellspacing="0"
                   style="margin-top:40px;border-top:1px solid #e0e0e0;padding-top:20px;">
              <tr>
                <td style="font-family:Georgia,serif;font-size:13px;color:#555;line-height:1.9;">
                  Warm regards,<br>
                  <strong style="color:#1a1a1a;">People and Culture Team</strong><br>
                  <strong style="color:#1565c0;">Taleemabad</strong><br>
                  <a href="mailto:hiring@taleemabad.com"
                     style="color:#1565c0;text-decoration:none;">hiring@taleemabad.com</a>
                  &nbsp;|&nbsp;
                  <a href="http://www.taleemabad.com"
                     style="color:#1565c0;text-decoration:none;">www.taleemabad.com</a><br>
                </td>
              </tr>
            </table>

          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""
    return html


# ── EMAIL: SEND ───────────────────────────────────────────────────────────────
def send_invite(to_email, full_name, greet_name, pilot, cc_list=None):
    subject = f"Invitation for the Values Interview for {POSITION} - {full_name}"
    if pilot:
        subject = "[PILOT – ] " + subject

    msg            = MIMEMultipart("related")
    msg["From"]    = SENDER
    msg["To"]      = to_email
    msg["Subject"] = subject
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(build_email_html(greet_name, BOOKING_LINK), "html"))
    msg.attach(alt)

    for cid, fname in INLINE_IMAGES:
        fpath = os.path.join(ASSETS_DIR, fname)
        with open(fpath, "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", f"<{cid}>")
        img.add_header("Content-Disposition", "inline", filename=fname)
        msg.attach(img)

    recipients = [to_email] + (cc_list or [])
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(SENDER, PASSWORD)
        if not pilot:
            allow_candidate_addresses(recipients)
        safe_sendmail(smtp, SENDER, recipients, msg.as_string(),
                      context=f"job42_values_invite_{'PILOT_' if pilot else ''}{full_name}")

    print(f"  Sent: {subject} -> {to_email}" + (f" (CC: {', '.join(cc_list)})" if cc_list else ""))


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Job 42 - Senior Manager Growth")
    print("Values Interview Invitations (10 shortlisted)")
    print(f"Mode: {'PILOT (all 10 to Ayesha only)' if PILOT_MODE else 'LIVE (candidates + CC)'}")
    print("=" * 60)

    todo = [c for c in CANDIDATES if not ONLY or c["name"] in ONLY]
    print(f"Sending to {len(todo)} candidate(s): {', '.join(c['name'] for c in todo)}")
    sent, failed = 0, []
    for c in todo:
        try:
            if PILOT_MODE:
                send_invite(PILOT_TO, c["name"], c["greet"], pilot=True, cc_list=None)
            else:
                send_invite(c["email"], c["name"], c["greet"], pilot=False, cc_list=CC_STANDARD)
            sent += 1
        except Exception as e:
            print(f"  FAILED for {c['name']}: {e}")
            failed.append(c["name"])

    print(f"\nDone. {sent}/{len(CANDIDATES)} sent.")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    if PILOT_MODE:
        print("Review in Ayesha's inbox. On approval set PILOT_MODE = False and rerun.")
    print("=" * 60)


if __name__ == "__main__":
    main()
