"""
One-time OAuth setup for Google Sheets API access.
Run this script once — a browser window will open for you to approve.
Token saved to token_sheets.json.
"""

from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import json

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

# Use absolute paths
script_dir = Path(__file__).parent.parent.parent
creds_file = script_dir / "data" / "credentials.json"
token_file = script_dir / "token_sheets.json"

flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), SCOPES)
creds = flow.run_local_server(port=0)

with open(str(token_file), "w") as f:
    f.write(creds.to_json())

print("Done. token_sheets.json saved.")
print("Scopes granted:", creds.scopes)
