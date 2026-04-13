"""
Combined reply to Sabeena's "Impact hiring Update" thread.
Job 35 (Junior Research Associate) + Job 36 (Field Coordinator) decision briefs in one email.
PILOT: Ayesha only first. Then full thread send after approval.
"""

import os, sys, smtplib, base64
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# ── Drive links (uploaded 8 Apr 2026) ─────────────────────────────────────────

DL35 = {
    'Shahid Kamal':    'https://drive.google.com/file/d/1JBf4GoN1qenknnazJ1HCffSuFrRreQzg/view',
    'Nain Tara':       'https://drive.google.com/file/d/18Bb5JtgebLi_xmN6OGNdR31i8WZMmnBu/view',
    'Ali Muhammad':    'https://drive.google.com/file/d/1Ne5J--TugGbeiCYRDuAzrFHnT8VqDBp6/view',
    'Hadiyah Shaheen': 'https://drive.google.com/file/d/1JYFtYVgxxz0Nni1iuARJA5V4kSJ7ZBEd/view',
    'Wasif Mehdi':     'https://drive.google.com/file/d/15FfduJnjyNvziwrzPLtBsLzz9iqZuLp-/view',
    'Fatima Tu Zahra': 'https://drive.google.com/file/d/1QvxALhHjMF6K3GO6BYj4gmzqwjPZjlAZ/view',
    'Ayesha Nadeem':   'https://drive.google.com/file/d/1q4xsDYcgbjiP837IANEyxL3UPuMJl23s/view',
    'Rameez Wasif':    'https://drive.google.com/file/d/1mMTjLXgJpfG3mtsBb-jcGh27_kaudk3j/view',
    'Mariam Rehman':   'https://drive.google.com/file/d/1CY-gTWgolKkRFvb8AkZpThA1-RPEuAXz/view',
    'Daniyah Noor':    'https://drive.google.com/file/d/1Vc7MBRgCwgnNj4zpXRfsYQZSyn7OQyXp/view',
    'Maria Malik':     'https://drive.google.com/file/d/1MOeWBcVo0eZ4DhnzKnswCozG9cKQkrgh/view',
    # Leading candidates
    'Rahima Omar':     'https://drive.google.com/file/d/1os0Zw5DqFyNQgrgc_I2qffVL0ppenM2l/view',
    'Dur E Nayab':     'https://drive.google.com/file/d/1N0TrfVRtEJP-z5qMErGzrhyeqDbbAWuX/view',
    'Mahnoor Hasan':   'https://drive.google.com/file/d/1GDRsXmkzqhguAg8aTImkfUczG-iYCZcM/view',
    'Hassan Zafar':    'https://drive.google.com/file/d/1Dj0FAkVfvRNmlBdMzImL8SeELrao4FGW/view',
    # Pipeline / failed
    'Rabia Zafar':     'https://drive.google.com/file/d/12EHRfUi39zksM5afxz0gGRiQsBgGcEH7/view',
    'Zeeshan Ali':     'https://drive.google.com/file/d/1eR_cr08eRwrHAeCgc2Bth276fN4nCuRO/view',
    'Faryal Afridi':   'https://drive.google.com/file/d/1PBifzHAB1h2QlcHcyGmlJD4PEyP837Mr/view',
    'Muhammad Junaid': 'https://drive.google.com/file/d/1n5mctbGWovtRgyVqJSD4Xjus8fgAYrh4/view',
}

DL36 = {
    'Scheherazade Noor':  'https://drive.google.com/file/d/1bSV3Ih2G3hPG6IzJDHeiqYAZD9Tb8kxV/view',
    'Zubair Hussain':     'https://drive.google.com/file/d/1uBLJhyqMkLEQkOTFrjyopbMH3SZRtFuG/view',
    'Asad Farooq':        'https://drive.google.com/file/d/1NfxuYVFFDyEdAzu5rLz3sEY0DX2yZD93/view',
    'Usman Ahmed Khan':   'https://drive.google.com/file/d/1FWADcrag4sIaSeEsPRuZzfKW0WfoA04U/view',
    'Mehwish':            'https://drive.google.com/file/d/14zjhM18RGTjO1op_9fuRe1otnLEkMQxq/view',
    'Amina Batool':       'https://drive.google.com/file/d/1S1DEoMfi15lzcnNEjmtXQ7VbnsCcOpjn/view',
    'Muhammad Abubakr':   'https://drive.google.com/file/d/1iR2wkOj9G-jAcnLlTo5u-XncZcr5YuSV/view',
    'Rosheen Naeem':      'https://drive.google.com/file/d/14WbHQvVluolqwAO5C4_dZZMFPICcZN1o/view',
    'Jalal Ud Din':       'https://drive.google.com/file/d/1AvtbuEz38iLhRpO1RETsjGf-fFz9-EuW/view',
    'Shazmina':           'https://drive.google.com/file/d/1lrwHYf9LuPMyXs6mitVm27CjKJKsI2DU/view',
    'Moiz Khan':          'https://drive.google.com/file/d/1uP25L7XbeJuDXf6BN4nd58UkAHC43NA-/view',
    'Maria Karim':        'https://drive.google.com/file/d/1act8w-QBwOigNkSTWG_ctphv_ejG8Rz7/view',
    'Jawad Khan':         'https://drive.google.com/file/d/1gLlCouu1Hkc0-A3zVSSOF2Fi6BprwAKN/view',
    'Fatima Razzaq':      'https://drive.google.com/file/d/1VwsqCtdXZS32ji2aY2cK93nrjvFHjFaI/view',
    'Fatima Mughal':      'https://drive.google.com/file/d/1pzP_tnNrJD-8HQOn4amgdMv7zeMwSHzG/view',
    'HabibunNabi':        'https://drive.google.com/file/d/1F-LRpVcj91eY91kQipX1nlSzr5k2hd8m/view',
    'Ali Zia':            'https://drive.google.com/file/d/172j9gQ9CG00VmI2A5xzATSfra77HDnOQ/view',
    'Asif Khan':          'https://drive.google.com/file/d/19ahUMTzHeWtV-oMpnG_gPI10HxZUWL1R/view',
    'Faryal Afridi':      'https://drive.google.com/file/d/1FgxXTNwh5qvxgC_naKyqU30BJhuvNan8/view',
    'Muhammad Omer Khan': 'https://drive.google.com/file/d/1_3-1WUQj8qhtuAZ5qaLcWYgob1PU6-R_/view',
    'Muhammad Siddique':  'https://drive.google.com/file/d/16Ee6X9w7ZJ-VmZjWLDS2zz-3jy3VpKu_/view',
}


# ── Job 35 data ────────────────────────────────────────────────────────────────

J35_LEADING = [
    {
        "name": "Rahima Omar", "score": "—", "verdict": "DEBRIEF TODAY",
        "debrief": "8 Apr — today",
        "tagline": "Values cleared. Case study in. Debrief today.",
        "signal": "Values cleared. Case study submitted. Debrief is scheduled for today, 8 April.",
        "probe": "Research design ownership — designed or implemented? Field data collection experience. Analytical tools used.",
    },
    {
        "name": "Dur E Nayab", "score": "—", "verdict": "DEBRIEF DONE",
        "debrief": "7 Apr — done yesterday",
        "tagline": "Debrief done 7 April. Panel decision pending.",
        "signal": "Values cleared. Debrief completed yesterday, 7 April. Panel decision pending.",
        "probe": "Panel decision: proceed or not? Document and communicate to candidate.",
    },
    {
        "name": "Mahnoor Hasan", "score": "—", "verdict": "DEBRIEF CONFIRMED",
        "debrief": "9 Apr, 4pm",
        "tagline": "Debrief confirmed tomorrow at 4pm.",
        "signal": "Values cleared. Case study submitted. Debrief confirmed for 9 April at 4pm.",
        "probe": "Research methodology depth. Impact measurement experience. Policy translation skills.",
    },
    {
        "name": "Hassan Zafar", "score": "—", "verdict": "DEBRIEF CONFIRMED",
        "debrief": "10 Apr, 2pm",
        "tagline": "Debrief confirmed Friday at 2pm.",
        "signal": "Values cleared. Case study submitted. Debrief confirmed for 10 April at 2pm.",
        "probe": "Quantitative vs qualitative balance. Report writing for policy audiences. Research design ownership.",
    },
]

J35_DISCUSSION = [
    {
        "name": "Hadiyah Shaheen", "score": "8.4", "verdict": "OVERDUE",
        "debrief": "Case study — 13 days overdue",
        "tagline": "Values cleared. Case study sent — 13 days overdue. No submission.",
        "signal": "Values cleared 24 March. Case study sent but not yet submitted — now 13 days overdue. Needs a follow-up nudge or a decision on whether to close this candidacy.",
        "probe": "Follow up: confirm whether she is still in the process.",
    },
    {
        "name": "Maria Malik", "score": "7.8", "verdict": "CASE STUDY SENT",
        "debrief": "Case study sent 7 Apr",
        "tagline": "Values cleared. Case study sent 7 April. Awaiting submission.",
        "signal": "Values cleared. Case study sent 7 April. Awaiting submission. Within budget at PKR 70,000.",
        "probe": "At debrief: research design experience. Analytical tools. Report writing for external audiences.",
    },
    {
        "name": "Nain Tara", "score": "8.6", "verdict": "CASE STUDY SENT",
        "debrief": "Case study sent — awaiting submission",
        "tagline": "Values cleared. Case study sent. Salary ask unusually low at PKR 55,000 — verify.",
        "signal": "Values cleared. Case study sent. Salary ask PKR 55,000 — unusually low for this role. Verify before progressing to offer.",
        "probe": "Salary verification. At debrief: research design ownership. Field experience.",
    },
    {
        "name": "Ali Muhammad", "score": "8.9", "verdict": "VALUES PASS",
        "debrief": "Scorecard pending",
        "tagline": "Values pass confirmed. Scorecard not yet entered in DB.",
        "signal": "Values interview completed. Result: pass. Scorecard not yet entered in DB. Case study not yet sent.",
        "probe": "Action: enter scorecard in DB, then send case study.",
    },
    {
        "name": "Wasif Mehdi", "score": "9.1", "verdict": "NOT INTERVIEWED",
        "debrief": "Values interview not yet done",
        "tagline": "Highest pending CV score at 9.1. Values interview not yet completed.",
        "signal": "Highest CV score among pending candidates at 9.1. Values interview not yet completed. Salary ask PKR 100,000 — within budget.",
        "probe": "Action: schedule values interview urgently — he leads the pending group.",
    },
    {
        "name": "Rameez Wasif", "score": "8.0", "verdict": "VALUES PASS",
        "debrief": "Case study not yet sent",
        "tagline": "Values pass 26 March (host: Jawwad). Case study not yet sent.",
        "signal": "Cleared values 26 March (host: Jawwad Ali). Case study has not been sent yet. PKR 130,000 — within budget.",
        "probe": "Action: send case study immediately — values pass is already 12 days old.",
    },
]

J35_PIPELINE = [
    {"name": "Ayesha Nadeem",   "status": "VALUES PASS 25 Mar — scorecard missing from DB · PKR 70,000"},
    {"name": "Mariam Rehman",   "status": "Values interview not yet completed · CV score 8.5 · PKR 120,000"},
    {"name": "Shahid Kamal",    "status": "Values interview not yet completed · CV score 8.6 · PKR 150,000"},
    {"name": "Fatima Tu Zahra", "status": "Values interview not yet completed · CV score 8.3 · PKR 70–80k"},
    {"name": "Daniyah Noor",    "status": "Values interview not yet completed · CV score 7.5 · PKR 120,000"},
    {"name": "Rabia Zafar",     "status": "VALUES FAILED — OUT · CV score 9.4 · Host: Ayesha"},
    {"name": "Zeeshan Ali",     "status": "VALUES FAILED — OUT · CV score 9.0"},
    {"name": "Faryal Afridi",   "status": "VALUES FAILED — OUT · CV score 9.5 · Host: Jawwad"},
    {"name": "Muhammad Junaid", "status": "VALUES FAILED — OUT · 6 Apr · Host: Ayesha"},
]

J35_DEBRIEF_ROWS = [
    ("Rahima Omar",  "8 Apr (today)",  "Confirmed", "#fff3e0", "Debrief today."),
    ("Mahnoor Hasan","9 Apr, 4pm",     "Confirmed", "#f1f8e9", "Case study submitted."),
    ("Hassan Zafar", "10 Apr, 2pm",    "Confirmed", "#f1f8e9", "Case study submitted."),
]


# ── Job 36 data ────────────────────────────────────────────────────────────────

J36_LEADING = [
    {
        "name": "Jalal Ud Din", "score": "8.3", "verdict": "PANEL DECISION",
        "debrief": "8 Apr (today) — calendar declined 7 Apr",
        "tagline": "Debrief scheduled today — declined calendar invite yesterday. Confirm attendance.",
        "signal": "Debrief was scheduled for today, 8 April at 10:30am. He declined the calendar invite yesterday (7 Apr) — unclear whether the debrief is proceeding. Confirm immediately. Salary ask PKR 120,000 — within budget.",
        "probe": "Confirm debrief status. If yes: research design ownership, field team management, government interface at district level.",
    },
    {
        "name": "Scheherazade Noor", "score": "8.0", "verdict": "PANEL DECISION",
        "debrief": "2 Apr — debrief done",
        "tagline": "Debrief done 2 April. Panel decision pending. Salary within budget at 150–175k.",
        "signal": "Debrief completed 2 April. Salary ask PKR 150,000–175,000 — within budget. Panel decision pending.",
        "probe": "Panel decision: proceed or not? Document and communicate to candidate.",
    },
    {
        "name": "Zubair Hussain", "score": "9.4", "verdict": "VALUES PASS",
        "debrief": "Case study not yet scheduled",
        "tagline": "Highest values-cleared score at 9.4. Over budget at 220k — decision needed before case study.",
        "signal": "Strongest CV in values-cleared group, score 9.4. Cleared values 19 March. Salary ask PKR 220,000 — over ceiling of 200k. No case study issued. Budget exception decision needed before progressing.",
        "probe": "Pre-case study: confirm budget exception with HM. At debrief: complex field coordination, government liaison.",
    },
    {
        "name": "Rosheen Naeem", "score": "—", "verdict": "CASE STUDY IN",
        "debrief": "Submitted 3 Apr — debrief not yet scheduled",
        "tagline": "Values pass 30 Mar. Case study submitted 3 Apr. Debrief not booked.",
        "signal": "Cleared values 30 March (host: Jawwad). Case study submitted 3 April. Debrief not yet booked — action needed.",
        "probe": "Action: book her debrief. At debrief: research design quality, multi-site coordination, government interface.",
    },
    {
        "name": "Moiz Khan", "score": "—", "verdict": "DEBRIEF DONE",
        "debrief": "24 Mar — debrief done",
        "tagline": "Case study submitted 13 Mar. Debrief done 24 March. Panel decision pending.",
        "signal": "Case study submitted 13 March. Debrief completed 24 March. Active candidate — panel decision pending. No further steps taken since debrief.",
        "probe": "Panel decision: proceed or not? Document and communicate to candidate.",
    },
    {
        "name": "Maria Karim", "score": "—", "verdict": "DEBRIEF DONE",
        "debrief": "6 Apr — debrief done",
        "tagline": "Debrief done 6 April. Active candidate — panel decision pending.",
        "signal": "Debrief completed 6 April. Active candidate — panel decision pending. No next steps communicated yet.",
        "probe": "Panel decision: proceed or not? Document and communicate to candidate.",
    },
]

J36_DISCUSSION = [
    {
        "name": "Muhammad Abubakr", "score": "7.4", "verdict": "PANEL DECISION",
        "debrief": "Debrief done — 19 Mar",
        "tagline": "Debrief done 19 March. Panel decision pending. At budget ceiling at 250k.",
        "signal": "Debrief completed 19 March — over 6 weeks ago. Salary ask PKR 250,000 — at budget ceiling. Panel decision pending.",
        "probe": "Panel decision: proceed or not? Document outcome and confirm budget sign-off if proceeding.",
    },
    {
        "name": "Shazmina", "score": "—", "verdict": "PANEL DECISION",
        "debrief": "Debrief done — 25 Mar",
        "tagline": "Debrief done 25 March. Panel decision pending. No CV score on file.",
        "signal": "Debrief completed 25 March. PKR 200,000 — within budget. Panel decision pending.",
        "probe": "Panel decision: proceed or not? Document and communicate to candidate.",
    },
    {
        "name": "Usman Ahmed Khan", "score": "8.1", "verdict": "VALUES PASS",
        "debrief": "9 Apr, 12pm — confirmed",
        "tagline": "Values cleared. Debrief confirmed tomorrow at 12pm. Within budget at 160k.",
        "signal": "Cleared values 24 March. Salary ask PKR 160,000 — within budget. Debrief confirmed 9 April at 12pm.",
        "probe": "Field deployment experience, research design literacy, government interface at district level.",
    },
    {
        "name": "Amina Batool", "score": "7.4", "verdict": "VALUES PASS",
        "debrief": "10 Apr, 10am — confirmed",
        "tagline": "Values cleared. Debrief confirmed Friday at 10am. Over budget at 300–310k.",
        "signal": "Cleared values 16 March. Debrief confirmed 10 April at 10am. Salary ask PKR 300,000–310,000 — significantly over ceiling. Pre-confirm with HM whether this is a live candidacy.",
        "probe": "Pre-debrief: confirm budget exception with HM. If live: probe field leadership depth.",
    },
    {
        "name": "Asad Farooq", "score": "8.5", "verdict": "DEBRIEF DONE",
        "debrief": "3 Apr — panel decision pending",
        "tagline": "Values cleared. Debrief done 3 April. Panel decision pending.",
        "signal": "Cleared values 19 March. Debrief completed 3 April. Salary ask PKR 140,000 — within budget. Panel decision pending.",
        "probe": "Panel decision: proceed or not? Document outcome.",
    },
    {
        "name": "Mehwish", "score": "7.0", "verdict": "CASE STUDY SENT",
        "debrief": "Case study sent 7 Apr — awaiting submission",
        "tagline": "Values cleared. Case study sent 7 Apr. Within budget at 200k.",
        "signal": "Cleared values 24 March. Case study sent 7 April — awaiting submission. Salary PKR 200,000 — within budget.",
        "probe": "At debrief: research design ownership, field coordination depth.",
    },
]

J36_PIPELINE = [
    {"name": "Jawad Khan",         "status": "Values interview not yet completed · CV score 9.3 · PKR 200,000"},
    {"name": "Fatima Razzaq",      "status": "Values interview not yet completed · CV score 9.1 · PKR 185,999"},
    {"name": "Fatima Mughal",      "status": "Values interview not yet completed · CV score 8.8 · PKR 170,000"},
    {"name": "HabibunNabi",        "status": "Values interview not yet completed · CV score 8.6 · PKR 80,000"},
    {"name": "Ali Zia",            "status": "Values interview not yet completed · CV score 8.1 · As per budget"},
    {"name": "Asif Khan",          "status": "VALUES FAILED — OUT · CV score 10.0 (highest in cohort) · 19 Mar · Host: Jawwad"},
    {"name": "Faryal Afridi",      "status": "VALUES FAILED — OUT · 19 Mar · Host: Ayesha"},
    {"name": "Muhammad Omer Khan", "status": "VALUES FAILED — OUT · CV score 8.0 · 17 Mar · Host: Ayat Butt"},
    {"name": "Muhammad Siddique",  "status": "VALUES FAILED — OUT · CV score 7.9 · 25 Mar · Host: Aymen Abid"},
    {"name": "Nain Tara",          "status": "VALUES FAILED — OUT · 6 Apr · Host: Ayat Butt"},
    {"name": "Muhammad Junaid",    "status": "VALUES FAILED — OUT · 6 Apr · Host: Ayesha"},
]

J36_DEBRIEF_ROWS = [
    ("Jalal Ud Din",     "8 Apr, 10:30am (today)", "Declined calendar", "#fff3e0", "Declined invite 7 Apr — confirm whether debrief is happening today."),
    ("Usman Ahmed Khan", "9 Apr, 12pm",             "Confirmed",         "#f1f8e9", "Confirmed after multiple reschedules."),
    ("Amina Batool",     "10 Apr, 10am",            "Confirmed",         "#f1f8e9", "Over budget (300–310k). Pre-confirm with HM before the call."),
]


# ── HTML builders ──────────────────────────────────────────────────────────────

def cv_link(name, drive_links):
    url = drive_links.get(name)
    if url:
        return f'<a href="{url}" style="color:#1565c0;font-weight:bold;">{name}</a>'
    return f'<b>{name}</b>'

def verdict_badge(v):
    colors = {
        "DEBRIEF TODAY":     "#e65100",
        "DEBRIEF DONE":      "#636e72",
        "DEBRIEF CONFIRMED": "#1a7a4a",
        "CASE STUDY IN":     "#1a7a4a",
        "CASE STUDY SENT":   "#1a7a4a",
        "VALUES PASS":       "#1a7a4a",
        "PANEL DECISION":    "#1565c0",
        "NOT INTERVIEWED":   "#e65100",
        "OVERDUE":           "#c62828",
    }
    c = colors.get(v, "#636e72")
    return c

def candidate_block(c, drive_links):
    vc = verdict_badge(c["verdict"])
    return f"""
<div style="background:#f7f9fc;border-left:4px solid {vc};
            padding:14px 16px;margin-bottom:14px;border-radius:0 6px 6px 0;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr>
      <td style="font-size:14px;font-weight:bold;">{cv_link(c["name"], drive_links)}</td>
      <td style="text-align:center;width:140px;">
        <span style="color:{vc};font-weight:bold;font-size:11px;">{c["verdict"]}</span>
      </td>
      <td style="text-align:right;width:200px;font-size:11px;color:#636e72;font-style:italic;">{c["debrief"]}</td>
    </tr>
  </table>
  <p style="margin:6px 0 4px;font-size:12px;color:#636e72;font-style:italic;">{c["tagline"]}</p>
  <p style="margin:0 0 6px;font-size:13px;line-height:1.6;">{c["signal"]}</p>
  <p style="margin:0;font-size:12px;color:#7b341e;line-height:1.6;">
    <b>At debrief, probe:</b> {c["probe"]}
  </p>
</div>"""

def debrief_table(rows, drive_links):
    html = """<table width="100%" cellpadding="8" cellspacing="0"
       style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
  <tr style="background:#e8f0fb;">
    <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;width:26%">Candidate</td>
    <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;width:22%">Date &amp; Time</td>
    <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;width:16%">Status</td>
    <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;">Notes</td>
  </tr>"""
    for name, date, status, bg, note in rows:
        html += f"""
  <tr style="background:{bg};">
    <td style="border:1px solid #ddd;">{cv_link(name, drive_links)}</td>
    <td style="border:1px solid #ddd;">{date}</td>
    <td style="border:1px solid #ddd;">{status}</td>
    <td style="border:1px solid #ddd;">{note}</td>
  </tr>"""
    html += "\n</table>"
    return html

def pipeline_table(rows, drive_links):
    html = """<table width="100%" cellpadding="0" cellspacing="0"
       style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
  <tr style="background:#e8f0fb;">
    <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;width:28%">Candidate</td>
    <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;">Status</td>
  </tr>"""
    for i, p in enumerate(rows):
        bg = "#f7f9fc" if i % 2 == 0 else "#ffffff"
        html += f"""
  <tr style="background:{bg};">
    <td style="border:1px solid #dfe6e9;padding:8px 10px;font-weight:bold;">{cv_link(p["name"], drive_links)}</td>
    <td style="border:1px solid #dfe6e9;padding:8px 10px;">{p["status"]}</td>
  </tr>"""
    html += "\n</table>"
    return html

def sec(title):
    return (f'<p style="margin:20px 0 6px;font-size:13px;font-weight:bold;'
            f'color:#1565c0;border-bottom:1px solid #dfe6e9;padding-bottom:4px;">'
            f'{title}</p>')

def position_header(title, subtitle, stats_html):
    return f"""
<div style="background:#1a2a3a;padding:20px 28px;border-radius:6px 6px 0 0;margin-top:32px;">
  <p style="margin:0;font-size:10px;color:#90a4ae;letter-spacing:2px;text-transform:uppercase;
            font-family:Georgia,serif;">People &amp; Culture &middot; Hiring Decision Brief</p>
  <p style="margin:6px 0 2px;font-size:18px;font-weight:bold;color:#ffffff;font-family:Georgia,serif;">
    Final Candidates &amp; Decision View</p>
  <p style="margin:0;font-size:13px;color:#90caf9;font-family:Georgia,serif;">{title}</p>
</div>
<div style="background:#ffffff;border:1px solid #ddd;border-top:none;padding:24px 28px 28px;">
  <p style="margin:0 0 6px;font-size:12px;color:#888;">{subtitle}</p>
  {stats_html}"""

def position_footer():
    return "</div>"


def build_combined_html():

    # ── Job 35 stat boxes ──────────────────────────────────────────────────────
    stats35 = """
<table width="100%" cellpadding="0" cellspacing="0" style="margin:16px 0;">
  <tr>
    <td style="padding:12px 6px;background:#f3e5f5;border-radius:6px;text-align:center;width:18%">
      <div style="font-size:20px;font-weight:bold;color:#6a1b9a;">291</div>
      <div style="font-size:10px;color:#555;margin-top:2px;">Total applied</div>
    </td><td width="5"></td>
    <td style="padding:12px 6px;background:#e8f5e9;border-radius:6px;text-align:center;width:18%">
      <div style="font-size:20px;font-weight:bold;color:#1a7a4a;">9</div>
      <div style="font-size:10px;color:#555;margin-top:2px;">Values cleared</div>
    </td><td width="5"></td>
    <td style="padding:12px 6px;background:#e3f0fb;border-radius:6px;text-align:center;width:18%">
      <div style="font-size:20px;font-weight:bold;color:#1565c0;">4</div>
      <div style="font-size:10px;color:#555;margin-top:2px;">Case studies submitted</div>
    </td><td width="5"></td>
    <td style="padding:12px 6px;background:#fff8e1;border-radius:6px;text-align:center;width:18%">
      <div style="font-size:20px;font-weight:bold;color:#e65100;">4</div>
      <div style="font-size:10px;color:#555;margin-top:2px;">Debriefs this week</div>
    </td><td width="5"></td>
    <td style="padding:12px 6px;background:#fce4ec;border-radius:6px;text-align:center;width:18%">
      <div style="font-size:20px;font-weight:bold;color:#c62828;">4</div>
      <div style="font-size:10px;color:#555;margin-top:2px;">Values failed — OUT</div>
    </td>
  </tr>
</table>"""

    # ── Job 36 stat boxes ──────────────────────────────────────────────────────
    stats36 = """
<table width="100%" cellpadding="0" cellspacing="0" style="margin:16px 0;">
  <tr>
    <td style="padding:12px 6px;background:#f3e5f5;border-radius:6px;text-align:center;width:18%">
      <div style="font-size:20px;font-weight:bold;color:#6a1b9a;">238</div>
      <div style="font-size:10px;color:#555;margin-top:2px;">Total applied</div>
    </td><td width="5"></td>
    <td style="padding:12px 6px;background:#e3f0fb;border-radius:6px;text-align:center;width:18%">
      <div style="font-size:20px;font-weight:bold;color:#1565c0;">4</div>
      <div style="font-size:10px;color:#555;margin-top:2px;">Panel decisions pending</div>
    </td><td width="5"></td>
    <td style="padding:12px 6px;background:#e8f5e9;border-radius:6px;text-align:center;width:18%">
      <div style="font-size:20px;font-weight:bold;color:#1a7a4a;">6</div>
      <div style="font-size:10px;color:#555;margin-top:2px;">Values cleared</div>
    </td><td width="5"></td>
    <td style="padding:12px 6px;background:#fff8e1;border-radius:6px;text-align:center;width:18%">
      <div style="font-size:20px;font-weight:bold;color:#e65100;">2</div>
      <div style="font-size:10px;color:#555;margin-top:2px;">Debriefs this week</div>
    </td><td width="5"></td>
    <td style="padding:12px 6px;background:#fce4ec;border-radius:6px;text-align:center;width:18%">
      <div style="font-size:20px;font-weight:bold;color:#c62828;">6</div>
      <div style="font-size:10px;color:#555;margin-top:2px;">Values failed — OUT</div>
    </td>
  </tr>
</table>"""

    # ── Where We Are narratives ────────────────────────────────────────────────
    where35 = """<p style="margin:0 0 10px;font-size:13px;line-height:1.7;color:#1a1a1a;">
291 candidates applied for the Junior Research Associate role. Budget is PKR 150,000–200,000.
Nine candidates have cleared values. Four case studies have been submitted and debriefs are underway this week:
Rahima Omar (today), Mahnoor Hasan (9 Apr) and Hassan Zafar (10 Apr) have debriefs confirmed.
Dur E Nayab's debrief was completed yesterday — panel decision pending.
Hadiyah Shaheen's case study submission is 13 days overdue and needs a follow-up.
Rameez Wasif cleared values on 26 March but has not yet received his case study.
Ali Muhammad cleared values but the scorecard is not yet in DB — this needs to be entered before the case study is sent.
Wasif Mehdi (score 9.1) leads the pending group and has not yet had his values interview.
Four candidates failed values and are out of the pipeline.
</p>"""

    where36 = """<p style="margin:0 0 10px;font-size:13px;line-height:1.7;color:#1a1a1a;">
238 candidates applied for the Field Coordinator role. Budget is PKR 200,000–250,000.
Six candidates have cleared values. Four candidates have completed debriefs with panel decisions pending:
Jalal Ud Din, Scheherazade Noor, Muhammad Abubakr, and Shazmina.
Moiz Khan and Maria Karim have also completed debriefs and are active candidates — panel decisions pending on both.
Debriefs confirmed this week: Usman Ahmed Khan (9 Apr, 12pm) and Amina Batool (10 Apr, 10am).
Jalal Ud Din declined his calendar invite (7 Apr) — status of today's debrief needs confirmation.
Rosheen Naeem submitted her case study on 3 April with no debrief yet booked.
Zubair Hussain (highest values-cleared score at 9.4) is awaiting a budget exception decision before his case study is sent.
Six candidates failed values and are out.
</p>"""

    j35_leading_html    = "".join(candidate_block(c, DL35) for c in J35_LEADING)
    j35_discussion_html = "".join(candidate_block(c, DL35) for c in J35_DISCUSSION)
    j35_pipeline_html   = pipeline_table(J35_PIPELINE, DL35)
    j35_debrief_html    = debrief_table(J35_DEBRIEF_ROWS, DL35)

    j36_leading_html    = "".join(candidate_block(c, DL36) for c in J36_LEADING)
    j36_discussion_html = "".join(candidate_block(c, DL36) for c in J36_DISCUSSION)
    j36_pipeline_html   = pipeline_table(J36_PIPELINE, DL36)
    j36_debrief_html    = debrief_table(J36_DEBRIEF_ROWS, DL36)

    html = f"""\
<html>
<body style="font-family:Georgia,serif;font-size:14px;color:#1a1a1a;
             max-width:700px;margin:auto;background:#f0f4f0;padding:24px 0;">

<!-- INTRO -->
<table width="700" cellpadding="0" cellspacing="0"
       style="background:#ffffff;border-radius:8px;
              box-shadow:0 2px 12px rgba(0,0,0,0.08);margin-bottom:8px;">
  <tr>
    <td style="padding:24px 32px;">
      <p style="margin:0 0 8px;">Hi Sabeena,</p>
      <p style="margin:0;font-size:13px;color:#444;line-height:1.7;">
        Sharing below the hiring decision briefs for both positions you asked about.
        Pipeline state as of <strong>8 April 2026</strong>.
        Candidate names are hyperlinked — click any name to open their CV.
      </p>
    </td>
  </tr>
</table>

<!-- JOB 35 -->
<table width="700" cellpadding="0" cellspacing="0"
       style="background:#ffffff;border-radius:8px;
              box-shadow:0 2px 12px rgba(0,0,0,0.08);margin-bottom:16px;overflow:hidden;">
  <tr>
    <td style="background:#1a2a3a;padding:20px 32px;">
      <p style="margin:0;font-size:10px;color:#90a4ae;letter-spacing:2px;
                text-transform:uppercase;font-family:Georgia,serif;">
        Position 1 &middot; Hiring Decision Brief
      </p>
      <p style="margin:6px 0 2px;font-size:18px;font-weight:bold;
                color:#ffffff;font-family:Georgia,serif;">
        Final Candidates &amp; Decision View
      </p>
      <p style="margin:0;font-size:13px;color:#90caf9;font-family:Georgia,serif;">
        Junior Research Associate, Impact &amp; Policy &nbsp;&middot;&nbsp; PKR 150,000–200,000
      </p>
    </td>
  </tr>
  <tr>
    <td style="padding:24px 32px;">
      {stats35}
      {sec("Where We Are")}
      {where35}
      {sec("Debrief Schedule — This Week")}
      {j35_debrief_html}
      {sec("Leading Candidates")}
      <p style="margin:0 0 10px;font-size:13px;color:#444;">Values-cleared candidates with debriefs done or imminent.</p>
      {j35_leading_html}
      {sec("Discussion Candidates")}
      <p style="margin:0 0 10px;font-size:13px;color:#444;">Open decisions, flags, and candidates needing action.</p>
      {j35_discussion_html}
      {sec("Also in Pipeline")}
      {j35_pipeline_html}
    </td>
  </tr>
</table>

<!-- JOB 36 -->
<table width="700" cellpadding="0" cellspacing="0"
       style="background:#ffffff;border-radius:8px;
              box-shadow:0 2px 12px rgba(0,0,0,0.08);margin-bottom:16px;overflow:hidden;">
  <tr>
    <td style="background:#1a2a3a;padding:20px 32px;">
      <p style="margin:0;font-size:10px;color:#90a4ae;letter-spacing:2px;
                text-transform:uppercase;font-family:Georgia,serif;">
        Position 2 &middot; Hiring Decision Brief
      </p>
      <p style="margin:6px 0 2px;font-size:18px;font-weight:bold;
                color:#ffffff;font-family:Georgia,serif;">
        Final Candidates &amp; Decision View
      </p>
      <p style="margin:0;font-size:13px;color:#90caf9;font-family:Georgia,serif;">
        Field Coordinator, Research &amp; Impact Studies &nbsp;&middot;&nbsp; PKR 200,000–250,000
      </p>
    </td>
  </tr>
  <tr>
    <td style="padding:24px 32px;">
      {stats36}
      {sec("Where We Are")}
      {where36}
      {sec("Debrief Schedule — This Week")}
      {j36_debrief_html}
      {sec("Leading Candidates")}
      <p style="margin:0 0 10px;font-size:13px;color:#444;">Candidates with debriefs done or imminent, and values-cleared candidates at case study stage.</p>
      {j36_leading_html}
      {sec("Discussion Candidates")}
      <p style="margin:0 0 10px;font-size:13px;color:#444;">Open decisions, upcoming debriefs, or flags needing resolution.</p>
      {j36_discussion_html}
      {sec("Also in Pipeline")}
      {j36_pipeline_html}
    </td>
  </tr>
</table>

<!-- FOOTER -->
<table width="700" cellpadding="0" cellspacing="0"
       style="background:#ffffff;border-radius:8px;">
  <tr>
    <td style="padding:12px 32px;background:#f5f5f5;font-size:11px;color:#888;
               font-family:Georgia,serif;border-radius:0 0 8px 8px;">
      Taleemabad Talent Acquisition &nbsp;|&nbsp; hiring@taleemabad.com
      &nbsp;|&nbsp; 8 April 2026
    </td>
  </tr>
</table>

</body>
</html>"""
    return html


def main(pilot=True):
    html = build_combined_html()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Re: Impact hiring Update"
    msg["From"]    = EMAIL_USER

    if pilot:
        msg["To"] = "ayesha.khan@taleemabad.com"
        recipients = ["ayesha.khan@taleemabad.com"]
        print("Sending PILOT to Ayesha only...")
    else:
        msg["To"] = "sabeena.abbasi@taleemabad.com"
        msg["Cc"] = ("jawwad.ali@taleemabad.com, zeshan.dhillon@taleemabad.com, "
                     "muzzammil.patel@taleemabad.com, ahwaz.akhtar@taleemabad.com, "
                     "haroon.yasin@taleemabad.com, hiring@taleemabad.com")
        # Threading headers for Gmail reply
        msg["In-Reply-To"]  = "<CAM0yQNEZX6QqfFEtUZnOnsJFY=0EoLy5foNL6uBxp2ws26A6XQ@mail.gmail.com>"
        msg["References"]   = ("<CAG0n=g-SVRTK344wEWOEiAth+BEp35R23T2nRr89LGQY8ynPOA@mail.gmail.com> "
                               "<CAM0yQNEZX6QqfFEtUZnOnsJFY=0EoLy5foNL6uBxp2ws26A6XQ@mail.gmail.com>")
        recipients = ["sabeena.abbasi@taleemabad.com", "jawwad.ali@taleemabad.com",
                      "zeshan.dhillon@taleemabad.com", "muzzammil.patel@taleemabad.com",
                      "ahwaz.akhtar@taleemabad.com", "haroon.yasin@taleemabad.com",
                      "hiring@taleemabad.com"]
        print("Sending LIVE reply to full thread...")

    msg.attach(MIMEText(html, "html", "utf-8"))
    allow_candidate_addresses(recipients)
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo(); s.starttls(); s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(),
                      context="impact_hiring_update_combined_reply")
    print(f"Done. Sent to: {recipients}")


if __name__ == "__main__":
    import sys
    pilot_mode = "--live" not in sys.argv
    main(pilot=pilot_mode)
