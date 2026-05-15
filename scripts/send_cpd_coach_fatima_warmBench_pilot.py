#!/usr/bin/env python3
"""
Warm Bench Email - CPD Coach - Fatima Saeed
Pilot send using LOCKED TEMPLATE (2026-05-15)
GWC feedback only (no values interview data)
Recipients: Ayesha Khan + Jawwad Ali
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

sys.path.insert(0, 'c:/Agent Coco/scripts')
from utils.safe_send import safe_sendmail

load_dotenv()

SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")

subject = "When Personal Experience Becomes Professional Calling"

body_content = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 16px 0; line-height:1.75; text-align:justify;">
This isn't a yes for now.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
But we need to tell you something about what we saw in your interview that the panel kept discussing afterward, because it reveals something important about who you are as a person and as a coach.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
You described your own experience in the TFP fellowship - the difficulty, the uncertainty, the moment when someone believed in you enough to help you see what was possible. You spoke about that coach with such clarity and gratitude that the panel understood immediately where your motivation comes from. It isn't abstract. It isn't theoretical. You want to become for government teachers what someone became for you. That kind of personally grounded mission is rare. It's also powerful.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:32px 0 16px 0; line-height:1.75; text-align:justify;">
What Stayed With Us
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
The roleplay was your standout moment. We gave you a tired, defensive teacher - someone who has heard every improvement idea before, someone whose workload feels permanent. Most coaches jump to solutions. You didn't. You stopped first. You said something like, "I can see this is overwhelming." You acknowledged the burden before you raised the gaps. That's not technique. That's someone who actually sees the person inside the resistance.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
Then you offered low-effort, practical strategies instead of prescriptive instructions. You used self-reflection prompts. When we asked about rote learning in government schools, you brought in Bloom's Taxonomy, and it wasn't theoretical - it was grounded in real classroom context. That combination - empathy first, knowledge applied with compassion - is what good coaching looks like.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
What really caught the room was your closing questions. You didn't ask whether we offer training or whether teachers attend. You asked about coach training itself, about programme-level outcome metrics, about emerging challenges. That's not willingness. That's intellectual curiosity. You're entering this role with genuine hunger to understand what works and why - the kind of thinking that makes coaches better over time.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
There was also something the panel appreciated quietly: you raised your one-month notice period directly and framed it as a matter of professional integrity. You didn't hide it. You didn't apologize for it. You just named it honestly. In a field where people often hedge, that kind of directness is trustworthy.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:32px 0 16px 0; line-height:1.75; text-align:justify;">
Here's the Honest Part
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
Your interview stayed with us after the conversation ended. There was genuine discussion. Your personal motivation is the most grounded we've seen in this process. Your empathy in the roleplay was clear. Your knowledge is real and applied with compassion for context. Your intellectual curiosity about what makes coaching impact is exactly what this role needs. That doesn't change based on one hiring decision.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
But here's where we need to be honest with you. These decisions are sometimes incredibly narrow and situational. We have one role. We made a choice that reflected something very specific about what we thought this moment needed. It wasn't about you not being right for coaching. It was about us making a decision that, in the end, pointed somewhere else. That doesn't diminish what we saw. It just means the timing and the specific path didn't align this time.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:32px 0 16px 0; line-height:1.75; text-align:justify;">
Where We Want to Leave This
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
We'd genuinely like to stay connected. If an opportunity ever aligns with who you are and what you're looking for, we'd welcome talking again. You're exactly the kind of person who should be coaching teachers in government schools. And we meant that.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
Your interview reminded the panel what it looks like when someone's personal experience and professional calling are the same thing.
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:32px 0 8px 0; line-height:1.6; text-align:left;">
Warm regards,<br/>
<span style="font-weight:bold;">People and Culture Team</span><br/>
<span style="color:#1565C0; font-weight:bold;">Taleemabad</span>
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:8px 0; line-height:1.6; text-align:left;">
<a href="mailto:hiring@taleemabad.com" style="color:#1565C0; text-decoration:none;">hiring@taleemabad.com</a> | <a href="http://www.taleemabad.com" style="color:#1565C0; text-decoration:none;">www.taleemabad.com</a>
</p>

<p style="font-family:Georgia,serif; font-size:13px; color:#888; margin:12px 0 0 0; line-height:1.6; text-align:left;">
Sent on behalf of Talent Acquisition Team by Coco
</p>

<p style="font-family:Georgia,serif; font-size:13px; color:#666; margin:32px 0 0 0; padding:16px 0 0 0; border-top:1px solid #ddd; line-height:1.6; text-align:justify;">
<strong>P.S.</strong> That coach you described from your TFP fellowship, the one who believed in you enough to help you see what was possible - that's exactly who you're positioned to become for a government teacher. That's what your interview showed us. And that's what makes this particular timing so difficult.
</p>
"""

# Locked template (from c:\Agent Coco\templates\warm_bench_email.html)
html_body = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0; padding:0; background-color:#f3f4f6; font-family:Georgia,serif;">

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#f3f4f6;">
  <tr>
    <td align="center" style="padding:60px 0;">
      <table cellpadding="0" cellspacing="0" border="0" width="620" style="background-color:#ffffff; border-radius:8px; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

        <tr>
          <td align="center" style="padding:60px 70px 10px 70px;">
            <h1 style="font-family:Georgia,serif; font-size:32px; font-weight:bold; color:#1565C0; margin:0; line-height:1.2;">
              Fatima Saeed
            </h1>
          </td>
        </tr>

        <tr>
          <td align="center" style="padding:0 70px 32px 70px;">
            <p style="font-family:Georgia,serif; font-size:14px; color:#7986CB; margin:0; line-height:1.4;">
              CPD Coach
            </p>
          </td>
        </tr>

        <tr>
          <td style="padding:30px 70px 50px 70px;">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td style="height:2px; background-color:#1565C0;"></td>
              </tr>
            </table>
          </td>
        </tr>

        <tr>
          <td style="padding:0 70px 50px 70px;">
            """ + body_content + """
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>

</body>
</html>
"""

recipients = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]

try:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "[PILOT] " + subject
    msg["From"] = SENDER
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(html_body, "html"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)

    safe_sendmail(
        smtp_server=server,
        sender=SENDER,
        recipients=recipients,
        message=msg.as_string(),
        context="warm_bench_cpd_coach_fatima_pilot"
    )

    server.quit()

    print("PILOT SENT - Fatima Saeed")
    print("Recipients: " + ", ".join(recipients))
    print("Subject: [PILOT] " + subject)
    print("Content:")
    print("  - GWC feedback only (no values interview)")
    print("  - Roleplay standout moment (tired teacher, empathy first)")
    print("  - Intellectual curiosity, Bloom's Taxonomy, direct integrity")
    print("  - Personal TFP fellowship motivation")
    print("  - Word count: ~950 words")
    print("  - Justified text, no em dashes, poetic subject")

except Exception as e:
    print("Error sending pilot: " + str(e))
    sys.exit(1)
