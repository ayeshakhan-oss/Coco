import psycopg2
import json

conn = psycopg2.connect(
    host='ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech',
    dbname='neondb',
    user='neondb_owner',
    password='npg_kBQ10OASHEmd',
    sslmode='require'
)
cur = conn.cursor()

# Fetch candidates with GWC scorecard (gwc_scorecard is not null)
# who are NOT hired
cur.execute("""
    SELECT
        c.first_name,
        c.last_name,
        c.email,
        a.status,
        a.gwc_scorecard
    FROM candidates c
    JOIN applications a ON a.candidate_id = c.id
    JOIN jobs j ON a.job_id = j.id
    WHERE j.title = 'Hackathon 2026'
      AND a.gwc_scorecard IS NOT NULL
      AND a.status NOT IN ('hired')
    ORDER BY c.first_name
""")

rows = cur.fetchall()
print(f"\nFound {len(rows)} candidates with GWC scorecard but not hired for Hackathon 2026:\n")

for r in rows:
    first_name, last_name, email, status, gwc_scorecard = r
    print(f"{first_name} {last_name}")
    print(f"  Email: {email}")
    print(f"  Status: {status}")
    if gwc_scorecard:
        try:
            scorecard = json.loads(gwc_scorecard) if isinstance(gwc_scorecard, str) else gwc_scorecard
            print(f"  GWC Data: {json.dumps(scorecard, indent=2)[:200]}...")
        except:
            print(f"  GWC Data: (could not parse)")
    print()

conn.close()
