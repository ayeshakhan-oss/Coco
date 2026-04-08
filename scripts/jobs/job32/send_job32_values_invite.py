"""
Job 32 — Fundraising & Partnerships Manager
Values Interview (Zero In) Invitation — 6 shortlisted candidates.

WORKFLOW:
  1. Run with PILOT_MODE = True  --> sends to Ayesha + Jawwad only for review.
  2. On approval, set PILOT_MODE = False and run again --> sends to all 6 candidates.
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
PILOT_MODE  = False  # True = Ayesha + Jawwad only; False = all 6 candidates

POSITION    = "Fundraising & Partnerships Manager"
SENDER      = "ayesha.khan@taleemabad.com"
PASSWORD    = os.getenv("EMAIL_PASSWORD")
HIRING_MGR  = "sabeena.abbasi@taleemabad.com"
CC_STANDARD = [
    "hiring@taleemabad.com",
    HIRING_MGR,
    "jawwad.ali@taleemabad.com",
    "ayesha.khan@taleemabad.com",
]

PILOT_RECIPIENTS = [
    {"email": "ayesha.khan@taleemabad.com", "name": "Ayesha"},
    {"email": "jawwad.ali@taleemabad.com",  "name": "Jawwad"},
]

BOOKING_LINK = "https://calendar.app.google/wJSR5Gx4GQv2QvkW6"
JD_LINK      = "https://docs.google.com/document/d/1eN5-zaUqcuG2YbM940Ra2os24LylVNkrzfx5gPPghYE/edit?usp=sharing"
TEAMS_LINK   = ""   # add when confirmed

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets")

INLINE_IMAGES = [
    ("logo_taleemabad", "logo_taleemabad.png"),
]

# ── CANDIDATES (6 shortlisted — emails from Markaz DB) ───────────────────────
CANDIDATES = [
    {"name": "Huma Mumtaz", "email": "huma.mumtaz3@gmail.com"},
]


# ── EMAIL: BUILD HTML (v8 theme — matches feedback email design) ──────────────
def build_email_html(candidate_name, booking_url):

    booking_block = ""
    if booking_url:
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

    teams_line = ""
    if TEAMS_LINK:
        teams_line = f'<p style="margin:0 0 18px 0;text-align:justify;"><strong>Meeting link:</strong> <a href="{TEAMS_LINK}" style="color:#1565c0;">Join on Microsoft Teams</a></p>'

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

            <p style="margin:0 0 18px 0;text-align:justify;">Hi {candidate_name},</p>

            <p style="margin:0 0 18px 0;text-align:justify;">
              Thank you for your interest in the <strong>{POSITION}</strong> role at
              Taleemabad. We have reviewed your application and would like to invite you
              for a <strong>45-minute values conversation</strong> with our team, to learn
              more about you and how your persona aligns with the way we work.
            </p>

            <p style="margin:0 0 18px 0;text-align:justify;">
              The JD for this position is
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
              <a href="https://docs.google.com/document/d/1TBbBAimVX9PxSR6-rT13bLKf38itNdbp5v6EbWuDtkg/edit?tab=t.0"
                 style="color:#1565c0;">interview prep guide</a>
              to understand what to expect from this conversation.
            </p>

            {teams_line}

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
                  <span style="font-size:12px;color:#aaa;margin-top:4px;display:block;">
                    Sent on behalf of Talent Acquisition Team by Coco
                  </span>
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
def send_invite(to_email, to_name, cc_list=None):
    subject = f"Invitation for the Values Interview for {POSITION} - {to_name}"

    msg            = MIMEMultipart("related")
    msg["From"]    = SENDER
    msg["To"]      = to_email
    msg["Subject"] = subject
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(build_email_html(to_name, BOOKING_LINK), "html"))
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
        allow_candidate_addresses(recipients)
        safe_sendmail(smtp, SENDER, recipients, msg.as_string(),
                      context=f"job32_values_invite_{to_email}")

    cc_str = f" (CC: {', '.join(cc_list)})" if cc_list else ""
    print(f"  Sent to {to_name} <{to_email}>{cc_str}")


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Job 32 - Fundraising & Partnerships Manager")
    print("Zero In Call — Values Interview Invitations")
    print(f"Mode: {'PILOT (Ayesha + Jawwad)' if PILOT_MODE else 'LIVE (all 6 candidates)'}")
    print("=" * 60)

    if PILOT_MODE:
        for p in PILOT_RECIPIENTS:
            send_invite(p["email"], p["name"], cc_list=None)
        print(f"\nPilot sent to: {', '.join(p['email'] for p in PILOT_RECIPIENTS)}")
        print("Review it. Then set PILOT_MODE = False and run again to send to all 6.")
    else:
        sent, failed = 0, []
        for c in CANDIDATES:
            try:
                send_invite(c["email"], c["name"], cc_list=CC_STANDARD)
                sent += 1
            except Exception as e:
                print(f"  FAILED for {c['name']}: {e}")
                failed.append(c["name"])

        print(f"\nDone. {sent}/{len(CANDIDATES)} invites sent.")
        if failed:
            print(f"Failed: {', '.join(failed)}")

    print("=" * 60)


if __name__ == "__main__":
    main()
