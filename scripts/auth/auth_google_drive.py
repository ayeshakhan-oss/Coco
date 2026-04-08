"""
One-time Google Drive OAuth — adds Drive file upload scope.
Run once, approve in browser, saves token_drive.json.
"""
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

flow = InstalledAppFlow.from_client_secrets_file(
    "c:/Agent Coco/credentials.json", SCOPES)
creds = flow.run_local_server(port=0)

with open("c:/Agent Coco/token_drive.json", "w") as f:
    f.write(creds.to_json())

print("Drive token saved to token_drive.json")
print("Scopes:", creds.scopes)
