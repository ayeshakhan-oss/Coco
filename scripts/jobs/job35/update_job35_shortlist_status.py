"""
Update status = 'shortlisted' for Job 35 top 20 candidates
(matches what Markaz UI "Shortlist Candidate" action does)
"""

import psycopg2

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode": "require",
}

# Top 20 application IDs for Job 35
SHORTLIST_APP_IDS = [
    1878,  # Rameez Wasif
    1774,  # Fatima Tu Zahra
    1569,  # Rabia Zafar
    1558,  # Hadiyah Shaheen
    1369,  # Hassan Zafar
    1816,  # Dur E Nayab
    1777,  # Rahima Omar
    1771,  # Wasif Mehdi
    1663,  # Zeeshan Ali
    1701,  # Mahnoor Hasan
    1949,  # Maria Malik
    1821,  # Ayesha Nadeem
    1829,  # Muhammad Burhan Hassan
    1445,  # Faryal Afridi
    1592,  # Muhammad Junaid
    1456,  # Shahid Kamal
    1429,  # Scheherazade Noor
    1550,  # Ali Muhammad
    1944,  # Mariam Rehman (app 1)
    1945,  # Mariam Rehman (app 2 — same candidate, double application)
    1947,  # Daniyah Noor
]

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    try:
        cur.execute(
            """
            UPDATE applications
            SET status = 'shortlisted'
            WHERE id = ANY(%s)
            """,
            (SHORTLIST_APP_IDS,)
        )
        updated = cur.rowcount
        conn.commit()
        print(f"Done. {updated} applications marked as 'shortlisted'.")

    except Exception as e:
        conn.rollback()
        print(f"ERROR — rolled back: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
