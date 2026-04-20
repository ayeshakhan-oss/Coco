"""
Soul Architect / Conversational UX Designer (Job 26)
Batch Screening with Progress Tracking
Processes candidates in batches, extracts CVs, scores against 5 criteria
"""

import os, sys, base64, io, re, json
import psycopg2
from datetime import datetime

DB_CONN = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

def parse_pdf_bytes(pdf_bytes, timeout_secs=10):
    """Extract text from PDF with PyPDF2 (no OCR for speed)"""
    text = ""
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    except Exception as e:
        return f"[PDF parse error: {str(e)[:30]}]"
    return text.strip()


def assess_candidate(cv_text, name):
    """Score against 5 Soul Architect criteria"""
    cv_lower = cv_text.lower()
    score = 0
    criteria_met = []

    # 1. Product Mindset
    product_signals = [
        'product', 'problem', 'tradeoff', 'owned', 'outcome', 'strategy',
        'define.*problem', 'business requirement', 'go-to-market', 'vision'
    ]
    product_count = sum(1 for sig in product_signals if re.search(sig, cv_lower))
    if product_count >= 2:
        score += 1.5
        criteria_met.append('Product Mindset')

    # 2. Builder Orientation
    builder_signals = [
        'built', 'shipped', 'launched', 'developed', 'created', 'independent',
        'freelance', 'founder', 'startup', 'side project'
    ]
    builder_count = sum(1 for sig in builder_signals if re.search(sig, cv_lower))
    if builder_count >= 2:
        score += 1.5
        criteria_met.append('Builder Orientation')

    # 3. Human-Centered Depth
    human_signals = [
        'psychology', 'behavioral', 'anthropology', 'user research', 'qualitative',
        'ethnograph', 'hci', 'user interview', 'user testing'
    ]
    human_count = sum(1 for sig in human_signals if re.search(sig, cv_lower))
    if human_count >= 1:
        score += 1
        criteria_met.append('Human-Centered Depth')

    # 4. Ambiguity Comfort
    ambiguity_signals = [
        'startup', 'emerging', 'undefined', 'innovation', 'exploration',
        'experimentation', 'research'
    ]
    ambiguity_count = sum(1 for sig in ambiguity_signals if re.search(sig, cv_lower))
    if ambiguity_count >= 1:
        score += 0.5
        criteria_met.append('Ambiguity Comfort')

    # 5. Bonus Signals
    bonus_signals = [
        'ai', 'chatbot', 'conversational', 'education', 'coaching', 'cross-cultural'
    ]
    bonus_count = sum(1 for sig in bonus_signals if re.search(sig, cv_lower))
    if bonus_count >= 1:
        score += 0.5
        criteria_met.append('Bonus Signals')

    # Verdict (use dict keys, not display names)
    if score >= 3.5:
        verdict = "TOP_TIER"
    elif score >= 2.5:
        verdict = "CONSIDER"
    elif score >= 1:
        verdict = "MAYBE"
    else:
        verdict = "NO_HIRE"

    return round(score, 1), criteria_met, verdict


def main():
    print("=" * 80)
    print("SOUL ARCHITECT SCREENING — BATCH PROCESSING")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()

    # Fetch all 42 candidates
    cur.execute("""
        SELECT a.id, a.candidate_id, c.resume_data, c.first_name, c.last_name
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = 26
        ORDER BY a.id
    """)
    rows = cur.fetchall()
    print(f"Total candidates: {len(rows)}\n")

    results = {'TOP_TIER': [], 'CONSIDER': [], 'MAYBE': [], 'NO_HIRE': []}
    processed = 0
    no_cv = 0
    failed = 0

    for i, (app_id, cand_id, resume_b64, fname, lname) in enumerate(rows, 1):
        name = f"{fname} {lname}"
        print(f"[{i:2d}/42] {name:35s}", end=" ", flush=True)

        if not resume_b64:
            print("NO CV")
            results['NO_HIRE'].append({
                'id': cand_id, 'name': name, 'score': 0,
                'verdict': 'NO_HIRE', 'reason': 'No CV data'
            })
            no_cv += 1
            continue

        try:
            pdf_bytes = base64.b64decode(resume_b64)
            cv_text = parse_pdf_bytes(pdf_bytes)
        except Exception as e:
            print(f"FAILED: {str(e)[:20]}")
            failed += 1
            continue

        if not cv_text.strip() or len(cv_text) < 50:
            print("UNREADABLE")
            results['NO_HIRE'].append({
                'id': cand_id, 'name': name, 'score': 0,
                'verdict': 'NO_HIRE', 'reason': 'CV unreadable'
            })
            continue

        # Score
        score, criteria, verdict = assess_candidate(cv_text, name)
        results[verdict].append({
            'id': cand_id, 'name': name, 'score': score,
            'verdict': verdict, 'criteria': criteria
        })
        processed += 1

        # Print verdict (display names)
        display_verdict = verdict.replace('_', ' ')
        print(f"{display_verdict} ({score})")

        # Save progress every 10
        if i % 10 == 0:
            with open(r"c:\Agent Coco\soul_architect_results_partial.json", 'w') as f:
                json.dump(results, f, indent=2)
            print(f"  [Progress saved at {i}/42]\n")

    # Final save
    with open(r"c:\Agent Coco\soul_architect_results_final.json", 'w') as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    print(f"Processed: {processed} | Failed: {failed} | No CV: {no_cv}")
    print(f"Top Tier: {len(results['TOP_TIER'])} | Consider: {len(results['CONSIDER'])} | "
          f"Maybe: {len(results['MAYBE'])} | No-Hire: {len(results['NO_HIRE'])}")

    # Top tier summary
    if results['TOP_TIER']:
        print("\nTOP TIER CANDIDATES:")
        for r in results['TOP_TIER']:
            print(f"  {r['name']} (ID: {r['id']}) — Score: {r['score']}/5")
            print(f"    Criteria: {', '.join(r['criteria'])}")

    print("\n" + "=" * 80)
    print(f"Results saved to: c:\\Agent Coco\\soul_architect_results_final.json")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    conn.close()


if __name__ == '__main__':
    main()
