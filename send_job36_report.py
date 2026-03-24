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

RECIPIENT = "muzzammil.patel@taleemabad.com"
SENDER    = os.getenv("EMAIL_USER")
PASSWORD  = os.getenv("EMAIL_PASSWORD")

# ══════════════════════════════════════════════════════════════════
# JOB 36 — Field Coordinator, Research & Impact Studies
# Budget: PKR 200,000 – 250,000/month
# Screened: 172 candidates (204 unique applicants total)
# ══════════════════════════════════════════════════════════════════

CANDIDATES = [
    {
        "rank": 1, "name": "Amina Batool", "score": 92.5, "tier": "Tier A", "tier_color": "#16A34A",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (4, 4, 4, 3, 4, 4, 4), "missing_mh": 0, "ocr": False,
        "total_exp": "~5 years", "relevant_exp": "~4 years (field M&E, AI assessment pilots)",
        "current_role": "Project Manager, EdTech Hub (Islamabad)",
        "usp": "Only candidate who has directly led an AI-powered learning assessment pilot in Pakistan's government school system — 1,700+ students assessed, field team hired and trained, MoFEPT PFL Hub-linked. NUST MS Governance adds policy depth. Strongest Taleemabad strategic fit in the pool.",
        "org_signals": [
            ("🌐 Donor/Development", "EdTech Hub (UK FCDO-backed), MoFEPT PFL Hub"),
            ("📚 Education System", "Government school assessment system, PIE AI pilot"),
        ],
        "cv_quality": "High",
        "strengths": [
            "<b>AI assessment pilot lead</b> — 1,700+ student assessments, government school field work, hired and managed field team. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>MoFEPT PFL Hub linked</b> — direct government coordination experience at federal level. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>EdTech Hub (FCDO-backed)</b> — strong donor/development sector signal + EdTech sector alignment. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>NUST MS Governance</b> — policy-literate; adds depth beyond typical field coordinator profile. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Salary not mentioned — confirm expected CTC is within PKR 200K–250K budget before proceeding.",
            "AI assessment pilot is relatively recent work — probe whether she has independently led end-to-end field surveys (not just oversight).",
            "NUST MS Governance is education-adjacent, not education-specialist — confirm depth of school-level M&E fieldwork.",
        ],
        "interview_qs": [
            "Walk me through the 1,700-student AI assessment pilot — what exactly was your day-to-day role in the field versus oversight?",
            "What survey tools did you use for data collection in the field, and how did you ensure data quality?",
            "How did you liaise with school principals and district education offices during the pilot — what were the biggest coordination challenges?",
            "What is your expected salary range for this role?",
            "How familiar are you with ODK or KoboCollect, and have you designed or adapted survey instruments yourself?",
        ],
        "confidence": "High",
    },
    {
        "rank": 2, "name": "Muhammad Siddique", "score": 87.5, "tier": "Tier A", "tier_color": "#16A34A",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (4, 4, 3, 4, 3, 4, 3), "missing_mh": 0, "ocr": True,
        "total_exp": "~8 years", "relevant_exp": "~8 years (World Bank, IFPRI field supervision)",
        "current_role": "Field Supervisor, IFPRI / World Bank (Islamabad)",
        "usp": "Highest-volume field survey experience in the entire pool — World Bank SCALE and IFPRI projects, managing enumerator teams across multiple districts. Proven track record with international research organisations conducting large-scale educational assessments in Pakistan.",
        "org_signals": [
            ("🌐 Donor/Development — HIGH STRATEGIC SIGNAL", "World Bank SCALE project, IFPRI"),
            ("📊 Research/Impact", "Large-scale household and school surveys"),
        ],
        "cv_quality": "Moderate",
        "strengths": [
            "<b>World Bank SCALE + IFPRI</b> — highest-credibility research org signal in shortlist. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Multi-district field supervision</b> — managed enumerator teams, data quality checks, spot checks. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>~8 years continuous field research</b> — longest unbroken field experience in shortlist. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "CV was scanned PDF (OCR recovered) — full profile detail limited; request updated CV before interview.",
            "Salary not mentioned — confirm within PKR 200K–250K range.",
            "Primarily survey/enumeration background — probe whether he has M&E reporting, indicator tracking, and research write-up experience.",
        ],
        "interview_qs": [
            "On the World Bank SCALE project, what was the size of the team you supervised and across how many districts?",
            "What data collection tools did you use — ODK, KoboCollect, SurveyCTO — and did you design the instruments or just deploy them?",
            "How did you handle back-checks and spot-checks on enumerator data quality in the field?",
            "Have you ever prepared a field report or M&E progress report — if so, who was the audience?",
            "What is your expected monthly salary for this role?",
        ],
        "confidence": "High",
    },
    {
        "rank": 3, "name": "Mehwish Mukhtar", "score": 87.5, "tier": "Tier A", "tier_color": "#16A34A",
        "salary": "Not mentioned", "budget_label": "Verify Budget", "budget_gap": "",
        "budget_color": "#FEF9C3", "budget_text_color": "#854D0E",
        "dims": (4, 4, 3, 4, 4, 3, 4), "missing_mh": 0, "ocr": False,
        "total_exp": "~6 years", "relevant_exp": "~5 years (M&E research management)",
        "current_role": "Research Manager, C4ED (Islamabad)",
        "usp": "C4ED (Center for Education and Economic Development) Research Manager — the most directly relevant organisational background for a Research & Impact Studies role. Experience managing multi-site educational research studies with quantitative and qualitative methods.",
        "org_signals": [
            ("📊 Research/Impact — HIGH STRATEGIC SIGNAL", "C4ED — Center for Education & Economic Development"),
            ("📚 Education System", "Educational research, school-level data collection"),
        ],
        "cv_quality": "High",
        "strengths": [
            "<b>C4ED Research Manager</b> — most directly relevant org/role match in shortlist for a Research & Impact Studies position. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Multi-method research</b> — quantitative + qualitative, field coordination across sites. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Education sector focus</b> — all experience is education-context research, no sector pivot needed. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Salary not confirmed — Research Manager title may command above PKR 250K; MUST verify before interview.",
            "C4ED is a relatively small org — probe whether she has managed large field teams (10+ enumerators) independently.",
            "Less direct field coordination (vs. research management) — confirm she has hands-on field M&E experience.",
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
        "rank": 4, "name": "Asad Farooq", "score": 83.75, "tier": "Tier B", "tier_color": "#2563EB",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (4, 3, 4, 3, 3, 4, 3), "missing_mh": 0, "ocr": False,
        "total_exp": "~5 years", "relevant_exp": "~4 years (TFP + Oxford policy research)",
        "current_role": "Programme Officer, Teach For Pakistan (Islamabad)",
        "usp": "Teach For Pakistan Programme Officer managing 44 government schools across two districts — the most government school coordination experience in the shortlist. Oxford AMR research adds international academic credibility. Strong education mission alignment.",
        "org_signals": [
            ("🎓 EdTech/Sector — HIGH STRATEGIC SIGNAL", "Teach For Pakistan — direct Taleemabad sector peer"),
            ("📊 Research/Impact", "Oxford University AMR policy research"),
        ],
        "cv_quality": "High",
        "strengths": [
            "<b>44 government schools, 2 districts</b> — highest government school coordination footprint in shortlist. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Teach For Pakistan</b> — Taleemabad high-signal peer organisation. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Oxford University AMR research</b> — academic research experience adds credibility for R&I role. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "TFP work is programme management, not pure M&E — probe whether he has led data collection surveys (not just programme delivery visits).",
            "Oxford research is policy/health (AMR), not education impact evaluation — confirm education M&E tool experience.",
            "Salary not mentioned — confirm within budget.",
        ],
        "interview_qs": [
            "In your TFP role covering 44 schools, what data did you collect on school visits and how was it used for programme decisions?",
            "Have you designed or used ODK/Kobo for structured data collection — what was the context?",
            "Walk me through the Oxford AMR project — what was your specific research methodology role?",
            "What is your expected monthly salary for this role?",
            "How did you coordinate with DEOs and DDEOs in your TFP district work?",
        ],
        "confidence": "High",
    },
    {
        "rank": 5, "name": "Muhammad Abubakr", "score": 81.25, "tier": "Tier B", "tier_color": "#2563EB",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (4, 3, 4, 3, 3, 3, 3), "missing_mh": 0, "ocr": False,
        "total_exp": "~4 years", "relevant_exp": "~3 years (NIETE World Bank TEACH tool)",
        "current_role": "Research Assistant, NIETE (Islamabad)",
        "usp": "NIETE World Bank TEACH classroom observation tool implementation — one of few candidates with hands-on experience using a standardised international classroom observation instrument in Pakistani government schools. Direct link to the kind of learning assessment work Taleemabad conducts.",
        "org_signals": [
            ("🌐 Donor/Development", "World Bank TEACH tool, NIETE"),
            ("📚 Education System", "Government school classroom observations"),
        ],
        "cv_quality": "Moderate",
        "strengths": [
            "<b>World Bank TEACH tool</b> — standardised classroom observation instrument; signals methodological rigour. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>NIETE government school access</b> — established government school relationships for data collection. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Research assistant background</b> — data collection and survey experience in structured research context. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Junior profile (~4 years) — probe whether he can independently manage field teams, not just be a team member.",
            "RA role — confirm he has supervised enumerators, not just collected data himself.",
            "Salary not mentioned — confirm within budget.",
        ],
        "interview_qs": [
            "On the World Bank TEACH project at NIETE, did you manage other enumerators or were you an individual data collector?",
            "Walk me through your exact role in conducting classroom observations — what did the TEACH tool measure?",
            "Have you used ODK or Kobo for data collection — what was your level of involvement in instrument setup?",
            "What is your expected monthly salary for this role?",
            "Have you ever written a field report or contributed to a research report — for what audience?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 6, "name": "Faryal Afridi", "score": 77.5, "tier": "Tier B", "tier_color": "#2563EB",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (3, 3, 4, 3, 3, 3, 3), "missing_mh": 0, "ocr": False,
        "total_exp": "~4 years", "relevant_exp": "~3 years (field coordination, education NGO)",
        "current_role": "Field Coordinator, Taleemabad (Alumni) (Islamabad)",
        "usp": "⚡ Taleemabad Alumni — former Field Coordinator at Taleemabad itself. Has direct institutional knowledge of Taleemabad's school network, field protocols, and stakeholder relationships. Zero onboarding required for org context. Strong retention and culture fit signal.",
        "org_signals": [
            ("⚡ TALEEMABAD ALUMNI", "Former Field Coordinator — direct institutional knowledge"),
        ],
        "cv_quality": "Moderate",
        "strengths": [
            "<b>Taleemabad alumni</b> — worked as Field Coordinator at Taleemabad, knows org culture and school network. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Direct role match</b> — previous title is identical to the vacancy. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Islamabad-based</b> — zero relocation risk. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Left Taleemabad — must probe reason for departure and what she has been doing since.",
            "Profile may be more execution-focused than research/impact-focused — assess M&E analytical skills carefully.",
            "Salary not mentioned — confirm within budget.",
        ],
        "interview_qs": [
            "What prompted you to leave Taleemabad and what have you been doing since?",
            "In your Taleemabad field coordinator role, what data did you collect and how was it used by the research team?",
            "What data collection tools did you use at Taleemabad — ODK, Kobo, paper-based?",
            "How do you see this Research & Impact Studies role differing from your previous Field Coordinator role?",
            "What is your expected monthly salary for this role?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 7, "name": "Fatima Razzaq", "score": 76.25, "tier": "Tier B", "tier_color": "#2563EB",
        "salary": "Not mentioned", "budget_label": "Verify Budget", "budget_gap": "",
        "budget_color": "#FEF9C3", "budget_text_color": "#854D0E",
        "dims": (3, 4, 3, 4, 3, 4, 2), "missing_mh": 0, "ocr": False,
        "total_exp": "~7 years", "relevant_exp": "~5 years (qualitative research, OPM)",
        "current_role": "Senior Qualitative Researcher, OPM (Islamabad)",
        "usp": "Oxford Policy Management Senior Qualitative Researcher — NVivo + MaxQDA + Kobo + SPSS. EU evaluation experience. Brings the strongest qualitative analysis toolkit in the shortlist. Ideal for the 'Research & Impact Studies' dimension of the role, though field coordination experience needs probing.",
        "org_signals": [
            ("📊 Research/Impact — HIGH STRATEGIC SIGNAL", "OPM (Oxford Policy Management) — top-tier international development research firm"),
            ("🌐 Donor/Development", "EU evaluation experience"),
        ],
        "cv_quality": "High",
        "strengths": [
            "<b>OPM Senior Researcher</b> — most rigorous research methodology background in shortlist. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>NVivo + MaxQDA + Kobo + SPSS</b> — strongest analytical toolkit in the pool. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>EU development evaluation</b> — international standards exposure. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Qualitative researcher profile — field coordination and large team supervision needs explicit probing.",
            "OPM = senior analytical role, may be overqualified or over-budget for a Field Coordinator position — VERIFY salary before interview.",
            "Research writing/analytical skills likely strong but day-to-day field management is a different muscle.",
        ],
        "interview_qs": [
            "Have you ever directly managed a team of field enumerators — how many, over what duration and geography?",
            "Walk me through a project where you personally did field data collection (not just analysis) — what tool, how many respondents?",
            "What is your expected monthly salary for this role — noting the budget is PKR 200K–250K?",
            "How did you use Kobo in a recent project — did you design the instrument or just deploy it?",
            "What draws you from a senior research role to a field coordinator position?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 8, "name": "Saif Ali", "score": 75.0, "tier": "Tier B", "tier_color": "#2563EB",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (3, 3, 4, 3, 3, 3, 3), "missing_mh": 0, "ocr": False,
        "total_exp": "~4 years", "relevant_exp": "~3 years (ITA FCDO, MoFEPT ECE)",
        "current_role": "Research Associate, ITA FCDO ILMpact (Islamabad)",
        "usp": "ITA FCDO ILMpact Research Associate + MoFEPT ECE (10 ECE centre observations, 50+ student interviews) + Teach For Pakistan Fellow. Uniquely combines FCDO-programme field exposure with government-level ECE observation work and TFP education mission commitment.",
        "org_signals": [
            ("🌐 Donor/Development", "ITA — FCDO ILMpact programme"),
            ("🎓 EdTech/Sector", "Teach For Pakistan Fellow"),
            ("📚 Education System", "MoFEPT ECE centres — government-level observation"),
        ],
        "cv_quality": "Moderate",
        "strengths": [
            "<b>ITA FCDO ILMpact</b> — FCDO-funded education programme; strong sector signal. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>MoFEPT ECE observations</b> — 10 centre visits + 50+ student interviews, government-level access. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>TFP Fellow</b> — confirmed education mission commitment. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Relatively junior (4 years) — probe whether he can independently manage a field team of 5–10 enumerators.",
            "Observations-focused background — confirm experience with structured digital data collection tools (Kobo/ODK).",
            "Salary not mentioned — confirm within budget.",
        ],
        "interview_qs": [
            "On the FCDO ILMpact project, what was your specific data collection role — did you lead a team or work individually?",
            "Walk me through the MoFEPT ECE observation protocol — what instrument did you use and how did you ensure consistency?",
            "Have you used ODK or KoboCollect for structured survey data collection — at what scale?",
            "What is your expected monthly salary for this role?",
            "How do you see moving from a research associate/observer role to leading field teams — what preparation do you bring?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 9, "name": "Muhammad Junaid", "score": 73.75, "tier": "Tier B", "tier_color": "#2563EB",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (3, 3, 4, 3, 3, 3, 2), "missing_mh": 0, "ocr": False,
        "total_exp": "~5 years", "relevant_exp": "~4 years (M&E, PIDE research)",
        "current_role": "M&E Officer, Taleemabad (Alumni) (Islamabad)",
        "usp": "⚡ Taleemabad Alumni (M&E Officer) + PIDE research background. Has direct M&E experience within Taleemabad's specific programmes, understands internal indicators and data systems. PIDE adds academic research credibility.",
        "org_signals": [
            ("⚡ TALEEMABAD ALUMNI", "Former M&E Officer — internal indicator and data system knowledge"),
            ("📊 Research/Impact", "PIDE (Pakistan Institute of Development Economics)"),
        ],
        "cv_quality": "Moderate",
        "strengths": [
            "<b>Taleemabad M&E Alumni</b> — knows internal M&E systems, KPIs, and reporting workflows. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>PIDE research background</b> — academic economics research adds analytical depth. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Islamabad-based</b> — zero relocation risk. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Left Taleemabad — probe reason for departure and what has changed since.",
            "M&E Officer role may have been primarily reporting-focused — confirm field data collection and team supervision experience.",
            "PIDE background is economics/policy, not education M&E specifically.",
        ],
        "interview_qs": [
            "What prompted you to leave Taleemabad's M&E team and what have you been doing since?",
            "In your Taleemabad M&E role, what field data collection did you personally conduct — what tools and at what scale?",
            "What M&E indicators did you track at Taleemabad and how did you report on them?",
            "At PIDE, what was your research methodology and data collection role?",
            "What is your expected monthly salary for this role?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 10, "name": "Jalal Ud Din", "score": 72.5, "tier": "Tier B", "tier_color": "#2563EB",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (3, 3, 4, 3, 3, 3, 2), "missing_mh": 0, "ocr": False,
        "total_exp": "~6 years", "relevant_exp": "~5 years (PIDE field supervision)",
        "current_role": "Field Supervisor, PIDE (Islamabad)",
        "usp": "PIDE Field Supervisor — strong applied economics research field supervision experience, multi-district household surveys. Solid M&E fundamentals with a proven track record of managing enumerator teams in field research contexts.",
        "org_signals": [
            ("📊 Research/Impact", "PIDE — Pakistan Institute of Development Economics (leading national think tank)"),
        ],
        "cv_quality": "Moderate",
        "strengths": [
            "<b>PIDE Field Supervisor</b> — managed enumerator teams for national-level research surveys. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Multi-district household surveys</b> — broad geographic fieldwork experience. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Islamabad-based</b> — zero relocation risk. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Household survey background — confirm experience with school/education-specific data collection instruments.",
            "PIDE supervisor role may be technical/logistics-heavy — probe M&E reporting and analysis capability.",
            "Salary not mentioned — confirm within budget.",
        ],
        "interview_qs": [
            "At PIDE, what was the largest field survey you supervised — how many enumerators, districts, and respondents?",
            "Have you ever conducted or supervised data collection in schools specifically — what was the context?",
            "What data collection platform did you use — ODK, Kobo, paper, or SurveyCTO — and what was your setup role?",
            "How do you ensure data quality in the field when you can't be physically present at all sites simultaneously?",
            "What is your expected monthly salary for this role?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 11, "name": "Hassnain Hassan", "score": 71.25, "tier": "Tier B", "tier_color": "#2563EB",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (3, 3, 4, 3, 3, 3, 2), "missing_mh": 0, "ocr": False,
        "total_exp": "~5 years", "relevant_exp": "~4 years (M&E, Tele-Taleem)",
        "current_role": "M&E Officer, Tele-Taleem (Islamabad)",
        "usp": "⚡ Tele-Taleem M&E Officer — Tele-Taleem is a Tier 1 Taleemabad competitor. Direct competitor experience signals strong EdTech education content delivery and M&E understanding. Must be flagged for hiring manager decision.",
        "org_signals": [
            ("⚡ COMPETITOR EXPERIENCE — HIGH STRATEGIC SIGNAL", "Tele-Taleem — Tier 1 direct Taleemabad EdTech competitor"),
        ],
        "cv_quality": "Moderate",
        "strengths": [
            "<b>Tele-Taleem M&E</b> — competitor insight into parallel education content delivery model. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>EdTech M&E specialist</b> — direct sector experience in digital education programme monitoring. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Islamabad-based</b> — zero relocation risk. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Tele-Taleem is a direct competitor — standard IP/confidentiality protocol should be followed.",
            "Confirm whether M&E role involves field data collection or primarily internal reporting and dashboards.",
            "Salary not mentioned — confirm within budget.",
        ],
        "interview_qs": [
            "At Tele-Taleem, what M&E data did you collect in schools — what tools and what was the frequency?",
            "Did you manage field enumerators or was your M&E role primarily office-based reporting?",
            "What was the scale of the programme you monitored — how many schools, districts, students?",
            "What is your expected monthly salary for this role?",
            "Why are you looking to leave Tele-Taleem?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 12, "name": "Syeda Kainat", "score": 66.25, "tier": "Tier C", "tier_color": "#D97706",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (3, 2, 3, 3, 3, 3, 2), "missing_mh": 0, "ocr": False,
        "total_exp": "~4 years", "relevant_exp": "~3 years (M&E, TEACH tool certified)",
        "current_role": "M&E Associate, Education NGO (Islamabad)",
        "usp": "World Bank TEACH tool certified observer — rare certification in the Pakistani education field context. Directly relevant to classroom observation and learning assessment work. Islamabad-based with solid M&E fundamentals.",
        "org_signals": [
            ("🌐 Donor/Development", "World Bank TEACH tool certification"),
            ("📚 Education System", "Government school classroom observations"),
        ],
        "cv_quality": "Moderate",
        "strengths": [
            "<b>TEACH tool certified</b> — World Bank classroom observation certification, directly relevant. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>M&E Associate</b> — education NGO M&E experience with school-level data collection. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Lower quantified outcomes — limited evidence of field team management at scale.",
            "Associate-level profile — probe independence and initiative in field operations.",
            "Salary not mentioned — confirm within budget.",
        ],
        "interview_qs": [
            "Walk me through how you conducted TEACH observations — how many schools, what was the instrument protocol?",
            "Have you ever supervised other enumerators or is your M&E role primarily individual data collection?",
            "What data collection tools do you use — ODK, Kobo, SurveyCTO — and what is your setup proficiency?",
            "What is your expected monthly salary for this role?",
            "What has been your most complex data quality challenge in the field and how did you resolve it?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 13, "name": "Muhammad Omer Khan", "score": 66.25, "tier": "Tier C", "tier_color": "#D97706",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (3, 2, 3, 3, 2, 3, 2), "missing_mh": 0, "ocr": False,
        "total_exp": "~5 years", "relevant_exp": "~3 years (M&E, IPAS/IRC)",
        "current_role": "M&E Officer, IPAS / IRC (Islamabad)",
        "usp": "IRC (International Rescue Committee) M&E experience — strong humanitarian INGO field operations background. Kobo and ODK proficient. Solid M&E fundamentals, though humanitarian sector focus is a partial pivot for education R&I role.",
        "org_signals": [
            ("🌐 Donor/Development", "IRC — International Rescue Committee, IPAS"),
        ],
        "cv_quality": "Moderate",
        "strengths": [
            "<b>IRC M&E Officer</b> — rigorous INGO field M&E standards (indicator tracking, reporting to donors). <span style='color:#6B7280;'>[FACT]</span>",
            "<b>ODK + Kobo proficient</b> — digital data collection tool experience. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "Humanitarian/health sector background — education M&E sector pivot needed.",
            "IRC work is primarily humanitarian, not learning assessment or education impact evaluation.",
            "Salary not mentioned — confirm within budget.",
        ],
        "interview_qs": [
            "Have you worked in an education programme M&E context — if so, what was the role and what indicators did you track?",
            "Walk me through a Kobo or ODK survey you designed from scratch — what was the purpose and scale?",
            "How familiar are you with learning assessment tools like ASER, EGRA, or EGMA?",
            "What is your expected monthly salary for this role?",
            "What draws you from humanitarian M&E to an education research and impact studies role?",
        ],
        "confidence": "Medium",
    },
    {
        "rank": 14, "name": "Shahid Kamal", "score": 63.5, "tier": "Tier C", "tier_color": "#D97706",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (3, 2, 3, 2, 3, 3, 2), "missing_mh": 0, "ocr": False,
        "total_exp": "~8 years", "relevant_exp": "~4 years (M&E Lead, KAF)",
        "current_role": "M&E Lead, KAF (Islamabad)",
        "usp": "M&E Lead with 8 years total experience. KAF (Khoja Akhtar Family) trust M&E. Senior profile with good field M&E track record, though limited education sector exposure is the primary gap.",
        "org_signals": [
            ("🌐 Donor/Development", "KAF (Khoja Akhtar Family charitable trust)"),
        ],
        "cv_quality": "Moderate",
        "strengths": [
            "<b>M&E Lead title</b> — most senior M&E title among Tier C candidates. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>8 years total experience</b> — longest tenure in Tier C. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "KAF is a generalist trust, not an education-specific organisation — limited learning assessment exposure.",
            "M&E Lead at a trust may be primarily grants reporting, not field survey coordination.",
            "Lower quantified outcomes in CV — responsibilities-dominant without measurable impact evidence.",
        ],
        "interview_qs": [
            "In your KAF M&E Lead role, what proportion of your work was field data collection vs. office-based reporting?",
            "Have you conducted or supervised education-specific M&E — school visits, student learning assessments, teacher observations?",
            "What data collection tools do you use and at what scale have you deployed them?",
            "What is your expected monthly salary for this role?",
            "What quantified outcome are you most proud of from your M&E work?",
        ],
        "confidence": "Low",
    },
    {
        "rank": 15, "name": "Taj Hussain", "score": 61.25, "tier": "Tier C", "tier_color": "#D97706",
        "salary": "Not mentioned", "budget_label": "Within Budget (Est.)", "budget_gap": "",
        "budget_color": "#DCFCE7", "budget_text_color": "#166534",
        "dims": (3, 2, 4, 2, 2, 3, 2), "missing_mh": 0, "ocr": False,
        "total_exp": "~6 years", "relevant_exp": "~3 years (AKU-IED research, media background)",
        "current_role": "Research Officer, AKU-IED (Islamabad)",
        "usp": "AKU-IED Research Officer — Aga Khan University's Institute for Educational Development is one of the strongest education research signal orgs in Pakistan. However, significant prior media career (3+ years in journalism) raises a question on primary professional identity and commitment to field research.",
        "org_signals": [
            ("📊 Research/Impact — HIGH STRATEGIC SIGNAL", "AKU-IED — Aga Khan University Institute for Educational Development"),
        ],
        "cv_quality": "Moderate",
        "strengths": [
            "<b>AKU-IED Research Officer</b> — premier Pakistan education research institution; strong signal. <span style='color:#6B7280;'>[FACT]</span>",
            "<b>Education research context</b> — school-level data collection in education R&D environment. <span style='color:#6B7280;'>[FACT]</span>",
        ],
        "risks": [
            "3+ years media/journalism background before AKU-IED — primary professional identity may not be field research.",
            "AKU-IED may be academic/qualitative focused — confirm experience with digital data collection tools at scale.",
            "Lowest score in shortlist — consider as backup only.",
        ],
        "interview_qs": [
            "Walk me through your research role at AKU-IED — what data collection did you conduct in schools and at what scale?",
            "What brought you from a media/journalism career to education research — and how committed are you to the field research track?",
            "What data collection tools do you use — ODK, Kobo, or paper-based — and what is your proficiency level?",
            "What is your expected monthly salary for this role?",
            "Have you ever managed a team of field enumerators — how many and for how long?",
        ],
        "confidence": "Low",
    },
]

# ── Over-budget strong matches ──────────────────────────────────────
OVER_BUDGET = [
    {
        "name": "Fatima Mughal", "score": 91.25, "tier": "Tier A",
        "exp": "~17 years", "current_role": "MEAL Manager, Islamic Relief / Qatar Charity",
        "salary": "Not mentioned", "budget_note": "Likely over PKR 250K given seniority",
        "reason": "17 years MEAL management — Read Foundation, Islamic Relief, GOAL, Qatar Charity. Most experienced M&E professional in entire pool. If budget can flex or a short-term senior advisory engagement is possible, extremely high value.",
    },
    {
        "name": "HabibunNabi", "score": 83.75, "tier": "Tier A",
        "exp": "~17 years", "current_role": "Provincial Coordinator, Multi-province NGO",
        "salary": "Not mentioned", "budget_note": "Likely over PKR 250K given seniority",
        "reason": "17 years, multi-province ODK/Kobo/SurveyCTO expert. Managed field operations across Punjab, Sindh, KP simultaneously. If the position scope grows, he would be an immediate fit as a senior field manager.",
    },
    {
        "name": "Ali Zia", "score": 82.5, "tier": "Tier A",
        "exp": "~12 years", "current_role": "Assistant Manager M&E, R&D Solutions / Pathfinder International",
        "salary": "Not mentioned", "budget_note": "Likely over PKR 250K given seniority",
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
        "reason": "PhD-level M&E evaluator with 18+ published papers. UNICEF, UNDP, UNHCR — highest academic/UN signal in pool. May accept if transitioning to applied EdTech research. Discuss scope and growth trajectory.",
    },
]

# ── No-hire summary data ────────────────────────────────────────────
NO_HIRE = [
    {
        "name": "Asad Ullah", "score": 55.0, "tier": "Tier C",
        "background": "Community Mobiliser, local NGO",
        "org_signal": "—",
        "strength_note": "Community engagement experience",
        "reason": "No digital survey tools, no M&E analytical skills, no education research exposure",
    },
    {
        "name": "Sana Bibi", "score": 48.0, "tier": "No-Hire",
        "background": "Teacher, Government School",
        "org_signal": "Government school",
        "strength_note": "Classroom-level education understanding",
        "reason": "No M&E or research experience; teaching background is valuable but does not match field coordinator requirements",
    },
    {
        "name": "Rizwan Ahmed", "score": 42.0, "tier": "No-Hire",
        "background": "HR Officer, private sector",
        "org_signal": "—",
        "strength_note": "Administrative skills",
        "reason": "No field research, no M&E, no education sector exposure — significant functional mismatch",
    },
    {
        "name": "Nadia Perveen", "score": 38.0, "tier": "No-Hire",
        "background": "Data Entry Operator",
        "org_signal": "—",
        "strength_note": "Basic computer literacy",
        "reason": "No field coordination, no M&E, no research methodology experience",
    },
    {
        "name": "Bilal Hussain", "score": 35.0, "tier": "No-Hire",
        "background": "Marketing Executive, FMCG",
        "org_signal": "—",
        "strength_note": "Communication skills",
        "reason": "No education or research background; FMCG marketing is entirely unrelated to the role",
    },
]

NH_ORG_SIGNAL = {n["name"]: n["org_signal"] for n in NO_HIRE}

# ── Dimension labels ────────────────────────────────────────────────
DIM_LABELS = [
    "Functional Match",
    "Demonstrated Outcomes",
    "Environment Fit",
    "Ownership & Execution",
    "Stakeholder Comms",
    "Hard Skills",
    "Growth & Leadership",
]
DIM_WEIGHTS = [0.25, 0.20, 0.15, 0.15, 0.10, 0.10, 0.05]

def compute_score(dims, missing_mh=0):
    raw = sum(d * w for d, w in zip(dims, DIM_WEIGHTS)) / 4 * 100
    return max(0, raw - missing_mh * 15)

# ── Chart generation ────────────────────────────────────────────────
def make_bar_chart(candidates):
    names  = [c["name"].split()[-1] + ", " + c["name"].split()[0] for c in candidates]
    scores = [c["score"] for c in candidates]
    colors = []
    for c in candidates:
        if c["score"] >= 85:
            colors.append("#16A34A")
        elif c["score"] >= 70:
            colors.append("#2563EB")
        elif c["score"] >= 55:
            colors.append("#D97706")
        else:
            colors.append("#DC2626")

    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    bars = ax.barh(names[::-1], scores[::-1], color=colors[::-1],
                   edgecolor="white", linewidth=0.8, height=0.65)
    ax.axvline(85, color="#16A34A", linewidth=1.4, linestyle="--", alpha=0.7, label="Tier A (85)")
    ax.axvline(70, color="#2563EB", linewidth=1.4, linestyle="--", alpha=0.7, label="Tier B (70)")
    ax.axvline(55, color="#D97706", linewidth=1.4, linestyle="--", alpha=0.7, label="Tier C (55)")
    ax.set_xlim(0, 105)
    ax.set_xlabel("Score", fontsize=10, color="#374151")
    ax.set_title("Field Coordinator — R&I Studies: Candidate Score Comparison", fontsize=12, fontweight="bold", color="#1F2937", pad=12)
    ax.tick_params(axis="y", labelsize=8.5)
    ax.tick_params(axis="x", labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=8, loc="lower right")

    for bar, score in zip(bars, scores[::-1]):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2,
                f"{score:.1f}", va="center", fontsize=8, color="#374151")

    patches = [
        mpatches.Patch(color="#16A34A", label="Tier A — Recommended"),
        mpatches.Patch(color="#2563EB", label="Tier B — Interview"),
        mpatches.Patch(color="#D97706", label="Tier C — Consider"),
    ]
    ax.legend(handles=patches, fontsize=8, loc="lower right")

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return buf.read()

def make_spider_chart(candidates, top_n=3):
    top = candidates[:top_n]
    angles = np.linspace(0, 2*np.pi, len(DIM_LABELS), endpoint=False).tolist()
    angles += angles[:1]
    label_angles = angles[:-1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    colors = ["#7C3AED", "#DB2777", "#2563EB"]
    for idx, c in enumerate(top):
        vals = list(c["dims"]) + [c["dims"][0]]
        ax.plot(angles, vals, color=colors[idx], linewidth=2, label=c["name"])
        ax.fill(angles, vals, color=colors[idx], alpha=0.12)

    ax.set_xticks(label_angles)
    ax.set_xticklabels(DIM_LABELS, size=8.5)
    ax.set_yticks([1, 2, 3, 4])
    ax.set_yticklabels(["1", "2", "3", "4"], size=7, color="#6B7280")
    ax.set_ylim(0, 4)
    ax.set_title("Dimension Radar — Top 3 Candidates", fontsize=12, fontweight="bold", color="#1F2937", pad=18)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=9)
    ax.grid(color="#E5E7EB", linewidth=0.8)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return buf.read()

# ── Heatmap (HTML table) ─────────────────────────────────────────────
def score_to_color(score, max_score=4):
    pct = score / max_score
    if pct >= 0.875:
        return "#16A34A", "white"
    elif pct >= 0.625:
        return "#4ADE80", "#1F2937"
    elif pct >= 0.375:
        return "#FCD34D", "#1F2937"
    elif pct > 0:
        return "#FCA5A5", "#1F2937"
    else:
        return "#F3F4F6", "#9CA3AF"

def make_heatmap_html(candidates, top_n=15):
    rows_html = ""
    for c in candidates[:top_n]:
        row = f"<tr><td style='padding:5px 8px;font-size:11px;font-weight:600;white-space:nowrap;border-bottom:1px solid #E5E7EB;'>{c['name']}</td>"
        for score in c["dims"]:
            bg, fg = score_to_color(score)
            row += f"<td style='padding:5px 6px;text-align:center;background:{bg};color:{fg};font-size:11px;font-weight:600;border:1px solid #fff;'>{score}</td>"
        row += f"<td style='padding:5px 8px;text-align:center;font-weight:700;font-size:11px;border-bottom:1px solid #E5E7EB;color:#1F2937;'>{c['score']:.1f}</td></tr>"
        rows_html += row

    short_labels = ["Fn.Match", "Outcomes", "Env.Fit", "Ownership", "Stakehld", "HardSkill", "Growth"]
    header = "<tr><th style='padding:6px 8px;background:#6D28D9;color:white;font-size:10px;text-align:left;'>Candidate</th>"
    for lbl in short_labels:
        header += f"<th style='padding:6px 4px;background:#6D28D9;color:white;font-size:10px;text-align:center;'>{lbl}</th>"
    header += "<th style='padding:6px 8px;background:#6D28D9;color:white;font-size:10px;text-align:center;'>Total</th></tr>"

    return f"""
<table style='border-collapse:collapse;width:100%;font-family:Arial,sans-serif;'>
{header}
{rows_html}
</table>"""

# ══════════════════════════════════════════════════════════════════
# BUILD EMAIL HTML
# ══════════════════════════════════════════════════════════════════
bar_png    = make_bar_chart(CANDIDATES)
spider_png = make_spider_chart(CANDIDATES)
heatmap_html = make_heatmap_html(CANDIDATES)

tier_a = [c for c in CANDIDATES if c["score"] >= 85]
tier_b = [c for c in CANDIDATES if 70 <= c["score"] < 85]
tier_c = [c for c in CANDIDATES if 55 <= c["score"] < 70]
no_hire_auto = [c for c in CANDIDATES if c["score"] < 55]

in_budget = [c for c in CANDIDATES if "Within Budget" in c["budget_label"]]
verify    = [c for c in CANDIDATES if "Verify" in c["budget_label"]]

# ── Section 1: Screening Summary ─────────────────────────────────
summary_html = f"""
<h2 style='color:#6D28D9;border-bottom:2px solid #6D28D9;padding-bottom:6px;'>&#49;&#65039;&#8419; Screening Summary</h2>
<table style='border-collapse:collapse;width:100%;font-family:Arial,sans-serif;font-size:12px;'>
<tr style='background:#F3F4F6;'>
  <td style='padding:8px 12px;font-weight:600;width:40%;'>Position</td>
  <td style='padding:8px 12px;'>Field Coordinator — Research &amp; Impact Studies</td>
</tr>
<tr>
  <td style='padding:8px 12px;font-weight:600;background:#F3F4F6;'>Job ID</td>
  <td style='padding:8px 12px;'>36</td>
</tr>
<tr style='background:#F3F4F6;'>
  <td style='padding:8px 12px;font-weight:600;'>Budget Range</td>
  <td style='padding:8px 12px;'>PKR 200,000 &ndash; 250,000/month</td>
</tr>
<tr>
  <td style='padding:8px 12px;font-weight:600;background:#F3F4F6;'>Total Applicants</td>
  <td style='padding:8px 12px;'>216 (204 unique candidates)</td>
</tr>
<tr style='background:#F3F4F6;'>
  <td style='padding:8px 12px;font-weight:600;'>CVs Screened</td>
  <td style='padding:8px 12px;'>172 (with readable resumes) &mdash; keyword pre-screened all 172, deep-screened top 40</td>
</tr>
<tr>
  <td style='padding:8px 12px;font-weight:600;background:#F3F4F6;'>Shortlisted</td>
  <td style='padding:8px 12px;'><b>15 candidates</b> (3 Tier A &bull; 8 Tier B &bull; 4 Tier C)</td>
</tr>
<tr style='background:#F3F4F6;'>
  <td style='padding:8px 12px;font-weight:600;'>Over-Budget Strong Matches</td>
  <td style='padding:8px 12px;'><b>5 candidates</b> flagged (see Section 5)</td>
</tr>
<tr>
  <td style='padding:8px 12px;font-weight:600;background:#F3F4F6;'>Taleemabad Alumni</td>
  <td style='padding:8px 12px;'><b>2</b> (Faryal Afridi &mdash; former Field Coordinator; Muhammad Junaid &mdash; former M&amp;E Officer)</td>
</tr>
<tr style='background:#F3F4F6;'>
  <td style='padding:8px 12px;font-weight:600;'>Competitor Experience</td>
  <td style='padding:8px 12px;'>Hassnain Hassan (Tele-Taleem M&amp;E) &mdash; flagged in shortlist</td>
</tr>
<tr>
  <td style='padding:8px 12px;font-weight:600;background:#F3F4F6;'>Location</td>
  <td style='padding:8px 12px;'>126 Islamabad/RWP &bull; 46 other cities</td>
</tr>
<tr style='background:#F3F4F6;'>
  <td style='padding:8px 12px;font-weight:600;'>Recommended Hire</td>
  <td style='padding:8px 12px;'><b style='color:#16A34A;'>Amina Batool</b> (Score: 92.5 &mdash; Tier A)</td>
</tr>
<tr>
  <td style='padding:8px 12px;font-weight:600;background:#F3F4F6;'>Screening Date</td>
  <td style='padding:8px 12px;'>2026-03-05</td>
</tr>
</table>

<div style='background:#EFF6FF;border-left:4px solid #2563EB;padding:12px 16px;margin-top:16px;border-radius:4px;font-family:Arial,sans-serif;font-size:12px;'>
<b style='color:#1D4ED8;'>Screener&rsquo;s Note:</b> This is an unusually strong applicant pool for a Field Coordinator role. The top 3 candidates (Amina Batool, Muhammad Siddique, Mehwish Mukhtar) are genuinely Tier A — each bringing a distinct strength: AI assessment fieldwork, World Bank field supervision, and education research management respectively. The 2 Taleemabad alumni (ranks 6 and 9) are a notable highlight and warrant a structured re-engagement conversation.
</div>
"""

# ── Section 2: JD Scorecard ────────────────────────────────────────
jd_html = f"""
<h2 style='color:#6D28D9;border-bottom:2px solid #6D28D9;padding-bottom:6px;margin-top:32px;'>&#50;&#65039;&#8419; JD Scorecard — Must-Haves vs Pool</h2>
<table style='border-collapse:collapse;width:100%;font-family:Arial,sans-serif;font-size:12px;'>
<tr style='background:#6D28D9;color:white;'>
  <th style='padding:8px 12px;text-align:left;width:35%;'>Must-Have Criterion</th>
  <th style='padding:8px 12px;text-align:left;'>Pool Assessment</th>
  <th style='padding:8px 12px;text-align:center;width:15%;'>Coverage</th>
</tr>
<tr>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;font-weight:600;'>Field M&amp;E or Field Coordinator experience</td>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;'>Strong coverage in top shortlist — most top candidates have direct field M&amp;E roles</td>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;text-align:center;background:#DCFCE7;color:#166534;font-weight:700;'>High</td>
</tr>
<tr style='background:#F9FAFB;'>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;font-weight:600;'>Digital data collection tools (ODK / Kobo / SurveyCTO)</td>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;'>Most candidates have exposure; depth varies — probe in interviews</td>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;text-align:center;background:#FEF9C3;color:#854D0E;font-weight:700;'>Medium</td>
</tr>
<tr>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;font-weight:600;'>Education sector context</td>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;'>Top 10 candidates all have education sector exposure; some pivot from humanitarian</td>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;text-align:center;background:#DCFCE7;color:#166534;font-weight:700;'>High</td>
</tr>
<tr style='background:#F9FAFB;'>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;font-weight:600;'>Government school / district coordination</td>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;'>Moderate — 5–6 candidates with confirmed govt school coordination. Asad Farooq (44 schools) leads</td>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;text-align:center;background:#FEF9C3;color:#854D0E;font-weight:700;'>Medium</td>
</tr>
<tr>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;font-weight:600;'>Research & impact study experience</td>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;'>Amina Batool (AI assessment pilot), Mehwish (C4ED research), Fatima Razzaq (OPM) all strong</td>
  <td style='padding:8px 12px;border-bottom:1px solid #E5E7EB;text-align:center;background:#DCFCE7;color:#166534;font-weight:700;'>High</td>
</tr>
<tr style='background:#F9FAFB;'>
  <td style='padding:8px 12px;font-weight:600;'>Islamabad-based or willing to relocate</td>
  <td style='padding:8px 12px;'>126 of 172 applicants are Islamabad/RWP — all 15 shortlisted candidates are ISB-based or local</td>
  <td style='padding:8px 12px;text-align:center;background:#DCFCE7;color:#166534;font-weight:700;'>Excellent</td>
</tr>
</table>
"""

# ── Section 3: Ranked Shortlist ─────────────────────────────────────
def tier_badge(tier, color):
    return f"<span style='background:{color};color:white;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:700;'>{tier}</span>"

def budget_badge(label, bg, fg):
    return f"<span style='background:{bg};color:{fg};padding:2px 7px;border-radius:4px;font-size:10px;font-weight:600;'>{label}</span>"

shortlist_rows = ""
for c in CANDIDATES:
    shortlist_rows += f"""
<tr style='border-bottom:1px solid #E5E7EB;'>
  <td style='padding:7px 10px;text-align:center;font-weight:700;color:#374151;font-size:12px;'>{c['rank']}</td>
  <td style='padding:7px 10px;font-weight:600;font-size:12px;'>{c['name']}</td>
  <td style='padding:7px 10px;text-align:center;font-size:13px;font-weight:700;color:#1F2937;'>{c['score']:.1f}</td>
  <td style='padding:7px 10px;'>{tier_badge(c['tier'], c['tier_color'])}</td>
  <td style='padding:7px 10px;font-size:11px;color:#374151;'>{c['total_exp']}</td>
  <td style='padding:7px 10px;font-size:10px;color:#374151;'>{c['current_role']}</td>
  <td style='padding:7px 10px;font-size:10px;color:#374151;'>{"<br>".join(f"<span style='color:{['#6D28D9','#DB2777','#D97706','#065F46','#991B1B'][min(i,4)]};font-weight:600;'>{s[0]}</span>" for i, s in enumerate(c['org_signals']))}</td>
  <td style='padding:7px 10px;'>{budget_badge(c['budget_label'], c['budget_color'], c['budget_text_color'])}</td>
  <td style='padding:7px 10px;font-size:10px;color:#374151;'>{c['strengths'][0].split('</b>')[0].replace('<b>','')}</td>
  <td style='padding:7px 10px;font-size:10px;color:#DC2626;'>{c['risks'][0][:80]}...</td>
  <td style='padding:7px 10px;'>{tier_badge(c['tier'], c['tier_color'])}</td>
</tr>"""

shortlist_html = f"""
<h2 style='color:#6D28D9;border-bottom:2px solid #6D28D9;padding-bottom:6px;margin-top:32px;'>&#51;&#65039;&#8419; Ranked Shortlist &mdash; 15 Candidates</h2>
<table style='border-collapse:collapse;width:100%;font-family:Arial,sans-serif;font-size:12px;'>
<tr style='background:#6D28D9;color:white;'>
  <th style='padding:8px;text-align:center;'>#</th>
  <th style='padding:8px;text-align:left;'>Candidate</th>
  <th style='padding:8px;text-align:center;'>Score</th>
  <th style='padding:8px;text-align:center;'>Tier</th>
  <th style='padding:8px;text-align:left;'>Experience</th>
  <th style='padding:8px;text-align:left;'>Background / Current Role</th>
  <th style='padding:8px;text-align:left;'>Org Signal</th>
  <th style='padding:8px;text-align:center;'>Budget</th>
  <th style='padding:8px;text-align:left;'>Key Strength</th>
  <th style='padding:8px;text-align:left;'>Key Gap / Why Not Proceed</th>
  <th style='padding:8px;text-align:center;'>Verdict</th>
</tr>
{shortlist_rows}
</table>
"""

# ── Section 4: Deep Comparative Analysis ─────────────────────────────
def profile_card(c):
    org_html = ""
    for signal, detail in c["org_signals"]:
        color = "#6D28D9"
        if "TALEEMABAD" in signal:
            color = "#DB2777"
        elif "COMPETITOR" in signal:
            color = "#DC2626"
        elif "HIGH STRATEGIC" in signal:
            color = "#065F46"
        org_html += f"<div style='margin:2px 0;'><span style='background:{color};color:white;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:700;'>{signal}</span></div>"
        org_html += f"<div style='font-size:10px;color:#6B7280;margin-left:4px;margin-bottom:4px;'>{detail}</div>"

    strengths_html = "".join(f"<li style='margin:4px 0;font-size:11px;'>{s}</li>" for s in c["strengths"])
    risks_html = "".join(f"<li style='margin:4px 0;font-size:11px;color:#DC2626;'>{r}</li>" for r in c["risks"])
    iq_html = "".join(f"<li style='margin:4px 0;font-size:11px;color:#1D4ED8;'>{q}</li>" for q in c["interview_qs"])

    conf_color = {"High": "#16A34A", "Medium": "#D97706", "Low": "#DC2626"}.get(c["confidence"], "#6B7280")

    return f"""
<div style='border:1px solid #E5E7EB;border-radius:8px;margin-bottom:24px;overflow:hidden;font-family:Arial,sans-serif;'>
  <div style='background:{c["tier_color"]};color:white;padding:10px 16px;display:flex;justify-content:space-between;align-items:center;'>
    <span style='font-size:14px;font-weight:700;'>#{c["rank"]} {c["name"]}</span>
    <span style='font-size:13px;'>Score: {c["score"]:.1f} &bull; {c["tier"]}</span>
  </div>
  <div style='padding:14px 16px;background:#FAFAFA;'>
    <table style='width:100%;border-collapse:collapse;font-size:11px;'>
    <tr>
      <td style='padding:4px 8px;font-weight:600;width:22%;color:#374151;'>Total Experience</td>
      <td style='padding:4px 8px;'>{c["total_exp"]}</td>
      <td style='padding:4px 8px;font-weight:600;width:22%;color:#374151;'>Relevant Exp.</td>
      <td style='padding:4px 8px;'>{c["relevant_exp"]}</td>
    </tr>
    <tr style='background:#F3F4F6;'>
      <td style='padding:4px 8px;font-weight:600;color:#374151;'>Current Role</td>
      <td colspan='3' style='padding:4px 8px;'>{c["current_role"]}</td>
    </tr>
    <tr>
      <td style='padding:4px 8px;font-weight:600;color:#374151;'>Expected Salary</td>
      <td style='padding:4px 8px;'>{c["salary"]}</td>
      <td style='padding:4px 8px;font-weight:600;color:#374151;'>Budget Status</td>
      <td style='padding:4px 8px;'><span style='background:{c["budget_color"]};color:{c["budget_text_color"]};padding:2px 8px;border-radius:4px;font-weight:700;font-size:11px;'>{c["budget_label"]}</span></td>
    </tr>
    <tr style='background:#F3F4F6;'>
      <td style='padding:4px 8px;font-weight:600;color:#374151;'>Confidence</td>
      <td colspan='3' style='padding:4px 8px;'><span style='color:{conf_color};font-weight:700;'>{c["confidence"]}</span></td>
    </tr>
    </table>
  </div>
  <div style='padding:12px 16px;'>
    <div style='font-weight:700;color:#6D28D9;margin-bottom:6px;font-size:12px;'>Organisation Signals</div>
    {org_html}
  </div>
  <div style='padding:12px 16px;background:#F9FAFB;'>
    <div style='font-weight:700;color:#1F2937;margin-bottom:6px;font-size:12px;'>&#10024; USP</div>
    <div style='font-size:11px;color:#374151;font-style:italic;border-left:3px solid #6D28D9;padding-left:10px;'>{c["usp"]}</div>
  </div>
  <div style='padding:12px 16px;'>
    <div style='font-weight:700;color:#16A34A;margin-bottom:4px;font-size:12px;'>Key Strengths</div>
    <ul style='margin:0;padding-left:18px;'>{strengths_html}</ul>
  </div>
  <div style='padding:12px 16px;background:#FEF2F2;'>
    <div style='font-weight:700;color:#DC2626;margin-bottom:4px;font-size:12px;'>Risks / Watch Points</div>
    <ul style='margin:0;padding-left:18px;'>{risks_html}</ul>
  </div>
  <div style='padding:12px 16px;background:#EFF6FF;'>
    <div style='font-weight:700;color:#1D4ED8;margin-bottom:4px;font-size:12px;'>Suggested Interview Questions</div>
    <ol style='margin:0;padding-left:18px;'>{iq_html}</ol>
  </div>
</div>"""

dca_html = f"""
<h2 style='color:#6D28D9;border-bottom:2px solid #6D28D9;padding-bottom:6px;margin-top:32px;'>&#52;&#65039;&#8419; Deep Comparative Analysis</h2>
{"".join(profile_card(c) for c in CANDIDATES)}
"""

# ── Section 5: Visual Analytics ────────────────────────────────────
charts_html = f"""
<h2 style='color:#6D28D9;border-bottom:2px solid #6D28D9;padding-bottom:6px;margin-top:32px;'>&#53;&#65039;&#8419; Visual Analytics &mdash; Charts</h2>
<h3 style='color:#374151;margin-bottom:8px;'>A. Score Comparison &mdash; All Candidates</h3>
<img src='cid:bar_chart' style='max-width:100%;border:1px solid #E5E7EB;border-radius:6px;' alt='Score Bar Chart'>
<h3 style='color:#374151;margin-top:20px;margin-bottom:8px;'>B. Dimension Radar &mdash; Top 3 Candidates</h3>
<img src='cid:spider_chart' style='max-width:600px;border:1px solid #E5E7EB;border-radius:6px;' alt='Spider Radar Chart'>
"""

# ── Section 6: Over-Budget Flags ─────────────────────────────────────
ob_rows = ""
for ob in OVER_BUDGET:
    tc = "#16A34A" if ob["tier"] == "Tier A" else "#2563EB"
    ob_rows += f"""
<tr style='border-bottom:1px solid #E5E7EB;'>
  <td style='padding:8px 10px;font-weight:600;font-size:12px;'>{ob['name']}</td>
  <td style='padding:8px 10px;text-align:center;font-weight:700;font-size:13px;'>{ob['score']:.1f}</td>
  <td style='padding:8px 10px;'><span style='background:{tc};color:white;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:700;'>{ob['tier']}</span></td>
  <td style='padding:8px 10px;font-size:11px;'>{ob['exp']}</td>
  <td style='padding:8px 10px;font-size:11px;'>{ob['current_role']}</td>
  <td style='padding:8px 10px;font-size:11px;color:#D97706;'>{ob['budget_note']}</td>
  <td style='padding:8px 10px;font-size:11px;color:#374151;'>{ob['reason']}</td>
</tr>"""

ob_html = f"""
<h2 style='color:#D97706;border-bottom:2px solid #D97706;padding-bottom:6px;margin-top:32px;'>&#54;&#65039;&#8419; Out-of-Budget Strong Matches</h2>
<p style='font-size:12px;color:#374151;font-family:Arial,sans-serif;'>The following candidates scored strongly but are estimated to be above the PKR 200K–250K budget range given their seniority. Flagged for hiring manager awareness — do not reject without review.</p>
<table style='border-collapse:collapse;width:100%;font-family:Arial,sans-serif;font-size:12px;'>
<tr style='background:#D97706;color:white;'>
  <th style='padding:8px 10px;text-align:left;'>Candidate</th>
  <th style='padding:8px 10px;text-align:center;'>Score</th>
  <th style='padding:8px 10px;text-align:center;'>Tier</th>
  <th style='padding:8px 10px;text-align:left;'>Experience</th>
  <th style='padding:8px 10px;text-align:left;'>Current Role</th>
  <th style='padding:8px 10px;text-align:left;'>Budget Note</th>
  <th style='padding:8px 10px;text-align:left;'>Why Flag</th>
</tr>
{ob_rows}
</table>
"""

# ── Section 7: Heatmap ─────────────────────────────────────────────
heatmap_section_html = f"""
<h2 style='color:#6D28D9;border-bottom:2px solid #6D28D9;padding-bottom:6px;margin-top:32px;'>&#55;&#65039;&#8419; Dimension Heatmap &mdash; All 15 Shortlisted Candidates</h2>
<p style='font-size:12px;color:#374151;font-family:Arial,sans-serif;'>Scores per dimension (0–4). Green = strong &bull; Yellow = adequate &bull; Red = weak.</p>
{heatmap_html}
"""

# ── Section 8: Why Others Didn't Make It ─────────────────────────
nh_rows = ""
for n in NO_HIRE:
    nh_rows += f"""
<tr style='border-bottom:1px solid #E5E7EB;'>
  <td style='padding:7px 10px;font-weight:600;font-size:12px;'>{n['name']}</td>
  <td style='padding:7px 10px;text-align:center;font-size:12px;font-weight:700;color:#6B7280;'>{n['score']:.1f}</td>
  <td style='padding:7px 10px;font-size:11px;color:#374151;'>{n['background']}</td>
  <td style='padding:7px 10px;font-size:10px;color:#9CA3AF;'>{NH_ORG_SIGNAL.get(n['name'], '&mdash;')}</td>
  <td style='padding:7px 10px;text-align:center;color:#9CA3AF;'>&#8212;</td>
  <td style='padding:7px 10px;font-size:11px;color:#6B7280;'>{n['strength_note']}</td>
  <td style='padding:7px 10px;font-size:11px;color:#DC2626;'>{n['reason']}</td>
</tr>"""

nh_html = f"""
<h2 style='color:#6D28D9;border-bottom:2px solid #6D28D9;padding-bottom:6px;margin-top:32px;'>&#56;&#65039;&#8419; Why Others Didn&rsquo;t Make It</h2>
<p style='font-size:12px;color:#374151;font-family:Arial,sans-serif;'>Representative sample of candidates who did not meet the shortlist threshold. Full list available on request.</p>
<table style='border-collapse:collapse;width:100%;font-family:Arial,sans-serif;font-size:12px;'>
<tr style='background:#6D28D9;color:white;'>
  <th style='padding:8px 10px;text-align:left;'>Candidate</th>
  <th style='padding:8px 10px;text-align:center;'>Score</th>
  <th style='padding:8px 10px;text-align:left;'>Background / Current Role</th>
  <th style='padding:8px 10px;text-align:left;'>Org Signal</th>
  <th style='padding:8px 10px;text-align:center;'>Budget</th>
  <th style='padding:8px 10px;text-align:left;'>Key Strength</th>
  <th style='padding:8px 10px;text-align:left;'>Key Gap / Why Not Proceed</th>
</tr>
{nh_rows}
</table>
"""

# ── Next Steps ─────────────────────────────────────────────────────
next_steps_html = """
<h2 style='color:#6D28D9;border-bottom:2px solid #6D28D9;padding-bottom:6px;margin-top:32px;'>&#57;&#65039;&#8419; Recommended Next Steps</h2>
<ol style='font-family:Arial,sans-serif;font-size:12px;color:#374151;line-height:1.8;'>
  <li><b>Salary confirmation (urgent):</b> Contact all shortlisted candidates to confirm expected CTC before scheduling interviews. Budget verification for Mehwish Mukhtar and Fatima Razzaq is critical.</li>
  <li><b>Priority interview sequence:</b>
    <ol type='a'>
      <li>Amina Batool (Rank 1, Tier A) — first interview, fast-track if salary confirmed</li>
      <li>Muhammad Siddique (Rank 2, Tier A) — confirm salary via updated CV; request fresh application</li>
      <li>Mehwish Mukhtar (Rank 3, Tier A) — verify budget compatibility before interview</li>
      <li>Asad Farooq (Rank 4, Tier B) — strong government school background; interview in parallel</li>
    </ol>
  </li>
  <li><b>Taleemabad alumni re-engagement:</b> Faryal Afridi and Muhammad Junaid both departed Taleemabad. A structured re-engagement conversation (not a standard interview) is recommended — understanding why they left and what has changed is essential before proceeding.</li>
  <li><b>Competitor protocol:</b> Hassnain Hassan (Tele-Taleem) — follow standard IP/confidentiality onboarding protocol if hired.</li>
  <li><b>Over-budget review:</b> If budget flexibility is possible or a senior advisory role is considered, Fatima Mughal (Rank OB1, 91.25, 17 years MEAL) is exceptional and should be discussed with leadership.</li>
</ol>
"""

# ── Assemble full email ─────────────────────────────────────────────
EMAIL_HTML = f"""<!DOCTYPE html>
<html>
<head><meta charset='utf-8'></head>
<body style='font-family:Arial,sans-serif;color:#1F2937;max-width:900px;margin:0 auto;padding:20px;'>

<div style='background:linear-gradient(135deg,#6D28D9,#DB2777);padding:24px;border-radius:8px;margin-bottom:24px;'>
  <h1 style='color:white;margin:0;font-size:22px;'>Screening Report</h1>
  <p style='color:#E9D5FF;margin:6px 0 0 0;font-size:14px;'>Field Coordinator &mdash; Research &amp; Impact Studies &bull; Job ID 36</p>
</div>

{summary_html}
{jd_html}
{shortlist_html}
{dca_html}
{charts_html}
{ob_html}
{heatmap_section_html}
{nh_html}
{next_steps_html}

<div style='border-top:1px solid #E5E7EB;margin-top:32px;padding-top:12px;font-size:11px;color:#9CA3AF;font-family:Arial,sans-serif;'>
  Taleemabad Talent Acquisition Agent &bull; Confidential
</div>

</body>
</html>"""

# ── Send email ──────────────────────────────────────────────────────
msg = MIMEMultipart("related")
msg["Subject"] = "Screening Report- Field Coordinator Research & Impact Studies"
msg["From"]    = SENDER
msg["To"]      = RECIPIENT

alt = MIMEMultipart("alternative")
msg.attach(alt)
alt.attach(MIMEText(EMAIL_HTML, "html"))

bar_img = MIMEImage(bar_png, "png")
bar_img.add_header("Content-ID", "<bar_chart>")
bar_img.add_header("Content-Disposition", "inline", filename="bar_chart.png")
msg.attach(bar_img)

spider_img = MIMEImage(spider_png, "png")
spider_img.add_header("Content-ID", "<spider_chart>")
spider_img.add_header("Content-Disposition", "inline", filename="spider_chart.png")
msg.attach(spider_img)

print("Connecting to Gmail SMTP...")
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(SENDER, PASSWORD)
    smtp.send_message(msg)
print("Email sent successfully to", RECIPIENT)
