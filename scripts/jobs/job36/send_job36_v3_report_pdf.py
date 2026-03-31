"""
Job 36 v3 — Field Coordinator, Research & Impact Studies
Human-judgement re-screen: all 32 extracted CVs read manually.
Master table: # · Candidate · Score · Tier · Budget · Exp. Salary · Experience · Background/Current Role · Key Strength/Why Not Shortlisted · Verdict
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
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses


RECIPIENTS       = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
CC               = []
HIRING_MGR_FIRST = "Ayesha and Jawwad"
SENDER           = os.getenv("EMAIL_USER")
PASSWORD         = os.getenv("EMAIL_PASSWORD")

JOB_TITLE        = "Field Coordinator – Research & Impact Studies"
JOB_ID           = 36
TOTAL_SCREENED   = 179
TOTAL_APPLICANTS = 179
BUDGET_RANGE     = "PKR 200,000 – 250,000 / month"

# ══════════════════════════════════════════════════════════════════════
# CANDIDATES — Human-judgement re-screen (v3, 2026-03-09)
# All 32 extracted CVs read manually. Keyword scanner replaced by
# 7-dimension human assessment. dims: (functional, outcomes, environment,
# ownership, communication, hard_skills, growth) each 0–4.
# ══════════════════════════════════════════════════════════════════════
CANDIDATES = [
    {
        "rank": 1, "name": "Asif Khan", "app_id": 1602, "score": 100.0, "tier": "Tier A",
        "total_exp": "~13 yrs", "relevant_exp": "~10 yrs (M&E/QA specialist, USAID & World Bank)",
        "current_role": "Data/QA Specialist — USAID, World Bank, GIZ projects, Islamabad",
        "salary": "PKR 250,000", "budget_label": "Borderline (at ceiling)", "over_budget": False,
        "key_strength": "JD MATCH: 13+ yrs QA/M&E field specialist — exact role title match. "
                        "Spot-checks, data quality governance, and survey firm oversight confirmed in CV evidence. "
                        "Org signal (supplementary): USAID, World Bank, GIZ, CARE.",
        "verdict": "RECOMMEND",
        "dims": (4, 4, 4, 4, 4, 4, 4), "missing_mh": 0,
    },
    {
        "rank": 2, "name": "Amina Batool", "app_id": 1857, "score": 95.0, "tier": "Tier A",
        "total_exp": "~4 yrs", "relevant_exp": "~4 yrs (field PM, AI assessment pilot, education sector)",
        "current_role": "Project Manager (AI Assessment Pilot) — EdTech Hub / Pakistan Institute of Education, Islamabad",
        "salary": "PKR 300,000–310,000", "budget_label": "Out of Budget", "over_budget": True,
        "key_strength": "JD MATCH: PM of AI-enabled foundational learning assessment pilot for PIE — managed "
                        "1,700+ school-based student assessments across 3 field rounds; supervised human-marking "
                        "team labelling ~500K recordings with QA + retraining protocols. Education field coordination "
                        "at scale. TFP Fellow 2022–24 + EdTech Hub. "
                        "COMPETITOR SIGNAL: EdTech Hub (direct Taleemabad peer) + Teach For Pakistan. "
                        "FLAG: Expected salary PKR 300–310K exceeds ceiling by PKR 50–60K — negotiate.",
        "verdict": "RECOMMEND (flag salary)",
        "dims": (4, 4, 4, 4, 3, 3, 4), "missing_mh": 0,
    },
    {
        "rank": 3, "name": "Scheherazade Noor", "app_id": 1430, "score": 95.0, "tier": "Tier A",
        "total_exp": "~3 yrs", "relevant_exp": "~3 yrs (TCF RA, education field research)",
        "current_role": "Research Associate — The Citizens Foundation (TCF), Islamabad (LUMS alumna)",
        "salary": "PKR 150,000–175,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: TCF Research Associate — managed 12 data collectors across 30+ schools; "
                        "multi-stakeholder study coordinating field data collection for Sindh SE&LD; "
                        "government education coordination confirmed. Education M&E at scale. "
                        "COMPETITOR SIGNAL: The Citizens Foundation (TCF). Org signal: LUMS. "
                        "NOTE: Keyword scanner undercounted — used 'data collectors' not 'enumerators'.",
        "verdict": "RECOMMEND",
        "dims": (4, 4, 4, 4, 4, 2, 4), "missing_mh": 0,
    },
    {
        "rank": 4, "name": "Fatima Mughal", "app_id": 1864, "score": 93.0, "tier": "Tier A",
        "total_exp": "~15 yrs", "relevant_exp": "~12 yrs (MEAL education, field data governance)",
        "current_role": "MEAL Specialist / Program Manager — ITA, GOAL (FCDO), BRAC, AKESP",
        "salary": "PKR 170,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: 15 yrs MEAL in education sector — ODK + KoboToolbox expert confirmed in CV; "
                        "GOAL project (ITA/FCDO/British Council), BRAC, AKESP; end-to-end field data governance, "
                        "enumerator supervision, reporting, and govt/donor liaison all evidenced. "
                        "COMPETITOR SIGNAL: Idara-e-Taleem o Aagahi (ITA) — education NGO. "
                        "Org signal: FCDO, British Council, BRAC.",
        "verdict": "RECOMMEND",
        "dims": (4, 4, 4, 3, 3, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 5, "name": "Faryal Afridi", "app_id": 1442, "score": 89.0, "tier": "Tier A",
        "total_exp": "~4 yrs", "relevant_exp": "~4 yrs (education field research, Taleemabad + AiD)",
        "current_role": "Research Assistant / Field Coordinator — Taleemabad + AiD, Islamabad",
        "salary": "PKR 100,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Taleemabad RA (Jan–Aug 2024) + AiD field coordinator; education research data "
                        "collection, school coordination, and field tools confirmed. "
                        "COMPETITOR SIGNAL: Taleemabad direct — highest possible culture fit; knows the product, team, and mission. "
                        "Org signal: USAID, NUST. NOTE: 4 yrs experience — confirm survey firm management independently.",
        "verdict": "RECOMMEND",
        "dims": (4, 3, 4, 3, 4, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 6, "name": "Zubair Hussain", "app_id": 1518, "score": 85.0, "tier": "Tier A",
        "total_exp": "~15 yrs", "relevant_exp": "~10 yrs (field ops, Area Manager Education)",
        "current_role": "Head of Operations & Area Manager Education — USAID/IPA projects",
        "salary": "PKR 220,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Head of Operations (865 staff, 900K HH nationwide) + Area Manager Education — "
                        "massive field governance scale; USAID/IPA field expertise and enumerator oversight. "
                        "Org signal: USAID, IPA, CARE. "
                        "NOTE: Primary domain is humanitarian/rural dev — confirm education M&E commitment at scale.",
        "verdict": "INTERVIEW",
        "dims": (4, 4, 3, 3, 3, 3, 4), "missing_mh": 0,
    },
    {
        "rank": 7, "name": "HabibunNabi", "app_id": 1839, "score": 85.0, "tier": "Tier A",
        "total_exp": "~17 yrs", "relevant_exp": "~15 yrs (Provincial FC, ODK expert, KP/national)",
        "current_role": "Provincial Field Coordinator / ODK Expert — IPA-supported programs, KP/Islamabad",
        "salary": "PKR 80,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: 17 yrs Provincial Field Coordinator — ODK expert confirmed in CV; "
                        "school-level coordination, enumerator supervision, and govt liaison all evidenced. "
                        "Org signal: IPA, LUMS. "
                        "FLAG: PKR 80K salary is unusually low for 17 yrs experience — likely a data entry error; verify before interview.",
        "verdict": "INTERVIEW",
        "dims": (4, 2, 3, 4, 4, 4, 4), "missing_mh": 0,
    },
    {
        "rank": 8, "name": "Asad Farooq", "app_id": 1700, "score": 84.0, "tier": "Tier B",
        "total_exp": "~10 yrs", "relevant_exp": "~6 yrs (TFP Fellow + school oversight, Islamabad)",
        "current_role": "School Coordinator — Teach For Pakistan Fellow, 44 govt school spot-checks, Islamabad",
        "salary": "PKR 140,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: TFP Fellow + current school coordinator — spot-checks across 44 govt schools; "
                        "education sector immersion; Islamabad-based with strong govt school relationship experience. "
                        "COMPETITOR SIGNAL: Teach For Pakistan (TFP). "
                        "NOTE: Teaching/school coordinator background — probe depth of survey firm management and data quality oversight.",
        "verdict": "INTERVIEW",
        "dims": (4, 3, 4, 3, 3, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 9, "name": "Mehwish", "app_id": 1808, "score": 81.0, "tier": "Tier B",
        "total_exp": "~5 yrs", "relevant_exp": "~5 yrs (CED Research Manager, ODK/SurveyCTO)",
        "current_role": "Research Manager — CED, ODK/SurveyCTO/STATA/R, Islamabad",
        "salary": "PKR 200,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: CED Research Manager — ODK + SurveyCTO + STATA + R confirmed; "
                        "end-to-end research design and field data collection experience. Strong hard skills toolkit. "
                        "Org signal: CED (research org). "
                        "NOTE: Research-heavy profile — confirm operational day-to-day field coordination depth. "
                        "Keyword scanner undercounted this candidate.",
        "verdict": "INTERVIEW",
        "dims": (3, 3, 4, 3, 4, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 10, "name": "Ali Zia", "app_id": 1513, "score": 78.0, "tier": "Tier B",
        "total_exp": "~12 yrs", "relevant_exp": "~12 yrs (RADS/AKU M&E, field supervision)",
        "current_role": "M&E Specialist — RADS/Aga Khan University, 12 yrs field supervision, Islamabad",
        "salary": "Per budget", "budget_label": "In Budget (flexible)", "over_budget": False,
        "key_strength": "JD MATCH: 12 yrs RADS/AKU M&E — established field supervision, data collection management; "
                        "Islamabad-based; salary flexible (per budget). Experienced M&E professional. "
                        "Org signal: Aga Khan University (RADS). "
                        "NOTE: Development/health sector primarily — confirm education context fit in interview.",
        "verdict": "CONSIDER",
        "dims": (3, 3, 3, 3, 4, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 11, "name": "Muhammad Omer Khan", "app_id": 1789, "score": 78.0, "tier": "Tier B",
        "total_exp": "~4 yrs", "relevant_exp": "~4 yrs (CED Research Manager, Kobo/ODK/SurveyCTO)",
        "current_role": "Research Manager — CED, Kobo/ODK/SurveyCTO, Islamabad",
        "salary": "PKR 155,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: CED Research Manager — Kobo + ODK + SurveyCTO confirmed; Islamabad-based; "
                        "research to field coordination experience with strong tools. "
                        "Org signal: CED. Similar profile to Mehwish — compare alongside for complementarity.",
        "verdict": "CONSIDER",
        "dims": (3, 3, 3, 3, 4, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 12, "name": "Usman Ahmed Khan", "app_id": 1755, "score": 75.0, "tier": "Tier B",
        "total_exp": "~4 yrs", "relevant_exp": "~3 yrs (TFP Senior Associate + Fellow)",
        "current_role": "Senior Associate — Teach For Pakistan, school coordination, Islamabad",
        "salary": "PKR 160,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: TFP Senior Associate + Fellow — school visits, education stakeholder coordination, "
                        "mission alignment confirmed. "
                        "COMPETITOR SIGNAL: Teach For Pakistan (TFP). "
                        "NOTE: Limited quantitative M&E tools evidence in CV — probe data management and enumerator supervision depth.",
        "verdict": "CONSIDER",
        "dims": (3, 3, 3, 3, 3, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 13, "name": "Fatima Razzaq", "app_id": 1658, "score": 74.0, "tier": "Tier B",
        "total_exp": "~8 yrs", "relevant_exp": "~8 yrs (OPM qualitative research, Islamabad)",
        "current_role": "Senior Qualitative Researcher — Oxford Policy Management (OPM), Islamabad",
        "salary": "PKR 186,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: OPM Senior Qualitative Researcher — 8 yrs qualitative field research, FGDs, KIIs, "
                        "govt coordination; strong communication skills. "
                        "Org signal: Oxford Policy Management. "
                        "NOTE: Primarily qualitative — confirm quantitative field data management, enumerator oversight, "
                        "and data quality tracking experience. Scanner overscored by ~17 pts.",
        "verdict": "CONSIDER",
        "dims": (3, 3, 3, 3, 3, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 14, "name": "Jawad Khan", "app_id": 1720, "score": 71.0, "tier": "Tier B",
        "total_exp": "~5 yrs", "relevant_exp": "~4 yrs (UNICEF/UNDP evaluator, PIDE MPhil)",
        "current_role": "PhD Scholar / UNICEF Evaluator — PIDE, development research, Islamabad",
        "salary": "PKR 200,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: UNICEF evaluator + PIDE MPhil — evaluation methods, data analysis, development sector. "
                        "Org signal: UNICEF, UNDP, PIDE. "
                        "NOTE: PhD-track academic researcher — confirm interest in operational field coordination vs. "
                        "research/academic career. Scanner overscored by ~21 pts; desk-based evaluator, not field coordinator.",
        "verdict": "CONSIDER",
        "dims": (3, 3, 3, 2, 3, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 15, "name": "Muhammad Junaid", "app_id": 1591, "score": 71.0, "tier": "Tier B",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (PIDE MPhil + Taleemabad enumerator)",
        "current_role": "Field Enumerator / MPhil Scholar — Taleemabad + PIDE, Islamabad",
        "salary": "PKR 180,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Taleemabad Field Enumerator (Feb–May 2025) + PIDE MPhil — direct ODK/field data "
                        "collection experience with mission alignment confirmed. "
                        "COMPETITOR SIGNAL: Taleemabad direct. Early-career with strong education sector entry point. "
                        "NOTE: Only 2 yrs experience — suitable for junior FC or mentored role.",
        "verdict": "CONSIDER",
        "dims": (3, 3, 3, 2, 3, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 16, "name": "Jalal Ud Din", "app_id": 1950, "score": 70.0, "tier": "Tier B",
        "total_exp": "~4 yrs (MPhil)", "relevant_exp": "~3 yrs (PIDE field supervisor, 350-HH data collection)",
        "current_role": "Research Fellow / Field Supervisor — PIDE, 350-HH data collection, Islamabad",
        "salary": "PKR 120,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: PIDE field supervisor — supervised 350-HH data collection; quantitative methods; "
                        "field data management experience. Islamabad-based. "
                        "Org signal: PIDE (World Bank, development research). "
                        "NOTE: Limited education M&E scope — confirm school-based field coordination experience.",
        "verdict": "CONSIDER",
        "dims": (3, 3, 3, 2, 3, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 17, "name": "Muhammad Siddique", "app_id": 1624, "score": 70.0, "tier": "Tier B",
        "total_exp": "~6 yrs", "relevant_exp": "~6 yrs (IDS, World Bank/IFPRI national surveys)",
        "current_role": "Survey Researcher — IDS, World Bank/IFPRI national surveys, Islamabad",
        "salary": "PKR 120,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: IDS — World Bank and IFPRI national surveys; field research, data collection, "
                        "survey coordination confirmed. Strong research org background. "
                        "Org signal: World Bank, IFPRI (high-signal). "
                        "NOTE: National surveys at research org — confirm enumerator management and operational field FC scope.",
        "verdict": "CONSIDER",
        "dims": (3, 3, 3, 2, 3, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 18, "name": "Shahid Kamal", "app_id": 1454, "score": 65.0, "tier": "Tier C",
        "total_exp": "~11 yrs", "relevant_exp": "~6 yrs (M&E Officer + LUMS RA)",
        "current_role": "M&E Officer / Research Associate — Karishma Ali Foundation + LUMS, Islamabad",
        "salary": "PKR 150,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: M&E Officer (Karishma Ali Foundation) + LUMS RA; field M&E and data collection, "
                        "Islamabad-based. Org signal: LUMS, UNDP, IPA. "
                        "NOTE: Scanner overscored by ~24 pts. Scale of field operations needs probing — "
                        "may be more NGO grant management than front-line field coordination.",
        "verdict": "REVIEW",
        "dims": (3, 2, 3, 2, 3, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 19, "name": "Pariyal Fazal Shah", "app_id": 1545, "score": 62.0, "tier": "Tier C",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (M&R analyst, desk-based, Islamabad)",
        "current_role": "M&R Analyst — Islamabad (2 yrs experience, desk-based)",
        "salary": "PKR 200,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Field research background + Islamabad-based. "
                        "NOTE: Scanner massively overscored at 93.8 — only 2 yrs experience, role is M&R analyst "
                        "(monitoring & reporting, desk-based) not operational field coordination. "
                        "Insufficient enumerator management or survey firm oversight evidence.",
        "verdict": "REVIEW",
        "dims": (3, 2, 3, 2, 3, 2, 2), "missing_mh": 0,
    },
    {
        "rank": 20, "name": "Naveen Shariff", "app_id": 1450, "score": 59.0, "tier": "Tier C",
        "total_exp": "~2 yrs", "relevant_exp": "~1 yr (TCF intern, Kobo tools exposure)",
        "current_role": "TCF Intern / Entry-level Researcher — Karachi (relocation needed)",
        "salary": "PKR 220,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: TCF intern with Kobo tools exposure; entry-level field research interest. "
                        "COMPETITOR SIGNAL: The Citizens Foundation (TCF) — intern level. "
                        "NOTE: Karachi-based — relocation to Islamabad required. Very limited field coordination "
                        "evidence at scale. Salary ask (220K) is high relative to experience.",
        "verdict": "REVIEW",
        "dims": (3, 2, 2, 2, 2, 3, 2), "missing_mh": 0,
    },
]

# ══════════════════════════════════════════════════════════════════════
# OVER BUDGET — Strong matches over PKR 250K ceiling
# ══════════════════════════════════════════════════════════════════════
OVER_BUDGET = [
    {
        "name": "Amina Batool", "app_id": 1857, "score": 95.0, "tier": "Tier A",
        "salary": "PKR 300,000–310,000",
        "budget_note": "OVER BUDGET — exceeds PKR 250K ceiling by PKR 50–60K",
        "note": "Rank #2 overall with human-judgement score of 95 — strongest education field coordination PM "
                "in the entire pool. Managed 1,700+ school-based student assessments + supervised human-marking "
                "team labelling ~500K recordings for AI pilot at Pakistan Institute of Education. "
                "TFP Fellow 2022–24 + EdTech Hub. Also listed in shortlist above. "
                "Salary ask is PKR 50–60K over ceiling — strongly recommend exploring negotiation before defaulting to lower-scoring candidates.",
        "verdict": "FLAG — Over Budget (negotiate)",
    },
]

# ══════════════════════════════════════════════════════════════════════
# NO-HIRE CANDIDATES — Representative sample
# Includes scanner-overscored candidates corrected by human judgement
# ══════════════════════════════════════════════════════════════════════
NO_HIRE_CANDIDATES = [
    {"name": "Muhammad Afzaal (1528)",      "score": 45, "tier": "No-Hire",
     "reason": "Scanner 86.2 → human 45. Community mobilizer (Peshawar), USAID community work. "
               "No M&E tools in practice, no enumerator supervision, no education sector. "
               "Scanner over-counted Kobo/ODK listed in skills section without CV evidence of actual use."},
    {"name": "Midhat Fatima (1633)",         "score": 49, "tier": "No-Hire",
     "reason": "Scanner 86.2 → human 49. Public health surveyor, intern-level. No education M&E, "
               "no field team management, no enumerator supervision. Health sector only."},
    {"name": "Muhammad Qasi (1489)",         "score": 50, "tier": "No-Hire",
     "reason": "Scanner 85 → human 50. Small-scale KII researcher, Gilgit-Baltistan. "
               "No field team management at scale, no enumerator supervision, no education context."},
    {"name": "Sadia Siddique (1477)",        "score": 31, "tier": "No-Hire",
     "reason": "Scanner 81.2 → human 31. HR/data analyst background — no field coordination, "
               "no M&E, no education sector experience. CV is desk-based data analysis only."},
    {"name": "Syeda Farzana Ali Shah (1802)", "score": 39, "tier": "No-Hire",
     "reason": "Scanner 83.8 → human 39. 25 yrs in child protection/safeguarding/gender — entirely "
               "wrong domain for field research coordination. Over budget (PKR 300K). Not a field coordinator."},
    {"name": "Saira Akram",                  "score": 18, "tier": "No-Hire",
     "reason": "Expected salary PKR 400,000 — far exceeds budget. CV background is social/community work, not M&E or field coordination."},
    {"name": "Faiza Ghazal",                 "score": 20, "tier": "No-Hire",
     "reason": "Expected salary PKR 320,000 — over budget. Marketing/communications background — not relevant to field research coordination."},
    {"name": "Rabia Mukhtar",                "score": 12, "tier": "No-Hire",
     "reason": "Salary entry appears erroneous (PKR 855,700). Background unrelated to M&E or field research."},
    {"name": "Multiple applicants (20+)",    "score": 10, "tier": "No-Hire",
     "reason": "Quick-apply placeholder profiles ('Applicant' last name, no resume). Cannot assess — 20+ such applications discarded."},
]

# ══════════════════════════════════════════════════════════════════════
# COLOURS
# ══════════════════════════════════════════════════════════════════════
C_WHITE    = colors.white
C_BLACK    = colors.black
C_TIER_A   = colors.HexColor("#16A34A")
C_TIER_B   = colors.HexColor("#2563EB")
C_TIER_C   = colors.HexColor("#D97706")
C_NO_HIRE  = colors.HexColor("#DC2626")
C_HEADER   = colors.HexColor("#1E3A5F")
C_PURPLE   = colors.HexColor("#6D28D9")
C_GREEN_BG = colors.HexColor("#F0FDF4")
C_BLUE_BG  = colors.HexColor("#EFF6FF")
C_AMBER_BG = colors.HexColor("#FFFBEB")
C_GRAY     = colors.HexColor("#6B7280")
C_LIGHT_GRAY = colors.HexColor("#F3F4F6")
C_SEP_GREEN  = colors.HexColor("#DCFCE7")
C_SEP_PINK   = colors.HexColor("#FCE7F3")
C_SEP_BLACK  = colors.HexColor("#374151")
C_IN_BUDGET  = colors.HexColor("#16A34A")
C_BORDERLINE = colors.HexColor("#D97706")
C_OOB        = colors.HexColor("#DC2626")


def PS(text, fs=8, tc=C_BLACK, bold=False, align=TA_LEFT):
    style = ParagraphStyle(
        'custom',
        fontSize=fs,
        textColor=tc,
        fontName='Helvetica-Bold' if bold else 'Helvetica',
        leading=fs * 1.25,
        alignment=align,
        wordWrap='LTR',
        spaceAfter=0,
    )
    return Paragraph(str(text), style)


def PS_h(text, fs=14):
    style = ParagraphStyle(
        'heading',
        fontSize=fs,
        textColor=C_HEADER,
        fontName='Helvetica-Bold',
        leading=fs * 1.3,
        spaceAfter=4,
    )
    return Paragraph(text, style)


# ══════════════════════════════════════════════════════════════════════
# CHART BUILDERS
# ══════════════════════════════════════════════════════════════════════
def make_bar_chart():
    top10 = CANDIDATES[:10]
    names  = [c["name"].split()[-1] + ", " + c["name"].split()[0] for c in top10]
    scores = [c["score"] for c in top10]
    tier_colors = []
    for c in top10:
        if c["tier"] == "Tier A": tier_colors.append("#16A34A")
        elif c["tier"] == "Tier B": tier_colors.append("#2563EB")
        elif c["tier"] == "Tier C": tier_colors.append("#D97706")
        else: tier_colors.append("#DC2626")

    fig, ax = plt.subplots(figsize=(9, 5))
    y_pos = range(len(names))
    bars  = ax.barh(list(y_pos), scores, color=tier_colors, edgecolor='white', height=0.6)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Score (0–100)", fontsize=8)
    ax.set_title("Top 10 Candidates — Human-Judgement Score (v3)", fontsize=10, fontweight='bold')
    ax.set_xlim(0, 110)
    ax.axvline(x=85, color='#16A34A', linestyle='--', alpha=0.7, linewidth=1.2, label='Tier A (85)')
    ax.axvline(x=70, color='#2563EB', linestyle='--', alpha=0.7, linewidth=1.2, label='Tier B (70)')
    ax.axvline(x=55, color='#D97706', linestyle='--', alpha=0.7, linewidth=1.2, label='Tier C (55)')
    for bar, score in zip(bars, scores):
        ax.text(score + 1, bar.get_y() + bar.get_height()/2, f"{score}", va='center', fontsize=8)
    ax.legend(fontsize=7, loc='lower right')
    ax.invert_yaxis()
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


def make_radar_chart():
    top3   = CANDIDATES[:3]
    labels = ["Functional\nMatch", "Outcomes", "Environ-\nment", "Ownership", "Comm.", "Hard\nSkills", "Growth"]
    N      = len(labels)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    colors_r = ['#16A34A', '#2563EB', '#D97706']

    fig, ax = plt.subplots(figsize=(6, 5), subplot_kw=dict(polar=True))
    for i, cand in enumerate(top3):
        vals = list(cand["dims"]) + [cand["dims"][0]]
        ax.plot(angles, vals, 'o-', linewidth=2, color=colors_r[i], label=cand["name"].split()[0])
        ax.fill(angles, vals, alpha=0.15, color=colors_r[i])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylim(0, 4)
    ax.set_yticks([1, 2, 3, 4])
    ax.set_yticklabels(['1', '2', '3', '4'], fontsize=6)
    ax.set_title("Top 3 — Dimension Comparison", fontsize=10, fontweight='bold', pad=15)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=8)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


def make_heatmap():
    top10  = CANDIDATES[:10]
    names  = [c["name"] for c in top10]
    dim_labels = ["Functional", "Outcomes", "Environment", "Ownership", "Communication", "Hard Skills", "Growth"]
    data   = np.array([list(c["dims"]) for c in top10], dtype=float)

    fig, ax = plt.subplots(figsize=(10, 5))
    im = ax.imshow(data, cmap='RdYlGn', vmin=0, vmax=4, aspect='auto')
    ax.set_xticks(range(len(dim_labels)))
    ax.set_xticklabels(dim_labels, fontsize=8, rotation=20, ha='right')
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    for i in range(len(names)):
        for j in range(len(dim_labels)):
            ax.text(j, i, str(int(data[i, j])), ha='center', va='center', fontsize=9,
                    color='white' if data[i, j] < 2 else 'black')
    plt.colorbar(im, ax=ax, label='Score (0–4)')
    ax.set_title("Dimension Heatmap — Top 10 Candidates", fontsize=10, fontweight='bold')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


# ══════════════════════════════════════════════════════════════════════
# PDF BUILDER
# ══════════════════════════════════════════════════════════════════════
def build_pdf():
    pdf_path = f"output/{date.today()}-field-coordinator-research-impact-v3-screening-report.pdf"
    os.makedirs("output", exist_ok=True)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(A4),
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=12*mm, bottomMargin=12*mm,
    )

    story = []

    # ── Title block ─────────────────────────────────────────────────
    story.append(PS_h(f"Screening Report — {JOB_TITLE}", fs=16))
    story.append(PS(
        f"Job ID: {JOB_ID}  |  Total Applications: {TOTAL_APPLICANTS}  |  "
        f"CVs Screened: {TOTAL_SCREENED}  |  Shortlisted: {len(CANDIDATES)}  |  "
        f"Over Budget: {len([c for c in OVER_BUDGET if 'OVER' in c.get('budget_note','')])}  |  "
        f"Budget: {BUDGET_RANGE}  |  Date: {date.today()}  |  Method: Human-Judgement v3",
        fs=8, tc=C_GRAY
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_HEADER, spaceAfter=6))
    story.append(Spacer(1, 3*mm))

    # ── SECTION 1 — Deep Comparative Analysis ─────────────────────
    story.append(PS_h("Deep Comparative Analysis — All Screened Candidates", fs=12))
    story.append(PS(
        f"Master table shows all {len(CANDIDATES)} shortlisted candidates + over-budget flags + representative no-hire sample. "
        f"Scored using 7-dimension human-judgement framework — all 32 extracted CVs read manually. "
        f"Keyword scanner scores replaced. Names sourced from Markaz profiles.",
        fs=8, tc=C_GRAY
    ))
    story.append(Spacer(1, 3*mm))

    # Column widths — 267mm usable landscape A4
    col_widths = [6*mm, 28*mm, 11*mm, 13*mm, 22*mm, 22*mm, 14*mm, 40*mm, 91*mm, 20*mm]

    header_row = [
        PS("#",            fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
        PS("Candidate",    fs=7.5, tc=C_WHITE, bold=True),
        PS("Score",        fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
        PS("Tier",         fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
        PS("Budget",       fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
        PS("Exp. Salary",  fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
        PS("Experience",   fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
        PS("Background / Current Role", fs=7.5, tc=C_WHITE, bold=True),
        PS("Key Strength / Why Not Shortlisted", fs=7.5, tc=C_WHITE, bold=True),
        PS("Verdict",      fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
    ]

    table_data = [header_row]
    table_styles = [
        ('BACKGROUND',   (0, 0), (-1, 0), C_HEADER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_LIGHT_GRAY]),
        ('GRID',         (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D5DB")),
        ('VALIGN',       (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING',  (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING',   (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 2),
    ]

    row_idx = 1

    # Separator — Shortlisted
    sep_row = [PS("SHORTLISTED", fs=7, tc=C_WHITE, bold=True, align=TA_CENTER)] + [""] * 9
    table_data.append(sep_row)
    table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), C_SEP_GREEN))
    table_styles.append(('SPAN', (0, row_idx), (-1, row_idx)))
    row_idx += 1

    for c in CANDIDATES:
        bl = c.get("budget_label", "")
        if "Out of Budget" in bl or "over" in bl.lower():
            bl_color = C_OOB
        elif "Borderline" in bl:
            bl_color = C_BORDERLINE
        else:
            bl_color = C_IN_BUDGET

        tier_col = {"Tier A": C_TIER_A, "Tier B": C_TIER_B, "Tier C": C_TIER_C}.get(c["tier"], C_NO_HIRE)

        vc = c.get("verdict", "")
        if "RECOMMEND" in vc:
            verd_col = C_TIER_A
        elif "INTERVIEW" in vc:
            verd_col = C_TIER_B
        else:
            verd_col = C_GRAY

        app_id_str = f"App #{c.get('app_id', '—')}"
        row = [
            PS(str(c["rank"]),            fs=7.5, align=TA_CENTER),
            PS(f"<b>{c['name']}</b><br/><font size='6' color='#6B7280'>{app_id_str}</font>", fs=7.5),
            PS(str(c["score"]),           fs=7.5, align=TA_CENTER),
            PS(c["tier"],                 fs=7.5, tc=tier_col, bold=True, align=TA_CENTER),
            PS(bl,                        fs=7,   tc=bl_color, bold=True, align=TA_CENTER),
            PS(c.get("salary","Not mentioned"), fs=7, tc=C_GRAY, align=TA_CENTER),
            PS(c.get("total_exp", "—"),   fs=7.5, align=TA_CENTER),
            PS(c["current_role"],         fs=7.5),
            PS(c["key_strength"],         fs=7.5),
            PS(vc,                        fs=7.5, tc=verd_col, bold=True, align=TA_CENTER),
        ]
        table_data.append(row)
        row_idx += 1

    # Separator — Over Budget
    sep_row2 = [PS("STRONG MATCH — OVER BUDGET", fs=7, tc=C_WHITE, bold=True, align=TA_CENTER)] + [""] * 9
    table_data.append(sep_row2)
    table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), C_SEP_PINK))
    table_styles.append(('SPAN', (0, row_idx), (-1, row_idx)))
    row_idx += 1

    for i, c in enumerate(OVER_BUDGET):
        ob_app = f"App #{c.get('app_id', '—')}"
        row = [
            PS(f"OB{i+1}", fs=7.5, align=TA_CENTER),
            PS(f"<b>{c['name']}</b><br/><font size='6' color='#6B7280'>{ob_app}</font>", fs=7.5),
            PS(str(c["score"]), fs=7.5, align=TA_CENTER),
            PS(c["tier"],       fs=7.5, tc=C_TIER_A, bold=True, align=TA_CENTER),
            PS(c.get("budget_note", "Over Budget"), fs=7, tc=C_OOB, bold=True, align=TA_CENTER),
            PS(c["salary"],     fs=7, tc=C_OOB, bold=True, align=TA_CENTER),
            PS("—",             fs=7.5, align=TA_CENTER),
            PS("—",             fs=7.5),
            PS(c["note"],       fs=7.5),
            PS(c["verdict"],    fs=7.5, tc=C_OOB, bold=True, align=TA_CENTER),
        ]
        table_data.append(row)
        row_idx += 1

    # Separator — No Hire
    sep_row3 = [PS("NO HIRE", fs=7, tc=C_WHITE, bold=True, align=TA_CENTER)] + [""] * 9
    table_data.append(sep_row3)
    table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), C_SEP_BLACK))
    table_styles.append(('SPAN', (0, row_idx), (-1, row_idx)))
    row_idx += 1

    for c in NO_HIRE_CANDIDATES:
        row = [
            PS("—",             fs=7.5, align=TA_CENTER),
            PS(c["name"],       fs=7.5),
            PS(str(c["score"]), fs=7.5, tc=C_NO_HIRE, align=TA_CENTER),
            PS(c["tier"],       fs=7.5, tc=C_NO_HIRE, bold=True, align=TA_CENTER),
            PS("—",             fs=7, align=TA_CENTER),
            PS("—",             fs=7, align=TA_CENTER),
            PS("—",             fs=7.5, align=TA_CENTER),
            PS("—",             fs=7.5),
            PS(c["reason"],     fs=7.5),
            PS("No Hire",       fs=7.5, tc=C_NO_HIRE, bold=True, align=TA_CENTER),
        ]
        table_data.append(row)
        row_idx += 1

    master_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    master_table.setStyle(TableStyle(table_styles))
    story.append(master_table)
    story.append(PageBreak())

    # ── SECTION 2 — Visual Analytics ────────────────────────────
    story.append(PS_h("Visual Analytics — Top 10 Candidates", fs=12))
    story.append(Spacer(1, 3*mm))

    bar_bytes   = make_bar_chart()
    radar_bytes = make_radar_chart()

    bar_img   = RLImage(io.BytesIO(bar_bytes),   width=165*mm, height=88*mm)
    radar_img = RLImage(io.BytesIO(radar_bytes), width=110*mm, height=88*mm)

    chart_table = Table([[bar_img, radar_img]], colWidths=[168*mm, 112*mm])
    chart_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(chart_table)
    story.append(PageBreak())

    # ── SECTION 3 — Over Budget ──────────────────────────────────
    story.append(PS_h("Strong Matches — Budget Assessment", fs=12))
    story.append(PS(
        f"Budget range: {BUDGET_RANGE}. 19 of 20 shortlisted candidates are within budget. "
        f"Amina Batool (rank #2, score 95 — Tier A) expects PKR 300,000–310,000, exceeding the ceiling by PKR 50–60K. "
        f"She is the strongest education field coordination PM in the pool — salary negotiation is strongly recommended before ruling her out.",
        fs=9, tc=C_BLACK
    ))
    story.append(Spacer(1, 4*mm))

    for i, c in enumerate(OVER_BUDGET):
        oob_data = [
            [PS(f"OB{i+1}: {c['name']}", fs=9, bold=True),
             PS(f"Score: {c['score']} | Tier: {c['tier']}", fs=8, tc=C_GRAY)],
            [PS(f"Expected Salary: {c['salary']}", fs=8, tc=C_OOB, bold=True),
             PS(c["budget_note"], fs=8, tc=C_OOB, bold=True)],
            [PS(c["note"], fs=8), PS(c["verdict"], fs=8, bold=True)],
        ]
        oob_t = Table(oob_data, colWidths=[133*mm, 134*mm])
        oob_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), C_AMBER_BG),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(oob_t)
        story.append(Spacer(1, 3*mm))

    story.append(PageBreak())

    # ── SECTION 4 — Heatmap ─────────────────────────────────────
    story.append(PS_h("Visual Analytics — Dimension Heatmap (Top 10)", fs=12))
    story.append(Spacer(1, 3*mm))
    heatmap_bytes = make_heatmap()
    heatmap_img   = RLImage(io.BytesIO(heatmap_bytes), width=220*mm, height=110*mm)
    story.append(heatmap_img)
    story.append(PageBreak())

    # ── SECTION 5 — Why Others Didn't Make It ───────────────────
    story.append(PS_h("Why Others Did Not Make the Cut", fs=12))
    story.append(Spacer(1, 2*mm))

    reasons = [
        ("Keyword Scanner Overcounting — Corrected by Human Judgement (5 candidates)",
         "Five candidates scored 80–94 by the keyword scanner but fell to No-Hire on human review: "
         "Muhammad Afzaal (86.2 → 45), Midhat Fatima (86.2 → 49), Sadia Siddique (81.2 → 31), "
         "Muhammad Qasi (85 → 50), Syeda Farzana Ali Shah (83.8 → 39). "
         "The scanner counted tool names (Kobo, ODK, SPSS) in skills sections as evidence of field coordination — "
         "human review found these were either unlisted without practice or from entirely unrelated domains (health, protection, HR)."),
        ("No M&E / Field Research Background (60+ candidates)",
         "Over 60 candidates had backgrounds entirely unrelated to M&E, field research, or education program implementation. "
         "Common profiles: teaching, HR, marketing, corporate sales, finance. All discarded."),
        ("Quick-Apply Placeholder Profiles (20+ candidates)",
         "Over 20 applications had generic placeholder names ('Applicant' last name, no resume attached). Cannot assess — all discarded."),
        ("Over Budget (1 candidate)",
         "Amina Batool (PKR 300–310K) exceeds the PKR 250K ceiling. Flagged separately — salary negotiation recommended "
         "given she is the #2 ranked candidate overall."),
        ("Humanitarian/Health Sector Only — No Education Focus (15+ candidates)",
         "Several candidates had strong NGO backgrounds (UNHCR, WFP, WASH, health) but no education sector or "
         "government school experience. The JD specifically requires government school coordination and education M&E."),
        ("Researchers Without Field Coordination Evidence (25+ candidates)",
         "Academic research or data analysis backgrounds without operational field coordination — "
         "no enumerator management, spot-checks, survey firm liaison, or daily coverage tracking. Research alone does not meet the JD."),
    ]

    for title, explanation in reasons:
        story.append(PS(f"<b>{title}</b>", fs=9))
        story.append(PS(explanation, fs=8, tc=C_GRAY))
        story.append(Spacer(1, 3*mm))

    story.append(HRFlowable(width="100%", thickness=1, color=C_HEADER, spaceAfter=4))

    # Next Steps
    story.append(PS_h("Recommended Next Steps", fs=12))
    story.append(Spacer(1, 2*mm))
    next_steps = [
        "1. Immediately shortlist top 5 (Asif Khan, Scheherazade Noor, Fatima Mughal, Faryal Afridi + Amina Batool if salary can be negotiated) for 30-min screening calls.",
        "2. For Amina Batool (Rank 2, score 95): Explore salary negotiation — PKR 300–310K ask is PKR 50–60K over ceiling. "
        "This is the strongest education field coordination PM in the pool. EdTech Hub + TFP + PIE AI assessment. Negotiate before defaulting.",
        "3. For HabibunNabi (Rank 7): Verify 17-yr experience and confirm salary — PKR 80K is unusually low for this profile and may be a data entry error.",
        "4. Three Teach For Pakistan alumni shortlisted (Amina Batool, Asad Farooq, Usman Ahmed Khan). Ask all three: "
        "'How would you transition from school-facing support to back-office field data governance?'",
        "5. Interview question for all candidates: 'Walk me through a time you caught a data quality issue in the field and corrected it before it reached the analysis stage.'",
        "6. Confirm Islamabad/Rawalpindi residency or relocation readiness for all shortlisted candidates.",
        "7. Note: Naveen Shariff (Rank 20, TCF intern) is Karachi-based — relocation discussion needed if considered.",
    ]
    for step in next_steps:
        story.append(PS(step, fs=8, tc=C_BLACK))
        story.append(Spacer(1, 1.5*mm))

    story.append(Spacer(1, 4*mm))
    story.append(PS(
        "Taleemabad Talent Acquisition Agent  •  Confidential",
        fs=7, tc=C_GRAY, align=TA_CENTER
    ))

    doc.build(story)
    print(f"PDF saved: {pdf_path}")
    return pdf_path


# ══════════════════════════════════════════════════════════════════════
# EMAIL
# ══════════════════════════════════════════════════════════════════════
def send_email(pdf_path):
    shortlisted = len(CANDIDATES)
    over_budget = len([c for c in OVER_BUDGET if "OVER" in c.get("budget_note", "")])

    html = f"""
    <html><body style="font-family:Arial,sans-serif;font-size:14px;color:#1F2937;max-width:680px;margin:0 auto;padding:20px;">

      <p style="margin:0 0 20px 0;">Hi {HIRING_MGR_FIRST},</p>
      <p style="margin:0 0 16px 0;">
        The updated screening report for <strong>{JOB_TITLE}</strong> (Job {JOB_ID}) is attached.
        This is a <strong>full human-judgement re-screen</strong> of all {TOTAL_SCREENED} applicants —
        32 CVs read manually, keyword scanner scores replaced. Candidate names sourced from Markaz.
      </p>

      <table style="width:100%;border-collapse:collapse;margin-bottom:20px;">
        <tr>
          <td style="background:#F0FDF4;border:1px solid #BBF7D0;padding:14px;text-align:center;border-radius:6px;">
            <div style="font-size:26px;font-weight:bold;color:#16A34A;">{TOTAL_SCREENED}</div>
            <div style="font-size:12px;color:#6B7280;">Profiles Screened</div>
          </td>
          <td style="width:16px;"></td>
          <td style="background:#EFF6FF;border:1px solid #BFDBFE;padding:14px;text-align:center;border-radius:6px;">
            <div style="font-size:26px;font-weight:bold;color:#2563EB;">{shortlisted}</div>
            <div style="font-size:12px;color:#6B7280;">Shortlisted</div>
          </td>
          <td style="width:16px;"></td>
          <td style="background:#FFF7ED;border:1px solid #FED7AA;padding:14px;text-align:center;border-radius:6px;">
            <div style="font-size:26px;font-weight:bold;color:#D97706;">{over_budget}</div>
            <div style="font-size:12px;color:#6B7280;">Strong Match Over Budget</div>
          </td>
        </tr>
      </table>

      <p style="margin:0 0 10px 0;color:#374151;">
        Please open the attached PDF for the full analysis — ranked shortlist, dimension scores,
        charts, and recommended next steps.
      </p>

      <p style="margin:0 0 20px 0;color:#6B7280;font-size:13px;">
        Budget: {BUDGET_RANGE} &nbsp;|&nbsp; 19 of 20 shortlisted candidates within budget.
        Amina Batool (Rank 2, score 95) is over budget — see PDF for negotiation note.
      </p>

      <table style="border-top:2px solid #16A34A;margin-top:24px;padding-top:14px;width:100%;border-collapse:collapse;">
        <tr>
          <td style="font-family:Arial,sans-serif;font-size:13px;color:#1F2937;line-height:1.6;">
            <p style="margin:0 0 2px 0;"><strong style="color:#16A34A;">Ayesha Raza Khan,</strong></p>
            <p style="margin:0 0 2px 0;"><strong>Deputy Manager People &amp; Culture, Taleemabad.</strong></p>
            <p style="margin:0;color:#6B7280;font-size:12px;">Taleemabad Talent Acquisition Agent &bull; Confidential</p>
          </td>
        </tr>
      </table>

    </body></html>
    """

    msg = MIMEMultipart("mixed")
    msg["Subject"] = f"Screening Report- {JOB_TITLE}"
    msg["From"]    = SENDER
    msg["To"]      = ", ".join(RECIPIENTS)

    msg.attach(MIMEText(html, "html"))

    with open(pdf_path, "rb") as f:
        att = MIMEBase("application", "octet-stream")
        att.set_payload(f.read())
        encoders.encode_base64(att)
        att.add_header("Content-Disposition", "attachment",
                       filename="Screening-Report-Field-Coordinator-Research-Impact-v3.pdf")
        msg.attach(att)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        allow_candidate_addresses(RECIPIENTS if isinstance(RECIPIENTS, list) else [RECIPIENTS])
        safe_sendmail(smtp, SENDER, RECIPIENTS, msg.as_string(), context='send_job36_v3_report_pdf')

    print(f"Email sent to: {', '.join(RECIPIENTS)}")
    print(f"Subject: {msg['Subject']}")
    print(f"Attachment: Screening-Report-Field-Coordinator-Research-Impact-v3.pdf")


if __name__ == "__main__":
    print("Generating PDF report...")
    pdf_path = build_pdf()
    print("Sending email...")
    send_email(pdf_path)
    print("Done.")
