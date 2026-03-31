"""
Status Report v2 — includes inbox emails needing response.
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
SUBJECT  = "Coco – Full Status Report + Emails Needing Your Response (11 Mar 2026)"

HTML = """<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:Arial,sans-serif;">
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#f4f4f4;">
  <tr><td align="center" style="padding:24px 16px;">
    <table cellpadding="0" cellspacing="0" border="0" width="660"
           style="background:#ffffff;border-radius:8px;border:1px solid #dddddd;">

      <!-- Header -->
      <tr>
        <td bgcolor="#2e7a4f" style="border-radius:8px 8px 0 0;padding:22px 32px;">
          <span style="font-size:20px;font-weight:bold;color:#ffffff;">
            Taleemabad &ndash; Talent Acquisition
          </span>
        </td>
      </tr>

      <tr><td style="padding:28px 32px 8px 32px;font-size:14px;color:#222;line-height:1.7;">

        <p style="margin:0 0 6px 0;">Hi Ayesha,</p>
        <p style="margin:0 0 22px 0;">
          Here is your full status report — work completed, what is still open,
          and the emails in your inbox that need your attention.
        </p>

        <!-- ══ SECTION 1: WORK DONE ══ -->
        <p style="margin:0 0 8px 0;font-size:15px;font-weight:bold;color:#2e7a4f;">
          &#10003; Work Completed (Coco)
        </p>
        <table cellpadding="6" cellspacing="0" border="0" width="100%"
               style="border-collapse:collapse;font-size:13px;margin-bottom:22px;">
          <tr style="background:#f0f7f3;">
            <td style="padding:8px 10px;font-weight:bold;border:1px solid #ddd;width:28%;">What</td>
            <td style="padding:8px 10px;font-weight:bold;border:1px solid #ddd;">Details</td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>Job 36 — Field Coordinator R&amp;I</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">179 screened &bull; 20 shortlisted &bull; PDF report sent to Muzzammil &bull; 17 values invites sent &bull; Markaz statuses updated</td>
          </tr>
          <tr style="background:#fafafa;">
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>Job 35 — Junior RA Impact &amp; Policy</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">291 screened &bull; 20 shortlisted &bull; PDF report sent &bull; 12 values invites sent today &bull; 20 marked Shortlisted on Markaz &bull; 270 marked Not a Fit on Markaz</td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>Job 32 — Fundraising Manager</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">48 screened &bull; 10 shortlisted &bull; PDF report sent to Sabeena</td>
          </tr>
          <tr style="background:#fafafa;">
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>Job 26 — Soul Architect</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">42 screened &bull; 2 shortlisted (Danyal Haroon, Aisha Bashir) &bull; Report sent</td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>Gmail inbox</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">13 position sub-labels created under Hiring &bull; all coloured &bull; ~1,302 emails organised</td>
          </tr>
          <tr style="background:#fafafa;">
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>Values invite design</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Redesigned — branded green header, real social logos, purple CTA button, updated content</td>
          </tr>
        </table>

        <!-- ══ SECTION 2: EMAILS NEEDING RESPONSE ══ -->
        <p style="margin:0 0 8px 0;font-size:15px;font-weight:bold;color:#c0392b;">
          &#9888; Emails Needing Your Response
        </p>
        <table cellpadding="6" cellspacing="0" border="0" width="100%"
               style="border-collapse:collapse;font-size:13px;margin-bottom:22px;">
          <tr style="background:#fdf3f3;">
            <td style="padding:8px 10px;font-weight:bold;border:1px solid #ddd;width:28%;">From</td>
            <td style="padding:8px 10px;font-weight:bold;border:1px solid #ddd;">What they need</td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
              <b>Scheherazade Noor</b><br>
              <span style="color:#888;font-size:12px;">noorscheherazade@gmail.com</span>
            </td>
            <td style="padding:8px 10px;border:1px solid #ddd;">
              Booked her Job 36 values interview slot but says the
              <b>JD Google Doc link requires access</b> — she cannot open it.
              Please share/grant view access to the JD doc.
            </td>
          </tr>
          <tr style="background:#fafafa;">
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
              <b>Nain Tara</b><br>
              <span style="color:#888;font-size:12px;">neno.farman@gmail.com</span>
            </td>
            <td style="padding:8px 10px;border:1px solid #ddd;">
              Following up on her application for <b>Junior Research Associate AND Field Coordinator</b>
              — she applied to both and wants a status update.
            </td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
              <b>Maryam Rafaqat</b><br>
              <span style="color:#888;font-size:12px;">maryamrafaqat88@gmail.com</span>
            </td>
            <td style="padding:8px 10px;border:1px solid #ddd;">
              Re: Hackathon 2026 Technical Interview — she is based in <b>Lahore</b> and
              asking if the interview can be conducted <b>online</b>. Needs a yes/no.
            </td>
          </tr>
          <tr style="background:#fafafa;">
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
              <b>Raiyaan Hamid</b><br>
              <span style="color:#888;font-size:12px;">raiyaanjhamid@gmail.com</span>
            </td>
            <td style="padding:8px 10px;border:1px solid #ddd;">
              Re: Hackathon 2026 Technical Interview — requesting to <b>shift slot from 11am to 12pm
              on 16th March</b>. Needs confirmation.
            </td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
              <b>Shahbaz Ali Khan</b><br>
              <span style="color:#888;font-size:12px;">via hiring@taleemabad.com</span>
            </td>
            <td style="padding:8px 10px;border:1px solid #ddd;">
              Re: Consulting contract with Rare Sense Inc — asking
              <b>what is the exact expiry date of the addendum</b>
              (states 6 months from Dec 2025 but no actual date mentioned).
            </td>
          </tr>
          <tr style="background:#fafafa;">
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;">
              <b>Asma Zaheer</b><br>
              <span style="color:#888;font-size:12px;">asma.zaheer@niete.edu.pk</span>
            </td>
            <td style="padding:8px 10px;border:1px solid #ddd;">
              Sent <b>Proposed Work Arrangement Options (March–May)</b> — a WFH support request
              that appears to need HR review and a response.
            </td>
          </tr>
        </table>

        <!-- ══ SECTION 3: FYI ══ -->
        <p style="margin:0 0 8px 0;font-size:15px;font-weight:bold;color:#555;">
          &#8505; FYI — No Action Needed
        </p>
        <table cellpadding="6" cellspacing="0" border="0" width="100%"
               style="border-collapse:collapse;font-size:13px;margin-bottom:22px;">
          <tr style="background:#f9f9f9;">
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;width:28%;"><b>Fatima Razzaq</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Declined Job 36 values interview — not interested in the position.</td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>Amina Batool</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Replied positively to Job 36 values invite — excited about the opportunity.</td>
          </tr>
          <tr style="background:#f9f9f9;">
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>New applications</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Maria Karim (Job 36), Shahzad (Odoo), Hamza Sattar (CPD Coach), Hassan Raza (Odoo), Muhammad Aman Khan (Job 32) — all in Markaz.</td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>Case Study — Nain Tara</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Submitted case study for Soul Architect / Conversational UX Designer.</td>
          </tr>
          <tr style="background:#f9f9f9;">
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>Danyal Haroon (Job 26)</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Case Study Debrief scheduled — Jawwad handling. Calendar invite sent for Fri 13 Mar, 11am.</td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>Waqas Pervaiz (Job 10)</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Confirmed Case Study Debrief — Wed 18 Mar, 3:30pm. Jawwad handling.</td>
          </tr>
        </table>

        <!-- ══ SECTION 4: STILL OPEN ══ -->
        <p style="margin:0 0 8px 0;font-size:15px;font-weight:bold;color:#e67e22;">
          &#9654; Still Open
        </p>
        <table cellpadding="6" cellspacing="0" border="0" width="100%"
               style="border-collapse:collapse;font-size:13px;margin-bottom:22px;">
          <tr style="background:#fef9f0;">
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;width:28%;"><b>Job 35 — Full report send</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Pilot was sent. Awaiting your go-ahead to send full report to Muzzammil.</td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>Job 26 — Budget</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Budget for Soul Architect not confirmed — needed for final budget-fit screening of Danyal and Aisha.</td>
          </tr>
          <tr style="background:#fef9f0;">
            <td style="padding:8px 10px;border:1px solid #ddd;vertical-align:top;"><b>Values interviews — Teams links</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Job 35 and Job 36 candidates are booking slots. Once booked, Teams links need to be added to the calendar invites.</td>
          </tr>
        </table>

        <p style="margin:0 0 24px 0;font-size:13px;color:#555;">
          Let me know if you'd like me to draft replies to any of the emails above.
        </p>

      </td></tr>

      <!-- Divider -->
      <tr><td style="padding:0 32px;">
        <table cellpadding="0" cellspacing="0" border="0" width="100%">
          <tr><td style="border-top:1px solid #e0e0e0;font-size:0;line-height:0;">&nbsp;</td></tr>
        </table>
      </td></tr>

      <!-- Footer -->
      <tr><td style="padding:16px 32px 24px 32px;">
        <p style="margin:0 0 4px 0;font-size:14px;font-weight:bold;color:#222;">See you soon,</p>
        <p style="margin:0 0 14px 0;font-size:14px;color:#222;">Team Taleemabad</p>
        <p style="margin:0;font-size:11px;color:#aaa;">Coco &ndash; AI Assistant Taleemabad</p>
      </td></tr>

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
        safe_sendmail(smtp, SENDER, [TO], msg.as_string(), context='send_status_report_v2')

    print(f"Report sent to {TO}")

if __name__ == "__main__":
    main()
