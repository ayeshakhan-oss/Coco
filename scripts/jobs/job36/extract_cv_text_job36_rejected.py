"""
Job 36 — Field Coordinator, Research & Impact Studies
Extract CV texts for ALL Category B rejected candidates (not individually reviewed).
Saves text to output/cv_texts_job36_rejected/ for Coco to screen.
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


def parse_pdf(b64_data):
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
            return text
    except Exception:
        pass
    # Fallback to OCR
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
            c.id AS candidate_id,
            TRIM(c.first_name || ' ' || c.last_name) AS full_name,
            c.email,
            c.resume_data,
            c.location,
            c.current_position,
            c.current_company,
            a.canned_answers->'desiredSalary'->>'answer' AS expected_salary,
            a.rejection_reason
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = 36
          AND a.status = 'rejected'
          AND c.email NOT LIKE '%.linkedin.temp'
          AND a.rejection_reason LIKE 'CV not individually reviewed%'
        ORDER BY c.first_name
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print(f"Found {len(rows)} Category B candidates to extract.")

    os.makedirs("output/cv_texts_job36_rejected", exist_ok=True)

    summary = []
    for app_id, cand_id, full_name, email, resume_b64, location, curr_pos, curr_company, salary, rej_reason in rows:
        print(f"Parsing: {full_name} (app {app_id}) ...", end=" ", flush=True)
        cv_text = parse_pdf(resume_b64) if resume_b64 else ""

        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', full_name)
        out_file = f"output/cv_texts_job36_rejected/{app_id}_{safe_name}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"APP ID: {app_id}\n")
            f.write(f"CANDIDATE ID: {cand_id}\n")
            f.write(f"NAME: {full_name}\n")
            f.write(f"EMAIL: {email}\n")
            f.write(f"LOCATION: {location or 'Not mentioned'}\n")
            f.write(f"CURRENT ROLE: {curr_pos or 'Not mentioned'}\n")
            f.write(f"CURRENT COMPANY: {curr_company or 'Not mentioned'}\n")
            f.write(f"EXPECTED SALARY: {salary or 'Not mentioned'}\n")
            f.write("=" * 80 + "\n\n")
            f.write(cv_text if cv_text.strip() else "[CV UNREADABLE OR EMPTY — no text extracted]")

        summary.append({
            "app_id": app_id,
            "candidate_id": cand_id,
            "name": full_name,
            "email": email,
            "location": location or "Not mentioned",
            "current_role": curr_pos or "Not mentioned",
            "current_company": curr_company or "Not mentioned",
            "salary": salary or "Not mentioned",
            "cv_len": len(cv_text),
            "readable": len(cv_text.strip()) > 50,
            "file": out_file,
        })
        print(f"{len(cv_text)} chars")

    print(f"\nDone. {len(summary)} CVs extracted.")
    readable = sum(1 for s in summary if s["readable"])
    unreadable = len(summary) - readable
    print(f"  Readable: {readable} | Unreadable/Empty: {unreadable}")

    with open("output/cv_texts_job36_rejected/_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print("Summary saved to output/cv_texts_job36_rejected/_summary.json")


if __name__ == "__main__":
    main()
