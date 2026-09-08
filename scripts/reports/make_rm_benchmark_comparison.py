"""
RM internal case study - question-by-question comparison of every submission against the
benchmark answer key (Revision 2).

Ayesha, 2026-09-08: "question by question analysis of each case study with comparison from
the benchmark answer we made, i also made a few additions to it... two documents, first one
will have the case study comparison result of people we just sent invite, these scored above
70 and then one for below 70."

Produces TWO PDFs:
  A - the 17 at or above 70 (invited to debrief 2026-09-07)
  B - the 8 below 70

Each document carries, per question: what the benchmark requires (with Ayesha's Revision 2
additions flagged), then per candidate what they actually did and where they sit against it.

SOURCES - nothing here is generated fresh:
  strict_scores.json  per-question anchors, marks, caps, and the question-tagged strengths
                      and gaps recorded during the full read of all 25 submissions
  qbq.json            the fuller answered/better analysis already written for the 8 below 70
  bench.py            benchmark requirements per question + targeted re-reads for the ten
                      question-slots where the scoring pass recorded a mark without a note
"""
import json
import os
import re
import subprocess
import sys
import tempfile

SCRATCH = (r"C:\Users\Dell\AppData\Local\Temp\claude\c--Agent-Coco"
           r"\7a2e7743-8713-4f95-9dd1-44dbccb04afa\scratchpad")
sys.path.insert(0, SCRATCH)
from bench import BENCH, FILL  # noqa: E402

SC = json.load(open(os.path.join(SCRATCH, "strict_scores.json"), encoding="utf-8"))
QBQ = json.load(open(os.path.join(SCRATCH, "qbq.json"), encoding="utf-8"))
ROSTER = {r["code"]: r["name"] for r in
          json.load(open(os.path.join(SCRATCH, "rm_subs", "roster.json"), encoding="utf-8"))}

NAVY, BLUE, RED, GREEN, RULE, SOFT, MUTE, AMBER = (
    "#16202e", "#2f4fa2", "#a8442a", "#1b7f4d", "#d7dce4", "#f4f6fa", "#5b6472", "#8a6d1f")
PTS = {"Q1": 10, "Q2": 15, "Q3": 10, "Q4": 15, "Q5": 10,
       "Q6": 10, "Q7": 10, "Q8": 10, "Q9": 10, "Q10": None}
QS = [f"Q{i}" for i in range(1, 11)]
ANCHOR_WORD = {5: "at the benchmark", 4: "close to it", 3: "part of the way",
               2: "short of it", 1: "well short", 0: "not attempted"}

rows = sorted(((v["total"], c) for c, v in SC.items()), reverse=True)
ABOVE = [c for t, c in rows if t >= 70]
BELOW = [c for t, c in rows if t < 70]


def tagged(code, q):
    """Question-tagged strengths and gaps recorded during the read."""
    v = SC[code]
    pat = re.compile(rf'^\s*{q}\b[:.\s]', re.I)
    s = [re.sub(pat, "", x).strip() for x in v["strengths"] if pat.match(x)]
    g = [re.sub(pat, "", x).strip() for x in v["gaps"] if pat.match(x)]
    # some items name the question mid-sentence rather than as a prefix
    if not s:
        s = [x for x in v["strengths"] if re.search(rf'\b{q}\b', x)]
    if not g:
        g = [x for x in v["gaps"] if re.search(rf'\b{q}\b', x)]
    return s, g


def content(code, q):
    """(did, distance) for one candidate/question."""
    if (code, q) in FILL:
        return FILL[(code, q)]
    if code in QBQ:                                   # the 8 - fuller text already written
        return QBQ[code]["qa"][q]["answered"], QBQ[code]["qa"][q]["better"]
    s, g = tagged(code, q)
    did = ("; ".join(x[0].upper() + x[1:] for x in s) + ".") if s else ""
    dist = ("; ".join(x[0].upper() + x[1:] for x in g) + ".") if g else ""
    a = SC[code]["anchors"].get(q)
    if not did:
        if a is None:                                  # Q10, banded
            did = (f"Banded <b>{SC[code]['q10band']}</b>. The band reflects the answer as a whole "
                   f"against the five criteria above rather than any single point.")
        elif a >= 4:
            did = ("Did what the key asks on this question. Nothing was singled out during the "
                   "read, which at this mark means the answer was complete rather than "
                   "exceptional.")
        else:
            did = ("Everything recorded on this question during the read was a shortfall against "
                   "the key - see the note below.")
    if not dist:
        if a is None:
            dist = (f"Banded {SC[code]['q10band']}; nothing specific recorded against the "
                    f"criteria above.")
        elif a == 5:
            dist = "Met the benchmark on this question. Nothing recorded against it."
        elif a == 4:
            dist = ("Close to the benchmark, with nothing material recorded against it - the "
                    "mark reflects depth rather than a missing requirement.")
        else:
            dist = ("Marked below the benchmark, but no single shortfall was isolated during the "
                    "read; the mark reflects the answer overall against the criteria above.")
    return did, dist


def para(t, sz=13, col="#232a35", mb=9, lh=1.62):
    return (f'<p style="margin:0 0 {mb}px;font:{sz}px/{lh} Georgia,serif;color:{col};">{t}</p>')


def bench_panel():
    out = ""
    for q in QS:
        head, reqs = BENCH[q]
        lis = ""
        for r, rev2 in reqs:
            badge = (f'<span style="background:{AMBER};color:#fff;font:700 8.5px Georgia,serif;'
                     f'padding:1px 5px;border-radius:3px;letter-spacing:.4px;">REV 2</span> '
                     if rev2 else "")
            lis += (f'<li style="margin:0 0 7px;font:12px/1.6 Georgia,serif;color:#232a35;">'
                    f'{badge}{r}</li>')
        pt = f"{PTS[q]} marks" if PTS[q] else "not scored, banded only"
        out += (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
                f'style="margin:0 0 13px;page-break-inside:avoid;"><tr><td>'
                f'<div style="font:700 13px Georgia,serif;color:{NAVY};border-bottom:1px solid {RULE};'
                f'padding-bottom:4px;margin-bottom:7px;">{q}. {head}'
                f'<span style="float:right;font:400 11px Georgia,serif;color:{MUTE};">{pt}</span></div>'
                f'<ul style="margin:0;padding-left:17px;">{lis}</ul></td></tr></table>')
    return out


def scoreboard(codes):
    hd = "".join(f'<th style="padding:4px 3px;font:700 10px Georgia,serif;color:{MUTE};'
                 f'border-bottom:1px solid {RULE};text-align:center;">{q}<br>'
                 f'<span style="font-weight:400;font-size:8px;">/{PTS[q]}</span></th>'
                 for q in QS[:9])
    body = ""
    for t, c in [(SC[x]["total"], x) for x in codes]:
        cells = ""
        for q in QS[:9]:
            a = SC[c]["anchors"][q]
            col = RED if a <= 2 else (GREEN if a == 5 else "#232a35")
            wt = 700 if a in (0, 1, 2, 5) else 400
            cells += (f'<td style="padding:4px 3px;font:{wt} 11px Georgia,serif;color:{col};'
                      f'text-align:center;border-bottom:1px solid #eef1f5;">{SC[c]["q"][q]:g}</td>')
        body += (f'<tr><td style="padding:4px 6px 4px 0;font:12px Georgia,serif;color:#232a35;'
                 f'border-bottom:1px solid #eef1f5;white-space:nowrap;">{ROSTER[c]}</td>'
                 f'<td style="padding:4px 8px 4px 0;font:700 12px Georgia,serif;color:{NAVY};'
                 f'text-align:right;border-bottom:1px solid #eef1f5;">{t:g}</td>{cells}</tr>')
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="border-collapse:collapse;margin:0 0 6px;"><tr>'
            f'<th style="text-align:left;padding:4px 0;font:700 10px Georgia,serif;color:{MUTE};'
            f'border-bottom:1px solid {RULE};">NAME</th>'
            f'<th style="text-align:right;padding:4px 8px 4px 0;font:700 10px Georgia,serif;'
            f'color:{MUTE};border-bottom:1px solid {RULE};">TOTAL</th>{hd}</tr>{body}</table>'
            f'<div style="font:10.5px/1.5 Georgia,serif;color:{MUTE};margin:0 0 4px;">'
            f'Green = at the benchmark for that question. Red = short of it or worse. '
            f'Q10 carries no printed mark and is banded separately.</div>')


def candidate_section(code, first):
    v = SC[code]
    marks = "  ".join(
        f'<span style="color:{MUTE};">{q}</span> '
        f'<span style="color:{RED if v["anchors"][q] <= 2 else "#dfe6f2"};font-weight:700;">'
        f'{v["q"][q]:g}</span>' for q in QS[:9])
    caps = (f'<div style="font:10.5px Georgia,serif;color:#e8b4a5;margin-top:3px;">'
            f'benchmark caps applied: {", ".join(v["caps"])}</div>' if v["caps"] else "")
    qb = ""
    for q in QS:
        head, _ = BENCH[q]
        a = v["anchors"].get(q)          # Q10 is banded, not anchored
        mk = (f'<span style="float:right;font:700 12px Georgia,serif;'
              f'color:{RED if a <= 2 else (GREEN if a == 5 else NAVY)};">{v["q"][q]:g}'
              f'<span style="font-weight:400;font-size:9.5px;color:{MUTE};">/{PTS[q]} &middot; '
              f'{ANCHOR_WORD[a]}</span></span>' if PTS[q] else
              f'<span style="float:right;font:11px Georgia,serif;color:{MUTE};">'
              f'not scored &middot; {v["q10band"]}</span>')
        did, dist = content(code, q)
        qb += (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
               f'style="margin:0 0 13px;page-break-inside:avoid;"><tr><td>'
               f'<div style="font:700 12.5px Georgia,serif;color:{NAVY};'
               f'border-bottom:1px solid {RULE};padding-bottom:3px;margin-bottom:7px;">'
               f'{q}. {head}{mk}</div>'
               + para(f'<b style="color:{NAVY};">What they did.</b> {did}', 12.5, mb=7)
               + f'<div style="border-left:2px solid {BLUE};background:#f6f8fc;padding:7px 10px;'
                 f'font:12px/1.6 Georgia,serif;color:#232a35;">'
                 f'<b style="color:{BLUE};">Against the benchmark.</b> {dist}</div>'
               + '</td></tr></table>')
    return (f'<div style="{"" if first else "page-break-before:always;"}">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin:0 0 13px;"><tr><td style="background:{NAVY};padding:11px 15px;">'
            f'<div style="font:700 16px Georgia,serif;color:#fff;">{ROSTER[code]}'
            f'<span style="float:right;font-size:19px;">{v["total"]:g}'
            f'<span style="font-size:11px;font-weight:400;color:#aab4c4;">/100</span></span></div>'
            f'<div style="font:10.5px Georgia,serif;color:#aab4c4;margin-top:3px;">'
            f'{code} &middot; {marks}</div>{caps}</td></tr></table>'
            f'<div style="border-left:3px solid {AMBER};background:#fdfaf3;padding:9px 12px;'
            f'margin:0 0 15px;font:12.5px/1.6 Georgia,serif;color:#232a35;">'
            f'<b style="color:{AMBER};">Overall against the key.</b> '
            f'{QBQ[code]["overall"] if code in QBQ else v["notes"]}</div>{qb}</div>')


def build(codes, title, strap, intro):
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<style>@page{{size:A4;margin:12mm 11mm;}} body{{margin:0;}}</style></head><body style="background:#fff;">
<div style="font:700 19px Georgia,serif;color:{NAVY};margin:0 0 3px;">{title}</div>
<div style="font:12px Georgia,serif;color:{MUTE};margin:0 0 11px;">{strap}</div>
<div style="border:1px solid {RULE};background:{SOFT};padding:10px 12px;margin:0 0 16px;
     font:12px/1.6 Georgia,serif;color:#232a35;">{intro}</div>
<div style="font:700 15px Georgia,serif;color:{NAVY};margin:0 0 3px;">
  What the benchmark required</div>
<div style="font:11.5px/1.55 Georgia,serif;color:{MUTE};margin:0 0 11px;">
  Revision 2 of the answer key, written and QA'd before any submission was opened.
  <span style="background:{AMBER};color:#fff;font:700 8.5px Georgia,serif;padding:1px 5px;
  border-radius:3px;">REV 2</span> marks the five points Ayesha added or corrected in her QA
  round on 2 September, after the key was first drafted.</div>
{bench_panel()}
<div style="page-break-before:always;font:700 15px Georgia,serif;color:{NAVY};margin:0 0 3px;">
  Where each submission landed, question by question</div>
<div style="font:11.5px/1.55 Georgia,serif;color:{MUTE};margin:0 0 9px;">
  Marks are the case's own printed allocation of 100 points across Q1&ndash;Q9.</div>
{scoreboard(codes)}
{"".join(candidate_section(c, i == 0) for i, c in enumerate(codes))}
</body></html>"""


DOC_A = build(
    ABOVE, "Regional Manager - case study against the benchmark",
    "The 17 at or above the 70% bar &middot; invited to debrief 7 September 2026",
    "These are the seventeen invited to the debrief. For each, and for each of the ten questions, "
    "this sets out what the benchmark answer required, what the submission actually did, and where "
    "it sits against the key. It is written to be read before a debrief: the 'Against the benchmark' "
    "block on each question is where the unanswered part of that person's thinking sits, and is the "
    "natural place to probe. Nobody here matched the key on everything - the two at 100 each missed "
    "something, and both are noted.")

DOC_B = build(
    BELOW, "Regional Manager - case study against the benchmark",
    "The 8 below the 70% bar &middot; 2 September 2026",
    "These are the eight who fell below the published bar. Same structure as the companion document "
    "for the seventeen: what the benchmark required, what each submission did, and the distance "
    "between them. Read together the pattern is consistent - these eight lost marks far more often "
    "to a required element being absent than to reasoning being wrong, and five of the eight lost "
    "most of their Q4 on the same thing, which was showing no arithmetic on the one question whose "
    "purpose is that the capacity numbers close.")

if __name__ == "__main__":
    chrome = next((c for c in [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"] if os.path.exists(c)), None)
    if not chrome:
        sys.exit("no Chrome/Edge for PDF render")
    out = os.path.join(SCRATCH, "bench_cmp")
    os.makedirs(out, exist_ok=True)
    for tag, doc, n in (("above70", DOC_A, len(ABOVE)), ("below70", DOC_B, len(BELOW))):
        src = os.path.join(out, f"{tag}.html")
        pdf = os.path.join(out, f"RM Case Study vs Benchmark - {tag}.pdf")
        open(src, "w", encoding="utf-8").write(doc)
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=20000", f"--print-to-pdf={pdf}", src],
                       check=True, capture_output=True, timeout=300)
        print(f"{tag}: {n} candidates | html {len(doc):,} | pdf {os.path.getsize(pdf):,} bytes")
        print(f"   -> {pdf}")
