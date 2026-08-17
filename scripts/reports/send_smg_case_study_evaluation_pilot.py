"""
SMG Case Study Evaluation Report (Job 42) — PILOT to Ayesha.

Scored against docs/case_studies/benchmarks/smg_execution_sprint_benchmark.md
using .claude/skills/02_candidate-evaluation/case-study-scoring-rubric.md

Internal report email. Mobile-responsive per CLAUDE.md Rule 16.
"""

import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.utils.safe_send import safe_sendmail  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SENDER = "ayesha.khan@taleemabad.com"
RECIPIENTS = ["ayesha.khan@taleemabad.com"]
SUBJECT = "SMG Case Study — Evaluation Report (all 8 scored) | Job 42"

DIMS = ["Data", "Execution", "Stakeholder", "Commercial", "Discipline", "Signal"]

CANDS = [
    dict(
        name="Shahmir Hashmat", app="3911", total=98, band="STRONG YES", proceed=True,
        colour="#1b7f4d", scores=[5, 5, 5, 5, 5, 4],
        link="https://drive.google.com/drive/folders/1cUA0MpaOSDf47pCva6_gA45N97gKXuI7",
        stands_out="""He found things our own answer key missed. <strong>27 of 118 coaching
        sessions fail (22.9%), median 38 minutes of audio lost</strong> — a teacher records most
        of a lesson and it disappears. Failed and completed sessions have near-identical
        durations, so it is not a length limit. He also checked the reading-assessment
        languages: <strong>all 87 are English or Urdu; no Sinhala or Tamil passage exists</strong>,
        so the flagship feature cannot work in half the user base. Both verified exactly.<br><br>
        He caught the missing channel attribution, the Sri Lanka registration inversion, and split
        the acquisition spikes rather than averaging them. He wrote a causal caution unprompted —
        "engaged users do more of everything, so this correlation alone does not prove coaching
        causes retention." His tracker is the best in the pool: formulas, fill conventions, a
        stated definition of "active teacher" applied to both sides of K, and a caveat that at
        n=33 one clinic swings K by 0.1. He refused to invent pilot figures for a government
        official, and his internal update names three things <em>he</em> got wrong.""",
        thin="""His DEO email carries [X]/[Y]/[A]/[B] placeholders — well justified, but a
        template rather than a finished artefact.<br><br><strong>His reflection is a voice note
        (.m4a) and I cannot transcribe audio.</strong> Permitted by the brief, but one of six
        dimensions is unassessed; his 98 is provisional on it.""",
        probes=[
            "The 22.9% coaching failure rate — you called it a week-1 bug fix. How do you get "
            "that prioritised with a product team that doesn't report to you?",
            "You wrote that no layer should hear about us first from the layer above, or usage "
            "becomes compliance. Where did you learn that?",
            "Your internal update names three things you'd have done differently. Which have you "
            "actually got wrong in a real deal, and what did it cost?",
        ],
    ),
    dict(
        name="Muhammad Arshan Bilal", app="3884", total=94, band="STRONG YES", proceed=True,
        colour="#1b7f4d", scores=[5, 5, 4, 5, 5, 4],
        link="https://drive.google.com/drive/folders/1Ch4FlR5BApHRDneajESEffu6d1Erc6al",
        stands_out="""The most methodologically careful submission in the pool. He
        <strong>defined his own retention measures and explained why the obvious ones are
        useless</strong> — active_week1 is true for ~99% of users, so he built "repeat" and
        "7-day retained" instead. He then flagged that the <strong>11 December cohort is too
        recent for a fair retention comparison because the dataset ends 16 December</strong>.
        Only he and Shahmir corrected for right-censoring.<br><br>
        He caught the attribution gap explicitly — "every user is tagged direct despite known
        institutional introductions; channel ROI cannot be trusted until institution_id /
        campaign_id / cohort_id are captured" — isolated the Nov 14 cohort, and segmented to
        Pakistani secondary teachers (65 users, 49.2% coaching adoption).<br><br>
        His commercial writing is excellent: 45%, moving to 65% on confirmed budget inclusion or
        below 25% without sponsor access by week 2, and the line <em>"I would not carry this at a
        high probability simply because the pilot succeeded."</em> He refused to invent a CAC
        ceiling, saying he would agree the affordable cost per retained teacher with the Head of
        Growth using real contract economics. His opening note states plainly that he did not
        invent day-level patterns the file cannot support.""",
        thin="""His DEO email is solid but not distinctive — it asks for 15 minutes and names the
        deadline, without shrinking the ask to something trivially easy to grant, the way Shahmir
        and Junaid do.<br><br>
        He missed the Sri Lanka college-teacher mechanism, the coaching failure rate and the
        language gap. His 60-day targets are stated as numbers to hit rather than derived from
        what the current base can plausibly produce.""",
        probes=[
            "You corrected for right-censoring on Dec 11. What else in this dataset would you "
            "not trust, and why?",
            "Sri Lanka has zero coaching adopters across 261 users. Give me your best three "
            "explanations and how you'd tell them apart in a fortnight.",
            "You declined to set a CAC ceiling without real economics. Tell me about a time you "
            "pushed back on a number someone senior wanted you to commit to.",
        ],
    ),
    dict(
        name="Yusra Amjad", app="4061", total=89, band="STRONG YES", proceed=True,
        colour="#1b7f4d", scores=[5, 4, 4, 5, 4, 5],
        link="https://drive.google.com/drive/folders/11bowQeg_prEXh8carJnXqyNpveznx5o1",
        stands_out="""She found the most forensic detail in the pool. <strong>Sri Lankan
        registrations complete in a median of 4.2 minutes, tightly clustered — 90th percentile
        just 11 minutes. Pakistan's median is 37.2 minutes and varies wildly, some taking
        days.</strong> Her conclusion — a pre-loaded contact list rather than organic signups —
        is verified exactly, and she labelled it honestly as an educated guess because the data
        carries no acquisition source.<br><br>
        Then she built a causal argument on it: in Pakistan, completing registration roughly
        doubles usage (2.3 → 4.3 sessions) and repeat rate (34% → 63%). In Sri Lanka it changes
        nothing (1.8 → 1.6, 22% → 19%). <em>"If the issue were just a clunky sign-up process,
        fixing it would help Sri Lanka too — it doesn't."</em> Every figure verified exact. That
        is diagnosis, not description.<br><br>
        She also found the college-teacher concentration (62 of 119 Sri Lankan registrants), gave
        the <strong>only split probability in the pool</strong> — 30–40% for the full 200 schools,
        55–60% for some expansion once a scoped fallback is tabled — and wrote the best reflection
        of the eight: as an 8th-grade English teacher she found the school's mandated
        five-times-corrections policy producing zero improvement after two weeks, sourced her own
        worksheets instead, and got real gains. Specific, self-directed, against official
        policy.""",
        thin="""Her 60-day plan is organised into four two-week phases rather than by named owner
        per action — clear on <em>what</em>, lighter on <em>who</em>, where Shahmir and Arshan are
        explicit.<br><br>
        Her DEO email opens "I wanted to reach out and share something exciting!" and closes
        "Congratulations again!" — warm, but over-bright for a stakeholder silent for six weeks.
        It also carries unfilled [X]/[Y]/[Z] placeholders.<br><br>
        She missed the Nov 14 cohort as a distinct replicable event — she reads the spikes as bulk
        onboarding but never isolates the one that worked.""",
        probes=[
            "You spotted that Sri Lankan registrations complete in 4 minutes flat. What would you "
            "have asked for before that campaign ran?",
            "Nov 14 produced 40 users and 23 of the platform's 35 coaching adopters. You didn't "
            "single it out — what would you do with that now?",
            "You split the probability into full versus partial expansion. When have you had to "
            "sell a smaller version of a deal internally?",
        ],
    ),
    dict(
        name="Umar Zahid", app="3902", total=78, band="YES", proceed=True,
        colour="#2f6fb5", scores=[4, 5, 2, 5, 4, 3],
        link="https://drive.google.com/drive/folders/1TbSvIc94OMAbGk4Y7dtj5dh4QGlzYpj1",
        stands_out="""One of the sharpest reads on the acquisition spikes. He isolated the
        <strong>14 November cohort — 40 users, 82.5% registration, 87.5% repeat use, 57.5%
        coaching adoption</strong> — against the other four introductions producing 254 users and
        zero coaching adopters. Every figure exact, and he built his second priority around
        replicating that event's mechanics rather than running more events.<br><br>
        His internal update is strong: 35%, gating events in both directions, four specific asks,
        and an explicit refusal to use the competitor as client pressure.""",
        thin="""<strong>The DEO email is the weakest part of a good submission.</strong> Five
        short lines. No acknowledgement of the six weeks of silence, no mention of the budget
        deadline that makes it urgent, and it asks for a meeting rather than something easy to
        give. Against an action plan that is sophisticated about procurement, the email underuses
        what he clearly knows.<br><br>
        Slides 5 and 6 are byte-identical duplicates, taking the deck to 7 pages against a
        6-slide limit. AI disclosure on one deliverable only. He missed the attribution gap and
        did not draw the conclusion from Sri Lanka's higher registration rate.<br><br>
        <strong>Correction from the previous report.</strong> I flagged his tracker as possibly
        missing. It exists, and it is arguably the best of the eight — five tabs: a 60-day control
        tower, weekly metrics with K decomposed into invites-per-seed, referral registration rate
        and activation rate against target with a gap column, a 200-row schools pipeline carrying
        source and referrer IDs, a 500-row teacher log with referrer teacher ID and a consent
        field, and an action log with an escalation flag. I could not see it because the copy I
        was sent was a PDF of the analysis sheet alone. His execution score has moved from 4 to 5
        and his total from 73 to 78.""",
        probes=[
            "Rewrite your DEO email in front of us. Six weeks of silence, five weeks to close — "
            "what changes?",
            "Every user has source='direct'. What would you have done differently in Assignment 1 "
            "knowing there is no channel attribution at all?",
            "What would have to be true next Tuesday to move the deal to 60%, and what drops it "
            "below 15%?",
        ],
    ),
    dict(
        name="Junaid Ali", app="3992", total=74, band="YES", proceed=True,
        colour="#2f6fb5", scores=[5, 3, 5, 3, 4, 1],
        link="https://drive.google.com/drive/folders/1xZ29_Q3qVtf1grj4kCO_8kbXUcCWGUyC",
        stands_out="""<strong>He is the only candidate who explains <em>why</em> Sri Lanka has
        zero coaching adoption.</strong> His argument: those users were a teacher-training-college
        population, not practising classroom teachers — and coaching requires recording a real
        class, which a trainer does not have. I checked it: <strong>52.1% of registered Sri Lankan
        users teach university level only, against 6.9% in Pakistan</strong> — a 7.5× difference.
        That is a causal mechanism, not a correlation, and neither the other candidates nor our own
        benchmark found it.<br><br>
        His signal-versus-noise framing is the cleanest of the eight: <em>"not how many people
        tried it, but whether trying it once predicts trying it again."</em> He opens by naming
        the trap outright — Sri Lanka wins every vanity metric, "but retention of what?"<br><br>
        His Assignment 3 contains the most politically astute move anyone made: before going to
        the Provincial Secretary he gives the DEO advance notice, so that if the escalation works
        <em>the DEO looks like the person who made it happen rather than the person who got
        bypassed.</em> He runs a donor-funding bridge in parallel as a hedge, refuses to automate
        a 32-person referral list before a manual pass proves the channel, and flags that a B2B2G
        pilot's 6–8 week lead time consumes the entire 8-week window.""",
        thin="""<strong>🔴 Three required pieces are missing.</strong> There is no reflective
        response at all. There is no AI-use disclosure anywhere. And his plan says "logs into the
        tracker — see spreadsheet," but <strong>his workbook contains only analysis tabs; there is
        no tracker in it.</strong> The brief asked for one explicitly.<br><br>
        <strong>He gives no probability.</strong> He writes "moderate, not high or low" and
        declines a number. His conditional reasoning beats most candidates' numbers, but it is not
        what was asked.<br><br>
        He states the teacher-training-college explanation as <em>"confirmed, not inferred"</em>,
        citing partner knowledge he cannot have from this dataset. The conclusion happens to be
        well supported — but presenting an external assumption as established fact is the habit
        that produces confident wrong answers.""",
        probes=[
            "You called the Sri Lanka explanation confirmed rather than inferred. What confirmed "
            "it, and what would you have done if you were wrong?",
            "There's no reflection, no AI disclosure and no tracker. Walk us through how you "
            "managed the time-box.",
            "You wouldn't give a probability. Give me one now, and tell me what moves it.",
        ],
    ),
    dict(
        name="Arooj Khalid", app="3868", total=70, band="YES", proceed=True,
        colour="#2f6fb5", scores=[4, 4, 3, 2, 4, 4],
        link="https://drive.google.com/drive/folders/1NOH-IiWtGST8oNPgNL48E5L5PYYx3dxN",
        stands_out="""The best feature-level read in the pool. She compared all four features on
        identical terms and <strong>used medians deliberately to stop outliers skewing it</strong>
        — the only candidate to make that choice explicit. It led her to the right conclusion:
        lesson plans and presentations "behave like one-time utilities" (73% and 88% single-use),
        while coaching and reading users return.<br><br>
        She then found something nobody else did: <strong>teachers who have used lesson plans
        adopt coaching at 12.9%, roughly double the 6.4% base</strong> — a warm audience hiding
        inside the feature she correctly dismissed. Verified exact (22 of 170). Her AI note is the
        most candid of the eight.""",
        thin="""<strong>No probability on the deal.</strong> The brief asked explicitly; she says
        "at risk rather than committed," which is directionally right but not the number
        requested.<br><br>
        She wrote Assignment 3 part 3 as an <em>email to the Head of Growth</em> rather than an
        internal update, which softens it into a status note. Her DEO email attaches a helpful
        draft selection letter but states "we agreed to scale it up to 200 schools" as settled
        fact when the whole problem is that the commitment was only verbal.<br><br>
        She recommends doubling down on Sri Lanka — not marked down, because she pairs it with a
        diagnostic designed to settle the question before spending. She missed the Nov 14 cohort
        entirely.""",
        probes=[
            "You were asked for a probability and didn't give one. Give me a number now, and tell "
            "me what it's based on.",
            "You found lesson-plan users adopt coaching at twice the base rate. How do you turn "
            "that into revenue rather than engagement?",
            "You'd double down on Sri Lanka. 52% of its registered users teach university only, "
            "and coaching needs a real classroom. Does that change your answer?",
        ],
    ),
    dict(
        name="Irfan Siddiqui", app="4144", total=53, band="BORDERLINE", proceed=False,
        colour="#c47f16", scores=[3, 3, 2, 2, 4, 2],
        link="https://drive.google.com/drive/folders/10CM1Mvz7YgO8hS0dOOU4sx0LWhr69Y4B",
        stands_out="""One piece of genuinely original digging: he broke the Pakistan registration
        funnel down by state and found <strong>23 users whose WhatsApp template never delivered
        and 52 who opened the registration flow and abandoned it</strong> — 75 addressable stuck
        leads nobody else noticed. Verified exact. His kill criteria are the most rigorous in the
        pool and the only ones written as compound falsifiable conditions.""",
        thin="""<strong>🔴 His DEO email presents Alpha Platform's dataset figures as results from
        the 40-school pilot.</strong> "275 lesson plans, 105 presentations, 88 coaching sessions"
        are platform-wide totals from a different scenario. Worse, he writes <strong>"59% of
        students assessed are now reading at or above grade level"</strong> — 59% is the reading
        assessment <em>completion rate</em> (51 of 87), not a proficiency measure. He labels them
        placeholder assumptions, so this is not fabrication under our rubric, but sending
        mislabelled statistics to a government official is the error that ends a relationship
        permanently — and he repeats the same figures unlabelled in the internal update.<br><br>
        <strong>His Assignment 1 walks into the central trap</strong>, picking lesson plans and
        presentations as leverage areas because they have the most users. He is also internally
        inconsistent: slide 1 says "need to focus on coaching and reading," slide 3 then selects
        lesson plans instead.<br><br>
        Slides 4 and 5 are empty headings; the experiments exist in the workbook rather than the
        deck, so the content is there but the package is disorganised. No probability on the deal
        at all.""",
        probes=[
            "In your DEO email you cite 59% of students reading at or above grade level. Where "
            "does that number come from?",
            "You chose lesson plans and presentations. 73% and 88% of those users never came "
            "back. Talk me through that.",
            "Slide 1 says focus on coaching; slide 3 picks lesson plans. Which is it?",
        ],
    ),
    dict(
        name="Syed Basit Hussain", app="4142", total=46, band="NO", proceed=False,
        colour="#b3261e", scores=[3, 2, 2, 2, 3, 2],
        link="https://drive.google.com/drive/folders/1ENRRftnC4SLDykVG3nSeE2pacNUGEQMi",
        stands_out="""Clean, correctly sourced arithmetic — 265/261 users, 43.8% vs 45.6%
        registration, 34 coaching users in Pakistan against zero in Sri Lanka. He correctly
        identifies that coaching and reading users are 4–5× more engaged on every retention
        measure, and his executive recommendation — deepen engagement rather than expand reach —
        is the right high-level call.""",
        thin="""<strong>The plan is strategy restated, not execution.</strong> "Conduct teacher
        orientation sessions," "send automated reminders," "present coaching outcomes" would fit
        any company selling anything. Owners are department names rather than a person doing a
        specific thing on a specific day, and no phase has an exit criterion. For a role whose JD
        leads with hands-on execution, this is the dimension that matters most and it is the
        weakest.<br><br>
        <strong>His tracker is two example rows and a dropdown list.</strong><br><br>
        <strong>65% probability is the clearest judgment error in the pool.</strong> Six weeks of
        silence, nothing in writing, no verified procurement stage, five weeks to close, an active
        competitor — and he calls it more likely than not, with no gating events either
        way.<br><br>
        His second deck, "made through NotebookLM," is <strong>eight slides with no extractable
        text</strong> — images only. No AI-use disclosure anywhere despite naming NotebookLM in
        his submission note. His reflection describes flagging a risk that then materialised
        anyway.""",
        probes=[
            "You put 65% on a deal with six weeks of silence and nothing in writing. Defend it.",
            "Your week-2 action is 'ensure every teacher completes their first coaching session.' "
            "It's Monday morning. What do you actually do?",
            "You used NotebookLM but disclosed no AI use. What was AI and what was you?",
        ],
    ),
]

BLOCKED = []


def stat_boxes():
    boxes = [("8", "Submitted", "#1a2b4c"), ("8", "Scored", "#2f6fb5"),
             ("6", "Recommended", "#1b7f4d"), ("3", "Flagged", "#b3261e")]
    tds = "".join(
        f'<td style="width:25%;padding:6px;"><div style="background:{c};border-radius:6px;'
        f'padding:16px 8px;text-align:center;">'
        f'<div style="font-family:Georgia,serif;font-size:28px;color:#fff;font-weight:bold;">{n}</div>'
        f'<div style="font-family:Arial,sans-serif;font-size:11px;color:#dbe5f5;'
        f'letter-spacing:0.8px;text-transform:uppercase;margin-top:4px;">{l}</div></div></td>'
        for n, l, c in boxes)
    return ('<table role="presentation" width="100%" style="width:100%;border-collapse:collapse;'
            f'margin:18px 0;"><tr>{tds}</tr></table>')


def ranked_table():
    head = "".join(f'<th style="background:#1a2b4c;color:#fff;padding:8px 6px;font-size:11px;'
                   f'text-align:center;">{d}</th>' for d in DIMS)
    rows = []
    for i, c in enumerate(CANDS):
        nm = (f'<a href="{c["link"]}" style="color:#2f4fa2;">{c["name"]}</a>'
              if c["link"] else c["name"])
        cells = "".join(
            f'<td style="text-align:center;padding:8px 6px;border-bottom:1px solid #e6e9ef;">{s}</td>'
            for s in c["scores"])
        rows.append(
            f'<tr style="background:{"#ffffff" if i%2==0 else "#f5f7fa"};">'
            f'<td style="padding:8px 10px;border-bottom:1px solid #e6e9ef;">{nm}<br>'
            f'<span style="font-size:11px;color:#6b7a90;">App {c["app"]}</span></td>'
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


def deep_dives():
    out = []
    for c in CANDS:
        probes = "".join(f'<li style="margin:6px 0;">{p}</li>' for p in c["probes"])
        verdict = ("PROCEED to case study debrief" if c["proceed"]
                   else "DO NOT proceed to debrief")
        vcol = "#1b7f4d" if c["proceed"] else "#b3261e"
        out.append(f"""
<div style="border:1px solid #dfe3ea;border-radius:8px;margin:22px 0;overflow:hidden;">
  <div style="background:{c['colour']};padding:14px 20px;">
    <span style="font-family:Georgia,serif;font-size:19px;color:#fff;">{c['name']}</span>
    <span style="font-family:Arial,sans-serif;font-size:13px;color:#e4ecf8;">
      &nbsp;&middot;&nbsp; App {c['app']} &nbsp;&middot;&nbsp; {c['total']}/100 &nbsp;&middot;&nbsp; {c['band']}</span>
  </div>
  <div style="padding:18px 20px;">
    <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1.2px;
                text-transform:uppercase;color:#1b7f4d;font-weight:bold;">What stands out</div>
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.7;color:#22303f;margin:8px 0 18px;">
      {c['stands_out']}</p>
    <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1.2px;
                text-transform:uppercase;color:#b3261e;font-weight:bold;">What is thin</div>
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.7;color:#22303f;margin:8px 0 18px;">
      {c['thin']}</p>
    <div style="background:{vcol};color:#fff;padding:9px 14px;border-radius:5px;
                font-family:Arial,sans-serif;font-size:13px;font-weight:bold;margin-bottom:14px;">
      {verdict}</div>
    <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1.2px;
                text-transform:uppercase;color:#2f4fa2;font-weight:bold;">Debrief probes</div>
    <ol style="font-family:Georgia,serif;font-size:14.5px;line-height:1.65;color:#22303f;
               margin:8px 0 0;padding-left:20px;">{probes}</ol>
  </div>
</div>""")
    return "".join(out)


def build_html():
    blocked_rows = "".join(
        f'<li style="margin:4px 0;">{n} — App {a}</li>' for n, a in BLOCKED)
    return f"""<!--[if mso]><table role="presentation" width="820" align="center"><tr><td><![endif]-->
<div style="background:#eef1f6;padding:22px 12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
       style="width:100%;max-width:820px;margin:0 auto;background:#ffffff;border-radius:8px;
              border:1px solid #dfe3ea;">
 <tr><td style="background:#1a2b4c;padding:24px 30px;border-radius:8px 8px 0 0;">
   <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1.6px;
               text-transform:uppercase;color:#93a7c9;">Taleemabad &middot; Talent Acquisition</div>
   <div style="font-family:Georgia,serif;font-size:23px;color:#fff;margin-top:6px;">
     SMG Case Study — Evaluation Report</div>
   <div style="font-family:Arial,sans-serif;font-size:13px;color:#c3d0e6;margin-top:8px;">
     Job 42 &middot; Senior Manager Growth &middot; 16 August 2026</div>
 </td></tr>
 <tr><td style="padding:24px 30px 34px;">

  {stat_boxes()}

  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:26px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Ranking</h2>
  {ranked_table()}
  <p style="font-family:Arial,sans-serif;font-size:12px;color:#6b7a90;margin:8px 0 0;">
    Dimensions scored 1–5. Weights: Data 20% &middot; Execution 25% &middot; Stakeholder 20%
    &middot; Commercial 15% &middot; Discipline 10% &middot; Signal 10%.</p>

  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 4px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Candidate detail</h2>
  {deep_dives()}

  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Method &amp; limits</h2>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    Scored against the benchmark answer and rubric sent earlier today. Every headline figure
    each candidate cited was recomputed from the raw Alpha Platform CSVs — Shahmir's failure
    rate and language finding, Arooj's lesson-plan-to-coaching bridge, Irfan's registration
    funnel, and Umar's cohort figures all check out exactly. <strong>No candidate fabricated
    data.</strong></p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>All eight are now scored.</strong> The three that were blocked behind Markaz's
    staff-login endpoint were retrieved from the "New Case Study Received" notification emails,
    which carry every submitted document as an attachment. That route makes the 401 wall
    irrelevant for good — it is now the standard first step, not a fallback.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Two further limits.</strong> Shahmir's reflection is a voice note I cannot
    transcribe, so one of his six dimensions is unassessed and his score is provisional on it.
    Basit's second deck is image-only, so I judged his Assignment 1 on his primary deck alone.
    And I read Umar's submission before the benchmark was written, as flagged this morning.</p>

 </td></tr>
 <tr><td style="background:#f5f7fa;padding:16px 30px;border-top:1px solid #dfe3ea;
        border-radius:0 0 8px 8px;font-family:Arial,sans-serif;font-size:12px;color:#6b7a90;">
   Taleemabad Talent Acquisition &middot; hiring@taleemabad.com &middot; 16 August 2026</td></tr>
</table></div>
<!--[if mso]></td></tr></table><![endif]-->"""


def main():
    load_dotenv(os.path.join(ROOT, ".env"))
    pw = os.getenv("EMAIL_PASSWORD")
    if not pw:
        raise SystemExit("EMAIL_PASSWORD missing")
    html = build_html()
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = ", ".join(RECIPIENTS)
    msg.attach(MIMEText("HTML report — view in an HTML-capable client.", "plain"))
    msg.attach(MIMEText(html, "html"))
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER, pw)
    safe_sendmail(s, SENDER, RECIPIENTS, msg.as_string(), context="smg_case_study_evaluation")
    s.quit()
    print(f"Sent to {RECIPIENTS} — {len(html):,} chars")


if __name__ == "__main__":
    main()
