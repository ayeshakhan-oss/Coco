"""
Audio Monitoring Officer (Assessments) — 15-day engagement confirmation.
Threads into each person's original "Welcome to Taleemabad" conversation.

Engagement: 20 August 2026 (Thu) -> 3 September 2026 (Thu) = 15 days inclusive.
Wording follows Ayesha's 15 Jul 2026 precedent email verbatim, dates swapped.

PILOT (default): ayesha.khan@taleemabad.com ONLY, no CC.
LIVE  (--live) : To = Ayat, CC = candidate + original distribution list,
                 mirroring the 15 Jul 2026 send exactly.

Message-IDs verified 18 Aug 2026 from ayesha.khan@taleemabad.com via Gmail API.
"""

import os
import sys
import smtplib
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

SUBJECT   = "Re: Welcome to Taleemabad – Audio Monitoring Officer (Assessments)"
START     = "20 August 2026"
END       = "3 September 2026"
COMP      = "PKR 50,000"

PILOT_TO  = "ayesha.khan@taleemabad.com"

# Original distribution list on the 8 May welcome + 15 Jul extension emails.
LIVE_CC_COMMON = [
    "accounts.query@taleemabad.com",
    "hr@taleemabad.com",
    "hiring@taleemabad.com",
    "muzzammil.patel@taleemabad.com",
    "salman.iqbal@taleemabad.com",
    "ahwaz.akhtar@taleemabad.com",
    "sabeena.abbasi@taleemabad.com",
]
LIVE_TO = "ayat@niete.edu.pk"

SIGNATURE_TEXT = """--
Ayesha Raza Khan,
Deputy Manager People & Culture, Taleemabad.
M: +92 335 4288844 |
Empowering millions of children with the learning tool of choice.  @
www.taleemabad.com
LinkedIn |"""

# Lifted verbatim from Ayesha's 15 Jul 2026 send (message-id
# CAE4XdQOZrGkg2RKCEaYQQW8upQHaj4RynbrcpJpfMeTZagkAxQ@mail.gmail.com)
# so the rendered signature is identical to what she normally sends.
SIGNATURE_HTML = (
    '<span class="gmail_signature_prefix">-- </span><br>'
    '<div dir="ltr" class="gmail_signature"><div dir="ltr">'
    '<b style="color:rgb(34,34,34)"><font color="#6aa84f">Ayesha Raza Khan,</font></b>'
    '<div style="color:rgb(34,34,34)"><b><font color="#3d85c6">'
    'Deputy Manager People &amp; Culture, Taleemabad.</font></b></div>'
    '<div style="color:rgb(34,34,34)"><font color="#3d85c6">'
    'M: +92 335 4288844 |&nbsp;</font></div>'
    '<div style="color:rgb(34,34,34)"><font color="#000000">'
    'Empowering millions of children with the learning tool of choice.&nbsp;&nbsp;@</font>'
    '<font color="#888888">&nbsp;</font>'
    '<a href="http://www.taleemabad.com/" style="color:rgb(17,85,204)" '
    'target="_blank">www.taleemabad.com</a></div>'
    '<div style="color:rgb(136,136,136)">'
    '<a href="https://www.linkedin.com/in/ayesha-raza-khan-386668177/" '
    'target="_blank">LinkedIn</a>&nbsp;|&nbsp;</div>'
    '</div></div>'
)


# ── Recipients ────────────────────────────────────────────────────────────────
# `email` is the address the ORIGINAL thread was sent to (drives threading).
# `live_email` is the address a LIVE send must actually use.
PEOPLE = [
    {
        "key": "fareeda",
        "salutation": "Fareeda",
        "email": "shaikhfareeda8@gmail.com",
        "live_email": "shaikhfareeda8@gmail.com",
        # last message in Ayesha's copy of the thread (29 Jul 2026)
        "in_reply_to": "<CAE4XdQOnDKjhB5jFR4c-rmC0YzVqsshoDS953hnLbte5nnL1RQ@mail.gmail.com>",
        "references": [
            "<CALNeUsGZ9M6hkX2fxtv1LqiOYkjtrZhS6Xyr3qG_QjAZjvB4RQ@mail.gmail.com>",
            "<CAE4XdQOZrGkg2RKCEaYQQW8upQHaj4RynbrcpJpfMeTZagkAxQ@mail.gmail.com>",
            "<CACGLuzLuXqCp8gty1r6n2yaLjYDTwtg6vVj0uCZ2Vw1OKMbibw@mail.gmail.com>",
            "<CACGLuz+776Bj=-Vz97WAhUWL+ju6RK9v0+0dqYG7h01y=AdwDg@mail.gmail.com>",
            "<CACGLuzLaR_y2fDr6qyX8Y0RXGFLFFLWbKbk04zPMqCMFcEiS2g@mail.gmail.com>",
            "<CAE4XdQOnDKjhB5jFR4c-rmC0YzVqsshoDS953hnLbte5nnL1RQ@mail.gmail.com>",
        ],
    },
    {
        "key": "kainat",
        "salutation": "Kainat",
        "email": "kaynatsyeda4@gmail.com",
        # 17 Jul 2026 send added this second address — carried into LIVE.
        "live_email": "kaynatsyeda4@gmail.com, kainatsyeda628@gmail.com",
        "in_reply_to": "<CAE4XdQPGBeOzYcrZJQD447EGga8GTh22btiDVjurKWe6_cgwWg@mail.gmail.com>",
        "references": [
            "<CALNeUsE-LkC+Y=vkPY_3_z3abEvyG=0ju8a1BKV1Kv3=QcYMGQ@mail.gmail.com>",
            "<CAE4XdQNmrZ+RSZ2xFgPXi3Kh-4j2Pa52Buh7zrcU6rndKwUZRw@mail.gmail.com>",
            "<CAE4XdQPGBeOzYcrZJQD447EGga8GTh22btiDVjurKWe6_cgwWg@mail.gmail.com>",
        ],
    },
    {
        "key": "laraib",
        "salutation": "Laraib",
        "email": "laraibsyed1999@gmail.com",
        "live_email": "laraibsyed1999@gmail.com",
        "in_reply_to": "<CALNeUsHzLOsdrb5mP7ZkFPi4182JhQm5oV1Xv4xnkPHnBqBJwg@mail.gmail.com>",
        "references": [
            "<CALNeUsHzLOsdrb5mP7ZkFPi4182JhQm5oV1Xv4xnkPHnBqBJwg@mail.gmail.com>",
        ],
    },
    {
        "key": "gulrukh",
        "salutation": "Gul Rukh",
        "email": "gulrukhdinal@gmail.com",
        "live_email": "gulrukhdinal@gmail.com",
        "in_reply_to": "<CALNeUsHJz_=tSGFssyd1uZTnQWe3kiQvhuTms3S=_buAfrnNNw@mail.gmail.com>",
        "references": [
            "<CALNeUsHJz_=tSGFssyd1uZTnQWe3kiQvhuTms3S=_buAfrnNNw@mail.gmail.com>",
        ],
    },
    {
        "key": "arshad",
        "salutation": "Arshad",
        "email": "arshadkhan285981@gmail.com",
        "live_email": "arshadkhan285981@gmail.com",
        "in_reply_to": "<CALNeUsEQKGnZOsXFp9JvT9KNssDqoxkQqhffNPk30qecaMJkoA@mail.gmail.com>",
        "references": [
            "<CALNeUsEQKGnZOsXFp9JvT9KNssDqoxkQqhffNPk30qecaMJkoA@mail.gmail.com>",
        ],
    },
    {
        "key": "muddasir",
        "salutation": "Muddasir",
        # Original welcome went to a MISTYPED address (@gamil.com) and never landed.
        "email": "Zamanmuddasir44@gamil.com",
        # Correct address, verified from his own calendar RSVP in Ayesha's mailbox.
        "live_email": "zamanmuddasir44@gmail.com",
        "in_reply_to": "<CALNeUsENX1Pxbqoe1PdiKr1QKjKfNLu4=+HUxdGsv+CxDD-x6A@mail.gmail.com>",
        "references": [
            "<CALNeUsENX1Pxbqoe1PdiKr1QKjKfNLu4=+HUxdGsv+CxDD-x6A@mail.gmail.com>",
        ],
    },
]


def build_text(salutation: str) -> str:
    """Plain-text alternative part."""
    return f"""Dear {salutation},

We hope you're doing well.

We're delighted to have you back with us for another 15-day Audio Monitoring \
project. We truly appreciated your contribution during the previous project, \
and we're excited to have you join us again for this next phase.

This email serves as confirmation of your employment for the upcoming project, \
which will run from {START} to {END}.

Your compensation for this 15-day engagement will be {COMP}.

We're looking forward to working with you again and appreciate your continued \
support on the project.

Should you have any questions or need any clarification, please don't hesitate \
to reach out to the HR team.

We wish you all the best and look forward to another successful engagement \
together.

{SIGNATURE_TEXT}
"""


def build_html(salutation: str) -> str:
    """HTML part — same paragraph/bold structure as the 15 Jul 2026 email.

    No fixed-width wrapper table, so it stays fluid on mobile (CLAUDE.md Rule 16).
    """
    return (
        '<div dir="ltr"><div dir="ltr"><div dir="ltr">'
        f'Dear {salutation},<br><div>'
        "<p>We hope you&#39;re doing well.</p>"
        "<p>We&#39;re delighted to have you back with us for another "
        "<strong>15-day Audio Monitoring project</strong>. We truly appreciated "
        "your contribution during the previous project, and we&#39;re excited to "
        "have you join us again for this next phase.</p>"
        "<p>This email serves as confirmation of your employment for the upcoming "
        f"project, which will run from <strong>{START} to {END}</strong>.</p>"
        "<p>Your compensation for this 15-day engagement will be "
        f"<strong>{COMP}.</strong></p>"
        "<p>We&#39;re looking forward to working with you again and appreciate "
        "your continued support on the project.</p>"
        "<p>Should you have any questions or need any clarification, please "
        "don&#39;t hesitate to reach out to the HR team.</p>"
        "<p>We wish you all the best and look forward to another successful "
        "engagement together.</p>"
        "</div></div></div>"
        '<div><br clear="all"></div><div><br></div>'
        f"{SIGNATURE_HTML}"
        "</div>"
    )


def send_one(server, person: dict, pilot: bool) -> list:
    msg = MIMEMultipart("alternative")
    msg.attach(MIMEText(build_text(person["salutation"]), "plain", "utf-8"))
    msg.attach(MIMEText(build_html(person["salutation"]), "html", "utf-8"))

    msg["Subject"]     = SUBJECT
    msg["From"]        = EMAIL_USER
    msg["In-Reply-To"] = person["in_reply_to"]
    msg["References"]  = " ".join(person["references"])

    if pilot:
        msg["To"]  = PILOT_TO
        recipients = [PILOT_TO]
    else:
        msg["To"]  = LIVE_TO
        cc = [a.strip() for a in person["live_email"].split(",")] + LIVE_CC_COMMON
        msg["Cc"]  = ", ".join(cc)
        recipients = [LIVE_TO] + cc

    allow_candidate_addresses(recipients)
    safe_sendmail(
        server, EMAIL_USER, recipients, msg.as_string(),
        context=f"audio_monitoring_extension_{person['key']}_{'pilot' if pilot else 'live'}",
    )
    return recipients


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="send to real recipients")
    ap.add_argument("--only", help="comma-separated keys to send (default: all)")
    args = ap.parse_args()

    pilot = not args.live
    people = PEOPLE
    if args.only:
        keys = {k.strip().lower() for k in args.only.split(",")}
        people = [p for p in PEOPLE if p["key"] in keys]
        if not people:
            sys.exit(f"No people matched --only {args.only}")

    mode = "PILOT (Ayesha only)" if pilot else "LIVE"
    print(f"Mode: {mode} | {len(people)} email(s) | {START} -> {END} | {COMP}\n")

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo()
        s.starttls()
        s.login(EMAIL_USER, EMAIL_PASSWORD)
        for p in people:
            rec = send_one(s, p, pilot)
            print(f"  [{p['key']:9}] {p['salutation']:9} -> {', '.join(rec)}")

    print(f"\nDone. {len(people)} sent.")


if __name__ == "__main__":
    main()
