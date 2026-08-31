"""
SMG Case Study Evaluation Report v2 (Job 42) — DEEP READ — PILOT to Ayesha.

Ayesha's brief 2026-08-18: same template (she likes it), but far more detailed —
document count per candidate, and thorough enough that reading this replaces reading
the case study. Written for her AND the hiring manager.

WHAT CHANGED vs v1 (2026-08-17):
  - Every submission re-sourced and read END TO END this session: 16 files, 595,215
    characters. All six narrative documents read page by page; all six workbooks opened
    sheet by sheet with formula counts (live model vs pasted values).
  - Per-candidate document inventory with arrival route.
  - Assignment-by-assignment breakdown (A1 analysis, A1 experiments, A2 loop, A3 deal,
    reflection) rather than a single "what stands out" paragraph.
  - Scores UNCHANGED from v1 — this is a deeper write-up of the same evaluation, not a
    re-score. Two v1 caveats now resolved (see method note); no score moved.

HONEST LIMITS carried forward and stated in the report:
  - Shahmir's reflection is an .m4a voice note. Cannot be transcribed here. Ayesha's
    instruction 2026-08-18: "leave voice notes." 1 of his 6 dimensions stays unassessed.
  - Arooj's 60-day timeline visual and some in-doc charts are images; text extraction
    cannot read them, so they were not assessed.

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
SUBJECT = "[PILOT - ] SMG Case Study - Full Evaluation Report (deep read, all 6 shortlisted) | Job 42"

DIMS = ["Data", "Execution", "Stakeholder", "Commercial", "Discipline", "Signal"]

CANDS = [
    dict(
        name="Shahmir Hashmat", app="3911", total=98, band="STRONG YES", proceed=True,
        colour="#1b7f4d", scores=[5, 5, 5, 5, 5, 4],
        link="https://drive.google.com/drive/folders/1cUA0MpaOSDf47pCva6_gA45N97gKXuI7",
        docs=[
            ("Case Study Response", "PDF, 14 pages", "All three assignments in one document. Page 14 states the reflection is a voice note."),
            ("Assignment2_Growth_Loop_Tracker", "XLSX, 4 sheets, 60 formulas", "A live working model, not a blank template. No raw dataset included."),
        ],
        docs_note="Arrived as attachments on the Markaz submission notification, 15 August. His reflection is a separate <strong>.m4a voice note</strong> — not transcribable here, so 1 of 6 dimensions is unassessed and the 98 is provisional on it.",
        a1="""<strong>Three findings, each with the counter-argument built in.</strong>
        (1) <em>Coaching is the activation event and almost nobody reaches it.</em> Among Pakistani users
        observed 14+ days: coaching starters n=34 returned 97.1% with 5.38 active days and 8.29 sessions;
        non-starters n=172 returned 47.1% with 2.00 days and 2.71 sessions. Coaching reaches 6.4% of all
        users (35/546), reading 2.4% (13/546). Of 1,340 logged sessions, 946 are general chat and
        <strong>exactly one is audio coaching</strong>. He then volunteers the objection himself:
        <em>"engaged users do more of everything, so this correlation alone does not prove coaching causes
        retention"</em> — and says finding 2 is what makes him willing to act on it.
        (2) <em>The spikes are not one thing, and the aggregate hides it.</em> 14 Nov (n=40, 100% PK) returned
        87.5% with 57.5% reaching coaching; 2 Dec (n=35, <strong>also 97% PK</strong>) returned 20.0% with 0%
        coaching; organic (n=150) returned 54.0%. The 14 Nov cohort beat organic by 33 points and 2 Dec
        trailed it by 34 — and because both are Pakistani, <strong>country is controlled for</strong>. The
        variable that moves with the outcome is coaching. Conclusion: event <em>format</em>, not event count.
        (3) <em>Sri Lanka is half the user base and zero percent of the value.</em> 261 of 546 users, not one
        has touched either flagship. It <em>registers better</em> than Pakistan (47.1% vs 42.7%) —
        <em>"which is exactly why this is dangerous"</em> on any dashboard led by signups. Supporting detail
        no one else found: all 87 reading assessments are English or Urdu, so
        <strong>no Sinhala or Tamil passage exists</strong> and the flagship reading feature is not currently
        usable in a Sri Lankan classroom.""",
        a1_noise="""Names five things he refuses to treat as signal, with reasons: <strong>source is 100%
        "direct" for all 546 users</strong> so there is no channel attribution in the data at all and
        <em>"any best-channel claim would be invented"</em>; active_day1/week1 is true for 99% by
        construction; registration rate as a headline (Sri Lanka wins it and loses everything downstream);
        raw spike volume (11 Dec delivered 86 users, 8.1% returned); and every country outside PK/LK —
        UAE n=5 shows 40% reading adoption, Germany 100% registration, <em>"not yet decision-grade."</em>""",
        a1_pri="""(1) Close the Pakistan activation gap — 83.5% of Pakistani users never reach coaching.
        Inside this he separates a <strong>bug from a hypothesis</strong>: 27 of 118 coaching sessions failed
        (22.9%), median audio on failed sessions 38 minutes against 36 on completed ones, so it is
        <em>not</em> a length limit — <em>"a 23% failure rate on the one feature that drives retention is a
        bug to fix in week 1, not a hypothesis to test."</em>
        (2) Stop scaling Sri Lanka for 8 weeks and run a diagnostic instead — and he prices the move
        correctly: <em>"this is a decision to stop spending, which is cheaper and faster than any growth
        initiative on this list."</em>""",
        a1_exp="""<strong>E1 Coaching-first onboarding.</strong> Replace the open-chat welcome with a
        three-tap "record 10 minutes of your next class" flow, 50% held as control. Baseline 16.5% → target
        25%. Kill: below 12% after 3 weeks and 100+ treated users, <em>or</em> treatment return rate below
        control.<br>
        <strong>E2 Clinic vs demo at institutional events.</strong> Four events, two run as clinics where
        nobody leaves without a completed coaching session (he supplies devices and connectivity), two as
        control. Measures 14-day return by format <strong>and cost per retained teacher</strong> — "the
        number that decides whether this channel fits the model." Target clinics ≥60% vs ~25%; kill below
        35% across both, and then explicitly reallocates budget from field events into in-product activation.<br>
        <strong>E3 Sri Lanka diagnostic.</strong> Two parallel probes because the two candidate causes need
        opposite responses: DM 60 registered users segmented by whether they are actually classroom
        teachers, and ship one Sinhala plus one Tamil passage to a 40-user subset. Kill: under 5% adoption
        <em>and</em> fewer than half of respondents classroom teachers → channel-model mismatch, stop Sri
        Lankan acquisition entirely.""",
        a2="""<strong>He diagnoses the loop before planning it.</strong> Step 3 — "the administrator
        notices" — is passive, and everything else depends on it: <em>"coaching feedback lands privately on a
        teacher's WhatsApp and the head teacher never sees it."</em> So he inserts a deliberate artefact
        there: a monthly one-page school report built from teacher usage, delivered to the head teacher,
        with consent captured at registration. It <em>"converts private teacher value into visible
        institutional value, which is what makes an administrator ask."</em> All 8 loop steps get an action,
        an owner and a channel, and every session is run as a clinic rather than a demo — justified with the
        14 Nov vs 2 Dec contrast.<br><br>
        <strong>The sequencing rule is the best stakeholder insight in the pool:</strong> <em>"no layer hears
        about us first from the layer above. If a district official mandates us downward, teacher usage
        becomes compliance and the loop stops producing genuine advocacy — the only fuel it runs on."</em>""",
        a2_k="""K = i × c, <strong>split into two separately-measured paths</strong> (K_school from
        admin-invited whole-school sessions, K_peer from champion-teacher shares) and summed. Attribution via
        codes carried in WhatsApp deep links (<em>wa.me/&lt;number&gt;?text=JOIN-KHI042-T17</em>), with the
        honest note that source is "direct" for all 546 users today so <em>"building this is step one, not an
        optimisation."</em> Denominator discipline: "active teacher" = ≥1 completed coaching session in the
        trailing 30 days, <strong>applied to both sides of the ratio</strong> — <em>"counting registrations
        instead would overstate the loop: an inactive teacher refers no one."</em> Then he works the target
        backwards on actuals: base of 33 active teachers means K=0.2 needs ~7 loop-attributed activations per
        30 days (2 clinics × 10 teachers × 27% ≈ 5, plus 15 champions × 0.5 shares × 27% ≈ 2). And he
        caveats his own number: <em>"at n=33, K is volatile — a single good clinic swings it by 0.1"</em> — so
        30-day rolling, absolute activations tracked alongside, and he would not act on one week's movement.""",
        a2_breaks="""<strong>2→3, the improvement stays invisible</strong> (his named most-likely break, and
        the reason the school report exists). Contingency: if under 40% of seed-school admins engage with the
        report by day 30, stop relying on teacher-mediated visibility and deliver it in person — <em>"weaker
        than teacher-push, but it does not stall."</em><br>
        <strong>5→6, sessions convert attendance not activation.</strong> Contingency: if in-room activation
        falls below the observed 27% baseline, drop large sessions for clinics of 6–8 — <em>"eight activated
        teachers feed the loop, forty registered ones do not."</em>""",
        a3_prob="30–35% full 200 this cycle · ~70% keep the district in some form",
        a3="""<strong>The strongest Assignment 3 in the pool, and the only one that refuses to invent
        numbers.</strong> He labels six assumptions explicitly, then leaves [X], [Y], [A], [B] as placeholders
        in the DEO email rather than estimating pilot results, because <em>"inventing results to send a
        government official is the one thing that would end this relationship permanently."</em><br><br>
        His read on the silence: not a change of mind, but the file sitting at a desk the DEO does not
        control, no budget line to receive it, or an undecided procurement route — plus a transfer/posting
        change to rule out in week one. <em>"He is not avoiding me — he is avoiding a conversation in which he
        has no answer."</em> Every move follows from that.<br><br>
        Week 1 is titled <strong>"Find the file, not the DEO"</strong>: call the PA/reader and ask one
        question — which section holds the file and what is the diary number — while confirming the DEO is
        still in post. Exit criterion: <em>"I end the week knowing the name and designation of the officer
        physically holding the file."</em> Week 2 gets the blocker named in person with three procurement
        routes on a one-pager, lowest-approval route marked, and if it is budget, the exact line-item name and
        the Deputy Director Finance. Week 3 converts verbal to paper — <em>"a file cannot move without a
        document in it"</em> — and asks for exactly one thing: 15 minutes with the DEO <em>and</em> the
        procurement/finance officer together. Day 18 escalation trigger, but through an introduction:
        <em>"I do not escalate over a DEO without offering him the room first."</em> Week 4 adds a
        donor-funded parallel funding route, written agreement to continue the 40 schools regardless, and on
        the competitor — <strong>say nothing</strong>, defend incumbency through usage instead. Week 5:
        <em>"be physically present at the district office on the deadline days. Presence moves files and email
        does not."</em><br><br>
        Four rules he holds throughout: every touch delivers something; never make him account for the
        silence; shrink the ask until saying yes is trivial; always give him an exit to delegate.""",
        a3_email="""Subject: <em>"40 schools — 12-week results, and one small question."</em> Written to be
        <strong>forwarded as-is</strong> if that helps the DEO. Asks only which section holds the file, offers
        to work with someone on his team instead, frames the budget deadline as preparation rather than
        pressure, and closes on the head teachers still bringing it up. No mention of the competitor.""",
        a3_internal="""30–35% full expansion, ~70% retention in some form — and he states the number will
        <strong>move sharply in one direction</strong> at end of week 2: 55% if the file is located and a
        budget line exists, below 10% if no line item exists at all, at which point he stops spending time on
        the 200 and goes all-in on the fallback. <strong>He then owns his share of the failure unprompted:</strong>
        never converted the verbal commitment into a written proposal in week one so there was nothing in the
        file to move; single-threaded on the DEO with no relationship at procurement or finance; and never
        mapped the procurement path at pilot design stage — <em>"so we are learning the rules with five weeks
        left instead of five months."</em> Asks: one provincial call in week 4, authority to size and price a
        60–80 school Phase 2 without returning for sign-off (<em>"speed matters more than margin here"</em>),
        sign-off on refresher clinics, and donor-programme contacts.""",
        reflection="""<strong>Not assessed — voice note (.m4a).</strong> Per your instruction today, voice
        notes are left alone. This is the one dimension of his six that carries no evidence, which is why the
        98 is marked provisional.""",
        verified="""Every headline figure recomputed from the raw CSVs and matched exactly, including the
        22.9% coaching failure rate (27/118), the 38-vs-36 minute median audio comparison, and the
        all-English/Urdu reading assessment finding. He also caught two dataset problems in his AI-use note:
        the right-censoring issue and a broken user_id join in the child tables.""",
        thin="""The reflection is unassessed (voice note). His workbook contains <strong>no raw dataset and
        no analytical working</strong> — the analysis was run in Python via Claude outside the file, so the
        numbers are correct but <strong>not reproducible from what he submitted</strong>; his tracker is a
        live model, but a reviewer cannot re-derive his findings from his own deliverable. He is also the most
        AI-assisted of the strong submissions by his own disclosure, though he separates tool from judgement
        cleanly each time.""",
        probes=[
            "The 22.9% coaching failure rate — you called it a week-1 bug fix. Walk me through how you actually get that fixed when you do not own the engineering roadmap. Who do you go to, and what do you trade away?",
            "Your workbook has no raw data — the analysis lived in Python. If I ask you to defend the 57.5% coaching figure in a room with the Head of Product, what do you put on screen?",
            "You would hold Sri Lankan acquisition flat for 8 weeks. That is half our acquisition. Who has to agree to that internally, and how do you sell a stop-spending decision upward?",
            "Your sequencing rule says no layer hears about us first from the layer above. What do you do when a DEO wants to mandate us downward because it is faster for them?",
        ],
    ),
    dict(
        name="Muhammad Arshan Bilal", app="3884", total=94, band="STRONG YES", proceed=True,
        colour="#1b7f4d", scores=[5, 5, 4, 5, 5, 4],
        link="https://drive.google.com/drive/folders/1Ch4FlR5BApHRDneajESEffu6d1Erc6al",
        docs=[
            ("Taleemabad Execution Sprint response", "PDF, 14 pages", "All three assignments plus a reflection and a closing 'submission assumptions' section."),
            ("Spreadsheet working", "XLSX, 6 sheets, ~82 formulas", "Includes the master dataset. Country Analysis and Exec Summary are live formulas; Feature and Cohort tabs are pasted values; Growth Loop Tracker is a live but unpopulated template."),
        ],
        docs_note="Arrived as attachments on the Markaz submission notification, 7 August — the earliest submission of the six.",
        a1="""<strong>He builds his own metrics before analysing anything, because the given ones are
        broken.</strong> active_week1 is true for ~99% of users and therefore non-discriminating, so he
        defines "repeat" = active on ≥2 unique days and "7-day retained" = ≥2 active days with a 7+ day
        lifespan, states both definitions in a footnote, and treats recent cohorts cautiously. That single
        move is what makes the rest of his numbers trustworthy.<br><br>
        Pakistan vs Sri Lanka: 265 vs 261 users, registration 43.8% vs 45.6% (<em>"registration is not the
        differentiator"</em>), sessions/user 3.16 vs 1.71, repeat 46.4% vs 20.7%, 7-day retained 25.7% vs
        11.1%, coaching starters 34 vs 0.<br><br>
        <strong>He is the only candidate to isolate a specific ICP with a school identity.</strong> Pakistan
        secondary-school teachers, n=65: registration 98.5%, 5.99 sessions/user, 81.5% repeat, 49.2% 7-day
        retained, 32/65 started coaching and 30/65 completed it. Among the coaching users inside that
        segment: 8.63 sessions, <strong>100% repeat</strong>, 65.6% 7-day retained. His conclusion is an
        operating decision, not an observation: <em>"secondary teachers with a school identity as the first
        operating ICP for an eight-week growth sprint."</em><br><br>
        His cohort table covers all five spikes with geography attached, and he flags right-censoring
        himself: <em>"Dec 11 is too recent for a fair 7-day retention comparison because the dataset ends
        Dec 16."</em>""",
        a1_noise="""Broad Sri Lanka acquisition (<em>"diagnose activation before buying more reach"</em>);
        general chat on its own — 433 users but materially weaker retention, <em>"a utility/entry behavior,
        not enough evidence of durable value"</em>; small international geographies; raw event spikes
        (<em>"I would not call an event successful unless the cohort activates a flagship feature and remains
        active"</em>); and the source field — every user tagged "direct" despite known institutional
        introductions, so <strong>channel ROI cannot be trusted until institution_id / campaign_id /
        cohort_id are captured</strong>.""",
        a1_pri="""(1) Pakistan secondary teachers + coaching, as the first operating ICP.
        (2) Institution-led Pakistan acquisition that reproduces the 14 Nov <em>mechanics</em> — institution-backed
        introduction plus guided activation — <strong>rather than more events</strong>: <em>"the Sri Lanka
        cohorts show that a large spike can still be non-compounding."</em> He also attaches a decision to
        each feature in a table (chat = entry point not the thesis; lesson plans = activation bridge;
        coaching = highest-priority flagship; reading = high signal, too small, validate in a focused cohort).""",
        a1_exp="""<strong>A. Coaching-first school cohort.</strong> 8 Pakistan secondary schools, 4
        coaching-first vs 4 normal onboarding, ~15 teachers each, first coaching within 48 hours. Success:
        ≥35% complete coaching, ≥25% 4-week retained, and treatment ≥1.5× control on flagship activation.
        Kill after 2 cohorts if completion &lt;15% or no lift.<br>
        <strong>B. Admin-visible proof handoff.</strong> 20 teachers with completed coaching, consent-based
        one-page improvement snapshot, admin contacted within 48h for a 20-minute review. Success: ≥40% admin
        meetings, ≥25% of shares create a school-wide session. Kill below 15% after 20 shares.<br>
        <strong>C. Costed institutional replication.</strong> 3 institution cohorts with unique
        institution_id/campaign_id, capturing <strong>full field and event cost</strong> against downstream
        usage — cost per registered, per coaching-completed and per 4-week-retained teacher.<br><br>
        <strong>His commercial discipline is the strongest in the pool:</strong> <em>"I would not invent a
        universal CAC threshold."</em> He would agree the maximum affordable cost per retained teacher with
        the Head of Growth in week 1 using actual pricing or contract economics, and base the model decision
        on <strong>cost per retained outcome, not cost per signup</strong>.""",
        a2="""<strong>He changes the unit of measurement, and says why:</strong> the loop is measured at
        <em>school</em> level <em>"because the desired compounding outcome is new school adoption, not just
        more WhatsApp users."</em> Six loop steps, each with an action, an owner/channel and a weekly metric.
        The admin ask is deliberately framed as <em>"a 20-minute evidence review, not a sales pitch,"</em> and
        teachers are never asked to sell — <em>"ask them to share observed value."</em><br><br>
        The 60-day cadence is the most numerically committed of the six: 10 source schools and ~20 champions
        seeded, ≥15 proof shares and ≥6 admin meetings by week 2; 6–8 school sessions and 60–100 teachers
        onboarded by week 4; ≥8 referred schools by week 6; ≥4 activated by week 8. On district officials he
        is deliberately patient: <em>"do not approach every official too early; engage when there is enough
        school-level proof to be credible."</em>""",
        a2_k="""School-level K = newly activated referred schools ÷ active source schools, worked to a
        concrete arithmetic: 20 active source schools generate 8 referred schools of which 4 activate → K =
        4/20 = 0.20. Five metric families tracked weekly, and <strong>one of them is Economics</strong> —
        field/event cost by school, cost per activated teacher, cost per retained teacher, cost per activated
        referred school. He is the only candidate who puts unit cost in the weekly scorecard rather than
        treating it as a finance question. Pipeline sits in one CRM with School/Institution as the account
        object; the weekly update to the Head of Growth is one page and explicitly <em>"no activity dump."</em>""",
        a2_breaks="""<strong>Teacher gets value but the admin never sees it</strong> — because teachers may
        not be comfortable forwarding AI feedback or may not know what matters to management. Contingency: an
        admin-safe one-page snapshot with teacher consent, offered with the teacher copied, followed within
        48h; and if sharing stays low, <strong>make "share proof" part of the facilitated coaching session
        itself</strong>.<br>
        <strong>Admin agrees but school-wide adoption stalls</strong> — scheduling friction, no teacher time.
        Contingency: book the session before leaving the admin conversation, 7-day SLA, live first-use
        activation, nominate a champion, day-3/day-10 office hours.""",
        a3_prob="45% inside the current budget cycle",
        a3="""Frames it correctly from the first line: <em>"I would manage it as a rescue deal, not as a
        normal follow-up."</em> His Day 1 move is the one a disciplined operator makes —
        <strong>reconstruct the file before contacting any senior stakeholder</strong>: file reference number,
        current desk, missing document, next approval, budget head, exact deadline, from internal
        programme/finance/legal and the procurement focal point. His reason is a single line worth quoting in
        the debrief: <em>"I need facts, not 'in process,' before escalation."</em><br><br>
        Days 1–2 reopen the DEO with a 15-minute budget-alignment call and a one-page pilot summary. Days 2–4
        work procurement and finance in parallel, delivering any Taleemabad-side document same day —
        <em>"relationship support does not replace procurement movement."</em> Week 2 escalates
        <strong>support, not pressure</strong>, through the office/PA and a trusted existing sponsor, with a
        peer-level nudge only if a real relationship exists: <em>"keeps respect intact and avoids an
        ambush."</em> Weeks 2–3 convert intent into a written next milestone with a named owner and a date,
        and ask whether a compliant phased option exists. Weeks 3–4 escalate institutionally with Head of
        Growth approval. Week 5 forces an honest outcome — <em>"avoids keeping a dead deal artificially
        open."</em>""",
        a3_email="""Subject: <em>"15 minutes on the 200-school expansion before the budget window
        closes."</em> Courteous, references their earlier support, states the five-week window as a fact,
        asks what is still required from our side, offers a one-page summary plus any procurement
        documentation, proposes two specific days, and offers to be redirected to whoever is better placed.
        Competent and professional; less warmth and less craft than Shahmir's or Junaid's, and it asks for a
        meeting rather than shrinking the ask to something trivially answerable.""",
        a3_internal="""Amber/Red at 45%, with the single best line in any internal update:
        <strong><em>"I would not carry this at a high probability simply because the pilot succeeded."</em></strong>
        Gating is explicit — to ~65% if finance confirms budget inclusion and procurement gives a dated next
        milestone; below ~25% if the sponsor is still unreachable and no budget path exists by end of week 2.
        Four specific asks. On the competitor: would not use it as client pressure, but internally it raises
        urgency. He closes the whole submission with a <strong>"submission assumptions" section</strong> —
        all findings from the supplied master dataset with no fabricated daily metrics, no invented CAC
        ceiling, and a note that his 60-day targets are execution targets for the exercise
        <em>"not claims about Taleemabad's existing performance."</em>""",
        reflection="""<strong>Futurenostics.</strong> The B2B growth problem was being treated as a volume
        problem when the real issue was execution consistency — outreach was happening, but segmentation,
        qualification, CRM discipline and follow-up were fragmented, so activity was not converting. He
        flagged that <em>"the strategy itself did not need to be replaced; the operating system around it
        did,"</em> then built target segments, outbound sequences, qualification, pipeline stages and
        recurring performance reviews, and looked at where prospects dropped rather than raising message
        volume. Result: roughly <strong>3× qualified meetings within 90 days and PKR 10M+ in structured
        qualified pipeline within six months</strong>. Directly on-point for this role.""",
        verified="""All figures recomputed and matched, including the n=65 secondary-teacher segment and the
        full five-cohort table. His self-imposed definitions are stated and applied consistently throughout.""",
        thin="""<strong>He analysed only the master dataset — by explicit choice</strong>
        (<em>"I did not invent day-level session patterns that cannot be reconstructed from this file
        alone"</em>). That is honest and defensible, but it means the two sharpest findings in the pool are
        absent from his work: the 22.9% coaching-session failure rate and the missing Sinhala/Tamil reading
        passages both live in the child tables he set aside. Stakeholder work is solid but generic where
        others got specific — no Pakistani district hierarchy, no procurement mechanics, no named artefact.
        His Feature and Cohort tabs are <strong>pasted values rather than formulas</strong>, so those two
        tables cannot be re-derived in-file, and his Growth Loop Tracker is a live template with all zeros —
        structure without a worked example.""",
        probes=[
            "You deliberately used only the master dataset. Two of the strongest findings in this round came out of the child tables — a 23% coaching failure rate and no Sinhala or Tamil reading passages. How do you decide when 'I can defend this file' becomes 'I have not looked hard enough'?",
            "You refused to invent a CAC ceiling and would set it with the Head of Growth in week 1. Suppose I tell you the ceiling is PKR 4,000 per retained teacher. Which of your three experiments dies first?",
            "Your stakeholder layer for district officials is 'engage when there is enough proof to be credible.' Concretely — who in a Pakistani district do you actually call, and what do you ask them for?",
            "Your loop targets are precise (15 proof shares, 6 admin meetings, 8 referred schools). Where did those numbers come from, and which one are you least confident in?",
        ],
    ),
    dict(
        name="Yusra Amjad", app="4061", total=89, band="STRONG YES", proceed=True,
        colour="#1b7f4d", scores=[5, 4, 4, 5, 4, 5],
        link="https://drive.google.com/drive/folders/11bowQeg_prEXh8carJnXqyNpveznx5o1",
        docs=[
            ("Taleemabad case study", "DOCX, 118 paragraphs, 5 tables", "All three assignments plus reflection and a per-assignment AI note."),
            ("Spreadsheets for Assignment 1 & 2", "XLSX, 6 sheets, ~45 formulas", "Every analysis tab is formula-driven, and tab 1.1 is a dedicated 'Assumptions & Method' sheet. No raw dataset included; pipeline tab carries worked sample rows."),
        ],
        docs_note="Arrived as attachments on the Markaz submission notification, 10 August. She is the only candidate who opened her workbook with a written method and assumptions tab.",
        a1="""<strong>She found the single most sophisticated piece of evidence in the round.</strong>
        Sri Lankan registrations complete in a median of about 4 minutes, <em>tightly clustered across
        users</em>; Pakistani registrations take a median 37 minutes and are highly variable, some running
        into days. Her read: a pre-loaded contact list, not organic signups. She labels it an educated guess
        because the data has no source attribution.<br><br>
        Then she does what separates a good analyst from a careful one — <strong>she corroborates it with a
        second, independent test.</strong> In Pakistan, finishing registration roughly doubles usage (2.3 →
        4.3 sessions) and return rate (34% → 63%). In Sri Lanka it changes nothing at all (1.8 → 1.6, 22% →
        19%). Her conclusion: <em>"If the issue were just a clunky sign-up process, fixing it would help Sri
        Lanka too — it doesn't, which suggests the real problem is something that happens after
        sign-up."</em> That is a genuine falsification test, and no one else ran one.<br><br>
        She also isolates the segment cleanly: more than half of Sri Lanka's registered users (62 of 119)
        teach college-level only. And on coaching: 94% of started sessions are completed (33 of 35), so
        <em>"the problem isn't that the feature is weak — it's that almost nobody tries it."</em> Coaching
        users show 8.29 sessions and 5.38 active days against 2.41 and 1.80 for non-users — 3.4× and 3.0×,
        with 2.5× the return rate.""",
        a1_noise="""The ten small countries (barely any users, almost none registered) and the college-only
        teacher group in both countries — lower usage, lower return, almost no coaching. Short and correctly
        reasoned rather than exhaustive.""",
        a1_pri="""(1) Get Pakistani school-age teachers into coaching — and she sizes the prize rather than
        asserting it: moving adoption from 14% to 25% adds roughly <strong>30 active coaching users, enough
        to trigger the loop</strong> in Assignment 2. (2) Diagnose Sri Lanka before spending more, and she
        lists the four candidate causes she would separate: is coaching actually available and working there,
        is there a language barrier, are we reaching the wrong teachers, or were these signups never real
        interest. <em>"Growing a market before we know the answer risks spending money on something that was
        never going to work."</em>""",
        a1_exp="""<strong>E1 "Coach a lesson" onboarding prompt.</strong> Replace the generic welcome with
        <em>"Ready to coach? Record your lesson and get AI feedback in 2 minutes"</em> within the first five
        messages; 20 control / 20 variant. Success ≥30% start coaching within 7 days vs &lt;15% baseline;
        kill below 20% after two weeks.<br>
        <strong>E2 Find out what is really going on in Sri Lanka.</strong> Take 20–30 Sri Lankan teachers and
        <strong>personally walk each one through recording and submitting a lesson</strong> by phone or
        WhatsApp — which, as she says, <em>"removes the 'didn't know about it' explanation
        completely."</em> If completion approaches Pakistan's 94%, it was awareness; kill criterion — under
        20% finishing <em>even with someone walking them through every step</em> points to a real product or
        fit problem, at which point she pauses Sri Lanka spend and escalates to product. Elegant design: one
        cheap manual test cleanly separates two expensive explanations.<br>
        <strong>E3 Differentiate school from university teachers at signup.</strong> One question — "what
        grades do you teach?" — routes school-age teachers straight to a coaching demo while college-only
        teachers stay on the current flow and become the comparison group. Kill under a 3-point gap after
        ~100 signups: <em>"it's not worth keeping two different sign-up paths."</em>""",
        a2="""Four 15-day phases mapped onto the six loop steps, with the honest note that by Phase 3
        several steps run at once, on repeat. Her mechanism for the hardest step is the cleverest in the pool:
        a <strong>one-tap "Principal Summary"</strong> generated after every coaching report, plus a
        dedicated WhatsApp number principals can message directly with no rep in the middle — which turns the
        invisible step into a measurable one. She names it exactly that: inbound admin pings are
        <em>"the real, observable version of 'admin notices'"</em>, with Principal Summaries generated as the
        leading indicator one step upstream.<br><br>
        Hard SLAs: any principal who messages gets a callback within 2 days and a workshop booked within 7.
        On teachers she imposes a restraint no one else did — <strong>never more than one ask per week</strong>,
        because <em>"the loop should feel like a byproduct of using the tool, not a campaign."</em> District
        officials come in only once a district has 3+ active schools, and the ask is endorsement and
        introductions, <strong>explicitly not budget or procurement</strong> — <em>"that conversation is a
        separate, longer motion."</em>""",
        a2_k="""K-factor proxy = new signups attributed to a referral link or school workshop ÷ users
        eligible to refer (defined as ≥3 completed coaching sessions) at the start of the period, reported as
        a <strong>trailing 4-week rolling average</strong> with the reasoning stated: <em>"at this volume a
        single strong or weak week is noise, not signal, before ~2 loop cycles have run."</em> One row per
        school in the tracker, updated same-day by whoever owns the touch — <em>"no end-of-week batch
        entry."</em> Weekly update to the Head of Growth is five fixed items including top-3 at-risk accounts
        and next week's confirmed workshops.""",
        a2_breaks="""<strong>Step 2→3, the teacher never actually shows the admin</strong> — and she
        identifies precisely why it is the fragile one: <em>"it happens outside the product, off-platform,
        and is only indirectly observable."</em> Contingency: make forwarding near-zero-effort via the
        one-tap summary, and flag any user with a summary generated but no inbound ping within 21 days as
        at-risk for a light manual check-in — <em>"not a hard sell, just 'did this land with your school
        head?'"</em><br>
        <strong>Step 4→5, admin invites then scheduling stalls.</strong> The 48-hour/7-day SLA is
        non-negotiable; if a school cannot commit a date within two weeks, a low-pressure holding message
        with a peer-school testimonial keeps it warm <em>"without letting the thread go cold."</em>""",
        a3_prob="30–40% for the full 200 · 55–60% for some expansion once a fallback is tabled",
        a3="""<strong>The only split probability in the pool, and the most commercially useful number
        anyone produced</strong> — because it tells the Head of Growth two different things to decide on. Her
        opening logic is sound: <em>"There's no point pushing harder on the person who's gone quiet — that
        just feels like pressure to someone who's already avoiding us for a reason we don't know yet."</em><br><br>
        Week 1 reopens through the paperwork office and the PA rather than the DEO, asking plainly what stage
        things are at and what is holding them up, <em>"much lower-pressure than another unanswered call to
        the top"</em> — while the DEO gets a value-first email with a one-pager <strong>built for their own
        paperwork</strong>. Week 2 delivers any blocking document same-day, adds a second contact inside the
        office so <em>"the relationship shouldn't run through one unresponsive person,"</em> and asks 2–3
        pilot head teachers for notes of support: <em>"peer proof re-creates urgency without Taleemabad
        looking pushy."</em> Week 3 asks for 15 minutes in person, upfront that it is about the deadline, with
        a scoped 60–80 school fallback ready. Week 4 protects what we already have — visiting the original 40
        schools for fresh success stories now that a competitor is active. Week 5 pushes for something in
        writing <strong>because a verbal agreement already fell through once</strong>, and if it is a no, she
        writes the position down, flags it unlikely, and sets a reminder for next year's round
        <em>"instead of just letting it fade away."</em>""",
        a3_email="""Subject: <em>"A quick summary, in case it helps with the budget request."</em> The most
        useful email of the six in one specific way — the attached one-pager is offered for the district's
        own budget paperwork, which makes saying yes cheaper for them. Credits their team for how well the
        trial ran, names the deadline without weaponising it, and lowers the bar to a reply:
        <em>"even a one-line reply on where things stand would help us plan on our end."</em> Slightly
        effusive in places ("something exciting", "Congratulations again").""",
        a3_internal="""Clear status, what is in motion, the split probability with its reasoning — six weeks
        of silence from a publicly enthusiastic DEO <em>"reads more like internal bureaucratic friction or
        competing budget priorities than a lost deal"</em> — and an explicit downgrade trigger if there is no
        real response in 1–2 weeks. Three precise asks: sign-off to offer the scoped-down expansion,
        any warmer or higher-level relationship into the district, and a review of the impact brief before it
        goes out externally.""",
        reflection="""<strong>The one reflection with no commercial context — and it is still a good
        story.</strong> Teaching 8th-grade English, some students could not write a complete sentence or
        conceptually grasp what a sentence was. School policy was to write each correction five times. After
        two weeks she saw zero improvement: <em>"Students were mechanically copying corrections without
        understanding why they were wrong. They were completing the task, but learning nothing."</em> She
        substituted two targeted worksheets on sentence-versus-fragment and full-stop placement; subsequent
        essays showed marked improvement, and she kept the worksheets as a standing resource. Correct
        instinct — measure the outcome, not the compliance — but it is a classroom example, not a growth or
        partnership one.""",
        verified="""The registration-time distribution and the registration-effect comparison both recomputed
        and matched, as did the 62-of-119 college-only figure and the 94% coaching completion rate. Her
        method tab makes every definition she used explicit, which is the easiest submission of the six to
        audit.""",
        thin="""<strong>She has no BD or growth background and says so</strong> — her AI note records that
        she used Claude <em>"to explain industry specific terms to me as someone without a BD
        background."</em> That candour is to her credit, and she then corrected the output and added her own
        break-point calls; but it is the central question on her candidacy for a senior growth role, and the
        reflection reinforces it by drawing on teaching rather than commercial work. Her prose is
        deliberately plain and explanatory — she defines "Coaching" in brackets for her reader — which reads
        as an accessible explainer rather than a senior operator's memo. Her workbook contains no raw data,
        so her best finding cannot be re-derived from her own file. Assignment 3's plan is the least
        procedurally specific of the three strong submissions: no procurement mechanics, no named officer
        roles, no file-location step.""",
        probes=[
            "Your registration-timing finding is the sharpest piece of analysis in this round. Talk me through how you got to it — what made you look at completion time at all?",
            "You have not worked in business development. This role is 2IC on growth with 40-60% travel and government-facing partnership work. Make the case for yourself, and tell me what you would need in the first 90 days.",
            "Your Sri Lanka experiment hand-holds 20-30 teachers through a recording. That is real staff time. Who does it, and what do you stop doing to free them up?",
            "You would offer a scoped-down 60-80 school fallback. What is the risk of putting a smaller number on the table before the DEO has said no to the bigger one?",
        ],
    ),
    dict(
        name="Umar Zahid", app="3902", total=78, band="YES", proceed=True,
        colour="#2f6fb5", scores=[4, 5, 2, 5, 4, 3],
        link="https://drive.google.com/drive/folders/1TbSvIc94OMAbGk4Y7dtj5dh4QGlzYpj1",
        docs=[
            ("Response", "PDF, 13 pages", "Slide-deck format, one headline argument per slide. Note: pages 5 and 6 are an identical duplicated slide."),
            ("Analysis and Tracker", "XLSX, 7 sheets, ~89 formulas", "Includes the master dataset, a pivot-table Analysis tab, a Dashboard, and a 56-formula Weekly Metrics model. Schools Pipeline, Teachers and Action Log are header-only."),
        ],
        docs_note="Arrived as attachments on the Markaz submission notification, 14 August. <strong>Correction carried forward from v1:</strong> his tracker was initially flagged as possibly missing because only a PDF of the Analysis sheet had been seen. The workbook exists, has five substantive tabs, and is among the best in the pool — his execution score moved 4 → 5 and his total 73 → 78.",
        a1="""<strong>The cleanest quantitative decomposition of the six.</strong> He is the only candidate
        who fully separates flagship reach: only <strong>8.1% of users (44 of 546) reached either flagship
        feature</strong> — 31 coaching-only, 9 reading-only, 4 both. His feature table gives adoption,
        attempts, attempts per adopter, completions and completion rate side by side: coaching 35 users /
        6.4% / 118 attempts / 3.4 per adopter / 88 completed / 75%; reading 13 / 2.4% / 87 / 6.7 / 51 / 59%.<br><br>
        Country: Pakistan's registered users return 3.3× more often and generate ~2.7× more sessions.
        Segment: school educators return 3.7× more and adopt coaching 7× more than university-only users —
        and he shows good restraint on the mixed segment, which has the highest repeat rate but
        <em>"only 25 users, too small to prioritize independently."</em><br><br>
        <strong>His framing of the event data is the sharpest single sentence on cohorts in the round:</strong>
        the 14 November introduction produced 40 users at 82.5% registration, 87.5% repeat and 57.5%
        coaching, while <em>"the other four institutional introductions collectively generated 254 users but
        only 22.0% repeated their usage, while none adopted coaching."</em> One of five events worked. That
        is the whole argument in one line.""",
        a1_noise="""Sri Lanka as reach without demonstrated core value — 261 users, 19.3% registered-user
        repeat use against Pakistan's 63.2%, 1.59 sessions per registered user against 4.36, zero coaching
        and zero reading adopters. Correct call, but thinner than the others on <em>why</em>, and he does not
        interrogate the source-attribution gap that Shahmir, Arshan and Junaid all flagged.""",
        a1_pri="""(1) Deepen coaching adoption among Pakistan's school educators — among 117 registered
        Pakistani users, 63.2% returned and 29.1% adopted coaching, and school-level educators are 109 of
        those 117 with 66.1% repeat use and 30.3% coaching adoption. (2) Replicate the 14 November
        institutional activation model specifically, on the one-of-five-events evidence above.""",
        a1_exp="""<strong>The most rigorously calibrated experiment set in the pool — every threshold is
        two-sided.</strong><br>
        <strong>1. Replicate 14 Nov.</strong> Six Pakistan schools, three with live coaching onboarding
        completing a first recording in-session, three standard. Success: ≥40% complete coaching within 7
        days <em>and</em> ≥15pp uplift over control. Kill: activation &lt;25% or uplift &lt;5pp after 80
        registrations.<br>
        <strong>2. Automate coaching activation.</strong> A/B the existing WhatsApp journey against one with a
        recording example, privacy guidance, a "record now" prompt and a scheduled reminder. Success: ≥15pp
        uplift with ≥70% completion. Kill: &lt;5pp after 100 users, or completion below 60%.<br>
        <strong>3. Convert usage into school expansion.</strong> Consent-based coaching summaries to
        administrators at 10–15 active schools. Success: ≥20% book a session within 14 days and onboard ≥10
        teachers. Kill: &lt;10% after 20 schools, or fewer than five teachers per converted school.""",
        a2="""Framed as a decision objective rather than a plan — <em>"make the designed coaching-to-school
        loop generate at least 0.20 verified activated teachers per eligible seed teacher"</em> — with an
        explicit statement of restraint that reads well for a 2IC role: <em>"The plan operationalizes the
        leadership-designed loop; it does not redesign it."</em> Five phases, each with owner, channel and a
        numeric exit metric, and a stakeholder table whose third column is <strong>"Required next
        action"</strong> — the only one of the six that specifies what the stakeholder must actually do
        rather than what we send them.<br><br>
        His 60-day decision rule is unusually disciplined: scale only if K ≥0.20 <em>and</em> coaching
        activation ≥40% <em>and</em> admin-to-session conversion ≥20% <strong>across at least three
        cohorts</strong> — and <em>"do not compensate for weak conversion with more top-of-funnel
        events."</em>""",
        a2_k="""K = unique referred teachers completing first coaching ÷ eligible seed teachers completing
        coaching, counting each downstream teacher <strong>once</strong> via a unique teacher ID, source type
        and referrer ID. <em>"No unattributed referral is included in K"</em> — the strictest attribution
        rule submitted, alongside Shahmir's. Every funnel stage carries a decision signal with a threshold
        (activation ≥40%, completion ≥70%, repeat ≥50%, feedback ≤24h; admin review ≥50%, booking ≥20%), plus
        a channel-efficiency line that would <em>"automate or stop motions that require high effort without
        activation."</em> Daily hygiene is specified — owners update by end of day, the Growth Lead reviews
        overdue items and referrals awaiting contact each morning, referred schools contacted within one
        business day.""",
        a2_breaks="""Both break points come with <strong>early-warning indicators as well as
        contingencies</strong>, which no one else provided.<br>
        <strong>1. Teacher does not complete or repeat coaching</strong> — warning signs: low recording
        starts, privacy objections, feedback taking over 24h, first-to-second conversion below 50%.
        Contingency includes completing the first recording in-session, a privacy script, champion office
        hours, and <em>"if activation remains &lt;25%, pause the cohort and interview non-completers before
        adding schools."</em><br>
        <strong>2. Evidence does not convert to administrator action</strong> — warning signs: pack not
        shared, review over 5 days, no explicit booking, session delayed over 7 days. Contingency escalates
        to a district sponsor introduction after two failed contacts, and redesigns the proof/ask if under
        10% book after 20 eligible schools.""",
        a3_prob="35% · classified at-risk/uncommitted, explicitly not commit",
        a3="""<strong>The most forecast-disciplined Assignment 3 of the six.</strong> Every week has a
        "specific ask / decision gate" column with a hard numeric consequence, which is exactly how a
        commercial pipeline should be run.<br><br>
        Week 1 establishes facts and reopens, in a defined contact order — internal owners first, then the
        DEO, then the procurement focal point, then the DEO's office for scheduling only,
        <em>"do not lobby for a decision."</em> The gate: by Day 5, a named budget/procurement owner, exact
        file stage, missing inputs, approval sequence and a meeting date — and if those remain unknown, keep
        the probability at-risk and prepare transparent escalation. Week 2 multi-threads
        <em>"without undermining sponsor"</em>, asks the senior sponsor for a peer check-in
        <em>"explicitly framed as support—not escalation"</em>, and reconfirms pilot champions' evidence
        while pointedly <strong>not</strong> asking them to pressure the DEO. Its gate is brutal and correct:
        <strong>no response or named owner by end of week 2 → reduce below 15% and remove from commit.</strong>
        Week 3 submits one decision-ready pack and holds a 30-minute working session —
        <em>"no 'in process' status without a named next step."</em> Week 4 demands one of three
        <em>written</em> outcomes: proceed this cycle, approve a defined phased route, or confirm inclusion is
        not feasible. Week 5 closes or resets cleanly, with the line that most hiring managers will
        appreciate: <em>"No false 'verbal commit' in committed forecast."</em>""",
        a3_email="""Subject: <em>"Meeting Request: Next Steps for the 200-School Expansion."</em> The
        shortest of the six at roughly 90 words — efficient, attaches a one-page pilot summary and
        implementation timeline, asks for 20 minutes. <strong>Two register issues worth raising at
        debrief:</strong> it opens <em>"Aoa District Education Officer"</em> — a transliterated informal
        salutation and a generic title rather than a name, for a re-opening approach to a senior government
        officer after six weeks of silence; and it carries the least relationship warmth of the six, with no
        reference to the pilot's specifics or the DEO's own public support.""",
        a3_internal="""35%, classified at-risk/uncommitted, with the reasoning itemised on both sides and
        explicit gating events — toward 60% only if week 1 produces written sponsor intent, a named
        budget/procurement owner and a dated approval path; below 15% and out of commit if those are absent
        by end of week 2. Four specific asks including finance/procurement 24-hour turnaround and
        pre-approved boundaries for a phased implementation. On the competitor: do not use as client
        pressure; <em>"preserve a dated next-cycle path rather than carrying a false-positive
        opportunity."</em>""",
        reflection="""<strong>Eclipse AI.</strong> The growth strategy depended on a sales-led enterprise
        model, but long cycles, multiple decision-makers and repeated demos were delaying the point at which
        users experienced value — <em>"the issue was not simply lead generation; the model created too much
        friction between interest and adoption."</em> He raised it early and proposed a shift to product-led
        growth, working with product, engineering and marketing on a self-service MVP, simplified onboarding
        and messaging built around immediate product value. Sign-ups rose roughly fourfold, and more
        importantly the team could diagnose product and onboarding problems from actual behaviour rather than
        sales feedback. Strong, relevant, and the mechanism is clearly explained.""",
        verified="""All cohort and feature figures recomputed and matched. His pivot-table Analysis tab
        reproduces the country and segment cuts from the raw master dataset inside the file, which makes his
        quantitative work the second-most auditable of the six after Yusra's.""",
        thin="""<strong>Stakeholder work is his weak dimension and it scored 2.</strong> The DEO email is the
        thinnest of the six on warmth and specificity, opens with an informal transliterated salutation and a
        generic title, and his stakeholder plan — while structurally excellent — treats the district as a
        process to be managed rather than relationships to be worked. There is no Pakistani district
        hierarchy, no named officer roles, no artefact prepared for the other side's convenience.
        <strong>Two presentation defects:</strong> pages 5 and 6 of his deck are an identical duplicated
        slide, which is a proofreading miss in a submission about execution discipline; and three of his
        seven workbook tabs (Schools Pipeline, Teachers, Action Log) are headers with no populated example,
        so the tracker is a design rather than a demonstration. The slide format also compresses his
        reasoning — his logic is present but often has to be inferred from bullets.""",
        probes=[
            "Your DEO email is 90 words and opens 'Aoa District Education Officer'. Six weeks of silence, five weeks to the deadline. Read it back and tell me what it does for the relationship.",
            "Your week-2 gate says: no named owner, drop below 15% and remove from commit. Your Head of Growth has already told the board this is landing. Hold the line for me.",
            "Pages 5 and 6 of your deck are the same slide. In a submission about execution discipline, how did that get through?",
            "Your pipeline, teacher and action-log tabs are empty templates. Populate one row for me now, from the 14 November cohort, and tell me what you would do with it on Monday.",
        ],
    ),
    dict(
        name="Junaid Ali", app="3992", total=74, band="YES", proceed=True,
        colour="#2f6fb5", scores=[5, 3, 5, 3, 4, 1],
        link="https://drive.google.com/drive/folders/1xZ29_Q3qVtf1grj4kCO_8kbXUcCWGUyC",
        docs=[
            ("SMG Case Study", "PDF, 14 pages", "All three assignments. The only submission with embedded charts (4 figures). Numbered lists run continuously across sections — a Word auto-numbering artefact."),
            ("Analysis file", "XLSX, 5 sheets, 59 formulas", "Includes master dataset, daily activity, country breakdown and aggregate metrics — and uniquely, a '0. Data Quality Checks' block at the top of the Analysis tab."),
        ],
        docs_note="Arrived as attachments on the Markaz submission notification, 9 August. He is the only candidate who built explicit data-quality checks before analysing.",
        a1="""<strong>He produced the only genuinely causal explanation in the round.</strong> Everyone
        else observed that Sri Lanka has zero coaching adoption. He explained the mechanism: the users
        onboarded in those spikes were from a <strong>Teacher Training College</strong>, and
        <em>"coaching requires an audio recording of an actual class being taught, and a
        teacher-training-college population mostly doesn't have a class of their own to record."</em> The
        users tick every registration box and never cross into the coaching loop because
        <em>"the product's core mechanic doesn't map onto who they are."</em><br><br>
        He then draws the right generalisation, which is worth more than the finding itself:
        <em>"the problem isn't that a partner-led bulk onboarding channel is inherently bad — it's that this
        specific cohort was the wrong population for a classroom-coaching product. Any future B2B2G push
        needs to explicitly target practicing classroom teachers, not adjacent populations like
        trainee/trainer cohorts, however convenient the list is to get."</em><br><br>
        He also opens by naming the vanity trap directly: country 94 wins on day-1 activation (100% vs
        97.7%) and week-1 retention (100% vs 98.1%), <em>"But retention of what?"</em> His feature framing is
        the crispest definition of compounding anyone offered — lesson plans and presentations are
        <em>"wide and shallow"</em> (31.1% adoption / 27.1% repeat; 16.7% / 12.1%), coaching and reading are
        <em>"narrow and deep"</em> (6.4% / 68.6%; 2.4% / 69.2%) — <em>"not how many people tried it, but
        whether trying it once predicts trying it again."</em> He picks coaching over reading on
        defensibility: 2.7× the adopter base inside a channel already known to work.""",
        a1_noise="""Country 94's registration volume, reframed as <em>"a segment-targeting problem, not a
        product-market-fit signal"</em>; lesson plans and presentations as standalone bets; and a finding
        nobody else surfaced — <strong>54.6% of all 546 users had one session or fewer, ever</strong>,
        largely in unregistered / flow_sent / template_send_failed states, which he correctly labels
        <em>"failed onboarding, not an engaged segment."</em>""",
        a1_pri="""(1) Country 92 rather than 94 — grow inside a base that already knows how to use the core
        product, since <em>"the other ~87% of 92's 265 users haven't touched coaching yet — that's the
        headroom."</em> (2) Coaching rather than lesson plans or presentations, on the repeat-rate argument
        above.""",
        a1_exp="""<strong>His experiment design shows the most operational realism of the six, and it is
        where his experience shows.</strong><br>
        <strong>E1 B2B2G pilot targeted at classroom teachers.</strong> Same partner-led model, cohort
        restricted to verified practising classroom teachers via a screening question at signup. He is the
        only candidate to impose a <strong>timeline reality check</strong>: a real B2B2G pilot has a 6–8 week
        lead time from first conversation to a live cohort, <em>"which is effectively the whole 8-week
        window, not a 'week 1' task with results by week 3"</em> — so week 1 is the start of cohort
        definition and the hypothesis is tested continuously as the pilot ramps. Kill: once 50+ verified
        classroom teachers are live, if coaching-start is still below ~5%, the warm-handoff mechanism itself
        is the problem, not the audience.<br>
        <strong>E2 Teacher-to-teacher referral from the 32 coaching completers.</strong> Explicitly run
        <strong>manually, not built</strong>: <em>"the cohort is only 32 people, too small to justify
        engineering time before we know the channel works."</em> Automation only after the manual pass
        converts.<br>
        <strong>E3 Coaching-first onboarding message A/B</strong>, isolating message design from channel
        quality — and he is the only candidate who specifies a <strong>guardrail metric</strong>, monitoring
        whether the treatment <em>hurts</em> registration completion because <em>"a message that's too pushy
        could suppress signups."</em><br><br>
        He closes with a "what's still worth watching" section that reads like someone who has run these
        before: E1's kill decision realistically lands late in the window so decide the fallback now, and
        <em>"whoever owns the manual outreach in Experiment 2 should be named before week 1 starts — with
        only 32 people to contact, this stalls immediately if it's nobody's explicit job."</em>""",
        a2="""Seeds from the 34 existing coaching-active teachers and runs execution through the existing
        local partner network. <strong>His distinctive contribution is a Days 1–7 precondition nobody else
        thought of:</strong> before seeding any new district, the partner runs a courtesy briefing with the
        district education office covering each of those teachers' schools — <em>"Not a pitch — a heads-up:
        'this is running in your schools, here's what it is.'"</em><br><br>
        And he grounds it in real experience rather than theory: <em>"learned from a real
        government-partnered pilot where the relevant department found out about teacher usage after the fact
        and it created friction that quietly killed engagement, because there was no top-down endorsement
        giving teachers a reason to prioritize it."</em> Standing biweekly touch with every active district
        follows, <em>"so we're never 'the tool nobody told them about.'"</em><br><br>
        His administrator design removes the obstacle rather than pushing through it: a 20-minute slot inside
        a staff meeting that already exists, <strong>not a separate event the admin has to organise or
        fund</strong>, with the district briefed in parallel <em>"so one admin's lack of authority can't kill
        it."</em> Asks to teachers are always small and specific and triggered right after a coaching win —
        <em>"never 'help us grow.'"</em>""",
        a2_k="""K = i × c on a trailing 4-week average, with a genuine measurement safeguard: he tracks a
        second, independent calculation — new coaching-active teachers attributable to the existing cohort ÷
        coaching-active teachers at the start of the period — and states that it should converge to the same
        0.2, <em>"and if it doesn't, one of the two components is being mismeasured."</em> That is the only
        self-checking metric definition submitted. Weekly update has a fixed four-part shape, with blockers
        named specifically <em>"especially district-endorsement status per district, since that's the step
        most likely to quietly stall things."</em>""",
        a2_breaks="""<strong>District/institutional visibility gap</strong> — and his description of the
        failure mode is the most precise in the pool: engagement <em>"doesn't get blocked outright — it just
        quietly decays, because there's no top-down endorsement giving teachers a reason to keep prioritizing
        it."</em> Treated as a Week-0 precondition <em>"not a reactive fix."</em><br>
        <strong>Admin enthusiasm without authority to act</strong> — genuinely impressed and still unable to
        invite a session, because they control neither budget nor scheduling. Contingency: remove the
        resourcing ask entirely and brief a second contact from day one.""",
        a3_prob="No number given — 'moderate, not high or low'",
        a3="""<strong>His Assignment 3 contains the single most politically astute move in the round, and
        also the clearest miss against the brief.</strong><br><br>
        The move: after giving the DEO a fair first chance and a week-2 courtesy heads-up that
        <em>"gives the DEO the chance to re-engage before we go above them"</em>, he goes to the provincial
        Secretary — <em>"never a surprise end-run"</em> — and then <strong>comes back to the DEO with that
        support behind him, so that "the DEO gets to look like the one who made it happen, not the one who
        got bypassed."</strong> Nobody else designed the escalation to leave the sponsor's face intact.<br><br>
        His diagnosis is also correct and unsentimental: <em>"government got the value of a free pilot,
        publicly praised it, and now the ask has become a real budget line with no paper trail behind
        it."</em> He runs an internal hedge from week 1 <em>regardless</em> of the DEO's response — what the
        department could plausibly self-fund at 200-school scale, and whether a donor relationship could
        bridge the timing. He goes to a <strong>named procurement individual, not "the file"</strong>, on the
        grounds that <em>"sometimes it really is one missing signature, not politics."</em> And he keeps the
        pilot schools warm in reserve rather than deploying them as pressure.<br><br>
        <strong>The miss:</strong> the brief asks explicitly for <em>"your honest read on the probability
        this closes."</em> He does not give a number — <em>"I'd call this moderate, not high or low"</em> —
        and hangs the whole forecast on one external variable he does not control. That is the difference
        between a growth manager and a growth manager who can be forecast against, and it is the main reason
        his total sits at 74 rather than in the high 80s.""",
        a3_email="""Among the best-judged of the six. Opens with genuine acknowledgement
        (<em>"I know budget season keeps everyone's calendars impossible right now"</em>), credits the DEO's
        own public comments on what teachers were seeing, names the real obstacle without blame
        (<em>"I don't want this to slip simply because the timing got tight"</em>), attaches two specific
        artefacts — a one-page impact summary quoting the DEO's own praise, and an updated cost note — offers
        to send them directly to whoever handles the submission, and frames the budget window as shared
        planning rather than an ultimatum.""",
        a3_internal="""Honest and self-aware in tone but <strong>unforecastable</strong>. No probability
        number; the read is explicitly contingent on whether the Secretary's office has room, with a fair
        articulation of both branches — close it if they do, otherwise lock a written next-year commitment
        plus a smaller funding-partner-backed interim rollout, <em>"which is a fine outcome, just not the one
        on this year's clock."</em> Three specific and well-chosen asks: a peer-level introduction into the
        Secretary's office, a green light on a phased interim rollout, and a read from partnerships on
        whether a donor bridge is real — <em>"I've started that conversation internally but don't want to
        overpromise on it externally until I know it's real."</em>""",
        reflection="""<strong>Not present as a separate reflection.</strong> His Assignment 2 draws on a
        real government-partnered pilot where the department learned of teacher usage after the fact, which
        is genuinely the same kind of evidence — but the standalone reflective response the brief asked for
        is missing from his submission. This is why his Signal dimension scored 1, the lowest single
        dimension score in the pool, and it is worth confirming at debrief whether it exists and simply was
        not attached.""",
        verified="""His causal finding is data-supported: <strong>52.1% of registered Sri Lankan users teach
        university level only against 6.9% in Pakistan</strong> — a 7.5× difference, recomputed and matched.
        The 54.6% single-touch figure and all feature adoption/repeat rates also check out.<br><br>
        <strong>One caveat that matters, and it is a debrief question rather than a data error.</strong> He
        writes that the Sri Lanka partner/teacher-trainer provenance is <em>"confirmed, not inferred."</em>
        The case brief anonymises the countries as codes 92 and 94 and says nothing about a partner
        organisation, Sri Lanka, or teacher-training colleges — I checked. His mechanism is properly
        evidenced from the data; the <em>provenance</em> claim is outside knowledge stated as established
        fact. He also refers to the product by its real name ("Rumi's thread") despite the case being
        anonymised, which suggests he researched Taleemabad's actual product before writing. That is
        initiative, and it is also exactly the habit that produces an over-claim.""",
        thin="""<strong>No probability number in Assignment 3, against an explicit instruction in the
        brief</strong> — the single largest deduction on his card. <strong>No standalone reflective
        response.</strong> Presenting outside knowledge as "confirmed" without flagging it as an assumption,
        in a submission where every other candidate labelled their assumptions explicitly. And the document
        carries visible auto-numbering defects: numbered lists run continuously across three separate
        sections, so the weekly-update list starts at 4, the break-points at 8, and items 10 and 11 appear
        inside the body of the DEO email. Individually trivial; collectively a discipline signal in a
        deliverable that will be read by a hiring manager.""",
        probes=[
            "You wrote that the Sri Lanka teacher-training-college provenance is 'confirmed, not inferred.' The brief gives you country codes and no partner context at all. Where did that come from, and would you write 'confirmed' again?",
            "The brief asked for your honest read on the probability this closes. You gave me 'moderate.' Give me the number now, and tell me what moves it.",
            "Your escalation lets the DEO look like the one who made it happen. Walk me through the actual conversation where you tell a DEO you have already spoken to the Secretary's office.",
            "Your reflective response is not in the submission. Was it written? And either way — tell me the story now.",
        ],
    ),
    dict(
        name="Arooj Khalid", app="3868", total=70, band="YES", proceed=True,
        colour="#2f6fb5", scores=[4, 4, 3, 2, 4, 4],
        link="https://drive.google.com/drive/folders/1NOH-IiWtGST8oNPgNL48E5L5PYYx3dxN",
        docs=[
            ("Assignment 1a", "DOCX, 29 paras, 5 tables", "Analysis memo with feature, country and three experiment tables."),
            ("Assignment 1b", "XLSX, 2 sheets, 0 formulas", "Feature Comparison and Country Comparison — pasted static values, no raw data, no working."),
            ("Assignment 2a", "DOCX, 33 paras, 3 tables", "Loop plan, stakeholder table, weekly metric locations. The 60-day timeline is an image and could not be read."),
            ("Assignment 2b", "XLSX, 3 sheets, 28 formulas", "Weekly Metrics model, a populated sample pipeline row, and a 'How to Use' tab."),
            ("Assignment 3", "DOCX, 29 paras, 1 table", "Five-week plan as a 3-row table, DEO email, and an email to the Head of Growth."),
            ("Reflection &amp; AI Note", "DOCX, 13 paras", "Separate document — the only candidate to submit the reflection and AI disclosure as a standalone file."),
        ],
        docs_note="<strong>Six documents — three times the pool norm — and the only submission that did NOT arrive through Markaz.</strong> She replied to the case-study email with a link to her own Drive folder (\"Arooj Khalid - Case Study, Taleemabad\"), organised into one subfolder per assignment. There is no Markaz submission notification for her, so anyone checking Markaz or scanning notifications would conclude she never submitted.",
        a1="""<strong>Her headline finding is the most immediately actionable in the whole round, and the
        benchmark missed it.</strong> Lesson-plan users adopt coaching at <strong>12.9% against the 6.4%
        platform base</strong> — 22 of 170, verified exact. That is roughly double, and it identifies
        <em>"the warm audience"</em> hiding inside the very feature she had just correctly dismissed as a
        one-time utility: <em>"The lesson plan feature isn't the destination, but it is a useful
        bridge."</em> Unlike every other insight in this round, it hands you a targetable list on Monday
        morning.<br><br>
        <strong>Her analytical method is also distinct — she is the only candidate to work in medians</strong>,
        deliberately, <em>"to keep the numbers from being skewed too much,"</em> and to add a
        <strong>"used it only once"</strong> column. That combination makes the one-time-utility argument far
        more convincingly than means would: coaching 35 users, 31% once-only, median 3 sessions, 11.2 median
        days on platform, 97% registered; reading 13, 31%, 2 sessions, 8.2 days, 69%; lesson plans 170,
        <strong>73% once-only</strong>, 1 session, 1.0 day, 60%; presentations 91, <strong>88%
        once-only</strong>, 1 session, 1.4 days, 45%. Her conclusion follows cleanly: lesson plans and
        presentations <em>"behave like one-time utilities: generate something once, then leave,"</em> while
        coaching and reading are used repeatedly and <em>"the typical user is still active over a week
        later."</em>""",
        a1_noise="""296 users (54% of the platform) who only ever chat and never touch another feature, plus
        124 (23%) who never finished registration but use the app — <em>"both groups look like curiosity, not
        intent."</em> She then adds a note the others did not: if we wanted to convert them,
        <em>"we could develop a strategy for that"</em> — correctly parked rather than pursued.""",
        a1_pri="""(1) Pakistan's verified-teacher segment. (2) <strong>Coaching and reading themselves,
        "wherever they can be replicated" — including Sri Lanka.</strong> This is the one place she takes the
        opposite position to all five other candidates. Rather than stopping or holding Sri Lanka, she argues
        the zero adoption <em>"doesn't mean that Sri Lankan teachers simply don't want these features. It
        could mean a possible context change, strategy revision, or testing the features with slight tweaks
        in the country,"</em> and makes it her second double-down with Experiment 2 designed to
        <em>"tell the difference before we write it off."</em> Defensible, and she has built the diagnostic —
        but she commits a priority slot to a market everyone else de-prioritised, which is the most important
        strategic disagreement in the round to test at debrief.""",
        a1_exp="""<strong>1. Nudge warm Pakistan users into a first coaching session</strong> — built
        directly on her own 12.9%-vs-6.4% finding, prioritising lesson-plan users first, one WhatsApp message
        after their session with a one-tap start link. Kill under 5% starting within 7 days, with the right
        conclusion attached: <em>"The nudge isn't the bottleneck, so I would stop and look at the Coaching
        flow itself instead of the messaging."</em><br>
        <strong>2. Root-cause Sri Lanka's zero adoption</strong> — 50 registered users invited to Reading
        Assessment rather than coaching, and her reasoning for choosing it is a real product insight:
        <em>"the simpler of the two features, since it just needs a student to read aloud in their preferred
        language."</em> Kill under 3% → channel-market mismatch, stop the feature push and escalate for a
        localisation review.<br>
        <strong>3. Recover coaching sessions that start but never finish</strong> — 25% never complete, so an
        automatic WhatsApp reminder 2 hours after an incomplete start, half treatment half control, kill
        under a 5-point lift. Note this targets the <em>same</em> non-completion problem Shahmir found, from
        the other direction: she treats it as friction to be nudged, he diagnosed it with median-audio
        evidence as a bug to fix in week 1. Both are valid; his is the stronger read of the same number.""",
        a2="""<strong>She is the only candidate who refuses the framing of the question, and she is
        right:</strong> <em>"This is not a 60-day project that finishes on day 60. It is a loop, and the plan
        below is one full turn of it. Every time a new teacher is identified, the same sequence starts again
        at Stage 1."</em><br><br>
        Seven stages, each with timeline, activity, owner/channel, frequency and outcome — and crucially her
        triggers are <strong>thresholds rather than dates</strong>: a growth rep calls or visits once a
        school hits <strong>2 active teachers</strong>, <em>"instead of waiting to be asked"</em>; Day-3 and
        Day-7 check-ins after every session; teachers with 2+ good cycles are asked to forward; new schools
        get a reply within 24 hours. Her breakpoint contingency carries the best single line in her
        submission: <em>"the session is not the finish line."</em><br><br>
        <strong>Her stakeholder map is the most locally literate of the six</strong> — she names AEOs, DEOs,
        DDEOs and SDEOs specifically, with district officials brought in only once school-level evidence
        exists. She also lists her three assumptions openly, including that referral-tracking instrumentation
        is presumed to exist.""",
        a2_k="""K = shares sent per active teacher × the percentage of those shares that convert into a new
        active teacher or school, explained in plain operator terms — <em>"A K of 0.2 means every 10 active
        teachers bring in 2 new ones through sharing alone"</em> — with the honest expectation that it
        <em>"would not exist from the beginning, but built up during the first few 60-day cycles."</em> She
        assumes the metrics would load into the sheet automatically from user data rather than by hand. Her
        tracker is the only one with a <strong>"How to Use" tab</strong> — she wrote operating instructions
        for whoever inherits her spreadsheet, which is a small thing that says something real about how she
        hands work over.""",
        a2_breaks="""<strong>The teacher gets good feedback but never tells the admin</strong> — <em>"sharing
        a win isn't something most teachers think to do on their own."</em> Contingency: don't wait for the
        teacher; auto-send the "share with your principal" note within 48 hours and call admins directly once
        a school crosses 2 active teachers.<br>
        <strong>A session happens but teachers stop using the feature afterwards</strong> — <em>"if usage
        drops after the session, there's nothing left worth referring."</em> Contingency: personal follow-up
        on Day 3 and Day 7 rather than showing everything at once.""",
        a3_prob="No number given — 'at risk rather than committed'",
        a3="""<strong>This is her weakest assignment and the reason her total sits at 70 — but it also
        contains the single most locally shrewd move in the round.</strong><br><br>
        The move: she attaches <strong>a draft letter for the selection of the 200 schools</strong> — and in
        her internal note, a draft letter for constituting the selection committee — so the DEO's office has
        less to write. Alongside Shahmir's "which section holds the file, what is the diary number," this is
        the most genuinely Pakistani-bureaucracy-aware instinct anyone showed: reduce the paperwork burden on
        the official rather than adding to it. She also says she would not rely on email alone — a similarly
        worded <strong>formal letter to the office</strong>, plus meetings with the SDEO and DDEO, which is
        how district offices actually move. And she is one of only two candidates to ask whether the delay
        was <em>our</em> fault: <em>"whether it was on our end or the DEA."</em><br><br>
        <strong>What is missing is structural.</strong> The five-week plan is a three-row table (Week 1 /
        Weeks 2–3 / Weeks 4–5) rather than a sequenced plan with gates, so there are no decision points and
        no defined contact order. There is no escalation path if the DEO stays silent, and no scoped fallback
        if 200 schools will not fit the cycle. Most tellingly, her Weeks 4–5 row <strong>assumes the deal
        lands</strong>: <em>"ensure notification of our product deployment in 200 schools... Begin deployment
        and remain in consistent contact with the DEA."</em> There is no branch for a no — which, in an
        exercise built entirely around a deal that has gone quiet, is the gap to press hardest.""",
        a3_email="""Warm, respectful and well-pitched to a government reader — credits the district and the
        head teachers, states the agreed 200-school scale-up, attaches the draft selection letter, and offers
        to support any adjustments or documentation. Where it is weaker than the best of the six: the ask
        stays broad (<em>"your continued support"</em>) rather than shrinking to one thing the DEO could
        answer in a sentence, and it does not name the budget deadline as a concrete date to work back from.""",
        a3_internal="""An email rather than a status update, and honest in substance — she is transparent
        that she would keep it <em>"at risk rather than committed given the lost time and the five-week
        budget deadline,"</em> and specific about what she is doing: the DEO email, the draft committee
        letter, the PA contact, an in-person office visit, and tapping her own network for a meeting.
        <strong>But there is no probability figure, no gating events, and no explicit ask of the Head of
        Growth</strong> — the brief asked for the honest probability and what help she needs, and this
        delivers neither cleanly.""",
        reflection="""<strong>The strongest domain-relevant reflection of the six.</strong> Newly joined and
        shaping a national project, her organisation had agreed with the lead partner to work across eight
        districts while delivering 10% of the overall target. She interrogated the reasoning: her org's model
        was to establish hubs in half the districts, a model it had <em>"rigorously tested"</em> and she
        believed in — but the donor wanted clear district-level ownership with one partner working directly
        with government. Critically, <strong>she names the risks in her own organisation's preferred
        model</strong>: <em>"overlapping roles, complex governance, and potential delays."</em> With neither
        side willing to move, she <em>"navigated sensitive partner dynamics and raised the issue repeatedly
        in senior management discussions."</em> Outcome: direct implementation in two districts at 10% of
        target while training other partners, plus increased school visits elsewhere to maintain technical
        oversight. Her lesson is the most mature sentence in any of the six reflections:
        <em>"good strategy requires knowing what must be protected, what can adapt, and how to make both
        work within a complex system."</em> Multi-partner, donor-facing, government-adjacent — the closest
        match to this role's actual terrain.""",
        verified="""Her 12.9%-vs-6.4% lesson-plan-to-coaching bridge recomputed and matched exactly (22 of
        170). Her median-based feature table and country figures also check out. Her rounding is coarser than
        the others' (44%, 13%, 4% rather than 43.8%, 12.8%, 4.2%), which is a presentation choice rather than
        an error.""",
        thin="""<strong>Her analysis workbook contains zero formulas and no raw data</strong> — both sheets
        are pasted static tables, so nothing in her Assignment 1 can be re-derived from her own file. That
        matters more given her AI disclosure, which is the most extensive of the six: she asked AI to analyse
        the data, to create the tables, and to build the spreadsheet. She is admirably candid about it —
        including that she would have asked Claude to assess her work as a Taleemabad recruiter
        <em>"but by then I had run out of Claude messages"</em> — but the combination of no working and heavy
        generation means her Assignment 1 is the least auditable in the pool despite its findings being
        correct.<br><br>
        Assignment 3 lacks a probability, gates, escalation and any branch for failure (above). Assignment 1a
        contains an unfinished, garbled sentence (<em>"do are the only real proof on this platform"</em>) —
        a proofreading miss. And her 60-day timeline is an image, so the timeline itself could not be
        assessed from the document; her stage table carried the plan instead.""",
        probes=[
            "Your lesson-plan-to-coaching bridge, 12.9% against a 6.4% base, is the most actionable finding anyone produced. What would you do with it in your first week, and how many teachers does it actually reach?",
            "Every other candidate would slow down or stop Sri Lanka. You made it a priority to double down on. Defend that with the 52% of Sri Lankan registered users who teach university only and have no class to record.",
            "Your five-week plan ends with 'begin deployment.' What happens in week five if the DEO has still not replied and the budget cycle closes?",
            "Your spreadsheet has no formulas and no raw data, and your AI note says you had AI analyse the data and build the tables. If I ask you to recreate the 12.9% figure from the CSVs in front of me, can you?",
            "You attached a draft school-selection letter for the DEO's office. Where did that instinct come from, and what else have you pre-written for a government counterpart?",
        ],
    ),
]


def stat_boxes():
    boxes = [("6", "Shortlisted", "#1a2b4c"), ("16", "Documents read", "#2f6fb5"),
             ("595k", "Characters", "#1b7f4d"), ("1", "Not assessable", "#b3261e")]
    tds = "".join(
        f'<td style="width:25%;padding:6px;"><div style="background:{c};border-radius:6px;'
        f'padding:16px 8px;text-align:center;">'
        f'<div style="font-family:Georgia,serif;font-size:26px;color:#fff;font-weight:bold;">{n}</div>'
        f'<div style="font-family:Arial,sans-serif;font-size:10.5px;color:#dbe5f5;'
        f'letter-spacing:0.8px;text-transform:uppercase;margin-top:4px;">{l}</div></div></td>'
        for n, l, c in boxes)
    return ('<table role="presentation" width="100%" style="width:100%;border-collapse:collapse;'
            f'margin:18px 0;"><tr>{tds}</tr></table>')


def ranked_table():
    head = "".join(f'<th style="background:#1a2b4c;color:#fff;padding:8px 6px;font-size:11px;'
                   f'text-align:center;">{d}</th>' for d in DIMS)
    rows = []
    for i, c in enumerate(CANDS):
        nm = f'<a href="{c["link"]}" style="color:#2f4fa2;">{c["name"]}</a>'
        cells = "".join(
            f'<td style="text-align:center;padding:8px 6px;border-bottom:1px solid #e6e9ef;">{s}</td>'
            for s in c["scores"])
        rows.append(
            f'<tr style="background:{"#ffffff" if i%2==0 else "#f5f7fa"};">'
            f'<td style="padding:8px 10px;border-bottom:1px solid #e6e9ef;">{nm}<br>'
            f'<span style="font-size:11px;color:#6b7a90;">App {c["app"]} &middot; '
            f'{len(c["docs"])} doc{"s" if len(c["docs"])>1 else ""}</span></td>'
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


def sec(label, colour, body):
    return (f'<div style="font-family:Arial,sans-serif;font-size:10.5px;letter-spacing:1.2px;'
            f'text-transform:uppercase;color:{colour};font-weight:bold;margin-top:20px;">{label}</div>'
            f'<p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;'
            f'margin:7px 0 0;">{body}</p>')


def doc_table(c):
    rows = "".join(
        f'<tr><td style="padding:6px 10px 6px 0;font-family:Georgia,serif;font-size:13.5px;'
        f'color:#1a2b4c;font-weight:bold;vertical-align:top;white-space:nowrap;">{n}</td>'
        f'<td style="padding:6px 10px 6px 0;font-family:Arial,sans-serif;font-size:12px;'
        f'color:#2f6fb5;vertical-align:top;white-space:nowrap;">{t}</td>'
        f'<td style="padding:6px 0;font-family:Georgia,serif;font-size:13.5px;color:#3d4c5c;'
        f'vertical-align:top;">{d}</td></tr>'
        for n, t, d in c["docs"])
    return (f'<div style="background:#f5f7fa;border-left:3px solid #2f6fb5;padding:12px 16px;'
            f'margin-top:14px;">'
            f'<div style="font-family:Arial,sans-serif;font-size:10.5px;letter-spacing:1.2px;'
            f'text-transform:uppercase;color:#1a2b4c;font-weight:bold;margin-bottom:6px;">'
            f'Submitted &mdash; {len(c["docs"])} document{"s" if len(c["docs"])>1 else ""}</div>'
            f'<div style="overflow-x:auto;"><table role="presentation" style="border-collapse:collapse;">'
            f'{rows}</table></div>'
            f'<p style="font-family:Georgia,serif;font-size:13.5px;line-height:1.7;color:#3d4c5c;'
            f'margin:10px 0 0;">{c["docs_note"]}</p></div>')


def deep_dives(subset):
    out = []
    for c in subset:
        probes = "".join(f'<li style="margin:7px 0;">{p}</li>' for p in c["probes"])
        verdict = "PROCEED to case study debrief" if c["proceed"] else "DO NOT proceed to debrief"
        vcol = "#1b7f4d" if c["proceed"] else "#b3261e"
        out.append(f"""
<div style="border:1px solid #dfe3ea;border-radius:8px;margin:26px 0;overflow:hidden;">
  <div style="background:{c['colour']};padding:14px 20px;">
    <span style="font-family:Georgia,serif;font-size:19px;color:#fff;">{c['name']}</span>
    <span style="font-family:Arial,sans-serif;font-size:13px;color:#e4ecf8;">
      &nbsp;&middot;&nbsp; App {c['app']} &nbsp;&middot;&nbsp; {c['total']}/100 &nbsp;&middot;&nbsp; {c['band']}</span>
  </div>
  <div style="padding:18px 20px 22px;">
    {doc_table(c)}
    {sec("Assignment 1 &mdash; what the analysis actually says", "#1b7f4d", c['a1'])}
    {sec("Assignment 1 &mdash; what they called noise", "#6b7a90", c['a1_noise'])}
    {sec("Assignment 1 &mdash; the two priorities they chose", "#1b7f4d", c['a1_pri'])}
    {sec("Assignment 1 &mdash; the three experiments", "#2f4fa2", c['a1_exp'])}
    {sec("Assignment 2 &mdash; the growth loop", "#2f4fa2", c['a2'])}
    {sec("Assignment 2 &mdash; how they measure K", "#2f4fa2", c['a2_k'])}
    {sec("Assignment 2 &mdash; where they say it breaks", "#2f4fa2", c['a2_breaks'])}
    <div style="background:#eef3fb;border-radius:6px;padding:10px 14px;margin-top:20px;
                font-family:Arial,sans-serif;font-size:13px;color:#1a2b4c;">
      <strong>Assignment 3 &mdash; their stated probability:</strong> {c['a3_prob']}</div>
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
</div>""")
    return "".join(out)


INTRO = """
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:6px 0 0;">
    This is the detailed version, written so that reading it replaces reading the submissions.
    Every document was re-sourced and read end to end for this report &mdash; 16 files, 595,215
    characters, every narrative page and every spreadsheet tab. Each candidate is covered
    assignment by assignment, with what they found, the numbers they used, the experiments they
    designed, how they would measure the loop, their stalled-deal probability, and what is thin.
    <strong>Scores are unchanged from the 17 August report</strong> &mdash; this is a deeper
    write-up of the same evaluation, not a re-score.</p>
  <p style="font-family:Georgia,serif;font-size:13.5px;line-height:1.7;color:#7b341e;
            background:#fdf6ec;border-left:3px solid #c47f16;padding:10px 14px;margin:14px 0 0;">
    <strong>Sent in two parts.</strong> The full report is too long for one email &mdash; Gmail
    clips anything over about 100KB behind a "view entire message" link, which would hide half of
    it. Part 1 covers Shahmir, Arshan and Yusra; Part 2 covers Umar, Junaid and Arooj plus the
    method note. The ranking table appears in both so each part stands on its own.</p>"""

SEPARATES = """
  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">What separates them</h2>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Nobody fabricated data.</strong> Every headline figure across all six submissions was
    recomputed from the raw CSVs and matched. The pool separates on three things instead.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>First, whether they distrusted the obvious metric.</strong> Sri Lanka registers better
    than Pakistan and has never touched either flagship feature. Every candidate spotted it; they
    differ in what they did next. Arshan rebuilt the metrics because active_week1 is 99% true and
    useless. Yusra ran a falsification test on her own hypothesis. Junaid explained the mechanism
    causally. Shahmir found that no Sinhala or Tamil reading passage exists at all. Arooj alone
    argued for doubling down on Sri Lanka rather than pausing it.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Second, whether the work is auditable.</strong> Only Yusra and Umar submitted workbooks
    in which the analysis can be re-derived from the data inside the file. Shahmir's numbers are
    right but live in Python outside his workbook; Arooj's workbook has no formulas and no raw data
    at all. For a role that will be asked to defend numbers in a room, that gap is worth probing.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Third, Assignment 3 is what actually spread the scores.</strong> The analysis quality is
    tightly bunched; the stalled-deal response is not. Shahmir, Arshan, Yusra and Umar all gave a
    number and said what would move it. <strong>Junaid and Arooj gave no probability at all</strong>,
    against an explicit instruction in the brief, and that single omission is most of the distance
    between 74/70 and the high 80s. Umar's forecast discipline is the strongest of the six; his DEO
    email is the weakest.</p>"""

METHOD = """
  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Method &amp; limits</h2>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    Scored against <em>smg_execution_sprint_benchmark.md</em> using the six-dimension rubric.
    For this report every submission was re-downloaded and read in full: PDFs page by page, Word
    documents including all tables, and every spreadsheet tab opened with a formula count so that a
    live model could be told apart from pasted values. Findings quoted are the candidates' own
    words.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Two things I could not assess, stated plainly.</strong> Shahmir's reflective response is
    an <em>.m4a</em> voice note that cannot be transcribed on this machine, so one of his six
    dimensions carries no evidence and his 98 remains provisional on it. Arooj's 60-day timeline and
    some in-document charts are images, so they were not read; her stage table carried the plan
    instead. Everything else in all six submissions has been read directly.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>One sourcing finding worth acting on.</strong> Arooj's submission never generated a
    Markaz notification &mdash; she replied to the case-study email with a link to her own Drive
    folder. Markaz shows nothing, and a scan of submission notifications shows nothing. Any process
    that relies on either would have recorded her as a non-submitter. She scored 70 and is in
    tomorrow's debrief.</p>"""


def build_html(part):
    subset = CANDS[:3] if part == 1 else CANDS[3:]
    names = ", ".join(c["name"].split()[-1] if c["name"] != "Muhammad Arshan Bilal" else "Arshan"
                      for c in subset)
    return f"""<!--[if mso]><table role="presentation" width="880" align="center"><tr><td><![endif]-->
<div style="background:#eef1f6;padding:22px 12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
       style="width:100%;max-width:880px;margin:0 auto;background:#ffffff;border-radius:8px;
              border:1px solid #dfe3ea;">
 <tr><td style="background:#1a2b4c;padding:24px 30px;border-radius:8px 8px 0 0;">
   <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1.6px;
               text-transform:uppercase;color:#93a7c9;">Taleemabad &middot; Talent Acquisition</div>
   <div style="font-family:Georgia,serif;font-size:23px;color:#fff;margin-top:6px;">
     SMG Case Study &mdash; Full Evaluation Report &middot; Part {part} of 2</div>
   <div style="font-family:Arial,sans-serif;font-size:13px;color:#c3d0e6;margin-top:8px;">
     Job 42 &middot; Senior Manager Growth &middot; 18 August 2026 &middot; {names}</div>
 </td></tr>
 <tr><td style="padding:24px 30px 34px;">

  {stat_boxes() if part == 1 else ""}
  {INTRO if part == 1 else ""}

  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:28px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Ranking</h2>
  {ranked_table()}
  <p style="font-family:Arial,sans-serif;font-size:12px;color:#6b7a90;margin:8px 0 0;">
    Dimensions scored 1&ndash;5. Weights: Data 20% &middot; Execution 25% &middot; Stakeholder 20%
    &middot; Commercial 15% &middot; Discipline 10% &middot; Signal 10%. All six scored 70+ and all
    six were invited to debrief on 18 August.</p>

  {SEPARATES if part == 1 else ""}

  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 4px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Candidate detail
             {"&mdash; 1 to 3 of 6" if part == 1 else "&mdash; 4 to 6 of 6"}</h2>
  {deep_dives(subset)}

  {METHOD if part == 2 else ""}

 </td></tr>
 <tr><td style="background:#f5f7fa;padding:16px 30px;border-top:1px solid #dfe3ea;
        border-radius:0 0 8px 8px;font-family:Arial,sans-serif;font-size:12px;color:#6b7a90;">
   Taleemabad Talent Acquisition &middot; hiring@taleemabad.com &middot; 18 August 2026</td></tr>
</table></div>
<!--[if mso]></td></tr></table><![endif]-->"""


def main():
    load_dotenv(os.path.join(ROOT, ".env"))
    pw = os.getenv("EMAIL_PASSWORD")
    if not pw:
        raise SystemExit("EMAIL_PASSWORD missing")
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER, pw)
    for part in (1, 2):
        html = build_html(part)
        size = len(html.encode())
        if size > 100_000:
            raise SystemExit(f"BLOCKED: part {part} is {size:,} bytes - Gmail would clip it")
        msg = MIMEMultipart("alternative")
        msg["Subject"] = SUBJECT.replace("| Job 42", f"- Part {part} of 2 | Job 42")
        msg["From"] = SENDER
        msg["To"] = ", ".join(RECIPIENTS)
        msg.attach(MIMEText("HTML report - view in an HTML-capable client.", "plain"))
        msg.attach(MIMEText(html, "html"))
        safe_sendmail(s, SENDER, RECIPIENTS, msg.as_string(),
                      context=f"smg_case_study_evaluation_v2_deep_part{part}")
        print(f"Part {part} sent to {RECIPIENTS} - {size:,} bytes")
    s.quit()


if __name__ == "__main__":
    main()
