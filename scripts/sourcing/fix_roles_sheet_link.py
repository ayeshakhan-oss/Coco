"""
Get the correct sheet ID for senior_manager_growth and fix the roles sheet link
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = 'tools/agent-coco-914edff20dde.json'
MASTER_SPREADSHEET_ID = '1eFf5ATqDyFvPi0qxgijPCbfrx_AWBvgtnj3ywe4UBNw'

credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
sheets_service = build('sheets', 'v4', credentials=credentials)

# Get all sheets in the spreadsheet
spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=MASTER_SPREADSHEET_ID).execute()
sheets = spreadsheet.get('sheets', [])

print("\nAll sheets in master spreadsheet:")
print("="*70)

smg_sheet_id = None
for sheet in sheets:
    title = sheet['properties']['title']
    sheet_id = sheet['properties']['sheetId']
    print(f"  Title: {title:40s} | ID: {sheet_id}")

    if title == 'senior_manager_growth':
        smg_sheet_id = sheet_id

print("\n" + "="*70)
if smg_sheet_id:
    print(f"[FOUND] senior_manager_growth sheet ID: {smg_sheet_id}")
    correct_link = f"https://docs.google.com/spreadsheets/d/{MASTER_SPREADSHEET_ID}/edit#gid={smg_sheet_id}"
    print(f"[CORRECT LINK] {correct_link}")

    # Now update the roles sheet with correct link
    print(f"\n[UPDATING] Fixing roles sheet with correct link...")

    # Read roles sheet
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=MASTER_SPREADSHEET_ID,
        range='roles!A:F'
    ).execute()

    rows = result.get('values', [])

    # Find and update SMG row
    for i, row in enumerate(rows):
        if row and row[0] and 'Senior Manager Growth' in row[0]:
            rows[i][2] = correct_link  # Update Sheet Link column
            print(f"[FOUND] SMG entry at row {i+1}")

            # Write back
            sheets_service.spreadsheets().values().update(
                spreadsheetId=MASTER_SPREADSHEET_ID,
                range=f'roles!A{i+1}:F{i+1}',
                valueInputOption='USER_ENTERED',
                body={'values': [rows[i]]}
            ).execute()

            print(f"[OK] Updated roles sheet with correct link")
            print(f"\nCORRECT LINK TO SHARE: {correct_link}")
            break
else:
    print("[ERROR] senior_manager_growth sheet not found")
