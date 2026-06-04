"""
Add Senior Manager Growth candidates to sourcing sheet
=======================================================
Creates 'senior_manager_growth' sheet in master spreadsheet and adds all 8 candidates.
Status: "Identified" (ready for DM drafting)
"""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

# Credentials
CREDENTIALS_FILE = 'tools/agent-coco-914edff20dde.json'
MASTER_SPREADSHEET_ID = '1eFf5ATqDyFvPi0qxgijPCbfrx_AWBvgtnj3ywe4UBNw'

# Authenticate
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
sheets_service = build('sheets', 'v4', credentials=credentials)

# Candidate data (from 3-layer search, 2026-06-03)
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

def create_or_get_sheet(spreadsheet_id, sheet_name):
    """Create or get existing sheet"""
    spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet.get('sheets', [])

    # Check if sheet exists
    for sheet in sheets:
        if sheet['properties']['title'] == sheet_name:
            return sheet['properties']['sheetId']

    # Create new sheet
    request = {
        'addSheet': {
            'properties': {
                'title': sheet_name,
                'gridProperties': {
                    'rowCount': 1000,
                    'columnCount': 12
                }
            }
        }
    }
    response = sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': [request]}
    ).execute()

    return response['replies'][0]['addSheet']['properties']['sheetId']

def add_candidates_to_sheet(spreadsheet_id, sheet_name, candidates):
    """Add candidates to sheet"""
    sheet_id = create_or_get_sheet(spreadsheet_id, sheet_name)

    # Headers
    headers = [
        'Name',
        'LinkedIn URL',
        'Current Role',
        'Current Company',
        'Location',
        'Key Experience',
        'Why Relevant',
        'Tier',
        'Status',
        'DM Sent',
        'Response',
        'Date Added'
    ]

    # Build rows
    rows = [headers]
    for candidate in candidates:
        row = [
            candidate['name'],
            candidate['linkedin'],
            candidate['role'],
            candidate['company'],
            candidate['location'],
            candidate['experience'],
            candidate['why_relevant'],
            candidate['tier'],
            'Identified',  # Status
            '',  # DM Sent
            '',  # Response
            datetime.now().strftime('%Y-%m-%d')
        ]
        rows.append(row)

    # Write to sheet
    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f'{sheet_name}!A1:L{len(rows)}',
        valueInputOption='USER_ENTERED',
        body={'values': rows}
    ).execute()

    # Format header row (bold) - simplified to avoid API issues
    requests = [
        {
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': 12
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {
                            'bold': True
                        }
                    }
                },
                'fields': 'userEnteredFormat.textFormat'
            }
        }
    ]

    sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    print(f"[OK] Added {len(candidates)} candidates to '{sheet_name}' sheet")
    print(f"[OK] Sheet URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={sheet_id}")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("Adding Senior Manager Growth candidates to sourcing sheet")
    print("="*70)

    add_candidates_to_sheet(
        MASTER_SPREADSHEET_ID,
        'senior_manager_growth',
        CANDIDATES
    )

    print("\n[OK] All candidates added with status='Identified'")
    print("[OK] Ready for DM drafting")
