
import os, base64, io, re
import psycopg2
import PyPDF2
try:
    import fitz, pytesseract
    from PIL import Image
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

conn = psycopg2.connect(host="ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    dbname="neondb", user="neondb_owner", password="npg_kBQ10OASHEmd", sslmode='require')
cur = conn.cursor()
cur.execute("""
    SELECT a.id, TRIM(c.first_name||' '||c.last_name), c.resume_data,
           a.canned_answers->'desiredSalary'->>'answer'
    FROM applications a JOIN candidates c ON a.candidate_id=c.id
    WHERE a.id IN (1857, 1674)
""")
rows = cur.fetchall()
cur.close(); conn.close()

def parse_pdf(b64):
    try:
        pdf_bytes = base64.b64decode(b64)
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = "".join(p.extract_text() or "" for p in reader.pages)
        if len(text.strip()) > 50: return text
    except: pass
    if OCR_AVAILABLE:
        try:
            doc = fitz.open(stream=base64.b64decode(b64), filetype="pdf")
            t = ""
            for page in doc:
                pix = page.get_pixmap(matrix=fitz.Matrix(2,2))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                t += pytesseract.image_to_string(img)
            doc.close(); return t
        except: pass
    return ""

os.makedirs("output/cv_texts_job36", exist_ok=True)
for app_id, name, b64, salary in rows:
    text = parse_pdf(b64) if b64 else ""
    safe = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    path = f"output/cv_texts_job36/{app_id}_{safe}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"APP ID: {app_id}\nNAME: {name}\nSALARY: {salary or 'Not mentioned'}\n{'='*80}\n\n{text or '[UNREADABLE]'}")
    print(f"{name} ({app_id}): {len(text)} chars -> {path}")
