"""
SMG Case Study Evaluation — ROUND 3 (Job 42) — DEEP READ — PILOT to Ayesha.

Ayesha, 2026-08-30: re-check for new submissions since the round-2 report (24 Aug), evaluate,
send the report.

WHAT CHANGED SINCE ROUND 2
  - Two new Markaz submissions: Vaneeza Tashfeen Baig (app 4033, 25 Aug) and Ali Wajdan Khan
    (app 3977, 29 Aug).
  - Only ONE is evaluable. Ali Wajdan's submission is a Google Doc link that is not shared with
    anyone: Ayesha's own account gets 404, anonymous gets 401, and no email carries the files.
  - Muhammad Ahmad Taj (app 3971) is still unretrievable, 11 days on.
  - Khushal Khan (app 4134) is sending repeated access requests for the case-study document
    itself and so has not been able to start.

METHOD (unchanged, so all three rounds are comparable)
  - Same benchmark answer key, same six-dimension rubric, same weights as 17 Aug and 24 Aug.
    Nothing from any round has been added to the benchmark.
  - Every deliverable read end to end; every spreadsheet tab opened with formulas preserved.
  - Every headline figure recomputed from the raw 546-row master dataset, not from our own
    summary table.

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
SUBJECT = "[PILOT - ] SMG Case Study - Evaluation Report, Round 3 | Job 42"

DIMS = ["Data", "Execution", "Stakeholder", "Commercial", "Discipline", "Signal"]

CANDS = [
    dict(
        name="Vaneeza Tashfeen Baig", app="4033", total=82, band="STRONG YES", proceed=True,
        colour="#1b7f4d", scores=[4, 4, 4, 4, 5, 4],
        link="https://drive.google.com/drive/folders/1_N7n0dgdTNQUzouhlT2M2tUC1IUW_xMo",
        docs=[
            ("Assignment 1 Memo", "DOCX", "Noise / signal / two priorities, then three experiments as full hypothesis-action-metric-kill tables."),
            ("Assignment 1 Working", "XLSX, 6 sheets, live formulas", "Raw Data (547 rows), Country Comparison, Feature Stickiness, Registration Funnel, Burst vs Trickle Signups, Other Countries. The analysis re-derives inside the file."),
            ("Assignment 2 Memo", "DOCX", "60-day plan in four dated phases, stakeholder-layer table, K-factor definition, two break points."),
            ("Assignment 2 Tracker", "XLSX, 3 sheets, live formulas", "Loop Tracker (one row per teacher-to-school chain, auto days-in-stage), Weekly Metrics with a 4-week rolling K-factor, and a Head of Growth update template."),
            ("Assignment 3 Memo", "DOCX", "Five-week plan, the DEO email, internal update."),
            ("Reflection", "DOCX", "Separate file."),
        ],
        docs_note="Submitted 25 August via Markaz (app 4033) as a Drive folder link, six deliverables. Her status still reads <em>case_study_sent</em> in Markaz rather than submitted, so she does not appear as a submitter on the status field alone.",
        a1="""<strong>The most methodologically careful analysis of the three rounds, and it comes
        from one decision.</strong> Every other candidate compared Pakistan and Sri Lanka on the full
        six-week window. She noticed that <strong>157 of Sri Lanka's 261 users signed up in the final
        eight days</strong> and refused to compare a six-week-old market with a two-week-old one. So
        she rebuilt the comparison <em>at matched maturity</em>, restricting both countries to users
        with 14+ days of tenure. Every figure she reports from that cut is exact: Pakistan 41%
        registration against Sri Lanka's 47%; 3.6 sessions against 2.0; 6.2 days of lifespan against
        3.8; and <strong>16.5% of mature Pakistani users have tried coaching against 0% in Sri
        Lanka.</strong>
        <br><br>That produces a conclusion nobody else reached: <em>"Sri Lanka looks weak on the
        surface... This is a two-week-old market on this data, not an underperforming one. I'm
        treating it as 'not yet tested' rather than noise, because those two calls lead to very
        different next steps."</em> The benchmark flags right-censoring as a caveat. She turned it
        into the argument.
        <br><br>On the core feature she is equally exact: 35 adopters (6.4%), averaging 8.7 sessions
        and a 12.5-day lifespan against 1.5 sessions and 1.2 days for chat-only users, and
        <strong>33 of 35 complete once they start (94%)</strong>. Her read:
        <em>"This isn't a feature that might work, it actually does work. The problem is simply that
        we haven't reached most of the user base yet."</em>""",
        a1_noise="""Three things, each sized. <strong>Chat-only users: 294 of 546, 54% of the
        base</strong>, at 1.5 sessions and 1.2 days &mdash; <em>"This group isn't one that warrants a
        strategy, since it reflects the natural outcome for anyone who is never directed to a feature
        with genuine pedagogical value."</em> The ten-country long tail, which she puts at 25 users
        (it is 20). And she explicitly declines to call Sri Lanka noise, giving her reason.""",
        a1_pri="""(1) <strong>Coaching distribution inside Pakistan</strong> &mdash; framed not as a
        product problem but a distribution one: <em>"Distribution problem on a feature that's already
        proven... Only 1 in 6 mature Pakistan users has tried it."</em>
        (2) <strong>Recovering the 206 users stuck mid-registration</strong> &mdash;
        <strong>180 flow_sent + 26 template_send_failed = 38% of the entire base</strong>, all four
        figures exact. Her case for it is the sharpest commercial argument in the round:
        <em>"These aren't cold leads... They showed up and used the product; something in the
        registration mechanics stopped them finishing. Recovering even 20&ndash;30% of this group is
        very likely cheaper than acquiring 60&ndash;70 fresh users."</em> No candidate in any round
        sized the stalled-registration segment as a growth lever with its own experiment.""",
        a1_exp="""Three, each a full table, and the <strong>kill criteria are the best-written of the
        fourteen submissions</strong> because two of them redirect the work rather than ending it.
        (1) <strong>Coaching nudge to Pakistan's 83 registered non-adopters</strong>, sent as a real
        voice note rather than a description. Kill below 8%, <em>"roughly double the ambient organic
        rate"</em> &mdash; and then: <em>"the blocker isn't awareness it's something structural...
        Stop iterating on message copy and go interview 10 non-adopters directly instead."</em>
        (2) <strong>Registration recovery</strong>, starting with the 26 template failures as
        <em>"the cleanest technical fix"</em> and a one-tap resume link for the rest. Kill under 10
        percentage points: <em>"this is a relevance problem, not a delivery one."</em>
        (3) <strong>Test coaching in Sri Lanka before writing it off</strong>, benchmarked against the
        16.5% Pakistan mature baseline.""",
        a2="""<strong>Correctly sized to the actual base.</strong> She opens by naming it:
        33 completers, <em>"not thousands of people. That's why this plan is intentionally carried
        out by hand and in a personal manner during the first few weeks. I don't believe the loop can
        run itself at this stage."</em> Four dated phases with her as named owner, and a deliberate
        succession plan &mdash; <em>"from week 3 a field associate has been shadowing me so that by
        the third phase there is not a bottleneck due to it being a one-person operation."</em>
        <br><br>The operational inventions are real: a one-page <strong>highlight card</strong> built
        from the teacher's own before-and-after coaching language; <strong>"session-in-a-box"</strong>,
        a fixed 45&ndash;60 minute format needing no per-school preparation, <em>"This eliminates the
        biggest source of difficulty, namely getting a yes followed by weeks of silence"</em>;
        same-day booking links; QR self-registration <em>during</em> the session so onboarding never
        depends on follow-up; and a hard rule that <em>"no chain sits untouched for more than 10 days
        without a decision to mark it stalled or dead."</em>""",
        a2_k="""<strong>K = i &times; c</strong>, where i is admin conversations plus peer shares per
        activated teacher that week, and c is the share of those invite events converting to a new
        activated teacher or school. What lifts it above the field is the honesty about timing:
        <em>"the full chain realistically takes 3&ndash;6 weeks to close end to end, so a single
        week's K-factor is noisy &mdash; the tracker computes a 4-week rolling figure, and that's the
        number I'd actually trust."</em> Target is <strong>rolling K &ge; 0.20 by week 9&ndash;10,
        once 2&ndash;3 full cycles have had time to close</strong> &mdash; the only candidate who
        noticed that a 60-day plan cannot honestly report a converged K-factor at day 60. The tracker
        computes both the weekly and the rolling figure.""",
        a2_breaks="""(1) <em>"The teacher gets a real win &rarr; admin never notices... it's the one
        truly passive link in the whole chain."</em> Contingency: build the highlight card and reach
        the admin herself once a teacher hits two completed sessions &mdash;
        <em>"treat noticing as something I manufacture, not something I hope for."</em>
        (2) <em>"Admin says yes &rarr; the session never actually gets scheduled. Classic pipeline
        death by school calendar and competing priorities, a verbal yes quietly evaporates."</em>
        Contingency: fixed format, booking attempt within 24 hours, day-5 and day-10 cadence.""",
        a3_prob="30&ndash;40% for the full 200 schools; 60&ndash;70% for a partial commitment that keeps next year open.",
        a3="""Opens on the right instinct &mdash; <em>"reopen the side doors not the front door"</em>
        &mdash; and works procurement, the district focal person and two or three pilot head teachers
        before going near the DEO, specifically to collect <em>"current proof, not three-month-old
        pilot numbers."</em> If the DEO does not reply in 5&ndash;7 working days she does not call
        again; she routes through the focal person <em>"framed as making it easier for the DEO's
        schedule, not as going around them."</em> Week 3 asks for <strong>time, not an answer</strong>,
        and prepares the phased fallback in parallel rather than after failure. Week 5 forces a
        written outcome: <em>"A real 'not this cycle' is more useful than open-ended silence."</em>
        She also keeps visiting schools throughout because <em>"those relationships hold value on
        their own and are the actual thing the competitor is trying to take."</em>""",
        a3_email="""Content-first and genuinely well judged in its body. It leads with new
        information rather than a request &mdash; teachers at pilot schools have carried on using
        coaching <em>"without any advice or encouragement from us, which is generally the best
        indication that something has really taken hold rather than merely benefiting from the
        initial enthusiasm of the pilot phase."</em> It removes work rather than adding it
        (<em>"we can put together a short written summary... in whatever form is most useful for you
        to share upward"</em>), asks for 15&ndash;20 minutes, and offers to travel to the DEO's
        office. It closes by crediting the DEO's team for the pilot result.
        <strong>It never mentions the five-week budget deadline.</strong>""",
        a3_internal="""Two probabilities rather than one, which is the more useful thing to hand a
        Head of Growth, and a reasoned read of the silence: <em>"if a government stakeholder truly
        lost an interest they would either send a clear message or it would be the junior staff who
        picked up on it, never just complete silence right after a public, on-record endorsement."</em>
        She then checks herself &mdash; <em>"That said, I'm not going to exaggerate the situation
        either"</em> &mdash; and lands on 30&ndash;40% full, 60&ndash;70% partial. Two asks, both
        specific: a peer-level contact if procurement and the focal person are both silent after two
        weeks, and <strong>pre-approved authority for the phased option</strong>, with the reason
        stated plainly: <em>"preferably I should have that authority already rather than lose two days
        asking for it as the deadline approaches."</em>""",
        reflection="""At Teach For Pakistan she was asked to fix an alumni database that senior
        management used to track long-term programme impact. She kept patching it, then stopped:
        <em>"the problem wasn't just a few faulty formulas, since the entire structure lacked a clear
        logic, and as a result every modification I made had simply added another level of
        confusion."</em> She told her manager that continuing to edit would not fix it and proposed a
        rebuild, which took a month and became the standard reference. The lesson is the right one
        &mdash; <em>"the need to recognise the sunk-cost instinct as early as possible, before having
        spent months defending a flawed approach"</em> &mdash; and she was arguing against her own
        completed work. It is a systems-and-tooling story rather than a strategy failing in the field,
        which is what the brief asks for, and the personal cost is lower than the strongest
        reflections in the pool.""",
        verified="""Recomputed from the raw 546-row dataset and exact: 35 coaching adopters at 6.4%;
        8.7 average sessions and 12.5-day lifespan; 33 of 35 completing (94%); 157 of Sri Lanka's 261
        signing up 8&ndash;16 December; the entire matched-maturity table for both countries
        (41%/3.6/6.2/16.5% and 47%/2.0/3.8/0%); 226 users across her three spike days (41% of the
        base); 64% versus 30% registration and 10.18% versus 3.75% coaching on those days; 180
        flow_sent and 26 template_send_failed at 2.4 and 1.5 sessions, 206 combined, 38% of the base;
        and 83 Pakistani registered users who never touched coaching. Two trivial slips: chat-only is
        294 not 296, and the long tail is 20 users not 25. <strong>Nothing is fabricated.</strong>
        AI use is disclosed per deliverable and is specific about what Claude did against what she
        decided.""",
        thin="""<strong>One real analytical error, and it sits on the most important fact in the
        dataset.</strong> She groups 14 November, 26 November and 11 December together as three
        high-conversion days and concludes that <em>"whatever caused those days... led to better-quality
        users, not just a higher number of users."</em> Her arithmetic is right &mdash; those 226
        users do register at 64% and adopt coaching at 10.2%. But the day-level split is
        <strong>14 Nov: 23 coaching adopters. 26 Nov: zero. 11 Dec: zero.</strong> Every adopter in
        her group comes from one of the three days, and the other two produced 186 users and no
        coaching adoption at all. Grouping them averages a two-thirds concentration into a blended
        rate and hides the single most actionable finding in the data &mdash; that one day out of five
        institutional events produced 23 of the platform's 35 coaching adopters. Her own instinct was
        right (<em>"When I first looked at it, I thought, 'spike, discount it'"</em>); the correction
        went one step too far.
        <br><br><strong>The attribution gap is never named.</strong> The source column reads "direct"
        for all 546 users, so the channel experiments she proposes could not be attributed as
        designed.
        <br><br><strong>The DEO email omits the deadline.</strong> Deliberate, given her content-first
        framing, but the five-week budget close is the entire constraint of the scenario and the email
        gives the DEO no reason to reply this week rather than next month.
        <br><br><strong>Consent is not raised.</strong> Her highlight card carries a named teacher's
        before-and-after coaching language to that teacher's administrator. She does ask the teacher
        to forward it or agree first, which is better than most, but the permission question is never
        made explicit.""",
        probes=[
            "Your three high-conversion days produced 23 coaching adopters. All 23 signed up on 14 November; 26 November and 11 December produced 186 users and zero. What does that change about which day you would try to replicate, and how?",
            "Matched maturity was the sharpest call in your submission. Walk me through the moment you decided the raw country comparison was misleading, and what you nearly concluded before that.",
            "Your highlight card sends a named teacher's coaching feedback to their head teacher. What do you tell that teacher before their first recording, and what happens to the loop if one of them feels caught out?",
        ],
    ),
]


def stat_boxes():
    boxes = [("2", "New submissions", "#1a2b4c"), ("1", "Evaluable", "#2f6fb5"),
             ("6", "Documents read", "#1b7f4d"), ("3", "Blocked", "#b3261e")]
    tds = "".join(
        f'<td style="width:25%;padding:6px;"><div style="background:{c};border-radius:6px;'
        f'padding:16px 8px;text-align:center;">'
        f'<div style="font-family:Georgia,serif;font-size:26px;color:#fff;font-weight:bold;">{n}</div>'
        f'<div style="font-family:Arial,sans-serif;font-size:10.5px;color:#dbe5f5;'
        f'letter-spacing:0.8px;text-transform:uppercase;margin-top:4px;">{l}</div></div></td>'
        for n, l, c in boxes)
    return ('<table role="presentation" width="100%" style="width:100%;border-collapse:collapse;'
            f'margin:18px 0;"><tr>{tds}</tr></table>')


def sec(label, colour, body):
    return (f'<div style="font-family:Arial,sans-serif;font-size:10.5px;letter-spacing:1.2px;'
            f'text-transform:uppercase;color:{colour};font-weight:bold;margin-top:20px;">{label}</div>'
            f'<p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;'
            f'margin:7px 0 0;">{body}</p>')


def doc_table(c):
    rows = "".join(
        f'<tr><td style="padding:6px 10px 6px 0;font-family:Georgia,serif;font-size:13.5px;'
        f'color:#1a2b4c;font-weight:bold;vertical-align:top;">{n}</td>'
        f'<td style="padding:6px 10px 6px 0;font-family:Arial,sans-serif;font-size:12px;'
        f'color:#2f6fb5;vertical-align:top;white-space:nowrap;">{t}</td>'
        f'<td style="padding:6px 0;font-family:Georgia,serif;font-size:13.5px;color:#3d4c5c;'
        f'vertical-align:top;">{d}</td></tr>'
        for n, t, d in c["docs"])
    return (f'<div style="background:#f5f7fa;border-left:3px solid #2f6fb5;padding:12px 16px;'
            f'margin-top:14px;">'
            f'<div style="font-family:Arial,sans-serif;font-size:10.5px;letter-spacing:1.2px;'
            f'text-transform:uppercase;color:#1a2b4c;font-weight:bold;margin-bottom:6px;">'
            f'Submitted &mdash; {len(c["docs"])} documents</div>'
            f'<div style="overflow-x:auto;"><table role="presentation" style="border-collapse:collapse;">'
            f'{rows}</table></div>'
            f'<p style="font-family:Georgia,serif;font-size:13.5px;line-height:1.7;color:#3d4c5c;'
            f'margin:10px 0 0;">{c["docs_note"]}</p></div>')


def score_table(c):
    heads = "".join(f'<th style="background:#1a2b4c;color:#fff;padding:7px 10px;font-size:11px;">{d}</th>'
                    for d in DIMS)
    cells = "".join(f'<td style="text-align:center;padding:9px;border-bottom:1px solid #e6e9ef;'
                    f'font-size:15px;">{s}</td>' for s in c["scores"])
    return ('<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:16px;">'
            '<table role="presentation" style="width:100%;border-collapse:collapse;'
            'font-family:Arial,sans-serif;font-size:13px;">'
            '<tr><th style="background:#1a2b4c;color:#fff;padding:7px 10px;font-size:11px;">Total</th>'
            f'{heads}<th style="background:#1a2b4c;color:#fff;padding:7px 10px;font-size:11px;">Band</th></tr>'
            f'<tr><td style="text-align:center;padding:9px;border-bottom:1px solid #e6e9ef;'
            f'font-weight:bold;font-size:17px;">{c["total"]}</td>{cells}'
            f'<td style="text-align:center;padding:9px;border-bottom:1px solid #e6e9ef;">'
            f'<span style="background:{c["colour"]};color:#fff;padding:3px 8px;border-radius:3px;'
            f'font-size:10px;white-space:nowrap;">{c["band"]}</span></td></tr></table></div>'
            '<p style="font-family:Arial,sans-serif;font-size:12px;color:#6b7a90;margin:8px 0 0;">'
            'Weights: Data 20% &middot; Execution 25% &middot; Stakeholder 20% &middot; Commercial 15% '
            '&middot; Discipline 10% &middot; Signal 10%. Same benchmark, rubric and weights as the '
            '17 and 24 August reports.</p>')


def deep_dive(c):
    probes = "".join(f'<li style="margin:7px 0;">{p}</li>' for p in c["probes"])
    verdict = "PROCEED to case study debrief" if c["proceed"] else "DO NOT proceed to debrief"
    vcol = "#1b7f4d" if c["proceed"] else "#b3261e"
    return f"""
<div style="border:1px solid #dfe3ea;border-radius:8px;margin:26px 0;overflow:hidden;">
  <div style="background:{c['colour']};padding:14px 20px;">
    <span style="font-family:Georgia,serif;font-size:19px;color:#fff;">
      <a href="{c['link']}" style="color:#fff;text-decoration:underline;">{c['name']}</a></span>
    <span style="font-family:Arial,sans-serif;font-size:13px;color:#e4ecf8;">
      &nbsp;&middot;&nbsp; App {c['app']} &nbsp;&middot;&nbsp; {c['total']}/100 &nbsp;&middot;&nbsp; {c['band']}</span>
  </div>
  <div style="padding:18px 20px 22px;">
    {score_table(c)}
    {doc_table(c)}
    {sec("Assignment 1 &mdash; what the analysis actually says", "#1b7f4d", c['a1'])}
    {sec("Assignment 1 &mdash; what she called noise", "#6b7a90", c['a1_noise'])}
    {sec("Assignment 1 &mdash; the two priorities she chose", "#1b7f4d", c['a1_pri'])}
    {sec("Assignment 1 &mdash; the three experiments", "#2f4fa2", c['a1_exp'])}
    {sec("Assignment 2 &mdash; the growth loop", "#2f4fa2", c['a2'])}
    {sec("Assignment 2 &mdash; how she measures K", "#2f4fa2", c['a2_k'])}
    {sec("Assignment 2 &mdash; where she says it breaks", "#2f4fa2", c['a2_breaks'])}
    <div style="background:#eef3fb;border-radius:6px;padding:10px 14px;margin-top:20px;
                font-family:Arial,sans-serif;font-size:13px;color:#1a2b4c;">
      <strong>Assignment 3 &mdash; her stated probability:</strong> {c['a3_prob']}</div>
    {sec("Assignment 3 &mdash; the five-week plan", "#7b341e", c['a3'])}
    {sec("Assignment 3 &mdash; the email to the DEO", "#7b341e", c['a3_email'])}
    {sec("Assignment 3 &mdash; the internal update", "#7b341e", c['a3_internal'])}
    {sec("Reflective response", "#5b3fc4", c['reflection'])}
    {sec("What I verified against the raw data", "#1b7f4d", c['verified'])}
    {sec("What is thin, missing or wrong", "#b3261e", c['thin'])}
    <div style="background:{vcol};color:#fff;padding:9px 14px;border-radius:5px;
                font-family:Arial,sans-serif;font-size:13px;font-weight:bold;margin:20px 0 14px;">
      {verdict}</div>
    <div style="font-family:Arial,sans-serif;font-size:10.5px;letter-spacing:1.2px;
                text-transform:uppercase;color:#2f4fa2;font-weight:bold;">Debrief probes</div>
    <ol style="font-family:Georgia,serif;font-size:14.5px;line-height:1.7;color:#22303f;
               margin:8px 0 0;padding-left:20px;">{probes}</ol>
  </div>
</div>"""


INTRO = """
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:6px 0 0;">
    Re-checked for submissions arriving after the 24 August report. <strong>Two came in
    &mdash; one can be assessed.</strong> Vaneeza Baig submitted six deliverables on 25 August and is
    scored in full below. Ali Wajdan Khan submitted on 29 August, but his link cannot be opened by
    anyone, so he is not scored here and nothing about his ability should be read into that.</p>
  <p style="font-family:Georgia,serif;font-size:13.5px;line-height:1.7;color:#1b4d3e;
            background:#eef7f1;border-left:3px solid #1b7f4d;padding:10px 14px;margin:14px 0 0;">
    <strong>Where she sits.</strong> Vaneeza scores <strong>82</strong>, which places her third of
    the fifteen candidates assessed across all three rounds &mdash; behind Shahmir Hashmat (98) and
    Arshan Bilal (94), level with Furqan Afzal (93) and Hania Khan (90) in band, and ahead of every
    other round-2 submission. She is a clear proceed.</p>"""

RUNNING = """
  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Running order &mdash; all 15 scored</h2>
  <div style="overflow-x:auto;-webkit-overflow-scrolling:touch;">
  <table role="presentation" style="width:100%;border-collapse:collapse;font-family:Arial,sans-serif;font-size:13px;">
    <tr><th style="background:#1a2b4c;color:#fff;padding:8px 10px;text-align:left;">Candidate</th>
        <th style="background:#1a2b4c;color:#fff;padding:8px;font-size:11px;">Score</th>
        <th style="background:#1a2b4c;color:#fff;padding:8px;font-size:11px;">Band</th>
        <th style="background:#1a2b4c;color:#fff;padding:8px;font-size:11px;">Round</th></tr>
    <tr style="background:#fff;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Shahmir Hashmat</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">98</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Strong yes</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">1</td></tr>
    <tr style="background:#f5f7fa;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Muhammad Arshan Bilal</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">94</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Strong yes</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">1</td></tr>
    <tr style="background:#fff;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Furqan Afzal</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">93</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Strong yes</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">2</td></tr>
    <tr style="background:#f5f7fa;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Hania Khan</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">90</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Strong yes</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">2</td></tr>
    <tr style="background:#fff;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Yusra Amjad</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">89</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Strong yes</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">1</td></tr>
    <tr style="background:#fffbe6;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;"><strong>Vaneeza Tashfeen Baig</strong></td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">82</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Strong yes</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;"><strong>3</strong></td></tr>
    <tr style="background:#f5f7fa;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Umar Zahid</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">78</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Yes</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">1</td></tr>
    <tr style="background:#fff;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Shafaq Syed</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">75</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Yes</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">2</td></tr>
    <tr style="background:#f5f7fa;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Junaid Ali</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">74</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Yes</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">1</td></tr>
    <tr style="background:#fff;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Lamis Maniar</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">73</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Yes</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">2</td></tr>
    <tr style="background:#f5f7fa;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Arooj Khalid</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">70</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Yes</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">1</td></tr>
    <tr style="background:#fff;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Kanooz Ahmed Siddiqui</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">62</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Borderline</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">2</td></tr>
    <tr style="background:#f5f7fa;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Irfan Siddiqui</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">53</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">Borderline</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">1</td></tr>
    <tr style="background:#fff;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Syed Basit Hussain</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">46</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">No</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">1</td></tr>
    <tr style="background:#f5f7fa;"><td style="padding:7px 10px;border-bottom:1px solid #e6e9ef;">Rimsha Taj</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;font-weight:bold;">45</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">No</td><td style="text-align:center;border-bottom:1px solid #e6e9ef;">2</td></tr>
  </table></div>"""

BLOCKED = """
  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Three candidates blocked &mdash; all need a reply today</h2>
  <div style="background:#fff5f5;border-left:3px solid #b3261e;padding:12px 16px;margin:12px 0;">
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:0;">
      <strong>Ali Wajdan Khan (app 3977) &mdash; submitted 29 August, link not shared.</strong> His
      Markaz submission is a single Google Doc link.
      <strong>Your own account returns 404 on it and an anonymous request returns 401</strong>, so the
      document is restricted to him. No email in the mailbox carries the files. He has done the work
      and it simply cannot be opened. One line back asking him to set the link to "anyone with the
      link can view", or to email the files to hiring@, unblocks it.</p>
  </div>
  <div style="background:#fff5f5;border-left:3px solid #b3261e;padding:12px 16px;margin:12px 0;">
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:0;">
      <strong>Khushal Khan (app 4134) &mdash; cannot open the case study at all.</strong> The case
      study was sent on 28 August. He has since sent <strong>three separate Google Docs access
      requests</strong> for the brief itself, the most recent today, and emailed the thread. He has
      not been able to start. This is a permissions problem on the case-study document, not a
      candidate problem, and his clock should not start until he has access.</p>
  </div>
  <div style="background:#fdf6ec;border-left:3px solid #c47f16;padding:12px 16px;margin:12px 0;">
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:0;">
      <strong>Muhammad Ahmad Taj (app 3971) &mdash; still missing, 11 days on.</strong> Flagged in the
      24 August report and nothing has changed. Markaz records a submission on 19 August; his note
      says the work is in an attached ZIP; Markaz accepts Word and Excel only, so the upload failed
      silently. No files, no link, nothing in the mailbox. He cannot be scored until he resends.</p>
  </div>
  <div style="background:#f5f7fa;border-left:3px solid #2f6fb5;padding:12px 16px;margin:12px 0;">
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:0;">
      <strong>Still outstanding from the 7 August batch.</strong> Muhammad Zeshan Nawaz (app 3921) and
      Muhammad Bilal Sadiq (app 4051) were sent the case study on 7 August, 23 days ago, and have
      never submitted or been nudged. Both still read as <em>shortlisted</em> in Markaz.</p>
  </div>"""

METHOD = """
  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Method &amp; limits</h2>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    Scored against <em>smg_execution_sprint_benchmark.md</em> on the six-dimension rubric &mdash;
    the same key, the same weights and the same reader as the 17 and 24 August reports, so all
    fifteen scores are directly comparable. Nothing from any round has been added to the benchmark.
    All six of her deliverables were read end to end, both spreadsheets opened tab by tab with
    formulas preserved, and every headline figure recomputed from the raw 546-row master dataset
    rather than checked against our own summary table. Quotations are her own words.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>One process note worth acting on.</strong> Three of the last five SMG submissions have
    been unreadable on arrival for three different reasons &mdash; a ZIP that Markaz will not accept,
    a Drive link shared with nobody, and a portal upload that failed and had to come by email. The
    submission step, not the candidates, is where this pipeline is losing work. Asking candidates to
    upload Word and Excel directly, or to email hiring@ as a matter of course, would remove all three
    failure modes.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    Her six files are archived in the Senior Manager Growth submissions folder under her own
    subfolder, together with a Submission Links note recording the Markaz folder and the two working
    spreadsheets she linked from her memos.</p>"""


def build_html():
    return f"""<!--[if mso]><table role="presentation" width="880" align="center"><tr><td><![endif]-->
<div style="background:#eef1f6;padding:22px 12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
       style="width:100%;max-width:880px;margin:0 auto;background:#ffffff;border-radius:8px;
              border:1px solid #dfe3ea;">
 <tr><td style="background:#1a2b4c;padding:24px 30px;border-radius:8px 8px 0 0;">
   <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1.6px;
               text-transform:uppercase;color:#93a7c9;">Taleemabad &middot; Talent Acquisition</div>
   <div style="font-family:Georgia,serif;font-size:23px;color:#fff;margin-top:6px;">
     SMG Case Study &mdash; Evaluation Report, Round 3</div>
   <div style="font-family:Arial,sans-serif;font-size:13px;color:#c3d0e6;margin-top:8px;">
     Job 42 &middot; Senior Manager Growth &middot; 30 August 2026 &middot; Vaneeza Baig</div>
 </td></tr>
 <tr><td style="padding:24px 30px 34px;">
  {stat_boxes()}
  {INTRO}
  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 4px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Candidate detail</h2>
  {deep_dive(CANDS[0])}
  {RUNNING}
  {BLOCKED}
  {METHOD}
 </td></tr>
 <tr><td style="background:#f5f7fa;padding:16px 30px;border-top:1px solid #dfe3ea;
        border-radius:0 0 8px 8px;font-family:Arial,sans-serif;font-size:12px;color:#6b7a90;">
   Taleemabad Talent Acquisition &middot; hiring@taleemabad.com &middot; 30 August 2026</td></tr>
</table></div>
<!--[if mso]></td></tr></table><![endif]-->"""


def main():
    load_dotenv(os.path.join(ROOT, ".env"))
    pw = os.getenv("EMAIL_PASSWORD")
    if not pw:
        raise SystemExit("EMAIL_PASSWORD missing")
    html = build_html()
    size = len(html.encode())
    if size > 100_000:
        raise SystemExit(f"BLOCKED: {size:,} bytes - Gmail would clip it")
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER, pw)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = ", ".join(RECIPIENTS)
    msg.attach(MIMEText("HTML report - view in an HTML-capable client.", "plain"))
    msg.attach(MIMEText(html, "html"))
    safe_sendmail(s, SENDER, RECIPIENTS, msg.as_string(),
                  context="smg_case_study_evaluation_round3")
    print(f"Sent to {RECIPIENTS} - {size:,} bytes")
    s.quit()


if __name__ == "__main__":
    main()
