"""
Job 26 — Extract CV texts to output/cv_texts_job26/ for manual screening
"""
import psycopg2, base64, os, re, io, json

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb", "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd", "sslmode": "require",
}
OUT_DIR = "output/cv_texts_job26"
os.makedirs(OUT_DIR, exist_ok=True)

def extract_text(pdf_bytes):
    text = ""
    try:
        import PyPDF2
        r = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = "\n".join(p.extract_text() or "" for p in r.pages).strip()
    except Exception:
        pass
    if len(text) < 50:
        try:
            import fitz
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = "\n".join(p.get_text() for p in doc).strip()
        except Exception:
            pass
    if len(text) < 50:
        try:
            import fitz, pytesseract
            from PIL import Image
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            texts = []
            for p in doc:
                pix = p.get_pixmap(dpi=200)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                texts.append(pytesseract.image_to_string(img))
            text = "\n".join(texts).strip()
        except Exception as e:
            text = f"[OCR failed: {e}]"
    return text

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, a.applied_at, c.first_name, c.last_name, c.email,
               c.current_position, c.current_company, c.location,
               c.experience, c.education, c.questions_answered, c.resume_data
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = 26
        ORDER BY a.applied_at DESC
    """)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close(); conn.close()

    summary = []
    for row in rows:
        r = dict(zip(cols, row))
        app_id = r['id']
        name = f"{r['first_name']} {r['last_name']}".strip()
        safe = re.sub(r'[^\w]', '_', name)
        fpath = os.path.join(OUT_DIR, f"{app_id}_{safe}.txt")

        cv_text = ""
        if r['resume_data']:
            try:
                cv_text = extract_text(base64.b64decode(r['resume_data']))
            except Exception as e:
                cv_text = f"[Decode error: {e}]"
        else:
            cv_text = "[No CV uploaded]"

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(f"APP ID: {app_id}\n")
            f.write(f"NAME: {name}\n")
            f.write(f"EMAIL: {r['email']}\n")
            f.write(f"APPLIED: {r['applied_at']}\n")
            for field in ['current_position','current_company','location','experience','education']:
                if r.get(field): f.write(f"{field.upper()}: {r[field]}\n")
            if r.get('questions_answered'):
                f.write(f"SCREENING_QS: {json.dumps(r['questions_answered'], ensure_ascii=False)}\n")
            f.write("="*80 + "\n\n")
            f.write(cv_text)

        print(f"[{app_id}] {name} — {len(cv_text)} chars")
        summary.append({"app_id": app_id, "name": name, "cv_len": len(cv_text), "file": fpath})

    with open(os.path.join(OUT_DIR, "_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nDone. {len(summary)} files written to {OUT_DIR}/")
    no_cv = [s for s in summary if s['cv_len'] < 50]
    if no_cv: print(f"No/unreadable CV: {[s['app_id'] for s in no_cv]}")

if __name__ == "__main__":
    main()
