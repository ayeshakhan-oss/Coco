"""
Fetch all Job 26 candidates with resume data from Neon DB
"""
import psycopg2
import base64
import json
import sys
import os

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode": "require",
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        # Query all Job 26 applications
        cur.execute("""
            SELECT
                a.id as app_id,
                c.id as candidate_id,
                c.first_name,
                c.last_name,
                c.resume_data,
                c.email,
                c.phone,
                c.current_position,
                c.current_company,
                c.location
            FROM applications a
            JOIN candidates c ON a.candidate_id = c.id
            WHERE a.job_id = 26
            ORDER BY a.id
        """)

        rows = cur.fetchall()

        candidates_list = []
        count = 0

        for idx, row in enumerate(rows, 1):
            (app_id, cand_id, first_name, last_name, resume_b64, email,
             phone, current_pos, current_co, location) = row

            name = f"{first_name} {last_name}" if first_name and last_name else "Unknown"

            # Try to decode resume
            resume_text = ""
            try:
                if resume_b64:
                    resume_bytes = base64.b64decode(resume_b64)
                    resume_text = resume_bytes.decode('utf-8', errors='replace')
            except Exception as e:
                resume_text = f"[ERROR decoding resume: {type(e).__name__}]"

            candidate = {
                "rank": idx,
                "app_id": app_id,
                "candidate_id": cand_id,
                "name": name,
                "email": email,
                "phone": phone,
                "current_position": current_pos,
                "current_company": current_co,
                "location": location,
                "resume_text": resume_text,
                "resume_length": len(resume_text)
            }
            candidates_list.append(candidate)
            count += 1

        # Save full data
        output_file = "c:/Agent Coco/output/job26_candidates_full.json"
        os.makedirs("c:/Agent Coco/output", exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(candidates_list, f, indent=2, ensure_ascii=False)

        print(f"Success: {count} candidates fetched and saved to {output_file}")

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
