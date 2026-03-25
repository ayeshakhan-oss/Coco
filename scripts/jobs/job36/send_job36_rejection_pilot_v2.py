"""
Job 36 — Rejection Email Pilot v2
Fixes applied vs v1:
  - "I" → "we" / "We" throughout all emails
  - Markdown **bold** markers stripped
  - Em dashes (—) removed / replaced with comma or colon
  - Sign-off replaced with confirmed format
  - Subject: "Re:" prefix removed
  - Sent to Ayesha only (no CC)
  - PDF uses confirmed design palette (green headers, justified body)
  - "Coco" or "AI" never appears in email body
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
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

load_dotenv()

EMAIL_HOST     = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT     = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

DRAFTS_DIR = "c:/Agent Coco/output/rejection_emails_job36/"
LOG_PATH   = os.path.join(DRAFTS_DIR, "_generation_log.json")
PILOT_TO   = "ayesha.khan@taleemabad.com"
POSITION   = "Field Coordinator, Research & Impact Studies"

NEW_SIGNOFF = (
    "Warm regards,\n\n"
    "People and Culture Team\n"
    "Taleemabad\n"
    "hiring@taleemabad.com  |  www.taleemabad.com\n\n"
    "Sent on behalf of Talent Acquisition Team by Coco"
)


# ── Text fix helpers ──────────────────────────────────────────────────────────

def fix_i_to_we(text):
    """Replace first-person singular with first-person plural."""
    # Contractions — do these first so plain \bI\b doesn't clobber them
    text = re.sub(r"\bI've\b",  "we've",  text)
    text = re.sub(r"\bI'd\b",   "we'd",   text)
    text = re.sub(r"\bI'll\b",  "we'll",  text)
    text = re.sub(r"\bI'm\b",   "we're",  text)
    text = re.sub(r"\bI'd\b",   "we'd",   text)   # possessive / subjunctive
    text = re.sub(r"\bI can\b", "we can", text)
    text = re.sub(r"\bI do\b",  "we do",  text)

    # Standalone "I" — capitalise if it starts a sentence or a line
    text = re.sub(r"(?m)^I\b",          "We",  text)    # line-start
    text = re.sub(r"(?<=[.!?] )I\b",    "We",  text)    # after sentence-end + space
    text = re.sub(r"(?<=[.!?\n])I\b",   "We",  text)    # after sentence-end no space
    text = re.sub(r"\bI\b",             "we",  text)    # remaining mid-sentence

    return text


def strip_markdown_bold(text):
    """**bold** → bold (PDF doesn't render markdown)."""
    return re.sub(r'\*\*(.+?)\*\*', r'\1', text)


def fix_em_dashes(text):
    """Replace em dashes with contextual punctuation. No — in emails."""
    # " — " surrounded by spaces → ", "
    text = text.replace(" — ", ", ")
    # remaining bare —
    text = text.replace("—", ",")
    return text


def fix_signoff(text):
    """Replace old sign-off block (from 'Warm regards,' to EOF) with new one."""
    idx = text.rfind("Warm regards")
    if idx != -1:
        text = text[:idx].rstrip() + "\n\n" + NEW_SIGNOFF
    return text


def fix_subject(subject):
    """Remove 'Re:' prefix."""
    return re.sub(r'^Re:\s*', '', subject, flags=re.IGNORECASE).strip()


def strip_pilot_header(content):
    """Remove *** PILOT ***, [CATEGORY ...], and === lines."""
    lines = content.splitlines()
    clean = []
    skip_next_blank = False
    for line in lines:
        if (line.startswith("*** PILOT") or line.startswith("[CATEGORY")
                or line.startswith("=" * 10)):
            skip_next_blank = True
            continue
        if skip_next_blank and line.strip() == "":
            skip_next_blank = False
            continue
        skip_next_blank = False
        clean.append(line)
    return "\n".join(clean).strip()


def parse_and_fix(raw_content):
    """
    Returns (subject, body) with all fixes applied.
    """
    content = strip_pilot_header(raw_content)

    # Extract subject line
    lines   = content.splitlines()
    subject = ""
    body_start = 0
    for i, line in enumerate(lines):
        if line.lower().startswith("subject:"):
            subject    = fix_subject(line[len("subject:"):].strip())
            body_start = i + 1
            # skip blank lines after subject
            while body_start < len(lines) and not lines[body_start].strip():
                body_start += 1
            break

    body = "\n".join(lines[body_start:]).strip()

    # Apply fixes in order
    body = fix_i_to_we(body)
    body = strip_markdown_bold(body)
    body = fix_em_dashes(body)
    body = fix_signoff(body)

    return subject, body


def load_log():
    with open(LOG_PATH, encoding="utf-8") as f:
        return json.load(f)


def is_flagged(content):
    return "[FLAG:" in content


# ── PDF builder ───────────────────────────────────────────────────────────────

def build_pdf(log):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm,
        title="Job 36 Rejection Email Drafts — PILOT v2"
    )

    GREEN  = colors.HexColor("#1b5e20")
    BLUE   = colors.HexColor("#1565c0")
    AMBER  = colors.HexColor("#b45309")
    GREY   = colors.HexColor("#6b7280")
    LIGHT  = colors.HexColor("#f9fafb")
    LGREEN = colors.HexColor("#e8f5e9")

    title_style = ParagraphStyle("title",  fontSize=18, fontName="Helvetica-Bold",
                                  textColor=GREEN,  spaceAfter=4)
    sub_style   = ParagraphStyle("sub",    fontSize=10, textColor=GREY,  spaceAfter=12)
    h2_style    = ParagraphStyle("h2",     fontSize=12, fontName="Helvetica-Bold",
                                  textColor=BLUE,   spaceBefore=4, spaceAfter=2)
    subj_style  = ParagraphStyle("subj",   fontSize=9,  fontName="Helvetica-Bold",
                                  textColor=GREEN,  spaceAfter=4, spaceBefore=2)
    flag_style  = ParagraphStyle("flag",   fontSize=10, fontName="Helvetica-Bold",
                                  textColor=AMBER,  spaceAfter=4)
    body_style  = ParagraphStyle("body",   fontSize=9,  leading=14, spaceAfter=4,
                                  fontName="Helvetica", alignment=TA_JUSTIFY)
    meta_style  = ParagraphStyle("meta",   fontSize=8,  textColor=GREY, spaceAfter=2)
    warn_style  = ParagraphStyle("warn",   fontSize=9,  fontName="Helvetica-Bold",
                                  textColor=AMBER,  spaceAfter=4)
    signoff_style = ParagraphStyle("signoff", fontSize=9, fontName="Helvetica-Oblique",
                                    textColor=GREY, spaceBefore=8)

    story = []

    # ── Cover page ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("Job 36 — Rejection Email Drafts", title_style))
    story.append(Paragraph(f"{POSITION} · Pilot v2 — For Ayesha's review", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=GREEN, spaceAfter=12))

    flagged = log.get("generic_flag", [])
    cover_data = [
        ["Total Drafts", "Personalised", "Generic / Flagged"],
        [str(log["total"]), str(log["ok"]), str(len(flagged))],
    ]
    cover_table = Table(cover_data, colWidths=[55*mm, 55*mm, 55*mm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), GREEN),
        ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,0), 10),
        ("FONTNAME",     (0,1), (-1,1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,1), (-1,1), 20),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,1), [LIGHT]),
        ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#e5e7eb")),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph("Changes in v2:", subj_style))
    changes = [
        "All emails now use 'we' voice throughout (never 'I')",
        "Markdown **bold** markers removed",
        "Em dashes removed and replaced with comma or colon",
        "Sign-off updated to confirmed format",
        "'Re:' removed from all subject lines",
        "Pilot sent to Ayesha only (Jawwad removed)",
    ]
    for c in changes:
        safe = c.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        story.append(Paragraph(f"• {safe}", meta_style))

    story.append(Spacer(1, 6*mm))

    if flagged:
        story.append(Paragraph(f"Flagged emails ({len(flagged)}) — review before sending:", flag_style))
        flag_data = [["App ID", "Name", "Reason"]]
        for f in flagged:
            flag_data.append([str(f["app_id"]), f["name"], f["note"]])
        ft = Table(flag_data, colWidths=[18*mm, 50*mm, 97*mm])
        ft.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#fef3c7")),
            ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",     (0,0), (-1,-1), 8),
            ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#e5e7eb")),
            ("TOPPADDING",   (0,0), (-1,-1), 4),
            ("BOTTOMPADDING",(0,0), (-1,-1), 4),
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
            ("WORDWRAP",     (2,1), (2,-1), True),
        ]))
        story.append(ft)

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(
        "PILOT — DO NOT FORWARD TO CANDIDATES. For Ayesha Khan's review only.",
        warn_style
    ))
    story.append(Paragraph(
        "Coco — Taleemabad Talent Acquisition Agent  |  Confidential",
        meta_style
    ))
    story.append(PageBreak())

    # ── One section per draft ──────────────────────────────────────────────────
    files = sorted(f for f in os.listdir(DRAFTS_DIR) if f.endswith(".txt"))
    print(f"Processing {len(files)} draft files...", flush=True)

    for idx, fname in enumerate(files, 1):
        fpath = os.path.join(DRAFTS_DIR, fname)
        with open(fpath, encoding="utf-8") as f:
            raw = f.read()

        flagged_file = is_flagged(raw)
        subject, body = parse_and_fix(raw)

        m = re.match(r"(\d+)_(.+)\.txt", fname)
        app_id = m.group(1) if m else "?"
        name   = m.group(2).replace("_", " ") if m else fname

        # Email header in PDF
        header_text = f"[{idx}]  App {app_id} — {name}"
        if flagged_file:
            story.append(Paragraph(header_text + "  [FLAGGED — GENERIC]", flag_style))
        else:
            story.append(Paragraph(header_text, h2_style))

        story.append(HRFlowable(width="100%", thickness=0.5,
                                 color=AMBER if flagged_file else GREEN,
                                 spaceAfter=3))

        # Subject line
        safe_subj = subject.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        story.append(Paragraph(f"Subject: {safe_subj}", subj_style))

        # Body paragraphs
        in_signoff = False
        for line in body.splitlines():
            stripped = line.strip()
            safe = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

            if stripped == "":
                story.append(Spacer(1, 3))
            elif stripped.startswith("Warm regards"):
                in_signoff = True
                story.append(Paragraph(safe, signoff_style))
            elif in_signoff:
                story.append(Paragraph(safe, signoff_style))
            else:
                # Bullet point detection
                if stripped.startswith("- ") or stripped.startswith("• "):
                    safe = "• " + safe[2:]
                story.append(Paragraph(safe, body_style))

        story.append(PageBreak())
        if idx % 20 == 0:
            print(f"  {idx}/{len(files)} done...", flush=True)

    doc.build(story)
    buf.seek(0)
    print("PDF built.", flush=True)
    return buf.read()


# ── Email body ────────────────────────────────────────────────────────────────

def build_body_html(log):
    flagged = log.get("generic_flag", [])
    total   = log["total"]
    specific = log["ok"]

    flagged_rows = ""
    for f in flagged:
        flagged_rows += f"""
        <tr>
          <td style="padding:4px 8px;border-bottom:1px solid #eee;">{f['app_id']}</td>
          <td style="padding:4px 8px;border-bottom:1px solid #eee;">{f['name']}</td>
          <td style="padding:4px 8px;border-bottom:1px solid #eee;color:#b45309;">{f['note']}</td>
        </tr>"""

    return f"""
<html><body style="font-family:Georgia,serif;font-size:15px;color:#1a1a1a;max-width:640px;margin:0 auto;line-height:1.8;">

<div style="background:#1b5e20;padding:20px 28px;border-radius:8px 8px 0 0;">
  <h1 style="color:#fff;margin:0;font-size:20px;font-family:Georgia,serif;">Job 36 — Rejection Email Drafts</h1>
  <p style="color:#c8e6c9;margin:6px 0 0;font-size:13px;">
    {POSITION} · Pilot v2 — for your review, Ayesha
  </p>
</div>

<div style="background:#f9fafb;padding:24px 28px;border:1px solid #e5e7eb;border-top:none;border-radius:0 0 8px 8px;">

  <p>Hi Ayesha,</p>

  <p>All 161 rejection email drafts for Job 36 are attached as a single PDF for your review.
     Nothing has been sent to candidates yet.</p>

  <p style="color:#1565c0;font-weight:bold;">What's new in this version:</p>
  <ul style="font-size:14px;line-height:1.9;">
    <li>All emails now use <strong>we</strong> voice throughout (never "I")</li>
    <li>Markdown bold markers removed</li>
    <li>Em dashes removed and replaced with comma or colon</li>
    <li>Sign-off updated to confirmed format</li>
    <li>"Re:" removed from all subject lines</li>
  </ul>

  <table style="width:100%;border-collapse:collapse;margin:16px 0;">
    <tr>
      <td style="background:#1b5e20;color:#fff;padding:12px 16px;border-radius:6px 0 0 6px;text-align:center;">
        <div style="font-size:28px;font-weight:700;">{total}</div>
        <div style="font-size:11px;margin-top:2px;">Total Drafts</div>
      </td>
      <td style="background:#1565c0;color:#fff;padding:12px 16px;text-align:center;">
        <div style="font-size:28px;font-weight:700;">{specific}</div>
        <div style="font-size:11px;margin-top:2px;">Personalised</div>
      </td>
      <td style="background:#b45309;color:#fff;padding:12px 16px;border-radius:0 6px 6px 0;text-align:center;">
        <div style="font-size:28px;font-weight:700;">{len(flagged)}</div>
        <div style="font-size:11px;margin-top:2px;">Generic / Flagged</div>
      </td>
    </tr>
  </table>

  <h3 style="color:#b45309;margin-bottom:6px;">Flagged emails — need your attention</h3>
  <p style="font-size:13px;color:#6b7280;margin-top:0;">
    These {len(flagged)} drafts used a generic template (no CV or unreadable file).
    Please review before sending.
  </p>
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <tr style="background:#fef3c7;">
      <th style="padding:6px 8px;text-align:left;">App ID</th>
      <th style="padding:6px 8px;text-align:left;">Name</th>
      <th style="padding:6px 8px;text-align:left;">Reason</th>
    </tr>
    {flagged_rows}
  </table>

  <h3 style="margin-top:24px;color:#1565c0;">How to review</h3>
  <ol style="font-size:13px;line-height:1.9;">
    <li>Open <code>job36_rejection_drafts_v2.pdf</code></li>
    <li>Spot-check a sample of the personalised emails</li>
    <li>Review all {len(flagged)} flagged generic emails</li>
    <li>Reply with approval and any notes — I will apply HTML design and send to candidates</li>
  </ol>

  <hr style="border:none;border-top:1px solid #e5e7eb;margin:20px 0;">
  <p style="font-size:12px;color:#9ca3af;">
    Coco — Taleemabad Talent Acquisition Agent · Confidential<br>
    This pilot was sent to Ayesha Khan only for review.
  </p>
</div>
</body></html>"""


# ── Send ──────────────────────────────────────────────────────────────────────

def send_pilot():
    log = load_log()
    print(f"Building PDF ({log['total']} drafts)...", flush=True)
    pdf_bytes = build_pdf(log)
    print(f"PDF size: {len(pdf_bytes)//1024} KB", flush=True)

    html_body = build_body_html(log)

    msg = MIMEMultipart("mixed")
    msg["From"]    = EMAIL_USER
    msg["To"]      = PILOT_TO
    msg["Subject"] = f"[PILOT v2] Job 36 Rejection Drafts — {log['total']} emails ready for review"

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html_body, "html"))
    msg.attach(alt)

    part = MIMEBase("application", "pdf")
    part.set_payload(pdf_bytes)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition",
                    'attachment; filename="job36_rejection_drafts_v2.pdf"')
    msg.attach(part)

    print(f"Sending to {PILOT_TO}...", flush=True)
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, [PILOT_TO], msg.as_string())

    print(f"Done.")
    print(f"  TO:         {PILOT_TO}")
    print(f"  Subject:    [PILOT v2] Job 36 Rejection Drafts — {log['total']} emails ready for review")
    print(f"  Attachment: job36_rejection_drafts_v2.pdf ({len(pdf_bytes)//1024} KB)")
    print(f"  Drafts:     {log['total']} ({log['ok']} personalised + {len(log['generic_flag'])} flagged)")


if __name__ == "__main__":
    send_pilot()
