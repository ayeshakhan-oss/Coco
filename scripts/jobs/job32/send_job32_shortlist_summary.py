"""
Send Job 32 shortlist summary to Ayesha.
"""
import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses


SENDER   = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")
TO       = "ayesha.khan@taleemabad.com"
SUBJECT  = "Shortlisted Candidates – Fundraising & Partnerships Manager (Job 32)"

HTML = """<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:Arial,sans-serif;">
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#f4f4f4;">
  <tr><td align="center" style="padding:24px 16px;">
    <table cellpadding="0" cellspacing="0" border="0" width="680"
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
        <p style="margin:0 0 20px 0;">
          Here are the shortlisted candidates for
          <b>Fundraising &amp; Partnerships Manager (Job 32)</b> from the most recent screening report.
          68 candidates assessed &bull; Budget: PKR 200K–270K
        </p>

        <!-- Table -->
        <table cellpadding="6" cellspacing="0" border="0" width="100%"
               style="border-collapse:collapse;font-size:12.5px;margin-bottom:24px;">
          <tr style="background:#2e7a4f;color:#ffffff;">
            <td style="padding:9px 10px;border:1px solid #ccc;font-weight:bold;">#</td>
            <td style="padding:9px 10px;border:1px solid #ccc;font-weight:bold;">Name</td>
            <td style="padding:9px 10px;border:1px solid #ccc;font-weight:bold;">Score</td>
            <td style="padding:9px 10px;border:1px solid #ccc;font-weight:bold;">Tier</td>
            <td style="padding:9px 10px;border:1px solid #ccc;font-weight:bold;">Budget</td>
            <td style="padding:9px 10px;border:1px solid #ccc;font-weight:bold;">Exp. Salary</td>
            <td style="padding:9px 10px;border:1px solid #ccc;font-weight:bold;">Current Role</td>
            <td style="padding:9px 10px;border:1px solid #ccc;font-weight:bold;">Verdict</td>
          </tr>

          <!-- SHORTLIST -->
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;">1</td>
            <td style="padding:8px 10px;border:1px solid #ddd;"><b>Danish Hussain</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">88</td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">A</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#c0392b;">Out of Budget</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">PKR 550,000</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Director Programs/Fundraising, multiple INGOs</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#e67e22;font-weight:bold;">HOLD – Location (Hyderabad)</td>
          </tr>
          <tr style="background:#f9f9f9;">
            <td style="padding:8px 10px;border:1px solid #ddd;">2</td>
            <td style="padding:8px 10px;border:1px solid #ddd;"><b>Mizhgan Kirmani</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">84</td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">B</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#1a6b3c;font-weight:bold;">In Budget</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">PKR 250,000</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Manager Donor Relations, TCF; BD Officer, Tearfund UK</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#1a6b3c;font-weight:bold;">SHORTLIST</td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;">3</td>
            <td style="padding:8px 10px;border:1px solid #ddd;"><b>Muhammad Adnan</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">82</td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">B</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#c0392b;">Out of Budget</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">PKR 575,000</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Global Acquisition Mgr, C4ED (Germany); prev CERP, GIZ, British Council</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#1a6b3c;font-weight:bold;">SHORTLIST</td>
          </tr>
          <tr style="background:#f9f9f9;">
            <td style="padding:8px 10px;border:1px solid #ddd;">4</td>
            <td style="padding:8px 10px;border:1px solid #ddd;"><b>Arsim Tariq</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">78</td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">B</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#e67e22;">Borderline</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">PKR 280K–300K</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Resource Mobilisation &amp; BD Consultant</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#1a6b3c;font-weight:bold;">SHORTLIST</td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;">5</td>
            <td style="padding:8px 10px;border:1px solid #ddd;"><b>Shahzad Saleem Abbasi</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">75</td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">B</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#1a6b3c;font-weight:bold;">In Budget</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">PKR 270,000</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Head Fundraising, Alkhidmat Rawalpindi</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#1a6b3c;font-weight:bold;">SHORTLIST</td>
          </tr>
          <tr style="background:#f9f9f9;">
            <td style="padding:8px 10px;border:1px solid #ddd;">6</td>
            <td style="padding:8px 10px;border:1px solid #ddd;"><b>Arsalan Ashraf</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">72</td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">B</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#c0392b;">Out of Budget</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">PKR 450,000</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">BD Manager, HANDS; prev Meta/Chevron CSR lead</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#1a6b3c;font-weight:bold;">SHORTLIST</td>
          </tr>

          <!-- CONSIDER -->
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;">7</td>
            <td style="padding:8px 10px;border:1px solid #ddd;"><b>Ahad Ahsan Khan</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">67</td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">C</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#c0392b;">Out of Budget</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">PKR 550,000</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Manager Grants (SRS), AKU Karachi</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#555;">CONSIDER</td>
          </tr>
          <tr style="background:#f9f9f9;">
            <td style="padding:8px 10px;border:1px solid #ddd;">8</td>
            <td style="padding:8px 10px;border:1px solid #ddd;"><b>Mushahid Hussain</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">65</td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">C</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#1a6b3c;font-weight:bold;">In Budget</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">PKR 170,000</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Manager Partnerships, READ Foundation</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#555;">CONSIDER</td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;">9</td>
            <td style="padding:8px 10px;border:1px solid #ddd;"><b>Hamdan Ahmad</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">60</td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">C</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#e67e22;">Borderline</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">PKR 320,000</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Social Safeguards Consultant, World Bank Group</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#555;">CONSIDER</td>
          </tr>
          <tr style="background:#f9f9f9;">
            <td style="padding:8px 10px;border:1px solid #ddd;">10</td>
            <td style="padding:8px 10px;border:1px solid #ddd;"><b>Sobia Ayub</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">58</td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">C</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#e67e22;">Borderline</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">PKR 300,000</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Fulbright Scholar; Masters Int'l Dev, Univ. of Pittsburgh 2025</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#555;">CONSIDER</td>
          </tr>
          <tr>
            <td style="padding:8px 10px;border:1px solid #ddd;">11</td>
            <td style="padding:8px 10px;border:1px solid #ddd;"><b>Faheem Baig</b></td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">55</td>
            <td style="padding:8px 10px;border:1px solid #ddd;text-align:center;">C</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#1a6b3c;font-weight:bold;">In Budget</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">PKR 145,000</td>
            <td style="padding:8px 10px;border:1px solid #ddd;">Program Manager, AKDN</td>
            <td style="padding:8px 10px;border:1px solid #ddd;color:#555;">CONSIDER</td>
          </tr>
        </table>

        <p style="margin:0 0 6px 0;font-size:13px;color:#555;">
          <b>In-budget shortlisted:</b> Mizhgan Kirmani (PKR 250K) &bull; Shahzad Saleem Abbasi (PKR 270K) &bull; Mushahid Hussain (PKR 170K) &bull; Faheem Baig (PKR 145K)
        </p>
        <p style="margin:0 0 24px 0;font-size:13px;color:#555;">
          <b>Strongest candidate</b> is Danish Hussain (score 88, PKR 1B+ closed) but he is out of budget and based in Hyderabad. Recommend discussing with Sabeena whether to proceed with an exploratory call.
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
        safe_sendmail(smtp, SENDER, [TO], msg.as_string(), context='send_job32_shortlist_summary')
    print(f"Sent to {TO}")

if __name__ == "__main__":
    main()
