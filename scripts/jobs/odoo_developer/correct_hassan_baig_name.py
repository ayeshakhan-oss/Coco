"""
Correct candidate name from "Hassan Baig" to "Muhammad Hassan Baig"
"""

import psycopg2

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

    # Update the candidate name to correct full name
    cur.execute(
        """
        UPDATE candidates
        SET first_name = %s
        WHERE id = %s
        """,
        ("Muhammad Hassan", 2561)
    )

    print(f"[OK] Updated candidate name to 'Muhammad Hassan Baig' (ID: 2561)")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
