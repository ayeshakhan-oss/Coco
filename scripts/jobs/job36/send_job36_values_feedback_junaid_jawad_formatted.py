"""
Job 36 — Field Coordinator, Research & Impact Studies
Values Interview Feedback Emails — PILOT (Formatted v8)

Candidates: Muhammad Junaid & Jawad Khan
PILOT MODE: sends to Ayesha + Jawwad for review
Set PILOT_MODE = False to go live
"""

import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
from scripts.utils.feedback_widget import feedback_widget
from scripts.utils.check_token_expiry import check_all_tokens

check_all_tokens(print_output=True)

PILOT_MODE = True
SENDER   = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")
PILOT_TO = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
CC_LIVE  = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]
ROLE     = "Field Coordinator, Research &amp; Impact Studies"

LOGO_PATH = os.path.join(os.path.dirname(__file__), "../../..", "assets", "logo_taleemabad.png")

# ── HTML HELPERS (v8 design) ──────────────────────────────────────────────────

H   = lambda t: f'<h2 style="color:#1565c0;font-size:17px;font-weight:bold;margin:36px 0 6px 0;letter-spacing:0.3px;">{t}</h2>'
SUB = lambda t: f'<p style="color:#1b5e20;font-weight:bold;margin:0 0 14px 0;font-size:14px;">{t}</p>'
P   = lambda t: f'<p style="margin:0 0 18px 0;text-align:justify;font-family:Georgia,serif;font-size:15px;line-height:1.8;">{t}</p>'
PS  = lambda t: f'<p style="margin:32px 0 0 0;padding:20px 24px;background:#f1f8e9;border-left:4px solid #1b5e20;font-style:italic;color:#2a2a2a;font-size:14px;line-height:1.7;font-family:Georgia,serif;">{t}</p>'

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

def header_block(subject_line):
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


# ── EMAIL 1: MUHAMMAD JUNAID ──────────────────────────────────────────────────

JUNAID_SUBJECT = "Your commitment, your experience, and what we need to see next"

JUNAID_BODY = (
    P("Dear Muhammad Junaid,") +
    P("We have completed our evaluation of your values conversation for the Field Coordinator role. We are writing to let you know that we will not be moving you forward at this time. We want to be honest with you about that, and we also want this to feel like something worth reading: a genuine account of what we observed, not a formality.") +

    H("What We Liked Most About You") +
    P("Your commitment to your work and the communities you serve came through with clarity in our conversation. You shared thoughtfully about your experience and your drive to make an impact, and we genuinely appreciated your openness and your willingness to reflect on your journey. The specificity you brought to your fieldwork examples, the way you named the challenges you had encountered, and the care with which you described the populations you serve all signal someone who thinks deeply about the meaning of their work.") +
    P("Your willingness to engage with difficult questions and reflect honestly on your own approach to problem-solving showed a level of professional maturity that we value. The fact that you could articulate both what you have learned and what you are still learning demonstrated a growth mindset that matters in a fast-moving field environment.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We share what follows with care, because we believe honest reflection is more useful than softness.") +
    P("The dimensions where we found ourselves most uncertain were around <strong>All for One</strong> and <strong>Continuously Improve</strong>. When we asked about moments of collaboration, particularly around how you show up for colleagues and how you help lift the team as a whole, the examples that emerged felt more individual than collective. We heard about your own contributions and your own learning, but we found ourselves wanting to hear more about how you actively support teammates, how you absorb someone else's work when the team needs it, or how you show up in ways that make someone else's job easier. Those stories may be there. They just did not come through in this conversation.") +
    P("On <strong>Continuously Improve</strong>, when we explored how you approach your own growth and how you help your team develop better ways of working together, the focus remained largely on your own skill-building. What we were looking for was evidence of how you push the team or the organization toward better practices, how you identify gaps in how you work together, and how you take initiative to address them. The individual learning is real. The team-facing improvement orientation is what remained open.") +
    P("On <strong>Hold Space for Different Perspectives</strong>, you showed openness to hearing other viewpoints. Where we found ourselves wondering was around how actively you create room for those perspectives, especially in moments when they differ significantly from your own. We heard openness. The evidence of actively defending another person's right to think differently, or pushing back on a group dynamic that was excluding a viewpoint, did not fully emerge.") +

    H("What We Think You Should Do Next") +
    P("The field experience is real. Your commitment to the mission is real. Your individual initiative is real. What the conversation did not yet surface was the collaborative and team-building side of who you are: how you show up for others on the team, how you help create a culture of continuous improvement together, and how you actively protect space for different voices and perspectives in your team environment.") +
    P("Before your next conversation of this kind, we would encourage you to go back through your experience and look specifically for: a time you absorbed a teammate's workload or mistake so they could learn, a time you proposed or led a change in how your team works together, and a time you actively defended or made space for a perspective that differed from your own. Those stories will sharpen how your values land in any room.") +
    P("The door here remains open. Should you continue building in this direction and find yourself drawn back to our mission, we would welcome that conversation. Keep an eye on our careers page at <a href='http://www.taleemabad.com' style='color:#1565c0;'>www.taleemabad.com</a>.") +

    PS("<strong>P.S.</strong> The thoughtfulness you bring to understanding impact and the care you demonstrate toward the communities you serve are genuinely valuable qualities. Keep cultivating those. And as you reflect on the feedback above, pay particular attention to how you can translate that care outward: toward the people on your team, toward building systems that work better for everyone, and toward holding multiple perspectives as equally worthy of space and voice.") +

    FOOTER +
    feedback_widget("Muhammad Junaid", ROLE, 1592, "Application Feedback")
)

JUNAID_HTML = wrap(JUNAID_SUBJECT, JUNAID_BODY)


# ── EMAIL 2: JAWAD KHAN ───────────────────────────────────────────────────────

JAWAD_SUBJECT = "Your field experience, your perspective, and where we found ourselves"

JAWAD_BODY = (
    P("Dear Jawad,") +
    P("We have completed our evaluation of your values conversation for the Field Coordinator role. We are writing to let you know that we will not be moving you forward at this time. We want to be straightforward with you about that, and we also want this to feel like something worth reading: an honest account of what we observed, not a standard reply.") +

    H("What We Liked Most About You") +
    P("Your field experience is solid and the insights you bring from your background are genuine. You shared meaningful perspectives on impact and your approach to this kind of work, and we appreciated your willingness to engage in a substantive conversation about the role. The specificity of your field knowledge and your ability to articulate what you have seen and learned on the ground came through clearly, and that matters in a coordinator role where credibility with communities is essential.") +
    P("Your engagement with the technical side of the work and your focus on getting the fundamentals right demonstrate a grounded approach to problem-solving. You showed genuine interest in understanding how this role would function within the broader Taleemabad mission, and that curiosity about fit is something we value.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We share what follows with care, because we believe honest reflection is more useful than softness.") +
    P("The dimension where we found ourselves most uncertain was <strong>Practice Joy</strong>. When we explored how you bring energy to your work and to the teams you are part of, the conversation remained fairly practical and task-focused. What we were hoping to hear was something about how you create moments of lightness, how you lift people around you, how you bring genuine warmth to the work beyond the output. You described the work thoughtfully, but we did not yet hear about the joy or the human connection that sustains it. That story may be there. It just did not come through in this conversation.") +
    P("On <strong>Continuously Improve and Staying Curious</strong>, you spoke about your work with thoughtfulness, but when we asked about how you approach your own learning and how you help teams develop better ways of working together, the focus remained fairly static. What we were looking for was evidence of active curiosity, of identifying gaps and pursuing solutions, of bringing new approaches into how you and your team work. The engagement is genuine. The hunger to learn and improve continuously is what remained open in how you presented it.") +
    P("On <strong>Have Courageous Conversations</strong>, when we explored how you handle difficult moments or conversations with colleagues or stakeholders, the examples felt more reflective than active. What we found ourselves wondering about was a time you initiated a hard conversation, held your position on something important when it would have been easier to let it go, or told someone directly something they did not want to hear. The willingness to reflect is real. The evidence of active courage in the moment did not fully emerge.") +

    H("What We Think You Should Do Next") +
    P("The technical competence is there. The field credibility is there. Your grounded perspective on the work is there. What the conversation did not yet surface was the interpersonal and learning-oriented side of who you are: how you bring genuine joy and warmth to teams, how you actively cultivate your own growth and push teams toward better ways of working, and how you engage in the harder conversations that move things forward.") +
    P("Before your next conversation of this kind, we would encourage you to look specifically for: a moment when you brought real lightness or energy to a difficult situation or team moment, a moment when you actively pursued learning or improvement in how something works, and a moment when you initiated a conversation that mattered even though it was uncomfortable. Those stories will significantly sharpen how you land in any room.") +
    P("The door here remains open. Should you continue building in this direction and find yourself drawn back to our mission, we would welcome that conversation. Keep an eye on our careers page at <a href='http://www.taleemabad.com' style='color:#1565c0;'>www.taleemabad.com</a>.") +

    PS("<strong>P.S.</strong> Your grounded field experience is genuinely valuable, and field coordinators need exactly that kind of practical knowledge. As you develop further, invest in the people side just as much as the technical side. The teams and communities you work with remember how you made them feel far more than what you accomplished. Bring that intentionality forward.") +

    FOOTER +
    feedback_widget("Jawad Khan", ROLE, 1785, "Application Feedback")
)

JAWAD_HTML = wrap(JAWAD_SUBJECT, JAWAD_BODY)


# ── SEND ──────────────────────────────────────────────────────────────────────

EMAILS = [
    {"name": "Muhammad Junaid", "email": "junaidjadee912@gmail.com", "app_id": 1592,
     "subject": JUNAID_SUBJECT, "html": JUNAID_HTML},
    {"name": "Jawad Khan",       "email": "jawadmarwat47@gmail.com", "app_id": 1785,
     "subject": JAWAD_SUBJECT,   "html": JAWAD_HTML},
]

def send_email(to_email, to_name, subject, html, cc_list=None):
    msg = MIMEMultipart("related")
    msg["From"]    = SENDER
    msg["To"]      = to_email
    msg["Subject"] = subject
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html, "html", "utf-8"))
    msg.attach(alt)

    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", "<taleemabad_logo>")
        img.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
        msg.attach(img)

    recipients = [to_email] + (cc_list or [])
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(SENDER, PASSWORD)
        allow_candidate_addresses(recipients)
        safe_sendmail(server, SENDER, recipients, msg.as_string(),
                      context=f"job36_values_feedback_{'pilot' if PILOT_MODE else 'live'}_{to_name.replace(' ','_')}")
    cc_str = f" (CC: {', '.join(cc_list)})" if cc_list else ""
    print(f"  Sent: {to_name} -> {to_email}{cc_str}")


def main():
    print("=" * 60)
    print(f"Job 36 — Field Coordinator | Values Feedback")
    print(f"Mode: {'PILOT (Ayesha + Jawwad)' if PILOT_MODE else 'LIVE'}")
    print("=" * 60)

    for e in EMAILS:
        if PILOT_MODE:
            send_email(e["email"], e["name"],
                       f"[PILOT — {e['name']}] {e['subject']}", e["html"],
                       cc_list=PILOT_TO if PILOT_TO else None)
        else:
            send_email(e["email"], e["name"], e["subject"], e["html"], cc_list=CC_LIVE)

    print(f"\nDone. {len(EMAILS)} emails {'piloted' if PILOT_MODE else 'sent live'}.")
    print("=" * 60)


if __name__ == "__main__":
    main()
