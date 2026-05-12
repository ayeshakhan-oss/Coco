"""
Populate missing display fields for Laiba Ahmad values scorecard
Job 20 — Senior Product Manager
"""

import psycopg2
import json
from datetime import datetime

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode": "require"
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Update display fields for Markaz UI
    cur.execute("""
        UPDATE applications
        SET values_interview_result = %s,
            values_interview_notes = %s,
            values_interviewer_name = %s
        WHERE id = %s
    """, (
        'pass',
        'PASS - 4 pluses (Don\'t Walk Away, All for One, Continuously Improve, Courageous Conversations), 2 plus-minuses (Don\'t Hold On Tight, Practice Joy). Zero minuses. Ready for Right Seat interview.',
        'Ayesha Khan',
        1389
    ))

    print(f"[OK] Updated values_interview_result, values_interview_notes, values_interviewer_name for App 1389")

    conn.commit()
    cur.close()
    conn.close()
    print("[OK] Fields updated successfully. Scorecard should now display in Markaz UI.")

if __name__ == "__main__":
    main()
