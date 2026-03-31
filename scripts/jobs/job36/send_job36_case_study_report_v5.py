"""
Job 36 — Field Coordinator, Research & Impact Studies
Case Study Analysis & Evaluation Report v5 — Full Batch (10 candidates)
Format: Rich HTML email body
TO = ayesha.khan@taleemabad.com | CC = jawwad.ali@taleemabad.com
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
SUBJECT   = "Field Coordinator / Research & Impact Studies — Case Study Evaluation | 10 Candidates | March 2026 (Updated)"
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
    "BORDERLINE":        "#e17055",
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
            "Hourly 48-hr action plan (0-12 · 12-18 · 18-24 · 24-48) with explicit reasoning per block. "
            "Government coordination framed as a relationship problem, not a scheduling problem — DEO and headmaster "
            "identified as separate relationships requiring separate outreach. Named contact and deadline per approval "
            "level in her stakeholder checklist. Only candidate who put a Treatment/Control column in her tracker, "
            "recognising this is an RCT study design. Consent escalation documented in-tracker to Research Lead."
        ),
        "gap": "Tracker submitted as Excel — structurally exceptional (Treatment/Control column, formula-driven flags, 5 dedicated sheets). One thing to verify at GWC: her 48-hr plan is built around ideal information flow. In real field conditions, data from the firm is often delayed or incomplete. Probe how she makes decisions when the monitoring dashboard is behind by a day or two.",
        "integrity": "Clean. Personal, non-linear writing with visible uncertainty throughout. No AI signals.",
    },
    {
        "rank": 2, "name": "Maria Karim", "score": 84, "score_label": "84%",
        "verdict": "HIRE", "confidence": "High",
        "stage": "Case study evaluated",
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
        "gap": "Written responses are correct but thinner on reasoning — she states the right action without always showing how she arrived at it. In Scenario 3, her response ends abruptly mid-sentence ('ensure that district education officials are firmly informed at the very start of any future studies who school receive talk down') suggesting she ran out of time or space. The gap to probe at GWC: when does she escalate to the Research Lead vs. handle independently? Her submission doesn't show that boundary clearly.",
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
        "gap": "Written analysis is correct but not investigative — he lists the right steps without showing how he diagnosed the problem. For example, on the fast-completion schools he goes straight to 'send a supervisor for an unannounced visit' without first forming a hypothesis about what might be happening. At GWC, probe whether he can think out loud through an ambiguous field scenario, not just name the correct procedure.",
        "integrity": "Clean. No AI signals. Tracker sophistication is consistent with written work.",
    },
    {
        "rank": 4, "name": "Amina Batool", "score": 76, "score_label": "76%",
        "verdict": "HIRE", "confidence": "High",
        "stage": "Case study evaluated",
        "tagline": "Practically grounded with real Pakistan bureaucracy instinct — some depth gaps on research ethics.",
        "scores": [4, 4, 3, 4, 4],
        "narrative": (
            "Amina is practical and grounded. She correctly calculated expected study pace (6 schools/day, "
            "6 enumerator pairs) — a clean signal that she read the parameters. Pakistan-specific instinct: "
            "'follow up from desk to desk, best done in-person' is rare and genuine field intuition. "
            "Structured three concrete catch-up options (A/B/C) with trade-offs for the Research Lead. "
            "Tracker submitted as Google Sheet — formula-driven with auto-flagging and includes School Replacement "
            "and Consent as dedicated columns — directly maps to Scenarios 1 and 2. "
            "Where she falls short: she does not flag consent-compromised data to the Research Lead — a "
            "research ethics gap that matters if a data validity challenge arises post-study."
        ),
        "gap": "Two gaps worth probing at GWC. First: she does not flag the consent-compromised student data to the Research Lead — she corrects the enumerator and moves on, but data collected without informed consent has ethical and legal implications that sit above field coordinator authority. Second: on the 12 missed schools she presents three options (A/B/C) and defers the decision to the Research Lead rather than making a recommendation. In the field, the Research Lead expects a suggested path, not a menu. Probe whether this is ownership hesitancy or appropriate deference.",
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
        "gap": "Her framing of the sampling breach stays procedural ('the school should have been approved first') rather than reaching the validity-level consequence (an unapproved substitution breaks baseline-endline comparability and may invalidate the comparison group). This is the distinction between a field operator and a field researcher. Her tracker is functional but flags are entered manually — under real field pressure with 12 enumerators across 120 schools, manual flagging gets missed. Both are coachable gaps, not disqualifying ones.",
        "integrity": "Clean. No AI signals. Writing is direct and personal throughout.",
    },
    {
        "rank": 6, "name": "Usman Ahmed Khan", "score": 71, "score_label": "71% (prov.)",
        "verdict": "HIRE (Prov.)", "confidence": "Medium",
        "stage": "Tracker pending",
        "tagline": "Strong on field judgment and research framing — score is provisional pending tracker review.",
        "scores": [5, 5, 5, 4, None],
        "narrative": (
            "Usman's written submission is the second strongest in the batch — his risk analysis is thorough, "
            "cross-referencing the high-output enumerators against the fast-completion schools as a connected "
            "signal. He names the sampling breach as a 'major protocol breach' with explicit validity consequences. "
            "His 48-hr plan is time-bound and escalation-aware. In Scenario 2, he stops the session immediately "
            "and correctly flags consent-compromised data to the Research Lead. Government coordination is "
            "adequate — names AEO as the correct escalation point and proposes a live coordination tracker. "
            "Score is provisional (71%) based on 4 evaluated criteria. Tracker was submitted on Markaz but "
            "the file was not available in the hiring@ inbox — full score pending receipt."
        ),
        "gap": "Tracker file exists on Markaz but was not accessible via the hiring inbox — score is provisional at 71% across 4 of 5 criteria. The one written gap worth probing: in Scenario 3, he correctly names the AEO as the escalation point but does not distinguish who should make that call. Outreach to government officials should come from Taleemabad directly, not from the survey firm — a subtle but important relationship boundary that the top candidates flagged explicitly.",
        "integrity": "Clean based on written submission. Tracker integrity pending review.",
    },
    {
        "rank": 7, "name": "Asad Farooq", "score": 66, "score_label": "66%",
        "verdict": "CONDITIONAL", "confidence": "Medium",
        "stage": "Case study evaluated",
        "tagline": "Empathetic framing and strong tracker — written analysis lacks the investigative depth of the top tier.",
        "scores": [3, 3, 3, 4, 4],
        "narrative": (
            "Asad's submission is technically correct across all criteria — he identifies the right flags, "
            "maps the right escalation path, and his tracker is well-organised (8 sheets: Dashboard, School Data, "
            "Enumerator Data, DQ Log, Risk Log, Daily Log, Chart Data, Instructions). His government coordination "
            "stands out: he correctly names MoFEPT as Taleemabad's leverage point and proposes a personal visit "
            "to the DEO with the Research Lead — specific and actionable. Where he falls short is investigative "
            "depth. His responses are framed around 'empathetic engagement' with the survey firm, which softens "
            "the urgency needed when data integrity is at risk. His proposal to pause all fieldwork for refresher "
            "training when the team is already 40% behind is an operational misjudgment — the right call is "
            "targeted retraining of flagged enumerators, not a full stop."
        ),
        "gap": "Two specific gaps. First: in Scenario 1, he proposes pausing all fieldwork for refresher training when the team is already 40% behind — this would compound the timeline problem, not solve it. The right call is targeted retraining of the flagged enumerators while the rest of the team continues. Second: his research integrity framing on the sampling breach stays at the process level ('unauthorized replacements would be strictly halted') without naming why it matters — that an unapproved substitution breaks the comparability of baseline and endline data. At GWC, probe whether the 'empathetic lens' framing reflects genuine field leadership or a tendency to soften accountability when it's needed.",
        "integrity": "Low concern. Repetitive use of 'empathetic lens' across all three scenarios may be a stylistic pattern or AI echoing. No other signals. Probe at GWC if advancing.",
    },
    {
        "rank": 8, "name": "Jalal Ud Din", "score": 60, "score_label": "60%",
        "verdict": "CONDITIONAL", "confidence": "High",
        "stage": "Case study evaluated",
        "tagline": "Exceptional tracker, thin written analysis — the gap between the two needs probing before advancing.",
        "scores": [3, 3, 3, 2, 4],
        "narrative": (
            "Jalal presents the most notable internal inconsistency in this batch: his tracker (6 sheets, "
            "Supervisor Observation compliance checks, DEO/AEO coordination columns, 'Sampling Integrity Affected?' "
            "risk log column) is structurally strong, while his written analysis is the weakest. "
            "He correctly identifies unauthorised substitution as a validity threat — not just a process issue. "
            "But his written responses are procedurally correct and shallow: he lists steps without showing "
            "root-cause reasoning or field judgment. He suggests personally assessing students to 'evaluate' them — "
            "a Field Coordinator does not administer the assessment tool. The tracker has no auto-flagging formulas. "
            "For a role that requires both operational structure and field judgment, this split profile carries real risk."
        ),
        "gap": "The main concern is the gap between his tracker and his written analysis — his tracker has 6 sheets with Supervisor Observation compliance checks and a 'Sampling Integrity Affected?' column in the risk log, yet his written responses show no equivalent depth. He also suggests personally assessing students to 'evaluate' them — a Field Coordinator does not administer the assessment tool, and this signals a possible misunderstanding of the role boundary. At GWC, probe whether the tracker was independently designed or assisted, and whether he can articulate root causes verbally when he cannot write them out.",
        "integrity": "Low concern. 'Epic focus on ethical protocols' is an outlier phrase in otherwise plain writing. Tracker/analysis discrepancy of this magnitude — one of the two was likely AI-assisted. Probe explicitly at GWC.",
    },
    {
        "rank": 9, "name": "Muhammad Abubakr", "score": 60, "score_label": "60%",
        "verdict": "CONDITIONAL", "confidence": "High",
        "stage": "GWC done",
        "tagline": "Consistently adequate across all criteria — no critical gaps, but no standout strengths either.",
        "scores": [3, 3, 3, 3, 3],
        "narrative": (
            "Abubakr's submission is uniformly competent: he addresses each scenario correctly, identifies "
            "the right escalation path, and structures his tracker logically. What is absent is depth. "
            "His risk identification stops at the surface (data looks wrong — contact firm) without "
            "forming a hypothesis about why. His government coordination response is procedurally "
            "accurate but generic — no Pakistan-specific instinct, no differentiation between DEO and "
            "headmaster relationships. His tracker is functional but reactive: columns map to what "
            "happened rather than what could go wrong. In a batch with four candidates scoring in the "
            "HIRE range, he does not differentiate above the conditional threshold."
        ),
        "gap": "Uniformly adequate but with no moment that rises above procedure. His risk identification stops at 'data looks wrong, contact the firm' — he does not form a hypothesis about why. His government coordination answer is correctly sequenced but generic, with no Pakistan-specific instinct (no mention of in-person visits, DEO vs. headmaster as separate relationships, or Taleemabad as the outreach lead rather than the firm). In a batch where four candidates score HIRE or above, this level of adequacy does not differentiate. GWC would need to show significantly stronger independent judgment to justify advancement.",
        "integrity": "Clean. No AI signals. Consistent voice throughout — adequacy appears genuine.",
    },
    {
        "rank": 10, "name": "Zubair Hussain", "score": 42, "score_label": "42%",
        "verdict": "BORDERLINE", "confidence": "High",
        "stage": "Case study evaluated",
        "tagline": "Field operations experience visible — foundational assessment methodology gaps prevent advancement at this stage.",
        "scores": [2, 2, 1, 3, 3],
        "narrative": (
            "Zubair shows familiarity with the government coordination landscape — he correctly identifies "
            "the top-down approach (District level to Tehseel to school head), names TEO as a relevant "
            "contact, and references MoU/NoC documentation. These are genuine field signals. "
            "However, two foundational misreads disqualify him at this stage. First: his response to "
            "enumerator paraphrasing is 'it depends whether the paraphrasing is correct or makes it more "
            "complex' — verbatim administration is non-negotiable in standardised assessments, no exceptions. "
            "Second: on supervisor absence he says 'it is no serious concern because one supervisor is not "
            "expected to be available at a time in each school' — this misunderstands the monitoring function "
            "entirely. Supervisors are expected to observe and rotate across schools; absence is a control failure. "
            "His proposed corrective action — halt the entire survey immediately — would cause significant "
            "timeline damage for issues that require targeted, not wholesale, response."
        ),
        "gap": "Two specific misreads that are knowledge gaps, not coaching gaps. (1) On enumerator paraphrasing, he wrote 'it depends whether the enumerator is correctly paraphrasing to help students understand' — verbatim administration is non-negotiable in standardised assessments regardless of intent, and this is a foundational research protocol. (2) He described supervisor absence as 'no serious concern because one supervisor is not expected to be available at a time in each school' — supervisors are expected to rotate across schools and actively observe enumerators; absence during active assessment is a control failure. These gaps would require significant training before he could independently manage a research-grade evaluation.",
        "integrity": "Moderate concern. Responses are brief and directive with no reasoning shown — pattern consistent with someone who knows field logistics but could not articulate the 'why' under time pressure. Tracker is basic but consistent with written work.",
    },
]


# ── HTML HELPERS ───────────────────────────────────────────────────────────────
def td(content, bg=WHITE, color=DARK, bold=False, center=False, pad="8px 10px", size="13px", border=None):
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
                f'padding:2px 7px;border-radius:4px">-</span>')
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
    parts.append(f'<div style="font-family:Arial,sans-serif;max-width:940px;margin:0 auto;background:{WHITE}">')

    # HEADER
    parts.append(f'''
    <div style="background:{WHITE};padding:28px 32px;border-radius:6px 6px 0 0;border-bottom:3px solid {BLUE}">
      <span style="background:{BLUE};color:{WHITE};font-size:10px;font-weight:bold;
                   padding:2px 8px;border-radius:3px;letter-spacing:1px">INTERNAL</span>
      <h1 style="color:{BLUE};font-size:26px;margin:10px 0 4px;font-weight:bold">
        Field Coordinator — Case Study Evaluation</h1>
      <p style="color:{MID};margin:0 0 14px;font-size:14px">Research &amp; Impact Studies &nbsp;&middot;&nbsp; Taleemabad</p>
      <table cellpadding="0" cellspacing="0" border="0"><tr>
        <td style="background:#e8f0fe;color:{BLUE};font-size:12px;font-weight:bold;
                   padding:4px 12px;border-radius:3px">Field Coordinator</td>
        <td style="width:8px"></td>
        <td style="background:#e8f0fe;color:{BLUE};font-size:12px;font-weight:bold;
                   padding:4px 12px;border-radius:3px">10 Candidates &nbsp;&middot;&nbsp; Full Batch</td>
        <td style="width:8px"></td>
        <td style="background:#e8f0fe;color:{BLUE};font-size:12px;font-weight:bold;
                   padding:4px 12px;border-radius:3px">{EVAL_DATE}</td>
      </tr></table>
    </div>
    ''')

    parts.append(f'<div style="padding:24px 32px;background:{WHITE};border:1px solid {RULE};border-top:none">')

    # ABOUT
    parts.append(section_header("About This Document"))
    parts.append(f'<p style="font-size:13px;color:{DARK};line-height:1.6;margin:0 0 4px">'
                 f'Full-batch case study evaluation for Job 36 Field Coordinator — Research &amp; Impact Studies. '
                 f'10 candidates evaluated across 5 weighted criteria. Scores use a 1-5 scale per criterion. '
                 f'Moiz Khan, Shazmina, and Muhammad Abubakr completed GWC calls before case study submission; '
                 f'their scores reflect the written submission only, independent of GWC outcomes. '
                 f'Usman Ahmed Khan score is provisional (71%) pending tracker file receipt — '
                 f'4 of 5 criteria scored. Asad Farooq and Zubair Hussain are new additions evaluated in this batch.</p>')

    # SCORING FRAMEWORK
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

    # SCORES AT A GLANCE
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
                 f'2 = weak &nbsp;|&nbsp; 1 = absent &nbsp;|&nbsp; - = not yet evaluated</td></tr>')
    parts.append('</table>')

    # CANDIDATE EVALUATIONS
    parts.append(section_header("Candidate Evaluations"))

    for c in CANDIDATES:
        vc = VERDICT_COLORS[c["verdict"]]
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
        parts.append(f'<div style="background:{BG};border-left:3px solid {vc};'
                     f'padding:8px 14px;font-style:italic;font-size:13px;color:{MID};'
                     f'border-right:1px solid {RULE};border-bottom:1px solid {RULE}">'
                     f'{c["tagline"]}</div>')
        score_chips = ''.join(
            f'<td style="padding:4px 8px;text-align:center">'
            f'<div style="font-size:10px;color:{MID};margin-bottom:2px">{CRITERIA[j][0]}</div>'
            f'{score_chip(c["scores"][j])}</td>'
            for j in range(len(CRITERIA))
        )
        parts.append(f'<div style="background:{WHITE};border:1px solid {RULE};border-top:none;padding:12px 14px">')
        parts.append(f'<table cellpadding="0" cellspacing="0" border="0" style="margin-bottom:12px"><tr>{score_chips}</tr></table>')
        parts.append(f'<p style="font-size:13px;color:{DARK};line-height:1.7;margin:0 0 10px">{c["narrative"]}</p>')
        parts.append(f'<div style="background:#fff8e6;border-left:3px solid {AMBER};padding:8px 12px;'
                     f'margin-bottom:8px;font-size:12px;color:{DARK}">'
                     f'<b style="color:{AMBER}">Gap:</b> {c["gap"]}</div>')
        int_concern = any(w in c["integrity"].lower() for w in ("concern", "probe", "discrepancy", "pending"))
        int_bg     = "#fff8e6" if int_concern else BG
        int_border = AMBER     if int_concern else RULE
        parts.append(f'<div style="background:{int_bg};border-left:3px solid {int_border};padding:8px 12px;'
                     f'font-size:12px;color:{MID}">'
                     f'<b>Integrity Check:</b> {c["integrity"]}</div>')
        parts.append('</div>')
        parts.append('<div style="height:16px"></div>')

    # INTEGRITY FLAGS
    parts.append(section_header("Integrity Flags"))
    parts.append(f'<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse">')
    parts.append(f'<tr>{th("Candidate")}{th("Signal")}{th("Severity")}</tr>')
    flags = [
        ("Jalal Ud Din",
         "6-sheet tracker with Supervisor Observation compliance checks, DEO/AEO columns, and 'Sampling Integrity Affected?' "
         "risk log is structurally strong. Written analysis is the weakest in the batch — procedurally correct, "
         "no root-cause reasoning. Phrase 'epic focus on ethical protocols' is an outlier in otherwise plain writing. "
         "Tracker/analysis discrepancy of this magnitude suggests one of the two was AI-assisted.",
         "Low concern — probe explicitly at GWC"),
        ("Zubair Hussain",
         "Two foundational misreads: (1) paraphrasing response says 'it depends' — no assessment professional with "
         "standardised tool experience would write this. (2) Supervisor absence described as 'no serious concern.' "
         "Responses are brief and directive with no reasoning shown — may indicate limited familiarity with "
         "research-grade fieldwork despite operational experience.",
         "Moderate concern — not recommended for advancement"),
        ("Asad Farooq",
         "Repetitive use of 'empathetic lens' across all three scenarios may be a stylistic pattern or AI echoing. "
         "No other signals detected.",
         "Low concern — probe at GWC if advancing"),
        ("Usman Ahmed Khan",
         "Tracker file not received — cannot complete integrity check on tracker. Written submission is clean.",
         "Pending — flag if tracker unavailable"),
        ("All others",
         "Clean. No AI content dump signals, no mirroring across candidates, no foundational misreads.",
         "None"),
    ]
    for i, (name, signal, severity) in enumerate(flags):
        row_bg = "#fff8e6" if i < 4 else BG
        sev_color = AMBER if i < 4 else MID
        parts.append(f'<tr>'
                     f'{td(f"<b>{name}</b>", bg=row_bg)}'
                     f'{td(signal, bg=row_bg, size="12px")}'
                     f'{td(severity, bg=row_bg, size="12px", color=sev_color)}'
                     f'</tr>')
    parts.append('</table>')

    # PIPELINE RECOMMENDATIONS
    parts.append(section_header("Pipeline Recommendations"))
    parts.append(f'<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse">')
    parts.append(f'<tr>{th("Candidate")}{th("Current Stage")}{th("Recommendation")}</tr>')
    pipeline = [
        ("Scheherazade Noor",  "Case study evaluated",  GREEN,
         "Advance to GWC — no conditions."),
        ("Maria Karim",        "Case study evaluated",  GREEN,
         "Advance to GWC — no conditions."),
        ("Moiz Khan",          "GWC done",              BLUE,
         "Case study clears at HIRE (83%). Consolidate GWC outcome with case study score for final decision."),
        ("Amina Batool",       "Case study evaluated",  BLUE,
         "Advance to GWC — probe consent-data escalation gap and ownership instinct."),
        ("Shazmina",           "GWC done",              BLUE,
         "Case study clears at HIRE (73%). Research integrity framing is coachable. Consolidate with GWC outcome."),
        ("Usman Ahmed Khan",   "Tracker pending",       MID,
         "Hold advancement until tracker received and scored. Written submission provisionally supports HIRE."),
        ("Asad Farooq",        "Case study evaluated",  AMBER,
         "CONDITIONAL — advance only if pool is thin. Probe fieldwork pause misjudgment and empathy-vs-accountability balance at GWC."),
        ("Jalal Ud Din",       "Case study evaluated",  AMBER,
         "CONDITIONAL — advance only if pool is thin. Probe tracker/analysis discrepancy explicitly at GWC."),
        ("Muhammad Abubakr",   "GWC done",              AMBER,
         "CONDITIONAL — 60% in a competitive batch. Consolidate with GWC outcome before deciding."),
        ("Zubair Hussain",     "Case study evaluated",  RED,
         "Not recommended for advancement. Two foundational assessment methodology misreads are a knowledge gap, not a coaching gap."),
    ]
    for i, (name, stage, vc, rec) in enumerate(pipeline):
        row_bg = BG if i % 2 == 0 else WHITE
        parts.append(f'<tr>'
                     f'{td(f"<b style=\'color:{vc}\'>{name}</b>", bg=row_bg)}'
                     f'{td(stage, bg=row_bg, size="12px", color=MID)}'
                     f'{td(rec, bg=row_bg, size="13px")}'
                     f'</tr>')
    parts.append('</table>')

    # FOOTER
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
        safe_sendmail(server, SENDER, all_recipients, msg.as_string(), context='send_job36_case_study_report_v5')
    print(f"Sent to: {', '.join(all_recipients)}")


if __name__ == "__main__":
    send()
