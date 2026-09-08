"""
RM internal case study - question-by-question developmental analysis for the 8 candidates
scoring below the published 70% bar.

Ayesha, 2026-09-02: "send me question by question analysis for people below 70 as we will
reject them and they are internal candidates so i want a very thorough analysis. of what was
asked, what was answered by and what could have been better or improved."

STRUCTURE - for each of the 8, for each of Q1-Q10:
  What the question asked   (verbatim from the case, with its mark value)
  What <name> answered      (factual account of what is actually in their submission)
  What would have made it stronger  (specific and actionable, not a restatement of the mark)

Each candidate starts on a new page so a single section can be lifted out for an individual
conversation without the others attached.

Sources: strict_scores.json (marks + caps), qbq.json (per-question analysis), roster.json.
Internal report to Ayesha only. Mobile-responsive per CLAUDE.md Rule 16.
"""

import json
import os
import smtplib
import subprocess
import sys
import tempfile
import shutil
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.utils.safe_send import safe_sendmail  # noqa: E402

SENDER = "ayesha.khan@taleemabad.com"
RECIPIENTS = ["ayesha.khan@taleemabad.com"]
SUBJECT = "RM Case Study - question-by-question analysis, the 8 below the line"

SCRATCH = (r"C:\Users\Dell\AppData\Local\Temp\claude\c--Agent-Coco"
           r"\7a2e7743-8713-4f95-9dd1-44dbccb04afa\scratchpad")
SC = json.load(open(os.path.join(SCRATCH, "strict_scores.json"), encoding="utf-8"))
QBQ = json.load(open(os.path.join(SCRATCH, "qbq.json"), encoding="utf-8"))
ROSTER = {r["code"]: r["name"] for r in
          json.load(open(os.path.join(SCRATCH, "rm_subs", "roster.json"), encoding="utf-8"))}

NAVY, BLUE, RED, GREEN, RULE, SOFT, MUTE, AMBER = (
    "#16202e", "#2f4fa2", "#a8442a", "#1b7f4d", "#d7dce4", "#f4f6fa", "#5b6472", "#8a6d1f")
PTS = {"Q1": 10, "Q2": 15, "Q3": 10, "Q4": 15, "Q5": 10,
       "Q6": 10, "Q7": 10, "Q8": 10, "Q9": 10, "Q10": None}

ASKED = {
"Q1": ("The 10 most important pieces of information",
 "Before taking action, identify the 10 most important pieces of information you would need. For "
 "each piece of information, explain: <b>why you need it</b>, <b>where you would get it</b>, and "
 "<b>what decision it would influence</b>."),
"Q2": ("Is Urban performing better than Rural?",
 "Based on the information currently available, can you conclude that the Urban region is "
 "performing better than Rural? Explain your reasoning. Your answer must distinguish between "
 "<b>adoption, implementation quality, teacher practice, student outcomes, infrastructure and data "
 "reliability</b>."),
"Q3": ("Three root causes of low Rural adoption",
 "Identify the three most likely root causes behind the rural region's low adoption. For each one, "
 "explain <b>how you would test whether your assumption is correct before introducing an "
 "intervention</b>."),
"Q4": ("Forced prioritisation",
 "You have only 100% coach capacity, but current demands require 115%. You must reduce the workload "
 "by at least 15%. What would you <b>Continue &rarr; Reduce &rarr; Pause &rarr; Delegate &rarr; "
 "Redesign</b>? You must justify every decision. (Senior management has separately asked for a 25% "
 "increase in classroom observation coverage.)"),
"Q5": ("&ldquo;Everything is a priority&rdquo;",
 "Senior management says: &ldquo;Everything is a priority.&rdquo; How would you respond? Your answer "
 "should demonstrate how an RM can <b>push back professionally without appearing resistant</b> to "
 "organisational priorities."),
"Q6": ("Coach leadership",
 "Create an individual management approach for each of four coaches - A: high productivity, poor "
 "collaboration; B: excellent teacher relationships, poor reporting discipline; C: low productivity "
 "but strong potential; D: strong technically, showing signs of burnout. For each, explain <b>what "
 "you would discuss, what support you would provide, what expectation you would set, how you would "
 "measure improvement, and when you would escalate</b>."),
"Q7": ("The LE experiment",
 "The LE team wants to start the LP experiment next Monday. You believe the coaches are already "
 "overloaded. Research warns that added coaching support would contaminate results. Would you: "
 "<b>A</b> approve as planned, <b>B</b> delay it, <b>C</b> reduce its scope, <b>D</b> redesign the "
 "implementation, or <b>E</b> run it in one region only? <b>Choose one</b> and justify it."),
"Q8": ("Stakeholder management plan",
 "Create a stakeholder management plan for the Programme Director, the AEO, the LE Team and the "
 "Coaches. For each stakeholder, explain <b>what they need from you, what you need from them, what "
 "information you will share, what you will negotiate, and what you will escalate</b>."),
"Q9": ("The 72 hours",
 "You have 72 hours to make the programme stable. Identify your top 5 actions and rank them 1&ndash;5. "
 "For each, explain <b>why it comes first, who will own it, what you will deprioritise, what risk it "
 "reduces, and what evidence will tell you it worked</b>."),
"Q10": ("Five-minute executive response",
 "&ldquo;If I give you no additional staff and no additional budget, what three things will you "
 "change in the next 90 days that will have the greatest impact on teacher practice and student "
 "learning?&rdquo; Prepare your five-minute executive response."),
}

below = sorted(((SC[c]["total"], c) for c in QBQ), reverse=True)


def para(t, sz=13, col="#232a35", mb=9, lh=1.62):
    return (f'<p style="margin:0 0 {mb}px;font:{sz}px/{lh} Georgia,serif;color:{col};'
            f'text-align:left;">{t}</p>')


# ------------------------------------------------------------------ PDF document
sections = ""
for idx, (total, code) in enumerate(below):
    v, q = SC[code], QBQ[code]
    marks = "  ".join(
        f'<span style="color:{MUTE};">{k}</span> '
        f'<span style="color:{RED if v["anchors"][k] <= 2 else "#232a35"};font-weight:700;">'
        f'{v["q"][k]:g}</span><span style="color:{MUTE};font-size:9px;">/{PTS[k]}</span>'
        for k in [f"Q{i}" for i in range(1, 10)])

    qblocks = ""
    for k in [f"Q{i}" for i in range(1, 11)]:
        title, asked = ASKED[k]
        mark = (f'<span style="float:right;font:700 13px Georgia,serif;'
                f'color:{RED if v["anchors"][k] <= 2 else NAVY};">{v["q"][k]:g}'
                f'<span style="font-weight:400;font-size:10px;color:{MUTE};">/{PTS[k]}</span>'
                f'</span>' if PTS[k] else
                f'<span style="float:right;font:11px Georgia,serif;color:{MUTE};">'
                f'not scored &middot; {v["q10band"]}</span>')
        qblocks += (
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin:0 0 15px;page-break-inside:avoid;"><tr><td>'
            f'<div style="font:700 13px Georgia,serif;color:{NAVY};border-bottom:1px solid {RULE};'
            f'padding-bottom:4px;margin-bottom:8px;">{k}. {title}{mark}</div>'
            f'<div style="background:{SOFT};border-left:2px solid {MUTE};padding:8px 11px;'
            f'margin:0 0 9px;font:11.5px/1.55 Georgia,serif;color:{MUTE};">'
            f'<b style="color:{NAVY};">What the question asked.</b> {asked}</div>'
            + para(f'<b style="color:{NAVY};">What {ROSTER[code].split()[0]} answered.</b> '
                   f'{q["qa"][k]["answered"]}')
            + f'<div style="border-left:2px solid {BLUE};background:#f6f8fc;padding:8px 11px;'
              f'margin:0 0 4px;font:12.5px/1.6 Georgia,serif;color:#232a35;">'
              f'<b style="color:{BLUE};">What would have made it stronger.</b> '
              f'{q["qa"][k]["better"]}</div>'
            + '</td></tr></table>')

    sections += (
        f'<div style="{"page-break-before:always;" if idx else ""}">'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
        f'style="margin:0 0 14px;"><tr><td style="background:{NAVY};padding:12px 15px;">'
        f'<div style="font:700 17px Georgia,serif;color:#fff;">{ROSTER[code]}'
        f'<span style="float:right;font-size:20px;">{total:g}<span style="font-size:12px;'
        f'font-weight:400;color:#aab4c4;">/100</span></span></div>'
        f'<div style="font:11px Georgia,serif;color:#aab4c4;margin-top:3px;">'
        f'{code} &middot; {marks}</div></td></tr></table>'
        + f'<div style="border-left:3px solid {AMBER};background:#fdfaf3;padding:10px 13px;'
          f'margin:0 0 16px;font:12.5px/1.6 Georgia,serif;color:#232a35;">'
          f'<b style="color:{AMBER};">Overall.</b> {q["overall"]}</div>'
        + qblocks + '</div>')

DETAIL = f"""<!doctype html><html><head><meta charset="utf-8">
<title>RM Case Study - Question-by-Question Analysis</title>
<style>@page{{size:A4;margin:13mm 12mm;}} body{{margin:0;}}</style></head>
<body style="background:#fff;">
<div style="font:700 20px Georgia,serif;color:{NAVY};margin:0 0 4px;">
  Regional Manager &mdash; question-by-question analysis</div>
<div style="font:12px Georgia,serif;color:{MUTE};margin:0 0 12px;">
  The eight submissions scoring below the published 70% bar &middot; 2 September 2026</div>
<div style="border:1px solid {RULE};background:{SOFT};padding:11px 13px;margin:0 0 18px;
     font:12px/1.6 Georgia,serif;color:#232a35;">
  Marks are against the case's own printed allocation of 100 points across Q1&ndash;Q9. Q10 carries
  no printed mark and is banded only. A figure in red is an anchor of 2 or below on the 0&ndash;5
  scale. Every submission was read in full and scored blind by code against a benchmark answer key
  written and reviewed before any submission was opened; names were attached only after all scores
  were final. Each candidate begins on a new page so a single section can be used on its own.</div>
{sections}
</body></html>"""

# ------------------------------------------------------------------ email body
lst = ""
for t, c in below:
    lst += (f'<tr><td style="padding:5px 6px;border-bottom:1px solid {RULE};'
            f'font:13px Georgia,serif;color:#232a35;">{ROSTER[c]}'
            f'<span style="color:{MUTE};font-size:11px;"> &nbsp;{c}</span></td>'
            f'<td style="padding:5px 6px;border-bottom:1px solid {RULE};font:700 13px Georgia,serif;'
            f'color:{RED};text-align:right;">{t:g}</td></tr>')

BODY = f"""
{para("Attached is the question-by-question analysis for the eight who fell below the line. For "
      "each of them, and for each of the ten questions, it sets out three things: what the "
      "question actually asked and what it was worth, what that person actually wrote, and what "
      "would have made it stronger. Each candidate starts on a new page, so you can lift one "
      "section out for an individual conversation without the other seven attached.", 14)}

<table role="presentation" width="100%" cellpadding="0" cellspacing="0"
       style="border-collapse:collapse;margin:14px 0;">{lst}</table>

{para("<b>Three things worth knowing before you use it.</b>", 14)}

{para("<b>First, none of these eight failed for lack of judgement.</b> They failed on execution "
      "against what each question specified. Five of the eight lost most of their Q4 marks to the "
      "same thing: no arithmetic at all on a fifteen-mark question whose entire purpose is that "
      "the capacity numbers close. Several lost marks on elements simply being absent rather than "
      "wrong: no source column in Q1, no escalation trigger in Q6, three of five columns in Q8, no "
      "deprioritisation in Q9. That is a coachable failure, not a capability one, and it is worth "
      "saying so if you speak to them.", 14)}

{para("<b>Second, the strengths in here are real and I would not bury them.</b> Javeria works out "
      "that ten schools per coach mathematically produces a two-week visit cycle, which reframes "
      "the AEO complaint from carelessness to workload design. Salman spots that the AEO's "
      "complaint is independent evidence to get the observation demand dropped, which is better "
      "than the benchmark answer. Toseef's four teachers who all look like low adoption for four "
      "different reasons is the clearest statement of the diagnostic principle anyone gave. Hafsa "
      "has a documented precedent for using the AEO to lift training completion. These are people "
      "worth developing.", 14)}

{para("<b>Third, two of the eight made a substantive error rather than an omission,</b> and the "
      "feedback treats them differently. Hafsa concluded that Urban performs better across both "
      "student groups, which is the reverse of what the data supports on the cohort that matters. "
      "Areej answered the central question with a plain yes without ever using the student subgroup "
      "data. Both are handled in the attachment as reasoning to correct rather than as effort to "
      "criticise.", 14)}

{para("If you want this reshaped as individual letters to each person rather than one internal "
      "document, say the word and I will draft them against the locked candidate-communication "
      "tone. These are colleagues who will keep working here, so the wording of what they receive "
      "matters more than usual.", 14)}
"""

html = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>RM Question-by-Question Analysis</title></head>
<body style="margin:0;padding:0;background:#eef1f6;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#eef1f6;">
<tr><td align="center" style="padding:20px 10px;">
<!--[if mso]><table role="presentation" width="660" cellpadding="0" cellspacing="0"><tr><td><![endif]-->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"
       style="max-width:660px;background:#fff;border:1px solid {RULE};">
<tr><td style="background:{NAVY};padding:19px 23px;">
  <div style="font:600 17px Georgia,serif;color:#fff;">
    Question-by-question analysis &mdash; the eight below the line</div>
  <div style="font:13px Georgia,serif;color:#aab4c4;margin-top:3px;">
    Regional Manager case study &middot; what was asked, what was answered, what would have been
    better &middot; 2 September 2026</div>
</td></tr>
<tr><td style="padding:23px;">{BODY}</td></tr>
<tr><td style="background:{SOFT};padding:13px 23px;border-top:1px solid {RULE};
        font:12px/1.6 Georgia,serif;color:{MUTE};">
  Analysis attached as PDF, one candidate per page. Marks are against the case's own allocation of
  100 points across Q1&ndash;Q9; Q10 is banded only.
</td></tr>
</table>
<!--[if mso]></td></tr></table><![endif]-->
</td></tr></table></body></html>"""


if __name__ == "__main__":
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
    pw = os.getenv("EMAIL_PASSWORD")
    if not pw:
        sys.exit("EMAIL_PASSWORD not set")

    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, "qbq.html")
    pdf = os.path.join(tmp, "qbq.pdf")
    open(src, "w", encoding="utf-8").write(DETAIL)
    chrome = next((c for c in [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"] if os.path.exists(c)), None)
    if not chrome:
        sys.exit("no Chrome/Edge found for PDF render")
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=15000", f"--print-to-pdf={pdf}", src],
                   check=True, capture_output=True, timeout=240)
    if not os.path.exists(pdf) or os.path.getsize(pdf) < 30000:
        sys.exit("PDF render failed or too small")
    print(f"PDF rendered: {os.path.getsize(pdf):,} bytes")

    msg = MIMEMultipart("mixed")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = ", ".join(RECIPIENTS)
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html, "html", "utf-8"))
    msg.attach(alt)
    att = MIMEApplication(open(pdf, "rb").read(), _subtype="pdf")
    att.add_header("Content-Disposition", "attachment",
                   filename="RM Case Study - Question-by-Question Analysis (below 70).pdf")
    msg.attach(att)

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(SENDER, pw)
        safe_sendmail(s, SENDER, RECIPIENTS, msg.as_string(), context="rm_below70_qbq")
    print(f"SENT -> {RECIPIENTS}")
    print(f"body {len(html):,} chars | detail {len(DETAIL):,} chars | {len(below)} candidates")
    shutil.rmtree(tmp, ignore_errors=True)
