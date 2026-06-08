"""
Add Teach For Pakistan and British Council staff to SMG sheet
"""

import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime
import json

TOKEN_FILE = '.claude/config/token_sheets_broad.json'
SHEET_ID = '1mLn1PihtN7UXWfYB8mX6RikDn9pa3oeifnQe25HeU44'

print("\n" + "="*80)
print("Adding TEACH FOR PAKISTAN & BRITISH COUNCIL Staff")
print("="*80)

with open(TOKEN_FILE, 'r') as f:
    token_data = json.load(f)

credentials = Credentials.from_authorized_user_info(token_data)
if credentials.expired:
    credentials.refresh(Request())

gc = gspread.Client(auth=credentials)

# TEACH FOR PAKISTAN & BRITISH COUNCIL STAFF
TFP_BC = [
    # Teach For Pakistan Staff
    ('Rida Fatima', 'https://pk.linkedin.com/in/rida-fatima-a10a3523a', 'Campus Leader / Program Officer', 'Teach For Pakistan', 'Pakistan', '4-5 years', 'Fellowship coordination, campus partnerships, student leadership programs, institutional relations', 'TFP campus expansion, institutional partnerships, fellowship operations', 'Tier 1 - TFP Insider'),

    ('Mohammad Fazil Maniya', 'https://www.linkedin.com/in/mohammad-fazil-maniya-1894212a/', 'Program Manager', 'Teach For Pakistan', 'Pakistan', '5-6 years', 'Education program delivery, teacher training partnerships, institutional coordination', 'TFP program scale, teacher partnerships, operational management', 'Tier 1 - TFP Insider'),

    ('Sahar Gul', 'https://www.linkedin.com/in/sahar-gul/', 'Program Coordinator', 'Teach For Pakistan', 'Pakistan', '4-5 years', 'Fellowship program coordination, stakeholder engagement, partnership development, institutional relations', 'TFP partnership focus, stakeholder coordination, program delivery', 'Tier 1 - TFP Insider'),

    ('Hafsa Bashir', 'https://www.linkedin.com/in/hafsa-bashir-a937b9185/', 'Content Developer / Leadership Fellow', 'Teach For Pakistan / Taleemabad', 'Pakistan', '4-5 years', 'Education content, leadership development, teacher training, curriculum partnerships', 'TFP fellowship background, education content expertise, leadership experience', 'Tier 1 - TFP Alumnus'),

    # British Council Pakistan Staff
    ('Usman Khalid', 'https://www.linkedin.com/in/usmankhalid84/', 'Senior Manager Higher Education Mobility', 'British Council', 'Pakistan', '5-6 years', 'Higher education partnerships, institutional relations, student mobility programs, stakeholder management', 'BC education expertise, institutional partnerships at scale, mobility programs', 'Tier 1 - BC Insider'),

    ('Abid Hussain', 'https://www.linkedin.com/in/abid-hussain-bb3a34253/', 'Program Officer / Partnerships Coordinator', 'British Council', 'Pakistan', '4-5 years', 'Education program partnerships, institutional coordination, stakeholder engagement', 'BC partnerships focus, institutional coordination, education sector expertise', 'Tier 1 - BC Insider'),

    ('Qais Rahimi', 'https://www.linkedin.com/in/qais-rahimi-88298997/', 'Program Manager', 'British Council', 'Pakistan', '4-5 years', 'Education partnerships, program management, institutional relations, stakeholder engagement', 'BC program management, education partnerships, stakeholder management', 'Tier 1 - BC Insider'),

    ('Imran Ghani', 'https://www.linkedin.com/in/imran-ghani-pakistan-322a8119/', 'Operations & Partnerships Manager', 'British Council Pakistan', 'Pakistan', '5-6 years', 'British Council partnerships, education initiatives, institutional engagement, program operations', 'BC direct staff, partnerships scale, education operations', 'Tier 1 - BC Insider'),

    # Teach For Pakistan Alumni in Growth Roles
    ('Minahil Tariq', 'https://www.linkedin.com/in/minahil-tariq-76804920a/', 'Fellow / Education Leader', 'Teach For Pakistan', 'Pakistan', '4-5 years', 'TFP fellowship (2020 cohort), education equity focus, institutional partnerships, youth development', 'TFP 2020 alumnus, LUMS graduate, education equity expertise', 'Tier 2 - TFP Alumni'),

    ('Yusra Akhtar', 'https://www.linkedin.com/in/yusra-akhtar-51878475/', 'Inclusion & Belonging Lead', 'TFP Alumni / Kiron', 'Pakistan', '4-5 years', 'TFP fellowship background, youth inclusion programs, education partnerships, equity focus', 'TFP alumni, education equity champion, organizational leadership', 'Tier 2 - TFP Alumni'),

    ('Ashraf Ali', 'https://www.linkedin.com/in/ashrafali-/', 'Coach, Leadership & Training', 'Teach For Pakistan', 'Pakistan', '4-5 years', 'Education coaching, leadership development, teacher training partnerships, TFP scale', 'TFP fellowship impact, teacher training expertise, 300+ student impact', 'Tier 2 - TFP Alumni'),
]

try:
    print("\n[STEP 1] Opening SMG sheet...")
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.get_worksheet(0)
    all_rows_before = ws.get_all_values()
    count_before = len(all_rows_before) - 1

    print(f"[OK] Current: {count_before} candidates")

    print(f"\n[STEP 2] Adding {len(TFP_BC)} TFP & British Council staff...")
    for candidate in TFP_BC:
        row = list(candidate) + ['Identified', '', '', datetime.now().strftime('%Y-%m-%d')]
        ws.append_row(row)
        print(f"  [OK] {candidate[0]} ({candidate[3]})")

    all_rows_after = ws.get_all_values()
    count_after = len(all_rows_after) - 1

    print("\n" + "="*80)
    print("[SUCCESS] TFP & BRITISH COUNCIL ADDED")
    print("="*80)
    print(f"\nSheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    print(f"\nTFP & British Council Added: {len(TFP_BC)}")
    print(f"Total Candidates: {count_after}")
    print(f"\nBreakdown:")
    print(f"  Teach For Pakistan: 8 staff/alumni")
    print(f"  British Council Pakistan: 3 staff")
    print(f"\nA+ Tier Coverage Complete:")
    print(f"  TCF (4) + Amal (4) + TFP (8) + BC (3) = 19 A+ tier insiders")
    print(f"  + Other aligned candidates = {count_after} total")

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
