import psycopg2
import base64
import io
import json
import os

# Neon DB connection
conn = psycopg2.connect(
    host="ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    database="neondb",
    user="neondb_owner",
    password="npg_kBQ10OASHEmd",
    sslmode="require"
)

# Application IDs for job 32
app_ids = [1225,1317,1327,1332,1333,1334,1335,1336,1337,1341,
           1342,1344,1346,1347,1348,1349,1350,1354,1355,1356,
           1357,1362,1363]

cur = conn.cursor()
results = {}

for app_id in app_ids:
    cur.execute("""
        SELECT a.id, c.first_name, c.last_name, c.email, c.location,
               c.resume_data, c.resume_file_name, c.resume_mime_type
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.id = %s
    """, (app_id,))
    row = cur.fetchone()
    if not row:
        continue

    aid, fname, lname, email, location, resume_data, filename, mime = row
    name = f"{fname} {lname}".strip()

    if not resume_data:
        results[app_id] = {"name": name, "email": email, "location": location,
                           "cv_text": None, "error": "No resume uploaded"}
        print(f"[{app_id}] {name} — No resume")
        continue

    try:
        raw = base64.b64decode(resume_data)

        # Try PDF first
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(raw))
            text = ""
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
            if len(text.strip()) < 50:
                raise ValueError("PDF text too short")
            results[app_id] = {"name": name, "email": email, "location": location,
                               "filename": filename, "cv_text": text.strip()}
            print(f"[{app_id}] {name} — PDF OK ({len(text)} chars)")
            continue
        except Exception as e1:
            pass

        # Try DOCX
        try:
            import docx
            doc = docx.Document(io.BytesIO(raw))
            text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            if len(text.strip()) < 50:
                raise ValueError("DOCX text too short")
            results[app_id] = {"name": name, "email": email, "location": location,
                               "filename": filename, "cv_text": text.strip()}
            print(f"[{app_id}] {name} — DOCX OK ({len(text)} chars)")
            continue
        except Exception as e2:
            pass

        results[app_id] = {"name": name, "email": email, "location": location,
                           "filename": filename, "cv_text": None,
                           "error": "Could not parse PDF or DOCX"}
        print(f"[{app_id}] {name} — Parse failed")

    except Exception as e:
        results[app_id] = {"name": name, "email": email, "location": location,
                           "cv_text": None, "error": str(e)}
        print(f"[{app_id}] {name} — Error: {e}")

cur.close()
conn.close()

# Save extracted texts
os.makedirs("output", exist_ok=True)
with open("output/extracted_cvs.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nDone. Extracted {sum(1 for v in results.values() if v.get('cv_text'))} / {len(app_ids)} CVs.")
print("Saved to output/extracted_cvs.json")
