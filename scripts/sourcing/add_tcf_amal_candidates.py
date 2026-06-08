"""
Add TCF and Amal Academy candidates to SMG sheet
Focus: Direct staff at A+ tier target organizations
"""

import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime
import json

TOKEN_FILE = '.claude/config/token_sheets_broad.json'
SHEET_ID = '1mLn1PihtN7UXWfYB8mX6RikDn9pa3oeifnQe25HeU44'

print("\n" + "="*80)
print("Adding TCF & AMAL ACADEMY Direct Staff")
print("="*80)

with open(TOKEN_FILE, 'r') as f:
    token_data = json.load(f)

credentials = Credentials.from_authorized_user_info(token_data)
if credentials.expired:
    credentials.refresh(Request())

gc = gspread.Client(auth=credentials)

# TCF & AMAL ACADEMY STAFF - Mid-level, partnerships/operations focus
TCF_AMAL = [
    # TCF Staff
    ('Zeeshan Shafiq', 'https://www.linkedin.com/in/zeeshan-shafiq-822316159/', 'Program Manager', 'The Citizens Foundation', 'Pakistan', '5-6 years', 'Education program management, community outreach, stakeholder partnerships, TCF scale', 'Direct TCF staff, education program expertise, 320k student network', 'Tier 1 - TCF Insider'),

    ('Isfandyar Inayat', 'https://pk.linkedin.com/in/isfandyarinayat', 'Program Officer', 'The Citizens Foundation', 'Pakistan', '4-5 years', 'Education program delivery, stakeholder engagement, community partnerships, TCF operations', 'TCF direct staff, education scale, operational partnerships', 'Tier 1 - TCF Insider'),

    ('Adeel Baloch', 'https://www.linkedin.com/in/adeel-kaloi/', 'Community Partnerships Coordinator', 'The Citizens Foundation', 'Pakistan', '4-5 years', 'Community engagement, institutional partnerships, TCF volunteer programs, donor relations', 'TCF community partnerships, stakeholder management, network building', 'Tier 1 - TCF Insider'),

    ('Mansoor Ali Soomro', 'https://pk.linkedin.com/in/mansoor-ali-soomro-0a3b8a36', 'Operations Manager', 'The Citizens Foundation', 'Pakistan', '5-6 years', 'TCF operations, school management partnerships, regional coordination, stakeholder liaison', 'TCF operations expertise, partnership scaling, regional management', 'Tier 1 - TCF Insider'),

    # Amal Academy Staff
    ('Ramsha Khan', 'https://pk.linkedin.com/in/ramsha-khan-58b7b3107', 'Project Manager / Program Associate', 'Amal Academy', 'Pakistan', '4-5 years', 'Fellowship program management, institutional partnerships, project coordination, Amal scale', 'Direct Amal Academy staff, fellowship expansion (2019-2020), partnership focus', 'Tier 1 - Amal Insider'),

    ('Syed Musa Raza', 'https://www.linkedin.com/in/syed-musa-raza-718256210/', 'Outreach Manager / Training Coordinator', 'Amal Academy', 'Pakistan', '4-5 years', 'Outreach strategy, educational institution partnerships, network expansion, training delivery', 'Amal outreach leadership, institutional partnership development, strategic planning', 'Tier 1 - Amal Insider'),

    ('Ahmed Raza', 'https://www.linkedin.com/in/ahmed-raza-b8a784191/', 'Program Officer', 'Amal Academy', 'Pakistan', '4-5 years', 'Fellowship program management, stakeholder coordination, Amal ecosystem partnerships', 'Amal Academy direct staff, fellowship operations, partnership coordination', 'Tier 1 - Amal Insider'),

    ('Amina R.', 'https://pk.linkedin.com/in/amina-rahim94', 'Program Coordinator', 'Amal Academy', 'Pakistan', '4-5 years', 'Education program coordination, institutional partnerships, Amal fellowship support, stakeholder engagement', 'Amal Academy staff, fellowship coordination, stakeholder management', 'Tier 1 - Amal Insider'),
]

try:
    print("\n[STEP 1] Opening SMG sheet...")
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.get_worksheet(0)
    all_rows_before = ws.get_all_values()
    count_before = len(all_rows_before) - 1

    print(f"[OK] Current: {count_before} candidates")

    print(f"\n[STEP 2] Adding {len(TCF_AMAL)} TCF & Amal Academy insiders...")
    for candidate in TCF_AMAL:
        row = list(candidate) + ['Identified', '', '', datetime.now().strftime('%Y-%m-%d')]
        ws.append_row(row)
        print(f"  [OK] {candidate[0]} ({candidate[3]})")

    all_rows_after = ws.get_all_values()
    count_after = len(all_rows_after) - 1

    print("\n" + "="*80)
    print("[SUCCESS] TCF & AMAL ACADEMY CANDIDATES ADDED")
    print("="*80)
    print(f"\nSheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    print(f"\nTCF & Amal Staff Added: {len(TCF_AMAL)}")
    print(f"Total Candidates: {count_after}")
    print(f"\nBreakdown:")
    print(f"  TCF (The Citizens Foundation): 4 direct staff")
    print(f"    - 320,000+ students network")
    print(f"    - 2,261 school units")
    print(f"    - Partnerships focus")
    print(f"\n  Amal Academy: 4 direct staff")
    print(f"    - Fellowship expansion (2019-2020)")
    print(f"    - Karachi, Peshawar expansion")
    print(f"    - Institutional partnerships")
    print(f"\nAll A+ tier insider knowledge - they know the scaling game")

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
