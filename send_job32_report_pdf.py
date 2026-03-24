#!/usr/bin/env python3
"""
Job 32 — Fundraising & Partnerships Manager
Human-judgement re-screen by Coco — All 67 candidates assessed
Budget: PKR 150,000 – 270,000
Send to: ayesha.khan@taleemabad.com ONLY (no CC)
"""
import smtplib, ssl, os, io
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# ─── CONFIG ────────────────────────────────────────────────────────────────────
GMAIL_USER   = "ayesha.khan@taleemabad.com"
GMAIL_APP_PW = os.environ.get("GMAIL_APP_PASSWORD", "")
TO_EMAIL     = "ayesha.khan@taleemabad.com"
CC_EMAILS    = []   # NO CC — per explicit user instruction

JOB_TITLE    = "Fundraising & Partnerships Manager"
JOB_ID       = 32
BUDGET_STR   = "PKR 150K–270K"
PDF_FILE     = "output/job32_screening_report.pdf"
os.makedirs("output", exist_ok=True)

# ─── CANDIDATES ────────────────────────────────────────────────────────────────
# Tuple: (app_id, name, score, tier, budget_status, exp_salary,
#         experience, current_role, key_note, verdict)
CANDIDATES = [
    # ── SHORTLISTED / CONSIDER ────────────────────────────────────────────────
    (1346, "Danish Hussain",         88, "Tier A", "Out of Budget", "PKR 550,000",
     "20+ yrs (rel: 15+ yrs)",
     "Director Programs/Fundraising, multiple INGOs (Hyderabad)",
     "STRONGEST in pool: PKR 1B+ closed (WB, ADB, FCDO, EU, UN); bilateral+multilateral; LOCATION FLAG - Hyderabad",
     "HOLD - Location"),
    (1327, "mizhgan kirmani",        84, "Tier B", "In Budget", "PKR 250,000",
     "6+ yrs (rel: 4-5 yrs)",
     "Manager Donor Relations, TCF; BD Officer, Tearfund UK (ISB)",
     "TCF+Tearfund UK competitor signal; PKR 72.2M closed FY23-24; bilateral donor network; ISB-based",
     "SHORTLIST"),
    (2013, "Muhammad Adnan",         82, "Tier B", "Out of Budget", "PKR 575,000",
     "12+ yrs (rel: 6+ yrs)",
     "Global Acquisition Mgr, C4ED (Germany); prev CERP World Bank, GIZ Pakistan, British Council (ISB)",
     "Manages bids/proposals for WB, UN agencies, GIZ, FCDO at C4ED; CERP CLEAR Initiative (WB); GIZ TVET; ISB-based",
     "SHORTLIST"),
    (1354, "Arsim Tariq",            78, "Tier B", "Borderline", "PKR 280K-300K",
     "10+ yrs (rel: 8 yrs)",
     "Resource Mobilisation & BD Consultant (ISB)",
     "20+ multilateral projects secured (WB, UN Women, UNDP); structured pipeline management; ISB-based",
     "SHORTLIST"),
    (1851, "Shahzad Saleem Abbasi",  75, "Tier B", "In Budget", "PKR 270,000",
     "15+ yrs (rel: 15 yrs)",
     "Head Fundraising, Alkhidmat Rawalpindi (ISB)",
     "PKR 400M+/yr fundraising; 10,000+ donors; 12 CSR partnerships; Islamic philanthropy + CSR; ISB",
     "SHORTLIST"),
    (1357, "Arsalan Ashraf",         72, "Tier B", "Out of Budget", "PKR 450,000",
     "7+ yrs (rel: 5 yrs)",
     "BD Manager, HANDS; prev Meta/Chevron CSR lead (Karachi, open to ISB relocation)",
     "Closed: Meta USD 100K, Chevron USD 250K, Govt Sindh PKR 30M, START Network GBP 15K, diaspora USD 40K/month recurring; open ISB move",
     "SHORTLIST"),
    (1722, "Ahad Ahsan Khan",        67, "Tier C", "Out of Budget", "PKR 550,000",
     "8+ yrs (rel: 6 yrs)",
     "Manager Grants (SRS), AKU Karachi; prev WB-HEDP Consultant ISB",
     "AKU $134M grants portfolio; raised PKR 26.5M at NHSD NGO (UN, USAID, GGP Japan); ISB hometown; willing to relocate",
     "CONSIDER"),
    (1769, "Mushahid Hussain",       65, "Tier C", "In Budget", "PKR 170,000",
     "8+ yrs (rel: 3 yrs)",
     "Donor Reporting Offr → Manager Partnerships, READ Foundation (ISB)",
     "READ Foundation competitor signal; USD 600K 'contributed to' — supporting BD role, not independently led; ISB-based",
     "CONSIDER"),
    (1381, "Hamdan Ahmad",           60, "Tier C", "Borderline", "PKR 320,000",
     "5 yrs (rel: 2 yrs)",
     "Social Safeguards Consultant, World Bank Group (ISB)",
     "Deep WB ecosystem network; strong stakeholder communication; ISB-based; high growth potential toward donor relations",
     "CONSIDER"),
    (2001, "Sobia Ayub",             58, "Tier C", "Borderline", "PKR 300,000",
     "2 yrs (rel: 1 yr)",
     "Fulbright Scholar; Masters Int'l Dev, Univ. of Pittsburgh 2025 (ISB-based)",
     "Fulbright (top credential); 8 RFP responses at Three Rivers Youth; grant writing Capstone; strong comms & representation profile; ISB-based",
     "CONSIDER"),
    (1431, "Faheem Baig",            55, "Tier C", "In Budget", "PKR 145,000",
     "10+ yrs (rel: 4 yrs)",
     "Program Manager, AKDN; prev DG-ECHO, GIZ, UN Women, USAID projects (ISB)",
     "Strong donor ecosystem exposure (DG-ECHO, GIZ, UN Women, USAID, AKDN); program lead who fundraises — not dedicated BD role",
     "CONSIDER"),
    # ── NO-HIRE: Borderline / Development Sector ─────────────────────────────
    (1958, "Sarmad Iqbal",           52, "No-Hire", "Out of Budget", "PKR 1,200,000",
     "20+ yrs",
     "B2G Partnerships Consultant (org names withheld in CV)",
     "Claims IRC Pakistan multi-year European institutional donor deal; unverifiable — all org names and dates deliberately removed from CV",
     "NO-HIRE"),
    (1874, "Mohammad Aqeel Qureshi", 48, "No-Hire", "In Budget", "PKR 180,000",
     "20+ yrs (rel: ~2 yrs)",
     "Manager Fundraising, Shifa Foundation (1 yr); Regional Mgr, Akhuwat (1.5 yrs)",
     "Community-level events/zakat fundraising; 20 yrs development program implementation, not BD lead",
     "NO-HIRE"),
    (1650, "Muhammad Usman",         44, "No-Hire", "Borderline", "PKR 350,000",
     "18+ yrs (rel: <2 yrs)",
     "Dy. Dir. Advancement, NUST (ISB); prev Program Mgr, Ali Trust",
     "University advancement + nonprofit ops; broad background; no bilateral donor network or closed deals",
     "NO-HIRE"),
    (1716, "Sadia Sohail",           42, "No-Hire", "In Budget", "PKR 140,000",
     "7+ yrs (rel: 2 yrs)",
     "Donor Relations Officer, READ Foundation (Rawalpindi, 2 yrs)",
     "READ competitor signal but junior supporting role; no quantified funding amounts independently raised",
     "NO-HIRE"),
    (1349, "Mahnoor Mellu",          40, "No-Hire", "Borderline", "PKR 350,000",
     "5 yrs (rel: 0 yrs)",
     "Partnerships Manager, Cloudways/DigitalOcean; Quoli.io; Educative (Lahore)",
     "Strong SaaS/tech partnerships experience (agency partners, B2B pipeline); zero institutional donor or development sector experience",
     "NO-HIRE"),
    (1517, "Zubair Hussain",         38, "No-Hire", "In Budget", "PKR 30,000*",
     "13+ yrs",
     "Program Mgr / Gender Specialist, GSF/Teach The World (ISB, Sindh work)",
     "Development sector background; proposal writing in supporting role; no lead BD track record (*salary entry appears to be a data error)",
     "NO-HIRE"),
    (1380, "Shakir Manzoor Khan",    36, "No-Hire", "Borderline", "PKR 350,000",
     "15+ yrs",
     "Head Healthcare Partnerships, Meethi Zindagi (RWP); prev Bayer HealthCare",
     "15+ yrs pharma sales; supported grant proposals in healthcare NGO; wrong sector",
     "NO-HIRE"),
    (1964, "Mehboob Alam",           36, "No-Hire", "Out of Budget", "USD 2,800/mo",
     "15+ yrs",
     "National Consultant, OCG Japan-JICA; prev Sr. Mgr Operations, AIMS Pakistan",
     "Program management; diaspora campaigns ($50K USD+32K GBP); USD-denominated salary ~PKR 780K",
     "NO-HIRE"),
    (1961, "Hira Noureen Khan",      35, "No-Hire", "In Budget", "PKR 250,000",
     "17+ yrs",
     "Manager PR & Resource Dev., Meethi Zindagi (RWP); prev Pharma Territory Mgr",
     "Healthcare NGO fundraising; diaspora $70K raised; pharma ecosystem, not institutional donors",
     "NO-HIRE"),
    (1875, "Samreen Durrani",        28, "No-Hire", "In Budget", "PKR 270,000",
     "8 yrs",
     "Content Developer Economy, MoIB (ISB); prev ops mgr, restaurant owner",
     "LUMS MPhil Economics; operations/research background; no fundraising track record",
     "NO-HIRE"),
    (1910, "Sikandar Khurshid",      25, "No-Hire", "In Budget", "PKR 185,000",
     "7 yrs",
     "Sales Manager, Shadiyana (ISB); prev Customer Success Mgr, Taleemabad",
     "Sales/CRM in tech; former Taleemabad employee (wrong function); no donor experience",
     "NO-HIRE"),
    (1541, "Sani Muhammad",          22, "No-Hire", "Out of Budget", "PKR 450,000",
     "8 yrs",
     "PM / Chief of Staff, ReBiz (US/PK tech); prev Zones LLC, Orbispay (ISB)",
     "Tech/SaaS B2B partnerships; wrong ecosystem; no development sector or institutional donor experience",
     "NO-HIRE"),
    (1884, "Bilal Shahid",           22, "No-Hire", "Not Disclosed", "Negotiable",
     "3 yrs",
     "M&A Team Manager, Jonas Software/Contour (Lahore)",
     "Corporate M&A; TCF volunteer fundraising only; Lahore-based; wrong sector",
     "NO-HIRE"),
    (1317, "Bareera Rauf",           22, "No-Hire", "Out of Budget", "USD 2,000/mo",
     "3 yrs",
     "Founder HopeWorks; Consultant (Karachi)",
     "Chevening Scholar, IDS Sussex; grassroots fundraising only; Karachi-based; junior; USD-denominated ~PKR 560K",
     "NO-HIRE"),
    (1991, "Bilal Muhammad Sajid",   22, "No-Hire", "In Budget", "PKR 160,000",
     "Intern",
     "LUMS Student (2026 graduation); AIESEC BD; ASI intern (ISB)",
     "Final-year undergrad; applied for wrong role (Impact & Policy); no relevant exp",
     "NO-HIRE"),
    (1355, "Samana Qaseem",          22, "No-Hire", "Out of Budget", "PKR 430,000",
     "Unknown", "Karachi-based", "Incomplete CV — Karachi-based; no relevant experience visible", "NO-HIRE"),
    (1970, "Sahrish Kashif",         18, "No-Hire", "In Budget", "PKR 250,000",
     "2 yrs",
     "Project Manager, Karishma Ali Foundation (ISB)",
     "Grassroots advocacy/SRHR programs; no institutional donor fundraising experience",
     "NO-HIRE"),
    (1699, "Hasan Shahid",           18, "No-Hire", "Out of Budget", "PKR 455,000",
     "4 yrs",
     "Project Manager, Turing (AI/LLM) - Lahore",
     "Media production / AI project management; SOAS Economics; no relevant fundraising",
     "NO-HIRE"),
    (1667, "Laveeza shah",           18, "No-Hire", "In Budget", "PKR 160,000",
     "1 yr",
     "Digital Marketing Specialist, Pixako Technologies (ISB)",
     "BBA grad 2024; volunteer fundraising at SOS Village only; no professional BD",
     "NO-HIRE"),
    (1363, "Arooj Irfan",            15, "No-Hire", "In Budget", "PKR 100,000",
     "12 yrs",
     "Clinical Psychologist, PIMS & Max Health Hospital (ISB)",
     "12 yrs clinical psychology; zero fundraising or development sector experience",
     "NO-HIRE"),
    (1963, "Ibrahim Basit",          15, "No-Hire", "In Budget", "PKR 100,000",
     "3 yrs",
     "Management Trainee, SMASH; prev Marketing Exec, Quantum Vision (ISB/Lahore)",
     "Marketing/content writer; no fundraising experience",
     "NO-HIRE"),
    (1362, "Moeen Hassan",           15, "No-Hire", "In Budget", "PKR 180,000+",
     "7 yrs",
     "AutoCAD Engineer / Operations Mgr (Lahore)",
     "Construction/real estate background; completely wrong profile for this role",
     "NO-HIRE"),
    (1957, "Bushra Nawaz",           15, "No-Hire", "In Budget", "PKR 175,000",
     "3 yrs",
     "Business & Job Placement Officer, Islamic Relief Pakistan (Muzaffarabad)",
     "Livelihoods/INGO field work; wrong location (Muzaffarabad); no fundraising",
     "NO-HIRE"),
    (1580, "Zainab",                 12, "No-Hire", "In Budget", "PKR 150,000",
     "1 yr",
     "TFP Fellow / Freelance Writer (Peshawar)",
     "Peshawar-based fresh grad; TFP = teaching role; no fundraising",
     "NO-HIRE"),
    (1702, "Asim Ur Rehman",         12, "No-Hire", "In Budget", "PKR 45,000",
     "2 yrs",
     "Social Mobilizer, Rehman Foundation (Peshawar)",
     "Peshawar-based; Sociology fresh grad; no fundraising experience",
     "NO-HIRE"),
    (2008, "Tanveer Alam",           12, "No-Hire", "In Budget", "PKR 145,000",
     "4 yrs",
     "Project Coord., GbeeTechive (Gilgit)",
     "Gilgit-based; project coordinator / proposal support; not fundraising lead",
     "NO-HIRE"),
    (1542, "Muhammad Akmal",         10, "No-Hire", "In Budget", "PKR 65,000",
     "1 yr",
     "Financial Mgmt. Trainer, Kashf Foundation (Jhang, Punjab)",
     "Jhang-based; financial trainer; no fundraising experience",
     "NO-HIRE"),
    # ── DUPLICATES ────────────────────────────────────────────────────────────
    (1347, "Danish Hussain",         88, "Tier A", "Out of Budget", "PKR 550,000",
     "20+ yrs",
     "Duplicate - see App 1346 (Hyderabad-based)",
     "Duplicate application; same profile; LOCATION FLAG (Hyderabad)",
     "DUPLICATE"),
    (1959, "sarmad iqbal",           52, "No-Hire", "Out of Budget", "PKR 1,200,000",
     "20+ yrs",
     "Duplicate - see App 1958",
     "Duplicate application",
     "DUPLICATE"),
    # ── INCOMPLETE APPLICATIONS ────────────────────────────────────────────────
    (1356, "Abdul Salam",            18, "No-Hire", "Out of Budget", "PKR 400,000",
     "Unknown", "Not disclosed", "Incomplete application", "NO-HIRE"),
    (1365, "Muhammad Ali Zafar",     18, "No-Hire", "In Budget", "PKR 100,000",
     "Unknown", "Not disclosed", "Incomplete application", "NO-HIRE"),
    (1387, "Imran Haider",           20, "No-Hire", "Borderline", "PKR 350,000",
     "Unknown", "Not disclosed", "Incomplete application", "NO-HIRE"),
    (1421, "AQSA GUL",               18, "No-Hire", "In Budget", "PKR 70,000",
     "Unknown", "Not disclosed", "Incomplete application", "NO-HIRE"),
    (1424, "Syeda Kainat",           20, "No-Hire", "In Budget", "PKR 110,000",
     "Unknown", "Not disclosed", "Incomplete application", "NO-HIRE"),
    (1333, "Zain Ul Abideen",        18, "No-Hire", "Borderline", "PKR 350,000",
     "Unknown", "Not disclosed", "Incomplete application — custom answer only, no CV submitted", "NO-HIRE"),
    (1334, "Ahmed Ali",              18, "No-Hire", "Out of Budget", "USD 3,500/mo",
     "Unknown", "Not disclosed", "Incomplete application; Yemen-based; USD salary", "NO-HIRE"),
    (1335, "Fahad Khan",             18, "No-Hire", "Borderline", "PKR 350,000",
     "Unknown", "Not disclosed", "Incomplete application", "NO-HIRE"),
    (1337, "Sameen Amjad Ali",       18, "No-Hire", "Out of Budget", "PKR 650,000",
     "Unknown", "Not disclosed", "Incomplete application", "NO-HIRE"),
    (1341, "Anita Kanwal",           18, "No-Hire", "In Budget", "PKR 200,000",
     "Unknown", "Not disclosed", "Incomplete application (dup of App 1336)", "NO-HIRE"),
    (1342, "Muhammad Taqi",          18, "No-Hire", "Out of Budget", "PKR 500,000",
     "Unknown", "Not disclosed", "Incomplete application", "NO-HIRE"),
    (1344, "Muhammad Sumraiz Kundi", 18, "No-Hire", "In Budget", "PKR 140,000",
     "Unknown", "Not disclosed", "Incomplete application", "NO-HIRE"),
    # ── LINKEDIN QUICK APPLY - NO CV ──────────────────────────────────────────
    (1225, "Aymen",                  10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV or info submitted", "NO-HIRE"),
    (1332, "umair",                  10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV submitted", "NO-HIRE"),
    (1336, "anitakanwal",            10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV (dup 1341)", "Duplicate; no CV", "NO-HIRE"),
    (1348, "mahnoor",                10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV submitted", "NO-HIRE"),
    (1350, "abeernoorbano",          10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV submitted", "NO-HIRE"),
    (1366, "tanveeralamm",           10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV submitted", "NO-HIRE"),
    (1372, "usmaanq",                10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV submitted", "NO-HIRE"),
    (1386, "imran",                  10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV submitted", "NO-HIRE"),
    (1393, "AAMIR SOHAIL",           10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "CV essentially empty (40 chars)", "Submitted near-empty CV twice", "NO-HIRE"),
    (1407, "saad",                   10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV submitted", "NO-HIRE"),
    (1418, "AAMIR SOHAIL",           10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV (dup 1393)", "Duplicate; no CV", "NO-HIRE"),
    (1515, "hassansajjadkhan",       10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV submitted", "NO-HIRE"),
    (1889, "rida",                   10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV submitted", "NO-HIRE"),
    (1938, "nayab",                  10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV submitted", "NO-HIRE"),
    (1967, "areebawaseempasha",      10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV submitted", "NO-HIRE"),
    (1972, "aftab",                  10, "No-Hire", "N/A", "Not Disclosed",
     "Unknown", "LinkedIn Quick Apply - no CV", "No CV submitted", "NO-HIRE"),
]

# Sort by score descending
CANDIDATES.sort(key=lambda x: -x[2])

SHORTLIST  = [c for c in CANDIDATES if c[9] in ("SHORTLIST", "CONSIDER") and c[3] != "No-Hire"]
HOLD       = [c for c in CANDIDATES if "HOLD" in c[9]]
TOP10      = CANDIDATES[:10]

# ─── STYLES ────────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    S = {}
    S["title"]    = ParagraphStyle("title",    parent=base["Normal"],
        fontSize=17, fontName="Helvetica-Bold", spaceAfter=3,
        textColor=colors.HexColor("#1a1a2e"))
    S["subtitle"] = ParagraphStyle("subtitle", parent=base["Normal"],
        fontSize=10, fontName="Helvetica", spaceAfter=10,
        textColor=colors.HexColor("#555555"))
    S["section"]  = ParagraphStyle("section",  parent=base["Normal"],
        fontSize=12, fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=5,
        textColor=colors.HexColor("#1a1a2e"))
    S["body"]     = ParagraphStyle("body",     parent=base["Normal"],
        fontSize=8.5, fontName="Helvetica", leading=11, spaceAfter=3)
    S["small"]    = ParagraphStyle("small",    parent=base["Normal"],
        fontSize=7.5, fontName="Helvetica", leading=10, spaceAfter=2,
        leftIndent=8)
    S["cell"]     = ParagraphStyle("cell",     parent=base["Normal"],
        fontSize=6.8, fontName="Helvetica", leading=8.5, wordWrap="LTR")
    S["cell_b"]   = ParagraphStyle("cell_b",   parent=base["Normal"],
        fontSize=6.8, fontName="Helvetica-Bold", leading=8.5, wordWrap="LTR")
    S["footer"]   = ParagraphStyle("footer",   parent=base["Normal"],
        fontSize=7, fontName="Helvetica-Oblique", textColor=colors.grey,
        alignment=TA_CENTER)
    S["warn"]     = ParagraphStyle("warn",     parent=base["Normal"],
        fontSize=7, fontName="Helvetica", leading=9,
        textColor=colors.HexColor("#8B0000"), wordWrap="LTR")
    return S

# ─── COLOUR HELPERS ────────────────────────────────────────────────────────────
TIER_FG = {
    "Tier A": colors.HexColor("#1a6b3c"),
    "Tier B": colors.HexColor("#1a4d8f"),
    "Tier C": colors.HexColor("#b36b00"),
    "No-Hire": colors.HexColor("#666666"),
}
TIER_BG = {
    "Tier A": colors.HexColor("#d4edda"),
    "Tier B": colors.HexColor("#cce5ff"),
    "Tier C": colors.HexColor("#fff3cd"),
    "No-Hire": colors.HexColor("#f0f0f0"),
}

BUDGET_BG = {
    "In Budget":     colors.HexColor("#d4edda"),
    "Borderline":    colors.HexColor("#fff3cd"),
    "Out of Budget": colors.HexColor("#f8d7da"),
    "Not Disclosed": colors.HexColor("#f0f0f0"),
}
BUDGET_FG = {
    "In Budget":     colors.HexColor("#1a6b3c"),
    "Borderline":    colors.HexColor("#856404"),
    "Out of Budget": colors.HexColor("#721c24"),
    "Not Disclosed": colors.HexColor("#666666"),
}

def verdict_color(v):
    if v == "SHORTLIST":     return colors.HexColor("#1a6b3c")
    if v == "CONSIDER":      return colors.HexColor("#b36b00")
    if "HOLD" in v:          return colors.HexColor("#8B6914")
    if v == "DUPLICATE":     return colors.HexColor("#888888")
    return colors.HexColor("#666666")

# ─── CHARTS ────────────────────────────────────────────────────────────────────
def make_bar_chart():
    names  = [c[1][:22] for c in TOP10]
    scores = [c[2]      for c in TOP10]
    tiers  = [c[3]      for c in TOP10]
    clr_map = {"Tier B": "#2e6da4", "Tier C": "#c47a17", "No-Hire": "#aaaaaa"}
    bar_clrs = [clr_map.get(t, "#aaaaaa") for t in tiers]

    fig, ax = plt.subplots(figsize=(11, 4.0))
    bars = ax.barh(range(len(names)), scores, color=bar_clrs, edgecolor="white", height=0.65)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Score (0-100)", fontsize=8)
    ax.set_title(f"Job {JOB_ID} - Top 10 Candidate Scores", fontsize=10,
                 fontweight="bold", pad=8)
    for th, clr, lbl in [(85,"#1a6b3c","Tier A (85+)"),
                          (70,"#2e6da4","Tier B (70+)"),
                          (55,"#c47a17","Tier C (55+)")]:
        ax.axvline(th, color=clr, linestyle="--", linewidth=0.8, alpha=0.6, label=lbl)
    for bar, s in zip(bars, scores):
        ax.text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2,
                str(s), va="center", ha="left", fontsize=7)
    ax.legend(fontsize=7, loc="lower right")
    ax.set_xlim(0, 105)
    ax.set_facecolor("#fafafa")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

DIMS = ["Functional\nMatch", "Demonstrated\nOutcomes", "Environment\nFit",
        "Ownership &\nExecution", "Stakeholder\nComms", "Hard Skills\n/Technical",
        "Growth &\nLeadership"]

RADAR_DATA = {
    1346: [4.0, 4.0, 1.5, 4.0, 3.5, 3.5, 3.5],  # Danish (docked env: location)
    1327: [4.0, 3.5, 4.0, 3.5, 3.5, 3.0, 3.0],  # mizhgan
    2013: [4.0, 3.5, 4.0, 4.0, 3.5, 3.0, 3.0],  # Adnan (C4ED bids: WB/GIZ/FCDO; ISB)
    1354: [4.0, 3.5, 4.0, 3.5, 3.0, 3.0, 3.0],  # Arsim
    1851: [3.5, 3.5, 4.0, 3.5, 3.5, 2.5, 3.0],  # Shahzad
    1357: [3.5, 3.5, 2.0, 3.5, 3.0, 3.0, 3.0],  # Arsalan (docked env: Karachi)
    1722: [3.0, 3.0, 3.5, 3.0, 3.0, 3.0, 3.0],  # Ahad
    1769: [3.0, 2.5, 4.0, 3.0, 3.0, 3.0, 2.5],  # Mushahid (revised down: supporting role)
    1381: [2.5, 2.0, 4.0, 2.5, 3.0, 2.5, 2.5],  # Hamdan (WB network; ISB-based)
    2001: [2.5, 2.5, 4.0, 2.5, 3.0, 2.0, 3.0],  # Sobia (academic strength; ISB-based)
}

def make_radar_chart():
    N = len(DIMS)
    angles = [n / float(N) * 2 * 3.14159 for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7.5, 5.5), subplot_kw=dict(polar=True))
    ax.set_theta_offset(3.14159 / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks([n / float(N) * 2 * 3.14159 for n in range(N)])
    ax.set_xticklabels(DIMS, size=7)
    ax.set_ylim(0, 4)
    ax.set_yticks([1, 2, 3, 4])
    ax.set_yticklabels(["1","2","3","4"], size=6)
    ax.set_facecolor("#fafafa")

    cmap = plt.cm.get_cmap("tab10")
    idx = 0
    for c in TOP10:
        if c[0] not in RADAR_DATA:
            continue
        vals = RADAR_DATA[c[0]] + [RADAR_DATA[c[0]][0]]
        ax.plot(angles, vals, linewidth=1.2, color=cmap(idx),
                label=c[1][:18], alpha=0.85)
        ax.fill(angles, vals, alpha=0.07, color=cmap(idx))
        idx += 1

    ax.legend(loc="upper right", bbox_to_anchor=(1.4, 1.15), fontsize=6.5)
    ax.set_title(f"Job {JOB_ID} - Competency Radar (Top 10)", size=9,
                 fontweight="bold", pad=18)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

def make_heatmap():
    short_dims = ["Func\nMatch","Outcomes","Env\nFit",
                  "Ownership","Comms","Hard\nSkills","Growth"]
    names = [c[1][:20] for c in TOP10]
    data = []
    for c in TOP10:
        if c[0] in RADAR_DATA:
            data.append(RADAR_DATA[c[0]])
        else:
            data.append([0]*7)
    data = [[float(v) for v in row] for row in data]

    fig, ax = plt.subplots(figsize=(11, 3.8))
    im = ax.imshow(data, aspect="auto", cmap="YlGn", vmin=0, vmax=4)
    ax.set_xticks(range(len(short_dims)))
    ax.set_xticklabels(short_dims, fontsize=7)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=7.5)
    for i in range(len(names)):
        for j in range(len(short_dims)):
            ax.text(j, i, f"{data[i][j]:.1f}", ha="center", va="center",
                    fontsize=7, color="black" if data[i][j] < 3 else "white")
    plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02, label="Score (0-4)")
    ax.set_title(f"Job {JOB_ID} - Competency Heatmap (Top 10)", size=9,
                 fontweight="bold", pad=8)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

# ─── BUILD PDF ─────────────────────────────────────────────────────────────────
def build_pdf(bar_buf, radar_buf, heatmap_buf):
    doc = SimpleDocTemplate(
        PDF_FILE,
        pagesize=landscape(A4),
        leftMargin=1.4*cm, rightMargin=1.4*cm,
        topMargin=1.4*cm,  bottomMargin=1.4*cm,
    )
    W, H = landscape(A4)
    CW = W - 2.8*cm
    S = build_styles()
    story = []

    # ── HEADER ────────────────────────────────────────────────────────────────
    story.append(Paragraph(f"Job {JOB_ID} — {JOB_TITLE}", S["title"]))
    story.append(Paragraph(
        f"Screening Report  |  Human-judgement re-screen by Coco  |  "
        f"68 candidates assessed  |  Budget: {BUDGET_STR}  |  Salary sourced from Markaz application form",
        S["subtitle"]))
    story.append(HRFlowable(width="100%", thickness=1.5,
                             color=colors.HexColor("#1a1a2e")))
    story.append(Spacer(1, 0.25*cm))

    # ── SECTION 1: DCA ────────────────────────────────────────────────────────
    story.append(Paragraph("1  Deep Comparative Analysis — All 68 Candidates", S["section"]))
    story.append(Paragraph(
        "All 68 applications screened against JD competency framework (Donor Ecosystem, Relationship Builder, "
        "Pipeline & Deal Execution, Communication, Personal Traits). Sorted by score (highest first). "
        "Expected salary sourced from Markaz application form (canned_answers). "
        "Budget column colour-coded: green = In Budget (≤270K) · amber = Borderline (271K–350K) · red = Out of Budget (>350K). "
        "Duplicates and LinkedIn-only applications listed at end.",
        S["body"]))
    story.append(Spacer(1, 0.15*cm))

    COL_W = [0.45*cm, 3.4*cm, 0.95*cm, 1.1*cm, 0.9*cm, 1.5*cm,
             2.0*cm, 4.2*cm, 5.9*cm, 1.85*cm]
    HDRS  = ["#", "Candidate", "Score", "Tier", "Budget", "Exp. Salary",
             "Experience", "Background / Current Role", "Key Strength / Note", "Verdict"]
    tdata = [[Paragraph(h, S["cell_b"]) for h in HDRS]]

    for idx, c in enumerate(CANDIDATES, 1):
        (app_id, name, score, tier, budget_status, exp_salary,
         exp, current_role, key_note, verdict) = c

        tdata.append([
            Paragraph(str(idx),     S["cell"]),
            Paragraph(f"<b>{name}</b><br/><font size='5.5'>App {app_id}</font>",
                      S["cell"]),
            Paragraph(f"<b>{score}</b>", S["cell_b"]),
            Paragraph(tier,             S["cell"]),
            Paragraph(budget_status,    S["cell"]),
            Paragraph(exp_salary,       S["cell"]),
            Paragraph(exp,              S["cell"]),
            Paragraph(current_role,     S["cell"]),
            Paragraph(key_note,         S["cell"]),
            Paragraph(verdict,          S["cell_b"]),
        ])

    tbl = Table(tdata, colWidths=COL_W, repeatRows=1)

    ts = [
        ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#2c5282")),
        ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
        ("ALIGN",         (0,0), (-1,-1), "LEFT"),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 3),
        ("RIGHTPADDING",  (0,0), (-1,-1), 2),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("GRID",          (0,0), (-1,-1), 0.25, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.white, colors.HexColor("#f8f8f8")]),
    ]
    for idx, c in enumerate(CANDIDATES, 1):
        tier = c[3]; budget_status = c[4]; verdict = c[9]; score = c[2]
        ts.append(("BACKGROUND", (3,idx),(3,idx), TIER_BG.get(tier, colors.white)))
        ts.append(("TEXTCOLOR",  (3,idx),(3,idx), TIER_FG.get(tier, colors.black)))
        ts.append(("BACKGROUND", (4,idx),(4,idx), BUDGET_BG.get(budget_status, colors.white)))
        ts.append(("TEXTCOLOR",  (4,idx),(4,idx), BUDGET_FG.get(budget_status, colors.black)))
        ts.append(("TEXTCOLOR",  (9,idx),(9,idx), verdict_color(verdict)))
        if score >= 70:
            ts.append(("BACKGROUND",(2,idx),(2,idx), colors.HexColor("#e6f4ea")))
        elif score >= 55:
            ts.append(("BACKGROUND",(2,idx),(2,idx), colors.HexColor("#fff8e1")))

    tbl.setStyle(TableStyle(ts))
    story.append(tbl)
    story.append(Spacer(1, 0.4*cm))

    # ── SECTION 2: VISUAL ANALYTICS ────────────────────────────────────────────
    story.append(Paragraph("2  Visual Analytics — Top 10 Candidates", S["section"]))

    bar_img   = RLImage(bar_buf,   width=CW*0.56, height=4.5*cm)
    radar_img = RLImage(radar_buf, width=CW*0.42, height=5.5*cm)
    ct = Table([[bar_img, radar_img]], colWidths=[CW*0.58, CW*0.42])
    ct.setStyle(TableStyle([
        ("VALIGN",       (0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",  (0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(-1,-1), 0),
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
    ]))
    story.append(ct)
    story.append(Spacer(1, 0.3*cm))

    # ── SECTION 3: STRONG MATCH — OUT OF BUDGET / LOCATION FLAG ───────────────
    story.append(Paragraph("3  Strong Match — Out of Budget / Location Flag", S["section"]))
    story.append(Paragraph(
        "Four strong candidates scored Tier A/B but are out of budget (salary > PKR 270K) or location-flagged. "
        "Recommend salary negotiation or relocation check before passing on these profiles.",
        S["body"]))
    story.append(Spacer(1, 0.15*cm))

    oob_hdrs = ["App", "Candidate", "Score", "Exp. Salary", "Issue",
                "Why They're Strong", "Recommended Action"]
    oob_cws  = [0.9*cm, 3.0*cm, 1.0*cm, 2.2*cm, 2.2*cm, 7.0*cm, 7.0*cm]
    oob_data = [[Paragraph(h, S["cell_b"]) for h in oob_hdrs]]

    oob_rows = [
        (1346, "Danish Hussain",    88, "PKR 550,000", "OOB + Hyderabad",
         "PKR 1B+ closed (WB, ADB, FCDO, EU, UN); 20+ yrs institutional fundraising; strongest in pool.",
         "Confirm relocation intent first. If willing to relocate AND negotiate: priority interview."),
        (2013, "Muhammad Adnan",    82, "PKR 575,000", "Out of Budget",
         "Global Acquisition Mgr at C4ED — manages WB/UN/GIZ/FCDO bids; CERP World Bank CLEAR; GIZ TVET; ISB-based.",
         "Strong donor BD profile; ISB-based. PKR 575K is 2× budget — engage on salary."),
        (1357, "Arsalan Ashraf",    72, "PKR 450,000", "OOB + Karachi",
         "Closed Meta USD 100K, Chevron USD 250K, Govt Sindh PKR 30M; diaspora USD 40K/month recurring.",
         "Confirm ISB relocation. If salary negotiable and location confirmed: interview."),
        (1722, "Ahad Ahsan Khan",   67, "PKR 550,000", "Out of Budget",
         "AKU $134M grants portfolio; raised PKR 26.5M at NHSD NGO (UN, USAID, GGP Japan); ISB hometown; willing to relocate.",
         "Solid grants background. Salary 2× budget. Only pursue if budget is flexible."),
    ]
    for app_id, name, score, salary, issue, strength, action in oob_rows:
        oob_data.append([
            Paragraph(str(app_id), S["cell"]),
            Paragraph(f"<b>{name}</b>", S["cell"]),
            Paragraph(f"<b>{score}</b>", S["cell_b"]),
            Paragraph(salary, S["warn"]),
            Paragraph(issue, S["warn"]),
            Paragraph(strength, S["cell"]),
            Paragraph(action, S["cell"]),
        ])

    oob_tbl = Table(oob_data, colWidths=oob_cws, repeatRows=1)
    oob_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), colors.HexColor("#2c5282")),
        ("TEXTCOLOR",     (0,0),(-1,0), colors.white),
        ("GRID",          (0,0),(-1,-1), 0.3, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.HexColor("#fff8f8"), colors.HexColor("#fffdf0")]),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 3),
        ("RIGHTPADDING",  (0,0),(-1,-1), 3),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
    ]))
    story.append(oob_tbl)
    story.append(Spacer(1, 0.4*cm))

    # ── SECTION 4: HEATMAP ────────────────────────────────────────────────────
    story.append(Paragraph("4  Competency Heatmap — Top 10 Candidates", S["section"]))
    hm_img = RLImage(heatmap_buf, width=CW*0.80, height=4.5*cm)
    story.append(hm_img)
    story.append(Spacer(1, 0.4*cm))

    # ── SECTION 5: WHY OTHERS DIDN'T MAKE IT ─────────────────────────────────
    story.append(Paragraph("5  Why Others Didn't Make the Cut", S["section"]))

    reasons = [
        ("Pool Quality Warning",
         "This was a weak pool for a senior fundraising role. Of 67 applications, only 4 "
         "Tier B candidates are genuinely ISB-based with relevant institutional donor track "
         "records. The posting attracted heavy volume from marketing professionals, IT/SaaS "
         "sales, development program managers, and fresh graduates — candidates who can pitch "
         "but have never closed institutional donor deals. Recommend re-advertising with "
         "explicit donor keywords: DFID/FCDO, World Bank, USAID, bilateral, grant pipeline."),
        ("14 LinkedIn Quick Apply / Empty CVs "
         "(Apps 1225, 1332, 1336, 1348, 1350, 1366, 1372, 1386, 1393, 1407, 1418, 1515, "
         "1889, 1938, 1967, 1972)",
         "No CV or near-empty placeholder submitted. Cannot assess."),
        ("Sarmad Iqbal (1958/1959) — 52 pts",
         "Claims 20+ years and an IRC Pakistan multi-year European institutional donor deal "
         "in his cover letter. However, the CV deliberately withholds all organisation names "
         "and dates. Unverifiable. May warrant a brief screening call only if shortlisted "
         "candidates don't move forward."),
        ("Development Sector Professionals Without Fundraising Lead Role "
         "(Aqeel Qureshi 48, Muhammad Usman 44, Sadia Sohail 42, Mahnoor Mellu 40, "
         "Zubair Hussain 38, Shakir Manzoor Khan 36, Mehboob Alam 36)",
         "Solid professional CVs — but no dedicated fundraising / BD lead role. Aqeel's "
         "'Manager Fundraising' at Shifa Foundation was only 1 year, preceded by 20 years "
         "of program implementation. Mahnoor Mellu (Cloudways/Quoli) has strong SaaS "
         "partnerships skills but zero institutional donor or development sector experience. "
         "Sadia Sohail at READ Foundation was a junior Donor Relations Officer (2 yrs) "
         "with no independently raised amounts stated."),
        ("IT / Tech / Sales / Marketing / Adjacent Sectors "
         "(Sikandar, Sani, Bilal Shahid, Ibrahim Basit, Moeen Hassan, Hasan Shahid, "
         "Laveeza Shah, Bilal Sajid, Samreen Durrani, Sahrish Kashif, Arooj Irfan)",
         "Candidates from SaaS, M&A, digital marketing, clinical psychology, construction, "
         "and AI/tech backgrounds. Several wrote strong cover letters but have no institutional "
         "donor relationships, no Pakistan bilateral-donor track record, and no experience "
         "closing grants or government partnerships at scale."),
        ("Healthcare Sector Fundraisers (Hira Noureen Khan 35, Shakir Manzoor Khan 36)",
         "Resource mobilisation experience exists but in healthcare NGOs (Type 1 diabetes "
         "programs, pharma partnerships). Meethi Zindagi's fundraising ecosystem is diaspora "
         "and pharma CSR — completely distinct from DFID/WB/USAID bilateral donor relations "
         "needed for EdTech/education sector."),
        ("Location Disqualifiers (Danish Hussain Hyderabad, Arsalan Ashraf Karachi, "
         "Mehboob Alam Peshawar, Zainab/Asim Peshawar, Bushra Nawaz Muzaffarabad, "
         "Tanveer Alam Gilgit, Zubair Hussain Sindh-work)",
         "JD is explicit: in-office Islamabad only. Candidates not based in or credibly "
         "willing to relocate to Islamabad were not shortlisted. Danish Hussain is flagged "
         "separately as a strong profile contingent on relocation confirmation."),
        ("Fresh Graduates / Students "
         "(Bilal Sajid, Laveeza Shah, Asim Ur Rehman, Zainab, Bareera Rauf)",
         "Year 1 target is $500K-$1M in new funding. Requires existing relationships and "
         "a proven deal-closing track record — not achievable at entry-level."),
    ]

    for heading, detail in reasons:
        story.append(Paragraph(f"<b>{heading}</b>", S["body"]))
        story.append(Paragraph(detail, S["small"]))
        story.append(Spacer(1, 0.12*cm))

    story.append(Spacer(1, 0.3*cm))

    # ── SECTION 6: NEXT STEPS ─────────────────────────────────────────────────
    story.append(Paragraph("6  Next Steps", S["section"]))

    steps = [
        "1.  IN-BUDGET PRIORITY — Interview mizhgan kirmani (1327, Score 84, PKR 250K). "
        "Best ISB-based in-budget candidate: TCF + Tearfund UK competitor signal, "
        "PKR 72.2M closed FY23-24, bilateral donor network. Start here.",
        "2.  IN-BUDGET — Interview Shahzad Saleem Abbasi (1851, Score 75, PKR 270K — exactly "
        "at budget ceiling). PKR 400M+/yr at Alkhidmat; 10,000+ donors; ISB-based.",
        "3.  IN-BUDGET TIER C — Mushahid Hussain (1769, Score 65, PKR 170K) and "
        "Faheem Baig (1431, Score 55, PKR 145K). Both comfortably in budget. "
        "Mushahid: READ Foundation competitor signal. Faheem: GIZ/AKDN/DG-ECHO donor exposure.",
        "4.  SALARY NEGOTIATION — Engage Muhammad Adnan (2013, Score 82, PKR 575K). "
        "ISB-based. Manages WB/GIZ/FCDO bids at C4ED — exactly the right background. "
        "Budget gap is large (2×) but worth the conversation given the profile strength.",
        "5.  BORDERLINE — Arsim Tariq (1354, Score 78, PKR 280K-300K) is slightly above "
        "budget ceiling. Strongest multilateral pipeline experience (20+ WB/UNDP/UN Women "
        "projects). Consider if budget has any flex.",
        "6.  LOCATION + SALARY CHECK — Danish Hussain (1346, Score 88, PKR 550K, Hyderabad) "
        "is the strongest in the pool on track record. Two barriers to clear: salary and "
        "relocation. If either is resolved, interview immediately.",
        "7.  Arsalan Ashraf (1357, Score 72, PKR 450K, Karachi) — confirm ISB relocation "
        "intent AND salary negotiability before proceeding. Strong CSR closings.",
        "8.  Hamdan Ahmad (1381, 60, PKR 320K) and Sobia Ayub (2001, 58, PKR 300K) — both "
        "borderline on budget. Good profiles for consideration if Tier B interviews don't close.",
        "9.  Pool warning: Of 68 applications, only 2–3 candidates are genuinely qualified "
        "AND in-budget. Re-post with explicit salary range visible and stronger donor keywords "
        "(FCDO/DFID, World Bank, USAID, bilateral) to attract the right experience level.",
    ]
    for step in steps:
        story.append(Paragraph(step, S["body"]))
        story.append(Spacer(1, 0.08*cm))

    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.12*cm))
    story.append(Paragraph(
        f"Coco — Taleemabad Talent Acquisition Agent  |  Confidential  |  "
        f"Job {JOB_ID}: {JOB_TITLE}  |  Screened 2026-03-10",
        S["footer"]))

    doc.build(story)
    size_kb = os.path.getsize(PDF_FILE) // 1024
    print(f"PDF built: {PDF_FILE}  ({size_kb} KB)")

# ─── SEND EMAIL ────────────────────────────────────────────────────────────────
def send_email():
    n_shortlisted = len(SHORTLIST)
    n_hold        = len(HOLD)

    html = f"""
<html><body style="font-family:Arial,sans-serif;font-size:14px;color:#1a1a2e;
                   max-width:620px;margin:auto;padding:20px">
<p>Hi Ayesha,</p>
<p>Please find attached the <b>re-screened report</b> for
<b>Job {JOB_ID} — {JOB_TITLE}</b>.
This is a full human-judgement re-screen of all 67 applications.
The previous automated screening has been discarded.</p>

<table width="100%" cellpadding="14" cellspacing="0"
       style="border-collapse:collapse;margin:20px 0">
  <tr>
    <td align="center"
        style="background:#e8f4fd;border:1px solid #b8daff;border-radius:6px;width:32%">
      <div style="font-size:26px;font-weight:bold;color:#1a1a2e">68</div>
      <div style="font-size:11px;color:#555">Total Screened</div>
    </td>
    <td width="8"></td>
    <td align="center"
        style="background:#e6f4ea;border:1px solid #b8dbc4;border-radius:6px;width:32%">
      <div style="font-size:26px;font-weight:bold;color:#1a6b3c">{n_shortlisted}</div>
      <div style="font-size:11px;color:#555">Shortlisted</div>
    </td>
    <td width="8"></td>
    <td align="center"
        style="background:#fff8e1;border:1px solid #ffc107;border-radius:6px;width:32%">
      <div style="font-size:26px;font-weight:bold;color:#8B6914">{n_hold}</div>
      <div style="font-size:11px;color:#555">Location Flagged</div>
    </td>
  </tr>
</table>

<p><b>In-budget top pick:</b> <b>mizhgan kirmani</b> (App 1327, Score 84, PKR 250K) —
TCF + Tearfund UK, PKR 72.2M closed FY23-24, bilateral donor network, ISB-based, within budget.</p>

<p><b>Strongest overall:</b> <b>Danish Hussain</b> (App 1346, Score 88, expected PKR 550K) and
<b>Muhammad Adnan</b> (App 2013, Score 82, expected PKR 575K) are the most qualified profiles
but both exceed budget. See Section 3 for the out-of-budget flagged candidates and recommended actions.</p>

<p><b>Budget note:</b> Expected salaries are now sourced directly from the Markaz application form.
Of the top 5 shortlisted candidates, only mizhgan (250K) and Shahzad (270K) are in budget.
Consider whether budget can flex for the right profile, or re-post with salary range visible.</p>

<p>Full analysis in the attached PDF.</p>

<p style="margin-top:28px;font-size:12px;color:#888">
Coco — Taleemabad Talent Acquisition Agent &nbsp;|&nbsp; Confidential
</p>
</body></html>
"""

    msg = MIMEMultipart("mixed")
    msg["From"]    = GMAIL_USER
    msg["To"]      = TO_EMAIL
    msg["Subject"] = f"Screening Report- {JOB_TITLE}"

    msg.attach(MIMEText(html, "html"))

    with open(PDF_FILE, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        fname = f"Job{JOB_ID}_Fundraising_Partnerships_Screening.pdf"
        part.add_header("Content-Disposition", f'attachment; filename="{fname}"')
        msg.attach(part)

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as s:
        s.login(GMAIL_USER, GMAIL_APP_PW)
        s.sendmail(GMAIL_USER, [TO_EMAIL], msg.as_string())
    print(f"Email sent to: {TO_EMAIL}")

# ─── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Building charts...")
    bar_buf     = make_bar_chart()
    radar_buf   = make_radar_chart()
    heatmap_buf = make_heatmap()

    print("Building PDF...")
    build_pdf(bar_buf, radar_buf, heatmap_buf)

    bar_buf.seek(0); radar_buf.seek(0); heatmap_buf.seek(0)

    if not GMAIL_APP_PW:
        print("GMAIL_APP_PASSWORD not set — skipping email.")
        print(f"PDF saved: {PDF_FILE}")
    else:
        print("Sending email...")
        send_email()
        print("Done.")
