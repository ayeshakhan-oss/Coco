"""
Job 17 — CPD Coach
Filter: Female candidates who are TFP Fellows, not already hired.
Pulls directly from Neon DB, decodes PDFs, scans for TFP mentions.
"""

import base64
import re
import psycopg2

import fitz  # pymupdf

DB_URL = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

FEMALE_NAMES = {
    'ayesha','fatima','zainab','hira','sara','sana','nadia','amna','maryam','rabia',
    'khadija','asma','iqra','mahnoor','mehwish','nimra','saima','samia','sidra','sumera',
    'uzma','aliya','anam','bushra','farah','faria','farida','hafsa','hajra','huma',
    'iram','irum','javeria','kiran','laiba','lubna','madiha','maheen','maha','maria',
    'noor','noreen','ramsha','rida','rimsha','sadaf','safia','sahar','salma','saman',
    'samreen','shabana','shagufta','shaista','shazia','sobia','sumaira','sundas',
    'tayyaba','tooba','urooj','wardah','warda','yasmin','zahida','zara','zohra',
    'zunaira','naila','naima','nasreen','nosheen','rehana','robina','saadia','sabrina',
    'qurat','quratulain','palwasha','rukhsar','romaisa','aneesa','aneeqa','areeba',
    'arfa','arooj','asiya','bisma','dua','emaan','eman','erum','fiza','ghazal',
    'hadia','humera','ifra','iman','inaya','isha','jaweria','kinza','laraib','maira',
    'maleeha','maliha','mehreen','mishal','momina','munaza','muneeba','nabila',
    'naeema','natasha','nazia','neha','nida','rania','reema','rizwana','roohi',
    'sabeena','sadia','saeeda','samavia','sameen','sameera','samina','saniya',
    'sehrish','shahida','shamsa','shehla','shumaila','sibgha','soha','sumaiyya',
    'summaya','syeda','tahira','tania','tehreem','umama','umme','unsa','urwa',
    'ushna','wajeeha','yusra','zeba','zeenat','zimal','zobia','zoha','zoya',
    'zunera','kashmala','anmol','komal','sumbul','anum','ruba','alina','amara',
    'amreen','anila','ansa','aqsa','aroha','arwa','asna','azra','bareeha','barira',
    'dania','diba','esha','faiza','falak','farha','farwa','freeha','haleema','hina',
    'hoorain','humaira','ifza','iffat','irsa','isma','kainat','khansa','layla',
    'madeha','maham','maida','malak','mariam','marriam','mehak','muniba','nabiha',
    'nafeesa','najma','namra','naureen','nazish','pakeeza','pari','rafia','raheela',
    'rahila','razia','reeha','ruqaiya','sabreena','safinaz','saghar','sahira','saira',
    'saliha','samra','shaheena','shaheen','shahnaz','shanza','sheeza','sohaila',
    'somia','sonia','subhana','suha','summera','swera','tabinda','tanzeela','tehmina',
    'ulfat','unaiza','uroosa','vaneeza','wajiha','wareesha','yashfa','yumna','zakia',
    'zarqa','zehra','zikra','zobia','raheela',
}

TFP_PATTERNS = [
    r'teach\s+for\s+pakistan',
    r'tfp\s+fellow',
    r'fellow.*teach\s+for\s+pakistan',
    r'teach\s+for\s+pakistan.*fellow',
    r'\btfp\b',
]


def extract_text(pdf_bytes):
    text = ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        text = f"[ERROR: {e}]"
    return text.strip()


def is_tfp(text):
    t = text.lower()
    return any(re.search(p, t) for p in TFP_PATTERNS)


def main():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT ON (c.id)
            c.id as candidate_id,
            a.id as application_id,
            c.first_name, c.last_name,
            c.email, c.phone, c.location,
            c.resume_data,
            a.status, a.applied_at,
            a.values_interview_result
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = 17
          AND a.status != 'hired'
          AND c.resume_data IS NOT NULL
        ORDER BY c.id, a.applied_at DESC
    """)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    candidates = [dict(zip(cols, r)) for r in rows]
    cur.close()
    conn.close()

    print(f"Scanning {len(candidates)} unique candidates with resumes...\n")

    tfp_females = []

    for i, c in enumerate(candidates):
        fn = (c['first_name'] or '').strip().lower()
        if fn not in FEMALE_NAMES:
            continue

        try:
            pdf_bytes = base64.b64decode(c['resume_data'])
        except Exception:
            continue

        text = extract_text(pdf_bytes)
        full_name = f"{c['first_name']} {c['last_name']}".strip()
        print(f"[{i+1}] {full_name} — scanning...", end=" ")

        if is_tfp(text):
            print("TFP FOUND")
            tfp_females.append({
                'name': full_name,
                'email': c['email'],
                'phone': c['phone'],
                'location': c['location'] or 'N/A',
                'status': c['status'],
                'applied_at': str(c['applied_at'])[:10],
                'values_result': c['values_interview_result'] or 'N/A',
                'app_id': c['application_id'],
                'candidate_id': c['candidate_id'],
            })
        else:
            print("no TFP")

    print(f"\n{'='*60}")
    print(f"FEMALE TFP FELLOWS — CPD Coach (Job 17)")
    print(f"{'='*60}")
    if not tfp_females:
        print("None found.")
    for idx, r in enumerate(tfp_females, 1):
        print(f"\n#{idx} {r['name']}")
        print(f"   Location  : {r['location']}")
        print(f"   Email     : {r['email']}")
        print(f"   Phone     : {r['phone']}")
        print(f"   Applied   : {r['applied_at']}")
        print(f"   Status    : {r['status']}")
        print(f"   Values    : {r['values_result']}")
        print(f"   App ID    : {r['app_id']} | Candidate ID: {r['candidate_id']}")

    print(f"\nTotal: {len(tfp_females)} female TFP Fellow(s) found.")


if __name__ == '__main__':
    main()
