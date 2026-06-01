#!/usr/bin/env python3
"""
GWC Rejection Email - Muhammad Adnan (Job 32 - Fundraising & Partnerships)
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
SUBJECT = "[PILOT – Muhammad Adnan] When Maturity Meets a Different Kind of Hunger"
CANDIDATE_NAME = "Muhammad Adnan"
CANDIDATE_EMAIL = "muhammad.adnan@email.com"  # Not used in pilot
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
        <p class="body-text">Hi Muhammad,</p>

        <!-- Opening -->
        <p class="body-text">This is not a yes for now.</p>
        <p class="body-text">But we need to tell you something about what we saw in your interview that the panel kept discussing afterward.</p>

        <!-- Section 1 -->
        <div class="section-heading">What Stayed With Us</div>

        <p class="body-text">There's a particular kind of professional maturity that doesn't come from textbooks. It comes from having done hard things across multiple organizations and having the discipline to see them through. That's what showed up in your history.</p>

        <p class="body-text">When you mapped the entire exam delivery process at British Council, the third-largest exam delivery operation globally, you didn't just document what existed. You observed existing practice, costed resources down to staff hours and venue logistics, built an envisioned process with input from both management and ground-level staff, and then had the judgment to pilot on a smaller October/November session before scaling to the May/June rollout. You developed a shift model that reduced invigilator headcount and costs without compromising quality. That's not someone executing a plan. That's someone thinking about systems.</p>

        <p class="body-text">What also stayed with the panel was how you handled the difficult moment at Naya Tel. You had a team member whose behavior was disrupting colleagues, creating constant workload comparisons. You didn't manage them out. Instead, you initiated a formal performance improvement plan, monitored progress across six months to a year, collected feedback, and when the improvement wasn't sufficient, you advocated for their transfer to a better-fit role rather than simply removing the problem. You championed that person's future. That speaks to something foundational: how you see people.</p>

        <p class="body-text">And there's the moment at C4AD that says something about your relationship with difficulty. Donor compliance requirements tightened on a live project, demanding multiple report revisions far beyond the original scope. The team felt the work was outside the agreement and had stretched resources. And yet you delivered to the client's satisfaction. Not because you were forced to, but because "quitting is never an option." You didn't frame that as aspiration. You said it as something you practice.</p>

        <p class="body-text">The panel could feel that foundation.</p>

        <!-- Section 2 -->
        <div class="section-heading">Here's the Honest Part</div>

        <p class="body-text">You came into the interview as someone who has genuinely done this work across three organizations. You understand the role. You grasped the scope, the challenges, the responsibilities. You understood what we were asking of you. That clarity came through.</p>

        <p class="body-text">But here's what also came through, and this is where the conversation shifted for the panel. the panel's final-round conversation with you surfaced something fundamental about operating contexts. The environment you've worked in has required careful adoption of AI, strong QA processes, and thoughtful validation before deployment. That's been appropriate for the contexts you've operated in. The challenge is that this role currently operates under very different constraints and assumptions.</p>

        <p class="body-text">Taleemabad is an AI-native organization running at a sprint pace. The fundraising role you'd be stepping into isn't inheriting a built machine. It's building one from scratch under Sabeena, with a team of just three people. And the operating model requires something the panel named directly in your conversation: you would be "thrown into an AI flood" on day one. Not eventually. Not after onboarding. Day one. The systems, the processes, the speed of iteration: all of it runs on AI at a pace that assumes rapid experimentation and learning by doing. That would require operating differently than the sector-specific approach that has served you well elsewhere.</p>

        <p class="body-text">Your strength, and we saw this throughout all conversations, is your ability to bring order to complexity. You excel at building frameworks, establishing discipline, creating systems that last. Those are superpowers in the right environment. But in a fundraising function being built from zero in an organization running at breakneck pace on AI tools you'd be learning as you go, the thing the role needs most isn't order; it's comfort with controlled chaos. It's the ability to move fast, test, fail, iterate with AI as your teammate, and trust that the structure will emerge later rather than trying to architect it before you start.</p>

        <p class="body-text">This isn't about capability. You absolutely could learn the tools. But it's about what energizes you versus what drains you. Your career path shows you thrive when there's architecture to build, frameworks to optimize, rigor to install. You light up talking about process improvements and bringing order to chaos. The Fundraising role here right now needs someone who lights up doing the opposite: building in the chaos, treating uncertainty as the operating condition, letting the systems emerge from experimentation rather than preceding it.</p>

        <!-- Section 3 -->
        <div class="section-heading">Where We Want to Leave This</div>

        <p class="body-text">You carry something genuine in how you lead and move through difficulty. The way you think about systems, the way you see people even when they're struggling, your commitment to follow through, the calm you bring under pressure: those aren't things people build accidentally. You've built them through real work, across real organizations, with real stakes.</p>

        <p class="body-text">Your real value is evident in how you approach building institutions. When a function exists but needs to be systematized. When a team is in place but lacks processes. When relationships exist but need infrastructure around them. You come in after the chaos and build the architecture that lasts. That's what you've done at the World Bank, at Naya Tel, at British Council. You see disorder and you create order that doesn't break. The strongest evidence from your career suggests you do exceptional work when a function reaches the stage where it needs to be institutionalized, scaled, and made durable. Taleemabad's Fundraising team may well need that capacity later, as it matures. Right now, at this stage, it needs someone whose energy and instinct move in a different direction.</p>

        <p class="body-text">We'd genuinely like to stay connected. If you're open to it, we'd rather not let this be the final word.</p>

        <!-- P.S. -->
        <div class="ps-section">
            <div class="ps-heading">P.S.</div>
            <p class="body-text">the panel asked you a hard question: what's a real weakness, something you'd tell your wife and kids? And instead of the easy answer, you went deeper. You showed vulnerability. That honesty matters. That willingness to sit with discomfort and answer hard questions truthfully: that's a character strength that will serve you well in whatever you build next.</p>
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
            context=f"job32_gwc_rejection_muhammad_adnan_pilot"
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
