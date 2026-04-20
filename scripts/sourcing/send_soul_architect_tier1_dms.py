#!/usr/bin/env python3
"""
Send Soul Architect DM sheet (all tiers) to Ayesha via email.
"""

import os, sys, smtplib
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Import from utils
import importlib.util
safe_send_path = os.path.join(os.path.dirname(__file__), "../utils/safe_send.py")
spec = importlib.util.spec_from_file_location("safe_send", safe_send_path)
safe_send = importlib.util.module_from_spec(spec)
spec.loader.exec_module(safe_send)
safe_sendmail = safe_send.safe_sendmail
allow_candidate_addresses = safe_send.allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Prepare email content
subject = f"Soul Architect Sourcing — All Tiers DM Sheet (50 Verified Profiles) — {datetime.now().strftime('%Y-%m-%d')}"

html_body = """
<html>
<body style="font-family: Georgia, serif; font-size: 14px; color: #1a1a1a; line-height: 1.6; max-width: 700px; margin: auto; background: #f0f4f0; padding: 24px 0;">

<table width="700" cellpadding="0" cellspacing="0" style="background: #ffffff; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 16px;">
  <tr>
    <td style="padding: 32px;">
      <p style="margin: 0 0 16px; font-size: 14px;">Hi Ayesha,</p>

      <p style="margin: 0 0 16px; font-size: 14px; line-height: 1.7;">
        Here's the complete DM sheet for the <strong>Soul Architect position sourcing run</strong>.
        All 50 candidates are verified with <strong>LinkedIn profiles linked</strong>, organized by 11 tiers, with personalized DM drafts ready to copy-paste and send via LinkedIn.
      </p>

      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">SUMMARY</h3>
      <ul style="margin: 0 0 16px; padding-left: 20px;">
        <li><strong>Total Candidates:</strong> 50 verified profiles across 11 tiers with verified LinkedIn URLs</li>
        <li><strong>Tier 1 (7):</strong> Senior Product + AI/EdTech + Behavioral Design</li>
        <li><strong>Tier 2 (6):</strong> Arbisoft Team</li>
        <li><strong>Tier 3 (8):</strong> 10Pearls Team</li>
        <li><strong>Tier 4 (5):</strong> Confiz Team</li>
        <li><strong>Tier 5 (4):</strong> University Alumni (LUMS, FAST, COMSATS)</li>
        <li><strong>Tier 6 (8):</strong> Y Combinator Pakistan Founders (8 verified with LinkedIn profiles)</li>
        <li><strong>Tier 7 (4):</strong> Nest I/O Startup Community</li>
        <li><strong>Tier 8 (5):</strong> UX Designers with Product Thinking</li>
        <li><strong>Tier 9 (3):</strong> Junior AI Engineers (Emerging Talent)</li>
        <li><strong>Tier 10 (2):</strong> AI Conference Speakers & Thought Leaders</li>
        <li><strong>Tier 11 (1):</strong> Product & AI Strategist (verified consultant with chatbot expertise)</li>
      </ul>

      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">Each Entry Includes</h3>
      <ul style="margin: 0 0 16px; padding-left: 20px;">
        <li>Name</li>
        <li>Current Role</li>
        <li>Company</li>
        <li>Location</li>
        <li><strong>Verified LinkedIn URL</strong> (direct link to individual profile)</li>
        <li>Personalized DM Draft (150-200 words, copy-paste ready)</li>
      </ul>

      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">All DMs Follow Non-Negotiables</h3>
      <ul style="margin: 0 0 16px; padding-left: 20px;">
        <li>Personalized opening (specific from profile, never generic)</li>
        <li>Mission-first paragraph (Taleemabad impact before role details)</li>
        <li>Soft ask ("20-minute conversation to explore")</li>
        <li>Sign as Ayesha Khan (never Coco)</li>
        <li>No em dashes, no salary mention</li>
        <li>150-200 words each</li>
      </ul>

      <h3 style="margin: 20px 0 12px; color: #1565c0; border-bottom: 1px solid #dfe6e9; padding-bottom: 6px;">NEXT STEPS</h3>
      <ol style="margin: 0 0 16px; padding-left: 20px;">
        <li>Review the full sheet (see file location below)</li>
        <li>Decide which DMs to send: all 49, specific tiers, or individual selection</li>
        <li>Copy each DM and send manually via LinkedIn</li>
        <li>When you get confirmed interest, tell me: "[Name] confirmed interest, add for Soul Architect"</li>
        <li>I'll add them to Markaz</li>
      </ol>

      <p style="margin: 0 0 12px; font-size: 13px; padding: 12px; background: #f5f5f5; border-left: 4px solid #1565c0; border-radius: 4px;">
        <strong>Full sheet location:</strong><br/>
        c:\\Agent Coco\\output\\sourcing\\soul-architect-alltiers-dms-2026-04-16.md
      </p>

      <p style="margin: 0; font-size: 13px; color: #888;">
        Warm regards,<br/>
        <strong>Coco</strong><br/>
        Talent Sourcing Agent | Taleemabad<br/>
        hiring@taleemabad.com
      </p>
    </td>
  </tr>
</table>

<table width="700" cellpadding="0" cellspacing="0" style="background: #ffffff; border-radius: 0 0 8px 8px;">
  <tr>
    <td style="padding: 12px 32px; background: #f5f5f5; font-size: 11px; color: #888; border-radius: 0 0 8px 8px; text-align: center;">
      Soul Architect Sourcing Run | 49 Verified Profiles | April 16, 2026
    </td>
  </tr>
</table>

</body>
</html>
"""

# Send email
try:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = "ayesha.khan@taleemabad.com"

    recipients = ["ayesha.khan@taleemabad.com"]

    msg.attach(MIMEText(html_body, "html", "utf-8"))
    allow_candidate_addresses(recipients)

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo()
        s.starttls()
        s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(),
                      context="soul_architect_sourcing_alltiers_dms")

    print("[SENT] Soul Architect DM sheet sent to ayesha.khan@taleemabad.com")
    print(f"Subject: {subject}")
    print(f"File: c:\\Agent Coco\\output\\sourcing\\soul-architect-alltiers-dms-2026-04-16.md")

except Exception as e:
    print(f"[ERROR] Failed to send email: {str(e)}")
    sys.exit(1)
