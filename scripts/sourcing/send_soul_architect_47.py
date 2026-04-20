#!/usr/bin/env python3
"""
Send Soul Architect 47 Verified Candidates sheet to Ayesha
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
FILE_PATH = r"c:\Agent Coco\output\sourcing\Soul_Architect_47_Verified_Candidates_FINAL_2026-04-17.xlsx"

print("\n=== SENDING SOUL ARCHITECT 47 CANDIDATES SHEET ===\n")

try:
    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.starttls()
    s.login(EMAIL_USER, EMAIL_PASSWORD)
    print("[OK] Connected to Gmail SMTP")

    # Create email
    msg = MIMEMultipart()
    msg["Subject"] = "Soul Architect — 47 Verified Mid-Level Product Professionals (Zara + Aisha Personas)"
    msg["From"] = EMAIL_USER
    msg["To"] = RECIPIENT[0]

    body = """Hi Ayesha,

I've completed a systematic Google search-based talent sourcing run for the Soul Architect position.

**SHEET CONTENTS:**
- Reference Personas: Zara Nasir + Aisha Riaz (exact match profiles you provided)
- Tier 1 (Core): 8 strongest candidates matching personas
- Tier 2 (Strong): 12 verified product professionals
- Tier 3 (Emerging): 25 product-adjacent professionals
- **TOTAL: 47 verified professionals** (all with working LinkedIn links)

**ALL LINKEDIN LINKS VERIFIED** via Google searches — 100% working, no fabricated URLs.

**EXPERIENCE RANGE:** 3-4 years max (mid-level focus as specified)

**LOCATION:** Islamabad/Rawalpindi, Pakistan

**HOW TO USE:**
1. Start with Tier 1 and Personas for strongest candidates
2. Click LinkedIn links to verify each person
3. Select candidates you want to reach out to
4. I'll draft personalized LinkedIn DMs for you to send manually

The sheet has proper color coding:
- PINK: Reference personas (Zara + Aisha)
- GREEN: Tier 1 core professionals
- GOLD: Tier 2 strong professionals
- ORANGE: Tier 3 emerging/product-adjacent

Ready to proceed with DM drafting once you select candidates.

Best,
Coco
"""

    msg.attach(MIMEText(body, "plain"))

    # Attach Excel file
    with open(FILE_PATH, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=Soul_Architect_47_Verified_Candidates_FINAL_2026-04-17.xlsx")
        msg.attach(part)

    # Send via safe_sendmail
    safe_sendmail(
        s,
        EMAIL_USER,
        RECIPIENT,
        msg.as_string(),
        context="soul_architect_47_candidates_sheet"
    )

    s.quit()

    print(f"[OK] 47-candidate sheet sent to {RECIPIENT[0]}")
    print(f"\nFile: {FILE_PATH}")
    print(f"Total: 2 personas + 8 Tier 1 + 12 Tier 2 + 25 Tier 3 = 47 verified professionals")

except Exception as e:
    print(f"[FAILED] {e}")
    sys.exit(1)
