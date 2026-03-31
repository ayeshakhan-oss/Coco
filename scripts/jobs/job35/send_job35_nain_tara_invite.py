"""
Job 35 — Junior Research Associate – Impact & Policy
Values Interview Invitation — Nain Tara (app_id 1534)

Steps:
1. Updates DB status: rejected -> shortlisted
2. Sends values invite email
"""

import os, smtplib, psycopg2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv(dotenv_path="c:/Agent Coco/.env")
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses


# ── CONFIG ────────────────────────────────────────────────────────────────────
POSITION     = "Junior Research Associate \u2013 Impact & Policy"
SENDER       = "ayesha.khan@taleemabad.com"
PASSWORD     = os.getenv("EMAIL_PASSWORD")
HIRING_MGR   = "muzzammil.patel@taleemabad.com"
CC_LIST      = ["hiring@taleemabad.com", HIRING_MGR, "jawwad.ali@taleemabad.com", "ayesha.khan@taleemabad.com"]

CANDIDATE    = {"name": "Nain Tara", "email": "neno.farman@gmail.com", "app_id": 1534}

BOOKING_LINK = "https://calendar.app.google/W76uYNddZAgAHTPy5"
JD_LINK      = ("https://docs.google.com/document/d/1AadGm4xtwKLnTOLaUuPfomI39XeqS_T2W7ZxTrJe7VQ"
                "/edit?tab=t.0#heading=h.ukg679hibl9s")

ASSETS_DIR   = os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets")

INLINE_IMAGES = [
    ("logo_taleemabad", "logo_taleemabad.png"),
    ("logo_facebook",   "logo_facebook.png"),
    ("logo_instagram",  "logo_instagram.png"),
    ("logo_linkedin",   "logo_linkedin.png"),
]

# ── STEP 1: UPDATE DB STATUS ──────────────────────────────────────────────────
def update_status():
    conn = psycopg2.connect(
        host="ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
        dbname="neondb",
        user="neondb_owner",
        password="npg_kBQ10OASHEmd",
        sslmode="require",
    )
    cur  = conn.cursor()
    cur.execute(
        "UPDATE applications SET status = 'shortlisted' WHERE id = %s",
        (CANDIDATE["app_id"],)
    )
    conn.commit()
    print(f"DB updated: app_id {CANDIDATE['app_id']} -> shortlisted")
    cur.close()
    conn.close()

# ── STEP 2: BUILD EMAIL HTML ──────────────────────────────────────────────────
def build_html(name):
    return f"""<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; background-color:#f4f4f4;">
<table cellpadding="0" cellspacing="0" border="0" width="100%"
       style="background-color:#f4f4f4;">
  <tr>
    <td align="center" style="padding:24px 16px;">
      <table cellpadding="0" cellspacing="0" border="0" width="620"
             style="background-color:#ffffff; border-radius:8px; border:1px solid #dddddd;">

        <!-- Green header -->
        <tr>
          <td bgcolor="#2e7a4f" style="border-radius:8px 8px 0 0; padding:22px 32px;">
            <span style="font-family:Arial,sans-serif; font-size:20px; font-weight:bold;
                         color:#ffffff; letter-spacing:0.3px;">
              Taleemabad &ndash; Talent Acquisition
            </span>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:28px 32px 8px 32px; font-family:Arial,sans-serif;
                     font-size:14px; color:#222222; line-height:1.6;">

            <p style="margin:0 0 14px 0;">Hi {name},</p>

            <p style="margin:0 0 14px 0;">
              Thanks for your interest in the <b>{POSITION}</b> role. As a next step,
              we would like to have a <b>45-minute conversation</b> to learn more about
              you and how your persona aligns with Taleemabad values.
            </p>

            <p style="margin:0 0 14px 0;">
              Sharing the key details below so you have everything in one place.
            </p>

            <p style="margin:0 0 6px 0;">
              The JD for this position is
              <a href="{JD_LINK}" style="color:#1a73e8;">here</a>,
              and you can explore more about Taleemabad through the following links:
            </p>

            <table cellpadding="0" cellspacing="0" border="0" style="margin:0 0 14px 0;">
              <tr>
                <td style="padding:3px 0 3px 14px;">
                  &#8226;&nbsp;
                  <a href="https://impact-microsite.vercel.app/"
                     style="color:#1a73e8;">10 Years Of Impact - Taleemabad</a>
                </td>
              </tr>
            </table>

            <p style="margin:0 0 14px 0; font-weight:bold; color:#1a73e8;">
              This session will be recorded, and by joining, you consent to being a
              part of the recorded call.
            </p>

            <p style="margin:0 0 14px 0;">
              Please go through the
              <a href="https://docs.google.com/document/d/1TBbBAimVX9PxSR6-rT13bLKf38itNdbp5v6EbWuDtkg/edit?tab=t.0"
                 style="color:#1a73e8;">interview prep guide</a>
              to understand the process.
            </p>

            <p style="margin:0 0 24px 0;">
              Let us know if you need anything ahead of the interview.
            </p>

          </td>
        </tr>

        <!-- Book button -->
        <tr>
          <td>
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td align="center" style="padding:20px 0 8px 0;">
                  <table cellpadding="0" cellspacing="0" border="0">
                    <tr>
                      <td bgcolor="#5b3fa6" style="border-radius:6px; padding:13px 28px;">
                        <a href="{BOOKING_LINK}"
                           style="color:#ffffff; font-size:15px; font-weight:bold;
                                  text-decoration:none; font-family:Arial,sans-serif;">
                          &#128197;&nbsp; Book your Interview
                        </a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr>
                <td align="center"
                    style="font-family:Arial,sans-serif; font-size:12px; color:#888888;
                           padding:0 0 16px 0;">
                  Please submit the information at your earliest convenience.
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Divider -->
        <tr>
          <td style="padding:0 32px;">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td style="border-top:1px solid #e0e0e0; font-size:0; line-height:0;">&nbsp;</td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="padding:20px 32px 28px 32px;">
            <p style="margin:0 0 10px 0; font-family:Arial,sans-serif;
                      font-size:13px; color:#555555;">
              Feel free to connect with us on our socials to get a sense of our culture:
            </p>
            <table cellpadding="0" cellspacing="0" border="0" style="margin-bottom:18px;">
              <tr>
                <td style="padding-right:12px;" valign="middle">
                  <a href="https://taleemabad.com" style="text-decoration:none;">
                    <img src="cid:logo_taleemabad" width="26" height="46"
                         alt="Taleemabad" style="display:block;border:0;">
                  </a>
                </td>
                <td style="padding-right:10px;" valign="middle">
                  <a href="https://www.facebook.com/taleemabad" style="text-decoration:none;">
                    <img src="cid:logo_facebook" width="36" height="36"
                         alt="Facebook" style="display:block;border:0;border-radius:6px;">
                  </a>
                </td>
                <td style="padding-right:10px;" valign="middle">
                  <a href="https://www.instagram.com/taleemabad" style="text-decoration:none;">
                    <img src="cid:logo_instagram" width="36" height="36"
                         alt="Instagram" style="display:block;border:0;border-radius:6px;">
                  </a>
                </td>
                <td valign="middle">
                  <a href="https://www.linkedin.com/company/taleemabad" style="text-decoration:none;">
                    <img src="cid:logo_linkedin" width="36" height="36"
                         alt="LinkedIn" style="display:block;border:0;border-radius:6px;">
                  </a>
                </td>
              </tr>
            </table>
            <p style="margin:0 0 4px 0; font-family:Arial,sans-serif;
                      font-size:14px; font-weight:bold; color:#222222;">
              See you soon,
            </p>
            <p style="margin:0 0 14px 0; font-family:Arial,sans-serif;
                      font-size:14px; color:#222222;">
              Team Taleemabad
            </p>
            <p style="margin:0; font-family:Arial,sans-serif; font-size:11px; color:#aaaaaa;">
              Coco &ndash; AI Assistant Taleemabad
            </p>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
</body>
</html>"""


# ── STEP 3: SEND EMAIL ────────────────────────────────────────────────────────
def send_invite():
    name    = CANDIDATE["name"]
    to      = CANDIDATE["email"]
    subject = f"Invitation for the Values Interview for {POSITION} - {name}"

    msg          = MIMEMultipart("related")
    msg["From"]  = SENDER
    msg["To"]    = to
    msg["Subject"] = subject
    msg["Cc"]    = ", ".join(CC_LIST)

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(build_html(name), "html"))
    msg.attach(alt)

    for cid, fname in INLINE_IMAGES:
        with open(os.path.join(ASSETS_DIR, fname), "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", f"<{cid}>")
        img.add_header("Content-Disposition", "inline", filename=fname)
        msg.attach(img)

    recipients = [to] + CC_LIST
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        allow_candidate_addresses(recipients if isinstance(recipients, list) else [recipients])
        safe_sendmail(smtp, SENDER, recipients, msg.as_string(), context='send_job35_nain_tara_invite')

    print(f"Invite sent to {name} <{to}>")
    print(f"CC: {', '.join(CC_LIST)}")


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("Job 35 — Nain Tara | Values Invite + Status Update")
    print("=" * 60)
    update_status()
    send_invite()
    print("Done.")
    print("=" * 60)
