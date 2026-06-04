"""
Add Senior Manager Growth to the master 'roles' sheet
=====================================================
Updates the roles tracking sheet with SMG entry and sheet link
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

def read_roles_sheet():
    """Read the roles sheet to understand its structure"""
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=MASTER_SPREADSHEET_ID,
        range='roles!A:F'
    ).execute()

    rows = result.get('values', [])

    print("\n" + "="*80)
    print("MASTER 'ROLES' SHEET STRUCTURE")
    print("="*80)

    if rows:
        headers = rows[0]
        print(f"\nHeaders: {headers}")
        print(f"\nExisting entries:")
        for i, row in enumerate(rows[1:], 1):
            print(f"  {i}. {row}")
    else:
        print("[INFO] Roles sheet is empty or not found")

    return rows

def add_smg_to_roles_sheet():
    """Add Senior Manager Growth to the roles sheet"""

    # Read current state
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=MASTER_SPREADSHEET_ID,
        range='roles!A:F'
    ).execute()

    rows = result.get('values', [])

    # Check if SMG already exists
    for row in rows[1:]:
        if row and row[0] and 'Senior Manager Growth' in row[0]:
            print("[SKIP] Senior Manager Growth already in roles sheet")
            return

    # Add new row for SMG
    smg_sheet_id = 236617803  # From the creation output
    smg_row = [
        'Senior Manager Growth',  # Role Name
        'SMG',  # Position Folder
        f'https://docs.google.com/spreadsheets/d/{MASTER_SPREADSHEET_ID}/edit#gid={smg_sheet_id}',  # Sheet Link
        'Identified - 8 candidates',  # Status
        datetime.now().strftime('%Y-%m-%d'),  # Last Updated
        'Tier 1: 4 (Khizr Ahmed Khan, Ahmad Aslam, M. Shaharyar Lakhani, Inayat Ullah). Tier 2: 2. Tier 3: 2. DM drafting ready.'  # Notes
    ]

    # Append to roles sheet
    sheets_service.spreadsheets().values().append(
        spreadsheetId=MASTER_SPREADSHEET_ID,
        range='roles!A:F',
        valueInputOption='USER_ENTERED',
        body={'values': [smg_row]}
    ).execute()

    print("\n[OK] Added Senior Manager Growth to 'roles' sheet")
    print(f"\nEntry Details:")
    print(f"  Role Name: {smg_row[0]}")
    print(f"  Position Folder: {smg_row[1]}")
    print(f"  Sheet Link: {smg_row[2]}")
    print(f"  Status: {smg_row[3]}")
    print(f"  Last Updated: {smg_row[4]}")
    print(f"  Notes: {smg_row[5]}")

if __name__ == '__main__':
    # First, read and display the roles sheet structure
    print("\n[STEP 1] Reading master 'roles' sheet...")
    read_roles_sheet()

    # Then add SMG
    print("\n[STEP 2] Adding Senior Manager Growth to roles sheet...")
    add_smg_to_roles_sheet()

    print("\n[OK] Sourcing workflow update complete")
    print("[OK] Next: Draft personalized DMs for candidates")
