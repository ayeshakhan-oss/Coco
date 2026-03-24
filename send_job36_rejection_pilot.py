"""
Send pilot email to Ayesha (TO) + Jawwad (CC) with all 161 Job 36 rejection
email drafts attached as a single PDF. Does NOT send to candidates.
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
                                 PageBreak, HRFlowable, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

load_dotenv()

EMAIL_HOST     = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT     = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

DRAFTS_DIR   = "c:/My First Agent/output/rejection_emails_job36/"
LOG_PATH     = os.path.join(DRAFTS_DIR, "_generation_log.json")
PILOT_TO     = "ayesha.khan@taleemabad.com"
PILOT_CC     = "jawwad.ali@taleemabad.com"
POSITION     = "Field Coordinator, Research & Impact Studies"


def load_log():
    with open(LOG_PATH, encoding="utf-8") as f:
        return json.load(f)


def strip_header(content):
    """Remove the PILOT header and category markers, return clean email text."""
    # Drop lines starting with *** or [CATEGORY or ===
    lines = content.splitlines()
    clean = []
    skip_next_blank = False
    for line in lines:
        if line.startswith("*** PILOT") or line.startswith("[CATEGORY") or line.startswith("=" * 10):
            skip_next_blank = True
            continue
        if skip_next_blank and line.strip() == "":
            skip_next_blank = False
            continue
        skip_next_blank = False
        clean.append(line)
    return "\n".join(clean).strip()


def is_flagged(content):
    return "[FLAG:" in content


def build_pdf(log):
    """Build a single PDF with all 161 email drafts."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm,
        title="Job 36 Rejection Email Drafts — PILOT"
    )

    styles = getSampleStyleSheet()
    GREEN  = colors.HexColor("#2e7a4f")
    AMBER  = colors.HexColor("#b45309")
    GREY   = colors.HexColor("#6b7280")
    LIGHT  = colors.HexColor("#f9fafb")

    title_style = ParagraphStyle("title", fontSize=18, fontName="Helvetica-Bold",
                                  textColor=GREEN, spaceAfter=4)
    sub_style   = ParagraphStyle("sub", fontSize=10, textColor=GREY, spaceAfter=12)
    h2_style    = ParagraphStyle("h2", fontSize=12, fontName="Helvetica-Bold",
                                  textColor=GREEN, spaceBefore=4, spaceAfter=2)
    flag_style  = ParagraphStyle("flag", fontSize=10, fontName="Helvetica-Bold",
                                  textColor=AMBER, spaceAfter=4)
    body_style  = ParagraphStyle("body", fontSize=9, leading=14, spaceAfter=4,
                                  fontName="Helvetica")
    meta_style  = ParagraphStyle("meta", fontSize=8, textColor=GREY, spaceAfter=2)

    story = []

    # ── Cover page ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("Job 36 — Rejection Email Drafts", title_style))
    story.append(Paragraph("Field Coordinator, Research &amp; Impact Studies", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=GREEN, spaceAfter=12))

    flagged = log.get("generic_flag", [])
    cover_data = [
        ["Total Drafts", "Personalised", "Generic / Flagged"],
        [str(log["total"]), str(log["ok"]), str(len(flagged))],
    ]
    cover_table = Table(cover_data, colWidths=[55*mm, 55*mm, 55*mm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), GREEN),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,0), 10),
        ("FONTNAME",   (0,1), (-1,1), "Helvetica-Bold"),
        ("FONTSIZE",   (0,1), (-1,1), 20),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,1), [LIGHT]),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#e5e7eb")),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 10*mm))

    # Flagged list on cover
    if flagged:
        story.append(Paragraph("Flagged emails — review before sending:", flag_style))
        flag_data = [["App ID", "Name", "Reason"]]
        for f in flagged:
            flag_data.append([str(f["app_id"]), f["name"], f["note"]])
        ft = Table(flag_data, colWidths=[20*mm, 55*mm, 90*mm])
        ft.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#fef3c7")),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",   (0,0), (-1,-1), 8),
            ("GRID",       (0,0), (-1,-1), 0.4, colors.HexColor("#e5e7eb")),
            ("TOPPADDING", (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ]))
        story.append(ft)

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(
        "PILOT — DO NOT FORWARD TO CANDIDATES. For review by Ayesha Khan and Jawwad Ali only.",
        ParagraphStyle("warn", fontSize=9, fontName="Helvetica-Bold",
                       textColor=AMBER, spaceAfter=4)
    ))
    story.append(Paragraph(
        "Coco — Taleemabad Talent Acquisition Agent  |  Confidential",
        ParagraphStyle("footer", fontSize=8, textColor=GREY)
    ))
    story.append(PageBreak())

    # ── One section per draft ─────────────────────────────────────────────────
    files = sorted(f for f in os.listdir(DRAFTS_DIR) if f.endswith(".txt"))
    for idx, fname in enumerate(files, 1):
        fpath = os.path.join(DRAFTS_DIR, fname)
        with open(fpath, encoding="utf-8") as f:
            raw = f.read()

        flagged_file = is_flagged(raw)
        content = strip_header(raw)

        # Parse app_id and name from filename: 1401_Name_Name.txt
        m = re.match(r"(\d+)_(.+)\.txt", fname)
        app_id = m.group(1) if m else "?"
        name   = m.group(2).replace("_", " ") if m else fname

        # Header
        header_text = f"[{idx}]  App {app_id} — {name}"
        if flagged_file:
            story.append(Paragraph(header_text + "  [FLAGGED — GENERIC]", flag_style))
        else:
            story.append(Paragraph(header_text, h2_style))

        story.append(HRFlowable(width="100%", thickness=0.5,
                                 color=AMBER if flagged_file else GREEN,
                                 spaceAfter=4))

        # Email content — escape XML chars, preserve line breaks
        for line in content.splitlines():
            line = line.strip()
            safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if safe == "":
                story.append(Spacer(1, 3))
            else:
                story.append(Paragraph(safe, body_style))

        story.append(PageBreak())

    doc.build(story)
    buf.seek(0)
    return buf.read()


def build_body_html(log):
    flagged = log.get("generic_flag", [])
    api_fail = log.get("api_fail", [])
    total    = log["total"]
    specific = log["ok"]

    flagged_rows = ""
    for f in flagged:
        flagged_rows += f"""
        <tr>
          <td style="padding:4px 8px;border-bottom:1px solid #eee;">{f['app_id']}</td>
          <td style="padding:4px 8px;border-bottom:1px solid #eee;">{f['name']}</td>
          <td style="padding:4px 8px;border-bottom:1px solid #eee;color:#b45309;">{f['note']}</td>
        </tr>"""

    fail_section = ""
    if api_fail:
        fail_section = f"""
        <p style="color:#dc2626;"><strong>⚠ API failures ({len(api_fail)}) — review manually:</strong><br>
        {', '.join(f['name'] for f in api_fail)}</p>"""

    return f"""
<html><body style="font-family:Arial,sans-serif;font-size:14px;color:#1a1a1a;max-width:700px;margin:0 auto;">

<div style="background:#2e7a4f;padding:20px 28px;border-radius:8px 8px 0 0;">
  <h1 style="color:#fff;margin:0;font-size:20px;">Job 36 — Rejection Email Drafts</h1>
  <p style="color:#d1fae5;margin:6px 0 0;font-size:13px;">{POSITION} · Pilot review — do not forward to candidates</p>
</div>

<div style="background:#f9fafb;padding:24px 28px;border:1px solid #e5e7eb;border-top:none;border-radius:0 0 8px 8px;">

  <p>Hi Ayesha,</p>

  <p>All rejection email drafts for Job 36 are ready for your review. Please find the full set attached as a ZIP file (<code>job36_rejection_drafts.zip</code>). Every file begins with <strong>"*** PILOT — DO NOT SEND YET ***"</strong> — nothing has been sent to candidates.</p>

  <table style="width:100%;border-collapse:collapse;margin:16px 0;">
    <tr>
      <td style="background:#2e7a4f;color:#fff;padding:12px 16px;border-radius:6px 0 0 6px;text-align:center;">
        <div style="font-size:28px;font-weight:700;">{total}</div>
        <div style="font-size:11px;margin-top:2px;">Total Drafts</div>
      </td>
      <td style="background:#1d4ed8;color:#fff;padding:12px 16px;text-align:center;">
        <div style="font-size:28px;font-weight:700;">{specific}</div>
        <div style="font-size:11px;margin-top:2px;">Personalised (AI)</div>
      </td>
      <td style="background:#b45309;color:#fff;padding:12px 16px;border-radius:0 6px 6px 0;text-align:center;">
        <div style="font-size:28px;font-weight:700;">{len(flagged)}</div>
        <div style="font-size:11px;margin-top:2px;">Generic / Flagged</div>
      </td>
    </tr>
  </table>

  <h3 style="color:#b45309;margin-bottom:6px;">⚑ Flagged emails — need your attention</h3>
  <p style="font-size:13px;color:#6b7280;margin-top:0;">These {len(flagged)} drafts used a generic template (no CV available or file issue). Review before sending.</p>
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <tr style="background:#fef3c7;">
      <th style="padding:6px 8px;text-align:left;">App ID</th>
      <th style="padding:6px 8px;text-align:left;">Name</th>
      <th style="padding:6px 8px;text-align:left;">Reason</th>
    </tr>
    {flagged_rows}
  </table>

  {fail_section}

  <h3 style="margin-top:24px;">How to use this</h3>
  <ol style="font-size:13px;line-height:1.8;">
    <li>Unzip <code>job36_rejection_drafts.zip</code></li>
    <li>Spot-check a sample of the specific emails (files marked <code>[CATEGORY: B]</code> or <code>[CATEGORY: C]</code>)</li>
    <li>Review all 10 flagged emails (marked <code>[FLAG: GENERIC]</code>) — decide if any need a custom note</li>
    <li>Reply with approval and I'll send all emails directly to candidates</li>
  </ol>

  <p style="font-size:13px;color:#6b7280;">File naming: <code>[APP_ID]_[Candidate_Name].txt</code> — each contains the subject line + full email body.</p>

  <hr style="border:none;border-top:1px solid #e5e7eb;margin:20px 0;">
  <p style="font-size:12px;color:#9ca3af;">
    Coco — Taleemabad Talent Acquisition Agent · Confidential<br>
    This pilot was sent to Ayesha Khan (TO) and Jawwad Ali (CC) only.
  </p>
</div>
</body></html>"""


def send_pilot():
    log = load_log()
    print("Building PDF (161 drafts)...", flush=True)
    pdf_bytes = build_pdf(log)
    print(f"PDF built: {len(pdf_bytes)//1024} KB", flush=True)
    html_body = build_body_html(log)

    # Update body text to mention PDF instead of ZIP
    html_body = html_body.replace(
        'attached as a ZIP file (<code>job36_rejection_drafts.zip</code>)',
        'attached as a single PDF (<code>job36_rejection_drafts.pdf</code>)'
    ).replace(
        '<li>Unzip <code>job36_rejection_drafts.zip</code></li>',
        '<li>Open <code>job36_rejection_drafts.pdf</code> — all drafts are in one file</li>'
    ).replace(
        'files marked <code>[CATEGORY: B]</code> or <code>[CATEGORY: C]</code>',
        'entries marked in green headers'
    )

    msg = MIMEMultipart("mixed")
    msg["From"]    = EMAIL_USER
    msg["To"]      = PILOT_TO
    msg["Cc"]      = PILOT_CC
    msg["Subject"] = f"[PILOT] Job 36 Rejection Drafts — {log['total']} emails ready for review"

    # HTML body
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html_body, "html"))
    msg.attach(alt)

    # PDF attachment
    part = MIMEBase("application", "pdf")
    part.set_payload(pdf_bytes)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", 'attachment; filename="job36_rejection_drafts.pdf"')
    msg.attach(part)

    recipients = [PILOT_TO, PILOT_CC]
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, recipients, msg.as_string())

    print(f"OK: Pilot email sent")
    print(f"  TO: {PILOT_TO}")
    print(f"  CC: {PILOT_CC}")
    print(f"  Attachment: job36_rejection_drafts.pdf ({len(pdf_bytes)//1024} KB)")
    print(f"  Total drafts: {log['total']} ({log['ok']} specific + {len(log['generic_flag'])} flagged)")


if __name__ == "__main__":
    send_pilot()
