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

# Get ALL candidates with GWC scorecard for Hackathon 2026
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
    ORDER BY c.first_name
""")

rows = cur.fetchall()
print(f"All candidates with GWC scorecard for Hackathon 2026:\n")

for r in rows:
    first_name, last_name, email, status, gwc_scorecard = r

    try:
        scorecard = json.loads(gwc_scorecard) if isinstance(gwc_scorecard, str) else gwc_scorecard
        get_it = sum(1 for v in scorecard.get('getIt', {}).values() if v == 'Yes')
        want_it = sum(1 for v in scorecard.get('wantIt', {}).values() if v == 'Yes')
        capacity = sum(1 for v in scorecard.get('capacityToDoIt', {}).values() if v == 'Yes')

        # Determine if passed (need strong scores on all dimensions)
        overall = f"Get:{get_it}/3 Want:{want_it}/3 Cap:{capacity}/3"
        print(f"{first_name} {last_name} ({email})")
        print(f"  Status: {status}")
        print(f"  Scores: {overall}")
        print()
    except Exception as e:
        print(f"Error with {first_name} {last_name}: {e}\n")

conn.close()
