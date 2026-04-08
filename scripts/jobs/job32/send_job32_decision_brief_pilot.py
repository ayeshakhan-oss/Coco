"""
Job 32 — Fundraising & Partnerships Manager
"Final Candidates & Decision View" — PILOT (Ayesha + Jawwad)

Exact format: send_job36_decision_brief_pilot.py (approved April 2 2026).
CVs uploaded to Google Drive → shareable links injected into PDF via PyMuPDF.
Single PDF attachment only — no individual CV attachments.
"""

import os, sys, base64, io, smtplib, re
import fitz  # PyMuPDF
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build as gdrive_build
from googleapiclient.http import MediaFileUpload
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
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 PageBreak, HRFlowable, Table, TableStyle,
                                 KeepTogether)

from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

EMAIL_HOST     = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT     = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

CV_DIR      = "c:/Agent Coco/output/cvs_job32_pipeline/"
REPORT_PATH = "c:/Agent Coco/output/Job32_Decision_Brief.pdf"
PILOT_TO    = "ayesha.khan@taleemabad.com"
PILOT_CC    = "jawwad.ali@taleemabad.com"

LIVE_TO     = "sabeena.abbasi@taleemabad.com"
LIVE_CC     = ["haroon.yasin@taleemabad.com", "hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]

os.makedirs(CV_DIR, exist_ok=True)

# ── CANDIDATE DATA ─────────────────────────────────────────────────────────────
#
# ALL three candidates in Leading — all have completed GWC or have confirmed debrief.
# Mizhgan: HIRE (83%), debrief rescheduling — requested Fri 10 Apr, no slot confirmed yet
# Zain: HIRE (74%), debrief 7 Apr 11am confirmed
# Hamdan: GWC completed — panel decision pending

LEADING = [
    {
        "app_id": 1327, "name": "Mizhgan Kirmani", "score": "83%",
        "verdict": "HIRE",
        "debrief": "Rescheduling — requested 10 Apr",
        "tagline": "Strongest all-round submission. Donor-literate, practitioner-level cold room execution.",
        "signal": (
            "Best performance in this cohort across all five exercises. "
            "Pipeline prioritisation is specific and reasoned — deprioritisation calls are evidence-based, not gut feel. "
            "Cold room standout: she refuses the vague 'send me an email' brush-off and reframes to a targeted "
            "deliverable, a 2-pager specifically on how Taleemabad works with government at scale. "
            "That is a real practitioner technique. Re-engagement email is warm and forward-looking, "
            "leads with a genuine update (Punjab 6,000-school commitment) rather than a nudge. "
            "Funder brief adds an Insight layer before the solution: diagnoses why scale fails before "
            "positioning Taleemabad as the answer."
        ),
        "probe": (
            "E5 authenticity is the open question: track record framed as hypothetical, names a $350K "
            "Punjab schools result but no real funder or timeline. "
            "Probe: walk me through the last grant or partnership you personally led from identification "
            "to close. Name the funder, the amount, and the moment it almost fell apart."
        ),
    },
    {
        "app_id": 1333, "name": "Zain Ul Abideen", "score": "74%",
        "verdict": "HIRE",
        "debrief": "7 Apr, 11:00am — confirmed",
        "tagline": "Consistent, complete, technically sound. Sector transition from corporate IT is the open question.",
        "signal": (
            "Sound across all five exercises. Correctly identified Funder E as high-priority re-engagement: "
            "the prior objection (no government integration) has since been resolved by the Punjab "
            "6,000-school partnership — a specific, astute read requiring him to connect the funder's "
            "past objection to Taleemabad's current position. Cold room execution is structured; "
            "transitions are prepared rather than conversational. One credibility flag in E3: added prior "
            "relationship warmth that was not given information in the scenario — fabricating donor warmth "
            "in a real email is a real-world risk. Funder brief is metric-driven but reads as a product "
            "brochure with no tailored ask or amount."
        ),
        "probe": (
            "Sector transition is unresolved. His track record is a $10M Microsoft Enterprise Licence "
            "Agreement with a US Department of Corrections. What transfers: positioning, compliance "
            "navigation, deal structuring. What does not: funder psychology, bilateral cultivation cycles, "
            "grant stewardship. "
            "Probe: have you ever identified, cultivated, and closed a grant or partnership with a "
            "bilateral donor, foundation, or multilateral? If yes, walk me through it."
        ),
    },
    {
        "app_id": 1381, "name": "Hamdan Ahmad", "score": "52%",
        "verdict": "GWC DONE",
        "debrief": "GWC completed",
        "tagline": "Most analytically sophisticated submission in the cohort. GWC completed — decision pending panel read.",
        "signal": (
            "The case study showed the sharpest strategic instincts in this cohort. "
            "Only candidate to flag Funder F's three-week CSR decision window as a structural urgency "
            "signal — framing is commercially precise: position Rumi as a connectivity layer through the "
            "telco's own mobile infrastructure, name the CSR decision-maker, not the comms team. "
            "Re-engagement email is the best in the cohort: 'the ground has shifted considerably since "
            "we submitted it' — names specific milestones without overselling, offers a genuine exit, "
            "closes without pressure. Writing quality is noticeably above cohort average."
        ),
        "probe": (
            "GWC was the assessment point for cold room execution (E2) and track record (E5), "
            "both not submitted in the case study. "
            "Panel read on those two dimensions is the outstanding decision point before finalising."
        ),
    },
]

DISCUSSION = []   # All candidates have reached GWC/debrief stage

PIPELINE = [
    {"name": "Syed Arsalan Ashraf",  "status": "Values — FAIL (OUT) · 2 Apr · 3 pluses, 3 +/-, 0 minuses"},
    {"name": "Muhammad Adnan",       "status": "Values call completed — scorecard pending"},
    {"name": "Faheem Baig",          "status": "Values interview — 7 Apr · 11am–12pm · booked"},
    {"name": "Danish Hussain",       "status": "Values interview — 7 Apr · 2pm–3pm · booked"},
    {"name": "Shahzad Saleem Abbasi","status": "Values interview — 8 Apr · 2pm–3pm · booked"},
    {"name": "Huma Mumtaz",          "status": "Values interview — Today, 6 Apr · 2pm–3pm"},
]

CV_APP_IDS = {
    1327: "Mizhgan Kirmani",
    1333: "Zain Ul Abideen",
    1381: "Hamdan Ahmad",
}

# Pipeline candidate names — app_ids fetched dynamically by name from DB
PIPELINE_NAMES = [
    "Syed Arsalan Ashraf",
    "Muhammad Adnan",
    "Faheem Baig",
    "Danish Hussain",
    "Shahzad Saleem Abbasi",
    "Huma Mumtaz",
]


# ── HELPERS ────────────────────────────────────────────────────────────────────

def safe_fn(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


# ── STEP 1: FETCH CVs FROM DB ──────────────────────────────────────────────────

def fetch_cvs():
    """Fetch CVs for leading candidates (by app_id) and pipeline candidates (by name)."""
    print("Fetching CVs from DB...")
    conn = psycopg2.connect(
        host="ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
        dbname="neondb", user="neondb_owner",
        password="npg_kBQ10OASHEmd", sslmode="require"
    )
    cur = conn.cursor()

    # Leading candidates — fetch by app_id
    ids = list(CV_APP_IDS.keys())
    cur.execute("""
        SELECT a.id, c.first_name || ' ' || c.last_name AS full_name, c.resume_data
        FROM applications a JOIN candidates c ON a.candidate_id = c.id
        WHERE a.id = ANY(%s) AND c.resume_data IS NOT NULL
    """, (ids,))
    rows = cur.fetchall()

    # Pipeline candidates — fetch by name, job_id=32
    cur.execute("""
        SELECT a.id, c.first_name || ' ' || c.last_name AS full_name, c.resume_data
        FROM applications a JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = 32
          AND (c.first_name || ' ' || c.last_name) = ANY(%s)
          AND c.resume_data IS NOT NULL
    """, (PIPELINE_NAMES,))
    rows += cur.fetchall()

    cur.close(); conn.close()

    cv_paths = {}
    seen_names = {}
    for app_id, full_name, b64 in rows:
        name = CV_APP_IDS.get(app_id, full_name or str(app_id))
        if name in seen_names:
            continue
        seen_names[name] = True
        fname = f"{app_id}_{safe_fn(name)}_CV.pdf"
        path  = os.path.join(CV_DIR, fname)
        try:
            with open(path, "wb") as f:
                f.write(base64.b64decode(b64))
            cv_paths[app_id] = (path, fname, name)
            print(f"  Saved: {name}")
        except Exception as e:
            print(f"  FAILED {name}: {e}")
    return cv_paths


# ── STEP 2: UPLOAD CVs TO GOOGLE DRIVE ────────────────────────────────────────

def upload_cvs_to_drive(cv_paths):
    """Upload each CV to Drive, set anyone-can-view, return name -> URL dict."""
    creds = Credentials.from_authorized_user_file(
        "c:/Agent Coco/token_drive.json",
        scopes=["https://www.googleapis.com/auth/drive.file"])
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    service = gdrive_build("drive", "v3", credentials=creds)

    drive_links = {}
    for app_id, (cv_path, _, name) in cv_paths.items():
        if not os.path.exists(cv_path):
            print(f"  SKIP (not found): {name}")
            continue
        print(f"  Uploading: {name}...")
        meta  = {"name": f"{name} — CV (Job 32 Fundraising & Partnerships Manager).pdf"}
        media = MediaFileUpload(cv_path, mimetype="application/pdf")
        f     = service.files().create(body=meta, media_body=media, fields="id").execute()
        fid   = f["id"]
        service.permissions().create(
            fileId=fid, body={"type": "anyone", "role": "reader"}
        ).execute()
        drive_links[name] = f"https://drive.google.com/file/d/{fid}/view"
        print(f"    -> {drive_links[name]}")
    return drive_links


# ── COLOUR PALETTE ─────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#1a2a3a")
BLUE   = colors.HexColor("#1565c0")
GREEN  = colors.HexColor("#1a7a4a")
AMBER  = colors.HexColor("#c87800")
RED    = colors.HexColor("#c0392b")
PURPLE = colors.HexColor("#6a1b9a")
LGREY  = colors.HexColor("#f7f9fc")
MGREY  = colors.HexColor("#dfe6e9")
GREY   = colors.HexColor("#636e72")
WHITE  = colors.white
BLACK  = colors.HexColor("#1a1a1a")

VERDICT_COLOR = {
    "HIRE":     BLUE,
    "GWC DONE": PURPLE,
}


# ── STEP 3: BUILD PDF ──────────────────────────────────────────────────────────

def build_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             leftMargin=18*mm, rightMargin=18*mm,
                             topMargin=18*mm, bottomMargin=18*mm)
    SS = getSampleStyleSheet()

    T_COVER = ParagraphStyle("TCover", parent=SS["Normal"], fontSize=22,
                              textColor=NAVY, alignment=TA_CENTER,
                              fontName="Helvetica-Bold", spaceAfter=4)
    T_SUB   = ParagraphStyle("TSub",   parent=SS["Normal"], fontSize=11,
                              textColor=GREY, alignment=TA_CENTER, spaceAfter=3)
    T_WARN  = ParagraphStyle("TWarn",  parent=SS["Normal"], fontSize=9,
                              textColor=RED, alignment=TA_CENTER)
    T_SEC   = ParagraphStyle("TSec",   parent=SS["Normal"], fontSize=12,
                              textColor=BLUE, fontName="Helvetica-Bold",
                              spaceBefore=10, spaceAfter=5)
    T_BODY  = ParagraphStyle("TBody",  parent=SS["Normal"], fontSize=9.5,
                              leading=14, alignment=TA_JUSTIFY,
                              textColor=BLACK, spaceAfter=5)
    T_NOTE  = ParagraphStyle("TNote",  parent=SS["Normal"], fontSize=8.5,
                              textColor=GREY, alignment=TA_JUSTIFY,
                              leading=12, spaceAfter=4)
    T_CNAME = ParagraphStyle("TCName", parent=SS["Normal"], fontSize=11,
                              textColor=NAVY, fontName="Helvetica-Bold", spaceAfter=2)
    T_TAG   = ParagraphStyle("TTag",   parent=SS["Normal"], fontSize=9,
                              textColor=GREY, fontName="Helvetica-Oblique",
                              spaceAfter=5)
    T_PROBE = ParagraphStyle("TProbe", parent=SS["Normal"], fontSize=9,
                              textColor=colors.HexColor("#7b341e"),
                              leading=13, spaceAfter=0)

    def hr(color=MGREY, thick=0.5):
        return HRFlowable(width="100%", thickness=thick, color=color, spaceAfter=6)

    def candidate_block(c):
        vc = VERDICT_COLOR.get(c["verdict"], GREY)
        # Name: blue + underlined — PyMuPDF injects the Drive link over this text
        name_cell = Paragraph(
            f'<font color="#1565c0"><u><b>{c["name"]}</b></u></font>', T_CNAME)
        rows = [[
            name_cell,
            Paragraph(f'<font color="{vc.hexval()}"><b>{c["verdict"]}</b></font>', T_BODY),
            Paragraph(f'<i>{c["debrief"]}</i>', T_NOTE),
        ]]
        tbl = Table(rows, colWidths=[65*mm, 55*mm, 50*mm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), LGREY),
            ("TOPPADDING",    (0,0), (-1,-1), 7),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ("RIGHTPADDING",  (0,0), (-1,-1), 6),
            ("LINEBELOW",     (0,0), (-1,0),  0.8, vc),
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ]))
        items = [tbl]
        if c.get("tagline"):
            items.append(Spacer(1, 2*mm))
            items.append(Paragraph(c["tagline"], T_TAG))
        items.append(Paragraph(c["signal"], T_BODY))
        if c.get("probe"):
            items.append(Spacer(1, 1*mm))
            items.append(Paragraph(f'<b>At debrief, probe:</b> {c["probe"]}', T_PROBE))
        return KeepTogether(items + [Spacer(1, 5*mm)])

    story = []

    # ── COVER ──────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph("Final Candidates &amp; Decision View", T_COVER))
    story.append(Paragraph("Fundraising &amp; Partnerships Manager", T_SUB))
    story.append(Paragraph("Growth &amp; Partnerships Team · Taleemabad", T_SUB))
    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE, spaceAfter=6))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("6 April 2026 &nbsp;|&nbsp; PILOT — Ayesha &amp; Jawwad only", T_WARN))

    # ── WHERE WE ARE ───────────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Where We Are", T_SEC))
    story.append(hr())

    snap_data = [
        ["64 applications received", "10 shortlisted (15.6%)", "9 invited to values interview"],
        ["5 values calls completed",  "3 passed · 1 failed · 1 scorecard pending", "1 GWC completed"],
    ]
    snap_tbl = Table(snap_data, colWidths=[57*mm, 60*mm, 57*mm])
    snap_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LGREY),
        ("TEXTCOLOR",     (0,0), (-1,-1), NAVY),
        ("FONTNAME",      (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 10),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("GRID",          (0,0), (-1,-1), 0.5, MGREY),
    ]))
    story.append(snap_tbl)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "The pipeline produced three final-stage candidates from the case study. "
        "Five values calls have now been completed: the first batch of three all passed and went to case study. "
        "From the second batch, Syed Arsalan Ashraf did not clear values (OUT, 2 Apr). "
        "Muhammad Adnan's call is done and the scorecard is pending. "
        "Three further calls are confirmed this week: Faheem Baig (7 Apr, 11am), "
        "Danish Hussain (7 Apr, 2pm), and Shahzad Saleem Abbasi (8 Apr, 2pm). "
        "Huma Mumtaz's values call is today (6 Apr, 2pm). "
        "Hamdan Ahmad's GWC has been completed and a panel decision is pending. "
        "Zain's debrief is confirmed for 7 April. Mizhgan is rescheduling.",
        T_BODY
    ))

    # ── DEBRIEF SCHEDULE ───────────────────────────────────────────────────────
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Debrief Schedule", T_SEC))
    story.append(hr())

    sched_data = [
        ["Candidate",        "Date &amp; Time",   "Status",         "Notes"],
        ["Hamdan Ahmad",     "GWC completed",      "Done",           "Panel read pending — decision outstanding"],
        ["Zain Ul Abideen",  "7 Apr · 11:00am",   "7 Apr",          "Sabeena, Ayesha, Zain — confirmed"],
        ["Mizhgan Kirmani",  "TBC",                "Rescheduling",   "Requested Fri 10 Apr — no slot confirmed"],
    ]

    def sched_cell(cell, r, c_idx):
        if r == 0:
            return Paragraph(cell, ParagraphStyle("sc_hdr", parent=SS["Normal"],
                             fontSize=8.5, leading=12, textColor=BLUE,
                             fontName="Helvetica-Bold"))
        if c_idx == 0:
            return Paragraph(f'<u>{cell}</u>',
                             ParagraphStyle("sc_name", parent=SS["Normal"],
                             fontSize=8.5, leading=12, textColor=BLUE))
        return Paragraph(cell, ParagraphStyle("sc_cell", parent=SS["Normal"],
                         fontSize=8.5, leading=12, textColor=BLACK))

    s_tbl = Table(
        [[sched_cell(cell, r, c_idx) for c_idx, cell in enumerate(row)]
         for r, row in enumerate(sched_data)],
        colWidths=[48*mm, 32*mm, 28*mm, 62*mm]
    )
    row_bgs = [(0, WHITE)]
    for i in range(1, len(sched_data)):
        if "Done" in sched_data[i][2]:
            row_bgs.append((i, colors.HexColor("#ede7f6")))
        elif "Rescheduling" in sched_data[i][2]:
            row_bgs.append((i, colors.HexColor("#fff3e0")))
        else:
            row_bgs.append((i, WHITE if i % 2 == 0 else LGREY))
    s_style = [
        ("GRID",          (0,0), (-1,-1), 0.6, BLACK),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]
    for i, bg in row_bgs:
        s_style.append(("BACKGROUND", (0,i), (-1,i), bg))
    s_tbl.setStyle(TableStyle(s_style))
    story.append(s_tbl)

    # ── LEADING CANDIDATES ─────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Leading Candidates", T_SEC))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=6))
    story.append(Paragraph(
        "All three candidates cleared values and reached the final stage. "
        "Names are hyperlinked — click to open their CV. "
        "Scores shown are case study scores; debrief scorecards are yet to be completed "
        "for Mizhgan and Zain.",
        T_BODY
    ))
    story.append(Spacer(1, 4*mm))
    for c in LEADING:
        story.append(candidate_block(c))

    # ── ALSO IN PIPELINE ───────────────────────────────────────────────────────
    story.append(Paragraph("Also in Pipeline", T_SEC))
    story.append(hr(MGREY, 0.8))
    story.append(Paragraph(
        "Six candidates from the second values batch are tracked here. "
        "Syed Arsalan Ashraf did not clear values (2 Apr). Muhammad Adnan's call is done — scorecard pending. "
        "Three calls confirmed this week. Huma Mumtaz's call is today (6 Apr, 2pm). "
        "Names are hyperlinked — click to open their CV.",
        T_BODY
    ))
    story.append(Spacer(1, 3*mm))

    PH  = ParagraphStyle("ph",  parent=SS["Normal"], fontSize=8.5, textColor=BLUE,  fontName="Helvetica-Bold", leading=12)
    PN  = ParagraphStyle("pn",  parent=SS["Normal"], fontSize=8.5, textColor=BLUE,  fontName="Helvetica-Bold", leading=12)
    PS  = ParagraphStyle("ps",  parent=SS["Normal"], fontSize=8.5, textColor=BLACK, leading=13)

    pip_data = [
        [Paragraph("Candidate", PH), Paragraph("Status", PH)],
    ]
    for p in PIPELINE:
        # Blue + underline so PyMuPDF can inject the Drive link over the name
        name_para = Paragraph(f'<font color="#1565c0"><u><b>{p["name"]}</b></u></font>', PN)
        pip_data.append([name_para, Paragraph(p["status"], PS)])

    pip_tbl = Table(pip_data, colWidths=[62*mm, 108*mm])
    pip_style = [
        ("BACKGROUND",    (0,0), (-1,0),  colors.HexColor("#e8f0fb")),
        ("LINEBELOW",     (0,0), (-1,0),  1.0, BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("GRID",          (0,0), (-1,-1), 0.4, MGREY),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]
    for i in range(1, len(pip_data)):
        bg = LGREY if i % 2 == 1 else WHITE
        pip_style.append(("BACKGROUND", (0,i), (-1,i), bg))
    pip_tbl.setStyle(TableStyle(pip_style))
    story.append(pip_tbl)

    # ── NOTE: INTERNATIONAL OUTREACH ──────────────────────────────────────────
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("Note — International Pipeline", T_SEC))
    story.append(hr(MGREY, 0.8))
    story.append(Paragraph(
        "Also just to update everyone, on the international side, I am reaching out to people that I know. "
        "So far there are three potentials: "
        "Mark from Kenya — initially declined but is engaging in conversations and we are also talking about co-applying for certain grants. "
        "Priyanka (worked in JPAL — Harvard/Oxford grad) — she seems to be interested. Will line up call with her. "
        "Tomas from EIDU — he just resigned from EIDU so I have set up an exploratory call with him end of this month when he's back from his leave.",
        T_BODY
    ))

    # ── FOOTER ─────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 8*mm))
    story.append(hr())
    story.append(Paragraph(
        "Prepared by Coco — Taleemabad Talent Acquisition &nbsp;|&nbsp; "
        "hiring@taleemabad.com &nbsp;|&nbsp; 6 April 2026",
        ParagraphStyle("Foot", parent=SS["Normal"], fontSize=8,
                       textColor=GREY, alignment=TA_CENTER)
    ))

    doc.build(story)
    buf.seek(0)
    return buf.read()


# ── STEP 3b: BUILD HTML EMAIL BODY ────────────────────────────────────────────

def build_html_email(drive_links, pilot=False):
    """Build the full report as an inline HTML email. CV names are hyperlinked via drive_links."""

    def cv_link(name):
        url = drive_links.get(name)
        if url:
            return f'<a href="{url}" style="color:#1565c0;font-weight:bold;">{name}</a>'
        return f'<b>{name}</b>'

    # ── stat boxes ──────────────────────────────────────────────────────────
    stat_boxes = """
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0;">
      <tr>
        <td style="padding:14px 8px;background:#fce4ec;border-radius:6px;text-align:center;width:23%">
          <div style="font-size:22px;font-weight:bold;color:#c62828;">9</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">Total values calls</div>
        </td>
        <td width="7"></td>
        <td style="padding:14px 8px;background:#e3f0fb;border-radius:6px;text-align:center;width:23%">
          <div style="font-size:22px;font-weight:bold;color:#1565c0;">5</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">Values calls completed</div>
        </td>
        <td width="7"></td>
        <td style="padding:14px 8px;background:#e8f5e9;border-radius:6px;text-align:center;width:23%">
          <div style="font-size:22px;font-weight:bold;color:#1a7a4a;">2</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">HIRE-tier (case study)</div>
        </td>
        <td width="7"></td>
        <td style="padding:14px 8px;background:#ede7f6;border-radius:6px;text-align:center;width:23%">
          <div style="font-size:22px;font-weight:bold;color:#6a1b9a;">1</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">GWC completed</div>
        </td>
      </tr>
    </table>"""

    # ── where we are ────────────────────────────────────────────────────────
    where_we_are = """
    <p style="margin:0 0 10px;">
      The pipeline produced three final-stage candidates from the case study.
      Five values calls have now been completed: the first batch of three all passed and went to case study.
      From the second batch, Syed Arsalan Ashraf did not clear values (OUT, 2 Apr).
      Muhammad Adnan's call is done and the scorecard is pending.
      Three further calls are confirmed this week: Faheem Baig (7 Apr, 11am),
      Danish Hussain (7 Apr, 2pm), and Shahzad Saleem Abbasi (8 Apr, 2pm).
      Huma Mumtaz's values call is today (6 Apr, 2pm).
      Hamdan Ahmad's GWC has been completed and a panel decision is pending.
      Zain's debrief is confirmed for 7 April. Mizhgan is rescheduling.
    </p>"""

    # ── debrief schedule table ───────────────────────────────────────────────
    sched_rows = [
        ("Hamdan Ahmad",    "GWC completed",   "Done",         "Panel read pending — decision outstanding", "#ede7f6"),
        ("Zain Ul Abideen", "7 Apr · 11:00am", "Confirmed",    "Sabeena, Ayesha, Zain — confirmed",         "#f1f8e9"),
        ("Mizhgan Kirmani", "TBC",              "Rescheduling", "Requested Fri 10 Apr — no slot confirmed",  "#fff3e0"),
    ]
    sched_html = """
    <table width="100%" cellpadding="8" cellspacing="0"
           style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
      <tr style="background:#e8f0fb;">
        <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;width:24%">Candidate</td>
        <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;width:20%">Date &amp; Time</td>
        <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;width:16%">Status</td>
        <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;">Notes</td>
      </tr>"""
    for cname, date, status, notes, bg in sched_rows:
        sched_html += f"""
      <tr style="background:{bg};">
        <td style="border:1px solid #ddd;">{cv_link(cname)}</td>
        <td style="border:1px solid #ddd;">{date}</td>
        <td style="border:1px solid #ddd;">{status}</td>
        <td style="border:1px solid #ddd;">{notes}</td>
      </tr>"""
    sched_html += "\n    </table>"

    # ── leading candidate blocks ─────────────────────────────────────────────
    def verdict_color(v):
        return {"HIRE": "#1565c0", "GWC DONE": "#6a1b9a"}.get(v, "#636e72")

    def leading_block(c):
        vc = verdict_color(c["verdict"])
        return f"""
    <div style="background:#f7f9fc;border-left:4px solid {vc};
                padding:14px 16px;margin-bottom:14px;border-radius:0 6px 6px 0;">
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td style="font-size:14px;font-weight:bold;">{cv_link(c["name"])}</td>
          <td style="text-align:center;width:90px;">
            <span style="color:{vc};font-weight:bold;font-size:13px;">{c["verdict"]}</span>
          </td>
          <td style="text-align:right;width:160px;font-size:12px;color:#636e72;font-style:italic;">{c["debrief"]}</td>
        </tr>
      </table>
      <p style="margin:8px 0 4px;font-size:12px;color:#636e72;font-style:italic;">{c["tagline"]}</p>
      <p style="margin:0 0 8px;font-size:13px;line-height:1.6;">{c["signal"]}</p>
      <p style="margin:0;font-size:12px;color:#7b341e;line-height:1.6;">
        <b>At debrief, probe:</b> {c["probe"]}
      </p>
    </div>"""

    leading_html = "".join(leading_block(c) for c in LEADING)

    # ── pipeline table ────────────────────────────────────────────────────────
    pip_rows_html = ""
    for i, p in enumerate(PIPELINE):
        bg = "#f7f9fc" if i % 2 == 0 else "#ffffff"
        pip_rows_html += f"""
      <tr style="background:{bg};">
        <td style="border:1px solid #dfe6e9;padding:8px 10px;font-weight:bold;width:36%;">{cv_link(p["name"])}</td>
        <td style="border:1px solid #dfe6e9;padding:8px 10px;font-size:13px;">{p["status"]}</td>
      </tr>"""

    pipeline_html = f"""
    <table width="100%" cellpadding="0" cellspacing="0"
           style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
      <tr style="background:#e8f0fb;">
        <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;width:36%">Candidate</td>
        <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;">Status</td>
      </tr>{pip_rows_html}
    </table>"""

    # ── section heading helper ────────────────────────────────────────────────
    def sec(title):
        return (f'<p style="margin:24px 0 6px;font-size:14px;font-weight:bold;'
                f'color:#1565c0;border-bottom:1px solid #dfe6e9;padding-bottom:4px;">'
                f'{title}</p>')

    html = f"""\
<html>
<body style="font-family:Georgia,serif;font-size:14px;color:#1a1a1a;
             max-width:680px;margin:auto;background:#f0f4f0;padding:24px 0;">
<table width="680" cellpadding="0" cellspacing="0"
       style="background:#ffffff;border-radius:8px;
              box-shadow:0 2px 12px rgba(0,0,0,0.08);overflow:hidden;">

  <!-- HEADER -->
  <tr>
    <td style="background:#1a2a3a;padding:24px 32px;">
      <p style="margin:0;font-size:10px;color:#90a4ae;letter-spacing:2px;
                text-transform:uppercase;font-family:Georgia,serif;">
        People &amp; Culture &middot; Hiring Decision Brief
      </p>
      <p style="margin:8px 0 2px;font-size:20px;font-weight:bold;
                color:#ffffff;font-family:Georgia,serif;">
        Final Candidates &amp; Decision View
      </p>
      <p style="margin:0;font-size:13px;color:#90caf9;font-family:Georgia,serif;">
        Fundraising &amp; Partnerships Manager
      </p>
    </td>
  </tr>

  <!-- BODY -->
  <tr>
    <td style="padding:28px 32px;">

      <p style="margin:0 0 4px;">Hi Sabeena,</p>
      <p style="margin:0 0 16px;font-size:13px;color:#444;line-height:1.6;">
        Please find below the hiring decision brief for
        <strong>Fundraising &amp; Partnerships Manager</strong>.
        This covers where we are in the pipeline, the three final-stage candidates, and the values call schedule.
      </p>

      {stat_boxes}

      {sec("Where We Are")}
      {where_we_are}

      {sec("Debrief Schedule")}
      {sched_html}

      {sec("Leading Candidates")}
      <p style="margin:0 0 12px;font-size:13px;color:#444;line-height:1.6;">
        All three candidates cleared values and reached the final stage.
        Names are hyperlinked — click to open their CV.
        Scores shown are case study scores; debrief scorecards are yet to be completed
        for Mizhgan and Zain.
      </p>
      {leading_html}

      {sec("Also in Pipeline")}
      <p style="margin:0 0 12px;font-size:13px;color:#444;line-height:1.6;">
        Six candidates from the second values batch. Names are hyperlinked — click to open their CV.
      </p>
      {pipeline_html}

      {sec("Note — International Pipeline")}
      <p style="margin:0 0 20px;font-size:13px;line-height:1.7;">
        Also just to update everyone, on the international side, I am reaching out to people that I know.
        So far there are three potentials:
        <b>Mark from Kenya</b> — initially declined but is engaging in conversations and we are also talking
        about co-applying for certain grants.
        <b>Priyanka</b> (worked in JPAL — Harvard/Oxford grad) — she seems to be interested. Will line up call with her.
        <b>Tomas from EIDU</b> — he just resigned from EIDU so I have set up an exploratory call with him
        end of this month when he's back from his leave.
      </p>

    </td>
  </tr>

  <!-- FOOTER -->
  <tr>
    <td style="padding:12px 32px;background:#f5f5f5;font-size:11px;color:#888;
               font-family:Georgia,serif;">
      Taleemabad Talent Acquisition &nbsp;|&nbsp; hiring@taleemabad.com
      &nbsp;|&nbsp; 6 April 2026
    </td>
  </tr>

</table>
</body>
</html>"""
    return html


# ── MAIN ───────────────────────────────────────────────────────────────────────

def main():
    print("Step 1: Fetching CVs from DB...")
    cv_paths = fetch_cvs()
    print(f"CVs ready: {len(cv_paths)}")

    print("\nStep 2: Uploading CVs to Google Drive...")
    drive_links = upload_cvs_to_drive(cv_paths)
    print(f"Uploaded: {len(drive_links)} CVs")

    print("\nStep 3: Building HTML email...")
    html_body = build_html_email(drive_links)

    print("Step 4: Sending live email to Sabeena...")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Final Candidates & Decision View — Fundraising & Partnerships Manager"
    msg["From"]    = EMAIL_USER
    msg["To"]      = LIVE_TO
    msg["CC"]      = ", ".join(LIVE_CC)
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    recipients = [LIVE_TO] + LIVE_CC
    allow_candidate_addresses(recipients)

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.ehlo(); smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(smtp_server=smtp, sender=EMAIL_USER,
                      recipients=recipients, message=msg.as_string(),
                      context="job32_decision_brief_live")
    print(f"\nLive sent to: {LIVE_TO}")
    print(f"CC: {', '.join(LIVE_CC)}")


if __name__ == "__main__":
    main()
