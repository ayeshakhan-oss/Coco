"""
Preview email — Feedback Widget
Sends a dummy values feedback email with the widget appended.
TO: ayesha.khan@taleemabad.com + jawwad.ali@taleemabad.com
"""

import os, smtplib, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../..", ".env"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
from scripts.utils.feedback_widget import feedback_widget

SENDER    = os.getenv("EMAIL_USER")
PASSWORD  = os.getenv("EMAIL_PASSWORD")
PILOT_TO  = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
ROLE      = "Field Coordinator, Research &amp; Impact Studies"
SUBJECT   = "[PREVIEW] Feedback Widget — Values Feedback Email"
LOGO_PATH = os.path.join(os.path.dirname(__file__), "../..", "assets", "logo_taleemabad.png")

# ── HTML helpers (v8 design) ──────────────────────────────────────────────────

H   = lambda t: f'<h2 style="color:#1565c0;font-size:17px;font-weight:bold;margin:36px 0 6px 0;letter-spacing:0.3px;">{t}</h2>'
SUB = lambda t: f'<p style="color:#1b5e20;font-weight:bold;margin:0 0 14px 0;font-size:14px;">{t}</p>'
P   = lambda t: f'<p style="margin:0 0 18px 0;text-align:justify;">{t}</p>'
PS  = lambda t: f'<p style="margin:32px 0 0 0;padding:20px 24px;background:#f1f8e9;border-left:4px solid #1b5e20;font-style:italic;color:#2a2a2a;font-size:14px;line-height:1.7;">{t}</p>'

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

def header_block():
    return f"""
<table width="100%" cellpadding="0" cellspacing="0"
       style="border-radius:8px 8px 0 0;overflow:hidden;border-bottom:2px solid #1565c0;">
  <tr>
    <td align="center" bgcolor="#ffffff"
        style="background-color:#ffffff;padding:28px 40px 22px 40px;">
      <img src="cid:taleemabad_logo" height="38" alt="Taleemabad"
           style="display:block;margin:0 auto 14px auto;">
      <p style="margin:0;font-family:Georgia,serif;font-size:11px;
                color:#1565c0;letter-spacing:2px;text-transform:uppercase;">
        People &amp; Culture &nbsp;&bull;&nbsp; Values Interview
      </p>
      <p style="margin:10px 0 4px 0;font-family:Georgia,serif;font-size:17px;
                font-weight:bold;color:#1565c0;line-height:1.4;">
        A note on your values conversation
      </p>
      <p style="margin:0;font-family:Georgia,serif;font-size:12px;color:#5c85c7;">
        {ROLE}
      </p>
    </td>
  </tr>
</table>"""

def wrap(body_html):
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
        <tr><td>{header_block()}</td></tr>
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

# ── Dummy body ────────────────────────────────────────────────────────────────

DUMMY_BODY = (
    P("Dear [Candidate Name],") +
    P("This is a preview email demonstrating how the feedback widget appears at the bottom of a personalised values interview feedback email. The body you are reading is placeholder text only.") +

    H("What We Liked Most About You") +
    P("The candidate brought a clear example of resilience in a high-pressure field environment. Their instinct to step into a gap without being asked was the strongest signal in the conversation, and it came through with genuine specificity rather than rehearsed framing.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We share what follows with care, because we believe honest reflection is more useful than softness.") +
    P("There were moments where the examples stayed at the level of general orientation rather than a specific named incident. The invitation is to go back through past experience and look for the moments that prove what they already know about themselves.") +

    PS("<strong>P.S.</strong> This is a preview only. The widget below is the new addition — one tap per question, logs silently to the shared Google Sheet. No form, no external tool.") +

    FOOTER +
    feedback_widget("[Candidate Name]", "Field Coordinator", 0, "Application Feedback")
)

HTML = wrap(DUMMY_BODY)

# ── Send ──────────────────────────────────────────────────────────────────────

def send():
    msg = MIMEMultipart("related")
    msg["From"]    = SENDER
    msg["To"]      = ", ".join(PILOT_TO)
    msg["Subject"] = SUBJECT

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(HTML, "html", "utf-8"))
    msg.attach(alt)

    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", "<taleemabad_logo>")
        img.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
        msg.attach(img)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(SENDER, PASSWORD)
        allow_candidate_addresses(PILOT_TO)
        safe_sendmail(server, SENDER, PILOT_TO, msg.as_string(), context="feedback_widget_preview")

    print(f"Sent to: {', '.join(PILOT_TO)}")

if __name__ == "__main__":
    send()
