"""Fetch and decode all CVs for Job 32 candidates."""
import os, base64, json, re
import psycopg2
import fitz  # pymupdf

DB = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb", "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd", "sslmode": "require"
}

OUT = "output/cv_texts_job32"
os.makedirs(OUT, exist_ok=True)

conn = psycopg2.connect(**DB)
cur  = conn.cursor()

cur.execute("""
    SELECT a.id, c.first_name || ' ' || c.last_name, c.email,
           c.location, c.resume_data, c.resume_mime_type,
           a.cover_letter, a.custom_answers
    FROM applications a
    JOIN candidates c ON a.candidate_id = c.id
    WHERE a.job_id = 32
    ORDER BY a.id
""")
rows = cur.fetchall()
print(f"Fetched {len(rows)} rows")

summary = []
for app_id, name, email, location, resume_data, mime, cover, custom in rows:
    entry = {"app_id": app_id, "name": name, "email": email, "location": location}
    text = ""

    if resume_data:
        try:
            raw = base64.b64decode(resume_data)
            doc = fitz.open(stream=raw, filetype="pdf")
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            text = f"[PDF parse error: {e}]"

    if cover:
        text += f"\n\n--- COVER NOTE ---\n{cover}"
    if custom:
        text += f"\n\n--- CUSTOM ANSWERS ---\n{json.dumps(custom, ensure_ascii=False)}"

    if not text.strip():
        text = "[NO CV / INCOMPLETE APPLICATION]"

    entry["cv_length"] = len(text)
    entry["has_cv"] = bool(resume_data)

    fname = f"{app_id}_{re.sub(r'[^a-zA-Z0-9]', '_', name)}.txt"
    with open(f"{OUT}/{fname}", "w", encoding="utf-8") as f:
        f.write(f"=== App {app_id} | {name} | {email} | {location} ===\n\n")
        f.write(text)

    summary.append(entry)
    print(f"  {app_id} | {name[:30]:<30} | {'CV' if resume_data else 'NO CV'} | {len(text)} chars")

with open(f"{OUT}/_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

cur.close(); conn.close()
print(f"\nDone. Files saved to {OUT}/")
