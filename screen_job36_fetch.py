"""
Job 36 — Field Coordinator, Research & Impact Studies
Phase 1: Fetch all CVs from Neon DB, extract text, keyword-score, output ranked shortlist.
"""

import base64, io, re, sys, json
from collections import defaultdict

import psycopg2
import PyPDF2
import fitz          # pymupdf
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ── DB connection ──────────────────────────────────────────────────
DB = {
    "host":     "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname":   "neondb",
    "user":     "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode":  "require",
}

# ── JD keyword banks ───────────────────────────────────────────────
KW_FIELD_ME = [
    "field research","field work","field coordinator","field officer","field supervisor",
    "m&e","monitoring and evaluation","monitoring & evaluation","monitoring evaluation",
    "data collection","survey","baseline","endline","midline","enumerator","enumeration",
    "aser","egra","egma","learning assessment","assessment tool","household survey",
    "field visit","field supervision","field team",
]
KW_SURVEY_TOOLS = [
    "odk","kobo","kobocollect","kobotoolbox","surveycto","capi","cati","limesurvey",
    "sampling","sampling plan","sample size","stratified","cluster sampling",
    "data quality","data cleaning","data validation","data entry","quality check",
    "spot check","back-check","geotagging","gps tracking",
]
KW_EDUCATION = [
    "school","education","teacher","student","classroom","curriculum","tcf","cerp",
    "teach for pakistan","read foundation","akesp","aga khan","sabaq","tele-taleem",
    "ministry of education","moefpt","provincial education","district education",
    "government school","public school","primary school","secondary school",
    "snc","nemis","emis","Punjab education","sindh education","kp education",
    "ipp","independent power","learning outcomes","numeracy","literacy",
    "education ngo","education program","education project","school visits",
]
KW_RESEARCH = [
    "rct","randomized","quasi-experimental","impact evaluation","research",
    "j-pal","ipa","ieri","3ie","oxford policy","pid","policy","evidence",
    "research assistant","research officer","research associate",
    "quantitative research","qualitative research","mixed methods",
]
KW_GOVT = [
    "government","coordination","stakeholder","ministry","department",
    "district coordination","deo","ddeo","provincial","federal","ngo coordination",
    "government liaison","government relations","public sector",
]
KW_DATA_SKILLS = [
    "excel","spss","stata","r software","python","power bi","tableau","nvivo",
    "data analysis","statistics","statistical","regression","frequency analysis",
    "pivot table","vlookup","dashboard","reporting",
]
KW_ORG_SIGNAL = [
    "tcf","cerp","teach for pakistan","world bank","unicef","undp","usaid",
    "fcdo","dfid","british council","aga khan","akesp","3ie","j-pal","ipa",
    "ifpri","oxfam","save the children","care pakistan","plan international",
    "irc","action against hunger","idp","mercy corps","adb","ukaid",
    "pakistan reading project","prp","wfp","who","unfpa",
]

def kw_score(text, kw_list):
    t = text.lower()
    hits = sum(1 for kw in kw_list if kw in t)
    return min(hits, len(kw_list))  # cap at list length

def extract_text_pypdf(pdf_bytes):
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = " ".join(p.extract_text() or "" for p in reader.pages)
        return text.strip()
    except:
        return ""

def extract_text_ocr(pdf_bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        texts = []
        for page in doc:
            mat = fitz.Matrix(2, 2)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            texts.append(pytesseract.image_to_string(img))
        return " ".join(texts).strip()
    except:
        return ""

def extract_cv(b64_data):
    try:
        raw = base64.b64decode(b64_data)
    except:
        return "", False
    text = extract_text_pypdf(raw)
    ocr = False
    if len(text) < 100:
        text = extract_text_ocr(raw)
        ocr = True
    return text, ocr

def detect_years_exp(text):
    """Rough heuristic: find year ranges like 2020-2023."""
    t = text.lower()
    # Count year-pairs indicating job tenures
    years = re.findall(r'\b(20\d\d)\b', t)
    if len(years) < 2:
        return None
    years = sorted(set(int(y) for y in years))
    span = years[-1] - years[0]
    return span

def location_score(loc):
    if not loc:
        return 0
    loc = loc.lower()
    if "islamabad" in loc or "rawalpindi" in loc or "isb" in loc or "rwp" in loc:
        return 2   # ideal
    if "punjab" in loc and ("lahore" not in loc):
        return 1   # close, could commute
    return 0       # needs relocation

# ── Fetch applications ─────────────────────────────────────────────
print("Connecting to DB...", flush=True)
conn = psycopg2.connect(**DB)
cur  = conn.cursor()

cur.execute("""
    SELECT DISTINCT ON (c.id)
        a.id as app_id, a.candidate_id,
        c.first_name, c.last_name, c.location,
        c.current_position, c.current_company,
        c.experience, c.education, c.resume_data,
        LENGTH(c.resume_data) as resume_size
    FROM applications a
    JOIN candidates c ON a.candidate_id = c.id
    WHERE a.job_id = 36
      AND c.resume_data IS NOT NULL
      AND LENGTH(c.resume_data) > 5000
    ORDER BY c.id, a.id
""")
rows = cur.fetchall()
cols = [d[0] for d in cur.description]
conn.close()
print(f"Fetched {len(rows)} unique candidates with resumes.", flush=True)

# ── Score each candidate ───────────────────────────────────────────
results = []
for i, row in enumerate(rows):
    r = dict(zip(cols, row))
    name = f"{r['first_name']} {r['last_name']}".strip()
    sys.stdout.write(f"\r[{i+1}/{len(rows)}] {name[:40]:<40}")
    sys.stdout.flush()

    cv_text, ocr = extract_cv(r['resume_data'])
    if len(cv_text) < 80:
        cv_text = f"{r.get('experience','')} {r.get('education','')}"

    # Scores per category
    s_field = kw_score(cv_text, KW_FIELD_ME)
    s_tools = kw_score(cv_text, KW_SURVEY_TOOLS)
    s_edu   = kw_score(cv_text, KW_EDUCATION)
    s_res   = kw_score(cv_text, KW_RESEARCH)
    s_govt  = kw_score(cv_text, KW_GOVT)
    s_data  = kw_score(cv_text, KW_DATA_SKILLS)
    s_org   = kw_score(cv_text, KW_ORG_SIGNAL)
    s_loc   = location_score(r['location'])

    # Weighted total (max ~100)
    total = (
        s_field * 4.0 +   # most important
        s_tools * 3.0 +
        s_edu   * 2.5 +
        s_res   * 2.0 +
        s_govt  * 1.5 +
        s_data  * 1.5 +
        s_org   * 1.0 +
        s_loc   * 5.0     # location is a strong filter
    )

    exp_span = detect_years_exp(cv_text)

    # Save 1000 chars of CV text for manual review
    snippet = cv_text[:1200].replace('\n', ' ').strip()

    results.append({
        "app_id":       r['app_id'],
        "cand_id":      r['candidate_id'],
        "name":         name,
        "location":     r['location'] or "",
        "current_role": r['current_position'] or "",
        "current_co":   r['current_company'] or "",
        "education":    (r['education'] or "")[:120],
        "ocr":          ocr,
        "resume_bytes": r['resume_size'],
        "s_field":      s_field,
        "s_tools":      s_tools,
        "s_edu":        s_edu,
        "s_res":        s_res,
        "s_govt":       s_govt,
        "s_data":       s_data,
        "s_org":        s_org,
        "s_loc":        s_loc,
        "exp_span":     exp_span,
        "total":        round(total, 1),
        "snippet":      snippet,
    })

print("\nDone scoring.", flush=True)

# Sort by total descending
results.sort(key=lambda x: -x['total'])

# Save full results
with open("job36_prescreened.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# Print top 50
print(f"\n{'#':<4} {'Name':<32} {'Loc':<20} {'Score':>6}  {'Fld':>3} {'Tls':>3} {'Edu':>3} {'Res':>3} {'Dat':>3} {'Org':>3}  {'Current Role':<35}")
print("-"*160)
for i, r in enumerate(results[:50]):
    loc_short = r['location'][:18]
    role_short = r['current_role'][:33]
    print(f"{i+1:<4} {r['name']:<32} {loc_short:<20} {r['total']:>6.1f}  {r['s_field']:>3} {r['s_tools']:>3} {r['s_edu']:>3} {r['s_res']:>3} {r['s_data']:>3} {r['s_org']:>3}  {role_short:<35}")

print(f"\nFull results saved to job36_prescreened.json")
