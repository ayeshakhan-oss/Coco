"""
CPD Coach — Values Interview Feedback
Candidate: Syeda Siddiqa Fatima (application id 308, candidate id 266)
Interview: 2026-04-28 | Result: did not proceed (3 +/-, 3 +)

PILOT MODE: per CRITICAL rule 2026-06-08, pilot TO = ayesha.khan@taleemabad.com ONLY.
No CC, no hiring@, no other recipients in pilot.
Set PILOT_MODE = False ONLY after Ayesha's explicit approval to go live.

Format: v8 design (matches scripts/jobs/job36/send_job36_values_feedback_junaid_jawad_formatted.py)
Tone governed by: memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md
"""

import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
from scripts.utils.feedback_widget import feedback_widget
from scripts.utils.v8_template import H, SUB, P, PS, FOOTER, wrap, attach_logo, EYEBROW  # LOCKED layout

PILOT_MODE = True
SENDER   = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")

# PILOT: Ayesha ONLY (critical rule 2026-06-08). No CC.
PILOT_TO = ["ayesha.khan@taleemabad.com"]
# LIVE: candidate in TO, hiring@ + Ayesha in CC.
CANDIDATE_EMAIL = "siddiqa.fatima@dil.org"
CC_LIVE  = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]

ROLE     = "CPD Coach"
APP_ID   = 308
CAND_NAME = "Syeda Siddiqa Fatima"

# Layout (H/SUB/P/PS/wrap/attach_logo/EYEBROW) comes from the LOCKED shared
# module scripts/utils/v8_template.py — do not redefine it here.

# ── CONTENT ───────────────────────────────────────────────────────────────────

SUBJECT = "Stepping up for your team, and where our conversation left us"

BODY = (
    P("Dear Syeda,") +
    P("We have completed our evaluation of your values conversation for the CPD Coach role. We are writing to let you know that we will not be moving you forward at this time. We want to be honest with you about that, and we also want this to be something worth reading: a genuine account of what we observed, not a formality. You gave us your time and your reflections, and the least we can offer in return is a clear and thoughtful response.") +

    H("What We Liked Most About You") +
    P("One of the moments that stayed with us came when we asked about how you show up for the people you work alongside. You described a time your team had a gap in its training schedule, when colleagues were unable to cover a slot, and you stepped in to fill it. You did this without being asked, simply because you saw what the department needed and acted on it. That instinct, to notice a gap and quietly close it before it becomes a problem for everyone else, is exactly the kind of teamwork that holds an organization together. It told us something real about how you understand your place within a team.") +
    P("We were also struck by how you approached work that asked you to learn from the ground up. Stepping into training, you described picking up training design, manual creation, and lesson planning for adult learners, skills that were new to you. Rather than treating that unfamiliarity as a reason to hold back, you took them on and taught yourself what the work required. A willingness to be a beginner, and to stay curious while you find your footing, takes a kind of humility that matters a great deal in a coaching role.") +
    P("Finally, your career across chemistry, biology, and computer science, alongside your background in bioinformatics, showed us genuine range. What stood out most was that when a colleague held deeper expertise in computer science, you recognized it and stepped back to let them lead. Knowing where your own expertise ends, and trusting someone else to carry a subject further, is not something everyone can do gracefully. It reflects a maturity about teams that we valued.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We share what follows with care, because we believe honest reflection is more useful than softness.") +
    P("When we asked about a time you had pushed through something genuinely difficult, you mentioned a science lab construction project. What we found ourselves wanting was a clearer picture of the hard part itself: the moment it nearly came undone, what it cost you to keep going, and what you carried away from it. Coaching often means sitting inside difficulty for a long time, so the specific story of how you stay with something when it is genuinely hard is what we were most hoping to understand, and it stayed somewhat open for us.") +
    P("We also appreciated that you spoke about receiving feedback during your classroom observations with Teach for Pakistan. Being open to feedback is a real strength. What we were listening for, and did not fully hear, was the step that comes after: how that feedback changed what you did, the specific adjustment you made, and what shifted in your practice as a result. The most useful part of feedback often lives in what happens once the conversation ends, and that part of the story is what we found ourselves wanting more of.") +
    P("Finally, when we asked what brings you joy in your work, you described yourself as someone who brings positivity to the people around you. We believe that about you. What we were hoping to reach was the source underneath it: a specific moment that genuinely lit you up, the part of the work that feels alive and real to you, and not only the warmth you extend to others. That deeper, grounded version of joy is what we found ourselves reaching for and did not quite arrive at in our conversation.") +

    H("What We Think You Should Do Next") +
    P("None of what we have written is about ability. The care you show for your team is real, your willingness to learn is real, and your generosity in letting others lead is real. What our conversation did not yet surface was the depth beneath a few of these moments: the texture of the hard things you have moved through, what you do with feedback once you receive it, and what genuinely energizes you in the work.") +
    P("Before your next conversation of this kind, we would gently encourage you to gather a few specific stories in advance: a time something was genuinely hard and you stayed with it, a piece of feedback that changed how you work and exactly what you changed, and a moment in your work that brought you real joy. Those stories are almost certainly already part of your experience. Naming them clearly is what will let others see the full shape of who you are.") +
    P("The door here remains open. Should you keep building in this direction and find yourself drawn back to our mission, we would welcome that conversation. You can keep an eye on our openings at <a href='http://www.taleemabad.com' style='color:#1565c0;'>www.taleemabad.com</a>.") +

    PS("<strong>P.S.</strong> We want you to know that we did see you in that conversation: someone who steps up for others without being asked, who is unafraid to start as a beginner, and who makes room for the people around them to shine. Those qualities travel with you into whatever comes next, and we have no doubt they will serve you and the people lucky enough to work alongside you.") +

    FOOTER +
    feedback_widget(CAND_NAME, ROLE, APP_ID, "Application Feedback")
)

HTML = wrap(subject_line=SUBJECT, role=ROLE, eyebrow=EYEBROW["values_feedback"], body_html=BODY)


# ── SEND ────────────────────────────────────────────────────────────────────

def send_email(to_email, subject, html, cc_list=None):
    msg = MIMEMultipart("related")
    msg["From"]    = SENDER
    msg["To"]      = to_email
    msg["Subject"] = subject
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html, "html", "utf-8"))
    msg.attach(alt)

    attach_logo(msg)

    recipients = [to_email] + (cc_list or [])
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(SENDER, PASSWORD)
        allow_candidate_addresses(recipients)
        safe_sendmail(server, SENDER, recipients, msg.as_string(),
                      context=f"cpd_coach_values_feedback_{'pilot' if PILOT_MODE else 'live'}_syeda")
    cc_str = f" (CC: {', '.join(cc_list)})" if cc_list else ""
    print(f"  Sent -> {to_email}{cc_str}")


def main():
    print("=" * 60)
    print("CPD Coach | Values Feedback | Syeda Siddiqa Fatima")
    print(f"Mode: {'PILOT (Ayesha ONLY)' if PILOT_MODE else 'LIVE'}")
    print("=" * 60)

    if PILOT_MODE:
        send_email(PILOT_TO[0], f"[PILOT — {CAND_NAME}] {SUBJECT}", HTML)
    else:
        send_email(CANDIDATE_EMAIL, SUBJECT, HTML, cc_list=CC_LIVE)

    print("\nDone.")
    print("=" * 60)


if __name__ == "__main__":
    main()
