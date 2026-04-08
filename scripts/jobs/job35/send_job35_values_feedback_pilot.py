"""
Job 35 — Junior Research Associate, Impact & Policy
Values Interview Feedback Emails — PILOT

Three candidates: Muhammad Junaid, Rabia Zafar, Zeeshan Ali
PILOT MODE: sends to Ayesha only for review.
Set PILOT_MODE = False to go live.
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

PILOT_MODE = True
SENDER     = "ayesha.khan@taleemabad.com"
PASSWORD   = os.getenv("EMAIL_PASSWORD")
PILOT_TO   = "ayesha.khan@taleemabad.com"
CC_LIVE    = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]
ROLE       = "Junior Research Associate, Impact & Policy"
LOGO_PATH  = os.path.join(os.path.dirname(__file__), "../../..", "assets", "logo_taleemabad.png")

# ── HTML HELPERS (v8 design) ──────────────────────────────────────────────────

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

JUNAID_SUBJECT = "MATLAB at midnight, Skardu Springs, and what we kept coming back to"

JUNAID_BODY = (
    P("Dear Muhammad Junaid,") +
    P("We have completed our evaluation of your values conversation for the Junior Research Associate role. We are writing to let you know that we will not be moving you forward at this time. We want to be honest with you about that, and we also want this to feel like something worth reading: a genuine account of what we observed, not a formality.") +

    H("What We Liked Most About You") +
    P("Your learning story is one of the clearest things you brought to this conversation. MATLAB for thesis optimization, a World Bank research methodology program, Elsevier journal publication training, and a trail of Coursera certificates, none of it required, all of it self-initiated. The fact that you named each of these specifically, with a purpose attached, told us something real: you do not learn for the sake of learning. You learn because a problem asked you to. That is a meaningful distinction in a research role.") +
    P("Your field experience across Taleemabad, NIETE, PIET, and the Ministry of Planning, covering school observations, FGDs, KIIs, and monitoring work across urban and rural Islamabad and Rawalpindi, gives you a breadth of ground-level exposure that is not common at your stage. The fact that you have also written about it publicly, publishing field challenges in the Friday Times, suggests you think about your work beyond the task in front of you. That is a signal we do not take lightly.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We share what follows with care, because we believe honest reflection is more useful than softness.") +
    P("The dimension where we found ourselves most uncertain was around <strong>Practice Joy</strong>. When we asked you to describe yourself as one emoji, you chose a thumbs up and described Taleemabad's office culture as friendly, productive, and efficient. What we were hoping to hear was something about your own role in creating that environment: a time you lifted someone, made a moment lighter, brought energy to a team that needed it. You described the culture around you, but we did not yet hear your contribution to it. That story may be there. It just did not come through in this conversation.") +
    P("On <strong>All for One and One for All</strong>, you shared a thoughtful example of quietly guiding a colleague from Sindh who struggled with basic office ethics, using indirect conversations and practical examples rather than direct confrontation. That instinct, protecting someone's dignity while nudging them toward better habits, is admirable. What we were looking for, though, was a moment of backup: a time you absorbed a teammate's mistake, stood in front of a consequence, or sacrificed your own output so someone else could succeed. The mentoring instinct you showed is real. The backup instinct is what we did not yet see.") +
    P("On <strong>Have Courageous Conversations</strong>, you described post-field debriefs with data and impact team leads, daily WhatsApp reports of challenges, and Zoom meetings where you surfaced what was not working. That is genuine upward communication and it matters. Where we found ourselves wondering was around the harder version of the same courage: a time you told someone directly, face to face, something they did not want to hear and held that position. The reporting habit is clear. The confrontation habit is what remained open.") +
    P("On <strong>Don't Hold On Too Tight</strong>, you described delegating a thematic analysis section of an MPhil thesis to a student because your time was limited and their expertise was the better fit. Structurally, this fits the value. What was missing was the stakes. This was freelance work you had taken on, not something you had built over time or were protective of. The letting go did not feel costly, which meant it did not fully illuminate the value. We are left wondering whether there is a more revealing story somewhere in your experience that we did not reach.") +

    H("What We Think You Should Do Next") +
    P("The research orientation is real. The field credibility is real. The learning discipline is real. What the conversation did not yet surface was the relational and team-facing side of who you are: how you show up for others, how you create energy in a room, how you handle moments that require you to step back or step forward in ways that cost you something.") +
    P("Before your next conversation of this kind, we would encourage you to go back through your time at Taleemabad, NIETE, and PIET and look specifically for: the moment you held something for someone else, the moment you told a hard truth to a person rather than a group, the moment you let go of something you had invested in. Those stories are very likely already there. Learning to name them clearly is the single thing that will change how these conversations land.") +
    P("The door here remains open. Should you continue building in this direction and find yourself drawn back to the mission, we would welcome that conversation. Keep an eye on our careers page at <a href='http://www.taleemabad.com' style='color:#1565c0;'>www.taleemabad.com</a>.") +

    PS("<strong>P.S.</strong> The Skardu Springs detail, a family business providing natural spring water, internationally certified, run with pride alongside everything else you are building, told us something about the kind of person you are outside the professional frame. Carry that same specificity into every room you walk into. It is more compelling than any credential.") +

    FOOTER +
    feedback_widget("Muhammad Junaid", ROLE, 1592, "Application Feedback")
)

JUNAID_HTML = wrap(JUNAID_SUBJECT, JUNAID_BODY)


# ── EMAIL 2: RABIA ZAFAR ─────────────────────────────────────────────────────

RABIA_SUBJECT = "The student's slide, the defense panel, and what we kept returning to"

RABIA_BODY = (
    P("Dear Rabia,") +
    P("We have completed our evaluation of your values conversation for the Junior Research Associate role. We are writing to let you know that we will not be moving you forward at this time. We want to be honest with you about that, and we also want this to feel like something worth reading: a genuine account of what we observed, not a standard reply.") +

    H("What We Liked Most About You") +
    P("The moment that stayed with us longest happened in a classroom. A student made a slide error during a presentation. Other students began to laugh. You told the class it was not a mistake, publicly and without hesitation, to protect that student from a moment of embarrassment they had not chosen. That is not a policy or a procedure. That is a reflex. The instinct to put yourself between someone and a consequence they did not deserve is one of the things we look for most carefully in these conversations, and it came through with complete clarity.") +
    P("The methodological feedback you gave your technical supervisor at Javaiyo, telling him directly that the qualitative framework did not fit the project and proposing a revised approach including translation and transcription, also showed real professional courage. That is not an easy conversation to have upward, and the fact that the change was implemented suggests you made the case well.") +
    P("Your willingness to teach, sharing your own past research mistakes with students and peers, working through quantitative methodology with a friend until she successfully defended her thesis, reflects a genuine orientation toward the people around you and not just your own output.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We share what follows with care, because we believe honest reflection is more useful than softness.") +
    P("The dimension where we found ourselves most uncertain was <strong>Don't Hold On Too Tight</strong>. When we asked about a time you voluntarily released something you had built or believed in, the example you offered was your PhD proposal: extensive work, supervisor confirmed funding was unavailable, proposal dropped. The letting go was real, but it was driven entirely by an external constraint, not an internal decision. There was no reframe, no moment of choosing to make space for something new. We found ourselves wondering whether there has been a time when you let go because it was the right thing to do, not because the door closed. That story, if it exists, is the one this value is asking for.") +
    P("On <strong>Don't Walk Away from Hard Things</strong>, you described staying in a difficult job despite a colleague who was making your time there genuinely hard. Three months of endurance is real. What gave us pause was that the resolution came through escalating to the country director rather than through your own direct engagement with the situation. The staying was yours. The solving relied on someone else. We are not reading that as a character gap, but as a gap in the story we were able to hear.") +
    P("On <strong>Continuously Improve Our Craft</strong>, you described teaching others from your own mistakes and helping a peer navigate their thesis. Both are meaningful. What we did not yet hear was a moment of your own proactive improvement: a new method you pursued, a tool you built from scratch, a gap you identified in yourself and closed. The teaching instinct is strong. The self-directed learning story did not fully emerge.") +
    P("On <strong>Have Courageous Conversations</strong>, the feedback you gave your supervisor landed well. Where we found ourselves sitting with a question was in the receiving direction. When the defense panel expert criticized your work, your response was to maintain you were right, not to sit with the possibility that the criticism carried something worth examining. The ability to hold your ground is a strength. The ability to genuinely absorb a hard truth about your own work is what remained open.") +

    H("What We Think You Should Do Next") +
    P("The care you bring to people around you is evident and it is not small. The classroom moment, the thesis coaching, the methodological intervention with your supervisor: these are all signals of someone who takes their responsibilities seriously and who shows up for others. What the conversation asked for more of was the inward-facing version of the same rigor: the moment of genuine release, the moment of genuine reception, the moment of deliberate self-building.") +
    P("Before your next conversation of this kind, we would encourage you to look specifically for: a time you let go of something that was yours by choice rather than by circumstance, a time someone's hard feedback changed something real in how you work, and a time you built a new capability from scratch because the work demanded it. Those stories will sharpen how your values land in any room.") +
    P("The door here remains open. Should you continue building in this direction and find yourself drawn back to this mission, we would welcome that conversation. Keep an eye on our careers page at <a href='http://www.taleemabad.com' style='color:#1565c0;'>www.taleemabad.com</a>.") +

    PS("<strong>P.S.</strong> The classroom moment, telling the class it was not a mistake so a struggling student could hold their head up, is the kind of instinct that does not come from training. It comes from who you are. Carry it forward. It will matter in every room you work in.") +

    FOOTER +
    feedback_widget("Rabia Zafar", ROLE, 1569, "Application Feedback")
)

RABIA_HTML = wrap(RABIA_SUBJECT, RABIA_BODY)


# ── EMAIL 3: ZEESHAN ALI ─────────────────────────────────────────────────────

ZEESHAN_SUBJECT = "Tableau in 20 days, the scheduling fix, and the thing we could not yet see"

ZEESHAN_BODY = (
    P("Dear Zeeshan,") +
    P("We have completed our evaluation of your values conversation for the Junior Research Associate role. We are writing to let you know that we will not be moving you forward at this time. We want to be straightforward with you about that, and we also want this to feel like something worth reading: an honest account of what we saw, not a formality.") +

    H("What We Liked Most About You") +
    P("The hackathon story was the clearest signal in your conversation. A social science background, no data visualization experience, a fully functional Tableau dashboard to build, and 20 days to do it. You taught yourself through YouTube, figured it out, and placed in the top six nationally across all of Pakistan. What made this land was not the outcome. It was the decision to try at all rather than defer to someone with a technical background. That instinct, to run at a gap rather than around it, is one of the things this role genuinely requires. And the fact that you named it simply, without dramatizing it, made it more credible, not less.") +
    P("The team backup example was equally specific. When a colleague contacted the wrong expert for a market research interview, you intercepted the situation, explained the mix-up to the external contact, apologized on the team's behalf, and then sat down with your colleague and walked them through the correct process step by step. You did not flag it upward. You did not let it become a story about someone else's mistake. You handled it and then taught rather than blamed. That sequence, absorb, correct, teach, is not something you can train into someone easily. It was already there in how you described it.") +
    P("The conversation with management about last-minute scheduling changes stands out as well. Raising it in a team meeting, naming it specifically as a request for at least two days advance notice, and seeing the change implemented tells us you know how to turn a frustration into a proposal. A lot of people in early roles either stay quiet or complain sideways. You went to the room and made the case. That is a mature way to operate, and it is exactly what a research environment needs from someone joining it.") +
    P("And the shift you described around smiling, moving from low interaction to deliberate warmth after someone gave you feedback that your default manner was creating distance, and then acting on it visibly until it became part of who you are, told us something important. You received uncomfortable feedback about yourself and you did not defend against it. You used it. That is a harder thing than it sounds, and it came through clearly in how you spoke about it.") +
    P("You also described teaching Coursera data analytics skills to friends entering the field, walking them through from license applications through to Excel and Python fundamentals. The fact that you are doing this while still building your own skills suggests you understand that knowledge compounds when it moves. That is a good sign in someone who will eventually be working alongside junior colleagues or in team-based research settings.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We share what follows with care, because we believe honest reflection is more useful than softness.") +
    P("The one dimension where we found ourselves sitting with a question was <strong>Don't Hold On Too Tight</strong>. When we asked about a time you voluntarily released an initiative, a belief, or an approach you had invested in, you were honest: there was no specific incident you could point to. The example you offered, shifting from prescribed tools to your own preferred analysis tools mid-project when the prescribed approach was not producing good output, showed adaptability and judgment. What it did not yet show was the harder version of the same value: letting go of something that was genuinely yours, that you had built or believed in, because the work or the team asked you to step back. That story is what remained open in the conversation.") +
    P("We want to be honest with you about something else. The cohort you were evaluated alongside was unusually strong for this role. The threshold at this stage was set high, and the decision came down to a narrow gap rather than a broad one. Your conversation showed genuine alignment with most of what we look for. The one dimension that remained unresolved was enough to hold us back, but it was not a signal about your overall readiness or your fit with this kind of work.") +

    H("What We Think You Should Do Next") +
    P("The technical discipline is real. The team instincts are real. The willingness to receive and act on feedback is real. What the conversation asked for more of was an experience of genuine release: a project you stepped back from when someone else was better placed to carry it, an idea you changed your mind about because the evidence asked you to, a moment where you made space for something new by letting go of something old. That experience may come naturally as you take on more complex and longer-term work. When it does, you will have a much fuller answer to that question, and the rest of what you bring will carry even more weight.") +
    P("We would genuinely encourage you to apply again. The things you brought to this conversation are not common at your stage, and the gap that kept us from moving forward is closable with time and the right kind of work. Keep an eye on our careers page at <a href='http://www.taleemabad.com' style='color:#1565c0;'>www.taleemabad.com</a>, and do not hesitate to come back when you see a role that fits.") +

    PS("<strong>P.S.</strong> Twenty days, YouTube, and a top-six finish at a national hackathon with a social science background. That is a story worth telling in every room you walk into. It says more about how you approach hard things than almost anything else could.") +

    FOOTER +
    feedback_widget("Zeeshan Ali", ROLE, 1663, "Application Feedback")
)

ZEESHAN_HTML = wrap(ZEESHAN_SUBJECT, ZEESHAN_BODY)


# ── SEND ──────────────────────────────────────────────────────────────────────

EMAILS = [
    {"name": "Muhammad Junaid", "email": "junaidjadee912@gmail.com", "app_id": 1592,
     "subject": JUNAID_SUBJECT, "html": JUNAID_HTML},
    {"name": "Rabia Zafar",     "email": "rabiya.baloch.31@gmail.com", "app_id": 1569,
     "subject": RABIA_SUBJECT,  "html": RABIA_HTML},
    {"name": "Zeeshan Ali",     "email": "zeeshanali.gzr55@gmail.com", "app_id": 1663,
     "subject": ZEESHAN_SUBJECT,"html": ZEESHAN_HTML},
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
                      context=f"job35_values_feedback_{'pilot' if PILOT_MODE else 'live'}_{to_name.replace(' ','_')}")
    cc_str = f" (CC: {', '.join(cc_list)})" if cc_list else ""
    print(f"  Sent: {to_name} -> {to_email}{cc_str}")


def main():
    print("=" * 60)
    print(f"Job 35 — Junior Research Associate | Values Feedback")
    print(f"Mode: {'PILOT (Ayesha only)' if PILOT_MODE else 'LIVE'}")
    print("=" * 60)

    for e in EMAILS:
        if PILOT_MODE:
            send_email(PILOT_TO, e["name"],
                       f"[PILOT — {e['name']}] {e['subject']}", e["html"])
        else:
            send_email(e["email"], e["name"], e["subject"], e["html"], cc_list=CC_LIVE)

    print(f"\nDone. {len(EMAILS)} emails {'piloted' if PILOT_MODE else 'sent live'}.")
    print("=" * 60)


if __name__ == "__main__":
    main()
