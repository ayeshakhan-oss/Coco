"""
Update scorecard JSON to reflect correct candidate name: Muhammad Hassan Baig
"""

import psycopg2
import json

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

    # Fetch the current scorecard
    cur.execute(
        "SELECT values_scorecard FROM applications WHERE id = %s",
        (3185,)
    )
    result = cur.fetchone()

    if result and result[0]:
        scorecard = result[0]
        # Update candidate name in JSON
        scorecard["candidateName"] = "Muhammad Hassan Baig"

        # Update back to database
        cur.execute(
            "UPDATE applications SET values_scorecard = %s WHERE id = %s",
            (json.dumps(scorecard), 3185)
        )

        print(f"[OK] Updated scorecard with correct name 'Muhammad Hassan Baig' (App 3185)")
    else:
        print("[ERROR] Scorecard not found")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
