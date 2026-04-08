"""
Job 36 — Field Coordinator, Research & Impact Studies
"Final Candidates & Decision View" — PILOT (Ayesha + Jawwad)

Complete rebuild. Decision-framed, judgment-led, no TBC noise.
CVs attached as individual PDF files — no broken file:// links.
"""

import os, sys, base64, io, smtplib, re
import fitz  # PyMuPDF
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build as gdrive_build
from googleapiclient.http import MediaFileUpload
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import psycopg2
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 PageBreak, HRFlowable, Table, TableStyle,
                                 KeepTogether)

from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

EMAIL_HOST     = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT     = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

CV_DIR      = "c:/Agent Coco/output/cvs_job36_pipeline/"
REPORT_PATH = "c:/Agent Coco/output/Job36_Decision_Brief.pdf"
PILOT_TO    = "ayesha.khan@taleemabad.com"
PILOT_CC    = "jawwad.ali@taleemabad.com"

os.makedirs(CV_DIR, exist_ok=True)


# ── CANDIDATE DATA (from Case Study v5 evaluation + debrief calendar) ────────────────
#
# Grouping:
#   LEADING    — HIRE or STRONG HIRE, strong signal across values + case study
#   DISCUSSION — CONDITIONAL or BORDERLINE, mixed signals, needs alignment
#
# Debrief schedule (from Google Calendar):
#   Done    : Moiz Khan (24 Mar), Shazmina (25 Mar), Muhammad Abubakr (19 Mar)
#   Today   : Scheherazade Noor (2 Apr, 1pm)
#   Upcoming: Asad Farooq (3 Apr), Maria Karim (6 Apr), Amina Batool (7 Apr),
#             Jalal Ud Din (8 Apr), Usman Ahmed Khan (9 Apr)
#   Pending : Rosheen Naeem (case study just sent 1 Apr — not yet at debrief)

LEADING = [
    {
        "app_id": 1430, "name": "Scheherazade Noor", "score": "100%",
        "verdict": "STRONG HIRE",
        "debrief": "Today — 2 Apr, 1:00pm",
        "tagline": "Field-native thinker. Only candidate who read the study design correctly.",
        "signal": (
            "Strongest submission in the batch by a clear margin. Investigates before acting — "
            "her instinct on seeing clean-looking data was to flag it as suspicious before contacting "
            "the firm. Built a 48-hr action plan with explicit reasoning per time block. Only candidate "
            "who put a Treatment/Control column in her tracker, correctly reading this as an RCT. "
            "Government coordination framed as a relationship problem, not a scheduling problem. "
            "Consent escalation documented in-tracker to Research Lead."
        ),
        "probe": "How she makes decisions when the monitoring dashboard is delayed or incomplete.",
    },
    {
        "app_id": 2021, "name": "Maria Karim", "score": "84%",
        "verdict": "HIRE",
        "debrief": "6 Apr, 11:00am",
        "tagline": "Sharpest on research validity. Best articulation of why the sampling breach matters.",
        "signal": (
            "Conceptual clarity is her standout. Produced the most precise sampling statement in the "
            "batch — named the unauthorised substitution as something that 'undermines the ability of "
            "the study to draw any valid inference.' Her 7-sheet tracker includes a dedicated Substitution "
            "sheet labelled 'Sampling Violation' — unique across all submissions. "
            "Daily progress dashboard with time-flagging formula. DEO/AEO path correctly identified."
        ),
        "probe": "When does she escalate to the Research Lead vs. handle independently? Her submission doesn't show that boundary clearly.",
    },
    {
        "app_id": 2018, "name": "Moiz Khan", "score": "83%",
        "verdict": "HIRE",
        "debrief": "Done — 24 Mar",
        "tagline": "Strongest tracker in the batch. Systems thinking translates directly into field architecture.",
        "signal": (
            "Most operationally comprehensive tracker submitted — pre-built for the study's specific risks, "
            "formula-driven flags, dedicated sheets for enumerator compliance and school substitution. "
            "Solid across all criteria: correctly identifies the sampling breach as a validity threat, "
            "maps the DEO/AEO escalation path. Where he does not reach the top tier: "
            "responses are competent but lack the diagnostic depth of Scheherazade — he lists right steps "
            "without showing how he diagnosed the problem first."
        ),
        "probe": "Can he think out loud through an ambiguous field scenario, not just name the correct procedure?",
    },
    {
        "app_id": 1857, "name": "Amina Batool", "score": "76%",
        "verdict": "HIRE",
        "debrief": "7 Apr, 2:30pm",
        "tagline": "Practically grounded. Genuine Pakistan bureaucracy instinct.",
        "signal": (
            "Calculated expected study pace correctly (6 schools/day, 6 enumerator pairs) — clean signal "
            "she read the parameters. 'Follow up from desk to desk, best done in-person' is rare, genuine "
            "field intuition. Presented three concrete catch-up options with trade-offs for the Research Lead. "
            "Tracker includes School Replacement and Consent as dedicated columns. "
            "Gap: does not flag consent-compromised data to the Research Lead — a research ethics gap."
        ),
        "probe": "Does she make a recommendation or present a menu? Probe ownership vs. deference on hard calls.",
    },
    {
        "app_id": 2017, "name": "Shazmina", "score": "73%",
        "verdict": "HIRE",
        "debrief": "Done — 25 Mar",
        "tagline": "Field-competent and operationally reliable. Research integrity framing needs sharpening.",
        "signal": (
            "Genuine field instinct: risk identification is practical and grounded in what actually breaks "
            "during data collection in Pakistan — enumerator incentive drift, access friction, timeline "
            "slippage from approvals. Operational response is well-sequenced, DEO/AEO path correctly mapped. "
            "Gap: sampling breach framing stays at the process level ('the school should have been approved') "
            "without reaching the validity-level consequence. Tracker functional but flags are manual, not formula-driven."
        ),
        "probe": "Both gaps are coachable, not disqualifying. GWC done — awaiting hiring manager read.",
    },
    {
        "app_id": 1755, "name": "Usman Ahmed Khan", "score": "71% (prov.)",
        "verdict": "HIRE (Prov.)",
        "debrief": "9 Apr, 12:00pm",
        "tagline": "Second strongest written submission. Score provisional — tracker file not yet received.",
        "signal": (
            "Written analysis is strong: cross-references high-output enumerators against fast-completion "
            "schools as a connected signal. Names the sampling breach as a 'major protocol breach' with "
            "validity consequences. Stops the session immediately on consent breach and flags to Research Lead. "
            "Score is provisional at 71% across 4 of 5 criteria — tracker file exists on Markaz but "
            "was not accessible via the hiring inbox. Full score pending tracker review."
        ),
        "probe": "In Scenario 3, does not distinguish who should make the government outreach call. Taleemabad contacts government directly — not the survey firm. Subtle but important relationship boundary.",
    },
]

DISCUSSION = [
    {
        "app_id": 1700, "name": "Asad Farooq", "score": "66%",
        "verdict": "CONDITIONAL",
        "debrief": "3 Apr, 10:30am",
        "signal": (
            "Technically correct across all criteria. Government coordination standout — correctly names "
            "MoFEPT as leverage point, proposes a personal visit to the DEO. "
            "Where he falls short: 'empathetic engagement' framing softens urgency when data integrity is at risk. "
            "Proposed pausing all fieldwork for refresher training when team is 40% behind — "
            "an operational misjudgment. Right call is targeted retraining, not a full stop."
        ),
        "probe": "Does the empathetic lens reflect genuine field leadership or a tendency to soften accountability? Decision threshold: needs to show investigative depth at debrief.",
    },
    {
        "app_id": 1950, "name": "Jalal Ud Din", "score": "60%",
        "verdict": "CONDITIONAL",
        "debrief": "8 Apr, 10:30am",
        "signal": (
            "Most notable internal inconsistency in the batch: his tracker (6 sheets, Supervisor Observation "
            "compliance checks, 'Sampling Integrity Affected?' column) is structurally strong — "
            "his written analysis is the weakest. Suggests personally assessing students to 'evaluate' them — "
            "a Field Coordinator does not administer the assessment tool. "
            "Tracker/analysis gap of this magnitude raises integrity concerns: one of the two was likely assisted."
        ),
        "probe": "Probe explicitly whether the tracker was independently designed. Can he articulate root causes verbally when he cannot write them out?",
    },
    {
        "app_id": 1903, "name": "Muhammad Abubakr", "score": "60%",
        "verdict": "CONDITIONAL",
        "debrief": "Done — 19 Mar",
        "signal": (
            "Uniformly competent: addresses each scenario correctly, identifies the right escalation path. "
            "What is absent is depth — risk identification stops at the surface without forming a hypothesis. "
            "Government coordination is procedurally accurate but generic — no Pakistan-specific instinct. "
            "In a batch with four candidates scoring HIRE, he does not differentiate above the conditional threshold. "
            "Note: NIETE-affiliated (muhammad.abubakr@niete.edu.pk) — confirm whether standard process applies."
        ),
        "probe": "GWC done. Awaiting hiring manager's read. Would need to show significantly stronger independent judgment to justify advancement over the HIRE-tier candidates.",
    },
    {
        "app_id": 1430, "name": "Zubair Hussain", "score": "42%",
        "verdict": "BORDERLINE",
        "debrief": "Not scheduled",
        "signal": (
            "Field operations experience visible — correctly identifies top-down government coordination "
            "path, names TEO as relevant contact, references MoU/NoC documentation. "
            "Two foundational misreads prevent advancement: (1) on enumerator paraphrasing, wrote "
            "'it depends whether paraphrasing is correct' — verbatim administration is non-negotiable, "
            "no exceptions; (2) described supervisor absence as 'no serious concern' — supervisors are "
            "expected to rotate and actively observe. These are knowledge gaps, not coaching gaps. "
            "Note: Muzzammil's threshold is 40% minimum for GWC — Zubair is at 42%, borderline."
        ),
        "probe": "Below Muzzammil's stated threshold. Recommend excluding from final consideration.",
    },
]

# App IDs for CV attachment (leading candidates only)
CV_APP_IDS = {c["app_id"]: c["name"] for c in LEADING}
# Fix: Zubair Hussain's app_id in DB is 1518, not 1430 (1430 = Scheherazade)
# Correction from pipeline data:
CV_APP_IDS_CORRECT = {
    1430: "Scheherazade Noor",
    2021: "Maria Karim",
    2018: "Moiz Khan",
    1857: "Amina Batool",
    2017: "Shazmina",
    1755: "Usman Ahmed Khan",
    # Discussion candidates
    1700: "Asad Farooq",
    1950: "Jalal Ud Din",
    1903: "Muhammad Abubakr",
    1518: "Zubair Hussain",
    # Schedule-only (case study stage)
    1921: "Rosheen Naeem",
}


# ── STEP 1: FETCH CVs ──────────────────────────────────────────────────────────

def safe_fn(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


def fetch_cvs():
    print("Fetching CVs from DB...")
    conn = psycopg2.connect(
        host="ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
        dbname="neondb", user="neondb_owner",
        password="npg_kBQ10OASHEmd", sslmode="require"
    )
    cur = conn.cursor()
    ids = list(CV_APP_IDS_CORRECT.keys())
    cur.execute("""
        SELECT a.id, c.resume_data
        FROM applications a JOIN candidates c ON a.candidate_id = c.id
        WHERE a.id = ANY(%s) AND c.resume_data IS NOT NULL
    """, (ids,))
    rows = cur.fetchall()
    cur.close(); conn.close()

    cv_paths = {}
    for app_id, b64 in rows:
        name  = CV_APP_IDS_CORRECT.get(app_id, str(app_id))
        fname = f"{app_id}_{safe_fn(name)}_CV.pdf"
        path  = os.path.join(CV_DIR, fname)
        try:
            with open(path, "wb") as f:
                f.write(base64.b64decode(b64))
            cv_paths[app_id] = (path, fname)
            print(f"  Saved: {name}")
        except Exception as e:
            print(f"  FAILED {name}: {e}")
    return cv_paths


# ── COLOUR PALETTE ─────────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#1a2a3a")
BLUE    = colors.HexColor("#1565c0")
GREEN   = colors.HexColor("#1a7a4a")
AMBER   = colors.HexColor("#c87800")
RED     = colors.HexColor("#c0392b")
LGREY   = colors.HexColor("#f7f9fc")
MGREY   = colors.HexColor("#dfe6e9")
GREY    = colors.HexColor("#636e72")
WHITE   = colors.white
BLACK   = colors.HexColor("#1a1a1a")

VERDICT_COLOR = {
    "STRONG HIRE":     GREEN,
    "HIRE":            BLUE,
    "HIRE (Prov.)":    BLUE,
    "CONDITIONAL":     AMBER,
    "BORDERLINE":      RED,
}


# ── STEP 2: BUILD PDF ──────────────────────────────────────────────────────────

def build_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             leftMargin=18*mm, rightMargin=18*mm,
                             topMargin=18*mm, bottomMargin=18*mm)
    SS  = getSampleStyleSheet()

    # Styles
    T_COVER   = ParagraphStyle("TCover",  parent=SS["Normal"], fontSize=22,
                                textColor=NAVY, alignment=TA_CENTER,
                                fontName="Helvetica-Bold", spaceAfter=4)
    T_SUB     = ParagraphStyle("TSub",    parent=SS["Normal"], fontSize=11,
                                textColor=GREY, alignment=TA_CENTER, spaceAfter=3)
    T_WARN    = ParagraphStyle("TWarn",   parent=SS["Normal"], fontSize=9,
                                textColor=RED,  alignment=TA_CENTER)
    T_SEC     = ParagraphStyle("TSec",    parent=SS["Normal"], fontSize=12,
                                textColor=BLUE, fontName="Helvetica-Bold",
                                spaceBefore=10, spaceAfter=5)
    T_BODY    = ParagraphStyle("TBody",   parent=SS["Normal"], fontSize=9.5,
                                leading=14, alignment=TA_JUSTIFY,
                                textColor=BLACK, spaceAfter=5)
    T_LABEL   = ParagraphStyle("TLabel",  parent=SS["Normal"], fontSize=8,
                                textColor=GREY, spaceAfter=2)
    T_NOTE    = ParagraphStyle("TNote",   parent=SS["Normal"], fontSize=8.5,
                                textColor=GREY, alignment=TA_JUSTIFY,
                                leading=12, spaceAfter=4)
    T_CNAME   = ParagraphStyle("TCName",  parent=SS["Normal"], fontSize=11,
                                textColor=NAVY, fontName="Helvetica-Bold", spaceAfter=2)
    T_TAG     = ParagraphStyle("TTag",    parent=SS["Normal"], fontSize=9,
                                textColor=GREY, fontName="Helvetica-Oblique",
                                spaceAfter=5)
    T_PROBE   = ParagraphStyle("TProbe",  parent=SS["Normal"], fontSize=9,
                                textColor=colors.HexColor("#7b341e"),
                                leading=13, spaceAfter=0)

    def hr(color=MGREY, thick=0.5):
        return HRFlowable(width="100%", thickness=thick, color=color, spaceAfter=6)

    def verdict_chip(v):
        c = VERDICT_COLOR.get(v, GREY)
        return Paragraph(
            f'<font color="{c.hexval()}"><b>{v}</b></font>', T_BODY)

    def candidate_block(c, cv_path=None, cv_fname=None):
        vc  = VERDICT_COLOR.get(c["verdict"], GREY)
        # Name rendered as blue underlined text — PyMuPDF will add the internal link later
        name_cell = Paragraph(
            f'<font color="#1565c0"><u><b>{c["name"]}</b></u></font>',
            T_CNAME)

        # Show verdict only in header — no score percentage shown since debrief scorecard pending
        rows = [
            [
                name_cell,
                Paragraph(
                    f'<font color="{vc.hexval()}"><b>{c["verdict"]}</b></font>',
                    T_BODY),
                Paragraph(f'<i>{c["debrief"]}</i>', T_NOTE),
            ]
        ]
        tbl = Table(rows, colWidths=[65*mm, 55*mm, 50*mm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), LGREY),
            ("TOPPADDING",   (0,0), (-1,-1), 7),
            ("BOTTOMPADDING",(0,0), (-1,-1), 4),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
            ("LINEBELOW",    (0,0), (-1,0),  0.8, vc),
            ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ]))
        items = [tbl]
        if c.get("tagline"):
            items.append(Spacer(1, 2*mm))
            items.append(Paragraph(c["tagline"], T_TAG))
        items.append(Paragraph(c["signal"], T_BODY))
        if c.get("probe"):
            items.append(Spacer(1, 1*mm))
            items.append(Paragraph(
                f'<b>At debrief, probe:</b> {c["probe"]}', T_PROBE))
        return KeepTogether(items + [Spacer(1, 5*mm)])

    story = []

    # ── COVER ──────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph("Final Candidates &amp; Decision View", T_COVER))
    story.append(Paragraph("Field Coordinator, Research &amp; Impact Studies", T_SUB))
    story.append(Paragraph("Impact &amp; Policy Team · Taleemabad", T_SUB))
    story.append(Spacer(1, 3*mm))
    story.append(hr(BLUE, 1.5))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("2 April 2026 &nbsp;|&nbsp; PILOT — Ayesha &amp; Jawwad only", T_WARN))

    # ── SNAPSHOT ───────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Where We Are", T_SEC))
    story.append(hr())

    snap_data = [
        ["238 applications received", "17 shortlisted (7.1%)", "10 reached case study stage"],
        ["3 debriefs completed", "6 debriefs scheduled (2–9 Apr)", "1 candidate still at case stage"],
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
        "The pipeline produced a solid cohort. Six candidates scored HIRE or above on the case study. "
        "Three debriefs are done; six more are scheduled across 2–9 April. "
        "All scores shown are case study scores — debrief scorecards are pending for most candidates.",
        T_BODY
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Note (Muzzammil, 31 Mar): candidates scoring below 40% on case study should not be considered "
        "for debrief. Zubair Hussain at 42% is borderline and has been placed in the discussion section.",
        T_NOTE
    ))

    # ── DEBRIEF SCHEDULE ───────────────────────────────────────────────────────
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Debrief Schedule", T_SEC))
    story.append(hr())

    sched_data = [
        ["Candidate", "Date &amp; Time", "Status", "Attendees Confirmed"],
        ["Muhammad Abubakr", "19 Mar · 12:00pm", "Done", "Muzzammil, Abubakr"],
        ["Moiz Khan",        "24 Mar · 10:00am", "Done", "Muzzammil, Moiz"],
        ["Shazmina Sharif",  "25 Mar · 10:00am", "Done", "Muzzammil, Shazmina"],
        ["Scheherazade Noor","2 Apr · 1:00pm",   "2 Apr", "Muzzammil, Scheherazade, Ayesha"],
        ["Asad Farooq",      "3 Apr · 10:30am",  "3 Apr", "Muzzammil, Asad, Ayesha"],
        ["Maria Karim",      "6 Apr · 11:00am",  "6 Apr", "Muzzammil, Maria, Ayesha"],
        ["Amina Batool",     "7 Apr · 2:30pm",   "7 Apr", "Ayesha, Amina (Calendar not locked — Muzzammil)"],
        ["Jalal Ud Din",     "8 Apr · 10:30am",  "8 Apr", "Muzzammil, Jalal, Ayesha"],
        ["Usman Ahmed Khan", "9 Apr · 12:00pm",  "9 Apr", "Ayesha, Usman (Calendar not locked — Muzzammil)"],
        ["Rosheen Naeem",    "No slot yet",       "Case study sent 1 Apr", "Calendar not locked"],
    ]
    def sched_cell(cell, r, c_idx):
        # Column 0 = candidate name: blue + underlined (except header row)
        if r == 0:
            return Paragraph(cell, ParagraphStyle("sc_hdr", parent=SS["Normal"],
                             fontSize=8.5, leading=12, textColor=BLUE,
                             fontName="Helvetica-Bold"))
        if c_idx == 0:
            return Paragraph(f'<u>{cell}</u>',
                             ParagraphStyle("sc_name", parent=SS["Normal"],
                             fontSize=8.5, leading=12, textColor=BLUE,
                             fontName="Helvetica"))
        return Paragraph(cell, ParagraphStyle("sc_cell", parent=SS["Normal"],
                         fontSize=8.5, leading=12, textColor=BLACK,
                         fontName="Helvetica"))

    s_tbl = Table(
        [[sched_cell(cell, r, c_idx) for c_idx, cell in enumerate(row)]
         for r, row in enumerate(sched_data)],
        colWidths=[48*mm, 32*mm, 28*mm, 62*mm]
    )
    row_bgs = [(0, WHITE)]
    for i in range(1, len(sched_data)):
        if "Done" in sched_data[i][2]:
            row_bgs.append((i, colors.HexColor("#e8f5e9")))
        elif "Case study" in sched_data[i][2]:
            row_bgs.append((i, colors.HexColor("#fff3e0")))
        else:
            row_bgs.append((i, WHITE if i % 2 == 0 else LGREY))
    s_style = [
        ("GRID",         (0,0), (-1,-1), 0.6, BLACK),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ]
    for i, bg in row_bgs:
        s_style.append(("BACKGROUND", (0,i), (-1,i), bg))
    s_tbl.setStyle(TableStyle(s_style))
    story.append(s_tbl)

    # ── LEADING CANDIDATES ─────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Leading Candidates", T_SEC))
    story.append(hr(BLUE, 1))
    story.append(Paragraph(
        "These six candidates cleared the values interview and scored HIRE or above on the case study. "
        "Names are hyperlinked — click to open their CV. "
        "All scores are case study scores only; debrief scorecards are yet to be completed.",
        T_BODY
    ))
    story.append(Spacer(1, 4*mm))

    for c in LEADING:
        cv_fname = f"{c['app_id']}_{safe_fn(c['name'])}_CV.pdf"
        cv_path  = os.path.join(CV_DIR, cv_fname)
        story.append(candidate_block(c, cv_path=cv_path, cv_fname=cv_fname))

    # ── STILL UNDER DISCUSSION ─────────────────────────────────────────────────
    story.append(Paragraph("Still Under Discussion", T_SEC))
    story.append(hr(AMBER, 1))
    story.append(Paragraph(
        "These four candidates carry mixed signals from the case study. "
        "Each profile notes the specific gap that the debrief would need to resolve before advancing. "
        "Names are hyperlinked — click to open their CV.",
        T_BODY
    ))
    story.append(Spacer(1, 4*mm))

    for c in DISCUSSION:
        cv_fname = f"{c['app_id']}_{safe_fn(c['name'])}_CV.pdf"
        cv_path  = os.path.join(CV_DIR, cv_fname)
        story.append(candidate_block(c, cv_path=cv_path, cv_fname=cv_fname))

    # ── SUGGESTED CANDIDATES ───────────────────────────────────────────────────
    story.append(Paragraph("Suggested Candidates — Based on Case Study &amp; Resume", T_SEC))
    story.append(hr(BLUE, 1))
    story.append(Paragraph(
        "The following candidates showed the strongest signals across both resume and case study. "
        "This is a suggestion for the panel's consideration — the final decision rests with "
        "the hiring manager and the team after debrief scorecards are completed.",
        T_BODY
    ))
    story.append(Spacer(1, 4*mm))

    sug_data = [
        ["Candidate", "Debrief Status", "What stood out"],
        ["Scheherazade Noor", "2 Apr, 1:00pm",
         "Most methodologically rigorous submission. Investigated before acting, "
         "read the RCT study design correctly, named consent escalation in-tracker."],
        ["Maria Karim", "6 Apr, 11:00am",
         "Sharpest on research validity. Best articulation of the sampling breach "
         "consequence. Dedicated Substitution sheet in tracker labelled Sampling Violation."],
        ["Moiz Khan", "Done — 24 Mar",
         "Most operationally comprehensive tracker. Strong systems thinking. "
         "Debrief completed."],
        ["Amina Batool", "7 Apr, 2:30pm",
         "Practically grounded. Genuine Pakistan field instinct. "
         "Structured options with trade-offs for the Research Lead."],
        ["Shazmina Sharif", "Done — 25 Mar",
         "Field-competent and operationally reliable. "
         "Debrief completed. Research integrity framing needs sharpening."],
        ["Usman Ahmed Khan", "9 Apr, 12:00pm",
         "Second strongest written submission. Strong on field judgment and research framing."],
    ]
    sug_tbl = Table(
        [[Paragraph(cell, ParagraphStyle("sg", parent=SS["Normal"],
                    fontSize=9, leading=13,
                    textColor=(BLUE if r==0 else BLACK),
                    fontName=("Helvetica-Bold" if r==0 else "Helvetica")))
          for cell in row]
         for r, row in enumerate(sug_data)],
        colWidths=[48*mm, 30*mm, 92*mm]
    )
    sug_style = [
        ("BACKGROUND",    (0,0), (-1,0),  WHITE),
        ("TEXTCOLOR",     (0,0), (-1,0),  BLUE),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LGREY]),
        ("GRID",          (0,0), (-1,-1), 0.6, BLACK),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]
    sug_tbl.setStyle(TableStyle(sug_style))
    story.append(sug_tbl)

    # ── FOOTER ─────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 6*mm))
    story.append(hr())
    story.append(Paragraph(
        "Prepared by Coco — Taleemabad Talent Acquisition &nbsp;|&nbsp; "
        "hiring@taleemabad.com &nbsp;|&nbsp; 2 April 2026",
        ParagraphStyle("Foot", parent=SS["Normal"], fontSize=8,
                       textColor=GREY, alignment=TA_CENTER)
    ))

    doc.build(story)
    buf.seek(0)
    return buf.read()


def upload_cvs_to_drive(cv_paths_ordered):
    """
    Uploads each candidate CV to Google Drive, sets public view permission,
    returns dict: name -> view URL (https://drive.google.com/file/d/ID/view)
    """
    creds   = Credentials.from_authorized_user_file(
        "c:/Agent Coco/token_drive.json",
        scopes=["https://www.googleapis.com/auth/drive.file"])
    service = gdrive_build("drive", "v3", credentials=creds)

    drive_links = {}
    for name, cv_path in cv_paths_ordered:
        if not cv_path or not os.path.exists(cv_path):
            continue
        print(f"  Uploading: {name}...")
        meta   = {"name": f"{name} — CV (Job 36 Field Coordinator).pdf"}
        media  = MediaFileUpload(cv_path, mimetype="application/pdf")
        f      = service.files().create(body=meta, media_body=media,
                                         fields="id").execute()
        fid    = f["id"]
        # Set anyone-with-link can view
        service.permissions().create(
            fileId=fid,
            body={"type": "anyone", "role": "reader"}
        ).execute()
        drive_links[name] = f"https://drive.google.com/file/d/{fid}/view"
        print(f"    -> {drive_links[name]}")

    return drive_links


def inject_drive_links(report_bytes, drive_links):
    """
    Uses PyMuPDF to find each candidate name in the report and replace
    the text annotation with a real URI link to their Drive CV.
    """
    doc = fitz.open("pdf", report_bytes)
    for page in doc:
        for name, url in drive_links.items():
            for rect in page.search_for(name):
                page.insert_link({
                    "kind": fitz.LINK_URI,
                    "from": rect,
                    "uri":  url,
                })
    out = io.BytesIO()
    doc.save(out)
    doc.close()
    out.seek(0)
    return out.read()


# ── STEP 3: EMAIL ──────────────────────────────────────────────────────────────

def build_html_body():
    return """
<html><body style="font-family:Georgia,serif;font-size:14px;color:#1a1a1a;
                   max-width:620px;margin:auto;background:#f0f4f0;padding:24px 0;">
<table width="620" cellpadding="0" cellspacing="0"
       style="background:#ffffff;border-radius:8px;
              box-shadow:0 2px 12px rgba(0,0,0,0.08);overflow:hidden;">
  <tr>
    <td style="background:#1a2a3a;padding:24px 32px;">
      <p style="margin:0;font-family:Georgia,serif;font-size:11px;
                color:#90a4ae;letter-spacing:2px;text-transform:uppercase;">
        People &amp; Culture · Hiring Decision Brief
      </p>
      <p style="margin:8px 0 2px;font-family:Georgia,serif;font-size:18px;
                font-weight:bold;color:#ffffff;">
        Final Candidates &amp; Decision View
      </p>
      <p style="margin:0;font-family:Georgia,serif;font-size:12px;color:#90caf9;">
        Field Coordinator, Research &amp; Impact Studies
      </p>
    </td>
  </tr>
  <tr>
    <td style="padding:28px 32px;">
      <p style="margin:0 0 16px;">Hi Ayesha,</p>
      <p style="margin:0 0 16px;">
        Attached is the hiring decision brief for <strong>Field Coordinator, Research &amp; Impact Studies</strong>.
        This replaces the earlier pipeline report — it is framed around the decision, not the process.
      </p>
      <table width="100%" cellpadding="0" cellspacing="0" style="margin:16px 0;">
        <tr>
          <td style="padding:12px;background:#e3f0fb;border-radius:6px;text-align:center;width:30%">
            <strong style="font-size:20px;color:#1565c0;">6</strong><br>
            <span style="font-size:11px;color:#666;">Leading candidates (HIRE+)</span>
          </td>
          <td width="8"></td>
          <td style="padding:12px;background:#e8f5e9;border-radius:6px;text-align:center;width:30%">
            <strong style="font-size:20px;color:#1a7a4a;">3</strong><br>
            <span style="font-size:11px;color:#666;">Debriefs completed</span>
          </td>
          <td width="8"></td>
          <td style="padding:12px;background:#fff8e1;border-radius:6px;text-align:center;width:30%">
            <strong style="font-size:20px;color:#c87800;">6</strong><br>
            <span style="font-size:11px;color:#666;">Debriefs this week</span>
          </td>
        </tr>
      </table>
      <p style="margin:16px 0 8px;">
        CVs for all 10 pipeline candidates are attached individually to this email.
      </p>
      <p style="margin:0;font-size:12px;color:#c62828;">
        PILOT — Please review and share feedback before this goes to Muzzammil.
      </p>
    </td>
  </tr>
  <tr>
    <td style="padding:12px 32px;background:#f5f5f5;font-size:11px;color:#888;
               font-family:Georgia,serif;">
      Taleemabad Talent Acquisition &nbsp;|&nbsp; hiring@taleemabad.com
    </td>
  </tr>
</table>
</body></html>"""


def main():
    # Fetch CVs
    cv_paths = fetch_cvs()
    print(f"CVs ready: {len(cv_paths)}")

    # Upload CVs to Google Drive and get shareable view URLs
    print("\nUploading CVs to Google Drive...")
    cv_ordered = []
    for c in LEADING + DISCUSSION:
        app_id = c["app_id"]
        name   = c["name"]
        if app_id in cv_paths:
            cv_ordered.append((name, cv_paths[app_id][0]))
    # Add Rosheen (schedule-only candidate)
    if 1921 in cv_paths:
        cv_ordered.append(("Rosheen Naeem", cv_paths[1921][0]))
    drive_links = upload_cvs_to_drive(cv_ordered)
    print(f"Uploaded: {len(drive_links)} CVs")

    # Build report PDF (names rendered as blue underlined text)
    print("\nBuilding decision brief PDF...")
    report_bytes = build_pdf()

    # Inject Drive URLs as clickable links on candidate names
    print("Injecting hyperlinks into PDF...")
    pdf_bytes = inject_drive_links(report_bytes, drive_links)

    with open(REPORT_PATH, "wb") as f:
        f.write(pdf_bytes)
    print(f"PDF: {len(pdf_bytes):,} bytes -> {REPORT_PATH}")

    # Build email — single PDF attachment (report + all CVs merged)
    msg = MIMEMultipart("mixed")
    msg["Subject"] = "[PILOT] Final Candidates & Decision View — Field Coordinator"
    msg["From"]    = EMAIL_USER
    msg["To"]      = PILOT_TO
    msg["CC"]      = PILOT_CC

    msg.attach(MIMEText(build_html_body(), "html", "utf-8"))

    # Single merged PDF — names hyperlinked internally to CV pages
    rpt = MIMEBase("application", "pdf")
    rpt.set_payload(pdf_bytes)
    encoders.encode_base64(rpt)
    rpt.add_header("Content-Disposition", "attachment",
                   filename="Job36_Decision_Brief.pdf")
    msg.attach(rpt)

    recipients = [PILOT_TO, PILOT_CC]
    allow_candidate_addresses(recipients)

    print(f"\nSending pilot to {PILOT_TO} (CC: {PILOT_CC})...")
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.ehlo(); smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(smtp_server=smtp, sender=EMAIL_USER,
                      recipients=recipients, message=msg.as_string(),
                      context="job36_decision_brief_pilot")
    print("Pilot sent.")


if __name__ == "__main__":
    main()
