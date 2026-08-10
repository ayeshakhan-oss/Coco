#!/usr/bin/env python3
"""
Send GWC Rejection Email — Hira Abbasi (CPD Coach, Job 17)
===========================================================
Pilot to Ayesha for approval before sending live to candidate.
"""

import os
import sys
import smtplib
from pathlib import Path
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))
from utils.safe_send import safe_sendmail, allow_candidate_addresses

# Email metadata
TO = ["hiramehrban99@gmail.com"]
CC = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]
SUBJECT = "[PILOT – Hira Abbasi] The Gift of Knowing What You Need"
CANDIDATE_NAME = "Hira Abbasi"
JOB_TITLE = "CPD Coach"

# HTML Email Body with locked design
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

        <p class="body-text">Your pedagogical background is genuinely substantial. It came through not as theoretical knowledge, but as lived understanding. The kind that only comes from actually working with teachers and students over time. You've built real experience across curriculum design, understanding how students learn and where they get stuck, and translating that knowledge into practice.</p>

        <p class="body-text">When we asked you about the CPD Coach role, you didn't hesitate or need to think through what the position actually demands. You knew immediately. You could articulate what coaching a teacher looks like: listening for where the gap actually is, understanding their specific context and constraints, and then helping them build their own solution. That clarity mattered. It meant you weren't coming in needing to learn what the role is. You already understood.</p>

        <p class="body-text">During our discussion, you shared a specific example of working with a teacher who was struggling with a particular aspect of their practice. The way you described it—the listening, the diagnostic work, the way you adapted your approach based on what you were hearing—that revealed something important about how you think. You don't just deliver content. You meet teachers where they are.</p>

        <p class="body-text">That kind of pedagogical thoughtfulness, combined with the capacity to actually execute on it, is rare. Your understanding of what makes teachers grow, and your experience building that kind of growth in real situations, is exactly what this role is supposed to be.</p>

        <!-- Section 2: Here's the Honest Part -->
        <div class="section-heading">Here's the Honest Part</div>

        <p class="body-text">You came into the interview as someone who has genuinely done this work with teachers. You understand the role. You grasped the scope, the challenges, the responsibilities. That clarity came through.</p>

        <p class="body-text">But here's what also showed up in our conversation, and this is where things shifted for the panel. When we moved to discussing the role details, specifically the contract timeline, something genuine happened. The contract ends in May. Extension beyond that is genuinely uncertain. And you asked clarifying questions about what that means for continuation. That's entirely reasonable. That's what anyone would ask when told a role might end in four months with no guarantee of renewal.</p>

        <p class="body-text">At the same time, you shared that you currently hold a permanent position elsewhere. That means a one-month notice period before you could begin with us, and it also means you have real commitments and stability in that role right now. That's legitimate. That matters.</p>

        <p class="body-text">Here's where we want to be honest with you. The CPD Coach position requires someone who can walk in on day one and be completely focused on building relationships with teachers. Not partially focused. Not navigating uncertainty about whether they'll still be here in six months. Completely focused. The work is about presence. Not just pedagogical knowledge, but actual human presence in the lives of teachers you're coaching. That kind of presence is hard to give when you're managing uncertainty about contract renewal. It's hard to give when you're deciding whether to leave stability elsewhere.</p>

        <p class="body-text">This isn't us judging your response to the contract situation. Anyone would have concerns about a four-month contract with uncertain extension. That's not a flaw in your thinking. It's sensible. But it does mean that the conditions for your being fully present in this role aren't quite aligned right now.</p>

        <!-- Section 3: Where We Want to Leave This -->
        <div class="section-heading">Where We Want to Leave This</div>

        <p class="body-text">Your pedagogical capabilities are real and substantial. Your understanding of what teachers need is sharp. When you find yourself at a different point in your career, where a role's timeline and contract stability allow you to show up with complete commitment, that role will benefit from exactly what you bring. A coach with that depth of understanding, that kind of listening capacity, that genuine commitment to teacher growth.</p>

        <p class="body-text">We'd genuinely like to stay connected. Not in a "we'll call you if something changes" way. But in a real way. If the situation with this role evolves materially, or if you find yourself at a point where this kind of work becomes the right priority, we'd genuinely want to hear from you. We remember people who show up with this kind of thoughtfulness.</p>

        <p class="body-text">Thank you for being honest about your situation and constraints. That integrity matters.</p>

        <!-- P.S. -->
        <div class="ps-section">
            <div class="ps-heading">P.S.</div>
            <p class="body-text">The panel asked you a question about how you support a teacher who's stuck. And instead of the clinical answer, you went somewhere real. You talked about actually sitting with that teacher, understanding their frustration, and then helping them see possibility again. That kind of human attunement, that willingness to be present with difficulty rather than just solve it: that's a strength that will serve you well wherever you work next.</p>
        </div>

        <!-- Signature -->
        <div class="signature-block">
            <div class="signature">
                Warm regards,<br>
                People and Culture Team<br>
                Taleemabad<br><br>
                <a href="mailto:hiring@taleemabad.com" class="signature-link">hiring@taleemabad.com</a> | <a href="https://www.taleemabad.com" class="signature-link">www.taleemabad.com</a><br><br>
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
    msg['To'] = sender  # PILOT: send to Ayesha only for review
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
            context="hira_abbasi_gwc_rejection_pilot_v2"
        )

        server.quit()

        print("\n[PILOT EMAIL SENT]")
        print(f"   To: {sender} (Ayesha)")
        print(f"   CC: {', '.join(CC)}")
        print(f"   Subject: {SUBJECT}")
        print(f"   Logo: Embedded (cid:logo_taleemabad)")
        return True

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    send_pilot()
