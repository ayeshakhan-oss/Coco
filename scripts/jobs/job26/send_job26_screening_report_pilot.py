"""
Job 26 — Soul Architect / Conversational UX Designer
Initial Screening Report — PILOT (Ayesha only)
"""

import os, sys, smtplib, base64, re
sys.path.insert(0, "c:/Agent Coco")
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
import psycopg2
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build as gdrive_build
from googleapiclient.http import MediaFileUpload

load_dotenv(dotenv_path="c:/Agent Coco/.env")

EMAIL_HOST     = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT     = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

PILOT_TO  = "ayesha.khan@taleemabad.com"
LIVE_TO   = "waqas.tanveer@taleemabad.com"
LIVE_CC   = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]
CV_DIR   = "c:/Agent Coco/output/cvs_job26/"
os.makedirs(CV_DIR, exist_ok=True)

# All app_ids we want CVs for (shortlist + maybe + PM flags, deduped)
CV_APP_IDS = [1315, 1318, 1316, 1311, 1313, 1294, 1301, 1320, 1322, 974, 980, 1044, 1287]

# ── CV FETCH + DRIVE UPLOAD ────────────────────────────────────────────────────

def safe_fn(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)

def fetch_and_upload_cvs():
    print("Fetching CVs from DB...")
    conn = psycopg2.connect(
        host="ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
        dbname="neondb", user="neondb_owner",
        password="npg_kBQ10OASHEmd", sslmode="require"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, c.first_name || ' ' || c.last_name, c.resume_data
        FROM applications a JOIN candidates c ON a.candidate_id = c.id
        WHERE a.id = ANY(%s) AND c.resume_data IS NOT NULL
    """, (CV_APP_IDS,))
    rows = cur.fetchall()
    cur.close(); conn.close()

    cv_paths = {}
    for app_id, name, b64 in rows:
        path = os.path.join(CV_DIR, f"{app_id}_{safe_fn(name)}.pdf")
        try:
            with open(path, "wb") as f:
                f.write(base64.b64decode(b64))
            cv_paths[name] = path
        except Exception as e:
            print(f"  FAILED {name}: {e}")

    print(f"Fetched {len(cv_paths)} CVs. Uploading to Drive...")
    creds = Credentials.from_authorized_user_file(
        "c:/Agent Coco/token_drive.json",
        scopes=["https://www.googleapis.com/auth/drive.file"])
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    service = gdrive_build("drive", "v3", credentials=creds)

    drive_links = {}
    for name, path in cv_paths.items():
        meta  = {"name": f"{name} — CV (Job 26 Soul Architect).pdf"}
        media = MediaFileUpload(path, mimetype="application/pdf")
        f     = service.files().create(body=meta, media_body=media, fields="id").execute()
        fid   = f["id"]
        service.permissions().create(fileId=fid, body={"type": "anyone", "role": "reader"}).execute()
        drive_links[name] = f"https://drive.google.com/file/d/{fid}/view"
        print(f"  Uploaded: {name}")
    return drive_links


# ── DATA ───────────────────────────────────────────────────────────────────────

SHORTLIST = [
    {
        "app_id": 1315, "name": "Danyal Haroon", "match": "78%",
        "total_exp": "~4 yrs", "relevant_exp": "~4 yrs", "salary": "Not mentioned",
        "db_status": "shortlisted",
        "verdict": "#1 — TOP PICK",
        "verdict_color": "#c62828",
        "flag": None,
        "strength": (
            "Most complete profile across all dimensions the role requires day-to-day. "
            "MA Digital Media, Culture & Society — University of Manchester (dissertation: 'Evolution and "
            "Impact of AI Chatbot Interfaces'). BSc Computer Science — LUMS (Dean's Honours). "
            "UX Design Specialist at AIO App Inc. (AI restaurant platform, $1M funding); Product Design "
            "Expert at HBL Konnect (1M+ users, qualitative focus groups across 18 Pakistani cities). "
            "Non-Violent Communication trained. Uses Gemini deep research, Claude, Figma AI daily. "
            "He can iterate on Rumi's soul document, write and test prompts, and push changes "
            "without needing an engineer in the room — while also bringing the humanistic depth "
            "the role demands. The 18-city HBL focus groups are real ethnographic research at scale, "
            "not just product interviews. Application essay on xAI Ani chatbot is ethically grounded "
            "and references real AI companion literature."
        ),
        "gap": "Still completing MA (graduating 2025). Limited direct conversation/dialogue design implementation experience.",
    },
    {
        "app_id": 1318, "name": "Hulalah Khan", "match": "82%",
        "total_exp": "~3 yrs", "relevant_exp": "~3 yrs", "salary": "Not mentioned",
        "db_status": "rejected",
        "verdict": "#2 — TOP PICK",
        "verdict_color": "#c62828",
        "flag": "⚠️ Currently marked REJECTED in DB — needs re-evaluation",
        "strength": (
            "Deepest human science background in the entire pool of 42. "
            "LUMS BSc Sociology-Anthropology + Minor Psychology (CGPA 3.5, Dean's Honours 3 years). "
            "Qualitative research methods training; counselling psychology coursework; 300+ students "
            "psychosocial support at Orange Tree Foundation; Project Yaqeen listening sessions (10+); "
            "TCF curriculum development. Application answer — about the 'confessional without a face,' "
            "the ethics of non-human empathy, and user autonomy — is the most philosophically rigorous "
            "response in the pool. Ranked #2 over #1 solely because of the implementation gap: "
            "she has never worked with an AI tool, written a prompt, or shipped in a tech product. "
            "If Rumi has dedicated engineering support and this person's role is purely to define the soul, "
            "she becomes the stronger call. If the role requires semi-autonomous iteration, Danyal is."
        ),
        "gap": "Zero AI tool fluency and zero implementation experience. Needs engineering support to make changes to Rumi independently.",
    },
    {
        "app_id": 1316, "name": "Hamza Jamal", "match": "55%",
        "total_exp": "~6 yrs", "relevant_exp": "~2 yrs", "salary": "Not mentioned",
        "db_status": "rejected",
        "verdict": "SHORTLIST",
        "verdict_color": "#1565c0",
        "flag": "⚠️ Currently marked REJECTED in DB — needs re-evaluation",
        "strength": (
            "Sr. UX/UI Designer at Carbonteq — explicitly designed 'B2C experiences using AI-driven "
            "interactions' and 'conversational interfaces.' 5 years at Arbisoft (usability testing, "
            "affinity maps, journey mapping). IBM Enterprise Design Thinking Practitioner. "
            "'Designing Emotion' LinkedIn certification. Application answer: 'humans project soul onto "
            "anything that responds to us' — with the specific observation about a teacher apologising "
            "to a chatbot after a typo. Understands cultural deference dynamics (Pakistan Ustad hierarchy). "
            "If implementation speed is a priority, Hamza can start building immediately."
        ),
        "gap": "No formal behavioral/social science background. Conversational interface work is recent (current role only).",
    },
    {
        "app_id": 1311, "name": "Ghulam Qadir", "match": "52%",
        "total_exp": "~8 yrs", "relevant_exp": "~2 yrs", "salary": "Not mentioned",
        "db_status": "rejected",
        "verdict": "SHORTLIST",
        "verdict_color": "#1565c0",
        "flag": "⚠️ Currently marked REJECTED in DB — needs re-evaluation",
        "strength": (
            "Designed Chatwards AI end-to-end: chatbot dashboard, competitive research, user interviews, "
            "design system, conversational onboarding flows. EdTech at Chaajao (conversational onboarding, "
            "engagement systems). 8 years total. Application: 'people assign intent to buttons, tone to "
            "error messages, even character to loading states' — most precise UX-grounded articulation "
            "of AI personality design in the pool. Solo implementation capable (Lovable, Figma)."
        ),
        "gap": "No behavioral science or humanities background. Chatbot work is UI/dashboard, not soul/dialogue design.",
    },
    {
        "app_id": 1313, "name": "Aaqib Khan", "match": "42%",
        "total_exp": "~7 yrs", "relevant_exp": "~1.5 yrs", "salary": "Not mentioned",
        "db_status": "gwc_scheduled",
        "verdict": "SHORTLIST",
        "verdict_color": "#1565c0",
        "flag": None,
        "strength": (
            "7 years across AI-powered products (Artsify, Digital Identity, AI study tools). "
            "Application specifically frames conversational UX around trust and emotional design "
            "without pretending AI is human. Thoughtful on the ethics of non-human identity. "
            "Already in GWC stage in DB."
        ),
        "gap": "No behavioral science background. Primarily a visual product designer. Less philosophically deep than top picks.",
    },
]

MAYBE = [
    {"app_id": 1294, "name": "Asad Nawaz",         "match": "28%", "note": "Best AI product design exp (Vyro 100M users, Qlu AI tools). Declined to answer the core application question — significant concern for a role requiring philosophical engagement."},
    {"app_id": 1301, "name": "Manahil Ahmed",       "match": "35%", "note": "Strong application writing (references The Little Prince); NUST; data analysis skills. No behavioral science or dialogue design."},
    {"app_id": 1320, "name": "Nain Tara",           "match": "18%", "note": "MSc Sociology (underemphasised); designed AI chatbot UI at Applab Qatar. Sociology background relevant but no qualitative research shown."},
    {"app_id": 1322, "name": "Rimsha Faisal",       "match": "40%", "note": "AI-driven interfaces specialist; uses Claude as design co-pilot daily; AIO AI platform. No philosophical depth in application."},
    {"app_id": 974,  "name": "Muhammad Ammar Khan", "match": "45%", "note": "Strong written application; culturally aware; AI tools exposure. Student-level CV with no professional relevant experience."},
    {"app_id": 980,  "name": "Aisha Bashir",        "match": "38%", "note": "Taleemabad alumna; creative background; thoughtful application. Primarily illustrator — no conversational UX or behavioral science."},
]

PM_FLAGS = [
    {"app_id": 1294, "name": "Asad Nawaz",        "note": "PM-level scope at Qlu.ai — team scaling (1 to 6), GTM planning, $5M deal contribution. Designer title, PM function. Closest to actual PM work."},
    {"app_id": 1044, "name": "Ameer Hamza Tariq", "note": "Listed 'Product Owner & Designer' on two projects (Tazah, PreventScripts). Combined PO + design lead role."},
    {"app_id": 1287, "name": "Muhammad Jaffer",   "note": "Lists Product Management, Roadmapping, Stakeholder Management in skills. Functions as a UI/UX designer at Neem — PM-adjacent."},
    {"app_id": 1313, "name": "Aaqib Khan",         "note": "Product Development Lifecycle + Agile + Team Leadership listed. Designer title throughout."},
    {"app_id": 1311, "name": "Ghulam Qadir",       "note": "Led discovery, A/B experiments, product direction across 4+ products — PM scope in all but title."},
]


# ── BUILD HTML ─────────────────────────────────────────────────────────────────

def build_html(drive_links=None):

    def cv_link(name):
        url = (drive_links or {}).get(name)
        if url:
            return f'<a href="{url}" style="color:#1565c0;font-weight:bold;">{name}</a>'
        return f'<b>{name}</b>'

    def sec(title):
        return (f'<p style="margin:28px 0 8px;font-size:15px;font-weight:bold;color:#1565c0;'
                f'border-bottom:2px solid #1565c0;padding-bottom:5px;">{title}</p>')

    def candidate_block(c, i):
        flag_html = ""
        if c.get("flag"):
            flag_html = (f'<p style="margin:6px 0 0;font-size:12px;color:#c62828;'
                         f'font-weight:bold;">{c["flag"]}</p>')
        db_color = "#c62828" if c["db_status"] == "rejected" else "#1a7a4a" if c["db_status"] == "shortlisted" else "#6a1b9a"
        return f"""
    <div style="background:#f7f9fc;border-left:4px solid {c['verdict_color']};
                padding:14px 16px;margin-bottom:16px;border-radius:0 6px 6px 0;">
      <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:6px;">
        <tr>
          <td style="font-size:14px;font-weight:bold;color:#1a1a1a;">
            {i}. {cv_link(c['name'])}
          </td>
          <td style="text-align:center;width:80px;">
            <span style="color:{c['verdict_color']};font-weight:bold;font-size:12px;">{c['verdict']}</span>
          </td>
          <td style="text-align:right;width:70px;">
            <span style="font-size:13px;font-weight:bold;color:#1565c0;">{c['match']}</span>
          </td>
        </tr>
      </table>
      <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:8px;">
        <tr>
          <td style="font-size:11px;color:#636e72;">App ID: {c['app_id']}</td>
          <td style="font-size:11px;color:#636e72;">Total exp: {c['total_exp']}</td>
          <td style="font-size:11px;color:#636e72;">Relevant exp: {c['relevant_exp']}</td>
          <td style="font-size:11px;color:{db_color};font-weight:bold;">DB status: {c['db_status']}</td>
        </tr>
      </table>
      <p style="margin:0 0 6px;font-size:13px;line-height:1.7;color:#1a1a1a;">{c['strength']}</p>
      <p style="margin:0;font-size:12px;color:#7b341e;line-height:1.6;">
        <b>Gap:</b> {c['gap']}
      </p>
      {flag_html}
    </div>"""

    shortlist_blocks = "".join(candidate_block(c, i+1) for i, c in enumerate(SHORTLIST))

    maybe_rows = "".join(f"""
      <tr style="background:{'#f7f9fc' if i%2==0 else '#fff'};">
        <td style="border:1px solid #dfe6e9;padding:8px 10px;font-size:13px;width:25%;">{cv_link(c['name'])}</td>
        <td style="border:1px solid #dfe6e9;padding:8px 10px;text-align:center;font-size:13px;width:10%;">{c['match']}</td>
        <td style="border:1px solid #dfe6e9;padding:8px 10px;font-size:12px;line-height:1.6;">{c['note']}</td>
      </tr>""" for i, c in enumerate(MAYBE))

    pm_rows = "".join(f"""
      <tr style="background:{'#f7f9fc' if i%2==0 else '#fff'};">
        <td style="border:1px solid #dfe6e9;padding:8px 10px;font-size:13px;width:25%;">{cv_link(c['name'])}</td>
        <td style="border:1px solid #dfe6e9;padding:8px 10px;text-align:center;font-size:12px;color:#636e72;width:10%;">{c['app_id']}</td>
        <td style="border:1px solid #dfe6e9;padding:8px 10px;font-size:12px;line-height:1.6;">{c['note']}</td>
      </tr>""" for i, c in enumerate(PM_FLAGS))

    return f"""\
<html>
<body style="font-family:Georgia,serif;font-size:14px;color:#1a1a1a;
             max-width:700px;margin:auto;background:#f0f4f0;padding:24px 0;">
<table width="700" cellpadding="0" cellspacing="0"
       style="background:#ffffff;border-radius:8px;
              box-shadow:0 2px 12px rgba(0,0,0,0.08);overflow:hidden;">

  <!-- HEADER -->
  <tr>
    <td style="background:#1a2a3a;padding:24px 32px;">
      <p style="margin:0;font-size:10px;color:#90a4ae;letter-spacing:2px;
                text-transform:uppercase;font-family:Georgia,serif;">
        People &amp; Culture &middot; Initial Screening Report
      </p>
      <p style="margin:8px 0 2px;font-size:20px;font-weight:bold;
                color:#ffffff;font-family:Georgia,serif;">
        Soul Architect / Conversational UX Designer
      </p>
      <p style="margin:0;font-size:13px;color:#90caf9;font-family:Georgia,serif;">
        Job 26 &middot; Taleemabad
      </p>
    </td>
  </tr>

  <!-- BODY -->
  <tr>
    <td style="padding:28px 32px;">

      <p style="margin:0 0 16px;">Hi Waqas,</p>

      <!-- STAT BOXES -->
      <table width="100%" cellpadding="0" cellspacing="0" style="margin:16px 0 24px;">
        <tr>
          <td style="padding:14px 8px;background:#fce4ec;border-radius:6px;text-align:center;width:23%">
            <div style="font-size:22px;font-weight:bold;color:#c62828;">42</div>
            <div style="font-size:11px;color:#555;margin-top:3px;">Total applications</div>
          </td>
          <td width="7"></td>
          <td style="padding:14px 8px;background:#e3f0fb;border-radius:6px;text-align:center;width:23%">
            <div style="font-size:22px;font-weight:bold;color:#1565c0;">5</div>
            <div style="font-size:11px;color:#555;margin-top:3px;">Shortlisted</div>
          </td>
          <td width="7"></td>
          <td style="padding:14px 8px;background:#fff8e1;border-radius:6px;text-align:center;width:23%">
            <div style="font-size:22px;font-weight:bold;color:#f57f17;">6</div>
            <div style="font-size:11px;color:#555;margin-top:3px;">Maybe</div>
          </td>
          <td width="7"></td>
          <td style="padding:14px 8px;background:#f5f5f5;border-radius:6px;text-align:center;width:23%">
            <div style="font-size:22px;font-weight:bold;color:#636e72;">30</div>
            <div style="font-size:11px;color:#555;margin-top:3px;">No hire</div>
          </td>
        </tr>
      </table>

      <!-- KEY OBSERVATION -->
      {sec("Key Observation")}
      <p style="margin:0 0 16px;font-size:13px;line-height:1.7;color:#444;">
        35 of 42 applicants are traditional UI/UX designers with screen-based portfolios — this role attracted
        largely the wrong applicant type. Only 2 candidates (Danyal Haroon and Hulalah Khan) have the
        behavioral science and humanistic depth the JD says is non-negotiable. The application questions
        were excellent filters — written responses sorted candidates far more meaningfully than CVs alone.
      </p>

      <!-- SHORTLIST -->
      {sec("Shortlisted Candidates (5)")}
      <p style="margin:0 0 14px;font-size:13px;color:#444;line-height:1.6;">
        All five read and evaluated manually against the JD. Budget not specified for this role.
      </p>
      {shortlist_blocks}

      <!-- MAYBE -->
      {sec("Maybe — Worth a Conversation (7)")}
      <table width="100%" cellpadding="0" cellspacing="0"
             style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
        <tr style="background:#e8f0fb;">
          <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;">Candidate</td>
          <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;text-align:center;">Match</td>
          <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;">Note</td>
        </tr>
        {maybe_rows}
      </table>

      <!-- PM FLAGS -->
      {sec("Product Manager Experience — Flagged (as requested)")}
      <p style="margin:0 0 10px;font-size:13px;color:#444;line-height:1.6;">
        None hold a formal PM title. Asad Nawaz (1294) is the closest to actual PM-level work.
      </p>
      <table width="100%" cellpadding="0" cellspacing="0"
             style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
        <tr style="background:#e8f0fb;">
          <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;">Candidate</td>
          <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;text-align:center;">App ID</td>
          <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;">PM Experience Notes</td>
        </tr>
        {pm_rows}
      </table>

    </td>
  </tr>

  <!-- FOOTER -->
  <tr>
    <td style="padding:12px 32px;background:#f5f5f5;font-size:11px;color:#888;
               font-family:Georgia,serif;">
      Taleemabad Talent Acquisition &nbsp;|&nbsp; hiring@taleemabad.com
      &nbsp;|&nbsp; 6 April 2026
    </td>
  </tr>

</table>
</body>
</html>"""


# ── MAIN ───────────────────────────────────────────────────────────────────────

def main():
    print("Step 1: Fetching CVs and uploading to Drive...")
    drive_links = fetch_and_upload_cvs()
    print(f"Drive links ready: {len(drive_links)}\n")

    print("Step 2: Building screening report HTML...")
    html_body = build_html(drive_links)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Initial Screening — Soul Architect / Conversational UX Designer"
    msg["From"]    = EMAIL_USER
    msg["To"]      = LIVE_TO
    msg["CC"]      = ", ".join(LIVE_CC)
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    recipients = [LIVE_TO] + LIVE_CC
    allow_candidate_addresses(recipients)

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.ehlo(); smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(smtp_server=smtp, sender=EMAIL_USER,
                      recipients=recipients, message=msg.as_string(),
                      context="job26_screening_report_live")
    print(f"Live sent to: {LIVE_TO}")
    print(f"CC: {', '.join(LIVE_CC)}")


if __name__ == "__main__":
    main()
