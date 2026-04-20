#!/usr/bin/env python3
"""
Send GWC rejection emails with proper Taleemabad HTML format to pilot reviewers.
"""

import os, sys, smtplib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scripts.utils.safe_send import safe_sendmail

# Load environment
env_path = os.path.join(os.path.dirname(__file__), "../../..", ".env")
load_dotenv(env_path)

EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not EMAIL_USER or not EMAIL_PASSWORD:
    print("ERROR: EMAIL_USER or EMAIL_PASSWORD not found in .env")
    sys.exit(1)

# Read all 6 drafts
drafts = [
    ('Ali Jawad', 'scripts/jobs/hackathon/ali_jawad_warm_800.txt'),
    ('Umair Solangi', 'scripts/jobs/hackathon/umair_solangi_warm_800.txt'),
    ('Sultan Muhammad Hamad Sheharyar', 'scripts/jobs/hackathon/sultan_sheharyar_warm_800.txt'),
    ('Moaz Nadeem', 'scripts/jobs/hackathon/moaz_nadeem_warm_scorecard.txt'),
    ('Alishba Ramzan', 'scripts/jobs/hackathon/alishba_ramzan_warm_scorecard.txt'),
    ('Maryam Rafaqat', 'scripts/jobs/hackathon/maryam_rafaqat_warm_scorecard.txt'),
]

def format_draft_as_html(raw_text):
    """Convert plain text draft to HTML with Taleemabad format."""
    lines = raw_text.split('\n')
    html_body = ''

    content_started = False
    for line in lines:
        if line.startswith('Dear '):
            content_started = True
        if not content_started:
            continue
        if not line.strip():
            html_body += '<br>'
        elif line.startswith('## '):
            heading = line.replace('## ', '').strip()
            html_body += f'<p style="color: #1565c0; font-weight: bold; margin-top: 20px; margin-bottom: 10px; font-size: 14px;">{heading}</p>'
        elif line.startswith('**') and line.endswith('**'):
            text = line.replace('**', '')
            html_body += f'<p style="font-weight: bold;">{text}</p>'
        else:
            html_body += f'<p style="text-align: justify; line-height: 1.6;">{line}</p>'

    return html_body

# HTML template
html_template = """
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Georgia, serif; background-color: #f0f4f0; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: white; border-left: 4px solid #1565c0; }
        .header { background: white; padding: 20px; text-align: center; border-bottom: 2px solid #1565c0; }
        .logo { font-weight: bold; color: #333; margin-bottom: 10px; font-size: 18px; }
        .small-header { font-size: 11px; color: #1565c0; font-weight: bold; letter-spacing: 1px; margin-bottom: 15px; }
        .title { font-size: 24px; color: #1565c0; font-weight: bold; margin: 15px 0; }
        .subtitle { font-size: 14px; color: #666; margin-bottom: 15px; }
        .divider { height: 2px; background: #1565c0; margin: 20px 0; }
        .body { padding: 30px; }
        .body p { font-size: 11pt; line-height: 1.6; text-align: justify; color: #333; margin: 12px 0; }
        .draft-section { page-break-inside: avoid; margin: 40px 0; padding: 20px; border: 1px solid #ddd; border-radius: 4px; background: #fafafa; }
        .draft-name { color: #1565c0; border-bottom: 2px solid #1565c0; padding-bottom: 10px; font-size: 16px; font-weight: bold; }
        .pilot-note { background: #e3f2fd; border-left: 4px solid #1565c0; padding: 15px; margin-bottom: 20px; font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Taleemabad</div>
            <div class="small-header">PEOPLE & CULTURE • REJECTION DECISION</div>
            <div class="title">We're reflecting on your Hackathon 2026 application</div>
            <div class="subtitle">Hackathon 2026</div>
            <div class="divider"></div>
        </div>
        <div class="body">
            <div class="pilot-note">
                <strong>PILOT REVIEW</strong><br>
                All 6 candidate rejection emails below. Review for: tone, authenticity, format, and accuracy.
                All use SOP-compliant format (no em dashes, verified quotes, matched voice per candidate).
            </div>
            {CONTENT}
        </div>
    </div>
</body>
</html>
"""

# Build pilot content
pilot_content = ''
for name, filepath in drafts:
    with open(filepath, 'r') as f:
        raw_text = f.read()

    formatted = format_draft_as_html(raw_text)
    pilot_content += f"""
    <div class="draft-section">
        <div class="draft-name">{name}</div>
        {formatted}
    </div>
    """

full_html = html_template.replace("{CONTENT}", pilot_content)

# Create email
msg = MIMEMultipart("alternative")
msg["From"]    = EMAIL_USER
msg["To"]      = "ayesha.khan@taleemabad.com"
msg["Cc"]      = "aymen.abid@taleemabad.com"
msg["Subject"] = "PILOT: Hackathon 2026 GWC Rejection Emails (6 candidates) - HTML Format"

msg.attach(MIMEText(full_html, "html", "utf-8"))

# Send via SMTP
recipients = ["ayesha.khan@taleemabad.com", "aymen.abid@taleemabad.com"]
with smtplib.SMTP("smtp.gmail.com", 587) as s:
    s.ehlo()
    s.starttls()
    s.login(EMAIL_USER, EMAIL_PASSWORD)
    safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(),
                  context="hackathon_gwc_rejection_pilot_html")

print("[SENT] Pilot with proper Taleemabad HTML format")
print("  TO: ayesha.khan@taleemabad.com")
print("  CC: aymen.abid@taleemabad.com")
print("  Subject: PILOT: Hackathon 2026 GWC Rejection Emails (6 candidates) - HTML Format")
