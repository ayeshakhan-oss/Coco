"""
Pilot: compile all Job 35 CV-stage rejection emails into a single PDF
and send to Ayesha for review.
No emails are sent to candidates until Ayesha approves.

Run after generate_rejection_emails_job35.py completes.
"""

import os, json, smtplib, io, re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 PageBreak, HRFlowable)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

EMAIL_HOST     = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT     = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

DRAFTS_DIR = "c:/Agent Coco/output/rejection_emails_job35/"
CV_DIR     = "c:/Agent Coco/output/cv_texts_job35_rejected/"
PILOT_TO   = "ayesha.khan@taleemabad.com"
PILOT_CC   = "jawwad.ali@taleemabad.com"
POSITION   = "Junior Research Associate, Impact & Policy"


def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


def strip_header(content):
    lines = content.splitlines()
    clean = []
    skip_next_blank = False
    for line in lines:
        if (line.startswith("*** PILOT") or line.startswith("TO:") or
                line.startswith("CC:") or line.startswith("=" * 10)):
            skip_next_blank = True
            continue
        if skip_next_blank and line.strip() == "":
            skip_next_blank = False
            continue
        skip_next_blank = False
        clean.append(line)
    return "\n".join(clean).strip()


def read_draft(app_id, name):
    fname = f"{app_id}_{safe_filename(name)}.txt"
    path = os.path.join(DRAFTS_DIR, fname)
    if not os.path.exists(path):
        for f in os.listdir(DRAFTS_DIR):
            if f.startswith(f"{app_id}_") and f.endswith(".txt"):
                path = os.path.join(DRAFTS_DIR, f)
                break
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return strip_header(f.read())


def build_pdf(drafts, total_candidates, skipped_count):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             leftMargin=20*mm, rightMargin=20*mm,
                             topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()

    title_style  = ParagraphStyle("Title", parent=styles["Heading1"],
                                   fontSize=15, textColor=colors.HexColor("#1565c0"),
                                   spaceAfter=4)
    meta_style   = ParagraphStyle("Meta", parent=styles["Normal"],
                                   fontSize=9, textColor=colors.grey, spaceAfter=10)
    body_style   = ParagraphStyle("Body", parent=styles["Normal"],
                                   fontSize=10, leading=15, spaceAfter=5,
                                   alignment=TA_JUSTIFY)
    cover_h1     = ParagraphStyle("CoverH1", parent=styles["Heading1"],
                                   fontSize=20, textColor=colors.HexColor("#1565c0"),
                                   alignment=TA_CENTER, spaceAfter=8)
    cover_h2     = ParagraphStyle("CoverH2", parent=styles["Heading2"],
                                   alignment=TA_CENTER, spaceAfter=6)
    warn_style   = ParagraphStyle("Warn", parent=styles["Normal"],
                                   textColor=colors.red, fontSize=10, leading=14)

    story = []

    # Cover page
    story.append(Spacer(1, 36*mm))
    story.append(Paragraph("Job 35 Rejection Emails", cover_h1))
    story.append(Paragraph(POSITION, cover_h2))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(f"Total CV-stage rejected: {total_candidates}", styles["Normal"]))
    story.append(Paragraph(f"Emails generated:        {len(drafts)}", styles["Normal"]))
    story.append(Paragraph(f"Skipped (unreadable CV): {skipped_count}", styles["Normal"]))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(
        "PILOT REVIEW ONLY. These emails have NOT been sent to candidates. "
        "Please review all drafts and reply to confirm when ready to go live.",
        warn_style
    ))
    story.append(PageBreak())

    # Each email
    for i, (name, app_id, email_addr, text) in enumerate(drafts, 1):
        story.append(Paragraph(f"{i}. {name}", title_style))
        story.append(Paragraph(f"App ID: {app_id}  |  To: {email_addr}", meta_style))
        story.append(HRFlowable(width="100%", thickness=0.5,
                                 color=colors.HexColor("#1565c0"), spaceAfter=6))

        for para in text.split("\n\n"):
            para = para.strip()
            if not para:
                continue
            safe = para.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe, body_style))
            story.append(Spacer(1, 2*mm))

        if i < len(drafts):
            story.append(PageBreak())

    doc.build(story)
    buf.seek(0)
    return buf.read()


def build_html_body(total_candidates, generated, skipped):
    return f"""
<html><body style="font-family:Arial,sans-serif;font-size:14px;color:#222;max-width:640px;margin:auto;">
<div style="background:#1565c0;padding:20px 24px;border-radius:6px 6px 0 0;">
  <h2 style="color:#fff;margin:0;">Job 35 Rejection Emails</h2>
  <p style="color:#bbdefb;margin:4px 0 0;">{POSITION}</p>
</div>
<div style="padding:24px;background:#f9f9f9;border:1px solid #ddd;">
  <p>Hi Ayesha,</p>
  <p>Attached is the full pilot preview of CV-stage rejection emails for <strong>{POSITION}</strong>.</p>
  <table style="border-collapse:collapse;margin:16px 0;">
    <tr>
      <td style="padding:10px 18px;background:#e3f2fd;border-radius:4px;text-align:center;margin-right:12px;">
        <strong style="font-size:24px;color:#1565c0;">{total_candidates}</strong><br>
        <span style="font-size:11px;color:#666;">Total rejected</span>
      </td>
      <td style="width:12px;"></td>
      <td style="padding:10px 18px;background:#e8f5e9;border-radius:4px;text-align:center;">
        <strong style="font-size:24px;color:#2e7d32;">{generated}</strong><br>
        <span style="font-size:11px;color:#666;">Emails generated</span>
      </td>
      <td style="width:12px;"></td>
      <td style="padding:10px 18px;background:#fff3e0;border-radius:4px;text-align:center;">
        <strong style="font-size:24px;color:#e65100;">{skipped}</strong><br>
        <span style="font-size:11px;color:#666;">Skipped (unreadable CV)</span>
      </td>
    </tr>
  </table>
  <p>Please review all drafts in the attached PDF. Once you are happy, just reply and I will send them live to candidates with CC to hiring@ and ayesha.khan@.</p>
  <p style="color:#c62828;font-size:12px;"><strong>Pilot only.</strong> No emails have been sent to candidates yet.</p>
</div>
<div style="padding:12px 24px;background:#eee;font-size:11px;color:#666;">
  Taleemabad Talent Acquisition | hiring@taleemabad.com
</div>
</body></html>
"""


def main():
    # Load generation log
    log_path = os.path.join(DRAFTS_DIR, "_generation_log.json")
    if not os.path.exists(log_path):
        print("ERROR: No generation log found. Run generate_rejection_emails_job35.py first.")
        return

    with open(log_path, encoding="utf-8") as f:
        log = json.load(f)

    # Load candidate emails from CV summary
    summary_path = os.path.join(CV_DIR, "_summary.json")
    email_map = {}
    if os.path.exists(summary_path):
        with open(summary_path, encoding="utf-8") as f:
            for c in json.load(f):
                email_map[c["app_id"]] = c.get("email", "")

    ok_candidates   = log.get("ok", [])
    skip_candidates = log.get("skipped", [])
    total_candidates = len(ok_candidates) + len(skip_candidates) + len(log.get("fail", []))

    print(f"\nReading {len(ok_candidates)} generated drafts...")
    drafts = []
    missing = []
    for c in ok_candidates:
        text = read_draft(c["app_id"], c["name"])
        if text:
            email_addr = email_map.get(c["app_id"], "")
            drafts.append((c["name"], c["app_id"], email_addr, text))
        else:
            missing.append(c["name"])

    if missing:
        print(f"  WARNING: {len(missing)} draft files not found: {missing[:5]}")

    print(f"  Loaded: {len(drafts)} drafts")
    print(f"\nBuilding PDF...")
    pdf_bytes = build_pdf(drafts, total_candidates, len(skip_candidates))
    print(f"PDF built: {len(pdf_bytes):,} bytes")

    # Build and send email
    msg = MIMEMultipart("mixed")
    msg["Subject"] = f"[PILOT] Job 35 Rejection Emails — {len(drafts)} drafts for review"
    msg["From"]    = EMAIL_USER
    msg["To"]      = PILOT_TO
    msg["CC"]      = PILOT_CC

    html_part = MIMEText(build_html_body(total_candidates, len(drafts), len(skip_candidates)), "html", "utf-8")
    msg.attach(html_part)

    pdf_part = MIMEBase("application", "pdf")
    pdf_part.set_payload(pdf_bytes)
    encoders.encode_base64(pdf_part)
    pdf_part.add_header("Content-Disposition", "attachment",
                         filename="Job35_Rejection_Emails_Pilot.pdf")
    msg.attach(pdf_part)

    recipients = [PILOT_TO, PILOT_CC]
    allow_candidate_addresses(recipients)

    print(f"\nSending pilot PDF to {PILOT_TO}...")
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(
            smtp_server=smtp,
            sender=EMAIL_USER,
            recipients=recipients,
            message=msg.as_string(),
            context="job35_rejection_pilot_all"
        )
    print(f"Done. Pilot sent with {len(drafts)}-email PDF attached.")


if __name__ == "__main__":
    main()
