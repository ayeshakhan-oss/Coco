"""
One-time OAuth setup for Google Sheets API access.
Run this script once — a browser window will open for you to approve.
Token saved to token_sheets.json.
"""

from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)

with open("token_sheets.json", "w") as f:
    f.write(creds.to_json())

print("Done. token_sheets.json saved.")
print("Scopes granted:", creds.scopes)
