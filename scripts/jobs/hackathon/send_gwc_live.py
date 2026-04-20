#!/usr/bin/env python3
"""
Send GWC decision emails LIVE to 6 candidates.
CC: hiring@taleemabad.com, mashhood.rastgar@taleemabad.com, ayesha.khan@taleemabad.com
"""
import os, sys, smtplib, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv()

SENDER = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")

# HTML HELPERS (v8 design)
H = lambda t: f'<h2 style="color:#1565c0;font-size:17px;font-weight:bold;margin:36px 0 6px 0;letter-spacing:0.3px;">{t}</h2>'
P = lambda t: f'<p style="margin:0 0 18px 0;text-align:justify;font-family:Georgia,serif;font-size:15px;line-height:1.8;">{t}</p>'

FOOTER = """<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:40px;border-top:1px solid #e0e0e0;padding-top:20px;"><tr><td style="font-family:Georgia,serif;font-size:13px;color:#555;line-height:1.9;">Warm regards,<br><strong style="color:#1a1a1a;">People and Culture Team</strong><br><strong style="color:#1565c0;">Taleemabad</strong><br><a href="mailto:hiring@taleemabad.com" style="color:#1565c0;text-decoration:none;">hiring@taleemabad.com</a> &nbsp;|&nbsp; <a href="http://www.taleemabad.com" style="color:#1565c0;text-decoration:none;">www.taleemabad.com</a><br><span style="font-size:12px;color:#aaa;margin-top:4px;display:block;">Sent on behalf of Talent Acquisition Team by Coco</span></td></tr></table>"""

def header_block(subject_line):
    return f"""<table width="100%" cellpadding="0" cellspacing="0" style="border-radius:8px 8px 0 0;overflow:hidden;border-bottom:2px solid #1565c0;"><tr><td align="center" bgcolor="#ffffff" style="background-color:#ffffff;padding:28px 40px 22px 40px;"><p style="margin:0;font-family:Georgia,serif;font-size:11px;color:#1565c0;letter-spacing:2px;text-transform:uppercase;">People &amp; Culture &nbsp;&bull;&nbsp; Decision of Hackathon - Taleemabad</p><p style="margin:10px 0 4px 0;font-family:Georgia,serif;font-size:17px;font-weight:bold;color:#1565c0;line-height:1.4;">{subject_line}</p></td></tr></table>"""

def wrap(subject_line, body_html):
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body style="margin:0;padding:0;background-color:#f0f4f0;"><table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f4f0;padding:32px 0;"><tr><td align="center"><table width="620" cellpadding="0" cellspacing="0" style="max-width:620px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);"><tr><td>{header_block(subject_line)}</td></tr><tr><td style="background:#ffffff;padding:40px 52px 48px 52px;border-radius:0 0 8px 8px;font-family:Georgia,serif;font-size:15px;line-height:1.8;color:#1a1a1a;">{body_html}{FOOTER}</td></tr></table></td></tr></table></body></html>"""

def extract_email_body(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    # Normalize line endings
    content = content.replace("\r\n", "\n")
    lines = content.split("\n")
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("Dear "):
            body_start = i
            break
    return "\n".join(lines[body_start:]).strip()

def convert_emphasis(text):
    """Convert *text* to <strong>text</strong> for emphasis."""
    text = re.sub(r'\*([^*]+)\*', r'<strong>\1</strong>', text)
    return text

def text_to_html(text):
    paragraphs = text.split("\n\n")
    html = ""
    for para in paragraphs:
        para = para.strip()
        if para.startswith("## "):
            heading = para.replace("## ", "").strip()
            html += H(heading)
        elif para.startswith("**") and para.endswith("**") and len(para) > 4:
            heading = para.replace("**", "").strip()
            html += H(heading)
        elif para:
            para = convert_emphasis(para)
            html += P(para)
    return html

# 6 candidates with their email addresses and draft files
candidates = [
    ("Ali Jawad", "ali.jawad6204@gmail.com", "scripts/jobs/hackathon/ali_jawad_warm_800.txt", "Here's what we actually saw"),
    ("Umair Solangi", "bscs2112203@szabist.pk", "scripts/jobs/hackathon/umair_solangi_warm_800.txt", "Your backend is solid - here's what I actually noticed"),
    ("Sultan Muhammad Hamad Sheharyar", "pirzadahammadzakori@gmail.com", "scripts/jobs/hackathon/sultan_sheharyar_warm_800.txt", "We're concerned about some gaps - and here's why that matters"),
    ("Moaz Nadeem", "muazndm128@gmail.com", "scripts/jobs/hackathon/moaz_nadeem_warm_scorecard.txt", "You showed real promise - here's where we landed"),
    ("Alishba Ramzan", "alishbaramzan1@gmail.com", "scripts/jobs/hackathon/alishba_ramzan_warm_scorecard.txt", "Your learning attitude is real - and it matters"),
    ("Maryam Rafaqat", "maryamrafaqat88@gmail.com", "scripts/jobs/hackathon/maryam_rafaqat_warm_scorecard.txt", "Where we saw the gap"),
]

CC_LIST = [
    "hiring@taleemabad.com",
    "mashhood.rastgar@taleemabad.com",
    "ayesha.khan@taleemabad.com"
]

print("\n=== SENDING GWC DECISION EMAILS - LIVE ===\n")

# Whitelist candidate addresses before sending
candidate_emails = [email for _, email, _, _ in candidates]
allow_candidate_addresses(candidate_emails)
print(f"[OK] Approved {len(candidate_emails)} candidate addresses\n")

try:
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER, PASSWORD)
    print("[OK] Connected to Gmail SMTP\n")

    for name, email, filepath, subject in candidates:
        body_text = extract_email_body(filepath)
        body_html = text_to_html(body_text)
        html = wrap(subject, body_html)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"We're reflecting on your Hackathon 2026 application"
        msg["From"] = SENDER
        msg["To"] = email
        msg["Cc"] = ", ".join(CC_LIST)

        msg.attach(MIMEText(html, "html"))

        safe_sendmail(
            s,
            SENDER,
            [email] + CC_LIST,
            msg.as_string(),
            context=f"hackathon_decision_live_{name.replace(' ', '_')}"
        )
        print(f"[OK] Sent decision email to {name} ({email})")

    s.quit()
    print(f"\n" + "="*60)
    print(f"Sent 6 decision emails LIVE to:")
    for name, email, _, _ in candidates:
        print(f"  {name}: {email}")
    print(f"\nCC: {', '.join(CC_LIST)}")
    print(f"="*60)

except Exception as e:
    print(f"[FAILED] {e}")
    import traceback
    traceback.print_exc()
