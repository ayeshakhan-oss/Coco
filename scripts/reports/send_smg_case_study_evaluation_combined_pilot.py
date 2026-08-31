"""
SMG Case Study Evaluation — CONSOLIDATED (Job 42) — PILOT to Ayesha.

Ayesha, 2026-08-31: Ali Wajdan's case study is now accessible and Khushal has also submitted —
"now do it again".

SCOPE — 9 candidates, same locked format as the 24 and 30 August reports, now in three parts:
  - The SIX from the round-2 report (24 Aug): Furqan, Hania, Shafaq, Lamis, Kanooz, Rimsha.
  - Vaneeza Tashfeen Baig (submitted 25 Aug), scored 30 Aug.
  - Khushal Kakar (app 4134, submitted 30 Aug) — NEW, scored here.
  - Ali Wajdan Khan (app 3977, submitted 29 Aug) — NEW, scored here; his Doc link was shared
    with nobody until 31 Aug, so this is his first assessment.

Every previously reported score is unchanged. The two new write-ups use the same benchmark,
rubric and weights, and every headline figure was recomputed from the raw 546-row dataset.

Internal report email. Mobile-responsive per CLAUDE.md Rule 16.
"""

import importlib.util
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.utils.safe_send import safe_sendmail  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
SENDER = "ayesha.khan@taleemabad.com"
RECIPIENTS = ["ayesha.khan@taleemabad.com"]
SUBJECT = "[PILOT - ] SMG Case Study - Consolidated Evaluation Report (9 candidates) | Job 42"

DIMS = ["Data", "Execution", "Stakeholder", "Commercial", "Discipline", "Signal"]


def _load(fname, mod):
    spec = importlib.util.spec_from_file_location(mod, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R2 = _load("send_smg_case_study_evaluation_round2_pilot.py", "_r2")
R3 = _load("send_smg_case_study_evaluation_round3_pilot.py", "_r3")
R4 = _load("smg_round4_candidates.py", "_r4")

BY = {c["name"]: c for c in list(R2.CANDS) + list(R3.CANDS) + list(R4.CANDS)}
ORDER = ["Khushal Kakar", "Furqan Afzal", "Hania Khan", "Vaneeza Tashfeen Baig",
         "Shafaq Syed", "Lamis Maniar", "Kanooz Ahmed Siddiqui",
         "Ali Wajdan Khan", "Rimsha Taj"]
CANDS = [BY[n] for n in ORDER]

W = [20, 25, 20, 15, 10, 10]
for c in CANDS:
    got = sum(s / 5 * w for s, w in zip(c["scores"], W))
    assert abs(got - c["total"]) < 0.01, f"{c['name']} {got} != {c['total']}"
assert [c["total"] for c in CANDS] == sorted((c["total"] for c in CANDS), reverse=True), "not ranked"


def stat_boxes():
    boxes = [("9", "Scored", "#1a2b4c"), ("29", "Documents read", "#2f6fb5"),
             ("6", "Recommended", "#1b7f4d"), ("2", "Still blocked", "#b3261e")]
    tds = "".join(
        f'<td style="width:25%;padding:6px;"><div style="background:{c};border-radius:6px;'
        f'padding:16px 8px;text-align:center;">'
        f'<div style="font-family:Georgia,serif;font-size:26px;color:#fff;font-weight:bold;">{n}</div>'
        f'<div style="font-family:Arial,sans-serif;font-size:10.5px;color:#dbe5f5;'
        f'letter-spacing:0.8px;text-transform:uppercase;margin-top:4px;">{l}</div></div></td>'
        for n, l, c in boxes)
    return ('<table role="presentation" width="100%" style="width:100%;border-collapse:collapse;'
            f'margin:18px 0;"><tr>{tds}</tr></table>')


NEW = {"Khushal Kakar", "Ali Wajdan Khan"}


def ranked_table():
    head = "".join(f'<th style="background:#1a2b4c;color:#fff;padding:8px 6px;font-size:11px;'
                   f'text-align:center;">{d}</th>' for d in DIMS)
    rows = []
    for i, c in enumerate(CANDS):
        tag = ('<span style="background:#c47f16;color:#fff;padding:1px 5px;border-radius:3px;'
               'font-size:9px;margin-left:6px;">NEW</span>' if c["name"] in NEW else "")
        nm = f'<a href="{c["link"]}" style="color:#2f4fa2;">{c["name"]}</a>{tag}'
        cells = "".join(
            f'<td style="text-align:center;padding:8px 6px;border-bottom:1px solid #e6e9ef;">{s}</td>'
            for s in c["scores"])
        rows.append(
            f'<tr style="background:{"#ffffff" if i%2==0 else "#f5f7fa"};">'
            f'<td style="padding:8px 10px;border-bottom:1px solid #e6e9ef;">{nm}<br>'
            f'<span style="font-size:11px;color:#6b7a90;">App {c["app"]} &middot; '
            f'{len(c["docs"])} docs</span></td>'
            f'<td style="text-align:center;padding:8px;border-bottom:1px solid #e6e9ef;'
            f'font-weight:bold;font-size:16px;">{c["total"]}</td>{cells}'
            f'<td style="text-align:center;padding:8px;border-bottom:1px solid #e6e9ef;">'
            f'<span style="background:{c["colour"]};color:#fff;padding:3px 8px;border-radius:3px;'
            f'font-size:10px;white-space:nowrap;">{c["band"]}</span></td></tr>')
    return ('<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;">'
            '<table role="presentation" style="width:100%;border-collapse:collapse;'
            'font-family:Arial,sans-serif;font-size:13px;">'
            '<tr><th style="background:#1a2b4c;color:#fff;padding:8px 10px;text-align:left;">Candidate</th>'
            '<th style="background:#1a2b4c;color:#fff;padding:8px;font-size:11px;">Total</th>'
            f'{head}<th style="background:#1a2b4c;color:#fff;padding:8px;font-size:11px;">Band</th></tr>'
            + "".join(rows) + "</table></div>")


sec = R2.sec
doc_table = R2.doc_table
deep_dives = R2.deep_dives

INTRO = """
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:6px 0 0;">
    All nine Senior Manager Growth case studies from this batch, in one place.
    <strong>Two are new since the 30 August report</strong> &mdash; Khushal Kakar, who submitted on
    30 August, and Ali Wajdan Khan, whose document was shared with nobody until yesterday and is
    assessed here for the first time. The seven write-ups you have already read are reproduced
    unchanged; no previously reported score has moved.</p>
  <p style="font-family:Georgia,serif;font-size:13.5px;line-height:1.7;color:#1b4d3e;
            background:#eef7f1;border-left:3px solid #1b7f4d;padding:10px 14px;margin:14px 0 0;">
    <strong>Khushal Kakar enters at the top of the ranking on 98</strong>, level with Shahmir
    Hashmat from the first round and the highest score in this batch. He is the only candidate in
    any round who checked the dataset against itself before analysing it, and his workbook carries
    <strong>9,004 live formulas</strong> including a QA and reconciliation tab. He achieved it after
    losing two days unable to open the brief.</p>
  <p style="font-family:Georgia,serif;font-size:13.5px;line-height:1.7;color:#1b4d3e;
            background:#eef7f1;border-left:3px solid #1b7f4d;padding:10px 14px;margin:14px 0 0;">
    <strong>Figures were not checked against our own summary table.</strong> The raw 546-row user
    dataset was independently revalidated against the benchmark ground truth &mdash; 546 rows,
    Pakistan 265 and Sri Lanka 261, registration 43.8% and 45.6%, repeat use 62.9% and 19.3%,
    35 coaching adopters, 118 sessions started and 88 completed, five acquisition spikes &mdash;
    every figure reproduced exactly. Each candidate's headline numbers were then recomputed from
    that file. <strong>Nobody fabricated data.</strong></p>
  <p style="font-family:Georgia,serif;font-size:13.5px;line-height:1.7;color:#7b341e;
            background:#fdf6ec;border-left:3px solid #c47f16;padding:10px 14px;margin:14px 0 0;">
    <strong>Sent in three parts.</strong> Gmail clips anything over about 100KB behind a "view
    entire message" link. Part 1 covers Khushal, Furqan and Hania; Part 2 covers Vaneeza, Shafaq and
    Lamis; Part 3 covers Kanooz, Ali Wajdan and Rimsha, plus the outstanding items and the method
    note. The ranking table appears in all three so each part stands on its own.</p>"""

SEPARATES = """
  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">What separates them</h2>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>First, which coaching column they opened.</strong> The dataset carries two.
    <em>audio_coaching_sessions</em> sums to 1 across all 546 users; <em>coaching_started</em> sums
    to 118 across 35 adopters. Seven of the nine built on the real one. Rimsha used the wrong one and
    recommended deprioritising the flagship feature. Ali Wajdan used both &mdash; the wrong column in
    his feature table, the right one in his priorities &mdash; and never reconciled them, so his own
    submission contradicts itself.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Second, whether anyone checked the data before trusting it.</strong> One candidate did.
    Khushal built a reconciliation tab comparing fourteen master-file computations against the
    aggregate reference file, and it surfaced a registration count that does not agree with itself
    (240 by one field, 239 by another), a three-session gap between two chat totals, and a
    mislabelled aggregate field. Hania found the same registration discrepancy by hand. Nobody else
    looked.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Third, whether the comparison was fair before it was made.</strong> Sri Lanka registers
    slightly better than Pakistan and has produced zero coaching adopters. Two candidates checked the
    tenure first. Vaneeza found that 157 of Sri Lanka's 261 users signed up in the final eight days
    and re-ran the whole comparison at matched maturity. Khushal found that the 11 December cohort has
    <strong>zero</strong> users with seven observable days and refused to call it a failure. Both are
    right, and both conclusions are unavailable to anyone who compares raw totals.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Fourth, whether the ratio has the same population top and bottom.</strong> Lamis divides
    feature users by feature users and gets 1.15 uses per presentation adopter. Rimsha divides all
    Pakistani users' active days by the count of presentation sessions and gets 11.1, which is not a
    per-user figure at all &mdash; and because presentations are the least-used feature, the smallest
    denominator produces the biggest number, so the metric ranks features in inverse order of use.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Fifth, the 14 November concentration.</strong> One day produced 23 of the platform's 35
    coaching adopters. Khushal and Lamis both report 57.5% adoption for that cohort and Khushal draws
    the right instruction &mdash; <em>replicate the onboarding pattern, not "events" as a channel</em>.
    Furqan saw the week rather than the day. Vaneeza grouped it with two zero-adopter days and averaged
    the signal away. Kanooz, Shafaq, Rimsha and Ali Wajdan did no cohort work at all.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Sixth, Assignment 3 spread the scores, exactly as in the first round.</strong> Khushal
    gave a probability with movement in both directions on named week-1 and week-2 evidence, and told
    the Head of Growth what to carry it as. Hania said she would not raise the probability on a
    positive conversation alone. Shafaq and Vaneeza each gave two numbers. Kanooz's email never
    mentions the five-week deadline the whole scenario turns on; Ali Wajdan's contains an unfilled
    "xxx" and a literacy claim the data does not support; and Rimsha put the deal at 70% on the
    strength of a WhatsApp relationship.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Seventh, consent.</strong> Classroom audio reaching a teacher's administrator without
    permission is the loop's real failure mode, and the case never raises it. Khushal builds
    <em>"get permission to share"</em> into the loop stage itself; Hania and Shafaq raise it too.
    Furqan and Vaneeza both build artefacts carrying a named teacher's coaching feedback to their head
    teacher without establishing permission first.</p>"""

BLOCKED = """
  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Outstanding</h2>
  <div style="background:#eef7f1;border-left:3px solid #1b7f4d;padding:12px 16px;margin:12px 0;">
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:0;">
      <strong>Both blockers from the 30 August report are cleared.</strong> Ali Wajdan's document was
      opened and is scored here. Khushal got access to the brief and submitted on 30 August, and his
      submission is the strongest in the batch. Worth noting what that cost: he lost two days to
      access requests and still returned six deliverables inside the stated time-box.</p>
  </div>
  <div style="background:#fdf6ec;border-left:3px solid #c47f16;padding:12px 16px;margin:12px 0;">
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:0;">
      <strong>Muhammad Ahmad Taj (app 3971) &mdash; still missing, 12 days on.</strong> Markaz records
      a submission on 19 August; his note says the work is in an attached ZIP; Markaz accepts Word and
      Excel only, so the upload failed silently. No files, no link, nothing in the mailbox. He is the
      last candidate in this batch who has done work we cannot see.</p>
  </div>
  <div style="background:#fdf6ec;border-left:3px solid #c47f16;padding:12px 16px;margin:12px 0;">
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:0;">
      <strong>Never submitted, never nudged.</strong> Muhammad Zeshan Nawaz (app 3921) and Muhammad
      Bilal Sadiq (app 4051) were sent the case study on 7 August, 24 days ago. Both still read as
      <em>shortlisted</em> in Markaz, so they inflate the live pipeline.</p>
  </div>
  <div style="background:#f5f7fa;border-left:3px solid #2f6fb5;padding:12px 16px;margin:12px 0;">
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:0;">
      <strong>Markaz record hygiene.</strong> Hania Khan's submission still has <strong>no Markaz
      record at all</strong> &mdash; her portal upload failed and she emailed the files &mdash; so she
      reads as a non-submitter on the status field alone. Vaneeza Baig still shows as
      <em>case_study_sent</em> rather than submitted. Hania (4037), Lamis (4063) and Kanooz (3811)
      each carry a duplicate application sitting in <em>rejected</em>.</p>
  </div>"""

METHOD = """
  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Method &amp; limits</h2>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    Scored against <em>smg_execution_sprint_benchmark.md</em> on the six-dimension rubric, with the
    same key, the same weights and the same reader used for the 17 and 24 August reports, so every
    score in this document is comparable with those. The benchmark was written and QA'd before any
    submission was opened and nothing from any round has been added to it. Every deliverable was read
    end to end: PDFs page by page, Word documents including all tables, decks slide by slide, and
    every spreadsheet tab opened with formulas preserved so a live model could be told apart from
    pasted values. Quotations are the candidates' own words.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>One score carries a caveat that is ours to resolve, not the candidate's.</strong>
    Shafaq Syed states three times that the per-user dataset was not supplied and that cohort, source
    and week-level cuts were therefore unavailable. Furqan Afzal independently reported on 22 August
    that the dataset tab appeared to be missing from the same document. If the data was genuinely
    unreachable for some candidates, her Data score of 2 reflects our distribution rather than her
    judgment and should be revisited. Her first debrief probe is designed to settle it.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>On the borderline recommendation.</strong> Kanooz Ahmed Siddiqui scores 62, which the
    rubric places in the band to proceed only if the pool is thin. It is not thin &mdash; six
    candidates from the first round scored 70 or above and six more clear it here. Her Assignment 1
    is genuinely original and worth keeping on file; her Assignments 2 and 3 do not currently meet
    the bar. That is a recommendation, not a decision.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>The submission step is where this pipeline is losing work, and it nearly cost us the top
    candidate.</strong> Five of the last nine SMG submissions hit an access or format failure on
    arrival: a ZIP Markaz will not accept (still unresolved), a Drive link shared with nobody, a
    portal upload that failed and came by email with no Markaz record, a portal that will not take
    multiple files, and a candidate who could not open the brief for two days. <strong>Khushal scored
    98 after losing two of his days to access requests, and Ali Wajdan sat unassessed for two days for
    a sharing setting.</strong> None of this is a candidate quality signal. Letting candidates upload
    Word and Excel directly, or copying hiring@ as standard, would remove every one of these
    failure modes.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Every submission is archived.</strong> All files, including those that arrived only as
    links and those that arrived only by email, are in the Senior Manager Growth submissions folder,
    one subfolder per candidate. Each name in the ranking table links to its folder.</p>"""


PARTS = {1: CANDS[0:3], 2: CANDS[3:6], 3: CANDS[6:9]}
PART_LABEL = {1: "&mdash; 1 to 3 of 9", 2: "&mdash; 4 to 6 of 9", 3: "&mdash; 7 to 9 of 9"}


def build_html(part):
    subset = PARTS[part]
    names = ", ".join(c["name"].split()[0] for c in subset)
    return f"""<!--[if mso]><table role="presentation" width="880" align="center"><tr><td><![endif]-->
<div style="background:#eef1f6;padding:22px 12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
       style="width:100%;max-width:880px;margin:0 auto;background:#ffffff;border-radius:8px;
              border:1px solid #dfe3ea;">
 <tr><td style="background:#1a2b4c;padding:24px 30px;border-radius:8px 8px 0 0;">
   <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1.6px;
               text-transform:uppercase;color:#93a7c9;">Taleemabad &middot; Talent Acquisition</div>
   <div style="font-family:Georgia,serif;font-size:23px;color:#fff;margin-top:6px;">
     SMG Case Study &mdash; Consolidated Evaluation &middot; Part {part} of 3</div>
   <div style="font-family:Arial,sans-serif;font-size:13px;color:#c3d0e6;margin-top:8px;">
     Job 42 &middot; Senior Manager Growth &middot; 31 August 2026 &middot; {names}</div>
 </td></tr>
 <tr><td style="padding:24px 30px 34px;">

  {stat_boxes() if part == 1 else ""}
  {INTRO if part == 1 else ""}

  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:28px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Ranking</h2>
  {ranked_table()}
  <p style="font-family:Arial,sans-serif;font-size:12px;color:#6b7a90;margin:8px 0 0;">
    Dimensions scored 1&ndash;5. Weights: Data 20% &middot; Execution 25% &middot; Stakeholder 20%
    &middot; Commercial 15% &middot; Discipline 10% &middot; Signal 10%. Bands: 80+ strong yes
    &middot; 65&ndash;79 yes &middot; 50&ndash;64 borderline &middot; under 50 no.
    Six of the nine are recommended for debrief.</p>

  {SEPARATES if part == 1 else ""}

  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 4px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Candidate detail
             {PART_LABEL[part]}</h2>
  {deep_dives(subset)}

  {BLOCKED if part == 3 else ""}
  {METHOD if part == 3 else ""}

 </td></tr>
 <tr><td style="background:#f5f7fa;padding:16px 30px;border-top:1px solid #dfe3ea;
        border-radius:0 0 8px 8px;font-family:Arial,sans-serif;font-size:12px;color:#6b7a90;">
   Taleemabad Talent Acquisition &middot; hiring@taleemabad.com &middot; 31 August 2026</td></tr>
</table></div>
<!--[if mso]></td></tr></table><![endif]-->"""


def main():
    load_dotenv(os.path.join(ROOT, ".env"))
    pw = os.getenv("EMAIL_PASSWORD")
    if not pw:
        raise SystemExit("EMAIL_PASSWORD missing")
    parts = {p: build_html(p) for p in (1, 2, 3)}
    for p, h in parts.items():
        n = len(h.encode())
        if n > 100_000:
            raise SystemExit(f"BLOCKED: part {p} is {n:,} bytes - Gmail would clip it")
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER, pw)
    for p, html in parts.items():
        msg = MIMEMultipart("alternative")
        msg["Subject"] = SUBJECT.replace("| Job 42", f"- Part {p} of 3 | Job 42")
        msg["From"] = SENDER
        msg["To"] = ", ".join(RECIPIENTS)
        msg.attach(MIMEText("HTML report - view in an HTML-capable client.", "plain"))
        msg.attach(MIMEText(html, "html"))
        safe_sendmail(s, SENDER, RECIPIENTS, msg.as_string(),
                      context=f"smg_case_study_evaluation_combined_part{p}")
        print(f"Part {p} sent to {RECIPIENTS} - {len(html.encode()):,} bytes")
    s.quit()


if __name__ == "__main__":
    main()
