#!/usr/bin/env python3
"""
Automate Gmail Hiring Label Setup
- Creates "Hiring" label
- Retroactively labels all emails from/to hiring@taleemabad.com
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail(credentials_json_path):
    """Authenticate with Gmail API using provided credentials."""
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_json_path, SCOPES)
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

def create_label(service, label_name):
    """Create a label if it doesn't exist."""
    try:
        # Get existing labels
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        # Check if label already exists
        for label in labels:
            if label['name'] == label_name:
                print(f"[+] Label '{label_name}' already exists (ID: {label['id']})")
                return label['id']

        # Create new label
        label_body = {
            'name': label_name,
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show'
        }
        created_label = service.users().labels().create(
            userId='me', body=label_body).execute()
        print(f"[+] Created label '{label_name}' (ID: {created_label['id']})")
        return created_label['id']
    except Exception as e:
        print(f"[!] Error creating label: {e}")
        return None

def find_hiring_emails(service):
    """Find all emails from/to hiring@taleemabad.com"""
    try:
        query = 'from:hiring@taleemabad.com OR to:hiring@taleemabad.com'
        results = service.users().messages().list(
            userId='me', q=query, maxResults=500).execute()
        messages = results.get('messages', [])
        print(f"[+] Found {len(messages)} emails involving hiring@taleemabad.com")
        return messages
    except Exception as e:
        print(f"[!] Error searching emails: {e}")
        return []

def apply_label_to_emails(service, message_ids, label_id):
    """Apply label to all found emails."""
    if not message_ids:
        print("[*] No emails to label.")
        return

    success = 0
    failed = 0

    for msg_id in message_ids:
        try:
            service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'addLabelIds': [label_id]}
            ).execute()
            success += 1
            if success % 10 == 0:
                print(f"  [+] Labeled {success}/{len(message_ids)} emails...")
        except Exception as e:
            failed += 1
            print(f"  [!] Failed to label message {msg_id}: {e}")

    print(f"[+] Successfully labeled {success} emails")
    if failed > 0:
        print(f"[!] Failed to label {failed} emails")

def main():
    # Path to credentials
    credentials_path = "c:\\Agent Coco\\credentials.json"

    # Check if credentials file exists
    if not os.path.exists(credentials_path):
        print(f"[!] Credentials file not found at {credentials_path}")
        print("\n[*] Please save your OAuth credentials JSON to: c:\\Agent Coco\\credentials.json")
        return

    print("[*] Authenticating with Gmail API...")
    service = authenticate_gmail(credentials_path)

    print("\n[*] Creating 'Hiring' label...")
    label_id = create_label(service, 'Hiring')

    if not label_id:
        print("[!] Failed to create label. Exiting.")
        return

    print("\n[*] Searching for hiring emails...")
    messages = find_hiring_emails(service)

    if messages:
        print(f"\n[*] Applying label to {len(messages)} emails...")
        apply_label_to_emails(service, [msg['id'] for msg in messages], label_id)

    print("\n" + "="*60)
    print("[+] Setup complete!")
    print("\n[*] IMPORTANT: Manual step still required:")
    print("Go to Gmail > Settings > Filters and Blocked Addresses")
    print("Create filter: from:hiring@taleemabad.com OR to:hiring@taleemabad.com")
    print("Apply label: Hiring")
    print("="*60)

if __name__ == '__main__':
    main()
