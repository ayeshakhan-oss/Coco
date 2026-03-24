"""
Update ai_recommendation for Job 36 — Field Coordinator, Research & Impact Studies
Top 17 → shortlist | Rest of job 36 → discard
"""

import psycopg2
from datetime import datetime

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode": "require",
}

SHORTLIST_IDS = [1602, 1857, 1430, 1864, 1442, 1518, 1839, 1700, 1808, 1513, 1789, 1755, 1658, 1720, 1591, 1950, 1624]
JOB_ID = 36

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    try:
        # Step 1: Shortlist top 17
        cur.execute(
            """
            UPDATE applications
            SET ai_recommendation = 'shortlist',
                ai_screened_at = NOW()
            WHERE id = ANY(%s)
            """,
            (SHORTLIST_IDS,)
        )
        shortlisted = cur.rowcount
        print(f"Shortlisted: {shortlisted} rows updated")

        # Step 2: Discard all other applications for job 36
        cur.execute(
            """
            UPDATE applications
            SET ai_recommendation = 'discard',
                ai_screened_at = NOW()
            WHERE job_id = %s
              AND id != ALL(%s)
            """,
            (JOB_ID, SHORTLIST_IDS)
        )
        discarded = cur.rowcount
        print(f"Discarded: {discarded} rows updated")

        conn.commit()
        print(f"\nDone. {shortlisted} shortlisted + {discarded} discarded = {shortlisted + discarded} total updated.")

    except Exception as e:
        conn.rollback()
        print(f"ERROR — rolled back: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
