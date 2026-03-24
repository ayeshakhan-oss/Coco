"""
Check existing Gmail labels and list them.
"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file("token_gmail.json")
service = build("gmail", "v1", credentials=creds)

results = service.users().labels().list(userId="me").execute()
labels = results.get("labels", [])

print("Existing labels:")
for l in sorted(labels, key=lambda x: x["name"]):
    print(f"  [{l['id']}] {l['name']}")
