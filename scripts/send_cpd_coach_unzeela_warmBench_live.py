#!/usr/bin/env python3
"""
Warm Bench Email - CPD Coach - Unzeela Khalid
LIVE send using LOCKED TEMPLATE
Recipients: Unzeela + CC to Ayesha Khan + Hasnat Tariq
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

sys.path.insert(0, 'c:/Agent Coco/scripts')
from utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv()

allow_candidate_addresses(["hajra2357@gmail.com", "unzilak21@gmail.com", "fatimasaeed030499@gmail.com"])

SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")

subject = "When Difficult Things Become Safer"

body_content = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 16px 0; line-height:1.75; text-align:justify;">
This isn't a yes for now.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
But we need to tell you something about what we saw in your interview that the panel kept discussing afterward, because it reveals something important about who you are as a person.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
You described witnessing a corporal punishment incident from your own organization's staff. A difficult position - community backlash, teacher resistance, institutional risk. Most people would have reported it and moved on. You didn't. You talked to parents. You listened to the child. You reported to authorities. You saw the teacher not as a villain but as someone who needed understanding. You stayed with it through the backlash. After six months, that teacher had changed. Students felt safer. What stayed with the panel wasn't just your willingness to report - it was watching you understand that the hard thing and the right thing are sometimes the same, and that staying matters.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
That courage ran through every moment of your interview.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:32px 0 16px 0; line-height:1.75; text-align:justify;">
What Stayed With Us
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
There was a moment where you described a team member going through depression, hesitant to speak, causing project miscommunication. You didn't just notice the missed deadlines. You listened. You discovered the person behind the silence. You brought her voice back to the team - not as a complaint, but as a human reality. The team's response shifted. People realized mistakes have reasons. People need support, not blame. You changed the culture of that room by advocating for the quieter voices.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
There was also your conversation with the CEO about menstrual leave policy. You approached leadership with genuine courage about a topic that touches on dignity and cultural discomfort. You didn't demand. You proposed. You were heard. New policies were implemented. Women in your organization now feel understood and included. That's not just a conversation - that's upward feedback with real institutional outcome.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
In the coaching scenario with the tired, defensive teacher, something became clear. You didn't jump to solutions. You acknowledged the workload burden first. You let her know you understood. Then you offered low-effort, practical strategies - not prescriptive instructions. When you discussed what you might teach her using Bloom's Taxonomy, it wasn't theoretical. It was grounded in your understanding of how government school students actually learn. You're someone who knows curriculum deeply and applies it with compassion for context.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
But what really stayed with the room was your intentional career trajectory. TFP fellowship in underserved communities. Then Khudi Institute, where you wanted to see alternative learning at institutional level. Now seeking to scale through teacher-facing work. Each move reflects skill-building, self-awareness, genuine intellectual curiosity about how people develop. Your closing questions - about coach training, programme metrics, emerging challenges - revealed you're entering this role not with willingness, but with genuine hunger to understand what works.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:32px 0 16px 0; line-height:1.75; text-align:justify;">
Here's the Honest Part
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
Your interview stayed with us after the conversation ended. There was real discussion afterward. The way you lead with empathy, the way you take interpersonal risks, the way you stay with difficult things - those are clear. They're real. They matter. You are exactly the kind of coaching presence this work needs. That doesn't change based on one hiring decision.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
But here's where we need to be honest with you. These decisions are sometimes incredibly narrow and situational. We have one role. We made a choice that reflected something very specific about what we thought this moment needed. It wasn't about you not being right for coaching. It was about us making a decision that, in the end, pointed somewhere else. That doesn't diminish what we saw. It just means the timing and the specific path didn't align this time.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:32px 0 16px 0; line-height:1.75; text-align:justify;">
Where We Want to Leave This
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
We'd genuinely like to stay connected. If an opportunity aligns with who you are and what you're looking for, we'd welcome talking again. You're exactly the kind of person this institution should be in conversation with. And we meant that.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
Your interview reminded the panel what thoughtful, courageous coaching looks like.
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
<strong>P.S.</strong> The moment that stayed with everyone: a corporal punishment incident you stayed with, through backlash, for six months, until the teacher changed and students felt safer. That's what good coaching does - it sees the person inside the mistake and stays long enough for change to happen. That's what you do.
</p>
"""

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
              Unzeela Khalid
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

candidate_email = "unzilak21@gmail.com"
recipients = [candidate_email, "ayesha.khan@taleemabad.com", "hasnat.tariq@niete.edu.pk"]

try:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = candidate_email
    msg["CC"] = "ayesha.khan@taleemabad.com, hasnat.tariq@niete.edu.pk"
    msg.attach(MIMEText(html_body, "html"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)

    safe_sendmail(
        smtp_server=server,
        sender=SENDER,
        recipients=recipients,
        message=msg.as_string(),
        context="warm_bench_cpd_coach_unzeela_live"
    )

    server.quit()

    print("LIVE SENT - Unzeela Khalid")
    print("To: " + candidate_email)
    print("CC: ayesha.khan@taleemabad.com, hasnat.tariq@niete.edu.pk")
    print("Subject: " + subject)

except Exception as e:
    print("Error sending live: " + str(e))
    sys.exit(1)
