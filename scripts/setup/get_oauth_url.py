"""
Generate OAuth Authorization URL with Broader Scopes
===================================================
Copy-paste this URL in your browser to authorize
"""

from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os

CREDENTIALS_FILE = 'data/credentials.json'

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]

if not os.path.exists(CREDENTIALS_FILE):
    print(f"[ERROR] {CREDENTIALS_FILE} not found")
    exit(1)

flow = InstalledAppFlow.from_client_secrets_file(
    CREDENTIALS_FILE,
    scopes=SCOPES
)

# Get the authorization URL
auth_url, state = flow.authorization_url(access_type='offline', prompt='consent')

print("\n" + "="*80)
print("AUTHORIZATION URL - COPY AND PASTE IN YOUR BROWSER")
print("="*80)
print(f"\n{auth_url}\n")
print("="*80)
print("\nSteps:")
print("1. Copy the URL above")
print("2. Open your browser and paste it")
print("3. Login and authorize")
print("4. You'll see a code - copy it and send back to me")
print("\nOr: If browser opens automatically, just authorize and come back here")
print("="*80)

# Save flow for later use
with open('.claude/config/oauth_flow.json', 'w') as f:
    json.dump({
        'state': state,
        'credentials_file': CREDENTIALS_FILE
    }, f)
