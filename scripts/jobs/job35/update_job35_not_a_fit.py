"""
Mark all non-shortlisted Job 35 applications as 'rejected' (Not a Fit)
"""
import psycopg2

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode": "require",
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE applications
            SET status = 'rejected'
            WHERE job_id = 35
              AND status = 'new'
            """
        )
        updated = cur.rowcount
        conn.commit()
        print(f"Done. {updated} applications marked as 'rejected' (Not a Fit).")
    except Exception as e:
        conn.rollback()
        print(f"ERROR — rolled back: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
