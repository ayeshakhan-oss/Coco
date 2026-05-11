"""
Send Soul Architect Screening PILOT Report to Ayesha Khan & Jawwad Ali
==================================================================================
PILOT mode: For review + approval before live send to hiring manager

Recipients:
  TO: ayesha.khan@taleemabad.com
  CC: jawwad.ali@taleemabad.com

Status: PILOT — Awaiting approval
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv('C:\\Agent Coco\\.env')

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

SENDER = EMAIL_USER
TO_RECIPIENT = 'ayesha.khan@taleemabad.com'
CC_RECIPIENT = 'jawwad.ali@taleemabad.com'

SUBJECT = "[PILOT] Soul Architect Screening Report — Job 26 (42 candidates screened, 5 shortlisted)"

# Email body (plain text intro)
BODY = """Hi Ayesha and Jawwad,

Please see attached: Soul Architect screening report (PILOT mode).

SUMMARY:
  • Total candidates screened: 42
  • Shortlisted (top tier): 5
  • Maybe / Consider: 7
  • No Hire: 30

TOP 5 SHORTLISTED:
  1. Muhammad Abdullah Safdar (95% — #1 TOP PICK)
  2. Zikra Fiaz (92% — #2 TOP PICK)
  3. Aaqib Khan (90% — #3 TOP PICK)
  4. Arslan Saleem (82% — SHORTLIST)
  5. Asad Nawaz (78% — SHORTLIST)

EVALUATION CRITERIA (5):
  • Product Mindset
  • Builder Orientation
  • Human-Centered Depth
  • Comfort with Ambiguity
  • Bonus Signals (AI/chatbot, conversational design)

KEY OBSERVATION:
Strong product instincts across cohort, 4-7 yrs relevant experience. Major gap:
limited behavioral science background. Only 2 candidates show depth in human-centered
research methodology. Application responses more valuable than CVs for identifying
philosophical grounding on AI ethics.

SOP USED:
  • CV Screening SOP (cv-screening.md)
  • Execution Discipline Protocol
  • Locked format (Job 26 April 6 reference)
  • All 8 QA checklist items verified

CV HYPERLINKS:
All 12 candidate CVs uploaded to Google Drive and hyperlinked in report.
All links verified and active.

NEXT STEPS:
  1. Review PILOT report
  2. Check candidate data accuracy
  3. Verify CV links are working
  4. Approve or request changes
  5. If approved: forward to Waqas Tanveer (hiring manager)

STATUS: PILOT READY — Awaiting your approval

Report generated: 2026-04-20
Using locked format specification (zero drift guaranteed)

Best regards,
Coco
Talent Acquisition Agent
"""

# Read the HTML report
with open('C:\\Agent Coco\\soul_architect_screening_pilot_2026-04-20_FINAL.html', 'r') as f:
    html_report = f.read()

# Create message
msg = MIMEMultipart('alternative')
msg['Subject'] = SUBJECT
msg['From'] = SENDER
msg['To'] = TO_RECIPIENT
msg['Cc'] = CC_RECIPIENT

# Add text part
msg.attach(MIMEText(BODY, 'plain'))

# Add HTML part
msg.attach(MIMEText(html_report, 'html'))

# Prepare recipients list
recipients = [TO_RECIPIENT, CC_RECIPIENT]

print("\n" + "="*70)
print("SOUL ARCHITECT SCREENING PILOT — EMAIL PREPARATION")
print("="*70)
print()
print(f"Subject: {SUBJECT}")
print(f"From: {SENDER}")
print(f"To: {TO_RECIPIENT}")
print(f"Cc: {CC_RECIPIENT}")
print()
print(f"Body preview:\n{BODY[:200]}...")
print()
print("HTML Report attached: [OK]")
print()
print("="*70)
print("READY TO SEND")
print("="*70)
print()
print("Recipients:")
print(f"  • TO: Ayesha Khan (ayesha.khan@taleemabad.com)")
print(f"  • CC: Jawwad Ali (jawwad.ali@taleemabad.com)")
print()
print("Status: PILOT MODE")
print("Action: Awaiting approval before forwarding to hiring manager")
print()
print("To send PILOT report, run:")
print("  python send_soul_architect_pilot_to_ayesha_jawwad.py --send")
print()
print("="*70)

# Check for --send flag
import sys
if '--send' in sys.argv:
    print("\n[SENDING EMAIL...]")
    try:
        # Connect to Gmail SMTP
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(SENDER, EMAIL_PASSWORD)

        # Send email
        server.sendmail(SENDER, recipients, msg.as_string())
        server.quit()

        print("\n[OK] EMAIL SENT SUCCESSFULLY")
        print()
        print("Recipients received:")
        print(f"  • ayesha.khan@taleemabad.com (TO)")
        print(f"  • jawwad.ali@taleemabad.com (CC)")
        print()
        print("PILOT report sent for review and approval.")
        print()
    except Exception as e:
        print(f"\n✗ FAILED TO SEND: {e}")
        print()
else:
    print("\n[DRY RUN — EMAIL NOT SENT]")
    print()
    print("To actually send, run with --send flag:")
    print("  python send_soul_architect_pilot_to_ayesha_jawwad.py --send")
    print()
