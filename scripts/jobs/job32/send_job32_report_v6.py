import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses


RECIPIENT = "ayesha.khan@taleemabad.com"
SENDER    = os.getenv("EMAIL_USER")
PASSWORD  = os.getenv("EMAIL_PASSWORD")
HTML_OUT  = os.path.join(os.path.dirname(__file__), "output", "job32-report-interactive.html")

# ══════════════════════════════════════════════════════════════════
# INTERACTIVE HTML FILE  (details/summary accordion — no JS needed)
# ══════════════════════════════════════════════════════════════════

def score_color(s):
    if s == 4: return "#16A34A"
    if s == 3: return "#22C55E"
    if s == 2: return "#EAB308"
    if s == 1: return "#F97316"
    return "#DC2626"

def dim_cell(s):
    c = score_color(s)
    return f'<td style="text-align:center;font-weight:bold;color:{c};padding:6px 10px;border:1px solid #e5e7eb;">{s}/4</td>'

def make_profile_html(rank, emoji, name, score, tier, tier_color, salary, budget_label,
                      budget_color, budget_text_color, dims, strengths, risks, questions,
                      notes="", missing_mh=0, ocr=False):
    d1,d2,d3,d4,d5,d6,d7 = dims
    ocr_tag = ' <span style="background:#EFF6FF;color:#1D4ED8;border-radius:10px;padding:2px 6px;font-size:11px;">&#128269; OCR-recovered</span>' if ocr else ""
    mh_warn = f'<p style="color:#D97706;font-size:13px;margin:6px 0;"><b>&#9888; {missing_mh} missing must-have(s) applied — &minus;{missing_mh*15}% penalty</b></p>' if missing_mh > 0 else ""

    str_items = "".join(f"<li style='margin-bottom:4px;'>{s}</li>" for s in strengths)
    risk_items = "".join(f"<li style='margin-bottom:4px;'>{r}</li>" for r in risks)
    q_items    = "".join(f"<li style='margin-bottom:4px;'>{q}</li>" for q in questions)
    notes_html = f'<p style="font-size:12px;color:#6B7280;margin:8px 0;">{notes}</p>' if notes else ""

    return f"""
<details style="margin-bottom:14px;border-radius:8px;border:2px solid {tier_color};overflow:hidden;">
  <summary style="background:{tier_color};color:#fff;padding:14px 18px;cursor:pointer;list-style:none;font-size:15px;font-weight:bold;">
    #{rank} {emoji} {name}{ocr_tag}
    &nbsp;&nbsp;
    <span style="background:rgba(255,255,255,0.25);border-radius:12px;padding:3px 12px;">{score} / 100</span>
    &nbsp;
    <span style="background:rgba(0,0,0,0.15);border-radius:12px;padding:3px 12px;font-size:13px;">{tier}</span>
    &nbsp;
    <span style="background:{budget_color};color:{budget_text_color};border-radius:12px;padding:3px 12px;font-size:13px;">{budget_label}</span>
    <span style="float:right;font-size:18px;">&#9660;</span>
  </summary>
  <div style="padding:18px;background:#fff;">
    {mh_warn}
    <!-- Dimension Scores -->
    <h4 style="color:#4C1D95;margin:8px 0 6px 0;font-size:14px;">Dimension Scores</h4>
    <table border="1" cellpadding="0" cellspacing="0" style="border-collapse:collapse;width:100%;font-size:13px;margin-bottom:14px;">
      <thead>
        <tr style="background:#4C1D95;color:#fff;">
          <th style="padding:7px 10px;text-align:left;">D1 Functional<br><small>25%</small></th>
          <th style="padding:7px 10px;text-align:left;">D2 Outcomes<br><small>20%</small></th>
          <th style="padding:7px 10px;text-align:left;">D3 Environment<br><small>15%</small></th>
          <th style="padding:7px 10px;text-align:left;">D4 Ownership<br><small>15%</small></th>
          <th style="padding:7px 10px;text-align:left;">D5 Stakeholder<br><small>10%</small></th>
          <th style="padding:7px 10px;text-align:left;">D6 Hard Skills<br><small>10%</small></th>
          <th style="padding:7px 10px;text-align:left;">D7 Growth<br><small>5%</small></th>
        </tr>
      </thead>
      <tbody>
        <tr>{dim_cell(d1)}{dim_cell(d2)}{dim_cell(d3)}{dim_cell(d4)}{dim_cell(d5)}{dim_cell(d6)}{dim_cell(d7)}</tr>
      </tbody>
    </table>
    <!-- Salary -->
    <p style="font-size:13px;margin:4px 0;"><b>Salary desired:</b> {salary} &nbsp;|&nbsp; <b>Budget status:</b> <span style="background:{budget_color};color:{budget_text_color};border-radius:8px;padding:2px 8px;font-size:12px;">{budget_label}</span></p>
    <!-- Strengths -->
    <h4 style="color:#16A34A;margin:14px 0 4px 0;font-size:14px;">&#10003; Top Strengths</h4>
    <ul style="margin:0;padding-left:20px;font-size:13px;color:#374151;">{str_items}</ul>
    <!-- Risks -->
    <h4 style="color:#DC2626;margin:14px 0 4px 0;font-size:14px;">&#9888; Key Risks / Gaps</h4>
    <ul style="margin:0;padding-left:20px;font-size:13px;color:#374151;">{risk_items}</ul>
    <!-- Interview Questions -->
    <h4 style="color:#1D4ED8;margin:14px 0 4px 0;font-size:14px;">&#128172; Interview Questions</h4>
    <ol style="margin:0;padding-left:20px;font-size:13px;color:#374151;">{q_items}</ol>
    {notes_html}
  </div>
</details>"""


candidates = [
    dict(rank=1, emoji="&#127947;", name="Danish Hussain", score=97.5, tier="Tier A — Strong Move Forward",
         tier_color="#16A34A", salary="PKR 550,000/month",
         budget_label="Out of Budget +280K", budget_color="#FEE2E2", budget_text_color="#991B1B",
         dims=(4,4,3,4,4,4,4), missing_mh=0,
         strengths=[
             "<b>PKR 1B+ mobilised</b> across FCDO, World Bank, UNDP, ADB — highest quantified fundraising track record in pool. <span style='color:#6B7280;'>[FACT]</span>",
             "<b>Head of Grants &amp; Partnerships at INGO, 20 years</b> — most senior fundraising title in pool at exactly the right functional level. <span style='color:#6B7280;'>[FACT]</span>",
             "<b>Named active donor relationships:</b> FCDO Pakistan, UNDP Pakistan, ADB — the exact bilateral/multilateral network the JD requires. <span style='color:#6B7280;'>[FACT]</span>",
         ],
         risks=[
             "Hyderabad-based — states willing to relocate. Must be confirmed as firm commitment with timeline.",
             "WASH/humanitarian sector focus — EdTech fundraising is a pivot. Donor base overlaps significantly but EdTech positioning needs building.",
             "PKR 550,000 desired is 2× the budget ceiling — significant leadership exception required.",
         ],
         questions=[
             "You have stated willingness to relocate — what is your realistic timeline and are there conditions on that?",
             "Walk me through the largest single grant you personally closed — your exact role from inception to award letter.",
             "Your background is WASH/humanitarian — how would you reposition Taleemabad to FCDO, UNDP, and ADB as an EdTech investment priority?",
             "Which programme officers at FCDO Pakistan, UNDP Pakistan, and ADB are you currently in active relationship with?",
             "The budget ceiling is PKR 270,000/month. Your ask is 550,000. Is there a package structure — base + performance — that works for both sides?",
         ],
         notes="Confidence: High &bull; Missing must-haves: 0 &bull; Applied twice (1346 + duplicate 1347)"),

    dict(rank=2, emoji="&#127948;", name="Zain Ul Abideen", score=95.0, tier="Tier A — Strong Move Forward",
         tier_color="#16A34A", salary="PKR 350,000/month",
         budget_label="Out of Budget +80K", budget_color="#FEE2E2", budget_text_color="#991B1B",
         dims=(4,4,4,4,3,4,3), missing_mh=0, ocr=True,
         strengths=[
             "<b>Lifetime US $50M in won proposals</b> — US $8.44M at READ Foundation (UNICEF, UNFPA, US Embassy, British Council, Oxfam, IRC, WaterAid, Save the Children); US $4.42M at SPO. Dual-organisation track record confirms pattern not luck. <span style='color:#6B7280;'>[FACT]</span>",
             "<b>Deputy Manager Resource Mobilisation, Islamabad-based</b> — senior direct ownership of fundraising function + no relocation risk. <span style='color:#6B7280;'>[FACT]</span>",
             "<b>Breadth of donor portfolio</b> — UNICEF, UNFPA, US Embassy, British Council, Oxfam, IRC, WaterAid, Save the Children — strongest donor network breadth in pool. <span style='color:#6B7280;'>[FACT]</span>",
         ],
         risks=[
             "Freelance periods in CV — reasons and continuity of focus need probing.",
             "WASH/humanitarian sector dominant — EdTech fundraising is a pivot, though skill transfer is high.",
             "PKR 350,000 is PKR 80,000 above ceiling — smallest budget gap among all out-of-budget candidates. Negotiable.",
         ],
         questions=[
             "Walk me through the single largest proposal you wrote and won — your exact role from first draft to award.",
             "Which specific donor programme officers at UNICEF, USAID, FCDO have you worked with in Pakistan — are these relationships still active?",
             "You have raised predominantly in WASH/humanitarian — how would you position Taleemabad to the same donor base?",
             "What caused the freelance periods in your CV, and what were you working on during those times?",
             "The budget is PKR 150K–270K/month. Your ask is 350K. Is there flexibility, and what would make this worth the difference for you?",
         ],
         notes="Confidence: High &bull; Missing must-haves: 0 &bull; &#128269; CV was scanned — recovered via OCR. Would have been missed entirely without OCR capability."),

    dict(rank=3, emoji="&#127949;", name="Mizhgan Kirmani", score=78.8, tier="Tier B — Interview with Validation",
         tier_color="#1D4ED8", salary="PKR 250,000/month",
         budget_label="In Budget", budget_color="#DCFCE7", budget_text_color="#166534",
         dims=(3,3,4,3,3,3,3), missing_mh=0,
         strengths=[
             "Manager Donor Relations at TCF — live fundraising role with FCDO, UN Women, UNDP, USAID, Green Climate Fund. PKR 72M closed in FY. <span style='color:#6B7280;'>[FACT]</span>",
             "Islamabad-based, within budget at PKR 250K — zero location or budget risk. Best risk-adjusted in-budget option. <span style='color:#6B7280;'>[FACT]</span>",
             "8 years fundraising + Aga Khan Foundation background — deep education sector donor pedigree. <span style='color:#6B7280;'>[FACT]</span>",
         ],
         risks=[
             "PKR 72M (~$260K) is below the Year 1 target of $500K–$1M+. Scale of ambition needs validating.",
             "Largest single deal size unclear — no $500K+ independently closed grant evidenced.",
             "Government/policy engagement not evidenced — Islamabad ministry relationships missing from CV.",
         ],
         questions=[
             "What is the largest single grant you personally closed — walk through from identification to signature?",
             "How do you manage a pipeline of 30–50 opportunities simultaneously — tools and cadence?",
             "Which named donor officers at USAID, FCDO, or UNDP Pakistan have you built active relationships with?",
             "Have you written winning proposals without a dedicated proposal writer — can you share a sample or describe your writing process?",
             "The Year 1 target is $500K–$1M+ from cold. What would your 90-day plan look like at Taleemabad?",
         ],
         notes="Confidence: High &bull; Missing must-haves: 0 &bull; Best in-budget candidate"),

    dict(rank=4, emoji="&#127948;", name="Arsalan Ashraf", score=72.2, tier="Tier B — Interview with Validation",
         tier_color="#1D4ED8", salary="PKR 450,000/month",
         budget_label="Out of Budget +180K", budget_color="#FEE2E2", budget_text_color="#991B1B",
         dims=(4,3,3,4,3,3,4), missing_mh=1,
         strengths=[
             "Director of Fundraising/BD at multiple NGOs — built departments from scratch at 3 orgs. Closed Meta $100K, Chevron $250K, PKR 80M NAVTTC. <span style='color:#6B7280;'>[FACT]</span>",
             "Pipeline of 15–20 active opportunities managed simultaneously. <span style='color:#6B7280;'>[FACT]</span>",
             "Builder mentality — built fundraising functions from zero at 3 organisations — strong Taleemabad fit. <span style='color:#6B7280;'>[FACT]</span>",
         ],
         risks=[
             "Corporate CSR and foundation focus — limited multilateral/bilateral donor experience (USAID, World Bank, FCDO, EU). This is a missing must-have.",
             "Karachi-based — willing to relocate stated, but must be confirmed as firm commitment.",
             "PKR 450,000 ask is PKR 180K above ceiling — significant budget exception required.",
         ],
         questions=[
             "Your background is primarily corporate CSR — have you directly engaged USAID, FCDO, World Bank, or EU as a prime grantee?",
             "Walk me through the USAID sub-grantee experience — what was your specific role in that funding relationship?",
             "Which Pakistan-based multilateral donor programme officers are you currently in active relationship with?",
             "You have built fundraising functions from scratch at 3 orgs — what would your first 90 days look like here?",
             "Budget ceiling is 270K. Your ask is 450K. Is there a base + performance structure that bridges this?",
         ],
         notes="Confidence: High &bull; Missing must-haves: 1 (multilateral experience — &minus;15% penalty applied)"),

    dict(rank=5, emoji="&#127949;", name="Sadia Sohail", score=57.3, tier="Tier C — Risky / Backup Only",
         tier_color="#D97706", salary="PKR 140,000/month",
         budget_label="In Budget", budget_color="#DCFCE7", budget_text_color="#166534",
         dims=(3,2,3,3,2,3,2), missing_mh=1,
         strengths=[
             "8 dedicated years in donor relations at READ Foundation — proposal writing, donor comms, budget reporting. <span style='color:#6B7280;'>[FACT]</span>",
             "Fundraising-specific certifications: Major Donor Fundraising, NGO Boot Camp, Fundraising Essentials. <span style='color:#6B7280;'>[FACT]</span>",
             "Islamabad-based, within budget at PKR 140K — most affordable option with genuine donor relations background. <span style='color:#6B7280;'>[FACT]</span>",
         ],
         risks=[
             "READ Foundation is a domestic NGO — no multilateral or bilateral (USAID/WB/FCDO/EU) experience. Missing must-have.",
             "No quantified outcomes stated — grants won and amounts raised not cited anywhere in CV. Scored 2/4 on D2.",
             "8 years at Donor Relations Officer level without progression to Senior BD — management readiness unproven.",
         ],
         questions=[
             "Have you engaged with any international donors — USAID, FCDO, World Bank, UNDP, EU — in a fundraising capacity?",
             "What is the largest single grant you personally helped close — amount, donor, and your role?",
             "What is your understanding of how USAID or FCDO Pakistan structures competitive grant rounds?",
             "How would you approach building relationships with international donors you have not previously worked with?",
             "What has kept you at Donor Relations Officer level for 8 years — and what changed that you are seeking a Manager role?",
         ],
         notes="Confidence: High &bull; Missing must-haves: 1 (multilateral experience — &minus;15% penalty applied) &bull; Proceed only if Tier A and B candidates do not work out."),

    dict(rank=6, emoji="&#128198;", name="Arsim Tariq", score=49.2, tier="Extended Review — No-Hire",
         tier_color="#6B7280", salary="PKR 280,000–300,000/month",
         budget_label="Out of Budget (borderline)", budget_color="#FEF3C7", budget_text_color="#92400E",
         dims=(2,2,3,2,2,2,3), missing_mh=1,
         strengths=[
             "10+ years in development sector with FCDO and World Bank-funded contracts — deep sector knowledge. <span style='color:#6B7280;'>[FACT]</span>",
             "Islamabad-based, NUST MS graduate. <span style='color:#6B7280;'>[FACT]</span>",
             "EdTech experience mentioned — sector alignment. <span style='color:#6B7280;'>[FACT]</span>",
             "Contributed to winning proposals for FCDO and World Bank bids. <span style='color:#6B7280;'>[FACT]</span>",
         ],
         risks=[
             "Primary role is programme management and M&amp;E — not fundraising/BD ownership. [FACT — missing must-have]",
             "Proposal contributions were as technical/programme lead, not as BD/fundraising owner. [FACT]",
             "No evidence of independently closing new donor relationships or building a fundraising pipeline.",
             "Salary ceiling 280,000–300,000 PKR — borderline above budget (ceiling 270K).",
         ],
         questions=[
             "In the proposals you contributed to for FCDO and World Bank — were you the lead author and relationship owner, or the technical contributor?",
             "Have you independently managed a donor pipeline and closed new funding relationships without a BD lead above you?",
             "Can you walk me through a proposal you personally led from first contact with a donor to award?",
             "If hired as fundraising lead, how would you shift from a programme/M&amp;E mindset to a revenue acquisition mindset?",
             "Your salary range is 280–300K — the ceiling is 270K. Is there any flexibility?",
         ],
         notes="In extended review: sector knowledge is strong but role was M&amp;E/programme, not fundraising acquisition. Could develop into BD if time allows — not recommended for immediate hire."),

    dict(rank=7, emoji="&#128198;", name="Ahmed Al-Mayadeen", score=45.5, tier="Extended Review — No-Hire",
         tier_color="#6B7280", salary="~PKR 980,000/month (USD 3,500)",
         budget_label="Out of Budget (massively)", budget_color="#FEE2E2", budget_text_color="#991B1B",
         dims=(4,4,1,4,3,3,3), missing_mh=2,
         strengths=[
             "10+ years international fundraising with UN agencies and international NGOs — high functional match. <span style='color:#6B7280;'>[FACT]</span>",
             "Multi-million dollar campaign experience — quantified scale. <span style='color:#6B7280;'>[FACT]</span>",
             "Harvard Business School executive education — credibility and stakeholder communication. <span style='color:#6B7280;'>[FACT]</span>",
         ],
         risks=[
             "Yemen-based with no mention of willingness to relocate to Islamabad — deal-breaker must-have missing. [FACT]",
             "MENA region focus — no Pakistan donor landscape knowledge evidenced. [FACT — missing must-have]",
             "No named Pakistan donor relationships — network not transferable without local context.",
             "PKR 980,000 salary — massively over budget (3.6× ceiling).",
         ],
         questions=[
             "Are you willing and able to relocate to Islamabad, Pakistan on a permanent basis?",
             "What specific knowledge do you have of the Pakistan donor landscape — USAID Pakistan, World Bank Pakistan, FCDO Pakistan?",
             "Have you worked in South Asia or with South Asian development organisations?",
             "How quickly could you build a Pakistan-specific donor pipeline given no existing relationships here?",
             "What is driving your interest in Pakistan/EdTech specifically?",
         ],
         notes="High functional skills but two deal-breaker must-haves missing: location and Pakistan donor landscape. Only consider if willing to relocate AND can demonstrate Pakistan network."),

    dict(rank=8, emoji="&#128198;", name="Ahad Ahsan Khan", score=41.8, tier="Extended Review — No-Hire",
         tier_color="#6B7280", salary="PKR 550,000/month",
         budget_label="Out of Budget +280K", budget_color="#FEE2E2", budget_text_color="#991B1B",
         dims=(1,3,4,2,3,3,3), missing_mh=2,
         strengths=[
             "Manager Grants at AKU — $134M portfolio across 210 active grants, World Bank HEDP lead. <span style='color:#6B7280;'>[FACT]</span>",
             "9 years in grants management with deep institutional donor compliance knowledge. <span style='color:#6B7280;'>[FACT]</span>",
             "Islamabad hometown — no relocation issue. Strong stakeholder relationships at institutional level. <span style='color:#6B7280;'>[FACT]</span>",
         ],
         risks=[
             "Grants administration and compliance — not fundraising acquisition. [FACT — missing must-have]",
             "No evidence of independently writing and winning new competitive grants from scratch. [FACT — missing must-have]",
             "Managing existing grants &#8800; fundraising — explicitly listed as failure condition in JD.",
             "PKR 550,000 is above budget ceiling.",
         ],
         questions=[
             "In your 9 years managing grants at AKU, have you personally led a proposal from first draft to award for a new, competitive grant — not administering an existing one?",
             "Can you name a specific grant you won and describe your role from donor identification through to the award letter?",
             "What is the difference between grants management and fundraising acquisition — and which have you done?",
             "Your $134M portfolio is impressive — but that is compliance work. What experience do you have pitching to donors for new money?",
             "What would motivate you to move from grants administration to frontline fundraising, and what makes you confident you can succeed at acquisition?",
         ],
         notes="Impressive compliance credentials but wrong functional match. Grants administration and fundraising acquisition are distinct — this is a clear failure condition per the JD."),

    dict(rank=9, emoji="&#128198;", name="Muhammad Usman", score=36.1, tier="Extended Review — No-Hire",
         tier_color="#6B7280", salary="PKR 350,000/month",
         budget_label="Out of Budget +80K", budget_color="#FEE2E2", budget_text_color="#991B1B",
         dims=(2,1,3,2,3,1,3), missing_mh=2,
         strengths=[
             "18 years in government relations, public affairs, and international development alliances — senior stakeholder experience. <span style='color:#6B7280;'>[FACT]</span>",
             "Managed partnerships with international development organisations — donor-adjacent relationships. <span style='color:#6B7280;'>[FACT]</span>",
             "Rawalpindi/Islamabad-based — location aligned. <span style='color:#6B7280;'>[FACT]</span>",
         ],
         risks=[
             "States fundraising as competency but no specific grants won, amounts raised, or proposals cited. [FACT — missing must-have]",
             "Vague on whether activities were acquisition or relationship maintenance — cannot credit what is not evidenced. [FACT — missing must-have]",
             "No quantified outcomes across 18 years raises serious concerns about acquisition ownership.",
             "Government relations and public affairs &#8800; institutional grant fundraising.",
         ],
         questions=[
             "In 18 years, can you name a specific grant or partnership deal you personally closed — amount, donor, your exact role?",
             "When you say fundraising is a competency, can you give three concrete examples with outcomes?",
             "Were your international development alliance partnerships about managing existing relationships or acquiring new funding?",
             "What proposals have you written and submitted to bilateral or multilateral donors, and what was the outcome?",
             "What does your pipeline look like currently — how many active opportunities are you tracking and with which funders?",
         ],
         notes="Long career but zero quantified outcomes in 18 years is a significant red flag. Government relations background is adjacent but not equivalent to fundraising acquisition."),

    dict(rank=10, emoji="&#128198;", name="Mushahid Hussain", score=34.4, tier="Extended Review — No-Hire",
         tier_color="#6B7280", salary="PKR 170,000/month",
         budget_label="In Budget", budget_color="#DCFCE7", budget_text_color="#166534",
         dims=(2,1,3,2,2,2,2), missing_mh=2,
         strengths=[
             "Donor Reporting Officer at READ Foundation — 4 years in donor relations with some proposal exposure. <span style='color:#6B7280;'>[FACT]</span>",
             "Manages financial reporting to donors — compliance and funder communication skills. <span style='color:#6B7280;'>[FACT]</span>",
             "Islamabad-based, within budget at PKR 170K. <span style='color:#6B7280;'>[FACT]</span>",
         ],
         risks=[
             "Primarily reporting, not acquisition — junior-level role without independent grant winning. [FACT — missing must-have]",
             "No evidence of independently winning grants. [FACT — missing must-have]",
             "4 years experience at junior level — not ready for Year 1 $500K–$1M+ acquisition mandate.",
             "Some proposal writing exposure but supporting role, not lead.",
         ],
         questions=[
             "Have you personally led a proposal from conception to submission and won it — not as a contributor but as the lead?",
             "In your 4 years at READ Foundation, can you name a specific grant you helped close and describe your exact role?",
             "What exposure do you have to USAID, FCDO, World Bank, or other multilateral donors beyond reporting to them?",
             "What is your career goal — do you see yourself moving into frontline fundraising acquisition?",
             "What would your plan be to hit a $500K fundraising target in year one with no existing institutional relationships?",
         ],
         notes="Most affordable in-budget candidate but experience level is too junior for the Year 1 mandate. Consider for a future junior support role if the team grows."),
]


# ── Build interactive HTML ──────────────────────────────────────
profiles_html = ""
for c in candidates:
    profiles_html += make_profile_html(**c)

interactive_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Job 32 — Fundraising &amp; Partnerships Manager — Interactive Screening Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; font-size: 14px; color: #111827; max-width: 1100px; margin: 0 auto; padding: 24px; background: #f9fafb; }}
    h1 {{ color: #fff; }}
    h2 {{ color: #6B21A8; border-bottom: 3px solid #EC4899; padding-bottom: 6px; margin-top: 40px; font-size: 18px; }}
    h3 {{ color: #6B21A8; margin-top: 20px; font-size: 15px; }}
    table {{ border-collapse: collapse; }}
    details summary::-webkit-details-marker {{ display: none; }}
    details[open] summary span.arrow {{ transform: rotate(180deg); display: inline-block; }}
    .nav-bar a {{ color: #7C3AED; text-decoration: none; margin-right: 16px; font-weight: bold; font-size: 13px; }}
    .nav-bar a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>

<!-- HEADER -->
<div style="background:#4C1D95;padding:20px 24px;border-radius:8px;margin-bottom:8px;">
  <h1 style="margin:0;font-size:22px;">&#128203; Interactive Screening Report — Fundraising &amp; Partnerships Manager</h1>
</div>
<p style="color:#6B21A8;font-weight:bold;margin-top:4px;">v6 &bull; 7-Dimension Evidence-Based Framework &bull; Top 10 Candidates &bull; 2026-03-03</p>
<p style="font-size:13px;color:#6B7280;">
  <b>How to use:</b> Click any candidate row to expand their full profile. Click again to collapse.
  Candidates 1–5 are shortlisted (Tier A/B/C). Candidates 6–10 are Extended Review (No-Hire but closest to threshold).
</p>

<!-- QUICK STATS -->
<div style="background:#EDE9FE;border-left:5px solid #7C3AED;border-radius:6px;padding:14px 18px;margin-bottom:24px;">
  <b>Pool:</b> 48 applications &bull; 37 CVs assessed &bull;
  <b style="color:#16A34A;">Tier A: 2</b> &bull;
  <b style="color:#1D4ED8;">Tier B: 2</b> &bull;
  <b style="color:#D97706;">Tier C: 1</b> &bull;
  <b style="color:#6B7280;">Extended Review: 5</b> &bull;
  No-Hire: 27 &bull;
  <b>Budget:</b> PKR 150,000–270,000/month
</div>

<!-- NAV -->
<div class="nav-bar" style="margin-bottom:20px;">
  <a href="#shortlist">Shortlist (1–5)</a>
  <a href="#extended">Extended Review (6–10)</a>
  <a href="#heatmap">Dimension Heatmap</a>
</div>

<!-- RANKED TABLE -->
<h2>Ranked Top 10</h2>
<table border="1" cellpadding="9" cellspacing="0" width="100%" style="border-collapse:collapse;border-color:#E5E7EB;font-size:13px;margin-bottom:24px;">
  <thead>
    <tr style="background:#4C1D95;color:#fff;">
      <th>#</th><th>Candidate</th><th>Score</th><th>Tier</th>
      <th>D1</th><th>D2</th><th>D3</th><th>D4</th><th>D5</th><th>D6</th><th>D7</th>
      <th>Salary</th><th>Budget</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><b style="color:#6B21A8;">1</b></td><td><b>Danish Hussain</b></td><td><b>97.5</b></td>
      <td style="background:#16A34A;color:#fff;font-weight:bold;text-align:center;">Tier A</td>
      <td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#16A34A;font-weight:bold;">4</td>
      <td>PKR 550,000</td><td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 8px;border-radius:10px;">Out +280K</span></td></tr>
    <tr style="background:#F5F3FF;"><td><b style="color:#DB2777;">2</b></td><td><b>Zain Ul Abideen &#128269;</b></td><td><b>95.0</b></td>
      <td style="background:#16A34A;color:#fff;font-weight:bold;text-align:center;">Tier A</td>
      <td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td>
      <td>PKR 350,000</td><td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 8px;border-radius:10px;">Out +80K</span></td></tr>
    <tr><td><b style="color:#1D4ED8;">3</b></td><td><b>Mizhgan Kirmani</b></td><td><b>78.8</b></td>
      <td style="background:#1D4ED8;color:#fff;font-weight:bold;text-align:center;">Tier B</td>
      <td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td>
      <td>PKR 250,000</td><td><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:2px 8px;border-radius:10px;">In Budget</span></td></tr>
    <tr style="background:#F5F3FF;"><td><b style="color:#D97706;">4</b></td><td><b>Arsalan Ashraf</b></td><td><b>72.2</b></td>
      <td style="background:#1D4ED8;color:#fff;font-weight:bold;text-align:center;">Tier B</td>
      <td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#16A34A;font-weight:bold;">4</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#16A34A;font-weight:bold;">4</td>
      <td>PKR 450,000</td><td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 8px;border-radius:10px;">Out +180K</span></td></tr>
    <tr><td><b style="color:#DC2626;">5</b></td><td><b>Sadia Sohail</b></td><td><b>57.3</b></td>
      <td style="background:#D97706;color:#fff;font-weight:bold;text-align:center;">Tier C</td>
      <td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#EAB308;font-weight:bold;">2</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#EAB308;font-weight:bold;">2</td><td style="text-align:center;color:#22C55E;font-weight:bold;">3</td><td style="text-align:center;color:#EAB308;font-weight:bold;">2</td>
      <td>PKR 140,000</td><td><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:2px 8px;border-radius:10px;">In Budget</span></td></tr>
    <tr style="background:#F9FAFB;"><td style="color:#6B7280;">6</td><td>Arsim Tariq</td><td>49.2</td>
      <td style="background:#6B7280;color:#fff;text-align:center;font-size:11px;">Extended</td>
      <td style="text-align:center;color:#EAB308;">2</td><td style="text-align:center;color:#EAB308;">2</td><td style="text-align:center;color:#22C55E;">3</td><td style="text-align:center;color:#EAB308;">2</td><td style="text-align:center;color:#EAB308;">2</td><td style="text-align:center;color:#EAB308;">2</td><td style="text-align:center;color:#22C55E;">3</td>
      <td>PKR 280–300K</td><td><span style="background:#FEF3C7;color:#92400E;font-weight:bold;padding:2px 8px;border-radius:10px;">Borderline</span></td></tr>
    <tr><td style="color:#6B7280;">7</td><td>Ahmed Al-Mayadeen</td><td>45.5</td>
      <td style="background:#6B7280;color:#fff;text-align:center;font-size:11px;">Extended</td>
      <td style="text-align:center;color:#16A34A;">4</td><td style="text-align:center;color:#16A34A;">4</td><td style="text-align:center;color:#DC2626;">1</td><td style="text-align:center;color:#16A34A;">4</td><td style="text-align:center;color:#22C55E;">3</td><td style="text-align:center;color:#22C55E;">3</td><td style="text-align:center;color:#22C55E;">3</td>
      <td>~PKR 980,000</td><td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 8px;border-radius:10px;">Out massively</span></td></tr>
    <tr style="background:#F9FAFB;"><td style="color:#6B7280;">8</td><td>Ahad Ahsan Khan</td><td>41.8</td>
      <td style="background:#6B7280;color:#fff;text-align:center;font-size:11px;">Extended</td>
      <td style="text-align:center;color:#DC2626;">1</td><td style="text-align:center;color:#22C55E;">3</td><td style="text-align:center;color:#16A34A;">4</td><td style="text-align:center;color:#EAB308;">2</td><td style="text-align:center;color:#22C55E;">3</td><td style="text-align:center;color:#22C55E;">3</td><td style="text-align:center;color:#22C55E;">3</td>
      <td>PKR 550,000</td><td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 8px;border-radius:10px;">Out +280K</span></td></tr>
    <tr><td style="color:#6B7280;">9</td><td>Muhammad Usman</td><td>36.1</td>
      <td style="background:#6B7280;color:#fff;text-align:center;font-size:11px;">Extended</td>
      <td style="text-align:center;color:#EAB308;">2</td><td style="text-align:center;color:#DC2626;">1</td><td style="text-align:center;color:#22C55E;">3</td><td style="text-align:center;color:#EAB308;">2</td><td style="text-align:center;color:#22C55E;">3</td><td style="text-align:center;color:#DC2626;">1</td><td style="text-align:center;color:#22C55E;">3</td>
      <td>PKR 350,000</td><td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 8px;border-radius:10px;">Out +80K</span></td></tr>
    <tr style="background:#F9FAFB;"><td style="color:#6B7280;">10</td><td>Mushahid Hussain</td><td>34.4</td>
      <td style="background:#6B7280;color:#fff;text-align:center;font-size:11px;">Extended</td>
      <td style="text-align:center;color:#EAB308;">2</td><td style="text-align:center;color:#DC2626;">1</td><td style="text-align:center;color:#22C55E;">3</td><td style="text-align:center;color:#EAB308;">2</td><td style="text-align:center;color:#EAB308;">2</td><td style="text-align:center;color:#EAB308;">2</td><td style="text-align:center;color:#EAB308;">2</td>
      <td>PKR 170,000</td><td><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:2px 8px;border-radius:10px;">In Budget</span></td></tr>
  </tbody>
</table>

<!-- SHORTLISTED PROFILES -->
<h2 id="shortlist">Shortlisted Profiles — Tier A / B / C (Candidates 1–5)</h2>
<p style="font-size:13px;color:#6B7280;">Click each row to expand the full candidate profile, dimension scores, interview questions, and compensation analysis.</p>
{("".join(make_profile_html(**c) for c in candidates[:5]))}

<!-- EXTENDED REVIEW -->
<h2 id="extended">Extended Review — Candidates 6–10</h2>
<p style="font-size:13px;color:#6B7280;">These candidates did not meet the shortlist threshold but are the closest to it. Review if the pool above does not yield a hire.</p>
{("".join(make_profile_html(**c) for c in candidates[5:]))}

<!-- DIMENSION HEATMAP -->
<h2 id="heatmap">Dimension Heatmap — All 10 Candidates</h2>
<p style="font-size:13px;color:#6B7280;">Colour scale: <b style="color:#16A34A;">&#9632;</b> 4=Exceptional &nbsp; <b style="color:#22C55E;">&#9632;</b> 3=Strong &nbsp; <b style="color:#EAB308;">&#9632;</b> 2=Partial &nbsp; <b style="color:#F97316;">&#9632;</b> 1=Weak &nbsp; <b style="color:#DC2626;">&#9632;</b> 0=Missing</p>
<table border="1" cellpadding="10" cellspacing="0" width="100%" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;">
  <thead>
    <tr style="background:#4C1D95;color:#fff;">
      <th style="text-align:left;">Candidate</th><th>Score</th>
      <th>D1 Functional<br>25%</th><th>D2 Outcomes<br>20%</th><th>D3 Environment<br>15%</th>
      <th>D4 Ownership<br>15%</th><th>D5 Stakeholder<br>10%</th><th>D6 Hard Skills<br>10%</th><th>D7 Growth<br>5%</th>
    </tr>
  </thead>
  <tbody>"""

heatmap_rows = ""
for c in candidates:
    d1,d2,d3,d4,d5,d6,d7 = c['dims']
    def hc(s):
        colors = {4:"#16A34A",3:"#22C55E",2:"#EAB308",1:"#F97316",0:"#DC2626"}
        return f'<td style="text-align:center;background:{colors[s]};color:#fff;font-weight:bold;">{s}</td>'
    bg = "#F5F3FF" if c['rank'] % 2 == 0 else "#fff"
    heatmap_rows += f'<tr style="background:{bg};"><td style="font-weight:{"bold" if c["rank"]<=5 else "normal"};padding:8px;">{c["rank"]}. {c["name"]}</td><td style="text-align:center;font-weight:bold;">{c["score"]}</td>{hc(d1)}{hc(d2)}{hc(d3)}{hc(d4)}{hc(d5)}{hc(d6)}{hc(d7)}</tr>'

interactive_html += heatmap_rows + """
  </tbody>
</table>

<p style="font-size:12px;color:#6B7280;margin-top:24px;">
  D1=Functional Match (25%) &bull; D2=Demonstrated Outcomes (20%) &bull; D3=Environment Fit (15%) &bull;
  D4=Ownership &amp; Execution (15%) &bull; D5=Stakeholder &amp; Communication (10%) &bull;
  D6=Hard Skills/Technical (10%) &bull; D7=Growth &amp; Leadership (5%).<br>
  &#128269; = CV was scanned PDF recovered via OCR.
</p>

</body>
</html>"""

# Save the interactive HTML
os.makedirs(os.path.dirname(HTML_OUT), exist_ok=True)
with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(interactive_html)
print(f"Interactive HTML saved to: {HTML_OUT}")


# ══════════════════════════════════════════════════════════════════
# EMAIL HTML  (v6 — email-safe: tables only, inline styles, no SVG)
# ══════════════════════════════════════════════════════════════════

def email_dim_cell(s):
    colors = {4:"#16A34A", 3:"#22C55E", 2:"#EAB308", 1:"#F97316", 0:"#DC2626"}
    c = colors.get(s, "#DC2626")
    return f'<td bgcolor="{c}" style="background-color:{c};color:#fff;text-align:center;font-weight:bold;padding:6px 8px;">{s}/4</td>'

def email_profile(rank, emoji, name, score, tier, tier_color, salary, budget_label,
                  budget_color, budget_text_color, dims, strengths, risks, questions, notes="", missing_mh=0, ocr=False, **kwargs):
    d1,d2,d3,d4,d5,d6,d7 = dims
    ocr_tag = ' <span style="background:#EFF6FF;color:#1D4ED8;border-radius:10px;padding:2px 6px;font-size:11px;">&#128269; OCR</span>' if ocr else ""
    mh_warn = f'<p style="color:#D97706;font-size:12px;margin:4px 0;"><b>&#9888; {missing_mh} missing must-have(s) &mdash; &minus;{missing_mh*15}% penalty applied</b></p>' if missing_mh > 0 else ""
    str_items = "".join(f"<li style='margin-bottom:3px;font-size:13px;'>{s}</li>" for s in strengths)
    risk_items = "".join(f"<li style='margin-bottom:3px;font-size:13px;'>{r}</li>" for r in risks)
    q_items    = "".join(f"<li style='margin-bottom:3px;font-size:13px;'>{q}</li>" for q in questions)
    notes_html = f'<p style="font-size:12px;color:#6B7280;margin:6px 0;">{notes}</p>' if notes else ""

    return f"""
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:20px;">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-left:5px solid {tier_color};border-radius:6px;padding:16px;">
    <p style="margin:0 0 6px 0;font-size:15px;font-weight:bold;color:#111827;">
      {emoji} {name}{ocr_tag} &nbsp;
      <span style="background-color:{tier_color};color:#fff;border-radius:20px;padding:4px 14px;font-weight:bold;font-size:13px;">{score} / 100</span>
      &nbsp;<span style="background:{budget_color};color:{budget_text_color};font-weight:bold;padding:3px 10px;border-radius:12px;font-size:12px;">{budget_label}</span>
    </p>
    {mh_warn}
    <table width="100%" border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:11px;margin-bottom:10px;">
      <tr>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;padding:5px;">D1 Functional<br>25%</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;padding:5px;">D2 Outcomes<br>20%</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;padding:5px;">D3 Environment<br>15%</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;padding:5px;">D4 Ownership<br>15%</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;padding:5px;">D5 Stakeholder<br>10%</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;padding:5px;">D6 Hard Skills<br>10%</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;padding:5px;">D7 Growth<br>5%</th>
      </tr>
      <tr>{email_dim_cell(d1)}{email_dim_cell(d2)}{email_dim_cell(d3)}{email_dim_cell(d4)}{email_dim_cell(d5)}{email_dim_cell(d6)}{email_dim_cell(d7)}</tr>
    </table>
    <p style="margin:4px 0;font-size:12px;"><b>Salary:</b> {salary}</p>
    <p style="margin:6px 0;"><b style="color:#16A34A;">&#10003; Strengths:</b></p>
    <ul style="margin:2px 0;padding-left:18px;">{str_items}</ul>
    <p style="margin:6px 0;"><b style="color:#DC2626;">&#9888; Risks:</b></p>
    <ul style="margin:2px 0;padding-left:18px;">{risk_items}</ul>
    <p style="margin:6px 0;"><b style="color:#1D4ED8;">&#128172; Interview Questions:</b></p>
    <ol style="margin:2px 0;padding-left:18px;">{q_items}</ol>
    {notes_html}
  </td></tr>
</table>"""

def email_extended_profile(rank, name, score, dims, salary, budget_label, budget_color, budget_text_color, strengths, risks, notes, missing_mh=0, **kwargs):
    d1,d2,d3,d4,d5,d6,d7 = dims
    return f"""
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:12px;">
  <tr><td bgcolor="#F9FAFB" style="background:#F9FAFB;border:1px solid #E5E7EB;border-left:4px solid #6B7280;border-radius:6px;padding:12px 16px;">
    <p style="margin:0 0 4px 0;font-size:14px;font-weight:bold;color:#374151;">
      #{rank} {name} &nbsp;
      <span style="background:#6B7280;color:#fff;border-radius:12px;padding:2px 10px;font-size:12px;">{score} / 100</span>
      &nbsp;<span style="background:{budget_color};color:{budget_text_color};border-radius:10px;padding:2px 8px;font-size:11px;font-weight:bold;">{budget_label}</span>
    </p>
    {"".join(f'<p style="font-size:12px;color:#D97706;margin:2px 0;"><b>&#9888; {missing_mh} missing must-have(s)</b></p>' if missing_mh > 0 else "")}
    <table width="100%" border="1" cellpadding="4" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:11px;margin:6px 0;">
      <tr>
        <th bgcolor="#6B7280" style="background:#6B7280;color:#fff;text-align:center;padding:3px;">D1</th>
        <th bgcolor="#6B7280" style="background:#6B7280;color:#fff;text-align:center;padding:3px;">D2</th>
        <th bgcolor="#6B7280" style="background:#6B7280;color:#fff;text-align:center;padding:3px;">D3</th>
        <th bgcolor="#6B7280" style="background:#6B7280;color:#fff;text-align:center;padding:3px;">D4</th>
        <th bgcolor="#6B7280" style="background:#6B7280;color:#fff;text-align:center;padding:3px;">D5</th>
        <th bgcolor="#6B7280" style="background:#6B7280;color:#fff;text-align:center;padding:3px;">D6</th>
        <th bgcolor="#6B7280" style="background:#6B7280;color:#fff;text-align:center;padding:3px;">D7</th>
      </tr>
      <tr>{email_dim_cell(d1)}{email_dim_cell(d2)}{email_dim_cell(d3)}{email_dim_cell(d4)}{email_dim_cell(d5)}{email_dim_cell(d6)}{email_dim_cell(d7)}</tr>
    </table>
    <p style="font-size:12px;margin:4px 0;"><b>Salary:</b> {salary}</p>
    <p style="font-size:12px;margin:4px 0;color:#16A34A;"><b>Strength:</b> {strengths[0] if strengths else "—"}</p>
    <p style="font-size:12px;margin:4px 0;color:#DC2626;"><b>Key risk:</b> {risks[0] if risks else "—"}</p>
    <p style="font-size:11px;color:#6B7280;margin:4px 0;font-style:italic;">{notes}</p>
  </td></tr>
</table>"""


html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;font-size:14px;color:#111827;max-width:1100px;margin:0 auto;padding:24px;background:#fafafa;">

<!-- HEADER -->
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:8px;">
  <tr><td bgcolor="#4C1D95" style="background-color:#4C1D95;padding:20px 24px;border-radius:8px;">
    <span style="color:#ffffff;font-size:22px;font-weight:bold;">&#128203; Candidate Screening Report &mdash; Fundraising &amp; Partnerships Manager</span>
  </td></tr>
</table>
<p style="color:#6B21A8;font-weight:bold;margin-top:4px;">v6 &bull; 7-Dimension Evidence-Based Framework &bull; Top 10 Candidates &bull; 2026-03-03</p>

<!-- ══ 1. SCREENING SUMMARY ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">1. Screening Summary</h2>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#EDE9FE" style="background-color:#EDE9FE;border-left:5px solid #7C3AED;border-radius:6px;padding:16px 20px;">
    <table cellpadding="5" cellspacing="0" border="0">
      <tr><td style="color:#6B21A8;font-weight:bold;padding-right:20px;white-space:nowrap;">Job</td><td>Fundraising &amp; Partnerships Manager (Job ID JOB-0032)</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Date</td><td>2026-03-03</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Pool</td><td>48 applications</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">CVs assessed</td><td>37 (36 standard PDF + 1 OCR-recovered) &bull; 11 excluded (9 no-resume, 1 test/junk, 1 duplicate)</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Budget</td><td>PKR 150,000 &ndash; 270,000 / month</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Scoring</td><td>7-Dimension Evidence-Based Model (0&ndash;100)</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Shortlist</td><td><b style="color:#16A34A;">Tier A: 2</b> &bull; <b style="color:#1D4ED8;">Tier B: 2</b> &bull; <b style="color:#D97706;">Tier C: 1</b> &bull; <b style="color:#6B7280;">Extended Review: 5</b> &bull; No-Hire: 27</td></tr>
    </table>
  </td></tr>
</table>

<!-- ══ 2. TOP-10 RANKED TABLE ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">2. Ranked Top 10</h2>
<p style="font-size:12px;color:#6B7280;margin-bottom:8px;">Pool of 48 (&ge;40) &rarr; top 10 per shortlist size rule. Candidates 1&ndash;5 = shortlisted. Candidates 6&ndash;10 = Extended Review (see Section 6).</p>

<table width="100%" border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">#</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Candidate</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Score</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Tier</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D1</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D2</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D3</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D4</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D5</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D6</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D7</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Salary</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Budget</th>
  </tr>
  <!-- Tier A -->
  <tr>
    <td><b style="color:#6B21A8;">1</b></td><td><b>Danish Hussain</b></td><td><b>97.5</b></td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;font-weight:bold;text-align:center;">Tier A</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td>PKR 550,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 6px;border-radius:8px;">Out +280K</span></td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#DB2777;">2</b></td><td><b>Zain Ul Abideen &#128269;</b></td><td><b>95.0</b></td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;font-weight:bold;text-align:center;">Tier A</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td>PKR 350,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 6px;border-radius:8px;">Out +80K</span></td>
  </tr>
  <!-- Tier B -->
  <tr>
    <td><b style="color:#1D4ED8;">3</b></td><td><b>Mizhgan Kirmani</b></td><td><b>78.8</b></td>
    <td bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;font-weight:bold;text-align:center;">Tier B</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td>PKR 250,000</td>
    <td><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:2px 6px;border-radius:8px;">In Budget</span></td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#D97706;">4</b></td><td><b>Arsalan Ashraf</b></td><td><b>72.2</b></td>
    <td bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;font-weight:bold;text-align:center;">Tier B</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4</td>
    <td>PKR 450,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 6px;border-radius:8px;">Out +180K</span></td>
  </tr>
  <!-- Tier C -->
  <tr>
    <td><b style="color:#DC2626;">5</b></td><td><b>Sadia Sohail</b></td><td><b>57.3</b></td>
    <td bgcolor="#D97706" style="background-color:#D97706;color:#fff;font-weight:bold;text-align:center;">Tier C</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;font-weight:bold;">2</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;font-weight:bold;">2</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;font-weight:bold;">2</td>
    <td>PKR 140,000</td>
    <td><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:2px 6px;border-radius:8px;">In Budget</span></td>
  </tr>
  <!-- Extended Review divider -->
  <tr><td colspan="13" bgcolor="#F3F4F6" style="background-color:#F3F4F6;text-align:center;font-size:11px;color:#6B7280;padding:4px;font-style:italic;">
    &mdash;&mdash; Extended Review: closest to threshold, did not meet shortlist criteria &mdash;&mdash;
  </td></tr>
  <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
    <td style="color:#6B7280;">6</td><td>Arsim Tariq</td><td>49.2</td>
    <td bgcolor="#6B7280" style="background-color:#6B7280;color:#fff;text-align:center;font-size:11px;">Extended</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td style="font-size:11px;">PKR 280&ndash;300K</td>
    <td><span style="background:#FEF3C7;color:#92400E;padding:2px 6px;border-radius:8px;font-size:11px;">Borderline</span></td>
  </tr>
  <tr>
    <td style="color:#6B7280;">7</td><td>Ahmed Al-Mayadeen</td><td>45.5</td>
    <td bgcolor="#6B7280" style="background-color:#6B7280;color:#fff;text-align:center;font-size:11px;">Extended</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;">4</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;">4</td>
    <td bgcolor="#DC2626" style="background-color:#DC2626;color:#fff;text-align:center;">1</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;">4</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td style="font-size:11px;">~PKR 980,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;padding:2px 6px;border-radius:8px;font-size:11px;">Out massively</span></td>
  </tr>
  <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
    <td style="color:#6B7280;">8</td><td>Ahad Ahsan Khan</td><td>41.8</td>
    <td bgcolor="#6B7280" style="background-color:#6B7280;color:#fff;text-align:center;font-size:11px;">Extended</td>
    <td bgcolor="#DC2626" style="background-color:#DC2626;color:#fff;text-align:center;">1</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;">4</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td style="font-size:11px;">PKR 550,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;padding:2px 6px;border-radius:8px;font-size:11px;">Out +280K</span></td>
  </tr>
  <tr>
    <td style="color:#6B7280;">9</td><td>Muhammad Usman</td><td>36.1</td>
    <td bgcolor="#6B7280" style="background-color:#6B7280;color:#fff;text-align:center;font-size:11px;">Extended</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td bgcolor="#DC2626" style="background-color:#DC2626;color:#fff;text-align:center;">1</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td bgcolor="#DC2626" style="background-color:#DC2626;color:#fff;text-align:center;">1</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td style="font-size:11px;">PKR 350,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;padding:2px 6px;border-radius:8px;font-size:11px;">Out +80K</span></td>
  </tr>
  <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
    <td style="color:#6B7280;">10</td><td>Mushahid Hussain</td><td>34.4</td>
    <td bgcolor="#6B7280" style="background-color:#6B7280;color:#fff;text-align:center;font-size:11px;">Extended</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td bgcolor="#DC2626" style="background-color:#DC2626;color:#fff;text-align:center;">1</td>
    <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">3</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td bgcolor="#EAB308" style="background-color:#EAB308;color:#fff;text-align:center;">2</td>
    <td style="font-size:11px;">PKR 170,000</td>
    <td><span style="background:#DCFCE7;color:#166534;padding:2px 6px;border-radius:8px;font-size:11px;">In Budget</span></td>
  </tr>
</table>
<p style="font-size:11px;color:#6B7280;margin-top:4px;">D1=Functional Match &bull; D2=Demonstrated Outcomes &bull; D3=Environment Fit &bull; D4=Ownership &bull; D5=Stakeholder &bull; D6=Hard Skills &bull; D7=Growth. &#128269;=OCR-recovered.</p>

<!-- ══ 3. TIER A PROFILES ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">3. Tier A Profiles &mdash; Strong Move Forward</h2>
"""

# Add Tier A profiles
for c in candidates[:2]:
    html += email_profile(**c)

html += """
<!-- ══ 4. TIER B PROFILES ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">4. Tier B Profiles &mdash; Interview with Focused Validation</h2>
"""

for c in candidates[2:4]:
    html += email_profile(**c)

html += """
<!-- ══ 5. TIER C PROFILE ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">5. Tier C Profile &mdash; Risky / Backup Only</h2>
"""

html += email_profile(**candidates[4])

html += """
<!-- ══ 6. EXTENDED REVIEW ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">6. Extended Review &mdash; Candidates 6&ndash;10</h2>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#FEF3C7" style="background-color:#FEF3C7;border-left:5px solid #D97706;border-radius:6px;padding:12px 16px;margin-bottom:12px;">
    <p style="margin:0;font-size:13px;color:#92400E;">
      <b>Why these candidates are here:</b> They scored below 55 (No-Hire threshold) but are closest to the cut.
      If Tier A and B interviews do not yield a hire, these 5 are the next to consider &mdash; in that order.
      For full profiles with interview questions, open the interactive HTML report.
    </p>
  </td></tr>
</table>
<br>
"""

for c in candidates[5:]:
    html += email_extended_profile(**c)

html += """
<!-- ══ 7. SCORE BAR CHART ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">7. Charts &amp; Visuals</h2>

<h3 style="color:#6B21A8;margin-top:20px;">A. Score Distribution &mdash; All 10 Candidates</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:16px;">
    <table width="100%" cellpadding="0" cellspacing="5" border="0">

      <tr>
        <td width="200" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Danish Hussain <b style="color:#16A34A;">&#9650;A</b></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="97%" bgcolor="#16A34A" height="24" style="background-color:#16A34A;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">97.5 &nbsp;Out +280K</td>
          <td bgcolor="#F3F4F6" height="24" style="background-color:#F3F4F6;width:3%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="200" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Zain Ul Abideen &#128269; <b style="color:#16A34A;">&#9650;A</b></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="95%" bgcolor="#22C55E" height="24" style="background-color:#22C55E;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">95.0 &nbsp;Out +80K</td>
          <td bgcolor="#F3F4F6" height="24" style="background-color:#F3F4F6;width:5%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="200" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Mizhgan Kirmani <b style="color:#1D4ED8;">&#9650;B</b></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="79%" bgcolor="#1D4ED8" height="24" style="background-color:#1D4ED8;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">78.8 &nbsp;&#10003; In Budget</td>
          <td bgcolor="#F3F4F6" height="24" style="background-color:#F3F4F6;width:21%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="200" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Arsalan Ashraf <b style="color:#1D4ED8;">&#9650;B</b></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="72%" bgcolor="#7C3AED" height="24" style="background-color:#7C3AED;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">72.2 &nbsp;Out +180K</td>
          <td bgcolor="#F3F4F6" height="24" style="background-color:#F3F4F6;width:28%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="200" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Sadia Sohail <b style="color:#D97706;">&#9650;C</b></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="57%" bgcolor="#D97706" height="24" style="background-color:#D97706;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">57.3 &nbsp;&#10003; In Budget</td>
          <td bgcolor="#F3F4F6" height="24" style="background-color:#F3F4F6;width:43%;"></td>
        </tr></table></td>
      </tr>

      <tr><td colspan="2" style="padding:4px 0;"><hr style="border:none;border-top:1px dashed #D1D5DB;margin:2px 0;"></td></tr>

      <tr>
        <td width="200" align="right" style="font-size:11px;color:#9CA3AF;padding-right:8px;white-space:nowrap;">Arsim Tariq <span style="color:#6B7280;">Ext.</span></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="49%" bgcolor="#9CA3AF" height="20" style="background-color:#9CA3AF;color:#fff;font-size:10px;font-weight:bold;padding:0 6px;white-space:nowrap;">49.2</td>
          <td bgcolor="#F3F4F6" height="20" style="background-color:#F3F4F6;width:51%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="200" align="right" style="font-size:11px;color:#9CA3AF;padding-right:8px;white-space:nowrap;">Ahmed Al-Mayadeen <span style="color:#6B7280;">Ext.</span></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="45%" bgcolor="#9CA3AF" height="20" style="background-color:#9CA3AF;color:#fff;font-size:10px;font-weight:bold;padding:0 6px;white-space:nowrap;">45.5</td>
          <td bgcolor="#F3F4F6" height="20" style="background-color:#F3F4F6;width:55%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="200" align="right" style="font-size:11px;color:#9CA3AF;padding-right:8px;white-space:nowrap;">Ahad Ahsan Khan <span style="color:#6B7280;">Ext.</span></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="42%" bgcolor="#9CA3AF" height="20" style="background-color:#9CA3AF;color:#fff;font-size:10px;font-weight:bold;padding:0 6px;white-space:nowrap;">41.8</td>
          <td bgcolor="#F3F4F6" height="20" style="background-color:#F3F4F6;width:58%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="200" align="right" style="font-size:11px;color:#9CA3AF;padding-right:8px;white-space:nowrap;">Muhammad Usman <span style="color:#6B7280;">Ext.</span></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="36%" bgcolor="#9CA3AF" height="20" style="background-color:#9CA3AF;color:#fff;font-size:10px;font-weight:bold;padding:0 6px;white-space:nowrap;">36.1</td>
          <td bgcolor="#F3F4F6" height="20" style="background-color:#F3F4F6;width:64%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="200" align="right" style="font-size:11px;color:#9CA3AF;padding-right:8px;white-space:nowrap;">Mushahid Hussain <span style="color:#6B7280;">Ext.</span></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="34%" bgcolor="#9CA3AF" height="20" style="background-color:#9CA3AF;color:#fff;font-size:10px;font-weight:bold;padding:0 6px;white-space:nowrap;">34.4</td>
          <td bgcolor="#F3F4F6" height="20" style="background-color:#F3F4F6;width:66%;"></td>
        </tr></table></td>
      </tr>

    </table>
  </td></tr>
</table>

<!-- B. Pool Composition -->
<h3 style="color:#6B21A8;margin-top:24px;">B. Pool Composition</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:16px;">
    <p style="font-size:12px;margin:0 0 8px 0;color:#374151;"><b>48 Applications &rarr; Tier breakdown:</b></p>
    <table width="100%" cellpadding="0" cellspacing="2" border="0">
      <tr>
        <td width="5%" bgcolor="#16A34A" height="32" style="background-color:#16A34A;color:#fff;font-size:11px;font-weight:bold;text-align:center;padding:4px 2px;vertical-align:middle;">Tier A<br>2</td>
        <td width="5%" bgcolor="#1D4ED8" height="32" style="background-color:#1D4ED8;color:#fff;font-size:11px;font-weight:bold;text-align:center;padding:4px 2px;vertical-align:middle;">Tier B<br>2</td>
        <td width="3%" bgcolor="#D97706" height="32" style="background-color:#D97706;color:#fff;font-size:11px;font-weight:bold;text-align:center;padding:4px 2px;vertical-align:middle;">C<br>1</td>
        <td width="13%" bgcolor="#6B7280" height="32" style="background-color:#6B7280;color:#fff;font-size:11px;font-weight:bold;text-align:center;padding:4px 2px;vertical-align:middle;">Ext. Review<br>5</td>
        <td width="58%" bgcolor="#DC2626" height="32" style="background-color:#DC2626;color:#fff;font-size:11px;font-weight:bold;text-align:center;padding:4px 2px;vertical-align:middle;">No-Hire (27)</td>
        <td width="16%" bgcolor="#F3F4F6" height="32" style="background-color:#F3F4F6;color:#374151;font-size:11px;font-weight:bold;text-align:center;padding:4px 2px;vertical-align:middle;">No CV (11)</td>
      </tr>
    </table>
    <p style="font-size:11px;color:#6B7280;margin:8px 0 0 0;">Only 5 of 37 assessable CVs reached Tier C or above &mdash; this is a competitive specialist role.</p>
  </td></tr>
</table>

<!-- C. Dimension Heatmap (email version) -->
<h3 style="color:#6B21A8;margin-top:24px;">C. Dimension Heatmap &mdash; Top 10</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:12px;">
    <table width="100%" border="1" cellpadding="7" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:11px;">
      <tr>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:left;padding:6px 8px;">Candidate</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">Score</th>
        <th bgcolor="#7C3AED" style="background-color:#7C3AED;color:#fff;text-align:center;">D1<br>Funct.</th>
        <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">D2<br>Outcomes</th>
        <th bgcolor="#0891B2" style="background-color:#0891B2;color:#fff;text-align:center;">D3<br>Environ.</th>
        <th bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;">D4<br>Ownership</th>
        <th bgcolor="#D97706" style="background-color:#D97706;color:#fff;text-align:center;">D5<br>Stakeh.</th>
        <th bgcolor="#DC2626" style="background-color:#DC2626;color:#fff;text-align:center;">D6<br>Hard Sk.</th>
        <th bgcolor="#DB2777" style="background-color:#DB2777;color:#fff;text-align:center;">D7<br>Growth</th>
      </tr>
"""

# Heatmap rows for email
hmap_data = [
    ("Danish Hussain",      97.5, (4,4,3,4,4,4,4), True),
    ("Zain Ul Abideen &#128269;", 95.0, (4,4,4,4,3,4,3), True),
    ("Mizhgan Kirmani",     78.8, (3,3,4,3,3,3,3), True),
    ("Arsalan Ashraf",      72.2, (4,3,3,4,3,3,4), True),
    ("Sadia Sohail",        57.3, (3,2,3,3,2,3,2), True),
    ("Arsim Tariq",         49.2, (2,2,3,2,2,2,3), False),
    ("Ahmed Al-Mayadeen",   45.5, (4,4,1,4,3,3,3), False),
    ("Ahad Ahsan Khan",     41.8, (1,3,4,2,3,3,3), False),
    ("Muhammad Usman",      36.1, (2,1,3,2,3,1,3), False),
    ("Mushahid Hussain",    34.4, (2,1,3,2,2,2,2), False),
]

for i, (nm, sc, ds, is_sh) in enumerate(hmap_data):
    bg = "#F5F3FF" if i % 2 == 0 else "#ffffff"
    fw = "bold" if is_sh else "normal"
    row = f'<tr bgcolor="{bg}" style="background-color:{bg};">'
    row += f'<td style="font-weight:{fw};padding:5px 8px;">{nm}</td>'
    row += f'<td style="text-align:center;font-weight:bold;">{sc}</td>'
    for d in ds:
        colors_map = {4:"#16A34A",3:"#22C55E",2:"#EAB308",1:"#F97316",0:"#DC2626"}
        clr = colors_map.get(d,"#DC2626")
        row += f'<td bgcolor="{clr}" style="background-color:{clr};color:#fff;text-align:center;font-weight:bold;">{d}</td>'
    row += "</tr>"
    html += row

html += """
    </table>
    <p style="font-size:10px;color:#6B7280;margin:6px 0 0 0;">
      Colour: <b style="color:#16A34A;">&#9632;</b> 4=Exceptional &nbsp;
      <b style="color:#22C55E;">&#9632;</b> 3=Strong &nbsp;
      <b style="color:#EAB308;">&#9632;</b> 2=Partial &nbsp;
      <b style="color:#F97316;">&#9632;</b> 1=Weak &nbsp;
      <b style="color:#DC2626;">&#9632;</b> 0=Missing. Bold rows = shortlisted.
    </p>
  </td></tr>
</table>

<!-- ══ 8. NEXT STEPS ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">8. Recommended Next Steps</h2>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#F5F3FF" style="background-color:#F5F3FF;border-left:5px solid #7C3AED;border-radius:6px;padding:14px 18px;">
    <ol style="margin:0;padding-left:20px;font-size:13px;line-height:1.8;">
      <li><b>Immediately invite Zain Ul Abideen (#2)</b> for a first-round interview &mdash; PKR 80K gap is negotiable, no relocation risk, Islamabad-based, strongest evidence-backed track record relative to salary ask.</li>
      <li><b>Invite Mizhgan Kirmani (#3)</b> simultaneously &mdash; she is the only Tier B candidate fully within budget. Two interviews in parallel avoids sequencing delay.</li>
      <li><b>Discuss Danish Hussain (#1)</b> at leadership level before inviting &mdash; the PKR 280K salary gap needs a decision in principle before interviewing. If leadership can approve a PKR 400K+ package, he is the best candidate in the pool by significant margin.</li>
      <li><b>Hold Arsalan Ashraf (#4)</b> pending outcomes of #2 and #3 &mdash; the missing multilateral must-have and Karachi location are addressable but require effort.</li>
      <li><b>Sadia Sohail (#5)</b> and Extended Review candidates only if the above four do not yield a hire.</li>
      <li><b>Consider re-posting</b> with a stronger signal that multilateral/bilateral donor experience is required &mdash; many applicants came from programme delivery and domestic NGO backgrounds which do not meet the core must-haves.</li>
    </ol>
  </td></tr>
</table>

<!-- Interactive HTML note -->
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:24px;">
  <tr><td bgcolor="#EFF6FF" style="background-color:#EFF6FF;border:1px solid #BFDBFE;border-radius:6px;padding:12px 16px;">
    <p style="margin:0;font-size:13px;color:#1D4ED8;">
      <b>&#128196; Interactive Report:</b> A full interactive HTML report has been generated with collapsible profiles for all 10 candidates, including complete interview question sets for the Extended Review candidates.
      File: <b>output/job32-report-interactive.html</b> &mdash; open in any browser to use.
    </p>
  </td></tr>
</table>

<p style="font-size:11px;color:#9CA3AF;margin-top:24px;text-align:center;">
  Taleemabad Talent Acquisition Agent &bull; Screening Report v6 &bull; 2026-03-03 &bull; Confidential
</p>

</body></html>"""


# ══════════════════════════════════════════════════════════════════
# SEND EMAIL
# ══════════════════════════════════════════════════════════════════
msg = MIMEMultipart("alternative")
msg["Subject"] = "Screening Report v6 — Fundraising & Partnerships Manager — Top 10 Candidates (Job 32)"
msg["From"]    = SENDER
msg["To"]      = RECIPIENT
msg.attach(MIMEText(html, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER, PASSWORD)
    allow_candidate_addresses(RECIPIENT if isinstance(RECIPIENT, list) else [RECIPIENT])
        safe_sendmail(server, SENDER, RECIPIENT, msg.as_string(), context='send_job32_report_v6')

print("Email sent successfully!")
