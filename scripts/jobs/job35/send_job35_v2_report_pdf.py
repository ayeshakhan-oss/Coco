"""
Job 35 v2 — Junior Research Associate, Impact & Policy
Human-judgement re-screen: top 35 extracted CVs read manually.
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


PILOT_MODE = True   # True = Ayesha only; False = full send to hiring manager

PILOT_RECIPIENTS  = ["ayesha.khan@taleemabad.com"]
PILOT_CC          = []
PILOT_GREETING    = "Ayesha"

FULL_RECIPIENTS   = ["muzzammil.patel@taleemabad.com"]
FULL_CC           = ["hiring@taleemabad.com"]
FULL_GREETING     = "Muhammad Muzzammil"

RECIPIENTS        = PILOT_RECIPIENTS if PILOT_MODE else FULL_RECIPIENTS
CC_LIST           = PILOT_CC if PILOT_MODE else FULL_CC
HIRING_MGR_FIRST  = PILOT_GREETING if PILOT_MODE else FULL_GREETING

SENDER            = os.getenv("EMAIL_USER")
PASSWORD          = os.getenv("EMAIL_PASSWORD")

JOB_TITLE         = "Junior Research Associate – Impact & Policy"
JOB_ID            = 35
TOTAL_APPLICANTS  = 291
CVS_READ          = 63
BUDGET_RANGE      = "PKR 150,000 – 200,000 / month"

# ══════════════════════════════════════════════════════════════════════
# CANDIDATES — Full human-judgement screen (v2, 2026-03-11)
# 63 CVs read manually against JD. Entry-level role: 0–1 yr exp,
# quantitative analysis (Excel/Stata/R), Bachelor's in Social Sciences /
# Economics / Public Policy / Statistics, Islamabad-based.
# Scored using 7-dimension framework (0–4 each, weighted to 0–100).
# ══════════════════════════════════════════════════════════════════════
CANDIDATES = [
    {
        "rank": 1, "name": "Muhammad Burhan Hassan", "app_id": 1829, "score": 93.0, "tier": "Tier A",
        "total_exp": "2+ yrs", "relevant_exp": "2+ yrs (VIT Global: World Bank EGRA + ASPIRE + PHCIP)",
        "current_role": "Business Operations Associate — VIT Global Pvt. Ltd., Islamabad",
        "salary": "PKR 200,000", "budget_label": "Borderline (at ceiling)", "over_budget": False,
        "key_strength": "JD MATCH: Education-sector M&E specialist at VIT Global — directly relevant to Taleemabad. "
                        "Projects: EGRA (Early Grade Reading Assessment, RSU/World Bank), ASPIRE (teacher training "
                        "evaluation, NIETE/MoE), PHCIP (Punjab Human Capital Investment, World Bank/PSPA), ITA "
                        "library intervention evaluation. Builds CAPI tools in SurveyCTO/Tangerine, trains enumerators, "
                        "manages data QA, writes analytical reports. Full toolkit: SPSS, Stata, R, Python, MAXQDA, "
                        "KoboCollect, Power BI. MS Statistics (IIIU). Islamabad-based. Salary at budget ceiling but justified.",
        "verdict": "STRONGLY RECOMMEND",
        "dims": (4, 4, 4, 4, 4, 4, 3),
    },
    {
        "rank": 2, "name": "Rameez Wasif", "app_id": 1878, "score": 88.0, "tier": "Tier A",
        "total_exp": "~1.5 yrs", "relevant_exp": "~10 months (Tabadlab 4m + World Bank GIS 3m + Legal Aid Research 2m)",
        "current_role": "BS CS Student / Research Intern — Tabadlab + World Bank Project Alumni, Islamabad",
        "salary": "PKR 130,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Tabadlab Data & Policy Intern (Mar–Jun 2025, Islamabad) — mixed-methods analysis for "
                        "$50K DARE-RC project on 18th Amendment education devolution, synthesized data from 30+ interviews, "
                        "ML-based qualitative topic modelling, contributed to final publication. World Bank Data & GIS Member "
                        "(Jun–Aug 2023, $100K GFDRR) — climate-vulnerability framework + QGIS hazard maps for ~20M Karachi "
                        "residents, synthesized 80+ legislative/spatial documents. Legal Aid Society Research Intern (Oct–Nov 2025) "
                        "— judicial/DV case data analysis for $40K CFLI project. IBM Data Engineering + NYIF Risk Management certs. "
                        "BS CS Habib University (CGPA 3.36, 2022–2026). Toolkit: Excel, SQL, Python (pandas, scikit-learn), Power BI, QGIS. "
                        "Strong analytical rigour; evidence of publication-quality research work. Islamabad-based per application. "
                        "NOTE: BS CS (not policy degree) — confirm education research interest. No Stata/R.",
        "verdict": "STRONGLY RECOMMEND",
        "dims": (4, 4, 3, 3, 3, 3, 4),
    },
    {
        "rank": 3, "name": "Fatima Tu Zahra", "app_id": 1774, "score": 86.0, "tier": "Tier A",
        "total_exp": "<1 yr formal", "relevant_exp": "~7 months (PIDE TA 5m + SSDO Research Intern 2m) + MPhil thesis research",
        "current_role": "MPhil Public Policy Graduate — PIDE Islamabad (CGPA 3.96)",
        "salary": "PKR 70,000–80,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: MPhil Public Policy PIDE (CGPA 3.96, 2023–2025, Islamabad) — Pakistan's premier policy "
                        "research institution. Thesis uses mixed-methods (household survey + KIIs/FGDs) on climate disaster "
                        "governance — exactly Taleemabad's methodology. Published peer-reviewed paper in Policy Journal of "
                        "Social Science Review (Vol. 4, Issue 1, 2026). NDU BS Government & Public Policy (CGPA 3.68). "
                        "PIDE Teaching Assistant (Sep 2024–Feb 2025). SSDO Research Intern (Jul–Sep 2022) — policy research "
                        "on child rights/GBV. EPA Admin Intern — EIA reviews, field inspections. "
                        "Toolkit: SPSS + Stata (intermediate), Excel. Islamabad-based. PKR 70–80K — well within budget. "
                        "NOTE: Primarily academic research experience; limited professional M&E output. Assess with a data task.",
        "verdict": "STRONGLY RECOMMEND",
        "dims": (4, 3, 4, 3, 3, 3, 4),
    },
    {
        "rank": 4, "name": "Faryal Afridi", "app_id": 1445, "score": 84.0, "tier": "Tier B",
        "total_exp": "~2 yrs", "relevant_exp": "~14 months (AiD Research Coord. 6m + Taleemabad RA 8m)",
        "current_role": "Research Associate (AMR/Digital Health) — Associates in Social Development, Islamabad",
        "salary": "PKR 100,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Taleemabad Research Assistant (Jan–Aug 2024) — designed ODK surveys, ALP school visits, "
                        "FGDs/KIIs with JICA officials, data analysis reports. AiD Research Coordinator (PYWD/USAID) — "
                        "CAPI instrument design (Kobo), field QA, SPSS analysis, FGD transcription. MS Economics NUST "
                        "(CGPA 3.4, ongoing). Toolkit: R, ODK, SurveyCTO, KoboToolbox, Stata, SPSS, OxMetrics. "
                        "Well within budget (100K). Cross-applicant from Job 36 (Field Coordinator). "
                        "NOTE: Now in AMR/digital health role — confirm continued interest in education research.",
        "verdict": "RECOMMEND",
        "dims": (4, 3, 4, 3, 4, 4, 3),
    },
    {
        "rank": 5, "name": "Rabia Zafar", "app_id": 1569, "score": 84.0, "tier": "Tier B",
        "total_exp": "~2 yrs", "relevant_exp": "~2 yrs (Jhpiego qualitative RA + freelance data analyst)",
        "current_role": "Qualitative Research Associate (Jhpiego) + Freelance Data Analyst, Islamabad",
        "salary": "PKR 125,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: MS Development Studies NUST + MSc Sociology QAU — strong research methodology "
                        "foundation. Qualitative RA at Jhpiego (international health NGO). Freelance data analyst: "
                        "150+ completed jobs, 4.9 rating — strong evidence of independent analytical output quality. "
                        "M&E trainer. Both quantitative and qualitative competencies confirmed. "
                        "NOTE: Jhpiego is health-sector — probe education/policy context interest. "
                        "Freelance track record is unusually strong evidence of execution quality for entry-level.",
        "verdict": "RECOMMEND",
        "dims": (4, 4, 4, 4, 3, 3, 3),
    },
    {
        "rank": 6, "name": "Muhammad Junaid", "app_id": 1592, "score": 84.0, "tier": "Tier B",
        "total_exp": "~18 months", "relevant_exp": "~16 months (Taleemabad 4m + PIDE RA 6m + MoP RA 6m)",
        "current_role": "MPhil Scholar / Research Assistant — PIDE + Taleemabad, Islamabad",
        "salary": "PKR 150,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: MPhil Economics PIDE (CGPA 3.68). Taleemabad Field Enumerator (Feb–May 2025, ODK). "
                        "PIDE Research Assistant (Sep 2024–Feb 2025) — supply chain cost mapping with STATA/Excel, "
                        "survey design, KIIs, FGDs, policy briefs for government stakeholders. Ministry of Planning "
                        "RA (Feb–Aug 2024) — macroeconomic datasets, policy brief writing, automated data workflows. "
                        "Toolkit: STATA, R, SPSS, EViews, Power BI, ODK. Cross-applicant from Job 36. "
                        "Strong match: PIDE calibre + Taleemabad familiarity + econometrics depth.",
        "verdict": "RECOMMEND",
        "dims": (4, 3, 4, 3, 3, 4, 4),
    },
    {
        "rank": 7, "name": "Shahid Kamal", "app_id": 1456, "score": 82.0, "tier": "Tier B",
        "total_exp": "~3.5 yrs", "relevant_exp": "~3 yrs (LUMS RA 1yr + IDEAS data mgmt 7m + SLF project 9m + KAF M&E 9m)",
        "current_role": "M&E Officer (UNDP 'She Plays, She Wins') — Karishma Ali Foundation, Islamabad",
        "salary": "PKR 150,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: MPhil Political Science Summa Cum Laude (FCCU). M&E Officer on UNDP-funded project — "
                        "designs and implements surveys, field monitoring, progress reporting. Data Management Officer "
                        "at IDEAS/LUMS (Women's Political Participation study, Dr. Ali Cheema/Yale) — data collection "
                        "coordination, databases, analytical reports. Research Associate at LUMS (Super Abau MNCH "
                        "platform) — mobilized 1,500+ mothers, reporting. 2 published research papers. "
                        "Cross-applicant from Job 36 (Field Coordinator). Stronger M&E profile than most at entry-level. "
                        "NOTE: ~3 yrs experience — may be borderline over the 0–1 yr JD ceiling; confirm salary alignment.",
        "verdict": "RECOMMEND",
        "dims": (4, 3, 4, 4, 4, 3, 3),
    },
    {
        "rank": 8, "name": "Scheherazade Noor", "app_id": 1429, "score": 80.0, "tier": "Tier B",
        "total_exp": "~1.5 yrs", "relevant_exp": "~17 months (TCF RA 8m + Shirkat Gah 9m)",
        "current_role": "Senior Program Officer — Shirkat Gah Women's Resource Center (field coordination)",
        "salary": "PKR 150,000–175,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: TCF Research Associate (Oct 2024–May 2025, 8m) — led gender study across 30+ schools "
                        "(Sindh/Punjab), trained/supervised 12 data collectors, MAXQDA large-scale analysis of 120+ transcripts, "
                        "policy brief + presentations to national education management conference. Shirkat Gah Senior Program "
                        "Officer (Jun 2025–present, 9m) — fieldwork across 20+ sites, 14 data collectors, donor accountability "
                        "reports. BSc Anthropology & Sociology LUMS. Strong qualitative research design and field management. "
                        "NOTE: No Stata/R — qualitative-only toolkit (MAXQDA, Atlas.ti, Excel). Quantitative gap is significant "
                        "for this JD. Currently Karachi-based — confirm Islamabad relocation readiness.",
        "verdict": "RECOMMEND",
        "dims": (3, 3, 4, 4, 4, 1, 3),
    },
    {
        "rank": 9, "name": "Hadiyah Shaheen", "app_id": 1558, "score": 79.0, "tier": "Tier B",
        "total_exp": "<1 yr", "relevant_exp": "~2 months formal (CERP RCT) + 2 yrs TA (Stata/Econometrics)",
        "current_role": "Fresh Graduate / TA — LUMS, Islamabad",
        "salary": "PKR 90,000–100,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: BS Political Science LUMS (CGPA 3.7) — Best Senior Thesis Award 2025 for causal "
                        "analysis of incumbency effects using Regression Discontinuity Design (5 election cycles, "
                        "panel dataset 1970–2018). Teaching Assistant for Applied Statistics and Econometrics — "
                        "designed and graded Stata + Excel assignments for 300+ students; simplified econometrics "
                        "for humanities students. CERP Research Intern (RCT) — field implementation, digital commerce "
                        "training for 80+ women across 8 districts. Dean's Honor List 6 consecutive semesters. "
                        "Strongest academic credentials + demonstrated Stata competence in entry-level pool. "
                        "NOTE: Minimal formal work experience beyond academia — assess readiness for structured org.",
        "verdict": "RECOMMEND",
        "dims": (3, 4, 4, 3, 3, 3, 4),
    },
    {
        "rank": 10, "name": "Hassan Zafar", "app_id": 1369, "score": 77.0, "tier": "Tier B",
        "total_exp": "~1.5 yrs", "relevant_exp": "~1.5 yrs (IPRS Consulting 1yr + CRSM Consulting 4m)",
        "current_role": "Project Assistant — CRSM Consulting, Rawalpindi/Murree",
        "salary": "PKR 100,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: MS Economics NUST + BS Economics COMSATS. Research Associate at IPRS Consulting "
                        "(Oct 2023–Oct 2024, 1 yr) — cross-sectional and qualitative research designs, KIIs, FGDs, "
                        "thematic analysis, SPSS for data cleaning and analysis, secondary data research for market "
                        "and academic studies. Project Assistant at CRSM Consulting (Sep 2025–Jan 2026) — literature "
                        "reviews, proposal writing, data review. Well within budget. Close to Islamabad. "
                        "NOTE: Murree/RWP-based — confirm Islamabad commute or relocation readiness.",
        "verdict": "INTERVIEW",
        "dims": (3, 3, 4, 3, 3, 3, 3),
    },
    {
        "rank": 11, "name": "Ali Muhammad", "app_id": 1550, "score": 76.0, "tier": "Tier B",
        "total_exp": "~1.5 yrs", "relevant_exp": "~9 months (SIF MEAL 6m + ETI-GB M&E 3m)",
        "current_role": "Program Officer — AKCP, Islamabad",
        "salary": "PKR 120,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: BS International Relations NDU (CGPA 3.69). MEAL Associate at SIF (Sep 2024–Mar 2025) "
                        "— PDM, endline, KAP surveys for WFP/UNHCR/IFAD projects; database management, monitoring "
                        "reports; STATA, NVivo, KOBO, Power BI. M&E Associate at ETI-GB (Jun–Sep 2024) — impact "
                        "study support, EDL assessments, data cleaning, report writing. Strong M&E toolkit for entry "
                        "level. Islamabad G9/1. Within budget. "
                        "NOTE: Humanitarian sector (WFP/UNHCR) — probe education research and policy analytics fit. "
                        "IR degree; confirm quantitative depth with a data task.",
        "verdict": "INTERVIEW",
        "dims": (3, 3, 4, 3, 3, 3, 3),
    },
    {
        "rank": 12, "name": "Dur E Nayab", "app_id": 1816, "score": 75.0, "tier": "Tier B",
        "total_exp": "~9 months", "relevant_exp": "~6 months (Capacity Analytics: M&E analysis with Stata/Jamovi, MCSP)",
        "current_role": "Research Associate — Capacity Analytics, Islamabad",
        "salary": "PKR 120,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: BS Economics IIUI 2025. Capacity Analytics Research Associate (Sep–Oct 2025) + "
                        "Research Intern (May–Aug 2025): M&E analysis on MCSP (Mother & Child Support Program, SSPA) "
                        "across 15 districts using Stata and Jamovi — performance trend identification for monitoring. "
                        "UNDP-funded proposal drafts (x2), policy brief authored on Productive Capacity in Pakistan. "
                        "AHKNCRD Intern (Jul–Sep 2024) — drafted country paper for CIRDAP Conference 2024, 15+ countries. "
                        "Kobo listed in toolkit. Islamabad-based. PKR 120K — well within budget.",
        "verdict": "INTERVIEW",
        "dims": (3, 3, 3, 3, 2, 4, 3),
    },
    {
        "rank": 13, "name": "Mariam Rehman", "app_id": 1944, "score": 75.0, "tier": "Tier B",
        "total_exp": "~3 yrs", "relevant_exp": "~12 months (TCM BD 6m + COPAIR RA 5m + CSCR internships)",
        "current_role": "Communications & BD Associate — The Centrum Media (TCM), Islamabad",
        "salary": "PKR 120,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: NDU BS Peace & Conflict Studies (CGPA 3.75). Self-directed PSLM Stata project — "
                        "gendered employment analysis of 234,558+ individuals (cross-tabulations, provincial comparisons, "
                        "data visualization). Power BI dashboard (15K+ row dataset) and GIS spatial mapping project. "
                        "COPAIR Research Assistant (Oct 2024–Mar 2025) — EmpowerHER national policy dialogue, M&E "
                        "documentation. IRVI Research & Communications Lead (Aug 2024–present) — British Council + "
                        "UNESCO-funded project monitoring and reporting. National Assembly Intern (Aug–Sep 2022) — "
                        "committee documentation, datasets in Excel. CSCR Research Intern (x2, 2023). Islamabad-based. "
                        "NOTE: Most roles are communications/editorial; Stata is project-based — confirm analytical depth.",
        "verdict": "INTERVIEW",
        "dims": (3, 3, 3, 3, 3, 3, 3),
    },
    {
        "rank": 14, "name": "Daniyah Noor", "app_id": 1947, "score": 75.0, "tier": "Tier B",
        "total_exp": "~1.5 yrs", "relevant_exp": "~7 months (CRCC Impact Fellow 4m + MoFA intern 2m + MoHR intern 2m)",
        "current_role": "Impact Fellowship Associate — Climate Resourcing Coordination Center (CRCC), Lahore",
        "salary": "PKR 120,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: LUMS BSc Political Science (2021–2025). Quantitative Research Methods project — "
                        "STATA analysis on arms proliferation + terrorism, 40-country/10-year dataset (UNODC, GTD), "
                        "Z-tests, regression, residual analysis. CRCC Impact Fellowship (Nov 2025–present) — Pakistan's "
                        "first multi-city climate venture mobilization, 100+ startups mapped, diagnostic platform for "
                        "climate impact evaluation. Ministry of Foreign Affairs US Division Intern (Jul–Aug 2023). "
                        "Ministry of Human Rights Internee (Jul–Aug 2019). Policy writing + academic research skills. "
                        "Tools: Stata (academic projects), MS Office. "
                        "NOTE: Lahore-based (LUMS) — confirm Islamabad relocation. Stata use is academic, not professional.",
        "verdict": "INTERVIEW",
        "dims": (3, 3, 3, 3, 3, 3, 3),
    },
    {
        "rank": 15, "name": "Rahima Omar", "app_id": 1777, "score": 75.0, "tier": "Tier B",
        "total_exp": "~2 yrs", "relevant_exp": "~9 months (HBL Microfinance 3m + Planning Commission 3m + Finance Division 3m)",
        "current_role": "Co-Founder The Empowerment Curve / HBL Microfinance Intern (Sep–Nov 2025), Islamabad",
        "salary": "PKR 70,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: COMSATS BS Economics Islamabad (CGPA 3.6, 2021–2025). Stata + R (econometric "
                        "modeling) in skills toolkit. HBL Microfinance Intern (Sep–Nov 2025) — credit risk assessment, "
                        "climate risk analysis post-2025 floods, financial literacy training for underserved communities. "
                        "Planning Commission GoP Intern (Jun–Sep 2023) — policy research, macroeconomic frameworks. "
                        "Finance Division GoP Intern (Jun–Sep 2021). Millennium Fellow (Aug–Dec 2024) — secured PKR 200K+ "
                        "funding, 100+ students, UN Academic Impact recognition. Islamabad-based. PKR 70K, within budget. "
                        "NOTE: Roles lean coordination/advocacy; limited direct quant data work. Assess Stata/R depth.",
        "verdict": "INTERVIEW",
        "dims": (3, 3, 3, 3, 3, 3, 3),
    },
    {
        "rank": 16, "name": "Wasif Mehdi", "app_id": 1771, "score": 73.0, "tier": "Tier B",
        "total_exp": "~1 yr", "relevant_exp": "~1 yr (KIU RA + disaster risk analyst + internees)",
        "current_role": "Fresh MA Graduate — Rawalpindi (MA Economics, UIII Indonesia 2025)",
        "salary": "PKR 100,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: MA Economics UIII Indonesia (CGPA 3.42) — econometrics, time-series analysis. "
                        "BS Economics KIU. 4 peer-reviewed published papers in economics (AJIPS, etc.). "
                        "RA at China Study Center KIU (2021–2022). Tools: Stata, R, EViews, Excel — solid econometric "
                        "toolkit. Rawalpindi-based (close to Islamabad). Entry-level appropriate. Very within budget. "
                        "NOTE: MA from Indonesian university (lower-profile); thesis work primarily time-series "
                        "econometrics — confirm policy analytics interest and fieldwork readiness.",
        "verdict": "INTERVIEW",
        "dims": (3, 3, 4, 3, 2, 3, 4),
    },
    {
        "rank": 17, "name": "Zeeshan Ali", "app_id": 1663, "score": 72.0, "tier": "Tier B",
        "total_exp": "~1 yr", "relevant_exp": "~6 months formal (Vertex 6m + MoP intern 2m)",
        "current_role": "Research Analyst — Vertex Expert Network, Islamabad",
        "salary": "PKR 100,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: BS Economics NUST (Nov 2021–Jun 2025). Research Analyst at Vertex — industry "
                        "research, expert data segmentation, market intelligence. Data Analyst at MAS NUTRINUTS "
                        "(Mar–Aug 2025) — Tableau dashboards, sales KPI tracking. MoP Intern (2 months). "
                        "Exceptional data toolkit for entry level: Tableau, Python, R, STATA, Power BI, SQL, Excel. "
                        "Top 10 out of 500+ teams in Jazz Digital Hackathon. Islamabad DHA. Very within budget. "
                        "NOTE: Current experience is market intelligence / commercial analytics — not policy research. "
                        "Confirm interest in social impact / education research over commercial track.",
        "verdict": "CONSIDER",
        "dims": (3, 3, 4, 3, 2, 4, 3),
    },
    {
        "rank": 18, "name": "Mahnoor Hasan", "app_id": 1701, "score": 71.0, "tier": "Tier B",
        "total_exp": "~2.5 yrs", "relevant_exp": "~1.5 yrs (NUST RA 1yr + Data Analyst 5m)",
        "current_role": "Visiting Faculty — NUST ASAB/SNS, Rawalpindi (Statistics + ML Instructor)",
        "salary": "PKR 70,000–80,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: MS Bioinformatics NUST (CGPA 3.7) + BS Applied Biosciences NUST (3.79). NUST RA "
                        "(Sep 2024–Sep 2025, 1yr) — data collection/management, statistical analysis in Stata/SPSS/Python "
                        "(numpy, scipy, scikit-learn), ML predictive modelling (85–92% accuracy), 4 published/under-review "
                        "papers incl. Nature Mental Health. Data Analyst (electoral integrity research, Sep 2023–Feb 2024). "
                        "Visiting Faculty — teaches Statistics + 5 ML lab courses. Outstanding quant toolkit. "
                        "Rawalpindi-based. PKR 70–80K, within budget. "
                        "NOTE: Domain mismatch — all experience is healthcare/bioinformatics, not development/education. "
                        "Strong quant depth makes her worth interviewing if team can develop domain context.",
        "verdict": "INTERVIEW",
        "dims": (2, 4, 2, 3, 2, 4, 4),
    },
    {
        "rank": 19, "name": "Maria Malik", "app_id": 1949, "score": 71.0, "tier": "Tier B",
        "total_exp": "~3 months formal + MS ongoing", "relevant_exp": "~3 months (HBL Microfinance Data Analyst)",
        "current_role": "MS Economics Student (2023–2025) — NUST; former HBL Microfinance Data Analyst",
        "salary": "PKR 70,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: MS Economics NUST (GPA 3.45, 2023–2025 — advanced econometrics, Stata/R/MATLAB). "
                        "BS Economics Bahria University (GPA 3.84). HBL Microfinance Data Analyst (Jun–Sep 2023, 3m) — "
                        "gap analysis on microloan repayment data, customer segmentation, reported to Head of ADC "
                        "Channels. 3 academic publications (financial development, ML-based OCD risk, population dynamics). "
                        "Google Data Analytics + McKinsey Forward + Google BI certs. Strong quant toolkit: Stata, R, "
                        "MATLAB, Python, SQL, Power BI, Tableau. Islamabad-based. PKR 70K, well within budget. "
                        "NOTE: Very limited work experience (3-month banking internship + academics only). No M&E or "
                        "development-sector background. Assess development sector interest and Stata/R depth.",
        "verdict": "INTERVIEW",
        "dims": (3, 3, 3, 2, 2, 4, 3),
    },
    {
        "rank": 20, "name": "Ayesha Nadeem", "app_id": 1821, "score": 55.0, "tier": "Tier C",
        "total_exp": "~3 months (internships)", "relevant_exp": "~1 month (data analytics intern)",
        "current_role": "Final-year BS Computer Science student — COMSATS University Islamabad (CGPA 3.34)",
        "salary": "PKR 70,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "REFERRAL — Considered per referral + fresher policy. CS background (not policy/research domain): "
                        "Data Analytics Intern at ELevvo Pathways (Jul 2025, 1m) — Power BI dashboards, RFM segmentation, "
                        "sales data analysis. Strong Python/pandas toolkit and 3.34 CGPA. General Secretary COMSATS "
                        "Literary Society. Location: Wah Cantt (commutable to Islamabad). PKR 70K — well within budget. "
                        "NOTE: No Stata/R, no M&E or policy research exposure. Domain mismatch with JRA role; added as "
                        "referral candidate pending hiring team discretion.",
        "verdict": "INTERVIEW (Referral)",
        "dims": (2, 2, 2, 3, 2, 2, 3),
    },
]

# ══════════════════════════════════════════════════════════════════════
# OVERQUALIFIED — Strong JD match but significantly above entry-level
# ══════════════════════════════════════════════════════════════════════
OVER_BUDGET = [
    {
        "name": "Jawad Khan", "app_id": 1729, "score": 87.0, "tier": "Tier A",
        "salary": "PKR 160,000",
        "budget_note": "IN BUDGET — but massively overqualified (PhD, 7+ yrs)",
        "note": "PhD Scholar (PIDE) + UNICEF/UNDP/UNHCR M&E evaluator, 7+ years development research, 18+ published papers. "
                "Expected salary PKR 160K is technically within budget — but this is PhD-level talent applying for an entry-level role. "
                "JD match score: 87 (Tier A). The concern is retention: Taleemabad would be underutilizing him and he would likely leave quickly. "
                "Cross-applicant from Job 36 (Field Coordinator). If hiring team wants research depth immediately, he is worth a conversation — "
                "but clarify whether a JRA scope genuinely fits his trajectory.",
        "verdict": "FLAG — Overqualified (discuss scope fit)",
    },
    {
        "name": "Sidra Ishfaq", "app_id": 1902, "score": 85.0, "tier": "Tier A",
        "salary": "PKR 100,000",
        "budget_note": "IN BUDGET — but overqualified (PhD, 8+ yrs Senior Researcher)",
        "note": "PhD Economics PIDE (CGPA 3.80). Senior Research Officer at Health Services Academy, 8+ years research, "
                "7+ publications, HEC IRSIP scholarship winner. Expected salary PKR 100K is far below her likely market rate — "
                "this may be a misentry or she is actively seeking a role change. JD match score: 85 (Tier A). "
                "If the salary is accurate, worth a quick conversation to understand motivation — but ensure she is not using this "
                "as a temporary placeholder while job-hunting elsewhere.",
        "verdict": "FLAG — Overqualified (verify salary & motivation)",
    },
    {
        "name": "Sehrish Irfan", "app_id": 1514, "score": 84.0, "tier": "Tier B",
        "salary": "PKR 1,250,000",
        "budget_note": "OUT OF BUDGET — expects PKR 1.25M vs. PKR 200K ceiling",
        "note": "Senior Research Analyst at Reneergia LLC (World Bank/FAO projects, Jul 2024–present). MPhil Public Policy PIDE + "
                "MS Economics. 5–7 yrs relevant experience. Expected salary PKR 1,250,000 — 6x the budget ceiling. "
                "Not viable for this role at this budget. Strong profile for a senior research role if such an opening exists.",
        "verdict": "FLAG — Out of Budget (1.25M vs 200K ceiling)",
    },
    {
        "name": "Huma Jehangir", "app_id": 1841, "score": 91.0, "tier": "Tier A",
        "salary": "PKR 250,000–300,000",
        "budget_note": "OUT OF BUDGET — expects PKR 250–300K vs. PKR 200K ceiling",
        "note": "MPhil Anthropology QAU + BS Behavioural Sciences Gold Medalist (KIU). OPM Consultant (Sep 2025–Feb 2026) "
                "— child labour eradication policy, costed action plans (Sindh/Balochistan/ICT). PYCA Program Implementation Lead "
                "(Sep 2023–Aug 2025, 2 yrs) — national trans fats public health advocacy, 70M+ engagement, stakeholder "
                "management with parliamentarians. RSPN Young Dev Professional (Apr–Aug 2023) — field data collection, "
                "beneficiary interviews in Balochistan. Islamabad-based. JD match score: 91 (Tier A). "
                "Expected salary PKR 250–300K is 50–100K above the PKR 200K budget ceiling. "
                "Strong candidate for a mid-level research role; not viable at this JRA budget.",
        "verdict": "FLAG — Out of Budget (250–300K vs 200K ceiling)",
    },
]

# ══════════════════════════════════════════════════════════════════════
# NO-HIRE CANDIDATES — Representative sample
# ══════════════════════════════════════════════════════════════════════
NO_HIRE_CANDIDATES = [
    {"name": "Ijlal Haider (1730)",          "score": 54, "tier": "No-Hire",
     "reason": "MPhil Pakistan Studies QAU. TFP Fellow (Jul 2025–present) = TEACHING ROLE, not research. "
               "PIDE RA 9 months (Mapping Social Protection — basic) is the only relevant exp. "
               "Domain is political science/Pakistan studies — not economics, statistics, or policy analytics. "
               "R skills listed as basic. Fails the quantitative analysis must-have."},
    {"name": "Manal Shah (1649)",            "score": 62, "tier": "Tier C",
     "reason": "BA International Relations NDU. Research at ISSA (security think tank, 3 months) + Research Intern (3 months). "
               "Domain is security/strategic studies — not social science data analytics or policy impact research. "
               "Lists SPSS/STATA but no evidence of hands-on use in CV. Short tenures. Not a fit for Impact & Policy JRA."},
    {"name": "Muqqadas Saba (1532)",         "score": 62, "tier": "Tier C",
     "reason": "MSc Psychology CUST (3.83). RA at CUST (mental health HEC project, Feb 2025–present). "
               "Domain: psychology and mental health — not economics/policy/impact analytics. SPSS only. "
               "Qualitative FGDs and thematic analysis are solid but wrong domain for this role."},
    {"name": "Muhammad Usman (1512)",        "score": 67, "tier": "Tier C",
     "reason": "BS Sociology QAU (3.5). Research Executive at Ipsos (6 months) — KIIs, proposal development, QA/QC. "
               "Ipsos is a strong firm but work is market research, not development-sector policy analytics. "
               "SPSS only — no Stata or R. Sociology degree is adjacent but quantitative depth is limited."},
    {"name": "Hajra Asghar (1765)",          "score": 38, "tier": "No-Hire",
     "reason": "MPhil Management Sciences QAU. Currently Visiting Lecturer (2024–2026). "
               "Domain: business/marketing/customer experience research. Tools: SPSS, AMOS — management science focus. "
               "Not relevant to impact/policy research analytics. Teaching career trajectory, not policy research."},
    {"name": "Noor Fatima (1696)",           "score": 32, "tier": "No-Hire",
     "reason": "MS Governance & Public Policy NUST. GPP degree is relevant but all work experience is marketing/e-commerce "
               "(Batik, CyberVision, Pinkfly). Zero research or data analytics work history post-graduation. "
               "Despite strong academic background, career trajectory is fully commercial — not policy research."},
    {"name": "Muhammad Rafay (1820)",        "score": 40, "tier": "No-Hire",
     "reason": "BS Economics IBA Gold Medal, CGPA 3.87. UNICEF RA 4 months + AKU-IGHD RA 6 months. "
               "Would be a strong candidate but LOCATION: Karachi — relocation to Islamabad would be required. "
               "Current role (House of Habib Management Trainee) suggests corporate career trajectory. "
               "Consider only if relocation confirmed."},
    {"name": "Hassan Yasar (1899)",          "score": 56, "tier": "Tier C",
     "reason": "MSc Agricultural Economics. LOCATION: Multan — not Islamabad or nearby. "
               "Domain: agriculture sector research, rural surveys. Not the policy/education impact focus needed. "
               "Location is a deal-breaker for this in-office role."},
    {"name": "Sarim Kazi (1487)",            "score": 25, "tier": "No-Hire",
     "reason": "BS Business Analytics NUCES — still an undergraduate student (2022–2026). "
               "Experience is internship-level (3 short tech/data internships in summer 2025). "
               "Cannot be considered for a full-time professional role at this stage."},
    {"name": "Muhammad Zaheer Abbasi (1725)", "score": 10, "tier": "No-Hire",
     "reason": "PhD + PostDoc in Hydrology/Geosciences (Lanzhou University). Assistant Professor level. "
               "Domain: fluid mechanics, groundwater, environmental geology — entirely unrelated. "
               "Not suitable for a social science policy analytics role."},
    {"name": "Saira Shakoor (1855)",         "score": 12, "tier": "No-Hire",
     "reason": "MPhil Physical Chemistry QAU. Program Coordinator at Aspire/PIASS colleges (Sep 2017–Jun 2024). "
               "Chemistry researcher turned college administrator. No economics, data analytics, or policy background."},
    {"name": "Hanniya Fatima (1863)",        "score": 15, "tier": "No-Hire",
     "reason": "BS Software Engineering Iqra University. IT roles at PSEB (QA testing, IT operations). "
               "Software/IT domain — no social science, policy research, or development sector background."},
    {"name": "Syeda Kainat Bukhari (1417)", "score": 42, "tier": "No-Hire",
     "reason": "BS/MPhil English Literature & Linguistics (COMSATS + Univ. of Poonch). 6+ yrs experience but as: "
               "Field Enumerator (VTT Global/DAI/Orenda), Admin Manager (hostel), Visiting Lecturer, Army School Teacher. "
               "Tools listed: SurveyCTO, Kobo, TEACH Tool (World Bank cert.) — but all used in data COLLECTION roles, "
               "not analysis. Current role: Social Media Officer. No Stata/R/SPSS analysis work. "
               "Scanner overscored on M&E keywords; human read reveals field/admin career, not analytical research."},
    {"name": "Sadia Siddique (1478)",       "score": 38, "tier": "No-Hire",
     "reason": "MBA HRM + MS Project Management (ongoing, IIUI). 10+ yrs professional experience but: Recruitment & "
               "Operations Manager (2012–2014), home-based food business founder (2017–2024). "
               "Current role: Data Analyst at IPOR (2025) + IIUI academic support. Tools: SPSS, NVivo, SmartPLS. "
               "No Stata/R. HR and project management career — not policy/impact research. "
               "MS thesis on AI in Agile Project Management — business focus, not development sector."},
    {"name": "Hamza Abbasi (1888)",         "score": 45, "tier": "No-Hire",
     "reason": "BBA Iqra University (final year, expected Feb 2026). Research is academic/AI-focused: "
               "PLS-SEM on consumer behavior (marketing), GenAI detection (RoBERTa), XAI for agriculture. "
               "Campus Ambassador (FirstPassAI), Teaching Assistant (Data Science). "
               "No policy/development-sector M&E work; still enrolled as undergraduate. "
               "Strong data science toolkit (Python, R, SQL) but entirely wrong domain and not yet graduated."},
    {"name": "Naima Memoon (1627)",         "score": 48, "tier": "No-Hire",
     "reason": "BA Social Sciences & Liberal Arts IBA Karachi (2020–2024). Research Associate IHSR (Jan 2024, 1m) — "
               "constitutional/political research. TA IBA (Feb 2024–Dec 2025) — Pakistan History, Sociology, Islamic Politics. "
               "Research Enumerator SBP (Oct 2022–Apr 2023) — consumer/business confidence surveys. "
               "LOCATION: Karachi — not Islamabad. No Stata/R/quantitative analytics tools listed. "
               "Teaching track, not research analytics. Scanner overscored on 'research' and 'qualitative' keywords."},
    {"name": "Talha Iftikhar (1758)",       "score": 35, "tier": "No-Hire",
     "reason": "BS Data Science NUCES (Expected 2026 — still enrolled). Intern at Protect Lab (Python/security tools) "
               "and Digital Empowerment Network (AI/ML, ANN, CNN). Final Year Project: AI travel itinerary platform. "
               "Domain: AI/ML/cybersecurity — not policy, development sector, or social science research. "
               "No M&E, survey, or fieldwork experience. Not yet graduated from undergraduate."},
]

# ══════════════════════════════════════════════════════════════════════
# COLOURS
# ══════════════════════════════════════════════════════════════════════
C_WHITE      = colors.white
C_BLACK      = colors.black
C_TIER_A     = colors.HexColor("#16A34A")
C_TIER_B     = colors.HexColor("#2563EB")
C_TIER_C     = colors.HexColor("#D97706")
C_NO_HIRE    = colors.HexColor("#DC2626")
C_HEADER     = colors.HexColor("#1E3A5F")
C_PURPLE     = colors.HexColor("#6D28D9")
C_GREEN_BG   = colors.HexColor("#F0FDF4")
C_BLUE_BG    = colors.HexColor("#EFF6FF")
C_AMBER_BG   = colors.HexColor("#FFFBEB")
C_GRAY       = colors.HexColor("#6B7280")
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
    top10  = CANDIDATES[:10]
    names  = [c["name"].split()[-1] + ", " + c["name"].split()[0] for c in top10]
    scores = [c["score"] for c in top10]
    tier_colors = []
    for c in top10:
        if c["tier"] == "Tier A":   tier_colors.append("#16A34A")
        elif c["tier"] == "Tier B": tier_colors.append("#2563EB")
        elif c["tier"] == "Tier C": tier_colors.append("#D97706")
        else:                       tier_colors.append("#DC2626")

    fig, ax = plt.subplots(figsize=(9, 5))
    y_pos = range(len(names))
    bars  = ax.barh(list(y_pos), scores, color=tier_colors, edgecolor='white', height=0.6)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Score (0–100)", fontsize=8)
    ax.set_title("Top 10 Candidates — Human-Judgement Score (v2)", fontsize=10, fontweight='bold')
    ax.set_xlim(0, 110)
    ax.axvline(x=85, color='#16A34A', linestyle='--', alpha=0.7, linewidth=1.2, label='Tier A (85)')
    ax.axvline(x=70, color='#2563EB', linestyle='--', alpha=0.7, linewidth=1.2, label='Tier B (70)')
    ax.axvline(x=55, color='#D97706', linestyle='--', alpha=0.7, linewidth=1.2, label='Tier C (55)')
    for bar, score in zip(bars, scores):
        ax.text(score + 1, bar.get_y() + bar.get_height() / 2, f"{score}", va='center', fontsize=8)
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
    top10      = CANDIDATES[:10]
    names      = [c["name"] for c in top10]
    dim_labels = ["Functional", "Outcomes", "Environment", "Ownership", "Communication", "Hard Skills", "Growth"]
    data       = np.array([list(c["dims"]) for c in top10], dtype=float)

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
    pdf_path = f"output/{date.today()}-junior-research-associate-impact-policy-v2-screening-report.pdf"
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
        f"CVs Manually Read: {CVS_READ}  |  Shortlisted: {len(CANDIDATES)}  |  "
        f"Overqualified Flags: {len(OVER_BUDGET)}  |  "
        f"Budget: {BUDGET_RANGE}  |  Date: {date.today()}  |  Method: Human-Judgement v2",
        fs=8, tc=C_GRAY
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_HEADER, spaceAfter=6))
    story.append(Spacer(1, 3*mm))

    # ── SECTION 1 — Deep Comparative Analysis ─────────────────────
    story.append(PS_h("Deep Comparative Analysis — All Screened Candidates", fs=12))
    story.append(PS(
        f"Master table shows all {len(CANDIDATES)} shortlisted candidates + overqualified flags + representative no-hire sample. "
        f"Scored using 7-dimension human-judgement framework — all {CVS_READ} extracted CVs read manually against the JD. "
        f"Keyword scanner scores replaced. JD requirement: 0–1 yr exp, quant tools (Excel/Stata/R), "
        f"Bachelor's in Social Sciences / Economics / Public Policy / Statistics, Islamabad-based.",
        fs=8, tc=C_GRAY
    ))
    story.append(Spacer(1, 3*mm))

    # Column widths — 267mm usable landscape A4
    col_widths = [6*mm, 28*mm, 11*mm, 13*mm, 22*mm, 22*mm, 14*mm, 40*mm, 91*mm, 20*mm]

    header_row = [
        PS("#",             fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
        PS("Candidate",     fs=7.5, tc=C_WHITE, bold=True),
        PS("Score",         fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
        PS("Tier",          fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
        PS("Budget",        fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
        PS("Exp. Salary",   fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
        PS("Experience",    fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
        PS("Background / Current Role", fs=7.5, tc=C_WHITE, bold=True),
        PS("Key Strength / Why Not Shortlisted", fs=7.5, tc=C_WHITE, bold=True),
        PS("Verdict",       fs=7.5, tc=C_WHITE, bold=True, align=TA_CENTER),
    ]

    table_data   = [header_row]
    table_styles = [
        ('BACKGROUND',    (0, 0), (-1, 0), C_HEADER),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [C_WHITE, C_LIGHT_GRAY]),
        ('GRID',          (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D5DB")),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING',   (0, 0), (-1, -1), 3),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 3),
        ('TOPPADDING',    (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]

    row_idx = 1

    # Separator — Shortlisted
    sep_row = [PS("SHORTLISTED", fs=7, tc=C_WHITE, bold=True, align=TA_CENTER)] + [""] * 9
    table_data.append(sep_row)
    table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), C_SEP_GREEN))
    table_styles.append(('SPAN',       (0, row_idx), (-1, row_idx)))
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
        if "STRONGLY" in vc:    verd_col = C_TIER_A
        elif "RECOMMEND" in vc: verd_col = C_TIER_A
        elif "INTERVIEW" in vc: verd_col = C_TIER_B
        else:                   verd_col = C_GRAY

        app_id_str = f"App #{c.get('app_id', '—')}"
        row = [
            PS(str(c["rank"]),                                      fs=7.5, align=TA_CENTER),
            PS(f"<b>{c['name']}</b><br/><font size='6' color='#6B7280'>{app_id_str}</font>", fs=7.5),
            PS(str(c["score"]),                                     fs=7.5, align=TA_CENTER),
            PS(c["tier"],                                           fs=7.5, tc=tier_col, bold=True, align=TA_CENTER),
            PS(bl,                                                  fs=7,   tc=bl_color, bold=True, align=TA_CENTER),
            PS(c.get("salary", "Not mentioned"),                    fs=7,   tc=C_GRAY,   align=TA_CENTER),
            PS(c.get("total_exp", "—"),                             fs=7.5, align=TA_CENTER),
            PS(c["current_role"],                                   fs=7.5),
            PS(c["key_strength"],                                   fs=7.5),
            PS(vc,                                                  fs=7.5, tc=verd_col, bold=True, align=TA_CENTER),
        ]
        table_data.append(row)
        row_idx += 1

    # Separator — Overqualified
    sep_row2 = [PS("STRONG MATCH — OVERQUALIFIED / OVER BUDGET", fs=7, tc=C_WHITE, bold=True, align=TA_CENTER)] + [""] * 9
    table_data.append(sep_row2)
    table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), C_SEP_PINK))
    table_styles.append(('SPAN',       (0, row_idx), (-1, row_idx)))
    row_idx += 1

    for i, c in enumerate(OVER_BUDGET):
        ob_app = f"App #{c.get('app_id', '—')}"
        row = [
            PS(f"OQ{i+1}",          fs=7.5, align=TA_CENTER),
            PS(f"<b>{c['name']}</b><br/><font size='6' color='#6B7280'>{ob_app}</font>", fs=7.5),
            PS(str(c["score"]),      fs=7.5, align=TA_CENTER),
            PS(c["tier"],            fs=7.5, tc=C_TIER_A, bold=True, align=TA_CENTER),
            PS(c.get("budget_note", "Flag"), fs=7, tc=C_OOB, bold=True, align=TA_CENTER),
            PS(c["salary"],          fs=7,   tc=C_OOB, bold=True, align=TA_CENTER),
            PS("—",                  fs=7.5, align=TA_CENTER),
            PS("—",                  fs=7.5),
            PS(c["note"],            fs=7.5),
            PS(c["verdict"],         fs=7.5, tc=C_OOB, bold=True, align=TA_CENTER),
        ]
        table_data.append(row)
        row_idx += 1

    # Separator — No Hire
    sep_row3 = [PS("NO HIRE", fs=7, tc=C_WHITE, bold=True, align=TA_CENTER)] + [""] * 9
    table_data.append(sep_row3)
    table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), C_SEP_BLACK))
    table_styles.append(('SPAN',       (0, row_idx), (-1, row_idx)))
    row_idx += 1

    for c in NO_HIRE_CANDIDATES:
        row = [
            PS("—",             fs=7.5, align=TA_CENTER),
            PS(c["name"],       fs=7.5),
            PS(str(c["score"]), fs=7.5, tc=C_NO_HIRE, align=TA_CENTER),
            PS(c["tier"],       fs=7.5, tc=C_NO_HIRE, bold=True, align=TA_CENTER),
            PS("—",             fs=7,   align=TA_CENTER),
            PS("—",             fs=7,   align=TA_CENTER),
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
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 4),
    ]))
    story.append(chart_table)
    story.append(PageBreak())

    # ── SECTION 3 — Overqualified / OOB Flags ───────────────────
    story.append(PS_h("Strong Matches — Overqualified / Budget Flags", fs=12))
    story.append(PS(
        f"Budget range: {BUDGET_RANGE}. {len(CANDIDATES) - 1} of {len(CANDIDATES)} shortlisted candidates are within budget "
        f"(Burhan Hassan borderline at ceiling). "
        f"Four additional candidates show strong JD match but raise overqualification or budget concerns — "
        f"flagged below for hiring manager awareness.",
        fs=9, tc=C_BLACK
    ))
    story.append(Spacer(1, 4*mm))

    for i, c in enumerate(OVER_BUDGET):
        oob_data = [
            [PS(f"OQ{i+1}: {c['name']}", fs=9, bold=True),
             PS(f"Score: {c['score']} | Tier: {c['tier']}", fs=8, tc=C_GRAY)],
            [PS(f"Expected Salary: {c['salary']}", fs=8, tc=C_OOB, bold=True),
             PS(c["budget_note"], fs=8, tc=C_OOB, bold=True)],
            [PS(c["note"], fs=8), PS(c["verdict"], fs=8, bold=True)],
        ]
        oob_t = Table(oob_data, colWidths=[133*mm, 134*mm])
        oob_t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), C_AMBER_BG),
            ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
            ('VALIGN',     (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING',(0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING',(0,0),(-1, -1), 4),
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
        ("Wrong Domain — Psychology, Chemistry, IT, Humanities (12+ candidates)",
         "A significant portion of the top-35 scanner pool had strong academic profiles but in entirely wrong domains: "
         "psychology/mental health (Muqqadas Saba, Aabsha Tasaawar, Zainab Ashraf), chemistry (Saira Shakoor), "
         "hydrology/geosciences (Muhammad Zaheer Abbasi — PostDoc), software engineering (Hanniya Fatima, Sarim Kazi), "
         "IR/security studies (Manal Shah, Shahid Kamal from think-tank focus, Wajeeha Rehber). "
         "The scanner counted 'research' and 'data' keywords regardless of domain — human review corrected these."),
        ("Commercial Career Trajectory Despite Policy Degree (2 candidates)",
         "Noor Fatima (MS Governance & Public Policy NUST) and Hajra Asghar (MPhil Management Sciences) have relevant "
         "degrees but all professional experience is in marketing, e-commerce, or teaching. "
         "Policy/research degrees alone do not qualify — relevant work experience is the deciding factor."),
        ("Wrong Location — Not Islamabad/Rawalpindi (3 candidates)",
         "Hassan Yasar (Multan), Muhammad Rafay (Karachi), Syed Zashir Muhammad Naqvi (Karachi). "
         "The role is in-office in Islamabad. Karachi-based candidates were flagged unless they confirmed relocation. "
         "Muhammad Rafay (IBA Gold Medal, UNICEF RA) would have ranked in Tier B but for the location constraint."),
        ("Massively Overqualified — PhD / Senior Researchers (3 candidates)",
         "Jawad Khan (PhD, 7+ yrs, UNICEF/UNDP evaluator), Sidra Ishfaq (PhD Economics, 8+ yrs Senior Research Officer), "
         "Sehrish Irfan (MPhil Public Policy PIDE + 7 yrs Senior Research Analyst). "
         "All three score 84–87 on JD match but are 5–10x more experienced than the entry-level JD requires. "
         "Sehrish Irfan's expected salary (PKR 1.25M) confirms she is not genuinely seeking a JRA role. "
         "Flagged for awareness — not recommended for this vacancy."),
        ("Entry-Level Candidates with SPSS-Only Toolkit (4 candidates)",
         "Muhammad Usman (Ipsos, SPSS only), Wajeeha Rehber (Sociology MS, SPSS/Excel only), "
         "Muqqadas Saba (Psychology RA, SPSS only), Aabsha Tasaawar (Psychology MPhil, SPSS only). "
         "The JD specifies Excel/Stata/R proficiency. Candidates who list SPSS alone without Stata or R "
         "do not meet the quantitative threshold — particularly for a role involving Taleemabad's impact evaluations."),
        ("Still Enrolled Undergrad (1 candidate)",
         "Sarim Kazi (BS Business Analytics NUCES, 2022–2026) is still in the final year of his undergraduate degree. "
         "Not eligible for this full-time role."),
    ]

    for title, explanation in reasons:
        story.append(PS(f"<b>{title}</b>", fs=9))
        story.append(PS(explanation, fs=8, tc=C_GRAY))
        story.append(Spacer(1, 3*mm))

    story.append(HRFlowable(width="100%", thickness=1, color=C_HEADER, spaceAfter=4))

    # ── Next Steps ───────────────────────────────────────────────
    story.append(PS_h("Recommended Next Steps", fs=12))
    story.append(Spacer(1, 2*mm))
    next_steps = [
        "1. Immediately shortlist top 5 (Muhammad Burhan Hassan, Faryal Afridi, Rabia Zafar, Muhammad Junaid, Shahid Kamal) "
        "for 30-min screening calls.",
        "2. Muhammad Burhan Hassan (Rank 1, Score 93): Strongest match — education-sector data work at VIT Global on "
        "World Bank EGRA and ASPIRE (teacher training evaluation). This is directly what Taleemabad's R&I team does. "
        "Salary at budget ceiling (PKR 200K) — justified by experience depth.",
        "3. For Hadiyah Shaheen (Rank 6, LUMS Best Senior Thesis): Give her a short data task (30 min, Stata or Excel). "
        "Her RDD thesis and 2-yr TA role are strong academic signals — confirm she can apply the skills in a structured org.",
        "4. Three cross-applicants from Job 36 in this pool (Faryal Afridi, Muhammad Junaid, Shahid Kamal) — "
        "if they are already being considered for Field Coordinator, coordinate across both pipelines to avoid double-offer.",
        "5. Interview question for all candidates: 'Walk me through a dataset you cleaned — what issues did you find and "
        "how did you handle them before analysis?'",
        "6. For Jawad Khan (Overqualified, Score 87): Consider only if the team needs an immediate senior research capacity "
        "and is willing to discuss a higher-level contract. At PKR 160K, he may accept out of interest in Taleemabad's mission — "
        "but the JRA scope will not hold him long.",
        "7. Verify Islamabad / Rawalpindi location or relocation readiness for Hassan Zafar (Murree) and Wasif Mehdi (Rawalpindi).",
    ]
    for step in next_steps:
        story.append(PS(step, fs=8, tc=C_BLACK))
        story.append(Spacer(1, 1.5*mm))

    story.append(Spacer(1, 4*mm))
    story.append(PS(
        "Coco — Taleemabad Talent Acquisition Agent  •  Confidential",
        fs=7, tc=C_GRAY, align=TA_CENTER
    ))

    doc.build(story)
    print(f"PDF saved: {pdf_path}")
    return pdf_path


# ══════════════════════════════════════════════════════════════════════
# EMAIL
# ══════════════════════════════════════════════════════════════════════
def send_email(pdf_path):
    shortlisted  = len(CANDIDATES)
    not_listed   = TOTAL_APPLICANTS - shortlisted

    html = f"""
    <html><body style="font-family:Arial,sans-serif;font-size:14px;color:#1F2937;max-width:680px;margin:0 auto;padding:20px;">

      <p style="margin:0 0 20px 0;">Hi {HIRING_MGR_FIRST},</p>
      <p style="margin:0 0 16px 0;">
        Please find attached the screening report for <strong>{JOB_TITLE}</strong> (Job {JOB_ID}).
      </p>

      <table style="width:100%;border-collapse:collapse;margin-bottom:20px;">
        <tr>
          <td style="background:#F0FDF4;border:1px solid #BBF7D0;padding:14px;text-align:center;border-radius:6px;">
            <div style="font-size:26px;font-weight:bold;color:#16A34A;">{TOTAL_APPLICANTS}</div>
            <div style="font-size:12px;color:#6B7280;">Applications Received</div>
          </td>
          <td style="width:16px;"></td>
          <td style="background:#EFF6FF;border:1px solid #BFDBFE;padding:14px;text-align:center;border-radius:6px;">
            <div style="font-size:26px;font-weight:bold;color:#2563EB;">{shortlisted}</div>
            <div style="font-size:12px;color:#6B7280;">Shortlisted</div>
          </td>
          <td style="width:16px;"></td>
          <td style="background:#FFF7ED;border:1px solid #FED7AA;padding:14px;text-align:center;border-radius:6px;">
            <div style="font-size:26px;font-weight:bold;color:#D97706;">{not_listed}</div>
            <div style="font-size:12px;color:#6B7280;">Not Shortlisted</div>
          </td>
        </tr>
      </table>

      <p style="margin:0 0 10px 0;color:#374151;">
        Please open the attached PDF for the full analysis — ranked shortlist, dimension scores,
        charts, and recommended next steps.
      </p>

      <p style="margin:0 0 20px 0;color:#6B7280;font-size:13px;">
        Budget: {BUDGET_RANGE} &nbsp;|&nbsp; {shortlisted - 1} shortlisted candidates are within budget; 1 borderline (Burhan Hassan at ceiling).
        <strong>Top pick: Muhammad Burhan Hassan</strong> (Score 93, education M&E at World Bank EGRA/ASPIRE — directly relevant to Taleemabad).
      </p>

      <table style="border-top:2px solid #16A34A;margin-top:24px;padding-top:14px;width:100%;border-collapse:collapse;">
        <tr>
          <td style="font-family:Arial,sans-serif;font-size:13px;color:#1F2937;line-height:1.6;">
            <p style="margin:0 0 2px 0;"><strong style="color:#16A34A;">Ayesha Raza Khan,</strong></p>
            <p style="margin:0 0 2px 0;"><strong>Deputy Manager People &amp; Culture, Taleemabad.</strong></p>
            <p style="margin:0;color:#6B7280;font-size:12px;">Coco — Taleemabad Talent Acquisition Agent &bull; Confidential</p>
          </td>
        </tr>
      </table>

    </body></html>
    """

    msg            = MIMEMultipart("mixed")
    msg["Subject"] = f"Screening Report- {JOB_TITLE}"
    msg["From"]    = SENDER
    msg["To"]      = ", ".join(RECIPIENTS)
    if CC_LIST:
        msg["Cc"]  = ", ".join(CC_LIST)

    msg.attach(MIMEText(html, "html"))

    with open(pdf_path, "rb") as f:
        att = MIMEBase("application", "octet-stream")
        att.set_payload(f.read())
        encoders.encode_base64(att)
        att.add_header("Content-Disposition", "attachment",
                       filename="Screening-Report-Junior-Research-Associate-Impact-Policy-v2.pdf")
        msg.attach(att)

    all_recipients = RECIPIENTS + CC_LIST
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        allow_candidate_addresses(all_recipients if isinstance(all_recipients, list) else [all_recipients])
        safe_sendmail(smtp, SENDER, all_recipients, msg.as_string(), context='send_job35_v2_report_pdf')

    print(f"Email sent to: {', '.join(all_recipients)}")
    print(f"Subject: {msg['Subject']}")
    print(f"Attachment: Screening-Report-Junior-Research-Associate-Impact-Policy-v2.pdf")


if __name__ == "__main__":
    print(f"Mode: {'PILOT (Ayesha only)' if PILOT_MODE else 'FULL SEND'}")
    print("Generating PDF report...")
    pdf_path = build_pdf()
    print("Sending email...")
    send_email(pdf_path)
    print("Done.")
