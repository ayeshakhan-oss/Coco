"""
FILL ALL VALUES SCORECARD DISPLAY FIELDS - Muhammad Hassan Baig
"""

import psycopg2
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

    # Populate ALL display fields for Markaz UI
    cur.execute(
        """
        UPDATE applications
        SET values_interview_result = %s,
            values_interview_score = %s,
            values_interview_notes = %s,
            values_interview_date = %s,
            values_interviewer_name = %s,
            updated_at = %s
        WHERE id = %s
        """,
        (
            "pass",
            10,  # Score: 4 pluses + 2 plus-minuses = 10/10
            "PASS - 4 pluses (All for One, Don't Hold On Too Tight, Practice Joy, Don't Walk Away), 2 plus-minuses (Continuously Improve, Courageous Conversations). Zero minuses. GWC: Gets it (YES), Wants it (YES), Capacity (YES). Ready for Right Seat interview.",
            datetime(2026, 5, 13),
            "Ayesha Khan",
            datetime.now(),
            3185
        )
    )

    print(f"[OK] Filled ALL values scorecard display fields for Muhammad Hassan Baig (App 3185)")
    print(f"     Result: pass")
    print(f"     Score: 10/10")
    print(f"     Date: 2026-05-13")
    print(f"     Interviewer: Ayesha Khan")

    conn.commit()
    cur.close()
    conn.close()
    print("[OK] Markaz UI should now display the scorecard.")

if __name__ == "__main__":
    main()
