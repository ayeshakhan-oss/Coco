"""
Create SEPARATE Google Sheet using OAuth user credentials (not service account)
This has broader permissions to create new sheets
"""

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime
import json
import os

# Use OAuth token instead of service account
TOKEN_FILE = '.claude/config/token_sheets.json'
MASTER_SPREADSHEET_ID = '1eFf5ATqDyFvPi0qxgijPCbfrx_AWBvgtnj3ywe4UBNw'

# Load OAuth credentials
if not os.path.exists(TOKEN_FILE):
    print(f"[ERROR] Token file not found: {TOKEN_FILE}")
    exit(1)

with open(TOKEN_FILE, 'r') as f:
    token_data = json.load(f)

credentials = Credentials.from_authorized_user_info(token_data)

# Refresh if needed
if credentials.expired:
    credentials.refresh(Request())

sheets_service = build('sheets', 'v4', credentials=credentials)

CANDIDATES = [
    {
        'name': 'Khizr Ahmed Khan',
        'linkedin': 'https://www.linkedin.com/in/khizr-ahmed-khan-25b0a128b/',
        'role': 'Business Development Manager',
        'company': 'SmartThink.Org',
        'location': 'Lahore',
        'experience': 'EdTech nonprofit, B2B deal management, customer success, SaaS growth',
        'why_relevant': 'Direct match: EdTech nonprofit, stakeholder engagement, growth loop management',
        'tier': 'Tier 1 - Highest Fit'
    },
    {
        'name': 'Ahmad Aslam',
        'linkedin': 'https://www.linkedin.com/in/ahmad-aslam/',
        'role': 'Country Manager, Business Development',
        'company': 'PeopleCert',
        'location': 'Pakistan (Multi-city)',
        'experience': 'BD expansion across Pakistan, scaled centers from 0 to 8+, institutional stakeholders',
        'why_relevant': 'Government + institutional partnerships, multi-city acquisition strategy',
        'tier': 'Tier 1 - High Fit'
    },
    {
        'name': 'M. Shaharyar Lakhani',
        'linkedin': 'https://www.linkedin.com/in/m-shaharyar-lakhani-8700a54a/',
        'role': 'Partnership Sales Manager',
        'company': 'Multiple',
        'location': 'Pakistan',
        'experience': 'Strategic partnership identification and management, revenue growth focus',
        'why_relevant': 'Stakeholder relationship builder at scale, partnership-driven growth',
        'tier': 'Tier 1 - High Fit'
    },
    {
        'name': 'Inayat Ullah',
        'linkedin': 'https://pk.linkedin.com/in/inayat-ullah-6981978',
        'role': 'Senior Manager',
        'company': 'Universal Service Fund Pakistan',
        'location': 'Islamabad',
        'experience': 'USAID nonprofit, government partnerships, institutional stakeholder management',
        'why_relevant': 'USAID-funded development work, government relationship expertise',
        'tier': 'Tier 1 - High Fit'
    },
    {
        'name': 'Palwasha Khan',
        'linkedin': 'https://www.linkedin.com/in/palwasha-khan-64797511a/',
        'role': 'Manager, Digital Channels Growth (FS)',
        'company': 'Telenor Pakistan',
        'location': 'Pakistan',
        'experience': 'Digital acquisition channels, multi-stakeholder B2B2C scaling',
        'why_relevant': 'Channel optimization and growth scaling in complex environments',
        'tier': 'Tier 2 - Medium Fit'
    },
    {
        'name': 'Salman Hassan',
        'linkedin': 'https://www.linkedin.com/in/salman-hassan-47631656/',
        'role': 'Regional Manager',
        'company': 'Multiple',
        'location': 'Pakistan (Peshawar, Lahore, Karachi)',
        'experience': 'Provincial office establishment, stakeholder relationships, regional expansion',
        'why_relevant': 'Multi-city expansion, government + private sector partnerships',
        'tier': 'Tier 2 - Medium Fit'
    },
    {
        'name': 'Mehak Saeed',
        'linkedin': 'https://www.linkedin.com/in/mehak-saeed-/',
        'role': 'Growth Operations',
        'company': 'NK DEMONS',
        'location': 'Pakistan',
        'experience': 'Early-stage growth, EdTech/startup context, business development',
        'why_relevant': 'EdTech growth background, startup acquisition experience',
        'tier': 'Tier 3 - Exploratory'
    },
    {
        'name': 'Maryam Khan',
        'linkedin': 'https://www.linkedin.com/in/maryam-khan-bb1b09201',
        'role': 'Growth Marketer',
        'company': 'Dcode',
        'location': 'Pakistan',
        'experience': 'Growth loop optimization, ROI improvement (2.1M to 5M PKR portfolio)',
        'why_relevant': 'Demonstrated channel optimization and acquisition growth',
        'tier': 'Tier 3 - Exploratory'
    }
]

print("\n" + "="*80)
print("Creating SEPARATE Google Sheet with OAuth user credentials")
print("="*80)

# Step 1: Create SEPARATE Google Sheet
print("\n[STEP 1] Creating new Google Sheet (using OAuth user credentials)...")

spreadsheet_body = {
    'properties': {
        'title': 'Senior Manager Growth - Talent Slate (2026-06-03)',
        'locale': 'en_US'
    }
}

try:
    spreadsheet = sheets_service.spreadsheets().create(
        body=spreadsheet_body,
        fields='spreadsheetId'
    ).execute()

    new_sheet_id = spreadsheet['spreadsheetId']
    print(f"[OK] Created: {new_sheet_id}")
except Exception as e:
    print(f"[ERROR] Failed to create sheet: {e}")
    exit(1)

# Step 2: Add headers and candidates
print("\n[STEP 2] Adding candidate data...")

headers = [
    'Name', 'LinkedIn URL', 'Current Role', 'Current Company', 'Location',
    'Key Experience', 'Why Relevant', 'Tier', 'Status', 'DM Sent', 'Response', 'Date Added'
]

rows = [headers]
for candidate in CANDIDATES:
    row = [
        candidate['name'],
        candidate['linkedin'],
        candidate['role'],
        candidate['company'],
        candidate['location'],
        candidate['experience'],
        candidate['why_relevant'],
        candidate['tier'],
        'Identified',
        '',
        '',
        datetime.now().strftime('%Y-%m-%d')
    ]
    rows.append(row)

sheets_service.spreadsheets().values().update(
    spreadsheetId=new_sheet_id,
    range='Sheet1!A1:L{}'.format(len(rows)),
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

print(f"[OK] Added {len(CANDIDATES)} candidates")

# Step 3: Generate sheet URL
sheet_url = f"https://docs.google.com/spreadsheets/d/{new_sheet_id}/edit"

print("\n" + "="*80)
print("[SUCCESS] SEPARATE SHEET CREATED")
print("="*80)
print(f"\nSheet ID: {new_sheet_id}")
print(f"Sheet URL: {sheet_url}")

# Step 4: Update master roles sheet
print("\n[STEP 3] Updating master roles sheet with link to new sheet...")

try:
    # Read current roles sheet
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=MASTER_SPREADSHEET_ID,
        range='Roles!A:F'
    ).execute()

    roles_rows = result.get('values', [])

    # Find SMG row
    updated = False
    for i, row in enumerate(roles_rows):
        if row and len(row) > 0 and 'Senior Manager Growth' in row[0]:
            roles_rows[i][2] = sheet_url
            print(f"[FOUND] SMG at row {i+1}")

            sheets_service.spreadsheets().values().update(
                spreadsheetId=MASTER_SPREADSHEET_ID,
                range=f'Roles!A{i+1}:F{i+1}',
                valueInputOption='USER_ENTERED',
                body={'values': [roles_rows[i]]}
            ).execute()
            updated = True
            print(f"[OK] Updated master roles sheet")
            break

    if not updated:
        print("[INFO] Adding new SMG entry to roles sheet...")
        new_row = [
            'Senior Manager Growth',
            'SMG',
            sheet_url,
            'Identified - 8 candidates',
            datetime.now().strftime('%Y-%m-%d'),
            'Tier 1: 4. Tier 2: 2. Tier 3: 2. Ready for DM drafting.'
        ]
        sheets_service.spreadsheets().values().append(
            spreadsheetId=MASTER_SPREADSHEET_ID,
            range='Roles!A:F',
            valueInputOption='USER_ENTERED',
            body={'values': [new_row]}
        ).execute()
        print(f"[OK] Added SMG to master roles sheet")

except Exception as e:
    print(f"[WARNING] Could not update master roles sheet: {e}")
    print(f"[INFO] You can manually add this link to the master roles sheet:")
    print(f"  {sheet_url}")

print("\n" + "="*80)
print("[FINAL] WORKFLOW COMPLETE")
print("="*80)
print(f"\nSeparate Sheet: {sheet_url}")
print(f"\nNext step: Draft personalized DMs for candidates")
