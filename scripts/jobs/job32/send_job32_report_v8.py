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
<p style="color:#6B21A8;font-weight:bold;margin-top:4px;">v8 &bull; Updated 12-Step Framework &bull; Organisation Signal Analysis &bull; CV Quality &bull; USP &bull; 2026-03-04</p>

<!-- ══ CHARTS AT TOP (before clip point) ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:28px;font-size:18px;">&#54;&#65039;&#8419; Visual Analytics</h2>
<h3 style="color:#6B21A8;margin-top:16px;font-size:15px;">A. Score Comparison &mdash; All 10 Candidates</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:12px;text-align:center;">
  <img src="cid:bar_chart" style="max-width:100%;height:auto;" alt="Candidate Score Bar Chart">
</td></tr></table>
<h3 style="color:#6B21A8;margin-top:20px;font-size:15px;">B. Dimension Radar &mdash; Top 3 Candidates</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:12px;text-align:center;">
  <img src="cid:spider_chart" style="max-width:700px;height:auto;" alt="Dimension Radar Spider Chart">
</td></tr></table>

<!-- ══════════════════════════════════════════════════════════════
     SECTION 1: SCREENING SUMMARY
═══════════════════════════════════════════════════════════════ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:32px;font-size:18px;">&#49;&#65039;&#8419; Screening Summary</h2>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td bgcolor="#EDE9FE" style="background-color:#EDE9FE;border-left:5px solid #7C3AED;border-radius:6px;padding:16px 20px;">
  <table cellpadding="5" cellspacing="0" border="0">
    <tr><td style="color:#6B21A8;font-weight:bold;white-space:nowrap;padding-right:20px;">Total Profiles Reviewed</td><td>48 applications &bull; 37 CVs parsed (36 standard PDF + 1 OCR-recovered) &bull; 11 excluded (9 no-resume, 1 junk, 1 duplicate)</td></tr>
    <tr><td style="color:#6B21A8;font-weight:bold;">Role</td><td>Fundraising &amp; Partnerships Manager &mdash; Job ID JOB-0032</td></tr>
    <tr><td style="color:#6B21A8;font-weight:bold;">Budget Range</td><td>PKR 150,000 &ndash; 270,000 / month</td></tr>
    <tr><td style="color:#6B21A8;font-weight:bold;">Recommended Shortlist</td><td>Top 10 (pool of 48 sits at the 40&ndash;50 boundary &rarr; applying upper end of 20&ndash;40 rule: 7&ndash;10)</td></tr>
    <tr><td style="color:#6B21A8;font-weight:bold;">Tier Breakdown</td><td>
      <b style="color:#16A34A;">Tier A (85+): 2</b> &bull;
      <b style="color:#1D4ED8;">Tier B (70&ndash;84): 2</b> &bull;
      <b style="color:#D97706;">Tier C (55&ndash;69): 1</b> &bull;
      <b style="color:#6B7280;">Extended Review: 5</b> &bull;
      No-Hire: 27
    </td></tr>
  </table>
</td></tr>
</table>
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:12px;">
<tr><td bgcolor="#F5F3FF" style="background-color:#F5F3FF;border-left:5px solid #EC4899;border-radius:6px;padding:14px 18px;">
  <p style="margin:0;font-size:13px;line-height:1.7;color:#374151;">
    <b>Overall Talent Quality Assessment:</b> This is a demanding specialist role and the pool reflects that challenge.
    Only 5 of 37 assessable CVs reached Tier C or above under the 7-dimension evidence-based framework.
    The top two candidates &mdash; Danish Hussain and Zain Ul Abideen &mdash; are exceptional: both carry multi-million dollar
    fundraising track records with named bilateral/multilateral donors in Pakistan, and both score in the 95&ndash;98 range.
    The critical constraint is budget: neither is within the PKR 150&ndash;270K range.
    The only fully in-budget, zero-risk Tier B candidate is Mizhgan Kirmani (TCF, PKR 250K), whose active FCDO/UNDP/USAID
    relationships make her the most deployable hire without a salary exception.
    <b>Organisation Signal quality is strong</b> &mdash; TCF, READ Foundation, and UN agency alumni appear across the top 5.
    The Extended Review pool (6&ndash;10) shows sector-adjacent experience but lacks acquisition ownership.
    Re-posting with a stronger multilateral-mandate signal is recommended if this shortlist does not yield a hire.
  </p>
</td></tr>
</table>

<!-- ══════════════════════════════════════════════════════════════
     SECTION 2: JD SCORECARD
═══════════════════════════════════════════════════════════════ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">&#50;&#65039;&#8419; JD Scorecard</h2>
<p style="font-size:12px;color:#6B7280;margin-bottom:8px;font-style:italic;">Role Mission: Build and run Taleemabad&rsquo;s institutional fundraising function from Islamabad. Find, develop, and close $500K&ndash;$1M+ in Year 1 from multilateral donors (USAID, World Bank, FCDO, JICA, EU, UN agencies), foundations, and bilateral partners.</p>

<p style="font-size:13px;font-weight:bold;color:#4C1D95;margin:12px 0 4px 0;">Must-Have Criteria &mdash; Shortlist Match</p>
<table width="100%" border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;margin-bottom:16px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:left;">Must-Have Requirement</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;white-space:nowrap;">Pool Match<br>(37 CVs)</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:left;">Best Evidence in Shortlist</th>
  </tr>
  <tr>
    <td><b>1. Direct fundraising / BD ownership</b><br><span style="font-size:11px;color:#6B7280;">(not programme delivery — acquisition only)</span></td>
    <td style="text-align:center;"><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 8px;border-radius:8px;">~16%</span><br><span style="font-size:10px;color:#6B7280;">~6 of 37</span></td>
    <td style="font-size:12px;">Danish: Head of Grants &amp; Partnerships, 20 yrs &bull; Zain: Deputy Manager Resource Mobilisation &bull; Mizhgan: Manager Donor Relations, TCF</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b>2. Pakistan donor landscape knowledge</b><br><span style="font-size:11px;color:#6B7280;">(USAID, World Bank, DFID/FCDO, JICA, EU, multilaterals)</span></td>
    <td style="text-align:center;"><span style="background:#FEF3C7;color:#92400E;font-weight:bold;padding:2px 8px;border-radius:8px;">~24%</span><br><span style="font-size:10px;color:#6B7280;">~9 of 37</span></td>
    <td style="font-size:12px;">Zain: UNICEF, UNFPA, US Embassy, British Council Pakistan &bull; Mizhgan: FCDO, UN Women, UNDP, USAID at TCF &bull; Danish: FCDO Pak, UNDP Pak, ADB</td>
  </tr>
  <tr>
    <td><b>3. Proposals / grant writing &mdash; submitted and won</b></td>
    <td style="text-align:center;"><span style="background:#FEF3C7;color:#92400E;font-weight:bold;padding:2px 8px;border-radius:8px;">~22%</span><br><span style="font-size:10px;color:#6B7280;">~8 of 37</span></td>
    <td style="font-size:12px;">Zain: US $50M lifetime &bull; Danish: PKR 1B+ mobilised &bull; Mizhgan: PKR 72M in FY &bull; Arsalan: Meta $100K, Chevron $250K, PKR 80M NAVTTC</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b>4. Pipeline management (30&ndash;50+ live opportunities)</b></td>
    <td style="text-align:center;"><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 8px;border-radius:8px;">~11%</span><br><span style="font-size:10px;color:#6B7280;">~4 of 37</span></td>
    <td style="font-size:12px;">Danish: Yes &bull; Zain: Yes &bull; Arsalan: 15&ndash;20 active opportunities cited</td>
  </tr>
  <tr>
    <td><b>5. Islamabad-based or explicitly willing to relocate</b></td>
    <td style="text-align:center;"><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:2px 8px;border-radius:8px;">~68%</span><br><span style="font-size:10px;color:#6B7280;">~25 of 37</span></td>
    <td style="font-size:12px;">Most of the pool is Islamabad-based. Exceptions: Danish (willing to relocate), Arsalan (willing to relocate), Ahmed Al-Mayadeen (Yemen, not mentioned = deal-breaker)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b>6. Strong written communication &amp; presentation</b></td>
    <td style="text-align:center;"><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:2px 8px;border-radius:8px;">~54%</span><br><span style="font-size:10px;color:#6B7280;">~20 of 37</span></td>
    <td style="font-size:12px;">Top 5 all demonstrate strong communication clarity in CV. Ahmed Al-Mayadeen (HBS) is the strongest communicator signal.</td>
  </tr>
</table>

<p style="font-size:13px;font-weight:bold;color:#1D4ED8;margin:12px 0 4px 0;">Nice-to-Have Criteria &mdash; Shortlist Match</p>
<table width="100%" border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;margin-bottom:12px;">
  <tr>
    <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:left;">Nice-to-Have Requirement</th>
    <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">Pool Match</th>
    <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:left;">Evidence</th>
  </tr>
  <tr>
    <td>Independently closed $500K+ single deal</td>
    <td style="text-align:center;"><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 6px;border-radius:6px;">~5%</span></td>
    <td style="font-size:12px;">Danish (PKR 1B+ total, individual deal size not specified) &bull; Zain ($8.44M at one org) &bull; Ahmed (multi-million dollar campaigns)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td>Named bilateral/multilateral relationships in Pakistan</td>
    <td style="text-align:center;"><span style="background:#FEF3C7;color:#92400E;font-weight:bold;padding:2px 6px;border-radius:6px;">~16%</span></td>
    <td style="font-size:12px;">Zain: UNICEF, British Council, US Embassy &bull; Mizhgan: FCDO, UN Women, UNDP, USAID &bull; Danish: FCDO Pak, UNDP Pak, ADB</td>
  </tr>
  <tr>
    <td>Education sector experience</td>
    <td style="text-align:center;"><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:2px 6px;border-radius:6px;">~35%</span></td>
    <td style="font-size:12px;">Mizhgan (TCF) &bull; Sadia &amp; Mushahid (READ Foundation) &bull; Zain (READ Foundation) &bull; Ahad (AKU)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td>Government/policy engagement in Islamabad</td>
    <td style="text-align:center;"><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 6px;border-radius:6px;">~8%</span></td>
    <td style="font-size:12px;">Muhammad Usman (public affairs background) &bull; Arsim Tariq (policy sector projects)</td>
  </tr>
</table>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;border-radius:6px;padding:10px 16px;text-align:center;">
  <b style="font-size:14px;">Overall JD Match Score across 37 assessed CVs: ~19%</b>
  <span style="font-size:12px;opacity:0.85;"> &mdash; Only 7 candidates met 4+ of 6 must-haves. This is a specialist role with a thin Pakistan pipeline.</span>
</td></tr>
</table>
"""

# ── SECTION 3: RANKED SHORTLIST ──────────────────────────────────
html += """
<!-- ══════════════════════════════════════════════════════════════
     SECTION 3: RANKED SHORTLIST
═══════════════════════════════════════════════════════════════ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">&#51;&#65039;&#8419; Ranked Shortlist &mdash; Top 10 Candidates</h2>
<p style="font-size:12px;color:#6B7280;margin-bottom:12px;">Candidates 1&ndash;5 = shortlisted (Tier A/B/C). Candidates 6&ndash;10 = Extended Review (closest to threshold). Full profiles below.</p>
"""

# Quick-view table
html += """
<table width="100%" border="1" cellpadding="7" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;margin-bottom:24px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">#</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Candidate</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Score</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Tier</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">CV Quality</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Org Signal</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Salary</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Budget</th>
  </tr>"""

quality_colors = {"High": "#16A34A", "Moderate-High": "#22C55E", "Moderate": "#EAB308", "Low-Moderate": "#F97316", "Low": "#DC2626"}
for c in CANDIDATES:
    even = c["rank"] % 2 == 0
    bg = "#F5F3FF" if even else "#ffffff"
    qlabel = c["cv_quality"]
    qc = quality_colors.get(qlabel, "#6B7280")
    signals_short = "; ".join(s[0][:20]+"…" if len(s[0])>20 else s[0] for s in c["org_signals"]) if c["org_signals"] else "None"
    ocr_mark = " &#128269;" if c.get("ocr") else ""
    fw = "bold" if c["rank"] <= 5 else "normal"
    html += f"""
  <tr bgcolor="{bg}" style="background-color:{bg};">
    <td style="font-weight:{fw};">{c["rank"]}</td>
    <td style="font-weight:{fw};">{c["name"]}{ocr_mark}</td>
    <td style="font-weight:{fw};text-align:center;">{c["score"]}</td>
    <td bgcolor="{c["tier_color"]}" style="background-color:{c["tier_color"]};color:#fff;font-weight:bold;text-align:center;font-size:11px;">{c["tier"]}</td>
    <td style="text-align:center;"><span style="background:{qc};color:#fff;border-radius:8px;padding:2px 7px;font-size:11px;font-weight:bold;">{qlabel}</span></td>
    <td style="font-size:11px;color:#374151;">{signals_short}</td>
    <td style="font-size:11px;">{c["salary"]}</td>
    <td><span style="background:{c["budget_color"]};color:{c["budget_text_color"]};border-radius:8px;padding:2px 7px;font-size:11px;font-weight:bold;">{c["budget_label"]}</span></td>
  </tr>"""

html += "</table>"

# ── Full individual profiles ─────────────────────────────────────
for c in CANDIDATES:
    border_color = c["tier_color"]
    ocr_tag = ' <span style="background:#EFF6FF;color:#1D4ED8;border-radius:10px;padding:2px 6px;font-size:11px;">&#128269; OCR-recovered</span>' if c.get("ocr") else ""
    mh_warn = f'<p style="color:#D97706;font-size:12px;margin:4px 0;"><b>&#9888; {c["missing_mh"]} missing must-have(s) &mdash; &minus;{c["missing_mh"]*15}% penalty applied</b></p>' if c["missing_mh"] > 0 else ""

    # Org signals
    if c["org_signals"]:
        sig_rows = "".join(f'<li style="margin-bottom:2px;"><b style="color:#6B21A8;">{s[0]}</b> &mdash; {s[1]}</li>' for s in c["org_signals"])
        sig_html = f'<p style="margin:8px 0 2px 0;font-size:12px;font-weight:bold;color:#6B21A8;">&#127942; Strategic Signals:</p><ul style="margin:0;padding-left:18px;font-size:12px;">{sig_rows}</ul>'
    else:
        sig_html = '<p style="font-size:12px;color:#9CA3AF;margin:4px 0;">&#127942; Strategic Signal: None identified</p>'

    # CV quality
    qc = quality_colors.get(c["cv_quality"], "#6B7280")
    cv_qual_html = f'<p style="font-size:12px;margin:6px 0;"><b>CV Quality:</b> <span style="background:{qc};color:#fff;border-radius:8px;padding:2px 8px;font-size:11px;font-weight:bold;">{c["cv_quality"]}</span> &mdash; <span style="color:#6B7280;">{c["cv_quality_note"]}</span></p>'

    str_items = "".join(f"<li style='margin-bottom:3px;font-size:13px;'>{s}</li>" for s in c["strengths"])
    risk_items = "".join(f"<li style='margin-bottom:3px;font-size:13px;'>{r}</li>" for r in c["risks"])
    q_items    = "".join(f"<li style='margin-bottom:3px;font-size:13px;'>{q}</li>" for q in c["interview_qs"])
    d1,d2,d3,d4,d5,d6,d7 = c["dims"]

    section_label = "SHORTLIST" if c["rank"] <= 5 else "EXTENDED REVIEW"
    if c["rank"] == 6:
        html += """<h3 style="color:#6B7280;border-top:2px dashed #D1D5DB;padding-top:16px;margin-top:32px;font-size:15px;">Extended Review &mdash; Candidates 6&ndash;10 (closest to threshold)</h3>
<p style="font-size:12px;color:#6B7280;">These candidates did not reach Tier C but are the closest to it. Consider only if Tier A/B/C candidates do not yield a hire.</p>"""

    html += f"""
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:18px;">
<tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #E5E7EB;border-left:5px solid {border_color};border-radius:6px;padding:16px;">
  <p style="margin:0 0 6px 0;font-size:15px;font-weight:bold;color:#111827;">
    #{c["rank"]} {c["name"]}{ocr_tag} &nbsp;
    <span style="background-color:{c["tier_color"]};color:#fff;border-radius:20px;padding:4px 14px;font-weight:bold;font-size:13px;">{c["score"]} / 100 &mdash; {c["tier"]}</span>
    &nbsp;<span style="background:{c["budget_color"]};color:{c["budget_text_color"]};font-weight:bold;padding:3px 10px;border-radius:12px;font-size:12px;">{c["budget_label"]} {c["budget_gap"]}</span>
  </p>
  {mh_warn}
  <table cellpadding="4" cellspacing="0" border="0" width="100%" style="margin-bottom:8px;">
    <tr>
      <td style="font-size:12px;color:#6B7280;width:50%;"><b>Total experience:</b> {c["total_exp"]} &bull; <b>Relevant:</b> {c["relevant_exp"]}</td>
      <td style="font-size:12px;color:#6B7280;"><b>Current role:</b> {c["current_role"]}</td>
    </tr>
  </table>
  <!-- Dimension Score Grid -->
  <table width="100%" border="1" cellpadding="5" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:11px;margin-bottom:10px;">
    <tr>
      <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D1 Funct.<br>25%</th>
      <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D2 Outcomes<br>20%</th>
      <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D3 Environ.<br>15%</th>
      <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D4 Ownership<br>15%</th>
      <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D5 Stakeh.<br>10%</th>
      <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D6 Hard Sk.<br>10%</th>
      <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D7 Growth<br>5%</th>
    </tr>
    <tr>{cell(d1)}{cell(d2)}{cell(d3)}{cell(d4)}{cell(d5)}{cell(d6)}{cell(d7)}</tr>
  </table>
  <!-- USP -->
  <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:8px;">
  <tr><td bgcolor="#F5F3FF" style="background-color:#F5F3FF;border-left:3px solid #7C3AED;border-radius:4px;padding:8px 12px;">
    <p style="margin:0;font-size:12px;color:#374151;"><b style="color:#6B21A8;">&#128161; USP:</b> {c["usp"]}</p>
  </td></tr>
  </table>
  {sig_html}
  {cv_qual_html}
  <p style="margin:8px 0 3px 0;font-size:13px;"><b style="color:#16A34A;">&#10003; Key Strengths:</b></p>
  <ul style="margin:0;padding-left:18px;">{str_items}</ul>
  <p style="margin:8px 0 3px 0;font-size:13px;"><b style="color:#DC2626;">&#9888; Risks / Gaps:</b></p>
  <ul style="margin:0;padding-left:18px;">{risk_items}</ul>
  <p style="margin:8px 0 3px 0;font-size:13px;"><b style="color:#1D4ED8;">&#128172; Interview Questions:</b></p>
  <ol style="margin:0;padding-left:18px;">{q_items}</ol>
  <p style="font-size:11px;color:#6B7280;margin:8px 0 0 0;"><b>Confidence:</b> {c["confidence"]} &bull; <b>Budget:</b> {c["salary"]} {c["budget_gap"]}</p>
</td></tr>
</table>"""

# ── SECTION 4: DEEP COMPARE TOP 3 ───────────────────────────────
html += """
<!-- ══════════════════════════════════════════════════════════════
     SECTION 4: DEEP COMPARATIVE ANALYSIS — TOP 3
═══════════════════════════════════════════════════════════════ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">&#52;&#65039;&#8419; Deep Comparative Analysis &mdash; Top 3 Strongest Candidates</h2>
<p style="font-size:12px;color:#6B7280;margin-bottom:8px;">Danish Hussain (#1) &bull; Zain Ul Abideen (#2) &bull; Mizhgan Kirmani (#3) &mdash; selected regardless of budget.</p>

<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;margin-bottom:16px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:left;width:22%;">Criterion</th>
    <th bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;width:26%;">#1 Danish Hussain<br>97.5 / Tier A</th>
    <th bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;width:26%;">#2 Zain Ul Abideen &#128269;<br>95.0 / Tier A</th>
    <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;width:26%;">#3 Mizhgan Kirmani<br>78.8 / Tier B</th>
  </tr>
  <tr>
    <td style="font-weight:bold;color:#6B21A8;">Experience Depth</td>
    <td style="text-align:center;">20 years &mdash; Head of Grants &amp; Partnerships. Most senior title in pool.</td>
    <td style="text-align:center;">~10 years &mdash; Deputy Manager Resource Mobilisation. Senior individual contributor.</td>
    <td style="text-align:center;">~8 years &mdash; Manager Donor Relations. Mid-senior level.</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td style="font-weight:bold;color:#6B21A8;">Track Record</td>
    <td style="text-align:center;"><b style="color:#16A34A;">PKR 1B+ mobilised</b><br>FCDO, World Bank, UNDP, ADB</td>
    <td style="text-align:center;"><b style="color:#16A34A;">US $50M lifetime</b><br>$8.44M + $4.42M at 2 orgs</td>
    <td style="text-align:center;"><b style="color:#1D4ED8;">PKR 72M / FY</b><br>FCDO, UN Women, UNDP, USAID</td>
  </tr>
  <tr>
    <td style="font-weight:bold;color:#6B21A8;">Organisation Quality</td>
    <td style="text-align:center;">&#127760; International INGO<br>Donor: FCDO, UNDP, ADB</td>
    <td style="text-align:center;">&#127979; READ Foundation &#11088;<br>Donor: UNICEF, UNFPA, British Council</td>
    <td style="text-align:center;">&#127979; TCF &#11088; + Aga Khan Foundation<br>Donor: FCDO, UN Women, USAID</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td style="font-weight:bold;color:#6B21A8;">Org Signal Rating</td>
    <td style="text-align:center;"><span style="background:#EFF6FF;color:#1D4ED8;border-radius:8px;padding:2px 8px;font-size:11px;">🌐 Donor/Development</span></td>
    <td style="text-align:center;"><span style="background:#F0FDF4;color:#166534;border-radius:8px;padding:2px 8px;font-size:11px;">🎓 EdTech + 🌐 Donor</span></td>
    <td style="text-align:center;"><span style="background:#F0FDF4;color:#166534;border-radius:8px;padding:2px 8px;font-size:11px;">🎓 EdTech (TCF) + 🌐 Donor</span></td>
  </tr>
  <tr>
    <td style="font-weight:bold;color:#6B21A8;">CV Quality</td>
    <td style="text-align:center;"><span style="background:#16A34A;color:#fff;border-radius:8px;padding:2px 8px;font-size:11px;">High</span></td>
    <td style="text-align:center;"><span style="background:#16A34A;color:#fff;border-radius:8px;padding:2px 8px;font-size:11px;">High</span></td>
    <td style="text-align:center;"><span style="background:#16A34A;color:#fff;border-radius:8px;padding:2px 8px;font-size:11px;">High</span></td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td style="font-weight:bold;color:#6B21A8;">Location Risk</td>
    <td style="text-align:center;"><span style="background:#FEF3C7;color:#92400E;border-radius:8px;padding:2px 8px;font-size:11px;">&#9888; Hyderabad<br>Willing to relocate</span></td>
    <td style="text-align:center;"><span style="background:#DCFCE7;color:#166534;border-radius:8px;padding:2px 8px;font-size:11px;">&#10003; Islamabad-based</span></td>
    <td style="text-align:center;"><span style="background:#DCFCE7;color:#166534;border-radius:8px;padding:2px 8px;font-size:11px;">&#10003; Islamabad-based</span></td>
  </tr>
  <tr>
    <td style="font-weight:bold;color:#6B21A8;">Budget</td>
    <td style="text-align:center;"><span style="background:#FEE2E2;color:#991B1B;border-radius:8px;padding:2px 8px;font-size:11px;">PKR 550,000<br>Out +280K</span></td>
    <td style="text-align:center;"><span style="background:#FEE2E2;color:#991B1B;border-radius:8px;padding:2px 8px;font-size:11px;">PKR 350,000<br>Out +80K</span></td>
    <td style="text-align:center;"><span style="background:#DCFCE7;color:#166534;border-radius:8px;padding:2px 8px;font-size:11px;">PKR 250,000<br>&#10003; In Budget</span></td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td style="font-weight:bold;color:#6B21A8;">Leadership Potential</td>
    <td style="text-align:center;">Head-level immediately — could lead a team of 3–5 within 12 months.</td>
    <td style="text-align:center;">Senior Manager now. Head of Fundraising in 18–24 months.</td>
    <td style="text-align:center;">Manager level. Senior Manager in 12–18 months with scaled delivery.</td>
  </tr>
  <tr>
    <td style="font-weight:bold;color:#6B21A8;">Recommended Level</td>
    <td style="text-align:center;"><b>Head of Fundraising &amp; Partnerships</b><br>(if salary exception approved)</td>
    <td style="text-align:center;"><b>Senior Fundraising Manager</b><br>(path to Head in 18 months)</td>
    <td style="text-align:center;"><b>Fundraising Manager</b><br>(as posted — exact level match)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td style="font-weight:bold;color:#DC2626;">Key Risk</td>
    <td style="text-align:center;color:#DC2626;">PKR 280K salary gap + relocation confirmation needed before interview.</td>
    <td style="text-align:center;color:#DC2626;">PKR 80K gap + freelance gaps need explanation. Easiest risk to mitigate.</td>
    <td style="text-align:center;color:#DC2626;">Year-1 target scale ($1M+) larger than evidenced track record ($260K FY). Ambition needs validation.</td>
  </tr>
</table>

<table cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td bgcolor="#F5F3FF" style="background-color:#F5F3FF;border-left:5px solid #7C3AED;border-radius:6px;padding:12px 16px;">
<p style="margin:0;font-size:13px;color:#374151;">
<b>Strategic recommendation:</b> If you can approve one budget exception, make it for <b>Zain Ul Abideen</b> first —
PKR 80K gap is the most defensible exception (smallest delta, Islamabad-based, zero relocation risk, US $50M track record).
Simultaneously interview <b>Mizhgan Kirmani</b> at no budget cost.
If both proceed, interview Danish only after getting leadership sign-off on a PKR 400–450K total package (base + performance) —
he is the highest-ceiling hire in the pool but requires a structural salary conversation first.
</p>
</td></tr>
</table>
"""

# ── SECTION 5: STRONG MATCH BUT OUT OF BUDGET ───────────────────
html += """
<!-- ══════════════════════════════════════════════════════════════
     SECTION 5: STRONG MATCH BUT OUT OF BUDGET
═══════════════════════════════════════════════════════════════ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">&#53;&#65039;&#8419; Strong Match but Out of Budget</h2>

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

# ── SECTION 6: VISUAL ANALYTICS ─────────────────────────────────
html += """
<!-- ══════════════════════════════════════════════════════════════
     SECTION 6: VISUAL ANALYTICS
═══════════════════════════════════════════════════════════════ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">&#54;&#65039;&#8419; Visual Analytics</h2>

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

# ── SECTION 7: WHY OTHERS DIDN'T MAKE IT ────────────────────────
html += """
<!-- ══════════════════════════════════════════════════════════════
     SECTION 7: WHY OTHERS DID NOT MAKE IT
═══════════════════════════════════════════════════════════════ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">&#55;&#65039;&#8419; Why Others Did Not Make the Shortlist</h2>
<p style="font-size:12px;color:#6B7280;margin-bottom:12px;">Grouped by primary disqualifying reason. Every candidate was reviewed in full &mdash; these decisions reflect JD evidence, not assumptions.</p>

<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;width:35%;">Reason</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;width:10%;">Count</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Candidates</th>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">Development sector adjacent &mdash; no fundraising acquisition ownership</b><br><span style="font-size:11px;color:#6B7280;">Programme delivery, M&amp;E, reporting, and compliance roles were confused with fundraising in applications. Managing existing grants &ne; acquiring new funding.</span></td>
    <td style="text-align:center;font-weight:bold;">6</td>
    <td style="font-size:11px;">Faheem Baig (programme implementation) &bull; Hamdan Ahmad (World Bank programme management) &bull; Mushahid Hussain (donor reporting, not acquisition) &bull; Shakir Manzoor (supporting role) &bull; Abdul Salam (WASH delivery) &bull; Ahad Ahsan Khan (grants compliance)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#DC2626;">Completely unrelated professional background</b><br><span style="font-size:11px;color:#6B7280;">These candidates bring genuine skills in their fields but none of their experience maps to institutional donor fundraising.</span></td>
    <td style="text-align:center;font-weight:bold;">15</td>
    <td style="font-size:11px;">Sheraz Khan (Microsoft licensing) &bull; Muhammad Taqi (SaaS sales) &bull; Sameen Amjad Ali (marketing/comms) &bull; Hasan Shahid (digital marketing) &bull; Moeen Hassan (AutoCAD/real estate) &bull; Sani Muhammad (IT ops) &bull; Muhammad Akmal (admin) &bull; Arooj Irfan (clinical psychologist) &bull; Aqsa Gul (customer service) &bull; Laveeza Shah (HR) &bull; Asim Ur Rehman (rural volunteer) &bull; Muhammad Sumraiz Kundi (telecom sales) &bull; Muhammad Ali Zafar (research intern) &bull; Zainab (early-career HR) &bull; Syeda Kainat (M&amp;E/comms)</td>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">Wrong sector or geography &mdash; no Pakistan donor network</b><br><span style="font-size:11px;color:#6B7280;">Skills may be strong but the donor relationships and landscape knowledge required for this role are Pakistan-specific and were absent.</span></td>
    <td style="text-align:center;font-weight:bold;">5</td>
    <td style="font-size:11px;">Fahad Khan (hospital charity fundraising) &bull; Mahnoor Mellu (SaaS partnerships) &bull; Imran Haider (education policy, not BD) &bull; Anita Kanwal (digital charity campaigns, UK-based) &bull; Ahmed Al-Mayadeen (MENA-based, no Pakistan donor knowledge &mdash; deal-breaker combination)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#DC2626;">No evidence of impact ownership &mdash; activity without outcomes</b><br><span style="font-size:11px;color:#6B7280;">These candidates have worked in relevant organisations but could not evidence direct ownership of fundraising results. Supporting a team that raises money is not the same as personally mobilising it.</span></td>
    <td style="text-align:center;font-weight:bold;">4</td>
    <td style="font-size:11px;">Muhammad Usman (18 years, zero quantified outcomes) &bull; Arsim Tariq (M&amp;E lead on funded projects, not the funder-acquisition owner) &bull; Zubair Hussain (field specialist, salary anomaly) &bull; Bareera Rauf (researcher, not fundraiser)</td>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">Junior profile vs required seniority</b><br><span style="font-size:11px;color:#6B7280;">These candidates show genuine interest in fundraising but do not yet have the depth or deal-closing record needed for a Year-1 $500K&ndash;$1M+ mandate.</span></td>
    <td style="text-align:center;font-weight:bold;">4</td>
    <td style="font-size:11px;">Mushahid Hussain (4 years, supporting role) &bull; Samana Qaseem (alumni admin background) &bull; Muhammad Ali Zafar (research intern) &bull; Zainab (early-career generalist)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#6B7280;">No resume submitted / data gaps</b></td>
    <td style="text-align:center;font-weight:bold;">9</td>
    <td style="font-size:11px;">Apps 1332, 1336, 1348, 1350, 1366, 1372, 1386, 1407, 1515 &mdash; LinkedIn Quick Apply with no CV attached. Cannot be assessed.</td>
  </tr>
  <tr>
    <td><b style="color:#6B7280;">Excluded (junk / duplicate)</b></td>
    <td style="text-align:center;font-weight:bold;">2</td>
    <td style="font-size:11px;">AAMIR SOHAIL (1393) &mdash; salary entered as &ldquo;1&rdquo;, junk entry &bull; Danish Hussain (1347) &mdash; duplicate of application 1346</td>
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
  Taleemabad Talent Acquisition Agent &bull; Screening Report v8 &bull; Updated Framework (12-step + Org Signal + CV Quality + USP) &bull; 2026-03-04 &bull; Confidential
</p>
</body></html>"""

# ══════════════════════════════════════════════════════════════════
# SEND EMAIL — multipart/related with CID inline images
# Structure: related > alternative > text/html  +  image/png × 2
# ══════════════════════════════════════════════════════════════════
msg = MIMEMultipart("related")
msg["Subject"] = "Screening Report v8 — Fundraising & Partnerships Manager — Job 32"
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
        safe_sendmail(server, SENDER, RECIPIENT, msg.as_string(), context='send_job32_report_v8')

print("Email sent — CID inline charts embedded in email body.")
