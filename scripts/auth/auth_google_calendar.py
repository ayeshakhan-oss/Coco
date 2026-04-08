"""
One-time Google Calendar OAuth authentication.
Run this once to generate token.json.
After that, all other scripts use token.json automatically.
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
]

CREDENTIALS_FILE = "c:/Agent Coco/credentials.json"
TOKEN_FILE = "c:/Agent Coco/token.json"


def main():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing existing token...")
            creds.refresh(Request())
        else:
            print("Opening browser for Google login...")
            print("Log in with: ayesha.khan@taleemabad.com")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        print(f"\ntoken.json saved to: {TOKEN_FILE}")
    else:
        print("token.json already valid — no action needed.")

    print("\nAuthentication successful. Google Calendar API is ready.")


if __name__ == '__main__':
    main()
