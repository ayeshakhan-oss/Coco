#!/usr/bin/env python3
"""
LOCKED WARM BENCH FEEDBACK EMAIL SCRIPT (2026-05-04)
Status: PRODUCTION READY

Generic script for sending warm bench feedback emails to candidates who:
- Cleared values interview (Values PASS)
- Had strong GWC assessment (YES or CONDITIONAL)
- Were NOT selected for the current role
- May fit future roles

Usage:
    python warm_bench_locked.py --candidate "Dur E Nayab" --email "email@domain.com" --position "Junior Research Associate" --body-file path/to/body.html

Or programmatically:
    from scripts.warm_bench_locked import send_warm_bench_email
    send_warm_bench_email(
        candidate_name="Dur E Nayab",
        candidate_email="email@domain.com",
        position="Junior Research Associate",
        body_html="<p>Hi Dur E Nayab,...</p>",
        pilot_mode=True,
        pilot_recipients=["ayesha.khan@taleemabad.com"]
    )
"""

import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Load locked template
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '../templates/warm_bench_email.html')
with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    EMAIL_TEMPLATE = f.read()

def send_warm_bench_email(candidate_name, candidate_email, position, body_html, subject=None, pilot_mode=True, pilot_recipients=None, cc_list=None):
    """
    Send warm bench feedback email with locked design.

    Args:
        candidate_name: Full name of candidate
        candidate_email: Candidate's email address
        position: Job position title (e.g., "Junior Research Associate")
        body_html: HTML body content with paragraphs/sections
        subject: Optional custom subject line (defaults to "Your Application for {position}")
        pilot_mode: If True, send to pilot_recipients instead of candidate
        pilot_recipients: List of pilot review emails

    Returns:
        True if sent successfully, False otherwise
    """

    # Append signature to body content
    signature_html = """<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:30px 0 0 0; line-height:1.6;">
Warm regards,<br/>
<span style="font-weight:bold;">People and Culture Team</span><br/>
<span style="color:#1565C0; font-weight:bold;">Taleemabad</span>
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:8px 0 0 0; line-height:1.6;">
<a href="mailto:hiring@taleemabad.com" style="color:#1565C0; text-decoration:none;">hiring@taleemabad.com</a> | <a href="http://www.taleemabad.com" style="color:#1565C0; text-decoration:none;">www.taleemabad.com</a>
</p>
"""

    body_with_signature = body_html + signature_html

    # Format template with candidate name, position, and body
    html_body = EMAIL_TEMPLATE.format(
        candidate_name=candidate_name,
        position=position,
        body_content=body_with_signature
    )

    # Create email
    msg = MIMEMultipart('related')
    msg['From'] = EMAIL_USER
    msg['Subject'] = subject if subject else f"Your Application for {position}"

    # Determine recipients
    if pilot_mode and pilot_recipients:
        msg['To'] = ', '.join(pilot_recipients)
        recipients = pilot_recipients
        print(f"[PILOT] {candidate_name} -> {recipients}")
    else:
        msg['To'] = candidate_email
        # Use provided CC list or default
        if cc_list:
            cc_string = ', '.join(cc_list)
        else:
            cc_string = 'hiring@taleemabad.com, ayesha.khan@taleemabad.com'
        msg['Cc'] = cc_string
        recipients = [candidate_email] + (cc_list if cc_list else ['hiring@taleemabad.com', 'ayesha.khan@taleemabad.com'])
        print(f"[LIVE] {candidate_name} -> {candidate_email}")

    # Attach HTML
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(html_body, 'html', 'utf-8'))

    # Attach logo image with Content ID
    logo_path = os.path.join(os.path.dirname(__file__), '../assets/logo_taleemabad.png')
    try:
        with open(logo_path, 'rb') as f:
            logo_image = MIMEImage(f.read(), name='logo_taleemabad.png')
            logo_image.add_header('Content-ID', '<logo_taleemabad>')
            logo_image.add_header('Content-Disposition', 'inline', filename='logo_taleemabad.png')
            msg.attach(logo_image)
    except Exception as e:
        print(f"ERROR: Could not attach logo: {e}")
        return False

    # Send email
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"[OK] {candidate_name} email sent successfully")
        return True
    except Exception as e:
        print(f"[FAIL] {candidate_name} email FAILED: {e}")
        return False

# ====================
# CLI INTERFACE
# ====================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send warm bench feedback email (LOCKED)')
    parser.add_argument('--candidate', required=True, help='Candidate name')
    parser.add_argument('--email', required=True, help='Candidate email')
    parser.add_argument('--position', required=True, help='Job position title')
    parser.add_argument('--body-file', required=True, help='Path to HTML body content file')
    parser.add_argument('--pilot', action='store_true', help='Send as pilot (to reviewers)')
    parser.add_argument('--pilot-recipients', nargs='+',
                       default=['ayesha.khan@taleemabad.com', 'jawwad.ali@taleemabad.com'],
                       help='Pilot reviewer emails')

    args = parser.parse_args()

    # Read body HTML from file
    try:
        with open(args.body_file, 'r', encoding='utf-8') as f:
            body_html = f.read()
    except Exception as e:
        print(f"ERROR: Could not read body file: {e}")
        exit(1)

    # Send email
    success = send_warm_bench_email(
        candidate_name=args.candidate,
        candidate_email=args.email,
        position=args.position,
        body_html=body_html,
        pilot_mode=args.pilot,
        pilot_recipients=args.pilot_recipients
    )

    exit(0 if success else 1)
