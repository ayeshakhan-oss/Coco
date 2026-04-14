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

# Fetch candidates with GWC scorecard but not hired
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
print(f"\n=== GWC Status for Hackathon 2026 (Not Hired) ===\n")

gwc_passed = []
gwc_failed = []

for r in rows:
    first_name, last_name, email, status, gwc_scorecard = r

    try:
        scorecard = json.loads(gwc_scorecard) if isinstance(gwc_scorecard, str) else gwc_scorecard

        # Determine pass/fail based on scorecard
        get_it_answers = scorecard.get('getIt', {})
        want_it_answers = scorecard.get('wantIt', {})
        capacity_answers = scorecard.get('capacity', {})

        # Count Yes answers
        get_it_count = sum(1 for v in get_it_answers.values() if v == 'Yes')
        want_it_count = sum(1 for v in want_it_answers.values() if v == 'Yes')
        capacity_count = sum(1 for v in capacity_answers.values() if v == 'Yes')

        # Show details
        cand_name = f"{first_name} {last_name}"
        print(f"{cand_name} ({email})")
        print(f"  Status: {status}")
        print(f"  Get It: {get_it_count}/3 Yes")
        print(f"  Want It: {want_it_count}/3 Yes")
        print(f"  Capacity: {capacity_count}/3 Yes")

        # Determine pass (all 3 must have at least 2/3 Yes, or all Yes)
        if get_it_count == 3 and want_it_count == 3 and capacity_count == 3:
            print(f"  Result: GWC PASSED ✓")
            gwc_passed.append((cand_name, email, status))
        else:
            print(f"  Result: GWC FAILED ✗")
            gwc_failed.append((cand_name, email, status))
        print()
    except Exception as e:
        print(f"Error parsing {first_name} {last_name}: {e}\n")

print(f"\n=== SUMMARY ===")
print(f"GWC Passed but not hired: {len(gwc_passed)}")
for name, email, status in gwc_passed:
    print(f"  - {name} ({status})")

print(f"\nGWC Failed or Rejected: {len(gwc_failed)}")
for name, email, status in gwc_failed:
    print(f"  - {name} ({status})")

conn.close()
