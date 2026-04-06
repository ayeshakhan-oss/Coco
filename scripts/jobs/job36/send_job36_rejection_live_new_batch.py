"""
Job 36 New Batch — Rejection Emails LIVE SEND
Sends CV-stage rejection emails to all 15 candidates individually.
CC: hiring@taleemabad.com + ayesha.khan@taleemabad.com on every email.
HTML v8 design: white header + blue border + CID logo + Georgia serif body.
"""

import os, re, smtplib, base64, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
from scripts.utils.feedback_widget import feedback_widget

EMAIL_HOST     = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT     = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

DRAFTS_DIR = "c:/Agent Coco/output/rejection_emails_job36_new_batch/"
LOGO_PATH  = os.path.join(os.path.dirname(__file__), "../../..", "assets", "logo_taleemabad.png")
CC         = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]
ROLE       = "Field Coordinator, Research &amp; Impact Studies"
SUBJECT    = "Your Application for Field Coordinator, Research & Impact Studies"

CANDIDATES = [
    {"app_id": 2124, "name": "Hafiza Iqra Bashir",       "email": "hafizaiqrabashir@hotmail.com"},
    {"app_id": 2122, "name": "Ali Haider Baloch",         "email": "alihaiderbaloch1512@gmail.com"},
    {"app_id": 2119, "name": "Hassan Tahir",              "email": "hasstahir395@gmail.com"},
    {"app_id": 2108, "name": "Hiba Ahmed",                "email": "hibaahmed7604@gmail.com"},
    {"app_id": 2106, "name": "Faris Meher Ali",           "email": "farismeherali@gmail.com"},
    {"app_id": 2105, "name": "Hamza Khan",                "email": "hamzasikhan@gmail.com"},
    {"app_id": 2103, "name": "Attiqua Urfa",              "email": "Attiqua.urfaabdullah786@gmail.com"},
    {"app_id": 2090, "name": "Mehreen Tariq",             "email": "26020521@lums.edu.pk"},
    {"app_id": 2079, "name": "Umme Farwa",                "email": "ummef127@gmail.com"},
    {"app_id": 2061, "name": "Easha Imtiaz",              "email": "eashaimtiaz4@gmail.com"},
    {"app_id": 2053, "name": "Hamza Sattar",              "email": "sattarh630@gmail.com"},
    {"app_id": 2050, "name": "Anosha Umer",               "email": "anoshaumer19@gmail.com"},
    {"app_id": 2029, "name": "Syed Muhammad Ali Abbas",   "email": "26100287@lums.edu.pk"},
    {"app_id": 2024, "name": "Mohid Naveed Sufi",         "email": "mohidsufi@gmail.com"},
    {"app_id": 2022, "name": "Maheen Sughra",             "email": "sughra.maheenn@gmail.com"},
]


def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


def read_draft(app_id, name):
    fname = f"{app_id}_{safe_filename(name)}.txt"
    path = os.path.join(DRAFTS_DIR, fname)
    if not os.path.exists(path):
        return None, None
    with open(path, encoding="utf-8") as f:
        content = f.read()
    # Strip pilot header
    lines = content.splitlines()
    body_lines = []
    skip = True
    for line in lines:
        if skip and line.startswith("=" * 10):
            skip = False
            continue
        if skip:
            continue
        body_lines.append(line)
    raw = "\n".join(body_lines).strip()

    # Split subject from body
    subject = SUBJECT
    if raw.startswith("Subject:"):
        first_nl = raw.index("\n")
        subject = raw[:first_nl].replace("Subject:", "").strip()
        raw = raw[first_nl:].strip()

    return subject, raw


def text_to_html(text):
    """Convert plain text email body to HTML paragraphs."""
    P = lambda t: f'<p style="margin:0 0 18px 0;text-align:justify;">{t}</p>'
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    html_parts = []
    for para in paras:
        # Skip the sign-off block — rendered by FOOTER
        if para.startswith("Warm regards"):
            break
        safe = (para
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br>"))
        html_parts.append(P(safe))
    return "\n".join(html_parts)


def header_block():
    return f"""
<table width="100%" cellpadding="0" cellspacing="0"
       style="border-radius:8px 8px 0 0;overflow:hidden;
              border-bottom:2px solid #1565c0;">
  <tr>
    <td align="center" bgcolor="#ffffff"
        style="background-color:#ffffff;padding:28px 40px 22px 40px;">
      <img src="cid:taleemabad_logo" height="38" alt="Taleemabad"
           style="display:block;margin:0 auto 14px auto;">
      <p style="margin:0;font-family:Georgia,serif;font-size:11px;
                color:#1565c0;letter-spacing:2px;text-transform:uppercase;">
        People &amp; Culture &nbsp;&bull;&nbsp; Application Update
      </p>
      <p style="margin:10px 0 4px 0;font-family:Georgia,serif;font-size:17px;
                font-weight:bold;color:#1565c0;line-height:1.4;">
        Your Application for Field Coordinator
      </p>
      <p style="margin:0;font-family:Georgia,serif;font-size:12px;color:#5c85c7;">
        {ROLE}
      </p>
    </td>
  </tr>
</table>"""


FOOTER = """
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
</table>"""


def wrap_html(body_html):
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background-color:#f0f4f0;">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background-color:#f0f4f0;padding:32px 0;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0"
             style="max-width:620px;border-radius:8px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);">
        <tr><td>{header_block()}</td></tr>
        <tr>
          <td style="background:#ffffff;padding:40px 52px 48px 52px;
                     border-radius:0 0 8px 8px;
                     font-family:Georgia,serif;font-size:15px;
                     line-height:1.8;color:#1a1a1a;">
            {body_html}
            {FOOTER}
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


def build_message(cand, subject, body_html):
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_USER
    msg["To"]      = cand["email"]
    msg["CC"]      = ", ".join(CC)

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(wrap_html(body_html), "html", "utf-8"))
    msg.attach(alt)

    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            logo = MIMEImage(f.read())
        logo.add_header("Content-ID", "<taleemabad_logo>")
        logo.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
        msg.attach(logo)

    return msg


def main():
    print(f"\n{'='*60}")
    print(f"Job 36 New Batch — LIVE REJECTION SEND ({len(CANDIDATES)} candidates)")
    print(f"{'='*60}\n")

    results = {"sent": [], "failed": []}

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)

        for i, cand in enumerate(CANDIDATES, 1):
            name   = cand["name"]
            app_id = cand["app_id"]
            to     = cand["email"]
            print(f"[{i}/{len(CANDIDATES)}] {name} -> {to}...", end=" ", flush=True)

            subject, body_text = read_draft(app_id, name)
            if not body_text:
                print("SKIP — draft not found")
                results["failed"].append({"app_id": app_id, "name": name, "reason": "draft missing"})
                continue

            body_html = text_to_html(body_text)
            body_html += feedback_widget(name, ROLE, app_id, 'Application Feedback')
            msg = build_message(cand, subject, body_html)
            recipients = [to] + CC
            allow_candidate_addresses(recipients)

            try:
                safe_sendmail(
                    smtp_server=smtp,
                    sender=EMAIL_USER,
                    recipients=recipients,
                    message=msg.as_string(),
                    context=f"job36_rejection_live_new_batch_{app_id}"
                )
                results["sent"].append({"app_id": app_id, "name": name, "email": to})
                print("SENT")
            except Exception as e:
                print(f"FAILED: {e}")
                results["failed"].append({"app_id": app_id, "name": name, "reason": str(e)})

            time.sleep(1.5)  # avoid Gmail rate limits

    print(f"\n{'='*60}")
    print(f"DONE")
    print(f"  Sent:   {len(results['sent'])}")
    print(f"  Failed: {len(results['failed'])}")
    print(f"{'='*60}\n")

    if results["failed"]:
        print("FAILED:")
        for f in results["failed"]:
            print(f"  - {f['name']} ({f.get('reason', '')})")


if __name__ == "__main__":
    main()
