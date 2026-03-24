import base64, sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

TOKEN_FILE = 'C:/Users/Dell/Downloads/token.json'
creds = Credentials.from_authorized_user_file(TOKEN_FILE, [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
])
service = build('gmail', 'v1', credentials=creds)

def get_full_body(payload):
    plain = ''
    html = ''
    def extract(part):
        nonlocal plain, html
        mime = part.get('mimeType', '')
        data = part.get('body', {}).get('data', '')
        if mime == 'text/plain' and data:
            plain = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        elif mime == 'text/html' and data:
            html = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        for subpart in part.get('parts', []):
            extract(subpart)
    extract(payload)
    return plain, html

q = 'subject:"Invitation for the Values Interview for Field Coordinator" "Amina Batool" from:ayesha.khan@taleemabad.com'
r = service.users().messages().list(userId='me', q=q, maxResults=1).execute()
msgs = r.get('messages', [])

for m in msgs:
    msg = service.users().messages().get(userId='me', id=m['id'], format='full').execute()
    headers = {h['name']: h['value'] for h in msg['payload']['headers']}
    plain, html = get_full_body(msg['payload'])
    print(f"Subject: {headers.get('Subject','')}")
    print(f"\n--- PLAIN TEXT ---\n{plain[:2000]}")
    # Save HTML to file instead of printing
    with open('C:/Agent Coco/invite_template.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("\nHTML saved to C:/Agent Coco/invite_template.html")
