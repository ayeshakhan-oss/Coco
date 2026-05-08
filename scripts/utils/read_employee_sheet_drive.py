#!/usr/bin/env python3
"""
Read employee headcount from Google Sheet via Drive API (handles Office files).
Uses Drive API to export the sheet, then parses the CSV.
"""

import sys
import csv
import io
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Set stdout to UTF-8 for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

SPREADSHEET_ID = "1tIKIU0LKCR2YYuCS0u0lb_Gr-rDm6ks_"
TOKEN_PATH = Path(__file__).parent.parent.parent / "token_sheets.json"
SHEET_DESC = "Employee Headcount"

def read_employee_sheet():
    """Read sheet via Drive API and parse tabs."""
    if not TOKEN_PATH.exists():
        print(f"[ERROR] token_sheets.json not found at {TOKEN_PATH}")
        print("        Run: python scripts/setup/setup_sheets_token.py first")
        sys.exit(1)

    try:
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
        # Refresh if expired
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_PATH, 'w') as f:
                f.write(creds.to_json())
            print("[OK] Token refreshed\n")
    except Exception as e:
        print(f"[ERROR] Loading credentials: {e}")
        sys.exit(1)

    try:
        drive = build('drive', 'v3', credentials=creds)
        sheets = build('sheets', 'v4', credentials=creds)
    except Exception as e:
        print(f"[ERROR] Building API client: {e}")
        sys.exit(1)

    print(f"[*] Extracting {SHEET_DESC.upper()}...\n")

    # Try to get sheet metadata first
    try:
        meta = sheets.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        tabs = [s['properties']['title'] for s in meta['sheets']]
        print(f"[OK] Found {len(tabs)} sheets\n")
    except Exception as e:
        # If Sheets API fails (Office file), try Drive API
        if "not supported for this document" in str(e):
            print("[!] Sheet is an Office file, using Drive API to export...\n")
            return read_via_drive_export(drive)
        else:
            print(f"[ERROR] Fetching metadata: {e}")
            sys.exit(1)

    # Try to read each sheet via Sheets API
    results = []
    total_count = 0

    for tab in tabs:
        try:
            range_spec = f"'{tab}'!A:A"
            resp = sheets.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=range_spec
            ).execute()
            rows = resp.get('values', [])

            # Count non-empty rows (skip header)
            count = sum(1 for r in rows[1:] if r and len(r) > 0 and str(r[0]).strip())
            results.append({'sheet': tab, 'count': count})
            total_count += count
            print(f"  [OK] {tab.ljust(30)} : {count}")

        except Exception as e:
            print(f"  [ERROR] {tab.ljust(30)} : {e}")
            results.append({'sheet': tab, 'count': None})

    print_summary(results, total_count)
    return {'results': results, 'total': total_count}

def read_via_drive_export(drive):
    """Export spreadsheet as CSV via Drive API."""
    try:
        # Export as CSV (mime type for CSV export)
        request = drive.files().export(
            fileId=SPREADSHEET_ID,
            mimeType='text/csv'
        )
        csv_content = request.execute()

        if isinstance(csv_content, bytes):
            csv_text = csv_content.decode('utf-8')
        else:
            csv_text = csv_content

        # Parse CSV
        reader = csv.reader(io.StringIO(csv_text))
        rows = list(reader)

        if not rows:
            print("[ERROR] No data in exported CSV")
            sys.exit(1)

        # Assuming first column is employee name/ID, count non-empty rows
        total_count = sum(1 for r in rows[1:] if r and len(r) > 0 and str(r[0]).strip())

        print(f"  [OK] Employee Data: {total_count} rows")
        print("\n" + "="*80)
        print(f"\n{SHEET_DESC.upper()} SUMMARY\n")
        print(f"Total entries: {total_count}\n")
        print("="*80 + "\n")

        return {'total': total_count}

    except Exception as e:
        print(f"[ERROR] Exporting via Drive: {e}")
        sys.exit(1)

def print_summary(results, total_count):
    """Print results table."""
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

if __name__ == '__main__':
    read_employee_sheet()
