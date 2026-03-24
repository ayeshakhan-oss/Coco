"""
Job 36 v2 — Deep parse top 15 CVs for enrichment data.
Extracts: current role, total experience, key org signals, key strengths from CV text.
Uses Markaz names.
"""

import os, sys, json, base64, io, re
import psycopg2
from dotenv import load_dotenv
import PyPDF2
try:
    import fitz
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

# Top 15 app IDs from screening (deduplicated, ranked by score)
TOP_APP_IDS = [
    1602,  # Asif Khan        100.0
    1518,  # Zubair Hussain    93.8
    1545,  # PARIYAL FAZAL SHAH 93.8
    1720,  # Jawad Khan        92.5
    1658,  # Fatima Razzaq     91.3
    1454,  # Shahid Kamal      88.8
    1864,  # Fatima Mughal     87.5
    1528,  # Muhammad Afzaal   86.2
    1633,  # Midhat Fatima     86.2
    1839,  # HabibunNabi       86.2
    1489,  # Muhammad Qasi     85.0
    1700,  # Asad Farooq       85.0
    1802,  # syeda farzana ali shah 83.8
    1950,  # Jalal Ud Din      82.5
    1442,  # Faryal Afridi     81.2
]

HIGH_SIGNAL_ORGS = [
    "taleemabad", "tcf", "the citizens foundation", "teach for pakistan",
    "read foundation", "sabaq", "unicef", "undp", "usaid", "world bank",
    "fcdo", "dfid", "giz", "aga khan", "cerp", "ipa", "j-pal",
    "pide", "ifpri", "lums", "nust", "aga khan university",
    "aku", "ibadat", "oxford", "cambridge", "georgetown",
    "ministry of education", "mofe", "district government",
    "provincial government", "government of", "department of education",
    "unicef pakistan", "save the children", "plan international", "care",
    "action aid", "oxfam", "mercy corps",
]


def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(str(text).encode('ascii', errors='replace').decode('ascii'))


def parse_pdf(b64_data):
    try:
        pdf_bytes = base64.b64decode(b64_data)
    except Exception:
        return ""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "")
        if len(text.strip()) > 50:
            return text
    except Exception:
        pass
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
            return ocr_text
        except Exception:
            pass
    return ""


def extract_orgs(text):
    text_lower = text.lower()
    found = []
    for org in HIGH_SIGNAL_ORGS:
        if org in text_lower and org not in [o.lower() for o in found]:
            found.append(org.upper() if len(org) <= 5 else org.title())
    return found[:5]  # top 5 org signals


def extract_experience_years(text):
    # Look for year ranges like "2019 – 2023", "Jan 2020 – Dec 2022"
    patterns = [
        r'(\d{4})\s*[-–—]\s*(?:present|current|ongoing|now|\d{4})',
        r'(\d+)\s*\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
    ]
    years = []
    for pat in patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            years.append(m.group(0))

    # Count distinct year ranges
    year_numbers = re.findall(r'\b(20\d{2}|19\d{2})\b', text)
    if year_numbers:
        try:
            years_int = [int(y) for y in year_numbers if 1990 <= int(y) <= 2026]
            if years_int:
                span = max(years_int) - min(years_int)
                if span > 0:
                    return f"~{span} yrs"
        except:
            pass
    return "Not clear from CV"


def extract_current_role(text):
    # Look for current/present role patterns
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        if any(kw in line_lower for kw in ['present', 'current', 'ongoing', 'till date', 'to date']):
            # Look at surrounding lines for job title
            for j in range(max(0, i-2), min(len(lines), i+2)):
                candidate = lines[j].strip()
                if 10 < len(candidate) < 80 and not any(c.isdigit() for c in candidate[:3]):
                    return candidate[:70]

    # Fallback: look for common role keywords in first 500 chars
    first_part = text[:800]
    role_patterns = [
        r'(field\s+\w+(?:\s+\w+)?)',
        r'(research\s+\w+(?:\s+\w+)?)',
        r'(program\s+\w+(?:\s+\w+)?)',
        r'(monitoring\s+\w+(?:\s+\w+)?)',
        r'(coordinator\s*[-–]\s*\w+(?:\s+\w+)?)',
        r'(m\s*&\s*e\s+\w+(?:\s+\w+)?)',
    ]
    for pat in role_patterns:
        m = re.search(pat, first_part, re.IGNORECASE)
        if m:
            return m.group(0).strip().title()[:60]

    return "See CV"


def main():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER,
        password=DB_PASS, sslmode='require'
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT
            a.id AS app_id,
            TRIM(c.first_name || ' ' || c.last_name) AS full_name,
            c.resume_data,
            a.canned_answers->'desiredSalary'->>'answer' AS expected_salary
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.id = ANY(%s)
        ORDER BY array_position(%s, a.id)
    """, (TOP_APP_IDS, TOP_APP_IDS))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    results = {}
    for app_id, full_name, resume_b64, salary in rows:
        safe_print(f"Deep parsing: {full_name} (app {app_id})")
        cv_text = parse_pdf(resume_b64)
        if not cv_text.strip():
            safe_print(f"  -> Unreadable")
            results[app_id] = {
                "name": full_name, "app_id": app_id,
                "current_role": "CV unreadable", "exp": "N/A",
                "orgs": [], "salary": salary or "Not mentioned",
                "cv_snippet": "",
            }
            continue

        orgs    = extract_orgs(cv_text)
        exp     = extract_experience_years(cv_text)
        role    = extract_current_role(cv_text)

        # Print first 600 chars of CV for manual review
        snippet = cv_text[:600].replace('\n', ' ').strip()

        results[app_id] = {
            "name":         full_name,
            "app_id":       app_id,
            "current_role": role,
            "exp":          exp,
            "orgs":         orgs,
            "salary":       salary or "Not mentioned",
            "cv_snippet":   snippet,
        }

        safe_print(f"  Role: {role}")
        safe_print(f"  Exp:  {exp}")
        safe_print(f"  Orgs: {orgs}")
        safe_print(f"  CV:   {snippet[:200]}")
        safe_print("")

    out_path = "output/job36_v2_enriched.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    safe_print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
