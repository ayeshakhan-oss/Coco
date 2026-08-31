"""
SMG Case Study Evaluation — ROUND 2 (Job 42) — DEEP READ — PILOT to Ayesha.

Ayesha's brief 2026-08-24: "read each and every document and each and every line,
compare with our benchmark answer."

SCOPE: the six SMG candidates who submitted AFTER the 17-18 August evaluation and have
never been scored. The eight already scored (Shahmir, Arshan, Yusra, Umar, Junaid,
Arooj, Irfan, Basit) are not re-opened here.

METHOD:
  - Benchmark FIRST (rubric Rule 0). The answer key already existed and was QA'd for the
    17 August round; it was re-read before any round-2 submission was opened, and no
    round-2 material has been added to it (benchmark hygiene, 2026-08-17).
  - Every deliverable retrieved and read end to end: 21 files across the six candidates.
    Narrative documents page by page and slide by slide; every spreadsheet tab opened
    with formulas preserved so a live model can be told from pasted values.
  - Figures were NOT checked against our own summary table. The raw 546-row
    01_master_user_dataset was recovered from a candidate workbook, independently
    revalidated against the benchmark ground truth (546 rows, PK 265 / SL 261, 43.8% /
    45.6% registration, 62.9% / 19.3% repeat, 35 coaching adopters, 118/88 sessions,
    5 spikes) — every figure reproduced exactly — and then used to recompute each
    candidate's headline numbers.

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
SUBJECT = "[PILOT - ] SMG Case Study - Evaluation Report, Round 2 (6 new submissions) | Job 42"

DIMS = ["Data", "Execution", "Stakeholder", "Commercial", "Discipline", "Signal"]

CANDS = [
    dict(
        name="Furqan Afzal", app="4145", total=93, band="STRONG YES", proceed=True,
        colour="#1b7f4d", scores=[4, 5, 5, 4, 5, 5],
        link="https://drive.google.com/drive/folders/14NEkhsEd-73qEJ8RZFcUeikVxNFMw0Lo",
        docs=[
            ("Assignment 1 Slides", "PPTX, 6 slides", "Country landscape, two leverage areas, three experiments. Every claim carries its n."),
            ("Assignment 1 Workbook", "XLSX, 11 sheets, live formulas", "Raw_Users (547 rows), Data_Overview, Country_Analysis, Feature_Segments, Cohort_Trend, Daily_Activity, Experiment_Tracker plus the raw country and aggregate files. The analysis can be re-derived inside the file."),
            ("Assignment 2 Growth Loop Plan", "DOCX", "Stage-by-stage plan with an automation/assumptions table and a breakpoint table."),
            ("Assignment 2 Tracker", "XLSX, 3 sheets, live formulas", "Pipeline_Tracker, Weekly_Metrics_KFactor (auto-calculating realised K plus a leading indicator), Breakpoint_Log. Worked example rows included and marked for deletion."),
            ("Assignment 3 Stalled Deal", "DOCX", "Ten-step contact plan, the DEO email, internal update."),
            ("Reflective Response", "DOCX, 179 words", "Self-counted word count stated at the foot."),
        ],
        docs_note="Submitted 23 August via Markaz as a Drive folder link (app 4145). Worth knowing the context: he emailed on 21 August saying he had never received the case study, then on 22 August that the dataset tab appeared missing. He started at noon on 23 August, spent two hours, took a break, and spent a further 45 minutes reviewing &mdash; all of which he volunteered unprompted in his submission note. <strong>This is the most time-pressured submission in the pool and the second-highest scoring.</strong>",
        a1="""<strong>He scopes before he analyses.</strong> 546 users across 12 countries, but
        96.3% sit in two of them and the other ten average under four users each, so he excludes them
        explicitly rather than quietly. Then the central read:
        <em>"Registration and Week-1 activity look almost identical between the two. The split only
        shows up once you look at coaching/reading adoption."</em> Country 92 registers 43.8% and
        Country 94 registers 45.6%; coaching adoption is 12.8% against <strong>0%</strong>, reading
        4.2% against 0%. Average lifespan 4.92 days against 1.81.
        <br><br>His strongest single move is one nobody else in either round made.
        Rather than writing Sri Lanka off, he refuses to call it until a prior question is answered:
        <em>"nothing in this dataset tells us whether that's low demand or the feature never reaching
        them. First step before writing it off: confirm with the team whether coaching/reading were
        even live and localized in Country 94 during this window."</em> That is the difference between
        a demand conclusion and an access conclusion, and the data genuinely cannot separate them.""",
        a1_noise="""He does not run a separate noise section; he prices the thinness into each claim
        instead. Reading is his second leverage area at n=11 and he says so plainly:
        <em>"Honest caveat: n=11 is thin. This is a discovery problem, not a proven-at-scale one."</em>
        The cross-feature overlap behind Experiment 3 is n=3 and he flags it as
        <em>"directionally suggestive, not statistically robust. That thinness is exactly why this is
        framed as an experiment, not a conclusion."</em> The ten minor countries are excluded from
        everything downstream.""",
        a1_pri="""(1) <strong>Coaching in the Country 92 school-affiliated segment</strong> &mdash;
        29.1% adoption there against 0% in every other country/school combination, coaching users at
        5.38 average active days against a 1.26 chat-only baseline, and 12.04-day lifespan against
        1.3. (2) <strong>Reading Assessment as a discovery problem</strong> &mdash; the highest
        retention of any Country 92 segment at 5.45 active days and 12.29-day lifespan, on n=11.
        Picking a base of eleven is the most debatable call in his submission and he argues it
        knowingly rather than by accident.""",
        a1_exp="""(1) <strong>Coaching-first onboarding.</strong> 117 school-affiliated signups, 34
        activate coaching, <em>"83 qualifying users (70.9%) never activate coaching today. Nothing in
        the flow routes them there."</em> Week 1: WhatsApp nudge to record a first lesson within 24h
        against a control. Kill: test group under 10% after two weeks.
        (2) <strong>Warm versus broadcast acquisition</strong> &mdash; targeted push through 3-5
        partner schools, tagged distinctly against concurrent broadcast. Kill: no 2&times; lift.
        (3) <strong>Surface reading to coaching completers</strong> &mdash; auto follow-up after every
        coaching completion. Kill: under 15% try it and no retention lift. He also queues a
        prerequisite that is not an experiment: confirm feature availability in Country 94.""",
        a2="""<strong>The most operationally serious plan in the pool.</strong> Seven loop stages,
        each tagged by who actually acts &mdash; an automated system trigger, a system-assisted step a
        Growth Associate still sends personally, or a fully manual relationship step. He then writes
        the assumptions down as a table: WhatsApp business-initiated messages need five Meta-approved
        templates submitted in week 1 (<em>"approval typically takes 24-48h, confirm with engineering
        before Day 1"</em>); admin WhatsApp numbers are not captured at school registration today, so
        if that field cannot be added in 60 days <em>"Stage 3 reverts to fully manual... Slower, but
        the loop still runs"</em>; and stages 4 and 6 stay manual deliberately because
        <em>"relationship-sensitive moments... convert worse when templated."</em> Phases overlap by
        design (days 1-14, 5-30, 15-50, 25-60, 30-60) rather than running as clean sequential blocks.""",
        a2_k="""K = new schools that ask in during the period, tagged loop-attributable via a
        "How did you hear about us?" source field, divided by active schools at the start of the
        period. Paid and broad-broadcast acquisition are <em>"tracked and excluded separately."</em>
        He then adds something no one else did: because realised K lags conversion time, he defines a
        <strong>separate weekly leading indicator</strong> &mdash; referral actions taken this week
        (admin invites + teacher shares + district mentions) over active schools &mdash; and reads it
        alongside realised K every two weeks. His tracker calculates both automatically.""",
        a2_breaks="""Stage 3, the administrator never noticing, which he identifies as
        <em>"the one fully organic, passive step in the loop... most of the loop's value dies quietly
        right here."</em> Contingency is to remove the dependency on noticing altogether: auto-generate
        the Impact Snapshot and pair it with direct outreach the same week. Second, teachers not
        transferring or sharing &mdash; <em>"a discretionary, low-frequency action nobody is naturally
        motivated to take"</em> &mdash; answered by naming champions early and making the ask specific
        and light (one voice note). His Breakpoint_Log has a worked entry showing a real stall, the
        contingency applied, and the process fix that followed.""",
        a3_prob="40&ndash;50% within this budget cycle.",
        a3="""A ten-step contact sequence with dates, channels and a specific ask at each step. It
        opens with pilot head teachers for an informal read on what is happening inside the DEO's
        office, then procurement for a factual status check <em>"(not the DEO)... No pressure on the
        DEO"</em>, then the DEO. The governing principle is stated up front:
        <em>"every touch this cycle leads with value or new information, never just 'checking in'...
        any escalation is flagged to the DEO first so it reads as urgency, not distrust. The budget
        deadline is used as a real, external fact, stated plainly, not as manufactured pressure."</em>
        Step 9 escalates to the Provincial Education Secretary <em>with a heads-up call to the DEO
        first</em> &mdash; <em>"The DEO is told this is happening, not surprised by it."</em>""",
        a3_email="""About 130 words, and he states the count and the reason:
        <em>"a busy official reads this in under a minute, and nothing in it asks for an immediate
        decision, only a small, easy next step."</em> It opens with news rather than a request &mdash;
        the pilot is holding up, nearby schools have asked to join informally &mdash; then names the
        deadline as a fact (<em>"I wanted to flag it now while there's still time to act"</em>), then
        asks for fifteen minutes and offers to send data, documentation or a phased option. It never
        asks why he has not heard back.""",
        a3_internal="""40&ndash;50%, with the reasoning separated into what is real and what is
        warning: <em>"The DEO's praise did not read as courtesy either, so the interest is genuine.
        However, six weeks of silence plus a vague procurement status is a real warning sign."</em>
        Three asks: a reserved senior-to-senior call if his own outreach fails by end of week 2, a
        decision on whether a phased 100+100 commitment can be offered, and awareness that
        <em>"even if this specific deal slips, we may need a parallel plan to protect the existing 40
        schools from the competitor now active in the district."</em>""",
        reflection="""179 words, and the best in the round. At Weather Walay he was told to run a
        giveaway-led acquisition formula <em>"without pushback"</em>, saw that users were
        <em>"subscribing for the prize, not the service, and churning right after entry closed"</em>,
        and built an alternative creative approach <strong>on his own</strong> &mdash; then tested it
        alongside the giveaway rather than replacing it, so the data could settle it. Ends on the
        transferable point: <em>"a strategy can hit its top-of-funnel number and still be quietly
        broken underneath it."</em> Specific, costly to admit, and the outcome is quantified.""",
        verified="""Every headline figure reproduced exactly from the raw data: PK coaching adoption
        12.8%, reading 4.2%, SL both 0%, has_school 44.2% / 45.6%, school-affiliated n=117 with 29.1%
        coaching adoption, coaching-user active days 5.38 and lifespan 12.04, coaching-only active
        days 4.74, PK reading n=11 with 5.45 active days and 12.29 lifespan, weekly cohorts
        15/76/21/57/81/13, and 35.5% coaching adoption in the week beginning 10 November.
        His AI disclosure is the most precise of any submission in either round &mdash; per
        deliverable, and specific about what Claude did against what he directed and reviewed.""",
        thin="""<strong>He found the Nov-10 week, not the Nov-14 day.</strong> Working in weekly
        cohorts, he correctly reports 35.5% coaching adoption for the week beginning 10 November, but
        the sharper fact is inside it: a single day, 14 November, produced 40 users and
        <strong>23 of the platform's 35 coaching adopters</strong>. The weekly view dilutes a
        two-thirds concentration into a 35.5% average.
        <br><br><strong>Consent is not raised anywhere.</strong> His Stage 3 fix auto-generates an
        Impact Snapshot from a teacher's coaching result and sends it to that teacher's administrator.
        That is precisely the loop's real failure mode &mdash; classroom evidence reaching a teacher's
        boss without permission &mdash; and it is the one thing the case never prompts for. He is not
        alone in missing it, but his design makes it automatic rather than incidental.
        <br><br><strong>The probability is a range, not a number</strong>, and he does not say what
        would move it upward. Two minor arithmetic slips: the coaching-and-reading overlap is 4 users
        rather than 3, and PK reading completion is 57.7% by session count (his 63.6% is
        users-who-completed over users-who-started &mdash; a defensible denominator, not an error).""",
        probes=[
            "Your Impact Snapshot goes from a teacher's coaching result to that teacher's administrator automatically. Walk me through what you would tell a teacher about that before their first recording.",
            "You reported 35.5% coaching adoption for the week of 10 November. If I tell you 23 of the platform's 35 coaching adopters all signed up on 14 November alone, what changes in your plan?",
            "You picked Reading as a leverage area on eleven users and said so honestly. What would have to be true in the first three weeks for you to drop it, and what would you spend that effort on instead?",
        ],
    ),
    dict(
        name="Hania Khan", app="4035", total=90, band="STRONG YES", proceed=True,
        colour="#1b7f4d", scores=[5, 5, 4, 5, 5, 2],
        link="https://drive.google.com/drive/folders/18WfPtlukeeRbzgjsk8MsNXdb745E1H73",
        docs=[
            ("Final Memo", "PDF, 8 pages", "Assignments 1, 2 and 3 in one document. No reflective response."),
            ("Combined Assignment Spreadsheets", "XLSX, 13 sheets, live formulas", "Eight Assignment 1 analysis tabs including an explicit Method &amp; Notes tab, then a 41-column School Pipeline tracker, a Weekly Dashboard and a Lists &amp; Definitions tab."),
        ],
        docs_note="Submitted <strong>by email on 21 August</strong> after the Markaz portal upload failed &mdash; she sent a screenshot of the error with her files. <strong>Markaz has no submission record for her at all</strong> (app 4035, case_study_status still null), so any process reading Markaz alone would record her as a non-submitter. She also has a duplicate application, 4037, sitting in rejected.",
        a1="""<strong>The most careful reader of the dataset in this round.</strong> Her framing is
        that this is <em>"a quality-of-activation problem, not a registration-volume problem"</em>,
        and she earns it: Pakistan and Sri Lanka register at 43.8% and 45.6% but repeat at 46.4%
        against 20.7%, with lifespans of 4.92 and 1.81 days.
        <br><br>Three things nobody else in this round caught.
        First, the attribution hole, stated as an operating constraint:
        <em>"The master source field is 'direct' for all 546 users, so future experiments must
        explicitly tag institution, channel, onboarding variant and follow-up."</em>
        Second, a data-quality discrepancy she went looking for:
        <em>"The aggregate file reports 240 completed registrations while the strict master indicator
        gives 239; user-level analysis uses the strict master indicator."</em> Both numbers are
        correct &mdash; registration_state says completed for 240 rows, the completed_registration
        flag is true for 239 &mdash; and she is the only person in either round to reconcile them.
        Third, the coaching experience itself is failing at a measurable rate: <strong>22.9% of
        coaching sessions fail</strong>, which becomes the spine of her second bet and her first
        breakpoint.""",
        a1_noise="""Four things she refuses to treat as signal, each with the reason: countries
        outside PK/LK, where <em>"high percentages on n=2&ndash;5 should not drive strategy"</em>;
        signup spikes without downstream use, which she calls real acquisition but not compounding
        &mdash; <em>"I would optimize events on retained users, not registrations"</em>; Reading at
        13 users, <em>"I would not infer Product&ndash;Channel Fit from that sample yet"</em>; and
        late-December cohorts, which she treats as early signals rather than retention outcomes
        because they have less time to mature inside the six-week window. She also states plainly
        that <em>"historical feature relationships are associations, not causal effects."</em>""",
        a1_pri="""(1) <strong>Replicate the Pakistan institutional acquisition that produces retained
        users</strong>, starting with Secondary teachers &mdash; n=64, 5.95 sessions, 4.05 active days,
        9.69-day lifespan, against Primary at 4.49/2.96/7.49 and Uni/College at 3.29/2.43/5.48.
        (2) <strong>Convert General Chat into successful Coaching activation</strong> &mdash; coaching
        reaches 6.4% of users but 97.1% of them repeat, and Pakistani coaching users average 8.29
        sessions. She argues Chat is the entry point rather than the destination, and answers the
        obvious objection in a footnote about why not Lesson Plans.""",
        a1_exp="""All three are properly controlled and all three carry a labelled success rule.
        (1) <strong>Chat-first institutional onboarding</strong> against a standard
        registration/demonstration cohort, at 2-4 comparable introductions, tagging institution,
        segment and variant. Kill: under 5 percentage points of lift after two cohorts.
        (2) <strong>Contextual Chat &rarr; Coaching prompt</strong>, randomised, measuring
        <em>successful</em> activation (completed first coaching over eligible chat users) and killing
        it not only on weak lift but <em>"if failure rises above the historical 22.9%, or if prompting
        materially reduces General Chat repeat engagement"</em> &mdash; a guard against winning one
        metric by damaging another. (3) <strong>Guided against self-serve first coaching</strong>,
        measured in <em>retained successfully coached teachers per staff hour</em>. That is the only
        unit-economics metric anyone proposed in this round.""",
        a2="""Opens with the rule the rest of the plan obeys:
        <em>"Every stage ends with a named owner, a dated next action and a measurable exit criterion.
        'Administrator interested' is not a pipeline stage; 'administrator call booked for Thursday'
        is."</em> Seven stages, each with action, owner, channel and an explicit exit. She defines what
        an activated school actually means &mdash; a whole-school session held plus at least three
        teachers completing a first coaching experience within seven days &mdash; and marks it as an
        assumption to calibrate in the first fortnight. She also makes a deliberate restraint call:
        <em>"I would avoid prizes or referral rewards for teachers during the first 60 days to observe
        the loop's organic referral behavior without contaminating the signal."</em>
        <br><br>Consent appears without being prompted, in the loop design and again in Assignment 3.""",
        a2_k="""School-level: K = average qualified school referrals per activated school &times;
        referral-to-activated-school conversion, target 0.20, worked as 0.8 &times; 25%. Both
        components are tracked weekly and separately, realised K is reported only on mature cohorts,
        and <em>"raw WhatsApp forwards do not count."</em> Her tracker enforces it in formulas: every
        referred school is entered as a new row carrying a Referring School ID, so attribution is
        structural rather than manual, and the dashboard decomposes K into its two drivers, flags
        overdue next actions, and marks any school sitting in one stage past a threshold.""",
        a2_breaks="""First, the first coaching outcome failing &mdash; anchored to her own 22.9%
        finding, with every failed seed-teacher attempt getting follow-up within 24 hours, a logged
        failure reason and a supported retry, patterns escalated weekly to Product, and a hard
        restraint: <em>"I would not aggressively scale a school where teachers are repeatedly entering
        a broken experience."</em> Second, teacher value never reaching the administrator, answered by
        making the handoff systematic within 48 hours of documented improvement, with consent, plus
        two concrete session options.""",
        a3_prob="25% &mdash; the most conservative figure in either round.",
        a3="""Two parallel tracks for five weeks, a relationship track and a deal-execution track. Week
        1 is four factual questions to procurement (where the file is, whose approval is pending, what
        is outstanding from us, the latest date to make this budget) with a hard gate:
        <em>"If I cannot establish those four things by the end of Week 1, I would classify the deal
        as materially at risk."</em> Every meeting must end with <em>owner + action + date</em>. On
        the competitor: <em>"I would not attack the competitor"</em> &mdash; instead she lists the
        incumbency advantages, including <em>"ability to expand without restarting the learning
        curve."</em>""",
        a3_email="""Well judged in its business half. It asks for 10&ndash;15 minutes, poses two
        precise questions (is the expansion still a district priority, and what is the single most
        important next action from our side before the window closes), and offers immediate turnaround
        on any documentation. <strong>But it opens with a gift.</strong> She proposes sending a
        physical "Classrooms of Pakistan" package to the DEO's office to mark Independence Day, and
        the email leads with it for three paragraphs before reaching the business ask.""",
        a3_internal="""The strongest forecast discipline in either round. 25%, treated as materially
        at risk, with the single best line on commercial honesty across all fourteen submissions:
        <em>"I will not increase deal probability based on a positive conversation alone. I will
        increase it when we have a named owner, dated next action and viable path into the current
        budget."</em> She then does something no one else did &mdash; rather than one probability, she
        defines the diagnosis that has to come first: is this a process delay, a budget constraint, or
        a loss of sponsorship? Support asks are staged by week, and the escalation is conditional:
        <em>"I will only trigger that escalation once I can give you the specific blocker and desired
        outcome."</em>""",
        reflection="""<strong>Missing.</strong> The brief asks for a reflective response of 200 words
        or fewer as an explicit final deliverable. Her memo ends at the Assignment 3 internal update
        and neither file contains one. Her AI disclosure is present and good &mdash; per deliverable,
        and it distinguishes AI structuring and editing from her own Stata analysis and judgment
        &mdash; but half of this dimension has nothing to score.""",
        verified="""Every figure reproduced exactly: PK/SL repeat 46.4% and 20.7%, the 240-versus-239
        registration discrepancy, coaching users repeating at 97.1%, PK coaching users at 8.29 average
        sessions, the 14 November cohort at 87.5% repeat and 4.88 sessions, the 26 November Sri Lankan
        cohort at n=98 with 27.6% repeat and 1.96 sessions, chat reach 433 users / 79.3%, and all four
        grade-segment rows. Her 22.9% coaching failure rate is drawn from the coaching-sessions status
        field rather than started-minus-completed (which gives 25.4%) &mdash; the more precise of the
        two, not an error.""",
        thin="""<strong>The missing reflective response is a required deliverable, and it costs her
        the top of the ranking.</strong> On the six dimensions she is otherwise the equal of anyone in
        either round; this single omission moves her from roughly 96 to 90.
        <br><br><strong>The gift package needs a decision from us, not from her.</strong> Sending a
        physical package to a serving government official while a procurement file on our own contract
        is live is a real compliance exposure, whatever the intent. To her credit she fences it twice
        &mdash; <em>"Subject to Taleemabad's normal stakeholder-engagement practices"</em> and, in her
        assumptions, <em>"Taleemabad stakeholder-gifting policy... would be confirmed before
        execution"</em> &mdash; so she has flagged it as a policy question rather than assumed a
        green light. It is still the instinct to probe. The related cost is that her DEO email spends
        its opening on the package and reaches the ask late.
        <br><br><strong>She cites the 14 November cohort but not its concentration</strong> &mdash;
        that 23 of 35 platform-wide coaching adopters came from that single day.""",
        probes=[
            "Your reflective response is not in either file. Tell me now, in two minutes: a time you saw a strategy failing on the ground and flagged it early, what it cost you, and what happened.",
            "Talk me through the Independence Day package. If our legal or finance lead said no gifts to a serving official while a procurement file is open, what does your week-one reopening look like instead?",
            "You said you would not raise the probability on a positive conversation alone. In week three the DEO calls, is warm, and promises to push it. What number do you report, and what do you tell the Head of Growth?",
        ],
    ),
    dict(
        name="Shafaq Syed", app="4137", total=75, band="YES", proceed=True,
        colour="#2f6fb5", scores=[2, 4, 4, 5, 4, 4],
        link="https://drive.google.com/drive/folders/195rAhn6i9QFm8Z1AxLOWYI_7lexYRHh6",
        docs=[
            ("Taleemabad Case Study", "PDF, 9 pages", "All three assignments plus the reflection in one continuous document."),
            ("Case study data working", "XLSX, 12 sheets", "A tabulated 168-row summary sheet, a strategy working tab, an experiment scorecard, and five tracker templates."),
        ],
        docs_note="Submitted 20 August via Markaz (app 4137), Word and Excel uploaded properly. <strong>Read the data note below before reading her scores</strong> &mdash; her Assignment 1 rests on a belief about the dataset that turns out not to be true, and it may be our problem rather than hers.",
        a1="""<strong>She identified the right strategic object and then analysed it with one hand
        tied.</strong> The thesis is correct and well put: <em>"Do not optimise for activity. Identify
        the behaviours that create value, turn that value into proof, and make the proof travel from
        teacher to teacher and school to school."</em> She builds it on coaching &mdash; 34 coaching
        starters and 32 users with a completion in Pakistan, both exact &mdash; and reads Sri Lanka as
        a second-session problem: 79.3% of Sri Lankan users are active on only one day, and 80.8% of
        their sessions are General Chat.
        <br><br>The problem is what she believed she had. Three times she states that the supplied file
        is <em>"an aggregate 14-metric summary, not the per-user dataset described in the brief"</em>
        and that <em>"country, cohort, language, source, and week-level retention cuts are therefore
        not observable."</em> They were observable; the 546-row per-user file exists and four other
        candidates in this round worked from it. Everything downstream of that belief is missing as a
        result: no cohort analysis, no acquisition-spike work, no attribution finding, and a
        high-intent behavioural intersection she designed but declared uncomputable.""",
        a1_noise="""A genuinely good section, and the most disciplined about denominators in the round.
        Generic Chat volume &mdash; <em>"High volume is not the outcome"</em>. Reading &mdash; 87
        starts and 51 completions, correct to the row. Audio/video &mdash; too small. Small markets
        &mdash; PK plus SL is 526 of 546, so the rest stay exploratory. She adds a caveats block on
        Pakistan registration friction (only 40.5% of registration-time entries immediate, 41.4% at
        20+ hours) and warns against reading infrastructure noise as weak demand.""",
        a1_pri="""(1) <strong>Pakistan: teacher value &rarr; champion &rarr; school</strong>, built on
        coaching completion as the proof-generating event. (2) <strong>Sri Lanka: Chat &rarr;
        structured value &rarr; second session</strong>, an English-first chat experience that
        recommends one lesson plan or task and creates a 24-hour reason to return.""",
        a1_exp="""Three, each with a hypothesis, a week-1 action, a numeric success rule, a kill
        criterion and the fit it tests &mdash; the cleanest experiment scorecard format in the round.
        Teacher Champion &rarr; School Introduction (kill: fewer than 2 qualified admin replies from
        20 shares); Registration Recovery Concierge (kill: under 15% recovery after 30 contacts);
        Sri Lanka 24-Hour Return Loop (kill: under 5 percentage points of lift after 100 exposed
        users). She also separates two experiments others would have merged, and explains why:
        one tests the product transition into structured value, the other tests whether that value
        produces a second session.""",
        a2="""Seven loop steps with owner, channel, action and a conversion metric each, and a 60-day
        cadence carrying numeric exit criteria &mdash; 25 teachers invited and 10 first completions by
        day 10; 50% first coaching completion and 20% admin response by day 25; three school-wide
        sessions and 60% attendee activation by day 40. Stakeholder cadence is specified per layer
        (teachers weekly with a cap of two reminders per action, administrators bi-weekly and
        event-triggered, district officials biweekly, asked for <em>"convening power and access, not
        day-to-day execution"</em>). Her trackers are well-designed but empty templates &mdash; the
        columns are right, nothing is worked through.""",
        a2_k="""K = average qualified invites sent per activated teacher &times; invite-to-activated
        conversion, with a stated control point of 0.8 &times; 25% = 0.20. Clean and correctly
        decomposed. She then repeats the dataset claim &mdash; that user-level intersections are not
        observable &mdash; and proposes the tracker establish the baseline from day 1 instead.""",
        a2_breaks="""Teachers completing coaching but not sharing proof (early warning: under 30% of
        completers consent to or forward proof) answered by co-creating the proof in the debrief,
        offering anonymised school-level evidence and asking for a warm introduction rather than a
        public testimonial. And administrator interest not converting to a scheduled session (early
        warning: no date within 7 days) answered with two fixed dates and a 30-minute low-lift option.
        Consent appears here, which is to her credit.""",
        a3_prob="35% for a full close, 60% for a budget-preserving or phased commitment.",
        a3="""Structured week by week with a contact order, a specific ask and an exit criterion for
        each. The strongest part is a short block called <strong>Relationship safeguards</strong>:
        reference the DEO's earlier support positively, <em>"avoid 'six weeks of silence'"</em>, make
        it easy to respond with a choice of two times or a forwarding instruction, and
        <em>"Do not imply commitment, bypass authority, or manufacture urgency. Anchor every
        escalation to the budget timetable and the need to complete the administration's own
        process."</em> That is an unusually mature articulation of how to handle a government sponsor
        who has gone quiet.""",
        a3_email="""Short, well-judged and correctly aimed. Subject:
        <em>"20-minute decision check-in on the 200-school expansion."</em> It thanks the DEO for the
        public support, names the five-week window, asks to <em>"agree on the shortest path to a
        decision"</em>, offers two time options, and then gives the DEO a graceful exit:
        <em>"If another colleague is now leading the file, I would be grateful if you could direct me
        to them so we can support the process without adding to your workload."</em> Her own note on
        why: <em>"It creates a graceful path for the DEO to delegate the file without loss of
        face."</em>""",
        a3_internal="""The two-number framing is sophisticated &mdash; 35% for the full close and 60%
        for a phased or budget-preserving outcome, which is a more useful thing to give a Head of
        Growth than one blended figure. Gating is explicit: by end of week 2 she requires a named
        owner, a documented procurement path and a dated decision milestone, and
        <em>"If any are missing, downgrade the opportunity and activate senior sponsor support."</em>
        Pipeline status amber-red, kept in commit only on those conditions. Four specific asks
        including authority to offer a phased rollout within approved pricing guardrails, and a clear
        line that the competitor <em>"should not drive unproductive discounting or pressure."</em>""",
        reflection="""Strong. Coordinating the Digitalization of Parliament programme across the
        Senate and National Assembly, she saw a workplan that assumed government sign-off, EU funding
        and vendor delivery would move in a straight line when in fact each was waiting on the others
        &mdash; <em>"yet portfolio reviews kept reporting steady progress."</em> She mapped where the
        bottlenecks actually sat and <em>"replaced broad status language with dated actions, named
        owners, and explicit escalation points."</em> The lesson is specific and transferable:
        <em>"momentum dies in the handoffs between institutions and vendors, not in the strategy
        itself."</em>""",
        verified="""Checked against the raw data and correct: PK active 2+ days 46.4%, SL single-day
        79.3%, SL 25+ messages 7.7%, SL chat share 80.8%, PK chat share 65.6% (she said 65.4%), PK
        lesson-plan share 24.5% (she said 24.4%), PK coaching 34 starters and 32 completers, reading
        87 starts and 51 completions, PK+SL 526 of 546. Two small misses: she reports 11 Pakistani
        reading starters among 117 registered users when it is 8 among 116 (11 is all Pakistani
        reading users), and 94% of registered Sri Lankan users choosing English when it is 100%.
        Neither changes a conclusion. AI use is disclosed on every page, honestly and broadly:
        Microsoft Copilot <em>"used to structure the analysis, calculate supplied metrics, and draft
        the deliverable."</em>""",
        thin="""<strong>The data score is about one belief, and we should check whether it is our
        fault before holding it against her.</strong> She worked from a pre-tabulated 168-row summary
        and stated three times that the per-user file was not supplied. Furqan independently reported
        on 22 August that the dataset tab appeared missing from the same case-study document. If the
        data tab was genuinely not reachable for some candidates, this is a distribution failure on
        our side and her Data score of 2 should be revisited on that basis. If she had the file and
        did not open it, the 2 stands. <strong>Her Assignment 1 is the only part of her submission
        that is weak, and it is weak for a reason we can resolve in ten minutes.</strong>
        <br><br>Whichever it is, the consequences are real in the submission as it stands: no cohort
        or spike analysis at all, so the 14 November concentration is absent; the source-attribution
        gap is never named; and she recommends an eight-week Sri Lanka bet without noting that
        Sri Lanka has produced <strong>zero</strong> coaching and reading adopters from 261 users.
        <br><br><strong>Her trackers are empty templates.</strong> The column design is sound, but
        nothing is worked, so there is no evidence of the thing actually being used.""",
        probes=[
            "You wrote three times that the per-user dataset was not supplied. Show me what you opened and where you looked, so we can work out whether that was our distribution failure or a retrieval one.",
            "Sri Lanka is 261 users, zero coaching adopters and zero reading adopters. Given that, defend spending a third of an eight-week plan there.",
            "Your relationship-safeguards block is the best thing in your submission. Tell me about the government sponsor who went quiet on you in real life, and what you actually did.",
        ],
    ),
    dict(
        name="Lamis Maniar", app="4062", total=73, band="YES", proceed=True,
        colour="#2f6fb5", scores=[5, 3, 3, 4, 4, 3],
        link="https://drive.google.com/drive/folders/1hJVx3spKg8zKCOUSZ8UutUsomH0qWBI2",
        docs=[
            ("Assignment 1 vFinal", "PPTX, 7 slides", "Priorities, country comparison, feature comparison, a five-cohort table, deprioritisation call, three experiments, AI declaration."),
            ("Assignment 1 Analysis vFinal", "XLSX, 12 sheets, live formulas", "Key Findings, Country/Feature/Segment/Cohort Analysis, a K-Factor Calculator, a 107-row Growth Loop Tracker, plus all four raw source files."),
            ("Assignment 2 &mdash; 60 Day Growth Loop Execution Plan", "DOCX", "Prose plan in five dated phases."),
            ("Assignment 2 workbook", "XLSX", "K-factor calculator and the operating tracker."),
            ("Assignment 3 &mdash; The Stalled Deal", "DOCX", "Five-week plan, DEO email, internal update."),
            ("Reflective Response", "DOCX", "Separate file; also bundled in the combined PDF."),
        ],
        docs_note="Submitted 20 August via Markaz (app 4062) &mdash; Word and Excel uploaded <em>and</em> a Drive folder link, so her work arrived twice over. Six distinct deliverables, the most complete package in the round. She also has a duplicate application, 4063, sitting in rejected.",
        a1="""<strong>The best data work in this round, and the best cohort analysis in either
        round.</strong> Her Cohort Analysis tab does what nobody else managed: it takes all five
        acquisition spikes and splits each one by country, registration, sessions, multi-day rate,
        D7 return and adoption of every feature. That single table dissolves several traps at once.
        14 November: 40 users, all Pakistani, 82.5% registration, 87.5% multi-day,
        <strong>57.5% coaching adoption</strong>. 26 November: 100 users of whom 98 are Sri Lankan,
        29% multi-day, <strong>zero</strong> coaching. 2 December she labels
        <em>"presentation-heavy burst; very weak D7 return"</em> &mdash; 65.7% presentation adoption
        and 5.7% D7. 11 December: 86 users, 74.4% registration, 8.1% multi-day.
        <br><br>She reads the registration trap correctly: Pakistan 44%, Sri Lanka 46%, therefore
        <em>"Sri Lanka's main problem does not appear to be registration. It is what happens after
        acquisition."</em> And she declines to cut it &mdash; <em>"I would not recommend abandoning
        Sri Lanka. I would put it into diagnostic mode"</em> &mdash; which is a defensible call
        argued rather than assumed.""",
        a1_noise="""Feature by feature, with base sizes attached and a different verdict for each:
        coaching is <em>"a retention product"</em>, lesson plans <em>"an activation product"</em>,
        presentations <em>"more like a demo/use-once feature"</em> at 1.15 uses per adopter and 12%
        repeat, and reading <em>"too concentrated to justify growth investment yet"</em> because
        <strong>one user alone accounts for 64% of all reading starts</strong>. Her deprioritise list
        names presentation-led event spikes, indiscriminate Sri Lanka acquisition, and
        <em>"events measured only by registrations."</em>""",
        a1_pri="""(1) <strong>Pakistan institutional cohorts &rarr; Secondary teachers &rarr;
        Coaching.</strong> Her sharpest segment cut: registered Pakistani Secondary teachers, n=65,
        averaging 5.98 sessions, 81.5% multi-day activity and 49.2% coaching adoption &mdash; against
        a 12.8% all-Pakistan baseline. (2) <strong>Lesson Plans as the broad activation wedge</strong>
        &mdash; 170 users at 31.1% of the base, with Pakistani lesson-plan adopters at 4.82 sessions
        and 44.2% D7 against 2.09 and 14.7% for non-users. Coaching is deep and narrow; lesson plans
        are shallow and wide; she uses each for what it is good at.""",
        a1_exp="""(1) <strong>Replicate 14 November</strong> in 2-3 Pakistani secondary schools, with
        the teacher completing registration <em>and</em> a first coaching submission during the
        session. Success: 70% registration, 30% coaching completion within 72h, 40% D7. Kill: after
        two cohorts, under 15% coaching completion or D7 under 20%.
        (2) <strong>"Tomorrow's Lesson" activation</strong>, A/B against standard onboarding with
        day-2 and day-5 WhatsApp prompts. (3) <strong>Teacher proof &rarr; admin handoff</strong>
        after two coaching completions. Kill: under 10% admin conversations after 20 eligible
        teachers. All three carry real numeric thresholds.""",
        a2="""<strong>The gap between her Assignment 1 and her Assignment 2 is the story of this
        submission.</strong> The plan is sensible, correctly sequenced and written in fluent prose
        &mdash; 10-15 schools, one champion each, coaching as the target first action with lesson
        plans as an easier fallback, WhatsApp follow-up in 24-48 hours, administrator introduction
        only after the teacher has seen value, and a deliberate instinct to
        <em>"agree a date for the school session during the same conversation rather than leaving it
        as an open follow-up."</em> But it is written as a narrative rather than an operating
        document: no named owners, and the phase exits are questions to review
        (<em>"Which schools moved most quickly...?"</em>) rather than numeric thresholds. Her tracker
        is live and well-built &mdash; 21 columns, formula-driven K, referral IDs &mdash; which makes
        the softness of the plan itself the odder gap.""",
        a2_k="""School-level and decomposed into three inputs in a working calculator: 50% of
        activated schools generating at least one referral &times; 1 referred school each &times; 40%
        activating = 0.20. In the narrative she states it as <em>"10 active schools &rarr; 2
        additional active schools"</em> and adds the right instinct:
        <em>"I would also track the steps behind this number so that if the K-factor is low, we can
        see whether the problem is a lack of referrals or poor conversion of referred schools."</em>
        She does not flag that she has changed the unit of measurement from teachers to schools.""",
        a2_breaks="""Teachers trying coaching once and not returning, answered with fast follow-up and
        lesson plans as an easier route; and the teacher-to-administrator handoff never happening,
        answered by making the handoff deliberate and helping the teacher share the evidence. Both are
        correct and both are the obvious two. No early-warning thresholds are attached to either, so
        there is nothing that would tell her a breakpoint had been hit.""",
        a3_prob="40%, moving to 60% on named owner and dated milestone within a week.",
        a3="""Sensible and correctly ordered &mdash; procurement first to locate the file, DEO in
        parallel, then a pilot-side contact in week 2 <em>"not to go around the DEO"</em>, then all
        relevant parties into one conversation in week 3 rather than continuing separate follow-ups,
        then careful escalation. Two good instincts: escalation framed
        <em>"on the budget deadline rather than on the lack of response from the DEO"</em>, and
        continuing to engage the 40 pilot schools because a competitor is in the district and
        <em>"I would not want Taleemabad to disappear from the schools while the government process is
        delayed."</em> Week 5 ends on a commitment to honesty: document why, secure a written next
        step, and <em>"update the opportunity honestly rather than leaving it in the pipeline as if it
        is still likely to close."</em>""",
        a3_email="""The weakest part of a strong submission. Subject:
        <em>"Follow-up on the 200-school expansion."</em> It is polite, correctly brief, thanks the
        DEO for the support and names the budget window. But it accepts the stall passively
        (<em>"I understand the file is currently going through the internal process"</em>), the offer
        is to send more material rather than to remove work, and the ask is
        <em>"Would you be available for a short call sometime this week?"</em> &mdash; open-ended,
        undated, and asking the DEO for a decision rather than for a person. It could have been sent
        to any stalled contact in any sector.""",
        a3_internal="""Honest and correctly gated. 40%, with the distinction that matters:
        <em>"I am still positive about the opportunity itself... My concern is the process."</em>
        Movement is defined in both directions &mdash; a named owner, an outstanding-actions list and
        a dated milestone within the week takes it to 60%; absence of those by end of next week drops
        it significantly and triggers escalation. Two asks: who steps in for senior escalation, and
        whether there is flexibility on scope or commercial terms.""",
        reflection="""Real but the mildest in the round. At Impetus, field teams resisted a digital
        data-collection process for an immunisation programme because it added work during demanding
        campaigns; she proposed piloting in one smaller district first, worked the issues with the
        team, showed them the dashboards, and it expanded once they saw the value. It is a true story,
        told plainly. What it does not have is a cost to her, a moment where she was arguing against
        the room, or a consequence if she had stayed quiet &mdash; and the closing lesson
        (<em>"listening to what is happening on the ground, testing on a smaller scale"</em>) is the
        generic version of the point.""",
        verified="""Her figures are the most accurate in the round, essentially to the decimal:
        35 coaching adopters, 3.37 starts per adopter, 75% completion, 69% repeat, 97% multi-day; 170
        lesson-plan users at 31.1% and 1.62 uses each; 91 presentation users at 1.15 uses; 13 reading
        adopters with one user at 64% of starts; Pakistani lesson-plan adopters at 4.82 sessions
        against 2.09; and every cell of the five-cohort table. Her Secondary segment reads n=65 /
        5.98 sessions / 81.5% multi-day / 49.2% coaching where the raw file gives 64 / 5.95 / 81.2% /
        48.4% &mdash; a one-row difference in how a multi-grade teacher was bucketed, not an error of
        substance.""",
        thin="""<strong>Her analysis is a 5 and her execution is a 3, and for a 2IC role that carries
        40-60% travel, execution is the weighted dimension.</strong> The 60-day plan has no named
        owners and no numeric exit criteria; it reads as a well-reasoned intention rather than
        something a growth associate could be handed on Monday.
        <br><br><strong>The DEO email is generic.</strong> It is the one deliverable where she does
        not bring the specificity she shows everywhere else.
        <br><br><strong>Two data misses.</strong> She never states outright that Sri Lanka has zero
        coaching and zero reading adopters &mdash; it is implicit in her cohort notes but never made
        the finding &mdash; and she does not catch that the source column reads "direct" for all 546
        users, so her three channel experiments would not be attributable if run today.
        <br><br><strong>Her AI declaration is thinner than her work implies.</strong> Assignments 2
        and 3 say AI was used <em>"to proofread the draft and help revise the wording and structure"</em>;
        Assignment 1 says it supported the data analysis. Given the depth of the cohort table, that
        is worth a direct question rather than an assumption.""",
        probes=[
            "Your cohort table is the best piece of analysis in this round. Take me through how you built it, which tab you started in, and what you tried that did not work.",
            "Hand me your 60-day plan as if I am the growth associate running it. Who owns day 12, and what number tells me on day 21 that it is going wrong?",
            "Rewrite the opening two sentences of your DEO email out loud. Assume he has read six weeks of our follow-ups and answered none of them.",
        ],
    ),
    dict(
        name="Kanooz Ahmed Siddiqui", app="4111", total=62, band="BORDERLINE", proceed=False,
        colour="#c47f16", scores=[4, 3, 2, 3, 4, 3],
        link="https://drive.google.com/drive/folders/1AQy-QpAQDnkXuu7nPlGlcvY2BHNmSAaL",
        docs=[
            ("Assignment 1 &mdash; Analysis", "Google Sheet, 9 tabs", "Full 546-row master dataset plus country pivots, a grade-analysis tab and a country-mapping tab."),
            ("Pakistan vs Sri Lanka Analysis", "Google Slides, 6 slides", "The Assignment 1 memo, delivered as a deck."),
            ("Assignment 2 &amp; 3", "Google Doc", "Loop table, weekly metrics, the DEO email, internal update and the reflective essay."),
        ],
        docs_note="Submitted 19 August via Markaz (app 4111) as three Google links with a per-deliverable AI-use note against each. Her workbook is the file from which the raw 546-row dataset was recovered for this round's verification &mdash; it is the most complete raw-data submission in the pool. She also has a duplicate application, 3811, sitting in rejected from Job 41.",
        a1="""<strong>An original segmentation nobody else found, and the cleanest statement of the
        Sri Lanka problem in either round.</strong> Slide 2 puts it flatly:
        <em>"Nearly identical sign-up and registration-completion rates &mdash; but Sri Lanka has never
        converted a single registrant into a coaching or reading user."</em> Pakistan coaching
        completion 75.65%, Sri Lanka 0.00%. Both figures are exact.
        <br><br>Her original contribution is <strong>grade breadth</strong>. Rather than asking which
        grade a teacher teaches, she asks how many: Pakistani registered teachers who select multiple
        grades adopt coaching at 44.2% (n=43) against 19.2% for single-grade teachers (n=73). Inside
        the single-grade group the spread is enormous &mdash; Secondary 50%, Uni/College 12.5%,
        Primary 3.0%, Early Years 0%. She also notes that reading skews the opposite way from
        coaching, toward Early Years and Primary. That is a real, actionable targeting rule that the
        benchmark answer does not contain.""",
        a1_noise="""Explicit and correctly reasoned: Sri Lanka at 0% feature adoption on matching
        volume; single-grade Primary teachers at 3.0% coaching; single-grade Early Years at 0% on both
        features. She is willing to name segments she would not spend against, which is more than most
        submissions do.""",
        a1_pri="""(1) Pakistani multi-grade teachers. (2) Pakistani Secondary teachers plus coaching.
        Both follow directly from her own numbers, which is the point.""",
        a1_exp="""Three, and their <strong>kill criteria are the best-constructed in the round</strong>
        because each is anchored to a measured baseline rather than a round number: target
        Secondary/multi-grade schools, kill at or below the 12.8% all-Pakistan coaching baseline;
        remind the 83 Pakistani teachers who registered but never touched coaching, same baseline;
        cross-sell reading to coaching users, kill at or below the 8.8% organic crossover rate. A
        threshold that says "no better than doing nothing" is a genuinely disciplined way to write a
        kill criterion. What they are not, though, is channel experiments &mdash; all three are
        targeting and messaging tests, and the assignment asked about Product&ndash;Channel and
        Channel&ndash;Model fit.""",
        a2="""A day-banded loop table with three actor columns &mdash; Growth Team, Teacher,
        Administrator &mdash; which correctly forces her to say what each party does at each step. One
        strong instinct: at the stage where the administrator notices, her Growth Team instruction is
        <em>"Support the teacher in sharing the win if needed; <strong>do not approach the
        administrator first</strong>"</em>. That is a candidate running the loop as designed rather
        than quietly replacing it with direct sales, which is exactly what the assignment asked for
        and what several stronger submissions did not resist. Beyond that the plan thins out: no
        tracker file, no numeric exit criteria per phase, and the weekly metrics are a bullet list of
        field names rather than an operating cadence.""",
        a2_k="""Defined cleanly: <em>"loop-generated new active teachers &divide; existing active
        teachers; track toward 0.2. Only teacher-sharing/referral acquisitions count as
        loop-generated."</em> That last clause is the one that matters and she includes it. What is
        missing is any working of the number, any decomposition into drivers, or any instrument to
        collect it.""",
        a2_breaks="""Two, both tied to observable fields, which is a nice touch &mdash; a teacher
        signing up but never reaching coaching, detected on <em>active_week1 = FALSE</em>, answered
        with a targeted call; and a teacher having a win the administrator never notices, answered by
        helping the teacher articulate and share it. Neither carries a threshold that would trigger a
        change of approach rather than more of the same.""",
        a3_prob="40%, at risk, not treated as a committed close.",
        a3="""A five-week table with sensible content: internal questions first, then the DEO with a
        pilot results report, then procurement to confirm file status and the next approval step, then
        a testimonial video, then a call, then escalation, then either final approvals or
        <em>"Mark as at-risk/deferred and maintain the relationship for the next budget cycle."</em>
        The ordering is right and procurement is worked in parallel rather than after. It is thinner
        than the field on gates: nothing in the plan says what result would make her stop, downgrade,
        or change route.""",
        a3_email="""<strong>The weakest deliverable in the round, and the reason her total sits where
        it does.</strong> It is warm, courteous and correctly short, and it does contain one good move
        &mdash; attaching a pilot results report so the DEO has something to circulate internally. But
        <strong>it never mentions the budget deadline.</strong> The entire scenario turns on five
        weeks to a cycle close after which the expansion waits a year, and the email that is supposed
        to reopen the relationship omits it entirely. The ask is
        <em>"We would welcome the opportunity to meet with you at a time convenient for you"</em>
        &mdash; undated, open-ended, and requesting a meeting rather than a named person or a specific
        next action. Nothing in it would make a busy official who has already ignored six weeks of
        contact respond this week rather than next month.""",
        a3_internal="""Honest in its framing and correct in its status &mdash;
        <em>"I would keep it in the pipeline but not treat it as a committed close"</em> &mdash; but
        it is four sentences and a support line. There is no reasoning behind the 40%, nothing that
        would move it in either direction, no dated gate, and the support ask is
        <em>"Pilot results/testimonials, and escalation guidance if stalled"</em>, which asks the Head
        of Growth to supply the judgment rather than the resource.""",
        reflection="""True and clearly her own, but the smallest stakes in the round. A donor told her
        they only heard from the organisation once a year; she introduced a donor tagging system with
        reporting frequency by type, at least quarterly. The closing line is genuinely good &mdash;
        <em>"a strategy can work on paper but still not work for the people it is meant to serve"</em>
        &mdash; but the brief asks for a strategy failing <em>on the ground</em> that she flagged
        early, and this is a reporting-cadence improvement prompted by someone else's remark rather
        than something she spotted and raised against resistance.""",
        verified="""Correct almost throughout: Pakistan coaching completion 75.65% and reading
        completion 57.69% both exact to two decimals; coaching users at 5.57 average active days
        against 1.57 for non-users, and reading users at 5.62 against 1.73, all exact; multi-grade
        n=43 at 44.2% coaching, exact; 83 Pakistani registered teachers who never coached, exact;
        the 12.8% and 8.8% baselines, exact. Her single-grade counts run one row high (74 against 73,
        Secondary 25 against 24, so 20.3% against 19.2% and 52.0% against 50.0%) &mdash; a bucketing
        difference, not a fabrication. AI use is disclosed per deliverable and specifically.""",
        thin="""<strong>Assignment 1 is a 4 and Assignments 2 and 3 are not close to it.</strong> The
        imbalance is the finding. Her analysis is original and exact; the execution plan has no
        tracker, no thresholds and no dated exits; and the stalled-deal work omits the deadline the
        whole scenario is built on.
        <br><br><strong>One causal overclaim.</strong> Her slide is titled <em>"Features Drive
        Retention, Not Just Correlate"</em>, and the evidence underneath is a cross-sectional
        comparison of active days between feature users and non-users. That comparison cannot separate
        cause from selection &mdash; engaged users do more of everything &mdash; and the headline
        asserts precisely the thing the data cannot support. Candidates in the first round hit this
        same fork and volunteered the objection themselves.
        <br><br><strong>No cohort or spike work at all.</strong> The five acquisition events, and the
        fact that one day produced two-thirds of all coaching adopters, are absent. She also does not
        catch the source-attribution gap, which matters because her three experiments would not be
        attributable as designed.""",
        probes=[
            "Your grade-breadth cut is the most original finding in this round. What made you look at how many grades a teacher selects rather than which one?",
            "Read your DEO email back and tell me what a district officer would do after reading it. Then tell me why the five-week budget deadline is not in it.",
            "Your slide says features drive retention rather than just correlate with it. What in the data separates those two, and what would you need to run to actually show it?",
        ],
    ),
    dict(
        name="Rimsha Taj", app="3956", total=45, band="NO", proceed=False,
        colour="#b3261e", scores=[1, 3, 3, 2, 2, 2],
        link="https://drive.google.com/drive/folders/1cplnC8M84DO9Zia11tum6gdT3KXBje57",
        docs=[
            ("SMG Consolidated Recruitment Test", "PDF, 11 pages", "All three assignments plus the reflection."),
            ("SGM Assignment 1 and 2", "XLSX, 4 sheets, live formulas", "An A1 pivot-working tab, a 546-row master extract cut to 13 columns, and an A2 daily tracker."),
        ],
        docs_note="Submitted 19 August via Markaz (app 3956), Word and Excel uploaded properly, and separately emailed. Her arithmetic is careful and her tracker has real formulas &mdash; the failure here is not effort or care, it is which columns she chose and what she then built on them.",
        a1="""<strong>She measured the platform's flagship feature with the wrong column, and the
        whole submission follows from it.</strong> The dataset carries two different coaching fields.
        <em>audio_coaching_sessions</em> sums to <strong>1</strong> across all 546 users.
        <em>coaching_started</em> sums to <strong>118</strong> across 35 adopters, with 88 completions.
        She used the first. Her conclusion:
        <em>"Audio coaching and video are particularly weak signals: almost no users engage with audio
        coaching... These features currently do not generate enough repeated behaviour to justify
        significant investment."</em> The feature she recommends deprioritising is the one the case
        describes as the core value proposition, and the one holding all of the platform's real
        retention.
        <br><br>Her country work is accurate &mdash; Pakistan 3.16 sessions and 2.26 active days
        against Sri Lanka's 1.71 and 1.36, all exact &mdash; and her school-affiliation cut is exact
        too. But she reads registration-day and week-1 activity as a comparison point (Sri Lanka 100%,
        Pakistan 98%) without noticing that the field is true for 540 of 546 users and therefore
        cannot discriminate anything.""",
        a1_noise="""She names audio coaching, video and general chat as the non-compounding signals.
        Two of those three are defensible. The third is the flagship, and it is the one place in this
        pool where a candidate's "noise" list contains the answer.""",
        a1_pri="""<strong>Both priorities rest on a broken ratio.</strong> She recommends doubling
        down on lesson planning and presentations, on the evidence that
        <em>"Users engaging with lesson plans average 4.47 active days, while presentation users
        average 11.1 active days."</em> Neither number means that. In her workbook, cell K6 is
        <code>AVERAGE(K4:K5)</code> where K4 is <code>K2/J2</code> &mdash; the sum of active days for
        <em>every Pakistani user</em> (599) divided by the count of <em>lesson-plan sessions</em>
        (205). Numerator and denominator describe different populations, so the result is not active
        days per lesson-plan user; the true figure is 2.58. The presentation version is worse: 11.1 is
        the average of 599/75 and 356/25. Because presentations are the <em>least</em>-used feature,
        the smaller denominator mechanically produces the largest number &mdash; so the metric ranks
        features in inverse order of their actual use. <strong>Her top priority is the platform's
        least-adopted utility, and it is top precisely because it is least adopted.</strong> The true
        figure is 3.02.
        <br><br>Her second priority, teachers with school affiliation (240 users, 3.04 sessions and
        2.20 active days against 2.00 and 1.52), is sound and exactly computed.""",
        a1_exp="""Three, each with a hypothesis, a week-1 action, a numeric success metric and a
        numeric kill criterion &mdash; structurally complete and correctly formatted. A guided weekly
        lesson workflow (kill: under 5% improvement after two weeks, or fewer than 10% completing the
        workflow); a school-teacher distribution network with 1-2 champions across 10 schools (kill:
        under 5% activation improvement); and a usage-to-school expansion with weekly summaries to
        champions (kill: under 10% of schools adding another active teacher after four weeks). The
        design discipline is real. The targets they optimise are the wrong ones.""",
        a2="""Genuinely detailed, and the strongest part of her submission. A phased table with
        Description, Responsible, Action, Channel, Frequency and Targeted Result columns, and the
        responsibility split is specific in a way most submissions were not &mdash;
        <em>"scoping by Senior Manager Growth, endorsed by Growth Lead, executed by Growth
        Associate(s)"</em>. Her A2 Daily Tracker has 29 columns covering the full chain from coaching
        status through report generation, admin sharing, EOI click, admin meeting, school conversion
        and referral, with live COUNTIF formulas and a K-factor cell.
        <br><br>What it is not is a plan that concentrates on the transition that actually stalls. It
        is a promotional programme &mdash; LinkedIn certifications, a Champion of Change Challenge
        with a weekly leaderboard, free subscription months, a bi-annual award function &mdash; and
        the volumes (8 weekly cohorts of 25 teachers, 200 total) are asserted rather than derived from
        a base of 35 adopters.""",
        a2_k="""<strong>Reverse-engineered to land on the answer.</strong> The chain is 200 teachers
        &rarr; 70% activate (140) &rarr; 50% refer (70) &rarr; 2 links each (140) &rarr; 40% click
        (56) &rarr; 50% convert (28), giving 28/140 = 0.2. Every one of those five rates is invented;
        none is derived from the dataset, and the platform's real base is 35 adopters, not 200
        teachers. To her credit she labels the biggest weakness herself &mdash;
        <em>"*the calculations assume that there is no drop out"</em> &mdash; but a target that is
        produced by choosing five assumptions until the arithmetic returns 0.2 is a presentation of
        the target, not a measurement of it.""",
        a2_breaks="""She identifies three levels rather than two &mdash; teacher, administration,
        district &mdash; and names the administration and district levels as the likely breaks. The
        content is thoughtful: reports built to carry institutionally useful indicators rather than
        just teacher ones, clickable EOI links, school certification for positioning, quarterly
        district review meetings with aggregated dashboards. Every mitigation is an incentive or a
        communication, though; none is a threshold that would tell her the loop had broken, and none
        would stop work.""",
        a3_prob="Around 70% <em>if</em> the district is highly responsive in the first two weeks.",
        a3="""The best-structured Assignment 3 element she produced is the scenario framework: A, full
        200-school expansion; B, phased at 100 or another viable number with phase two formally
        planned for the next cycle; C, blocked, in which case secure a formal commitment, timeline and
        pre-procurement work for next year plus any smaller immediately fundable intervention. Having
        three costed routes ready before the meeting is a real strength. The five-week plan around it
        is reasonable &mdash; email the DEO, request a focal person, work the pilot focal contact
        through to procurement and finance, gather clarity on file, stage and funding.""",
        a3_email="""Mixed. It contains one of the better asks in the round &mdash; requesting that the
        DEO <em>"assign a focal person from your team who could coordinate with us on the next
        steps"</em>, which is a far easier thing to grant than a decision, and she names herself as
        the counterpart focal so the DEO's office carries no coordination burden. Against that, it
        opens with two paragraphs of congratulation on a pilot that finished three months ago, states
        our own value proposition at length (<em>"proven impact, efficient use of public expenditure,
        and minimal implementation risk"</em>), and asks the DEO to <em>"kindly endorse that we are
        aligned"</em> &mdash; which invites him to restate a commitment he has already gone quiet on.
        The deadline appears only as <em>"Given the upcoming budget cycle"</em>, not as a date.""",
        a3_internal="""<strong>The weakest commercial judgment in the round.</strong> 70% is the
        highest probability anyone assigned to this deal, in a scenario built from six weeks of
        silence, an unverified procurement stage and an active competitor. It is conditional on
        responsiveness, which is honest, but the support for it is not:
        <em>"My action plan assumes that the pilot project focal person will be immediately responsive
        and facilitate connecting with other departments. <strong>I am quite certain because we are
        continuously engaged on WhatsApp.</strong>"</em> A WhatsApp relationship with a focal person is
        not evidence that a budget line will move, and the assumption sits directly against the six
        weeks of silence in the brief. She does flag the time crunch honestly, and her one ask is
        concrete and useful &mdash; authority to proceed with a reduced-scope Scenario B without
        further board approval.""",
        reflection="""<strong>Her strongest deliverable.</strong> A government department where senior
        leadership was enthusiastically engaged across multiple projects but nothing converted, causing
        <em>"attention fatigue from both sides."</em> She built a parallel workstream at operational
        level, learned through that counterpart about an internal restructuring that explained the
        stall, and went to her Head of Department to argue that
        <em>"instead of chasing signoffs, I should lead this partnership at the operational level
        first."</em> She then got the priority item onto her counterpart's recurring meeting agenda so
        it stayed visible, and converted it into a formally endorsed action plan once the restructuring
        completed. Specific, self-directed, and the diagnosis is exactly the one Assignment 3 rewards
        &mdash; which makes it all the more notable that her Assignment 3 forecast does not carry the
        same scepticism.""",
        verified="""What is right is right: Pakistan 265 users at 3.16 sessions and 2.26 active days;
        Sri Lanka 261 at 1.71 and 1.36; school-affiliated 240 users at 3.04 and 2.20 against 2.00 and
        1.52 for the rest; and active-day-1 rates of 98% and 100%. All exact.
        <br><br>What is wrong: <em>lesson plans 4.47 active days</em> (true value 2.58) and
        <em>presentations 11.1 active days</em> (true value 3.02), both produced by the population
        mismatch described above; and <em>"almost no users engage with audio coaching"</em>, which is
        true of the <em>audio_coaching_sessions</em> column and false of the platform &mdash; 35 users
        started 118 coaching sessions and completed 88.
        <br><br><strong>No AI-use disclosure appears anywhere in her submission</strong>, and the brief
        asks for one. Her prose does not read as AI-generated &mdash; it carries her own typos and
        phrasing throughout &mdash; so this is recorded as an instruction breach rather than as
        undisclosed AI.""",
        thin="""<strong>The recommendation is the problem, not the effort.</strong> She has produced a
        real 60-day operating table, a 29-column tracker with working formulas, three properly
        structured experiments with numeric kill criteria, a three-scenario negotiation framework and
        the most self-directed reflection in the round. The care is visible. But Assignment 1 asks
        which features to double down on and which are noise, and her answer inverts both: it
        promotes the two convenience utilities and deprioritises the flagship, on the basis of a
        metric that rewards features for being little used.
        <br><br>Nothing else in the dataset is examined. No cohort or spike analysis, so the 14
        November concentration is absent. No attribution finding. No observation that Sri Lanka
        registers <em>better</em> than Pakistan while producing zero adopters of either flagship
        feature &mdash; she reports Sri Lanka's higher week-1 activity as a point in its favour.
        <br><br><strong>For a role whose first task is to tell the Head of Growth which numbers to
        trust, an eight-week plan aimed at the least-adopted feature is not a near miss.</strong>""",
        probes=[
            "In the dataset, audio_coaching_sessions sums to 1 and coaching_started sums to 118 across 35 users. Walk me through how you chose between them.",
            "Open your A1 tables tab and talk me through cell K6. What population is the numerator and what population is the denominator?",
            "Your reflection describes reading a government stall accurately and acting on it early. Your Assignment 3 puts this deal at 70%. Reconcile those two for me.",
        ],
    ),
]


def stat_boxes():
    boxes = [("6", "Scored", "#1a2b4c"), ("21", "Documents read", "#2f6fb5"),
             ("4", "Recommended", "#1b7f4d"), ("1", "Not assessable", "#b3261e")]
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
    Six Senior Manager Growth candidates submitted case studies after the 18 August evaluation and
    had not been scored. This report covers those six. The eight already scored are not re-opened
    here. Every deliverable was read end to end &mdash; 21 files, every narrative page and slide,
    every spreadsheet tab with formulas preserved &mdash; and each candidate is covered assignment
    by assignment: what they found, the numbers they used, the experiments they designed, how they
    would measure the loop, their stalled-deal probability, and what is thin.</p>
  <p style="font-family:Georgia,serif;font-size:13.5px;line-height:1.7;color:#1b4d3e;
            background:#eef7f1;border-left:3px solid #1b7f4d;padding:10px 14px;margin:14px 0 0;">
    <strong>Figures were not checked against our own summary table.</strong> The raw 546-row user
    dataset was recovered and independently revalidated against the benchmark ground truth &mdash;
    546 rows, Pakistan 265 and Sri Lanka 261, registration 43.8% and 45.6%, repeat use 62.9% and
    19.3%, 35 coaching adopters, 118 sessions started and 88 completed, five acquisition spikes
    &mdash; every figure reproduced exactly. Each candidate's headline numbers were then recomputed
    from that file. <strong>Nobody fabricated data.</strong></p>
  <p style="font-family:Georgia,serif;font-size:13.5px;line-height:1.7;color:#7b341e;
            background:#fdf6ec;border-left:3px solid #c47f16;padding:10px 14px;margin:14px 0 0;">
    <strong>Sent in two parts.</strong> Gmail clips anything over about 100KB behind a "view entire
    message" link, which would hide half the report. Part 1 covers Furqan, Hania and Shafaq; Part 2
    covers Lamis, Kanooz and Rimsha, plus the outstanding items and the method note. The ranking
    table appears in both so each part stands on its own.</p>"""

SEPARATES = """
  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">What separates them</h2>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>First, which coaching column they opened.</strong> The dataset carries two.
    <em>audio_coaching_sessions</em> sums to 1 across all 546 users; <em>coaching_started</em> sums
    to 118 across 35 adopters. Five of the six found the real one and built on it. One did not, and
    recommended deprioritising the platform's flagship feature as a result. This single choice is
    the widest scoring gap in the round.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Second, whether the ratio has the same population top and bottom.</strong> Two
    submissions rank features by a per-user retention figure. Lamis divides feature users by feature
    users and gets 1.15 uses per presentation adopter. Rimsha divides all Pakistani users' active
    days by the count of presentation sessions and gets 11.1, which is not a per-user figure at all
    &mdash; and because presentations are the least-used feature, the smallest denominator produces
    the biggest number, so the metric ranks features in inverse order of their use.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Third, Assignment 3 spread the scores again, exactly as it did in the first round.</strong>
    The analysis quality is bunched; the stalled-deal work is not. Hania said she would not raise the
    probability on a positive conversation alone. Shafaq gave two numbers, one for a full close and
    one for a phased outcome. Furqan flagged every escalation to the DEO before making it. Kanooz's
    email never mentions the five-week deadline the whole scenario turns on, and Rimsha put the deal
    at 70% on the strength of a WhatsApp relationship.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Fourth, consent.</strong> Classroom audio reaching a teacher's administrator without
    permission is the loop's real failure mode, and the case never raises it. Only Hania and Shafaq
    did. Furqan's design makes the sharing automatic, which makes the omission more consequential in
    his plan than in the others.</p>"""

OUTSTANDING = """
  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Outstanding &mdash; needs a decision</h2>
  <div style="background:#fff5f5;border-left:3px solid #b3261e;padding:12px 16px;margin:12px 0;">
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:0;">
      <strong>Muhammad Ahmad Taj (app 3971) &mdash; submitted, but nothing arrived.</strong> Markaz
      records a submission on 19 August and his note says the deliverables
      <em>"are shared in the attached ZIP file"</em>. There is no attachment on the notification, no
      Word or Excel file stored against the application, and no link in the submission text. His
      note describes all three assignments and a separate reflective response, so the work appears to
      exist &mdash; Markaz accepts Word and Excel, not archives, so the upload most likely failed
      silently. He cannot be scored until the files are in hand. Recommend asking him to resend to
      hiring@ today.</p>
  </div>
  <div style="background:#fdf6ec;border-left:3px solid #c47f16;padding:12px 16px;margin:12px 0;">
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:0;">
      <strong>Two candidates were sent the case study on 7 August and have never submitted &mdash;
      17 days, and neither was ever nudged.</strong> Muhammad Zeshan Nawaz (app 3921) and Muhammad
      Bilal Sadiq (app 4051). Both still sit in Markaz as <em>shortlisted</em>, so they read as live
      candidates in every pipeline view. Every other SMG invitee has now either submitted or been
      chased. Recommend either a final nudge with a deadline, or closing them out.</p>
  </div>
  <div style="background:#f5f7fa;border-left:3px solid #2f6fb5;padding:12px 16px;margin:12px 0;">
    <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:0;">
      <strong>Markaz record hygiene.</strong> Hania Khan's submission has no Markaz record at all
      &mdash; her portal upload failed and she emailed the files instead, so
      <em>case_study_status</em> is still null on app 4035. Any view built on Markaz alone would show
      the second-highest scorer in this round as a non-submitter. Separately, Hania (4037), Lamis
      (4063) and Kanooz (3811) each carry a duplicate application sitting in <em>rejected</em>, which
      will distort counts until they are merged or cleared.</p>
  </div>"""

METHOD = """
  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 10px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Method &amp; limits</h2>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    Scored against <em>smg_execution_sprint_benchmark.md</em> using the six-dimension rubric, the
    same key and the same weights as the 18 August report, so the two rounds are directly comparable.
    The benchmark was written and QA'd before any submission in either round was opened, and nothing
    from this round has been added to it. Every submission was read in full: PDFs page by page,
    Word documents including all tables, decks slide by slide including speaker notes, and every
    spreadsheet tab opened with formulas preserved so a live model could be told apart from pasted
    values. Findings quoted are the candidates' own words.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>One score carries a caveat that is ours to resolve, not the candidate's.</strong>
    Shafaq Syed states three times that the per-user dataset was not supplied and that cohort,
    source and week-level cuts were therefore unavailable. Furqan Afzal independently reported on
    22 August that the dataset tab appeared to be missing from the same case-study document. If the
    data was genuinely unreachable for some candidates, her Data score of 2 reflects our
    distribution rather than her judgment and should be revisited. Her first debrief probe is
    designed to settle it.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>On the borderline recommendation.</strong> Kanooz Ahmed Siddiqui scores 62, which the
    rubric places in the band to proceed only if the pool is thin. It is not thin &mdash; six
    candidates from the first round scored 70 or above and four more clear it here. Her Assignment 1
    is genuinely original and worth keeping on file; her Assignments 2 and 3 do not currently meet
    the bar for the role. That is a recommendation, not a decision.</p>
  <p style="font-family:Georgia,serif;font-size:14.5px;line-height:1.75;color:#22303f;margin:10px 0;">
    <strong>Every submission is archived.</strong> All 21 files, including the three that arrived
    only as links and the two that arrived only by email, are now in the Senior Manager Growth
    submissions folder, one subfolder per candidate. Each name in the ranking table links to its
    folder.</p>"""


def build_html(part):
    subset = CANDS[:3] if part == 1 else CANDS[3:]
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
     SMG Case Study &mdash; Evaluation Report, Round 2 &middot; Part {part} of 2</div>
   <div style="font-family:Arial,sans-serif;font-size:13px;color:#c3d0e6;margin-top:8px;">
     Job 42 &middot; Senior Manager Growth &middot; 24 August 2026 &middot; {names}</div>
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
    Four of the six are recommended for debrief.</p>

  {SEPARATES if part == 1 else ""}

  <h2 style="font-family:Georgia,serif;font-size:19px;color:#1a2b4c;margin:30px 0 4px;
             border-bottom:2px solid #2f4fa2;padding-bottom:6px;">Candidate detail
             {"&mdash; 1 to 3 of 6" if part == 1 else "&mdash; 4 to 6 of 6"}</h2>
  {deep_dives(subset)}

  {OUTSTANDING if part == 2 else ""}
  {METHOD if part == 2 else ""}

 </td></tr>
 <tr><td style="background:#f5f7fa;padding:16px 30px;border-top:1px solid #dfe3ea;
        border-radius:0 0 8px 8px;font-family:Arial,sans-serif;font-size:12px;color:#6b7a90;">
   Taleemabad Talent Acquisition &middot; hiring@taleemabad.com &middot; 24 August 2026</td></tr>
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
                      context=f"smg_case_study_evaluation_round2_part{part}")
        print(f"Part {part} sent to {RECIPIENTS} - {size:,} bytes")
    s.quit()


if __name__ == "__main__":
    main()
