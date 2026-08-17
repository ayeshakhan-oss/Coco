"""
Email the SMG "Execution Sprint" benchmark answer + scoring rubric to Ayesha for QA.

Internal document email (NOT a candidate communication) — the v8 candidate-comms layout
does not apply. Mobile-responsive per CLAUDE.md Rule 16: no fixed width on the outer
table, max-width in CSS, MSO ghost table for Outlook.

Recipient: ayesha.khan@taleemabad.com ONLY.
"""

import os
import re
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.utils.safe_send import safe_sendmail  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BENCHMARK = os.path.join(ROOT, "docs", "case_studies", "benchmarks",
                         "smg_execution_sprint_benchmark.md")
RUBRIC = os.path.join(ROOT, ".claude", "skills", "02_candidate-evaluation",
                      "case-study-scoring-rubric.md")

SENDER = "ayesha.khan@taleemabad.com"
RECIPIENTS = ["ayesha.khan@taleemabad.com"]
SUBJECT = "SMG Case Study — Benchmark Answer + Scoring Rubric (for QA)"

# ----------------------------------------------------------------------------- markdown

def _inline(t: str) -> str:
    t = (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    t = re.sub(r"`([^`]+)`",
               r'<code style="background:#eef1f6;padding:1px 5px;border-radius:3px;'
               r'font-family:Consolas,Monaco,monospace;font-size:13px;">\1</code>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t, flags=re.S)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
               r'<a href="\2" style="color:#2f4fa2;">\1</a>', t)
    return t


def md_to_html(md: str) -> str:
    """Minimal markdown -> email-safe HTML. Handles what the benchmark actually uses."""
    out, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        ln = lines[i]

        if not ln.strip():
            i += 1
            continue

        if re.match(r"^---+\s*$", ln):
            out.append('<hr style="border:0;border-top:1px solid #dfe3ea;margin:26px 0;">')
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            lvl, txt = len(m.group(1)), _inline(m.group(2))
            sz = {1: 23, 2: 19, 3: 16, 4: 14}[lvl]
            top = {1: 30, 2: 26, 3: 20, 4: 16}[lvl]
            col = "#1a2b4c" if lvl <= 2 else "#2f4fa2"
            rule = ("border-bottom:2px solid #2f4fa2;padding-bottom:6px;"
                    if lvl == 1 else "")
            out.append(
                f'<h{lvl} style="font-family:Georgia,serif;font-size:{sz}px;color:{col};'
                f'margin:{top}px 0 10px;line-height:1.3;{rule}">{txt}</h{lvl}>')
            i += 1
            continue

        # table
        if ln.strip().startswith("|") and i + 1 < len(lines) and \
                re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            hdr = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ['<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin:14px 0;">'
                 '<table role="presentation" style="width:100%;border-collapse:collapse;'
                 'font-family:Arial,sans-serif;font-size:13px;">']
            t.append('<tr>' + "".join(
                f'<th style="background:#1a2b4c;color:#fff;text-align:left;padding:8px 10px;'
                f'font-weight:600;">{_inline(c)}</th>' for c in hdr) + "</tr>")
            for n, r in enumerate(rows):
                bg = "#ffffff" if n % 2 == 0 else "#f5f7fa"
                t.append(f'<tr style="background:{bg};">' + "".join(
                    f'<td style="padding:8px 10px;border-bottom:1px solid #e6e9ef;'
                    f'vertical-align:top;">{_inline(c)}</td>' for c in r) + "</tr>")
            t.append("</table></div>")
            out.append("".join(t))
            continue

        # blockquote
        if ln.strip().startswith(">"):
            buf = []
            while i < len(lines) and (lines[i].strip().startswith(">") or
                                      (lines[i].strip() and buf and
                                       not lines[i].strip().startswith("|"))):
                if not lines[i].strip().startswith(">"):
                    break
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner = md_to_html("\n".join(buf))
            out.append('<div style="border-left:3px solid #2f4fa2;background:#f5f7fa;'
                       'padding:10px 18px;margin:14px 0;">' + inner + "</div>")
            continue

        # list
        if re.match(r"^\s*([-*]|\d+\.)\s+", ln):
            ordered = bool(re.match(r"^\s*\d+\.\s+", ln))
            items = []
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                buf = [re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i])]
                i += 1
                # absorb continuation lines so inline spans aren't split mid-item
                while (i < len(lines) and lines[i].strip()
                       and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[i])
                       and not re.match(r"^(#{1,4}\s|>|\||---+\s*$)", lines[i].strip())):
                    buf.append(lines[i].strip())
                    i += 1
                items.append(_inline(" ".join(buf)))
            tag = "ol" if ordered else "ul"
            out.append(f'<{tag} style="font-family:Georgia,serif;font-size:15px;'
                       f'line-height:1.7;color:#22303f;margin:12px 0;padding-left:22px;">'
                       + "".join(f"<li style='margin:5px 0;'>{it}</li>" for it in items)
                       + f"</{tag}>")
            continue

        # paragraph
        buf = []
        while i < len(lines) and lines[i].strip() and \
                not re.match(r"^(#{1,4}\s|\s*[-*]\s|\s*\d+\.\s|>|\|)", lines[i]) and \
                not re.match(r"^---+\s*$", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append('<p style="font-family:Georgia,serif;font-size:15px;line-height:1.75;'
                       'color:#22303f;margin:12px 0;">' + _inline(" ".join(buf)) + "</p>")
    return "".join(out)


# ----------------------------------------------------------------------------- shell

INTRO = """
<p style="font-family:Georgia,serif;font-size:15px;line-height:1.75;color:#22303f;margin:0 0 14px;">
Hi Ayesha,</p>
<p style="font-family:Georgia,serif;font-size:15px;line-height:1.75;color:#22303f;margin:0 0 14px;">
Here is the SMG case study benchmark answer for your QA, with the scoring rubric attached
alongside it. Nothing gets scored until you have signed this off.</p>
<p style="font-family:Georgia,serif;font-size:15px;line-height:1.75;color:#22303f;margin:0 0 14px;">
Every figure in it was computed directly from the Alpha Platform CSVs, so the ground-truth
table doubles as the answer key for checking any candidate's numbers.</p>
<p style="font-family:Georgia,serif;font-size:15px;line-height:1.75;color:#22303f;margin:0 0 6px;">
<strong>Two things worth your eye:</strong></p>
<ol style="font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#22303f;margin:0 0 14px;padding-left:22px;">
<li style="margin:6px 0;"><strong>Is the bar right?</strong> I pitched Strong Yes at roughly
what Umar produced plus catching one structural trap. If that is too high for a 3-hour task,
I would lower the band thresholds rather than weaken the benchmark.</li>
<li style="margin:6px 0;"><strong>Weighting.</strong> Execution specificity carries the most
weight (25%) because the JD is emphatic that this is a hands-on execution role. Easy to change
if you would rather data judgment led.</li>
</ol>
<p style="font-family:Georgia,serif;font-size:15px;line-height:1.75;color:#22303f;margin:0 0 14px;">
One disclosure: we agreed the benchmark would be written before I read any submission, and I
read Umar's first because it arrived early. I recomputed everything independently from the raw
data, and found two things his analysis missed — but you should judge the bar knowing that.</p>
"""


def build_html(body_md: str) -> str:
    return f"""<!--[if mso]><table role="presentation" width="760" align="center"><tr><td><![endif]-->
<div style="background:#eef1f6;padding:22px 12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
       style="width:100%;max-width:760px;margin:0 auto;background:#ffffff;
              border-radius:8px;border:1px solid #dfe3ea;">
  <tr>
    <td style="background:#1a2b4c;padding:24px 30px;border-radius:8px 8px 0 0;">
      <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1.6px;
                  text-transform:uppercase;color:#93a7c9;margin-bottom:6px;">
        Taleemabad &middot; Talent Acquisition</div>
      <div style="font-family:Georgia,serif;font-size:22px;color:#ffffff;line-height:1.3;">
        SMG Case Study — Benchmark &amp; Rubric</div>
      <div style="font-family:Arial,sans-serif;font-size:13px;color:#c3d0e6;margin-top:8px;">
        Job 42 &middot; Senior Manager Growth &middot; for QA before scoring</div>
    </td>
  </tr>
  <tr><td style="padding:26px 30px 34px;">{INTRO}
    <hr style="border:0;border-top:1px solid #dfe3ea;margin:24px 0;">
    {md_to_html(body_md)}
  </td></tr>
  <tr>
    <td style="background:#f5f7fa;padding:16px 30px;border-top:1px solid #dfe3ea;
               border-radius:0 0 8px 8px;font-family:Arial,sans-serif;font-size:12px;
               color:#6b7a90;">
      Benchmark: <code>docs/case_studies/benchmarks/smg_execution_sprint_benchmark.md</code><br>
      Rubric: <code>.claude/skills/02_candidate-evaluation/case-study-scoring-rubric.md</code>
    </td>
  </tr>
</table></div>
<!--[if mso]></td></tr></table><![endif]-->"""


def main() -> None:
    load_dotenv(os.path.join(ROOT, ".env"))
    password = os.getenv("EMAIL_PASSWORD")
    if not password:
        raise SystemExit("EMAIL_PASSWORD missing from .env")

    body_md = open(BENCHMARK, encoding="utf-8").read()
    html = build_html(body_md)

    msg = MIMEMultipart("mixed")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = ", ".join(RECIPIENTS)

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText("HTML email — please view in an HTML-capable client.", "plain"))
    alt.attach(MIMEText(html, "html"))
    msg.attach(alt)

    for path, name in ((BENCHMARK, "SMG_Execution_Sprint_BENCHMARK.md"),
                       (RUBRIC, "Case_Study_Scoring_Rubric.md")):
        with open(path, "rb") as fh:
            att = MIMEApplication(fh.read(), _subtype="octet-stream")
        att.add_header("Content-Disposition", "attachment", filename=name)
        msg.attach(att)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, password)
    safe_sendmail(server, SENDER, RECIPIENTS, msg.as_string(),
                  context="smg_case_study_benchmark_qa")
    server.quit()
    print(f"Sent to {RECIPIENTS} — {len(html):,} chars HTML + 2 attachments")


if __name__ == "__main__":
    main()
