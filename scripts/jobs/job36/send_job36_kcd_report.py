"""
Job 36 — Field Coordinator, Research & Impact Studies
KCD Case Study Evaluation Report — Batch 1 (4 candidates)
Pilot mode: TO = ayesha.khan@taleemabad.com, CC = jawwad.ali@taleemabad.com
"""

import smtplib, os, io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from datetime import date

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses


SENDER   = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
TO       = ["ayesha.khan@taleemabad.com"]
CC       = ["jawwad.ali@taleemabad.com"]

JOB_TITLE  = "Field Coordinator – Research & Impact Studies"
EVAL_DATE  = date.today().strftime("%d %B %Y")

# ── CANDIDATE DATA ──────────────────────────────────────────────────────────
CANDIDATES = [
    {
        "rank": 1,
        "name": "Scheherazade Noor",
        "score": 100,
        "verdict": "STRONG HIRE",
        "confidence": "High",
        "scores": {
            "Field & DQ Risk Identification (25%)": 5,
            "Operational Judgment & Firm Mgmt (25%)": 5,
            "Research Integrity & Sampling (20%)": 5,
            "Government & Stakeholder Coordination (15%)": 5,
            "Tracker Design & Systems Thinking (15%)": 5,
        },
        "narrative": (
            "Scheherazade doesn't just respond to scenarios — she diagnoses them. Before contacting the "
            "survey firm, she investigates; before writing a report, she forms a hypothesis. Her insight "
            "that fabricated data looks 'too neat' while genuine speed produces varied, uneven data is "
            "original field research thinking — not generic. Her framing of the government problem as "
            "relational rather than logistical reflects real experience. Her tracker included a "
            "Treatment/Control column — she understood this is a randomised impact evaluation, the only "
            "candidate who did. Every recommendation is specific enough to implement and traceable to a "
            "signal in the scenarios. She is honest about what she knows vs. what she is still investigating."
        ),
        "strengths": [
            "Data pattern analysis: 'Rushed or made-up data tends to look too neat' — original insight",
            "Hourly 48-hr breakdown (0–12, 12–18, 18–24, 24–48) with explicit reasoning per block",
            "Correctly identified DEO and headmaster as separate relationships needing separate outreach",
            "Stakeholder checklist: named contact + deadline at each approval level, not confirmed until all three cleared",
            "Treatment/Control column in tracker — only candidate who recognised the RCT study design",
            "5-sheet tracker pre-populated with realistic examples from every case study scenario",
        ],
        "integrity": "None. Writing is personal, narrative, and contains original observations. Visible uncertainty throughout is a human signal.",
    },
    {
        "rank": 2,
        "name": "Maria Karim",
        "score": 84,
        "verdict": "HIRE",
        "confidence": "High",
        "scores": {
            "Field & DQ Risk Identification (25%)": 4,
            "Operational Judgment & Firm Mgmt (25%)": 4,
            "Research Integrity & Sampling (20%)": 5,
            "Government & Stakeholder Coordination (15%)": 4,
            "Tracker Design & Systems Thinking (15%)": 4,
        },
        "narrative": (
            "Maria's conceptual clarity is her greatest strength. She produced the most precise statement "
            "on sampling integrity across all submissions: the unauthorised substitution 'undermines the "
            "ability of the study to draw any valid inference while comparing baseline and endline.' Her "
            "tracker includes a dedicated School Substitution sheet — unique across all candidates — "
            "labelling the deviation as 'Sampling Violation.' Where she falls short of Scheherazade is "
            "narrative depth: she lists correct actions but is less explicit about the reasoning behind them."
        ),
        "strengths": [
            "Best statement on sampling validity: named baseline/endline comparability threat explicitly",
            "Dedicated School Substitution Tracker sheet — only candidate to isolate this as a distinct log",
            "Correctly flagged previous assessments of protocol-breaching enumerator for re-collection",
            "DEO/AEO correctly identified as access escalation path",
            "7-sheet tracker with daily progress dashboard pre-populated with actual dates",
        ],
        "integrity": "None. Language imperfections and an incomplete final sentence in Q3 are consistent with a non-native speaker writing under time pressure — human signals.",
    },
    {
        "rank": 3,
        "name": "Amina Batool",
        "score": 76,
        "verdict": "HIRE",
        "confidence": "High",
        "scores": {
            "Field & DQ Risk Identification (25%)": 4,
            "Operational Judgment & Firm Mgmt (25%)": 4,
            "Research Integrity & Sampling (20%)": 3,
            "Government & Stakeholder Coordination (15%)": 4,
            "Tracker Design & Systems Thinking (15%)": 4,
        },
        "narrative": (
            "Amina is practical and grounded. She correctly calculated the expected study pace (6 schools/day, "
            "6 pairs of 2) and structured three concrete catch-up options for the Research Lead. Her strongest "
            "moment is the government coordination note: 'personally follow up on the progress of permission "
            "letters from desk to desk — best if done in-person.' That is hard to fake and reflects real "
            "experience navigating Pakistan's district-level bureaucracy. Her tracker has 5 functional sheets "
            "with School Replacement and Consent as dedicated columns — directly mapping both Scenarios 1 and 2. "
            "Where she falls short: she does not explicitly flag consent-compromised student data to the Research "
            "Lead, and presenting three options rather than a recommendation shows some hesitancy in ownership."
        ),
        "strengths": [
            "Correctly calculated 6 schools/day pace and 6 enumerator pairs from study parameters",
            "Pakistan-specific: 'follow up from desk to desk, best done in-person' — genuine field intuition",
            "School Replacement and Consent as dedicated tracker columns",
            "5-sheet tracker with auto-flagging (Fast/OK) and formula-driven dashboard",
            "Dashboard simulates Scenario 1 data: Expected 30, Actual 1, Gap -29",
        ],
        "integrity": "None. Self-corrections ('ideally I should review the dashboard every day') and manual calculations are human signals.",
    },
    {
        "rank": 4,
        "name": "Jalal Ud Din",
        "score": 63,
        "verdict": "CONDITIONAL",
        "confidence": "High",
        "scores": {
            "Field & DQ Risk Identification (25%)": 3,
            "Operational Judgment & Firm Mgmt (25%)": 3,
            "Research Integrity & Sampling (20%)": 3,
            "Government & Stakeholder Coordination (15%)": 2,
            "Tracker Design & Systems Thinking (15%)": 5,
        },
        "narrative": (
            "Jalal presents a notable internal inconsistency: his written responses are procedurally correct "
            "but shallow, while his tracker is one of the most sophisticated in the batch. The tracker includes "
            "a Supervisor Observation sheet with binary compliance checks (Q read verbatim? Student spacing OK? "
            "Consent explained?) and a School Coordination sheet with DEO/AEO columns — domain knowledge that "
            "is not reflected in the written analysis. For this role, both matter. The written responses suggest "
            "he may not yet demonstrate the analytical depth needed to handle ambiguous field situations without "
            "clear guidance. Recommend advancing to GWC only if the hiring manager wants to probe the discrepancy."
        ),
        "strengths": [
            "6-sheet tracker — most sheets of any submission",
            "Supervisor Observation sheet: binary checks for verbatim reading, spacing, consent — maps directly to Scenario 2",
            "School Coordination sheet with DEO/AEO informed columns — maps directly to Scenario 3",
            "Risk & Issues log includes 'Sampling Integrity Affected?' as a dedicated column",
            "Correctly identified unauthorized substitution as validity threat",
        ],
        "integrity": (
            "Low concern. Phrase 'epic focus on ethical protocols' is unusual and may be AI-assisted. "
            "Written action items are generic ('daily monitoring, productivity checks') despite the tracker "
            "showing domain-specific knowledge. Discrepancy between tracker quality and written response quality "
            "is notable — recommend a debrief question at GWC if advanced."
        ),
    },
]

VERDICT_COLORS = {
    "STRONG HIRE": colors.HexColor("#1a7a4a"),
    "HIRE":        colors.HexColor("#2e86de"),
    "CONDITIONAL": colors.HexColor("#e67e22"),
    "BORDERLINE":  colors.HexColor("#c0392b"),
    "NOT RECOMMENDED": colors.HexColor("#7f8c8d"),
}

SCORE_COLOR = {
    5: colors.HexColor("#1a7a4a"),
    4: colors.HexColor("#27ae60"),
    3: colors.HexColor("#e67e22"),
    2: colors.HexColor("#e74c3c"),
    1: colors.HexColor("#c0392b"),
}

# ── PDF BUILD ────────────────────────────────────────────────────────────────
def build_pdf(buf):
    doc = SimpleDocTemplate(
        buf,
        pagesize=landscape(A4),
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=12*mm, bottomMargin=12*mm,
    )
    W = landscape(A4)[0] - 30*mm

    styles = getSampleStyleSheet()
    def sty(name, **kw):
        return ParagraphStyle(name, parent=styles["Normal"], **kw)

    H1    = sty("H1",    fontSize=18, fontName="Helvetica-Bold",  textColor=colors.HexColor("#1a1a2e"), spaceAfter=4)
    H2    = sty("H2",    fontSize=13, fontName="Helvetica-Bold",  textColor=colors.HexColor("#1a7a4a"), spaceAfter=3)
    H3    = sty("H3",    fontSize=10, fontName="Helvetica-Bold",  textColor=colors.HexColor("#1a1a2e"), spaceAfter=2)
    BODY  = sty("BODY",  fontSize=8.5, leading=13, spaceAfter=4)
    SMALL = sty("SMALL", fontSize=7.5, leading=11, textColor=colors.HexColor("#444444"))
    META  = sty("META",  fontSize=8,  textColor=colors.HexColor("#666666"), spaceAfter=2)
    LABEL = sty("LABEL", fontSize=7.5, fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_CENTER)

    story = []

    # ── HEADER ────────────────────────────────────────────────────────────
    story.append(Paragraph(f"KCD Case Study Evaluation", H1))
    story.append(Paragraph(f"{JOB_TITLE}  ·  Taleemabad  ·  {EVAL_DATE}", META))
    story.append(Paragraph("Batch 1 of 2  ·  4 candidates evaluated  ·  1 pending (Usman Ahmed Khan)", META))
    story.append(HRFlowable(width=W, thickness=1.5, color=colors.HexColor("#1a7a4a"), spaceAfter=8))

    # ── SUMMARY TABLE ─────────────────────────────────────────────────────
    story.append(Paragraph("Summary", H2))

    sum_data = [["#", "Candidate", "Score", "Verdict", "Confidence",
                 "DQ Risk\n(25%)", "Op. Judgment\n(25%)", "Research\nIntegrity (20%)",
                 "Govt\nCoord (15%)", "Tracker\n(15%)"]]
    for c in CANDIDATES:
        sc = list(c["scores"].values())
        sum_data.append([
            str(c["rank"]),
            c["name"],
            f"{c['score']}%",
            c["verdict"],
            c["confidence"],
            str(sc[0]), str(sc[1]), str(sc[2]), str(sc[3]), str(sc[4]),
        ])

    col_w = [8*mm, 45*mm, 16*mm, 32*mm, 20*mm, 22*mm, 22*mm, 28*mm, 22*mm, 18*mm]
    sum_tbl = Table(sum_data, colWidths=col_w)

    sum_style = TableStyle([
        ("BACKGROUND",   (0,0), (-1,0),  colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",    (0,0), (-1,0),  colors.white),
        ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.HexColor("#f8f9fa"), colors.white]),
        ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#dddddd")),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ])
    # Colour verdict cells
    for i, c in enumerate(CANDIDATES, 1):
        vc = VERDICT_COLORS.get(c["verdict"], colors.grey)
        sum_style.add("BACKGROUND", (3,i), (3,i), vc)
        sum_style.add("TEXTCOLOR",  (3,i), (3,i), colors.white)
        sum_style.add("FONTNAME",   (3,i), (3,i), "Helvetica-Bold")
        # Colour score cells
        for j, s in enumerate(c["scores"].values()):
            col = j + 5
            sum_style.add("BACKGROUND", (col,i), (col,i), SCORE_COLOR.get(s, colors.grey))
            sum_style.add("TEXTCOLOR",  (col,i), (col,i), colors.white)
            sum_style.add("FONTNAME",   (col,i), (col,i), "Helvetica-Bold")

    sum_tbl.setStyle(sum_style)
    story.append(sum_tbl)
    story.append(Spacer(1, 6*mm))

    # ── BAR CHART ─────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 2.2))
    names  = [c["name"].split()[0] for c in CANDIDATES]
    scores = [c["score"] for c in CANDIDATES]
    bar_colors = [
        "#1a7a4a" if s >= 85 else
        "#2e86de" if s >= 70 else
        "#e67e22" if s >= 55 else "#e74c3c"
        for s in scores
    ]
    bars = ax.barh(names[::-1], scores[::-1], color=bar_colors[::-1], height=0.55)
    for bar, score in zip(bars, scores[::-1]):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f"{score}%", va="center", ha="left", fontsize=9, fontweight="bold")
    ax.set_xlim(0, 115)
    ax.axvline(85, color="#1a7a4a", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.axvline(70, color="#2e86de", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.axvline(55, color="#e67e22", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.set_xlabel("KCD Score (%)", fontsize=8)
    ax.set_title("KCD Scores — Batch 1", fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    plt.tight_layout()

    chart_buf = io.BytesIO()
    fig.savefig(chart_buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    chart_buf.seek(0)

    from reportlab.platypus import Image as RLImage
    chart_img = RLImage(chart_buf, width=110*mm, height=28*mm)
    story.append(chart_img)
    story.append(Spacer(1, 4*mm))

    story.append(PageBreak())

    # ── CANDIDATE DETAIL PAGES ────────────────────────────────────────────
    for c in CANDIDATES:
        vc = VERDICT_COLORS.get(c["verdict"], colors.grey)

        # Name + verdict header
        header_data = [[
            Paragraph(f"#{c['rank']}  {c['name']}", sty("ch", fontSize=14, fontName="Helvetica-Bold", textColor=colors.white)),
            Paragraph(f"{c['verdict']}  ·  {c['score']}%  ·  Confidence: {c['confidence']}",
                      sty("cv", fontSize=10, fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_LEFT)),
        ]]
        header_tbl = Table(header_data, colWidths=[90*mm, W - 90*mm])
        header_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), vc),
            ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING", (0,0), (-1,-1), 7),
            ("BOTTOMPADDING",(0,0),(-1,-1),7),
            ("LEFTPADDING",(0,0),(-1,-1), 8),
        ]))
        story.append(KeepTogether([header_tbl]))
        story.append(Spacer(1, 3*mm))

        # Scores table
        score_data = [["Criterion", "Score", "Max"]]
        for crit, val in c["scores"].items():
            score_data.append([crit, str(val), "5"])

        sc_tbl = Table(score_data, colWidths=[100*mm, 20*mm, 15*mm])
        sc_style = TableStyle([
            ("BACKGROUND",   (0,0), (-1,0),  colors.HexColor("#2c3e50")),
            ("TEXTCOLOR",    (0,0), (-1,0),  colors.white),
            ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
            ("FONTSIZE",     (0,0), (-1,-1), 8),
            ("ALIGN",        (1,0), (-1,-1), "CENTER"),
            ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.HexColor("#f0f0f0"), colors.white]),
            ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
            ("TOPPADDING",   (0,0), (-1,-1), 4),
            ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ])
        for i, val in enumerate(c["scores"].values(), 1):
            sc_style.add("BACKGROUND", (1,i), (1,i), SCORE_COLOR.get(val, colors.grey))
            sc_style.add("TEXTCOLOR",  (1,i), (1,i), colors.white)
            sc_style.add("FONTNAME",   (1,i), (1,i), "Helvetica-Bold")
        sc_tbl.setStyle(sc_style)

        # Strengths
        str_items = "".join(f"&bull; {s}<br/>" for s in c["strengths"])
        str_para  = Paragraph(str_items, SMALL)

        # Layout: scores left, strengths right
        layout = Table(
            [[sc_tbl, str_para]],
            colWidths=[138*mm, W - 142*mm]
        )
        layout.setStyle(TableStyle([
            ("VALIGN",      (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (1,0), (1,0),   6),
        ]))
        story.append(layout)
        story.append(Spacer(1, 3*mm))

        # Narrative
        story.append(Paragraph("Evaluation Narrative", H3))
        story.append(Paragraph(c["narrative"], BODY))
        story.append(Spacer(1, 2*mm))

        # Integrity
        integ_color = colors.HexColor("#fff3cd") if "concern" in c["integrity"].lower() or "low" in c["integrity"].lower() else colors.HexColor("#e8f5e9")
        integ_data = [[Paragraph(f"<b>Integrity Check:</b>  {c['integrity']}", SMALL)]]
        integ_tbl = Table(integ_data, colWidths=[W])
        integ_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), integ_color),
            ("TOPPADDING",    (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ("BOX",           (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ]))
        story.append(integ_tbl)

        if c["rank"] < len(CANDIDATES):
            story.append(PageBreak())

    # ── PENDING NOTE ──────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Pending Evaluation", H2))
    pending_data = [[
        Paragraph("<b>Usman Ahmed Khan</b>", BODY),
        Paragraph("Submission confirmed on Markaz (submitted 25 March 2026). File not yet available locally. "
                  "Will be evaluated in Batch 2 and a supplementary report issued.", BODY),
    ]]
    p_tbl = Table(pending_data, colWidths=[50*mm, W - 54*mm])
    p_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#f8f9fa")),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
    ]))
    story.append(p_tbl)
    story.append(Spacer(1, 4*mm))

    # ── NEXT STEPS ────────────────────────────────────────────────────────
    story.append(Paragraph("Recommended Next Steps", H2))
    steps = [
        "Advance <b>Scheherazade Noor</b> and <b>Maria Karim</b> to GWC interview — no conditions.",
        "Advance <b>Amina Batool</b> to GWC interview — no conditions.",
        "<b>Jalal Ud Din</b> — CONDITIONAL. Advance only if pool is thin. If advanced, probe the discrepancy between tracker quality and written analysis depth at GWC.",
        "Await Usman Ahmed Khan submission — Batch 2 report to follow.",
    ]
    for s in steps:
        story.append(Paragraph(f"&rarr;&nbsp; {s}", BODY))

    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width=W, thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "Sent on behalf of Talent Acquisition Team by Coco  ·  hiring@taleemabad.com  ·  www.taleemabad.com",
        sty("footer", fontSize=7, textColor=colors.HexColor("#999999"), alignment=TA_CENTER)
    ))

    doc.build(story)


# ── EMAIL ────────────────────────────────────────────────────────────────────
def send():
    pdf_buf = io.BytesIO()
    build_pdf(pdf_buf)
    pdf_buf.seek(0)

    msg = MIMEMultipart("mixed")
    msg["From"]    = SENDER
    msg["To"]      = ", ".join(TO)
    msg["CC"]      = ", ".join(CC)
    msg["Subject"] = f"KCD Evaluation Report — {JOB_TITLE} (Batch 1 of 2)"

    html = f"""
    <div style="font-family:Arial,sans-serif;font-size:14px;color:#1a1a2e;max-width:600px">
      <div style="background:#1a7a4a;padding:20px 24px;border-radius:6px 6px 0 0">
        <h2 style="color:white;margin:0;font-size:18px">KCD Evaluation Report</h2>
        <p style="color:#d4edda;margin:4px 0 0">{JOB_TITLE} &nbsp;·&nbsp; Taleemabad</p>
      </div>
      <div style="background:#f8f9fa;padding:20px 24px;border:1px solid #dee2e6;border-top:none">
        <p style="margin:0 0 16px">Hi Ayesha and Jawwad,</p>
        <p style="margin:0 0 16px">Please find attached the KCD case study evaluation report for <b>Batch 1</b> of the Field Coordinator role. 4 candidates evaluated. 1 pending (Usman Ahmed Khan — Batch 2 to follow).</p>

        <table style="width:100%;border-collapse:collapse;margin-bottom:16px">
          <tr style="background:#1a1a2e;color:white">
            <th style="padding:8px 12px;text-align:left">Candidate</th>
            <th style="padding:8px 12px;text-align:center">Score</th>
            <th style="padding:8px 12px;text-align:center">Verdict</th>
          </tr>
          <tr style="background:#f8f9fa">
            <td style="padding:8px 12px">Scheherazade Noor</td>
            <td style="padding:8px 12px;text-align:center"><b>100%</b></td>
            <td style="padding:8px 12px;text-align:center"><span style="background:#1a7a4a;color:white;padding:3px 10px;border-radius:4px;font-size:12px"><b>STRONG HIRE</b></span></td>
          </tr>
          <tr>
            <td style="padding:8px 12px">Maria Karim</td>
            <td style="padding:8px 12px;text-align:center"><b>84%</b></td>
            <td style="padding:8px 12px;text-align:center"><span style="background:#2e86de;color:white;padding:3px 10px;border-radius:4px;font-size:12px"><b>HIRE</b></span></td>
          </tr>
          <tr style="background:#f8f9fa">
            <td style="padding:8px 12px">Amina Batool</td>
            <td style="padding:8px 12px;text-align:center"><b>76%</b></td>
            <td style="padding:8px 12px;text-align:center"><span style="background:#2e86de;color:white;padding:3px 10px;border-radius:4px;font-size:12px"><b>HIRE</b></span></td>
          </tr>
          <tr>
            <td style="padding:8px 12px">Jalal Ud Din</td>
            <td style="padding:8px 12px;text-align:center"><b>63%</b></td>
            <td style="padding:8px 12px;text-align:center"><span style="background:#e67e22;color:white;padding:3px 10px;border-radius:4px;font-size:12px"><b>CONDITIONAL</b></span></td>
          </tr>
        </table>

        <p style="margin:0 0 8px">Full evaluation with criterion-by-criterion scores, narratives, and integrity checks is in the attached PDF.</p>
        <p style="margin:0;color:#666;font-size:12px">Usman Ahmed Khan — submission received on Markaz but file not yet available locally. Batch 2 report to follow.</p>
      </div>
      <div style="padding:14px 24px;font-size:11px;color:#999;text-align:center">
        Warm regards,&nbsp; People and Culture Team &nbsp;·&nbsp; Taleemabad<br>
        hiring@taleemabad.com &nbsp;|&nbsp; www.taleemabad.com<br>
        Sent on behalf of Talent Acquisition Team by Coco
      </div>
    </div>
    """

    msg.attach(MIMEText(html, "html"))

    att = MIMEBase("application", "pdf")
    att.set_payload(pdf_buf.read())
    encoders.encode_base64(att)
    att.add_header("Content-Disposition", "attachment",
                   filename=f"KCD_Evaluation_FieldCoordinator_Batch1_{date.today().strftime('%Y%m%d')}.pdf")
    msg.attach(att)

    all_rcpt = TO + CC
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(SENDER, PASSWORD)
        allow_candidate_addresses(all_rcpt if isinstance(all_rcpt, list) else [all_rcpt])
        safe_sendmail(s, SENDER, all_rcpt, msg.as_string(), context='send_job36_kcd_report')
    print(f"Sent to: {', '.join(all_rcpt)}")

if __name__ == "__main__":
    send()
