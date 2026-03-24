"""
Extract full CV text for Job 36 — extended set (top 30 + Siddique + Mehwish).
Skips candidates already extracted.
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

# Additional candidates not in first extraction (top 30 beyond the original 15 + duplicates)
# Duplicates: 1546=PARIYAL(same as 1545), 1942=FatimaRazzaq(same as 1658) — skip
NEW_IDS = [
    1477,  # Sadia Siddique    81.2  #18
    1513,  # Ali Zia           81.2  #19
    1639,  # Wajeeha rehber    81.2  #20
    1755,  # Usman Ahmed Khan  81.2  #21
    1430,  # Scheherazade Noor 80.0  #22
    1450,  # Naveen Shariff    80.0  #23
    1453,  # Abid Hussain      80.0  #24
    1591,  # Muhammad Junaid   80.0  #25
    1600,  # Adil Javed        80.0  #26
    1789,  # Muhammad Omer Khan 80.0 #27
    1495,  # Shabbir Hussain   78.8  #28
    1556,  # Sana Mehboob      78.8  #29
    1608,  # Afaq Ahmad        78.8  #30
]


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
            TRIM(c.first_name || ' ' || c.last_name) AS full_name,
            c.resume_data,
            a.canned_answers->'desiredSalary'->>'answer' AS expected_salary
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.id = ANY(%s)
        ORDER BY array_position(%s, a.id)
    """, (NEW_IDS, NEW_IDS))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    os.makedirs("output/cv_texts_job36", exist_ok=True)

    for app_id, full_name, resume_b64, salary in rows:
        print(f"Parsing: {full_name} (app {app_id})")
        cv_text = parse_pdf(resume_b64) if resume_b64 else ""

        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', full_name)
        out_file = f"output/cv_texts_job36/{app_id}_{safe_name}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"APP ID: {app_id}\n")
            f.write(f"NAME: {full_name}\n")
            f.write(f"SALARY: {salary or 'Not mentioned'}\n")
            f.write("=" * 80 + "\n\n")
            f.write(cv_text if cv_text.strip() else "[CV UNREADABLE OR EMPTY]")

        print(f"  -> {len(cv_text)} chars saved to {out_file}")

    print(f"\nDone. {len(rows)} CVs extracted.")


if __name__ == "__main__":
    main()
