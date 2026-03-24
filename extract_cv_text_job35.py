"""
Extract CV text for Job 35 (Junior Research Associate - Impact & Policy)
Top 35 candidates by scanner score for manual human-judgement re-screen.
Saves to output/cv_texts_job35/
"""

import os, base64, io, re
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

# Top 35 by scanner score (+ Mariam Rehman duplicate flagged)
CANDIDATE_IDS = [
    1514,  # Sehrish Irfan           9.8
    1729,  # Jawad Khan              9.8
    1445,  # Faryal Afridi           9.5
    1569,  # Rabia Zafar             9.4
    1899,  # Hassan Yasar            9.4
    1369,  # Hassan Zafar            9.3
    1592,  # Muhammad Junaid         9.3
    1902,  # Sidra Ishfaq            9.1
    1734,  # Syed Zashir Naqvi       9.1
    1730,  # Ijlal Haider            9.1
    1771,  # Wasif Mehdi             9.1
    1663,  # Zeeshan Ali             9.0
    1649,  # Manal Shah              9.0
    1829,  # Muhammad Burhan Hassan  9.0
    1820,  # Muhammad Rafay          9.0
    1532,  # Muqqadas Saba           8.9
    1512,  # Muhammad Usman          8.9
    1550,  # Ali Muhammad            8.9
    1665,  # ZainabAshraf            8.8
    1765,  # Hajra Asghar            8.6
    1641,  # Wajeeha Rehber          8.6
    1402,  # Aabsha Tasaawar         8.6
    1534,  # Nain Tara               8.6
    1696,  # Noor Fatima             8.6
    1456,  # Shahid Kamal            8.6
    1487,  # Sarim Kazi              8.6
    1490,  # Muhammad Zain Ul Haq    8.5
    1880,  # Nabiha Asghar           8.5  (Mombasa/Kenya - flag)
    1854,  # Muhammad Abdullah       8.5
    1945,  # Mariam Rehman (1)       8.5
    1855,  # Saira Shakoor           8.5
    1725,  # Muhammad Zaheer Abbasi  8.5
    1848,  # Huzaifa Mazhar          8.5
    1558,  # Hadiyah Shaheen         8.4
    1863,  # Hanniya Fatima          8.3
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output", "cv_texts_job35")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_text_pypdf2(pdf_bytes):
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        return text.strip()
    except Exception:
        return ""


def extract_text_ocr(pdf_bytes):
    if not OCR_AVAILABLE:
        return ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            pix = page.get_pixmap(dpi=200)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text += pytesseract.image_to_string(img) + "\n"
        return text.strip()
    except Exception:
        return ""


def extract_cv_text(pdf_bytes):
    text = extract_text_pypdf2(pdf_bytes)
    if len(text) < 50:
        text = extract_text_ocr(pdf_bytes)
    return text


def main():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, sslmode="require"
    )
    cur = conn.cursor()

    print(f"Extracting CVs for {len(CANDIDATE_IDS)} Job 35 candidates...")
    print(f"Output: {OUTPUT_DIR}\n")

    success, failed = 0, []

    for app_id in CANDIDATE_IDS:
        cur.execute("""
            SELECT c.first_name, c.last_name, c.resume_data, a.ai_overall_score,
                   COALESCE(c.location, '') as location
            FROM applications a
            JOIN candidates c ON a.candidate_id = c.id
            WHERE a.id = %s
        """, (app_id,))
        row = cur.fetchone()

        if not row:
            print(f"  [{app_id}] NOT FOUND in DB")
            failed.append(app_id)
            continue

        first_name, last_name, resume_data, score, location = row
        full_name = f"{first_name} {last_name}".strip()
        safe_name = re.sub(r'[^A-Za-z0-9_]', '_', full_name)
        filename = f"{app_id}_{safe_name}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(filepath):
            print(f"  [{app_id}] {full_name} — already exists, skipping")
            success += 1
            continue

        if not resume_data:
            print(f"  [{app_id}] {full_name} — no resume data")
            failed.append(app_id)
            continue

        try:
            pdf_bytes = base64.b64decode(resume_data)
            cv_text = extract_cv_text(pdf_bytes)

            if len(cv_text) < 50:
                print(f"  [{app_id}] {full_name} — unreadable PDF (OCR fallback too)")
                cv_text = "[CV UNREADABLE — OCR FAILED]"

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"APP ID: {app_id}\n")
                f.write(f"NAME: {full_name}\n")
                f.write(f"SCANNER SCORE: {score}\n")
                f.write(f"LOCATION: {location}\n")
                f.write("=" * 80 + "\n\n")
                f.write(cv_text)

            print(f"  [{app_id}] {full_name} — saved ({len(cv_text)} chars)")
            success += 1

        except Exception as e:
            print(f"  [{app_id}] {full_name} — ERROR: {e}")
            failed.append(app_id)

    cur.close()
    conn.close()

    print(f"\nDone. {success}/{len(CANDIDATE_IDS)} extracted.")
    if failed:
        print(f"Failed IDs: {failed}")


if __name__ == "__main__":
    main()
