"""
RM internal case study - RECALIBRATION NOTICE to Hafsa Bashir (RM-11).

Ayesha, 2026-09-11: "we need send an email to hafsa, that thank you so much for speaking
with us upon recalibration request and we acknowledge the your score is this ... also draft
should sound like recalibrate request."

WHY THIS IS NOT scripts/send_rm_case_study_outcome_pilot.py
  That script sends a REJECTION and its _gate() hard-blocks exactly what this email needs:
  a printed numeric score, any reference to a conversation, and a forward commitment. This
  is a correction notice, a different type, so it carries its own gate.

WHAT HAPPENED
  Hafsa was told on 2026-09-08 that she fell below the 70% benchmark. She asked for a
  recalibration. A full re-read of her 58-page submission against Revision 2 of the
  benchmark answer key found three marking errors, all running against her:
    1. Q4 was marked at anchor 2, below its own cap. C4 caps at 3 and a cap is a ceiling,
       not a floor. Her cut is 25pp with line-by-line arithmetic that closes.
    2. Cap C1a was applied to Q2 in error. C1a is for reading the below-grade figures as
       composition shares; she does not do that.
    3. A gap note about escalation thresholds was carried over from another script.
  Q1 and Q9 were also under-marked. Total 62.0 -> 72.0, above the published bar.

TWO DELIBERATE DEVIATIONS, BOTH AYESHA'S CALL 2026-09-11
  PRINT_SCORE: CLAUDE.md Rule 25 says never print an individual score in a candidate
    letter. Here the figure IS printed. She already holds her number in her workbook, and
    a correction that withholds the corrected figure reads evasive. Scoped to this email.
  NO_RULE10_OPENING: "This is not a yes for now." would be false. This is a yes.

THREADING (CLAUDE.md Rule 19)
  Threads onto the original decision email, resolved in the SENDING mailbox (ayesha.khan@
  via the local .env app password), never the MCP connector. No [PILOT - ] prefix, because
  that breaks threading and a pilot to Ayesha alone is safe without it.

Usage:
    python scripts/send_rm_recalibration_notice_pilot.py --check   # gate only, send nothing
    python scripts/send_rm_recalibration_notice_pilot.py           # pilot to Ayesha ONLY
    python scripts/send_rm_recalibration_notice_pilot.py --live    # needs Ayesha's approval
"""

import argparse
import json
import os
import re
import smtplib
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.utils.safe_send import safe_sendmail  # noqa: E402
from scripts.utils.v8_template import EYEBROW, FOOTER, P, attach_logo, wrap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT, ".env"))

ROLE = "Regional Manager"
CODE = "RM-11"
FIRST = "Hafsa"
FULL = "Hafsa Bashir"
TO_LIVE = "hafsa.bashir@niete.edu.pk"
SENDER = "ayesha.khan@taleemabad.com"
PILOT_TO = "ayesha.khan@taleemabad.com"

SUBJECT = "Re: An Update on Your Regional Manager Case Study"
# RFC822 Message-ID of the 2026-09-08 live decision email, read from ayesha.khan@ Sent Mail.
PARENT_MSGID = "<6aa0315c.5fb1dcdd.23510d.3f97@mx.google.com>"

# Live CC given by Ayesha 2026-09-11: hiring, ali.sipra, asma.zaheer, ayesha.khan, then
# "add bilal tyoo" on the flag that he was on the 2026-09-08 decision email. The list is
# therefore the thread's own five, matching Rule 19. No bare first name was resolved from
# the repo (Rule 22): every address below already appears in this thread's own headers.
LIVE_CC = [
    "hiring@taleemabad.com",
    "ali.sipra@taleemabad.com",
    "asma.zaheer@niete.edu.pk",
    "bilal@niete.edu.pk",
    "ayesha.khan@taleemabad.com",
]

KEEP = os.path.join(ROOT, "output", "rm_marking")
SCORES_SOURCE = os.path.join(KEEP, "strict_scores.json")
XLSX = os.path.join(KEEP, "individual", f"RM Case Study Feedback - {FULL}.xlsx")

STRICT = json.load(open(SCORES_SOURCE, encoding="utf-8"))
NEW_TOTAL = int(STRICT[CODE]["total"])
ALL_NAMES = [v["name"] for v in
             json.load(open(os.path.join(KEEP, "roster.json"), encoding="utf-8")).values()]

FIRST_PERSON = r"\b(I|I'm|I've|I'll|I'd|my|me|mine|myself)\b"
INTENT_WORDS = [r"you assumed", r"you believed", r"you thought", r"you seemed",
                r"you appeared", r"you lacked", r"you felt", r"you chose not to"]
COMPARISONS = [r"other candidates", r"the pool\b", r"the strongest submission",
               r"the weakest", r"\branked\b", r"compared to others", r"than others"]
CORPORATE = [r"we regret to inform", r"after careful consideration"]
INTERVIEWER_NAMES = [r"\bJawwad\b", r"\bJawad\b", r"\bAyesha\b", r"\bWaqas\b", r"\bZeshan\b",
                     r"\bMoiz\b", r"\bNoah\b"]


def strip_tags(html: str) -> str:
    import html as _h
    txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    txt = re.sub(r"<br\s*/?>", "\n", txt, flags=re.I)
    txt = re.sub(r"</p>|</h2>|</li>", "\n", txt, flags=re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    return re.sub(r"[ \t]+", " ", _h.unescape(txt))


def body() -> str:
    return (
        P(f"Dear {FIRST},") +
        P("Thank you for speaking with us, and for asking us to recalibrate your case "
          "study. Setting your reasoning out as clearly as you did made it straightforward "
          "to go back and check properly.") +
        P("Following your request, we have recalibrated your submission in full against "
          "the benchmark answer key, question by question. The recalibration found errors "
          "in our own marking, and all of them ran in the same direction, against you.") +
        P("You were right on two of the points you raised. On the forced prioritisation "
          "question, your table does carry the arithmetic, the reductions are specific "
          "rather than asserted, and it closes. It had been marked below the level our own "
          "criteria set for that kind of answer. On the information question, all ten items "
          "carry every part the question asked for, including where each piece would come "
          "from, and grouping several of them around data quality was a reasonable choice "
          "rather than repetition.") +
        P("On the regional comparison, your overall conclusion was the one the benchmark "
          "reaches, and your point about the absence of baseline data is fair. One part of "
          "that answer does still differ from the benchmark, and it is set out in the "
          "sheet, but the marking rule applied to it was not the right one and that has "
          "been corrected. A fourth question also moved on the recalibration, which you had "
          "not raised.") +
        P(f"<strong>Your recalibrated score is {NEW_TOTAL}%, against the 70% benchmark we "
          f"had set for moving forward.</strong>") +
        P("Your submission therefore meets the benchmark we published, and we are taking "
          "your application forward to the case study debrief, the same next step as "
          "everyone else who met it.") +
        P("We will send the case study debrief invite separately so you can lock a time. "
          "If you would rather not wait for it, reply to this note with two or three slots "
          "that suit you and we will lock one in from our side.") +
        P("We are sending a corrected evaluation sheet with this note, so the document you "
          "hold matches the outcome. Please treat the earlier one as withdrawn.") +
        P("We are sorry the recalibration was needed. The error was ours, and you should "
          "not have had to ask for it to be found.") +
        P("Thank you again for raising it.") +
        FOOTER
    )


def gate(html: str, subject: str, live: bool, headers: dict) -> None:
    text = strip_tags(html)
    blocks = []

    if not os.path.exists(XLSX):
        blocks.append(f"corrected workbook missing: {XLSX}")
    if not re.search(rf"Dear\s+{FIRST},", text):
        blocks.append("no salutation to the recipient")
    if "70%" not in text:
        blocks.append("the 70% benchmark rule is not stated")

    # The corrected figure must appear, exactly once, and must be the stored total.
    hits = re.findall(rf"\b{NEW_TOTAL}%", text)
    if len(hits) != 1:
        blocks.append(f"corrected figure {NEW_TOTAL}% appears {len(hits)} times, expected 1")
    if str(NEW_TOTAL) != "72":
        blocks.append(f"stored total is {NEW_TOTAL}, not the 72 this letter was written for")
    # The superseded figure must not appear anywhere.
    if re.search(r"\b62\b", text):
        blocks.append("the superseded score 62 appears in the body")

    for nm in ALL_NAMES:
        if nm != FULL and re.search(rf"\b{re.escape(nm)}\b", text):
            blocks.append(f"another colleague is named: {nm}")

    for pats, label in ((INTENT_WORDS, "intent inference"),
                        (COMPARISONS, "candidate comparison"),
                        (CORPORATE, "corporate boilerplate"),
                        (INTERVIEWER_NAMES, "staff name")):
        for p in pats:
            if re.search(p, text, re.I):
                blocks.append(f"{label}: {p}")

    if re.search(FIRST_PERSON, text):
        blocks.append('first-person "I" voice, must be collective "we"')
    if "—" in text or "&mdash;" in html:
        blocks.append("em dash present")

    # Threading is the whole point of this send: a correction that starts a new thread
    # leaves the original decision sitting uncorrected in her inbox.
    for h in ("In-Reply-To", "References"):
        if not headers.get(h):
            blocks.append(f"{h} header is empty")
    if not subject.startswith("Re: "):
        blocks.append("subject does not continue the thread")
    if "[PILOT" in subject:
        blocks.append("PILOT prefix would break threading")

    if live and not LIVE_CC:
        blocks.append("live send with no CC list")

    if blocks:
        print("\n  BLOCKED")
        for b in blocks:
            print(f"     - {b}")
        raise SystemExit("gate failed")
    print(f"  gate passed  |  {len(text.split())} words  |  score {NEW_TOTAL}%")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="send to Hafsa (needs approval)")
    ap.add_argument("--check", action="store_true", help="gate only, send nothing")
    a = ap.parse_args()

    html = wrap(SUBJECT, ROLE, EYEBROW["case_study_outcome"], body())
    headers = {"In-Reply-To": PARENT_MSGID, "References": PARENT_MSGID}
    gate(html, SUBJECT, a.live, headers)

    to = [TO_LIVE] if a.live else [PILOT_TO]
    cc = LIVE_CC if a.live else []
    rcpt = to + [c for c in cc if c not in to]

    print(f"  {'LIVE' if a.live else 'PILOT'}  to={to}  cc={cc or 'none'}")
    if a.check:
        print("  --check: nothing sent")
        return

    msg = MIMEMultipart("mixed")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = ", ".join(to)
    if cc:
        msg["Cc"] = ", ".join(cc)
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="taleemabad.com")
    msg["In-Reply-To"] = headers["In-Reply-To"]
    msg["References"] = headers["References"]

    alt = MIMEMultipart("related")
    alt.attach(MIMEText(html, "html", "utf-8"))
    attach_logo(alt)
    msg.attach(alt)

    with open(XLSX, "rb") as fh:
        att = MIMEApplication(fh.read(), _subtype=(
            "vnd.openxmlformats-officedocument.spreadsheetml.sheet"))
    att.add_header("Content-Disposition", "attachment",
                   filename=f"RM Case Study Feedback - {FULL} (recalibrated).xlsx")
    msg.attach(att)

    pw = os.getenv("EMAIL_PASSWORD")
    if not pw:
        sys.exit("EMAIL_PASSWORD not set")
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(SENDER, pw)
        safe_sendmail(s, SENDER, rcpt, msg.as_string(),
                      context=f"rm_recalibration_{'live' if a.live else 'pilot'}_{CODE}")
    print(f"  SENT -> {rcpt}  (threaded onto {PARENT_MSGID})")


if __name__ == "__main__":
    main()
