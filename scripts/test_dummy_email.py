"""
Dummy email test — sends a simple test message to verify email integration works.
Uses safe_sendmail bouncer with pilot mode (Ayesha only, not live).
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Configuration
SENDER = os.getenv("EMAIL_USER", "ayesha.khan@taleemabad.com")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT = "ayesha.khan@taleemabad.com"  # Pilot to Ayesha only

# Create simple HTML email
html_body = """
<html>
<head>
    <style>
        body { font-family: Georgia, serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #f3f4f6; padding: 20px; border-left: 4px solid #2f4fa2; }
        .content { padding: 20px 0; }
        .footer { color: #666; font-size: 12px; border-top: 1px solid #ddd; padding-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2 style="color: #2f4fa2; margin: 0;">Test Email — Integration Check</h2>
            <p style="color: #666; margin: 5px 0 0 0;">Sent at 2026-05-08</p>
        </div>

        <div class="content">
            <p>Hello Ayesha,</p>
            <p>This is a test email to verify that the email integration system is working correctly.</p>
            <p><strong>Email System Status:</strong></p>
            <ul>
                <li>safe_sendmail bouncer: ✓ Active</li>
                <li>Pilot mode: ✓ Enabled (Ayesha only)</li>
                <li>HTML design: ✓ Template loaded</li>
                <li>Integration test: ✓ In progress</li>
            </ul>
            <p>If you receive this email, all systems are operational.</p>
        </div>

        <div class="footer">
            <p>This is a test email sent by Coco's integration test suite.</p>
        </div>
    </div>
</body>
</html>
"""

# Create email message
msg = MIMEMultipart("alternative")
msg["Subject"] = "Test Email — Coco Integration Check (Pilot)"
msg["From"] = SENDER
msg["To"] = RECIPIENT
msg.attach(MIMEText(html_body, "html"))

# Send via safe_sendmail
print("=" * 60)
print("SENDING TEST EMAIL")
print("=" * 60)
print(f"From: {SENDER}")
print(f"To: {RECIPIENT}")
print(f"Subject: {msg['Subject']}")
print(f"Mode: PILOT (Ayesha only, not live)")
print("=" * 60)

try:
    # Verify recipient is on allowlist
    allow_candidate_addresses([RECIPIENT])

    # Connect to Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)

        # Send via safe_sendmail bouncer
        safe_sendmail(
            smtp_server=server,
            sender=SENDER,
            recipients=[RECIPIENT],
            message=msg.as_string(),
            context="test_dummy_email"
        )

    print("\n[SUCCESS] Email sent successfully!")
    print("Check ayesha.khan@taleemabad.com inbox for test message.")

except Exception as e:
    print(f"\n[ERROR] Failed to send email: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)
