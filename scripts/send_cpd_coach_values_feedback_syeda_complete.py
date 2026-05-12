#!/usr/bin/env python3
"""
Send values feedback email for Syeda Siddiqa Fatima - CPD Coach role (STYLED FORMAT)
PILOT MODE: sends to Ayesha + Jawad only
Tone: Warm, observational, genuine care
"""

import os
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.utils.safe_send import safe_sendmail

PILOT_MODE = True
SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")
PILOT_RECIPIENTS = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]

subject = "[PILOT — Syeda Siddiqa Fatima] We Saw Something Beautiful in You"

html_body = """<html>
<head>
<style>
body {
  font-family: Georgia, serif;
  font-size: 11px;
  line-height: 1.6;
  color: #333;
  text-align: justify;
}
h1 {
  color: #1565C0;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  margin: 20px 0;
}
h2 {
  color: #1565C0;
  font-size: 13px;
  font-weight: bold;
  margin: 20px 0 10px 0;
}
p {
  margin: 12px 0;
  line-height: 1.8;
}
.header {
  color: #1565C0;
  font-size: 10px;
  text-align: center;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 15px;
}
.ps-box {
  background-color: #f9f9f9;
  border-left: 3px solid #1565C0;
  padding: 15px;
  margin: 30px 0;
  font-style: italic;
}
</style>
</head>
<body>

<div class="header">PEOPLE &amp; CULTURE • FEEDBACK</div>

<h1>We Wanted to Share What We Saw</h1>
<p style="text-align: center; font-size: 12px; color: #1565C0; margin: 0 0 30px 0;">Your Values Interview for CPD Coach</p>

<hr style="border: none; border-top: 2px solid #1565C0; margin: 20px 0;">

<p>Dear Syeda,</p>

<p>Thank you for spending time with us in your values interview on April 28th. We want to share what we saw and felt during our conversation with you. This isn't a yes for this role, but we wanted to be thoughtful about why, because we believe there's real value in what we observed about you as a person and as someone who could grow into leadership roles.</p>

<h2>What Stood Out to Us</h2>

<p>When we asked about times you've shown up for your team, you didn't hesitate. You told us about stepping in to cover training schedules when your colleagues couldn't fill the gap. Not because anyone asked you to. Not because it was expected of you. But because you saw what needed to happen and you did it. That kind of intuitive care for the people around you is rare. You saw a gap, felt responsibility, and acted. We felt the genuineness in that story, and it revealed something important about how you think about your role within a team.</p>

<p>You also came into the CPD Coach position as someone completely willing to learn new skills from scratch. Training design, lesson planning for adult learners, manual building — these weren't areas of expertise for you. You could have let that uncertainty hold you back. Instead, you picked them up because the role required it, and you stayed curious and open while learning. We see someone who is willing to be a beginner, which takes a kind of humility and courage that actually matters a lot. There's no fear in your approach to growth — you just do what needs to be done.</p>

<p>You also recognized when colleagues in your teaching career had expertise you didn't — particularly in computer science — and you stepped back from those subjects to let them lead. That's not something everyone can do easily. It shows you understand that good teams aren't about one person knowing everything. They're about recognizing where others excel and creating space for that. That's wisdom.</p>

<h2>Where Our Conversation Left Us Thinking</h2>

<p>There were also a few moments where we felt there was more depth to your experiences than what came through in the conversation, and we would have loved to hear a little more about those moments.</p>

<p>When you talked about challenges you've faced, you mentioned the science lab construction project. We were hoping to better understand how certain experiences shaped you personally and professionally over time. Those are the kind of moments that often stay with us and change how we approach things. We wanted to understand not just what happened, but what it meant to you — what you learned about yourself or about how you work.</p>

<p>You mentioned receiving feedback during your time with Teach for Pakistan, which tells us you're open to input. That's valuable. We would have loved to hear more about how that feedback influenced your approach afterward. Sometimes the most important part of feedback isn't hearing it in the moment — it's what you actually do with it afterward. We wanted to understand how that shaped your work going forward.</p>

<p>And when we asked what brings you joy, you described yourself as someone who brings positivity to others. We believe that about you. The kind of presence and energy that comes from something genuinely meaningful to you is often what people connect with most. We would have loved to understand more about what that looks like for you — the moments that genuinely light you up, the things that feel real to you.</p>

<h2>What We Hope for You</h2>

<p>If I could say one thing, it would be this: Don't stop being the person who steps up for others. That instinct — to see a gap and fill it without being asked — is valuable, and it will take you far in whatever role comes next.</p>

<p>Keep learning new things that stretch you. Keep staying open to feedback. Keep growing. Those aren't small things. They're the foundation of any meaningful contribution.</p>

<p>As you move forward, we'd encourage you to spend time reflecting on the experiences that have shaped your perspective. Those moments — the hard ones, the surprising ones, the ones where you learned something about yourself — often help people communicate themselves with more clarity and confidence over time.</p>

<p>Keep noticing what genuinely brings you alive. The kind of presence and energy that comes from something real to you is something that makes teams better. It's how people know they can trust you.</p>

<p>You have the qualities to lead. You care deeply. You're willing to learn. You know how to be part of something bigger than yourself. And even though this role wasn't the right fit, we saw your potential clearly, and we believe in what you're becoming.</p>

<div class="ps-box">
<p><strong>P.S.</strong> We want you to know that we did see you in that interview. We saw someone who cares about the people around them, who is willing to learn and grow, and who brings a genuine warmth to their interactions. Those qualities matter, regardless of where your path takes you next. We believe in what we saw, and we believe in who you're becoming.</p>
</div>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:30px 0 0 0; line-height:1.6;">
Warm regards,<br/>
<span style="font-weight:bold;">People and Culture Team</span><br/>
<span style="color:#1565C0; font-weight:bold;">Taleemabad</span>
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:8px 0 0 0; line-height:1.6;">
<a href="mailto:hiring@taleemabad.com" style="color:#1565C0; text-decoration:none;">hiring@taleemabad.com</a> | <a href="http://www.taleemabad.com" style="color:#1565C0; text-decoration:none;">www.taleemabad.com</a>
</p>

<p style="font-family:Georgia,serif; font-size:13px; color:#888; margin:12px 0 0 0; line-height:1.6;">
Sent on behalf of Talent Acquisition Team by Coco
</p>

</body>
</html>"""

def send_pilot_email():
    """Send pilot email to Ayesha and Jawad only"""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = ", ".join(PILOT_RECIPIENTS)
    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER, PASSWORD)
        safe_sendmail(
            server,
            SENDER,
            PILOT_RECIPIENTS,
            msg.as_string(),
            context="CPD Coach values feedback pilot (STYLED)"
        )
        print("Styled pilot email sent successfully to Ayesha and Jawad")
        print(f"  Subject: {subject}")
        print(f"  Recipients: {', '.join(PILOT_RECIPIENTS)}")
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending pilot email: {e}")
        return False

if __name__ == "__main__":
    send_pilot_email()
