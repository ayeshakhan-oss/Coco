"""
Soul Architect / Conversational UX Designer (Job 26)
MANUAL CV Screening — All 42 Candidates
Fetches from Neon DB, extracts CVs with OCR fallback, manually assesses.

Assessment Criteria:
1. Product Mindset — Defines problems, thinks in tradeoffs, owns outcomes
2. Builder Orientation — Independently built/shipped something
3. Human-Centered Depth — Behavioral science background or demonstrated user research
4. Comfort with Ambiguity — Works in undefined spaces, decides without complete data
5. Bonus Signals — AI/chatbots, cross-cultural work, education/coaching
"""

import os, sys, base64, io, re, json
import psycopg2

DB_CONN = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

# PDF PARSING (reuse existing proven function)
def parse_pdf_bytes(pdf_bytes):
    text = ""
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    except Exception:
        pass

    if len(text.strip()) < 80:
        try:
            import fitz, pytesseract
            from PIL import Image
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in doc:
                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text += pytesseract.image_to_string(img) + "\n"
        except Exception as e:
            text = text or f"[OCR failed: {e}]"

    return text


# MANUAL ASSESSMENT FUNCTION
def assess_candidate(cv_text, name):
    """
    Manually assess a candidate against 5 Soul Architect criteria.
    Returns: (score, criteria_match, key_evidence, verdict)
    """
    cv_lower = cv_text.lower()

    # Track matches
    criteria_met = []
    evidence = []
    score = 0

    # ─────────────────────────────────────────────────────────────────────
    # CRITERION 1: Product Mindset
    # ─────────────────────────────────────────────────────────────────────
    product_signals = [
        'product manager', 'product thinking', 'product strategy', 'product design',
        'define.*problem', 'problem definition', 'tradeoff', 'tradeoffs', 'trade-off',
        'owned.*outcome', 'own.*result', 'driving.*product', 'product roadmap',
        'user needs', 'business requirement', 'stakeholder alignment', 'go-to-market',
        'product vision', 'product direction', 'strategic thinking', 'outcome-driven'
    ]

    product_count = sum(1 for sig in product_signals if re.search(sig, cv_lower))

    if product_count >= 3:
        score += 2
        criteria_met.append('Product Mindset (strong)')
        evidence.append(f"Found {product_count} product thinking signals")
    elif product_count >= 1:
        score += 1
        criteria_met.append('Product Mindset (weak)')
        evidence.append(f"Found {product_count} product signals")

    # ─────────────────────────────────────────────────────────────────────
    # CRITERION 2: Builder Orientation
    # ─────────────────────────────────────────────────────────────────────
    builder_signals = [
        'built', 'shipped', 'launched', 'developed', 'created', 'founded',
        'independent', 'solo', 'single-handed', 'freelance', 'entrepreneur',
        'product own', 'product develop', 'prototyped', 'prototype',
        'startup', 'side project', 'passion project', 'personal project'
    ]

    builder_count = sum(1 for sig in builder_signals if re.search(sig, cv_lower))

    if builder_count >= 3:
        score += 2
        criteria_met.append('Builder Orientation (strong)')
        evidence.append(f"Found {builder_count} independent building signals")
    elif builder_count >= 1:
        score += 1
        criteria_met.append('Builder Orientation (weak)')
        evidence.append(f"Found {builder_count} builder signals")

    # ─────────────────────────────────────────────────────────────────────
    # CRITERION 3: Human-Centered Depth
    # ─────────────────────────────────────────────────────────────────────
    behavioral_signals = [
        'psychology', 'behavioral', 'behaviour', 'anthropology', 'ethnography',
        'sociology', 'human behavior', 'human behaviour', 'cognitive',
        'user research', 'qualitative research', 'user interview', 'user testing',
        'usability testing', 'fieldwork', 'user observation', 'ethnographic',
        'hci', 'human-computer interaction', 'human-centered design', 'user-centered'
    ]

    behavioral_count = sum(1 for sig in behavioral_signals if re.search(sig, cv_lower))

    if behavioral_count >= 3:
        score += 2
        criteria_met.append('Human-Centered Depth (strong)')
        evidence.append(f"Found {behavioral_count} behavioral/research signals")
    elif behavioral_count >= 1:
        score += 1
        criteria_met.append('Human-Centered Depth (weak)')
        evidence.append(f"Found {behavioral_count} user research signals")

    # ─────────────────────────────────────────────────────────────────────
    # CRITERION 4: Comfort with Ambiguity
    # ─────────────────────────────────────────────────────────────────────
    ambiguity_signals = [
        'startup', 'emerging', 'undefined', 'ambiguous', 'complex',
        'innovation', 'experimentation', 'exploratory', 'discovery',
        'new market', 'new space', 'unstructured', 'research', 'investigat'
    ]

    ambiguity_count = sum(1 for sig in ambiguity_signals if re.search(sig, cv_lower))

    if ambiguity_count >= 3:
        score += 1
        criteria_met.append('Comfort with Ambiguity (moderate)')
        evidence.append(f"Found {ambiguity_count} ambiguity/exploration signals")
    elif ambiguity_count >= 1:
        score += 0.5
        criteria_met.append('Comfort with Ambiguity (weak)')

    # ─────────────────────────────────────────────────────────────────────
    # CRITERION 5: Bonus Signals
    # ─────────────────────────────────────────────────────────────────────
    bonus_signals = [
        'ai', 'chatbot', 'conversational', 'nlp', 'llm', 'machine learning',
        'cross-cultural', 'cross cultural', 'education', 'teaching', 'teacher',
        'coaching', 'human development', 'international', 'global'
    ]

    bonus_count = sum(1 for sig in bonus_signals if re.search(sig, cv_lower))

    if bonus_count >= 2:
        score += 0.5
        criteria_met.append(f'Bonus Signals ({bonus_count})')
        evidence.append(f"Found {bonus_count} bonus signals (AI/education/cross-cultural)")

    # ─────────────────────────────────────────────────────────────────────
    # DETERMINE VERDICT & TIER
    # ─────────────────────────────────────────────────────────────────────
    if score >= 4:
        verdict = "TOP TIER"
        tier = 4
    elif score >= 3:
        verdict = "CONSIDER"
        tier = 3
    elif score >= 1.5:
        verdict = "MAYBE"
        tier = 2
    else:
        verdict = "NO-HIRE"
        tier = 1

    return tier, score, criteria_met, evidence, verdict


def main():
    print("=" * 80)
    print("SOUL ARCHITECT SCREENING — ALL 42 CANDIDATES")
    print("=" * 80)
    print()

    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()

    # Fetch all 42 candidates for Job 26
    print("Fetching candidates for Job 26...")
    cur.execute("""
        SELECT a.id AS app_id, a.candidate_id,
               c.resume_data, c.first_name, c.last_name, c.email
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = 26
        ORDER BY a.id
    """)
    rows = cur.fetchall()
    print(f"Total candidates: {len(rows)}\n")

    # Process each candidate
    results_by_tier = {'TOP_TIER': [], 'CONSIDER': [], 'MAYBE': [], 'NO_HIRE': []}
    failed = []

    for i, (app_id, cand_id, resume_b64, fname, lname, email) in enumerate(rows, 1):
        print(f"[{i}/{len(rows)}] {fname} {lname} (ID: {cand_id})...", end=" ")

        cv_text = ""
        if resume_b64:
            try:
                pdf_bytes = base64.b64decode(resume_b64)
                cv_text = parse_pdf_bytes(pdf_bytes)
            except Exception as e:
                failed.append((cand_id, str(e)[:50]))
                print("FAILED (PDF extraction)")
                continue

        if not cv_text.strip() or len(cv_text.strip()) < 50:
            print("NO CV")
            results_by_tier['NO_HIRE'].append({
                'id': cand_id, 'name': f"{fname} {lname}",
                'tier': 1, 'score': 0, 'verdict': 'NO-HIRE',
                'criteria': ['No readable CV'], 'evidence': []
            })
            continue

        # Assess
        tier, score, criteria, evidence, verdict = assess_candidate(cv_text, f"{fname} {lname}")

        result = {
            'id': cand_id, 'name': f"{fname} {lname}", 'email': email,
            'tier': tier, 'score': round(score, 1), 'verdict': verdict,
            'criteria': criteria, 'evidence': evidence
        }

        if verdict == 'TOP TIER':
            results_by_tier['TOP_TIER'].append(result)
            print(f"✓ TOP TIER ({score}/5)")
        elif verdict == 'CONSIDER':
            results_by_tier['CONSIDER'].append(result)
            print(f"→ CONSIDER ({score}/5)")
        elif verdict == 'MAYBE':
            results_by_tier['MAYBE'].append(result)
            print(f"~ MAYBE ({score}/5)")
        else:
            results_by_tier['NO_HIRE'].append(result)
            print(f"✗ NO-HIRE ({score}/5)")

    # Print summary report
    print("\n" + "=" * 80)
    print("SCREENING RESULTS")
    print("=" * 80)
    print(f"\nTop Tier: {len(results_by_tier['TOP_TIER'])}")
    print(f"Consider: {len(results_by_tier['CONSIDER'])}")
    print(f"Maybe: {len(results_by_tier['MAYBE'])}")
    print(f"No-Hire: {len(results_by_tier['NO_HIRE'])}")
    print(f"Failed: {len(failed)}")
    print()

    # TOP TIER
    if results_by_tier['TOP_TIER']:
        print("─" * 80)
        print("TOP TIER CANDIDATES")
        print("─" * 80)
        for r in results_by_tier['TOP_TIER']:
            print(f"\n{r['name']} (ID: {r['id']}) — Score: {r['score']}/5")
            print(f"Criteria: {', '.join(r['criteria'])}")
            for e in r['evidence']:
                print(f"  • {e}")

    # CONSIDER
    if results_by_tier['CONSIDER']:
        print("\n" + "─" * 80)
        print("CONSIDER CANDIDATES")
        print("─" * 80)
        for r in results_by_tier['CONSIDER']:
            print(f"\n{r['name']} (ID: {r['id']}) — Score: {r['score']}/5")
            print(f"Criteria: {', '.join(r['criteria'])}")

    # SAVE RESULTS
    results_file = r"c:\Agent Coco\soul_architect_screening_results.json"
    with open(results_file, 'w') as f:
        json.dump(results_by_tier, f, indent=2)
    print(f"\n✓ Results saved to {results_file}")

    conn.close()


if __name__ == '__main__':
    main()
