"""
Mark values interview as COMPLETED in Markaz tracking fields
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

    # First check current state
    cur.execute(
        "SELECT completed_stages, call_done FROM applications WHERE id = %s",
        (3186,)
    )
    result = cur.fetchone()
    current_stages = result[0] if result[0] else []
    current_call_done = result[1]

    print(f"[DEBUG] Current completed_stages: {current_stages}")
    print(f"[DEBUG] Current call_done: {current_call_done}")

    # Ensure values_interview is in completed_stages
    if not current_stages:
        current_stages = []
    if "values_interview" not in current_stages:
        current_stages.append("values_interview")

    # Update both fields
    cur.execute(
        """
        UPDATE applications
        SET completed_stages = %s,
            call_done = %s,
            updated_at = %s
        WHERE id = %s
        """,
        (
            json.dumps(current_stages),
            True,
            datetime.now(),
            3186
        )
    )

    print(f"[OK] Marked values interview as COMPLETED")
    print(f"     completed_stages: {current_stages}")
    print(f"     call_done: true")
    print(f"[OK] Refresh Markaz — form should now display!")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
