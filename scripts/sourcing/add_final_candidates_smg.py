"""
Add final batch of candidates to SMG sheet - focus on 4-6 years mid-level
"""

import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime
import json

TOKEN_FILE = '.claude/config/token_sheets_broad.json'
SHEET_ID = '1mLn1PihtN7UXWfYB8mX6RikDn9pa3oeifnQe25HeU44'

print("\n" + "="*80)
print("Adding FINAL Batch of 4-6 Year Mid-Level Candidates")
print("="*80)

# Load broader-scoped credentials
with open(TOKEN_FILE, 'r') as f:
    token_data = json.load(f)

credentials = Credentials.from_authorized_user_info(token_data)
if credentials.expired:
    credentials.refresh(Request())

gc = gspread.Client(auth=credentials)

# FINAL BATCH - Strict 4-6 Years, Mid-Level Focus
FINAL_BATCH = [
    # British Council education partnerships
    ('Muhammad Imran Khan', 'https://www.linkedin.com/in/muhammad-imran-khan-a788a826/', 'Account Manager', 'British Council', 'Karachi', '5-6 years', 'Education account management, institutional partnerships, stakeholder relations', 'British Council education sector, account management experience', 'Tier 1 - Education Sector'),

    # Fintech/startup partnerships - mid-level
    ('Nauman Khan', 'https://www.linkedin.com/in/nauman-khan-9a826973/', 'Project & Partnerships Manager', 'Multiple Fintech/Startups', 'Pakistan', '4-5 years', 'Fintech partnerships, platform growth, startups ecosystem, certified scrum', 'Fintech/startup partnerships builder, growth focus', 'Tier 1 - Fintech Partnerships'),

    # Banking relationship managers - 4-5 years only
    ('Safeer Ahmad', 'https://www.linkedin.com/in/safeer-ahmad-7676a156/', 'Relationship Manager', 'Mobilink Microfinance Bank Limited', 'Pakistan', '5-6 years', 'Retail banking relationships, stakeholder management, channel partnerships', 'Fintech/microfinance retail expansion, relationship building', 'Tier 2 - Banking Partnerships'),

    ('Mahvish Zaheer', 'https://www.linkedin.com/in/mahvish-zaheer-689a95178/', 'Relationship Manager', 'Faysal Bank Limited', 'Pakistan', '5-6 years', 'Banking partnerships, corporate account management, stakeholder relations', 'Banking sector partnership experience, relationship focus', 'Tier 2 - Banking Relationships'),

    # Zindagi Trust connections (education nonprofit)
    ('Zafar Masud', 'https://www.linkedin.com/in/zafarmasud/', 'Partnerships Coordinator', 'Pakistan Banks Association / Education Initiatives', 'Pakistan', '5-6 years', 'Education partnerships, financial sector collaboration, institutional engagement', 'Banking-education sector bridge, partnership coordination', 'Tier 2 - Education-Finance Bridge'),
]

try:
    print("\n[STEP 1] Opening SMG sheet...")
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.get_worksheet(0)
    print(f"[OK] Sheet opened")

    # Get current count before adding
    all_rows_before = ws.get_all_values()
    count_before = len(all_rows_before) - 1

    print(f"\n[STEP 2] Adding {len(FINAL_BATCH)} final candidates...")
    for candidate in FINAL_BATCH:
        row = list(candidate) + ['Identified', '', '', datetime.now().strftime('%Y-%m-%d')]
        ws.append_row(row)
        print(f"  [OK] {candidate[0]} ({candidate[2]})")

    # Get updated count
    all_rows_after = ws.get_all_values()
    count_after = len(all_rows_after) - 1

    print("\n" + "="*80)
    print("[SUCCESS] SMG SHEET UPDATED - MID-LEVEL FOCUS")
    print("="*80)
    print(f"\nSheet: Senior Manager Growth - Candidates IMPROVED")
    print(f"Link: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    print(f"\nCandidates Added This Batch: {len(FINAL_BATCH)}")
    print(f"Total Candidates: {count_after}")
    print(f"\nComposition:")
    print(f"  - 4-6 years experience (MID-LEVEL)")
    print(f"  - Education sector partnerships (British Council, Zindagi Trust)")
    print(f"  - Fintech/banking partnerships (Mobilink, Faysal, fintech startups)")
    print(f"  - Startup ecosystem partnerships")
    print(f"\nKey Baseline: Basit Hussain (LUMS Partnerships Specialist) - your preferred profile")
    print(f"\nNext: Review sheet, shortlist for DM outreach")

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
