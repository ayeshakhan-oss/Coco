"""
Job 36 - Field Coordinator, Research & Impact Studies
Values Interview Feedback Emails - PILOT v4

Changes from v3:
- Header: white background with blue text (user requested to compare)
- Subject lines revised (removed gap-referencing endings)
- Closing paragraph updated: values-failed framing (door open, candidate comes back)
- All previous corrections maintained

PILOT MODE: sends to Ayesha + Jawwad only.
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
PILOT_TO  = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]  # pilot recipients
CC_LIVE   = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]
ROLE     = "Field Coordinator, Research &amp; Impact Studies"

LOGO_PATH = os.path.join(os.path.dirname(__file__), "../../..", "assets", "logo_taleemabad.png")


# ── SHARED HTML HELPERS ───────────────────────────────────────────────────────

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


# ── EMAIL 1: Muhammad Omer Khan ───────────────────────────────────────────────

OMER_SUBJECT = "The Punjab handover, the honest answer, and where it left us"

OMER_BODY = (
    P("Dear Omer,") +
    P("We have completed our evaluation of your values interview. We are writing to let you know that we will not be moving you forward for the Field Coordinator, Research and Impact Studies role. We want to be honest with you about that decision, and we also want this to be genuinely useful, so please do read it through.") +

    H("What We Liked Most About You") +
    P("The moment that stood out earliest in the conversation was the UNICEF child labour study in Punjab. Your manager left for a family emergency mid-project, and without fuss or hesitation, you stepped into full project management. You navigated high-risk areas in DG Khan, communicated access constraints proactively to the donor, and adapted your sampling plan on the ground. What stayed with us was not the scale of the action but the instinct behind it: you did not wait to be told, you did not look for permission, and you did not let the project stall. That kind of quiet ownership under pressure is something we genuinely value.") +
    P("Your craft development trajectory also made us pay close attention. Three successive domains, none of which you knew coming in: infection prevention and control at Indus Hospital, sexual reproductive health for the Embassy of Netherlands, and now post-abortion care at ASSD. Most practitioners in research and M&amp;E build expertise in one area and stay there. You made a different choice each time, starting from zero, measuring your own improvement, and building until you were genuinely useful. The shift from paper-based data collection to digital tools like KoboToolbox, Survey CTO, and Google Forms when the old approach became obsolete is a good signal of someone who tracks the profession, not just the task.") +
    P("The enumerator conversation deserved a mention too. When data quality issues surfaced during Punjab data collection, you did not sidestep it or manage around it. You had the direct conversation: corrective action was required, and if not, you would reassign. Specific, clear, and outcome-focused. That kind of directness takes a certain confidence.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We share what follows not as a judgment, but because we believe honest reflection is more useful to you than silence.") +
    P("We want to start by saying that what we share here is not a reflection of your ability or your work ethic, both of which came through clearly. What we found ourselves sitting with were questions about two specific values, and we think naming them honestly is the most respectful thing we can do.") +
    P("The first was <strong>All for One and One for All</strong>. The enumerator-sharing example you gave, sending your team to your colleague's districts when her North Punjab targets were falling behind, genuinely showed us this value in action and we appreciated it. Where we found ourselves wondering was in a later question: whether you had ever set aside a personal ambition or desire for the greater good of the team. Your answer was honest and direct — <em>&ldquo;I think it would be a no.&rdquo;</em> We held that with care, because honesty is something we respect. At the same time, this value sits at the core of how we work at Taleemabad, and we found it difficult to move forward without a moment that showed us the collective instinct in a more personal context.") +
    P("The second was <strong>Practice Joy</strong>. When asked what fun or quirky ritual you might bring into your first month, you described more research-based and evidence-based decision-making. We want to be gentle here, because we do not think this reflects a lack of warmth in you. What it did leave us wondering was whether joy as a deliberate, creative act is something you have yet had the chance to explore in a team setting. In a small, mission-driven team like ours, the people who sustain energy through difficult stretches often do so through small, intentional rituals. We found ourselves wishing we had seen a little more of that side of you.") +

    H("What We Think You Should Do Next") +
    P("Your M&amp;E profile is genuinely strong, and we mean that. The domain breadth, the field management experience, the data systems work. These are real and they will serve you well. What we are pointing to is not technical at all. It is more about the stories you carry and whether you have found the language for them yet.") +
    P("On the sacrifice question, we would gently encourage you to look back through your experience and ask whether there were moments where the team's need and your own interest pulled in different directions, and what you chose. Those moments likely exist. They may simply not yet be the ones you lead with. Finding them and being able to speak about them naturally will make a real difference.") +
    P("On joy, the invitation is simply to notice what you already do that lifts a room. Everyone has something. Once you find yours and can name it, it becomes easy to bring into a conversation like this one.") +
    P("The areas we have named above are genuinely closable with time and reflection. Should you work through them and find yourself drawn back to our mission, we would welcome that conversation with a genuinely open mind. Keep an eye on our careers page at <a href='http://www.taleemabad.com' style='color:#1565c0;'>www.taleemabad.com</a>.") +

    PS("<strong>P.S.</strong> The enumerator-sharing story. You sent your team across districts without being asked, because a colleague's numbers were falling. That instinct is exactly the spirit of All for One. We were simply hoping to find that same quality in a moment that cost you something more personally. It is in you. We hope you find the story that shows it.") +

    FOOTER
)

OMER_HTML = wrap(OMER_SUBJECT, OMER_BODY)


# ── EMAIL 2: Faryal Afridi ────────────────────────────────────────────────────

FARYAL_SUBJECT = "Sehri, Iftari, and what stayed with us"

FARYAL_BODY = (
    P("Dear Faryal,") +
    P("We have completed our evaluation of your values interview. We are writing to let you know that we will not be moving you forward for the Field Coordinator, Research and Impact Studies role at this time. We want to be honest with you about that, and we also want this to feel like something worth holding on to: not just a decision, but a genuine reflection of what we saw in you.") +

    H("What We Liked Most About You") +
    P("The Ramadan data entry story stopped us. Your data-entry team flagged that a submission deadline could not be met. Entering that data was not strictly your responsibility. You came in anyway, and you stayed through Sehri and Iftari to get it done. What made this story land was not the effort itself, though the effort was real. It was the fact that you did not frame it as a sacrifice. You did not negotiate for recognition or calculate whether it was worth doing. You just did it because the work needed doing. That instinct is one of the most genuine things we encounter in these conversations.") +
    P("The two-week solo coverage episode was equally compelling. Your implementation manager left for two weeks, and three parallel workstreams landed in your lap: GPS quarterly data collection, doctor training sessions, and provider forums, none of which were formally yours. Instead of flagging the overload or treating them as out of scope, you built a detailed call log mapping available doctors across districts by timeline and delivered all three within the window. The line you used to describe your philosophy stayed with us long after the interview: <em>the work will always get done; the question is how you handle the stress of doing it.</em> That is a mature and grounded way to move through hard moments.") +
    P("The sunflower was a good choice. Asking to check your WhatsApp before committing to an emoji, then explaining that your colleagues immediately notice when you go quiet because your default presence is warm enough that silence feels like an absence, told us something more accurate than any self-description could have. Joy that is this naturally part of who you are is a real asset in any team.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We share what follows with care, because we believe honest reflection is more useful to you than softness.") +
    P("We want to say first that none of what follows changes our reading of your character or your work ethic. What we noticed were some gaps in the stories we were able to hear, and we think naming them clearly is the most respectful thing we can offer.") +
    P("The dimension where we found ourselves most uncertain was <strong>All for One and One for All</strong>. When asked whether you had ever covered for a colleague's mistake without being asked, you reflected on it honestly and at length, and that honesty itself told us something good. What you described, though, was more of a management posture: I am responsible for what leaves my team, and I keep it clean. That is a genuinely important stance. What we were hoping to hear was a specific moment where someone else's mistake landed and you chose to stand in front of it, absorb it, or quietly shield them from it. We found ourselves wishing that story had come through, because we have a feeling it may be there.") +
    P("On <strong>Continuously Improve Our Craft</strong>, you described meaningful behavioural shifts: learning to ask for clarification quickly, and learning to hold a boundary with field staff who become overly casual. Both are real. Where we found ourselves wondering was whether there had been a newer skill, tool, or methodology you had actively built — something the work demanded of you and you went and learned. That picture did not quite emerge, and it left this dimension feeling a little open.") +
    P("On <strong>Courageous Conversations</strong>, you shared your dynamic with your flatmate in Islamabad: an open culture of calling each other out and receiving hard feedback without defensiveness. The self-awareness in that answer is genuine, and your framing of feedback as data rather than a personal attack is exactly the right orientation. Where we sat with a question was around the weight of the moment. What we were listening for was a time when choosing honesty felt genuinely risky — when the stakes were real and you spoke anyway. That level of difficulty did not come through fully in the example, and it left us curious about moments we may not have reached.") +
    P("On <strong>Don't Hold On Too Tight</strong>, when asked whether you had ever handed something over to someone better suited for greater impact, you paused and drew a blank. We are not reading that as a character gap. But across a few values, a gentle pattern emerged: strong instincts and clear professional orientation, but answers that stayed at the level of what you tend to do rather than a specific named moment. The invitation here is simply to go looking for those stories, because we suspect they exist.") +

    H("What We Think You Should Do Next") +
    P("You are a strong field practitioner with real operational grit, and the warmth you carry is not just pleasant. It is functional and sustaining for any team around you. Nothing we have said above diminishes that.") +
    P("What we are pointing to is a skill that is entirely learnable: identifying and narrating the moments that already prove what you know about yourself. Before your next conversation of this kind, we would encourage you to go back through your DSP, ICARS, and ASSD experience and look deliberately for the specific incidents — the time you absorbed a mistake, the time you challenged someone at a real moment of risk, the time you stepped back and made space for someone else. They are very likely already there. Learning to surface them with a name, a date, and an outcome is the single thing that will change how your values conversations land.") +
    P("The areas we have named above are genuinely closable with time and reflection. Should you work through them and find yourself drawn back to our mission, we would welcome that conversation with a genuinely open mind. Keep an eye on our careers page at <a href='http://www.taleemabad.com' style='color:#1565c0;'>www.taleemabad.com</a>.") +

    PS("<strong>P.S.</strong> Working through Sehri and Iftari for data that was not yours to enter. That story is the clearest window we have into who you are when no one is watching and no one asked. Carry it into every interview you have from this point forward. It is worth more than ten well-structured answers.") +

    FOOTER
)

FARYAL_HTML = wrap(FARYAL_SUBJECT, FARYAL_BODY)


# ── LOAD LOGO ─────────────────────────────────────────────────────────────────

with open(LOGO_PATH, "rb") as f:
    LOGO_BYTES = f.read()


# ── SEND FUNCTION ─────────────────────────────────────────────────────────────

def send_email(subject, html, to_addr, label):
    msg = MIMEMultipart("related")
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html, "html"))
    msg.attach(alt)

    logo = MIMEImage(LOGO_BYTES, "png")
    logo.add_header("Content-ID", "<taleemabad_logo>")
    logo.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
    msg.attach(logo)

    msg["From"]    = SENDER
    msg["To"]      = to_addr
    msg["Cc"]      = ", ".join(CC_LIVE)
    msg["Subject"] = subject

    all_recipients = [to_addr] + CC_LIVE

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER, PASSWORD)
        allow_candidate_addresses(all_recipients if isinstance(all_recipients, list) else [all_recipients])
        safe_sendmail(server, SENDER, all_recipients, msg.as_string(), context='send_job36_values_feedback_pilot')

    print(f"Sent [{label}] -> TO: {to_addr} | CC: {', '.join(CC_LIVE)}")


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    send_email(OMER_SUBJECT,   OMER_HTML,   "mokhan.2173@gmail.com",    "Omer Khan")
    send_email(FARYAL_SUBJECT, FARYAL_HTML, "faryalafridi4@gmail.com",  "Faryal Afridi")
    print("Done. Emails sent to candidates.")
