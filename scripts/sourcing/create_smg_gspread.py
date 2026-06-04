"""
Create SEPARATE Google Sheet using gspread library
This library handles Google Sheets more intelligently
"""

import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime
import json
import os

TOKEN_FILE = '.claude/config/token_sheets.json'
MASTER_SPREADSHEET_ID = '1eFf5ATqDyFvPi0qxgijPCbfrx_AWBvgtnj3ywe4UBNw'

# Load OAuth credentials
with open(TOKEN_FILE, 'r') as f:
    token_data = json.load(f)

credentials = Credentials.from_authorized_user_info(token_data)
if credentials.expired:
    credentials.refresh(Request())

# Initialize gspread client with OAuth credentials
gc = gspread.Client(auth=credentials)

CANDIDATES = [
    ('Khizr Ahmed Khan', 'https://www.linkedin.com/in/khizr-ahmed-khan-25b0a128b/', 'Business Development Manager', 'SmartThink.Org', 'Lahore', 'EdTech nonprofit, B2B deal management, customer success, SaaS growth', 'Direct match: EdTech nonprofit, stakeholder engagement, growth loop management', 'Tier 1 - Highest Fit', 'Identified', '', '', datetime.now().strftime('%Y-%m-%d')),
    ('Ahmad Aslam', 'https://www.linkedin.com/in/ahmad-aslam/', 'Country Manager, Business Development', 'PeopleCert', 'Pakistan (Multi-city)', 'BD expansion across Pakistan, scaled centers from 0 to 8+, institutional stakeholders', 'Government + institutional partnerships, multi-city acquisition strategy', 'Tier 1 - High Fit', 'Identified', '', '', datetime.now().strftime('%Y-%m-%d')),
    ('M. Shaharyar Lakhani', 'https://www.linkedin.com/in/m-shaharyar-lakhani-8700a54a/', 'Partnership Sales Manager', 'Multiple', 'Pakistan', 'Strategic partnership identification and management, revenue growth focus', 'Stakeholder relationship builder at scale, partnership-driven growth', 'Tier 1 - High Fit', 'Identified', '', '', datetime.now().strftime('%Y-%m-%d')),
    ('Inayat Ullah', 'https://pk.linkedin.com/in/inayat-ullah-6981978', 'Senior Manager', 'Universal Service Fund Pakistan', 'Islamabad', 'USAID nonprofit, government partnerships, institutional stakeholder management', 'USAID-funded development work, government relationship expertise', 'Tier 1 - High Fit', 'Identified', '', '', datetime.now().strftime('%Y-%m-%d')),
    ('Palwasha Khan', 'https://www.linkedin.com/in/palwasha-khan-64797511a/', 'Manager, Digital Channels Growth (FS)', 'Telenor Pakistan', 'Pakistan', 'Digital acquisition channels, multi-stakeholder B2B2C scaling', 'Channel optimization and growth scaling in complex environments', 'Tier 2 - Medium Fit', 'Identified', '', '', datetime.now().strftime('%Y-%m-%d')),
    ('Salman Hassan', 'https://www.linkedin.com/in/salman-hassan-47631656/', 'Regional Manager', 'Multiple', 'Pakistan (Peshawar, Lahore, Karachi)', 'Provincial office establishment, stakeholder relationships, regional expansion', 'Multi-city expansion, government + private sector partnerships', 'Tier 2 - Medium Fit', 'Identified', '', '', datetime.now().strftime('%Y-%m-%d')),
    ('Mehak Saeed', 'https://www.linkedin.com/in/mehak-saeed-/', 'Growth Operations', 'NK DEMONS', 'Pakistan', 'Early-stage growth, EdTech/startup context, business development', 'EdTech growth background, startup acquisition experience', 'Tier 3 - Exploratory', 'Identified', '', '', datetime.now().strftime('%Y-%m-%d')),
    ('Maryam Khan', 'https://www.linkedin.com/in/maryam-khan-bb1b09201', 'Growth Marketer', 'Dcode', 'Pakistan', 'Growth loop optimization, ROI improvement (2.1M to 5M PKR portfolio)', 'Demonstrated channel optimization and acquisition growth', 'Tier 3 - Exploratory', 'Identified', '', '', datetime.now().strftime('%Y-%m-%d')),
]

HEADERS = ['Name', 'LinkedIn URL', 'Current Role', 'Current Company', 'Location', 'Key Experience', 'Why Relevant', 'Tier', 'Status', 'DM Sent', 'Response', 'Date Added']

print("\n" + "="*80)
print("Creating SEPARATE Google Sheet using gspread")
print("="*80)

try:
    print("\n[STEP 1] Creating new spreadsheet...")
    sh = gc.create('Senior Manager Growth - Talent Slate (2026-06-03)')
    new_sheet_id = sh.id
    print(f"[OK] Created: {new_sheet_id}")

    # Get the first worksheet
    worksheet = sh.get_worksheet(0)

    # Add headers
    print("\n[STEP 2] Adding headers and candidates...")
    worksheet.append_row(HEADERS)

    # Add all candidate rows
    for candidate in CANDIDATES:
        worksheet.append_row(list(candidate))

    print(f"[OK] Added {len(CANDIDATES)} candidates")

    # Generate URL
    sheet_url = f"https://docs.google.com/spreadsheets/d/{new_sheet_id}/edit"

    print("\n" + "="*80)
    print("[SUCCESS] SEPARATE SHEET CREATED")
    print("="*80)
    print(f"\nSheet ID: {new_sheet_id}")
    print(f"Sheet URL: {sheet_url}")

    # Update master roles sheet
    print("\n[STEP 3] Updating master roles sheet...")
    master_sh = gc.open_by_key(MASTER_SPREADSHEET_ID)
    roles_ws = master_sh.worksheet('Roles')

    # Get all rows
    all_rows = roles_ws.get_all_values()

    # Find and update SMG row
    updated = False
    for i, row in enumerate(all_rows, 1):
        if len(row) > 0 and 'Senior Manager Growth' in row[0]:
            # Update the Sheet Link column (index 2)
            roles_ws.update_cell(i, 3, sheet_url)
            print(f"[OK] Updated master roles sheet (row {i})")
            updated = True
            break

    if not updated:
        print("[INFO] SMG not in roles sheet, adding new entry...")
        new_row = [
            'Senior Manager Growth',
            'SMG',
            sheet_url,
            'Identified - 8 candidates',
            datetime.now().strftime('%Y-%m-%d'),
            'Tier 1: 4. Tier 2: 2. Tier 3: 2. Ready for DM drafting.'
        ]
        roles_ws.append_row(new_row)
        print("[OK] Added SMG to master roles sheet")

    print("\n" + "="*80)
    print("[WORKFLOW COMPLETE]")
    print("="*80)
    print(f"\nSeparate Candidates Sheet: {sheet_url}")
    print(f"\nMaster Roles Sheet: Updated")
    print(f"\nStatus: Ready for DM drafting")

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
