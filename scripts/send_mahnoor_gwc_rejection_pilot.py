#!/usr/bin/env python3
"""
GWC Rejection Email — Mahnoor Qureshi (CPD Coach, Job 17)
Application ID: 362
Candidate ID: 314
Status: Pilot to Ayesha Khan for approval

Draft: Locked approach, warm bench structure, 1,032 words
Haroon Yasin balance: 4 praise specifics = 3 decision specifics
No intent inference, no abstractions, no jargon
"""

from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib
import os
from dotenv import load_dotenv
import sys
sys.path.insert(0, str(Path(__file__).parent))

from utils.safe_send import safe_sendmail

load_dotenv()

CANDIDATE_NAME = "Mahnoor Qureshi"
POSITION = "CPD Coach"
SUBJECT = "[PILOT – Mahnoor Qureshi] When Resilience Meets the Work That's Waiting"
PILOT_EMAIL = "ayesha.khan@taleemabad.com"

BODY_CONTENT = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">Dear Mahnoor,</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">This is not a yes for now.</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">But we need to tell you something about what we saw in your interview that the panel kept discussing afterward.</p>

<p style="font-family:Georgia,serif; font-size:18px; color:#1565C0; font-weight:bold; margin:30px 0 15px 0; padding-top:20px;">What Stayed With Us</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">Your background in research and policy analysis is genuinely substantial. You've spent years translating complex data into actionable insights, working across gender equality, governance, and social policy—disciplines that require both intellectual rigor and a capacity to hold nuance. That kind of work builds clarity.</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">What came through most distinctly in your interview was your communication. You articulated your thinking with precision. You listened carefully to our questions and responded thoughtfully, not defensively. When we pressed you on how you'd approach different scenarios in a coaching context, you didn't rush to conclusions. You asked clarifying questions first. That's a disciplined approach to complexity, and it showed up consistently.</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">And underneath it all was something the panel noted with genuine appreciation: resilience. Your CV tells a story of someone who moves through different environments, learns quickly, adapts approach, and keeps going. You've worked as an intern learning research methodology at SSDO. You've contributed to archival work at AIMH. You've executed mixed-method frameworks at D-Mark. There's a pattern here of someone who shows up, figures things out, and doesn't let discomfort become an excuse to disengage. That matters.</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">You're also genuinely motivated about the education sector. That wasn't performance in the room. You've thought about why this work matters to you. You've articulated what transformation in education looks like to you. Motivation of that kind—rooted in something concrete rather than abstract aspiration—is rare.</p>

<p style="font-family:Georgia,serif; font-size:18px; color:#1565C0; font-weight:bold; margin:30px 0 15px 0; padding-top:20px;">Here's the Honest Part</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">This decision wasn't driven by concerns about your ability to learn or your capacity to commit. You've proven both of those.</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">The position we're filling requires someone who arrives with pedagogical knowledge already embedded. The CPD Coach works directly with teachers to improve their classroom practice. Teachers look to a coach to name what they're seeing in their own teaching—the gaps in sequencing, the moments students check out, the patterns in how they respond to struggle. A coach needs to see those things quickly and articulate them in language teachers recognize. That's pedagogy-in-action. It's not something we can ask someone to build from first principles while they're also building relationships with teachers.</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">In our conversation, when we asked about teaching and learning, what became clear was that this framework isn't yet where you're standing. Your research background means you think in terms of systems and data. A teacher thinks in terms of a specific student in a specific moment. Both perspectives are valuable, but they're not the same. It's not a matter of commitment or intelligence. It's a matter of what you've spent years developing expertise in, and what we need someone to already know.</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">There was a second pattern that mattered to the panel. When we explored problem-solving scenarios—situations where a teacher is stuck or resistant—there was a sense that you were thinking your way through rather than drawing from experience. You'd consider the options, but you weren't anchoring in "I've seen this before" or "Here's how I'd navigate this because I know what works." That kind of pattern recognition—problem-solving born from lived experience in the classroom—is something the role genuinely requires.</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">These aren't character judgments. They're honest realities about where you are in your professional journey and what we need someone to have already built. You could absolutely develop this over time with the right mentorship. But we're starting a role right now, and the teachers we work with need someone who's already made that journey.</p>

<p style="font-family:Georgia,serif; font-size:18px; color:#1565C0; font-weight:bold; margin:30px 0 15px 0; padding-top:20px;">Where We Want to Leave This</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">We want you to keep moving toward the education sector if that's genuinely where your energy is. Your background in research and systems thinking could be invaluable in other roles—curriculum development, teacher training program design, institutional research, policy work at the district or organizational level. Those paths exist, and your skillset would serve them well.</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">And if your path does lead back to classroom-facing work—if you decide to spend time as a teacher first, building that lived experience—we'd genuinely like to talk again. That's not a polite deflection. It's because what you brought to this conversation matters. The clarity, the listening, the resilience, the genuine investment in the work—those are exactly the qualities that make someone a good coach eventually. They just need the foundation underneath them.</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">We're keeping this door open. Stay in touch.</p>
"""

PS_CONTENT = "When you described your work on the gender-responsive governance frameworks at SSDO, the way you talked about it—how you'd seen communities shift when they understood why women's voices mattered—there was something genuine there. That's the person we saw. We hope the next opportunity you pursue gets to work with that version of you."

# Load template
TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "warm_bench_email.html"
with open(TEMPLATE_PATH, 'r') as f:
    template = f.read()

# Fill template
html_body = template.format(
    candidate_name=CANDIDATE_NAME,
    position=POSITION,
    body_content=BODY_CONTENT,
    ps_content=PS_CONTENT
)

# Create message
msg = MIMEMultipart('related')
msg['Subject'] = SUBJECT
msg['From'] = 'hiring@taleemabad.com'
msg['To'] = PILOT_EMAIL
msg['Cc'] = 'zeshan.dhillon@taleemabad.com'

# Attach HTML body
msg_alternative = MIMEMultipart('alternative')
msg.attach(msg_alternative)
msg_alternative.attach(MIMEText(html_body, 'html'))

# Attach logo
logo_path = Path(__file__).parent.parent / "assets" / "logo_taleemabad.png"
if logo_path.exists():
    with open(logo_path, 'rb') as attachment:
        img = MIMEImage(attachment.read(), name="logo_taleemabad.png")
        img.add_header('Content-ID', '<logo_taleemabad>')
        img.add_header('Content-Disposition', 'inline', filename="logo_taleemabad.png")
        msg.attach(img)

# Send via safe_sendmail
SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")

print(f"Sending pilot to {PILOT_EMAIL}...")
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(SENDER, PASSWORD)

try:
    safe_sendmail(
        smtp_server=server,
        sender=SENDER,
        recipients=[PILOT_EMAIL],
        message=msg.as_string(),
        context="GWC Rejection — Mahnoor Qureshi (CPD Coach, Job 17, App ID 362)"
    )
    print("[SUCCESS] Pilot sent to {}".format(PILOT_EMAIL))
except Exception as e:
    print("[ERROR] {}".format(e))
    sys.exit(1)
finally:
    server.quit()
