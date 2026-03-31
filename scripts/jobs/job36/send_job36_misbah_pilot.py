"""
Single pilot email — Misbah Zafar Iqbal
Sends the confirmed HTML design to Ayesha only so she can see
exactly how it will land in a candidate's inbox.
"""

import os, smtplib, base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__)
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
, "../../..", ".env"))

SENDER   = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")
PILOT_TO = "ayesha.khan@taleemabad.com"
ROLE     = "Field Coordinator, Research &amp; Impact Studies"
LOGO_PATH = os.path.join(os.path.dirname(__file__), "../../..", "assets", "logo_taleemabad.png")


# ── HTML helpers (confirmed design) ──────────────────────────────────────────

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


def wrap(subject_line, body_html):
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background-color:#f0f4f0;">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background-color:#f0f4f0;padding:32px 0;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0"
             style="max-width:620px;border-radius:8px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);">
        <tr><td>{header_block(subject_line)}</td></tr>
        <tr>
          <td style="background:#ffffff;padding:40px 52px 48px 52px;
                     border-radius:0 0 8px 8px;
                     font-family:Georgia,serif;font-size:15px;
                     line-height:1.8;color:#1a1a1a;">
            {body_html}
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


H      = lambda t: f'<h2 style="color:#1565c0;font-size:17px;font-weight:bold;margin:36px 0 6px 0;letter-spacing:0.3px;">{t}</h2>'
SUB    = lambda t: f'<p style="color:#1b5e20;font-weight:bold;margin:0 0 14px 0;font-size:14px;">{t}</p>'
P      = lambda t: f'<p style="margin:0 0 18px 0;text-align:justify;">{t}</p>'
FOOTER = """
<table width="100%" cellpadding="0" cellspacing="0"
       style="margin-top:40px;border-top:1px solid #e0e0e0;padding-top:20px;">
  <tr>
    <td style="font-family:Georgia,serif;font-size:13px;color:#555;line-height:1.9;">
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


# ── Misbah's email ────────────────────────────────────────────────────────────

SUBJECT = "Your Application for Field Coordinator, Research & Impact Studies"

BODY = (
    P("Dear Misbah,") +

    P("Thank you so much for applying to the Field Coordinator role at Taleemabad. "
      "We genuinely appreciated reviewing your profile. It is clear you bring real depth "
      "in coordination work, and we wanted to take the time to give you thoughtful feedback "
      "rather than a generic response.") +

    H("What We Appreciated In Your Profile") +

    P("Your background is genuinely impressive in many ways. Your three years as Assistant "
      "Director at the Ministry of Poverty Alleviation and Social Safety shows you understand "
      "how to navigate complex stakeholder environments, coordinate across government levels, "
      "and manage monitoring visits at scale. That is real experience in a challenging sector. "
      "Your MA in Social Work and MPhil in Public Policy also signal that you think deeply "
      "about implementation and systems, and that is exactly the kind of grounding we value "
      "at Taleemabad.") +

    P("Your current work at FAST University, combined with your volunteer advisory role at "
      "Ecosphere Shift, shows you are someone who stays engaged with meaningful work even "
      "outside of formal employment. That matters, and we noticed it.") +

    H("Why We Are Not Moving Forward at This Stage") +

    SUB("We share this not as a judgment of your capability, but because we believe honest "
        "and specific feedback is more respectful than silence.") +

    P("After carefully reading your CV, we do not think this particular role is the right "
      "fit, not because you lack capability, but because the skill set we need for Field "
      "Coordinator is quite specific, and your strongest experience lies elsewhere.") +

    P("The Field Coordinator role is operationally intense. The core work is on-the-ground "
      "field management: directly supervising and quality-checking enumerators, enforcing "
      "sampling plans in real time, spotting data quality issues as they happen, and pushing "
      "back hard when field standards slip. It is about being in schools, managing third-party "
      "survey firms, running daily dashboards, and solving logistics problems in the moment. "
      "It is less about policy coordination and stakeholder relations, which you do very well, "
      "and more about ground-level operational oversight of research teams.") +

    P("Looking at your experience, your strength has been at the coordination and advisory "
      "level: working with donors, organizing steering committee meetings, preparing progress "
      "reports with M&amp;E teams, and providing strategic direction. That is valuable work, "
      "and it is genuinely different from what this role demands. Your monitoring visits were "
      "likely focused on compliance and reporting, not on the day-to-day management of field "
      "teams and survey operations.") +

    P("What the role specifically requires, and what we did not yet see strongly evidenced "
      "in your CV, is hands-on experience managing survey firms or enumerator teams: someone "
      "who has actually trained, observed, and course-corrected field staff in real time, "
      "read a sampling plan and enforced it when a firm wants to cut corners, and built "
      "dashboards to flag anomalies. These are operational muscles that take time to develop, "
      "and we want to be fair to you: this role asks for someone with one to three years of "
      "that very specific kind of field research or M&amp;E execution experience. Your "
      "background in health and social development is solid, but it does not yet translate "
      "directly to the research operations environment we are building.") +

    H("What We Would Encourage You to Consider") +

    P("Please do not take this as a signal to stop applying to Taleemabad. We genuinely "
      "think there could be roles here that play to your actual strengths. Your stakeholder "
      "management experience, your policy background, your ability to work across government "
      "and civil society: these are exactly what we need as we scale our impact work. A role "
      "focused on government coordination, policy partnerships, or a more strategic monitoring "
      "and evaluation position could be a much better match for what you bring.") +

    P("We would encourage you to keep an eye on our careers page at "
      "<a href='http://www.taleemabad.com' style='color:#1565c0;'>www.taleemabad.com</a>, "
      "or feel free to reach out directly if you want to explore where else your profile "
      "might add real value to our team. Your commitment to community-centered work is clear, "
      "and that is the energy we want more of.") +

    FOOTER
)


# ── Send ──────────────────────────────────────────────────────────────────────

def send():
    html = wrap(SUBJECT, BODY)

    msg = MIMEMultipart("related")
    msg["From"]    = SENDER
    msg["To"]      = PILOT_TO
    msg["Subject"] = SUBJECT

    msg.attach(MIMEText(html, "html"))

    # Attach logo as CID
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", "<taleemabad_logo>")
        img.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
        msg.attach(img)
    else:
        print(f"Warning: logo not found at {LOGO_PATH}")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(SENDER, PASSWORD)
        allow_candidate_addresses([PILOT_TO] if isinstance([PILOT_TO], list) else [[PILOT_TO]])
        safe_sendmail(server, SENDER, [PILOT_TO], msg.as_string(), context='send_job36_misbah_pilot')

    print(f"Sent.")
    print(f"  TO:      {PILOT_TO}")
    print(f"  Subject: {SUBJECT}")


if __name__ == "__main__":
    send()
