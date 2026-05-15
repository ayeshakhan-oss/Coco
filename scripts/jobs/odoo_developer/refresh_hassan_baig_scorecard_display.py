"""
Refresh display fields to trigger Markaz UI update
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

    # Touch the updated_at timestamp to trigger UI refresh
    cur.execute(
        """
        UPDATE applications
        SET updated_at = %s
        WHERE id = %s
        """,
        (datetime.now(), 3185)
    )

    print(f"[OK] Refreshed application timestamp to trigger Markaz UI update (App 3185)")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
