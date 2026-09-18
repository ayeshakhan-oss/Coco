#!/usr/bin/env python3
"""
Warm Bench Feedback Email - Salman Tariq
Position: Growth Manager - Lahore (Job 39, Markaz application 3656)

EVIDENCE (verified 2026-09-18, read from Markaz/Neon application 3656 only):
  - values_scorecard (interview 24 Jul 2026): PASS, 6(+) / 0(+/-) / 0(-)
  - gwc_scorecard: Get It 7 / Want It 9 / Capacity 8, final mark Yes

WHAT THIS LETTER USES (selective, not exhaustive - Rule 31a):
  1. Upward pushback on the one-day implementation-plan request (Courageous
     Conversations deepDive) -> opening + subject line
  2. The four-year incubation-centre project carried to completion
     (Don't Walk Away deepDive)
  3. Team bonuses / promotions ahead of his own, and fighting his own
     organisation so a colleague's family received what they were owed
     (All for One deepDive, stated as what HE DID - see below)
  4. Releasing his own Punjab Startup Portal feasibility work + dropping
     over-explaining (Don't Hold On Too Tight deepDive) -> P.S.

WHAT THIS LETTER DELIBERATELY OMITS (Rule 31b/b2 - removed, not softened):
  - The father's 25-day ICU vigil, the coma-scale readings and the outcome
    (family crisis narrated as a scene; a death)
  - The office boy who was killed, the widow, the death benefit figure
    (another person's death). Only what SALMAN DID is kept.
  - The therapy disclosure (mental-health disclosure)
  These are HARD BLOCKS in scripts/evals/candidate_communication_eval.py and
  were the reason the 15 Sep draft round happened. Do not reinstate them.

THE ONE GAP (Rule 31c): moving a decision from interest to a committed yes with
senior government officials through relationship groundwork. Stated once, as
what WE needed and could not establish. No role-play is replayed, no answer is
graded, and the hiring manager's own wording is nowhere in the letter (Rule 30 /
core tone behaviour 6).

Layout: scripts/utils/v8_template.py (locked 2026-06-10) - imported, never inlined.
Tone:   memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md (core tone 2026-09-14)
SOP:    .claude/skills/01_candidate-communication/03_warm-bench-feedback-email.md

PILOT recipient: ayesha.khan@taleemabad.com ONLY (Rule 4). No CC.
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, root_dir)

from dotenv import load_dotenv
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
from scripts.utils.v8_template import H, P, PS, FOOTER, wrap, attach_logo, EYEBROW
from scripts.utils.feedback_widget import feedback_widget

load_dotenv(dotenv_path=os.path.join(root_dir, ".env"))

# -- Configuration ------------------------------------------------------------
CANDIDATE_NAME  = "Salman Tariq"
CANDIDATE_EMAIL = "salman.tariq@rocketmail.com"
POSITION        = "Growth Manager - Lahore"
APP_ID          = 3656

PILOT_MODE = True   # pilot to Ayesha ONLY; flip to False only after her approval

SENDER   = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")

PILOT_TO = "ayesha.khan@taleemabad.com"

TITLE_LINE = "The Plan You Would Not Rush"
SUBJECT    = (f"[PILOT - {CANDIDATE_NAME}] {TITLE_LINE}" if PILOT_MODE else TITLE_LINE)

# -- Body (warm bench: 3 sections + P.S.) -------------------------------------
body = "\n".join([
    P("Dear Salman,"),

    P("This is not a yes for now."),

    P("But we want to tell you something about what we saw across our conversations "
      "with you, because the panel kept returning to it afterwards and it is the "
      "reason this decision took us as long as it did."),

    P("One moment in particular stayed in the room. You told us about the day you "
      "were given a single night to produce a complete rollout design: nine district "
      "headquarters, every public university in the province, and a pipeline running "
      "from first contact through to investment. The easy route was open to you: "
      "agree on the spot, assemble something overnight from what already existed on "
      "paper, and let the gaps surface later, when they would have been somebody "
      "else's problem to find. Instead you went back and asked for more time "
      "and more support, because the design needed fieldwork of its own before anyone "
      "could stand behind it. What we noticed was not only that you made that case, "
      "but that you made it upward, to the person who had just asked you for the "
      "opposite, and that you made it about the work rather than about your own hours."),

    H("What Stayed With Us"),

    P("Two other things from our conversations sat with us in the same way."),

    P("The first was the national incubation programme you carried for four years. "
      "You described the ministries, the district administration, the chambers, the "
      "universities, student numbers that kept moving underneath you, and sites that "
      "shifted from Jamshoro to Lasbela while the work was still live. Four years is "
      "a long time after the interesting part of a project is over. Most of it is the "
      "unglamorous middle, where nothing is new and the reasons to quietly let "
      "something drift are everywhere. You stayed with it until it was finished, and "
      "you described the obstacles plainly, without arranging them into a story where "
      "you came out as the hero. That plainness registered with us."),

    P("The second was how you have treated the people around you when nobody was "
      "counting. You made sure your team received money they were entitled to and did "
      "not know about. At appraisal you argued for your team members' promotions "
      "before your own, and yours did not come through that year. And you went "
      "against your own organisation so that a colleague's family received what they "
      "were owed, at a point when it would have been easier for everyone if no one "
      "had raised it. None of this reached us as a claim about your values. It came "
      "out as things you had done, in order, with the costs attached. What we noticed "
      "was that in each one you absorbed the friction so that somebody else did not "
      "have to."),

    H("Here's the Honest Part"),

    P("We owe you a straight account of where this landed, because you gave this "
      "process a great deal of your time. This role sits inside education and "
      "government systems that are already "
      "running before we arrive. They keep to their own calendars, their own sign-off "
      "chains and their own priorities, and none of that rearranges itself because "
      "our case is a good one. The person in this seat has to move a specific "
      "decision from polite interest to a real commitment with people who hold "
      "genuine power: secretaries, ministers, senior officials with full desks and "
      "very little reason to add us to them. In our experience the thing that carries "
      "that final step is rarely the strength of the analysis. It is the relationship "
      "that was already in place before the ask was ever made, built over months with "
      "nothing visible to show for the time."),

    P("What we could see clearly was how well you understand that machinery. Your "
      "years inside government gave you a real feel for how those institutions decide "
      "things rather than how their org charts suggest they do, you were precise "
      "about where a decision truly sits and who has to move before anything else "
      "can, and on the question of where you would draw an ethical line we came away "
      "with no ambiguity at all. That last one matters more to us than it may sound, "
      "and we do not take it for granted. What we needed for this seat and were not "
      "able to establish was a record of carrying one of those relationships yourself "
      "to the point where a senior official committed, where something moved from "
      "interest into a funded and signed arrangement because of groundwork you had "
      "personally laid."),

    P("We want to be careful about what we are and are not saying. We are not saying "
      "this work is beyond you, and we are not making a prediction about you at all. "
      "We are saying something narrower. This is a single seat whose first months are "
      "relationship work before they are anything else, we needed certainty about "
      "that one thing from day one, and the evidence in front of us did not let us "
      "reach it. That is the whole of the decision, and it turned on that alone."),

    H("Where We Want to Leave This"),

    P("Both of these things are true at once, and we do not want the second to erase "
      "the first. You pushed back upward when the work deserved it. You finished "
      "something long after the novelty had gone. You put your team ahead of yourself "
      "in the moments when that cost you. You read institutions clearly and described "
      "them honestly. That is what we saw, and saying no to this role does not unsay "
      "any of it."),

    P("We would be glad to hear from you again. If another role opens here, we would "
      "welcome a fresh application from you, and we would come to it remembering "
      "these conversations rather than starting from nothing. Thank you for the "
      "seriousness you brought "
      "to every stage of this, and for the directness you showed us in asking for an "
      "honest answer. You were right to ask."),

    PS("<strong>P.S.</strong> The moment we keep returning to is the Punjab Startup "
       "Portal work. You had put real effort into that feasibility study, the "
       "benchmarking, the slides, the references, and when leadership decided it was "
       "not the priority, you let it go. Holding your own work that lightly while "
       "still caring about it that much is not a small thing, and it stayed with us."),

    feedback_widget(CANDIDATE_NAME, POSITION, APP_ID, "Application Feedback"),

    FOOTER,
])

HTML = wrap(subject_line=TITLE_LINE, role=POSITION,
            eyebrow=EYEBROW["warm_bench"], body_html=body)


def build_message(to_addr, cc_addr=None):
    msg = MIMEMultipart("related")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = to_addr
    if cc_addr:
        msg["Cc"] = cc_addr
    alt = MIMEMultipart("alternative")
    msg.attach(alt)
    alt.attach(MIMEText(HTML, "html"))
    attach_logo(msg)
    return msg


if __name__ == "__main__":
    if PILOT_MODE:
        recipients = [PILOT_TO]
        msg = build_message(PILOT_TO)
    else:
        # Live CC list for this thread, per the case study debrief invite that
        # already went to him (7 Aug): Waqas Tanveer, Ayesha, hiring@, Ali Sipra,
        # Zeest Qureshi. Confirm with Ayesha before flipping PILOT_MODE.
        cc_list = [
            "waqas.tanveer@taleemabad.com",
            "ayesha.khan@taleemabad.com",
            "hiring@taleemabad.com",
            "ali.sipra@taleemabad.com",
            "zeest.qureshi@taleemabad.com",
        ]
        recipients = [CANDIDATE_EMAIL] + cc_list
        msg = build_message(CANDIDATE_EMAIL, cc_addr=", ".join(cc_list))
        allow_candidate_addresses([CANDIDATE_EMAIL])

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    safe_sendmail(
        smtp_server=server,
        sender=SENDER,
        recipients=recipients,
        message=msg.as_string(),
        context="warm_bench_feedback_salman_tariq_gm_lahore",
    )
    server.quit()

    where = PILOT_TO if PILOT_MODE else f"{CANDIDATE_EMAIL} (+ CC)"
    print(f"\n[{'PILOT' if PILOT_MODE else 'LIVE'} SENT] to {where}")
    print(f"Candidate: {CANDIDATE_NAME} ({CANDIDATE_EMAIL})")
    print(f"Position : {POSITION}  |  Markaz application {APP_ID}")
    print(f"Subject  : {SUBJECT}")
