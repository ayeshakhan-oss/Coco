#!/usr/bin/env python3
"""
Warm Bench Email - CPD Coach - Hajra Sajjad
Pilot send using LOCKED TEMPLATE (2026-05-04)
Incorporates both values + GWC scorecard feedback
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

subject = "The Principal's Expressions Changed When Data Spoke"

# Body content to be inserted into locked template
body_content = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 16px 0; line-height:1.75; text-align:justify;">
This isn't a yes for now.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
But we need to tell you something about what we saw in your interview that the panel kept discussing afterward, because it reveals something important about who you are as a person.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
You described standing in front of a principal who had said no to your Bridging Gaps community partnership project. He was skeptical. "No tangible outcomes," he'd told you. The room felt like it had sealed shut - institutional resistance can feel permanent. But you didn't walk away from that hard thing. Instead, you conducted a need assessment. You gathered surveys. You talked to parents, teachers, students. You turned what you were hearing into data. When you came back with numbers and stories in hand, something shifted in the room. You watched his expressions change as the evidence accumulated. And when students' grades improved and you'd created a student booklet, that skepticism finally became something closer to pride.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
What stayed with us wasn't just your persistence. It was watching you understand what that principal needed to hear - not to convince him to abandon his concerns, but to help him see what was possible on the other side of them. That kind of listening, that kind of thoughtfulness, left an impression on everyone in the conversation.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:32px 0 16px 0; line-height:1.75; text-align:justify;">
What Stayed With Us
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
There was a moment where you described the teachers coming to you overwhelmed. The lesson plan format simply wasn't working anymore. You didn't just identify the problem - you consulted the subject specialists first. You listened. You reached your supervisor with specific data about what was happening in the classroom. You proposed a thoughtful change. Your supervisor was hesitant at first. But you stayed with the conversation. The format worked. The target was achieved.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
The panel kept returning to that moment. Not because you solved a problem, but because of <em>how</em> you approached it. You listened before you proposed. You used evidence thoughtfully. You didn't push when it would have damaged the relationship. You let the work speak for itself.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
There was also the curriculum mapping workshop. You were assigned to deliver the technical training. But as you thought about it, you realized a peer team member was genuinely better equipped for that piece of work. So you stepped back. You didn't hold on tight to the role. In a field where expertise can feel protective, the willingness to say "someone else is stronger here" - that takes a kind of security and humility that doesn't come easily.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
When we asked you about your understanding of the CPD coach role, something became very clear. You didn't describe it as a delivery function. You described it as an ongoing trust-based mentoring process. You framed feedback as a continuous two-way loop grounded in classroom-specific data. And you connected everything - everything - back to student learning outcomes. It was precise. It was practiced. It was grounded in real field experience, not theory.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
Your scenario responses reinforced this. When we asked about a teacher resistant to training, you didn't jump to enforcement. You started with direct conversations. If that didn't work, structured reminders. And only then, leadership escalation - but with full awareness that you were asking someone else to step in. That's not just procedural thinking. That's someone who understands how to maintain trust while driving accountability. When we asked about safeguarding concerns, you moved quickly to clarity - address it directly in the debrief, one-on-one, and escalate to a safeguarding focal person for repeat incidents. No hesitation. Clear policy-awareness with compassion.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
But what really stayed with the room was your closing question. You asked how we measure CPD impact at programme level. Not whether we offer training. Not whether teachers attend. Whether the training translates into classroom practice and measurable student outcomes. You articulated a belief that felt mission-driven and specific: training only creates impact when it moves from the workshop into the classroom and into student learning. And you're already thinking at that level - programme level - before you've even started the role.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:32px 0 16px 0; line-height:1.75; text-align:justify;">
Here's the Honest Part
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
Your interview stayed with us after the conversation ended. There was a lot of discussion afterward. The way you think about people, the way you listen, the way you stay with difficult conversations - those things are clear. They're real. They matter. Your practical coaching mindset, your scenario handling, your mission-driven approach - none of that changes based on one hiring decision.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
But here's where we need to be honest with you. These decisions are sometimes incredibly narrow and situational. We have one role. We made a choice that reflected something very specific about what we thought this moment needed. It wasn't about you not being right for coaching. It was about us making a decision that, in the end, pointed somewhere else. That doesn't diminish what we saw in your interview. It just means the timing and the specific path didn't align this time.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:32px 0 16px 0; line-height:1.75; text-align:justify;">
Where We Want to Leave This
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:16px 0; line-height:1.75; text-align:justify;">
We'd genuinely like to stay connected. If an opportunity ever aligns with who you are and what you're looking for, we'd welcome talking again. You're exactly the kind of person we should be in conversation with. And we meant that.
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
<strong>P.S.</strong> The moment that stayed with everyone: a principal's skepticism transforming into pride when you came back with data and stories. Not to convince him he was wrong, but to help him see what was possible. That's what good coaching does. That's what you do.
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

        <!-- Candidate Name -->
        <tr>
          <td align="center" style="padding:60px 70px 10px 70px;">
            <h1 style="font-family:Georgia,serif; font-size:32px; font-weight:bold; color:#1565C0; margin:0; line-height:1.2;">
              Hajra Sajjad
            </h1>
          </td>
        </tr>

        <!-- Position -->
        <tr>
          <td align="center" style="padding:0 70px 32px 70px;">
            <p style="font-family:Georgia,serif; font-size:14px; color:#7986CB; margin:0; line-height:1.4;">
              CPD Coach
            </p>
          </td>
        </tr>

        <!-- Divider -->
        <tr>
          <td style="padding:30px 70px 50px 70px;">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td style="height:2px; background-color:#1565C0;"></td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Body Content -->
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
    # Build email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "[PILOT] " + subject
    msg["From"] = SENDER
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(html_body, "html"))

    # Connect and send
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)

    # Use safe_sendmail bouncer
    safe_sendmail(
        smtp_server=server,
        sender=SENDER,
        recipients=recipients,
        message=msg.as_string(),
        context="warm_bench_cpd_coach_hajra_expanded_gwc"
    )

    server.quit()

    print("PILOT SENT - Expanded with GWC feedback")
    print("Recipients: " + ", ".join(recipients))
    print("Subject: [PILOT] " + subject)
    print("Content:")
    print("  - Values interview moments (Bridging Gaps, lesson plans, curriculum mapping)")
    print("  - GWC insights (coaching mindset, scenario handling, mission-driven approach)")
    print("  - Word count: ~1150 words")
    print("  - Justified text, no em dashes, poetic subject")

except Exception as e:
    print("Error sending pilot: " + str(e))
    sys.exit(1)
