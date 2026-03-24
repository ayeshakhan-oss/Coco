"""
Job 26 — Soul Architect / Conversational UX Designer
Screening report PDF — send to ayesha.khan@taleemabad.com only
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
import numpy as np

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, PageBreak, HRFlowable
)

load_dotenv()

RECIPIENT = "ayesha.khan@taleemabad.com"
SENDER    = os.getenv("EMAIL_USER")
PASSWORD  = os.getenv("EMAIL_PASSWORD")

JOB_TITLE      = "Soul Architect / Conversational UX Designer"
JOB_ID         = 26
TOTAL_SCREENED = 42
BUDGET_RANGE   = "TBD"

C_TEAL  = colors.HexColor("#005F73")
C_AMBER = colors.HexColor("#EE9B00")
C_RED   = colors.HexColor("#AE2012")
C_GREEN = colors.HexColor("#2D6A4F")
C_LIGHT = colors.HexColor("#F4F4F4")
C_MID   = colors.HexColor("#E0E0E0")
C_DARK  = colors.HexColor("#1A1A2E")
C_WHITE = colors.white

TIER_COLOURS = {
    "Tier B":  colors.HexColor("#2D6A4F"),
    "Tier C":  colors.HexColor("#EE9B00"),
    "No-Hire": colors.HexColor("#AE2012"),
}

def PS(name, **kw):
    return ParagraphStyle(name, **kw)

hdr_s  = PS("hdr",  fontName="Helvetica-Bold", fontSize=6.5, textColor=C_WHITE,
             alignment=TA_CENTER, leading=9, wordWrap="LTR")
cell_s = PS("cell", fontName="Helvetica", fontSize=6.5, leading=8.5, wordWrap="LTR", textColor=C_DARK)
cent_s = PS("cent", fontName="Helvetica", fontSize=6.5, leading=8.5, alignment=TA_CENTER,
             textColor=C_DARK, wordWrap="LTR")
bold_s = PS("bold", fontName="Helvetica-Bold", fontSize=6.5, leading=8.5, textColor=C_DARK, wordWrap="LTR")
h1_s   = PS("h1",   fontName="Helvetica-Bold", fontSize=14, textColor=C_TEAL, leading=18, spaceAfter=4)
h2_s   = PS("h2",   fontName="Helvetica-Bold", fontSize=10, textColor=C_DARK, leading=13,
             spaceAfter=3, spaceBefore=8)
body_s = PS("body", fontName="Helvetica", fontSize=8, leading=11, textColor=C_DARK)
foot_s = PS("foot", fontName="Helvetica", fontSize=6.5, alignment=TA_CENTER,
             textColor=colors.HexColor("#888888"))

CANDIDATES = [
    # TIER B — genuine JD match
    {"rank":1,"name":"Danyal Haroon","app_id":1315,"score":73.0,"tier":"Tier B",
     "total_exp":"~4 yrs","relevant_exp":"~2 yrs (UX/AI design + academic human-AI research)",
     "current_role":"UX Design Specialist — AIO App Inc. (AI restaurant platform, Silicon Valley); "
                    "currently MA Digital Media — Univ. of Manchester",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Best overall JD match in pool. LUMS CS + MA dissertation on AI chatbot interfaces. "
                    "Daily AI tool user (ChatGPT, Claude, Gemini). Qualitative research: 18-city HBL focus groups. "
                    "Strong writer. Understands human-AI interaction academically and practically. "
                    "Gap: behavioral science is adjacent (MA coursework), not primary training — not a trained "
                    "psychologist or anthropologist. Only candidate who hits 4/5 JD must-haves.",
     "verdict":"RECOMMEND","dims":(3,4,4,3,4,4,4)},
    # TIER C — Taleemabad-native, worth interviewing
    {"rank":2,"name":"Aisha Bashir","app_id":980,"score":65.0,"tier":"Tier C",
     "total_exp":"~10 yrs","relevant_exp":"~6 yrs (Taleemabad educational content creation + team lead)",
     "current_role":"Animator & Illustrator — Taleemabad (Apr 2024–Dec 2025); MPhil Art & Design, Indus Valley",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"10 years creating educational content at Taleemabad — script writing, lesson planning, "
                    "supervising 40+ Urdu ed-videos and 86+ books. Deep practical knowledge of teacher psychology "
                    "and educational media. Strong writer and creative director. MPhil Art & Design. "
                    "Gap: no AI tool fluency evidenced; no formal behavioral science or qualitative research. "
                    "Interview to assess AI readiness and research thinking — Taleemabad context is a real asset.",
     "verdict":"CONSIDER","dims":(2,3,4,3,3,2,3)},
    # TIER C — Conversational UX / HCI profile
    {"rank":3,"name":"Muhammad Taimoor","app_id":1259,"score":62.0,"tier":"Tier C",
     "total_exp":"~4 yrs","relevant_exp":"~2 yrs (Conversational UX, HCI-focused UX design)",
     "current_role":"UX Designer — Rofoof, Saudi Arabia (Oct 2023–Apr 2025, Remote); "
                    "MSc Human-Centered Systems & Digital Products, Univ. of Gujrat",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Conversational UX Designer profile — explicitly lists Conversational UX, "
                    "Prompt-Based UX Exploration, and AI-Assisted Design. MSc in Human-Centered Systems. "
                    "4 years UX across SaaS, marketplace, telehealth, and a language translation app "
                    "(cross-cultural scope). Fits 'Conversational UX Designer' and 'HCI' profiles directly. "
                    "Gap: no behavioral science training; domain is e-commerce/SaaS rather than ed-tech.",
     "verdict":"CONSIDER","dims":(2,2,3,3,3,3,3)},
    # TIER C — AI Interaction / Behavioral Designer profile
    {"rank":4,"name":"Muhammad Ammar Khan","app_id":974,"score":55.0,"tier":"Tier C",
     "total_exp":"~1 yr","relevant_exp":"~1 yr (AI-assisted design, behavior-driven UX)",
     "current_role":"UX/AI Design — Freelance (SZABIST CS graduate 2025, Rawalpindi)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Profile states: 'focused on how people emotionally and culturally interact with digital systems; "
                    "human-AI relationships, behavior-driven design, culturally responsive experiences.' "
                    "Daily AI tool user (ChatGPT, Gemini, Runway, Claude). Analyses how tone, wording, "
                    "and structure change user perception — behavioral design language. "
                    "JD says 'we don't care about the degree' — profile intent + AI fluency are genuine. "
                    "Fits 'AI Interaction Designer' and 'Behavioral Designer' profiles. "
                    "Gap: fresh grad, limited formal experience.",
     "verdict":"CONSIDER","dims":(2,1,3,3,3,3,4)},
    # NO-HIRE
    {"rank":5,"name":"Hulalah Khan","app_id":1318,"score":48.0,"tier":"No-Hire",
     "total_exp":"~2.5 yrs","relevant_exp":"~2.5 yrs (counselling, teaching, academic research)",
     "current_role":"College Counsellor — The Orange Tree Foundation (Nov 2023–Present)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Strong behavioral science foundation (LUMS Sociology-Anthropology + Psychology minor). "
                    "Good qualitative research training and writing ability. "
                    "Missing the critical JD must-have: AI tool fluency. No evidence of daily AI usage, "
                    "prompt writing, or conversational design. Skills (SPSS, R-Studio) are traditional research tools. "
                    "Early-career profile — the implementation layer is absent.",
     "verdict":"NO-HIRE","dims":(4,2,3,2,3,1,3)},
    {"rank":6,"name":"Asad Nawaz","app_id":1294,"score":42.0,"tier":"No-Hire",
     "total_exp":"~5 yrs","relevant_exp":"0 (product design; no JD must-haves met)",
     "current_role":"Sr. Product Designer — Addo AI, San Francisco (Jan 2025–Present, Remote)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Impressive product design portfolio (Vyro.ai 100M+ downloads, Qlu.ai $5M deal). "
                    "This role is NOT primarily a product design role — it requires behavioral science, "
                    "ethnographic research, philosophical thinking, and persuasive writing. "
                    "Electrical Engineering + fintech domain. Does not meet core JD requirements.",
     "verdict":"NO-HIRE","dims":(1,3,1,3,2,3,2)},
    {"rank":7,"name":"Rimsha Faisal","app_id":1322,"score":52.0,"tier":"No-Hire",
     "total_exp":"~1 yr","relevant_exp":"<1 yr (UI/UX)",
     "current_role":"Product Designer — AIO App Inc. (Dec 2024–Present, Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Junior UI/UX designer with AI interface work. No behavioral science, conversational design depth, or content writing specialty.",
     "verdict":"NO-HIRE","dims":(2,1,3,2,2,3,2)},
    {"rank":8,"name":"Hamza Ahmed","app_id":1285,"score":47.0,"tier":"No-Hire",
     "total_exp":"~3 yrs","relevant_exp":"0",
     "current_role":"Product Designer — GrowthRune, Florida (Nov 2025–Present, Remote)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Experienced product designer but fintech/SaaS. No behavioral science, conversational AI, or content writing.",
     "verdict":"NO-HIRE","dims":(1,3,2,3,3,3,2)},
    {"rank":9,"name":"Arslan Saleem","app_id":1260,"score":45.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0",
     "current_role":"Lead UX/UI Designer (Lahore)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Solid UX/UI portfolio. No behavioral science, conversational design, or AI writing.",
     "verdict":"NO-HIRE","dims":(1,2,2,3,3,3,2)},
    {"rank":10,"name":"Faizan Ullah","app_id":1326,"score":45.0,"tier":"No-Hire",
     "total_exp":"~3 yrs","relevant_exp":"0",
     "current_role":"UI/UX Designer — UET Peshawar (currently Riyadh, visit visa)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"3+ yrs UI/UX. No behavioral science or conversational design. Based abroad.",
     "verdict":"NO-HIRE","dims":(1,2,1,2,2,3,2)},
    {"rank":11,"name":"Ghulam Qadir","app_id":1311,"score":43.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Staff UI/UX Designer (Karachi)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"UI/UX background. No behavioral science or conversational design.",
     "verdict":"NO-HIRE","dims":(1,2,2,2,2,3,2)},
    {"rank":12,"name":"Muhammad Jaffer","app_id":1287,"score":42.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UI/UX Designer (Rawalpindi)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"UI/UX designer. No conversational design, behavioral science, or AI writing.",
     "verdict":"NO-HIRE","dims":(1,2,3,2,2,2,2)},
    {"rank":13,"name":"Aaqib Khan","app_id":1313,"score":40.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UI/UX Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"UI/UX profile. No behavioral science, conversational AI, or content writing.",
     "verdict":"NO-HIRE","dims":(1,2,3,2,2,2,2)},
    {"rank":14,"name":"Nain Tara","app_id":1320,"score":38.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UX Designer / Researcher (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"UX researcher background. No behavioral science framework or conversational design.",
     "verdict":"NO-HIRE","dims":(1,1,3,2,2,2,2)},
    {"rank":15,"name":"Hassan Bin Tariq","app_id":1289,"score":38.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Product / UX Designer (Rawalpindi)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Product/UX design focus. No behavioral science or conversational AI depth.",
     "verdict":"NO-HIRE","dims":(1,1,3,2,2,2,2)},
    {"rank":16,"name":"Muhammad Taufeeq","app_id":1279,"score":37.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UI/UX Designer (Rawalpindi)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Standard UI/UX profile. No JD fit on behavioral science or conversational design.",
     "verdict":"NO-HIRE","dims":(1,1,3,2,2,2,2)},
    {"rank":17,"name":"Talal Hassan Khan","app_id":1319,"score":36.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UI Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Visual UI focus. No behavioral science, conversational design, or AI writing.",
     "verdict":"NO-HIRE","dims":(1,1,3,2,2,2,2)},
    {"rank":18,"name":"Ahmad Hamdan Akram","app_id":1263,"score":35.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UX Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"UX design background. No behavioral science or conversational AI.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,2,2,2)},
    {"rank":19,"name":"Manahil Ahmed","app_id":1301,"score":35.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UX Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"UI/UX profile. No behavioral science, conversational design, or AI fluency.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,2,2,2)},
    {"rank":20,"name":"Asma Butt","app_id":1309,"score":35.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UX Researcher (Lahore)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"UX research focus. No behavioral science framework, conversational AI, or content writing.",
     "verdict":"NO-HIRE","dims":(1,1,1,1,2,2,2)},
    {"rank":21,"name":"Hamza Jamal","app_id":1316,"score":33.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UI/UX Designer (Lahore)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"UI/UX designer. No JD alignment on behavioral science or conversational design.",
     "verdict":"NO-HIRE","dims":(1,1,1,1,2,2,2)},
    {"rank":22,"name":"Zehra Rashid","app_id":1302,"score":32.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UX / Content Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Some content design exposure but no behavioral science depth or AI fluency.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,2,2,1)},
    {"rank":23,"name":"Zikra Fiaz","app_id":1307,"score":30.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UX Designer (Rawalpindi)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Junior UX profile. No behavioral science, conversational design, or AI tools.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,2,1)},
    {"rank":24,"name":"Muhammad Abdullah Safdar","app_id":1277,"score":30.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Graphic / UI Designer (Rawalpindi)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Graphic/UI focus. No relevance to behavioral science or conversational UX.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,2,1)},
    {"rank":25,"name":"Ameer Hamza Tariq","app_id":1044,"score":28.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UI Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Junior designer profile. Does not meet JD requirements.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,2,1)},
    {"rank":26,"name":"Zia Ullah","app_id":1273,"score":28.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UI/UX Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Standard UI/UX profile. No behavioral science or conversational design match.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,2,1)},
    {"rank":27,"name":"Sanaullah Mukhtar","app_id":1286,"score":28.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UX Designer (Faisalabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Brief UX profile. No behavioral science or conversational AI match.",
     "verdict":"NO-HIRE","dims":(1,1,1,1,1,2,1)},
    {"rank":28,"name":"Muhammad Ali","app_id":1300,"score":28.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Designer (Rawalpindi)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Designer profile. No JD fit on behavioral science or conversational design.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,2,1)},
    {"rank":29,"name":"Hadia Sajjad","app_id":1328,"score":27.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UX Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Short UX profile. No behavioral science, conversational AI, or content writing.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,2,1)},
    {"rank":30,"name":"Muhammad Wasi Haider","app_id":1268,"score":25.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"UI Designer (Rawalpindi)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"UI designer. Does not meet JD requirements.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,1,1)},
    {"rank":31,"name":"UIxFly (Moheed)","app_id":1270,"score":25.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Freelance UI Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Freelance UI design. No behavioral science or conversational UX.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,1,1)},
    {"rank":32,"name":"Sameen Ali","app_id":1291,"score":25.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Designer profile. No JD match.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,1,1)},
    {"rank":33,"name":"Saad Imran","app_id":1304,"score":25.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Designer (Wah Cantt)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Junior designer. Does not meet JD requirements.",
     "verdict":"NO-HIRE","dims":(1,1,2,1,1,1,1)},
    {"rank":34,"name":"Syed Manan Ali","app_id":1284,"score":22.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Junior Designer (Rawalpindi)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Very junior profile. No JD match.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,1,1)},
    {"rank":35,"name":"Saad Sajid","app_id":1297,"score":22.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Junior profile. Does not meet JD requirements.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,1,1)},
    {"rank":36,"name":"Muhammad Ibrahim Khan","app_id":1272,"score":20.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Very brief profile. No JD fit.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,1,1)},
    {"rank":37,"name":"Majid Raffique","app_id":1290,"score":20.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Minimal profile. No JD match.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,1,1)},
    {"rank":38,"name":"Muhammad Ali (II)","app_id":1296,"score":18.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Designer (Rawalpindi)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Thin profile. Does not meet JD requirements.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,1,1)},
    {"rank":39,"name":"Sholmiyat Adnan","app_id":976,"score":15.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Designer (Islamabad)",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"Minimal CV content. No JD fit.",
     "verdict":"NO-HIRE","dims":(1,1,3,1,1,1,1)},
    {"rank":40,"name":"zennab Applicant","app_id":1262,"score":5.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Incomplete application",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"No CV or profile submitted. Could not be assessed.",
     "verdict":"NO-HIRE","dims":(0,0,0,0,0,0,0)},
    {"rank":41,"name":"wajihazainab Applicant","app_id":1305,"score":5.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Incomplete application",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"No CV or profile submitted. Could not be assessed.",
     "verdict":"NO-HIRE","dims":(0,0,0,0,0,0,0)},
    {"rank":42,"name":"hamza Applicant","app_id":1314,"score":5.0,"tier":"No-Hire",
     "total_exp":"—","relevant_exp":"0","current_role":"Incomplete application",
     "salary":"Not mentioned","budget_label":"TBD",
     "key_strength":"No CV or profile submitted. Could not be assessed.",
     "verdict":"NO-HIRE","dims":(0,0,0,0,0,0,0)},
]

SHORTLIST = [c for c in CANDIDATES if c["score"] >= 55]


def bar_chart():
    names  = [c["name"] for c in SHORTLIST]
    scores = [c["score"] for c in SHORTLIST]
    bar_colors = ["#2D6A4F" if c["tier"]=="Tier B" else "#EE9B00" for c in SHORTLIST]
    fig, ax = plt.subplots(figsize=(9, 3.0))
    ax.barh(names[::-1], scores[::-1], color=bar_colors[::-1], height=0.5, edgecolor="white")
    ax.set_xlim(0, 100)
    ax.axvline(70, color="#2D6A4F", lw=1.0, linestyle="--", alpha=0.6, label="Tier B (70)")
    ax.axvline(55, color="#EE9B00", lw=1.0, linestyle=":",  alpha=0.6, label="Tier C (55)")
    for i, s in enumerate(scores[::-1]):
        ax.text(s+1, i, f"{s:.0f}", va="center", ha="left", fontsize=8, fontweight="bold")
    ax.set_xlabel("Human-Judgement Score (0-100)", fontsize=8)
    ax.set_title(f"Candidate Scores - {JOB_TITLE}", fontsize=9, fontweight="bold")
    ax.legend(fontsize=7, loc="lower right")
    ax.set_facecolor("#FAFAFA"); fig.patch.set_facecolor("white")
    plt.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=150, bbox_inches="tight"); plt.close(fig)
    buf.seek(0); return buf.read()


def radar_chart():
    dims = ["Functional\nMatch","Demonstrated\nOutcomes","Environment\nFit",
            "Ownership &\nExecution","Stakeholder\nComms","Hard Skills\n/ Technical","Growth\nPotential"]
    N = len(dims)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist(); angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 5), subplot_kw=dict(polar=True))
    pal = ["#005F73","#2D6A4F","#EE9B00","#94D2BD","#E9D8A6","#CA6702"]
    for i, c in enumerate(SHORTLIST[:6]):
        vals = list(c["dims"]) + [c["dims"][0]]
        ax.plot(angles, vals, "o-", lw=1.6, color=pal[i], label=c["name"].split()[0], markersize=3)
        ax.fill(angles, vals, alpha=0.07, color=pal[i])
    ax.set_thetagrids(np.degrees(angles[:-1]), dims, fontsize=7)
    ax.set_ylim(0, 4); ax.set_yticks([1,2,3,4]); ax.set_yticklabels(["1","2","3","4"], fontsize=6)
    ax.set_title("7-Dimension Radar - Top Candidates", fontsize=9, fontweight="bold", pad=18)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=7)
    fig.patch.set_facecolor("white"); plt.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=150, bbox_inches="tight"); plt.close(fig)
    buf.seek(0); return buf.read()


def heatmap_chart():
    dim_labels = ["Func.\nMatch","Outcomes","Env.\nFit","Ownership","Comms","Hard\nSkills","Growth"]
    names = [c["name"] for c in SHORTLIST[:6]]
    data  = np.array([list(c["dims"]) for c in SHORTLIST[:6]], dtype=float)
    fig, ax = plt.subplots(figsize=(9, 3.0))
    im = ax.imshow(data, cmap="YlGn", aspect="auto", vmin=0, vmax=4)
    ax.set_xticks(range(len(dim_labels))); ax.set_xticklabels(dim_labels, fontsize=7)
    ax.set_yticks(range(len(names)));     ax.set_yticklabels(names, fontsize=7)
    for r in range(len(names)):
        for c_idx in range(len(dim_labels)):
            v = data[r, c_idx]
            ax.text(c_idx, r, f"{v:.0f}", ha="center", va="center", fontsize=8,
                    color="white" if v >= 3 else "#333333", fontweight="bold")
    plt.colorbar(im, ax=ax, shrink=0.8, label="Score (0-4)")
    ax.set_title("Dimension Heatmap - Shortlisted Candidates", fontsize=9, fontweight="bold")
    fig.patch.set_facecolor("white"); plt.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=150, bbox_inches="tight"); plt.close(fig)
    buf.seek(0); return buf.read()


def build_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=12*mm, rightMargin=12*mm,
                            topMargin=12*mm, bottomMargin=12*mm)
    story = []

    story.append(Paragraph("Taleemabad - Talent Acquisition Report", h1_s))
    story.append(Paragraph(f"{JOB_TITLE}  |  Job #{JOB_ID}  |  {date.today().strftime('%d %B %Y')}", body_s))
    story.append(Spacer(1, 4*mm))

    stat_data = [[
        Paragraph(f"<b>{TOTAL_SCREENED}</b><br/>CVs Screened", cent_s),
        Paragraph(f"<b>{len(SHORTLIST)}</b><br/>Shortlisted", cent_s),
        Paragraph(f"<b>0</b><br/>Out of Budget", cent_s),
        Paragraph(f"<b>TBD</b><br/>Budget", cent_s),
    ]]
    stat_tbl = Table(stat_data, colWidths=[60*mm]*4)
    stat_tbl.setStyle(TableStyle([
        ("BOX",(0,0),(-1,-1),0.5,C_MID),("INNERGRID",(0,0),(-1,-1),0.5,C_MID),
        ("BACKGROUND",(0,0),(-1,-1),C_LIGHT),("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),("ALIGN",(0,0),(-1,-1),"CENTER"),
    ]))
    story.append(stat_tbl); story.append(Spacer(1,5*mm))

    # Section 1: DCA
    story.append(Paragraph("1. Deep Comparative Analysis", h2_s))
    story.append(HRFlowable(width="100%", thickness=1, color=C_TEAL, spaceAfter=4))

    col_hdr = [Paragraph(t, hdr_s) for t in
               ["#","Candidate","Score","Tier","Budget","Exp. Salary","Experience",
                "Background / Current Role","Key Strength / Note","Verdict"]]
    col_w = [w*mm for w in [8,28,12,14,14,22,30,50,74,24]]

    rows = [col_hdr]
    for c in CANDIDATES:
        rows.append([
            Paragraph(str(c["rank"]), cent_s),
            Paragraph(f"<b>{c['name']}</b>", bold_s),
            Paragraph(f"<b>{c['score']:.0f}</b>", cent_s),
            Paragraph(c["tier"], cent_s),
            Paragraph(c["budget_label"], cent_s),
            Paragraph(c["salary"], cell_s),
            Paragraph(f"Total: {c['total_exp']}<br/>Relevant: {c['relevant_exp']}", cell_s),
            Paragraph(c["current_role"], cell_s),
            Paragraph(c["key_strength"], cell_s),
            Paragraph(f"<b>{c['verdict']}</b>", bold_s),
        ])

    tbl = Table(rows, colWidths=col_w, repeatRows=1)
    cmds = [
        ("BACKGROUND",(0,0),(-1,0),C_DARK),("TEXTCOLOR",(0,0),(-1,0),C_WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,0),6.5),
        ("ALIGN",(0,0),(-1,0),"CENTER"),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_WHITE,C_LIGHT]),
        ("GRID",(0,0),(-1,-1),0.3,C_MID),("VALIGN",(0,0),(-1,-1),"TOP"),
    ]
    for i, c in enumerate(CANDIDATES, 1):
        tc = TIER_COLOURS.get(c["tier"], C_DARK)
        cmds += [("TEXTCOLOR",(3,i),(3,i),tc),("FONTNAME",(3,i),(3,i),"Helvetica-Bold")]
        vc = C_GREEN if c["score"]>=70 else C_AMBER if c["score"]>=55 else C_RED
        cmds += [("TEXTCOLOR",(9,i),(9,i),vc),("FONTNAME",(9,i),(9,i),"Helvetica-Bold")]
    tbl.setStyle(TableStyle(cmds))
    story.append(tbl); story.append(PageBreak())

    # Section 2: Visual Analytics
    story.append(Paragraph("2. Visual Analytics", h2_s))
    story.append(HRFlowable(width="100%", thickness=1, color=C_TEAL, spaceAfter=4))
    chart_row = Table(
        [[RLImage(io.BytesIO(bar_chart()),   width=160*mm, height=60*mm),
          RLImage(io.BytesIO(radar_chart()), width=110*mm, height=90*mm)]],
        colWidths=[165*mm,115*mm])
    chart_row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),("ALIGN",(0,0),(-1,-1),"CENTER")]))
    story.append(chart_row); story.append(PageBreak())

    # Section 3: Heatmap
    story.append(Paragraph("3. Dimension Heatmap - Shortlisted Candidates", h2_s))
    story.append(HRFlowable(width="100%", thickness=1, color=C_TEAL, spaceAfter=4))
    story.append(RLImage(io.BytesIO(heatmap_chart()), width=170*mm, height=60*mm))
    story.append(Spacer(1,5*mm))

    dim_rows = [[Paragraph(t, hdr_s) for t in ["Dimension","Weight","What it measures"]]] + [
        [Paragraph(a,cell_s), Paragraph(b,cent_s), Paragraph(c,cell_s)] for a,b,c in [
            ("Functional Match","25%","Behavioral science + conversational UX + content writing alignment to JD"),
            ("Demonstrated Outcomes","20%","Concrete evidence: products shipped, users impacted, writing published"),
            ("Environment Fit","15%","Education/EdTech sector fit; Islamabad location; collaborative profile"),
            ("Ownership & Execution","15%","Self-directed work; drives projects end-to-end independently"),
            ("Stakeholder & Comms","10%","Translates behavioral insights into clear, engaging content"),
            ("Hard Skills / Technical","10%","AI tools (ChatGPT, Claude, etc.), UX tools (Figma), research methods"),
            ("Growth & Leadership","5%","Learning trajectory, curiosity, potential to grow the function"),
        ]
    ]
    dk_tbl = Table(dim_rows, colWidths=[55*mm,20*mm,185*mm])
    dk_tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),C_DARK),("TEXTCOLOR",(0,0),(-1,0),C_WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEFTPADDING",(0,0),(-1,-1),4),("GRID",(0,0),(-1,-1),0.3,C_MID),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_WHITE,C_LIGHT]),
    ]))
    story.append(dk_tbl); story.append(PageBreak())

    # Section 4: Why Others Didn't Make Cut
    story.append(Paragraph("4. Why Others Didn't Make the Cut", h2_s))
    story.append(HRFlowable(width="100%", thickness=1, color=C_TEAL, spaceAfter=4))
    story.append(Paragraph(
        "This is a rare hybrid role — behavioral scientist + AI practitioner + persuasive writer. "
        "The JD's five must-haves (human sciences training, qualitative research, daily AI tool fluency, "
        "strong writing, philosophical depth) form a profile that barely exists in Pakistan's current talent market. "
        "The pool of 42 was overwhelmingly UI/UX designers who did not match the core requirements.", body_s))
    story.append(Spacer(1,3*mm))

    why_rows = [[Paragraph(t, hdr_s) for t in ["Issue","Candidates affected"]]] + [
        [Paragraph(a,cell_s), Paragraph(b,cell_s)] for a,b in [
            ("UI/UX visual designers — wrong specialist profile for a human-sciences role",
             "~30 candidates (ranks 7-39)"),
            ("AI tool fluency absent — listed as skill but not evidenced in actual work",
             "~28 candidates"),
            ("No behavioral science, anthropology, psychology, or sociolinguistics background",
             "~35 candidates"),
            ("No qualitative research or ethnographic work experience",
             "~35 candidates"),
            ("No evidence of persuasive or manifesto-style writing",
             "~38 candidates"),
            ("Incomplete applications — no CV submitted","3 candidates (ranks 40-42)"),
        ]
    ]
    why_tbl = Table(why_rows, colWidths=[170*mm,90*mm])
    why_tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),C_DARK),("TEXTCOLOR",(0,0),(-1,0),C_WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),7.5),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),5),("GRID",(0,0),(-1,-1),0.3,C_MID),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_WHITE,C_LIGHT]),
    ]))
    story.append(why_tbl); story.append(Spacer(1,5*mm))
    story.append(Paragraph(
        "<b>Pool verdict:</b> Weak pool for this specialist role. 4 candidates merit interviews: "
        "Danyal Haroon (best overall JD match -- UX + AI tools + academic human-AI research, score 73), "
        "Aisha Bashir (deep Taleemabad institutional knowledge + writing + education context, score 65 -- assess AI readiness), "
        "Muhammad Taimoor (Conversational UX Designer profile -- MSc Human-Centered Systems, explicitly lists Conversational UX and Prompt-Based UX, score 62), and "
        "Muhammad Ammar Khan (AI Interaction Designer profile -- behavior-driven design, human-AI relationships, daily AI tools, score 55 -- fresh grad, limited experience). "
        "If none convert, re-post with clearer signals -- 'behavioral scientist,' "
        "'AI behavior designer,' or 'human-AI researcher' in the title will attract a more relevant pool "
        "than 'Conversational UX Designer,' which pulls visual designers.", body_s))
    story.append(Spacer(1,5*mm))

    # Section 5: Next Steps
    story.append(Paragraph("5. Recommended Next Steps", h2_s))
    story.append(HRFlowable(width="100%", thickness=1, color=C_TEAL, spaceAfter=4))
    for step in [
        "1. Interview Danyal Haroon (rank 1) — take-home task: ask him to write a 1-page 'soul note' "
           "defining how Rumi should respond to a teacher who says 'I feel like giving up.' "
           "Evaluate: depth of behavioral thinking, writing quality, ethical nuance.",
        "2. Interview Aisha Bashir (rank 2) — assess AI tool readiness and research thinking. "
           "Her Taleemabad context and writing are assets; confirm she can operate with AI tools and "
           "take an independent analytical position.",
        "3. Interview Muhammad Taimoor (rank 3) — confirm that Conversational UX and HCI skills go "
           "beyond skill-section listings into actual practice. Ask for examples of conversation design "
           "work and assess behavioral thinking depth.",
        "4. Interview Muhammad Ammar Khan (rank 4) — fresh grad but genuine AI fluency and behavioral "
           "design intent. Use the same take-home task to assess writing quality and depth of thinking "
           "on human-AI relationships.",
        "5. Set the salary budget before extending any offer — budget is currently TBD.",
        "6. If none convert, re-post with 'AI Behavior Designer' or 'Human-AI Researcher' "
           "in the title. Explicitly name behavioral science, anthropology, or psychology in requirements "
           "to stop attracting visual UI/UX designers.",
    ]:
        story.append(Paragraph(step, body_s)); story.append(Spacer(1,2*mm))

    story.append(Spacer(1,6*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_MID))
    story.append(Spacer(1,2*mm))
    story.append(Paragraph("Coco — Taleemabad Talent Acquisition Agent  |  Confidential", foot_s))

    doc.build(story)
    buf.seek(0); return buf.read()


def send_email(pdf_bytes):
    msg = MIMEMultipart()
    msg["Subject"] = f"Screening Report- {JOB_TITLE}"
    msg["From"]    = SENDER
    msg["To"]      = RECIPIENT

    today_str = date.today().strftime("%d %B %Y")
    html_body = f"""
<html><body style="font-family:Arial,sans-serif;font-size:14px;color:#1A1A2E;max-width:620px;margin:0 auto;">
  <p>Hi Ayesha,</p>
  <p>Please find attached the screening report for the <b>{JOB_TITLE}</b> position (Job #{JOB_ID}).</p>
  <table cellpadding="0" cellspacing="0" width="100%" style="margin:20px 0;">
    <tr>
      <td align="center" width="33%" style="background:#005F73;color:#ffffff;padding:16px 10px;border-radius:6px 0 0 6px;">
        <div style="font-size:22px;font-weight:bold;">{TOTAL_SCREENED}</div>
        <div style="font-size:12px;margin-top:4px;">CVs Screened</div>
      </td>
      <td align="center" width="33%" style="background:#2D6A4F;color:#ffffff;padding:16px 10px;">
        <div style="font-size:22px;font-weight:bold;">{len(SHORTLIST)}</div>
        <div style="font-size:12px;margin-top:4px;">Shortlisted</div>
      </td>
      <td align="center" width="33%" style="background:#6C757D;color:#ffffff;padding:16px 10px;border-radius:0 6px 6px 0;">
        <div style="font-size:22px;font-weight:bold;">TBD</div>
        <div style="font-size:12px;margin-top:4px;">Budget</div>
      </td>
    </tr>
  </table>
  <p>See the attached PDF for the full analysis -- Deep Comparative Analysis, visual charts, heatmap, and recommended next steps.</p>
  <p><b>Quick summary:</b> Pool of 42 was overwhelmingly visual UI/UX designers who did not match the JD's core requirements
  (behavioral science, qualitative research, AI tool fluency, persuasive writing). 4 candidates merit interviews:
  <b>Danyal Haroon</b> (strongest JD match -- UX + daily AI tools + human-AI research, score 73),
  <b>Aisha Bashir</b> (deep Taleemabad educational content background + strong writer, score 65 -- assess AI readiness),
  <b>Muhammad Taimoor</b> (Conversational UX Designer -- MSc Human-Centered Systems, explicitly lists Conversational UX and Prompt-Based UX, score 62), and
  <b>Muhammad Ammar Khan</b> (AI Interaction Designer -- behavior-driven design, human-AI relationships, daily AI tools, score 55 -- fresh grad).
  If none convert, recommend re-posting with a clearer title targeting behavioral scientists and AI practitioners.</p>
  <p style="margin-top:24px;">Best regards,<br/><b>Coco — Taleemabad Talent Acquisition Agent</b></p>
  <hr style="border:none;border-top:1px solid #e0e0e0;margin-top:24px;"/>
  <p style="font-size:11px;color:#888888;">Coco — Taleemabad Talent Acquisition Agent | Confidential | {today_str}</p>
</body></html>
"""
    msg.attach(MIMEText(html_body, "html"))
    fname = f"Screening_Report_Job{JOB_ID}_{JOB_TITLE.replace(' ','_').replace('/','_')}.pdf"
    part = MIMEBase("application", "octet-stream")
    part.set_payload(pdf_bytes)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{fname}"')
    msg.attach(part)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(SENDER, PASSWORD)
        s.sendmail(SENDER, [RECIPIENT], msg.as_string())
    print(f"Email sent to {RECIPIENT}")


if __name__ == "__main__":
    print("Building PDF...")
    pdf = build_pdf()
    os.makedirs("output", exist_ok=True)
    out = f"output/Screening_Report_Job{JOB_ID}.pdf"
    with open(out, "wb") as f: f.write(pdf)
    print(f"PDF saved: {out} ({len(pdf)//1024} KB)")
    print("Sending email...")
    send_email(pdf)
    print("Done.")
