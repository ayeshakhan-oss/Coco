"""
Job 35 — Junior Research Associate, Impact & Policy
CV-Stage Rejection Emails — LIVE SEND

Sends personalised rejection emails to all candidates whose drafts were generated.
PILOT_MODE = True  → sends to Ayesha only (with candidate name in subject prefix)
PILOT_MODE = False → sends to each candidate with CC to hiring@ + ayesha.khan@

Run ONLY after Ayesha has reviewed the PDF pilot and confirmed approval.
"""

import os, json, re, smtplib, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
from scripts.utils.feedback_widget import feedback_widget

PILOT_MODE = False  # Approved by Ayesha — 2026-04-07

# Candidates to exclude — active in other pipelines or user instruction
EXCLUDED_APP_IDS = {
    1417,  # Syeda Kainat — user instruction
    1753,  # Usman Ahmed Khan — Job 36 values PASS, shortlisted
    1729,  # Jawad Khan — Job 36 Field Coordinator, shortlisted
    1901,  # Mohammed Raiyaan Junaid Hamid — has offer on Hackathon 2026
    1870,  # Ayesha Raza Khan — shortlisted on Job 16
    1868,  # Ayesha Raza Khan (duplicate app)
    1423,  # AQSA GUL — applied Job 32
    1373,  # Alizay Babar — applied Job 17
    1675,  # Amina Jabin — applied Job 17
    1635,  # Anisa Shah — applied Job 17
    1446,  # Hisham Ijaz — applied Job 20
    1589,  # Hooria Huda — applied Job 17
    1522,  # Imama Tahir — applied Job 17
    1822,  # M Arslan Khalid — applied Job 37
    1881,  # Mahnoor — applied Job 17
    1565,  # Mahroosha Saleem — applied Job 17
    1759,  # Mahrukh Waqar — applied Job 13
    1787,  # Muhammad Ali Zafar — applied Job 32
    1829,  # Muhammad Burhan Hassan — applied Job 9
    1790,  # Muhammad Omer Khan — applied Job 36
    1748,  # Muhammad Usman Shabbir — applied Job 17
    1735,  # Muhammad Wasim khan — applied Job 17
    1399,  # Muhammad Zain Mobeen — applied Job 17
    1918,  # Nasir Hussain — applied Job 24
    1578,  # Rida Zanib — applied Job 17 / 20
    1409,  # Rida.e.fatima — applied Job 17
    1410,  # Rida.e.fatima (duplicate app)
    1838,  # Warda Ghafoor — applied Job 17
    1599,  # Zainab — applied Job 17 / 32
    1732,  # sumera adnan — applied Job 17
}

SENDER     = "ayesha.khan@taleemabad.com"
PASSWORD   = os.getenv("EMAIL_PASSWORD")
PILOT_TO   = "ayesha.khan@taleemabad.com"
CC_LIVE    = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]
ROLE       = "Junior Research Associate, Impact & Policy"
LOGO_PATH  = os.path.join(os.path.dirname(__file__), "../../..", "assets", "logo_taleemabad.png")

DRAFTS_DIR = "c:/Agent Coco/output/rejection_emails_job35/"
CV_DIR     = "c:/Agent Coco/output/cv_texts_job35_rejected/"


# ── HTML DESIGN (v8 universal theme) ─────────────────────────────────────────

H  = lambda t: f'<h2 style="color:#1565c0;font-size:17px;font-weight:bold;margin:36px 0 6px 0;letter-spacing:0.3px;">{t}</h2>'
P  = lambda t: f'<p style="margin:0 0 18px 0;text-align:justify;">{t}</p>'
PS = lambda t: f'<p style="margin:32px 0 0 0;padding:20px 24px;background:#f1f8e9;border-left:4px solid #1b5e20;font-style:italic;color:#2a2a2a;font-size:14px;line-height:1.7;">{t}</p>'

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


def header_block():
    return f"""
<table width="100%" cellpadding="0" cellspacing="0"
       style="border-radius:8px 8px 0 0;overflow:hidden;border-bottom:2px solid #1565c0;">
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
        Your Application for Junior Research Associate
      </p>
      <p style="margin:0;font-family:Georgia,serif;font-size:12px;color:#5c85c7;">
        {ROLE}
      </p>
    </td>
  </tr>
</table>"""


def wrap(body_html):
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
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


def strip_header(content):
    lines = content.splitlines()
    clean = []
    skip_next_blank = False
    for line in lines:
        if (line.startswith("*** PILOT") or line.startswith("TO:") or
                line.startswith("CC:") or line.startswith("Subject:") or
                line.startswith("=" * 10)):
            skip_next_blank = True
            continue
        if skip_next_blank and line.strip() == "":
            skip_next_blank = False
            continue
        skip_next_blank = False
        clean.append(line)
    return "\n".join(clean).strip()


def plain_to_html(plain_text, app_id, name):
    """Convert plain text email body to v8 HTML, detect section headers and PS."""
    paragraphs = [p.strip() for p in plain_text.split("\n\n") if p.strip()]
    html_parts = []
    for para in paragraphs:
        if para.startswith("P.S.") or para.startswith("P.S "):
            html_parts.append(PS(f"<strong>P.S.</strong> {para[4:].strip()}"))
        elif para.startswith("Warm regards,"):
            html_parts.append(FOOTER)
            html_parts.append(feedback_widget(name, ROLE, app_id, "Application Feedback"))
        elif len(para) < 80 and para.endswith((":", "?")):
            html_parts.append(H(para.rstrip(":")))
        elif para.isupper() or (len(para) < 80 and not para.endswith(".")):
            # Likely a section header
            html_parts.append(H(para))
        else:
            # Convert single newlines within a paragraph to spaces
            clean = " ".join(para.splitlines())
            html_parts.append(P(clean))
    return wrap("".join(html_parts))


def read_draft(app_id, name):
    fname = f"{app_id}_{safe_filename(name)}.txt"
    path = os.path.join(DRAFTS_DIR, fname)
    if not os.path.exists(path):
        for fn in os.listdir(DRAFTS_DIR):
            if fn.startswith(f"{app_id}_") and fn.endswith(".txt"):
                path = os.path.join(DRAFTS_DIR, fn)
                break
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return strip_header(f.read())


def send_email(to_email, to_name, app_id, html_body, cc_list=None):
    msg = MIMEMultipart("related")
    msg["From"]    = SENDER
    msg["To"]      = to_email
    msg["Subject"] = f"Your Application for {ROLE}"
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(alt)

    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", "<taleemabad_logo>")
        img.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
        msg.attach(img)

    recipients = [to_email] + (cc_list or [])
    for attempt in range(5):
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.login(SENDER, PASSWORD)
                allow_candidate_addresses(recipients)
                safe_sendmail(server, SENDER, recipients, msg.as_string(),
                              context=f"job35_cv_rejection_{'pilot' if PILOT_MODE else 'live'}_{to_name.replace(' ','_')}")
            cc_str = f" (CC: {', '.join(cc_list)})" if cc_list else ""
            print(f"  Sent: {to_name} -> {to_email}{cc_str}")
            return
        except Exception as e:
            wait = 30 * (attempt + 1)
            print(f"  RETRY ({attempt+1}/5) {to_name}: {e} — waiting {wait}s")
            time.sleep(wait)
    print(f"  FAILED after 5 attempts: {to_name}")


def main():
    log_path = os.path.join(DRAFTS_DIR, "_generation_log.json")
    if not os.path.exists(log_path):
        print("ERROR: No generation log. Run generate_rejection_emails_job35.py first.")
        return

    with open(log_path, encoding="utf-8") as f:
        log = json.load(f)

    # Load emails from CV summary
    summary_path = os.path.join(CV_DIR, "_summary.json")
    email_map = {}
    if os.path.exists(summary_path):
        with open(summary_path, encoding="utf-8") as f:
            for c in json.load(f):
                email_map[c["app_id"]] = c.get("email", "")

    candidates = log.get("ok", [])

    # Load already-sent names from audit log to avoid double-sending
    already_sent = set()
    audit_log = os.path.join(os.path.dirname(__file__), "../../..", "logs", "email_audit.log")
    if os.path.exists(audit_log):
        with open(audit_log, encoding="utf-8") as f:
            for line in f:
                if "job35_cv_rejection_live_" in line and "SENT" in line:
                    # extract name from context=job35_cv_rejection_live_First_Last
                    import re as _re
                    m = _re.search(r"job35_cv_rejection_live_(.+?) \|", line)
                    if m:
                        already_sent.add(m.group(1))

    print("=" * 60)
    print(f"Job 35 — {ROLE} | CV Rejection")
    print(f"Mode: {'PILOT (Ayesha only)' if PILOT_MODE else 'LIVE'}")
    print(f"Candidates: {len(candidates)}")
    print("=" * 60)

    sent = 0
    skipped = 0

    for c in candidates:
        app_id = c["app_id"]
        name   = c["name"]
        email  = email_map.get(app_id, "")

        name_key = name.replace(' ', '_')
        if name_key in already_sent:
            print(f"  SKIP: {name} — already sent")
            skipped += 1
            continue

        if app_id in EXCLUDED_APP_IDS:
            print(f"  SKIP: {name} — excluded (active in other pipeline)")
            skipped += 1
            continue

        if not email:
            print(f"  SKIP: {name} — no email found")
            skipped += 1
            continue

        draft_text = read_draft(app_id, name)
        if not draft_text:
            print(f"  SKIP: {name} — draft not found")
            skipped += 1
            continue

        html_body = plain_to_html(draft_text, app_id, name)

        if PILOT_MODE:
            send_email(PILOT_TO, name,
                       app_id, html_body)
        else:
            send_email(email, name, app_id, html_body, cc_list=CC_LIVE)
        sent += 1
        time.sleep(1.5)

    print(f"\nDone. {sent} emails {'piloted' if PILOT_MODE else 'sent live'}. {skipped} skipped.")
    print("=" * 60)


if __name__ == "__main__":
    main()
