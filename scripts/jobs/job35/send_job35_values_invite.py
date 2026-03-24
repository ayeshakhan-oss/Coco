"""
Job 35 - Junior Research Associate – Impact & Policy
Values Interview Invitation - 12 candidates (top 20 minus 8 who also applied to Job 36).

Excluded (applied/shortlisted in Job 36):
  Muhammad Burhan Hassan, Faryal Afridi, Muhammad Junaid, Shahid Kamal,
  Scheherazade Noor, Ali Muhammad, Mariam Rehman, Daniyah Noor

WORKFLOW:
  1. Run with PILOT_MODE = True  --> sends to Ayesha only for review.
  2. On approval, set PILOT_MODE = False and run again --> sends to all 12.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()

# ── CONFIG ────────────────────────────────────────────────────────────────────
PILOT_MODE  = False  # True = Ayesha only; False = all 12 candidates

POSITION    = "Junior Research Associate – Impact & Policy"
SENDER      = "ayesha.khan@taleemabad.com"
PASSWORD    = os.getenv("EMAIL_PASSWORD")
HIRING_MGR  = "muzzammil.patel@taleemabad.com"
CC_STANDARD = ["hiring@taleemabad.com", HIRING_MGR, "jawwad.ali@taleemabad.com", "ayesha.khan@taleemabad.com"]

PILOT_RECIPIENTS = [
    {"email": "ayesha.khan@taleemabad.com", "name": "Ayesha"},
]

BOOKING_LINK = "https://calendar.app.google/W76uYNddZAgAHTPy5"

JD_LINK = ("https://docs.google.com/document/d/1AadGm4xtwKLnTOLaUuPfomI39XeqS_T2W7ZxTrJe7VQ"
           "/edit?tab=t.0#heading=h.ukg679hibl9s")

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

INLINE_IMAGES = [
    ("logo_taleemabad", "logo_taleemabad.png"),
    ("logo_facebook",   "logo_facebook.png"),
    ("logo_instagram",  "logo_instagram.png"),
    ("logo_linkedin",   "logo_linkedin.png"),
]

# ── CANDIDATES (12 shortlisted — emails from Markaz DB) ──────────────────────
CANDIDATES = [
    {"name": "Rameez Wasif",    "email": "rameezwasif1@gmail.com"},
    {"name": "Fatima Tu Zahra", "email": "fatimachohan110@gmail.com"},
    {"name": "Rabia Zafar",     "email": "rabiya.baloch.31@gmail.com"},
    {"name": "Hadiyah Shaheen", "email": "hadiyahshaheen01@gmail.com"},
    {"name": "Hassan Zafar",    "email": "hassanzafar8004474@gmail.com"},
    {"name": "Dur E Nayab",     "email": "durenayab349@gmail.com"},
    {"name": "Rahima Omar",     "email": "rahimaomar321@gmail.com"},
    {"name": "Wasif Mehdi",     "email": "wasifmehdi550@gmail.com"},
    {"name": "Zeeshan Ali",     "email": "zeeshanali.gzr55@gmail.com"},
    {"name": "Mahnoor Hasan",   "email": "mahnoorhasan122@gmail.com"},
    {"name": "Maria Malik",     "email": "malik_maria99@hotmail.com"},
    {"name": "Ayesha Nadeem",   "email": "ayeshanadeem2408@gmail.com"},
]


# ── EMAIL: BUILD HTML ─────────────────────────────────────────────────────────
def build_email_html(candidate_name, booking_url):

    booking_block = f"""
        <tr>
          <td align="center" style="padding:20px 0 8px 0;">
            <table cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td bgcolor="#5b3fa6" style="border-radius:6px; padding:13px 28px;">
                  <a href="{booking_url}"
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
        </tr>"""

    html = f"""<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; background-color:#f4f4f4;">

<table cellpadding="0" cellspacing="0" border="0" width="100%"
       style="background-color:#f4f4f4;">
  <tr>
    <td align="center" style="padding:24px 16px;">

      <table cellpadding="0" cellspacing="0" border="0" width="620"
             style="background-color:#ffffff; border-radius:8px;
                    border:1px solid #dddddd;">

        <!-- Green header -->
        <tr>
          <td bgcolor="#2e7a4f" style="border-radius:8px 8px 0 0; padding:22px 32px;">
            <span style="font-family:Arial,sans-serif; font-size:20px;
                          font-weight:bold; color:#ffffff; letter-spacing:0.3px;">
              Taleemabad &ndash; Talent Acquisition
            </span>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:28px 32px 8px 32px; font-family:Arial,sans-serif;
                     font-size:14px; color:#222222; line-height:1.6;">

            <p style="margin:0 0 14px 0;">Hi {candidate_name},</p>

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
              {booking_block}
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

            <p style="margin:0; font-family:Arial,sans-serif;
                      font-size:11px; color:#aaaaaa;">
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
    return html


# ── EMAIL: SEND ───────────────────────────────────────────────────────────────
def send_invite(to_email, to_name, booking_url, cc_list=None):
    subject = f"Invitation for the Values Interview for {POSITION} - {to_name}"

    msg            = MIMEMultipart("related")
    msg["From"]    = SENDER
    msg["To"]      = to_email
    msg["Subject"] = subject
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(build_email_html(to_name, booking_url), "html"))
    msg.attach(alt)

    for cid, fname in INLINE_IMAGES:
        with open(os.path.join(ASSETS_DIR, fname), "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", f"<{cid}>")
        img.add_header("Content-Disposition", "inline", filename=fname)
        msg.attach(img)

    recipients = [to_email] + (cc_list or [])
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.sendmail(SENDER, recipients, msg.as_string())

    cc_str = f" (CC: {', '.join(cc_list)})" if cc_list else ""
    print(f"  Sent to {to_name} <{to_email}>{cc_str}")


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Job 35 - Values Interview Invites")
    print(f"Mode: {'PILOT (Ayesha only)' if PILOT_MODE else 'FULL SEND (all 12 candidates)'}")
    print("=" * 60)

    booking_url = BOOKING_LINK
    print(f"\nBooking link: {booking_url}")

    print(f"\n[Sending invites...]")

    if PILOT_MODE:
        for p in PILOT_RECIPIENTS:
            send_invite(p["email"], p["name"], booking_url, cc_list=None)
        print(f"\nPilot sent to: {', '.join(p['email'] for p in PILOT_RECIPIENTS)}.")
        print("Review it. Then set PILOT_MODE = False and run again to send to all 12.")
    else:
        sent, failed = 0, []
        for c in CANDIDATES:
            try:
                send_invite(c["email"], c["name"], booking_url, cc_list=CC_STANDARD)
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
