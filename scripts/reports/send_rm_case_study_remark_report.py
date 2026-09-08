"""
RM (Regional Manager) internal case study - FULL STRICT RE-MARK of all 25 submissions.

Ayesha, 2026-09-02: "why are they all above 70 / were they actually that good" -> then
"read all 25 line by line, I don't think everybody can pass that 70% line."

She was right. The first pass never used the bottom half of the scale: on four of the nine
questions the WORST answer of 25 still scored 70%. This report leads with that diagnosis,
then gives the re-mark.

WHAT CHANGED
  - Same benchmark (Revision 2, QA'd by Ayesha before any submission was opened).
  - Anchors converted on the FULL 0-5 scale (5=100%, 4=80%, 3=60%, 2=40%, 1=20%, 0=0),
    not the 1-5 floor used first time.
  - Mechanical caps applied from the benchmark's own text, not by feel: factual error against
    the case data, no arithmetic on Q4, a Very High activity paused, a required structural
    element absent, refusing to choose on Q7.
  - All 25 re-read in full and re-scored from the anonymised files by code.

RESULT: mean 88.3 -> 75.0, spread 30 -> 44 points, 8 of 25 now below the 70% line.

Internal report email to Ayesha only. Mobile-responsive per CLAUDE.md Rule 16.
"""

import json
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.utils.safe_send import safe_sendmail  # noqa: E402

SENDER = "ayesha.khan@taleemabad.com"
RECIPIENTS = ["ayesha.khan@taleemabad.com"]
SUBJECT = "RM Case Study - full re-mark of all 25, and why the first pass was wrong"

SCRATCH = (r"C:\Users\Dell\AppData\Local\Temp\claude\c--Agent-Coco"
           r"\7a2e7743-8713-4f95-9dd1-44dbccb04afa\scratchpad")
NEW = json.load(open(os.path.join(SCRATCH, "strict_scores.json"), encoding="utf-8"))
OLD = json.load(open(os.path.join(SCRATCH, "scores.json"), encoding="utf-8"))
ROSTER = {r["code"]: r["name"] for r in
          json.load(open(os.path.join(SCRATCH, "rm_subs", "roster.json"), encoding="utf-8"))}

NAVY, BLUE, RED, GREEN, RULE, SOFT, MUTE = (
    "#16202e", "#2f4fa2", "#a8442a", "#1b7f4d", "#d7dce4", "#f4f6fa", "#5b6472")
QS = [f"Q{i}" for i in range(1, 10)]
QLAB = {"Q1": "Info needs", "Q2": "Urban v Rural", "Q3": "Root causes", "Q4": "Prioritisation",
        "Q5": "Everything is a priority", "Q6": "Coach leadership", "Q7": "Experiment",
        "Q8": "Stakeholders", "Q9": "72 hours"}
PTS = {"Q1": 10, "Q2": 15, "Q3": 10, "Q4": 15, "Q5": 10, "Q6": 10, "Q7": 10, "Q8": 10, "Q9": 10}

rows = sorted(((v["total"], c) for c, v in NEW.items()), reverse=True)


def h(t, sz=15, col=NAVY, mt=26, mb=8):
    return (f'<h2 style="margin:{mt}px 0 {mb}px;font:600 {sz}px/1.3 Georgia,serif;'
            f'color:{col};">{t}</h2>')


def p(t, col="#232a35", sz=14):
    return (f'<p style="margin:0 0 12px;font:{sz}px/1.65 Georgia,serif;color:{col};'
            f'text-align:left;">{t}</p>')


def box(t, bg=SOFT, bd=BLUE):
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin:14px 0;"><tr><td style="background:{bg};border-left:3px solid {bd};'
            f'padding:12px 14px;font:14px/1.6 Georgia,serif;color:#232a35;">{t}</td></tr></table>')


# ---------------------------------------------------------------- diagnosis table
diag = [("Q1", 40), ("Q2", 40), ("Q3", 75), ("Q4", 60), ("Q5", 70),
        ("Q6", 60), ("Q7", 70), ("Q8", 60), ("Q9", 70)]
dg = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
      f'style="border-collapse:collapse;margin:8px 0 4px;">'
      f'<tr><td style="padding:6px 8px;border-bottom:2px solid {RULE};font:600 12px Georgia,serif;'
      f'color:{MUTE};">QUESTION</td>'
      f'<td style="padding:6px 8px;border-bottom:2px solid {RULE};font:600 12px Georgia,serif;'
      f'color:{MUTE};text-align:right;">LOWEST MARK I GAVE, OF 25</td></tr>')
for q, low in diag:
    col = RED if low >= 70 else "#232a35"
    w = "600" if low >= 70 else "400"
    dg += (f'<tr><td style="padding:6px 8px;border-bottom:1px solid {RULE};'
           f'font:13px Georgia,serif;color:#232a35;">{q} &nbsp;{QLAB[q]}</td>'
           f'<td style="padding:6px 8px;border-bottom:1px solid {RULE};font:{w} 13px Georgia,serif;'
           f'color:{col};text-align:right;">{low}%</td></tr>')
dg += "</table>"

# ---------------------------------------------------------------- results table
res = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
       f'style="border-collapse:collapse;margin:10px 0;">'
       f'<tr style="background:{NAVY};">'
       f'<td style="padding:7px 6px;font:600 11px Georgia,serif;color:#fff;">#</td>'
       f'<td style="padding:7px 6px;font:600 11px Georgia,serif;color:#fff;">NAME</td>'
       f'<td style="padding:7px 6px;font:600 11px Georgia,serif;color:#fff;text-align:right;">NOW</td>'
       f'<td style="padding:7px 6px;font:600 11px Georgia,serif;color:#fff;text-align:right;">WAS</td>'
       f'<td style="padding:7px 6px;font:600 11px Georgia,serif;color:#fff;text-align:right;">&Delta;</td>'
       f'</tr>')
for i, (t, c) in enumerate(rows, 1):
    o = OLD[c]["total"]
    d = t - o
    bg = "#ffffff" if i % 2 else SOFT
    if t < 70:
        tc, tw = RED, "700"
    elif t >= 90:
        tc, tw = GREEN, "700"
    else:
        tc, tw = "#232a35", "600"
    res += (f'<tr style="background:{bg};">'
            f'<td style="padding:6px;border-bottom:1px solid {RULE};font:12px Georgia,serif;'
            f'color:{MUTE};">{i}</td>'
            f'<td style="padding:6px;border-bottom:1px solid {RULE};font:13px Georgia,serif;'
            f'color:#232a35;">{ROSTER[c]}<span style="color:{MUTE};font-size:11px;"> &nbsp;{c}</span></td>'
            f'<td style="padding:6px;border-bottom:1px solid {RULE};font:{tw} 13px Georgia,serif;'
            f'color:{tc};text-align:right;">{t:.0f}</td>'
            f'<td style="padding:6px;border-bottom:1px solid {RULE};font:12px Georgia,serif;'
            f'color:{MUTE};text-align:right;">{o:.0f}</td>'
            f'<td style="padding:6px;border-bottom:1px solid {RULE};font:12px Georgia,serif;'
            f'color:{RED if d < 0 else MUTE};text-align:right;">{d:+.0f}</td></tr>')
res += "</table>"

# ---------------------------------------------------------------- per candidate
cards = ""
for t, c in rows:
    v = NEW[c]
    per = " &nbsp;".join(
        f'<span style="color:{MUTE};">{q}</span> '
        f'<span style="color:{RED if v["anchors"][q] <= 2 else "#232a35"};font-weight:600;">'
        f'{v["q"][q]:g}</span><span style="color:{MUTE};font-size:10px;">/{PTS[q]}</span>'
        for q in QS)
    cards += (
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
        f'style="margin:0 0 18px;border:1px solid {RULE};border-top:3px solid '
        f'{RED if t < 70 else (GREEN if t >= 90 else BLUE)};">'
        f'<tr><td style="padding:13px 15px;">'
        f'<div style="font:600 15px Georgia,serif;color:{NAVY};margin-bottom:2px;">'
        f'{ROSTER[c]} <span style="color:{MUTE};font-weight:400;font-size:12px;">{c}</span>'
        f'<span style="float:right;font-size:17px;color:'
        f'{RED if t < 70 else (GREEN if t >= 90 else NAVY)};">{t:g}</span></div>'
        f'<div style="font:11px/1.9 Georgia,serif;margin:8px 0 10px;">{per}</div>'
        f'<div style="font:13px/1.6 Georgia,serif;color:#232a35;">{v["notes"]}</div>'
        f'<div style="font:600 11px Georgia,serif;color:{GREEN};margin:12px 0 3px;">STRONG</div>'
        + "".join(f'<div style="font:12px/1.5 Georgia,serif;color:#3a4250;padding-left:12px;'
                  f'margin-bottom:3px;">&bull; {s}</div>' for s in v["strengths"][:4])
        + f'<div style="font:600 11px Georgia,serif;color:{RED};margin:11px 0 3px;">'
          f'MISSING OR WRONG</div>'
        + "".join(f'<div style="font:12px/1.5 Georgia,serif;color:#3a4250;padding-left:12px;'
                  f'margin-bottom:3px;">&bull; {g}</div>' for g in v["gaps"][:4])
        + "</td></tr></table>")

body = f"""
{h("You were right. They were not all that good.", 19, NAVY, 0, 10)}
{p("I re-read all twenty-five line by line against the same benchmark and re-marked them "
   "on a real scale. <strong>Eight of them now fall below the 70% line.</strong> The mean drops "
   "from 88.3 to 75.0 and the spread widens from 30 points to 44.")}

{h("Why the first pass put everyone above 70")}
{p("It was my marking, not the pool. Across twenty-five submissions I never once used the "
   "bottom half of the scale. On four of the nine questions the <em>worst</em> answer of the "
   "twenty-five still earned 70%:")}
{dg}
{p("A question where the weakest of twenty-five people scores 70% is not measuring anything. "
   "Three things caused it.", MUTE, 13)}
{box("<strong>1. My anchors had a floor of 20%, not zero.</strong> A submission that answered "
     "the wrong question still banked a fifth of every item. Nine questions of guaranteed floor "
     "is roughly twenty points of free base.<br><br>"
     "<strong>2. I credited structure and method over correctness.</strong> I rewarded a "
     "well-organised answer built on a misreading. I had also written into the benchmark that a "
     "well-defended different conclusion scores as high as agreement, which is right in principle "
     "but on Q2 one of the readings is arithmetically impossible, and my own rule let it score well.<br><br>"
     "<strong>3. I never applied the benchmark's own caps.</strong> It says plainly that no "
     "arithmetic on Q4 is a bottom-anchor answer, and that a factual error against the case data "
     "is serious. I treated both as deductions of a mark or two.")}
{p("The proof is in one number. I told you only six of twenty-five read the student data "
   "correctly, yet Q2 averaged 85% and the data question's floor was 11 out of 15. Getting the "
   "central analytic task <em>wrong</em> cost about two marks in fifteen. That is where the "
   "inflation lived.")}

{h("What I changed")}
{p("Same benchmark, same submissions, same blind codes. Three changes to the marking:")}
{p("&bull; <strong>The full 0-5 scale</strong>, converted pro rata, with zero available.<br>"
   "&bull; <strong>Mechanical caps taken from the benchmark's own text</strong>, applied by rule "
   "rather than by feel: a factual error against the case data, no arithmetic on Q4, pausing a "
   "Very High activity, a required structural element absent across an answer, refusing to choose "
   "on Q7.<br>"
   "&bull; <strong>Every required element ticked individually</strong> rather than judging an "
   "answer as a whole. That is what surfaced the missing escalation triggers, the absent source "
   "columns and the stakeholder grids running three columns instead of five.")}
{box("<strong>Q4 was the single biggest correction.</strong> It is fifteen marks and its whole "
     "point is that the numbers must close. Six submissions contain no arithmetic at all - no "
     "after-figures, no total, no quantified saving. Under the old marking they averaged in the "
     "high seventies on it. Two more misquote the case's own baseline figures. Only four price "
     "the +25% observation demand correctly and fund it.", "#fdf6f4", RED)}

{h("The re-mark")}
{res}
{p(f"Mean 75.0, median 72.0, range 56 to 100. Red is below the published line; green is 90 or "
   f"above. Codes were assigned by a hash of the name, so code order carries no information, and "
   f"names were attached only after every score was final.", MUTE, 12)}

{h("What this does and does not settle")}
{p("<strong>It settles the bar.</strong> Seventeen clear 70%, eight do not. The line now does "
   "work, and you can apply it as published without raising it after the fact.")}
{p("<strong>It does not settle the shortlist.</strong> Seventeen is still too many. The natural "
   "break is at the top: <strong>five candidates score 89 or above</strong> - Ateeb, Danish, Moiz, "
   "Warda, Meerab - and each of them did something specific the benchmark treats as a "
   "discriminator. Below that, 85 to 70 is a continuous slope with no honest gap in it.")}
{box("<strong>Two things you should know before you use this.</strong><br><br>"
     "<strong>RM-09 (Danish) and RM-15 (Meerab) warrant a look.</strong> Overall text overlap is "
     "low, but the distinctive phrases they share sit in matching positions and their derived "
     "figures are identical - both compute the real gap as 21 points not 15, both give 91% during "
     "the pause and 98% at steady state, both rank the 72 hours the same way. Meerab's submission "
     "reads as a condensed version of Danish's analysis. I scored both as written and the overlap "
     "changed neither score. It is your call whether to look further.<br><br>"
     "<strong>RM-23 (Ashas) quotes internal Slack and RUMI data</strong> with channel names and "
     "dates. It is accurate, clearly sourced, and I credited it as evidence. Whether that is "
     "appropriate use of internal data in an application is a judgement for you, not a scoring "
     "matter.", "#fdfaf3", "#b8860b")}

{h("Still open")}
{p("&bull; <strong>Q10 carries no points</strong> and is in no total - banded only. Nineteen "
   "Standout, five Meets, one Below.<br>"
   "&bull; <strong>The +25% denominator.</strong> Ateeb argues it runs through HITL and DC "
   "together, giving 11 points and 126% demand. Danish, Meerab and Moiz price it on HITL alone "
   "at about 6 points. Both are defensible; the benchmark leaves it open. It did not change the "
   "ranking, but a second marker needs one answer.<br>"
   "&bull; <strong>Shafaq Tahir's resume</strong> is still missing.")}
{p("Full per-candidate detail is below. Happy to walk through any of the eight that fell below "
   "the line, or to have a second reader re-score a sample to check me - given I got the "
   "calibration wrong the first time, that is worth doing.")}

"""

html = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>RM Case Study Re-mark</title></head>
<body style="margin:0;padding:0;background:#eef1f6;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#eef1f6;">
<tr><td align="center" style="padding:20px 10px;">
<!--[if mso]><table role="presentation" width="700" cellpadding="0" cellspacing="0"><tr><td><![endif]-->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"
       style="max-width:700px;background:#ffffff;border:1px solid {RULE};">
<tr><td style="background:{NAVY};padding:20px 24px;">
  <div style="font:600 17px Georgia,serif;color:#ffffff;">Regional Manager &mdash; Case Study Re-mark</div>
  <div style="font:13px Georgia,serif;color:#aab4c4;margin-top:3px;">
    All 25 submissions &middot; strict re-mark against benchmark Rev 2 &middot; 2 September 2026</div>
</td></tr>
<tr><td style="padding:24px;">{body}</td></tr>
<tr><td style="background:{SOFT};padding:14px 24px;border-top:1px solid {RULE};
        font:12px/1.6 Georgia,serif;color:{MUTE};">
  Benchmark written and QA'd before any submission was opened. All 25 read in full and scored
  blind by code against the case's printed allocation of 100 points across Q1&ndash;Q9.
</td></tr>
</table>
<!--[if mso]></td></tr></table><![endif]-->
</td></tr></table></body></html>"""

DETAIL = f"""<!doctype html><html><head><meta charset="utf-8">
<title>RM Case Study - Candidate Detail</title>
<style>@page{{size:A4;margin:14mm 13mm;}} body{{margin:0;}}</style></head>
<body style="background:#ffffff;">
<div style="font:600 19px Georgia,serif;color:{NAVY};margin:0 0 3px;">
  Regional Manager &mdash; Case Study Re-mark: candidate detail</div>
<div style="font:12px Georgia,serif;color:{MUTE};margin:0 0 4px;">
  All 25, ranked. Strict re-mark against benchmark Revision 2 &middot; 2 September 2026</div>
<div style="font:12px/1.6 Georgia,serif;color:{MUTE};margin:0 0 16px;">
  Per-question marks are shown against the case's own allocation. A figure in red is an anchor of
  2 or below on the 0&ndash;5 scale. Red rule = below the 70% line; green = 90 or above.</div>
{cards}
</body></html>"""

if __name__ == "__main__":
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
    pw = os.getenv("EMAIL_PASSWORD")
    if not pw:
        sys.exit("EMAIL_PASSWORD not set")

    import subprocess, tempfile, shutil
    from email.mime.application import MIMEApplication

    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, "detail.html")
    pdf = os.path.join(tmp, "RM_Case_Study_Candidate_Detail.pdf")
    open(src, "w", encoding="utf-8").write(DETAIL)
    chrome = next((c for c in [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"] if os.path.exists(c)), None)
    if not chrome:
        sys.exit("no Chrome/Edge found for PDF render")
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=12000",
                    f"--print-to-pdf={pdf}", src], check=True, capture_output=True, timeout=180)
    if not os.path.exists(pdf) or os.path.getsize(pdf) < 20000:
        sys.exit(f"PDF render failed or too small: {os.path.getsize(pdf) if os.path.exists(pdf) else 0}")
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
                   filename="RM Case Study - Candidate Detail (all 25).pdf")
    msg.attach(att)

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(SENDER, pw)
        safe_sendmail(s, SENDER, RECIPIENTS, msg.as_string(), context="rm_case_study_remark")
    print(f"SENT -> {RECIPIENTS}")
    print(f"subject: {SUBJECT}")
    print(f"body: {len(html):,} chars | detail pdf attached | {len(rows)} candidates")
    shutil.rmtree(tmp, ignore_errors=True)
