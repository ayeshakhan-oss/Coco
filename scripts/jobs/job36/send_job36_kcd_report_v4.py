"""
Job 36 — Field Coordinator, Research & Impact Studies
KCD Case Study Evaluation Report v4 — Full Batch (8 candidates)
Format: Rich HTML email body (no PDF) — Noah's Soul Architect template
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


SENDER    = os.getenv("EMAIL_USER")
PASSWORD  = os.getenv("EMAIL_PASSWORD")
TO        = ["ayesha.khan@taleemabad.com"]
CC        = ["jawwad.ali@taleemabad.com"]
SUBJECT   = "Field Coordinator / Research & Impact Studies — KCD Evaluation | 8 Candidates | Full Batch | March 2026"
EVAL_DATE = date.today().strftime("%d %B %Y")

# ── COLOUR TOKENS ─────────────────────────────────────────────────────────────
DARK   = "#1e2a38"
GREEN  = "#1a7a4a"
BLUE   = "#1565c0"
AMBER  = "#c87800"
RED    = "#c0392b"
MID    = "#636e72"
RULE   = "#dfe6e9"
BG     = "#f7f9fc"
WHITE  = "#ffffff"
SCORE_COLORS   = {5: "#1a7a4a", 4: "#27ae60", 3: "#c87800", 2: "#e17055", 1: "#c0392b"}
VERDICT_COLORS = {
    "STRONG HIRE":       "#1a7a4a",
    "HIRE":              "#1565c0",
    "HIRE (Prov.)":      "#1565c0",
    "CONDITIONAL":       "#c87800",
    "NOT RECOMMENDED":   "#c0392b",
}

# ── CRITERIA ──────────────────────────────────────────────────────────────────
CRITERIA = [
    ("Field &amp; DQ Risk",  "25%"),
    ("Op. Judgment",         "25%"),
    ("Research Integrity",   "20%"),
    ("Govt Coord.",          "15%"),
    ("Tracker",              "15%"),
]
WEIGHTS = [25, 25, 20, 15, 15]

# ── CANDIDATE DATA ─────────────────────────────────────────────────────────────
# scores: [DQ Risk, Op Judge, Research Int, Govt, Tracker] — None = not evaluated
CANDIDATES = [
    {
        "rank": 1, "name": "Scheherazade Noor", "score": 100, "score_label": "100%",
        "verdict": "STRONG HIRE", "confidence": "High",
        "stage": "KCD evaluated",
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
            "recognising this is an RCT study design. Consent escalation documented in-tracker to Research Lead."
        ),
        "gap": "Tracker submitted as Google Sheet — verify that her day-to-day tracking is as functional in offline/field conditions as it is conceptually strong.",
        "integrity": "Clean. Personal, non-linear writing with visible uncertainty throughout. No AI signals.",
    },
    {
        "rank": 2, "name": "Maria Karim", "score": 84, "score_label": "84%",
        "verdict": "HIRE", "confidence": "High",
        "stage": "KCD evaluated",
        "tagline": "Sharpest on research validity in the batch — produced the most precise articulation of why the sampling breach matters.",
        "scores": [4, 4, 5, 4, 4],
        "narrative": (
            "Maria's conceptual clarity is her greatest strength. She produced the best sampling statement in the batch: "
            "the unauthorised school substitution 'undermines the ability of the study to draw any valid inference "
            "while comparing baseline and endline.' Her 7-sheet tracker includes a dedicated Substitution sheet "
            "labelled 'Sampling Violation' — unique across all submissions. She flagged that previous assessments "
            "from the protocol-breaching enumerator should be re-collected. DEO/AEO correctly identified as the "
            "access escalation path. Daily progress dashboard with time-flagging formula (Too Fast / Too Long / OK)."
        ),
        "gap": "Written responses are correct but less narratively deep than Scheherazade's. May need guidance on when to escalate vs. resolve at field level.",
        "integrity": "Clean. Language imperfections and an incomplete sentence in Q3 are human signals — non-native speaker under time pressure.",
    },
    {
        "rank": 3, "name": "Moiz Khan", "score": 83, "score_label": "83%",
        "verdict": "HIRE", "confidence": "High",
        "stage": "GWC done",
        "tagline": "Strongest tracker in the batch — systems thinking translates directly into field architecture.",
        "scores": [4, 4, 4, 4, 5],
        "narrative": (
            "Moiz's primary strength is structural: his tracker is the most operationally comprehensive submitted — "
            "pre-built for the study's specific risks with formula-driven flags, dedicated sheets for enumerator "
            "compliance and school substitution, and clear escalation triggers. His written analysis is solid across "
            "all criteria: he correctly identifies the sampling breach as a validity threat, maps the DEO/AEO "
            "escalation path, and sequences his operational response clearly. Where he does not reach the top tier: "
            "his field judgment responses are competent but lack the diagnostic depth of Scheherazade or the research "
            "precision of Maria. He responds correctly but does not show the hypothesis-first instinct that separates "
            "a field coordinator from a field executor."
        ),
        "gap": "Written analysis is correct but not investigative — he answers what to do without showing how he arrived at the diagnosis. Probe independent judgment at GWC.",
        "integrity": "Clean. No AI signals. Tracker sophistication is consistent with written work.",
    },
    {
        "rank": 4, "name": "Amina Batool", "score": 76, "score_label": "76%",
        "verdict": "HIRE", "confidence": "High",
        "stage": "KCD evaluated",
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
        "rank": 5, "name": "Shazmina", "score": 73, "score_label": "73%",
        "verdict": "HIRE", "confidence": "Medium",
        "stage": "GWC done",
        "tagline": "Field-competent and operationally reliable — research integrity framing needs sharpening.",
        "scores": [4, 4, 3, 4, 3],
        "narrative": (
            "Shazmina demonstrates genuine field instinct: her risk identification is practical and "
            "grounded in what actually breaks during data collection in Pakistan — enumerator incentive "
            "drift, access friction at the school level, and timeline slippage from government approvals. "
            "Her operational response is well-sequenced and she correctly maps the DEO/AEO coordination path. "
            "Where she is weaker: her framing of the sampling breach stays at the process level ('the school "
            "should have been approved first') without reaching the validity-level argument (the breach "
            "compromises baseline-endline comparability). Her tracker is functional but not pre-emptively "
            "structured — flags are manual rather than formula-driven, and it lacks a dedicated substitution or "
            "consent sheet."
        ),
        "gap": "Research integrity reasoning stays procedural rather than methodological. Tracker needs formula-driven flagging to operate reliably under field pressure. Both are coachable with mentorship in the first 2–3 months.",
        "integrity": "Clean. No AI signals. Writing is direct and personal throughout.",
    },
    {
        "rank": 6, "name": "Usman Ahmed Khan", "score": 71, "score_label": "71% (prov.)",
        "verdict": "HIRE (Prov.)", "confidence": "Medium",
        "stage": "Tracker pending",
        "tagline": "Strong on field judgment and research framing — score is provisional pending tracker review.",
        "scores": [4, 4, 3, 3, None],
        "narrative": (
            "Usman's written submission shows solid field judgment. He identifies fabrication signals "
            "correctly and frames his operational response in a clear sequence. His government coordination "
            "thinking is adequate — he names the DEO escalation path and understands the relationship-first "
            "dynamic, but does not differentiate between stakeholder types as precisely as the top candidates. "
            "His research integrity framing is correct at the process level but does not reach the "
            "validity-level consequence of the sampling breach. "
            "Score is provisional (71%) based on 4 evaluated criteria (DQ Risk 4, Op. Judgment 4, "
            "Research Integrity 3, Govt Coordination 3). Tracker was submitted on Markaz but the attached "
            "file was not available in the hiring@ inbox — full score pending receipt."
        ),
        "gap": "Tracker not yet evaluated — final score may shift. Government coordination framing is adequate but not differentiated. Probe field experience depth at GWC.",
        "integrity": "Clean based on written submission. Tracker integrity pending review.",
    },
    {
        "rank": 7, "name": "Jalal Ud Din", "score": 60, "score_label": "60%",
        "verdict": "CONDITIONAL", "confidence": "High",
        "stage": "KCD evaluated",
        "tagline": "Exceptional tracker, thin written analysis — the gap between the two needs probing before advancing.",
        "scores": [3, 3, 3, 2, 4],
        "narrative": (
            "Jalal presents the most notable internal inconsistency in this batch: his tracker (6 sheets, "
            "Supervisor Observation compliance checks, DEO/AEO coordination columns, 'Sampling Integrity Affected?' "
            "risk log column) is structurally strong, while his written analysis is the weakest. "
            "He correctly identifies unauthorised substitution as a validity threat — not just a process issue. "
            "But his written responses are procedurally correct and shallow: he lists steps without showing "
            "root-cause reasoning or field judgment. The tracker has no auto-flagging formulas — percentage "
            "calculations only — which limits its operational value under real field pressure. "
            "For a role that requires both operational structure and field judgment, this split profile carries real risk."
        ),
        "gap": "Main risk: may struggle to independently diagnose root causes in ambiguous field situations. Analytical thinness suggests reactive rather than preventive instincts. Would need close mentorship in first 3 months.",
        "integrity": "Low concern. 'Epic focus on ethical protocols' is an outlier phrase in otherwise plain writing. Tracker/analysis discrepancy — one of the two was likely AI-assisted. Probe explicitly at GWC.",
    },
    {
        "rank": 8, "name": "Muhammad Abubakr", "score": 60, "score_label": "60%",
        "verdict": "CONDITIONAL", "confidence": "High",
        "stage": "GWC done",
        "tagline": "Consistently adequate across all criteria — no critical gaps, but no standout strengths either.",
        "scores": [3, 3, 3, 3, 3],
        "narrative": (
            "Abubakr's submission is uniformly competent: he addresses each scenario correctly, identifies "
            "the right escalation path, and structures his tracker logically. What is absent is depth. "
            "His risk identification stops at the surface (data looks wrong → contact firm) without "
            "forming a hypothesis about why. His government coordination response is procedurally "
            "accurate but generic — no Pakistan-specific instinct, no differentiation between DEO and "
            "headmaster relationships. His tracker is functional but reactive: columns map to what "
            "happened rather than what could go wrong. In a batch with four candidates scoring in the "
            "HIRE range, he does not differentiate above the conditional threshold."
        ),
        "gap": "Across-the-board adequacy without depth. In a competitive pool this scores CONDITIONAL. Would need a significantly stronger GWC to advance. Probe whether the surface-level responses reflect the submission or genuinely reflect his analytical ceiling.",
        "integrity": "Clean. No AI signals. Consistent voice throughout — adequacy appears genuine.",
    },
]


# ── HTML HELPERS ───────────────────────────────────────────────────────────────
def td(content, bg=WHITE, color=DARK, bold=False, center=False, pad="8px 10px", size="13px",
       border=None):
    if border is None:
        border = f"1px solid {RULE}"
    fw = "bold" if bold else "normal"
    align = "center" if center else "left"
    return (f'<td style="background:{bg};color:{color};font-weight:{fw};text-align:{align};'
            f'padding:{pad};font-size:{size};border:{border};vertical-align:top">{content}</td>')

def th(content, bg=DARK, color=WHITE, center=False):
    align = "center" if center else "left"
    return (f'<th style="background:{bg};color:{color};font-weight:bold;text-align:{align};'
            f'padding:8px 10px;font-size:12px;border:1px solid {RULE}">{content}</th>')

def score_chip(val):
    if val is None:
        return (f'<span style="background:{MID};color:white;font-weight:bold;font-size:12px;'
                f'padding:2px 7px;border-radius:4px">—</span>')
    bg = SCORE_COLORS.get(val, MID)
    return (f'<span style="background:{bg};color:white;font-weight:bold;font-size:12px;'
            f'padding:2px 7px;border-radius:4px">{val}</span>')

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
    parts.append(f'<div style="font-family:Arial,sans-serif;max-width:940px;margin:0 auto;background:{WHITE}">')

    # ── HEADER ──
    parts.append(f'''
    <div style="background:{WHITE};padding:28px 32px;border-radius:6px 6px 0 0;border-bottom:3px solid {BLUE}">
      <span style="background:{BLUE};color:{WHITE};font-size:10px;font-weight:bold;
                   padding:2px 8px;border-radius:3px;letter-spacing:1px">INTERNAL</span>
      <h1 style="color:{BLUE};font-size:26px;margin:10px 0 4px;font-weight:bold">
        Field Coordinator Case Study Evaluation</h1>
      <p style="color:{MID};margin:0 0 14px;font-size:14px">Research &amp; Impact Studies &nbsp;&middot;&nbsp; Taleemabad</p>
      <table cellpadding="0" cellspacing="0" border="0"><tr>
        <td style="background:#e8f0fe;color:{BLUE};font-size:12px;font-weight:bold;
                   padding:4px 12px;border-radius:3px">Field Coordinator</td>
        <td style="width:8px"></td>
        <td style="background:#e8f0fe;color:{BLUE};font-size:12px;font-weight:bold;
                   padding:4px 12px;border-radius:3px">8 Candidates &nbsp;&middot;&nbsp; Full Batch</td>
        <td style="width:8px"></td>
        <td style="background:#e8f0fe;color:{BLUE};font-size:12px;font-weight:bold;
                   padding:4px 12px;border-radius:3px">{EVAL_DATE}</td>
      </tr></table>
    </div>
    ''')

    parts.append(f'<div style="padding:24px 32px;background:{WHITE};border:1px solid {RULE};border-top:none">')

    # ── ABOUT ──
    parts.append(section_header("About This Document"))
    parts.append(f'<p style="font-size:13px;color:{DARK};line-height:1.6;margin:0 0 4px">'
                 f'Full-batch KCD evaluation for Job 36 Field Coordinator — Research &amp; Impact Studies. '
                 f'8 candidates evaluated across 5 weighted criteria. Scores use a 1&ndash;5 scale per criterion. '
                 f'Moiz Khan, Shazmina, and Muhammad Abubakr completed GWC calls before case study submission; '
                 f'their KCD scores reflect the written submission only, independent of GWC outcomes. '
                 f'Usman Ahmed Khan score is provisional (71%) pending tracker file receipt — '
                 f'4 of 5 criteria scored.</p>')

    # ── SCORING FRAMEWORK ──
    parts.append(section_header("Scoring Framework"))
    parts.append(f'<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse;margin-bottom:4px">')
    parts.append(f'<tr>{th("Criterion")}{th("Weight", center=True)}{th("What We Evaluated")}</tr>')
    fw_rows = [
        ("Field &amp; Data Quality Risk Identification", "25%",
         "Ability to spot fabrication signals and pattern anomalies — not just flag 'data looks wrong'. "
         "Hypothesis formation before action. Distinction between speed signals and data quality signals."),
        ("Operational Judgment &amp; Survey Firm Management", "25%",
         "Knowing which lever to pull — influence vs. escalation. Response to firm non-compliance: "
         "framing, documentation, escalation chain. Phased planning with explicit reasoning per block."),
        ("Research Integrity &amp; Sampling Discipline", "20%",
         "Understanding of why unauthorised school substitution breaks the study — not just process, "
         "but baseline/endline comparability. Consent-data escalation to Research Lead."),
        ("Government &amp; Stakeholder Coordination", "15%",
         "Pakistan-specific DEO/AEO navigation. Relationship-first vs. process-first framing. "
         "Differentiated outreach strategies for different stakeholder types."),
        ("Tracker Design &amp; Systems Thinking", "15%",
         "Pre-emptive vs. reactive structure. Formula-driven flags. Columns that map directly "
         "to the study's specific risks (substitution, consent, sampling integrity, enumerator compliance)."),
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
    parts.append(f'<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse">')
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
        cells += td(f'<b style="color:{vc}">{c["score_label"]}</b>', bg=row_bg, center=True)
        cells += td(verdict_chip(c["verdict"]), bg=row_bg)
        parts.append(f'<tr>{cells}</tr>')

    parts.append(f'<tr><td colspan="8" style="padding:6px 10px;font-size:11px;color:{MID};'
                 f'background:{BG};border:1px solid {RULE}">'
                 f'5 = exceptional &nbsp;|&nbsp; 4 = strong &nbsp;|&nbsp; 3 = adequate &nbsp;|&nbsp; '
                 f'2 = weak &nbsp;|&nbsp; 1 = absent &nbsp;|&nbsp; — = not yet evaluated</td></tr>')
    parts.append('</table>')

    # ── CANDIDATE EVALUATIONS ──
    parts.append(section_header("Candidate Evaluations"))

    for c in CANDIDATES:
        vc = VERDICT_COLORS[c["verdict"]]
        # candidate header bar
        parts.append(f'''
        <table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse;margin-bottom:0">
          <tr>
            <td style="background:{vc};padding:12px 16px;border-radius:4px 4px 0 0">
              <span style="color:{WHITE};font-size:16px;font-weight:bold">
                #{c["rank"]} &nbsp; {c["name"]}</span>
            </td>
            <td style="background:{vc};padding:12px 16px;text-align:right;border-radius:4px 4px 0 0">
              <span style="color:{WHITE};font-size:13px;font-weight:bold">{c["score_label"]}</span>
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
        int_concern = any(w in c["integrity"].lower() for w in ("concern", "probe", "discrepancy", "pending"))
        int_bg     = "#fff8e6" if int_concern else BG
        int_border = AMBER     if int_concern else RULE
        parts.append(f'<div style="background:{int_bg};border-left:3px solid {int_border};padding:8px 12px;'
                     f'font-size:12px;color:{MID}">'
                     f'<b>Integrity Check:</b> {c["integrity"]}</div>')
        parts.append('</div>')
        parts.append('<div style="height:16px"></div>')

    # ── INTEGRITY FLAGS ──
    parts.append(section_header("Integrity Flags"))
    parts.append(f'<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse">')
    parts.append(f'<tr>{th("Candidate")}{th("Signal")}{th("Severity")}</tr>')
    flags = [
        ("Jalal Ud Din",
         "6-sheet tracker (Supervisor Observation compliance checks, DEO/AEO columns, 'Sampling Integrity Affected?' "
         "risk log) is structurally strong. Written analysis is the weakest in the batch — procedurally correct, "
         "no root-cause reasoning. Phrase 'epic focus on ethical protocols' is an outlier in otherwise plain writing. "
         "Tracker/analysis discrepancy of this magnitude suggests one of the two was AI-assisted.",
         "Low concern — probe explicitly at GWC"),
        ("Usman Ahmed Khan",
         "Tracker file not received — cannot complete integrity check on tracker. Written submission is clean.",
         "Pending — flag if tracker is unavailable by EOD"),
        ("All others",
         "Clean. No AI content dump signals, no mirroring across candidates, no foundational misreads.",
         "None"),
    ]
    for i, (name, signal, severity) in enumerate(flags):
        row_bg = "#fff8e6" if i < 2 else BG
        sev_color = AMBER if i < 2 else MID
        parts.append(f'<tr>'
                     f'{td(f"<b>{name}</b>", bg=row_bg)}'
                     f'{td(signal, bg=row_bg, size="12px")}'
                     f'{td(severity, bg=row_bg, size="12px", color=sev_color)}'
                     f'</tr>')
    parts.append('</table>')

    # ── PIPELINE RECOMMENDATIONS ──
    parts.append(section_header("Pipeline Recommendations"))
    parts.append(f'<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse">')
    parts.append(f'<tr>{th("Candidate")}{th("Current Stage")}{th("Recommendation")}</tr>')
    pipeline = [
        ("Scheherazade Noor",  "KCD evaluated",                GREEN,
         "Advance to GWC — no conditions."),
        ("Maria Karim",        "KCD evaluated",                GREEN,
         "Advance to GWC — no conditions."),
        ("Moiz Khan",          "GWC done",                     BLUE,
         "KCD clears at HIRE (83%). Consolidate GWC outcome with KCD score for final decision."),
        ("Amina Batool",       "KCD evaluated",                BLUE,
         "Advance to GWC — probe consent-data escalation gap and ownership instinct."),
        ("Shazmina",           "GWC done",                     BLUE,
         "KCD clears at HIRE (73%). Research integrity framing is coachable. Consolidate with GWC outcome."),
        ("Usman Ahmed Khan",   "Tracker pending",              MID,
         "Hold advancement until tracker received and scored. Written submission supports HIRE provisionally."),
        ("Jalal Ud Din",       "KCD evaluated",                AMBER,
         "CONDITIONAL — advance only if pool is thin. Probe tracker/analysis discrepancy explicitly at GWC."),
        ("Muhammad Abubakr",   "GWC done",                     AMBER,
         "CONDITIONAL — 60% in a competitive batch. Consolidate with GWC outcome before deciding."),
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
      Warm regards &nbsp;&middot;&nbsp; People and Culture Team &nbsp;&middot;&nbsp; Taleemabad<br>
      <a href="mailto:hiring@taleemabad.com" style="color:{BLUE}">hiring@taleemabad.com</a>
      &nbsp;|&nbsp;
      <a href="http://www.taleemabad.com" style="color:{BLUE}">www.taleemabad.com</a><br>
      <span style="color:#b2bec3">Sent on behalf of Talent Acquisition Team by Coco</span>
    </div>
    ''')

    parts.append('</div></div>')
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
        safe_sendmail(server, SENDER, all_recipients, msg.as_string(), context='send_job36_kcd_report_v4')

    print(f"Sent to: {', '.join(all_recipients)}")


if __name__ == "__main__":
    send()
