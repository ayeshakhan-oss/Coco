"""
OAuth Reauthorization with Broader Scopes
==========================================
Allows Google Drive + Sheets creation for talent sourcing
"""

from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os

CREDENTIALS_FILE = 'data/credentials.json'
TOKEN_FILE = '.claude/config/token_sheets_broad.json'

# Broader scopes for Drive + Sheets creation
SCOPES = [
    'https://www.googleapis.com/auth/drive',  # Full Drive access
    'https://www.googleapis.com/auth/spreadsheets'  # Full Sheets access
]

print("\n" + "="*80)
print("OAuth Reauthorization with Broader Scopes")
print("="*80)

if not os.path.exists(CREDENTIALS_FILE):
    print(f"\n[ERROR] OAuth client credentials not found: {CREDENTIALS_FILE}")
    print("Contact your admin to set up OAuth credentials")
    exit(1)

print("\n[STEP 1] Starting OAuth flow with broader scopes...")
print(f"  Scopes: Drive (full) + Sheets (full)")
print(f"\nA browser window will open for authorization.")
print("If it doesn't, copy the URL shown below and open it manually.\n")

try:
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES
    )

    # This opens a browser for user authorization
    credentials = flow.run_local_server(port=0)

    print("\n[OK] Authorization successful!")

    # Save the new token with broader scopes
    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)

    token_data = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)

    print(f"[OK] Token saved to: {TOKEN_FILE}")
    print("\n" + "="*80)
    print("[SUCCESS] OAuth Reauthorization Complete")
    print("="*80)
    print(f"\nYou now have:")
    print(f"  - Full Google Drive access (create/delete files)")
    print(f"  - Full Google Sheets access (create/modify sheets)")
    print(f"\nToken file: {TOKEN_FILE}")
    print(f"\nNext: Run create_smg_separate_sheet.py to create the separate sheet")

except Exception as e:
    print(f"\n[ERROR] Authorization failed: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure data/credentials.json exists")
    print("2. Make sure you're logged in with the right Google account")
    print("3. Try again in a few moments")
    exit(1)
