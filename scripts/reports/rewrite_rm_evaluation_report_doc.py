"""
Rewrite the RM evaluation report Google Doc IN PLACE with the STRICT re-mark.

Ayesha, 2026-09-08, twice: the linked evaluation report is wrong. She is right, and swapping the
link was not the fix. The Doc itself carries the superseded first pass.

  Doc 1suHQOhKzAjjBe26uPjSpHkl0EoSVBGqkhtReqjs8QMc, titled "RM Case Study - Evaluation Report
  (all 25)", opens with "Mean 88.3 | Range 70-100" and "the bar no longer separates anyone".
  Its results table shows Javeria 91.5, Khadija 86, Sana 83, Hafsa 80, Salman 74.5, Rida 73,
  Areej 70. Those are FIRST-PASS numbers. The live result is the strict re-mark: mean 75.0,
  range 56-100, 8 below the 70% bar.

  docs/case_studies/rm_evaluation_report_2026_09_02.md, the markdown the Doc was generated
  from, carries the same superseded numbers and is rewritten here too.

WHY REWRITE IN PLACE rather than link a different file: this Doc's URL has been shared. A new
file leaves the wrong numbers live at a link people already hold. Same file ID, corrected
content, so every existing link now resolves to the truth.

Source of truth: output/rm_marking/strict_scores.json (anchors, per-question marks, caps,
notes, strengths, gaps) - the same data behind the marked-scripts sheet and the individual
candidate workbooks, so all four artefacts now agree.
"""

import io
import json
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build as gbuild
from googleapiclient.http import MediaIoBaseUpload

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TOKEN = os.path.join(ROOT, ".claude", "config", "token_sheets_broad.json")
KEEP = os.path.join(ROOT, "output", "rm_marking")
DOC_ID = "1suHQOhKzAjjBe26uPjSpHkl0EoSVBGqkhtReqjs8QMc"
MD = os.path.join(ROOT, "docs", "case_studies", "rm_evaluation_report_2026_09_02.md")

PTS = {"Q1": 10, "Q2": 15, "Q3": 10, "Q4": 15, "Q5": 10,
       "Q6": 10, "Q7": 10, "Q8": 10, "Q9": 10}
CAP_TEXT = {
    "C1": "Q2 below-grade-level figures read as composition shares",
    "C1a": "Q2 capped at 2, misreading drove the verdict",
    "C1b": "Q2 dropped one anchor, verdict held on the other axes",
    "C2": "Q4 capped at 1, no arithmetic shown",
    "C3": "Q4 capped at 2, a Very High activity paused or dropped",
    "C4": "Q4 capped at 3, cut 15pp and never priced the +25%",
    "C5": "Q7 capped at 2, refused to choose",
    "C6": "capped at 3, a required structural element absent",
    "C7": "not attempted",
}
BAR = 70


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_html(strict, roster, below):
    order = sorted(strict, key=lambda c: -strict[c]["total"])
    rows = []
    for i, cd in enumerate(order, 1):
        r = strict[cd]
        nm = roster[cd]["name"]
        met = cd not in below
        bg = "#eef7f1" if met else "#fff5f5"
        rows.append(
            f'<tr style="background:{bg}"><td>{i}</td><td>{cd}</td><td>{esc(nm)}</td>'
            f'<td align="center"><b>{r["total"]:.0f}</b></td>'
            f'<td align="center">{esc(r.get("q10band",""))}</td>'
            f'<td>{"Met the 70% benchmark" if met else "Below the 70% benchmark"}</td></tr>')

    detail = []
    for cd in order:
        r = strict[cd]
        nm = roster[cd]["name"]
        met = cd not in below
        marks = "  ".join(f'{q} {r["q"][q]:.0f}/{PTS[q]}' for q in PTS)
        caps = ", ".join(CAP_TEXT.get(c, c) for c in r["caps"]) or "none"
        s_items = "".join(f"<li>{esc(x)}</li>" for x in (r.get("strengths") or []))
        g_items = "".join(f"<li>{esc(x)}</li>" for x in (r.get("gaps") or []))
        detail.append(
            f'<h3>{esc(nm)} &mdash; {cd} &mdash; {r["total"]:.0f}/100 '
            f'({"met the benchmark" if met else "below the benchmark"})</h3>'
            f'<p style="font-family:monospace;font-size:9pt">{marks}</p>'
            f'<p>{esc(r["notes"])}</p>'
            f'<p><b>What was strong</b></p><ul>{s_items or "<li>-</li>"}</ul>'
            f'<p><b>What was missing</b></p><ul>{g_items or "<li>-</li>"}</ul>'
            f'<p><i>Marking rules applied: {esc(caps)}</i></p>')

    n_below = len(below)
    mean = sum(v["total"] for v in strict.values()) / len(strict)
    lo = min(v["total"] for v in strict.values())
    hi = max(v["total"] for v in strict.values())
    return f"""<html><body style="font-family:Georgia,serif">
<h1>Regional Manager &mdash; Case Study Evaluation</h1>
<p><b>All 25 internal submissions, strict re-mark against benchmark Revision 2</b><br>
Mean {mean:.1f} &nbsp;|&nbsp; Range {lo:.0f}&ndash;{hi:.0f} &nbsp;|&nbsp;
<b>{n_below} of 25 below the 70% benchmark</b> &nbsp;|&nbsp; Updated 8 September 2026</p>

<h2>What changed, and why this version replaces the first one</h2>
<p>An earlier version of this report put all 25 submissions above the 70% benchmark, with a mean
of 88.3 and a lowest score of exactly 70.0, and concluded that the bar no longer separated
anyone. That conclusion was an artefact of the marking scale, not a finding about the pool. The
scale used anchors of 5, 3 and 1, which puts a floor of 20% under every question and never uses
the bottom half of the range. On four of the nine questions the weakest of 25 answers still
scored 60% or more.</p>
<p>This version is a strict re-mark of the same 25 submissions against the same benchmark, using
the full 0 to 5 scale with a real zero and applying the benchmark's own marking caps
mechanically rather than by feel. The mean falls from 88.3 to {mean:.1f}, the range widens from
30 points to {hi - lo:.0f}, and <b>{n_below} submissions fall below the 70% benchmark</b>.
Nothing about the benchmark changed, and no submission was re-read for a different purpose.</p>
<p>The 70% figure was published to staff in the announcement, so it is a commitment and has been
applied as written rather than adjusted after seeing the pool.</p>

<h2>Results</h2>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;font-size:10pt">
<tr style="background:#1a2b4c;color:#ffffff"><th>#</th><th>Code</th><th>Name</th>
<th>Score /100</th><th>Q10 band</th><th>Outcome</th></tr>
{''.join(rows)}
</table>
<p style="font-size:9pt">Question 10 carries no printed point value in the case, so it is banded
and described but is not part of any total. Every other question converts its 0 to 5 band
pro-rata to the point value the case prints: Q1 10, Q2 15, Q3 10, Q4 15, Q5 10, Q6 10, Q7 10,
Q8 10, Q9 10.</p>

<h2>Candidate by candidate</h2>
{''.join(detail)}

<h2>Method and limits</h2>
<p>The benchmark answer key was written and reviewed before any submission was opened, and
submissions were anonymised before marking, so each was read on the answer alone. Marks convert
each question's 0 to 5 band to the case's own printed allocation. Marking caps come from the
benchmark's text and were applied mechanically.</p>
<p>Two limits worth stating. Candidates self-identify through the substance of their answers,
their region, their tenure, their own experiments, so anonymity is partial by design; stripping
that would have destroyed the evidence that makes a strong answer strong. And this is a single
unmoderated marker. A second reader independently re-scoring the candidates clustered just above
and just below the line would be a cheap check on the ranking.</p>
</body></html>"""


def main():
    strict = json.load(open(os.path.join(KEEP, "strict_scores.json"), encoding="utf-8"))
    roster = json.load(open(os.path.join(KEEP, "roster.json"), encoding="utf-8"))
    below = set(json.load(open(os.path.join(KEEP, "qbq.json"), encoding="utf-8")))

    assert len(strict) == 25, f"expected 25 scored, got {len(strict)}"
    assert len(below) == 8, f"expected 8 below the bar, got {len(below)}"
    for cd in below:
        assert strict[cd]["total"] < BAR, f"{cd} listed below the bar but scored {strict[cd]['total']}"
    for cd in set(strict) - below:
        assert strict[cd]["total"] >= BAR, f"{cd} not listed below the bar but scored {strict[cd]['total']}"

    html = build_html(strict, roster, below)

    c = Credentials.from_authorized_user_file(TOKEN)
    if c.expired and c.refresh_token:
        c.refresh(Request())
    drive = gbuild("drive", "v3", credentials=c)

    before = drive.files().get(fileId=DOC_ID, fields="name,modifiedTime").execute()
    drive.files().update(
        fileId=DOC_ID,
        media_body=MediaIoBaseUpload(io.BytesIO(html.encode("utf-8")),
                                     mimetype="text/html", resumable=False),
        body={"mimeType": "application/vnd.google-apps.document"}).execute()
    after = drive.files().get(fileId=DOC_ID, fields="name,modifiedTime").execute()
    print(f"Doc rewritten in place: {before['name']}")
    print(f"  {before['modifiedTime']} -> {after['modifiedTime']}")

    # verify by reading it back
    txt = drive.files().export(fileId=DOC_ID, mimeType="text/plain").execute().decode(
        "utf-8", "replace")
    checks = {
        "no 88.3 headline": "Mean 88.3" not in txt,
        "states 8 below the bar": "8 of 25 below the 70% benchmark" in txt,
        "Rida Abbas at 56": "56" in txt and "Rida Abbas" in txt,
        "Areej Noshad present": "Areej Noshad" in txt,
        "old claim removed": "the bar no longer separates anyone" not in txt,
    }
    for k, v in checks.items():
        print(f"  {'OK ' if v else 'FAIL'} {k}")
    if not all(checks.values()):
        raise SystemExit("verification failed")

    # keep the repo markdown from staying the stale source
    with open(MD, "w", encoding="utf-8") as fh:
        fh.write("<!-- SUPERSEDED. The live evaluation report is the strict re-mark, held as a\n"
                 "Google Doc and rewritten in place by\n"
                 "scripts/reports/rewrite_rm_evaluation_report_doc.py:\n"
                 f"https://docs.google.com/document/d/{DOC_ID}/edit\n"
                 "This file previously carried the first-pass numbers (mean 88.3, nobody below\n"
                 "70) and is kept only so the history is not lost. Do not cite it. -->\n\n"
                 "# Regional Manager - Case Study Evaluation (SUPERSEDED first pass)\n\n"
                 "The live result is the strict re-mark: mean 75.0, range 56-100, 8 of 25 below\n"
                 "the published 70% benchmark. See the Google Doc linked above, the marked\n"
                 "scripts sheet, and output/rm_marking/strict_scores.json.\n")
    print(f"  repo markdown marked superseded: {os.path.relpath(MD, ROOT)}")
    print(f"\nhttps://docs.google.com/document/d/{DOC_ID}/edit")


if __name__ == "__main__":
    sys.exit(main())
