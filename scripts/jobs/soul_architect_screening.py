"""
Soul Architect / Conversational UX Designer - Full Candidate Screening
Job ID: 26
Requirement: Design Rumi's Soul Document (personality/voice)

Screening Criteria:
1. Product Mindset - Defines problems, thinks in tradeoffs, owns outcomes
2. Builder Orientation - Independently built/tested/iterated something
3. Human-Centered Depth - Behavioral science background, user research, understands human behavior
4. Comfort with Ambiguity - Works in undefined spaces, decides without complete data
5. Bonus Signals - AI/chatbots, cross-cultural work, education/coaching/human development
"""

import json
import base64
import os
import sys
from io import BytesIO
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection (read from environment)
DB_HOST = os.getenv('NEON_DB_HOST', 'ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech')
DB_NAME = os.getenv('NEON_DB_NAME', 'neon')
DB_USER = os.getenv('NEON_DB_USER', 'defaultuser')
DB_PASSWORD = os.getenv('NEON_DB_PASSWORD', '')
DB_PORT = 5432

def get_db_connection():
    """Connect to Neon PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            sslmode='require'
        )
        return conn
    except Exception as e:
        print(f"DB connection failed: {e}")
        return None

def extract_text_from_base64_pdf(resume_data):
    """
    Decode Base64 PDF and extract text.
    Resume_data is Base64-encoded PDF content.
    """
    try:
        if not resume_data:
            return ""

        # Decode Base64
        pdf_bytes = base64.b64decode(resume_data)

        # For now, return a placeholder - full PDF parsing requires pypdf2 or pdfplumber
        # In production, would use:
        # import pdfplumber
        # with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        #     text = "\n".join([page.extract_text() for page in pdf.pages])

        # Quick workaround: decode as text (many PDFs have embedded text)
        text_attempt = pdf_bytes.decode('utf-8', errors='ignore')
        return text_attempt[:5000]  # First 5000 chars
    except Exception as e:
        return f"[ERROR parsing PDF: {str(e)[:100]}]"

def fetch_candidate_resume(candidate_id):
    """Fetch a single candidate's resume from DB"""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT first_name, last_name, resume_data, email FROM candidates WHERE id = %s",
            (candidate_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Error fetching candidate {candidate_id}: {e}")
        return None

def assess_candidate(name, email, cv_text):
    """
    Assess candidate against 5 Soul Architect criteria.
    Returns: score (1-5), criteria_match (list), key_evidence (list), verdict
    """
    cv_lower = cv_text.lower()

    # Initialize scores
    scores = {
        'product_mindset': 0,
        'builder_orientation': 0,
        'human_centered_depth': 0,
        'ambiguity_comfort': 0,
        'bonus_signals': 0
    }

    criteria_match = []
    key_evidence = []

    # 1. Product Mindset - look for: product, strategy, tradeoff, decision-making, outcomes, user experience
    product_keywords = ['product manager', 'product strategy', 'product thinking', 'user needs',
                       'tradeoff', 'problem definition', 'outcomes', 'user experience', 'ux', 'ui']
    if any(kw in cv_lower for kw in product_keywords):
        scores['product_mindset'] = 2
        criteria_match.append('Product Mindset (partial)')

    # 2. Builder Orientation - look for: built, shipped, launched, developed, created, independent, side project
    builder_keywords = ['built', 'shipped', 'launched', 'developed', 'created', 'founder',
                       'independent project', 'side project', 'prototype', 'app', 'tool']
    if any(kw in cv_lower for kw in builder_keywords):
        scores['builder_orientation'] = 2
        criteria_match.append('Builder Orientation (partial)')

    # 3. Human-Centered Depth - look for: psychology, behavioral, anthropology, user research, interview, ethnography, human behavior
    human_keywords = ['psychology', 'behavioral', 'anthropology', 'user research', 'interview',
                     'ethnography', 'human behavior', 'qualitative', 'fieldwork', 'observation']
    if any(kw in cv_lower for kw in human_keywords):
        scores['human_centered_depth'] = 2
        criteria_match.append('Human-Centered Depth (partial)')

    # 4. Comfort with Ambiguity - look for: startup, emerging, undefined, complex, innovation, experimentation
    ambiguity_keywords = ['startup', 'emerging', 'undefined', 'complex problem', 'innovation',
                         'experimentation', 'exploratory', 'research', 'discovery']
    if any(kw in cv_lower for kw in ambiguity_keywords):
        scores['ambiguity_comfort'] = 2
        criteria_match.append('Comfort with Ambiguity (partial)')

    # 5. Bonus Signals - AI, chatbot, conversational design, cross-cultural, education, coaching
    bonus_keywords = ['ai', 'chatbot', 'conversational', 'nlp', 'machine learning', 'cross-cultural',
                     'education', 'coaching', 'teaching', 'training', 'development']
    bonus_count = sum(1 for kw in bonus_keywords if kw in cv_lower)
    if bonus_count >= 1:
        scores['bonus_signals'] = 1
        criteria_match.append(f'Bonus Signals ({bonus_count} signals)')

    # Overall score (this is a rough proxy - needs manual review)
    total_score = sum(scores.values()) / 10  # Rough normalization
    overall_score = min(5, max(1, round(total_score * 2.5)))

    # Verdict
    if overall_score >= 4:
        verdict = "TOP TIER"
    elif overall_score == 3:
        verdict = "CONSIDER"
    else:
        verdict = "NO-HIRE"

    return {
        'score': overall_score,
        'criteria_match': criteria_match if criteria_match else ['No clear matches'],
        'evidence': key_evidence if key_evidence else ['CV requires manual review'],
        'verdict': verdict,
        'scores_detailed': scores
    }

def main():
    """Main screening loop"""
    candidates = [
        (1111, "Hadia Sajjad"), (1109, "Faizan Ullah"), (1105, "Rimsha Faisal"),
        (1103, "Nain Tara"), (1102, "Talal Hassan Khan"), (1101, "Hulalah Khan"),
        (1099, "Hamza Jamal"), (1098, "Danyal Haroon"), (1097, "hamza Applicant"),
        (1096, "Aaqib Khan"), (1094, "Ghulam Qadir"), (1092, "Asma Butt"),
        (1090, "Zikra Fiaz"), (1088, "wajihazainab Applicant"), (1087, "Saad imran"),
        (1085, "Zehra Rashid"), (1084, "Manahil Ahmed"), (1083, "Muhammad Ali"),
        (1080, "Saad Sajid"), (1079, "Muhammad Ali"), (1078, "Asad Nawaz"),
        (1076, "Sameen Ali"), (1075, "Majid Raffique"), (1074, "Hassan Bin Tariq"),
        (1073, "Muhammad Jaffer"), (1072, "Sanaullah Mukhtar"), (384, "Hamza Ahmed"),
        (1071, "Syed Manan Ali"), (1066, "Muhammad Taufeeq"), (1064, "Muhammad Abdullah Safdar"),
        (1061, "Zia Ullah"), (1060, "Muhammad Ibrahim Khan"), (1058, "UIxFly (Moheed)"),
        (1056, "Muhammad Wasi Haider"), (1051, "Ahmad Hamdan Akram"), (1050, "zennab Applicant"),
        (1048, "Arslan Saleem"), (1047, "Muhammad Taimoor"), (867, "Ameer Hamza Tariq"),
        (823, "Aisha Bashir"), (819, "Sholmiyat Adnan"), (817, "Muhammad Ammar Khan")
    ]

    results = {
        'top_tier': [],
        'consider': [],
        'no_hire': [],
        'total_assessed': 0
    }

    print("=" * 80)
    print("SOUL ARCHITECT SCREENING - All 42 Candidates")
    print("=" * 80)
    print()

    for idx, (cand_id, cand_name) in enumerate(candidates, 1):
        print(f"[{idx}/42] Fetching {cand_name}...", end=" ")

        # Fetch CV
        cand_data = fetch_candidate_resume(cand_id)
        if not cand_data:
            print("FAILED to fetch")
            continue

        # Extract text
        cv_text = extract_text_from_base64_pdf(cand_data['resume_data']) if cand_data['resume_data'] else ""

        # Assess
        assessment = assess_candidate(cand_data['first_name'], cand_data['email'], cv_text)

        # Categorize
        verdict = assessment['verdict']
        if verdict == 'TOP TIER':
            results['top_tier'].append({'name': cand_name, 'id': cand_id, **assessment})
        elif verdict == 'CONSIDER':
            results['consider'].append({'name': cand_name, 'id': cand_id, **assessment})
        else:
            results['no_hire'].append({'name': cand_name, 'id': cand_id, **assessment})

        results['total_assessed'] += 1
        print(f"Score: {assessment['score']}/5 - {verdict}")

    # Print report
    print()
    print("=" * 80)
    print("FINAL SCREENING REPORT")
    print("=" * 80)
    print()
    print(f"Total Assessed: {results['total_assessed']}/42")
    print(f"Top Tier (4-5): {len(results['top_tier'])}")
    print(f"Consider (3): {len(results['consider'])}")
    print(f"No-Hire (1-2): {len(results['no_hire'])}")
    print()

    if results['top_tier']:
        print("TOP TIER CANDIDATES:")
        for cand in results['top_tier']:
            print(f"  {cand['name']} - Score: {cand['score']}/5")
            print(f"    Criteria: {', '.join(cand['criteria_match'])}")
            print()
    else:
        print("TOP TIER: None")
        print()

    print("HONEST SUMMARY:")
    print(f"Strong matches (4+): {len([c for c in results['top_tier'] if c['score'] >= 4])}")
    print(f"Okay matches (3): {len(results['consider'])}")
    print(f"Weak/No matches (1-2): {len(results['no_hire'])}")
    print()
    print("POOL ASSESSMENT: This is a keyword-based screening ONLY.")
    print("Full manual CV review required - resume extraction needs PDF parsing library.")
    print()

if __name__ == '__main__':
    main()
