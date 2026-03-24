"""
Job 36 v2 — Field Coordinator, Research & Impact Studies
Full re-screen with Markaz profile names, JD-aligned scoring.
10-column master table: # · Candidate · Score · Tier · Budget · Exp. Salary · Experience · Background/Current Role · Key Strength/Why Not Shortlisted · Verdict
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
# CANDIDATES — Top 15 Shortlisted (Markaz names, JD-based scoring)
# dims: (functional, outcomes, environment, ownership, communication, hard_skills, growth)  0–4
# ══════════════════════════════════════════════════════════════════════
CANDIDATES = [
    # ── NOTE ON SCORING ───────────────────────────────────────────────
    # Rankings are based on JD keyword alignment (field M&E, survey management,
    # enumerator oversight, data quality, govt coordination).
    # Org/competitor signals are SUPPLEMENTARY FLAGS only — shown in key_strength
    # but do NOT inflate scores. A candidate from TCF with weak JD keywords ranks
    # lower than a candidate from an unknown org with strong JD evidence.
    # ──────────────────────────────────────────────────────────────────
    {
        "rank": 1, "name": "Asif Khan", "app_id": 1602, "score": 92.0, "tier": "Tier A",
        "total_exp": "~13 yrs", "relevant_exp": "~10 yrs (M&E/QA specialist, USAID & World Bank)",
        "current_role": "Data/QA Specialist — USAID/World Bank projects, Islamabad",
        "salary": "PKR 250,000", "budget_label": "Borderline (at ceiling)", "over_budget": False,
        "key_strength": "JD MATCH: 13+ yrs M&E/QA field work; direct 'Data/QA Specialist' role = exact match to "
                        "field governance mandate; spot-check, data quality, and survey firm oversight from CV. "
                        "Org signal (supplementary): USAID, World Bank, GIZ, CARE.",
        "verdict": "RECOMMEND",
        "dims": (4, 4, 4, 4, 4, 4, 4), "missing_mh": 0,
    },
    {
        "rank": 2, "name": "Pariyal Fazal Shah", "app_id": 1545, "score": 90.0, "tier": "Tier A",
        "total_exp": "~6 yrs", "relevant_exp": "~6 yrs (field research, M&E, World Bank/IPA projects)",
        "current_role": "Field Research & M&E Professional — Islamabad",
        "salary": "PKR 200,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Islamabad-based; data quality, sampling, and field coordination keywords "
                        "throughout CV; results-oriented professional with field M&E evidence. "
                        "Org signal (supplementary): World Bank, Aga Khan, IPA, Georgetown.",
        "verdict": "RECOMMEND",
        "dims": (4, 4, 4, 3, 4, 4, 2), "missing_mh": 0,
    },
    {
        "rank": 3, "name": "Zubair Hussain", "app_id": 1518, "score": 88.0, "tier": "Tier A",
        "total_exp": "~15 yrs", "relevant_exp": "~10 yrs (field coordination, USAID/IPA)",
        "current_role": "Humanitarian & Field Expert — USAID/IPA projects",
        "salary": "PKR 220,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: 15 yrs field work; strong field governance, data collection, QA, "
                        "and survey firm coordination from CV evidence. "
                        "Org signal (supplementary): USAID, IPA, CARE. "
                        "NOTE: Humanitarian/gender focus — confirm education M&E fit.",
        "verdict": "RECOMMEND",
        "dims": (4, 4, 4, 3, 4, 3, 4), "missing_mh": 0,
    },
    {
        "rank": 4, "name": "Fatima Razzaq", "app_id": 1658, "score": 87.0, "tier": "Tier A",
        "total_exp": "~8 yrs", "relevant_exp": "~8 yrs (development & evaluation, Islamabad)",
        "current_role": "Development & Evaluation Professional — Islamabad",
        "salary": "PKR 186,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: 8 yrs development/evaluation; M&E, data analysis, reporting, and "
                        "field outcomes in CV; Islamabad-based. "
                        "Org signal (supplementary): Oxford affiliation.",
        "verdict": "RECOMMEND",
        "dims": (4, 3, 4, 4, 3, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 5, "name": "Jawad Khan", "app_id": 1720, "score": 86.0, "tier": "Tier A",
        "total_exp": "~5 yrs (PhD Scholar)", "relevant_exp": "~5 yrs (research & evaluation)",
        "current_role": "PhD Scholar — Research, Data Analysis & Evaluation, Islamabad",
        "salary": "PKR 200,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Research, evaluation, and data analysis keywords from CV; Islamabad-based. "
                        "Org signal (supplementary): UNICEF, UNDP. "
                        "NOTE: PhD-level — confirm operational field coordination vs. research role interest.",
        "verdict": "INTERVIEW",
        "dims": (4, 4, 4, 2, 4, 4, 4), "missing_mh": 0,
    },
    {
        "rank": 6, "name": "HabibunNabi", "app_id": 1839, "score": 86.0, "tier": "Tier A",
        "total_exp": "~17 yrs", "relevant_exp": "~15 yrs (field ops, provincial coordination)",
        "current_role": "Field Operations Specialist / Provincial Coordinator",
        "salary": "PKR 80,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: CV title = 'Field Operations Specialist' + 'Provincial Coordinator' — "
                        "direct role match; 17 yrs field experience; enumerator supervision, spot-checks, "
                        "govt/school coordination all evidenced in CV. "
                        "Org signal (supplementary): IPA, LUMS. "
                        "FLAG: Salary PKR 80K unusually low for 17 yrs — verify before interview.",
        "verdict": "INTERVIEW",
        "dims": (4, 2, 4, 3, 4, 4, 4), "missing_mh": 0,
    },
    {
        "rank": 7, "name": "Shahid Kamal", "app_id": 1454, "score": 85.0, "tier": "Tier A",
        "total_exp": "~11 yrs", "relevant_exp": "~8 yrs (development research, Islamabad)",
        "current_role": "Developmental & Academic Researcher — Islamabad",
        "salary": "PKR 150,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: 11 yrs development research; field M&E, reporting, and stakeholder "
                        "communication evidenced in CV; Islamabad-based. "
                        "Org signal (supplementary): UNDP, IPA, LUMS.",
        "verdict": "INTERVIEW",
        "dims": (4, 3, 4, 3, 4, 3, 4), "missing_mh": 0,
    },
    {
        "rank": 8, "name": "Fatima Mughal", "app_id": 1864, "score": 83.0, "tier": "Tier B",
        "total_exp": "~7 yrs", "relevant_exp": "~7 yrs (program management, education sector)",
        "current_role": "Development Professional / Program Manager",
        "salary": "PKR 170,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Field program management, M&E, and donor reporting from CV. "
                        "COMPETITOR SIGNAL: READ Foundation (education NGO — direct Taleemabad peer). "
                        "Org signal (supplementary): UNICEF, FCDO, IPA, LUMS. "
                        "NOTE: Program management may be more strategic than operational — probe spot-check depth.",
        "verdict": "INTERVIEW",
        "dims": (4, 3, 4, 3, 4, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 9, "name": "Asad Farooq", "app_id": 1700, "score": 82.0, "tier": "Tier B",
        "total_exp": "~10 yrs", "relevant_exp": "~8 yrs (field research, education impact)",
        "current_role": "Field Research & Education Impact Professional — Islamabad",
        "salary": "PKR 140,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Self-described 'field research and education impact professional'; "
                        "10 yrs field experience; education sector alignment from CV. "
                        "Org signal (supplementary): IPA, PIDE, Oxford.",
        "verdict": "CONSIDER",
        "dims": (4, 2, 4, 3, 4, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 10, "name": "Muhammad Afzaal", "app_id": 1528, "score": 80.0, "tier": "Tier B",
        "total_exp": "~11 yrs", "relevant_exp": "~8 yrs (community mobilization, social sector)",
        "current_role": "Capacity Building & Community Mobilization Professional — Peshawar",
        "salary": "PKR 130,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: 11 yrs social sector field work; training, oversight, and field "
                        "supervision from CV. Org signal (supplementary): IPA. "
                        "FLAG: Peshawar-based — confirm Islamabad relocation willingness.",
        "verdict": "CONSIDER",
        "dims": (4, 2, 4, 3, 4, 4, 4), "missing_mh": 0,
    },
    {
        "rank": 11, "name": "Muhammad Qasi", "app_id": 1489, "score": 80.0, "tier": "Tier B",
        "total_exp": "~5 yrs", "relevant_exp": "~5 yrs (AKDN/PPAF, social development)",
        "current_role": "Researcher / Social Development Project Lead — Islamabad",
        "salary": "PKR 100,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: 5 yrs mixed-methods research, end-to-end data collection, "
                        "and field project leadership from CV; Islamabad-based. "
                        "Org signal (supplementary): Aga Khan (AKDN), PPAF, Global Affairs Canada.",
        "verdict": "CONSIDER",
        "dims": (4, 2, 4, 3, 4, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 12, "name": "Jalal Ud Din", "app_id": 1950, "score": 79.0, "tier": "Tier B",
        "total_exp": "~5 yrs (MPhil)", "relevant_exp": "~4 yrs (economics research)",
        "current_role": "MPhil Economics Researcher — UNDP/World Bank projects",
        "salary": "PKR 120,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Research methods, data analysis from CV; MPhil Economics. "
                        "Org signal (supplementary): UNDP, World Bank, IPA, PIDE. "
                        "NOTE: Research profile — limited operational field coordination evidence.",
        "verdict": "CONSIDER",
        "dims": (4, 2, 4, 3, 4, 3, 3), "missing_mh": 0,
    },
    {
        "rank": 13, "name": "Faryal Afridi", "app_id": 1442, "score": 78.0, "tier": "Tier B",
        "total_exp": "~4 yrs", "relevant_exp": "~4 yrs (field research, Taleemabad/USAID)",
        "current_role": "Field Researcher / RA — Taleemabad-linked, Islamabad",
        "salary": "PKR 100,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Field research, data collection from CV; Islamabad-based; NUST. "
                        "COMPETITOR SIGNAL: Taleemabad direct exposure — strongest culture fit. "
                        "Org signal (supplementary): USAID, IPA. "
                        "NOTE: 4 yrs — junior; confirm survey firm management independently.",
        "verdict": "CONSIDER",
        "dims": (4, 2, 4, 4, 1, 4, 3), "missing_mh": 0,
    },
    {
        "rank": 14, "name": "Midhat Fatima", "app_id": 1633, "score": 76.0, "tier": "Tier B",
        "total_exp": "~6 yrs", "relevant_exp": "~4 yrs (public health field research)",
        "current_role": "Public Health Field Researcher — Islamabad",
        "salary": "PKR 90,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Public health field research and community data collection from CV; "
                        "Islamabad-based. Org signal (supplementary): IPA. "
                        "NOTE: Public health sector — education M&E experience needs confirmation.",
        "verdict": "CONSIDER",
        "dims": (4, 2, 4, 3, 4, 4, 4), "missing_mh": 0,
    },
    {
        "rank": 15, "name": "Sadia Siddique", "app_id": 1477, "score": 75.0, "tier": "Tier B",
        "total_exp": "~5 yrs", "relevant_exp": "~5 yrs (field research, monitoring)",
        "current_role": "Field Researcher / Monitor — NGO sector",
        "salary": "PKR 150,000", "budget_label": "In Budget", "over_budget": False,
        "key_strength": "JD MATCH: Field monitoring and data collection from CV; education/NGO sector. "
                        "Org signal: No high-signal affiliations in CV. "
                        "NOTE: Confirm government coordination and enumerator management experience.",
        "verdict": "CONSIDER",
        "dims": (3, 2, 3, 3, 3, 3, 3), "missing_mh": 0,
    },
]

# ══════════════════════════════════════════════════════════════════════
# OVER BUDGET
# ══════════════════════════════════════════════════════════════════════
OVER_BUDGET = [
    {
        "name": "Syeda Farzana Ali Shah", "app_id": 1802, "score": 83.8, "tier": "Tier B",
        "salary": "PKR 300,000",
        "budget_note": "OVER BUDGET — exceeds PKR 250K ceiling by PKR 50K",
        "note": "JD MATCH: 25 yrs field experience, government coordination, M&E. "
                "Org signal: UNICEF, UNDP, USAID, FCDO — strong development sector. "
                "Child protection/gender/safeguarding focus. Over budget by PKR 50K — worth salary discussion only if top 5 shortlist fails.",
        "verdict": "FLAG — Over Budget",
    },
    {
        "name": "Naveen Shariff", "app_id": 1450, "score": 80.0, "tier": "Tier B",
        "salary": "PKR 220,000",
        "budget_note": "IN BUDGET — within PKR 200K–250K range",
        "note": "Corrected: previously flagged as over-budget in error. PKR 220K is within the PKR 200K–250K range. Scored 80.0 — CONSIDER tier. Review alongside Tier B shortlist.",
        "verdict": "RECONSIDER — In Budget",
    },
]

# ══════════════════════════════════════════════════════════════════════
# NO-HIRE CANDIDATES — Representative sample
# ══════════════════════════════════════════════════════════════════════
NO_HIRE_CANDIDATES = [
    {"name": "Saira Akram",      "score": 18, "tier": "No-Hire", "reason": "Expected salary PKR 400,000 — far exceeds budget ceiling. CV background is social/community work, not M&E or field coordination."},
    {"name": "Faiza Ghazal",     "score": 20, "tier": "No-Hire", "reason": "Expected salary PKR 320,000 — over budget. Marketing/communications background, not relevant to field research coordination."},
    {"name": "Rabia Mukhtar",    "score": 12, "tier": "No-Hire", "reason": "Salary entry appears erroneous (PKR 855,700). Background unrelated to M&E or field research."},
    {"name": "Iqra parvez",      "score": 15, "tier": "No-Hire", "reason": "No M&E, field research, or education sector experience. No relevant data tools demonstrated in CV."},
    {"name": "Amanullah Naich",  "score": 10, "tier": "No-Hire", "reason": "Salary stated as '80' (unclear). CV background unrelated to research, M&E, or field coordination."},
    {"name": "Maryam bibi",      "score": 12, "tier": "No-Hire", "reason": "40K salary; no field research or M&E background. Academic focus only, no field or program implementation experience."},
    {"name": "MUBARAH CHAUDHARY","score": 12, "tier": "No-Hire", "reason": "40K salary; no relevant background. Does not meet minimum 1-year field research or M&E experience requirement."},
    {"name": "Multiple applicants (20+)", "score": 10, "tier": "No-Hire", "reason": "Applied via quick-apply with placeholder profiles ('Applicant' last name, no resume). Cannot assess qualifications — 20+ such applications discarded."},
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
    pdf_path = f"output/{date.today()}-field-coordinator-research-impact-v2-screening-report.pdf"
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
        f"Budget: {BUDGET_RANGE}  |  Date: {date.today()}",
        fs=8, tc=C_GRAY
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_HEADER, spaceAfter=6))
    story.append(Spacer(1, 3*mm))

    # ── SECTION 1 — Deep Comparative Analysis ─────────────────────
    story.append(PS_h("Deep Comparative Analysis — All Screened Candidates", fs=12))
    story.append(PS(
        f"Master table shows top {len(CANDIDATES)} shortlisted candidates + over-budget flags + representative no-hire sample. "
        f"Candidates screened against JD using 7-dimension framework. Names sourced from Markaz profiles.",
        fs=8, tc=C_GRAY
    ))
    story.append(Spacer(1, 3*mm))

    # Column widths — 10 columns, 267mm usable landscape A4
    # # | Candidate | Score | Tier | Budget | Exp.Salary | Experience | Background | Key Strength | Verdict
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

    shortlisted = CANDIDATES
    for c in shortlisted:
        # Budget colour
        bl = c.get("budget_label", "")
        if "Over" in bl or "over" in bl:
            bl_color = C_OOB
        elif "Borderline" in bl:
            bl_color = C_BORDERLINE
        else:
            bl_color = C_IN_BUDGET

        # Tier colour
        tier_col = {"Tier A": C_TIER_A, "Tier B": C_TIER_B, "Tier C": C_TIER_C}.get(c["tier"], C_NO_HIRE)

        # Verdict colour
        vc = c.get("verdict", "")
        if vc == "RECOMMEND":
            verd_col = C_TIER_A
        elif vc == "INTERVIEW":
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
            PS(c["tier"],       fs=7.5, tc=C_TIER_B, bold=True, align=TA_CENTER),
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
        f"Budget range: {BUDGET_RANGE}. All 15 shortlisted candidates are within budget. "
        f"One candidate (Syeda Farzana Ali Shah, score 83.8) expects PKR 300,000 — over budget by PKR 50,000. "
        f"Note: Naveen Shariff (PKR 220,000) was previously flagged as over-budget in error — she is within range.",
        fs=9, tc=C_BLACK
    ))
    story.append(Spacer(1, 4*mm))

    for i, c in enumerate(OVER_BUDGET):
        oob_data = [
            [PS(f"OB{i+1}: {c['name']}", fs=9, bold=True),
             PS(f"Score: {c['score']} | Tier: {c['tier']}", fs=8, tc=C_GRAY)],
            [PS(f"Expected Salary: {c['salary']}", fs=8,
                tc=C_OOB if 'OVER' in c.get('budget_note','') else C_IN_BUDGET, bold=True),
             PS(c["budget_note"], fs=8,
                tc=C_OOB if 'OVER' in c.get('budget_note','') else C_IN_BUDGET, bold=True)],
            [PS(c["note"], fs=8), PS(c["verdict"], fs=8, bold=True)],
        ]
        oob_t = Table(oob_data, colWidths=[133*mm, 134*mm])
        oob_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0),
             C_AMBER_BG if 'OVER' in c.get('budget_note','') else C_GREEN_BG),
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
        ("No M&E / Field Research Background (60+ candidates)",
         "Over 60 candidates had backgrounds entirely unrelated to M&E, field research, or education program implementation. "
         "Common profiles: teaching, HR, marketing, corporate sales, finance. These do not meet the JD's minimum requirement of "
         "1–3 years in field research or M&E. All discarded."),
        ("Quick-Apply Placeholder Profiles (20+ candidates)",
         "Over 20 applications had generic placeholder names (e.g., 'usman Applicant', 'saba Applicant') with no resume attached. "
         "Without a CV, it is impossible to assess qualifications. All discarded."),
        ("Over Budget (2 candidates)",
         "Saira Akram (PKR 400,000) and Syeda Farzana Ali Shah (PKR 300,000) exceed the PKR 250K ceiling. "
         "Syeda Farzana is flagged separately as she has strong field credentials worth discussing with the hiring manager."),
        ("Humanitarian Sector Only — No Education Focus (15+ candidates)",
         "Several candidates had strong international NGO backgrounds (UNHCR, WFP, humanitarian relief) but no education "
         "sector or government school experience. The JD specifically requires government school coordination and education "
         "program M&E — sector alignment is a must."),
        ("Researchers Without Field Coordination Experience (25+ candidates)",
         "A significant group had academic research or data analysis backgrounds (PhDs, research assistants) but "
         "lacked evidence of operational field coordination — managing enumerators, conducting spot-checks, "
         "liaising with survey firms, or tracking daily coverage. Research alone does not meet the JD."),
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
        "1. Immediately shortlist top 5 (Asif Khan, Pariyal Fazal Shah, Zubair Hussain, Fatima Razzaq, Jawad Khan) for 30-min screening calls.",
        "2. For HabibunNabi (Rank 6): verify 17-yr experience and confirm salary (PKR 80K seems unusually low for this profile — may be a data entry error).",
        "3. For Asif Khan (Rank 1): clarify long-term commitment at PKR 250K ceiling; confirm government school coordination experience.",
        "4. For Jawad Khan (Rank 5): confirm field coordination role interest vs. research/academic preference.",
        "5. Interview question to ask all: 'Walk me through a time you caught a data quality issue in the field and corrected it before it reached the analysis stage.'",
        "6. Confirm Islamabad/Rawalpindi residency or relocation readiness for all shortlisted candidates.",
        "7. Negotiate salary for Syeda Farzana Ali Shah (PKR 300K ask) only if top 5 don't meet expectations — strong profile worth revisiting.",
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
        The screening report for <strong>{JOB_TITLE}</strong> (Job {JOB_ID}) is attached.
        This is a <strong>full re-screen</strong> of all {TOTAL_SCREENED} applicants against the JD —
        candidate names sourced directly from Markaz profiles.
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
        Budget: {BUDGET_RANGE} &nbsp;|&nbsp; All shortlisted candidates within budget.
        Salary data sourced from application forms (Markaz).
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
                       filename="Screening-Report-Field-Coordinator-Research-Impact-v2.pdf")
        msg.attach(att)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.sendmail(SENDER, RECIPIENTS, msg.as_string())

    print(f"Email sent to: {', '.join(RECIPIENTS)}")
    print(f"Subject: {msg['Subject']}")
    print(f"Attachment: Screening-Report-Field-Coordinator-Research-Impact-v2.pdf")


if __name__ == "__main__":
    print("Generating PDF report...")
    pdf_path = build_pdf()
    print("Sending email...")
    send_email(pdf_path)
    print("Done.")
