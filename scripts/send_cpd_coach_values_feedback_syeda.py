#!/usr/bin/env python3
"""
Send values feedback email for Syeda Siddiqa Fatima - CPD Coach role
PILOT MODE: sends to Ayesha + Jawad only
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

subject = "[PILOT — Syeda Siddiqa Fatima] When You Let Others Lead: A Reflection on Your Values Interview"

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

<div class="header">PEOPLE &amp; CULTURE • VALUES FEEDBACK</div>

<h1>Your Values Interview for CPD Coach</h1>
<p style="text-align: center; font-size: 12px; color: #1565C0; margin: 0 0 30px 0;">CPD Coach, Learning &amp; Development</p>

<hr style="border: none; border-top: 2px solid #1565C0; margin: 20px 0;">

<p>Dear Syeda,</p>

<p>This isn't a yes for now. But we need to tell you something about what we saw in your values interview on April 28th. You showed real aptitude for training and some genuine alignment with how we work here at Taleemabad. We want to be thoughtful about why this round didn't move forward, because the feedback is honest and we believe it matters for your growth.</p>

<h2>What We Liked Most About You</h2>

<p>First, the strengths we observed. When we asked about your experience stepping up for your team, you didn't hesitate. You talked about covering your colleagues' training schedules when no one else could fill the gap. That's "All for One and One for All" in practice. You saw a need, you recognized your team would suffer if you didn't act, and you stepped in. That matters. That's the kind of person who keeps things moving when circumstances get tight.</p>

<p>Second, you came to the CPD Coach role as a beginner in training design. You weren't pretending to know everything. You learned training frameworks, lesson planning for adult learners, manual crafting—all while doing the work. That demonstrates what we call "Continuously Improving Our Craft." You picked up a skill set you didn't have, stayed self-directed about it, and kept growing. You recognized when colleagues in your teaching career were better equipped at certain subjects—chemistry versus computer science—and you let them lead. You didn't hold on too tight to territory that wasn't yours. You saw expertise, respected it, and stepped back gracefully.</p>

<h2>Where We Found Ourselves Sitting With Questions</h2>

<p>And now, the part that mattered most in our decision. We asked you about a hard thing you'd persisted through. You mentioned science lab construction, but when we dug in, the response lacked specificity. What exactly made that hard? Did you almost quit? Did you want to quit? What did you actually do when the difficulty showed up? The story existed, but it stayed at the surface level. We were looking for the moment when you felt like walking away—and you stayed. We didn't find that moment. We found a transition from teaching to training, but no concrete evidence of pushing through something that felt genuinely hard.</p>

<p>You talked about receiving feedback during your Teach for Pakistan classroom observations. That's good—feedback is a gift. But here's what we needed to see: How did that feedback change you? Did you implement something different? Did your thinking shift? Did your behavior reflect the feedback in a visible way? You acknowledged the feedback, but we didn't see evidence of integration or behavioral change afterward. When someone has "Courageous Conversations" with you, what actually shifts as a result?</p>

<p>Finally, when we asked what brings you joy, you described yourself as a "smiley face emoji" bringing positivity to others. That sounds nice, but it felt like a tactic—something you've learned to say—rather than grounded in a real, embodied example. We were looking for "Practice Joy" through a story: a moment when something genuinely delighted you, when your joy was contagious, when being around you made things better because you couldn't help but find the good in a situation. Instead, we got a self-description. That was the gap.</p>

<p>Three values came back mixed. We call these plus-minus ratings. You exceeded our limit for mixed signals. We need more clarity and more depth in how you live our values, particularly around persisting through genuine hardship, embodying the impact of feedback, and practicing joy from a place of authenticity rather than performance.</p>

<h2>What We Think You Should Do Next</h2>

<p>Here's what we'd reflect on if we were in your position. First, get comfortable sitting with discomfort. Think back to something that genuinely tested you. Not a surface challenge, but something where you wanted to quit and stayed anyway. What made you stay? What did you learn about yourself? Build a few of those stories so you can speak from real experience, not idea. When someone asks you about hard things, you'll have lived evidence, not theory.</p>

<p>Second, when feedback comes your way—whether from a manager, a colleague, or an interview—track the follow-up. What specifically did you change? When did you first try that change? What happened as a result? Make the connection visible. The courage isn't just in hearing the feedback; it's in what you do with it afterward.</p>

<p>Third, find moments of genuine joy that are yours. Not a smile you put on for the team, but something that actually moves you. A win you celebrate privately. A connection that felt real. A moment when you let your guard down. Practice naming those moments, not performing joy, but actually living it. Your authenticity will resonate far more than any emoji description.</p>

<div class="ps-box">
<p><strong>P.S.</strong> You have trainer instincts. You care about your team. You're willing to learn. Those aren't small things. The feedback we've shared is meant to help you build on those strengths in whatever path you choose next. We've closed this door for now, but the characteristics we observed—your team orientation, your learner's mindset—those are valuable everywhere. Keep building on them.</p>
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
            context="CPD Coach values feedback pilot"
        )
        print("Pilot email sent successfully to Ayesha and Jawad")
        print(f"  Subject: {subject}")
        print(f"  Recipients: {', '.join(PILOT_RECIPIENTS)}")
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending pilot email: {e}")
        return False

if __name__ == "__main__":
    send_pilot_email()
