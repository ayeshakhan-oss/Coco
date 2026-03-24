"""
Extract full CV text for Job 36 manual reassessment candidates.
Saves text to output/cv_texts_job36/ directory for human review.
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

# Top 15 from v2 keyword screening + Siddique + Mehwish
CANDIDATE_IDS = [
    1602,  # Asif Khan        100.0  #1
    1518,  # Zubair Hussain    93.8  #2
    1545,  # PARIYAL FAZAL SHAH 93.8 #3
    1720,  # Jawad Khan        92.5  #4
    1658,  # Fatima Razzaq     91.3  #5
    1454,  # Shahid Kamal      88.8  #6
    1864,  # Fatima Mughal     87.5  #7
    1528,  # Muhammad Afzaal   86.2  #8
    1633,  # Midhat Fatima     86.2  #9
    1839,  # HabibunNabi       86.2  #10
    1489,  # Muhammad Qasi     85.0  #11
    1700,  # Asad Farooq       85.0  #12
    1802,  # syeda farzana ali shah 83.8 #13
    1950,  # Jalal Ud Din      82.5  #14
    1442,  # Faryal Afridi     81.2  #15
    1624,  # Muhammad Siddique 78.8  #29 - manually check
    1808,  # Mehwish           70.0  #63 - manually check
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
    """, (CANDIDATE_IDS, CANDIDATE_IDS))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    os.makedirs("output/cv_texts_job36", exist_ok=True)

    summary = []
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

        summary.append({
            "app_id": app_id,
            "name": full_name,
            "salary": salary or "Not mentioned",
            "cv_len": len(cv_text),
            "file": out_file,
        })
        print(f"  -> {len(cv_text)} chars saved to {out_file}")

    print(f"\nDone. {len(summary)} CVs extracted.")
    with open("output/cv_texts_job36/_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
