"""
Task 3 — Send Ayesha a status report covering all completed work,
pending items, and inbox note (pending Gmail OAuth).
"""
import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses


SENDER   = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")
TO       = "ayesha.khan@taleemabad.com"
SUBJECT  = "Coco – Work Status Report (as of 11 Mar 2026)"

HTML = """<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:Arial,sans-serif;">
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#f4f4f4;">
  <tr><td align="center" style="padding:24px 16px;">
    <table cellpadding="0" cellspacing="0" border="0" width="640"
           style="background:#ffffff;border-radius:8px;border:1px solid #dddddd;">

      <!-- Header -->
      <tr>
        <td bgcolor="#2e7a4f" style="border-radius:8px 8px 0 0;padding:22px 32px;">
          <span style="font-family:Arial,sans-serif;font-size:20px;font-weight:bold;
                        color:#ffffff;">Taleemabad &ndash; Talent Acquisition</span>
        </td>
      </tr>

      <!-- Body -->
      <tr>
        <td style="padding:28px 32px 8px 32px;font-size:14px;color:#222222;line-height:1.7;">

          <p style="margin:0 0 6px 0;">Hi Ayesha,</p>
          <p style="margin:0 0 20px 0;">Here is a full summary of everything we have done so far and what is still open.</p>

          <!-- ── COMPLETED ── -->
          <p style="margin:0 0 8px 0;font-size:15px;font-weight:bold;color:#2e7a4f;">
            ✅ Completed
          </p>

          <table cellpadding="6" cellspacing="0" border="0" width="100%"
                 style="border-collapse:collapse;font-size:13px;margin-bottom:22px;">
            <tr style="background:#f0f7f3;">
              <td style="padding:8px 10px;font-weight:bold;border:1px solid #ddd;width:30%;">Position</td>
              <td style="padding:8px 10px;font-weight:bold;border:1px solid #ddd;">What was done</td>
            </tr>
            <tr>
              <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
                <b>Job 36</b><br>Field Coordinator, R&amp;I Studies
              </td>
              <td style="padding:8px 10px;border:1px solid #ddd;">
                179 applications screened &bull; 32 CVs manually read &bull; 20 shortlisted &bull;
                PDF report sent to Muzzammil &bull; All 17 values interview invites sent
                (incl. Amina Batool OOB) &bull; All shortlisted marked on Markaz
              </td>
            </tr>
            <tr style="background:#fafafa;">
              <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
                <b>Job 35</b><br>Junior Research Associate – Impact &amp; Policy
              </td>
              <td style="padding:8px 10px;border:1px solid #ddd;">
                291 applications screened &bull; 63 CVs manually read &bull; 20 shortlisted &bull;
                PDF report sent to Muzzammil &bull; Top 20 marked shortlisted on Markaz &bull;
                270 marked Not a Fit on Markaz &bull;
                Values interview invites sent to 12 candidates today
                (8 excluded — applied to Job 36)
              </td>
            </tr>
            <tr>
              <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
                <b>Job 32</b><br>Fundraising &amp; Partnerships Manager
              </td>
              <td style="padding:8px 10px;border:1px solid #ddd;">
                48 CVs assessed &bull; 10 shortlisted &bull; 3 OOB flags &bull;
                PDF report sent to Sabeena &bull; HTML report v9 sent to you
              </td>
            </tr>
            <tr style="background:#fafafa;">
              <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
                <b>Job 26</b><br>Soul Architect / Conversational UX Designer
              </td>
              <td style="padding:8px 10px;border:1px solid #ddd;">
                42 CVs screened &bull; 2 shortlisted (Danyal Haroon 73, Aisha Bashir 65) &bull;
                Report sent to you &bull; Budget not yet confirmed
              </td>
            </tr>
            <tr>
              <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
                <b>Email design</b><br>Values invite template
              </td>
              <td style="padding:8px 10px;border:1px solid #ddd;">
                Redesigned with branded green header, real social media logos (CID inline),
                purple CTA button, updated content (10 Years of Impact link, bold recording consent)
              </td>
            </tr>
          </table>

          <!-- ── PENDING / INCOMPLETE ── -->
          <p style="margin:0 0 8px 0;font-size:15px;font-weight:bold;color:#c0392b;">
            ⚠️ Still Open / Needs Your Attention
          </p>

          <table cellpadding="6" cellspacing="0" border="0" width="100%"
                 style="border-collapse:collapse;font-size:13px;margin-bottom:22px;">
            <tr style="background:#fdf3f3;">
              <td style="padding:8px 10px;font-weight:bold;border:1px solid #ddd;width:30%;">Item</td>
              <td style="padding:8px 10px;font-weight:bold;border:1px solid #ddd;">What is needed</td>
            </tr>
            <tr>
              <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
                Job 35 — Full screening report
              </td>
              <td style="padding:8px 10px;border:1px solid #ddd;">
                Pilot was sent. Full send to Muzzammil is pending your go-ahead
                (set PILOT_MODE = False in send_job35_v2_report_pdf.py)
              </td>
            </tr>
            <tr style="background:#fafafa;">
              <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
                Job 26 — Budget confirmation
              </td>
              <td style="padding:8px 10px;border:1px solid #ddd;">
                Budget for Soul Architect role not yet set — needed before budget-fit screening
                can be finalised for Danyal and Aisha
              </td>
            </tr>
            <tr>
              <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
                Gmail inbox organisation
              </td>
              <td style="padding:8px 10px;border:1px solid #ddd;">
                In progress — waiting for you to complete the one-time Gmail OAuth
                (run auth_gmail.py). Once done I will create sub-labels under Hiring
                and sort all emails.
              </td>
            </tr>
            <tr style="background:#fafafa;">
              <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
                Emails to respond to
              </td>
              <td style="padding:8px 10px;border:1px solid #ddd;">
                Cannot check until Gmail access is granted. Will send you a follow-up
                count once the OAuth is complete.
              </td>
            </tr>
            <tr>
              <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
                Job 36 &amp; 35 — Values interviews
              </td>
              <td style="padding:8px 10px;border:1px solid #ddd;">
                Invites sent. Candidates are self-booking via Google Calendar.
                Next step: once slots are filled, confirm Teams links and
                share calendar with interviewers.
              </td>
            </tr>
            <tr style="background:#fafafa;">
              <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
                Gmail App Password
              </td>
              <td style="padding:8px 10px;border:1px solid #ddd;">
                If email sending stops working, the Gmail App Password may have expired
                and will need to be regenerated.
              </td>
            </tr>
          </table>

          <p style="margin:0 0 24px 0;font-size:13px;color:#555555;">
            Let me know if anything above needs to be actioned or corrected.
          </p>

        </td>
      </tr>

      <!-- Divider -->
      <tr>
        <td style="padding:0 32px;">
          <table cellpadding="0" cellspacing="0" border="0" width="100%">
            <tr><td style="border-top:1px solid #e0e0e0;font-size:0;line-height:0;">&nbsp;</td></tr>
          </table>
        </td>
      </tr>

      <!-- Footer -->
      <tr>
        <td style="padding:16px 32px 24px 32px;">
          <p style="margin:0 0 4px 0;font-size:14px;font-weight:bold;color:#222222;">See you soon,</p>
          <p style="margin:0 0 14px 0;font-size:14px;color:#222222;">Team Taleemabad</p>
          <p style="margin:0;font-size:11px;color:#aaaaaa;">Coco &ndash; AI Assistant Taleemabad</p>
        </td>
      </tr>

    </table>
  </td></tr>
</table>
</body>
</html>"""


def main():
    msg = MIMEMultipart("alternative")
    msg["From"]    = SENDER
    msg["To"]      = TO
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(HTML, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        allow_candidate_addresses([TO] if isinstance([TO], list) else [[TO]])
        safe_sendmail(smtp, SENDER, [TO], msg.as_string(), context='send_status_report')

    print(f"Status report sent to {TO}")

if __name__ == "__main__":
    main()
