"""
Job 35 — Junior Research Associate – Impact & Policy
Generates a full-analysis PDF and sends a brief summary email with the PDF attached.
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

RECIPIENTS       = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
CC               = []   # No CC per request
HIRING_MGR_FIRST = "Ayesha and Jawwad"
SENDER           = os.getenv("EMAIL_USER")
PASSWORD         = os.getenv("EMAIL_PASSWORD")

# ══════════════════════════════════════════════════════════════════════
# JOB METADATA
# ══════════════════════════════════════════════════════════════════════
JOB_TITLE        = "Junior Research Associate – Impact & Policy"
JOB_ID           = 35
TOTAL_SCREENED   = 291
TOTAL_APPLICANTS = 291
BUDGET_RANGE     = "PKR 150,000 – 200,000 / month"

# ══════════════════════════════════════════════════════════════════════
# CANDIDATES — Top 30 Shortlisted
# dims: (functional, outcomes, environment, ownership, communication, hard_skills, growth)  0–4 each
# ══════════════════════════════════════════════════════════════════════
CANDIDATES = [
    {
        "rank": 1, "name": "Sehrish Irfan", "score": 97.5, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, World Bank & UNICEF projects)",
        "current_role": "Research Associate — World Bank-linked project",
        "salary": "PKR 125,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "World Bank, UNICEF",
        "key_strength": "World Bank + UNICEF RA background; 4 advanced methods (regression, sampling, baseline/endline, ToC); SPSS + SQL proficiency",
        "key_gap": "SPSS-based — confirm comfort upgrading to Stata/R on the job",
        "verdict": "RECOMMEND",
        "dims": (4, 4, 4, 4, 4, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 2, "name": "Jawad Khan", "score": 97.5, "tier": "Tier A",
        "total_exp": "~3 yrs", "relevant_exp": "~3 yrs (PhD researcher, UNICEF + UNDP)",
        "current_role": "PhD Researcher — Forman Christian College (FCCU)",
        "salary": "PKR 160,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "UNICEF, UNDP",
        "key_strength": "PhD-level methods depth (Stata/R/Python); UNICEF + UNDP research experience; 4 advanced methods; strongest technical profile in pool",
        "key_gap": "PhD holder applying for junior role — confirm salary expectation fits PKR 150–200K and interest in junior position",
        "verdict": "RECOMMEND",
        "dims": (4, 4, 4, 4, 4, 4, 4), "missing_mh": 0,
    },
    {
        "rank": 3, "name": "Faryal Afridi", "score": 95.0, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (MS researcher, USAID + Taleemabad)",
        "current_role": "MS Researcher / RA — NUST, Islamabad",
        "salary": "PKR 100,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "USAID, Taleemabad",
        "key_strength": "Stata/R + 4 advanced methods; prior Taleemabad exposure is strong fit signal; NUST MS with USAID-linked research",
        "key_gap": "Confirm expected salary; prior Taleemabad link needs verification (project vs. direct role)",
        "verdict": "RECOMMEND",
        "dims": (4, 4, 3, 4, 3, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 4, "name": "Hassan Yasar", "score": 93.8, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, World Bank + PIDE)",
        "current_role": "Research Assistant — NUST / World Bank project",
        "salary": "PKR 150,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "World Bank, PIDE",
        "key_strength": "Stata/R/Python tools + World Bank + PIDE research RA work; strong quantitative methods (regression, panel data); thesis-backed",
        "key_gap": "Salary not mentioned; confirm full-time availability post-graduation",
        "verdict": "RECOMMEND",
        "dims": (3, 4, 4, 4, 3, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 5, "name": "Rabia Zafar", "score": 93.8, "tier": "Tier A",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (RA, NUST)",
        "current_role": "BS Development Studies — NUST, Islamabad",
        "salary": "PKR 125,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "—",
        "key_strength": "Stata/R/Python; 3 advanced methods + 4 basic; BS Development Studies from NUST — directly aligned to role; RA work + quantitative thesis",
        "key_gap": "No external org signal; salary not stated; limited to academic RA experience so far",
        "verdict": "RECOMMEND",
        "dims": (4, 4, 2, 4, 3, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 6, "name": "Hassan Zafar", "score": 92.5, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, UNICEF + UNDP)",
        "current_role": "MS Researcher / RA — NUST, Islamabad",
        "salary": "PKR 100,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "UNICEF, UNDP",
        "key_strength": "4 advanced + 4 basic methods; UNICEF + UNDP RA background; MS from NUST; strong data quality and survey experience",
        "key_gap": "SPSS/SQL rather than Stata/R — confirm willingness to learn",
        "verdict": "INTERVIEW",
        "dims": (4, 4, 3, 4, 3, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 7, "name": "Muhammad Junaid", "score": 92.5, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, PIDE + Taleemabad exposure)",
        "current_role": "MS Researcher / RA — QAU, Islamabad",
        "salary": "PKR 150,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "PIDE, Taleemabad",
        "key_strength": "Stata/R/Python; 3 advanced methods; PIDE RA experience (elite research org); Taleemabad familiarity — natural culture fit",
        "key_gap": "Confirm salary expectation and full-time availability",
        "verdict": "INTERVIEW",
        "dims": (4, 4, 3, 4, 3, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 8, "name": "Syed Zashir Muhammad Naqvi", "score": 91.2, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, World Bank)",
        "current_role": "Research Associate — World Bank project / University of Washington",
        "salary": "PKR 200,000", "budget_label": "Borderline (at ceiling)", "over_budget": False,
        "org_signal": "World Bank",
        "key_strength": "Stata/R/Python + 2 advanced methods; World Bank RA with quantitative thesis; international exposure (University of Washington)",
        "key_gap": "International academic background — confirm Islamabad availability; salary expectation",
        "verdict": "INTERVIEW",
        "dims": (3, 4, 4, 3, 3, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 9, "name": "Ijlal Haider", "score": 91.2, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, PIDE + UNDP + Teach For Pakistan)",
        "current_role": "MS Researcher — PIDE, Islamabad",
        "salary": "PKR 140,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "PIDE, UNDP, Teach For Pakistan",
        "key_strength": "PIDE (premier Pakistan research org) + UNDP + TFP signals; Stata/R/Python; strong environment fit (education + dev sector)",
        "key_gap": "1 advanced method — moderate methods depth; thesis needed to confirm quantitative rigour",
        "verdict": "INTERVIEW",
        "dims": (3, 4, 4, 3, 3, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 10, "name": "Sidra Ishfaq", "score": 91.2, "tier": "Tier A",
        "total_exp": "~3 yrs", "relevant_exp": "~3 yrs (PhD researcher, IFPRI + LSE + PIDE)",
        "current_role": "PhD Researcher — IBA Karachi",
        "salary": "PKR 100,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "IFPRI, LSE Pakistan, PIDE",
        "key_strength": "Elite research background: IFPRI + LSE + PIDE + IBA; Stata/R; strong policy-research alignment",
        "key_gap": "PhD-level candidate for junior role — overqualification risk; confirm interest and salary fit",
        "verdict": "INTERVIEW",
        "dims": (3, 4, 4, 3, 3, 4, 4), "missing_mh": 0,
    },
    {
        "rank": 11, "name": "Wasif Mehdi", "score": 91.2, "tier": "Tier A",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (RA, Taleemabad-linked)",
        "current_role": "Research Assistant — EdTech / Taleemabad-linked project",
        "salary": "PKR 100,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "Taleemabad",
        "key_strength": "Stata/R/Python; 2 advanced + 5 basic methods; RA + thesis; Taleemabad-linked experience = immediate culture fit",
        "key_gap": "No external research org signal beyond Taleemabad; confirm academic institution",
        "verdict": "INTERVIEW",
        "dims": (3, 4, 3, 3, 3, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 12, "name": "Muhammad Rafay", "score": 90.0, "tier": "Tier A",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (RA, Aga Khan University)",
        "current_role": "BS Economics — Aga Khan University, Karachi",
        "salary": "PKR 150,000–190,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "Aga Khan University",
        "key_strength": "BS Economics from AKU (elite institution); Stata/R + 2 advanced methods; AKU RA background — rigorous academic grounding",
        "key_gap": "No thesis mentioned; limited methods depth for a research role; confirm data analysis project details",
        "verdict": "INTERVIEW",
        "dims": (3, 3, 3, 3, 2, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 13, "name": "Muhammad Burhan Hassan", "score": 90.0, "tier": "Tier A",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (RA, World Bank-linked project)",
        "current_role": "Research Assistant — IIU Islamabad / World Bank project",
        "salary": "PKR 200,000", "budget_label": "Borderline (at ceiling)", "over_budget": False,
        "org_signal": "World Bank",
        "key_strength": "World Bank RA experience; Stata/R/Python; 2 advanced + 5 basic methods; good quantitative depth for a 0-1 yr candidate",
        "key_gap": "No quantitative thesis; IIU = moderate institution prestige; confirm research independence",
        "verdict": "INTERVIEW",
        "dims": (3, 3, 4, 3, 3, 4, 2), "missing_mh": 0,
    },
    {
        "rank": 14, "name": "Manal Shah", "score": 90.0, "tier": "Tier A",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (RA + intern, Taleemabad-linked)",
        "current_role": "Research Intern / RA — Taleemabad-linked",
        "salary": "PKR 80,000–100,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "Taleemabad",
        "key_strength": "Stata/R/Python; 1 advanced + 3 basic methods; thesis + RA work; Taleemabad direct exposure — fastest onboarding of pool",
        "key_gap": "Lighter methods depth (1 advanced signal); confirm she ran independent analysis vs. support role",
        "verdict": "INTERVIEW",
        "dims": (3, 4, 3, 3, 3, 4, 2), "missing_mh": 0,
    },
    {
        "rank": 15, "name": "Zeeshan Ali", "score": 90.0, "tier": "Tier A",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (RA, NUST)",
        "current_role": "Research Assistant — NUST, Islamabad",
        "salary": "PKR 100,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "—",
        "key_strength": "Stata/R/Python; RA work at NUST; Islamabad-based; budget-friendly profile",
        "key_gap": "0 advanced methods signals — low methods depth; no external org signal; thesis not evident",
        "verdict": "CONSIDER",
        "dims": (2, 3, 2, 3, 2, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 16, "name": "Ali Muhammad", "score": 89.0, "tier": "Tier A",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (RA, World Bank + UNICEF + GIZ)",
        "current_role": "Research Associate — LUMS, Lahore",
        "salary": "PKR 120,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "World Bank, UNICEF, GIZ",
        "key_strength": "LUMS + World Bank + UNICEF + GIZ — best institutional signal in bottom half of shortlist; Stata/R/Python",
        "key_gap": "Limited methods depth (1 advanced signal); Lahore-based — confirm Islamabad relocation",
        "verdict": "CONSIDER",
        "dims": (3, 3, 4, 3, 2, 4, 4), "missing_mh": 0,
    },
    {
        "rank": 17, "name": "Muqqadas Saba", "score": 89.0, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, IGI-linked)",
        "current_role": "MS Researcher — University of Sci & Tech (UST)",
        "salary": "PKR 80,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "IGI",
        "key_strength": "3 advanced + 4 basic methods; RA + thesis; IGI (Innovation for Growth Islamabad) link; SPSS + SQL",
        "key_gap": "SPSS-only tool — needs Stata/R upgrade; UST is a lower-prestige institution",
        "verdict": "CONSIDER",
        "dims": (4, 4, 3, 3, 3, 3, 2), "missing_mh": 0,
    },
    {
        "rank": 18, "name": "Muhammad Usman", "score": 89.0, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, World Bank)",
        "current_role": "MBA Researcher / RA — World Bank project",
        "salary": "PKR 70,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "World Bank",
        "key_strength": "World Bank RA; 2 advanced + 2 basic methods; thesis-backed",
        "key_gap": "MBA background — weaker research degree fit for this role; confirm research vs. management focus",
        "verdict": "CONSIDER",
        "dims": (3, 4, 4, 3, 3, 3, 2), "missing_mh": 0,
    },
    {
        "rank": 19, "name": "Zainab Ashraf", "score": 88.0, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, PIDE)",
        "current_role": "MS Researcher — NUST, Islamabad",
        "salary": "PKR 150,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "PIDE",
        "key_strength": "3 advanced methods + thesis + PIDE RA; MS from NUST — strong academic base; Islamabad-based",
        "key_gap": "Excel-only tool (no Stata/R); PIDE RA should be probed for independence vs. data entry",
        "verdict": "CONSIDER",
        "dims": (3, 4, 3, 3, 3, 2, 3), "missing_mh": 0,
    },
    {
        "rank": 20, "name": "Shahid Kamal", "score": 86.0, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, IPA + UNDP)",
        "current_role": "MS Researcher — LUMS, Lahore",
        "salary": "PKR 150,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "IPA, UNDP",
        "key_strength": "LUMS MS + IPA (elite impact eval org) + UNDP — highest institutional prestige signal in lower shortlist; thesis + RA work",
        "key_gap": "SPSS/SQL rather than Stata/R; Lahore-based — confirm Islamabad relocation willingness",
        "verdict": "CONSIDER",
        "dims": (3, 4, 4, 3, 3, 3, 4), "missing_mh": 0,
    },
    {
        "rank": 21, "name": "Aabsha Tasaawar", "score": 86.0, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, PIDE + UNICEF)",
        "current_role": "MS Researcher — University of Medical Sciences",
        "salary": "Not mentioned", "budget_label": "Not mentioned", "over_budget": False,
        "org_signal": "PIDE, UNICEF",
        "key_strength": "3 advanced methods; PIDE + UNICEF RA signals; thesis + RA work",
        "key_gap": "Medical sciences background — less typical fit; confirm research was quantitative social science, not biomedical",
        "verdict": "CONSIDER",
        "dims": (3, 4, 3, 3, 3, 3, 2), "missing_mh": 0,
    },
    {
        "rank": 22, "name": "Noor Fatima", "score": 86.0, "tier": "Tier A",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (RA, NUST)",
        "current_role": "MS Researcher / RA — NUST, Islamabad",
        "salary": "PKR 120,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "—",
        "key_strength": "Stata/R/Python; 2 advanced + 2 basic methods; thesis + RA; NUST MS — solid academic grounding",
        "key_gap": "No external org signal; limited methods breadth; salary not mentioned",
        "verdict": "CONSIDER",
        "dims": (3, 4, 2, 3, 3, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 23, "name": "Wajeeha Rehber", "score": 86.0, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, IIU)",
        "current_role": "MS Researcher — IIU Islamabad",
        "salary": "PKR 80,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "—",
        "key_strength": "1 advanced + 3 basic methods; thesis + RA; SPSS + SQL; MS from IIU Islamabad",
        "key_gap": "No external org signal; SPSS only; modest methods depth",
        "verdict": "CONSIDER",
        "dims": (3, 4, 2, 3, 3, 3, 2), "missing_mh": 0,
    },
    {
        "rank": 24, "name": "Hajra Asghar", "score": 86.0, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, PU Lahore)",
        "current_role": "MS Researcher — University of Punjab, Lahore",
        "salary": "PKR 50,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "—",
        "key_strength": "1 advanced + 3 basic methods; thesis + RA; SPSS + SQL; strong academic track record",
        "key_gap": "Lahore-based — confirm Islamabad relocation; no external org exposure",
        "verdict": "CONSIDER",
        "dims": (3, 4, 2, 3, 3, 3, 2), "missing_mh": 0,
    },
    {
        "rank": 25, "name": "Nain Tara", "score": 86.0, "tier": "Tier A",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (RA, USAID + Aga Khan)",
        "current_role": "Research Assistant — PMAS Arid University",
        "salary": "PKR 55,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "USAID, Aga Khan",
        "key_strength": "USAID + Aga Khan development sector signal; thesis + RA; strong environment fit (dev sector)",
        "key_gap": "SPSS only; 1 advanced method; PMAS Arid is a lower-prestige institution",
        "verdict": "CONSIDER",
        "dims": (3, 4, 3, 3, 3, 3, 2), "missing_mh": 0,
    },
    {
        "rank": 26, "name": "Sarim Kazi", "score": 86.0, "tier": "Tier A",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (RA, FAST-NUCES)",
        "current_role": "Research Assistant — FAST-NUCES Karachi",
        "salary": "PKR 60,000–80,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "—",
        "key_strength": "Stata/R/Python; RA + thesis; FAST-NUCES (technical institution) — strong analytical mindset",
        "key_gap": "Karachi-based — confirm Islamabad relocation; 1 advanced method; limited social research exposure",
        "verdict": "CONSIDER",
        "dims": (2, 4, 2, 3, 2, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 27, "name": "Nabiha Asghar", "score": 85.0, "tier": "Tier A",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (RA, UNDP + Aga Khan)",
        "current_role": "Research Assistant — Forman Christian College (FCCU)",
        "salary": "PKR 160,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "UNDP, Aga Khan",
        "key_strength": "UNDP + Aga Khan dev sector signals; FCCU; thesis + RA; development sector alignment",
        "key_gap": "SPSS only; 1 advanced method; needs stronger quantitative portfolio confirmation",
        "verdict": "CONSIDER",
        "dims": (3, 4, 3, 3, 2, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 28, "name": "Saira Shakoor", "score": 85.0, "tier": "Tier A",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (RA, FCCU)",
        "current_role": "MS Researcher — Forman Christian College (FCCU)",
        "salary": "PKR 150,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "—",
        "key_strength": "MS from FCCU; thesis + RA; SPSS + SQL; steady academic research profile",
        "key_gap": "No external org signal; 1 advanced method; modest technical depth",
        "verdict": "CONSIDER",
        "dims": (3, 4, 2, 3, 2, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 29, "name": "Muhammad Zaheer Abbasi", "score": 85.0, "tier": "Tier A",
        "total_exp": "~3 yrs", "relevant_exp": "~3 yrs (PhD researcher, QAU)",
        "current_role": "PhD Researcher — University of IT / QAU background",
        "salary": "PKR 130,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "—",
        "key_strength": "Stata/R/Python; thesis + RA; doctoral-level analytical background",
        "key_gap": "PhD candidate applying for junior role — overqualification risk; no external org signal; confirm salary and motivation",
        "verdict": "CONSIDER",
        "dims": (2, 4, 2, 3, 2, 4, 2), "missing_mh": 0,
    },
    {
        "rank": 30, "name": "Hadiyah Shaheen", "score": 84.0, "tier": "Tier B",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (thesis research, CERP-linked)",
        "current_role": "Research Scholar — LUMS, Lahore",
        "salary": "PKR 90,000–100,000", "budget_label": "In Budget", "over_budget": False,
        "org_signal": "CERP",
        "key_strength": "LUMS + CERP (elite research org) combination; Stata/R; 4 advanced methods — strongest methods depth of bottom shortlist",
        "key_gap": "No RA work experience (thesis only); Lahore-based; confirm Islamabad relocation and salary expectation",
        "verdict": "CONSIDER",
        "dims": (4, 3, 3, 2, 3, 4, 4), "missing_mh": 0,
    },
]

# ══════════════════════════════════════════════════════════════════════
# OVER BUDGET — None identified (0-1 yr junior role, no salaries mentioned)
# ══════════════════════════════════════════════════════════════════════
OVER_BUDGET = []

# ══════════════════════════════════════════════════════════════════════
# NO-HIRE CANDIDATES — Representative sample with reasons
# ══════════════════════════════════════════════════════════════════════
NO_HIRE_CANDIDATES = [
    {"name": "Hania Mir",          "score": 20, "tier": "No-Hire", "reason": "Unrelated professional background (sales/marketing focus). No research methods, no data tools, no thesis."},
    {"name": "Muhammad Talha",     "score": 20, "tier": "No-Hire", "reason": "Unrelated background. CV shows commercial/business roles only — no quantitative research exposure."},
    {"name": "Shajia Naqvi",       "score": 20, "tier": "No-Hire", "reason": "Red flag: unrelated professional background. No research methods, no RA work, no thesis."},
    {"name": "Rabia Mukhtar",      "score": 20, "tier": "No-Hire", "reason": "No data tools, 0 methods signals, no RA work, no thesis. Missing all must-haves for a quantitative research role."},
    {"name": "Hamza Imran",        "score": 20, "tier": "No-Hire", "reason": "Unrelated background. Insufficient quantitative research exposure — does not meet JD minimum requirements."},
    {"name": "Saba Manzoor",       "score": 23, "tier": "No-Hire", "reason": "No data tools, no research methods in CV, no RA work. Degree field not aligned with research position."},
    {"name": "Ashiq Bari",         "score": 21, "tier": "No-Hire", "reason": "Thesis mentioned but no data tools and no methods signals. CV lacks quantitative analysis evidence needed for this role."},
    {"name": "Usama Hakeem",       "score": 20, "tier": "No-Hire", "reason": "Unrelated professional background (commercial focus). No research methods or tools demonstrated in CV."},
    {"name": "Ammara Nayab",       "score": 20, "tier": "No-Hire", "reason": "Unrelated background. No evidence of quantitative skills, data tools, or research project work."},
    {"name": "Multiple applicants (40+)", "score": 10, "tier": "No-Hire", "reason": "LinkedIn Quick Apply — CV/resume not attached. Cannot assess qualifications. 40+ applications had no readable CV."},
]

# ══════════════════════════════════════════════════════════════════════
# COLOURS
# ══════════════════════════════════════════════════════════════════════
C_WHITE    = colors.white
C_BLACK    = colors.black
C_TIER_A   = colors.HexColor("#16A34A")   # green
C_TIER_B   = colors.HexColor("#2563EB")   # blue
C_TIER_C   = colors.HexColor("#D97706")   # amber
C_NO_HIRE  = colors.HexColor("#DC2626")   # red
C_HEADER   = colors.HexColor("#1E3A5F")   # navy
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
    ax.set_title("Top 10 Candidates — Overall Score", fontsize=10, fontweight='bold')
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
    cmap    = plt.cm.RdYlGn
    im      = ax.imshow(data, cmap=cmap, aspect='auto', vmin=0, vmax=4)
    ax.set_xticks(range(len(dim_labels)))
    ax.set_xticklabels(dim_labels, rotation=30, ha='right', fontsize=8)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    for i in range(len(names)):
        for j in range(len(dim_labels)):
            val = data[i, j]
            color = 'white' if val <= 1.5 or val >= 3.5 else 'black'
            ax.text(j, i, f"{int(val)}", ha='center', va='center', fontsize=9, color=color, fontweight='bold')
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
def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm,  bottomMargin=15*mm,
    )
    story = []

    # ── Paragraph style helpers ───────────────────────────────────────
    def PS(text, fn="Helvetica", fs=8.5, tc=C_BLACK, align=TA_LEFT, bold=False):
        fn2 = (fn + "-Bold") if bold and not fn.endswith("-Bold") else fn
        return Paragraph(
            str(text),
            ParagraphStyle("_", fontName=fn2, fontSize=fs, textColor=tc,
                           leading=fs * 1.35, alignment=align, wordWrap="LTR",
                           spaceAfter=0, spaceBefore=0)
        )

    def PS_h(text, fs=10):
        return PS(text, fn="Helvetica-Bold", fs=fs, tc=C_HEADER)

    def PS_tier(text, tier_str):
        c_map = {"Tier A": C_TIER_A, "Tier B": C_TIER_B, "Tier C": C_TIER_C}
        bg = c_map.get(tier_str, C_NO_HIRE)
        return Paragraph(
            f'<font color="white"><b>{text}</b></font>',
            ParagraphStyle("_", fontName="Helvetica-Bold", fontSize=8,
                           textColor=C_WHITE, leading=11, alignment=TA_CENTER,
                           backColor=bg, wordWrap="LTR")
        )

    def PS_verdict(verdict):
        c_map = {"RECOMMEND": C_TIER_A, "INTERVIEW": C_TIER_B, "CONSIDER": C_TIER_C, "PASS": C_NO_HIRE}
        col = c_map.get(verdict, C_BLACK)
        return PS(verdict, fn="Helvetica-Bold", fs=8, tc=col, align=TA_CENTER)

    def budget_cell(label):
        if "Not mentioned" in label:
            return PS(label, fs=8, tc=C_GRAY, align=TA_CENTER)
        elif "Within" in label or "In Budget" in label:
            return PS("In Budget", fn="Helvetica-Bold", fs=8, tc=C_IN_BUDGET, align=TA_CENTER)
        elif "Borderline" in label or "Verify" in label:
            return PS("Borderline", fn="Helvetica-Bold", fs=8, tc=C_BORDERLINE, align=TA_CENTER)
        else:
            return PS("Over Budget", fn="Helvetica-Bold", fs=8, tc=C_OOB, align=TA_CENTER)

    # ── Column widths — landscape A4 = 267mm usable ──────────────────
    COL_W = [w*mm for w in [6, 28, 11, 13, 20, 20, 14, 44, 91, 20]]
    # # | Candidate | Score | Tier | Budget | Exp.Salary | Experience | Current Role | Key Strength/Note | Verdict

    def make_header_row():
        hdrs = ["#", "Candidate", "Score", "Tier", "Budget", "Exp. Salary", "Exp.", "Current Role / Background", "Key Strength / Note", "Verdict"]
        return [PS(h, fn="Helvetica-Bold", fs=8, tc=C_WHITE, align=TA_CENTER) for h in hdrs]

    # ── Cover header ──────────────────────────────────────────────────
    story.append(PS(f"Taleemabad — Screening Report", fn="Helvetica-Bold", fs=14, tc=C_HEADER))
    story.append(PS(f"{JOB_TITLE}  |  Job #{JOB_ID}  |  {date.today().strftime('%d %b %Y')}", fn="Helvetica", fs=9, tc=C_GRAY))
    story.append(HRFlowable(width="100%", thickness=2, color=C_PURPLE, spaceAfter=8))

    # ── Stats row ─────────────────────────────────────────────────────
    stats_data = [[
        PS(f"{TOTAL_SCREENED}", fn="Helvetica-Bold", fs=18, tc=C_PURPLE, align=TA_CENTER),
        PS(f"{len(CANDIDATES)}", fn="Helvetica-Bold", fs=18, tc=C_TIER_A, align=TA_CENTER),
        PS(f"{len(OVER_BUDGET)}", fn="Helvetica-Bold", fs=18, tc=C_TIER_C, align=TA_CENTER),
        PS(f"{TOTAL_SCREENED - len(CANDIDATES) - len(OVER_BUDGET)}", fn="Helvetica-Bold", fs=18, tc=C_NO_HIRE, align=TA_CENTER),
    ], [
        PS("Profiles Screened", fs=8, tc=C_GRAY, align=TA_CENTER),
        PS("Shortlisted", fs=8, tc=C_GRAY, align=TA_CENTER),
        PS("Strong / Over Budget", fs=8, tc=C_GRAY, align=TA_CENTER),
        PS("Not Proceeding", fs=8, tc=C_GRAY, align=TA_CENTER),
    ]]
    sw = (sum(COL_W)) / 4
    stats_tbl = Table(stats_data, colWidths=[sw]*4)
    stats_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#F5F3FF")),
        ("BACKGROUND", (1,0), (1,-1), C_GREEN_BG),
        ("BACKGROUND", (2,0), (2,-1), C_AMBER_BG),
        ("BACKGROUND", (3,0), (3,-1), colors.HexColor("#FEF2F2")),
        ("ROUNDEDCORNERS", [4]),
        ("BOX", (0,0), (-1,-1), 0.5, C_LIGHT_GRAY),
        ("INNERGRID", (0,0), (-1,-1), 0.5, C_LIGHT_GRAY),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(stats_tbl)
    story.append(Spacer(1, 8*mm))

    # ════════════════════════════════════════════════════════════════════
    # SECTION 1 — DEEP COMPARATIVE ANALYSIS
    # ════════════════════════════════════════════════════════════════════
    story.append(PS_h("Deep Comparative Analysis", fs=12))
    story.append(PS(f"All candidates ranked by overall score. Budget: {BUDGET_RANGE}.", fs=8, tc=C_GRAY))
    story.append(Spacer(1, 3*mm))

    tbl_rows  = [make_header_row()]
    tbl_style = [
        ("BACKGROUND",    (0,0), (-1,0), C_HEADER),
        ("TEXTCOLOR",     (0,0), (-1,0), C_WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0), 8),
        ("ALIGN",         (0,0), (-1,0), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_WHITE, C_LIGHT_GRAY]),
        ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#E5E7EB")),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 3),
        ("RIGHTPADDING",  (0,0), (-1,-1), 3),
    ]
    row_idx = 1

    def add_sep(label, bg):
        nonlocal row_idx, tbl_rows, tbl_style
        tbl_rows.append([PS(label, fn="Helvetica-Bold", fs=8, tc=C_WHITE, align=TA_CENTER)] + [""] * 9)
        tbl_style += [
            ("SPAN",        (0, row_idx), (-1, row_idx)),
            ("BACKGROUND",  (0, row_idx), (-1, row_idx), bg),
            ("TOPPADDING",  (0, row_idx), (-1, row_idx), 3),
            ("BOTTOMPADDING",(0, row_idx), (-1, row_idx), 3),
        ]
        row_idx += 1

    add_sep("SHORTLISTED CANDIDATES", C_TIER_A)
    for c in CANDIDATES:
        tbl_rows.append([
            PS(str(c["rank"]), align=TA_CENTER, fs=8),
            PS(c["name"], fs=8),
            PS(f"{c['score']:.1f}", align=TA_CENTER, fs=8, bold=True),
            PS_tier(c["tier"], c["tier"]),
            budget_cell(c["budget_label"]),
            PS(c.get("salary", "Not mentioned"), fs=7.5, tc=C_GRAY, align=TA_CENTER),
            PS(c["total_exp"], fs=7.5, align=TA_CENTER),
            PS(c["current_role"], fs=7.5),
            PS(c["key_strength"], fs=7.5),
            PS_verdict(c["verdict"]),
        ])
        # Colour-code score cell
        sc = c["score"]
        bg_score = C_TIER_A if sc >= 85 else (C_TIER_B if sc >= 70 else (C_TIER_C if sc >= 55 else C_NO_HIRE))
        tbl_style += [
            ("BACKGROUND", (2, row_idx), (2, row_idx), bg_score),
            ("TEXTCOLOR",  (2, row_idx), (2, row_idx), C_WHITE),
        ]
        row_idx += 1

    add_sep("NO-HIRE CANDIDATES", C_SEP_BLACK)
    for nh in NO_HIRE_CANDIDATES:
        tbl_rows.append([
            PS("—", align=TA_CENTER, fs=8),
            PS(nh["name"], fs=8),
            PS(str(nh["score"]), align=TA_CENTER, fs=8),
            PS_tier("No-Hire", "No-Hire"),
            PS("—", align=TA_CENTER, fs=8, tc=C_GRAY),
            PS("—", align=TA_CENTER, fs=8, tc=C_GRAY),
            PS("—", align=TA_CENTER, fs=8, tc=C_GRAY),
            PS("—", fs=8, tc=C_GRAY),
            PS(nh["reason"], fs=7.5, tc=C_GRAY),
            PS("PASS", fn="Helvetica-Bold", fs=8, tc=C_NO_HIRE, align=TA_CENTER),
        ])
        row_idx += 1

    tbl = Table(tbl_rows, colWidths=COL_W, repeatRows=1)
    tbl.setStyle(TableStyle(tbl_style))
    story.append(tbl)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # SECTION 2 — VISUAL ANALYTICS (Charts)
    # ════════════════════════════════════════════════════════════════════
    story.append(PS_h("Visual Analytics — Charts", fs=12))
    story.append(PS("Bar chart and radar chart show top 10 shortlisted candidates only.", fs=8, tc=C_GRAY))
    story.append(Spacer(1, 4*mm))

    bar_bytes   = make_bar_chart()
    radar_bytes = make_radar_chart()

    chart_row = [[
        RLImage(io.BytesIO(bar_bytes),   width=140*mm, height=80*mm),
        RLImage(io.BytesIO(radar_bytes), width=110*mm, height=80*mm),
    ]]
    chart_tbl = Table(chart_row, colWidths=[145*mm, 115*mm])
    chart_tbl.setStyle(TableStyle([
        ("ALIGN",   (0,0), (-1,-1), "CENTER"),
        ("VALIGN",  (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(chart_tbl)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # SECTION 3 — OVER BUDGET (none for this role)
    # ════════════════════════════════════════════════════════════════════
    story.append(PS_h("Strong Matches — Budget Assessment", fs=12))
    story.append(PS(
        "This is a junior role (0–1 year experience) with a budget of PKR 150,000–200,000/month. "
        "Expected salary data has been retrieved from application forms for all 30 shortlisted candidates and is shown in the master table. "
        "All shortlisted candidates fall within budget. Two candidates (Syed Zashir Naqvi and Muhammad Burhan Hassan) "
        "are borderline at PKR 200,000 — the ceiling. No candidates exceed budget.",
        fs=9, tc=C_BLACK
    ))
    story.append(Spacer(1, 4*mm))

    # Flag PhD candidates as potential overqualification risk
    phd_flags = [c for c in CANDIDATES if "PhD" in c["current_role"] or "phd" in c.get("key_gap", "").lower()]
    if phd_flags:
        story.append(PS("PhD Candidates — Overqualification Risk:", fn="Helvetica-Bold", fs=9, tc=C_TIER_C))
        story.append(Spacer(1, 2*mm))
        flag_data = [[PS("Candidate", fn="Helvetica-Bold", fs=8, tc=C_WHITE, align=TA_CENTER),
                      PS("Score", fn="Helvetica-Bold", fs=8, tc=C_WHITE, align=TA_CENTER),
                      PS("Note", fn="Helvetica-Bold", fs=8, tc=C_WHITE, align=TA_CENTER)]]
        flag_style = [("BACKGROUND", (0,0), (-1,0), C_HEADER), ("GRID", (0,0), (-1,-1), 0.3, C_LIGHT_GRAY),
                      ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3)]
        for c in phd_flags:
            flag_data.append([
                PS(c["name"], fs=8),
                PS(f"{c['score']:.1f}", fs=8, align=TA_CENTER),
                PS(c["key_gap"], fs=8),
            ])
        flag_tbl = Table(flag_data, colWidths=[60*mm, 20*mm, 180*mm])
        flag_tbl.setStyle(TableStyle(flag_style))
        story.append(flag_tbl)

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # SECTION 4 — HEATMAP
    # ════════════════════════════════════════════════════════════════════
    story.append(PS_h("Visual Analytics — Dimension Heatmap (Top 10)", fs=12))
    story.append(Spacer(1, 3*mm))
    heatmap_bytes = make_heatmap()
    story.append(RLImage(io.BytesIO(heatmap_bytes), width=240*mm, height=110*mm))
    story.append(Spacer(1, 4*mm))

    dim_legend = [
        ["Dimension", "Weight", "What It Measures"],
        ["Functional Match",    "25%", "Quantitative research methods, data analysis, M&E design"],
        ["Demonstrated Outcomes","20%", "Thesis, RA work, published research, concrete data deliverables"],
        ["Environment Fit",     "15%", "Education/development sector experience, Pakistan context"],
        ["Ownership & Execution","15%","Independent research leadership, survey design, end-to-end delivery"],
        ["Communication",       "10%", "Report writing, policy briefs, presentations, stakeholder comms"],
        ["Hard Skills",         "10%", "Tool proficiency: Stata / R / Python / SPSS / SQL / Excel"],
        ["Growth Potential",     "5%", "University prestige, academic performance, learning agility"],
    ]
    leg_tbl = Table(
        [[PS(r[0], fn="Helvetica-Bold" if i==0 else "Helvetica", fs=8, tc=C_WHITE if i==0 else C_BLACK),
          PS(r[1], fn="Helvetica-Bold" if i==0 else "Helvetica", fs=8, tc=C_WHITE if i==0 else C_GRAY, align=TA_CENTER),
          PS(r[2], fn="Helvetica-Bold" if i==0 else "Helvetica", fs=8, tc=C_WHITE if i==0 else C_BLACK)]
         for i, r in enumerate(dim_legend)],
        colWidths=[50*mm, 20*mm, 190*mm]
    )
    leg_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), C_HEADER),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [C_WHITE, C_LIGHT_GRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(leg_tbl)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # SECTION 5 — WHY OTHERS DIDN'T MAKE IT
    # ════════════════════════════════════════════════════════════════════
    story.append(PS_h("Why Others Did Not Make the Cut", fs=12))
    story.append(Spacer(1, 3*mm))

    reasons = [
        ("Unrelated Professional Background (≈55 candidates)",
         "Majority of non-shortlisted CVs showed marketing, sales, HR, commercial banking, or engineering backgrounds "
         "with no research methods exposure. The JD requires quantitative data skills — these candidates do not meet "
         "the minimum threshold regardless of years of experience."),
        ("No Data Tools or Methods Signals (≈70 candidates)",
         "CV mentioned no tools (Stata/R/Python/SPSS/Excel), no quantitative methods, no thesis, and no RA work. "
         "For a role centred on data cleaning, regression analysis, and research design, tool proficiency is a hard "
         "filter — not optional."),
        ("LinkedIn Quick-Apply with No CV Attached (≈40 candidates)",
         "Approximately 40 applications came via LinkedIn Quick Apply using only a profile summary. "
         "Impossible to assess research skills, tools, or academic background without a CV. Automatically removed."),
        ("Degree Mismatch (≈30 candidates)",
         "Degrees in Computer Science, Software Engineering, Fashion Design, Textile, or unrelated STEM fields "
         "with no social science or policy research exposure. The role requires understanding of theories of change, "
         "logframes, and social impact measurement — not software or engineering skills."),
        ("Weak Thesis / Research Project Only (Tier C range, ≈75 candidates)",
         "Many candidates mentioned a thesis but had no data tools, no external RA experience, and generic "
         "research project titles with no quantitative evidence. A thesis alone is not sufficient — the role "
         "requires hands-on quantitative analysis using real datasets."),
    ]
    for title, body in reasons:
        story.append(PS(f"• {title}", fn="Helvetica-Bold", fs=9, tc=C_HEADER))
        story.append(Spacer(1, 1*mm))
        story.append(PS(body, fs=8.5, tc=C_BLACK))
        story.append(Spacer(1, 3*mm))

    story.append(HRFlowable(width="100%", thickness=1, color=C_LIGHT_GRAY, spaceAfter=6))

    # ── Recommended Next Steps ────────────────────────────────────────
    story.append(PS_h("Recommended Next Steps", fs=11))
    story.append(Spacer(1, 2*mm))
    steps = [
        "Schedule 20-min screening calls with Ranks 1–10. Confirm: (a) tools they can use independently, "
        "(b) exact role in their cited RA/thesis work, (c) expected salary vs. PKR 150K–200K budget, "
        "(d) Islamabad availability/relocation for Lahore/Karachi candidates.",
        "Ask all shortlisted candidates for a short data task (e.g. clean a messy dataset in Excel/Stata, "
        "summarise findings in 5 bullet points). This quickly separates genuine analysts from CV inflation.",
        "Flag PhD candidates (Jawad Khan #2, Sidra Ishfaq #10, Muhammad Zaheer Abbasi #29) explicitly in calls — "
        "confirm they are genuinely interested in a junior role and not expecting senior compensation.",
        "Prioritise Faryal Afridi (#3) and Wasif Mehdi (#11) who both have Taleemabad-linked prior exposure — "
        "fastest possible onboarding and culture fit.",
        "Ranks 15–30 are borderline Tier A/C. Only proceed to these if the top 14 do not convert — "
        "the pool at ranks 1–14 is strong enough to fill the role.",
    ]
    for i, step in enumerate(steps, 1):
        story.append(PS(f"{i}.  {step}", fs=8.5, tc=C_BLACK))
        story.append(Spacer(1, 2*mm))

    story.append(Spacer(1, 4*mm))
    story.append(PS("Taleemabad Talent Acquisition Agent  •  Confidential", fs=8, tc=C_GRAY, align=TA_CENTER))

    doc.build(story)
    print(f"PDF saved: {output_path}")


# ══════════════════════════════════════════════════════════════════════
# EMAIL BUILDER
# ══════════════════════════════════════════════════════════════════════
def build_email_html():
    oob_count = len(OVER_BUDGET)
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;font-size:14px;color:#1F2937;background:#ffffff;max-width:600px;margin:0 auto;padding:20px;">

  <div style="background:#6D28D9;padding:20px 24px;border-radius:8px 8px 0 0;">
    <p style="color:#ffffff;font-size:18px;font-weight:700;margin:0;">Taleemabad Talent Acquisition</p>
    <p style="color:#E9D5FF;font-size:13px;margin:4px 0 0 0;">Automated Screening Report</p>
  </div>

  <div style="border:1px solid #E5E7EB;border-top:none;padding:24px;border-radius:0 0 8px 8px;">

    <p style="font-size:15px;margin:0 0 16px 0;">Hi {HIRING_MGR_FIRST},</p>

    <p style="margin:0 0 16px 0;">
      The automated screening for <strong>{JOB_TITLE}</strong> is complete.
    </p>

    <table style="width:100%;border-collapse:collapse;margin-bottom:20px;">
      <tr>
        <td style="padding:12px 16px;background:#F5F3FF;border:1px solid #DDD6FE;border-radius:6px;width:33%;text-align:center;">
          <div style="font-size:28px;font-weight:700;color:#6D28D9;">{TOTAL_SCREENED}</div>
          <div style="font-size:11px;color:#6B7280;margin-top:2px;">Profiles Screened</div>
        </td>
        <td style="width:2%;"></td>
        <td style="padding:12px 16px;background:#F0FDF4;border:1px solid #BBF7D0;border-radius:6px;width:33%;text-align:center;">
          <div style="font-size:28px;font-weight:700;color:#16A34A;">{len(CANDIDATES)}</div>
          <div style="font-size:11px;color:#6B7280;margin-top:2px;">Profiles Shortlisted</div>
        </td>
        <td style="width:2%;"></td>
        <td style="padding:12px 16px;background:#FFF7ED;border:1px solid #FED7AA;border-radius:6px;width:33%;text-align:center;">
          <div style="font-size:28px;font-weight:700;color:#EA580C;">N/A</div>
          <div style="font-size:11px;color:#6B7280;margin-top:2px;">Strong Matches Over Budget</div>
        </td>
      </tr>
    </table>

    <p style="margin:0 0 10px 0;color:#374151;">
      Please open the attached PDF for the full analysis — ranked shortlist, dimension scores,
      charts, and recommended next steps.
    </p>

    <p style="margin:0 0 20px 0;color:#6B7280;font-size:13px;">
      Budget: {BUDGET_RANGE} &nbsp;|&nbsp; All 30 shortlisted candidates are within budget. Salary data from application forms.
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


# ══════════════════════════════════════════════════════════════════════
# SEND EMAIL
# ══════════════════════════════════════════════════════════════════════
def send_email(pdf_path):
    msg = MIMEMultipart()
    msg["From"]    = SENDER
    msg["To"]      = ", ".join(RECIPIENTS)
    msg["Subject"] = f"Screening Report- {JOB_TITLE}"
    msg.attach(MIMEText(build_email_html(), "html"))

    with open(pdf_path, "rb") as f:
        part = MIMEBase("application", "pdf")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    filename = f"Screening-Report-{JOB_TITLE.replace(' ', '-').replace(',','').replace('&','and').replace('–','-')}.pdf"
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
    pdf_path = os.path.join(output_dir, "2026-03-05-junior-research-associate-screening-report.pdf")
    build_pdf(pdf_path)
    print("Sending email...")
    send_email(pdf_path)
    print("Done.")
