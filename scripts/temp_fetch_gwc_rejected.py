import psycopg2

conn = psycopg2.connect(
    host='ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech',
    dbname='neondb',
    user='neondb_owner',
    password='npg_kBQ10OASHEmd',
    sslmode='require'
)
cur = conn.cursor()

cur.execute("""
    SELECT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        a.id as app_id,
        a.gwc_interview_result,
        a.status
    FROM candidates c
    JOIN applications a ON a.candidate_id = c.id
    JOIN jobs j ON a.job_id = j.id
    WHERE j.title = 'Hackathon 2026'
      AND a.gwc_interview_result = 'pass'
      AND a.status NOT IN ('hired', 'offer')
    ORDER BY c.first_name
""")

rows = cur.fetchall()
print(f"\nFound {len(rows)} candidates with GWC Passed but not hired for Hackathon 2026:\n")
for r in rows:
    cand_id, first_name, last_name, email, app_id, gwc_result, status = r
    print(f"{first_name} {last_name} ({email}) - Status: {status}, GWC: {gwc_result}")

conn.close()
