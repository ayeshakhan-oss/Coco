"""
Extract CV text for all Job 35 CV-stage rejected candidates.
Job 35: Junior Research Associate, Impact & Policy
Filters: status=rejected, values_interview_result IS NULL, no LinkedIn temp emails.
Saves text files to output/cv_texts_job35_rejected/
"""

import os, sys, base64, io, json, re
import psycopg2
import PyPDF2
try:
    import fitz
    import pytesseract
    from PIL import Image
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

DB_HOST = "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech"
DB_NAME = "neondb"
DB_USER = "neondb_owner"
DB_PASS = "npg_kBQ10OASHEmd"

JOB_ID     = 35
OUTPUT_DIR = "output/cv_texts_job35_rejected"


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


def main():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER,
        password=DB_PASS, sslmode='require'
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT
            a.id AS app_id,
            TRIM(c.first_name || ' ' || COALESCE(c.last_name, '')) AS full_name,
            c.email,
            c.location,
            c.resume_data,
            a.canned_answers->'desiredSalary'->>'answer' AS expected_salary
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = %s
          AND a.status = 'rejected'
          AND a.values_interview_result IS NULL
          AND c.email NOT ILIKE '%%linkedin%%'
        ORDER BY a.id DESC
    """, (JOB_ID,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    summary = []
    print(f"\n{'='*60}")
    print(f"Job 35 — CV Rejection Extraction ({len(rows)} candidates)")
    print(f"{'='*60}\n")

    for app_id, full_name, email, location, resume_b64, salary in rows:
        print(f"Parsing: {full_name} (app {app_id})...", end=" ", flush=True)
        cv_text = parse_pdf(resume_b64) if resume_b64 else ""

        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', full_name)
        out_file = f"{OUTPUT_DIR}/{app_id}_{safe_name}.txt"

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"APP ID:   {app_id}\n")
            f.write(f"NAME:     {full_name}\n")
            f.write(f"EMAIL:    {email}\n")
            f.write(f"LOCATION: {location or 'Not mentioned'}\n")
            f.write(f"SALARY:   {salary or 'Not mentioned'}\n")
            f.write("=" * 80 + "\n\n")
            f.write(cv_text if cv_text.strip() else "[CV UNREADABLE OR EMPTY]")

        status = f"OK ({len(cv_text)} chars)" if cv_text.strip() else "UNREADABLE"
        print(status)

        summary.append({
            "app_id": app_id,
            "name": full_name,
            "email": email,
            "location": location or "Not mentioned",
            "salary": salary or "Not mentioned",
            "cv_len": len(cv_text),
            "readable": bool(cv_text.strip()),
            "file": out_file,
        })

    summary_path = f"{OUTPUT_DIR}/_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    readable = sum(1 for s in summary if s["readable"])
    print(f"\n{'='*60}")
    print(f"DONE. {len(summary)} candidates processed.")
    print(f"  Readable CVs:   {readable}")
    print(f"  Unreadable:     {len(summary) - readable}")
    print(f"  Output dir:     {OUTPUT_DIR}/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
