#!/usr/bin/env python3
"""
Send Soul Architect 7 New Candidates sheet to Ayesha
"""
import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

sys.path.insert(0, "c:/Agent Coco")

from scripts.utils.safe_send import safe_sendmail

load_dotenv(dotenv_path="c:/Agent Coco/.env")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

RECIPIENT = ["ayesha.khan@taleemabad.com"]
FILE_PATH = r"c:\Agent Coco\output\sourcing\Soul_Architect_7_New_Candidates_2026-04-18.xlsx"

print("\n=== SENDING SOUL ARCHITECT 7 NEW CANDIDATES SHEET ===\n")

try:
    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.starttls()
    s.login(EMAIL_USER, EMAIL_PASSWORD)
    print("[OK] Connected to Gmail SMTP")

    # Create email
    msg = MIMEMultipart()
    msg["Subject"] = "Soul Architect — 7 Additional Product Professionals (User-Researched)"
    msg["From"] = EMAIL_USER
    msg["To"] = RECIPIENT[0]

    body = """Hi Ayesha,

I've compiled the 7 new candidates you researched into a dedicated Excel sheet.

**SHEET CONTENTS:**
- 7 new product/design-focused candidates (all Pakistan-based)
- Tier: NEW (fresh additions to your sourcing slate)
- All with verified LinkedIn links

**CANDIDATES:**
1. Mohsin Khan — Product Automation | UIUX Designer
2. Zohaib Khan — UI/UX Designer
3. Ahmed Shahwar — User Research Associate (AI)
4. Syed Sarib Sultan — Product Design Specialist
5. Parivash Mir — UX Designer | Content Design | AI
6. Shafaq Noor — Communications/Brand
7. Laraib Piracha — Product & Growth Analyst

Ready to review, rank, and draft DMs for any of these candidates once you prioritize.

Best,
Coco
"""

    msg.attach(MIMEText(body, "plain"))

    # Attach Excel file
    with open(FILE_PATH, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=Soul_Architect_7_New_Candidates_2026-04-18.xlsx")
        msg.attach(part)

    # Send via safe_sendmail
    safe_sendmail(
        s,
        EMAIL_USER,
        RECIPIENT,
        msg.as_string(),
        context="soul_architect_7_new_candidates_sheet"
    )

    s.quit()

    print(f"[OK] 7-candidate sheet sent to {RECIPIENT[0]}")
    print(f"File: {FILE_PATH}")
    print(f"Total: 7 new verified professionals")

except Exception as e:
    print(f"[FAILED] {e}")
    sys.exit(1)
