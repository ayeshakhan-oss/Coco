#!/usr/bin/env python3
"""
Warm Bench Email Pilot — Huma Mumtaz
Position: Fundraising & Partnerships Manager
Values Interview: Pass (Apr 6, 2026 with Jawwad Ali)
GWC Interview: Pass (Apr 13, 2026)
Status: warm_bench
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

# Set path to root directory
script_dir = os.path.dirname(__file__)
root_dir = os.path.join(script_dir, "..")
sys.path.insert(0, root_dir)

from scripts.utils.safe_send import safe_sendmail

load_dotenv(dotenv_path=os.path.join(root_dir, ".env"))

# Configuration
CANDIDATE_NAME = "Huma Mumtaz"
CANDIDATE_EMAIL = "huma.mumtaz3@gmail.com"
POSITION = "Fundraising & Partnerships Manager"
VALUES_INTERVIEWER = "Jawwad Ali"
VALUES_DATE = "April 6, 2026"
GWC_DATE = "April 13, 2026"

PILOT_MODE = True
PILOT_TO = "ayesha.khan@taleemabad.com"

SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")

# Email content
SUBJECT = "[PILOT – Huma Mumtaz] When You Stop a Meeting to Protect Your Team"

BODY = f"""<html>
<head>
<style>
  body, p, div, span {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    line-height: 1.75;
    color: #333;
  }}
  .container {{
    background-color: #f5f5f5;
    padding: 40px 0;
    text-align: center;
  }}
  .wrapper {{
    background-color: #e5e7e2;
    padding: 0;
    display: inline-block;
    width: 100%;
    max-width: 775px;
  }}
  .card {{
    background-color: #ffffff;
    padding: 70px;
    text-align: left;
    width: 100%;
    box-sizing: border-box;
  }}
  .header {{
    text-align: center;
    margin-bottom: 40px;
  }}
  .header-title {{
    color: #2f4fa2;
    font-size: 28px;
    font-weight: bold;
    margin: 20px 0 10px 0;
    font-family: Georgia, Cambria, "Times New Roman", serif;
  }}
  .header-subtitle {{
    color: #5a6ea8;
    font-size: 16px;
    margin: 0;
    font-style: italic;
  }}
  .divider {{
    height: 2px;
    background-color: #4b6cb7;
    margin: 30px 0;
  }}
  .body-text {{
    font-size: 16px;
    line-height: 1.85;
    color: #333;
    text-align: justify;
    margin: 0 0 20px 0;
  }}
  .section-heading {{
    color: #2f4fa2;
    font-size: 18px;
    font-weight: bold;
    margin: 30px 0 15px 0;
    font-family: Georgia, Cambria, "Times New Roman", serif;
  }}
  .signature {{
    margin-top: 40px;
    padding-top: 15px;
    border-top: 1px solid #ccc;
    font-size: 14px;
    color: #666;
  }}
  .signature-name {{
    font-weight: bold;
    color: #333;
    margin: 5px 0 0 0;
    font-size: 14px;
  }}
  .signature-company {{
    font-weight: bold;
    color: #2f4fa2;
    margin: 0;
    font-size: 14px;
  }}
  .signature-coco {{
    font-size: 13px;
    color: #888;
    margin: 10px 0 0 0;
  }}
  .ps {{
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #e0e0e0;
    font-size: 15px;
    font-style: italic;
    color: #555;
  }}
</style>
</head>
<body>
<div class="container">
  <div class="wrapper">
    <div class="card">
      <div class="header">
        <img src="cid:logo_taleemabad" width="34" height="34" alt="Taleemabad" style="display:block; border-radius:17px;" />
        <div class="header-title">Huma, We're Thinking of You</div>
        <div class="header-subtitle">A warm bench opportunity from Taleemabad</div>
      </div>

      <div class="divider"></div>

      <p class="body-text">
Hi Huma,

This is not a yes for now.

But we need to tell you something about what we saw in your interview that the panel kept discussing afterward, because it reveals something important about who you are and how you approach your work.
      </p>

      <div class="section-heading">What Stayed With Us</div>

      <p class="body-text">
You described a moment in a management meeting where you stopped the conversation mid-flow. The room was discussing someone's performance without that person present. You said either invite them so they hear the feedback directly, or do not discuss it here. The team changed its approach because of what you said.

This wasn't theory for you. It was something you felt needed to be said, and you had the courage to interrupt a room of people to say it. That matters. We think a lot at Taleemabad about how we build organizations where people know they're treated fairly, where their voice matters, where they're not discussed in their absence. You clearly live that.

There was also the Abu Dhabi government RFP story—discovering 2–3 days before deadline that everything they'd been building was in the wrong format. You didn't escalate it and step back. You pulled in colleagues, stayed at the office until 11pm, completely rebuilt the proposal to spec. You described feeling guilty that the design team's work couldn't be used. But you delivered on time anyway. That combination—moving fast under pressure AND genuinely caring about the human cost—is rare.

And the financial modelling course. You identified a gap in your own skillset. No one required it. You took an Eastern European online program (Better Fund) with daily lectures and assignments. You're still working through it. You've told us you're not great at it yet. But you keep going. You don't look away from hard things.

The panel discussed all of this afterward. What showed up was someone who sees problems clearly, cares about people inside the resistance, and doesn't let discomfort be an excuse to stop.
      </p>

      <div class="section-heading">Here's the Honest Part</div>

      <p class="body-text">
Your interview created genuine discussion. There was real appreciation for how you show up—for your integrity, for the way you care about the people you work with, for your willingness to learn things that scare you. The panel also saw your self-awareness, your clarity about what you know and what you're still learning, and the way you carry responsibility. None of that is ambiguous. The panel saw it.

There was also an observation that your communication style—how energetic and proactive you come across in real time—resonated differently with different people in the room. Not a flaw. Just a note about how you present yourself in the moment.

But here's where we need to be honest with you. These decisions are sometimes incredibly narrow and situational. We have one role. We made a choice that reflected something very specific about what we thought this moment needed. It wasn't about you not being right for the position. It was about us making a decision that, in the end, pointed somewhere else. That doesn't diminish what we saw. It just means the timing and the specific path didn't align this time.
      </p>

      <div class="section-heading">Where We Want to Leave This</div>

      <p class="body-text">
We'd genuinely like to stay connected. If an opportunity ever aligns with who you are and what you're looking for, we'd welcome talking again. You're exactly the kind of person who should be leading on the partnerships and fundraising side at organizations that matter. And we meant that.

Your interview reminded the panel what it looks like when someone's personal integrity and professional judgment are the same thing.
      </p>

      <div class="ps">
<strong>P.S.</strong> — That moment in the management meeting—when you stopped the room and said either include this person or do not have this conversation—that's leadership. Not the formal kind. The kind that changes how a team actually behaves. That's what your interview showed us. And that's exactly why this timing is difficult.
      </div>

      <div class="signature">
Warm regards,<br />
<div class="signature-name">People and Culture Team</div>
<div class="signature-company">Taleemabad</div>
<br />
<a href="mailto:hiring@taleemabad.com" style="color:#2f4fa2; text-decoration:none;">hiring@taleemabad.com</a> | <a href="http://www.taleemabad.com" style="color:#2f4fa2; text-decoration:none;">www.taleemabad.com</a>
<br /><br />
<div class="signature-coco">Sent on behalf of Talent Acquisition Team by Coco</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""

# Send pilot
if __name__ == "__main__":
    # Build email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER

    if PILOT_MODE:
        recipients = [PILOT_TO]
        msg["To"] = PILOT_TO
    else:
        recipients = [CANDIDATE_EMAIL]
        msg["To"] = CANDIDATE_EMAIL
        msg["Cc"] = "hiring@taleemabad.com"

    msg.attach(MIMEText(BODY, "html"))

    # Attach logo image
    logo_path = os.path.join(root_dir, "assets", "logo_taleemabad.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as attachment:
            img_part = MIMEImage(attachment.read(), name=os.path.basename(logo_path))
            img_part.add_header("Content-ID", "<logo_taleemabad>")
            img_part.add_header("Content-Disposition", "inline", filename=os.path.basename(logo_path))
            msg.attach(img_part)

    # Send via safe_sendmail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)

    safe_sendmail(
        smtp_server=server,
        sender=SENDER,
        recipients=recipients,
        message=msg.as_string(),
        context="warm_bench_feedback_huma_mumtaz"
    )

    server.quit()

    if PILOT_MODE:
        print(f"\n[PILOT SENT] to {PILOT_TO}")
        print(f"Candidate: {CANDIDATE_NAME} ({CANDIDATE_EMAIL})")
        print(f"Position: {POSITION}")
        print(f"Subject: {SUBJECT}")
        print(f"\nAwait Ayesha's approval before sending live.")
    else:
        print(f"\n[LIVE SENT] to {CANDIDATE_EMAIL}")
        print(f"CC: hiring@taleemabad.com")
