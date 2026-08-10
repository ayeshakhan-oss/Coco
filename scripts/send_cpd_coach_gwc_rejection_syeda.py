#!/usr/bin/env python3
"""
Send GWC rejection email for Syeda Siddiqa Fatima - CPD Coach role
PILOT MODE: sends to Ayesha + Jawad only
Per SOP: 5 sections, 400-770 words, scorecard data only, warm mentoring tone
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

subject = "[PILOT — Syeda Siddiqa Fatima] Feedback on Your Case Study Interview"

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
</style>
</head>
<body>

<div class="header">PEOPLE &amp; CULTURE • REJECTION DECISION</div>

<h1>We're Reflecting on Your CPD Coach Application</h1>
<p style="text-align: center; font-size: 12px; color: #1565C0; margin: 0 0 30px 0;">Your Case Study Interview</p>

<hr style="border: none; border-top: 2px solid #1565C0; margin: 20px 0;">

<p>Dear Syeda,</p>

<p>Thank you for the time and thoughtfulness you brought to your case study interview with us. We know these conversations take real energy and vulnerability. We've completed our review, and we've decided not to move forward with your application. We wanted to be direct about that, and we also wanted to share what we observed.</p>

<h2>What We Saw</h2>

<p>Your background is genuinely strong. You have real credentials as an educator and trainer: TFP 2022, an MS in Bioinformatics, and current experience as a trainer. When we presented the scenario, you quickly identified the right strategic elements. You understood that reminders, principal escalation, and stakeholder coordination were the levers to pull. That structural thinking is important, and it showed us that you grasp the architecture of how a school operates.</p>

<p>You also brought warmth and flexibility to the conversation. The tone you set was open, thoughtful, and genuinely interested in understanding what the role demanded. That matters. We appreciated the directness with which you engaged.</p>

<h2>Where We're at</h2>

<p>What emerged through the interview was a mismatch between how you currently think about education and what the CPD Coach role actually requires. You have built your professional toolkit in the trainer model: designing content, running group workshops, delivering to cohorts. But this role demands a different posture entirely. It requires daily field presence, one-on-one observation of individual teachers, and facilitation through questioning rather than delivery. The moves are quite different.</p>

<p>When we asked about foundational knowledge, some details felt uncertain. We also noticed that when we asked you to bring texture to the scenario, you could identify what needed to happen, but you couldn't walk us through a specific moment where you had done something similar with a teacher. The operational depth wasn't there. For a role that depends on coaching credibility, that depth matters.</p>

<h2>What Matters Next</h2>

<p>As you move forward, we'd encourage you to reflect on what actually energizes you in education work. Is it the design and facilitation of group learning? Or is it the one-on-one moment when a teacher has a breakthrough? Understanding that for yourself will help you find a role where your strengths are what the job actually needs.</p>

<p>We'd also suggest building real depth in a domain you care about. Get to know one area well enough that people trust you completely. That kind of depth transforms feedback from "I've heard about this" to "I know this," and it makes a real difference in how people respond to you.</p>

<h2>Closing Thoughts</h2>

<p>We saw someone thoughtful and committed to education in that room. Those qualities matter, and they will serve you well. This particular role just needed something different. We genuinely wish you well in what comes next, and we believe you'll find the right fit.</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:30px 0 0 0; line-height:1.6;">
Warm regards,<br/>
<span style="font-weight:bold;">People and Culture Team</span><br/>
<span style="color:#1565C0; font-weight:bold;">Taleemabad</span>
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:8px 0 0 0; line-height:1.6;">
<a href="mailto:hiring@taleemabad.com" style="color:#1565C0; text-decoration:none;">hiring@taleemabad.com</a> | <a href="http://www.taleemabad.com" style="color:#1565C0; text-decoration:none;">www.taleemabad.com</a>
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
            context="CPD Coach GWC rejection pilot"
        )
        print("GWC rejection pilot email sent successfully to Ayesha and Jawad")
        print(f"  Subject: {subject}")
        print(f"  Recipients: {', '.join(PILOT_RECIPIENTS)}")
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending pilot email: {e}")
        return False

if __name__ == "__main__":
    send_pilot_email()
