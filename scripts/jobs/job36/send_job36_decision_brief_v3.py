"""
Job 36 — Field Coordinator, Research & Impact Studies
"Final Candidates & Decision View" — PILOT (Ayesha + Jawwad)

Format: matches send_job32_decision_brief_pilot.py (approved April 2026).
CVs uploaded to Google Drive → shareable links injected into HTML email.
Pipeline state verified against DB + Gmail + Calendar — 8 April 2026.
"""

import os, sys, base64, io, smtplib, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import psycopg2
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build as gdrive_build
from googleapiclient.http import MediaFileUpload

from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

CV_DIR      = "c:/Agent Coco/output/cvs_job36_pipeline/"
PILOT_TO    = "ayesha.khan@taleemabad.com"
PILOT_CC    = "jawwad.ali@taleemabad.com"

POSITION = "Field Coordinator, Research &amp; Impact Studies"
DATE     = "8 April 2026"
BUDGET   = "PKR 200,000 – 250,000"

os.makedirs(CV_DIR, exist_ok=True)

# ── CANDIDATE DATA ─────────────────────────────────────────────────────────────
#
# VERIFIED 8 Apr 2026 — DB + Gmail + Calendar.
#
# PANEL DECISION PENDING (4): Jalal Ud Din, Scheherazade Noor, Muhammad Abubakr, Shazmina
#   NOTE: Jalal declined debrief calendar invite (7 Apr) — debrief today (8 Apr) status unclear.
#   Scheherazade debrief done 2 Apr. Abubakr debrief done 19 Mar. Shazmina debrief done 25 Mar.
# DEBRIEF DONE — ACTIVE (2): Moiz Khan (24 Mar), Maria Karim (6 Apr) — both active, panel decision pending.
#
# VALUES PASS (6):
#   Zubair Hussain (19 Mar, Ayesha), Amina Batool (16 Mar, Ayesha),
#   Usman Ahmed Khan (24 Mar, Ayesha), Mehwish (24 Mar, Ayesha),
#   Asad Farooq (19 Mar, Ayesha) — status=rejected in DB post-debrief (3 Apr),
#   Rosheen Naeem (30 Mar, Jawwad) — case study submitted 3 Apr, status=applied (DB anomaly)
#
# VALUES FAIL (6): Asif Khan, Faryal Afridi, Muhammad Omer Khan, Muhammad Siddique,
#                  Nain Tara (app 1536, 6 Apr, Ayat Butt), Muhammad Junaid (6 Apr, Ayesha)
#
# DEBRIEFS:
#   Scheherazade Noor — 2 Apr (declined calendar, offer extended)
#   Asad Farooq       — 3 Apr done (post-debrief status = rejected)
#   Maria Karim       — 6 Apr, declined debrief, not in pipeline
#   Jalal Ud Din      — 8 Apr today, declined calendar invite 7 Apr
#   Usman Ahmed Khan  — 9 Apr 12pm, confirmed
#   Amina Batool      — 10 Apr 10am, confirmed
#
# TOTAL APPLIED: 238

LEADING = [
    {
        "app_id": 1950, "name": "Jalal Ud Din", "score": "8.3",
        "verdict": "PANEL DECISION",
        "debrief": "8 Apr (today) — calendar declined 7 Apr",
        "tagline": "Debrief scheduled today — declined calendar invite yesterday. Confirm attendance.",
        "signal": (
            "Debrief was scheduled for today, 8 April at 10:30am. "
            "He declined the calendar invite yesterday (7 Apr) — unclear whether the debrief is proceeding. "
            "This needs to be confirmed immediately. Salary ask PKR 120,000 — well within budget."
        ),
        "probe": (
            "Confirm whether today's debrief is happening. If yes: "
            "probe research design ownership — has he designed a study or implemented others'? "
            "Field team management: largest team, longest deployment, most difficult context. "
            "Government interface at district level."
        ),
    },
    {
        "app_id": 1430, "name": "Scheherazade Noor", "score": "8.0",
        "verdict": "PANEL DECISION",
        "debrief": "2 Apr — debrief done",
        "tagline": "Debrief done 2 April. Panel decision pending. Salary within budget at 150–175k.",
        "signal": (
            "Debrief completed 2 April. Salary ask PKR 150,000–175,000 — within budget. "
            "Panel decision pending — no further steps taken since debrief."
        ),
        "probe": (
            "What is the panel's post-debrief decision? Document outcome and communicate to candidate."
        ),
    },
    {
        "app_id": 1518, "name": "Zubair Hussain", "score": "9.4",
        "verdict": "VALUES PASS",
        "debrief": "Case study not yet scheduled",
        "tagline": "Highest values-cleared score at 9.4. Over budget at 220k — decision needed before case study.",
        "signal": (
            "Strongest CV in the values-cleared group, score 9.4. Cleared values 19 March (host: Ayesha). "
            "Salary ask PKR 220,000 — over the budget ceiling of 200k. "
            "No case study has been issued. A budget exception decision is needed before moving him forward. "
            "He has been waiting since March — this needs a call either way."
        ),
        "probe": (
            "Pre-case study: confirm with hiring manager whether 220k is acceptable. "
            "At debrief: most complex field coordination assignment — team size, geography, research design. "
            "Experience with district/provincial government liaison."
        ),
    },
    {
        "app_id": 1921, "name": "Rosheen Naeem", "score": "—",
        "verdict": "CASE STUDY IN",
        "debrief": "Submitted 3 Apr — debrief not yet scheduled",
        "tagline": "Values pass 30 Mar (host: Jawwad). Case study submitted 3 Apr. Debrief not booked.",
        "signal": (
            "Cleared values 30 March (host: Jawwad Ali). Case study submitted 3 April. "
            "No debrief has been scheduled. She is an active case study candidate — debrief should be booked. "
            "DB status shows 'applied' — likely a data entry gap, not a withdrawal."
        ),
        "probe": (
            "Action: book her debrief. "
            "At debrief: quality of research design choices in the submission. "
            "Field experience: multi-site data collection coordination. "
            "Government and community interface."
        ),
    },
    {
        "app_id": 2018, "name": "Moiz Khan", "score": "—",
        "verdict": "DEBRIEF DONE",
        "debrief": "24 Mar — debrief done",
        "tagline": "Case study submitted 13 Mar. Debrief done 24 March. Panel decision pending.",
        "signal": (
            "Case study sent 11 March, submitted 13 March. Debrief completed 24 March. "
            "Active candidate — panel decision pending. "
            "No further steps have been taken since the debrief. Needs a call on next steps."
        ),
        "probe": (
            "What is the panel's decision post-debrief? Document outcome and communicate to candidate."
        ),
    },
    {
        "app_id": 2021, "name": "Maria Karim", "score": "—",
        "verdict": "DEBRIEF DONE",
        "debrief": "6 Apr — debrief done",
        "tagline": "Debrief done 6 April. Active candidate — panel decision pending.",
        "signal": (
            "Debrief completed 6 April. Active candidate — panel decision pending. "
            "She declined the calendar notification but attended the debrief. "
            "No next steps have been communicated yet."
        ),
        "probe": (
            "What is the panel's decision post-debrief? If proceeding: confirm next step. "
            "If not: document reason and communicate to candidate."
        ),
    },
]

DISCUSSION = [
    {
        "app_id": 1903, "name": "Muhammad Abubakr", "score": "7.4",
        "verdict": "PANEL DECISION",
        "debrief": "Debrief done — 19 Mar",
        "tagline": "Debrief done 19 March. Panel decision pending. At budget ceiling at 250k.",
        "signal": (
            "Debrief completed 19 March — over 6 weeks ago. Salary ask PKR 250,000 — at the budget ceiling. "
            "Panel decision pending. No further steps have been taken since the debrief. "
            "A call needs to be made and documented."
        ),
        "probe": (
            "What is the panel's post-debrief decision? Document outcome and confirm budget sign-off if proceeding."
        ),
    },
    {
        "app_id": 2017, "name": "Shazmina", "score": "—",
        "verdict": "PANEL DECISION",
        "debrief": "Debrief done — 25 Mar",
        "tagline": "Debrief done 25 March. Panel decision pending. No CV score on file.",
        "signal": (
            "Debrief completed 25 March. PKR 200,000 — within budget. "
            "No CV score on file. Panel decision pending — no further steps taken since debrief."
        ),
        "probe": (
            "What is the panel's post-debrief decision? Document and communicate to candidate."
        ),
    },
    {
        "app_id": 1755, "name": "Usman Ahmed Khan", "score": "8.1",
        "verdict": "VALUES PASS",
        "debrief": "9 Apr, 12pm — confirmed",
        "tagline": "Values cleared. Debrief confirmed tomorrow at 12pm. Within budget at 160k.",
        "signal": (
            "Cleared values 24 March (host: Ayesha). Salary ask PKR 160,000 — within budget. "
            "Debrief confirmed tomorrow, 9 April at 12pm — rescheduled multiple times, now confirmed. "
            "Case study submitted. Profile shows research coordination experience relevant to the role."
        ),
        "probe": (
            "At debrief: field deployment experience — geography, team size, duration. "
            "Research design literacy: contributed to study design or only data collection? "
            "Government and community interface at district level."
        ),
    },
    {
        "app_id": 1857, "name": "Amina Batool", "score": "7.4",
        "verdict": "VALUES PASS",
        "debrief": "10 Apr, 10am — confirmed",
        "tagline": "Values cleared. Debrief confirmed Friday 10 Apr at 10am. Over budget at 300–310k.",
        "signal": (
            "Cleared values 16 March (host: Ayesha). Debrief confirmed 10 April at 10am. "
            "Salary ask PKR 300,000–310,000 — significantly over the budget ceiling of 250k. "
            "Confirm with the hiring manager before the call whether this is a live candidacy or courtesy debrief."
        ),
        "probe": (
            "Pre-debrief: confirm with HM whether budget exception is on the table. "
            "If yes: probe field leadership depth to justify the salary ask."
        ),
    },
    {
        "app_id": 1700, "name": "Asad Farooq", "score": "8.5",
        "verdict": "DEBRIEF DONE",
        "debrief": "3 Apr — status: rejected in DB",
        "tagline": "Values cleared. Debrief done 3 April. DB shows rejected. Verify panel decision.",
        "signal": (
            "Cleared values 19 March (host: Ayesha). Debrief completed 3 April. "
            "DB shows status as 'rejected'. Needs confirmation — was he rejected post-debrief or is this an entry error? "
            "Salary ask PKR 140,000 — within budget. CV score 8.5."
        ),
        "probe": (
            "Clarify post-debrief decision. Document reason if rejected."
        ),
    },
    {
        "app_id": 1808, "name": "Mehwish", "score": "7.0",
        "verdict": "VALUES PASS",
        "debrief": "Case study sent 7 Apr — awaiting submission",
        "tagline": "Values cleared. Case study sent 7 Apr. Within budget at 200k.",
        "signal": (
            "Cleared values 24 March (host: Ayesha). Case study sent 7 April. "
            "Salary ask PKR 200,000 — within budget. Awaiting submission. "
            "Lowest CV score (7.0) among values-cleared candidates — case study is the real test."
        ),
        "probe": (
            "At debrief: research design ownership — designed independently or implemented others' designs? "
            "Field coordination: largest team, most complex deployment."
        ),
    },
]

DEBRIEF_SCHEDULE = [
    ("Jalal Ud Din",     "8 Apr, 10:30am (today)", "Declined calendar",  "Declined invite 7 Apr — confirm whether debrief is happening today."),
    ("Usman Ahmed Khan", "9 Apr, 12pm",             "Confirmed",          "Case study debrief — confirmed after multiple reschedules."),
    ("Amina Batool",     "10 Apr, 10am",            "Confirmed",          "Case study debrief — over budget. Pre-confirm with HM before call."),
]

PIPELINE = [
    {"name": "Jawad Khan",        "status": "Values interview not yet completed · CV score 9.3 · PKR 200,000"},
    {"name": "Fatima Razzaq",     "status": "Values interview not yet completed · CV score 9.1 · PKR 185,999"},
    {"name": "Fatima Mughal",     "status": "Values interview not yet completed · CV score 8.8 · PKR 170,000"},
    {"name": "HabibunNabi",       "status": "Values interview not yet completed · CV score 8.6 · PKR 80,000"},
    {"name": "Ali Zia",           "status": "Values interview not yet completed · CV score 8.1 · As per budget"},
    {"name": "Asif Khan",         "status": "VALUES FAILED — OUT · CV score 10.0 (highest in cohort) · 19 Mar · Host: Jawwad"},
    {"name": "Faryal Afridi",     "status": "VALUES FAILED — OUT · 19 Mar · Host: Ayesha"},
    {"name": "Muhammad Omer Khan","status": "VALUES FAILED — OUT · CV score 8.0 · 17 Mar · Host: Ayat Butt"},
    {"name": "Muhammad Siddique", "status": "VALUES FAILED — OUT · CV score 7.9 · 25 Mar · Host: Aymen Abid"},
    {"name": "Nain Tara",         "status": "VALUES FAILED — OUT · 6 Apr · Host: Ayat Butt (separate application from Job 35)"},
    {"name": "Muhammad Junaid",   "status": "VALUES FAILED — OUT · 6 Apr · Host: Ayesha (separate application from Job 35)"},
]

CV_APP_IDS = {
    1950: "Jalal Ud Din",
    1430: "Scheherazade Noor",
    1518: "Zubair Hussain",
    1921: "Rosheen Naeem",
    1903: "Muhammad Abubakr",
    2017: "Shazmina",
    1755: "Usman Ahmed Khan",
    1857: "Amina Batool",
    1700: "Asad Farooq",
    1808: "Mehwish",
}

PIPELINE_NAMES = [
    "Jawad Khan", "Fatima Razzaq", "Fatima Mughal", "HabibunNabi", "Ali Zia",
    "Asif Khan", "Faryal Afridi", "Muhammad Omer Khan", "Muhammad Siddique",
]


# ── STEP 1: FETCH CVs FROM DB ──────────────────────────────────────────────────

def fetch_cvs():
    print("Fetching CVs from DB...")
    conn = psycopg2.connect(
        host="ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
        dbname="neondb", user="neondb_owner",
        password="npg_kBQ10OASHEmd", sslmode="require"
    )
    cur = conn.cursor()

    ids = list(CV_APP_IDS.keys())
    cur.execute("""
        SELECT a.id, c.first_name || ' ' || c.last_name AS full_name, c.resume_data
        FROM applications a JOIN candidates c ON a.candidate_id = c.id
        WHERE a.id = ANY(%s) AND c.resume_data IS NOT NULL
    """, (ids,))
    rows = cur.fetchall()

    cur.execute("""
        SELECT a.id, c.first_name || ' ' || c.last_name AS full_name, c.resume_data
        FROM applications a JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = 36
          AND (c.first_name || ' ' || c.last_name) = ANY(%s)
          AND c.resume_data IS NOT NULL
    """, (PIPELINE_NAMES,))
    rows += cur.fetchall()

    cur.close(); conn.close()

    cv_paths = {}
    seen_names = {}
    for app_id, full_name, b64 in rows:
        name = CV_APP_IDS.get(app_id, full_name or str(app_id))
        if name in seen_names:
            continue
        seen_names[name] = True
        fname = f"{app_id}_{re.sub(r'[^a-zA-Z0-9_]', '_', name)}_CV.pdf"
        path  = os.path.join(CV_DIR, fname)
        try:
            with open(path, "wb") as f:
                f.write(base64.b64decode(b64))
            cv_paths[app_id] = (path, fname, name)
            print(f"  Saved: {name}")
        except Exception as e:
            print(f"  FAILED {name}: {e}")
    return cv_paths


# ── STEP 2: UPLOAD CVs TO GOOGLE DRIVE ────────────────────────────────────────

def upload_cvs_to_drive(cv_paths):
    creds = Credentials.from_authorized_user_file(
        "c:/Agent Coco/token_drive.json",
        scopes=["https://www.googleapis.com/auth/drive.file"])
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    service = gdrive_build("drive", "v3", credentials=creds)

    drive_links = {}
    for app_id, (cv_path, _, name) in cv_paths.items():
        if not os.path.exists(cv_path):
            print(f"  SKIP (not found): {name}")
            continue
        print(f"  Uploading: {name}...")
        meta  = {"name": f"{name} — CV (Job 36 Field Coordinator, Research & Impact Studies).pdf"}
        media = MediaFileUpload(cv_path, mimetype="application/pdf")
        f     = service.files().create(body=meta, media_body=media, fields="id").execute()
        fid   = f["id"]
        service.permissions().create(
            fileId=fid, body={"type": "anyone", "role": "reader"}
        ).execute()
        drive_links[name] = f"https://drive.google.com/file/d/{fid}/view"
        print(f"    -> {drive_links[name]}")
    return drive_links


# ── STEP 3: BUILD HTML EMAIL ───────────────────────────────────────────────────

def build_html_email(drive_links):

    def cv_link(name):
        url = drive_links.get(name)
        if url:
            return f'<a href="{url}" style="color:#1565c0;font-weight:bold;">{name}</a>'
        return f'<b>{name}</b>'

    stat_boxes = """
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0;">
      <tr>
        <td style="padding:14px 8px;background:#f3e5f5;border-radius:6px;text-align:center;width:18%">
          <div style="font-size:22px;font-weight:bold;color:#6a1b9a;">238</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">Total applied</div>
        </td>
        <td width="6"></td>
        <td style="padding:14px 8px;background:#e3f0fb;border-radius:6px;text-align:center;width:18%">
          <div style="font-size:22px;font-weight:bold;color:#1565c0;">4</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">Panel decisions pending</div>
        </td>
        <td width="6"></td>
        <td style="padding:14px 8px;background:#e8f5e9;border-radius:6px;text-align:center;width:18%">
          <div style="font-size:22px;font-weight:bold;color:#1a7a4a;">6</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">Values cleared</div>
        </td>
        <td width="6"></td>
        <td style="padding:14px 8px;background:#fff8e1;border-radius:6px;text-align:center;width:18%">
          <div style="font-size:22px;font-weight:bold;color:#e65100;">2</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">Debriefs this week</div>
        </td>
        <td width="6"></td>
        <td style="padding:14px 8px;background:#fce4ec;border-radius:6px;text-align:center;width:18%">
          <div style="font-size:22px;font-weight:bold;color:#c62828;">6</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">Values failed — OUT</div>
        </td>
      </tr>
    </table>"""

    where_we_are = f"""
    <p style="margin:0 0 10px;font-size:13px;line-height:1.7;color:#1a1a1a;">
      238 candidates applied for the Field Coordinator role. Budget is {BUDGET}.
      Four candidates have completed debriefs and are at panel decision stage: Jalal Ud Din, Scheherazade Noor,
      Muhammad Abubakr, and Shazmina — all awaiting a panel call on next steps.
      Moiz Khan and Maria Karim have also completed debriefs and are active — panel decisions pending on both.
      Six candidates cleared values: Zubair Hussain, Asad Farooq, Usman Ahmed Khan,
      Amina Batool, Mehwish, and Rosheen Naeem.
      Six candidates failed values and are out: Asif Khan (highest CV score at 10.0), Faryal Afridi,
      Muhammad Omer Khan, Muhammad Siddique, and two additional candidates from the 6 April batch.
      Debriefs confirmed this week: Usman Ahmed Khan (9 Apr, 12pm) and Amina Batool (10 Apr, 10am).
      Jalal Ud Din declined his debrief calendar invite (7 Apr) — status of today's debrief needs confirmation.
      Rosheen Naeem submitted her case study on 3 April with no debrief yet booked.
      Zubair Hussain (highest values-cleared score, 9.4) is still awaiting a case study — budget exception decision needed.
      Five candidates are still pending values: Jawad Khan leads at CV score 9.3.
    </p>"""

    sched_html = """
    <table width="100%" cellpadding="8" cellspacing="0"
           style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
      <tr style="background:#e8f0fb;">
        <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;width:26%">Candidate</td>
        <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;width:22%">Date &amp; Time</td>
        <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;width:16%">Status</td>
        <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;">Notes</td>
      </tr>"""
    sched_rows = [
        ("Jalal Ud Din",     "8 Apr, 10:30am (today)", "Declined calendar", "#fff3e0"),
        ("Usman Ahmed Khan", "9 Apr, 12pm",             "Confirmed",         "#f1f8e9"),
        ("Amina Batool",     "10 Apr, 10am",            "Confirmed",         "#f1f8e9"),
    ]
    notes = [
        "Declined invite 7 Apr — confirm whether debrief is still happening today.",
        "Confirmed after multiple reschedules.",
        "Over budget (300–310k). Pre-confirm with HM before the call.",
    ]
    for (cname, date, status, bg), note in zip(sched_rows, notes):
        sched_html += f"""
      <tr style="background:{bg};">
        <td style="border:1px solid #ddd;">{cv_link(cname)}</td>
        <td style="border:1px solid #ddd;">{date}</td>
        <td style="border:1px solid #ddd;">{status}</td>
        <td style="border:1px solid #ddd;">{note}</td>
      </tr>"""
    sched_html += "\n    </table>"

    def verdict_color(v):
        return {
            "OFFER OUT":        "#1565c0",
            "VALUES PASS":      "#1a7a4a",
            "CASE STUDY IN":    "#1a7a4a",
            "POST-DEBRIEF":     "#e65100",
        }.get(v, "#636e72")

    def candidate_block(c):
        vc = verdict_color(c["verdict"])
        return f"""
    <div style="background:#f7f9fc;border-left:4px solid {vc};
                padding:14px 16px;margin-bottom:14px;border-radius:0 6px 6px 0;">
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td style="font-size:14px;font-weight:bold;">{cv_link(c["name"])}</td>
          <td style="text-align:center;width:120px;">
            <span style="color:{vc};font-weight:bold;font-size:12px;">{c["verdict"]}</span>
          </td>
          <td style="text-align:right;width:180px;font-size:12px;color:#636e72;font-style:italic;">{c["debrief"]}</td>
        </tr>
      </table>
      <p style="margin:8px 0 4px;font-size:12px;color:#636e72;font-style:italic;">{c["tagline"]}</p>
      <p style="margin:0 0 8px;font-size:13px;line-height:1.6;">{c["signal"]}</p>
      <p style="margin:0;font-size:12px;color:#7b341e;line-height:1.6;">
        <b>At debrief, probe:</b> {c["probe"]}
      </p>
    </div>"""

    leading_html    = "".join(candidate_block(c) for c in LEADING)
    discussion_html = "".join(candidate_block(c) for c in DISCUSSION)

    pip_rows_html = ""
    for i, p in enumerate(PIPELINE):
        bg = "#f7f9fc" if i % 2 == 0 else "#ffffff"
        pip_rows_html += f"""
      <tr style="background:{bg};">
        <td style="border:1px solid #dfe6e9;padding:8px 10px;font-weight:bold;width:28%;">{cv_link(p["name"])}</td>
        <td style="border:1px solid #dfe6e9;padding:8px 10px;font-size:13px;">{p["status"]}</td>
      </tr>"""

    pipeline_html = f"""
    <table width="100%" cellpadding="0" cellspacing="0"
           style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
      <tr style="background:#e8f0fb;">
        <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;width:28%">Candidate</td>
        <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;">Status</td>
      </tr>{pip_rows_html}
    </table>"""

    def sec(title):
        return (f'<p style="margin:24px 0 6px;font-size:14px;font-weight:bold;'
                f'color:#1565c0;border-bottom:1px solid #dfe6e9;padding-bottom:4px;">'
                f'{title}</p>')

    html = f"""\
<html>
<body style="font-family:Georgia,serif;font-size:14px;color:#1a1a1a;
             max-width:680px;margin:auto;background:#f0f4f0;padding:24px 0;">
<table width="680" cellpadding="0" cellspacing="0"
       style="background:#ffffff;border-radius:8px;
              box-shadow:0 2px 12px rgba(0,0,0,0.08);overflow:hidden;">

  <!-- HEADER -->
  <tr>
    <td style="background:#1a2a3a;padding:24px 32px;">
      <p style="margin:0;font-size:10px;color:#90a4ae;letter-spacing:2px;
                text-transform:uppercase;font-family:Georgia,serif;">
        People &amp; Culture &middot; Hiring Decision Brief
      </p>
      <p style="margin:8px 0 2px;font-size:20px;font-weight:bold;
                color:#ffffff;font-family:Georgia,serif;">
        Final Candidates &amp; Decision View
      </p>
      <p style="margin:0;font-size:13px;color:#90caf9;font-family:Georgia,serif;">
        Field Coordinator, Research &amp; Impact Studies
      </p>
    </td>
  </tr>

  <!-- BODY -->
  <tr>
    <td style="padding:28px 32px;">

      <p style="margin:0 0 4px;">Hi Ayesha,</p>
      <p style="margin:0 0 16px;font-size:13px;color:#444;line-height:1.6;">
        Here is the hiring decision brief for
        <strong>Field Coordinator, Research &amp; Impact Studies</strong>.
        Pipeline state as of {DATE}. Budget: {BUDGET}.
      </p>

      {stat_boxes}

      {sec("Where We Are")}
      {where_we_are}

      {sec("Debrief Schedule — This Week")}
      {sched_html}

      {sec("Leading Candidates")}
      <p style="margin:0 0 12px;font-size:13px;color:#444;line-height:1.6;">
        Candidates with debriefs done or imminent, and values-cleared candidates at case study stage.
        Names are hyperlinked — click to open their CV.
      </p>
      {leading_html}

      {sec("Discussion Candidates")}
      <p style="margin:0 0 12px;font-size:13px;color:#444;line-height:1.6;">
        Candidates with open decisions, upcoming debriefs, or flags that need resolution.
      </p>
      {discussion_html}

      {sec("Also in Pipeline")}
      <p style="margin:0 0 12px;font-size:13px;color:#444;line-height:1.6;">
        Values pending and values-failed candidates.
      </p>
      {pipeline_html}

    </td>
  </tr>

  <!-- FOOTER -->
  <tr>
    <td style="padding:12px 32px;background:#f5f5f5;font-size:11px;color:#888;
               font-family:Georgia,serif;">
      Taleemabad Talent Acquisition &nbsp;|&nbsp; hiring@taleemabad.com
      &nbsp;|&nbsp; {DATE} &nbsp;|&nbsp; PILOT — Ayesha &amp; Jawwad only
    </td>
  </tr>

</table>
</body>
</html>"""
    return html


# ── MAIN ───────────────────────────────────────────────────────────────────────

def main():
    print("Step 1: Fetching CVs from DB...")
    cv_paths = fetch_cvs()
    print(f"CVs ready: {len(cv_paths)}")

    print("\nStep 2: Uploading CVs to Google Drive...")
    drive_links = upload_cvs_to_drive(cv_paths)
    print(f"Uploaded: {len(drive_links)} CVs")

    print("\nStep 3: Building HTML email...")
    html_body = build_html_email(drive_links)

    print("Step 4: Sending pilot email...")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "[PILOT] Final Candidates & Decision View — Field Coordinator, Research & Impact Studies"
    msg["From"]    = EMAIL_USER
    msg["To"]      = PILOT_TO
    msg["CC"]      = PILOT_CC
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    recipients = [PILOT_TO, PILOT_CC]
    allow_candidate_addresses(recipients)
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo(); s.starttls(); s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(),
                      context="job36_decision_brief_v3_pilot")
    print(f"Sent to {PILOT_TO} (CC: {PILOT_CC})")


if __name__ == "__main__":
    main()
