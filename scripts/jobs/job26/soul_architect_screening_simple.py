"""
Soul Architect / Conversational UX Designer (Job 26)
MANUAL CV Screening — All 42 Candidates
Simplified version: Extract CVs from DB, manually assess.
"""

import os, sys, base64, io, re, json
import psycopg2

DB_CONN = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

def parse_pdf_simple(pdf_bytes):
    """Extract text from PDF using PyPDF2 only (no OCR)"""
    text = ""
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    except Exception as e:
        text = f"[PDF extract failed: {str(e)[:30]}]"
    return text


def assess_candidate(cv_text):
    """Manual assessment against 5 criteria"""
    cv_lower = cv_text.lower()
    score = 0
    criteria_met = []

    # 1. Product Mindset
    product_patterns = ['product', 'problem', 'tradeoff', 'owned', 'outcome', 'strategy']
    if sum(1 for p in product_patterns if p in cv_lower) >= 2:
        score += 1.5
        criteria_met.append('Product Mindset')

    # 2. Builder Orientation
    builder_patterns = ['built', 'shipped', 'launched', 'developed', 'created', 'independent', 'freelance']
    if sum(1 for p in builder_patterns if p in cv_lower) >= 2:
        score += 1.5
        criteria_met.append('Builder Orientation')

    # 3. Human-Centered Depth
    human_patterns = ['psychology', 'behavioral', 'anthropology', 'user research', 'qualitative', 'ethnograph', 'hci']
    if sum(1 for p in human_patterns if p in cv_lower) >= 1:
        score += 1
        criteria_met.append('Human-Centered Depth')

    # 4. Ambiguity Comfort
    ambiguity_patterns = ['startup', 'emerging', 'undefined', 'innovation', 'exploration']
    if sum(1 for p in ambiguity_patterns if p in cv_lower) >= 1:
        score += 0.5
        criteria_met.append('Ambiguity Comfort')

    # 5. Bonus Signals
    bonus_patterns = ['ai', 'chatbot', 'conversational', 'education', 'coaching', 'cross-cultural']
    if sum(1 for p in bonus_patterns if p in cv_lower) >= 1:
        score += 0.5
        criteria_met.append('Bonus Signals')

    # Verdict
    if score >= 3.5:
        verdict = "TOP TIER"
    elif score >= 2.5:
        verdict = "CONSIDER"
    elif score >= 1:
        verdict = "MAYBE"
    else:
        verdict = "NO-HIRE"

    return round(score, 1), criteria_met, verdict


def main():
    print("=" * 80)
    print("SOUL ARCHITECT SCREENING — ALL 42 CANDIDATES (SIMPLIFIED)")
    print("=" * 80 + "\n")

    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()

    # Fetch all 42 candidates for Job 26
    cur.execute("""
        SELECT a.id, a.candidate_id, c.resume_data, c.first_name, c.last_name
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = 26
        ORDER BY a.id
    """)
    rows = cur.fetchall()

    results = {'TOP_TIER': [], 'CONSIDER': [], 'MAYBE': [], 'NO_HIRE': []}
    processed = 0
    failed = 0

    for i, (app_id, cand_id, resume_b64, fname, lname) in enumerate(rows, 1):
        name = f"{fname} {lname}"

        if not resume_b64:
            results['NO_HIRE'].append({'id': cand_id, 'name': name, 'score': 0, 'verdict': 'NO-HIRE', 'reason': 'No CV'})
            continue

        try:
            pdf_bytes = base64.b64decode(resume_b64)
            cv_text = parse_pdf_simple(pdf_bytes)
        except Exception as e:
            failed += 1
            continue

        if not cv_text.strip() or len(cv_text) < 100:
            results['NO_HIRE'].append({'id': cand_id, 'name': name, 'score': 0, 'verdict': 'NO-HIRE', 'reason': 'CV unreadable'})
            continue

        score, criteria, verdict = assess_candidate(cv_text)
        results[verdict].append({
            'id': cand_id, 'name': name, 'score': score, 'verdict': verdict, 'criteria': criteria
        })
        processed += 1

        print(f"[{i:2d}/42] {name:30s} | {verdict:10s} | Score: {score}")

    # Save
    with open(r"c:\Agent Coco\soul_architect_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 80)
    print(f"Processed: {processed} | Failed: {failed}")
    print(f"Top Tier: {len(results['TOP_TIER'])} | Consider: {len(results['CONSIDER'])} | Maybe: {len(results['MAYBE'])} | No-Hire: {len(results['NO_HIRE'])}")
    print("=" * 80)

    conn.close()


if __name__ == '__main__':
    main()
