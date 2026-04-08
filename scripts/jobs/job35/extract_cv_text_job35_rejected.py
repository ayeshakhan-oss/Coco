"""
Extract CV text for 3 pilot candidates — Job 35 CV-stage rejections
App IDs: 1396 (Hadia Akram), 1537 (Zainab Azhar), 1634 (Midhat Fatima)
"""

import psycopg2, base64, io, os
import PyPDF2

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode": "require"
}

APP_IDS = [1396, 1537, 1634]

def extract_text(resume_data):
    try:
        pdf_bytes = base64.b64decode(resume_data)
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        return f"[ERROR: {e}]"

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, c.first_name, c.last_name, c.email, c.resume_data,
               a.ai_screening_summary, a.ai_jd_analysis
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.id = ANY(%s)
    """, (APP_IDS,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    for row in rows:
        app_id, first, last, email, resume_data, summary, tier = row
        print(f"\n{'='*60}")
        print(f"App {app_id} — {first} {last} | {email}")
        print(f"Tier: {tier} | Summary: {summary}")
        print(f"{'='*60}")
        if resume_data:
            text = extract_text(resume_data)
            print(text[:3000].encode('ascii', errors='replace').decode('ascii'))
        else:
            print("[No CV]")

if __name__ == "__main__":
    main()
