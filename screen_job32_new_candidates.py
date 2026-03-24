"""
Job 32 — Fundraising & Partnerships Manager
Screen the 13 candidates who were NOT included in the original screening.
Outputs: job32_new_candidates.json
"""

import base64, io, json, sys
import psycopg2
import PyPDF2
import fitz
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

DB = {
    "host":     "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname":   "neondb",
    "user":     "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode":  "require",
}

# Application IDs of candidates never screened for Job 32
# Deduplicated: AAMIR SOHAIL take 1393 only, sarmad iqbal take 1958 only
UNSCREENED_APP_IDS = [
    1225,   # aymen
    1393,   # AAMIR SOHAIL
    1851,   # Shahzad Saleem Abbasi
    1874,   # Mohammad Aqeel Qureshi
    1875,   # Samreen Durrani
    1884,   # Bilal Shahid
    1910,   # Sikandar Khurshid
    1957,   # Bushra Nawaz
    1958,   # sarmad iqbal
    1961,   # Hira Noureen Khan
    1963,   # Ibrahim Basit
    1964,   # Mehboob Alam
    1970,   # SAHRISH KASHIF
]

JD_SUMMARY = """
Role: Fundraising & Partnerships Manager at Taleemabad (EdTech, Islamabad)
Budget: PKR 150,000 – 270,000/month

MUST-HAVES:
1. Direct fundraising/BD ownership — not support, not compliance, not programme delivery
2. Pakistan donor landscape knowledge (USAID, World Bank, FCDO, EU, multilaterals)
3. Proposals independently written and won from institutional donors
4. Pipeline management (30–50+ live opportunities)
5. Islamabad-based OR explicitly willing to relocate to Islamabad
6. Strong written English communication (proposals, pitch decks, concept notes)

NICE-TO-HAVES:
- Independently closed $500K+ deal
- Named bilateral/multilateral relationships (programme officers)
- Education sector experience
- Government/policy engagement in Islamabad

INSTANT DISQUALIFIERS:
- Domestic charity fundraising only (no international donors)
- Programme management/M&E — not acquisition
- Pure grants compliance (no pipeline building)
- UK/MENA-based with no relocation stated
- No fundraising function at all (HR, admin, IT, sales, clinical)

Year 1 target: $500K–$1M+ in closed funding from cold.
"""


def extract_text_pypdf2(pdf_bytes):
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        pages = [p.extract_text() or "" for p in reader.pages]
        return "\n".join(pages).strip()
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
        return "\n".join(texts).strip()
    except:
        return ""


def get_cv_text(resume_data_b64):
    pdf_bytes = base64.b64decode(resume_data_b64)
    text = extract_text_pypdf2(pdf_bytes)
    if len(text) < 100:
        print("  >> OCR fallback", flush=True)
        text = extract_text_ocr(pdf_bytes)
    return text


def score_candidate(name, location, cv_text):
    """
    Quick JD-alignment keyword scoring for the Fundraising & Partnerships Manager role.
    Returns a dict with keyword hits and a rough tier.
    """
    text_lower = cv_text.lower()

    # Core fundraising/BD signals
    fundraising_kw = [
        "fundraising","fund raising","fundraise","resource mobilisation","resource mobilization",
        "business development","bd manager","partnerships manager","grants manager",
        "proposal writing","concept note","pitch","donor relations","donor engagement",
        "winning proposals","grant writing","mobilised","mobilized","raised","secured funding",
        "funding secured","grants won","award","awarded","successful bid",
    ]
    donor_kw = [
        "usaid","fcdo","dfid","world bank","undp","unicef","unfpa","eu delegation",
        "european union","jica","adb","ifad","gef","global fund","ford foundation",
        "bill gates","gates foundation","open society","british council","embass",
        "multilateral","bilateral","institutional donor","international donor",
    ]
    pipeline_kw = [
        "pipeline","opportunities","rfp","request for proposal","eoi","expression of interest",
        "grant portal","prospect","cultivate","cultivation","stewardship","crm","salesforce",
        "30 opportunities","40 opportunities","50 opportunities","live opportunities",
        "active pipeline","manage pipeline",
    ]
    islamabad_kw = [
        "islamabad","rawalpindi","isb","willing to relocate","open to relocation",
        "can relocate","available to relocate","based in islamabad",
    ]
    written_kw = [
        "proposal","concept note","pitch deck","grant application","written communication",
        "english","report writing","technical writing","donor report","narrative",
    ]
    education_kw = [
        "education","school","teacher","student","edtech","curriculum","tcf","read foundation",
        "teach for pakistan","sabaq","ministry of education","learning outcomes",
    ]
    disqualifiers = [
        "human resources","hr manager","clinical","psychologist","autocad","real estate",
        "it operations","telecom","domestic charity","hospital fundraising","digital marketing",
        "saas sales","software sales","customer service",
    ]

    def hits(keywords):
        return sum(1 for kw in keywords if kw in text_lower)

    fr_hits    = hits(fundraising_kw)
    donor_hits = hits(donor_kw)
    pipe_hits  = hits(pipeline_kw)
    isb_hits   = hits(islamabad_kw)
    write_hits = hits(written_kw)
    edu_hits   = hits(education_kw)
    dq_hits    = hits(disqualifiers)

    # Rough scoring (out of 100)
    score = min(30, fr_hits * 5) + min(25, donor_hits * 5) + min(15, pipe_hits * 5) + \
            min(10, isb_hits * 5) + min(10, write_hits * 3) + min(10, edu_hits * 2)

    # Disqualifier penalty
    if dq_hits >= 2:
        score = max(0, score - 20)

    location_lower = (location or "").lower()
    is_islamabad = any(x in location_lower for x in ["islamabad","rawalpindi","isb","lahore","karachi","peshawar","pakistan"])

    return {
        "fundraising_hits": fr_hits,
        "donor_hits": donor_hits,
        "pipeline_hits": pipe_hits,
        "islamabad_signal": isb_hits,
        "education_hits": edu_hits,
        "disqualifier_hits": dq_hits,
        "keyword_score": round(score, 1),
        "location": location or "Unknown",
        "text_length": len(cv_text),
    }


def main():
    print("Connecting to DB...", flush=True)
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    results = []

    for app_id in UNSCREENED_APP_IDS:
        cur.execute("""
            SELECT c.first_name, c.last_name, c.location, c.resume_data,
                   c.current_position, c.current_company, c.experience
            FROM applications a
            JOIN candidates c ON c.id = a.candidate_id
            WHERE a.id = %s
        """, (app_id,))
        row = cur.fetchone()
        if not row:
            print(f"  [SKIP] App {app_id} not found", flush=True)
            continue

        first, last, location, resume_data, curr_pos, curr_co, exp = row
        name = f"{first} {last}".strip()
        print(f"\n[{app_id}] {name} | {location}", flush=True)

        if not resume_data:
            print("  >> No resume data", flush=True)
            results.append({
                "app_id": app_id, "name": name, "location": location,
                "status": "NO_RESUME", "keyword_score": 0,
                "cv_text_preview": ""
            })
            continue

        print(f"  >> Extracting CV ({len(resume_data)//1024}KB base64)...", flush=True)
        try:
            cv_text = get_cv_text(resume_data)
        except Exception as e:
            print(f"  >> ERROR extracting CV: {e}", flush=True)
            cv_text = ""

        if len(cv_text) < 50:
            print(f"  >> Unreadable CV (only {len(cv_text)} chars)", flush=True)
            results.append({
                "app_id": app_id, "name": name, "location": location,
                "status": "UNREADABLE", "keyword_score": 0,
                "cv_text_preview": cv_text[:200]
            })
            continue

        scores = score_candidate(name, location, cv_text)
        print(f"  >> Score: {scores['keyword_score']} | FR:{scores['fundraising_hits']} "
              f"Donor:{scores['donor_hits']} Pipeline:{scores['pipeline_hits']} "
              f"DQ:{scores['disqualifier_hits']}", flush=True)

        result = {
            "app_id": app_id,
            "name": name,
            "location": location,
            "current_position": curr_pos,
            "current_company": curr_co,
            "experience": exp,
            "status": "SCREENED",
            **scores,
            "cv_text_preview": cv_text[:3000],
            "cv_text_full": cv_text,
        }
        results.append(result)

    conn.close()

    # Sort by keyword score desc
    results.sort(key=lambda x: x.get("keyword_score", 0), reverse=True)

    out_path = r"c:\My First Agent\job32_new_candidates.json"
    # Save without full CV text to keep file manageable
    save_results = []
    for r in results:
        r_save = {k: v for k, v in r.items() if k != "cv_text_full"}
        save_results.append(r_save)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(save_results, f, indent=2, ensure_ascii=False)

    # Save full text separately for deep screening
    full_path = r"c:\My First Agent\job32_new_cvtext.json"
    with open(full_path, "w", encoding="utf-8") as f:
        cv_texts = {r["name"]: r.get("cv_text_full", "") for r in results}
        json.dump(cv_texts, f, indent=2, ensure_ascii=False)

    print(f"\n\n{'='*60}")
    print(f"RESULTS SUMMARY — Job 32 New Candidates")
    print(f"{'='*60}")
    for r in results:
        status = r.get("status","?")
        score  = r.get("keyword_score", 0)
        print(f"  [{r['app_id']}] {r['name']:<30} Score:{score:>5}  Status:{status}")

    print(f"\nSaved to: {out_path}")
    print(f"CV texts: {full_path}")


if __name__ == "__main__":
    main()
