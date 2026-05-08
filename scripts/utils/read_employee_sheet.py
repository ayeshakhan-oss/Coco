#!/usr/bin/env python3
"""
Read employee headcount from Google Sheet.
Adapter pattern: loads OAuth token → builds API client → fetches all tabs → counts rows per tab.
Based on SHEETS-API-TEMPLATE.js integration guide.

Usage:
    python scripts/utils/read_employee_sheet.py
"""

import sys
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Set stdout to UTF-8 for Windows compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
SPREADSHEET_ID = "1J5vhVUrHiW0r_zlz_BFTh_aiOkUIjUu9Q7Pmqb7U7Jg"
TOKEN_PATH = Path(__file__).parent.parent.parent / "token_sheets.json"
SHEET_DESC = "Employee Headcount"
COUNT_COLUMN = "A"
SKIP_ROWS = 1  # Skip 1 header row
NUMERIC_ONLY = True  # Count only numeric IDs

def validate_token(creds):
    """Refresh token if expired."""
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save refreshed token
            with open(TOKEN_PATH, 'w') as f:
                f.write(creds.to_json())
            print("✓ OAuth token refreshed and saved\n")
        except Exception as e:
            print(f"⚠️  Warning: Could not refresh token: {e}")
            print("   Token may expire soon.\n")

def extract_sheet_data():
    """Main: fetch all sheets and count rows per sheet."""
    # Load credentials from token
    if not TOKEN_PATH.exists():
        print(f"❌ Error: token_sheets.json not found at {TOKEN_PATH}")
        print("   Run: python scripts/setup/setup_sheets_token.py to authenticate first.")
        sys.exit(1)

    try:
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
        validate_token(creds)
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        sys.exit(1)

    # Build Sheets API client
    try:
        service = build('sheets', 'v4', credentials=creds)
    except Exception as e:
        print(f"❌ Error building API client: {e}")
        sys.exit(1)

    # Step 1: Fetch all tab names from spreadsheet metadata
    try:
        print(f"📊 EXTRACTING {SHEET_DESC.upper()}...\n")
        meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        tabs = [s['properties']['title'] for s in meta['sheets']]
        print(f"Found {len(tabs)} sheets:\n")
    except Exception as e:
        print(f"❌ Error fetching spreadsheet metadata: {e}")
        if "deleted_client" in str(e):
            print("   The OAuth client was deleted. Re-run setup_sheets_token.py")
        sys.exit(1)

    # Step 2: Count rows per tab
    results = []
    total_count = 0

    for tab in tabs:
        try:
            # Fetch data from COUNT_COLUMN
            range_spec = f"'{tab}'!{COUNT_COLUMN}:{COUNT_COLUMN}"
            resp = service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=range_spec
            ).execute()
            rows = resp.get('values', [])

            # Count rows: skip headers, optionally filter numeric only
            count = 0
            for i in range(SKIP_ROWS, len(rows)):
                if rows[i] and len(rows[i]) > 0:
                    cell_value = str(rows[i][0]).strip()

                    if NUMERIC_ONLY:
                        # Count only if numeric (like employee IDs)
                        if cell_value and cell_value.isdigit():
                            count += 1
                    else:
                        # Count any non-empty cell
                        if cell_value:
                            count += 1

            results.append({'sheet': tab, 'count': count})
            total_count += count
            print(f"  ✓ {tab.ljust(30)} : {count}")

        except Exception as e:
            print(f"  ✗ {tab.ljust(30)} : Error — {e}")
            results.append({'sheet': tab, 'count': None})

    # Step 3: Display results
    print("\n" + "="*80)
    print(f"\n{SHEET_DESC.upper()} SUMMARY\n")
    print("Sheet Name".ljust(35) + "Count")
    print("-"*80)

    for r in results:
        if r['count'] is not None:
            print(f"{r['sheet'].ljust(35)}{r['count']}")
        else:
            print(f"{r['sheet'].ljust(35)}ERROR")

    print("-"*80)
    print(f"{'TOTAL'.ljust(35)}{total_count}")
    print("\n" + "="*80 + "\n")

    # Step 4: Markdown table output
    print("📋 MARKDOWN TABLE:\n")
    print("| Sheet | Count |")
    print("|---|---|")
    for r in results:
        count_str = str(r['count']) if r['count'] is not None else "ERROR"
        print(f"| {r['sheet']} | {count_str} |")
    print(f"| **TOTAL** | **{total_count}** |")
    print("")

    return {'results': results, 'total': total_count}

def main():
    extract_sheet_data()

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
