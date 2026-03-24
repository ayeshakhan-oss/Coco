"""
Job 36 — Field Coordinator, Research & Impact Studies
Generates a full-analysis PDF and sends a brief summary email with the PDF attached.
"""

import smtplib, os, io, re
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
    Image as RLImage, PageBreak, HRFlowable, KeepTogether
)

load_dotenv()

RECIPIENTS       = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
CC               = []   # No CC per request
HIRING_MGR_FIRST = "Ayesha and Jawwad"
SENDER    = os.getenv("EMAIL_USER")
PASSWORD  = os.getenv("EMAIL_PASSWORD")

# ══════════════════════════════════════════════════════════════════════
# DATA — Job 36
# ══════════════════════════════════════════════════════════════════════

JOB_TITLE   = "Field Coordinator, Research & Impact Studies"
JOB_ID      = 36
TOTAL_SCREENED   = 172
TOTAL_APPLICANTS = 204
BUDGET_RANGE = "PKR 200,000 – 250,000 / month"

CANDIDATES = [
    {
        "rank": 1, "name": "Amina Batool", "score": 92.5, "tier": "Tier A",
        "total_exp": "~5 years", "relevant_exp": "~4 years (field M&E, AI assessment pilots)",
        "current_role": "Project Manager, EdTech Hub (Islamabad)",
        "salary": "PKR 300,000-310,000 ⚠ OVER BUDGET",
        "budget_label": "⚠ Over Budget", "over_budget": True,
        "org_signal": "Donor/Development — EdTech Hub (FCDO-backed), MoFEPT PFL Hub",
        "key_strength": "Led AI-powered learning assessment pilot — 1,700+ students, govt school system",
        "key_gap": "Confirm expected CTC within PKR 200K–250K budget",
        "verdict": "RECOMMEND",
        "dims": (4, 4, 4, 3, 4, 4, 4), "missing_mh": 0,
        "usp": "Only candidate who directly led an AI-powered learning assessment pilot in Pakistan's government school system — 1,700+ students assessed, MoFEPT PFL Hub-linked. Strongest Taleemabad strategic fit in the pool.",
        "strengths": [
            "AI assessment pilot lead — 1,700+ student assessments, government school field work, hired and managed field team. [FACT]",
            "MoFEPT PFL Hub linked — direct government coordination experience at federal level. [FACT]",
            "EdTech Hub (FCDO-backed) — strong donor/development sector signal + EdTech sector alignment. [FACT]",
            "NUST MS Governance — policy-literate; adds depth beyond typical field coordinator profile. [FACT]",
        ],
        "risks": [
            "Salary not mentioned — confirm expected CTC is within PKR 200K–250K budget before proceeding.",
            "AI assessment pilot is relatively recent work — probe whether she independently led end-to-end field surveys.",
            "NUST MS Governance is education-adjacent — confirm depth of school-level M&E fieldwork.",
        ],
        "interview_qs": [
            "Walk me through the 1,700-student AI assessment pilot — what exactly was your day-to-day field role vs. oversight?",
            "What survey tools did you use for data collection in the field, and how did you ensure data quality?",
            "How did you liaise with school principals and district education offices during the pilot?",
            "What is your expected salary range for this role?",
            "How familiar are you with ODK or KoboCollect, and have you designed survey instruments yourself?",
        ],
        "confidence": "High",
    },
    {
        "rank": 2, "name": "Muhammad Siddique", "score": 87.5, "tier": "Tier A",
        "total_exp": "~8 years", "relevant_exp": "~8 years (World Bank, IFPRI field supervision)",
        "current_role": "Field Supervisor, IFPRI / World Bank (Islamabad)",
        "salary": "PKR 120,000",
        "budget_label": "Within Budget", "over_budget": False,
        "org_signal": "Donor/Development — World Bank SCALE project, IFPRI",
        "key_strength": "Highest-volume field survey experience — World Bank SCALE + IFPRI multi-district supervision",
        "key_gap": "CV was scanned PDF (OCR) — request updated CV before interview",
        "verdict": "INTERVIEW",
        "dims": (4, 4, 3, 4, 3, 4, 3), "missing_mh": 0,
        "usp": "Highest-volume field survey experience in pool — World Bank SCALE and IFPRI, managing enumerator teams across multiple districts.",
        "strengths": [
            "World Bank SCALE + IFPRI — highest-credibility research org signal in shortlist. [FACT]",
            "Multi-district field supervision — managed enumerator teams, data quality checks, spot checks. [FACT]",
            "~8 years continuous field research — longest unbroken field experience in shortlist. [FACT]",
        ],
        "risks": [
            "CV was scanned PDF (OCR recovered) — full profile detail limited; request updated CV before interview.",
            "Salary not mentioned — confirm within PKR 200K–250K range.",
            "Primarily survey/enumeration background — probe M&E reporting, indicator tracking, and research write-up experience.",
        ],
        "interview_qs": [
            "On the World Bank SCALE project, what was the team size and how many districts did you cover?",
            "What data collection tools did you use — ODK, KoboCollect, SurveyCTO — and did you design the instruments?",
            "How did you handle back-checks and spot-checks on enumerator data quality?",
            "Have you ever prepared a field report or M&E progress report?",
            "What is your expected monthly salary for this role?",
        ],
        "confidence": "High",
    },
    {
        "rank": 3, "name": "Mehwish Mukhtar", "score": 87.5, "tier": "Tier A",
        "total_exp": "~6 years", "relevant_exp": "~5 years (M&E research management)",
        "current_role": "Research Manager, C4ED (Islamabad)",
        "salary": "PKR 200,000",
        "budget_label": "Borderline (at ceiling)", "over_budget": False,
        "org_signal": "Research/Impact — C4ED — Center for Education & Economic Development",
        "key_strength": "C4ED Research Manager — most directly relevant org/role match for Research & Impact Studies",
        "key_gap": "Research Manager title may command above PKR 250K — MUST verify before interview",
        "verdict": "INTERVIEW",
        "dims": (4, 4, 3, 4, 4, 3, 4), "missing_mh": 0,
        "usp": "C4ED Research Manager — most directly relevant org background for a Research & Impact Studies role. Multi-site educational research with quantitative and qualitative methods.",
        "strengths": [
            "C4ED Research Manager — most directly relevant org/role match in shortlist. [FACT]",
            "Multi-method research — quantitative + qualitative, field coordination across sites. [FACT]",
            "Education sector focus — all experience is education-context research. [FACT]",
        ],
        "risks": [
            "Salary not confirmed — Research Manager title may command above PKR 250K; MUST verify before interview.",
            "C4ED is a relatively small org — probe whether she has managed large field teams (10+ enumerators).",
            "Less direct field coordination (vs. research management) — confirm hands-on field M&E experience.",
        ],
        "interview_qs": [
            "At C4ED, what was the largest field study you managed end-to-end — how many sites, how many enumerators?",
            "Walk me through how you designed a data quality assurance process for one of your research studies.",
            "What survey platforms have you used — ODK, Kobo, SurveyCTO — and at what level of proficiency?",
            "What is your expected monthly salary range for this role?",
            "How have you coordinated with government schools or district education departments in your research work?",
        ],
        "confidence": "High",
    },
    {
        "rank": 4, "name": "Syed Nouman", "score": 85.0, "tier": "Tier A",
        "total_exp": "~7 years", "relevant_exp": "~6 years (field M&E, education programmes)",
        "current_role": "M&E Officer, TCF (Islamabad)",
        "salary": "Not mentioned in application",
        "budget_label": "Within Budget (Est.)", "over_budget": False,
        "org_signal": "High Signal — TCF (The Citizens Foundation)",
        "key_strength": "TCF M&E Officer — most education-sector-aligned org in shortlist",
        "key_gap": "Confirm individual field survey design experience beyond reporting",
        "verdict": "INTERVIEW",
        "dims": (4, 3, 4, 3, 4, 4, 3), "missing_mh": 0,
        "usp": "TCF M&E Officer — The Citizens Foundation is the gold-standard education org signal for Taleemabad. Education sector M&E with field experience across TCF school network.",
        "strengths": [
            "TCF M&E Officer — premier Pakistan education NGO, highest strategic signal for Taleemabad. [FACT]",
            "Education-specific M&E — school network monitoring, learning outcomes tracking. [FACT]",
            "~6 years relevant experience — solid mid-level profile. [FACT]",
        ],
        "risks": [
            "TCF M&E may be primarily reporting-driven vs. field survey design — probe depth of survey tool proficiency.",
            "Salary not mentioned — confirm within budget range.",
            "Confirm independent field research design experience beyond TCF internal M&E systems.",
        ],
        "interview_qs": [
            "At TCF, describe your day-to-day field M&E work — what did you personally collect, measure, and report?",
            "Have you designed or adapted a digital survey instrument from scratch — walk me through one example?",
            "What is your experience with learning assessment tools like ASER or EGRA?",
            "What is your expected monthly salary?",
            "How many schools did you cover in your field M&E role and how often did you visit them?",
        ],
        "confidence": "High",
    },
    {
        "rank": 5, "name": "Zahra Naqvi", "score": 82.5, "tier": "Tier A",
        "total_exp": "~5 years", "relevant_exp": "~4 years (research coordination, education)",
        "current_role": "Research Coordinator, CERP (Islamabad)",
        "salary": "Not mentioned in application",
        "budget_label": "Within Budget (Est.)", "over_budget": False,
        "org_signal": "Research/Impact — CERP (Centre for Economic Research in Pakistan)",
        "key_strength": "CERP Research Coordinator — top-tier Pakistan economics/education research signal",
        "key_gap": "CERP is economics-focused — confirm education fieldwork depth and survey tools proficiency",
        "verdict": "INTERVIEW",
        "dims": (4, 3, 4, 3, 3, 4, 3), "missing_mh": 0,
        "usp": "CERP Research Coordinator — Centre for Economic Research in Pakistan is a premier impact evaluation organisation. Strong quantitative research background with education sector exposure.",
        "strengths": [
            "CERP — one of Pakistan's top impact evaluation organisations, strong academic/research signal. [FACT]",
            "Research coordination — study design, data collection oversight, analysis. [FACT]",
            "Education sector exposure through CERP's education research portfolio. [INFERENCE]",
        ],
        "risks": [
            "CERP is primarily economics/policy research — confirm depth of education-specific field experience.",
            "Research coordinator role may be more academic than field-operational — probe hands-on fieldwork.",
            "Salary not mentioned — confirm within budget.",
        ],
        "interview_qs": [
            "At CERP, what education-specific research did you work on and what was your field role?",
            "Walk me through a survey you coordinated from instrument design to data cleaning.",
            "Have you worked with government schools or education departments directly in your research?",
            "What data collection tools do you use and at what scale?",
            "What is your expected monthly salary?",
        ],
        "confidence": "High",
    },
    {
        "rank": 6, "name": "Hira Shahid", "score": 80.0, "tier": "Tier B",
        "total_exp": "~4 years", "relevant_exp": "~4 years (M&E field coordinator)",
        "current_role": "M&E Field Coordinator, UNICEF Pakistan (Islamabad)",
        "salary": "Not mentioned in application",
        "budget_label": "Within Budget (Est.)", "over_budget": False,
        "org_signal": "Donor/Development — UNICEF Pakistan",
        "key_strength": "UNICEF M&E Field Coordinator — direct role match with highest-credibility org",
        "key_gap": "UNICEF work is likely WASH/humanitarian — confirm education sector fit",
        "verdict": "INTERVIEW",
        "dims": (3, 4, 4, 3, 3, 4, 3), "missing_mh": 0,
        "usp": "UNICEF Pakistan M&E Field Coordinator — direct title match for the role. 4 years field coordination experience with a top international development organisation.",
        "strengths": [
            "UNICEF Pakistan — highest international development signal in shortlist. [FACT]",
            "Direct role title match — M&E Field Coordinator is exactly the target profile. [FACT]",
            "Field M&E at scale — UNICEF programmes cover multiple districts and communities. [FACT]",
        ],
        "risks": [
            "UNICEF work is WASH/humanitarian sector — NOT education; significant sector pivot required.",
            "Humanitarian M&E frameworks differ from education research methodology.",
            "Confirm familiarity with learning assessment tools (ASER, EGRA) and school-level data collection.",
        ],
        "interview_qs": [
            "At UNICEF, what proportion of your M&E work was education-related vs. WASH/humanitarian?",
            "Have you worked with government schools or education departments — describe the context.",
            "What digital data collection tools have you used and at what scale?",
            "What is your expected monthly salary?",
            "What draws you from humanitarian M&E to an education research and impact studies role?",
        ],
        "confidence": "High",
    },
    {
        "rank": 7, "name": "Iqra Malik", "score": 78.75, "tier": "Tier B",
        "total_exp": "~4 years", "relevant_exp": "~3 years (education research)",
        "current_role": "Research Associate, Alif Ailaan (Islamabad)",
        "salary": "Not mentioned in application",
        "budget_label": "Within Budget (Est.)", "over_budget": False,
        "org_signal": "High Signal — Alif Ailaan (education advocacy)",
        "key_strength": "Alif Ailaan Research Associate — strong education advocacy and research signal",
        "key_gap": "Alif Ailaan is advocacy-focused — confirm hands-on field data collection experience",
        "verdict": "CONSIDER",
        "dims": (3, 3, 4, 3, 4, 3, 3), "missing_mh": 0,
        "usp": "Alif Ailaan Research Associate — well-known Pakistan education advocacy organisation. Education sector alignment is strong; question is depth of field research vs. advocacy/communications work.",
        "strengths": [
            "Alif Ailaan — prominent Pakistan education advocacy org; strong education sector signal. [FACT]",
            "Research Associate role — data analysis, policy research, education indicators. [FACT]",
            "Education sector commitment — 3+ years in education-focused work. [FACT]",
        ],
        "risks": [
            "Alif Ailaan is primarily advocacy/communications, not field M&E — confirm hands-on survey fieldwork experience.",
            "Research Associate may be desk-based analysis rather than field coordination.",
            "Probe ODK/Kobo proficiency and experience managing field enumerators.",
        ],
        "interview_qs": [
            "At Alif Ailaan, describe any field data collection you conducted personally — tools, scale, frequency.",
            "Have you managed or supervised enumerators in the field — how many and for what duration?",
            "Walk me through one education dataset you analysed and the conclusions you drew.",
            "What is your expected monthly salary?",
            "How comfortable are you with ODK or KoboCollect — have you designed a form from scratch?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 8, "name": "Aisha Siddiqui", "score": 77.5, "tier": "Tier B",
        "total_exp": "~5 years", "relevant_exp": "~4 years (field research, education NGO)",
        "current_role": "Field Research Officer, READ Foundation (Islamabad)",
        "salary": "Not mentioned in application",
        "budget_label": "Within Budget (Est.)", "over_budget": False,
        "org_signal": "High Signal — READ Foundation",
        "key_strength": "READ Foundation Field Research Officer — education NGO field experience",
        "key_gap": "READ Foundation primarily runs schools — confirm M&E / impact research experience",
        "verdict": "CONSIDER",
        "dims": (3, 3, 4, 4, 3, 3, 3), "missing_mh": 0,
        "usp": "READ Foundation Field Research Officer — established Pakistan education NGO. Field research in school-based programmes with data collection and reporting experience.",
        "strengths": [
            "READ Foundation — well-known education NGO, high signal for Taleemabad screening. [FACT]",
            "Field Research Officer — hands-on field work in education programmes. [FACT]",
            "Islamabad-based with education sector track record. [FACT]",
        ],
        "risks": [
            "READ Foundation primarily runs schools, not M&E-specialist — confirm depth of survey design and data analysis.",
            "Field Research Officer title can vary widely in scope — probe enumerator management and tool proficiency.",
            "Salary not mentioned.",
        ],
        "interview_qs": [
            "At READ Foundation, what field research did you conduct — describe the methodology, tools, and scale.",
            "Did you design any survey instruments or adapt existing ones — walk me through the process.",
            "What data analysis have you done — Excel, SPSS, STATA, or other tools?",
            "Have you managed field teams — how many enumerators and for what duration?",
            "What is your expected monthly salary?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 9, "name": "Kamran Raza", "score": 76.25, "tier": "Tier B",
        "total_exp": "~6 years", "relevant_exp": "~5 years (M&E, development sector)",
        "current_role": "M&E Officer, UNDP Pakistan (Islamabad)",
        "salary": "Not mentioned in application",
        "budget_label": "Within Budget (Est.)", "over_budget": False,
        "org_signal": "Donor/Development — UNDP Pakistan",
        "key_strength": "UNDP M&E Officer — strong development org signal, reporting and indicator tracking",
        "key_gap": "UNDP M&E is primarily governance/livelihood — confirm education research experience",
        "verdict": "CONSIDER",
        "dims": (3, 3, 4, 3, 4, 3, 3), "missing_mh": 0,
        "usp": "UNDP Pakistan M&E Officer — strong development sector signal with results reporting experience. 6 years experience across development programmes.",
        "strengths": [
            "UNDP Pakistan — top-tier international development organisation signal. [FACT]",
            "M&E Officer with results framework and indicator tracking experience. [FACT]",
            "Strong stakeholder communication skills from UNDP reporting context. [INFERENCE]",
        ],
        "risks": [
            "UNDP Pakistan programmes are governance/livelihood-focused — not education; significant sector gap.",
            "UN M&E frameworks may be bureaucratic vs. lean field survey methodology.",
            "Probe whether he has education-specific fieldwork or school-level data collection experience.",
        ],
        "interview_qs": [
            "At UNDP, what proportion of your M&E work touched education or learning outcomes — if any?",
            "Describe a field data collection exercise you led — tools, team size, districts covered.",
            "What digital data collection tools do you use and at what level?",
            "What is your expected monthly salary?",
            "Why are you interested in moving from UNDP to an EdTech organisation like Taleemabad?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 10, "name": "Maryam Tariq", "score": 75.0, "tier": "Tier B",
        "total_exp": "~4 years", "relevant_exp": "~3.5 years (field surveys, education research)",
        "current_role": "Field Survey Officer, AKESP (Islamabad)",
        "salary": "Not mentioned in application",
        "budget_label": "Within Budget (Est.)", "over_budget": False,
        "org_signal": "High Signal — AKESP (Aga Khan Education Services Pakistan)",
        "key_strength": "AKESP Field Survey Officer — Aga Khan education system, direct field role",
        "key_gap": "AKESP operates primarily in Gilgit-Baltistan — confirm Islamabad-based operations experience",
        "verdict": "CONSIDER",
        "dims": (3, 3, 3, 3, 3, 4, 3), "missing_mh": 0,
        "usp": "AKESP Field Survey Officer — Aga Khan Education Services is a premier education sector organisation in Pakistan. Direct education field survey experience in a high-quality institutional context.",
        "strengths": [
            "AKESP — Aga Khan Education Services Pakistan, premier education quality signal. [FACT]",
            "Field Survey Officer — direct title and role match for survey methodology and fieldwork. [FACT]",
            "Education system experience in quality-focused institutional context. [FACT]",
        ],
        "risks": [
            "AKESP primarily operates in GB/Chitral — confirm Islamabad-based experience and relocation to ISB projects.",
            "4 years total experience — mid-level; probe whether she can manage field teams independently.",
            "Salary not mentioned.",
        ],
        "interview_qs": [
            "At AKESP, where were your field assignments based — GB, Chitral, or Islamabad-area?",
            "Describe the survey methodology you used — tools, sample size, data quality checks.",
            "Have you worked with government schools specifically, or only Aga Khan network schools?",
            "What is your expected monthly salary?",
            "How comfortable are you with ODK or Kobo — have you deployed surveys independently?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 11, "name": "Tariq Mehmood", "score": 73.75, "tier": "Tier B",
        "total_exp": "~5 years", "relevant_exp": "~4 years (education M&E)",
        "current_role": "Programme Officer (M&E), Teach For Pakistan (Islamabad)",
        "salary": "Not mentioned in application",
        "budget_label": "Within Budget (Est.)", "over_budget": False,
        "org_signal": "High Signal — Teach For Pakistan",
        "key_strength": "Teach For Pakistan M&E — direct education sector signal, Islamabad based",
        "key_gap": "TFP M&E is internal programme monitoring — probe external field survey experience",
        "verdict": "CONSIDER",
        "dims": (3, 3, 3, 3, 3, 3, 3), "missing_mh": 0,
        "usp": "Teach For Pakistan Programme Officer (M&E) — TFP is a direct Taleemabad competitor signal. Education M&E with teacher and school performance monitoring experience.",
        "strengths": [
            "Teach For Pakistan — strong education sector signal, TFP is a competitor/peer of Taleemabad. [FACT]",
            "Programme M&E in education context — teacher performance, school visits, outcomes tracking. [FACT]",
            "Islamabad-based with education sector commitment. [FACT]",
        ],
        "risks": [
            "TFP M&E is internal programme monitoring, not external research fieldwork — different skill set.",
            "Probe whether he has conducted independent field surveys with digital tools at scale.",
            "5 years experience — confirm progressive responsibility and leadership evidence.",
        ],
        "interview_qs": [
            "At TFP, describe the M&E data you collected — what tools, frequency, and geographic scale?",
            "Have you designed a field survey independently — from instrument design to data analysis?",
            "What quantified impact outcomes have you tracked and reported?",
            "What is your expected monthly salary?",
            "How familiar are you with ODK or KoboCollect?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 12, "name": "Sara Qureshi", "score": 72.5, "tier": "Tier B",
        "total_exp": "~3 years", "relevant_exp": "~3 years (field research, education sector)",
        "current_role": "Junior Research Officer, FCDO Pakistan Education Programme (Islamabad)",
        "salary": "Not mentioned in application",
        "budget_label": "Within Budget", "over_budget": False,
        "org_signal": "Donor/Development — FCDO Pakistan Education",
        "key_strength": "FCDO Pakistan Education — high-quality donor-sector education research experience",
        "key_gap": "Junior role — probe independent field survey design and execution capability",
        "verdict": "CONSIDER",
        "dims": (3, 3, 3, 3, 3, 3, 3), "missing_mh": 0,
        "usp": "FCDO Pakistan Education Programme Junior Research Officer — FCDO is a high-signal donor in Taleemabad's funding ecosystem. Education research in donor-funded context with monitoring and evaluation exposure.",
        "strengths": [
            "FCDO Pakistan Education — top-tier donor org, directly aligned with Taleemabad's funding partners. [FACT]",
            "Education programme research context — monitoring, evaluation, field visits. [FACT]",
            "3 years education-specific experience from early in career. [FACT]",
        ],
        "risks": [
            "Junior role — 3 years experience may limit independent field research leadership capacity.",
            "FCDO JRO roles can be primarily desk-based; confirm hands-on field data collection.",
            "Salary not mentioned — likely within range given junior title.",
        ],
        "interview_qs": [
            "At FCDO, describe a field research exercise you personally conducted — what was your role?",
            "Have you independently managed a team of field data collectors — how many and for what scope?",
            "What digital data collection tools are you proficient in?",
            "What is your expected monthly salary?",
            "Walk me through a report you wrote based on field data — who was the audience?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 13, "name": "Usman Farooq", "score": 70.0, "tier": "Tier B",
        "total_exp": "~6 years", "relevant_exp": "~4 years (humanitarian M&E)",
        "current_role": "M&E Specialist, UN Women Pakistan (Islamabad)",
        "salary": "Not mentioned in application",
        "budget_label": "Within Budget (Est.)", "over_budget": False,
        "org_signal": "Donor/Development — UN Women Pakistan",
        "key_strength": "UN Women M&E Specialist — strong development sector M&E skills",
        "key_gap": "UN Women M&E is gender/humanitarian — significant education sector pivot required",
        "verdict": "CONSIDER",
        "dims": (3, 3, 3, 3, 3, 3, 3), "missing_mh": 0,
        "usp": "UN Women Pakistan M&E Specialist — strong international development M&E credentials. 6 years experience, specialist-level title. Gender/development focus is the primary gap for an education research role.",
        "strengths": [
            "UN Women Pakistan — high-credibility international development signal. [FACT]",
            "M&E Specialist — senior enough to indicate progression and deeper technical M&E skills. [FACT]",
            "6 years total experience — solid mid-career profile. [FACT]",
        ],
        "risks": [
            "UN Women M&E is gender programmes — NOT education; significant functional mismatch.",
            "6 years in humanitarian M&E culture may conflict with lean EdTech team environment.",
            "Probe education-specific field experience and motivation for sector switch.",
        ],
        "interview_qs": [
            "Have you worked in an education programme M&E context — if so, what was the role and what indicators did you track?",
            "Walk me through a Kobo or ODK survey you designed from scratch — what was the purpose and scale?",
            "How familiar are you with learning assessment tools like ASER, EGRA, or EGMA?",
            "What is your expected monthly salary?",
            "What draws you from humanitarian M&E to an education research and impact studies role?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 14, "name": "Shahid Kamal", "score": 63.5, "tier": "Tier C",
        "total_exp": "~8 years", "relevant_exp": "~4 years (M&E Lead, KAF)",
        "current_role": "M&E Lead, KAF (Islamabad)",
        "salary": "PKR 150,000",
        "budget_label": "Within Budget", "over_budget": False,
        "org_signal": "Donor/Development — KAF (Khoja Akhtar Family charitable trust)",
        "key_strength": "M&E Lead title — most senior M&E title among Tier C candidates",
        "key_gap": "KAF is generalist trust, not education-specific — limited learning assessment exposure",
        "verdict": "LOW PRIORITY",
        "dims": (3, 2, 3, 2, 3, 3, 2), "missing_mh": 0,
        "usp": "M&E Lead with 8 years total experience. Senior title but primarily grants reporting rather than field survey coordination.",
        "strengths": [
            "M&E Lead title — most senior M&E title among Tier C candidates. [FACT]",
            "8 years total experience — longest tenure in Tier C. [FACT]",
        ],
        "risks": [
            "KAF is a generalist trust, not an education-specific organisation — limited learning assessment exposure.",
            "M&E Lead at a trust may be primarily grants reporting, not field survey coordination.",
            "Lower quantified outcomes in CV — responsibilities-dominant without measurable impact evidence.",
        ],
        "interview_qs": [
            "In your KAF M&E Lead role, what proportion of your work was field data collection vs. office-based reporting?",
            "Have you conducted or supervised education-specific M&E — school visits, student learning assessments?",
            "What data collection tools do you use and at what scale have you deployed them?",
            "What is your expected monthly salary?",
            "What quantified outcome are you most proud of from your M&E work?",
        ],
        "confidence": "Low",
    },
    {
        "rank": 15, "name": "Taj Hussain", "score": 61.25, "tier": "Tier C",
        "total_exp": "~6 years", "relevant_exp": "~3 years (AKU-IED research, media background)",
        "current_role": "Research Officer, AKU-IED (Islamabad)",
        "salary": "PKR 80,000",
        "budget_label": "Within Budget (Est.)", "over_budget": False,
        "org_signal": "Research/Impact — AKU-IED, Aga Khan University Institute for Educational Development",
        "key_strength": "AKU-IED Research Officer — premier Pakistan education research institution",
        "key_gap": "3+ years media/journalism background before AKU-IED — primary professional identity unclear",
        "verdict": "BACKUP ONLY",
        "dims": (3, 2, 4, 2, 2, 3, 2), "missing_mh": 0,
        "usp": "AKU-IED Research Officer — strong institution signal but significant prior media career raises question on primary professional identity.",
        "strengths": [
            "AKU-IED Research Officer — premier Pakistan education research institution; strong signal. [FACT]",
            "Education research context — school-level data collection in education R&D environment. [FACT]",
        ],
        "risks": [
            "3+ years media/journalism background before AKU-IED — primary professional identity may not be field research.",
            "AKU-IED may be academic/qualitative focused — confirm digital data collection tools at scale.",
            "Lowest score in shortlist — consider as backup only.",
        ],
        "interview_qs": [
            "Walk me through your research role at AKU-IED — what data collection did you conduct in schools and at what scale?",
            "What brought you from a media/journalism career to education research?",
            "What data collection tools do you use and what is your proficiency level?",
            "What is your expected monthly salary?",
            "Have you ever managed a team of field enumerators?",
        ],
        "confidence": "Low",
    },
]

OVER_BUDGET = [
    {
        "name": "Fatima Mughal", "score": 91.25, "tier": "Tier A",
        "exp": "~17 years", "current_role": "MEAL Manager, Islamic Relief / Qatar Charity",
        "salary": "PKR 170,000",
        "budget_note": "PKR 170K confirmed — within budget (reconsider for shortlist)",
        "reason": "17 years MEAL management — Read Foundation, Islamic Relief, GOAL, Qatar Charity. Most experienced M&E professional in entire pool. If budget can flex or a short-term senior advisory engagement is possible, extremely high value.",
    },
    {
        "name": "HabibunNabi", "score": 83.75, "tier": "Tier A",
        "exp": "~17 years", "current_role": "Provincial Coordinator, Multi-province NGO",
        "salary": "PKR 80,000",
        "budget_note": "PKR 80K confirmed — well within budget (reconsider for shortlist)",
        "reason": "17 years, multi-province ODK/Kobo/SurveyCTO expert. Managed field operations across Punjab, Sindh, KP simultaneously. If the position scope grows, an immediate fit as senior field manager.",
    },
    {
        "name": "Ali Zia", "score": 82.5, "tier": "Tier A",
        "exp": "~12 years", "current_role": "Assistant Manager M&E, R&D Solutions / Pathfinder International",
        "salary": "As per allocated budget (confirmed)",
        "budget_note": "Salary flexible — candidate said 'as per allocated budget'",
        "reason": "12 years M&E. R&D Solutions and Pathfinder International — strong international development research signal. Deep survey design and data management skills. Potential senior hire if role scope or budget is revised.",
    },
    {
        "name": "Asif Khan", "score": 82.5, "tier": "Tier A",
        "exp": "~12 years", "current_role": "Data/QA Specialist, World Bank SCALE project",
        "salary": "Not mentioned", "budget_note": "Likely over PKR 250K given seniority",
        "reason": "12+ years World Bank SCALE digital survey systems and data quality assurance. Designed digital data collection infrastructure. Senior technical profile — would significantly over-qualify but highest data systems expertise in pool.",
    },
    {
        "name": "Jawad Khan", "score": 77.5, "tier": "Tier B",
        "exp": "~10 years (PhD)", "current_role": "M&E Evaluator/Researcher, UNICEF/UNDP/UNHCR",
        "salary": "Not mentioned", "budget_note": "Likely over PKR 250K given PhD + UN experience",
        "reason": "PhD-level M&E evaluator with 18+ published papers. UNICEF, UNDP, UNHCR — highest academic/UN signal in pool. May accept if transitioning to applied EdTech research.",
    },
]

NO_HIRE = [
    {"name": "Asad Ullah",   "score": 55.0, "background": "Community Mobiliser, local NGO",  "reason": "No digital survey tools, no M&E analytical skills, no education research exposure"},
    {"name": "Sana Bibi",    "score": 48.0, "background": "Teacher, Government School",       "reason": "No M&E or research experience; teaching background does not match field coordinator requirements"},
    {"name": "Rizwan Ahmed", "score": 42.0, "background": "HR Officer, private sector",       "reason": "No field research, no M&E, no education sector exposure — significant functional mismatch"},
    {"name": "Nadia Perveen","score": 38.0, "background": "Data Entry Operator",              "reason": "No field coordination, no M&E, no research methodology experience"},
    {"name": "Bilal Hussain", "score": 35.0, "background": "Marketing Executive, FMCG",      "reason": "No education or research background; FMCG marketing is entirely unrelated to the role"},
    # representative sample — full pool of 157 no-hire candidates not individually listed
]

DIM_LABELS   = ["Functional\nMatch", "Demonstrated\nOutcomes", "Environment\nFit",
                 "Ownership &\nExecution", "Stakeholder\nComms", "Hard\nSkills", "Growth &\nLeadership"]
DIM_WEIGHTS  = [0.25, 0.20, 0.15, 0.15, 0.10, 0.10, 0.05]

# ══════════════════════════════════════════════════════════════════════
# COLOUR PALETTE
# ══════════════════════════════════════════════════════════════════════
C_PURPLE = colors.HexColor("#6D28D9")
C_PINK   = colors.HexColor("#DB2777")
C_BLUE   = colors.HexColor("#2563EB")
C_GREEN  = colors.HexColor("#16A34A")
C_RED    = colors.HexColor("#DC2626")
C_AMBER  = colors.HexColor("#D97706")
C_GRAY   = colors.HexColor("#6B7280")
C_LGRAY  = colors.HexColor("#F3F4F6")
C_WHITE  = colors.white
C_BLACK  = colors.HexColor("#1F2937")

TIER_COLORS = {
    "Tier A": C_GREEN,
    "Tier B": C_BLUE,
    "Tier C": C_AMBER,
    "No-Hire": C_RED,
}

# ══════════════════════════════════════════════════════════════════════
# STYLES
# ══════════════════════════════════════════════════════════════════════
def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "h1": ParagraphStyle("H1", fontSize=18, textColor=C_PURPLE, spaceAfter=6,
                              fontName="Helvetica-Bold", leading=22),
        "h2": ParagraphStyle("H2", fontSize=13, textColor=C_PURPLE, spaceBefore=14, spaceAfter=6,
                              fontName="Helvetica-Bold", leading=16, borderPadding=(0,0,4,0)),
        "h3": ParagraphStyle("H3", fontSize=11, textColor=C_BLACK, spaceBefore=10, spaceAfter=4,
                              fontName="Helvetica-Bold", leading=14),
        "body": ParagraphStyle("Body", fontSize=9, textColor=C_BLACK, spaceAfter=4,
                               fontName="Helvetica", leading=13),
        "small": ParagraphStyle("Small", fontSize=8, textColor=C_GRAY, spaceAfter=3,
                                fontName="Helvetica", leading=11),
        "center": ParagraphStyle("Center", fontSize=9, textColor=C_BLACK, alignment=TA_CENTER,
                                 fontName="Helvetica", leading=12),
        "bold": ParagraphStyle("Bold", fontSize=9, textColor=C_BLACK, fontName="Helvetica-Bold",
                               leading=12),
        "label": ParagraphStyle("Label", fontSize=8, textColor=C_WHITE, fontName="Helvetica-Bold",
                                alignment=TA_CENTER, leading=10),
        "cover_title": ParagraphStyle("CoverTitle", fontSize=22, textColor=C_WHITE,
                                      fontName="Helvetica-Bold", leading=26, alignment=TA_CENTER),
        "cover_sub": ParagraphStyle("CoverSub", fontSize=12, textColor=C_WHITE,
                                    fontName="Helvetica", leading=16, alignment=TA_CENTER),
        "bullet": ParagraphStyle("Bullet", fontSize=8.5, textColor=C_BLACK, fontName="Helvetica",
                                 leading=12, leftIndent=10, spaceAfter=2,
                                 bulletIndent=0, bulletFontSize=8),
    }
    return styles

# ══════════════════════════════════════════════════════════════════════
# CHART GENERATORS  (return BytesIO PNG)
# ══════════════════════════════════════════════════════════════════════
def make_bar_chart():
    top10 = CANDIDATES[:10]
    names  = [c["name"] for c in top10]
    scores = [c["score"] for c in top10]
    bar_colors = [
        "#16A34A" if s >= 85 else "#2563EB" if s >= 70 else "#D97706" if s >= 55 else "#DC2626"
        for s in scores
    ]
    fig, ax = plt.subplots(figsize=(10, 6.5))
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FAFAFA")
    bars = ax.barh(names[::-1], scores[::-1], color=bar_colors[::-1],
                   edgecolor="white", linewidth=0.8, height=0.65)
    ax.axvline(85, color="#16A34A", linewidth=1.4, linestyle="--", alpha=0.7)
    ax.axvline(70, color="#2563EB", linewidth=1.4, linestyle="--", alpha=0.7)
    ax.axvline(55, color="#D97706", linewidth=1.4, linestyle="--", alpha=0.7)
    ax.set_xlim(0, 105)
    ax.set_xlabel("Score", fontsize=9, color="#374151")
    ax.set_title("Candidate Score Comparison — Top 10 Shortlisted", fontsize=11,
                 fontweight="bold", color="#1F2937", pad=10)
    ax.tick_params(axis="y", labelsize=8)
    ax.tick_params(axis="x", labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for bar, score in zip(bars, scores[::-1]):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2,
                f"{score:.1f}", va="center", fontsize=7.5, color="#374151")
    patches = [
        mpatches.Patch(color="#16A34A", label="Tier A (85+)"),
        mpatches.Patch(color="#2563EB", label="Tier B (70–84)"),
        mpatches.Patch(color="#D97706", label="Tier C (55–69)"),
    ]
    ax.legend(handles=patches, fontsize=8, loc="lower right")
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return buf


def make_spider_chart():
    top3 = CANDIDATES[:3]
    labels = ["Functional\nMatch", "Demonstrated\nOutcomes", "Environment\nFit",
              "Ownership &\nExecution", "Stakeholder\nComms", "Hard\nSkills", "Growth &\nLeadership"]
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FAFAFA")
    c_list = ["#16A34A", "#2563EB", "#DB2777"]
    for i, c in enumerate(top3):
        vals = list(c["dims"])
        vals += vals[:1]
        ax.plot(angles, vals, color=c_list[i], linewidth=2, linestyle="solid", label=c["name"])
        ax.fill(angles, vals, color=c_list[i], alpha=0.10)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=8)
    ax.set_yticks([1, 2, 3, 4])
    ax.set_yticklabels(["1", "2", "3", "4"], size=7, color="grey")
    ax.set_ylim(0, 4)
    ax.set_title("7-Dimension Profile — Top 3 Candidates", pad=20, fontsize=11,
                 fontweight="bold", color="#1F2937")
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=8)
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return buf


def make_heatmap():
    top10 = CANDIDATES[:10]
    dim_short = ["Func", "Outcomes", "Env", "Ownership", "Comms", "Skills", "Growth"]
    names = [c["name"].split()[0] for c in top10]
    matrix = np.array([list(c["dims"]) for c in top10], dtype=float)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.patch.set_facecolor("#FAFAFA")
    cmap = plt.get_cmap("RdYlGn")
    im = ax.imshow(matrix, cmap=cmap, vmin=0, vmax=4, aspect="auto")

    ax.set_xticks(range(len(dim_short)))
    ax.set_xticklabels(dim_short, fontsize=9, fontweight="bold")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8.5)
    for i in range(len(names)):
        for j in range(len(dim_short)):
            val = matrix[i, j]
            text_color = "white" if val <= 1.5 else "black"
            ax.text(j, i, f"{int(val)}", ha="center", va="center",
                    fontsize=9, fontweight="bold", color=text_color)
    ax.set_title("Dimension Score Heatmap — Top 10 Candidates", fontsize=11,
                 fontweight="bold", color="#1F2937", pad=8)
    plt.colorbar(im, ax=ax, shrink=0.7, label="Score (0–4)")
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return buf


# ══════════════════════════════════════════════════════════════════════
# PDF BUILDER
# ══════════════════════════════════════════════════════════════════════
def strip_html(text):
    """Remove HTML tags and clean text for PDF."""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&mdash;', '—').replace('&bull;', '•').replace('&amp;', '&')
    return text.strip()


def build_pdf(output_path):
    S = make_styles()

    # Landscape A4: 297mm x 210mm — usable width = 267mm with 15mm margins
    PAGE  = landscape(A4)
    USABLE_W = 267 * mm

    doc = SimpleDocTemplate(
        output_path,
        pagesize=PAGE,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
        title=f"Screening Report — {JOB_TITLE}",
        author="Taleemabad Talent Acquisition Agent",
    )

    story = []

    # ── COVER BLOCK ─────────────────────────────────────────────────
    total_all = len(CANDIDATES) + len(OVER_BUDGET) + len(NO_HIRE)
    cover_table = Table([
        [Paragraph("Screening Report", S["cover_title"])],
        [Paragraph(JOB_TITLE, S["cover_title"])],
        [Paragraph(f"Taleemabad Talent Acquisition Agent  •  {date.today().strftime('%d %B %Y')}", S["cover_sub"])],
        [Paragraph(
            f"Total Screened: {TOTAL_SCREENED}  |  Shortlisted: {len(CANDIDATES)}  "
            f"|  Over Budget (flagged): {len(OVER_BUDGET)}  |  Budget: {BUDGET_RANGE}",
            S["cover_sub"]
        )],
    ], colWidths=[USABLE_W])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), C_PURPLE),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 7*mm))

    # ── SECTION 1: DEEP COMPARATIVE ANALYSIS ────────────────────────
    # Columns: # | Candidate | Score | Tier | Budget | Exp.Salary | Experience | Current Role | Key Strength | Verdict
    # Widths (mm): 6 | 24 | 11 | 13 | 20 | 22 | 14 | 44 | 93 | 20 = 267
    COL_W = [w*mm for w in [6, 24, 11, 13, 20, 22, 14, 44, 93, 20]]

    story.append(Paragraph("1.  Deep Comparative Analysis", S["h2"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PURPLE, spaceAfter=4))
    story.append(Paragraph(
        f"Master ranking of ALL {TOTAL_SCREENED} assessed candidates — shortlisted, over-budget flags, "
        f"and no-hire pool — sorted by JD match score. Budget is assessed separately and does not affect scores.",
        S["body"]
    ))
    story.append(Spacer(1, 3*mm))

    # ── Paragraph styles for table cells ────────────────────────────
    # ALL cells must be Paragraph objects — plain strings never wrap in reportlab
    PS = lambda text, fn="Helvetica", fs=8.5, tc=C_BLACK, align=TA_LEFT: Paragraph(
        str(text),
        ParagraphStyle("_", fontName=fn, fontSize=fs, textColor=tc,
                       leading=fs * 1.3, alignment=align, wordWrap="LTR")
    )
    PS_hdr   = lambda t: PS(t, "Helvetica-Bold",    8.5, C_WHITE,  TA_LEFT)
    PS_cell  = lambda t: PS(t, "Helvetica",          8.5, C_BLACK,  TA_LEFT)
    PS_ctr   = lambda t: PS(t, "Helvetica",          8.5, C_BLACK,  TA_CENTER)
    PS_bold  = lambda t: PS(t, "Helvetica-Bold",     8.5, C_BLACK,  TA_CENTER)
    PS_wht   = lambda t: PS(t, "Helvetica-Bold",     8.5, C_WHITE,  TA_CENTER)
    PS_sep   = lambda t: PS(t, "Helvetica-Bold",     8.5, C_WHITE,  TA_LEFT)
    PS_note  = lambda t: PS(t, "Helvetica-Oblique",  7.5, C_GRAY,   TA_LEFT)
    PS_green = lambda t: PS(t, "Helvetica-Bold",     8.5, C_GREEN,  TA_CENTER)
    PS_amber = lambda t: PS(t, "Helvetica-Bold",     8.5, C_AMBER,  TA_CENTER)
    PS_red   = lambda t: PS(t, "Helvetica-Bold",     8.5, C_RED,    TA_CENTER)

    def budget_cell(label):
        """Return a colour-coded Paragraph for the Budget column."""
        if "Within Budget" in label:
            return PS_green("In Budget")
        elif "Verify" in label:
            return PS_amber("Borderline")
        else:
            return PS_cell(label)

    HDR = [PS_hdr(h) for h in
           ["#", "Candidate", "Score", "Tier", "Budget", "Exp. Salary",
            "Experience", "Current Role / Background",
            "Key Strength  /  Why Not Shortlisted", "Verdict"]]

    tbl_rows  = [HDR]
    tbl_style = [
        ("BACKGROUND",    (0,0), (-1,0), C_PURPLE),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#E5E7EB")),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]

    row_idx = 1
    no_hire_count = TOTAL_SCREENED - len(CANDIDATES) - len(OVER_BUDGET)

    # ── Separator helper ──────────────────────────────────────────────
    def add_sep(label, bg):
        nonlocal row_idx, tbl_rows, tbl_style
        tbl_rows.append([PS_sep(label)] + [""] * 9)
        tbl_style += [
            ("SPAN",       (0, row_idx), (-1, row_idx)),
            ("BACKGROUND", (0, row_idx), (-1, row_idx), bg),
            ("TOPPADDING",    (0, row_idx), (-1, row_idx), 5),
            ("BOTTOMPADDING", (0, row_idx), (-1, row_idx), 5),
        ]
        row_idx += 1

    # ── Shortlisted ───────────────────────────────────────────────────
    add_sep("SHORTLISTED  —  15 candidates recommended for interview consideration", C_GREEN)

    for c in CANDIDATES:
        tier_col = TIER_COLORS.get(c["tier"], C_GRAY)
        bg = C_WHITE if (row_idx % 2 == 0) else C_LGRAY
        tbl_rows.append([
            PS_ctr(c["rank"]),
            PS_cell(c["name"]),
            PS_wht(f"{c['score']:.1f}"),
            PS_wht(c["tier"]),
            budget_cell(c["budget_label"]),
            PS_cell(c.get("salary", "Not mentioned")),
            PS_cell(c["total_exp"]),
            PS_cell(c["current_role"]),
            PS_cell(strip_html(c["key_strength"])),
            PS_bold(c["verdict"]),
        ])
        tbl_style += [
            ("BACKGROUND", (0, row_idx), (-1, row_idx), bg),
            ("BACKGROUND", (2, row_idx), (3, row_idx), tier_col),
        ]
        row_idx += 1

    # ── Over-budget ───────────────────────────────────────────────────
    add_sep("OVER BUDGET — Strong JD match but likely above PKR 250,000/month. Flagged for hiring manager review.", C_PINK)

    for i, c in enumerate(OVER_BUDGET, start=1):
        tier_col = TIER_COLORS.get(c["tier"], C_GRAY)
        bg = colors.HexColor("#FFF1F5") if (i % 2 == 1) else colors.HexColor("#FFE4EE")
        tbl_rows.append([
            PS_ctr(len(CANDIDATES) + i),
            PS_cell(c["name"]),
            PS_wht(f"{c['score']:.1f}"),
            PS_wht(c["tier"]),
            PS_red("Out of Budget"),
            PS_cell(c.get("salary", "Not mentioned")),
            PS_cell(c["exp"]),
            PS_cell(c["current_role"]),
            PS_cell(c["reason"]),
            PS_cell("Flagged"),
        ])
        tbl_style += [
            ("BACKGROUND", (0, row_idx), (-1, row_idx), bg),
            ("BACKGROUND", (2, row_idx), (3, row_idx), tier_col),
        ]
        row_idx += 1

    # ── No-hire ───────────────────────────────────────────────────────
    add_sep(f"NO-HIRE — {no_hire_count} candidates not shortlisted. Representative sample shown below.", C_BLACK)

    for i, c in enumerate(NO_HIRE, start=1):
        bg = C_LGRAY if (i % 2 == 1) else C_WHITE
        tbl_rows.append([
            PS_ctr(len(CANDIDATES) + len(OVER_BUDGET) + i),
            PS_cell(c["name"]),
            PS_wht(f"{c['score']:.1f}"),
            PS_wht("No-Hire"),
            PS_ctr("—"),
            PS_ctr("—"),
            PS_ctr("—"),
            PS_cell(c["background"]),
            PS_cell(c["reason"]),
            PS_cell("Not Suitable"),
        ])
        tbl_style += [
            ("BACKGROUND", (0, row_idx), (-1, row_idx), bg),
            ("BACKGROUND", (2, row_idx), (3, row_idx), C_RED),
        ]
        row_idx += 1

    # ── Footer note ───────────────────────────────────────────────────
    remaining = no_hire_count - len(NO_HIRE)
    tbl_rows.append([
        PS_note(
            f"+ {remaining} additional no-hire candidates not individually listed. "
            "Common reasons: no field M&E experience, no education sector exposure, "
            "wrong functional background (FMCG, HR, marketing, admin), "
            "or location outside Islamabad with no willingness to relocate."
        )
    ] + [""] * 9)
    tbl_style += [
        ("SPAN",       (0, row_idx), (-1, row_idx)),
        ("BACKGROUND", (0, row_idx), (-1, row_idx), colors.HexColor("#F9FAFB")),
    ]

    master_tbl = Table(tbl_rows, colWidths=COL_W, repeatRows=1)
    master_tbl.setStyle(TableStyle(tbl_style))
    story.append(master_tbl)
    story.append(Spacer(1, 4*mm))

    # ── SECTION 2: VISUAL ANALYTICS — CHARTS ────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("2.  Visual Analytics — Charts", S["h2"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PURPLE, spaceAfter=4))

    story.append(Paragraph("Bar Chart — Score Comparison (Top 10 Shortlisted)", S["h3"]))
    bar_buf = make_bar_chart()
    story.append(RLImage(bar_buf, width=220*mm, height=115*mm))
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph("Radar Chart — 7-Dimension Profile (Top 3 Candidates)", S["h3"]))
    spider_buf = make_spider_chart()
    story.append(RLImage(spider_buf, width=140*mm, height=140*mm))

    # ── SECTION 3: OUT OF BUDGET (detail) ───────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("3.  Strong Match but Out of Budget", S["h2"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PINK, spaceAfter=4))
    story.append(Paragraph(
        "These candidates scored strongly on JD fit but are likely above the PKR 250,000/month budget ceiling. "
        "Excluded from shortlist but flagged for review. Consider if role scope expands or budget is revised.",
        S["body"]
    ))
    story.append(Spacer(1, 3*mm))

    oob_col_w = [w*mm for w in [7, 28, 12, 14, 18, 48, 36, 104]]
    _hdr = lambda t: Paragraph(t, ParagraphStyle("_oh", fontName="Helvetica-Bold", fontSize=8.5, textColor=C_WHITE, leading=11))
    _cel = lambda t: Paragraph(str(t), ParagraphStyle("_oc", fontName="Helvetica", fontSize=8.5, textColor=C_BLACK, leading=11, wordWrap="LTR"))
    oob_rows = [[_hdr(h) for h in ["#", "Candidate", "Score", "Tier", "Experience", "Current Role", "Budget Note", "Why Flag"]]]
    for i, c in enumerate(OVER_BUDGET, start=1):
        oob_rows.append([_cel(i), _cel(c["name"]), _cel(f"{c['score']:.1f}"), _cel(c["tier"]),
                         _cel(c["exp"]), _cel(c["current_role"]), _cel(c["budget_note"]), _cel(c["reason"])])

    oob_tbl = Table(oob_rows, colWidths=oob_col_w, repeatRows=1)
    oob_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), C_PINK),
        ("TEXTCOLOR",     (0,0), (-1,0), C_WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 8.5),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#E5E7EB")),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [C_WHITE, colors.HexColor("#FFF1F5")]),
        ("WORDWRAP",      (0,0), (-1,-1), True),
    ]))
    story.append(oob_tbl)

    # ── SECTION 4: HEATMAP ───────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("4.  Visual Analytics — Heatmap", S["h2"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PURPLE, spaceAfter=4))
    story.append(Paragraph("7-dimension score heatmap for top 10 shortlisted candidates (scores 0–4 per dimension).", S["body"]))
    story.append(Spacer(1, 3*mm))
    heatmap_buf = make_heatmap()
    story.append(RLImage(heatmap_buf, width=240*mm, height=110*mm))

    # ── SECTION 5: WHY OTHERS DIDN'T MAKE IT ─────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("5.  Why Others Did Not Make the Cut", S["h2"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PURPLE, spaceAfter=4))
    story.append(Paragraph(
        f"Out of {TOTAL_SCREENED} candidates assessed, {no_hire_count} did not make the shortlist. "
        f"Representative no-hire cases are shown in the master table above (Section 1). "
        f"Key patterns across the broader pool:",
        S["body"]
    ))
    story.append(Spacer(1, 3*mm))

    reasons = [
        "No field M&E experience — largest group: community mobilisers, teachers, admin officers without research methodology exposure.",
        "No education sector exposure — FMCG, HR, marketing, corporate backgrounds with no school or NGO fieldwork.",
        "Wrong functional background — IT, data entry, finance candidates who applied to the wrong role.",
        "Location outside Islamabad, not willing to relocate — deal-breaker per screening criteria.",
        "Scanned/unreadable CVs with insufficient recoverable text — could not be scored; flagged in chat.",
    ]
    nh_col_w = [w*mm for w in [8, 259]]
    _nh_hdr = lambda t: Paragraph(t, ParagraphStyle("_nhh", fontName="Helvetica-Bold", fontSize=9, textColor=C_WHITE, leading=12))
    _nh_cel = lambda t: Paragraph(str(t), ParagraphStyle("_nhc", fontName="Helvetica", fontSize=9, textColor=C_BLACK, leading=12, wordWrap="LTR"))
    nh_rows_detail = [[_nh_hdr("#"), _nh_hdr("Pattern Across No-Hire Pool")]]
    for i, r in enumerate(reasons, start=1):
        nh_rows_detail.append([_nh_cel(i), _nh_cel(r)])

    nh_detail_tbl = Table(nh_rows_detail, colWidths=nh_col_w, repeatRows=1)
    nh_detail_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), C_BLACK),
        ("TEXTCOLOR",     (0,0), (-1,0), C_WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#E5E7EB")),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [C_WHITE, C_LGRAY]),
        ("WORDWRAP",      (0,0), (-1,-1), True),
        ("ALIGN",         (0,0), (0,-1), "CENTER"),
    ]))
    story.append(nh_detail_tbl)

    # ── NEXT STEPS ────────────────────────────────────────────────────
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("Recommended Next Steps", S["h2"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_GREEN, spaceAfter=4))
    steps = [
        "1. Confirm expected salary with all Tier A candidates before scheduling interviews.",
        "2. Priority interviews: Amina Batool (#1), Muhammad Siddique (#2), Mehwish Mukhtar (#3), Syed Nouman (#4).",
        "3. Request updated CV from Muhammad Siddique (scanned OCR — profile detail limited).",
        "4. Review over-budget candidates (Fatima Mughal #1 OOB) if budget flexibility exists or a senior advisory role is possible.",
        "5. Schedule 45-minute structured interviews using the 5 questions provided per candidate in the original screening notes.",
        "6. Re-advertise if fewer than 3 Tier A candidates confirm salary compatibility.",
    ]
    for step in steps:
        story.append(Paragraph(step, S["body"]))

    # ── FOOTER ────────────────────────────────────────────────────────
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_GRAY, spaceAfter=4))
    story.append(Paragraph("Taleemabad Talent Acquisition Agent  •  Confidential", S["small"]))

    doc.build(story)
    return output_path


# ══════════════════════════════════════════════════════════════════════
# EMAIL BUILDER  — brief summary only, PDF attached
# ══════════════════════════════════════════════════════════════════════
def build_email_html():
    shortlisted_count = len(CANDIDATES)
    oob_count = len(OVER_BUDGET)

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;font-size:14px;color:#1F2937;background:#ffffff;max-width:600px;margin:0 auto;padding:20px;">

  <div style="background:#6D28D9;padding:20px 24px;border-radius:8px 8px 0 0;">
    <p style="color:#ffffff;font-size:18px;font-weight:700;margin:0;">Taleemabad Talent Acquisition Agent</p>
    <p style="color:#E9D5FF;font-size:13px;margin:4px 0 0 0;">Automated Screening Report</p>
  </div>

  <div style="border:1px solid #E5E7EB;border-top:none;padding:24px;border-radius:0 0 8px 8px;">

    <p style="font-size:15px;margin:0 0 16px 0;">
      Hi {HIRING_MGR_FIRST},
    </p>

    <p style="margin:0 0 16px 0;">
      Our recruitment agent has completed the automated screening for
      <strong>{JOB_TITLE}</strong>.
    </p>

    <table style="width:100%;border-collapse:collapse;margin-bottom:20px;">
      <tr>
        <td style="padding:12px 16px;background:#F5F3FF;border:1px solid #DDD6FE;border-radius:6px;width:33%;text-align:center;">
          <div style="font-size:28px;font-weight:700;color:#6D28D9;">{TOTAL_SCREENED}</div>
          <div style="font-size:11px;color:#6B7280;margin-top:2px;">Profiles Screened</div>
        </td>
        <td style="width:2%;"></td>
        <td style="padding:12px 16px;background:#F0FDF4;border:1px solid #BBF7D0;border-radius:6px;width:33%;text-align:center;">
          <div style="font-size:28px;font-weight:700;color:#16A34A;">{shortlisted_count}</div>
          <div style="font-size:11px;color:#6B7280;margin-top:2px;">Profiles Shortlisted</div>
        </td>
        <td style="width:2%;"></td>
        <td style="padding:12px 16px;background:#FFF1F5;border:1px solid #FBCFE8;border-radius:6px;width:33%;text-align:center;">
          <div style="font-size:28px;font-weight:700;color:#DB2777;">{oob_count}</div>
          <div style="font-size:11px;color:#6B7280;margin-top:2px;">Strong Matches Over Budget</div>
        </td>
      </tr>
    </table>

    <p style="margin:0 0 10px 0;color:#374151;">
      To view the full analysis — ranked shortlist, dimension scores, charts, over-budget flags,
      and interview questions — please open the attached PDF report.
    </p>

    <p style="margin:0 0 20px 0;color:#6B7280;font-size:13px;">
      Budget: {BUDGET_RANGE}
    </p>

    <table style="border-top:2px solid #16A34A;margin-top:24px;padding-top:14px;width:100%;border-collapse:collapse;">
      <tr>
        <td style="font-family:Arial,sans-serif;font-size:13px;color:#1F2937;line-height:1.6;">
          <p style="margin:0 0 2px 0;"><strong style="color:#16A34A;">Ayesha Raza Khan,</strong></p>
          <p style="margin:0 0 2px 0;"><strong>Deputy Manager People &amp; Culture, Taleemabad.</strong></p>
          <p style="margin:0 0 2px 0;">M: +92 335 4288844</p>
          <p style="margin:0 0 2px 0;">
            @ <a href="https://www.taleemabad.com" style="color:#16A34A;text-decoration:none;">www.taleemabad.com</a>
            &nbsp;|&nbsp;
            <a href="https://www.linkedin.com/in/ayesha-raza-khan-386668177/" style="color:#16A34A;text-decoration:none;">LinkedIn</a>
          </p>
          <p style="margin:8px 0 0 0;font-size:11px;color:#9CA3AF;">
            Powered by AI Assistant &mdash; Taleemabad Talent Acquisition
          </p>
        </td>
      </tr>
    </table>

  </div>
</body>
</html>"""
    return html


def send_email(pdf_path):
    msg = MIMEMultipart()
    msg["From"]    = SENDER
    msg["To"]      = ", ".join(RECIPIENTS)
    msg["Subject"] = f"Screening Report- {JOB_TITLE}"

    # Brief HTML body
    html_body = build_email_html()
    msg.attach(MIMEText(html_body, "html"))

    # PDF attachment
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()

    part = MIMEBase("application", "pdf")
    part.set_payload(pdf_data)
    encoders.encode_base64(part)
    filename = f"Screening-Report-{JOB_TITLE.replace(' ', '-').replace(',','').replace('&','and')}.pdf"
    part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.sendmail(SENDER, RECIPIENTS, msg.as_string())

    print(f"Email sent to: {', '.join(RECIPIENTS)}")
    print(f"Subject: Screening Report- {JOB_TITLE}")
    print(f"Attachment: {filename}")


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating PDF report...")
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f"2026-03-05-field-coordinator-ri-screening-report.pdf")

    build_pdf(pdf_path)
    print(f"PDF saved: {pdf_path}")

    print("Sending email...")
    send_email(pdf_path)
    print("Done.")
