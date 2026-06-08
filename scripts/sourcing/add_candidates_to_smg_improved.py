"""
Add newly scraped 4-6 year experience candidates to existing SMG sheet
Sheet ID: 1mLn1PihtN7UXWfYB8mX6RikDn9pa3oeifnQe25HeU44
"""

import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime
import json

TOKEN_FILE = '.claude/config/token_sheets_broad.json'
SHEET_ID = '1mLn1PihtN7UXWfYB8mX6RikDn9pa3oeifnQe25HeU44'

print("\n" + "="*80)
print("Adding NEW 4-6 Year Experience Candidates to SMG Sheet")
print("="*80)

# Load broader-scoped credentials
with open(TOKEN_FILE, 'r') as f:
    token_data = json.load(f)

credentials = Credentials.from_authorized_user_info(token_data)
if credentials.expired:
    credentials.refresh(Request())

gc = gspread.Client(auth=credentials)

# NEW CANDIDATES - 4-6 YEARS EXPERIENCE ONLY (corrected)
NEW_CANDIDATES = [
    # Tier 1: Mid-level partnerships/growth at target companies
    ('Adil Sattar', 'https://www.linkedin.com/in/adil-sattar/', 'Associate (Education & Skills)', 'British Asian Trust', 'Pakistan', '4-5 years', 'Education partnerships, skills development projects, institutional engagement', 'British Asian Trust education focus, mid-level partnerships specialist', 'Tier 1 - Mid-Level Match'),
    ('Khush Bakht Andleeb', 'https://www.linkedin.com/in/khush-bakht-andleeb-970130153/', 'Business Development Lead', 'Multi-sector', 'Pakistan', '4-5 years', 'Education/social development BD, bid development, M&E, research and development', 'Commonwealth 2020 graduate, mid-level BD experience, education focus', 'Tier 1 - Mid-Level Match'),
    ('Sarah Abbas', 'https://pk.linkedin.com/in/sarah-abbas-', 'Partnerships & Growth Professional', 'Pakistan Startup Ecosystem', 'Pakistan', '4-5 years', 'Startup partnerships, growth strategy, institutional engagement, campaign strategy', 'IBA graduate, partnerships/growth in startups, Dean\'s List', 'Tier 1 - Mid-Level Match'),
    ('Alisha Naqvi', 'https://www.linkedin.com/in/alishanaqvi/', 'Head of Partnerships', 'Karak With Mahreen', 'Turkey/Pakistan', '5-6 years', 'EdTech partnerships, education marketplace, stakeholder management', 'Partnerships lead at EdTech platform, 5+ years relevant experience', 'Tier 1 - Mid-Level Match'),

    # Tier 2: Associates/Coordinators in education/nonprofit
    ('Alisha Parikh', 'https://www.linkedin.com/in/parikhalisha/', 'Inclusive Quality Education Associate', 'Plan International USA', 'Pakistan', '4-5 years', 'Education program management, partnership coordination, community engagement', 'Plan International education focus, associate-level partnerships', 'Tier 2 - Associate Level'),
    ('Saad Hashmi', 'https://www.linkedin.com/in/saadahashmi/', 'Business Professional', 'VentureDive', 'Pakistan', '4-5 years', 'Tech/startup partnerships, business development, venture ecosystem', 'VentureDive startup experience, partnerships in innovation sector', 'Tier 2 - Startup Experience'),
    ('Shehzad Jeeva', 'https://www.linkedin.com/in/shehzad-jeeva/', 'Education Director', 'International Baccalaureate', 'Pakistan', '5-6 years', 'Education partnerships, institutional relations, curriculum development', 'IB director-level, education sector partnerships', 'Tier 2 - Education Focus'),

    # Tier 3: Based on Basit Hussain feedback (the one profile you liked)
    # Keeping Basit as anchor and finding similar LUMS/education partnership specialists
    ('Zahid Mushtaq', 'https://www.linkedin.com/in/zahid-mushtaq-a316463b/', 'Co-Founder & Business Development', 'Connect Professionally (CP)', 'Pakistan', '4-5 years', 'B2B partnerships, distribution channels, educational networking platform', 'Startup co-founder, B2B partnerships, education-adjacent', 'Tier 2 - Co-Founder BD'),
]

try:
    print("\n[STEP 1] Opening existing SMG sheet...")
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.get_worksheet(0)
    print(f"[OK] Sheet opened: {sh.title}")

    print(f"\n[STEP 2] Adding {len(NEW_CANDIDATES)} new candidates...")
    for candidate in NEW_CANDIDATES:
        row = list(candidate) + ['Identified', '', '', datetime.now().strftime('%Y-%m-%d')]
        ws.append_row(row)
        print(f"  [OK] Added: {candidate[0]}")

    print(f"\n[STEP 3] Getting updated row count...")
    all_rows = ws.get_all_values()
    total_candidates = len(all_rows) - 1  # Minus header row

    print("\n" + "="*80)
    print("[SUCCESS] NEW CANDIDATES ADDED")
    print("="*80)
    print(f"\nSheet: Senior Manager Growth - Candidates IMPROVED (2026-06-04)")
    print(f"Sheet Link: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    print(f"\nTotal Candidates Now: {total_candidates}")
    print(f"New Candidates Added: {len(NEW_CANDIDATES)}")
    print(f"\nFocus: 4-6 years experience, mid-level partnerships/growth specialists")
    print(f"Key Profile Match: Basit Hussain (LUMS Partnerships Specialist) ✓")

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
