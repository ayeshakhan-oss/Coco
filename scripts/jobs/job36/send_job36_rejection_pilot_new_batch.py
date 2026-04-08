"""
Send pilot of Job 36 new batch rejection emails to Ayesha (TO) + Jawwad (CC).
All 15 email drafts compiled into a single PDF attachment.
Does NOT send to candidates.
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

DRAFTS_DIR = "c:/Agent Coco/output/rejection_emails_job36_new_batch/"
PILOT_TO   = "ayesha.khan@taleemabad.com"
PILOT_CC   = "jawwad.ali@taleemabad.com"
POSITION   = "Field Coordinator, Research & Impact Studies"

CANDIDATES = [
    {"app_id": 2124, "name": "Hafiza Iqra Bashir"},
    {"app_id": 2122, "name": "Ali Haider Baloch"},
    {"app_id": 2119, "name": "Hassan Tahir"},
    {"app_id": 2108, "name": "Hiba Ahmed"},
    {"app_id": 2106, "name": "Faris Meher Ali"},
    {"app_id": 2105, "name": "Hamza Khan"},
    {"app_id": 2103, "name": "Attiqua Urfa"},
    {"app_id": 2090, "name": "Mehreen Tariq"},
    {"app_id": 2079, "name": "Umme Farwa"},
    {"app_id": 2061, "name": "Easha Imtiaz"},
    {"app_id": 2053, "name": "Hamza Sattar"},
    {"app_id": 2050, "name": "Anosha Umer"},
    {"app_id": 2029, "name": "Syed Muhammad Ali Abbas"},
    {"app_id": 2024, "name": "Mohid Naveed Sufi"},
    {"app_id": 2022, "name": "Maheen Sughra"},
]


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
        return None
    with open(path, encoding="utf-8") as f:
        return strip_header(f.read())


def build_pdf(drafts):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             leftMargin=20*mm, rightMargin=20*mm,
                             topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("Title", parent=styles["Heading1"],
                                  fontSize=16, textColor=colors.HexColor("#1565c0"),
                                  spaceAfter=6)
    meta_style  = ParagraphStyle("Meta", parent=styles["Normal"],
                                  fontSize=9, textColor=colors.grey, spaceAfter=12)
    body_style  = ParagraphStyle("Body", parent=styles["Normal"],
                                  fontSize=10, leading=15, spaceAfter=6,
                                  alignment=TA_JUSTIFY)
    cover_style = ParagraphStyle("Cover", parent=styles["Heading1"],
                                  fontSize=20, textColor=colors.HexColor("#1565c0"),
                                  alignment=TA_CENTER, spaceAfter=10)

    story = []

    # Cover page
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph("Job 36 Rejection Emails", cover_style))
    story.append(Paragraph("Field Coordinator, Research & Impact Studies", styles["Heading2"]))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(f"New Batch Pilot Preview", styles["Normal"]))
    story.append(Paragraph(f"Total candidates: {len(drafts)}", styles["Normal"]))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "PILOT REVIEW ONLY. These emails have NOT been sent to candidates. "
        "Please review all drafts and confirm before live send.",
        ParagraphStyle("Warning", parent=styles["Normal"],
                       textColor=colors.red, fontSize=10, leading=14)
    ))
    story.append(PageBreak())

    # Each email
    for i, (name, app_id, text) in enumerate(drafts, 1):
        story.append(Paragraph(f"{i}. {name}", title_style))
        story.append(Paragraph(f"App ID: {app_id}", meta_style))
        story.append(HRFlowable(width="100%", thickness=0.5,
                                 color=colors.HexColor("#1565c0"), spaceAfter=8))

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


def build_html_body(total):
    return f"""
<html><body style="font-family:Arial,sans-serif;font-size:14px;color:#222;max-width:600px;margin:auto;">
<div style="background:#1565c0;padding:20px 24px;border-radius:6px 6px 0 0;">
  <h2 style="color:#fff;margin:0;">Job 36 Rejection Emails</h2>
  <p style="color:#bbdefb;margin:4px 0 0;">Field Coordinator, Research and Impact Studies</p>
</div>
<div style="padding:24px;background:#f9f9f9;border:1px solid #ddd;">
  <p>Hi Ayesha,</p>
  <p>Attached is the pilot preview of the new batch rejection emails for <strong>{POSITION}</strong>.</p>
  <table style="border-collapse:collapse;margin:16px 0;">
    <tr>
      <td style="padding:8px 16px;background:#e3f2fd;border-radius:4px;text-align:center;">
        <strong style="font-size:22px;color:#1565c0;">{total}</strong><br>
        <span style="font-size:11px;color:#666;">Emails drafted</span>
      </td>
      <td style="width:16px;"></td>
      <td style="padding:8px 16px;background:#fff3e0;border-radius:4px;text-align:center;">
        <strong style="font-size:22px;color:#e65100;">4</strong><br>
        <span style="font-size:11px;color:#666;">Skipped (LinkedIn temp)</span>
      </td>
    </tr>
  </table>
  <p>Please review all drafts in the attached PDF and confirm when ready to go live.</p>
  <p style="color:#c62828;font-size:12px;">This is a pilot preview only. No emails have been sent to candidates yet.</p>
</div>
<div style="padding:12px 24px;background:#eee;font-size:11px;color:#666;">
  Taleemabad Talent Acquisition | hiring@taleemabad.com
</div>
</body></html>
"""


def main():
    print("\nReading drafts...")
    drafts = []
    for c in CANDIDATES:
        text = read_draft(c["app_id"], c["name"])
        if text:
            drafts.append((c["name"], c["app_id"], text))
            print(f"  OK: {c['name']}")
        else:
            print(f"  MISSING: {c['name']} (app {c['app_id']})")

    print(f"\nBuilding PDF ({len(drafts)} emails)...")
    pdf_bytes = build_pdf(drafts)
    print(f"PDF built: {len(pdf_bytes):,} bytes")

    # Build email
    msg = MIMEMultipart("mixed")
    msg["Subject"] = f"[PILOT] Job 36 Rejection Emails — New Batch ({len(drafts)} drafts)"
    msg["From"]    = EMAIL_USER
    msg["To"]      = PILOT_TO
    msg["CC"]      = PILOT_CC

    html_part = MIMEText(build_html_body(len(drafts)), "html", "utf-8")
    msg.attach(html_part)

    pdf_part = MIMEBase("application", "pdf")
    pdf_part.set_payload(pdf_bytes)
    encoders.encode_base64(pdf_part)
    pdf_part.add_header("Content-Disposition",
                         "attachment",
                         filename="Job36_Rejection_Emails_NewBatch_Pilot.pdf")
    msg.attach(pdf_part)

    recipients = [PILOT_TO, PILOT_CC]
    allow_candidate_addresses(recipients)

    print(f"\nSending pilot to {PILOT_TO} (CC: {PILOT_CC})...")
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(
            smtp_server=smtp,
            sender=EMAIL_USER,
            recipients=recipients,
            message=msg.as_string(),
            context="job36_rejection_pilot_new_batch"
        )
    print("Pilot sent successfully.")


if __name__ == "__main__":
    main()
