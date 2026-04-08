"""
Job 32 — Fundraising & Partnerships Manager
Case Study Evaluation Report — 3 Candidates
PILOT: Ayesha + Jawwad only. Set PILOT_MODE = False for live send.
"""

import smtplib, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import date
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

PILOT_MODE = True

SENDER    = "ayesha.khan@taleemabad.com"
PASSWORD  = os.getenv("EMAIL_PASSWORD")
TO_LIVE   = ["sabeena.abbasi@taleemabad.com"]
CC_LIVE   = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]
TO_PILOT  = ["ayesha.khan@taleemabad.com"]
CC_PILOT  = ["jawwad.ali@taleemabad.com"]

SUBJECT   = "Fundraising & Partnerships Manager — Case Study Evaluation | 3 Candidates | March 2026"
EVAL_DATE = date.today().strftime("%d %B %Y")

# ── COLOUR TOKENS ──────────────────────────────────────────────────────────────
DARK  = "#1e2a38"
GREEN = "#1a7a4a"
BLUE  = "#1565c0"
AMBER = "#c87800"
RED   = "#c0392b"
MID   = "#636e72"
RULE  = "#dfe6e9"
BG    = "#f7f9fc"
WHITE = "#ffffff"

SCORE_COLORS   = {5: "#1a7a4a", 4: "#27ae60", 3: "#c87800", 2: "#e17055", 1: "#c0392b"}
VERDICT_COLORS = {
    "STRONG HIRE":     "#1a7a4a",
    "HIRE":            "#1565c0",
    "CONDITIONAL":     "#c87800",
    "BORDERLINE":      "#e17055",
    "NOT RECOMMENDED": "#c0392b",
}

# ── CRITERIA ───────────────────────────────────────────────────────────────────
CRITERIA = [
    ("Funder Intel",    "25%"),
    ("Rel. Craft",      "25%"),
    ("Communication",   "20%"),
    ("Strat. Diagnosis","20%"),
    ("Track Record",    "10%"),
]
WEIGHTS = [25, 25, 20, 20, 10]

# ── CANDIDATE DATA ─────────────────────────────────────────────────────────────
CANDIDATES = [
    {
        "rank": 1, "name": "Mizhgan Kirmani", "score": 83, "score_label": "83%",
        "verdict": "HIRE", "confidence": "High",
        "confidence_note": "High confidence across E1–E4. Single uncertainty: E5 track record is unverified — may be constructed. Capability read is solid regardless.",
        "tagline": "The strongest all-round submission in this cohort — technically sharp, donor-literate, and practitioner-level in cold room execution.",
        "scores": [4, 5, 4, 4, 4],
        "narrative": (
            "<b>E1 (Pipeline Prioritization)</b> — Correct and well-reasoned. D first on timing and access, C second on the warm intro signal, "
            "E third on the resolved objection — all defensible in a 90-day window. Deprioritization is specific: B (weak signal), "
            "A (wrong geography, long lead), F (low strategic value), G (revenue narrative required), H (12-month cultivation). "
            "Reasons, not gut feel.<br><br>"
            "<b>E2 (Cold Room)</b> — Best in cohort. She opens with curiosity, listens before bridging to Pakistan, and handles each "
            "objection with evidence-grounded pivots: governance risk, thin EdTech evidence, no prior Pakistan funding. "
            "The standout detail: she refuses the vague 'send me an email' brush-off and reframes to a targeted deliverable — "
            "'a 2-pager specifically on how we work with government at scale, rather than a general overview.' "
            "That is a real practitioner technique, not textbook advice.<br><br>"
            "<b>E3 (Re-engagement)</b> — Warm and forward-looking. Leads with a genuine update (Punjab 6,000-school commitment) "
            "rather than a nudge. Tone is respectful without being passive.<br><br>"
            "<b>E4 (Funder Brief)</b> — Adds an 'Insight' layer before the solution: diagnosing why scale fails (delivery model, "
            "not intent) before positioning Taleemabad as the answer. Better fundraising framing than a product brief."
        ),
        "gap": (
            "<b>E5 (Track Record)</b> — Structural flag. She frames it as a hypothetical: 'I would discuss a funding relationship I led.' "
            "The story names a result ($350K grant for Punjab schools) but no real funder, no timeline, no risk moment described. "
            "The scenario maps closely to Taleemabad's own context. This does not disqualify her — E1 through E4 are real capability. "
            "But there is no verified independent fundraising experience yet."
        ),
        "gwc_guide": [
            "E5 authenticity — Walk me through the last grant or partnership you personally led from identification to close. Name the funder, the amount, and the moment it almost fell apart.",
            "E2 live test — Her cold room script is strong on paper. Run a live skeptical funder persona and test whether she executes naturally under pressure.",
            "E1 vs Hamdan — She deprioritized Funder F as low strategic value. Hamdan prioritized it for the 3-week deadline. Ask her to defend her reasoning and probe her thinking on time-sensitive, low-upside wins.",
            "Pakistan donor landscape — Has she directly engaged bilateral donors or large foundations on Pakistan-based programs? Which organisations, which programmes?",
        ],
        "integrity": "Clean. No AI content dump signals. Writing voice is consistent and personal across all five exercises.",
    },
    {
        "rank": 2, "name": "Zain Ul Abideen", "score": 74, "score_label": "74%",
        "verdict": "HIRE", "confidence": "Medium",
        "confidence_note": "Medium confidence. Strong on process and execution instincts. Sector gap (corporate IT vs development fundraising) is unresolved — GWC is the decision point.",
        "tagline": "Consistent, complete, and technically sound — sector transition from corporate IT is the open question.",
        "scores": [4, 4, 4, 4, 3],
        "narrative": (
            "<b>E1 (Pipeline Prioritization)</b> — Sound. He correctly identified Funder E as a high-priority re-engagement opportunity: "
            "the prior objection (no government integration) has since been resolved by the Punjab 6,000-school partnership. "
            "That is a specific, astute read that required him to connect the funder's past objection to Taleemabad's current position.<br><br>"
            "<b>E2 (Cold Room)</b> — Structured. Opens with a listening question, reframes with RCT outcomes and government commitment, "
            "closes with a concrete next step. Execution is prepared rather than conversational — transitions are mechanical, "
            "less listening instinct than Mizhgan's version.<br><br>"
            "<b>E3 (Re-engagement)</b> — Competent, but contains one credibility error: 'the three detailed meetings we had where your "
            "team really appreciated our model' — this was not given information in the scenario. Fabricating prior relationship "
            "warmth in a donor email is a real-world risk.<br><br>"
            "<b>E4 (Funder Brief)</b> — Clean and metric-driven but reads as a product brochure, not a targeted ask. "
            "No specific amount, no tailored audience hook."
        ),
        "gap": (
            "<b>E5 (Track Record)</b> — Most significant open question. His track record is a $10M Microsoft Enterprise Licence "
            "Agreement with a US Government Department of Corrections. Corporate IT procurement, not institutional donor fundraising. "
            "Transferable skills are real: positioning, compliance navigation, deal structuring, relationship access at senior level. "
            "What does not transfer: funder psychology, bilateral and foundation cultivation cycles, grant stewardship, donor reporting. "
            "He has likely never run a full grant or partnership cycle with a bilateral, foundation, or CSR team."
        ),
        "condition": "Condition: advance only if GWC confirms credible sector transition narrative — specifically, evidence of any prior engagement with development sector donors (bilateral, foundation, multilateral, or CSR). If no prior development sector exposure is confirmed at GWC, this is a foundational gap for the role.",
        "gwc_guide": [
            "E5 sector transition — Walk me through how you see your Microsoft ELA experience mapping to institutional donor relationships. What carries over, and what doesn't?",
            "Development sector exposure — Have you ever identified, cultivated, and closed a grant or partnership with a bilateral donor, a foundation, or a multilateral? If yes, walk me through it.",
            "E3 assumption — In your re-engagement email you wrote 'the three detailed meetings where your team really appreciated our model.' That wasn't in the brief. Walk me through your thinking — why did you add that?",
            "E4 ask specificity — Your funder brief doesn't name an ask amount. In a real pitch to this funder, what would the ask be and why?",
        ],
        "integrity": "One assumption error in E3 (fabricated prior relationship warmth — not given information). No AI content dump signals elsewhere.",
    },
]

# Separate incomplete candidate — not ranked
INCOMPLETE = {
    "name": "Hamdan Ahmad", "score": 52, "score_label": "52%*",
    "confidence_note": "Cannot assign a confidence level — 3 of 5 criteria are unassessed. What was submitted signals strong potential. 52% is a floor, not a ceiling.",
    "tagline": "The most analytically sophisticated mind in this cohort — incomplete submission due to hospitalisation. Cannot be ranked against full submissions.",
    "scores": [4, 0, 4, 2, 0],
    "narrative": (
        "Hamdan submitted E1 in full, E3 (re-engagement email only), and did not submit E2, E4, or E5. "
        "He was hospitalised before the deadline and submitted via email when the Markaz portal was inaccessible. "
        "The 52% is a function of missing exercises, not assessed capability.<br><br>"
        "<b>E1 (Pipeline Prioritization)</b> — Most sophisticated analysis in this cohort. He was the only candidate to identify "
        "Funder F's three-week CSR decision window as a structural urgency signal worth acting on immediately. "
        "His framing is commercially precise: position Rumi as a connectivity layer through the telco's own mobile infrastructure, "
        "name the CSR decision-maker (not the comms team), deliver a co-branding proposal with projected reach. "
        "For Funder B, he maps funded organisations before the call, not during. This is field-level BD thinking.<br><br>"
        "<b>E3 (Re-engagement)</b> — Best re-engagement email in the cohort. Opens with: 'the ground has shifted considerably "
        "since we submitted it.' Names specific milestones without overselling. Offers a genuine exit: 'if the fit isn't right, "
        "I'd value knowing that too.' Closes without pressure. Writing quality is noticeably above cohort average — "
        "precise, fluid, donor-literate."
    ),
    "gap": (
        "E2 (cold room), E4 (funder brief), and E5 (track record) are not submitted. These cover three of the five core "
        "competency areas for this role. The cold room is the highest-stakes gap: we cannot assess whether his analytical "
        "clarity translates to live pitch execution under pressure. Track record is entirely unverified."
    ),
    "condition": "Condition: do not advance on this submission alone. Either (a) assign supplementary exercises covering E2 (cold room scenario) and E5 (track record walkthrough) before scheduling GWC, or (b) open the GWC itself with a structured live cold room and track record session to complete the assessment. Decision on GWC can only be made after those gaps are filled.",
    "gwc_guide": [
        "E2 live cold room — Run a live skeptical funder persona. His E1 shows sharp strategic instincts — test whether that translates to real-time pitch execution.",
        "E5 track record — Walk me through the last funding relationship you led from identification to close. Name the funder, the amount, your specific role, and what almost stopped it.",
        "E1 Funder F — You were the only candidate to flag Funder F's three-week window. Walk me through how you caught that and what you would have done in week one.",
        "E4 funder brief — Given your re-engagement email quality, describe how you would structure a one-page brief for a first-time bilateral donor unfamiliar with Taleemabad.",
    ],
    "integrity": (
        "Clean. Hospitalisation confirmed via email thread (12 Mar 2026). Submission via email confirmed due to Markaz portal "
        "access failure. No AI content dump signals. Writing voice in E1 and E3 is distinctly personal."
    ),
}

# ── HTML HELPERS ───────────────────────────────────────────────────────────────
def th(text, center=False):
    align = "center" if center else "left"
    return (f'<td style="background:{DARK};color:#ffffff;font-size:12px;font-weight:bold;'
            f'padding:8px 10px;text-align:{align};border:1px solid {RULE}">{text}</td>')

def td(text, bg=BG, center=False, bold=False, color=DARK, size="13px"):
    align = "center" if center else "left"
    weight = "bold" if bold else "normal"
    return (f'<td style="background:{bg};color:{color};font-size:{size};font-weight:{weight};'
            f'padding:8px 10px;text-align:{align};border:1px solid {RULE};vertical-align:top">{text}</td>')

def score_chip(s):
    if s == 0:
        return f'<span style="background:#dfe6e9;color:{MID};font-size:11px;font-weight:bold;padding:2px 7px;border-radius:3px">—</span>'
    c = SCORE_COLORS.get(s, MID)
    return f'<span style="background:{c};color:#fff;font-size:11px;font-weight:bold;padding:2px 7px;border-radius:3px">{s}</span>'

def verdict_chip(v):
    c = VERDICT_COLORS.get(v, MID)
    return f'<span style="background:{c};color:#fff;font-size:11px;font-weight:bold;padding:3px 9px;border-radius:3px">{v}</span>'

def section_header(title):
    return (f'<div style="margin:28px 0 10px;padding:10px 0 8px;'
            f'border-bottom:2px solid {BLUE}">'
            f'<span style="font-size:15px;font-weight:bold;color:{DARK}">{title}</span>'
            f'</div>')


# ── BUILD HTML ─────────────────────────────────────────────────────────────────
def build_html():
    parts = []

    parts.append(f'''
    <div style="font-family:Arial,sans-serif;max-width:860px;margin:0 auto;color:{DARK}">
    <div style="background:{BLUE};padding:28px 32px;border-radius:6px 6px 0 0">
      <p style="color:#ffffff;font-size:20px;font-weight:bold;margin:0 0 6px">
        Fundraising &amp; Partnerships Manager</p>
      <p style="color:#e3eaff;margin:0 0 14px;font-size:14px">
        Case Study Evaluation &nbsp;&middot;&nbsp; Taleemabad</p>
      <table cellpadding="0" cellspacing="0" border="0"><tr>
        <td style="background:#e8f0fe;color:{BLUE};font-size:12px;font-weight:bold;
                   padding:4px 12px;border-radius:3px">Job 32</td>
        <td style="width:8px"></td>
        <td style="background:#e8f0fe;color:{BLUE};font-size:12px;font-weight:bold;
                   padding:4px 12px;border-radius:3px">3 Candidates &nbsp;&middot;&nbsp; Full Batch</td>
        <td style="width:8px"></td>
        <td style="background:#e8f0fe;color:{BLUE};font-size:12px;font-weight:bold;
                   padding:4px 12px;border-radius:3px">{EVAL_DATE}</td>
      </tr></table>
    </div>
    ''')

    parts.append(f'<div style="padding:24px 32px;background:{WHITE};border:1px solid {RULE};border-top:none">')

    # ABOUT
    parts.append(section_header("About This Document"))
    parts.append(
        f'<p style="font-size:13px;color:{DARK};line-height:1.6;margin:0 0 4px">'
        f'Full-batch case study evaluation for Job 32 Fundraising &amp; Partnerships Manager. '
        f'3 candidates assessed across 5 weighted criteria using a 1–5 scale per criterion. '
        f'<strong>Ranked candidates: Mizhgan Kirmani and Zain Ul Abideen</strong> — both submitted all 5 exercises. '
        f'<strong>Hamdan Ahmad is listed separately as an incomplete submission</strong> — he was hospitalised before the '
        f'deadline and submitted Exercises 1 and 3 only via email when the Markaz portal was inaccessible. '
        f'A partial score cannot be ranked against full submissions. His evaluation is presented in a dedicated section '
        f'with a supplementary assessment recommendation. '
        f'<strong>Advancement threshold: 60% and above proceeds to GWC. '
        f'Both ranked candidates qualify. Hamdan requires supplementary evaluation before a GWC decision.</strong></p>'
    )

    # SCORING FRAMEWORK
    parts.append(section_header("Scoring Framework"))
    parts.append(f'<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse;margin-bottom:4px">')
    parts.append(f'<tr>{th("Criterion")}{th("Weight", center=True)}{th("What We Evaluated")}</tr>')
    fw_rows = [
        ("Funder Intelligence &amp; Prioritization", "25%",
         "Ranking logic within a 90-day window. Ability to distinguish access vs. alignment vs. urgency. "
         "Quality of first-move strategy per funder. Deprioritization reasoning."),
        ("Relationship &amp; Networking Craft", "25%",
         "Cold room execution: listening before pitching, handling objections without defensiveness, "
         "converting curiosity into a concrete next step. Donor cultivation instinct."),
        ("Communication Quality", "20%",
         "Writing clarity and precision across all exercises. Funder-facing materials: "
         "one-pager structure, metric use, narrative framing. Pitch fluency."),
        ("Strategic Diagnosis", "20%",
         "Accuracy of funder-gone-quiet diagnosis. Re-engagement strategy and email quality. "
         "Pipeline judgment: when to pursue, when to park, when to close."),
        ("Track Record &amp; Evidence", "10%",
         "Credibility and sector relevance of claimed funding experience. "
         "Development sector donor landscape literacy — bilateral, multilateral, foundation, CSR."),
    ]
    for i, (crit, wt, desc) in enumerate(fw_rows):
        row_bg = BG if i % 2 == 0 else WHITE
        parts.append(
            f'<tr>{td(f"<b>{crit}</b>", bg=row_bg)}'
            f'{td(wt, bg=row_bg, center=True, bold=True, color=BLUE)}'
            f'{td(desc, bg=row_bg, size="12px", color=MID)}</tr>'
        )
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

    # Hamdan — incomplete row
    ic = INCOMPLETE
    row_bg = "#f8f0ff"
    cells = td(f'<b>{ic["name"]}</b> <span style="font-size:11px;color:{MID}">(incomplete)</span>', bg=row_bg)
    for sc in ic["scores"]:
        cells += td(score_chip(sc), bg=row_bg, center=True)
    cells += td(f'<b style="color:{MID}">{ic["score_label"]}</b>', bg=row_bg, center=True)
    cells += td(f'<span style="background:{MID};color:#fff;font-size:11px;font-weight:bold;padding:3px 9px;border-radius:3px">INCOMPLETE</span>', bg=row_bg)
    parts.append(f'<tr>{cells}</tr>')

    parts.append(
        f'<tr><td colspan="8" style="padding:6px 10px;font-size:11px;color:{MID};'
        f'background:{BG};border:1px solid {RULE}">'
        f'5 = exceptional &nbsp;|&nbsp; 4 = strong &nbsp;|&nbsp; 3 = adequate &nbsp;|&nbsp; '
        f'2 = weak &nbsp;|&nbsp; 1 = absent &nbsp;|&nbsp; 0 = not submitted</td></tr>'
    )
    parts.append('</table>')

    # CANDIDATE EVALUATIONS
    parts.append(section_header("Candidate Evaluations"))

    for c in CANDIDATES:
        vc = VERDICT_COLORS[c["verdict"]]
        # Build GWC guide HTML
        gwc_items = "".join(
            f'<li style="margin-bottom:8px">{q}</li>'
            for q in c.get("gwc_guide", [])
        )
        # Build condition block if present
        condition_block = ""
        if c.get("condition"):
            condition_block = (
                f'<div style="margin-top:14px;padding:10px 14px;background:#fff8e6;'
                f'border-left:3px solid {AMBER};border-radius:3px;font-size:12px;color:{DARK};line-height:1.6">'
                f'<b style="color:{AMBER}">Condition to Advance</b><br>{c["condition"]}</div>'
            )
        parts.append(f'''
        <table cellpadding="0" cellspacing="0" border="0"
               style="width:100%;border-collapse:collapse;margin-bottom:0">
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
            </td>
          </tr>
          <tr>
            <td colspan="2"
                style="background:#f8f9fa;padding:8px 16px;border:1px solid {RULE};border-top:none;
                       font-size:13px;font-style:italic;color:{MID}">
              {c["tagline"]}
            </td>
          </tr>
          <tr>
            <td colspan="2"
                style="background:#eef3fb;padding:7px 16px;border:1px solid {RULE};border-top:none;
                       font-size:12px;color:{BLUE}">
              <b>Confidence:</b> {c["confidence"]} &nbsp;&mdash;&nbsp; {c["confidence_note"]}
            </td>
          </tr>
        </table>
        <table cellpadding="0" cellspacing="0" border="0"
               style="width:100%;border-collapse:collapse;margin-bottom:4px">
          <tr>
            <td style="background:{WHITE};padding:14px 16px;border:1px solid {RULE};border-top:none;
                       font-size:13px;color:{DARK};line-height:1.7;width:50%;vertical-align:top">
              <b style="color:{BLUE}">Evaluation — Per Exercise</b><br><br>{c["narrative"]}
            </td>
            <td style="width:10px;border:none"></td>
            <td style="background:{WHITE};padding:14px 16px;border:1px solid {RULE};border-top:none;
                       font-size:13px;color:{DARK};line-height:1.6;width:50%;vertical-align:top">
              <b style="color:{AMBER}">Gap</b><br><br>{c["gap"]}
              {condition_block}
              <br>
              <b style="color:{MID}">Integrity</b><br>{c["integrity"]}
            </td>
          </tr>
        </table>
        <table cellpadding="0" cellspacing="0" border="0"
               style="width:100%;border-collapse:collapse;margin-bottom:28px">
          <tr>
            <td style="background:#f0f7f0;padding:14px 16px;border:1px solid {RULE};border-top:none;
                       font-size:13px;color:{DARK};line-height:1.7;vertical-align:top">
              <b style="color:{GREEN}">GWC Conversation Guide</b>
              <ul style="margin:10px 0 0 0;padding-left:20px">{gwc_items}</ul>
            </td>
          </tr>
        </table>
        ''')

    # HAMDAN — INCOMPLETE SUBMISSION
    parts.append(section_header("Incomplete Submission — Hamdan Ahmad"))
    parts.append(
        f'<p style="font-size:13px;color:{MID};line-height:1.6;margin:0 0 12px">'
        f'Hamdan submitted 2.5 of 5 exercises (E1 full, E3 email only). He cannot be ranked alongside full submissions. '
        f'Missing exercises: E2 (cold room), E4 (funder brief), E5 (track record). '
        f'A supplementary assessment is required before any GWC decision.</p>'
    )
    ic = INCOMPLETE
    ic_gwc_items = "".join(
        f'<li style="margin-bottom:8px">{q}</li>'
        for q in ic.get("gwc_guide", [])
    )
    ic_condition_block = (
        f'<div style="margin-top:14px;padding:10px 14px;background:#fff8e6;'
        f'border-left:3px solid {AMBER};border-radius:3px;font-size:12px;color:{DARK};line-height:1.6">'
        f'<b style="color:{AMBER}">Condition to Advance</b><br>{ic["condition"]}</div>'
    )
    parts.append(f'''
    <table cellpadding="0" cellspacing="0" border="0"
           style="width:100%;border-collapse:collapse;margin-bottom:0">
      <tr>
        <td style="background:{MID};padding:12px 16px;border-radius:4px 4px 0 0">
          <span style="color:{WHITE};font-size:16px;font-weight:bold">{ic["name"]}</span>
        </td>
        <td style="background:{MID};padding:12px 16px;text-align:right;border-radius:4px 4px 0 0">
          <span style="color:{WHITE};font-size:13px;font-weight:bold">{ic["score_label"]}</span>
          &nbsp;
          <span style="background:rgba(255,255,255,0.2);color:{WHITE};font-size:11px;
                       font-weight:bold;padding:3px 9px;border-radius:3px">INCOMPLETE</span>
        </td>
      </tr>
      <tr>
        <td colspan="2"
            style="background:#f8f9fa;padding:8px 16px;border:1px solid {RULE};border-top:none;
                   font-size:13px;font-style:italic;color:{MID}">
          {ic["tagline"]}
        </td>
      </tr>
      <tr>
        <td colspan="2"
            style="background:#eef3fb;padding:7px 16px;border:1px solid {RULE};border-top:none;
                   font-size:12px;color:{BLUE}">
          <b>Confidence:</b> {ic["confidence_note"]}
        </td>
      </tr>
    </table>
    <table cellpadding="0" cellspacing="0" border="0"
           style="width:100%;border-collapse:collapse;margin-bottom:4px">
      <tr>
        <td style="background:{WHITE};padding:14px 16px;border:1px solid {RULE};border-top:none;
                   font-size:13px;color:{DARK};line-height:1.7;width:50%;vertical-align:top">
          <b style="color:{BLUE}">What We Assessed — Per Exercise</b><br><br>{ic["narrative"]}
        </td>
        <td style="width:10px;border:none"></td>
        <td style="background:{WHITE};padding:14px 16px;border:1px solid {RULE};border-top:none;
                   font-size:13px;color:{DARK};line-height:1.6;width:50%;vertical-align:top">
          <b style="color:{AMBER}">Gaps — Missing Exercises</b><br><br>{ic["gap"]}
          {ic_condition_block}
          <br>
          <b style="color:{MID}">Integrity</b><br>{ic["integrity"]}
        </td>
      </tr>
    </table>
    <table cellpadding="0" cellspacing="0" border="0"
           style="width:100%;border-collapse:collapse;margin-bottom:28px">
      <tr>
        <td style="background:#f0f7f0;padding:14px 16px;border:1px solid {RULE};border-top:none;
                   font-size:13px;color:{DARK};line-height:1.7;vertical-align:top">
          <b style="color:{GREEN}">Supplementary / GWC Conversation Guide</b>
          <ul style="margin:10px 0 0 0;padding-left:20px">{ic_gwc_items}</ul>
        </td>
      </tr>
    </table>
    ''')

    # CROSS-CANDIDATE COMPARATIVE ANALYSIS
    parts.append(section_header("Cohort Read"))
    parts.append(
        f'<div style="background:{BG};padding:16px 20px;border:1px solid {RULE};border-radius:4px;'
        f'font-size:13px;color:{DARK};line-height:1.8;margin-bottom:4px">'
        f'Mizhgan and Zain are strong in different ways. Mizhgan\'s strength concentrates in E2 and E4 — '
        f'she is the better live communicator and funder-facing writer. Zain\'s strength is in strategic analysis '
        f'and pipeline logic (E1 and E3 approach), but his execution reads as more prepared than instinctive. '
        f'Neither has a verified development sector track record — both E5 scores reflect an unresolved question, '
        f'not a known failure. The cohort as a whole is analytically capable but sector-inexperienced. '
        f'The GWC will function as the track record verification round for both candidates.'
        f'<br><br>'
        f'Hamdan\'s E1 is the most commercially sophisticated piece of reasoning in this entire batch — '
        f'his Funder F catch and framing is better than either ranked candidate\'s equivalent. '
        f'His E3 writing quality is also the highest. The risk is that we have no read on his live pitch capability or claimed experience. '
        f'If the supplementary assessment closes those gaps, he may rank above Zain.'
        f'</div>'
    )

    # INTEGRITY FLAGS
    parts.append(section_header("Integrity Flags"))
    parts.append(f'<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse">')
    parts.append(f'<tr>{th("Candidate")}{th("Signal")}{th("Severity")}</tr>')
    flags = [
        ("Mizhgan Kirmani",
         "Exercise 5 constructed as a hypothetical framework, not a real story. "
         "Named outcome ($350K grant) without a real funder or timeline. Cannot verify.",
         "Flag for GWC — not disqualifying"),
        ("Zain Ul Abideen",
         "Exercise 3: fabricated prior relationship warmth ('three detailed meetings where your team appreciated our model') "
         "— this was not given information. Assumption error. Exercise 5: Microsoft corporate IT deal is not development fundraising.",
         "Flag for GWC — probe sector experience"),
        ("Hamdan Ahmad",
         "3 of 5 exercises not submitted due to hospitalisation. Context verified in email thread (12 Mar 2026). "
         "Submission mode (email) confirmed due to Markaz portal access failure.",
         "Circumstantial — not an integrity concern"),
    ]
    for i, (name, signal, severity) in enumerate(flags):
        row_bg = "#fff8e6" if i < 2 else BG
        sev_color = AMBER if i < 2 else GREEN
        parts.append(
            f'<tr>{td(f"<b>{name}</b>", bg=row_bg)}'
            f'{td(signal, bg=row_bg, size="12px")}'
            f'{td(severity, bg=row_bg, size="12px", color=sev_color)}</tr>'
        )
    parts.append('</table>')

    # PIPELINE RECOMMENDATIONS
    parts.append(section_header("Pipeline Recommendations"))
    parts.append(
        f'<p style="font-size:13px;color:{DARK};line-height:1.6;margin:0 0 12px">'
        f'<strong>Advancement threshold: 60% and above.</strong> '
        f'Both ranked candidates (Mizhgan 83%, Zain 74%) advance to GWC. '
        f'Hamdan Ahmad requires supplementary assessment before a GWC decision can be made.</p>'
    )
    parts.append(f'<table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-collapse:collapse">')
    parts.append(f'<tr>{th("Candidate")}{th("Score")}{th("Current Stage")}{th("Recommendation")}</tr>')
    pipeline = [
        ("Mizhgan Kirmani", "83% — HIRE", GREEN,
         "Case study evaluated (5/5)",
         "Advance to GWC. Probe E5 directly: name the last grant she personally led from identification to close, "
         "the funder, the amount, and what almost killed it. Also run a live cold room scenario — her E2 is strong on paper, "
         "test whether she can execute it naturally under pressure with a skeptical funder persona."),
        ("Zain Ul Abideen", "74% — HIRE", BLUE,
         "Case study evaluated (5/5)",
         "Advance to GWC. Probe the sector transition: how does his Microsoft ELA experience map to institutional donor "
         "relationships — what carries over, what doesn't? Has he ever closed a grant or partnership with a bilateral, "
         "foundation, or multilateral? His answer determines whether this is a real sector pivot or a fundamental gap."),
        ("Hamdan Ahmad", "52%* — INCOMPLETE", MID,
         "Partial submission (2.5/5) — hospitalisation",
         "Do not advance on this submission alone. Assign a targeted supplementary exercise (E2 cold room + E5 track record) "
         "before the GWC, OR open the GWC with a structured live cold room and track record walkthrough. "
         "His 52% is a floor, not a ceiling — his E1 and E3 quality suggest significantly higher actual capability."),
    ]
    for i, (name, score, vc, stage, rec) in enumerate(pipeline):
        row_bg = BG if i % 2 == 0 else WHITE
        parts.append(
            f'<tr>{td(f"<b style=\'color:{vc}\'>{name}</b>", bg=row_bg)}'
            f'{td(f"<b style=\'color:{vc}\'>{score}</b>", bg=row_bg, size="12px")}'
            f'{td(stage, bg=row_bg, size="12px", color=MID)}'
            f'{td(rec, bg=row_bg, size="13px")}</tr>'
        )
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
    html  = build_html()
    to    = TO_PILOT if PILOT_MODE else TO_LIVE
    cc    = CC_PILOT if PILOT_MODE else CC_LIVE
    label = "PILOT" if PILOT_MODE else "LIVE"

    msg = MIMEMultipart("alternative")
    msg["From"]    = SENDER
    msg["To"]      = ", ".join(to)
    msg["Cc"]      = ", ".join(cc)
    msg["Subject"] = f"{'[PILOT] ' if PILOT_MODE else ''}{SUBJECT}"
    msg.attach(MIMEText(html, "html"))

    all_recipients = to + cc
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER, PASSWORD)
        allow_candidate_addresses(all_recipients)
        safe_sendmail(server, SENDER, all_recipients, msg.as_string(),
                      context="send_job32_case_study_report")

    print(f"[{label}] Sent -> TO: {', '.join(to)} | CC: {', '.join(cc)}")


if __name__ == "__main__":
    send()
