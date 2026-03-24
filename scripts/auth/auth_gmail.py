"""
One-time Gmail OAuth authorization.
Run this script once — it will open a browser for you to approve Gmail access.
A new token_gmail.json will be saved with Gmail scopes.
"""
from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.readonly",
]

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)

with open("token_gmail.json", "w") as f:
    f.write(creds.to_json())

print("Gmail token saved to token_gmail.json")
print(f"Scopes granted: {creds.scopes}")
