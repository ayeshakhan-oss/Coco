"""
Job 35 — Junior Research Associate, Impact & Policy
"Final Candidates & Decision View" — PILOT (Ayesha + Jawwad)

Format: matches send_job32_decision_brief_pilot.py (approved April 2026).
CVs uploaded to Google Drive → shareable links injected into HTML email.
Pipeline state as of 8 April 2026.
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

CV_DIR      = "c:/Agent Coco/output/cvs_job35_pipeline/"
PILOT_TO    = "ayesha.khan@taleemabad.com"
PILOT_CC    = "jawwad.ali@taleemabad.com"

POSITION = "Junior Research Associate, Impact &amp; Policy"
DATE     = "8 April 2026"

os.makedirs(CV_DIR, exist_ok=True)

# ── CANDIDATE DATA ─────────────────────────────────────────────────────────────
#
# CORRECTED 8 Apr 2026 — verified against DB, Gmail, and Google Calendar.
#
# VALUES CLEARED (8):
#   Rahima Omar    — cleared, submitted case study 28 Mar, debrief TODAY 8 Apr
#   Dur E Nayab    — cleared, submitted case study 28 Mar, debrief WAS YESTERDAY 7 Apr (result pending)
#   Mahnoor Hasan  — cleared, submitted case study 28 Mar, debrief TOMORROW 9 Apr 4pm
#   Hassan Zafar   — cleared, submitted case study 28 Mar, debrief 10 Apr 2pm
#   Hadiyah Shaheen— cleared, case study sent 26 Mar — NO SUBMISSION AFTER 13 DAYS (flag)
#   Maria Malik    — cleared, case study sent 7 Apr (yesterday)
#   Nain Tara      — cleared 6 Apr (host: Ayat Butt), case study not yet sent
#   Ali Muhammad   — Zero In 7 Apr 12pm, case study sent same day — scorecard not yet in DB
#
# VALUES FAILED (4):
#   Rabia Zafar, Zeeshan Ali, Faryal Afridi (2 Apr, host Jawwad),
#   Muhammad Junaid (6 Apr, host Ayesha)
#
# CALLS COMPLETED — SCORECARD PENDING:
#   Ayesha Nadeem — Zero In was 25 Mar. No result in DB after 2 weeks.
#   Mariam Rehman — Zero In booked TODAY 8 Apr 11am. Call happening now.
#
# VALUES PENDING (no call yet):
#   Wasif Mehdi, Shahid Kamal, Fatima Tu Zahra, Rameez Wasif, Daniyah Noor

LEADING = [
    {
        "app_id": 1777, "name": "Rahima Omar", "score": "—",
        "verdict": "DEBRIEF TODAY",
        "debrief": "8 Apr — case study debrief (today)",
        "tagline": "Cleared values. Case study submitted 28 Mar. Debrief is happening today.",
        "signal": (
            "Cleared the values interview and submitted her case study on 28 March, the same day as "
            "Dur E Nayab, Mahnoor Hasan, and Hassan Zafar — the full first case study cohort submitted together. "
            "Debrief is confirmed for today, 8 April. CV score not prominent at screening stage but "
            "values and case study performance are what matter at this point. "
            "The debrief will be the decisive assessment. Panel should come prepared on the submission."
        ),
        "probe": (
            "At debrief: trace her research design choices in the case study — why did she structure it "
            "this way? What would she do differently? "
            "Probe data literacy: what tools did she use? Has she worked with real field data vs. secondary datasets? "
            "Sector understanding: what is her model of how EdTech reaches government school students?"
        ),
    },
    {
        "app_id": 1816, "name": "Dur E Nayab", "score": "—",
        "verdict": "DEBRIEF DONE",
        "debrief": "7 Apr — debrief done yesterday (result pending)",
        "tagline": "Cleared values. Submitted case study 28 Mar. Debrief was yesterday — panel verdict outstanding.",
        "signal": (
            "Cleared values and submitted case study 28 March. Debrief was yesterday (7 April, 10am). "
            "No result has been recorded yet in the system. "
            "Panel decision should be documented and communicated before today's Rahima Omar debrief "
            "so the team has a live comparison point."
        ),
        "probe": (
            "Decision pending from yesterday's debrief — what is the panel's read? "
            "Key question: did she show research design ownership or primarily implementation capability? "
            "Document verdict before Rahima Omar's debrief today."
        ),
    },
    {
        "app_id": 1701, "name": "Mahnoor Hasan", "score": "—",
        "verdict": "DEBRIEF TOMORROW",
        "debrief": "9 Apr, 4pm — confirmed",
        "tagline": "Cleared values. Submitted case study 28 Mar. Debrief confirmed tomorrow at 4pm.",
        "signal": (
            "Cleared values and submitted case study 28 March. Debrief confirmed for tomorrow, 9 April at 4pm. "
            "Third of the four first-batch case study candidates. "
            "Panel should review her submission before the call — compare against Rahima and Dur E Nayab "
            "to maintain consistent assessment standards across the cohort."
        ),
        "probe": (
            "At debrief: research methodology rigour — what analytical approach did she take in the case study? "
            "Has she independently designed a study vs. implemented one? "
            "Policy writing: has she produced a memo or brief for a decision-maker? "
            "Commitment signal: what about this specific role drew her in?"
        ),
    },
    {
        "app_id": 1369, "name": "Hassan Zafar", "score": "—",
        "verdict": "DEBRIEF 10 APR",
        "debrief": "10 Apr, 2pm — confirmed",
        "tagline": "Cleared values. Submitted case study 28 Mar. Debrief Friday at 2pm.",
        "signal": (
            "Cleared values and submitted case study 28 March. Debrief confirmed for Friday, 10 April at 2pm. "
            "Final candidate in the first case study cohort. "
            "By the time his debrief happens, the panel will have completed three prior debriefs — "
            "use the accumulated read to sharpen the questions for him."
        ),
        "probe": (
            "At debrief: what is his strongest analytical contribution in the case study — not just what "
            "he recommended but how he arrived there. "
            "Research independence: has he led a study end-to-end or always supported? "
            "Probe sector depth: what is his understanding of the impact measurement challenge in EdTech?"
        ),
    },
]

DISCUSSION = [
    {
        "app_id": 1558, "name": "Hadiyah Shaheen", "score": "8.4",
        "verdict": "VALUES PASS",
        "debrief": "Case study sent 26 Mar — no submission (13 days)",
        "tagline": "Cleared values. Case study sent 26 March. No submission received after 13 days — needs follow-up today.",
        "signal": (
            "Cleared values in March with a strong scorecard. CV score 8.4. Salary ask PKR 90–100k — within budget. "
            "Case study was issued on 26 March. Today is 8 April — 13 days have passed with no submission. "
            "This is either a withdrawal signal or the candidate needs a deadline reminder. "
            "Recommend a direct follow-up today before closing her slot."
        ),
        "probe": (
            "Follow-up action: send a deadline reminder today. If no response by 10 April, treat as withdrawn. "
            "If she submits: at debrief probe depth of research design experience — was her case study "
            "analytically led or descriptive?"
        ),
    },
    {
        "app_id": 1949, "name": "Maria Malik", "score": "7.8",
        "verdict": "VALUES PASS",
        "debrief": "Case study sent 7 Apr — awaiting submission",
        "tagline": "Cleared values. Case study sent yesterday. Awaiting submission.",
        "signal": (
            "Cleared values. CV score 7.8. Salary ask PKR 70,000 — within budget. "
            "Case study was issued yesterday, 7 April. Submission is pending. "
            "CV alignment with the JD's research and impact requirements needs review at case study stage — "
            "score reflects acceptable but not standout fit. The case study will be the real test."
        ),
        "probe": (
            "At debrief: trace her most recent end-to-end research project — from question formulation to "
            "final output. What did she produce and for whom? "
            "Probe analytical rigour: what statistical methods does she use independently vs. with support?"
        ),
    },
    {
        "app_id": 1534, "name": "Nain Tara", "score": "8.6",
        "verdict": "VALUES PASS",
        "debrief": "Case study sent",
        "tagline": "Cleared values 6 Apr. Highest CV score among values-cleared candidates. Case study issued.",
        "signal": (
            "Cleared values on 6 April (host: Ayat Butt). CV score 8.6 — highest among values-cleared candidates. "
            "Salary ask PKR 55,000 — significantly below the budget floor of 150k. "
            "Case study has been sent. Verify salary expectations before the debrief conversation begins — "
            "confirm she understands the role is full-time, Lahore-based, and the budget range."
        ),
        "probe": (
            "At debrief: verify salary expectations first. "
            "Probe experience with primary data collection at scale — has she designed surveys herself or "
            "only assisted? What is her strongest quantitative tool and when did she use it in a live project?"
        ),
    },
    {
        "app_id": 1550, "name": "Ali Muhammad", "score": "8.9",
        "verdict": "VALUES PASS*",
        "debrief": "Zero In 7 Apr + case study sent same day — scorecard pending",
        "tagline": "Zero In was yesterday. Case study sent same day. Values result not yet recorded in system.",
        "signal": (
            "Zero In call was yesterday, 7 April at 12pm. Case study was issued the same day — "
            "which means he cleared values on the spot. CV score 8.9 — second-highest in the full pipeline. "
            "Salary ask PKR 120,000 — within budget. "
            "Values scorecard has not yet been recorded in Markaz — this should be logged before his case study "
            "submission arrives. Strong profile; if values were clean, he is likely the strongest remaining candidate."
        ),
        "probe": (
            "Immediate: record the values scorecard in Markaz. "
            "At debrief: probe research outputs — has he produced a deliverable independently? "
            "Probe 'Wants It': why this role specifically, and why now?"
        ),
    },
    {
        "app_id": 1878, "name": "Rameez Wasif", "score": "8.0",
        "verdict": "VALUES PASS",
        "debrief": "Case study not yet sent",
        "tagline": "Cleared values 26 Mar (host: Jawwad). Within budget at 130k. Case study not yet issued.",
        "signal": (
            "Cleared values on 26 March, host Jawwad Ali. CV score 8.0. Salary ask PKR 130,000 — within budget. "
            "Case study has not yet been sent to him. He is ahead of Nain Tara in the values timeline but "
            "has not yet been moved forward. Recommend issuing his case study alongside the others."
        ),
        "probe": (
            "At debrief: research methodology depth — has he led a study end-to-end or implemented others' designs? "
            "What is his strongest analytical output to date?"
        ),
    },
    {
        "app_id": 1771, "name": "Wasif Mehdi", "score": "9.1",
        "verdict": "PENDING VALUES",
        "debrief": "Values interview not yet scheduled",
        "tagline": "Highest CV score in the pending group at 9.1. No Zero In call booked yet.",
        "signal": (
            "CV score 9.1 — highest among pending candidates and among the highest in the full cohort. "
            "Salary ask PKR 100,000 — within budget. "
            "Values interview has not been scheduled. Given his score, he should be prioritised in the values queue."
        ),
        "probe": (
            "Book his Zero In slot as a priority. "
            "At values: probe genuine motivation — sector commitment vs. credential step. "
            "Watch for 'Wants It' signal specifically."
        ),
    },
]

# Case study debrief schedule
DEBRIEF_SCHEDULE = [
    ("Dur E Nayab",   "7 Apr (yesterday)", "Done — result pending",  "Debrief completed 7 Apr 10am. Panel verdict not yet recorded."),
    ("Rahima Omar",   "8 Apr (today)",      "Confirmed",              "Case study debrief — today. Panel: confirm time with attendees."),
    ("Mahnoor Hasan", "9 Apr, 4pm",         "Confirmed",              "Case study debrief — tomorrow at 4pm."),
    ("Hassan Zafar",  "10 Apr, 2pm",        "Confirmed",              "Case study debrief — Friday at 2pm."),
]

# Also in pipeline
PIPELINE = [
    {"name": "Ayesha Nadeem",   "status": "Zero In was 25 Mar — scorecard NOT yet recorded (2 weeks overdue). Follow up immediately."},
    {"name": "Mariam Rehman",   "status": "Zero In booked today (8 Apr, 11am) — call in progress. CV score 8.5 · PKR 120,000"},
    {"name": "Wasif Mehdi",     "status": "Values interview not yet scheduled · CV score 9.1 · PKR 100,000"},
    {"name": "Shahid Kamal",    "status": "Values interview not yet scheduled · CV score 8.6 · PKR 150,000"},
    {"name": "Fatima Tu Zahra", "status": "Values interview not yet scheduled · CV score 8.3 · PKR 70–80k"},
    {"name": "Daniyah Noor",    "status": "Values interview not yet scheduled · CV score 7.5 · PKR 120,000"},
    {"name": "Rabia Zafar",     "status": "VALUES FAILED — OUT · CV score 9.4 (highest in cohort) · 24 Mar"},
    {"name": "Zeeshan Ali",     "status": "VALUES FAILED — OUT · CV score 9.0 · 24 Mar"},
    {"name": "Faryal Afridi",   "status": "VALUES FAILED — OUT · CV score 9.5 · Host: Jawwad · 2 Apr"},
    {"name": "Muhammad Junaid", "status": "VALUES FAILED — OUT · Host: Ayesha · 6 Apr"},
]

CV_APP_IDS = {
    1534: "Nain Tara",
    1558: "Hadiyah Shaheen",
    1949: "Maria Malik",
    1771: "Wasif Mehdi",
    1550: "Ali Muhammad",
}

PIPELINE_NAMES = [
    "Shahid Kamal", "Mariam Rehman", "Fatima Tu Zahra",
    "Rameez Wasif", "Daniyah Noor", "Ayesha Nadeem",
    "Rabia Zafar", "Zeeshan Ali", "Faryal Afridi",
    "Rahima Omar", "Dur E Nayab", "Mahnoor Hasan", "Hassan Zafar",
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
        WHERE a.job_id = 35
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
        meta  = {"name": f"{name} — CV (Job 35 Junior Research Associate, Impact & Policy).pdf"}
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

    # stat boxes
    stat_boxes = """
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0;">
      <tr>
        <td style="padding:14px 8px;background:#f3e5f5;border-radius:6px;text-align:center;width:18%">
          <div style="font-size:22px;font-weight:bold;color:#6a1b9a;">291</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">Total applied</div>
        </td>
        <td width="6"></td>
        <td style="padding:14px 8px;background:#e8f5e9;border-radius:6px;text-align:center;width:18%">
          <div style="font-size:22px;font-weight:bold;color:#1a7a4a;">9</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">Values cleared</div>
        </td>
        <td width="6"></td>
        <td style="padding:14px 8px;background:#e3f0fb;border-radius:6px;text-align:center;width:18%">
          <div style="font-size:22px;font-weight:bold;color:#1565c0;">4</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">Case study submitted</div>
        </td>
        <td width="6"></td>
        <td style="padding:14px 8px;background:#fff8e1;border-radius:6px;text-align:center;width:18%">
          <div style="font-size:22px;font-weight:bold;color:#e65100;">4</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">Debriefs this week</div>
        </td>
        <td width="6"></td>
        <td style="padding:14px 8px;background:#fce4ec;border-radius:6px;text-align:center;width:18%">
          <div style="font-size:22px;font-weight:bold;color:#c62828;">4</div>
          <div style="font-size:11px;color:#555;margin-top:3px;">Values failed — OUT</div>
        </td>
      </tr>
    </table>"""

    where_we_are = """
    <p style="margin:0 0 10px;font-size:13px;line-height:1.7;color:#1a1a1a;">
      291 candidates applied for the Junior Research Associate role. Nine have cleared values.
      The first cohort of four — Rahima Omar, Dur E Nayab, Mahnoor Hasan, and Hassan Zafar — cleared values,
      submitted their case studies on 28 March, and are in the debrief stage this week.
      Dur E Nayab's debrief was yesterday (7 Apr) — panel verdict pending.
      Rahima Omar's is today (8 Apr). Mahnoor Hasan tomorrow (9 Apr, 4pm). Hassan Zafar on Friday (10 Apr, 2pm).
      Four candidates have failed values and are out: Rabia Zafar, Zeeshan Ali, Faryal Afridi, and Muhammad Junaid.
      Hadiyah Shaheen cleared values but has not submitted her case study in 13 days — follow-up needed today.
      Maria Malik and Nain Tara have received their case studies.
      Rameez Wasif cleared values on 26 March — case study not yet issued to him.
      Ali Muhammad had his Zero In call yesterday (7 Apr) and received the case study the same day —
      values scorecard not yet recorded in Markaz.
      Mariam Rehman's Zero In call is today (8 Apr, 11am).
      Ayesha Nadeem's call was 25 March — no scorecard recorded in two weeks.
    </p>"""

    # debrief schedule
    sched_html = """
    <table width="100%" cellpadding="8" cellspacing="0"
           style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
      <tr style="background:#e8f0fb;">
        <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;width:28%">Candidate</td>
        <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;width:18%">Date</td>
        <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;width:16%">Status</td>
        <td style="color:#1565c0;font-weight:bold;border:1px solid #ddd;">Notes</td>
      </tr>"""
    row_bgs = ["#ede7f6", "#fff3e0", "#f1f8e9", "#f1f8e9"]
    for (cname, date, status, notes), bg in zip(DEBRIEF_SCHEDULE, row_bgs):
        sched_html += f"""
      <tr style="background:{bg};">
        <td style="border:1px solid #ddd;">{cv_link(cname)}</td>
        <td style="border:1px solid #ddd;">{date}</td>
        <td style="border:1px solid #ddd;">{status}</td>
        <td style="border:1px solid #ddd;">{notes}</td>
      </tr>"""
    sched_html += "\n    </table>"

    def verdict_color(v):
        return {
            "VALUES PASS": "#1a7a4a",
            "PENDING VALUES": "#e65100",
            "GWC DONE": "#6a1b9a",
        }.get(v, "#636e72")

    def leading_block(c):
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
          <td style="text-align:right;width:160px;font-size:12px;color:#636e72;font-style:italic;">{c["debrief"]}</td>
        </tr>
      </table>
      <p style="margin:8px 0 4px;font-size:12px;color:#636e72;font-style:italic;">{c["tagline"]}</p>
      <p style="margin:0 0 8px;font-size:13px;line-height:1.6;">{c["signal"]}</p>
      <p style="margin:0;font-size:12px;color:#7b341e;line-height:1.6;">
        <b>At debrief, probe:</b> {c["probe"]}
      </p>
    </div>"""

    leading_html = "".join(leading_block(c) for c in LEADING)
    discussion_html = "".join(leading_block(c) for c in DISCUSSION)

    # pipeline table
    pip_rows_html = ""
    for i, p in enumerate(PIPELINE):
        bg = "#f7f9fc" if i % 2 == 0 else "#ffffff"
        pip_rows_html += f"""
      <tr style="background:{bg};">
        <td style="border:1px solid #dfe6e9;padding:8px 10px;font-weight:bold;width:32%;">{cv_link(p["name"])}</td>
        <td style="border:1px solid #dfe6e9;padding:8px 10px;font-size:13px;">{p["status"]}</td>
      </tr>"""

    pipeline_html = f"""
    <table width="100%" cellpadding="0" cellspacing="0"
           style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
      <tr style="background:#e8f0fb;">
        <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;width:32%">Candidate</td>
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
        Junior Research Associate, Impact &amp; Policy
      </p>
    </td>
  </tr>

  <!-- BODY -->
  <tr>
    <td style="padding:28px 32px;">

      <p style="margin:0 0 4px;">Hi Ayesha,</p>
      <p style="margin:0 0 16px;font-size:13px;color:#444;line-height:1.6;">
        Here is the hiring decision brief for
        <strong>Junior Research Associate, Impact &amp; Policy</strong>.
        Pipeline state as of {DATE}. Values stage in progress — no offers out yet.
      </p>

      {stat_boxes}

      {sec("Where We Are")}
      {where_we_are}

      {sec("Debrief Schedule — Case Study This Week")}
      {sched_html}

      {sec("Case Study Stage — Debriefs This Week")}
      <p style="margin:0 0 12px;font-size:13px;color:#444;line-height:1.6;">
        Four candidates cleared values, submitted case studies (28 Mar), and are in debrief this week.
        Names are hyperlinked — click to open their CV.
      </p>
      {leading_html}

      {sec("Also Values-Cleared — Case Study Pending")}
      <p style="margin:0 0 12px;font-size:13px;color:#444;line-height:1.6;">
        These candidates have cleared values but are not yet in the debrief stage. Action items noted per candidate.
      </p>
      {discussion_html}

      {sec("Also in Pipeline")}
      <p style="margin:0 0 12px;font-size:13px;color:#444;line-height:1.6;">
        Remaining pipeline — values pending and values-failed candidates.
        Names are hyperlinked where CVs are available.
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
    msg["Subject"] = f"[PILOT] Final Candidates & Decision View — Junior Research Associate, Impact & Policy"
    msg["From"]    = EMAIL_USER
    msg["To"]      = PILOT_TO
    msg["CC"]      = PILOT_CC
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    recipients = [PILOT_TO, PILOT_CC]
    allow_candidate_addresses(recipients)
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo(); s.starttls(); s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(),
                      context="job35_decision_brief_v2_pilot")
    print(f"Sent to {PILOT_TO} (CC: {PILOT_CC})")


if __name__ == "__main__":
    main()
