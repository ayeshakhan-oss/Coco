"""
Job 36 - Field Coordinator, Research & Impact Studies
Values Interview Invitation - send to 17 shortlisted candidates.

WORKFLOW:
  1. Run in PILOT_MODE = True  --> sends to Ayesha only for review.
  2. On approval, set PILOT_MODE = False and run again --> sends to all 17.

BEFORE RUNNING:
  - token.json must exist (run auth_google_calendar.py if not)
  - .env must have EMAIL_PASSWORD set
  - Set TEAMS_LINK once available
  - If booking URL creation fails, set BOOKING_LINK manually after creating
    the appointment page at calendar.google.com
"""

import os
import smtplib
import datetime
import requests as http_requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses


# ── CONFIG ────────────────────────────────────────────────────────────────────
PILOT_MODE  = True  # True = Ayesha + Jawwad only; False = all 17 candidates

POSITION    = "Field Coordinator, Research & Impact Studies"
SENDER      = "ayesha.khan@taleemabad.com"
PASSWORD    = os.getenv("EMAIL_PASSWORD")
HIRING_MGR  = "muzzammil.patel@taleemabad.com"
CC_STANDARD = ["hiring@taleemabad.com", HIRING_MGR, "ayesha.khan@taleemabad.com"]   # not used in pilot

PILOT_RECIPIENTS = [
    {"email": "ayesha.khan@taleemabad.com", "name": "Ayesha"},
]

# Add Teams link here when confirmed. Leave empty for now.
TEAMS_LINK  = ""

# If API creation fails, paste the booking URL here manually.
BOOKING_LINK = "https://calendar.app.google/J4Jn7aCvmTDp7ZQf9"

TOKEN_FILE  = os.path.join(os.path.dirname(__file__), "token.json")
SCOPES      = ["https://www.googleapis.com/auth/calendar"]

TODAY       = datetime.date.today()
START_DATE  = TODAY + datetime.timedelta(days=1)
END_DATE    = TODAY + datetime.timedelta(days=15)

# ── CANDIDATES (17 shortlisted from Markaz DB, Job 36) ───────────────────────
CANDIDATES = [
    {"name": "Asif Khan",           "email": "Asifmkhan771@gmail.com"},
    {"name": "Zubair Hussain",      "email": "zubair.hafiz8@gmail.com"},
    {"name": "Jawad Khan",          "email": "jawadmarwat47@gmail.com"},
    {"name": "Fatima Razzaq",       "email": "fatima.razzaq92@gmail.com"},
    {"name": "Fatima Mughal",       "email": "fatima_knz@yahoo.com"},
    {"name": "HabibunNabi",         "email": "habibbest@gmail.com"},
    {"name": "Asad Farooq",         "email": "masad.malik59@gmail.com"},
    {"name": "Jalal Ud Din",        "email": "jalalsaraikhan@gmail.com"},
    {"name": "Ali Zia",             "email": "alizia.hyder@outlook.com"},
    {"name": "Faryal Afridi",       "email": "faryalafridi4@gmail.com"},
    {"name": "Usman Ahmed Khan",    "email": "usmanumar646@gmail.com"},
    {"name": "Scheherazade Noor",   "email": "noorscheherazade@gmail.com"},
    {"name": "Muhammad Junaid",     "email": "junaidjadee912@gmail.com"},
    {"name": "Muhammad Omer Khan",  "email": "mokhan.2173@gmail.com"},
    {"name": "Muhammad Siddique",   "email": "siddiquemuhammad100@gmail.com"},
    {"name": "Amina Batool",        "email": "aminabatool2000@gmail.com"},
    {"name": "Mehwish",             "email": "aly_mehwish@yahoo.com"},
]


# ── GOOGLE CALENDAR: CREATE APPOINTMENT SCHEDULE (REST API) ──────────────────
def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise RuntimeError("token.json missing or invalid. Run auth_google_calendar.py first.")
    return creds


def create_appointment_schedule():
    """
    Creates a Google Calendar appointment schedule via REST API.
    Mon-Fri, 11am-12pm and 1pm-2pm PKT, 2-week window, 45 min duration.
    Returns booking URL or None.
    """
    try:
        creds = get_credentials()
        headers = {
            "Authorization": f"Bearer {creds.token}",
            "Content-Type": "application/json",
        }

        start_str = START_DATE.strftime("%Y-%m-%dT00:00:00+05:00")
        end_str   = END_DATE.strftime("%Y-%m-%dT23:59:59+05:00")

        body = {
            "title": f"Zero In Call for {POSITION}",
            "description": (
                "45-minute values conversation with the Taleemabad hiring team. "
                "Please book a slot that works for you."
            ),
            "appointmentDuration": "2700s",
            "schedulingWindow": {
                "startTime": start_str,
                "endTime":   end_str,
            },
            "availabilityWindows": [
                {
                    "startTimeOfDay": {"hours": 11, "minutes": 0},
                    "endTimeOfDay":   {"hours": 12, "minutes": 0},
                    "daysOfWeek": ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"],
                },
                {
                    "startTimeOfDay": {"hours": 13, "minutes": 0},
                    "endTimeOfDay":   {"hours": 14, "minutes": 0},
                    "daysOfWeek": ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"],
                },
            ],
        }

        url  = "https://www.googleapis.com/calendar/v3/users/me/appointmentSchedules"
        resp = http_requests.post(url, headers=headers, json=body)

        if resp.status_code in (200, 201):
            data        = resp.json()
            booking_url = data.get("bookingUrl") or data.get("selfLink", "")
            print(f"  Appointment schedule created.")
            print(f"  Booking URL: {booking_url}")
            return booking_url
        else:
            print(f"  API returned {resp.status_code}: {resp.text[:400]}")
            raise Exception(f"HTTP {resp.status_code}")

    except Exception as e:
        print(f"  WARNING: Could not create appointment schedule via API: {e}")
        print("  --> Create it manually in Google Calendar:")
        print("      calendar.google.com > Other calendars > + > Appointment schedule")
        print("  --> Set: 45 min, Mon-Fri, 11am-12pm and 1pm-2pm, 2 weeks")
        print("  --> Copy the booking page URL and paste as BOOKING_LINK in this script.")
        return None


# ── EMAIL: BUILD HTML ─────────────────────────────────────────────────────────
def build_email_html(candidate_name, booking_url):

    # "Book your Interview" button — shown only when booking_url exists
    if booking_url:
        booking_block = f"""
        <!-- Book your Interview button -->
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
    else:
        booking_block = ""

    teams_row = ""
    if TEAMS_LINK:
        teams_row = f"""
        <tr><td style="padding:6px 0;">
          <b>Meeting link:</b>&nbsp;
          <a href="{TEAMS_LINK}" style="color:#1a73e8;">Join on Microsoft Teams</a>
        </td></tr>"""

    html = f"""<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; background-color:#f4f4f4;">

<!-- ── Outer wrapper ── -->
<table cellpadding="0" cellspacing="0" border="0" width="100%"
       style="background-color:#f4f4f4;">
  <tr>
    <td align="center" style="padding:24px 16px;">

      <!-- ── Card ── -->
      <table cellpadding="0" cellspacing="0" border="0" width="620"
             style="background-color:#ffffff; border-radius:8px;
                    border:1px solid #dddddd;">

        <!-- ── Green header ── -->
        <tr>
          <td bgcolor="#2e7a4f" style="border-radius:8px 8px 0 0; padding:22px 32px;">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td>
                  <span style="font-family:Arial,sans-serif; font-size:20px;
                                font-weight:bold; color:#ffffff; letter-spacing:0.3px;">
                    Taleemabad &ndash; Talent Acquisition
                  </span>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ── Body ── -->
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
              <a href="https://docs.google.com/document/d/1iaaMX9NM9V3n97a6sovcd3RraXuQfFEpWk5v3ez2-oQ/edit?tab=t.0#heading=h.oyc4na9x2aos"
                 style="color:#1a73e8;">here</a>,
              and you can explore more about Taleemabad through the following links:
            </p>

            <table cellpadding="0" cellspacing="0" border="0"
                   style="margin:0 0 14px 0;">
              <tr>
                <td style="padding:3px 0 3px 14px;">
                  &#8226;&nbsp;
                  <a href="https://impact-microsite.vercel.app/"
                     style="color:#1a73e8;">10 Years Of Impact - Taleemabad</a>
                </td>
              </tr>
              {teams_row}
            </table>

            <p style="margin:0 0 14px 0;
                      font-weight:bold; color:#1a73e8;">
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

        <!-- ── Book button row ── -->
        <tr>
          <td>
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
              {booking_block}
            </table>
          </td>
        </tr>

        <!-- ── Divider ── -->
        <tr>
          <td style="padding:0 32px;">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td style="border-top:1px solid #e0e0e0; font-size:0; line-height:0;">&nbsp;</td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ── Footer ── -->
        <tr>
          <td style="padding:20px 32px 28px 32px;">

            <p style="margin:0 0 10px 0; font-family:Arial,sans-serif;
                      font-size:13px; color:#555555;">
              Feel free to connect with us on our socials to get a sense of our culture:
            </p>

            <!-- Social icons row -->
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
      <!-- ── /Card ── -->

    </td>
  </tr>
</table>

</body>
</html>"""
    return html


# ── EMAIL: SEND ───────────────────────────────────────────────────────────────
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

INLINE_IMAGES = [
    ("logo_taleemabad", "logo_taleemabad.png"),
    ("logo_facebook",   "logo_facebook.png"),
    ("logo_instagram",  "logo_instagram.png"),
    ("logo_linkedin",   "logo_linkedin.png"),
]


def send_invite(to_email, to_name, booking_url, cc_list=None):
    subject = f"Invitation for the Values Interview for {POSITION} - {to_name}"

    # Outer: related — allows inline CID image attachments
    msg            = MIMEMultipart("related")
    msg["From"]    = SENDER
    msg["To"]      = to_email
    msg["Subject"] = subject
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    # HTML part wrapped in alternative
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(build_email_html(to_name, booking_url), "html"))
    msg.attach(alt)

    # Inline logo attachments
    for cid, fname in INLINE_IMAGES:
        with open(os.path.join(ASSETS_DIR, fname), "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", f"<{cid}>")
        img.add_header("Content-Disposition", "inline", filename=fname)
        msg.attach(img)

    recipients = [to_email] + (cc_list or [])
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        allow_candidate_addresses(recipients if isinstance(recipients, list) else [recipients])
        safe_sendmail(smtp, SENDER, recipients, msg.as_string(), context='send_job36_values_invite')

    cc_str = f" (CC: {', '.join(cc_list)})" if cc_list else ""
    print(f"  Sent to {to_name} <{to_email}>{cc_str}")


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Job 36 - Values Interview Invites")
    print(f"Mode: {'PILOT (Ayesha + Jawwad)' if PILOT_MODE else 'FULL SEND (all 17 candidates)'}")
    print("=" * 60)

    # Step 1: Get booking URL
    print("\n[1/2] Setting up Google Calendar appointment schedule...")
    booking_url = BOOKING_LINK or None

    if not booking_url:
        booking_url = create_appointment_schedule()

    if not booking_url:
        print("\n  NOTE: Email will be sent WITHOUT a self-booking link.")
        print("  Add it by setting BOOKING_LINK in this script after creating manually.")

    # Step 2: Send emails
    print(f"\n[2/2] Sending invites...")

    if PILOT_MODE:
        for p in PILOT_RECIPIENTS:
            send_invite(p["email"], p["name"], booking_url, cc_list=None)
        print(f"\nPilot sent to: {', '.join(p['email'] for p in PILOT_RECIPIENTS)}.")
        print("Review it. Then set PILOT_MODE = False and run again to send to all 17.")
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
