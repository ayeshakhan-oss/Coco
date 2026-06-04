"""
Create senior_manager_growth sheet in MASTER spreadsheet and add candidates
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

CREDENTIALS_FILE = 'tools/agent-coco-914edff20dde.json'
MASTER_SPREADSHEET_ID = '1eFf5ATqDyFvPi0qxgijPCbfrx_AWBvgtnj3ywe4UBNw'

credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
sheets_service = build('sheets', 'v4', credentials=credentials)

CANDIDATES = [
    # TIER 1
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
    # TIER 2
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
    # TIER 3
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

# Step 1: Create sheet
print("\n[STEP 1] Creating senior_manager_growth sheet in master spreadsheet...")

request = {
    'addSheet': {
        'properties': {
            'title': 'senior_manager_growth',
            'gridProperties': {
                'rowCount': 500,
                'columnCount': 12
            }
        }
    }
}

response = sheets_service.spreadsheets().batchUpdate(
    spreadsheetId=MASTER_SPREADSHEET_ID,
    body={'requests': [request]}
).execute()

smg_sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']
print(f"[OK] Created sheet with ID: {smg_sheet_id}")

# Step 2: Add headers and data
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
    spreadsheetId=MASTER_SPREADSHEET_ID,
    range=f'senior_manager_growth!A1:L{len(rows)}',
    valueInputOption='USER_ENTERED',
    body={'values': rows}
).execute()

print(f"[OK] Added {len(CANDIDATES)} candidates")

# Step 3: Update roles sheet with correct link
print("\n[STEP 3] Updating roles sheet with correct link...")

correct_link = f"https://docs.google.com/spreadsheets/d/{MASTER_SPREADSHEET_ID}/edit#gid={smg_sheet_id}"

# Read roles sheet
result = sheets_service.spreadsheets().values().get(
    spreadsheetId=MASTER_SPREADSHEET_ID,
    range='Roles!A:F'
).execute()

roles_rows = result.get('values', [])

# Find and update SMG row
updated = False
for i, row in enumerate(roles_rows):
    if row and len(row) > 0 and 'Senior Manager Growth' in row[0]:
        roles_rows[i][2] = correct_link
        print(f"[FOUND] SMG at row {i+1}, updating link...")

        sheets_service.spreadsheets().values().update(
            spreadsheetId=MASTER_SPREADSHEET_ID,
            range=f'Roles!A{i+1}:F{i+1}',
            valueInputOption='USER_ENTERED',
            body={'values': [roles_rows[i]]}
        ).execute()
        updated = True
        break

if not updated:
    print("[INFO] SMG not in roles sheet, skipping update")

print(f"\n[FINAL] CORRECT SHEET LINK:")
print(f"{correct_link}")
print(f"\n[OK] Workflow complete - ready for DM drafting")
