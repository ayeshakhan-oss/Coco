import psycopg2

conn = psycopg2.connect(
    host='ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech',
    dbname='neondb',
    user='neondb_owner',
    password='npg_kBQ10OASHEmd',
    sslmode='require'
)
cur = conn.cursor()

target_names = ['Moaz Nadeem', 'Alishba Ramzan', 'Umair Solangi', 'Ali Jawad', 'Maryam Rafaqat', 'Sultan Muhammad Hamad Sheharyar']

for target in target_names:
    parts = target.split()
    first = parts[0]
    last = ' '.join(parts[1:])

    cur.execute("""
        SELECT c.first_name, c.last_name, c.email, a.id as app_id
        FROM candidates c
        JOIN applications a ON a.candidate_id = c.id
        JOIN jobs j ON a.job_id = j.id
        WHERE j.title = 'Hackathon 2026'
          AND LOWER(c.first_name) = LOWER(%s)
          AND LOWER(c.last_name) = LOWER(%s)
    """, (first, last))

    row = cur.fetchone()
    if row:
        first_name, last_name, email, app_id = row
        print(f'"{first_name} {last_name}": {{ "email": "{email}", "app_id": {app_id} }},')

conn.close()
