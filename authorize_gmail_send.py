from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

flow = InstalledAppFlow.from_client_secrets_file(
    'C:/Agent Coco/credentials.json',
    SCOPES
)

creds = flow.run_local_server(port=0)

with open('C:/Users/Dell/Downloads/token.json', 'w') as f:
    f.write(creds.to_json())

print("Authorization complete. Token saved.")
