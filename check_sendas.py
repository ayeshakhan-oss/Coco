from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = 'C:/Users/Dell/Downloads/token.json'
creds = Credentials.from_authorized_user_file(TOKEN_FILE, [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
])
service = build('gmail', 'v1', credentials=creds)

aliases = service.users().settings().sendAs().list(userId='me').execute()
for a in aliases.get('sendAs', []):
    print(f"{'[DEFAULT] ' if a.get('isDefault') else ''}{'[PRIMARY] ' if a.get('isPrimary') else ''}{a['sendAsEmail']} — {a.get('displayName','')}")
