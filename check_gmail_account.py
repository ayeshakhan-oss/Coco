from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = 'C:/Users/Dell/Downloads/token.json'
creds = Credentials.from_authorized_user_file(TOKEN_FILE, [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
])
service = build('gmail', 'v1', credentials=creds)

profile = service.users().getProfile(userId='me').execute()
print(f"Authenticated as: {profile['emailAddress']}")
