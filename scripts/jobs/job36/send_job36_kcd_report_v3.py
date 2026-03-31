"""
Job 36 — Field Coordinator, Research & Impact Studies
KCD Case Study Evaluation Report v3
Format: Rich HTML email body (no PDF) — following Noah's Soul Architect template exactly
Pilot: TO = ayesha.khan@taleemabad.com, CC = jawwad.ali@taleemabad.com
"""

import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import date

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses


SENDER   = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
TO       = ["ayesha.khan@taleemabad.com"]
CC       = ["jawwad.ali@taleemabad.com"]
SUBJECT  = "Field Coordinator / Research & Impact Studies — Case Study Evaluation | 4 Candidates | March 2026"
EVAL_DATE = date.today().strftime("%d %B %Y")

# ── COLOUR TOKENS ─────────────────────────────────────────────────────────────
DARK     = "#1e2a38"
GREEN    = "#1a7a4a"
BLUE     = "#1a5fa8"
AMBER    = "#c87800"
RED      = "#c0392b"
MID      = "#636e72"
RULE     = "#dfe6e9"
BG       = "#f7f9fc"
WHITE    = "#ffffff"
SCORE_COLORS = {5: "#1a7a4a", 4: "#27ae60", 3: "#c87800", 2: "#e17055", 1: "#c0392b"}
VERDICT_COLORS = {
    "STRONG HIRE":     "#1a7a4a",
    "HIRE":            "#1a5fa8",
    "CONDITIONAL":     "#c87800",
    "NOT RECOMMENDED": "#c0392b",
}

# ── CANDIDATE DATA ─────────────────────────────────────────────────────────────
CRITERIA = [
    ("Field &amp; DQ Risk",    "25%"),
    ("Op. Judgment",           "25%"),
    ("Research Integrity",     "20%"),
    ("Govt Coord.",            "15%"),
    ("Tracker",                "15%"),
]
WEIGHTS = [25, 25, 20, 15, 15]

CANDIDATES = [
    {
        "rank": 1, "name": "Scheherazade Noor", "score": 100, "verdict": "STRONG HIRE", "confidence": "High",
        "tagline": "Field-native thinker who diagnoses before acting — the only candidate who read the study design correctly.",
        "scores": [5, 5, 5, 5, 5],
        "narrative": (
            "The most methodologically rigorous submission in the batch. She investigates before responding: "
            "her first instinct on seeing rushed data is to form a hypothesis ('neat-looking data is the suspicious kind') "
            "before contacting the survey firm — original field research thinking, not a manual response. "
            "Hourly 48-hr action plan (0–12 · 12–18 · 18–24 · 24–48) with explicit reasoning per block. "
            "Government coordination framed as a relationship problem, not a scheduling problem — DEO and headmaster "
            "identified as separate relationships requiring separate outreach. Named contact + deadline per approval "
            "level in her stakeholder checklist. Only candidate who put a Treatment/Control column in her tracker, "
            "recognising this is an RCT study design."
        ),
        "gap": "Tracker submitted as Google Sheet — verify that her day-to-day tracking is as functional in offline/field conditions as it is conceptually strong.",
        "integrity": "Clean. Personal, non-linear writing with visible uncertainty throughout. No AI signals.",
    },
    {
        "rank": 2, "name": "Maria Karim", "score": 84, "verdict": "HIRE", "confidence": "High",
        "tagline": "Sharpest on research validity in the batch — produced the most precise articulation of why the sampling breach matters.",
        "scores": [4, 4, 5, 4, 4],
        "narrative": (
            "Maria's conceptual clarity is her greatest strength. She produced the best sampling statement in the batch: "
            "the unauthorised school substitution 'undermines the ability of the study to draw any valid inference "
            "while comparing baseline and endline.' Her 7-sheet tracker includes a dedicated Substitution sheet "
            "labelled 'Sampling Violation' — unique across all submissions. She flagged that previous assessments "
            "from the protocol-breaching enumerator should be re-collected. DEO/AEO correctly identified as the "
            "access escalation path. Daily progress dashboard with time-flagging (Too Fast / Too Long / OK)."
        ),
        "gap": "Written responses are correct but less narratively deep than Scheherazade's. May need guidance on when to escalate vs. resolve at field level. Government correspondence language may need light coaching.",
        "integrity": "Clean. Language imperfections and an incomplete sentence in Q3 are human signals — non-native speaker under time pressure.",
    },
    {
        "rank": 3, "name": "Amina Batool", "score": 76, "verdict": "HIRE", "confidence": "High",
        "tagline": "Practically grounded with real Pakistan bureaucracy instinct — some depth gaps on research ethics.",
        "scores": [4, 4, 3, 4, 4],
        "narrative": (
            "Amina is practical and grounded. She correctly calculated expected study pace (6 schools/day, "
            "6 enumerator pairs) — a clean signal that she read the parameters. Pakistan-specific instinct: "
            "'follow up from desk to desk, best done in-person' is rare and genuine field intuition. "
            "Structured three concrete catch-up options (A/B/C) with trade-offs for the Research Lead. "
            "Tracker is formula-driven with auto-flagging (Fast/OK) and includes School Replacement and "
            "Consent as dedicated columns — directly maps to Scenarios 1 and 2. "
            "Where she falls short: she does not flag consent-compromised data to the Research Lead — a "
            "research ethics gap that matters if a data validity challenge arises post-study."
        ),
        "gap": "Did not escalate consent-compromised student data to the Research Lead. Presenting three options rather than a recommendation shows ownership hesitancy — may need coaching to default to a position.",
        "integrity": "Clean. Self-corrections and manual calculations are human signals. No AI patterns.",
    },
    {
        "rank": 4, "name": "Jalal Ud Din", "score": 63, "verdict": "CONDITIONAL", "confidence": "High",
        "tagline": "Exceptional tracker, thin written analysis — the gap between the two needs probing before advancing.",
        "scores": [3, 3, 3, 2, 5],
        "narrative": (
            "Jalal presents the most notable internal inconsistency in this batch: his tracker (6 sheets, "
            "Supervisor Observation compliance checks, DEO/AEO coordination columns, 'Sampling Integrity Affected?' "
            "risk log column) is one of the strongest submitted, while his written analysis is the weakest. "
            "He correctly identifies unauthorised substitution as a validity threat — not just a process issue. "
            "But his written responses are procedurally correct and shallow: he lists steps without showing "
            "root-cause reasoning or field judgment. For a role that requires both operational structure and "
            "field judgment, this split profile carries real risk. Advance only if the pool justifies it."
        ),
        "gap": "Main risk: may struggle to independently diagnose root causes in ambiguous field situations. Analytical thinness suggests reactive rather than preventive instincts. Would need close mentorship in first 3 months.",
        "integrity": "Low concern. 'Epic focus on ethical protocols' is unusual phrasing for otherwise plain writing. Tracker/analysis discrepancy — one of the two was likely AI-assisted. Probe explicitly at GWC.",
    },
]

# ── HTML HELPERS ───────────────────────────────────────────────────────────────
def td(content, bg=WHITE, color=DARK, bold=False, center=False, pad="8px 10px", size="13px", border=f"1px solid {RULE}"):
    fw = "bold" if bold else "normal"
    align = "center" if center else "left"
    return (f'<td style="background:{bg};color:{color};font-weight:{fw};text-align:{align};'
            f'padding:{pad};font-size:{size};border:{border};vertical-align:top">{content}</td>')

def th(content, bg=DARK, color=WHITE, center=False):
    align = "center" if center else "left"
    return (f'<th style="background:{bg};color:{color};font-weight:bold;text-align:{align};'
            f'padding:8px 10px;font-size:12px;border:1px solid {RULE}">{content}</th>')

def score_chip(val):
    bg = SCORE_COLORS.get(val, MID)
    labels = {5: "5", 4: "4", 3: "3", 2: "2", 1: "1"}
    return (f'<span style="background:{bg};color:white;font-weight:bold;font-size:12px;'
            f'padding:2px 7px;border-radius:4px">{labels[val]}</span>')

def verdict_chip(v):
    bg = VERDICT_COLORS.get(v, AMBER)
    return (f'<span style="background:{bg};color:white;font-weight:bold;font-size:11px;'
            f'padding:3px 9px;border-radius:4px;letter-spacing:0.5px">{v}</span>')

def section_header(label):
    return (f'<p style="font-size:11px;font-weight:bold;color:{BLUE};letter-spacing:1.5px;'
            f'text-transform:uppercase;margin:24px 0 8px;border-bottom:2px solid {BLUE};'
            f'padding-bottom:4px">{label}</p>')

# ── BUILD HTML ─────────────────────────────────────────────────────────────────
def build_html():
    parts = []

    # wrapper
    parts.append(f'<div style="font-family:Arial,sans-serif;max-width:900px;margin:0 auto;background:{WHITE}">')

    # ── HEADER ──
    parts.append(f'''
    <div style="background:{WHITE};padding:28px 32px;border-radius:6px 6px 0 0;border-bottom:3px solid #1565c0">
      <span style="background:#1565c0;color:{WHITE};font-size:10px;font-weight:bold;
                   padding:2px 8px;border-radius:3px;letter-spacing:1px">INTERNAL</span>
      <h1 style="color:#1565c0;font-size:26px;margin:10px 0 4px;font-weight:bold">
        Field Coordinator Case Study Evaluation</h1>
      <p style="color:{MID};margin:0 0 14px;font-size:14px">Research &amp; Impact Studies &nbsp;·&nbsp; Taleemabad</p>
      <table cellpadding="0" cellspacing="0" border="0"><tr>
        <td style="background:#e8f0fe;color:#1565c0;font-size:12px;font-weight:bold;
                   padding:4px 12px;border-radius:3px">Field Coordinator</td>
        <td style="width:8px"></td>
        <td style="background:#e8f0fe;color:#1565c0;font-size:12px;font-weight:bold;
                   padding:4px 12px;border-radius:3px">4 Candidates &nbsp;·&nbsp; Batch 1 of 2</td>
        <td style="width:8px"></td>
        <td style="background:#e8f0fe;color:#1565c0;font-size:12px;font-weight:bold;
                   padding:4px 12px;border-radius:3px">{EVAL_DATE}</td>
      </tr></table>
    </div>
    ''')

    parts.append(f'<div style="padding:24px 32px;background:{WHITE};border:1px solid {RULE};border-top:none">')

    # ── ABOUT ──
    parts.append(section_header("About This Document"))
    parts.append(f'<p style="font-size:13px;color:{DARK};line-height:1.6;margin:0 0 4px">'
                 f'This is Coco\'s evaluation of all 4 Field Coordinator case study submissions (Batch 1), '
                 f'scored against the 5-criterion framework derived from the role\'s case study assignment. '
                 f'Scores are on a 1&ndash;5 scale per criterion, weighted to a final percentage. '
                 f'Integrity flags are noted where applicable. Usman Ahmed Khan (Batch 2) pending file receipt.</p>')

    # ── SCORING FRAMEWORK ──
    parts.append(section_header("Scoring Framework"))
    parts.append('<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse;margin-bottom:4px">')
    parts.append(f'<tr>{th("Criterion")}{th("Weight", center=True)}{th("What We Evaluated")}</tr>')
    fw_rows = [
        ("Field &amp; Data Quality Risk Identification", "25%",
         "Ability to spot fabrication signals and pattern anomalies — not just flag 'data looks wrong'. "
         "Hypothesis formation before action. Distinction between speed and data quality."),
        ("Operational Judgment &amp; Survey Firm Management", "25%",
         "Knowing which lever to pull — influence vs. escalation. Response to firm non-compliance: "
         "framing, documentation, escalation chain. Hourly/phased planning."),
        ("Research Integrity &amp; Sampling Discipline", "20%",
         "Understanding of why unauthorised school substitution breaks the study. "
         "Baseline/endline comparability threat. Consent-data escalation to Research Lead."),
        ("Government &amp; Stakeholder Coordination", "15%",
         "Pakistan-specific DEO/AEO navigation. Relationship-first vs. process-first framing. "
         "Separate outreach strategies for different stakeholder types."),
        ("Tracker Design &amp; Systems Thinking", "15%",
         "Pre-emptive vs. reactive structure. Formula-driven flags. Columns that map directly "
         "to the study's specific risks (substitution, consent, sampling integrity)."),
    ]
    for i, (crit, wt, desc) in enumerate(fw_rows):
        row_bg = BG if i % 2 == 0 else WHITE
        parts.append(f'<tr>'
                     f'{td(f"<b>{crit}</b>", bg=row_bg)}'
                     f'{td(wt, bg=row_bg, center=True, bold=True, color=BLUE)}'
                     f'{td(desc, bg=row_bg, size="12px", color=MID)}'
                     f'</tr>')
    parts.append('</table>')

    # ── SCORES AT A GLANCE ──
    parts.append(section_header("Scores at a Glance"))
    parts.append('<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse">')
    header_cells = th("Candidate")
    for crit, wt in CRITERIA:
        header_cells += th(f'{crit}<br><span style="font-weight:normal;font-size:10px">{wt}</span>', center=True)
    header_cells += th("Total", center=True)
    header_cells += th("Verdict")
    parts.append(f'<tr>{header_cells}</tr>')

    for i, c in enumerate(CANDIDATES):
        row_bg = BG if i % 2 == 0 else WHITE
        cells = td(f'<b>{c["name"]}</b>', bg=row_bg)
        for sc in c["scores"]:
            cells += td(score_chip(sc), bg=row_bg, center=True)
        vc = VERDICT_COLORS[c["verdict"]]
        cells += td(f'<b style="color:{vc}">{c["score"]}%</b>', bg=row_bg, center=True)
        cells += td(verdict_chip(c["verdict"]), bg=row_bg)
        parts.append(f'<tr>{cells}</tr>')

    parts.append(f'<tr><td colspan="8" style="padding:6px 10px;font-size:11px;color:{MID};'
                 f'background:{BG};border:1px solid {RULE}">'
                 f'5 = exceptional &nbsp;|&nbsp; 4 = strong &nbsp;|&nbsp; 3 = adequate &nbsp;|&nbsp; '
                 f'2 = weak &nbsp;|&nbsp; 1 = absent</td></tr>')
    parts.append('</table>')

    # ── CANDIDATE EVALUATIONS ──
    parts.append(section_header("Candidate Evaluations"))

    for c in CANDIDATES:
        vc  = VERDICT_COLORS[c["verdict"]]
        # candidate header bar
        parts.append(f'''
        <table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse;margin-bottom:0">
          <tr>
            <td style="background:{vc};padding:12px 16px;border-radius:4px 4px 0 0">
              <span style="color:{WHITE};font-size:16px;font-weight:bold">
                #{c["rank"]} &nbsp; {c["name"]}</span>
            </td>
            <td style="background:{vc};padding:12px 16px;text-align:right;border-radius:4px 4px 0 0">
              <span style="color:{WHITE};font-size:13px;font-weight:bold">{c["score"]}%</span>
              &nbsp;
              <span style="background:rgba(255,255,255,0.2);color:{WHITE};font-size:11px;
                           font-weight:bold;padding:3px 9px;border-radius:3px">{c["verdict"]}</span>
              &nbsp;
              <span style="color:rgba(255,255,255,0.7);font-size:11px">Confidence: {c["confidence"]}</span>
            </td>
          </tr>
        </table>
        ''')
        # tagline
        parts.append(f'<div style="background:{BG};border-left:3px solid {vc};'
                     f'padding:8px 14px;font-style:italic;font-size:13px;color:{MID};'
                     f'border-right:1px solid {RULE};border-bottom:1px solid {RULE}">'
                     f'{c["tagline"]}</div>')
        # criterion scores inline
        score_chips = ''.join(
            f'<td style="padding:4px 8px;text-align:center">'
            f'<div style="font-size:10px;color:{MID};margin-bottom:2px">{CRITERIA[j][0]}</div>'
            f'{score_chip(c["scores"][j])}</td>'
            for j in range(len(CRITERIA))
        )
        parts.append(f'<div style="background:{WHITE};border:1px solid {RULE};border-top:none;padding:12px 14px">')
        parts.append(f'<table cellpadding="0" cellspacing="0" border="0" style="margin-bottom:12px"><tr>{score_chips}</tr></table>')
        # narrative
        parts.append(f'<p style="font-size:13px;color:{DARK};line-height:1.7;margin:0 0 10px">{c["narrative"]}</p>')
        # gap
        parts.append(f'<div style="background:#fff8e6;border-left:3px solid {AMBER};padding:8px 12px;'
                     f'margin-bottom:8px;font-size:12px;color:{DARK}">'
                     f'<b style="color:{AMBER}">Gap:</b> {c["gap"]}</div>')
        # integrity
        int_bg = "#fff8e6" if "concern" in c["integrity"].lower() or "probe" in c["integrity"].lower() else BG
        int_border = AMBER if "concern" in c["integrity"].lower() or "probe" in c["integrity"].lower() else RULE
        parts.append(f'<div style="background:{int_bg};border-left:3px solid {int_border};padding:8px 12px;'
                     f'font-size:12px;color:{MID}">'
                     f'<b>Integrity Check:</b> {c["integrity"]}</div>')
        parts.append('</div>')
        parts.append('<div style="height:16px"></div>')

    # ── INTEGRITY FLAGS ──
    parts.append(section_header("Integrity Flags"))
    parts.append('<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse">')
    parts.append(f'<tr>{th("Candidate")}{th("Signal")}{th("Severity")}</tr>')
    flags = [
        ("Jalal Ud Din",
         "6-sheet tracker (Supervisor Observation compliance checks, DEO/AEO columns, 'Sampling Integrity Affected?' "
         "risk log) is structurally the strongest in the batch. Written analysis is the weakest — procedurally "
         "correct, no root-cause reasoning, generic action items. Internal inconsistency of this magnitude "
         "suggests one of the two was AI-assisted. Phrase 'epic focus on ethical protocols' is an outlier in "
         "otherwise plain writing.",
         "Low concern — probe at GWC"),
        ("All others",
         "Clean. No AI content dump signals, no mirroring across candidates, no foundational misreads.",
         "None"),
    ]
    for i, (name, signal, severity) in enumerate(flags):
        row_bg = "#fff8e6" if i == 0 else BG
        parts.append(f'<tr>'
                     f'{td(f"<b>{name}</b>", bg=row_bg)}'
                     f'{td(signal, bg=row_bg, size="12px")}'
                     f'{td(severity, bg=row_bg, size="12px", color=AMBER if i == 0 else MID)}'
                     f'</tr>')
    parts.append('</table>')

    # ── PIPELINE RECOMMENDATIONS ──
    parts.append(section_header("Pipeline Recommendations"))
    parts.append('<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse">')
    parts.append(f'<tr>{th("Candidate")}{th("Current Stage")}{th("Recommendation")}</tr>')
    pipeline = [
        ("Scheherazade Noor",  "KCD evaluated",                                          GREEN,
         "Advance to GWC — no conditions."),
        ("Maria Karim",        "KCD evaluated",                                          GREEN,
         "Advance to GWC — no conditions."),
        ("Amina Batool",       "KCD evaluated",                                          BLUE,
         "Advance to GWC — note consent-data escalation gap; probe at GWC."),
        ("Jalal Ud Din",       "KCD evaluated",                                          AMBER,
         "CONDITIONAL — advance only if pool is thin. Probe tracker/analysis discrepancy explicitly at GWC."),
        ("Usman Ahmed Khan",   "Submission confirmed on Markaz (25 Mar 2026)",           MID,
         "Awaiting local file — Batch 2 supplementary report to follow."),
    ]
    for i, (name, stage, vc, rec) in enumerate(pipeline):
        row_bg = BG if i % 2 == 0 else WHITE
        parts.append(f'<tr>'
                     f'{td(f"<b style=\'color:{vc}\'>{name}</b>", bg=row_bg)}'
                     f'{td(stage, bg=row_bg, size="12px", color=MID)}'
                     f'{td(rec, bg=row_bg, size="13px")}'
                     f'</tr>')
    parts.append('</table>')

    # ── FOOTER ──
    parts.append(f'''
    <div style="margin-top:32px;padding-top:16px;border-top:1px solid {RULE};
                font-size:12px;color:{MID};text-align:center">
      Warm regards &nbsp;·&nbsp; People and Culture Team &nbsp;·&nbsp; Taleemabad<br>
      <a href="mailto:hiring@taleemabad.com" style="color:{BLUE}">hiring@taleemabad.com</a>
      &nbsp;|&nbsp;
      <a href="http://www.taleemabad.com" style="color:{BLUE}">www.taleemabad.com</a><br>
      <span style="color:#b2bec3">Sent on behalf of Talent Acquisition Team by Coco</span>
    </div>
    ''')

    parts.append('</div></div>')  # close padding div + wrapper
    return ''.join(parts)


# ── SEND ───────────────────────────────────────────────────────────────────────
def send():
    html = build_html()

    msg = MIMEMultipart("alternative")
    msg["From"]    = SENDER
    msg["To"]      = ", ".join(TO)
    msg["CC"]      = ", ".join(CC)
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(html, "html"))

    all_recipients = TO + CC
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        allow_candidate_addresses(all_recipients if isinstance(all_recipients, list) else [all_recipients])
        safe_sendmail(server, SENDER, all_recipients, msg.as_string(), context='send_job36_kcd_report_v3')

    print(f"Sent to: {', '.join(all_recipients)}")


if __name__ == "__main__":
    send()
