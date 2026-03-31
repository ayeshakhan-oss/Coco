"""
Job 36 — Field Coordinator, Research & Impact Studies
KCD Case Study Evaluation Report v2 — Batch 1 (4 candidates)
Revised: sharper, skimmable, decision-ready hiring memo format
Pilot: TO = ayesha.khan@taleemabad.com, CC = jawwad.ali@taleemabad.com
"""

import smtplib, os, io, math
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from datetime import date

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image as RLImage
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

# ── COLOUR SYSTEM ────────────────────────────────────────────────────────────
C = {
    "green":       colors.HexColor("#1a7a4a"),   # STRONG HIRE / Taleemabad green
    "green_light": colors.HexColor("#e8f5ee"),
    "blue":        colors.HexColor("#1a5fa8"),   # HIRE / section headers
    "blue_light":  colors.HexColor("#eaf1fb"),
    "amber":       colors.HexColor("#c87800"),   # CONDITIONAL
    "amber_light": colors.HexColor("#fff8e6"),
    "red":         colors.HexColor("#c0392b"),   # NOT RECOMMENDED
    "red_light":   colors.HexColor("#fdf0ee"),
    "dark":        colors.HexColor("#1e2a38"),   # headings / table header
    "body":        colors.HexColor("#2d3436"),   # body text
    "mid":         colors.HexColor("#636e72"),   # meta / captions
    "rule":        colors.HexColor("#dfe6e9"),   # dividers
    "bg":          colors.HexColor("#f7f9fc"),   # alternate row / card bg
    "white":       colors.white,
    "score5":      colors.HexColor("#1a7a4a"),
    "score4":      colors.HexColor("#27ae60"),
    "score3":      colors.HexColor("#c87800"),
    "score2":      colors.HexColor("#e17055"),
    "score1":      colors.HexColor("#c0392b"),
}

VERDICT_COLOR = {
    "STRONG HIRE":     C["green"],
    "HIRE":            C["blue"],
    "CONDITIONAL":     C["amber"],
    "BORDERLINE":      colors.HexColor("#d35400"),
    "NOT RECOMMENDED": C["red"],
}
VERDICT_LIGHT = {
    "STRONG HIRE":     C["green_light"],
    "HIRE":            C["blue_light"],
    "CONDITIONAL":     C["amber_light"],
    "BORDERLINE":      colors.HexColor("#fde8d8"),
    "NOT RECOMMENDED": C["red_light"],
}
SCORE_COLOR = {5: C["score5"], 4: C["score4"], 3: C["score3"], 2: C["score2"], 1: C["score1"]}

# ── CANDIDATE DATA ────────────────────────────────────────────────────────────
CRITERIA_SHORT = ["DQ Risk", "Op. Judgment", "Research\nIntegrity", "Govt\nCoord.", "Tracker"]
CRITERIA_FULL  = [
    "Field & Data Quality Risk Identification (25%)",
    "Operational Judgment & Survey Firm Mgmt (25%)",
    "Research Integrity & Sampling Discipline (20%)",
    "Government & Stakeholder Coordination (15%)",
    "Tracker Design & Systems Thinking (15%)",
]
WEIGHTS = [25, 25, 20, 15, 15]

CANDIDATES = [
    {
        "rank": 1,
        "name": "Scheherazade Noor",
        "score": 100,
        "verdict": "STRONG HIRE",
        "confidence": "High",
        "tagline": "Field-native thinker who diagnoses before acting — the only candidate who read the study design correctly.",
        "scores": [5, 5, 5, 5, 5],
        "strengths": [
            "Data pattern insight: 'Rushed data looks too neat; genuine speed produces varied, uneven data' — original, not generic",
            "Hourly 48-hr plan (0–12 · 12–18 · 18–24 · 24–48) with explicit reasoning per block",
            "Framed survey firm conversation around mission stakes, not compliance — the correct lever",
            "Identified DEO and headmaster as separate relationships requiring separate outreach",
            "Stakeholder checklist: named contact + deadline per approval level; not confirmed until all three cleared",
            "Treatment/Control column in tracker — only candidate who recognised the RCT study design",
        ],
        "why_matters": (
            "The Field Coordinator cannot directly control the survey firm — influence is the only tool. "
            "Her approach of framing deviations in terms of study outcomes ('I need to defend every data point "
            "to government partners') is exactly how you get cooperation without escalating. Her RCT awareness "
            "means she will catch sampling deviations that corrupt the study, not just flag process violations."
        ),
        "risk": (
            "No significant operational risk identified from the submission. "
            "Tracker was submitted as a Google Sheet — verify that her day-to-day tracking is as functional "
            "in offline/field conditions as it is conceptually strong."
        ),
        "narrative": (
            "Scheherazade does not respond to scenarios — she diagnoses them. Before contacting the survey firm, "
            "she investigates. Before writing a report, she forms a hypothesis. Her insight on data fabrication "
            "(neat-looking data is the suspicious kind) is original field research thinking. Her government "
            "coordination framing — 'this is a relationship problem, not a scheduling problem' — reflects real "
            "field experience. Every recommendation is specific enough to implement."
        ),
        "integrity": "Clean. Personal, non-linear writing. Visible uncertainty throughout. No AI signals.",
    },
    {
        "rank": 2,
        "name": "Maria Karim",
        "score": 84,
        "verdict": "HIRE",
        "confidence": "High",
        "tagline": "Sharpest on research validity in the batch — produced the most precise articulation of why the sampling breach matters.",
        "scores": [4, 4, 5, 4, 4],
        "strengths": [
            "Best sampling statement across all submissions: named baseline/endline comparability threat explicitly",
            "Dedicated School Substitution Tracker sheet — unique across all candidates, labelled 'Sampling Violation'",
            "Flagged previous assessments of protocol-breaching enumerator for re-collection",
            "DEO/AEO correctly identified as access escalation path in Q3",
            "7-sheet tracker with daily progress dashboard and time-flagging (Too Fast / Too Long / OK)",
        ],
        "why_matters": (
            "Sampling integrity is the hardest failure to recover from in a field study. A Field Coordinator "
            "who can name the baseline/endline comparability threat — not just 'this was unapproved' — will "
            "catch the deviations that actually matter. Her dedicated substitution tracker shows she will "
            "institutionalise the right controls, not just react to them."
        ),
        "risk": (
            "Written responses are correct but less narratively deep than Scheherazade's. "
            "May need more explicit guidance on when to escalate vs. resolve at field level. "
            "Language precision in external government correspondence may need light coaching."
        ),
        "narrative": (
            "Maria's conceptual clarity is her greatest strength. She produced the most precise statement "
            "on sampling integrity: the unauthorised substitution 'undermines the ability of the study to draw "
            "any valid inference while comparing baseline and endline.' Her tracker includes a dedicated "
            "substitution sheet — unique in this batch — labelling the deviation as 'Sampling Violation.' "
            "She lists correct actions throughout but is less explicit than Scheherazade about the reasoning "
            "behind each one."
        ),
        "integrity": "Clean. Language imperfections and an incomplete final sentence in Q3 are human signals — non-native speaker under time pressure.",
    },
    {
        "rank": 3,
        "name": "Amina Batool",
        "score": 76,
        "verdict": "HIRE",
        "confidence": "High",
        "tagline": "Practically grounded with real Pakistan bureaucracy instinct — some depth gaps on research ethics.",
        "scores": [4, 4, 3, 4, 4],
        "strengths": [
            "Correctly calculated expected study pace: 6 schools/day, 6 enumerator pairs — read the parameters",
            "Pakistan-specific: 'follow up from desk to desk, best done in-person' — rare, genuine field intuition",
            "Three structured catch-up options (A/B/C) presented to Research Lead with trade-offs",
            "School Replacement and Consent as dedicated tracker columns — directly maps Scenarios 1 and 2",
            "5-sheet tracker with formula-driven auto-flagging (Fast/OK) and dashboard simulating Scenario 1 data",
        ],
        "why_matters": (
            "In Rawalpindi's government school environment, access refusals are the most common execution risk. "
            "Her instinct to physically follow permission letters from desk to desk is exactly what gets schools "
            "opened on time — not emails. That instinct is hard to train. Her tracker design shows she will "
            "build tools that the team can actually use in the field."
        ),
        "risk": (
            "Did not explicitly flag consent-compromised student data to the Research Lead — a research ethics "
            "gap that matters if a data validity challenge arises post-study. "
            "Presenting three options rather than a recommendation shows some hesitancy in ownership; "
            "may need coaching to default to a position, not a menu."
        ),
        "narrative": (
            "Amina is practical and grounded. She did the math (a simple signal that she read the parameters), "
            "structured three concrete catch-up options, and showed real bureaucratic navigation instinct. "
            "Her tracker is functional and formula-driven. Where she falls short: she does not flag "
            "consent-compromised records to the Research Lead, and her default to three options rather than "
            "a recommendation suggests some ownership hesitancy."
        ),
        "integrity": "Clean. Self-corrections and manual calculations are human signals. No AI patterns.",
    },
    {
        "rank": 4,
        "name": "Jalal Ud Din",
        "score": 63,
        "verdict": "CONDITIONAL",
        "confidence": "High",
        "tagline": "Exceptional tracker, thin written analysis — the gap between the two needs probing before advancing.",
        "scores": [3, 3, 3, 2, 5],
        "strengths": [
            "6-sheet tracker — most comprehensive structure in the batch",
            "Supervisor Observation sheet: binary checks for verbatim reading, spacing, consent — maps directly to Scenario 2",
            "School Coordination sheet with DEO/AEO columns — maps directly to Scenario 3",
            "Risk & Issues log includes dedicated 'Sampling Integrity Affected?' column",
            "Correctly identified unauthorized substitution as a validity threat (not just a process issue)",
        ],
        "why_matters": (
            "The Field Coordinator role requires both: tracking discipline for firm oversight, and field judgment "
            "for ambiguous situations. Jalal's tracker shows the former at a high level. His written analysis — "
            "the part that simulates real-time field decision-making — is procedurally correct but shallow. "
            "That gap is the gap that matters when conditions are non-standard and guidance is unavailable."
        ),
        "risk": (
            "Main risk: may struggle to independently diagnose root causes in ambiguous field situations. "
            "The analytical thin-ness in written responses suggests he may be reactive rather than preventive. "
            "Would need close mentorship in the first 3 months. "
            "Tracker/analysis discrepancy should be probed at GWC — one of the two was AI-assisted."
        ),
        "narrative": (
            "Jalal presents the most notable internal inconsistency in this batch: his tracker (6 sheets, "
            "Supervisor Obs compliance checks, DEO/AEO coordination columns) is one of the strongest submitted, "
            "while his written analysis is the weakest. The discrepancy is decision-relevant. For a role that "
            "requires both operational structure and field judgment, this split profile carries real risk. "
            "Advance only if the pool justifies it, and probe the discrepancy explicitly at GWC."
        ),
        "integrity": "Low concern. 'Epic focus on ethical protocols' is unusual phrasing. Generic action items despite domain-specific tracker. Tracker/analysis discrepancy — probe at GWC.",
    },
]

# ── STYLE HELPERS ─────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()
    def s(name, **kw):
        return ParagraphStyle(name, parent=base["Normal"], **kw)
    return {
        "title":   s("title",   fontSize=20, fontName="Helvetica-Bold",  textColor=C["dark"],  spaceAfter=2),
        "sub":     s("sub",     fontSize=9,  textColor=C["mid"],          spaceAfter=6),
        "h2":      s("h2",      fontSize=12, fontName="Helvetica-Bold",   textColor=C["blue"],  spaceAfter=4, spaceBefore=6),
        "h3":      s("h3",      fontSize=9,  fontName="Helvetica-Bold",   textColor=C["dark"],  spaceAfter=3, spaceBefore=4),
        "body":    s("body",    fontSize=8.5, leading=13, textColor=C["body"], spaceAfter=4),
        "small":   s("small",   fontSize=7.5, leading=11, textColor=C["body"]),
        "meta":    s("meta",    fontSize=7.5, textColor=C["mid"],          spaceAfter=2),
        "tagline": s("tagline", fontSize=9,  fontName="Helvetica-Oblique", textColor=C["mid"],  spaceAfter=0),
        "center":  s("center",  fontSize=8,  alignment=TA_CENTER,          textColor=C["body"]),
        "footer":  s("footer",  fontSize=7,  alignment=TA_CENTER,          textColor=C["mid"]),
        "label":   s("label",   fontSize=7.5, fontName="Helvetica-Bold",   textColor=C["white"], alignment=TA_CENTER),
    }

# ── CHART: OVERALL SCORES ──────────────────────────────────────────────────────
def chart_scores():
    fig, ax = plt.subplots(figsize=(9, 2.0))
    names  = [c["name"].split()[0] for c in CANDIDATES]
    scores = [c["score"] for c in CANDIDATES]
    bar_clrs = ["#1a7a4a", "#1a5fa8", "#1a5fa8", "#c87800"]
    bars = ax.barh(names[::-1], scores[::-1], color=bar_clrs[::-1], height=0.48, zorder=3)
    for bar, sc in zip(bars, scores[::-1]):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{sc}%", va="center", ha="left", fontsize=8.5, fontweight="bold",
                color="#1e2a38")
    for x, lbl, clr in [(85, "Strong Hire", "#1a7a4a"), (70, "Hire", "#1a5fa8"), (55, "Conditional", "#c87800")]:
        ax.axvline(x, color=clr, linestyle="--", linewidth=0.7, alpha=0.5, zorder=2)
    ax.set_xlim(0, 115)
    ax.set_xlabel("KCD Score (%)", fontsize=7.5, color="#636e72")
    ax.set_title("Overall KCD Scores", fontsize=9, fontweight="bold", color="#1e2a38", pad=6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#dfe6e9")
    ax.spines["bottom"].set_color("#dfe6e9")
    ax.tick_params(labelsize=8, colors="#636e72")
    ax.set_facecolor("#f7f9fc")
    fig.patch.set_facecolor("white")
    ax.grid(axis="x", color="#dfe6e9", linewidth=0.5, zorder=0)
    plt.tight_layout(pad=0.4)
    buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=160, bbox_inches="tight"); plt.close(fig)
    buf.seek(0); return buf

# ── CHART: RADAR ──────────────────────────────────────────────────────────────
def chart_radar():
    labels = ["DQ Risk\n(25%)", "Op.\nJudgment\n(25%)", "Research\nIntegrity\n(20%)", "Govt\nCoord.\n(15%)", "Tracker\n(15%)"]
    N = len(labels)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5.5, 5.5), subplot_kw=dict(polar=True))
    ax.set_facecolor("#f7f9fc")
    fig.patch.set_facecolor("white")

    candidate_colors = ["#1a7a4a", "#1a5fa8", "#1a5fa8", "#c87800"]
    candidate_alphas = [0.25, 0.20, 0.20, 0.18]

    for idx, (c, clr, alp) in enumerate(zip(CANDIDATES, candidate_colors, candidate_alphas)):
        vals = c["scores"] + c["scores"][:1]
        ax.plot(angles, vals, color=clr, linewidth=1.8 if idx == 0 else 1.3,
                linestyle="solid", zorder=3 + idx, label=c["name"].split()[0])
        ax.fill(angles, vals, alpha=alp, color=clr, zorder=2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=7.5, color="#1e2a38")
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], size=6.5, color="#aaaaaa")
    ax.set_ylim(0, 5.5)
    ax.grid(color="#dfe6e9", linewidth=0.6)
    ax.spines["polar"].set_color("#dfe6e9")
    ax.legend(loc="lower right", bbox_to_anchor=(1.28, -0.05), fontsize=7.5,
              frameon=True, framealpha=0.9, edgecolor="#dfe6e9")
    ax.set_title("Criterion Profile Comparison", fontsize=9, fontweight="bold",
                 color="#1e2a38", pad=18)
    plt.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=160, bbox_inches="tight"); plt.close(fig)
    buf.seek(0); return buf

# ── COLORED BOX HELPER ────────────────────────────────────────────────────────
def box(text, style, bg, border=None, lpad=8):
    border = border or bg
    tbl = Table([[Paragraph(text, style)]], colWidths=[None])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), lpad),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("BOX",           (0,0),(-1,-1), 0.5, border),
    ]))
    return tbl

# ── PDF BUILD ─────────────────────────────────────────────────────────────────
def build_pdf(buf):
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=14*mm, rightMargin=14*mm,
                            topMargin=11*mm, bottomMargin=11*mm)
    W = landscape(A4)[0] - 28*mm
    ST = make_styles()
    story = []

    # ── PAGE 1: COVER + SUMMARY ────────────────────────────────────────────
    story.append(Paragraph("KCD Case Study Evaluation", ST["title"]))
    story.append(Paragraph(
        f"{JOB_TITLE} &nbsp;·&nbsp; Taleemabad &nbsp;·&nbsp; {EVAL_DATE} &nbsp;·&nbsp; "
        "Batch 1 of 2 &nbsp;·&nbsp; 4 candidates &nbsp;·&nbsp; 1 pending",
        ST["sub"]))
    story.append(HRFlowable(width=W, thickness=1.5, color=C["green"], spaceAfter=6))

    # Summary table
    story.append(Paragraph("Decision Summary", ST["h2"]))
    hdr = ["#", "Candidate", "Tagline", "Score", "Verdict", "DQ\nRisk", "Op.\nJudgmt", "Research\nIntegrity", "Govt\nCoord.", "Tracker"]
    rows = [hdr]
    for c in CANDIDATES:
        sc = c["scores"]
        rows.append([
            str(c["rank"]), c["name"], c["tagline"],
            f"{c['score']}%", c["verdict"],
            str(sc[0]), str(sc[1]), str(sc[2]), str(sc[3]), str(sc[4]),
        ])

    cw = [7*mm, 38*mm, 90*mm, 14*mm, 28*mm, 14*mm, 14*mm, 18*mm, 14*mm, 14*mm]
    tbl = Table(rows, colWidths=cw, repeatRows=1)
    ts = TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  C["dark"]),
        ("TEXTCOLOR",     (0,0),(-1,0),  C["white"]),
        ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,-1), 7.5),
        ("ALIGN",         (0,0),(-1,-1), "CENTER"),
        ("ALIGN",         (2,1),(2,-1),  "LEFT"),
        ("ALIGN",         (1,1),(1,-1),  "LEFT"),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [C["bg"], C["white"]]),
        ("GRID",          (0,0),(-1,-1), 0.3, C["rule"]),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (1,0),(2,-1),  6),
    ])
    for i, c in enumerate(CANDIDATES, 1):
        vc = VERDICT_COLOR[c["verdict"]]
        vl = VERDICT_LIGHT[c["verdict"]]
        ts.add("BACKGROUND", (4,i), (4,i), vc)
        ts.add("TEXTCOLOR",  (4,i), (4,i), C["white"])
        ts.add("FONTNAME",   (4,i), (4,i), "Helvetica-Bold")
        ts.add("BACKGROUND", (0,i), (0,i), vl)
        for j, sv in enumerate(c["scores"]):
            col = j + 5
            ts.add("BACKGROUND", (col,i), (col,i), SCORE_COLOR[sv])
            ts.add("TEXTCOLOR",  (col,i), (col,i), C["white"])
            ts.add("FONTNAME",   (col,i), (col,i), "Helvetica-Bold")
    tbl.setStyle(ts)
    story.append(tbl)
    story.append(Spacer(1, 4*mm))

    # Charts row: scores bar + radar
    sc_buf  = chart_scores()
    rad_buf = chart_radar()
    sc_img  = RLImage(sc_buf,  width=115*mm, height=26*mm)
    rad_img = RLImage(rad_buf, width=72*mm,  height=72*mm)

    chart_row = Table([[sc_img, rad_img]], colWidths=[120*mm, 75*mm])
    chart_row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"), ("LEFTPADDING",(1,0),(1,0),6)]))
    story.append(chart_row)

    story.append(PageBreak())

    # ── PAGE 2: CROSS-CANDIDATE COMPARISON + DECISION TABLE ───────────────
    story.append(Paragraph("Cross-Candidate Comparison", ST["h2"]))
    story.append(Paragraph(
        "Where the candidates differ most — and what those differences mean for this role.", ST["meta"]))
    story.append(Spacer(1, 2*mm))

    comp_rows = [
        ["Dimension", "Scheherazade", "Maria", "Amina", "Jalal"],
        ["Diagnostic depth\n(field judgment)",
         "Exceptional — forms hypotheses, tests them before acting",
         "Strong — conceptually precise, less narrative depth",
         "Solid — correct instincts, some ownership hesitancy",
         "Weak — correct but procedural; does not show root-cause reasoning"],
        ["Research integrity\n(sampling / consent)",
         "Correctly interrogates sampling criteria; flags consent data",
         "Best statement on sampling validity in the batch",
         "Correct on sampling; misses consent-data escalation",
         "Identifies violation but does not articulate implications"],
        ["Government navigation\n(Pakistan-specific)",
         "Relationship-first framing; DEO + headmaster as separate",
         "Correctly escalates to DEO/AEO; standard prevention measures",
         "Desk-to-desk follow-up instinct — strongest field intuition here",
         "Identifies right level; does not show Pakistan-specific depth"],
        ["Operational structure\n(tracker / systems)",
         "5-sheet tracker; RCT Treatment/Control column; pre-populated",
         "7 sheets; dedicated Substitution Tracker; daily dashboard",
         "5 sheets; formula-driven; auto-flags; consent + replacement cols",
         "6 sheets; Supervisor Obs compliance checks; strongest structure"],
        ["Survey firm management",
         "Mission-framed engagement; most sophisticated approach",
         "Formal written incident report; escalation policy; firm warnings",
         "Assertive but standard; daily reporting requirement",
         "Scheduled formal meeting; generic action items"],
        ["Ownership under ambiguity",
         "Makes recommendations; honest about uncertainty",
         "Makes recommendations; less explicit on reasoning",
         "Presents 3 options to Research Lead rather than recommending",
         "Lists steps; does not prioritise or weigh trade-offs"],
    ]
    cw2 = [38*mm, 55*mm, 52*mm, 52*mm, 52*mm]
    comp_tbl = Table(comp_rows, colWidths=cw2, repeatRows=1)
    comp_ts = TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  C["dark"]),
        ("TEXTCOLOR",     (0,0),(-1,0),  C["white"]),
        ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,-1), 7.5),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("ALIGN",         (0,0),(0,-1),  "LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [C["bg"], C["white"]]),
        ("GRID",          (0,0),(-1,-1), 0.3, C["rule"]),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("FONTNAME",      (0,1),(0,-1),  "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,1),(0,-1),  C["blue"]),
    ])
    comp_tbl.setStyle(comp_ts)
    story.append(comp_tbl)
    story.append(Spacer(1, 5*mm))

    # Tradeoff callout
    tradeoff_txt = (
        "<b>Key tradeoffs for the hiring decision:</b>&nbsp;&nbsp;"
        "Scheherazade leads on judgment and field intuition but her tracker needs field-condition verification. &nbsp;|&nbsp; "
        "Maria leads on research validity instinct and tracker structure. &nbsp;|&nbsp; "
        "Amina's Pakistan bureaucracy instinct is the most transferable operational skill — her ethics gap is coachable. &nbsp;|&nbsp; "
        "Jalal's tracker vs. analysis split is the only unresolved signal in this batch."
    )
    story.append(box(tradeoff_txt, ST["small"], C["blue_light"], C["blue"]))
    story.append(Spacer(1, 5*mm))

    # Hiring Decision Summary
    story.append(Paragraph("Hiring Decision Summary", ST["h2"]))
    dec_rows = [["Candidate", "Decision", "Why advance", "Main risk"]]
    dec_data = [
        ("Scheherazade Noor", "STRONG HIRE",
         "Best field judgment in batch. RCT-aware. Mission-framed firm engagement.",
         "Tracker field-condition verification needed."),
        ("Maria Karim", "HIRE",
         "Clearest sampling integrity thinking. Dedicated substitution controls.",
         "May need escalation guidance. External writing may need coaching."),
        ("Amina Batool", "HIRE",
         "Practical, Pakistan-savvy, formula-driven tracker with correct instincts.",
         "Consent-data escalation gap. Ownership hesitancy under ambiguity."),
        ("Jalal Ud Din", "CONDITIONAL — advance only if pool is thin",
         "Strong tracker structure and systems discipline.",
         "Written analysis is procedurally thin. Tracker/analysis discrepancy unresolved."),
    ]
    for n, d, w, r in dec_data:
        dec_rows.append([n, d, w, r])

    cw3 = [42*mm, 50*mm, 90*mm, 68*mm]
    dec_tbl = Table(dec_rows, colWidths=cw3, repeatRows=1)
    dec_ts = TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  C["dark"]),
        ("TEXTCOLOR",     (0,0),(-1,0),  C["white"]),
        ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("ALIGN",         (0,0),(-1,-1), "LEFT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [C["bg"], C["white"]]),
        ("GRID",          (0,0),(-1,-1), 0.3, C["rule"]),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
    ])
    for i, (_, verdict, _, _) in enumerate(dec_data, 1):
        vc = VERDICT_COLOR.get(verdict.split(" —")[0].strip(), C["amber"])
        dec_ts.add("BACKGROUND", (1,i), (1,i), vc)
        dec_ts.add("TEXTCOLOR",  (1,i), (1,i), C["white"])
        dec_ts.add("FONTNAME",   (1,i), (1,i), "Helvetica-Bold")
        dec_ts.add("FONTSIZE",   (1,i), (1,i), 7.5)
    dec_tbl.setStyle(dec_ts)
    story.append(dec_tbl)
    story.append(Spacer(1, 4*mm))

    # Integrity Flags (consolidated)
    story.append(Paragraph("Integrity Flags", ST["h2"]))
    flag_rows = [
        ["Candidate", "Signal", "Severity"],
        ["Jalal Ud Din",
         "Tracker (6 sheets, compliance checks, sampling integrity column) vs. written analysis (procedurally thin, generic actions) is a large internal inconsistency. "
         "One of the two was likely AI-assisted. Phrase 'epic focus on ethical protocols' is an unusual outlier in otherwise plain writing.",
         "Low concern — probe at GWC"],
        ["All others", "Clean. No AI content dump signals, no mirroring across candidates, no foundational misreads.", "None"],
    ]
    fl_tbl = Table(flag_rows, colWidths=[42*mm, 185*mm, 35*mm], repeatRows=1)
    fl_ts = TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  C["dark"]),
        ("TEXTCOLOR",     (0,0),(-1,0),  C["white"]),
        ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [C["amber_light"], C["bg"]]),
        ("GRID",          (0,0),(-1,-1), 0.3, C["rule"]),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
    ])
    fl_tbl.setStyle(fl_ts)
    story.append(fl_tbl)
    story.append(Spacer(1, 5*mm))

    # Pipeline Recommendations
    story.append(Paragraph("Pipeline Recommendations", ST["h2"]))
    pipe_rows = [["Candidate", "Current Stage", "Recommendation"]]
    pipe_data = [
        ("Scheherazade Noor",  "KCD evaluated",  "Advance to GWC — no conditions."),
        ("Maria Karim",        "KCD evaluated",  "Advance to GWC — no conditions."),
        ("Amina Batool",       "KCD evaluated",  "Advance to GWC — note consent-data escalation gap for GWC probing."),
        ("Jalal Ud Din",       "KCD evaluated",  "CONDITIONAL — advance only if pool is thin. Probe tracker/analysis discrepancy explicitly at GWC."),
        ("Usman Ahmed Khan",   "Submission confirmed on Markaz (25 Mar 2026)", "Awaiting local file — Batch 2 report to follow."),
    ]
    for n, stage, rec in pipe_data:
        pipe_rows.append([n, stage, rec])
    cw4 = [48*mm, 70*mm, 135*mm]
    pipe_tbl = Table(pipe_rows, colWidths=cw4, repeatRows=1)
    pipe_ts = TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  C["dark"]),
        ("TEXTCOLOR",     (0,0),(-1,0),  C["white"]),
        ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [C["bg"], C["white"]]),
        ("GRID",          (0,0),(-1,-1), 0.3, C["rule"]),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
    ])
    pipe_tbl.setStyle(pipe_ts)
    story.append(pipe_tbl)

    story.append(PageBreak())

    # ── PAGES 3–6: CANDIDATE DETAIL ────────────────────────────────────────
    for idx, c in enumerate(CANDIDATES):
        vc   = VERDICT_COLOR[c["verdict"]]
        vl   = VERDICT_LIGHT[c["verdict"]]

        # — Candidate header —
        hdr_data = [[
            Paragraph(f"#{c['rank']} &nbsp; {c['name']}", ParagraphStyle(
                "ch", parent=getSampleStyleSheet()["Normal"],
                fontSize=15, fontName="Helvetica-Bold", textColor=C["white"])),
            Paragraph(
                f"<b>{c['verdict']}</b> &nbsp;·&nbsp; {c['score']}% &nbsp;·&nbsp; Confidence: {c['confidence']}",
                ParagraphStyle("cv", parent=getSampleStyleSheet()["Normal"],
                               fontSize=9, fontName="Helvetica-Bold", textColor=C["white"],
                               alignment=TA_RIGHT)),
        ]]
        hdr_tbl = Table(hdr_data, colWidths=[W*0.6, W*0.4])
        hdr_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), vc),
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
            ("LEFTPADDING",   (0,0),(0,0),   10),
            ("RIGHTPADDING",  (1,0),(1,0),   10),
        ]))
        story.append(hdr_tbl)

        # Tagline
        tl_tbl = Table([[Paragraph(c["tagline"], ST["tagline"])]], colWidths=[W])
        tl_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), vl),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ]))
        story.append(tl_tbl)
        story.append(Spacer(1, 3*mm))

        # — Left col: criterion scores | Right col: key strengths —
        sc_data = [["Criterion", "Score", "/ 5"]]
        for crit, val in zip(CRITERIA_FULL, c["scores"]):
            sc_data.append([crit, str(val), ""])
        sc_tbl = Table(sc_data, colWidths=[90*mm, 14*mm, 10*mm])
        sc_ts = TableStyle([
            ("BACKGROUND",    (0,0),(-1,0),  C["dark"]),
            ("TEXTCOLOR",     (0,0),(-1,0),  C["white"]),
            ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,-1), 8),
            ("ALIGN",         (1,0),(-1,-1), "CENTER"),
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [C["bg"], C["white"]]),
            ("GRID",          (0,0),(-1,-1), 0.3, C["rule"]),
            ("TOPPADDING",    (0,0),(-1,-1), 4),
            ("BOTTOMPADDING", (0,0),(-1,-1), 4),
            ("LEFTPADDING",   (0,0),(0,-1),  6),
        ])
        for i, val in enumerate(c["scores"], 1):
            sc_ts.add("BACKGROUND", (1,i),(1,i), SCORE_COLOR[val])
            sc_ts.add("TEXTCOLOR",  (1,i),(1,i), C["white"])
            sc_ts.add("FONTNAME",   (1,i),(1,i), "Helvetica-Bold")
        sc_tbl.setStyle(sc_ts)

        str_items = "".join(f"&bull; {s}<br/>" for s in c["strengths"])
        str_para  = Paragraph(str_items, ST["small"])

        cols_tbl = Table([[sc_tbl, str_para]], colWidths=[118*mm, W - 122*mm])
        cols_tbl.setStyle(TableStyle([
            ("VALIGN",      (0,0),(-1,-1), "TOP"),
            ("LEFTPADDING", (1,0),(1,0),   8),
        ]))
        story.append(cols_tbl)
        story.append(Spacer(1, 3*mm))

        # — Why this matters for the role —
        story.append(Paragraph("Why this matters for the role", ST["h3"]))
        story.append(box(c["why_matters"], ST["small"], C["blue_light"], C["blue"]))
        story.append(Spacer(1, 2*mm))

        # — Evaluation narrative —
        story.append(Paragraph("Evaluation Narrative", ST["h3"]))
        story.append(Paragraph(c["narrative"], ST["body"]))
        story.append(Spacer(1, 2*mm))

        # — Risk if hired —
        story.append(Paragraph("Risk if Hired", ST["h3"]))
        story.append(box(c["risk"], ST["small"], C["red_light"], C["red_light"]))
        story.append(Spacer(1, 2*mm))

        # — Integrity check —
        integ_bg = C["amber_light"] if "concern" in c["integrity"].lower() else C["bg"]
        story.append(box(f"<b>Integrity Check:</b> &nbsp; {c['integrity']}", ST["small"], integ_bg, C["rule"]))

        if idx < len(CANDIDATES) - 1:
            story.append(PageBreak())

    # ── PENDING + FOOTER ──────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Pending — Batch 2", ST["h2"]))
    story.append(box(
        "<b>Usman Ahmed Khan</b> — submission confirmed on Markaz (25 March 2026). "
        "File not yet available locally. Will be evaluated in Batch 2; supplementary report to follow.",
        ST["body"], C["bg"], C["rule"]
    ))
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width=W, thickness=0.5, color=C["rule"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "Warm regards, &nbsp; People and Culture Team &nbsp;·&nbsp; Taleemabad &nbsp;·&nbsp; "
        "hiring@taleemabad.com &nbsp;|&nbsp; www.taleemabad.com &nbsp;·&nbsp; "
        "Sent on behalf of Talent Acquisition Team by Coco",
        ST["footer"]))

    doc.build(story)


# ── EMAIL ─────────────────────────────────────────────────────────────────────
def send():
    pdf_buf = io.BytesIO()
    build_pdf(pdf_buf)
    pdf_buf.seek(0)

    msg = MIMEMultipart("mixed")
    msg["From"]    = SENDER
    msg["To"]      = ", ".join(TO)
    msg["CC"]      = ", ".join(CC)
    msg["Subject"] = f"KCD Evaluation Report v3 — {JOB_TITLE} (Batch 1 of 2)"

    html = f"""
    <div style="font-family:Arial,sans-serif;font-size:14px;color:#1e2a38;max-width:620px">
      <div style="background:#1a7a4a;padding:20px 24px;border-radius:6px 6px 0 0">
        <h2 style="color:white;margin:0;font-size:18px">KCD Evaluation Report</h2>
        <p style="color:#d4edda;margin:4px 0 0">{JOB_TITLE} &nbsp;·&nbsp; Taleemabad &nbsp;·&nbsp; {EVAL_DATE}</p>
      </div>
      <div style="background:#f7f9fc;padding:20px 24px;border:1px solid #dfe6e9;border-top:none">
        <p style="margin:0 0 14px">Hi Ayesha and Jawwad,</p>
        <p style="margin:0 0 14px">Attached is the revised KCD evaluation report for <b>Batch 1</b> of the Field Coordinator role (4 candidates). Format upgraded — includes cross-candidate comparison, role-specific risk analysis, and hiring decision summary.</p>
        <table style="width:100%;border-collapse:collapse;margin-bottom:16px;font-size:13px">
          <tr style="background:#1e2a38;color:white">
            <th style="padding:8px 12px;text-align:left">Candidate</th>
            <th style="padding:8px 12px;text-align:center">Score</th>
            <th style="padding:8px 12px;text-align:center">Verdict</th>
            <th style="padding:8px 12px;text-align:left">In one line</th>
          </tr>
          <tr style="background:#f7f9fc">
            <td style="padding:8px 12px">Scheherazade Noor</td>
            <td style="padding:8px 12px;text-align:center"><b>100%</b></td>
            <td style="padding:8px 12px;text-align:center"><span style="background:#1a7a4a;color:white;padding:3px 9px;border-radius:4px;font-size:11px"><b>STRONG HIRE</b></span></td>
            <td style="padding:8px 12px;font-size:12px;color:#636e72">Field-native thinker. Diagnoses before acting. Only candidate who read the RCT design.</td>
          </tr>
          <tr>
            <td style="padding:8px 12px">Maria Karim</td>
            <td style="padding:8px 12px;text-align:center"><b>84%</b></td>
            <td style="padding:8px 12px;text-align:center"><span style="background:#1a5fa8;color:white;padding:3px 9px;border-radius:4px;font-size:11px"><b>HIRE</b></span></td>
            <td style="padding:8px 12px;font-size:12px;color:#636e72">Sharpest on sampling validity. Dedicated substitution tracker.</td>
          </tr>
          <tr style="background:#f7f9fc">
            <td style="padding:8px 12px">Amina Batool</td>
            <td style="padding:8px 12px;text-align:center"><b>76%</b></td>
            <td style="padding:8px 12px;text-align:center"><span style="background:#1a5fa8;color:white;padding:3px 9px;border-radius:4px;font-size:11px"><b>HIRE</b></span></td>
            <td style="padding:8px 12px;font-size:12px;color:#636e72">Pakistan-savvy, grounded. Desk-to-desk follow-up instinct is rare.</td>
          </tr>
          <tr>
            <td style="padding:8px 12px">Jalal Ud Din</td>
            <td style="padding:8px 12px;text-align:center"><b>63%</b></td>
            <td style="padding:8px 12px;text-align:center"><span style="background:#c87800;color:white;padding:3px 9px;border-radius:4px;font-size:11px"><b>CONDITIONAL</b></span></td>
            <td style="padding:8px 12px;font-size:12px;color:#636e72">Exceptional tracker, thin written analysis. Discrepancy unresolved.</td>
          </tr>
        </table>
        <p style="margin:0;color:#636e72;font-size:12px">Usman Ahmed Khan — Batch 2 pending. Report to follow once file is received.</p>
      </div>
      <div style="padding:12px 24px;font-size:11px;color:#999;text-align:center;border:1px solid #dfe6e9;border-top:none;border-radius:0 0 6px 6px">
        Warm regards, &nbsp; People and Culture Team &nbsp;·&nbsp; Taleemabad<br>
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
                   filename=f"KCD_Evaluation_FieldCoordinator_Batch1_v2_{date.today().strftime('%Y%m%d')}.pdf")
    msg.attach(att)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(SENDER, PASSWORD)
        allow_candidate_addresses(TO + CC if isinstance(TO + CC, list) else [TO + CC])
        safe_sendmail(s, SENDER, TO + CC, msg.as_string(), context='send_job36_kcd_report_v2')
    print(f"Sent to: {', '.join(TO + CC)}")

if __name__ == "__main__":
    send()
