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

target_names = ['Moaz Nadeem', 'Umair Solangi', 'Ali Jawad', 'Maryam Rafaqat']

for target in target_names:
    first, last = target.split()

    cur.execute("""
        SELECT
            c.id,
            c.first_name,
            c.last_name,
            c.email,
            a.id as app_id,
            a.gwc_scorecard,
            a.gwc_interview_score,
            a.case_study_score,
            a.case_study_notes,
            a.panel_feedback,
            a.values_scorecard
        FROM candidates c
        JOIN applications a ON a.candidate_id = c.id
        JOIN jobs j ON a.job_id = j.id
        WHERE j.title = 'Hackathon 2026'
          AND LOWER(c.first_name) = LOWER(%s)
          AND LOWER(c.last_name) = LOWER(%s)
    """, (first, last))

    row = cur.fetchone()
    if row:
        cand_id, first_name, last_name, email, app_id, gwc_scorecard, gwc_score, case_study_score, case_study_notes, panel_feedback, values_scorecard = row

        print(f"\n=== {first_name} {last_name} ===")
        print(f"Email: {email}")
        print(f"GWC Interview Score: {gwc_score}")
        print(f"Case Study Score: {case_study_score}")

        if gwc_scorecard:
            try:
                scorecard = json.loads(gwc_scorecard) if isinstance(gwc_scorecard, str) else gwc_scorecard
                print(f"GWC Scorecard Summary:")
                for key, val in scorecard.items():
                    if key not in ['name', 'peer'] and isinstance(val, dict):
                        yes_count = sum(1 for v in val.values() if v == 'Yes')
                        print(f"  {key}: {yes_count}/3 Yes")
            except Exception as e:
                print(f"Could not parse GWC scorecard: {e}")

        if case_study_notes:
            print(f"Case Study Notes: {case_study_notes[:200]}")

        if panel_feedback:
            try:
                feedback = json.loads(panel_feedback) if isinstance(panel_feedback, str) else panel_feedback
                print(f"Panel Feedback: {json.dumps(feedback, indent=2)[:300]}")
            except:
                print(f"Panel Feedback: (raw data)")

conn.close()
