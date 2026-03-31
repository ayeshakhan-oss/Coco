import smtplib, os, io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses


RECIPIENT = "ayesha.khan@taleemabad.com"
SENDER    = os.getenv("EMAIL_USER")
PASSWORD  = os.getenv("EMAIL_PASSWORD")

# ══════════════════════════════════════════════════════════════════
# CANDIDATE DATA — enriched with USP, Org Signal, CV Quality
# (7-dimension scores from v5 screening, unchanged)
# ══════════════════════════════════════════════════════════════════

CANDIDATES = [
    {
        "rank": 1, "name": "Danish Hussain", "score": 97.5, "tier": "Tier A", "tier_color": "#16A34A",
        "salary": "PKR 550,000/month", "budget_label": "Out of Budget", "budget_gap": "+PKR 280,000",
        "budget_color": "#FEE2E2", "budget_text_color": "#991B1B",
        "dims": (4,4,3,4,4,4,4), "missing_mh": 0, "ocr": False,
        "total_exp": "~20 years", "relevant_exp": "~20 years (Head of Grants & Partnerships)",
        "current_role": "Head of Grants & Partnerships, INGO (Hyderabad)",
        "usp": "Only candidate with PKR 1B+ personally mobilised across FCDO, World Bank, UNDP, and ADB — the single highest verified fundraising track record in the entire 48-application pool. Brings a named multilateral network that would take years to build from scratch.",
        "org_signals": [
            ("🌐 Donor/Development", "FCDO Pakistan, World Bank, UNDP Pakistan, ADB — active named relationships"),
        ],
        "cv_quality": "High",
        "cv_quality_note": "Strongly quantified (PKR 1B+ mobilised), named donor relationships cited, clear career progression from grants officer to Head-level. Storytelling is focused and impact-driven.",
        "strengths": [
            "<b>PKR 1B+ mobilised</b> — highest single fundraising track record in pool. FCDO, World Bank, UNDP, ADB all named. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Head of Grants & Partnerships, 20 years</b> — most senior fundraising title in pool at exact functional level required. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Named active bilateral/multilateral relationships</b> — FCDO Pakistan, UNDP Pakistan, ADB. Donor network the JD is specifically designed to activate. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Hyderabad-based — states willing to relocate. Commitment and timeline must be confirmed in writing before proceeding.",
            "WASH/humanitarian sector dominant — EdTech fundraising is a pivot. Strong transferable donor base but Taleemabad positioning work needed.",
            "PKR 550,000 ask is 2× budget ceiling. Significant leadership sign-off needed before initiating interview.",
        ],
        "interview_qs": [
            "You've stated willingness to relocate — what is your realistic timeline and are there conditions on that commitment?",
            "Walk me through the single largest grant you personally closed — your exact role from first outreach to award letter.",
            "Your background is WASH/humanitarian — how would you reposition Taleemabad to FCDO, UNDP, and ADB as a credible EdTech investment?",
            "Which programme officers at FCDO Pakistan, UNDP Pakistan, and ADB are you in active relationship with right now?",
            "The budget ceiling is PKR 270K. Your ask is 550K. Is there a base + performance structure that could bridge this gap?",
        ],
        "confidence": "High",
    },
    {
        "rank": 2, "name": "Zain Ul Abideen", "score": 95.0, "tier": "Tier A", "tier_color": "#16A34A",
        "salary": "PKR 350,000/month", "budget_label": "Out of Budget", "budget_gap": "+PKR 80,000",
        "budget_color": "#FEE2E2", "budget_text_color": "#991B1B",
        "dims": (4,4,4,4,3,4,3), "missing_mh": 0, "ocr": True,
        "total_exp": "~10 years", "relevant_exp": "~10 years (resource mobilisation, two orgs)",
        "current_role": "Deputy Manager Resource Mobilisation, READ Foundation (Islamabad)",
        "usp": "US $50M lifetime fundraising proven across two separate Pakistan organisations (READ Foundation $8.44M + SPO $4.42M). Dual-organisation sequential success confirms a repeatable system, not single-org luck. Islamabad-based with the smallest budget gap of any out-of-budget candidate.",
        "org_signals": [
            ("🎓 EdTech/Competitor — HIGH STRATEGIC SIGNAL", "READ Foundation — direct Taleemabad sector competitor and peer organisation"),
            ("🌐 Donor/Development — HIGH STRATEGIC SIGNAL", "UNICEF, UNFPA, US Embassy, British Council, Oxfam, IRC, WaterAid, Save the Children"),
        ],
        "cv_quality": "High",
        "cv_quality_note": "Exceptionally specific: dollar amounts cited for two separate organisations, named donors listed, dual-org track record. The depth of evidence is the highest in the pool. CV was scanned PDF — recovered via OCR; would have been missed without OCR capability.",
        "strengths": [
            "<b>US $50M lifetime in won proposals</b> — $8.44M at READ Foundation (UNICEF, UNFPA, US Embassy, British Council, Oxfam, IRC, WaterAid, Save the Children) + $4.42M at SPO. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Deputy Manager Resource Mobilisation, Islamabad-based</b> — direct ownership of fundraising function, no relocation risk. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Broadest donor network breadth in pool</b> — 8 named international donor organisations with active Pakistan presence. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Freelance periods in CV — continuity of focus and reasons must be probed.",
            "WASH/humanitarian sector dominant — EdTech pivot required, though donor base overlaps significantly.",
            "PKR 350K is PKR 80K above ceiling — smallest gap in pool. Negotiable with a structured offer.",
        ],
        "interview_qs": [
            "Walk me through the single largest proposal you wrote and won — your exact role from first draft to award.",
            "Which specific programme officers at UNICEF, USAID, FCDO Pakistan have you worked with — are those relationships still active?",
            "You have raised predominantly in WASH/humanitarian — how would you approach pitching Taleemabad to those same donors?",
            "What caused the freelance periods in your CV and what were you working on during that time?",
            "Budget is PKR 150K–270K. Your ask is 350K. What flexibility exists, and what would make this worthwhile for you?",
        ],
        "confidence": "High",
    },
    {
        "rank": 3, "name": "Mizhgan Kirmani", "score": 78.8, "tier": "Tier B", "tier_color": "#1D4ED8",
        "salary": "PKR 250,000/month", "budget_label": "In Budget", "budget_gap": "—",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (3,3,4,3,3,3,3), "missing_mh": 0, "ocr": False,
        "total_exp": "~8 years", "relevant_exp": "~8 years (donor relations + resource mobilisation)",
        "current_role": "Manager, Donor Relations — The Citizens Foundation (TCF), Islamabad",
        "usp": "Only Tier B candidate who is simultaneously in-budget, Islamabad-based, and holds active relationships with FCDO, UN Women, UNDP, USAID, and Green Climate Fund — the exact donor mix Taleemabad needs. Zero location risk, zero budget risk. The best risk-adjusted hire in the pool.",
        "org_signals": [
            ("🎓 EdTech/Competitor — HIGH STRATEGIC SIGNAL", "The Citizens Foundation (TCF) — Pakistan's largest education NGO; direct peer and competitor to Taleemabad"),
            ("🌐 Donor/Development — HIGH STRATEGIC SIGNAL", "FCDO, UN Women, UNDP, USAID, Green Climate Fund — active donor relationships at TCF"),
        ],
        "cv_quality": "High",
        "cv_quality_note": "PKR 72M closed in a single financial year is clearly stated, donor names are specific, and role ownership is explicit. Strong organisational pedigree (TCF + Aga Khan Foundation). Clear progression visible.",
        "strengths": [
            "<b>Manager Donor Relations at TCF</b> — active fundraising with FCDO, UN Women, UNDP, USAID, Green Climate Fund. PKR 72M closed in FY. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Islamabad-based, in budget at PKR 250K</b> — zero location risk, zero budget exception required. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>8 years fundraising + Aga Khan Foundation background</b> — deep Pakistan education sector donor relationships. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "PKR 72M (~$260K) is below the Year 1 target of $500K–$1M+. Scale ambition needs validation.",
            "Largest independently closed single grant not evidenced — no $500K+ deal cited anywhere.",
            "Government/policy engagement in Islamabad not evidenced — ministry relationships absent from CV.",
        ],
        "interview_qs": [
            "What is the largest single grant you personally closed — walk through from donor identification to signed agreement?",
            "How do you manage a pipeline of 30–50 active opportunities simultaneously — what tools and cadence do you use?",
            "Which named programme officers at USAID Pakistan, FCDO Pakistan, or UNDP Pakistan have you built active relationships with?",
            "Have you written winning proposals without a dedicated proposal writer — can you describe your writing process and share a sample?",
            "The Year 1 target is $500K–$1M+ from cold. What does your 90-day plan look like from day one at Taleemabad?",
        ],
        "confidence": "High",
    },
    {
        "rank": 4, "name": "Arsalan Ashraf", "score": 72.2, "tier": "Tier B", "tier_color": "#1D4ED8",
        "salary": "PKR 450,000/month", "budget_label": "Out of Budget", "budget_gap": "+PKR 180,000",
        "budget_color": "#FEE2E2", "budget_text_color": "#991B1B",
        "dims": (4,3,3,4,3,3,4), "missing_mh": 1, "ocr": False,
        "total_exp": "~12 years", "relevant_exp": "~10 years (fundraising/BD at NGOs)",
        "current_role": "Director of Fundraising & Business Development, NGO (Karachi)",
        "usp": "Only candidate who has built fundraising functions from zero at three separate organisations — demonstrating a repeatable builder's playbook. If Taleemabad's priority is building the BD function from scratch, his track record of doing exactly that is uniquely relevant.",
        "org_signals": [],
        "cv_quality": "Moderate-High",
        "cv_quality_note": "Some quantification (Meta $100K, Chevron $250K, PKR 80M NAVTTC) and a clear builder narrative across three organisations. However, corporate CSR framing limits multilateral-sector clarity. Storytelling is good but sector-pivot gap is apparent.",
        "strengths": [
            "<b>Built fundraising functions from scratch at 3 NGOs</b> — clearest builder track record in pool for a zero-to-one mandate. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Pipeline of 15–20 active opportunities managed simultaneously</b> — strong pipeline discipline. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Closed Meta $100K, Chevron $250K, PKR 80M NAVTTC</b> — deal-closing track record even if corporate-focused. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Corporate CSR and foundation focus — limited multilateral/bilateral (USAID, World Bank, FCDO, EU) experience. Missing must-have (-15% penalty applied).",
            "Karachi-based — willing to relocate stated but requires confirmation as firm commitment with timeline.",
            "PKR 450K ask is PKR 180K above ceiling — significant exception required.",
        ],
        "interview_qs": [
            "Your background is primarily corporate CSR — have you directly engaged USAID, FCDO, World Bank, or EU as a prime grantee (not sub-grantee)?",
            "Walk me through the USAID sub-grantee experience — what was your specific role in that funding relationship?",
            "Which Pakistan-based multilateral donor programme officers are you currently in active relationship with?",
            "You have built fundraising functions from scratch at 3 orgs — what is your 90-day blueprint and what would you do differently at Taleemabad?",
            "Budget ceiling is PKR 270K. Your ask is 450K. Is there a base + performance structure that bridges this?",
        ],
        "confidence": "High",
    },
    {
        "rank": 5, "name": "Sadia Sohail", "score": 57.3, "tier": "Tier C", "tier_color": "#D97706",
        "salary": "PKR 140,000/month", "budget_label": "In Budget", "budget_gap": "—",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (3,2,3,3,2,3,2), "missing_mh": 1, "ocr": False,
        "total_exp": "~8 years", "relevant_exp": "~8 years (donor relations, READ Foundation)",
        "current_role": "Donor Relations Officer, READ Foundation (Islamabad)",
        "usp": "Most affordable in-budget option with 8 years of fundraising-adjacent experience at READ Foundation (a direct Taleemabad peer). Three fundraising certifications demonstrate deliberate career investment in the function. Best growth-potential option if timeline allows for a 6-month ramp-up.",
        "org_signals": [
            ("🎓 EdTech/Competitor — Strategic Signal", "READ Foundation — 8 years in donor relations at a direct Taleemabad peer organisation"),
        ],
        "cv_quality": "Moderate",
        "cv_quality_note": "Clear organisation tenure and certifications listed, but no quantified outcomes anywhere in CV. Responsibilities are described without amounts raised or grants won. Three fundraising certifications show intent but outcomes are absent.",
        "strengths": [
            "<b>8 years donor relations at READ Foundation</b> — proposal writing, donor comms, budget reporting. Direct sector pedigree. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>3 fundraising certifications</b> — Major Donor Fundraising, NGO Boot Camp, Fundraising Essentials. Investment in the craft. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Islamabad-based, in budget at PKR 140K</b> — most affordable option with genuine donor relations background. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "READ Foundation is a domestic NGO — no multilateral or bilateral (USAID/WB/FCDO/EU) experience. Missing must-have (-15% penalty applied).",
            "Zero quantified outcomes across 8 years — grants won and amounts raised not cited anywhere.",
            "8 years at Donor Relations Officer level without BD progression — management readiness unproven.",
        ],
        "interview_qs": [
            "Have you engaged with any international donors — USAID, FCDO, World Bank, UNDP, EU — in a fundraising capacity?",
            "What is the largest single grant you personally helped close — amount, donor, your exact role?",
            "What is your understanding of how USAID or FCDO Pakistan structures competitive grant rounds?",
            "How would you approach building relationships with international donors you have not previously worked with?",
            "What has kept you at Donor Relations Officer level for 8 years — and what changed that you are now seeking a Manager role?",
        ],
        "confidence": "High",
    },
    # Extended Review
    {
        "rank": 6, "name": "Arsim Tariq", "score": 49.2, "tier": "Extended Review", "tier_color": "#6B7280",
        "salary": "PKR 280,000–300,000/month", "budget_label": "Borderline Out", "budget_gap": "+PKR 10,000–30,000",
        "budget_color": "#FEF3C7", "budget_text_color": "#92400E",
        "dims": (2,2,3,2,2,2,3), "missing_mh": 1, "ocr": False,
        "total_exp": "~10 years", "relevant_exp": "~2 years (proposal contributions — not BD ownership)",
        "current_role": "Programme Manager / M&E Lead (FCDO & World Bank funded projects, Islamabad)",
        "usp": "Deepest sector context in the Extended Review pool — 10 years on FCDO and World Bank-funded contracts gives genuine understanding of donor requirements. Could transition into BD with targeted development; not ready for immediate Year-1 acquisition mandate.",
        "org_signals": [
            ("🌐 Donor/Development — Strategic Signal", "10+ years on FCDO and World Bank-funded contracts (programme management side)"),
        ],
        "cv_quality": "Moderate",
        "cv_quality_note": "Sector credibility is clear and FCDO/World Bank experience is specific. However, role descriptions conflate programme delivery with fundraising acquisition — outcome attribution is ambiguous. EdTech mention adds relevance.",
        "strengths": [
            "10+ years in development sector — FCDO and World Bank-funded contracts, deep sector knowledge.",
            "Islamabad-based, NUST MS graduate. EdTech experience mentioned.",
            "Contributed to winning proposals for FCDO and World Bank bids.",
        ],
        "risks": [
            "Primary role is programme management and M&E — not fundraising/BD ownership. Missing must-have.",
            "No evidence of independently closing new donor relationships or building a fundraising pipeline.",
            "Salary 280–300K is borderline above ceiling of 270K.",
        ],
        "interview_qs": [
            "In proposals you contributed to for FCDO and World Bank — were you the lead author and donor relationship owner, or the technical contributor?",
            "Have you independently managed a donor pipeline and closed new funding relationships without a BD lead above you?",
            "If hired as fundraising lead, how would you shift from a programme/M&E mindset to a revenue acquisition mindset?",
        ],
        "confidence": "High",
    },
    {
        "rank": 7, "name": "Ahmed Al-Mayadeen", "score": 45.5, "tier": "Extended Review", "tier_color": "#6B7280",
        "salary": "~PKR 980,000/month (USD 3,500)", "budget_label": "Out of Budget", "budget_gap": "+PKR 710,000",
        "budget_color": "#FEE2E2", "budget_text_color": "#991B1B",
        "dims": (4,4,1,4,3,3,3), "missing_mh": 2, "ocr": False,
        "total_exp": "~10 years", "relevant_exp": "~10 years (international fundraising — MENA)",
        "current_role": "Fundraising Lead, International NGO (Yemen-based)",
        "usp": "Strongest functional and outcomes scores (D1=4, D2=4, D4=4) after Danish and Zain — genuinely elite international fundraising skills. Only viable if fully committed to relocating to Islamabad AND actively building Pakistan donor relationships. Consider for a more senior role if these conditions are met.",
        "org_signals": [
            ("🌐 Donor/Development — HIGH STRATEGIC SIGNAL", "10+ years with UN agencies and international NGOs in the MENA region"),
            ("🏆 Academic Excellence Signal", "Harvard Business School executive education — not a scholarship but exceptional credibility marker"),
        ],
        "cv_quality": "High",
        "cv_quality_note": "Multi-million dollar scale cited, specific UN agency relationships, HBS credential. Well-structured and internationally benchmarked. The geo-mismatch and salary ask are deal-breakers, not CV quality issues.",
        "strengths": [
            "10+ years international fundraising — UN agencies and international NGOs, multi-million dollar scale.",
            "Harvard Business School executive education — elite stakeholder credibility.",
            "Quantified campaign scale — strongest evidence of fundraising outcomes after Zain and Danish.",
        ],
        "risks": [
            "Yemen-based — no willingness to relocate stated. Deal-breaker must-have missing.",
            "MENA region focus — zero Pakistan donor landscape knowledge. Missing must-have.",
            "PKR 980,000 salary — 3.6× budget ceiling.",
        ],
        "interview_qs": [
            "Are you willing and able to relocate to Islamabad, Pakistan on a permanent basis?",
            "What specific knowledge do you have of the Pakistan donor landscape — USAID Pakistan, World Bank Pakistan, FCDO Pakistan?",
            "How quickly could you build a Pakistan-specific donor pipeline given no existing relationships here?",
        ],
        "confidence": "High",
    },
    {
        "rank": 8, "name": "Ahad Ahsan Khan", "score": 41.8, "tier": "Extended Review", "tier_color": "#6B7280",
        "salary": "PKR 550,000/month", "budget_label": "Out of Budget", "budget_gap": "+PKR 280,000",
        "budget_color": "#FEE2E2", "budget_text_color": "#991B1B",
        "dims": (1,3,4,2,3,3,3), "missing_mh": 2, "ocr": False,
        "total_exp": "~9 years", "relevant_exp": "~0 years (grants compliance, not acquisition)",
        "current_role": "Manager Grants, Aga Khan University (AKU), Islamabad",
        "usp": "$134M portfolio across 210 active grants and World Bank HEDP lead — unmatched compliance depth. Could add exceptional value as a grants administration anchor if the BD hire is someone else; does not meet the acquisition requirement independently.",
        "org_signals": [
            ("📊 Research/Impact — HIGH STRATEGIC SIGNAL", "World Bank HEDP (Higher Education Development Programme) project lead at AKU"),
            ("🌐 Donor/Development — Strategic Signal", "Institutional donor compliance — World Bank, USAID, and international foundation grant portfolios"),
        ],
        "cv_quality": "High",
        "cv_quality_note": "$134M and 210 grants are unusually specific and well-evidenced. CV is clear and professional. The high effort is evident but the functional role — compliance — is misaligned with the acquisition mandate.",
        "strengths": [
            "Manager Grants at AKU — $134M portfolio across 210 active grants, World Bank HEDP lead.",
            "9 years in grants management — deep institutional donor compliance knowledge.",
            "Islamabad hometown — no relocation issue.",
        ],
        "risks": [
            "Grants administration and compliance — not fundraising acquisition. JD explicitly lists this as a failure condition.",
            "No evidence of independently writing and winning new competitive grants from scratch.",
            "PKR 550,000 is above budget ceiling.",
        ],
        "interview_qs": [
            "In your 9 years at AKU, have you personally led a proposal from first draft to award for a new competitive grant — not administering an existing one?",
            "What is the difference in your mind between grants management and fundraising acquisition — and which have you actually done?",
            "What would motivate you to move from grants administration to frontline fundraising?",
        ],
        "confidence": "High",
    },
    {
        "rank": 9, "name": "Muhammad Usman", "score": 36.1, "tier": "Extended Review", "tier_color": "#6B7280",
        "salary": "PKR 350,000/month", "budget_label": "Out of Budget", "budget_gap": "+PKR 80,000",
        "budget_color": "#FEE2E2", "budget_text_color": "#991B1B",
        "dims": (2,1,3,2,3,1,3), "missing_mh": 2, "ocr": False,
        "total_exp": "~18 years", "relevant_exp": "~0 years (government relations, not acquisition)",
        "current_role": "Public Affairs & Development Alliances Lead (Rawalpindi/Islamabad)",
        "usp": "18 years of government and international development alliance relationships provides stakeholder access that could complement a senior BD team. However, no demonstrated fundraising acquisition track record across entire career is a significant disqualifier.",
        "org_signals": [],
        "cv_quality": "Low-Moderate",
        "cv_quality_note": "18 years of experience with zero quantified outcomes is a significant red flag in a results-focused role. Language is generic and vague throughout — 'managed partnerships' without specifics. The length of career makes the absence of outcomes more, not less, concerning.",
        "strengths": [
            "18 years in government relations, public affairs, and international development alliances.",
            "Managed partnerships with international development organisations.",
            "Rawalpindi/Islamabad-based — location aligned.",
        ],
        "risks": [
            "States fundraising as competency but no specific grants won, amounts raised, or proposals cited. Missing must-have.",
            "Vague on whether activities were acquisition or relationship maintenance. Missing must-have.",
            "Zero quantified outcomes across 18 years is a serious concern for an acquisition role.",
        ],
        "interview_qs": [
            "In 18 years, can you name one specific grant or partnership deal you personally closed — amount, donor, your exact role?",
            "When you say fundraising is a competency, can you give three concrete examples with outcomes?",
            "What proposals have you written and submitted to bilateral or multilateral donors — what were the outcomes?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 10, "name": "Mushahid Hussain", "score": 34.4, "tier": "Extended Review", "tier_color": "#6B7280",
        "salary": "PKR 170,000/month", "budget_label": "In Budget", "budget_gap": "—",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (2,1,3,2,2,2,2), "missing_mh": 2, "ocr": False,
        "total_exp": "~4 years", "relevant_exp": "~4 years (donor reporting — not acquisition)",
        "current_role": "Donor Reporting Officer, READ Foundation (Islamabad)",
        "usp": "Most affordable in-budget option with READ Foundation pedigree. At 4 years and junior level, most suitable for a future BD support role once the senior BD hire is in place — not ready for the Year 1 acquisition mandate independently.",
        "org_signals": [
            ("🎓 EdTech/Competitor — Strategic Signal", "READ Foundation — 4 years in donor reporting at a direct Taleemabad peer organisation"),
        ],
        "cv_quality": "Low-Moderate",
        "cv_quality_note": "Responsibilities listed without any outcome quantification. Supporting role nature is clear. Effort appears moderate but the lack of any metrics across 4 years — even basic ones — is concerning for a fundraising context.",
        "strengths": [
            "Donor Reporting Officer at READ Foundation — 4 years in donor relations with proposal exposure.",
            "Manages financial reporting to donors — compliance and funder communication skills.",
            "Islamabad-based, in budget at PKR 170K.",
        ],
        "risks": [
            "Primarily reporting, not acquisition — no independently won grants. Missing must-have.",
            "4 years at junior level — not ready for Year 1 $500K–$1M+ acquisition mandate.",
            "No quantification of any outcome across entire CV.",
        ],
        "interview_qs": [
            "Have you personally led a proposal from conception to submission and won it?",
            "What exposure do you have to USAID, FCDO, World Bank beyond reporting to them?",
            "What is your plan to move into frontline fundraising acquisition?",
        ],
        "confidence": "High",
    },
]

# JD Must-Have criteria match per candidate (0=Missing, 1=Weak, 2=Partial, 3=Strong, 4=Fully meets)
JD_CRITERIA = {
    "must_have": [
        "Direct Fundraising / BD Ownership",
        "Pakistan Donor Landscape (USAID/WB/FCDO/EU)",
        "Proposals Won (submitted & awarded)",
        "Pipeline Mgmt (30–50+ live)",
        "Islamabad / Willing to Relocate",
        "Strong Written Communication",
    ],
    "nice_to_have": [
        "Independently Closed $500K+ Deal",
        "Named Bilateral / Multilateral Relationships",
        "Education Sector Experience",
        "Govt / Policy Engagement in Islamabad",
    ],
}

# Per-candidate match on each criterion (must-haves first, then nice-to-haves)
MH_SCORES = {
    "Danish Hussain":       [4, 4, 4, 4, 3, 4,   3, 4, 2, 2],
    "Zain Ul Abideen":      [4, 4, 4, 4, 4, 4,   4, 4, 2, 1],
    "Mizhgan Kirmani":      [3, 4, 3, 2, 4, 3,   2, 4, 4, 2],
    "Arsalan Ashraf":       [4, 2, 3, 3, 3, 3,   2, 2, 2, 2],
    "Sadia Sohail":         [3, 2, 2, 2, 4, 3,   1, 1, 3, 1],
    "Arsim Tariq":          [2, 3, 2, 1, 4, 2,   1, 2, 3, 2],
    "Ahmed Al-Mayadeen":    [4, 1, 4, 3, 0, 4,   3, 3, 1, 0],
    "Ahad Ahsan Khan":      [1, 3, 2, 1, 4, 3,   1, 3, 2, 1],
    "Muhammad Usman":       [2, 2, 1, 1, 4, 2,   1, 1, 1, 2],
    "Mushahid Hussain":     [2, 2, 2, 1, 4, 2,   1, 1, 3, 1],
}

# ══════════════════════════════════════════════════════════════════
# NO-HIRE CANDIDATES — all 38 assessed but eliminated (ranks 11–48)
# Includes 12 new candidates identified in follow-up DB review
# ══════════════════════════════════════════════════════════════════
NO_HIRE_CANDIDATES = [
    {"rank": 11, "name": "Mohammad Aqeel Qureshi", "score": 33,
     "background": "Fundraising Manager, Healthcare NGO (Shifa Foundation)",
     "current_role": "Manager Fundraising, Shifa Foundation (Islamabad)", "location": "Islamabad",
     "strength_note": "20 years of development experience; confirmed fundraising function title; advocacy, sustainable rural development, healthcare/WASH programmes at a registered NGO.",
     "reason": "Fundraising in healthcare/WASH domestic NGO — no multilateral/bilateral (USAID/FCDO/WB) institutional grant track record; Shifa Foundation donor base is domestic/charity; EdTech sector pivot also required.",
     "what_needed": "Evidence of independently winning competitive grants from USAID, FCDO, World Bank, or UN agencies; Pakistan development donor ecosystem relationships; education sector pivot.",
     "category": "Wrong Sector",
     "interview_qs": [
         "Of all the funds you've mobilised at Shifa Foundation — what percentage came from bilateral or multilateral institutional donors (USAID, FCDO, World Bank, UN agencies)?",
         "Have you personally written and won a competitive institutional grant — from RFP to award letter — without a BD lead above you?",
         "How would you position Taleemabad's AI teacher coaching model to a USAID education programme officer?",
     ], "cv_quality": "Moderate"},
    {"rank": 12, "name": "Faheem Baig", "score": 31,
     "background": "Programme Implementation, Development Sector",
     "current_role": "Programme Implementation Officer, Development Sector NGO (Rawalpindi)", "location": "Rawalpindi",
     "strength_note": "Development sector background; understands project delivery cycle and donor-funded project environments.",
     "reason": "Programme implementation — not fundraising acquisition; no BD ownership evidenced; delivery is the opposite function from donor acquisition.",
     "what_needed": "Transition from programme delivery to fundraising acquisition with 5+ years evidence of independently writing and winning institutional grants.",
     "category": "Sector-Adjacent",
     "interview_qs": [
         "Have you ever led a grant proposal from initial concept to award — without a fundraising lead above you?",
         "What is the difference in your understanding between programme management and fundraising acquisition?",
     ], "cv_quality": "Moderate"},
    {"rank": 13, "name": "Shahzad Saleem Abbasi", "score": 30,
     "background": "Domestic Charity / CSR Fundraising Executive",
     "current_role": "Head of BD, Fundraising & Policy Documentation, Junior Jinnah Trust (Islamabad)", "location": "Islamabad",
     "strength_note": "PKR 400M annually mobilised; 15+ years fundraising experience; Head-level BD title; 10,000+ donors managed; 12 CSR partnerships; 25+ university MoUs — impressive domestic charity capability.",
     "reason": "Domestic charity / CSR model — donors are individuals, major donors, and corporate CSR partners, NOT multilateral/bilateral institutional donors (USAID, FCDO, World Bank, EU). These are fundamentally different donor landscapes with different processes, relationships, and deal structures.",
     "what_needed": "Pivot from domestic charity/CSR to multilateral institutional fundraising; evidence of winning competitive bids from bilateral/multilateral donors; knowledge of USAID, FCDO, WB grant cycles.",
     "category": "Wrong Sector",
     "interview_qs": [
         "Of the PKR 400M you mobilise annually — what percentage came from bilateral/multilateral institutional donors (USAID, FCDO, World Bank, UN agencies) vs. individual/CSR donors?",
         "Have you independently written and won a competitive RFP/RFA from USAID, FCDO, World Bank, or a similar multilateral?",
         "How familiar are you with USAID's RFP/RFA process, FCDO's competitive bidding, and World Bank procurement frameworks?",
     ], "cv_quality": "High"},
    {"rank": 14, "name": "Hamdan Ahmad", "score": 29,
     "background": "World Bank Programme Management",
     "current_role": "Programme Manager, World Bank-Funded Programme (Islamabad)", "location": "Islamabad",
     "strength_note": "World Bank-funded programme experience; donor compliance and reporting knowledge; understands institutional donor requirements from the delivery side.",
     "reason": "Programme management on donor contracts — managing an awarded WB grant is not the same as winning one; no independently won proposals cited.",
     "what_needed": "Evidence of independently writing competitive grant proposals and winning them from scratch; clear transition from programme management to BD ownership.",
     "category": "Sector-Adjacent",
     "interview_qs": [
         "In your World Bank-funded programmes — were you the proposal author and donor relationship owner, or brought in after the grant was already awarded?",
         "Have you written a winning proposal to a new donor that you personally identified, cultivated, and closed?",
     ], "cv_quality": "Moderate"},
    {"rank": 15, "name": "Shakir Manzoor", "score": 27,
     "background": "Fundraising Support Role, Development NGO",
     "current_role": "Fundraising Support / Grants Assistant, Development NGO (Rawalpindi)", "location": "Rawalpindi",
     "strength_note": "Worked in fundraising environment; exposure to grant processes, proposal writing support, and donor communication workflows.",
     "reason": "Supporting role — no evidence of independently owning acquisition pipeline or closing grants; contributing to proposals is not the same as winning them.",
     "what_needed": "Transition from grants support to full ownership; 5+ years of independently cultivating donors and closing new competitive institutional grants.",
     "category": "Sector-Adjacent",
     "interview_qs": [
         "Have you independently led a proposal from initial outreach to award — without a senior BD person above you?",
         "What is the largest grant you have personally been responsible for closing?",
     ], "cv_quality": "Moderate"},
    {"rank": 16, "name": "Sarmad Iqbal", "score": 27,
     "background": "B2G Strategy & Governance Specialist",
     "current_role": "Head – Policy Advocacy, Strategic Partnerships & Communications, International Development Organisation (Islamabad)", "location": "Islamabad",
     "strength_note": "20+ years B2G and government engagement; strategic planning; policy advocacy; digital public finance; government relationship capital that could complement a fundraising team.",
     "reason": "B2G/governance strategy — policy advocacy and government engagement is distinct from multilateral grant proposal writing and closing; 'donor engagement' in B2G context means regulatory/government coordination, not independently closing competitive institutional grants.",
     "what_needed": "Clear evidence of independently winning competitive institutional grants (not government contracts or B2G agreements); USAID/FCDO/WB proposal writing and closing track record.",
     "category": "Sector-Adjacent",
     "interview_qs": [
         "Have you written and personally won a competitive institutional grant (USAID, FCDO, World Bank) — not a government contract or B2G agreement?",
         "How much of your 'donor engagement' involved closing new funding vs. managing existing government/regulatory relationships?",
         "Would you characterise your experience as fundraising acquisition or government/stakeholder engagement?",
     ], "cv_quality": "High"},
    {"rank": 17, "name": "Zubair Hussain", "score": 26,
     "background": "Field Specialist, Development Sector",
     "current_role": "Field Specialist, Development Sector NGO (Islamabad)", "location": "Islamabad",
     "strength_note": "Field implementation experience in the development sector; familiarity with donor-funded project environments.",
     "reason": "Field delivery role — no fundraising track record; field implementation is a completely different function from BD/acquisition.",
     "what_needed": "Complete function change to fundraising acquisition with 5+ years BD/donor relations experience.",
     "category": "Sector-Adjacent", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 18, "name": "Abdul Salam", "score": 24,
     "background": "WASH Sector Delivery",
     "current_role": "WASH Programme Officer (Islamabad)", "location": "Islamabad",
     "strength_note": "Worked with donor-funded programmes in WASH sector; understands project delivery in development contexts.",
     "reason": "WASH sector delivery — not fundraising acquisition; sector-pivot (WASH to EdTech) and function-pivot (delivery to BD) both required simultaneously.",
     "what_needed": "Career pivot to fundraising/BD AND sector pivot to education/EdTech — both gaps are significant.",
     "category": "Sector-Adjacent", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 19, "name": "Mehboob Alam", "score": 24,
     "background": "Programme Management / JICA Consultant",
     "current_role": "National Consultant, JICA / Senior Manager Operations, AIMS Pakistan (Peshawar/Islamabad)", "location": "Peshawar (CV) / Islamabad (application)",
     "strength_note": "15+ years in programme management; JICA/government engagement; 'donor relations and proposal development' listed as competency; cross-sector development experience.",
     "reason": "Programme management and capacity building — 'donor relations' in this context means compliance/coordination on awarded grants, not independently closing new competitive grants; Peshawar-based per CV (location risk).",
     "what_needed": "Transition from programme delivery to frontline BD acquisition; evidence of independently writing and winning competitive institutional grants; confirmed permanent Islamabad location.",
     "category": "Sector-Adjacent",
     "interview_qs": [
         "When you describe 'donor relations' — were you responsible for identifying new donors and winning competitive grants, or managing existing awarded contracts?",
         "Have you independently written a grant proposal that was submitted and awarded — without a BD lead above you?",
     ], "cv_quality": "Moderate"},
    {"rank": 20, "name": "Bareera Rauf", "score": 23,
     "background": "Researcher / Development Sector",
     "current_role": "Research Officer / Analyst, Development Sector (Karachi)", "location": "Karachi",
     "strength_note": "Development research background; strong analytical skills that could support proposal development; development sector understanding.",
     "reason": "Research function — no fundraising acquisition track record or donor pipeline ownership; also Karachi-based without relocation mention.",
     "what_needed": "Transition from research to fundraising; evidence of independently closing institutional grants; Islamabad location.",
     "category": "Sector-Adjacent", "interview_qs": [], "cv_quality": "Moderate"},
    {"rank": 21, "name": "Samana Qaseem", "score": 22,
     "background": "Alumni Relations & Admin, Education Sector",
     "current_role": "Alumni Relations / Administrative Officer, Education Sector (Karachi)", "location": "Karachi",
     "strength_note": "Education sector pedigree; alumni relationship management skills.",
     "reason": "Alumni/admin function — not fundraising acquisition; no grants won or pipeline evidenced; also Karachi-based.",
     "what_needed": "Pivot to fundraising function with evidence of winning institutional grants; Islamabad location.",
     "category": "Sector-Adjacent", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 22, "name": "Imran Haider", "score": 21,
     "background": "Education Policy Analyst",
     "current_role": "Education Policy Analyst (Islamabad)", "location": "Islamabad",
     "strength_note": "Education sector expertise; policy and government engagement; Islamabad-based — education policy knowledge directly relevant to Taleemabad's mandate.",
     "reason": "Policy analysis role — not BD/acquisition function; education policy knowledge is valuable but doesn't substitute for a donor acquisition track record; no proposals independently won.",
     "what_needed": "Transition from policy analysis to fundraising/BD; evidence of independently winning competitive institutional grants.",
     "category": "Wrong Sector", "interview_qs": [], "cv_quality": "Moderate"},
    {"rank": 23, "name": "Fahad Khan", "score": 20,
     "background": "Hospital / Domestic Charity Fundraising",
     "current_role": "Fundraising Officer, Hospital / Domestic Charity (Islamabad)", "location": "Islamabad",
     "strength_note": "Has fundraising function confirmed; proposal writing exposure; Islamabad-based; understands donor communication concepts.",
     "reason": "Domestic charity fundraising — no multilateral/bilateral (USAID/FCDO/WB) institutional donor knowledge; hospital/domestic charity is a completely different donor landscape.",
     "what_needed": "Transition from domestic to multilateral/bilateral institutional fundraising; knowledge of USAID, FCDO, WB grant processes; Pakistan development donor network.",
     "category": "Wrong Sector",
     "interview_qs": [
         "Have you engaged with any multilateral or bilateral donor (USAID, FCDO, World Bank, UNDP) in a fundraising capacity — pitching for competitive institutional grants?",
     ], "cv_quality": "Moderate"},
    {"rank": 24, "name": "Anita Kanwal", "score": 19,
     "background": "Digital Charity Campaigns, UK-based",
     "current_role": "Digital Fundraising / Campaign Manager, UK-based Organisation", "location": "UK-based (deal-breaker)",
     "strength_note": "Fundraising function confirmed; digital campaign management experience; some comms/outreach skills.",
     "reason": "UK-based — no willingness to relocate to Islamabad stated (deal-breaker); digital charity is not institutional donor fundraising; wrong geography and wrong donor type.",
     "what_needed": "Islamabad-based or explicitly committed to relocating; transition from digital charity to multilateral institutional fundraising.",
     "category": "Wrong Sector", "interview_qs": [], "cv_quality": "Moderate"},
    {"rank": 25, "name": "Mahnoor Mellu", "score": 18,
     "background": "SaaS / Tech Partnerships",
     "current_role": "Partnerships Manager, SaaS Company (Lahore)", "location": "Lahore",
     "strength_note": "Partnerships and BD experience in commercial tech sector; pipeline and relationship management in a commercial context.",
     "reason": "Commercial SaaS partnerships — no institutional donor fundraising or NGO ecosystem experience; Lahore-based.",
     "what_needed": "Sector pivot from SaaS to development sector; experience with institutional donors (USAID, FCDO, WB); Islamabad location.",
     "category": "Wrong Sector", "interview_qs": [], "cv_quality": "Moderate"},
    {"rank": 26, "name": "Muhammad Ali Zafar", "score": 17,
     "background": "Research Intern",
     "current_role": "Research Intern / Junior Researcher (Islamabad)", "location": "Islamabad",
     "strength_note": "Academic/research interest in development sector; Islamabad-based; analytical exposure.",
     "reason": "Research intern level — too junior for a Year-1 $500K+ acquisition mandate; no fundraising background or donor relationships.",
     "what_needed": "5-7 more years building fundraising/BD experience with demonstrable grant-winning track record.",
     "category": "Junior Profile", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 27, "name": "Zainab", "score": 16,
     "background": "Early-Career HR Generalist",
     "current_role": "HR Generalist / Junior HR Officer (Peshawar)", "location": "Peshawar",
     "strength_note": "Generalist people skills; some comms exposure.",
     "reason": "Early-career HR — no fundraising background; significant ramp-up required across both function and location.",
     "what_needed": "Complete career pivot to fundraising/BD; 5+ years of institutional grant acquisition experience; Islamabad location.",
     "category": "Junior Profile", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 28, "name": "Bushra Nawaz", "score": 16,
     "background": "Livelihoods & Business Placement, INGO (Islamic Relief Pakistan)",
     "current_role": "Business and Job Placement Officer, Islamic Relief Pakistan (Muzaffarabad)", "location": "Muzaffarabad",
     "strength_note": "INGO background at Islamic Relief Pakistan; livelihoods programme management; ILO/SIYB certified master trainer; some donor reporting exposure.",
     "reason": "Livelihoods and project management — not fundraising acquisition; Islamic Relief role involves programme delivery, not independently closing institutional grants; Muzaffarabad-based.",
     "what_needed": "Transition from programme delivery to fundraising acquisition; evidence of independently winning institutional grants; Islamabad location.",
     "category": "Sector-Adjacent", "interview_qs": [], "cv_quality": "Moderate"},
    {"rank": 29, "name": "Syeda Kainat", "score": 15,
     "background": "M&amp;E / Communications, Development Sector",
     "current_role": "M&amp;E / Communications Officer, Development NGO (Islamabad)", "location": "Islamabad",
     "strength_note": "Development sector exposure; M&amp;E and comms skills; Islamabad-based; familiarity with donor-funded project environments.",
     "reason": "M&amp;E and communications — adjacent but not acquisition; no BD or donor relations ownership; no evidence of independently winning grants.",
     "what_needed": "Transition from M&amp;E/comms to frontline fundraising acquisition; evidence of independently closing institutional grants.",
     "category": "Sector-Adjacent", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 30, "name": "Sameen Amjad Ali", "score": 13,
     "background": "Marketing / Communications",
     "current_role": "Marketing / Communications Professional (Islamabad)", "location": "Islamabad",
     "strength_note": "Strong comms and content skills; Islamabad-based.",
     "reason": "Marketing/comms background — no institutional donor fundraising or NGO ecosystem experience.",
     "what_needed": "Career pivot to fundraising/BD with development sector focus; evidence of winning institutional grants.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Moderate"},
    {"rank": 31, "name": "SAHRISH KASHIF", "score": 13,
     "background": "Community Development, Women&apos;s Programs (Foundation)",
     "current_role": "Project Manager, Karishma Ali Foundation (Islamabad)", "location": "Islamabad",
     "strength_note": "Project management in community development; women's empowerment programs; Islamabad-based; 'secured funding' mentioned for small community programs.",
     "reason": "Junior community development PM with no institutional fundraising track record; 'secured funding' refers to small foundation grants, not competitive multilateral/bilateral bids; Year-1 $500K+ mandate requires proven senior track record.",
     "what_needed": "5+ years specifically in institutional fundraising/BD; proven track record of winning competitive grants from USAID, FCDO, World Bank or similar multilaterals.",
     "category": "Junior Profile", "interview_qs": [], "cv_quality": "Moderate"},
    {"rank": 32, "name": "Hasan Shahid", "score": 12,
     "background": "Digital Marketing",
     "current_role": "Digital Marketing Manager (Islamabad)", "location": "Islamabad",
     "strength_note": "Digital outreach skills; some audience engagement experience; Islamabad-based.",
     "reason": "Digital marketing — no connection to institutional fundraising, development donors, or NGO ecosystem.",
     "what_needed": "Complete career pivot to fundraising/BD; NGO/development sector experience from the ground up.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 33, "name": "Muhammad Taqi", "score": 11,
     "background": "SaaS Sales",
     "current_role": "SaaS Sales Manager (Islamabad)", "location": "Islamabad",
     "strength_note": "Sales pipeline management; closing experience in commercial sector; Islamabad-based.",
     "reason": "SaaS/commercial sales — no NGO or donor ecosystem experience; institutional fundraising requires a completely different landscape, skillset, and network.",
     "what_needed": "Development sector pivot; institutional donor fundraising experience; commercial sales instincts could be transferable but 5+ years of development sector foundation needed first.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 34, "name": "Muhammad Sumraiz Kundi", "score": 10,
     "background": "Telecom Sales",
     "current_role": "Sales Officer, Telecom Company (Islamabad)", "location": "Islamabad",
     "strength_note": "Sales experience; negotiation skills; Islamabad-based.",
     "reason": "Telecom sales — no fundraising, NGO, or development sector background of any kind.",
     "what_needed": "Complete sector pivot to development/NGO fundraising.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 35, "name": "Bilal Shahid", "score": 9,
     "background": "M&amp;A / SaaS Business Development",
     "current_role": "M&amp;A Team Manager, Jonas Software / Constellation Software (Lahore)", "location": "Lahore",
     "strength_note": "M&amp;A and B2B business development; deal analysis and pipeline management in a commercial context; Constellation Software pedigree.",
     "reason": "Commercial SaaS M&amp;A — no development sector, NGO, or institutional donor experience; Lahore-based; M&amp;A deal-sourcing is a completely different domain from multilateral grant acquisition.",
     "what_needed": "Development sector career pivot; NGO/INGO fundraising experience; Islamabad location.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Moderate"},
    {"rank": 36, "name": "Asim Ur Rehman", "score": 9,
     "background": "Rural Volunteer Work",
     "current_role": "Rural Development Volunteer (Peshawar)", "location": "Peshawar",
     "strength_note": "Community engagement; grassroots development awareness; development sector interest.",
     "reason": "Volunteer work only — no professional fundraising or donor relations experience; Peshawar-based.",
     "what_needed": "Professional fundraising career with 5+ years of grant-winning track record; Islamabad location.",
     "category": "Junior Profile", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 37, "name": "Sikandar Khurshid", "score": 8,
     "background": "Customer Success &amp; Sales, Taleemabad Alumni",
     "current_role": "Sales Manager, Shadiyana / Former Customer Success Manager, Taleemabad (Islamabad)", "location": "Islamabad",
     "strength_note": "Taleemabad alumni with deep product knowledge; Customer Success Manager at Taleemabad itself (Jul 2023 – Jun 2025); Islamabad-based; knows the mission and team firsthand.",
     "reason": "Customer success and internal CRM management — not external fundraising acquisition; product knowledge is valuable but is not a substitute for institutional donor fundraising track record.",
     "what_needed": "Pivot to external fundraising/BD with institutional donor focus; 5+ years of donor acquisition experience with multilateral/bilateral institutions.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Moderate"},
    {"rank": 38, "name": "Sheraz Khan", "score": 8,
     "background": "Microsoft Licensing / IT Sales",
     "current_role": "Microsoft Licensing Advisor / Account Manager, Zones Inc. (Islamabad)", "location": "Islamabad",
     "strength_note": "Commercial deal-closing; account management; renewal and new client acquisition in tech licensing; Islamabad-based.",
     "reason": "IT/licensing commercial sales — no connection to fundraising, NGOs, or institutional donors of any kind.",
     "what_needed": "Complete sector pivot to development/NGO fundraising.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Moderate"},
    {"rank": 39, "name": "Muhammad Akmal", "score": 7,
     "background": "Administration",
     "current_role": "Administrative Officer (Punjab)", "location": "Punjab",
     "strength_note": "Organisational and coordination skills.",
     "reason": "Administrative background — no fundraising or donor relations experience at all.",
     "what_needed": "Complete career pivot; administrative skills provide no foundation for institutional fundraising.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 40, "name": "Laveeza Shah", "score": 6,
     "background": "Human Resources",
     "current_role": "HR Officer (Islamabad)", "location": "Islamabad",
     "strength_note": "People management; organisational understanding; Islamabad-based.",
     "reason": "HR function — no institutional fundraising or NGO ecosystem background.",
     "what_needed": "Complete career change to fundraising/BD.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 41, "name": "Samreen Durrani", "score": 6,
     "background": "Policy Research &amp; Economics (LUMS MPhil)",
     "current_role": "Content Developer Economy, NCSU / Ministry of Information (Islamabad)", "location": "Islamabad",
     "strength_note": "LUMS MPhil Economics (strong academic pedigree); policy research; Islamabad-based; government narrative and DAVOS 2026 communication work — signals high-level policy communication ability.",
     "reason": "Policy research and content development — no fundraising or donor acquisition experience; strong analytical and writing skills but no evidence of independently closing institutional grants.",
     "what_needed": "Transition from policy/research to fundraising BD; track record of winning institutional grants — LUMS background is a positive signal but function pivot is the critical gap.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "High"},
    {"rank": 42, "name": "Arooj Irfan", "score": 5,
     "background": "Clinical Psychologist",
     "current_role": "Clinical Psychologist (Islamabad)", "location": "Islamabad",
     "strength_note": "Strong analytical and communication skills; Islamabad-based.",
     "reason": "Clinical psychology — completely unrelated to institutional fundraising/partnerships mandate.",
     "what_needed": "Entirely different career trajectory; clinical skills have no application in multilateral donor acquisition.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Moderate"},
    {"rank": 43, "name": "Ibrahim Basit", "score": 5,
     "background": "Marketing &amp; Content, Early Career",
     "current_role": "Management Trainee Officer, SMASH (Islamabad)", "location": "Islamabad",
     "strength_note": "Marketing and content execution; Islamabad-based; early-stage career energy.",
     "reason": "Marketing trainee with no fundraising background; too junior and completely wrong function for a Year-1 acquisition mandate.",
     "what_needed": "Complete career pivot to fundraising/BD; 5+ years of institutional grant acquisition experience.",
     "category": "Junior Profile", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 44, "name": "Moeen Hassan", "score": 4,
     "background": "AutoCAD / Real Estate",
     "current_role": "AutoCAD Technician / Real Estate Professional (Lahore)", "location": "Lahore",
     "strength_note": "Technical precision; project planning skills.",
     "reason": "AutoCAD/real estate — completely unrelated to fundraising or development sector; also Lahore-based.",
     "what_needed": "Entirely different career trajectory; technical skills completely irrelevant to fundraising mandate.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 45, "name": "Hira Noureen Khan", "score": 4,
     "background": "Clinical Psychologist, NLP &amp; Hypnosis Practitioner",
     "current_role": "Clinical Psychologist / Diabetes Advocate (Rawalpindi)", "location": "Rawalpindi",
     "strength_note": "Strong clinical communication skills; community advocacy (T1D champion); Rawalpindi-based (Islamabad adjacent).",
     "reason": "Clinical psychology and NLP practice — completely unrelated to institutional fundraising; 'Manager Public Relations and Resource Development' title appears but in healthcare/clinical advocacy context, not donor acquisition.",
     "what_needed": "Entirely different career focus; clinical background has no application to multilateral institutional fundraising.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Moderate"},
    {"rank": 46, "name": "Aqsa Gul", "score": 3,
     "background": "Customer Service",
     "current_role": "Customer Service Officer (Islamabad)", "location": "Islamabad",
     "strength_note": "Client communication and stakeholder engagement; Islamabad-based.",
     "reason": "Customer service — no fundraising or donor relations background.",
     "what_needed": "Complete career pivot; customer service skills minimally transferable to institutional fundraising.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 47, "name": "Sani Muhammad", "score": 2,
     "background": "IT Operations",
     "current_role": "IT Operations Officer (Islamabad)", "location": "Islamabad",
     "strength_note": "Technical problem-solving; systems management; Islamabad-based.",
     "reason": "IT operations — completely unrelated to fundraising/partnerships mandate.",
     "what_needed": "Complete sector pivot; IT skills have no connection to institutional donor acquisition.",
     "category": "Unrelated Background", "interview_qs": [], "cv_quality": "Low"},
    {"rank": 48, "name": "AAMIR SOHAIL", "score": 0,
     "background": "Could Not Assess — Unreadable CV",
     "current_role": "Not assessable (Islamabad)", "location": "Islamabad",
     "strength_note": "Applied for the role; Islamabad-based.",
     "reason": "CV could not be extracted — scanned PDF returned zero text even after OCR attempt; application could not be assessed.",
     "what_needed": "Resubmit in searchable/text-based PDF format to enable proper assessment.",
     "category": "Could Not Assess", "interview_qs": [], "cv_quality": "N/A"},
]

# Org signal lookup for no-hire candidates
NH_ORG_SIGNAL = {
    "Faheem Baig":           "&#127760; Donor/Dev — Development sector NGO programme",
    "Hamdan Ahmad":          "&#128202; Research/Impact — World Bank-funded programme mgmt",
    "Shakir Manzoor":        "&#127760; Donor/Dev — NGO fundraising environment",
    "Zubair Hussain":        "&#127760; Donor/Dev — Development sector field work",
    "Abdul Salam":           "&#127760; Donor/Dev — WASH donor-funded delivery",
    "Bareera Rauf":          "&#128202; Research/Impact — Development sector research",
    "Samana Qaseem":         "&#127979; Education — Alumni relations, education sector",
    "Imran Haider":          "&#127979; Education — Education policy sector",
    "Syeda Kainat":          "&#127760; Donor/Dev — M&amp;E on donor-funded projects",
}

# Experience lookup for no-hire candidates (extracted from CV screening)
NH_EXP = {
    "Faheem Baig":           "~7 years",
    "Hamdan Ahmad":          "~6 years",
    "Shakir Manzoor":        "~5 years",
    "Zubair Hussain":        "~5 years",
    "Abdul Salam":           "~4 years",
    "Bareera Rauf":          "~4 years",
    "Samana Qaseem":         "~4 years",
    "Imran Haider":          "~5 years",
    "Fahad Khan":            "~4 years",
    "Anita Kanwal":          "~4 years",
    "Mahnoor Mellu":         "~3 years",
    "Muhammad Ali Zafar":    "~1 year",
    "Zainab":                "~2 years",
    "Syeda Kainat":          "~4 years",
    "Sameen Amjad Ali":      "~4 years",
    "Hasan Shahid":          "~3 years",
    "Muhammad Taqi":         "~4 years",
    "Muhammad Sumraiz Kundi":"~4 years",
    "Asim Ur Rehman":        "~3 years",
    "Sheraz Khan":           "~5 years",
    "Muhammad Akmal":        "~4 years",
    "Laveeza Shah":          "~3 years",
    "Arooj Irfan":           "~4 years",
    "Moeen Hassan":          "~3 years",
    "Aqsa Gul":              "~2 years",
    "Sani Muhammad":         "~3 years",
}

# ── chart generators (matplotlib → base64 PNG) ───────────────────

def generate_bar_chart():
    """Horizontal bar chart of all 10 candidates by score, colour-coded by tier."""
    names  = [c["name"] for c in CANDIDATES]
    scores = [c["score"] for c in CANDIDATES]
    colors = [c["tier_color"] for c in CANDIDATES]
    # Reverse so rank #1 appears at the top
    names_r  = names[::-1]
    scores_r = scores[::-1]
    colors_r = colors[::-1]

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#F5F3FF')

    bars = ax.barh(names_r, scores_r, color=colors_r, height=0.62,
                   edgecolor='white', linewidth=0.8)

    for bar, score in zip(bars, scores_r):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2,
                f'{score}', va='center', ha='left', fontsize=11,
                fontweight='bold', color='#374151')

    ax.set_xlim(0, 115)
    ax.set_xlabel('Score / 100', fontsize=12, color='#374151')
    ax.set_title('Candidate Score Comparison — All 10 Candidates',
                 fontsize=13, fontweight='bold', color='#4C1D95', pad=12)
    ax.axvline(x=85, color='#16A34A', linestyle='--', linewidth=1.4,
               alpha=0.75, label='Tier A threshold (85)')
    ax.axvline(x=70, color='#1D4ED8', linestyle='--', linewidth=1.4,
               alpha=0.75, label='Tier B threshold (70)')
    ax.axvline(x=55, color='#D97706', linestyle='--', linewidth=1.4,
               alpha=0.75, label='Tier C threshold (55)')

    legend_patches = [
        mpatches.Patch(color='#16A34A', label='Tier A (85+)'),
        mpatches.Patch(color='#1D4ED8', label='Tier B (70–84)'),
        mpatches.Patch(color='#D97706', label='Tier C (55–69)'),
        mpatches.Patch(color='#6B7280', label='Extended Review (<55)'),
    ]
    ax.legend(handles=legend_patches, loc='lower right', fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=10)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=140, bbox_inches='tight',
                facecolor='#FAFAFA')
    plt.close(fig)
    return buf.getvalue()


def generate_spider_chart():
    """Radar / spider chart of 7 dimensions for the top 3 candidates."""
    dim_labels = [
        'Functional\nMatch (D1)',
        'Outcomes\n(D2)',
        'Environment\nFit (D3)',
        'Ownership &\nExecution (D4)',
        'Stakeholder\n& Comms (D5)',
        'Hard Skills\n(D6)',
        'Growth &\nLeadership (D7)',
    ]
    N = len(dim_labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]          # close the polygon

    top3   = CANDIDATES[:3]
    colors = ['#16A34A', '#22C55E', '#1D4ED8']

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#F0F4FF')

    for cand, color in zip(top3, colors):
        values = list(cand["dims"]) + [cand["dims"][0]]   # close loop
        ax.plot(angles, values, 'o-', linewidth=2.5, color=color,
                label=f'#{cand["rank"]} {cand["name"]}  ({cand["score"]})')
        ax.fill(angles, values, alpha=0.12, color=color)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dim_labels, fontsize=10, color='#374151')
    ax.set_yticks([1, 2, 3, 4])
    ax.set_yticklabels(['1', '2', '3', '4'], fontsize=9, color='#6B7280')
    ax.set_ylim(0, 4)
    ax.set_title('Dimension Radar — Top 3 Candidates',
                 fontsize=14, fontweight='bold', color='#4C1D95', pad=24)
    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15), fontsize=11)
    ax.grid(color='#D1D5DB', linestyle='--', linewidth=0.7)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=140, bbox_inches='tight',
                facecolor='#FAFAFA')
    plt.close(fig)
    return buf.getvalue()


# ── helpers ──────────────────────────────────────────────────────
def clr(s):
    return {4:"#16A34A",3:"#22C55E",2:"#EAB308",1:"#F97316",0:"#DC2626"}.get(s,"#DC2626")

def cell(s, pad="7"):
    c = clr(s)
    return f'<td bgcolor="{c}" style="background-color:{c};color:#fff;text-align:center;font-weight:bold;padding:{pad}px 6px;">{s}</td>'

def stars(s):
    return "★" * s + "☆" * (4-s)

# ══════════════════════════════════════════════════════════════════
# Generate charts FIRST — must be before HTML so we can embed at top
# ══════════════════════════════════════════════════════════════════
bar_bytes    = generate_bar_chart()
spider_bytes = generate_spider_chart()

# ══════════════════════════════════════════════════════════════════
# EMAIL HTML — v8 — 7-SECTION FORMAT
# ══════════════════════════════════════════════════════════════════

html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;font-size:14px;color:#111827;max-width:1100px;margin:0 auto;padding:24px;background:#fafafa;">

<!-- HEADER -->
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:8px;">
  <tr><td bgcolor="#4C1D95" style="background-color:#4C1D95;padding:20px 24px;border-radius:8px;">
    <span style="color:#ffffff;font-size:22px;font-weight:bold;">&#128203; Candidate Screening Report &mdash; Fundraising &amp; Partnerships Manager</span>
  </td></tr>
</table>
"""

# ── SECTION 3: DEEP COMPARATIVE ANALYSIS — ALL CANDIDATES ────────
html += """
<!-- ══════════════════════════════════════════════════════════════
     SECTION 3: DEEP COMPARATIVE ANALYSIS — ALL CANDIDATES
═══════════════════════════════════════════════════════════════ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">&#49;&#65039;&#8419; Deep Comparative Analysis</h2>
<p style="font-size:12px;color:#6B7280;margin-bottom:4px;">64 applications received; 48 candidates assessed and ranked #1 (strongest fit) to #48 (no-hire). Tiers: <b style="color:#16A34A;">Tier&nbsp;A&nbsp;85+</b> &bull; <b style="color:#1D4ED8;">Tier&nbsp;B&nbsp;70&ndash;84</b> &bull; <b style="color:#D97706;">Tier&nbsp;C&nbsp;55&ndash;69</b> &bull; <b style="color:#6B7280;">Extended&nbsp;Review&nbsp;&lt;55</b> &bull; <b style="color:#374151;">No-Hire&nbsp;&lt;35</b>. Part A = master ranking table (all 48 assessed candidates).</p>
"""

# ── Part A: Master Comparison Table (all 10 candidates) ──────────
quality_colors = {"High": "#16A34A", "Moderate-High": "#22C55E", "Moderate": "#EAB308", "Low-Moderate": "#F97316", "Low": "#DC2626"}

KEY_STRENGTH = {
    "Danish Hussain":    "PKR 1B+ mobilised &bull; FCDO/UNDP/ADB relationships &bull; 20-yr Head-level",
    "Zain Ul Abideen":   "US $50M proven at 2 orgs &bull; READ Foundation &bull; Islamabad-based",
    "Mizhgan Kirmani":   "TCF Manager &bull; Active FCDO/UNDP/USAID &bull; In budget &bull; Zero risk",
    "Arsalan Ashraf":    "Built BD at 3 NGOs &bull; Pipeline discipline &bull; Builder mindset",
    "Sadia Sohail":      "8 yrs READ Foundation &bull; 3 fundraising certs &bull; Affordable",
    "Arsim Tariq":       "10 yrs FCDO/World Bank projects &bull; Sector depth &bull; Islamabad",
    "Ahmed Al-Mayadeen": "Strongest functional score &bull; Elite intl track record &bull; HBS",
    "Ahad Ahsan Khan":   "$134M 210-grant portfolio &bull; World Bank HEDP &bull; AKU depth",
    "Muhammad Usman":    "18 yrs govt/intl development alliances &bull; Stakeholder breadth",
    "Mushahid Hussain":  "READ Foundation pedigree &bull; Islamabad &bull; Most affordable",
}

KEY_GAP = {
    "Danish Hussain":    "PKR 280K over budget + WASH pivot + relocation confirmation",
    "Zain Ul Abideen":   "PKR 80K over budget + freelance gaps + WASH sector pivot",
    "Mizhgan Kirmani":   "Year-1 $1M target exceeds evidenced PKR 72M/FY track record",
    "Arsalan Ashraf":    "Missing multilateral (USAID/WB/FCDO) + PKR 180K over budget",
    "Sadia Sohail":      "Zero quantified outcomes + no multilateral/bilateral experience",
    "Arsim Tariq":       "Programme M&amp;E — not acquisition owner + borderline salary",
    "Ahmed Al-Mayadeen": "Yemen-based (no relocation stated) + no Pakistan donor network",
    "Ahad Ahsan Khan":   "Grants compliance — not acquisition + no pipeline-building record",
    "Muhammad Usman":    "Zero quantified outcomes across 18-yr career + vague evidence",
    "Mushahid Hussain":  "4 yrs junior donor reporting — not acquisition-ready",
}

VERDICT = {
    "Danish Hussain":    "Interview — salary sign-off first",
    "Zain Ul Abideen":   "Interview immediately",
    "Mizhgan Kirmani":   "Interview immediately",
    "Arsalan Ashraf":    "Hold — if #2 &amp; #3 fall through",
    "Sadia Sohail":      "Pipeline — ramp in 12&ndash;18 months",
    "Arsim Tariq":       "No — M&amp;E, not acquisition",
    "Ahmed Al-Mayadeen": "No — geo + budget deal-breaker",
    "Ahad Ahsan Khan":   "No — compliance, not acquisition",
    "Muhammad Usman":    "No — no quantified track record",
    "Mushahid Hussain":  "No — junior; BD support role later",
}

html += """
<h3 style="color:#6B21A8;margin-top:20px;margin-bottom:8px;font-size:15px;">Part A &mdash; Master Ranking Summary</h3>
<table width="100%" border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:11px;margin-bottom:8px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">#</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Candidate</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">Score</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">Tier</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">Experience</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Background / Current Role</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Org Signal</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">Budget</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Key Strength</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Key Gap / Why Not Proceed</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Verdict</th>
  </tr>"""

for c in CANDIDATES:
    even = c["rank"] % 2 == 0
    bg = "#F5F3FF" if even else "#ffffff"
    sig_short = c["org_signals"][0][0].split("—")[0].strip()[:30] if c["org_signals"] else "&mdash;"
    ocr_mark = " &#128269;" if c.get("ocr") else ""
    fw = "bold" if c["rank"] <= 5 else "normal"
    verdict = VERDICT.get(c["name"], "&mdash;")
    vl = verdict.lower()
    vcolor = "#16A34A" if "immediately" in vl else ("#D97706" if "sign-off" in vl or "hold" in vl or "pipeline" in vl else "#DC2626")
    html += f"""
  <tr bgcolor="{bg}" style="background-color:{bg};">
    <td style="font-weight:{fw};text-align:center;">{c["rank"]}</td>
    <td style="font-weight:{fw};">{c["name"]}{ocr_mark}</td>
    <td bgcolor="{c["tier_color"]}" style="background-color:{c["tier_color"]};color:#fff;font-weight:bold;text-align:center;">{c["score"]}</td>
    <td bgcolor="{c["tier_color"]}" style="background-color:{c["tier_color"]};color:#fff;text-align:center;font-size:10px;">{c["tier"]}</td>
    <td style="font-size:10px;text-align:center;">{c["total_exp"]}</td>
    <td style="font-size:10px;color:#374151;">{c["current_role"]}</td>
    <td style="font-size:10px;color:#374151;">{sig_short}</td>
    <td style="text-align:center;"><span style="background:{c["budget_color"]};color:{c["budget_text_color"]};border-radius:8px;padding:1px 5px;font-size:10px;font-weight:bold;">{c["budget_label"]}</span></td>
    <td style="font-size:10px;color:#374151;">{KEY_STRENGTH.get(c["name"], "&mdash;")}</td>
    <td style="font-size:10px;color:#DC2626;">{KEY_GAP.get(c["name"], "&mdash;")}</td>
    <td style="font-size:10px;font-weight:bold;color:{vcolor};">{verdict}</td>
  </tr>"""

# ── No-hire candidates (ranks 11–36) ─────────────────────────────
html += """
  <tr>
    <td colspan="11" bgcolor="#374151" style="background-color:#374151;color:#fff;font-weight:bold;font-size:11px;padding:6px 8px;text-align:center;">
      &#8212; NO-HIRE CANDIDATES (Ranks #11&ndash;#48) &mdash; Assessed but did not meet JD threshold &#8212;
    </td>
  </tr>"""

for n in NO_HIRE_CANDIDATES:
    even = n["rank"] % 2 == 0
    bg = "#F9FAFB" if even else "#F3F4F6"
    score_color = "#6B7280"
    nh_loc = n.get("location", "&mdash;")
    nh_role = n.get("current_role", n["background"])
    nh_org = NH_ORG_SIGNAL.get(n["name"], "")
    html += f"""
  <tr bgcolor="{bg}" style="background-color:{bg};">
    <td style="text-align:center;color:#6B7280;">{n["rank"]}</td>
    <td style="color:#374151;">{n["name"]}</td>
    <td bgcolor="#6B7280" style="background-color:#6B7280;color:#fff;font-weight:bold;text-align:center;">{n["score"]}</td>
    <td bgcolor="#6B7280" style="background-color:#6B7280;color:#fff;text-align:center;font-size:10px;">No-Hire</td>
    <td style="font-size:10px;text-align:center;color:#6B7280;">{nh_loc}</td>
    <td style="font-size:10px;color:#6B7280;font-style:italic;">{nh_role}</td>
    <td style="font-size:10px;color:#9CA3AF;">{nh_org if nh_org else "&mdash;"}</td>
    <td style="text-align:center;color:#9CA3AF;">&#8212;</td>
    <td style="font-size:10px;color:#6B7280;">{n["strength_note"]}</td>
    <td style="font-size:10px;color:#DC2626;">{n["reason"]}</td>
    <td style="font-size:10px;font-weight:bold;color:#DC2626;">No-Hire</td>
  </tr>"""

# No-resume and excluded rows
html += """
  <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
    <td style="text-align:center;color:#9CA3AF;">49+</td>
    <td style="color:#9CA3AF;font-style:italic;">13 applicants — No CV submitted</td>
    <td style="text-align:center;color:#9CA3AF;">N/A</td>
    <td bgcolor="#9CA3AF" style="background-color:#9CA3AF;color:#fff;text-align:center;font-size:10px;">Not Assessed</td>
    <td colspan="7" style="font-size:10px;color:#9CA3AF;">LinkedIn Quick Apply with no CV attached. Known app IDs: 1332, 1336, 1348, 1350, 1366, 1372, 1386, 1407, 1515 + 4 additional. Cannot be assessed without CV data.</td>
  </tr>
  <tr bgcolor="#F3F4F6" style="background-color:#F3F4F6;">
    <td style="text-align:center;color:#9CA3AF;">&mdash;</td>
    <td style="color:#9CA3AF;font-style:italic;">1 applicant — Excluded</td>
    <td style="text-align:center;color:#9CA3AF;">N/A</td>
    <td bgcolor="#9CA3AF" style="background-color:#9CA3AF;color:#fff;text-align:center;font-size:10px;">Excluded</td>
    <td colspan="7" style="font-size:10px;color:#9CA3AF;">Danish Hussain (app 1347) &mdash; duplicate of application 1346 (same candidate, already ranked #1)</td>
  </tr>
</table>
<p style="font-size:10px;color:#6B7280;margin:2px 0 20px 0;">&#128269; = OCR-recovered CV &bull; <b>Bold rows</b> = Tier A/B/C shortlist &bull; Scores for Ranks #11&ndash;#48 are calibrated estimates based on CV evidence and 7-dimension framework.</p>
"""

# ── Part C: No-Hire Individual Profile Cards (#11–#48) ───────────────────────────────
CAT_COLORS = {
    "Sector-Adjacent":      "#1D4ED8",
    "No Impact Ownership":  "#D97706",
    "Wrong Sector":         "#7C3AED",
    "Wrong Sector / Geo":   "#7C3AED",
    "Junior Profile":       "#0891B2",
    "Unrelated Background": "#6B7280",
    "Could Not Assess":     "#9CA3AF",
}
CAT_NOTES = {
    "Sector-Adjacent":      "Right ecosystem, wrong function — programme delivery, M&amp;E, compliance, or field work rather than donor acquisition.",
    "No Impact Ownership":  "Adjacent function but no evidence of independently owning a pipeline or closing institutional grants.",
    "Wrong Sector":         "Fundraising function confirmed but wrong sector (domestic charity, CSR, WASH) or wrong geography with no relocation commitment.",
    "Wrong Sector / Geo":   "Fundraising function confirmed but wrong sector (domestic charity, CSR, WASH) or wrong geography with no relocation commitment.",
    "Junior Profile":       "Correct direction but insufficient experience and seniority for a Year-1 $500K+ acquisition mandate.",
    "Unrelated Background": "No connection to institutional fundraising, NGO ecosystem, or development donors.",
    "Could Not Assess":     "CV submitted but could not be extracted — unreadable PDF returned zero text even after OCR.",
}

html += """
<!-- ── Charts: Score Comparison + Dimension Radar ── -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:32px;font-size:18px;">&#50;&#65039;&#8419; Visual Analytics &mdash; Charts</h2>
<h3 style="color:#6B21A8;margin-top:16px;font-size:15px;">A. Score Comparison &mdash; All Candidates</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:12px;text-align:center;">
  <img src="cid:bar_chart" style="max-width:100%;height:auto;" alt="Candidate Score Bar Chart">
</td></tr></table>
<h3 style="color:#6B21A8;margin-top:20px;font-size:15px;">B. Dimension Radar &mdash; Top 3 Candidates</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:12px;text-align:center;">
  <img src="cid:spider_chart" style="max-width:700px;height:auto;" alt="Dimension Radar Spider Chart">
</td></tr></table>
"""

# ── SECTION 4: STRONG MATCH BUT OUT OF BUDGET ───────────────────
html += """
<!-- ══════════════════════════════════════════════════════════════
     SECTION 4: STRONG MATCH BUT OUT OF BUDGET
═══════════════════════════════════════════════════════════════ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">&#51;&#65039;&#8419; Strong Match but Out of Budget</h2>

<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;margin-bottom:12px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Candidate</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Score</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Expected Salary</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Budget Gap</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Worth the Stretch?</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Justification</th>
  </tr>
  <tr>
    <td><b>Danish Hussain</b></td><td><b>97.5</b></td>
    <td>PKR 550,000/month</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 6px;border-radius:6px;">+PKR 280,000</span></td>
    <td><b style="color:#16A34A;">YES — with a structured offer</b></td>
    <td style="font-size:11px;">PKR 1B+ track record. Named FCDO/UNDP/ADB relationships. 20-year Head-level experience. Recommend a PKR 380–420K base + PKR 80–100K performance-on-milestones package. Present as Head of Fundraising &amp; Partnerships, not Manager. The uplift pays for itself in Year 1 grant closures.</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b>Zain Ul Abideen</b> &#128269;</td><td><b>95.0</b></td>
    <td>PKR 350,000/month</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 6px;border-radius:6px;">+PKR 80,000</span></td>
    <td><b style="color:#16A34A;">YES — immediately actionable</b></td>
    <td style="font-size:11px;">US $50M track record across two Pakistan organisations. Islamabad-based. PKR 80K is the most defensible budget exception in this pool. Recommend approving PKR 350K directly — the ROI on $50M in proven mobilisation experience is immediate. Smallest ask, highest evidence.</td>
  </tr>
  <tr>
    <td><b>Arsalan Ashraf</b></td><td><b>72.2</b></td>
    <td>PKR 450,000/month</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 6px;border-radius:6px;">+PKR 180,000</span></td>
    <td><b style="color:#EAB308;">CONDITIONAL — only if #1 and #2 fail</b></td>
    <td style="font-size:11px;">Strong builder track record at 3 orgs. Missing multilateral must-have is a real gap. Budget exception at this level is only justified if interviews with Zain and Mizhgan don't yield a hire AND Arsalan can demonstrate USAID/FCDO exposure in interview. His corporate CSR focus makes the exception harder to justify at this stage.</td>
  </tr>
</table>
"""

# ── SECTION 5: VISUAL ANALYTICS ─────────────────────────────────
html += """
<!-- ══════════════════════════════════════════════════════════════
     SECTION 5: VISUAL ANALYTICS
═══════════════════════════════════════════════════════════════ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">&#52;&#65039;&#8419; Visual Analytics</h2>

<!-- Chart A: JD Criteria Heatmap -->
<h3 style="color:#6B21A8;margin-top:20px;font-size:15px;">A. Heatmap &mdash; Candidate vs JD Must-Have Criteria Match</h3>
<p style="font-size:11px;color:#6B7280;margin-bottom:6px;">Scale: <b style="color:#16A34A;">&#9632;</b> 4=Fully meets &nbsp; <b style="color:#22C55E;">&#9632;</b> 3=Strong &nbsp; <b style="color:#EAB308;">&#9632;</b> 2=Partial &nbsp; <b style="color:#F97316;">&#9632;</b> 1=Weak &nbsp; <b style="color:#DC2626;">&#9632;</b> 0=Missing</p>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:12px;">
<table width="100%" border="1" cellpadding="7" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:11px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:left;padding:6px 8px;">Candidate</th>
    <th bgcolor="#7C3AED" style="background-color:#7C3AED;color:#fff;text-align:center;">MH1<br>Direct BD</th>
    <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">MH2<br>Pak Donors</th>
    <th bgcolor="#0891B2" style="background-color:#0891B2;color:#fff;text-align:center;">MH3<br>Proposals Won</th>
    <th bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;">MH4<br>Pipeline Mgmt</th>
    <th bgcolor="#D97706" style="background-color:#D97706;color:#fff;text-align:center;">MH5<br>Islamabad</th>
    <th bgcolor="#DC2626" style="background-color:#DC2626;color:#fff;text-align:center;">MH6<br>Comms</th>
    <th bgcolor="#DB2777" style="background-color:#DB2777;color:#fff;text-align:center;">NH1<br>$500K+ Deal</th>
    <th bgcolor="#9333EA" style="background-color:#9333EA;color:#fff;text-align:center;">NH2<br>Named Donors</th>
  </tr>"""

for i, c in enumerate(CANDIDATES):
    nm = c["name"]
    sc = MH_SCORES.get(nm, [0]*10)
    bg = "#F5F3FF" if i % 2 == 0 else "#fff"
    fw = "bold" if c["rank"] <= 5 else "normal"
    ocr = " &#128269;" if c.get("ocr") else ""
    row = f'<tr bgcolor="{bg}" style="background-color:{bg};"><td style="font-weight:{fw};padding:5px 8px;">{c["rank"]}. {nm}{ocr}</td>'
    for s in sc[:8]:
        row += cell(s, "5")
    row += "</tr>"
    html += row

html += """
</table>
<p style="font-size:10px;color:#6B7280;margin:6px 0 0 0;">MH=Must-Have &bull; NH=Nice-to-Have &bull; Bold rows = shortlisted. &#128269;=OCR-recovered.</p>
</td></tr>
</table>
"""

# Charts already embedded at top of email — nothing to add here

# ── SECTION 6: WHY OTHERS DIDN'T MAKE IT ────────────────────────
html += """
<!-- ══════════════════════════════════════════════════════════════
     SECTION 6: WHY OTHERS DID NOT MAKE IT
═══════════════════════════════════════════════════════════════ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">&#53;&#65039;&#8419; Why Others Did Not Make the Cut</h2>
<p style="font-size:12px;color:#6B7280;margin-bottom:12px;">Summary of elimination reasons (see Section 3 Part C for full individual profiles of all 38 no-hire candidates). Every candidate was reviewed in full &mdash; these decisions reflect JD evidence, not assumptions.</p>

<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;width:35%;">Reason</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;width:10%;">Count</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Candidates</th>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">Development sector adjacent &mdash; no fundraising acquisition ownership</b><br><span style="font-size:11px;color:#6B7280;">Programme delivery, M&amp;E, reporting, B2G, and compliance roles were confused with fundraising in applications. Managing grants or government contracts &ne; acquiring new institutional funding.</span></td>
    <td style="text-align:center;font-weight:bold;">9</td>
    <td style="font-size:11px;">Faheem Baig (programme implementation) &bull; Hamdan Ahmad (World Bank programme management) &bull; Shakir Manzoor (grants support role) &bull; Sarmad Iqbal (B2G strategy, not acquisition) &bull; Zubair Hussain (field specialist) &bull; Abdul Salam (WASH delivery) &bull; Mehboob Alam (JICA programme management) &bull; Bareera Rauf (development researcher) &bull; Bushra Nawaz (Islamic Relief livelihoods PM)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#DC2626;">Wrong sector &mdash; domestic charity / CSR / non-institutional fundraising</b><br><span style="font-size:11px;color:#6B7280;">Fundraising function confirmed but donor base is individual donors, CSR corporate partners, or hospital charity &mdash; fundamentally different from multilateral/bilateral institutional fundraising.</span></td>
    <td style="text-align:center;font-weight:bold;">5</td>
    <td style="font-size:11px;">Mohammad Aqeel Qureshi (Shifa Foundation healthcare charity) &bull; Shahzad Saleem Abbasi (Junior Jinnah Trust domestic CSR, PKR 400M but all individual/corporate) &bull; Fahad Khan (hospital charity fundraising) &bull; Imran Haider (education policy analyst, not BD) &bull; Anita Kanwal (UK-based digital charity campaigns, no relocation stated)</td>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">Completely unrelated professional background</b><br><span style="font-size:11px;color:#6B7280;">These candidates bring genuine skills in their fields but none of their experience maps to institutional donor fundraising.</span></td>
    <td style="text-align:center;font-weight:bold;">16</td>
    <td style="font-size:11px;">Bilal Shahid (SaaS M&amp;A) &bull; Mahnoor Mellu (SaaS partnerships) &bull; Muhammad Ali Zafar (research intern) &bull; Zainab (early-career HR) &bull; Sameen Amjad Ali (marketing/comms) &bull; Hasan Shahid (digital marketing) &bull; Muhammad Taqi (SaaS sales) &bull; Muhammad Sumraiz Kundi (telecom sales) &bull; Asim Ur Rehman (rural volunteer) &bull; Sikandar Khurshid (Taleemabad alumni — customer success) &bull; Sheraz Khan (Microsoft licensing) &bull; Muhammad Akmal (admin) &bull; Laveeza Shah (HR) &bull; Samreen Durrani (policy research/content) &bull; Arooj Irfan (clinical psychologist) &bull; Ibrahim Basit (marketing trainee) &bull; Moeen Hassan (AutoCAD/real estate) &bull; Hira Noureen Khan (clinical psychologist) &bull; Aqsa Gul (customer service) &bull; Sani Muhammad (IT operations)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#DC2626;">No evidence of impact ownership &mdash; activity without outcomes</b><br><span style="font-size:11px;color:#6B7280;">These candidates have worked in relevant organisations but could not evidence direct ownership of fundraising results.</span></td>
    <td style="text-align:center;font-weight:bold;">3</td>
    <td style="font-size:11px;">Muhammad Usman (18 years, zero quantified outcomes in entire career) &bull; Arsim Tariq (M&amp;E lead on funded projects, not the acquisition owner) &bull; Syeda Kainat (M&amp;E/comms on donor projects)</td>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">Junior profile vs required seniority</b><br><span style="font-size:11px;color:#6B7280;">These candidates show genuine interest in fundraising but do not yet have the depth or deal-closing record needed for a Year-1 $500K&ndash;$1M+ mandate.</span></td>
    <td style="text-align:center;font-weight:bold;">4</td>
    <td style="font-size:11px;">Mushahid Hussain (4 years, junior donor reporting only) &bull; Samana Qaseem (alumni/admin background) &bull; SAHRISH KASHIF (community development PM, small foundation grants only) &bull; Ahad Ahsan Khan (grants compliance, not acquisition) &bull; Sameen Amjad Ali (marketing/comms)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#DC2626;">Wrong geography &mdash; no relocation commitment</b><br><span style="font-size:11px;color:#6B7280;">Based outside Pakistan or outside Islamabad with no willingness-to-relocate stated.</span></td>
    <td style="text-align:center;font-weight:bold;">1</td>
    <td style="font-size:11px;">Ahmed Al-Mayadeen (Yemen-based, MENA fundraising background, no Pakistan donor network, no relocation stated &mdash; triple deal-breaker)</td>
  </tr>
  <tr>
    <td><b style="color:#6B7280;">CV unreadable / could not assess</b></td>
    <td style="text-align:center;font-weight:bold;">1</td>
    <td style="font-size:11px;">AAMIR SOHAIL (app 1393) &mdash; PDF submitted but zero text extracted even after OCR. Cannot be assessed without a readable CV. Candidate should resubmit in text-based PDF format.</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#6B7280;">No resume submitted / data gaps</b></td>
    <td style="text-align:center;font-weight:bold;">13</td>
    <td style="font-size:11px;">Apps 1332, 1336, 1348, 1350, 1366, 1372, 1386, 1407, 1515 + 4 additional &mdash; LinkedIn Quick Apply with no CV attached. Cannot be assessed without CV data.</td>
  </tr>
  <tr>
    <td><b style="color:#6B7280;">Excluded (duplicate)</b></td>
    <td style="text-align:center;font-weight:bold;">1</td>
    <td style="font-size:11px;">Danish Hussain (app 1347) &mdash; duplicate of application 1346 (same candidate, already ranked #1)</td>
  </tr>
</table>

<!-- Recommended Next Steps -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">&#128204; Recommended Next Steps</h2>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td bgcolor="#F5F3FF" style="background-color:#F5F3FF;border-left:5px solid #7C3AED;border-radius:6px;padding:14px 18px;">
  <ol style="margin:0;padding-left:20px;font-size:13px;line-height:1.9;">
    <li><b>Invite Zain Ul Abideen (#2) immediately</b> &mdash; PKR 80K gap, Islamabad-based, US $50M track record. Most immediately actionable hire.</li>
    <li><b>Invite Mizhgan Kirmani (#3) simultaneously</b> &mdash; zero budget exception, zero relocation risk, active FCDO/USAID/UNDP relationships at TCF. Run both interviews in parallel.</li>
    <li><b>Get leadership sign-off for Danish Hussain (#1)</b> before inviting &mdash; present as Head of Fundraising &amp; Partnerships at PKR 380–420K (base + performance). PKR 1B+ track record justifies the level and the package.</li>
    <li><b>Hold Arsalan Ashraf (#4)</b> pending outcomes of #2 and #3. His missing multilateral experience is a real gap but his builder mindset is relevant if others fall through.</li>
    <li><b>Re-post with clearer language</b> if the shortlist does not yield a hire &mdash; add &ldquo;Multilateral donor experience (USAID, FCDO, World Bank) essential&rdquo; to the JD title line to reduce volume of programme-delivery applications.</li>
  </ol>
</td></tr>
</table>

<p style="font-size:11px;color:#9CA3AF;margin-top:28px;text-align:center;">
  Taleemabad Talent Acquisition Agent &bull; Confidential
</p>
</body></html>"""

# ══════════════════════════════════════════════════════════════════
# SEND EMAIL — multipart/related with CID inline images
# Structure: related > alternative > text/html  +  image/png × 2
# ══════════════════════════════════════════════════════════════════
msg = MIMEMultipart("related")
msg["Subject"] = "Screening Report- Fundraising & Partnerships Manager"
msg["From"]    = SENDER
msg["To"]      = RECIPIENT

# HTML body lives inside an "alternative" child
alt = MIMEMultipart("alternative")
msg.attach(alt)
alt.attach(MIMEText(html, "html"))

# Bar chart — inline, referenced via cid:bar_chart in the HTML
bar_img = MIMEImage(bar_bytes, "png")
bar_img.add_header("Content-ID", "<bar_chart>")
bar_img.add_header("Content-Disposition", "inline")   # NOT attachment
msg.attach(bar_img)

# Spider chart — inline, referenced via cid:spider_chart in the HTML
spider_img = MIMEImage(spider_bytes, "png")
spider_img.add_header("Content-ID", "<spider_chart>")
spider_img.add_header("Content-Disposition", "inline")
msg.attach(spider_img)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER, PASSWORD)
    allow_candidate_addresses(RECIPIENT if isinstance(RECIPIENT, list) else [RECIPIENT])
        safe_sendmail(server, SENDER, RECIPIENT, msg.as_string(), context='send_job32_report_v10')

print("Email sent — CID inline charts embedded in email body.")
