"""
Job 36 — Field Coordinator, Research & Impact Studies
Pipeline Status Report — PILOT SEND (Ayesha + Jawwad only)

Steps:
1. Fetch CVs from DB for all pipeline candidates (values + KCD + GWC)
2. Save as PDF files to output/cvs_job36_pipeline/
3. Build pipeline report PDF with clickable CV hyperlinks
4. Send pilot email to Ayesha + Jawwad with report attached
"""

import os, sys, base64, json, smtplib, io, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import psycopg2
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 PageBreak, HRFlowable, Table, TableStyle,
                                 KeepTogether)

from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

# ── CONFIG ─────────────────────────────────────────────────────────────────────
EMAIL_HOST     = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT     = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DB_URL         = os.getenv("DATABASE_URL")

CV_OUT_DIR  = "c:/Agent Coco/output/cvs_job36_pipeline/"
REPORT_PATH = "c:/Agent Coco/output/Job36_Pipeline_Report.pdf"

PILOT_TO = "ayesha.khan@taleemabad.com"
PILOT_CC = "jawwad.ali@taleemabad.com"

os.makedirs(CV_OUT_DIR, exist_ok=True)

# ── PIPELINE DATA ──────────────────────────────────────────────────────────────

# 17 values invite candidates
VALUES_INVITED = [
    {"app_id": 1602, "name": "Asif Khan"},
    {"app_id": 1518, "name": "Zubair Hussain"},
    {"app_id": 1720, "name": "Jawad Khan"},
    {"app_id": 1658, "name": "Fatima Razzaq"},
    {"app_id": 1864, "name": "Fatima Mughal"},
    {"app_id": 1839, "name": "HabibunNabi"},
    {"app_id": 1700, "name": "Asad Farooq"},
    {"app_id": 1950, "name": "Jalal Ud Din"},
    {"app_id": 1513, "name": "Ali Zia"},
    {"app_id": 1442, "name": "Faryal Afridi"},
    {"app_id": 1755, "name": "Usman Ahmed Khan"},
    {"app_id": 1430, "name": "Scheherazade Noor"},
    {"app_id": 1591, "name": "Muhammad Junaid"},
    {"app_id": 1789, "name": "Muhammad Omer Khan"},
    {"app_id": 1624, "name": "Muhammad Siddique"},
    {"app_id": 1857, "name": "Amina Batool"},
    {"app_id": 1808, "name": "Mehwish"},
]

# Values rejected (feedback emails sent)
VALUES_REJECTED = ["Muhammad Omer Khan", "Faryal Afridi"]

# Case study sent
CASE_STUDY_SENT = [
    {"app_id": 1430, "name": "Scheherazade Noor"},
    {"app_id": 1950, "name": "Jalal Ud Din"},
    {"app_id": 1857, "name": "Amina Batool"},
    {"app_id": 2021, "name": "Maria Karim"},
    {"app_id": 1755, "name": "Usman Ahmed Khan"},
]

# GWC / Debrief scheduled
GWC_SCHEDULED = [
    {"app_id": 1903, "name": "Muhammad Abubakr"},
    {"app_id": 2018, "name": "Moiz Khan"},
    {"app_id": 2017, "name": "Shazmina"},
]

# All pipeline app_ids to fetch CVs for
ALL_PIPELINE = {c["app_id"]: c["name"] for c in
                VALUES_INVITED + CASE_STUDY_SENT + GWC_SCHEDULED +
                [{"app_id": 2021, "name": "Maria Karim"}]}


# ── STEP 1: FETCH AND SAVE CVs ─────────────────────────────────────────────────

def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


def fetch_and_save_cvs():
    print("Fetching CVs from DB...")
    conn = psycopg2.connect(
        host="ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
        dbname="neondb",
        user="neondb_owner",
        password="npg_kBQ10OASHEmd",
        sslmode="require"
    )
    cur  = conn.cursor()
    ids  = list(ALL_PIPELINE.keys())
    cur.execute("""
        SELECT a.id, c.first_name, c.last_name, c.resume_data
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.id = ANY(%s) AND c.resume_data IS NOT NULL
    """, (ids,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    cv_paths = {}
    for app_id, first, last, b64 in rows:
        name = ALL_PIPELINE.get(app_id, f"{first} {last}".strip())
        fname = f"{app_id}_{safe_filename(name)}.pdf"
        path  = os.path.join(CV_OUT_DIR, fname)
        try:
            pdf_bytes = base64.b64decode(b64)
            with open(path, "wb") as f:
                f.write(pdf_bytes)
            cv_paths[app_id] = path
            print(f"  Saved: {name}")
        except Exception as e:
            print(f"  FAILED {name}: {e}")
    return cv_paths


# ── STEP 2: BUILD REPORT PDF ───────────────────────────────────────────────────

BLUE   = colors.HexColor("#1565c0")
RED    = colors.HexColor("#c62828")
GREEN  = colors.HexColor("#2e7d32")
AMBER  = colors.HexColor("#e65100")
GREY   = colors.HexColor("#555555")
LGREY  = colors.HexColor("#f5f5f5")
WHITE  = colors.white
BLACK  = colors.HexColor("#1a1a1a")


def build_report(cv_paths):
    buf  = io.BytesIO()
    doc  = SimpleDocTemplate(buf, pagesize=A4,
                              leftMargin=20*mm, rightMargin=20*mm,
                              topMargin=20*mm, bottomMargin=20*mm)
    SS   = getSampleStyleSheet()

    cover_title = ParagraphStyle("CoverTitle", parent=SS["Heading1"],
                                  fontSize=22, textColor=BLUE,
                                  alignment=TA_CENTER, spaceAfter=6)
    cover_sub   = ParagraphStyle("CoverSub", parent=SS["Normal"],
                                  fontSize=12, textColor=GREY,
                                  alignment=TA_CENTER, spaceAfter=4)
    section_hd  = ParagraphStyle("SectionHd", parent=SS["Heading2"],
                                  fontSize=13, textColor=BLUE,
                                  spaceBefore=14, spaceAfter=6)
    body        = ParagraphStyle("Body", parent=SS["Normal"],
                                  fontSize=10, leading=15,
                                  alignment=TA_JUSTIFY, spaceAfter=6)
    note        = ParagraphStyle("Note", parent=SS["Normal"],
                                  fontSize=9, textColor=GREY,
                                  alignment=TA_JUSTIFY, spaceAfter=4)
    link_style  = ParagraphStyle("Link", parent=SS["Normal"],
                                  fontSize=10, leading=14,
                                  textColor=BLUE)

    def cv_link(app_id, name):
        path = cv_paths.get(app_id)
        if path:
            uri = "file:///" + path.replace("\\", "/").replace(" ", "%20")
            return Paragraph(f'<a href="{uri}" color="#1565c0"><u>{name}</u></a>', link_style)
        return Paragraph(name, link_style)

    def tbl(data, col_widths, row_colors=None):
        t = Table(data, colWidths=col_widths)
        style_cmds = [
            ("BACKGROUND",   (0, 0), (-1, 0),  BLUE),
            ("TEXTCOLOR",    (0, 0), (-1, 0),  WHITE),
            ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1, 0),  9),
            ("FONTSIZE",     (0, 1), (-1, -1), 9),
            ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LGREY]),
            ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
            ("TOPPADDING",   (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
            ("LEFTPADDING",  (0, 0), (-1, -1), 6),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ]
        if row_colors:
            for row_idx, bg in row_colors:
                style_cmds.append(("BACKGROUND", (0, row_idx), (-1, row_idx), bg))
        t.setStyle(TableStyle(style_cmds))
        return t

    story = []

    # ── COVER PAGE ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 35*mm))
    story.append(Paragraph("Job 36 — Pipeline Status Report", cover_title))
    story.append(Paragraph("Field Coordinator, Research &amp; Impact Studies", cover_sub))
    story.append(Paragraph("Impact &amp; Policy Team, Taleemabad", cover_sub))
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width="60%", thickness=1.5, color=BLUE,
                             hAlign="CENTER", spaceAfter=8))
    story.append(Paragraph("As of 2 April 2026", cover_sub))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(
        "PILOT PREVIEW — Internal review only. Not for distribution.",
        ParagraphStyle("Warn", parent=SS["Normal"], fontSize=10,
                       textColor=RED, alignment=TA_CENTER)
    ))

    # ── PIPELINE FUNNEL SUMMARY ─────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("1. Pipeline Funnel", section_hd))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BLUE, spaceAfter=8))

    funnel_data = [
        ["Stage", "Count", "Notes"],
        ["Total Applications Received",       "238", "Job open Feb–Mar 2026"],
        ["Shortlisted (moved to Values)",      "17",  "7.1% of applicants"],
        ["Rejected at CV Stage",               "216", "Includes LinkedIn temp accounts"],
        ["Pending / Unactioned",               "1",   "Rosheen Naeem — needs decision"],
        ["Values Interview Invites Sent",      "17",  "All shortlisted candidates"],
        ["Values Calls Conducted",             "TBC", "Confirm with hiring team"],
        ["Values Rejected (feedback sent)",    "2",   "Omer Khan, Faryal Afridi"],
        ["Case Study Sent",                    "5",   "See Section 4"],
        ["Case Study Submitted",               "TBC", "Gmail token needed to verify"],
        ["GWC / Debrief Scheduled",            "3",   "See Section 5"],
    ]
    story.append(tbl(funnel_data, [85*mm, 20*mm, 60*mm]))

    # ── REJECTION EMAIL STATUS ──────────────────────────────────────────────────
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph("2. Rejection Email Status", section_hd))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BLUE, spaceAfter=8))

    rej_data = [
        ["Batch", "Candidates", "Emails Sent", "Skipped", "Skip Reason"],
        ["Batch 1 (first round)",   "161", "146", "15",
         "10 no CV/unreadable · 5 duplicate emails"],
        ["Batch 2 (new, 2 Apr 2026)", "19",  "15",  "4",
         "LinkedIn temp accounts — no real email"],
        ["TOTAL",                   "180", "161", "19", ""],
        ["Remaining (not yet sent)", "~55", "0",   "—",
         "Not covered by either extraction run"],
    ]
    row_colors = [(4, colors.HexColor("#fff3e0"))]
    story.append(tbl(rej_data, [42*mm, 24*mm, 24*mm, 20*mm, 57*mm],
                     row_colors=row_colors))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Note: ~55 rejected candidates have not received a rejection email yet. "
        "These are candidates from earlier screening rounds whose CVs were not "
        "included in either extraction batch. A clean-up run can be done after "
        "this round closes.",
        note
    ))

    # ── VALUES INVITE CANDIDATES ────────────────────────────────────────────────
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("3. Values Interview — All 17 Invited Candidates", section_hd))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BLUE, spaceAfter=8))
    story.append(Paragraph(
        "Click a candidate name to open their CV. "
        "Links open locally — files saved at output/cvs_job36_pipeline/.",
        note
    ))
    story.append(Spacer(1, 3*mm))

    vi_data = [["#", "Candidate (click to open CV)", "Status", "Values Outcome"]]
    for i, c in enumerate(VALUES_INVITED, 1):
        name   = c["name"]
        app_id = c["app_id"]
        if name in VALUES_REJECTED:
            outcome = "Rejected — feedback sent"
            status  = "Rejected"
        elif name in [x["name"] for x in CASE_STUDY_SENT]:
            outcome = "Cleared — case study sent"
            status  = "Active"
        elif name in [x["name"] for x in GWC_SCHEDULED]:
            outcome = "Cleared — GWC scheduled"
            status  = "Active"
        else:
            outcome = "Pending / TBC"
            status  = "TBC"
        vi_data.append([str(i), cv_link(app_id, name), status, outcome])

    t = Table(vi_data, colWidths=[10*mm, 55*mm, 25*mm, 75*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  BLUE),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LGREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t)

    # ── CASE STUDY STAGE ───────────────────────────────────────────────────────
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("4. Case Study (KCD) Stage", section_hd))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BLUE, spaceAfter=8))

    cs_data = [["#", "Candidate (click to open CV)", "Email", "Submitted?"]]
    for i, c in enumerate(CASE_STUDY_SENT, 1):
        submitted = "TBC — Gmail token needed"
        if c["name"] in [x["name"] for x in GWC_SCHEDULED]:
            submitted = "Yes — debrief scheduled"
        cs_data.append([str(i), cv_link(c["app_id"], c["name"]),
                        "", submitted])

    t2 = Table(cs_data, colWidths=[10*mm, 55*mm, 60*mm, 42*mm])
    t2.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  BLUE),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LGREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t2)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Case study submission status (submitted / not submitted) cannot be "
        "confirmed until Gmail API token is regenerated. "
        "GWC-scheduled candidates have implicitly submitted.",
        note
    ))

    # ── GWC / DEBRIEF SCHEDULED ────────────────────────────────────────────────
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("5. GWC / Case Study Debrief — Scheduled", section_hd))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BLUE, spaceAfter=8))

    gwc_data = [["#", "Candidate (click to open CV)", "Email", "DB Status"]]
    for i, c in enumerate(GWC_SCHEDULED, 1):
        email = {1903: "muhammad.abubakr@niete.edu.pk",
                 2018: "amk.senzer@gmail.com",
                 2017: "shazminasharif9@gmail.com"}.get(c["app_id"], "")
        note_flag = " ⚑ NIETE" if c["app_id"] == 1903 else ""
        gwc_data.append([str(i), cv_link(c["app_id"], c["name"]),
                          email, f"gwc_scheduled{note_flag}"])

    t3 = Table(gwc_data, colWidths=[10*mm, 55*mm, 72*mm, 30*mm])
    t3.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  BLUE),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LGREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t3)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Note: Muhammad Abubakr (NIETE) — internal Taleemabad affiliate. "
        "Confirm whether standard external hiring process applies.",
        note
    ))

    # ── PENDING ACTIONS ────────────────────────────────────────────────────────
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("6. Pending Actions", section_hd))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BLUE, spaceAfter=8))

    pending_data = [
        ["#", "Action", "Owner", "Priority"],
        ["1", "Confirm how many values calls were conducted (exact count)",
         "Ayesha", "High"],
        ["2", "Confirm case study submission status (Scheherazade, Jalal, Amina, Maria, Usman)",
         "Ayesha", "High"],
        ["3", "Regenerate Gmail API token to enable automated submission check",
         "Ayesha (on machine)", "High"],
        ["4", "Decision on Rosheen Naeem (app 1921) — still in 'applied' status, unscreened",
         "Ayesha", "Medium"],
        ["5", "Send rejection emails to ~55 remaining rejected candidates not covered by batches 1 or 2",
         "Coco (after approval)", "Medium"],
        ["6", "Go/No-go decision on GWC candidates after debrief calls",
         "Muzzammil / Ayesha", "Active"],
    ]
    story.append(tbl(pending_data,
                     [8*mm, 80*mm, 40*mm, 22*mm]))

    # ── FOOTER NOTE ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 10*mm))
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor("#cccccc"), spaceAfter=6))
    story.append(Paragraph(
        "Report generated by Coco — Taleemabad Talent Acquisition Agent | "
        "hiring@taleemabad.com | 2 April 2026",
        ParagraphStyle("Footer", parent=SS["Normal"],
                       fontSize=8, textColor=GREY, alignment=TA_CENTER)
    ))

    doc.build(story)
    buf.seek(0)
    return buf.read()


# ── STEP 3: BUILD EMAIL AND SEND ───────────────────────────────────────────────

def build_body_html():
    return f"""
<html><body style="font-family:Arial,sans-serif;font-size:14px;color:#222;max-width:620px;margin:auto;">
<div style="background:#1565c0;padding:20px 24px;border-radius:6px 6px 0 0;">
  <h2 style="color:#fff;margin:0;">Job 36 — Pipeline Status Report</h2>
  <p style="color:#bbdefb;margin:4px 0 0;">Field Coordinator, Research &amp; Impact Studies</p>
</div>
<div style="padding:24px;background:#f9f9f9;border:1px solid #ddd;">
  <p>Hi Ayesha,</p>
  <p>Attached is the pilot pipeline status report for <strong>Field Coordinator, Research &amp; Impact Studies</strong>.</p>
  <table style="border-collapse:collapse;margin:16px 0;width:100%;">
    <tr>
      <td style="padding:10px 14px;background:#e3f2fd;border-radius:4px;text-align:center;">
        <strong style="font-size:22px;color:#1565c0;">238</strong><br>
        <span style="font-size:11px;color:#666;">Total Applied</span>
      </td>
      <td style="width:10px;"></td>
      <td style="padding:10px 14px;background:#e8f5e9;border-radius:4px;text-align:center;">
        <strong style="font-size:22px;color:#2e7d32;">17</strong><br>
        <span style="font-size:11px;color:#666;">Shortlisted</span>
      </td>
      <td style="width:10px;"></td>
      <td style="padding:10px 14px;background:#fce4ec;border-radius:4px;text-align:center;">
        <strong style="font-size:22px;color:#c62828;">216</strong><br>
        <span style="font-size:11px;color:#666;">Rejected</span>
      </td>
      <td style="width:10px;"></td>
      <td style="padding:10px 14px;background:#fff3e0;border-radius:4px;text-align:center;">
        <strong style="font-size:22px;color:#e65100;">3</strong><br>
        <span style="font-size:11px;color:#666;">GWC Scheduled</span>
      </td>
    </tr>
  </table>
  <p>The PDF includes clickable CV links for all pipeline candidates (values stage and above). Links open CV files locally.</p>
  <p style="color:#c62828;font-size:12px;">PILOT PREVIEW — Please review and confirm before this goes to Muzzammil.</p>
</div>
<div style="padding:12px 24px;background:#eee;font-size:11px;color:#666;">
  Taleemabad Talent Acquisition | hiring@taleemabad.com
</div>
</body></html>
"""


def main():
    # Step 1 — fetch and save CVs
    cv_paths = fetch_and_save_cvs()
    print(f"\nCVs saved: {len(cv_paths)}")

    # Step 2 — build PDF
    print("\nBuilding report PDF...")
    pdf_bytes = build_report(cv_paths)
    print(f"PDF built: {len(pdf_bytes):,} bytes")

    # Save locally too
    with open(REPORT_PATH, "wb") as f:
        f.write(pdf_bytes)
    print(f"Saved to: {REPORT_PATH}")

    # Step 3 — send pilot
    msg = MIMEMultipart("mixed")
    msg["Subject"] = "[PILOT] Job 36 Pipeline Status Report — Field Coordinator"
    msg["From"]    = EMAIL_USER
    msg["To"]      = PILOT_TO
    msg["CC"]      = PILOT_CC

    msg.attach(MIMEText(build_body_html(), "html", "utf-8"))

    pdf_part = MIMEBase("application", "pdf")
    pdf_part.set_payload(pdf_bytes)
    encoders.encode_base64(pdf_part)
    pdf_part.add_header("Content-Disposition", "attachment",
                         filename="Job36_Pipeline_Report.pdf")
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
            context="job36_pipeline_report_pilot"
        )
    print("Pilot sent.")


if __name__ == "__main__":
    main()
