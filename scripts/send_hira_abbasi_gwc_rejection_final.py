#!/usr/bin/env python3
"""
GWC Rejection Email - Hira Abbasi (CPD Coach, Job 17)
=====================================================
Locked SOP approach: warm bench structure + evidence-based methodology
"""

import os
import sys
import smtplib
from pathlib import Path
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
from utils.safe_send import safe_sendmail, allow_candidate_addresses

# Email metadata
TO = ["hiramehrban99@gmail.com"]
CC = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]
SUBJECT = "[PILOT – Hira Abbasi] What We Saw When You Listened"
CANDIDATE_NAME = "Hira Abbasi"
JOB_TITLE = "CPD Coach"

# HTML Email Body - Locked Taleemabad template
HTML_BODY = """
<html>
<head>
    <style>
        body {
            font-family: Georgia, serif;
            line-height: 1.75;
            color: #333;
            background-color: #f9f9f9;
        }
        .container {
            max-width: 620px;
            margin: 0 auto;
            padding: 70px;
            background-color: #ffffff;
            border-radius: 0;
        }
        .logo {
            text-align: center;
            margin-bottom: 20px;
        }
        .header-block {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid #2f4fa2;
        }
        .title {
            font-size: 18px;
            color: #2f4fa2;
            font-weight: bold;
            margin: 20px 0 10px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .subtitle {
            font-size: 14px;
            color: #666;
            font-style: italic;
            margin: 0;
        }
        .section-heading {
            font-size: 16px;
            color: #2f4fa2;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-top: 20px;
        }
        .body-text {
            text-align: justify;
            font-size: 14px;
            line-height: 1.75;
            color: #333;
            margin: 0 0 15px 0;
        }
        .ps-section {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }
        .ps-heading {
            font-weight: bold;
            color: #2f4fa2;
            margin-bottom: 10px;
        }
        .signature-block {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }
        .signature {
            font-size: 13px;
            line-height: 1.6;
            color: #666;
        }
        .signature-link {
            color: #2f4fa2;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Logo -->
        <div class="logo">
            <img src="cid:logo_taleemabad" width="48" height="48" alt="Taleemabad" style="display:block; margin:0 auto 20px auto; border-radius:0;" />
        </div>

        <!-- Header -->
        <div class="header-block">
            <div class="title">CPD Coach</div>
            <div class="subtitle">Taleemabad</div>
        </div>

        <!-- Greeting -->
        <p class="body-text">Dear Hira,</p>

        <!-- Opening -->
        <p class="body-text">This is not a yes for now.</p>
        <p class="body-text">But we need to tell you something about what we saw in your interview that the panel kept discussing afterward.</p>

        <!-- Section 1: What Stayed With Us -->
        <div class="section-heading">What Stayed With Us</div>

        <p class="body-text">Your pedagogical background is genuinely substantial. It came through not as theoretical knowledge, but as lived understanding. You've built real experience across curriculum design, understanding how students learn, and translating that knowledge into practice with teachers.</p>

        <p class="body-text">When we asked about the CPD Coach role, you didn't hesitate. You could articulate immediately what coaching a teacher looks like: listening for where the gap actually is, understanding their specific context, and then helping them build their own solution. You don't just deliver content. You meet teachers where they are. That clarity mattered to the panel.</p>

        <p class="body-text">During our discussion, you shared a specific example of working with a teacher who was struggling. The way you described it—the listening, the diagnostic work, the way you adapted your approach based on what you were hearing—revealed something important about how you think. That kind of pedagogical thoughtfulness combined with your capacity to execute on it is rare. It's exactly what this role is supposed to be.</p>

        <!-- Section 2: Here's the Honest Part -->
        <div class="section-heading">Here's the Honest Part</div>

        <p class="body-text">To be clear, this decision wasn't driven by concerns about your ability to do the work. If anything, it came from the opposite conclusion. We saw strong evidence that you could.</p>

        <p class="body-text">What the panel reflected on afterward was this: As we discussed the role details, specifically the contract timeline and what it means for continuity, something genuine happened. The position comes with real uncertainty around its extension beyond May. And you currently hold a permanent role that offers stability and continuity. Neither reality is inherently better than the other. But they create a tension that felt difficult to ignore.</p>

        <p class="body-text">Coaching works best when someone can step into the role with confidence about the choice they've made and the environment they're entering. As we looked at the alignment between your situation and what the role requires, we weren't fully convinced those conditions were in place right now. The contract uncertainty and the stability you currently have create a dynamic where your full commitment to this work would be genuinely difficult.</p>

        <p class="body-text">This isn't about you not being ready. It's about a specific mismatch in circumstances.</p>

        <!-- Section 3: Where We Want to Leave This -->
        <div class="section-heading">Where We Want to Leave This</div>

        <p class="body-text">Your capabilities are real. Your understanding of what teachers need is sharp. When you find yourself at a point where a role's stability, its timeline, and your other obligations all allow you to walk in with total confidence, that role will benefit from exactly what you bring.</p>

        <p class="body-text">The kind of person who listens before they teach, who stays curious about what's actually blocking someone, who has the courage to sit with difficulty rather than rush past it. Those aren't things people develop accidentally. You've built them through real work with real people.</p>

        <p class="body-text">We'd genuinely like to stay connected. If the situation with this role evolves materially, or if you find yourself at a different point, we'd genuinely want to hear from you. We remember people who show up with this kind of thoughtfulness.</p>

        <!-- P.S. -->
        <div class="ps-section">
            <div class="ps-heading">P.S.</div>
            <p class="body-text">The panel asked you a hard question about how you support a teacher who's stuck. And instead of the clinical answer, you went somewhere real. You talked about actually sitting with that teacher, understanding their frustration, and then helping them see possibility again. That kind of human attunement, that willingness to be present with difficulty rather than solve it, that's a strength that will serve you well wherever you work next.</p>
        </div>

        <!-- Signature -->
        <div class="signature-block">
            <div class="signature">
                Warm regards,<br>
                People and Culture Team<br>
                Taleemabad<br><br>
                <a href="mailto:hiring@taleemabad.com" class="signature-link">hiring@taleemabad.com</a> | <a href="https://www.taleemabad.com" class="signature-link">www.taleemabad.com</a><br><br>
                Sent on behalf of Talent Acquisition Team by Coco
            </div>
        </div>
    </div>
</body>
</html>
"""

def send_pilot():
    """Send pilot email to Ayesha"""
    load_dotenv()

    # Load logo
    logo_path = Path(__file__).parent.parent / "assets" / "logo_taleemabad.png"
    if not logo_path.exists():
        print(f"ERROR: Logo not found at {logo_path}")
        return False

    # Get credentials
    sender = "ayesha.khan@taleemabad.com"
    password = os.getenv("EMAIL_PASSWORD")
    if not password:
        print("ERROR: EMAIL_PASSWORD not found in .env")
        return False

    # Prepare email message
    msg = MIMEMultipart('related')
    msg['Subject'] = SUBJECT
    msg['From'] = sender
    msg['To'] = sender  # PILOT: send to Ayesha only
    msg['Cc'] = ", ".join(CC)

    # Attach HTML body
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(HTML_BODY, 'html'))

    # Attach logo as embedded image
    try:
        with open(logo_path, 'rb') as f:
            img = MIMEImage(f.read(), name='logo_taleemabad.png')
            img.add_header('Content-ID', '<logo_taleemabad>')
            img.add_header('Content-Disposition', 'inline', filename='logo_taleemabad.png')
            msg.attach(img)
    except Exception as e:
        print(f"ERROR: Failed to attach logo: {str(e)}")
        return False

    # Send via safe_sendmail
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)

        all_recipients = [sender] + CC
        safe_sendmail(
            smtp_server=server,
            sender=sender,
            recipients=all_recipients,
            message=msg.as_string(),
            context="hira_abbasi_gwc_rejection_final"
        )

        server.quit()

        print("\n[PILOT EMAIL SENT]")
        print(f"   To: {sender} (Ayesha)")
        print(f"   CC: {', '.join(CC)}")
        print(f"   Subject: {SUBJECT}")
        print(f"   Format: Locked Taleemabad template")
        print(f"   Approach: Warm bench SOP + evidence-based methodology")
        return True

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    send_pilot()
