"""
Email the two RM benchmark-comparison documents to Ayesha.

A - the 17 at or above 70 (invited to debrief 2026-09-07)
B - the 8 below 70

Documents are built by make_rm_benchmark_comparison.py. Internal report, Ayesha only.
Mobile-responsive per CLAUDE.md Rule 16.
"""
import importlib.util
import os
import smtplib
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.utils.safe_send import safe_sendmail  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "mk", os.path.join(os.path.dirname(__file__), "make_rm_benchmark_comparison.py"))
MK = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(MK)

SENDER = "ayesha.khan@taleemabad.com"
RECIPIENTS = ["ayesha.khan@taleemabad.com"]
SUBJECT = "RM case studies against the benchmark - two documents, above and below 70"

NAVY, BLUE, RED, GREEN, RULE, SOFT, MUTE = (
    "#16202e", "#2f4fa2", "#a8442a", "#1b7f4d", "#d7dce4", "#f4f6fa", "#5b6472")
QS = [f"Q{i}" for i in range(1, 10)]


def para(t, sz=14):
    return f'<p style="margin:0 0 13px;font:{sz}px/1.65 Georgia,serif;color:#232a35;">{t}</p>'


rows = ""
for q in QS:
    a = [MK.SC[c]["anchors"][q] for c in MK.SC]
    at, sh = sum(1 for x in a if x == 5), sum(1 for x in a if x <= 2)
    mean = sum(MK.SC[c]["q"][q] for c in MK.SC) / 25
    pct = mean / MK.PTS[q] * 100
    col = RED if pct < 70 else ("#232a35" if pct < 82 else GREEN)
    rows += (f'<tr>'
             f'<td style="padding:5px 6px 5px 0;border-bottom:1px solid {RULE};'
             f'font:12px Georgia,serif;color:#232a35;">{q} &nbsp;'
             f'<span style="color:{MUTE};">{MK.BENCH[q][0]}</span></td>'
             f'<td style="padding:5px 6px;border-bottom:1px solid {RULE};font:700 12px Georgia,serif;'
             f'color:{col};text-align:right;">{pct:.0f}%</td>'
             f'<td style="padding:5px 6px;border-bottom:1px solid {RULE};font:12px Georgia,serif;'
             f'color:{MUTE};text-align:right;">{at}</td>'
             f'<td style="padding:5px 0 5px 6px;border-bottom:1px solid {RULE};font:12px Georgia,serif;'
             f'color:{RED if sh else MUTE};text-align:right;">{sh}</td></tr>')

BODY = f"""
{para("Two documents attached, split at the 70 line as you asked. Each one carries, for every "
      "question, what the benchmark required, what each submission actually did, and the distance "
      "between the two. Your Revision 2 changes are flagged <b>REV 2</b> wherever they appear, so "
      "it is visible which requirements were added in your QA round rather than in the first draft "
      "of the key: the <b>Where from</b> column in Q1, the reframing of Q2 away from a flat no, the "
      "evidence-to-intervention rule in Q3, the corrected Q4 arithmetic together with the rule that "
      "<b>Very High activities are never paused</b>, and the fifth column restored in Q8.")}

{para("<b>The comparison says something the totals do not.</b> Two questions carry almost all the "
      "discrimination in this round, and they are the two worth most marks:")}

<table role="presentation" width="100%" cellpadding="0" cellspacing="0"
       style="border-collapse:collapse;margin:6px 0 16px;">
<tr><td style="padding:0 6px 4px 0;font:700 10px Georgia,serif;color:{MUTE};">QUESTION</td>
<td style="padding:0 6px 4px;font:700 10px Georgia,serif;color:{MUTE};text-align:right;">MEAN</td>
<td style="padding:0 6px 4px;font:700 10px Georgia,serif;color:{MUTE};text-align:right;">AT KEY</td>
<td style="padding:0 0 4px 6px;font:700 10px Georgia,serif;color:{MUTE};text-align:right;">SHORT</td></tr>
{rows}</table>
{para("<span style='color:" + MUTE + ";font-size:12px;'>Mean as a percentage of that question's "
      "marks, across all 25. AT KEY = reached the benchmark. SHORT = anchor of 2 or below.</span>", 12)}

{para("<b>Q2 and Q4 sit at 62%. Everything else sits between 78 and 85%.</b> On the seven other "
      "questions the pool is genuinely capable: nobody fell short on the root-cause testing in Q3, "
      "the professional pushback in Q5, the experiment decision in Q7 or the 72 hours in Q9. The "
      "round was decided almost entirely on two things.")}

{para("<b>Q2 - only two of twenty-five reached the key.</b> Seventeen of the twenty-five read the "
      "below-grade-level figures as shares of a population rather than as pass rates within each "
      "subgroup. Urban's 34 and 75 sum to 109, so they cannot be shares, and the correct reading "
      "reverses the finding: Rural passes 49% of the students who started behind against Urban's "
      "34%. Two people concluded outright that Urban was better on the strength of the misreading. "
      "This is the single most consequential thing the case tested and the pool overwhelmingly "
      "missed it.")}

{para("<b>Q4 - ten of twenty-five fell short, six showed no arithmetic at all.</b> The question "
      "supplies seven activities with percentages precisely so the numbers can be shown to close, "
      "and a quarter of the pool answered it with verbs and no figures. Only a handful priced the "
      "+25% observation demand, which is what turns a 15-point problem into a 21-point one.")}

{para("<b>For the debriefs specifically.</b> In the seventeen document, the block headed <i>Against "
      "the benchmark</i> under each question is where that person's thinking stops. That is the "
      "natural probe. Where it reads <i>Met the benchmark</i>, there is nothing left to test on that "
      "question and the time is better spent elsewhere. Even the two at 100 have something recorded "
      "against them, and both are noted.")}

{para("Worth saying plainly: these documents are my read, and the marking is a single unmoderated "
      "pass. If a debrief contradicts what is written here, the debrief is the better evidence.")}
"""

html = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>RM case studies against the benchmark</title></head>
<body style="margin:0;padding:0;background:#eef1f6;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#eef1f6;">
<tr><td align="center" style="padding:20px 10px;">
<!--[if mso]><table role="presentation" width="680" cellpadding="0" cellspacing="0"><tr><td><![endif]-->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"
       style="max-width:680px;background:#fff;border:1px solid {RULE};">
<tr><td style="background:{NAVY};padding:19px 23px;">
  <div style="font:600 17px Georgia,serif;color:#fff;">
    Case studies against the benchmark</div>
  <div style="font:13px Georgia,serif;color:#aab4c4;margin-top:3px;">
    Regional Manager &middot; question by question, all 25 &middot; two documents, split at 70</div>
</td></tr>
<tr><td style="padding:23px;">{BODY}</td></tr>
<tr><td style="background:{SOFT};padding:13px 23px;border-top:1px solid {RULE};
        font:12px/1.6 Georgia,serif;color:{MUTE};">
  Two PDFs attached, one candidate per page in each. Benchmark requirements are Revision 2 of the
  answer key, written and QA'd before any submission was opened.
</td></tr>
</table>
<!--[if mso]></td></tr></table><![endif]-->
</td></tr></table></body></html>"""


if __name__ == "__main__":
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
    pw = os.getenv("EMAIL_PASSWORD")
    if not pw:
        sys.exit("EMAIL_PASSWORD not set")

    base = os.path.join(MK.SCRATCH, "bench_cmp")
    files = [(f"RM Case Study vs Benchmark - {n} ({t}).pdf",
              os.path.join(base, f"RM Case Study vs Benchmark - {k}.pdf"))
             for k, n, t in (("above70", "above 70", f"{len(MK.ABOVE)} invited to debrief"),
                             ("below70", "below 70", f"{len(MK.BELOW)} candidates"))]
    for _, p in files:
        if not os.path.exists(p) or os.path.getsize(p) < 50000:
            sys.exit(f"missing or too small: {p}. Run make_rm_benchmark_comparison.py first.")

    msg = MIMEMultipart("mixed")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = ", ".join(RECIPIENTS)
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html, "html", "utf-8"))
    msg.attach(alt)
    for name, path in files:
        att = MIMEApplication(open(path, "rb").read(), _subtype="pdf")
        att.add_header("Content-Disposition", "attachment", filename=name)
        msg.attach(att)
        print(f"attached: {name} ({os.path.getsize(path):,} bytes)")

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(SENDER, pw)
        safe_sendmail(s, SENDER, RECIPIENTS, msg.as_string(), context="rm_benchmark_comparison")
    print(f"SENT -> {RECIPIENTS} | body {len(html):,} chars")
