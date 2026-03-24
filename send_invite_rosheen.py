import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = 'C:/Users/Dell/Downloads/token.json'
creds = Credentials.from_authorized_user_file(TOKEN_FILE, [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
])
service = build('gmail', 'v1', credentials=creds)

with open('C:/Agent Coco/invite_template.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('Hi Amina Batool,', 'Hi Rosheen,')

msg = MIMEMultipart('alternative')
msg['Subject'] = 'Invitation for the Values Interview for Field Coordinator, Research & Impact Studies - Rosheen Naeem'
msg['From'] = 'Taleemabad Markaz Hiring <hiring@taleemabad.com>'
msg['To'] = 'rosheen.naeem@gmail.com'
msg['Cc'] = 'ayesha.khan@taleemabad.com'

msg.attach(MIMEText(html, 'html'))

raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
print(f"Sent to rosheen.naeem@gmail.com — Message ID: {result['id']}")
