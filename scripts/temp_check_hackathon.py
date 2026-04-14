import psycopg2

conn = psycopg2.connect(
    host='ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech',
    dbname='neondb',
    user='neondb_owner',
    password='npg_kBQ10OASHEmd',
    sslmode='require'
)
cur = conn.cursor()

# Check job titles that contain "Hackathon"
print("=== Job titles containing 'Hackathon' ===")
cur.execute("SELECT id, title, job_id FROM jobs WHERE LOWER(title) LIKE '%hackathon%'")
for r in cur.fetchall():
    print(r)

# Check all applications for Hackathon 2026
print("\n=== All applications for Hackathon 2026 ===")
cur.execute("""
    SELECT c.first_name, c.last_name, c.email, a.status, a.gwc_interview_result, a.gwc_interview_score
    FROM candidates c
    JOIN applications a ON a.candidate_id = c.id
    JOIN jobs j ON a.job_id = j.id
    WHERE j.title = 'Hackathon 2026'
    ORDER BY c.first_name
""")
for r in cur.fetchall():
    print(r)

# Check unique gwc_interview_result values
print("\n=== Unique GWC interview result values ===")
cur.execute("SELECT DISTINCT gwc_interview_result FROM applications WHERE gwc_interview_result IS NOT NULL")
for r in cur.fetchall():
    print(r)

# Check unique statuses for Hackathon 2026
print("\n=== Unique statuses for Hackathon 2026 ===")
cur.execute("""
    SELECT DISTINCT a.status
    FROM applications a
    JOIN jobs j ON a.job_id = j.id
    WHERE j.title = 'Hackathon 2026'
""")
for r in cur.fetchall():
    print(r)

conn.close()
