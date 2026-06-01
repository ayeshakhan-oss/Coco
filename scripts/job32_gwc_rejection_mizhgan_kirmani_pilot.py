#!/usr/bin/env python3
"""
GWC Rejection Email - Mizhgan Kirmani (Job 32 - Fundraising & Partnerships)
Pilot to Ayesha + Jawwad for approval
PILOT_MODE = True
"""

import os
import sys
from pathlib import Path
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))
from utils.safe_send import safe_sendmail

# Email metadata
PILOT_MODE = True
TO = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
SUBJECT = "[PILOT – Mizhgan Kirmani] When Confidence Becomes the Blindfold"
CANDIDATE_NAME = "Mizhgan Kirmani"
CANDIDATE_EMAIL = "mizghan-kirmani@hotmail.com"  # Not used in pilot
JOB_TITLE = "Fundraising & Partnerships Manager"

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
            <div class="title">Fundraising & Partnerships Manager</div>
            <div class="subtitle">Taleemabad</div>
        </div>

        <!-- Greeting -->
        <p class="body-text">Hi Mizhgan,</p>

        <!-- Opening -->
        <p class="body-text">This is not a yes for now.</p>
        <p class="body-text">But we need to tell you something about what we saw in your interview that the panel kept discussing afterward.</p>

        <!-- Section 1 -->
        <div class="section-heading">What Stayed With Us</div>

        <p class="body-text">There's something specific about the way you move through difficulty that shows up in your career. Not just once, but consistently. And it matters.</p>

        <p class="body-text">At Tearfund UK, you worked with their team to build systems where none existed. And then you did it again at TCF Sahiwal. For thirty years, that organization had never had a donor relations focal person or a dedicated development function. You created both. You didn't wait for permission or infrastructure. You built it while working against institutional inertia, in a city where brand awareness was still low. The panel could feel that foundation in how you described it.</p>

        <p class="body-text">What also stayed with us was the moment with the TCF volunteer chapter head. She had been leading the chapter for over a year. She was showing signs of disengagement. Late, absent, deflecting blame. You called her one-on-one. You said directly that she seemed overwhelmed and should consider stepping back, naming the impact on the program's energy and on TCF's goals. She stepped down respectfully. A replacement was found. The program changed. Measurably. You held no guilt about that judgment because you knew it was right. That's not someone afraid of difficult conversations. That's someone who can see what's needed and say it.</p>

        <p class="body-text">And there's the foundation underneath all of this: you took what you learned in school debate competitions, what teachers criticized you for spending time on, and built it into your professional toolkit. Public speaking. Tone calibration. Jargon selection. Relationship-building at pitch meetings. Philosophy: learning is only real when it's implemented, tested with failure, refined through attempts. That's not someone coasting on past success. That's someone practicing your craft.</p>

        <!-- Section 2 -->
        <div class="section-heading">Here's the Honest Part</div>

        <p class="body-text">Here's what we also saw, and it shifted the conversation for the panel. The case study became important in the discussion because it was one of the few opportunities we had to see how you engage with a problem before a conversation begins. You hadn't arrived with a fully formed perspective. Instead, you worked through many of the questions in real time with us. Your communication skills carried the moment forward productively. What the panel left wanting was clearer evidence of how you think when given time to prepare, sit with a problem, form your own view, and test assumptions independently before entering the room.</p>

        <p class="body-text">During the interview, one theme that came through clearly was how much of your fundraising experience has been shaped by TCF's institutional strength. You spoke about an environment where donor trust already exists, where the organization carries deep credibility, and where part of the work is stewarding and structuring relationships around that existing trust. That's meaningful work, and it is not easy.</p>

        <p class="body-text">What the panel found itself wanting more evidence of was a slightly different muscle: donor creation rather than donor stewardship. We wanted to hear more about how you would identify cold or uncertain donor relationships, build credibility where it does not yet exist, and create momentum for an organization that is still earning its place in the donor's mind.</p>

        <p class="body-text">Taleemabad's fundraising reality right now is closer to that second challenge. We are building the function from zero in an organization that is still building brand awareness in the Pakistani education sector. This is not only about systematizing an existing donor pipeline. It is about creating one: finding the right people, opening doors, building trust, and shaping the story before institutional pull has fully formed.</p>

        <p class="body-text">So the question the interview left us with was not whether you understand fundraising. You clearly do. It was whether this particular kind of fundraising, the kind that begins before donor confidence has been established, is the challenge you were most ready to step into right now.</p>

        <!-- Section 3 -->
        <div class="section-heading">Where We Want to Leave This</div>

        <p class="body-text">You've genuinely built institutions in difficult contexts. Sahiwal matters. Your work at TCF matters. Those aren't small accomplishments. The panel recognized that. You can see what's needed in an organization and build it, even when it's never been done before, even when you're working against inertia.</p>

        <p class="body-text">The evidence suggests you do exceptional work when you're systematizing functions within organizations that have established reputations. Where the hard part is infrastructure and process. Where your confidence in your approach is grounded in the organization's existing market position. Roles where you're bringing order to a landscape that already has some institutional gravity.</p>

        <p class="body-text">Right now, Taleemabad's Fundraising function needs someone whose preparation and perspective on market entry align with what we actually face. Someone who understands building donor relationships from zero as the primary challenge, not a secondary one. Someone for whom the uncertainty of reputation-building in a new market is a central part of how they frame the role.</p>

        <p class="body-text">Your strengths are real. Your ability to build institutions in difficult environments is clear. But this particular role, at this particular moment, needs a different frame of reference. And that's honest information for both of us.</p>

        <p class="body-text">We'd genuinely like to stay connected. If you're open to it, we'd rather not let this be the final word.</p>

        <!-- P.S. -->
        <div class="ps-section">
            <div class="ps-heading">P.S.</div>
            <p class="body-text">The panel asked about a time you had to have a hard conversation. And you described the volunteer chapter head. The honesty and directness in that moment, and the fact that you felt no guilt because you knew your judgment was right: that's a character strength. That self-awareness about your own headstrong communication style, and your deliberate effort to tone it down when you sense others feel threatened: that's maturity. Those qualities will serve you well in whatever you build next.</p>
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
    """Send pilot email to Ayesha + Jawwad"""
    import smtplib
    from dotenv import load_dotenv

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
    msg['To'] = ", ".join(TO)

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

        safe_sendmail(
            smtp_server=server,
            sender=sender,
            recipients=TO,
            message=msg.as_string(),
            context=f"job32_gwc_rejection_mizhgan_kirmani_pilot"
        )

        server.quit()

        print("\n[PILOT EMAIL SENT]")
        print(f"   To: {', '.join(TO)}")
        print(f"   Subject: {SUBJECT}")
        print(f"   Mode: PILOT (candidate NOT included)")
        print(f"   Status: Awaiting approval from Ayesha")
        return True

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    send_pilot()
