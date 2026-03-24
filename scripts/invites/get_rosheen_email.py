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
    SELECT c.id, c.first_name, c.last_name, c.email, a.id as app_id, a.job_id
    FROM candidates c
    JOIN applications a ON a.candidate_id = c.id
    WHERE LOWER(c.first_name) LIKE '%rosheen%'
    OR LOWER(c.last_name) LIKE '%naeem%'
""")
rows = cur.fetchall()
for r in rows:
    print(r)

conn.close()
