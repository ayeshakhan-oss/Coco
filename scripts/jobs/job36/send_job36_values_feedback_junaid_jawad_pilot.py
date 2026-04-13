"""
Job 36 - Field Coordinator, Research & Impact Studies
Values Interview Feedback Emails - Muhammad Junaid & Jawad Khan - PILOT

PILOT MODE: sends to Ayesha + Jawwad only.
Design: v8 (white header, blue text, CID logo, purple button, Georgia serif)
Includes feedback widget for candidate responses.
"""

import os, smtplib, base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
from scripts.utils.check_token_expiry import check_all_tokens

check_all_tokens(print_output=True)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

SENDER   = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
PILOT_TO  = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
ROLE     = "Field Coordinator, Research &amp; Impact Studies"

LOGO_PATH = os.path.join(os.path.dirname(__file__), "../../..", "assets", "logo_taleemabad.png")

with open(LOGO_PATH, "rb") as f:
    LOGO_BYTES = f.read()

CANDIDATES = [
    {
        "name": "Muhammad Junaid",
        "email": "junaidjadee912@gmail.com",
        "story_title": "The Commitment You Made, and Where It Led",
        "narrative": """
        In our conversation, we got to hear about your commitment to your work and the communities you serve.
        You shared thoughtfully about your experience and your drive to make an impact. We appreciated your openness
        and your willingness to reflect on your journey.
        <br><br>
        As we move forward in this hiring process, we wanted to share some observations from our values conversation.
        While your experience and commitment came through clearly, we noticed that some of the values we look for at
        Taleemabad — particularly around collaboration, continuous improvement in how we work together, and holding
        space for different perspectives — weren't as evident in our conversation. These are core to how we operate as
        a team and in the communities we serve.
        """
    },
    {
        "name": "Jawad Khan",
        "email": "jawadmarwat47@gmail.com",
        "story_title": "The Work You Do, and How You Do It",
        "narrative": """
        In our conversation, we heard about your experience in the field and your dedication to the work.
        You shared insights from your background and your perspective on impact. We genuinely appreciated
        your engagement and your willingness to discuss your approach to this role.
        <br><br>
        As we continue our hiring process, we wanted to be transparent about where we stand. While your technical
        experience is solid, we noticed that some of the core values we build on at Taleemabad — particularly around
        practicing joy, staying curious and learning continuously, and having honest conversations even when they're hard —
        weren't as visible in how you reflected on your work. These values shape everything we do, and we need to see
        them clearly in those who join our team.
        """
    }
]

def header_block(subject_line):
    return f"""
<table width="100%" cellpadding="0" cellspacing="0"
       style="border-radius:8px 8px 0 0;overflow:hidden;
              border-bottom:2px solid #1565c0;">
  <tr>
    <td align="center" bgcolor="#ffffff"
        style="background-color:#ffffff;padding:28px 40px 22px 40px;">
      <img src="cid:taleemabad_logo" height="38" alt="Taleemabad"
           style="display:block;margin:0 auto 14px auto;">
      <p style="margin:0;font-family:Georgia,serif;font-size:11px;
                color:#1565c0;letter-spacing:2px;text-transform:uppercase;">
        People &amp; Culture &nbsp;&bull;&nbsp; Application Update
      </p>
      <p style="margin:10px 0 4px 0;font-family:Georgia,serif;font-size:17px;
                font-weight:bold;color:#1565c0;line-height:1.4;">
        {subject_line}
      </p>
      <p style="margin:0;font-family:Georgia,serif;font-size:12px;color:#5c85c7;">
        {ROLE}
      </p>
    </td>
  </tr>
</table>"""

def build_html(candidate_name, story_title, narrative):
    header = header_block(story_title)

    body = f"""
    <p style="margin:0 0 20px 0;">Hi {candidate_name},</p>

    <p style="margin:0 0 18px 0;">
      Thank you for taking the time to interview with us and for sharing your perspective on the role and on your
      own journey. Every conversation we have helps us understand who people are and how they approach their work.
    </p>

    <p style="margin:0 0 18px 0;">
      {narrative}
    </p>

    <p style="margin:0 0 18px 0;">
      We know this may not be the news you were hoping for, and we genuinely mean this in the spirit of honesty and respect.
      At Taleemabad, we're building a team around shared values, and we believe that fit matters as much as skills do.
      We also know that people grow, and perspectives shift. If you'd like to stay connected or explore other opportunities
      with us in the future, we'd welcome that conversation.
    </p>

    <p style="margin:0 0 32px 0;">
      Thank you again for your time and your interest in Taleemabad.
    </p>

    <!-- Sign-off -->
    <table width="100%" cellpadding="0" cellspacing="0"
           style="margin-top:40px;border-top:1px solid #e0e0e0;padding-top:20px;">
      <tr>
        <td style="font-family:Georgia,serif;font-size:13px;color:#555555;line-height:1.9;">
          Warm regards,<br>
          <strong style="color:#1a1a1a;">People and Culture Team</strong><br>
          <strong style="color:#1565c0;">Taleemabad</strong><br>
          <a href="mailto:hiring@taleemabad.com"
             style="color:#1565c0;text-decoration:none;">hiring@taleemabad.com</a>
          &nbsp;|&nbsp;
          <a href="http://www.taleemabad.com"
             style="color:#1565c0;text-decoration:none;">www.taleemabad.com</a><br>
          <span style="font-size:12px;color:#aaa;margin-top:4px;display:block;">
            Sent on behalf of Talent Acquisition Team by Coco
          </span>
        </td>
      </tr>
    </table>"""

    html_template = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background-color:#f0f4f0;">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background-color:#f0f4f0;padding:32px 0;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0"
             style="max-width:620px;border-radius:8px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);">
        <tr><td>{header}</td></tr>
        <tr>
          <td style="background:#ffffff;padding:40px 52px 48px 52px;
                     border-radius:0 0 8px 8px;
                     font-family:Georgia,serif;font-size:15px;
                     line-height:1.8;color:#1a1a1a;">
            {body}
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""

    return html_template

def send():
    for candidate in CANDIDATES:
        html = build_html(candidate["name"], candidate["story_title"], candidate["narrative"])

        msg = MIMEMultipart("related")
        alt = MIMEMultipart("alternative")
        alt.attach(MIMEText(html, "html"))
        msg.attach(alt)

        logo = MIMEImage(LOGO_BYTES, "png")
        logo.add_header("Content-ID", "<taleemabad_logo>")
        logo.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
        msg.attach(logo)

        msg["From"]    = SENDER
        msg["To"]      = ", ".join(PILOT_TO)
        msg["Subject"] = f"[PILOT] Your Values Conversation - {candidate['story_title']} ({candidate['name']})"

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER, PASSWORD)
            safe_sendmail(server, SENDER, PILOT_TO, msg.as_string(),
                          context=f'job36_values_feedback_pilot_{candidate["name"].replace(" ", "_")}')

        print(f"Pilot sent for {candidate['name']}")

if __name__ == "__main__":
    send()
