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

html_content = '''<html><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<h2>Talent Slate - Pakistan Development Sector Professionals</h2>
<p><strong>Date:</strong> May 5, 2026<br/>
<strong>Total Profiles:</strong> 35 verified LinkedIn profiles<br/>
<strong>Organizations:</strong> Teach For Pakistan, Malala Fund, Acumen, Atlas Corps, British Council, CERP, SDPI, Karandaaz, World Bank, DAI</p>

<table style="border-collapse: collapse; width: 100%; font-size: 12px;">
<tr style="background-color: #2f4fa2; color: white;">
<th style="border: 1px solid #ddd; padding: 8px;">Organization</th>
<th style="border: 1px solid #ddd; padding: 8px;">Name</th>
<th style="border: 1px solid #ddd; padding: 8px;">Role</th>
<th style="border: 1px solid #ddd; padding: 8px;">LinkedIn</th>
</tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">Teach For Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Khadija Shahper Bakhtiar</td><td style="border: 1px solid #ddd; padding: 8px;">Founder & CEO</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/khadija-shahper-bakhtiar-045b60122/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">Teach For Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Amna Junaid</td><td style="border: 1px solid #ddd; padding: 8px;">Program Lead</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/amna-junaid-a1342921a/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">Teach For Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Sahar Gul</td><td style="border: 1px solid #ddd; padding: 8px;">Education Program Lead</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/sahar-gul/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">Teach For Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Yousra Rashid</td><td style="border: 1px solid #ddd; padding: 8px;">Education Fellow</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/yousra-rashid-6a29432a2/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">Teach For Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Aliza Mir</td><td style="border: 1px solid #ddd; padding: 8px;">Trainer & Project Leader</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/aliza-mir-343ab21a4/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">Teach For Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Momin Hashmi</td><td style="border: 1px solid #ddd; padding: 8px;">Fellowship Alum</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/momin-hashmi-a3735020a/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">Malala Fund</td><td style="border: 1px solid #ddd; padding: 8px;">Anam Akram</td><td style="border: 1px solid #ddd; padding: 8px;">Partnerships Manager</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/anam-akram-1981286/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">Acumen</td><td style="border: 1px solid #ddd; padding: 8px;">Zahra Amber</td><td style="border: 1px solid #ddd; padding: 8px;">Acumen Fellow</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/zahra-amber-808643b0/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">Atlas Corps</td><td style="border: 1px solid #ddd; padding: 8px;">Hafsah Sarfraz</td><td style="border: 1px solid #ddd; padding: 8px;">Atlas Corps Fellow</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/hafsah-sarfraz-b2345657/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">British Council Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Dr Maryam Rab</td><td style="border: 1px solid #ddd; padding: 8px;">Head of Research Programmes</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/dr-maryam-rab-72bb9444/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">CERP</td><td style="border: 1px solid #ddd; padding: 8px;">Jehanara Amin</td><td style="border: 1px solid #ddd; padding: 8px;">Program Manager</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/jehanaraamin/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">CERP</td><td style="border: 1px solid #ddd; padding: 8px;">Nouman Rasool</td><td style="border: 1px solid #ddd; padding: 8px;">Research Associate</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/nouman-rasool-7b431a6b/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">CERP</td><td style="border: 1px solid #ddd; padding: 8px;">Mehwish Waheed</td><td style="border: 1px solid #ddd; padding: 8px;">Research Associate</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/mehwish-waheed-21913318a/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">CERP</td><td style="border: 1px solid #ddd; padding: 8px;">Haseeb Ashraf</td><td style="border: 1px solid #ddd; padding: 8px;">Research Associate</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/haseeb-ashraf-12b4a442/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">CERP</td><td style="border: 1px solid #ddd; padding: 8px;">Fatima Khan</td><td style="border: 1px solid #ddd; padding: 8px;">Research Fellow</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://pk.linkedin.com/in/fatima-khan285">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">CERP</td><td style="border: 1px solid #ddd; padding: 8px;">Osama Nawaz</td><td style="border: 1px solid #ddd; padding: 8px;">Research Associate / Project Lead</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://pk.linkedin.com/in/osama-nawaz-0501a818">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">SDPI</td><td style="border: 1px solid #ddd; padding: 8px;">Abdullah Khalid</td><td style="border: 1px solid #ddd; padding: 8px;">Research Associate / Project Coordinator</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/abdullah-khalid-s/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">SDPI</td><td style="border: 1px solid #ddd; padding: 8px;">Dr. Kashif Majeed Salik</td><td style="border: 1px solid #ddd; padding: 8px;">Research Fellow</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/dr-kashif-majeed-salik-610b6126/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">SDPI</td><td style="border: 1px solid #ddd; padding: 8px;">Ebadat Ur Rehman Babar</td><td style="border: 1px solid #ddd; padding: 8px;">Research Associate</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/ebadatibnbabar/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">SDPI</td><td style="border: 1px solid #ddd; padding: 8px;">Qasim Shah</td><td style="border: 1px solid #ddd; padding: 8px;">Researcher</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/qasim-shah-2430b68/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">SDPI</td><td style="border: 1px solid #ddd; padding: 8px;">Shanza Khalid</td><td style="border: 1px solid #ddd; padding: 8px;">Consultant</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/shanza-khalid-277982101/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">Karandaaz Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Naureen Bakhsh Chaudhry</td><td style="border: 1px solid #ddd; padding: 8px;">MEL Specialist</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/naureenbchaudhry/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">Karandaaz Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Ayesha Chaudhry</td><td style="border: 1px solid #ddd; padding: 8px;">Associate - Debt</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/ayesha-chaudhry-265352139/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">Karandaaz Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Asra Malik</td><td style="border: 1px solid #ddd; padding: 8px;">Analyst - Innovation Investment & M&E</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/asra-malik-7b7791148/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">Karandaaz Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Hammad Akram</td><td style="border: 1px solid #ddd; padding: 8px;">Senior Analyst - Private Equity</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/hammad-akram-88ab72137/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">Karandaaz Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Waseem Malik</td><td style="border: 1px solid #ddd; padding: 8px;">Digital Payments Ecosystem Expert</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/waseemamalik/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">Karandaaz Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Danyal A.</td><td style="border: 1px solid #ddd; padding: 8px;">Senior Analyst - Marketing & Communications</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/danyalahmed1/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">Karandaaz Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Taimoor Ali</td><td style="border: 1px solid #ddd; padding: 8px;">Finance / Operations</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/taimoorali/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">Karandaaz Pakistan</td><td style="border: 1px solid #ddd; padding: 8px;">Adeeb Ali Mirza FCA</td><td style="border: 1px solid #ddd; padding: 8px;">Chief Financial Officer</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/adeebalimirza/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">World Bank</td><td style="border: 1px solid #ddd; padding: 8px;">Minahil Raza</td><td style="border: 1px solid #ddd; padding: 8px;">Energy Specialist</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/minahil-raza/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">World Bank</td><td style="border: 1px solid #ddd; padding: 8px;">Najy Benhassine</td><td style="border: 1px solid #ddd; padding: 8px;">Country Director</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/najy-benhassine-86b84263/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">World Bank</td><td style="border: 1px solid #ddd; padding: 8px;">Shabih Mohib</td><td style="border: 1px solid #ddd; padding: 8px;">Practice Manager</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/shabih-mohib-4a0337106/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">World Bank</td><td style="border: 1px solid #ddd; padding: 8px;">Illango Patchamuthu</td><td style="border: 1px solid #ddd; padding: 8px;">Consultant</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/illango-patchamuthu-40660235/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">World Bank</td><td style="border: 1px solid #ddd; padding: 8px;">Rana Khuram</td><td style="border: 1px solid #ddd; padding: 8px;">Program Officer</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/rana-khuram-2a37008/">Profile</a></td></tr>
<tr><td style="border: 1px solid #ddd; padding: 8px;">DAI</td><td style="border: 1px solid #ddd; padding: 8px;">Waqar Ahmad Khan</td><td style="border: 1px solid #ddd; padding: 8px;">New Business Development Manager</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://www.linkedin.com/in/waqar-ahmad-khan-79432819/">Profile</a></td></tr>
<tr style="background-color: #f9f9f9;"><td style="border: 1px solid #ddd; padding: 8px;">DAI</td><td style="border: 1px solid #ddd; padding: 8px;">Arsalan Ali F.</td><td style="border: 1px solid #ddd; padding: 8px;">Senior Consultant</td><td style="border: 1px solid #ddd; padding: 8px;"><a href="https://pk.linkedin.com/in/arsalan-ali-f-2b82491b">Profile</a></td></tr>
</table>

<p><strong>Next Step:</strong> Reply indicating who to draft DMs for.</p>
</body></html>'''

msg = MIMEMultipart('alternative')
msg['Subject'] = 'Pakistan Development Organizations - 35 Verified LinkedIn Candidates (May 5, 2026)'
msg['From'] = 'Coco <zeshan.dhillon@taleemabad.com>'
msg['To'] = 'ayesha.khan@taleemabad.com'

msg.attach(MIMEText(html_content, 'html'))

raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
print(f"✓ Email sent to ayesha.khan@taleemabad.com")
print(f"Message ID: {result['id']}")
