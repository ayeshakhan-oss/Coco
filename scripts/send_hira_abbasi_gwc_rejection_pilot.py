#!/usr/bin/env python3
"""
Send GWC Rejection Email — Hira Abbasi (CPD Coach)
====================================================
Pilot email for Ayesha Khan review before sending live to candidate.
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from scripts.utils.safe_send import safe_sendmail

# Load credentials
load_dotenv()
SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")

# Recipient
RECIPIENT = "ayesha.khan@taleemabad.com"

# Email subject and body
SUBJECT = "[PILOT – Hira Abbasi] The Moment You Understood What Teachers Actually Need"

HTML_BODY = """<html>
<head>
<style>
body { font-family: Georgia, serif; color: #333; line-height: 1.75; margin: 0; padding: 0; }
.container { max-width: 620px; margin: 0 auto; padding: 20px; background-color: #f3f4f6; }
.card { background-color: #ffffff; padding: 70px; border-radius: 4px; }
.header { text-align: center; margin-bottom: 30px; }
.header-title { color: #2f4fa2; font-size: 24px; font-weight: bold; margin: 0 0 10px 0; font-family: Georgia, serif; }
.divider { height: 3px; background-color: #2f4fa2; margin: 20px 0 30px 0; }
.section-heading { color: #2f4fa2; font-size: 16px; font-weight: bold; margin-top: 25px; margin-bottom: 12px; }
p { text-align: justify; margin: 12px 0; }
.closing { margin-top: 30px; }
.signature { margin-top: 20px; font-size: 13px; line-height: 1.6; color: #666; }
a { color: #2f4fa2; text-decoration: none; }
</style>
</head>
<body>
<div class="container">
<div class="card">

<div class="header">
<div class="header-title">Thank You for Your Conversation With Us</div>
</div>

<div class="divider"></div>

<p>Dear Hira,</p>

<p>Thank you for making time for our conversation and engaging so thoughtfully in our GWC interview. We want to be transparent about what we saw, what impressed us, and how we came to our decision not to move forward.</p>

<div class="section-heading">What Stayed With Us</div>

<p>Your pedagogical background is genuinely substantial. It came through not as theoretical knowledge, but as lived understanding—the kind that only comes from actually working with teachers and students over time. You've built real experience across curriculum design, understanding how students learn and where they get stuck, and translating that knowledge into practice.</p>

<p>When we asked you about the CPD Coach role, you didn't hesitate or need to think through what the position actually demands. You knew immediately. You could articulate what coaching a teacher looks like: listening for where the gap actually is (not where you assume it is), understanding their specific context and constraints, and then helping them build their own solution. That clarity mattered. It meant you weren't coming in needing to learn what the role is; you already understood.</p>

<p>During our discussion, you shared a specific example of working with a teacher who was struggling with a particular aspect of their practice. The way you described it—the listening, the diagnostic work, the way you adapted your approach based on what you were hearing—that revealed something important about how you think. You don't just deliver content. You meet teachers where they are.</p>

<p>That kind of pedagogical thoughtfulness, combined with the capacity to actually execute on it, is rare. Your understanding of what makes teachers grow, and your experience building that kind of growth in real situations, is exactly what this role is supposed to be.</p>

<div class="section-heading">Here's What Happened</div>

<p>That first part of our conversation felt strong. We went in with genuine interest in your candidacy, and the depth you brought reinforced why you'd looked promising on paper.</p>

<p>But something concrete shifted when we moved to discussing the role details. Specifically, when we explained that the contract ends in May and that any extension beyond that is genuinely uncertain, we noticed a visible change. You asked clarifying questions about what that meant for continuation. That's entirely reasonable. It's the question anyone would ask. But the visible energy and engagement that had been there earlier in the conversation dimmed noticeably after we acknowledged that uncertainty.</p>

<p>At the same time, you shared that you currently hold a permanent position elsewhere. That means a one-month notice period before you could begin with us, and it also means you have real commitments and stability in that role.</p>

<p>These details, taken together, painted a specific picture. Not a picture of someone who lacks the capabilities or understanding we're looking for. But a picture of someone whose conditions for full commitment weren't quite aligned with what this role requires.</p>

<div class="section-heading">Why This Matters for Our Decision</div>

<p>Here's what we've learned about the CPD Coach position: it requires someone who can walk in on day one and be completely focused on building relationships with teachers. The work is about presence—not just pedagogical knowledge, but actual human presence. A coach who is partially engaged, or navigating uncertainty about whether they'll still be here in six months—that undermines the foundation of what coaching actually is.</p>

<p>We've seen good examples of this role work when there's total alignment. The coach brings expertise, but more than that, they bring undivided commitment to the people they're coaching. Teachers can feel when someone is genuinely invested in their growth versus when someone is managing a role they're not fully in.</p>

<p>Your situation has real constraints that are entirely legitimate. You have another position. You have stability elsewhere. Those are good things. They just mean that right now, in this moment, this particular role—with its contract ending in May and its demand for complete focus—isn't the right fit for where you are.</p>

<div class="section-heading">Where We Want to Leave This</div>

<p>Your pedagogical capabilities are real and substantial. Your understanding of what teachers need is sharp. When you find yourself at a different point—where a role's timeline, its contract stability, and your other obligations all allow you to show up completely—that role will benefit from exactly what you bring.</p>

<p>We'd genuinely like to stay connected. Not in a "we'll call you if something changes" way, but in a real way. If the situation with this role evolves materially, or if you find yourself at a point where this kind of work becomes the right priority, we'd genuinely want to hear from you. We remember people who show up with this kind of thoughtfulness.</p>

<p>Thank you for being honest about your situation and constraints. That integrity matters.</p>

<div class="closing">
<p>Warm regards,<br>
People and Culture Team<br>
Taleemabad</p>

<div class="signature">
hiring@taleemabad.com | www.taleemabad.com<br>
<br>
</div>
</div>

</div>
</div>
</body>
</html>"""

# Create email
msg = MIMEMultipart("alternative")
msg["Subject"] = SUBJECT
msg["From"] = SENDER
msg["To"] = RECIPIENT
msg.attach(MIMEText(HTML_BODY, "html"))

# Send via SMTP
print(f"[send_hira_abbasi_gwc_rejection] Connecting to SMTP...")
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(SENDER, PASSWORD)

print(f"[send_hira_abbasi_gwc_rejection] Sending to {RECIPIENT}...")
safe_sendmail(server, SENDER, [RECIPIENT], msg.as_string(), context="hira_abbasi_gwc_rejection_pilot")

server.quit()
print(f"[send_hira_abbasi_gwc_rejection] SENT to {RECIPIENT}")
