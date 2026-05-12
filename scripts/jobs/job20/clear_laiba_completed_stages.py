"""
Clear completed_stages for Laiba Ahmad to match Meer Muneeb's state
This allows the Markaz UI form to display properly
"""

import psycopg2

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode": "require"
}

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

print("[FIX] Clearing completed_stages for Laiba Ahmad (app 1389)...")
cur.execute("""
    UPDATE applications
    SET completed_stages = NULL
    WHERE id = 1389
""")

print("[OK] Laiba's completed_stages cleared. Scorecard should now display on Markaz UI.")
conn.commit()
cur.close()
conn.close()
