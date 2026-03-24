"""
Job 36 — Field Coordinator, Research & Impact Studies
Screen all 179 CVs against JD using keyword scoring.
Uses Markaz candidate names (first_name + last_name), not CV-extracted names.
Writes scores to DB and outputs ranked JSON.
"""

import os, sys, json, base64, io, re, time
import psycopg2
from dotenv import load_dotenv

# PDF parsing
import PyPDF2
try:
    import fitz          # pymupdf
    import pytesseract
    from PIL import Image
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

load_dotenv()

DB_HOST = "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech"
DB_NAME = "neondb"
DB_USER = "neondb_owner"
DB_PASS = "npg_kBQ10OASHEmd"
JOB_ID  = 36

# ══════════════════════════════════════════════════════════════════════
# JD KEYWORDS — Field Coordinator, Research & Impact Studies
# ══════════════════════════════════════════════════════════════════════

# 1. Functional Match (25%) — field research, M&E, survey coordination
DIM1_HIGH = [
    "field coordinator", "m&e", "monitoring and evaluation", "monitoring & evaluation",
    "survey management", "enumerator", "data collection", "field research",
    "fieldwork", "field work", "impact evaluation", "baseline", "endline", "midline",
    "field officer", "field supervisor", "data quality", "survey firm",
    "third-party evaluation", "third party evaluation", "spot check", "field governance",
    "sampling plan", "survey protocol", "kobo", "odk", "surveyto", "cto",
]
DIM1_MED = [
    "research coordinator", "program coordinator", "field officer", "data officer",
    "monitoring", "evaluation", "survey", "field", "coordination", "research assistant",
    "field visits", "school visits", "data collection", "research",
]

# 2. Demonstrated Outcomes (20%) — quantified results
DIM2_SIGNALS = [
    r"\d+\s*school", r"\d+\s*enumerator", r"\d+\s*household", r"\d+\s*survey",
    r"\d+\s*data\s*point", r"\d+\s*district", r"\d+\s*visit", r"\d+\s*school",
    r"trained\s*\d+", r"supervised\s*\d+", r"managed\s*\d+\s*(enumerator|staff|team)",
    r"\d+\s*%", r"\d+\s*percent", r"pki\s*\d+", r"pkr\s*\d+",
    r"covered\s*\d+", r"collected\s*\d+",
]

# 3. Environment Fit (15%) — education/NGO/dev sector, Islamabad
DIM3_EDU = [
    "taleemabad", "tcf", "the citizens foundation", "teach for pakistan",
    "read foundation", "sabaq", "unicef", "undp", "usaid", "world bank",
    "fcdo", "dfid", "giz", "aga khan", "akdn", "cerp", "ipa", "j-pal",
    "education", "school", "ngo", "government school", "public school",
    "ministry of education", "mofe", "provincial education",
    "development sector", "social sector", "impact", "policy",
    "islamabad", "rawalpindi", "i-8", "f-8", "g-9",
]
DIM3_MED = [
    "social development", "community", "women", "health", "pakistan",
    "karachi", "lahore", "peshawar", "multan", "quetta",
]

# 4. Ownership & Execution (15%) — led field ops, managed vendors
DIM4_HIGH = [
    "led field", "managed enumerator", "supervised enumerator", "managed survey",
    "coordinated field", "vendor management", "managed third", "survey firm management",
    "field coordination", "independently managed", "project lead",
    "team lead", "managed team", "supervised team", "oversaw",
    "quality assurance", "qa", "quality control", "qc",
]
DIM4_MED = [
    "led", "managed", "coordinated", "supervised", "oversaw", "handled",
    "responsible for", "organized", "planned", "executed",
]

# 5. Stakeholder & Communication (10%) — govt, schools, reporting
DIM5_HIGH = [
    "government coordination", "district coordination", "school coordination",
    "stakeholder management", "government liaison", "district government",
    "mou", "approval", "government approval", "school access",
    "dashboard", "weekly report", "progress report", "status update",
    "communication", "reporting", "documentation", "tracker",
]
DIM5_MED = [
    "presentation", "report", "written communication", "coordination",
    "liaison", "stakeholder", "community mobilization",
]

# 6. Hard Skills (10%) — data tools, M&E tools
DIM6_HIGH = [
    "kobo", "kobotoolbox", "odk", "survey cto", "surveyto",
    "stata", "spss", "r studio", "python", "gis", "arcgis",
    "power bi", "tableau", "salesforce",
]
DIM6_MED = [
    "excel", "google sheets", "microsoft office", "data analysis",
    "sql", "database", "data entry", "data cleaning",
]

# 7. Growth & Leadership (5%)
DIM7_HIGH = [
    "team leader", "field team leader", "senior", "head of", "manager",
    "master", "mphil", "phd", "m.sc", "msc", "m.a.", "post grad",
]
DIM7_MED = [
    "bachelor", "bs", "ba", "bsc", "b.sc", "b.a.", "university",
    "degree", "graduate", "diploma",
]

# Must-haves for Field Coordinator role
MUST_HAVES = [
    # Must-have 1: Field/M&E/research experience
    ["field", "m&e", "monitoring", "evaluation", "survey", "data collection",
     "research", "enumerator", "baseline", "endline"],
    # Must-have 2: Education or development sector
    ["education", "school", "ngo", "unicef", "usaid", "world bank", "development",
     "social", "government", "taleemabad", "tcf", "impact"],
]


# ══════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(str(text).encode('ascii', errors='replace').decode('ascii'))


def parse_pdf(b64_data):
    """Decode base64 PDF, extract text. Falls back to OCR for scanned PDFs."""
    try:
        pdf_bytes = base64.b64decode(b64_data)
    except Exception:
        return ""

    # Try PyPDF2 first
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "")
        if len(text.strip()) > 50:
            return text.lower()
    except Exception:
        pass

    # OCR fallback
    if OCR_AVAILABLE:
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            ocr_text = ""
            for page in doc:
                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                ocr_text += pytesseract.image_to_string(img)
            doc.close()
            return ocr_text.lower()
        except Exception:
            pass

    return ""


def score_dim(text, high_kws, med_kws=None, high_val=4, med_val=2):
    """Score a dimension based on keyword hits."""
    hits_high = sum(1 for kw in high_kws if kw.lower() in text)
    if hits_high >= 3:
        return high_val
    elif hits_high == 2:
        return high_val - 1
    elif hits_high == 1:
        return high_val - 1 if high_val <= 3 else 3
    if med_kws:
        hits_med = sum(1 for kw in med_kws if kw.lower() in text)
        if hits_med >= 3:
            return med_val
        elif hits_med >= 1:
            return max(1, med_val - 1)
    return 0


def score_outcomes(text):
    """Score on quantified outcomes using regex patterns."""
    hits = sum(1 for pat in DIM2_SIGNALS if re.search(pat, text))
    if hits >= 4:
        return 4
    elif hits >= 2:
        return 3
    elif hits >= 1:
        return 2
    return 1


def count_missing_must_haves(text):
    """Count how many must-haves are missing (each = -15% penalty)."""
    missing = 0
    for mh_group in MUST_HAVES:
        if not any(kw.lower() in text for kw in mh_group):
            missing += 1
    return missing


def compute_score(dims, missing_mh):
    """Weighted 7-dimension score, normalized to 100, with must-have penalties."""
    weights = [0.25, 0.20, 0.15, 0.15, 0.10, 0.10, 0.05]
    raw = sum(d * w for d, w in zip(dims, weights))
    normalized = (raw / 4.0) * 100
    # Apply must-have penalty
    penalty = 1.0 - (0.15 * missing_mh)
    return round(normalized * penalty, 1)


# ══════════════════════════════════════════════════════════════════════
# MAIN SCREENING LOOP
# ══════════════════════════════════════════════════════════════════════

def main():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER,
        password=DB_PASS, sslmode='require'
    )
    cur = conn.cursor()

    # Fetch all applications with resumes for job 36
    cur.execute("""
        SELECT
            a.id AS app_id,
            c.id AS candidate_id,
            TRIM(c.first_name || ' ' || c.last_name) AS full_name,
            c.resume_data,
            a.canned_answers->'desiredSalary'->>'answer' AS expected_salary
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = %s
          AND c.resume_data IS NOT NULL
          AND c.resume_data != ''
        ORDER BY a.id ASC
    """, (JOB_ID,))
    rows = cur.fetchall()

    safe_print(f"Found {len(rows)} applications with resumes for Job {JOB_ID}")

    results = []
    errors  = []

    for i, (app_id, cand_id, full_name, resume_b64, salary) in enumerate(rows):
        safe_print(f"[{i+1}/{len(rows)}] Screening: {full_name} (app {app_id})")

        # Parse CV
        cv_text = parse_pdf(resume_b64)
        if len(cv_text.strip()) < 30:
            safe_print(f"  -> Unreadable CV, skipping")
            errors.append({"app_id": app_id, "name": full_name, "reason": "Unreadable CV"})
            continue

        # Score 7 dimensions
        d1 = score_dim(cv_text, DIM1_HIGH, DIM1_MED)
        d2 = score_outcomes(cv_text)
        d3 = score_dim(cv_text, DIM3_EDU, DIM3_MED)
        d4 = score_dim(cv_text, DIM4_HIGH, DIM4_MED)
        d5 = score_dim(cv_text, DIM5_HIGH, DIM5_MED)
        d6 = score_dim(cv_text, DIM6_HIGH, DIM6_MED)
        d7 = score_dim(cv_text, DIM7_HIGH, DIM7_MED)

        dims       = (d1, d2, d3, d4, d5, d6, d7)
        missing_mh = count_missing_must_haves(cv_text)
        score      = compute_score(dims, missing_mh)

        # Determine tier
        if score >= 85:
            tier = "Tier A"
        elif score >= 70:
            tier = "Tier B"
        elif score >= 55:
            tier = "Tier C"
        else:
            tier = "No-Hire"

        # Write to DB
        try:
            recommendation = "shortlist" if score >= 55 else "discard"
            cur.execute("""
                UPDATE applications
                SET ai_overall_score = %s,
                    ai_jd_score      = %s,
                    ai_recommendation = %s,
                    ai_jd_analysis   = %s
                WHERE id = %s
            """, (round(score / 10, 2), round(score / 10, 2),
                  recommendation, tier, app_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            safe_print(f"  -> DB write error: {e}")

        results.append({
            "app_id":     app_id,
            "candidate_id": cand_id,
            "name":       full_name,
            "score":      score,
            "tier":       tier,
            "dims":       list(dims),
            "missing_mh": missing_mh,
            "salary":     salary or "Not mentioned",
            "cv_len":     len(cv_text),
        })

        if (i + 1) % 20 == 0:
            safe_print(f"  Progress: {i+1}/{len(rows)} done")

    cur.close()
    conn.close()

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)

    # Save output
    output = {
        "job_id":   JOB_ID,
        "total":    len(rows),
        "screened": len(results),
        "errors":   len(errors),
        "top30":    results[:30],
        "all":      results,
        "unreadable": errors,
    }
    out_path = "output/job36_v2_screen.json"
    os.makedirs("output", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    safe_print(f"\n=== DONE ===")
    safe_print(f"Screened: {len(results)} candidates")
    safe_print(f"Errors:   {len(errors)}")
    safe_print(f"Output:   {out_path}")
    safe_print(f"\nTop 15:")
    for c in results[:15]:
        safe_print(f"  #{results.index(c)+1:2d}  {c['score']:5.1f}  {c['tier']:<8}  {c['name']}")

    return results


if __name__ == "__main__":
    main()
