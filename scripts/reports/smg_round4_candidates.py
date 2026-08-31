"""
Round-4 SMG candidate write-ups: Khushal Kakar (app 4134) and Ali Wajdan Khan (app 3977).

Both were blocked in the 30 August consolidated report and both became readable on 31 August:
Ali Wajdan's Google Doc link was opened for us, and Khushal submitted on 30 August after finally
getting access to the case-study brief.

Same benchmark, same six-dimension rubric, same weights as rounds 1-3. Every headline figure
recomputed from the raw 546-row master dataset.
"""

CANDS = [
    dict(
        name="Khushal Kakar", app="4134", total=98, band="STRONG YES", proceed=True,
        colour="#1b7f4d", scores=[5, 5, 5, 5, 5, 4],
        link="https://drive.google.com/drive/folders/1vAOSPk8D86iBYUsZ_dHEEPJB2peX0iaN",
        docs=[
            ("Assignment 1 Presentation", "PDF, 6 slides", "Country signal, target segment, feature depth, cohort quality, two bets, three experiments."),
            ("Assignment 1 Analysis", "XLSX, 12 sheets, 9,004 formulas", "Raw_Master (547 rows, 8,190 derived cells), all four raw source files, and a dedicated <strong>QA &amp; Reconciliation</strong> tab. Country, Segment, Feature, Cohort and Daily analyses all re-derive from the raw data inside the file."),
            ("Assignment 2 60-Day Plan", "PDF, 2 pages", "Loop playbook with exit conditions, eight-period sprint with scaling gates, stakeholder rhythm, weekly scorecard, two breakpoints."),
            ("Assignment 2 Tracker", "XLSX, 6 sheets, 1,813 formulas", "Pipeline_Tracker (1,600 formulas), Weekly_Metrics, Dashboard, Friday_Update, plus Setup and Lists tabs."),
            ("Assignment 3 Stalled Deal", "PDF, 3 pages", "Five-week plan across three parallel tracks, the DEO email, internal update."),
            ("Final Reflection", "PDF", "Separate file."),
        ],
        docs_note="Submitted 30 August via Markaz (app 4134) as a Drive folder link, six deliverables. <strong>He could not open the case-study brief for two days</strong> &mdash; three Google Docs access requests between 28 and 30 August &mdash; and still returned this inside the stated time-box, reporting 2 hours 45 minutes. He also explains the folder link in his submission note: the portal does not accept multiple files, so he agreed the folder with the team first.",
        a1="""<strong>The most rigorous piece of analysis in the entire pool, across all four
        rounds.</strong> Two things set it apart before any conclusion is reached.
        <br><br>First, he <strong>defines his own metric and labels its limits</strong>:
        <em>"Retention metric used throughout = last activity &ge;7 days after signup among eligible
        users; it is a persistence proxy, not strict D7 retention"</em>, with the reason on the
        Definitions tab &mdash; <em>"The master data has first/last activity dates, not a daily
        user-level activity log."</em>
        <br><br>Second, he built a <strong>QA &amp; Reconciliation tab</strong> that checks fourteen
        master-file computations against the aggregate reference file and flags each MATCH or CHECK.
        It independently surfaces the <strong>240-versus-239 registration discrepancy</strong>, a
        three-session gap between the master and daily chat totals, and a mislabelled aggregate field
        (<em>"Aggregate label 'total_chat_sessions' actually equals total sessions"</em>). Nobody else
        in any round checked the data against itself before analysing it.
        <br><br>The findings are exact. Pakistan 3.1623 sessions against Sri Lanka's 1.7126; repeat
        after day zero 46.4% against 20.7%; coaching adoption 12.83% against <strong>0%</strong>. His
        target segment is Pakistani Secondary-only plus multi-grade teachers, and the line that makes
        it actionable: <strong>"94% of Pakistan Coaching users are in Secondary-only or Multi-grade
        segments (32 of 34)."</strong> Exact.""",
        a1_noise="""Three, each with the reason and the number. <strong>Broad Sri Lanka
        acquisition</strong> &mdash; <em>"Same scale as Pakistan, but much shallower repeated use and
        no Coaching starts in this sample."</em> <strong>Reading as the primary bet</strong> &mdash;
        <em>"Excellent depth signal, but only 13 users."</em> And, unusually,
        <strong>"All event acquisition as one channel"</strong> &mdash;
        <em>"Event quality varies sharply; replicate the high-quality onboarding pattern rather than
        treating events as one scalable channel."</em> He is the only candidate to name the events
        themselves as the thing being misread.""",
        a1_pri="""(1) <strong>Pakistan coaching-first institutional cohorts</strong>, targeting the
        68 Secondary-only and multi-grade teachers &mdash; <em>"Design introductions around completing
        the first Coaching workflow, not around registration alone."</em>
        (2) <strong>Lesson Plan &rarr; Coaching activation funnel</strong>: 104 Pakistani lesson-plan
        users at 4.82 sessions and 70.2% repeat, of whom <strong>38 registered users have never tried
        coaching</strong> &mdash; a warm pool, sized exactly, all four figures verified.""",
        a1_exp="""Three, each with a numeric success metric, a numeric kill criterion and the fit it
        tests. (1) <strong>Coaching-first cohort</strong>: run 4-5 Pakistan institution sessions and
        start the first recording before teachers leave. Success &ge;40% start within 72h AND &ge;35%
        7-day persistence; kill if &lt;20% start OR &lt;20% persistence after two cohorts.
        (2) <strong>Lesson Plan bridge</strong>: two message variants, one-tap path. Success &ge;15%
        start coaching in 7 days, <em>and he also tracks manual time and cost per converted user</em>.
        (3) <strong>Coaching proof &rarr; referral</strong>: success is activated-referral K &ge;0.20;
        kill at K &lt;0.08. His closing decision rule:
        <em>"scale retained activation, not registrations or event attendance."</em>""",
        a2="""<strong>Written as an operating document rather than a plan.</strong> Six loop stages,
        each with an action, a named owner, a channel and an <strong>exit condition</strong>
        (<em>"First Coaching started within 72h"</em>, <em>"Completed Coaching + proof asset"</em>).
        Then an <strong>eight-period sprint</strong> in which every period carries not only what
        happens and the required output but a <strong>gate before scaling</strong> &mdash;
        <em>"&ge;40% start Coaching in 72h target"</em>, <em>"Kill test if &lt;5% LP&rarr;Coaching
        after 2 variants"</em>, <em>"No opportunity without owner/date"</em>.
        <br><br>Consent is handled inside the loop rather than bolted on: stage 2 is
        <em>"capture one concrete lesson change + teacher quote/report screenshot; <strong>get
        permission to share</strong>."</em> His stakeholder table gives each layer a rule, not just a
        cadence &mdash; <em>"Never ask for referral before visible value"</em> for teachers, and for
        district officials <em>"Do not approach with product pitch alone; bring school evidence +
        defined next step"</em>, engaged <em>"only after multi-school evidence exists."</em>
        <br><br>He also puts a forecast rule in Assignment 2, which is where it actually bites:
        <em>"probability changes only when evidence changes (meeting booked, session held, referral
        generated, district next step confirmed) &mdash; not because someone 'sounds positive'."</em>""",
        a2_k="""<strong>Activated-referral K = new activated referral users &divide; teachers exposed
        to the referral ask</strong>, target contribution 0.20, owned by the SMG and tracked weekly
        alongside seven other metrics that each carry an explicit formula, a decision use and an
        owner. Two of those deserve naming: <em>7-day persistence proxy</em> as the scale-or-kill
        signal, and <strong>pipeline hygiene &mdash; "% active opportunities with owner + next action
        + due date", target 100%</strong>. The tracker computes it: 1,600 formulas across a
        202-row pipeline sheet feeding a Dashboard and a Friday_Update tab.""",
        a2_breaks="""(A) <em>Teacher signs up but does not reach coaching value</em> &mdash; early
        warning is low start or completion within 72h and <em>"admin has nothing concrete to
        notice"</em>. The contingency opens with the right instruction:
        <strong>"Do not add more acquisition."</strong> Run assisted first-use in-session, capture the
        failure reason, and if &lt;20% start or &lt;20% persist after two cohorts, stop or reshape the
        channel. (B) <em>Value stays with the teacher and never reaches the administrator</em> &mdash;
        warning is no warm introduction within five working days; contingency is a two-line intro
        script plus a proof card, then direct SMG follow-up with the teacher copied, then a different
        champion in the same school.""",
        a3_prob="50% today, moving to ~70% or below 25% on named week-1 and week-2 evidence.",
        a3="""<strong>He does not treat the DEO as the deal.</strong> The operating principle is
        three parallel tracks &mdash; relationship (DEO), approval (Directorate), budget
        (Secretary/budget team) &mdash; <em>"Keep the DEO informed, but do not let the file depend on
        one person's response."</em> Day 1-2 is a bottleneck map producing
        <em>"One-page process map: current location, required approvals, missing inputs, named owners
        and deadlines."</em> Week 2 closes every controllable gap within 48 hours so that
        <em>"the remaining delay is a government decision, not a Taleemabad input."</em> Week 3
        escalates <em>only the specific blockage</em>, and Head of Growth is used
        <em>"for a specific unblock or senior introduction, not a broad 'please help' escalation."</em>
        <br><br>He opens by labelling what the case does not tell him:
        <em>"Case assumption to verify on Day 1: the Directorate is the administrative approving
        authority... The case itself does not specify the exact approval chain, so I would confirm it
        with procurement before escalating."</em> And the relationship rule is the sharpest sentence
        in the round: <em>"I would never tell the DEO 'we are escalating because you are
        unresponsive.' I would frame Directorate/budget coordination as protecting the expansion he
        already supported."</em>""",
        a3_email="""Names the five-week deadline as shared context rather than pressure, explains
        that the team is already checking requirements with the Directorate so nothing waits on the
        DEO, and then makes the ask twice over so it is easy to grant:
        <em>"Could I request 15&ndash;20 minutes with you this week, or alternatively a focal person
        from your office whom we can coordinate with on the district side?"</em> It offers a one-page
        summary of results, scope and costing in advance. It never asks why he has not replied, and
        it commits to keeping his office informed at every step.""",
        a3_internal="""<strong>The best forecast discipline of the fifteen.</strong> 50% today, with
        the reasoning stated in one line &mdash; <em>"a verbal expansion is not an approval"</em>
        &mdash; and movement defined in both directions with named evidence:
        <strong>~70% if the Directorate confirms the approval path and the budget side confirms a
        viable inclusion route within Week 1; below 25% if by the end of Week 2 there is still no
        named approval owner or workable budget mechanism.</strong> His help-needed list is
        conditional rather than open (<em>"Approval to use you for one senior government intervention
        <strong>only if I can name the blocker and the person who owns it</strong>"</em>), and he
        tells the Head of Growth what to carry it as:
        <em>"Keep at 'at risk / 50%,' not 'likely.' ... No probability increase without a concrete
        government milestone."</em>""",
        reflection="""Specific, quantified and genuinely about a plan of his own that he changed.
        On an RCT in Khairpur covering 600 schools, 2,400 parents and 2,400 students, the plan was to
        recruit 40 enumerators on CVs, train for one day and start. <em>"During the first training, I
        realized this plan would not work"</em> &mdash; many enumerators were local to a rural
        underserved area with limited survey experience, against a nearly 200-question instrument. He
        extended training from one day to five, added a two-day pilot, and
        <em>"built a daily monitoring dashboard so I could review incoming data, identify mistakes
        each evening, and provide corrective feedback before the next day's fieldwork."</em> Outcome:
        roughly 95% validated data. The lesson lands: <em>"The objective stayed the same; the method
        had to change."</em>""",
        verified="""Recomputed from the raw dataset and exact: Pakistan and Sri Lanka at 3.1623 and
        1.7126 sessions, 2.2604 and 1.3640 active days, 46.4% and 20.7% repeat, 12.83% and 0%
        coaching adoption; coaching n=35 at 8.69 sessions, 97.1% repeat and 74.6% completion; multi-
        grade n=43 at 6.00 sessions and 88.4% repeat; 32 of 34 Pakistani coaching users inside his
        target segment; 104 Pakistani lesson-plan users at 4.82 sessions and 70.2% repeat with 38
        registered non-adopters; and the full cohort table for 14 November (40 users, 82.5%
        registration, 4.88 sessions, 87.5% repeat, 57.5% coaching) and 26 November (100, 47.0%, 2.00,
        29.0%, 0%). <strong>His 11 December call is exactly right</strong> &mdash; that cohort has
        <strong>zero</strong> users with seven observable days, so his refusal to label it a failure
        is correct, not cautious. Two sub-one-point differences in the Secondary-only bucket
        (24 users against his 68-user combined total of 67) reflect one row bucketed differently.
        Nothing is fabricated.""",
        thin="""<strong>He does not notice that Sri Lanka registers better than Pakistan.</strong>
        His country slide compares depth and adoption, where Sri Lanka loses on everything, but the
        registration rates &mdash; 43.8% Pakistan against 45.6% Sri Lanka &mdash; never appear. It is
        the one benchmark excellence marker he misses, and it is the sharpest available argument that
        registration is the wrong success metric.
        <br><br><strong>His AI disclosure is present but thin.</strong> Each deliverable carries a
        line, which is more than most, but the lines are <em>"I used ChatGPT to structure the data for
        analysis, and develop the first draft of the presentation to save time"</em>, <em>"to
        structure the execution plan"</em>, and <em>"to structure the response"</em>. Given the depth
        of the workbook, the boundary between what ChatGPT produced and what he decided is worth
        establishing directly rather than assuming. This is the only reason his Signal score is a 4
        and the only thing standing between him and a clean sweep.
        <br><br><strong>The 14 November concentration is present but not quantified platform-wide.</strong>
        He reports 57.5% coaching adoption within that cohort, which is the same fact from the inside;
        he does not state that those 23 users are 23 of the platform's 35 total adopters.""",
        probes=[
            "You built a QA tab and found the 240-versus-239 registration mismatch and a three-session chat gap. What did you expect to find when you built it, and what would you have done if a number had not reconciled?",
            "Sri Lanka registers at 45.6% and Pakistan at 43.8%, and Sri Lanka has zero coaching adopters. What does that tell you about what registration is worth as a metric, and what would you stop reporting?",
            "Your workbook has 9,004 formulas and your AI note says ChatGPT structured the data and drafted the deck. Take me through the Cohort_Analysis tab and show me which decisions in it were yours.",
        ],
    ),
    dict(
        name="Ali Wajdan Khan", app="3977", total=49, band="NO", proceed=False,
        colour="#b3261e", scores=[3, 2, 2, 3, 2, 3],
        link="https://drive.google.com/drive/folders/1fKGJ3LtOXPy5N4EVXShdnDbdiQp3LyBA",
        docs=[
            ("Case Study &mdash; Ali Wajdan", "DOCX, single document", "All three assignments and the reflection in one file, with two data tables embedded."),
        ],
        docs_note="Submitted 29 August via Markaz (app 3977) as a single Google Doc link. <strong>The link was shared with nobody on arrival</strong> &mdash; Ayesha's own account returned 404 and an anonymous request returned 401 &mdash; and was opened for us on 31 August. <strong>No supporting workbook and no tracker were submitted</strong>, so Assignment 1's working and Assignment 2's tracker, both named in the brief, are absent.",
        a1="""<strong>His arithmetic is sound and his reading of it is not.</strong> The two tables he
        embeds are exact to the row: lesson plans 170 users and 275 uses at 2.58 average active days;
        presentations 91 and 105 at 3.02; general chat 433 and 949 at 2.00; video 12 and 13; and
        <em>audio coaching, 1 user, 1 use</em>. The registration-state table is exact too &mdash;
        flow_sent 180 with 431 sessions and 3,655 messages, template_send_failed 26 with 39 and 298.
        <br><br>The problem is what he concludes from them.
        <strong>"Based on the above summary, the features with the strongest engagement appear to be
        General Chat &amp; Lesson Plans."</strong> That is what the table says, because the table
        measures coaching through <em>audio_coaching_sessions</em>, which is 1. Two paragraphs later
        he picks <strong>coaching</strong> as his top priority on completely different figures &mdash;
        <em>"~75% completion rate, ~57% Repeat usage"</em>, both correct, drawn from
        <em>coaching_started</em> and <em>coaching_completed</em>. He never reconciles the two, so his
        own noise-and-signal section contradicts his own priority section, and a reader cannot tell
        which he believes.""",
        a1_noise="""One line: <em>"the clearest noise activity is Presentation generation considering
        its overall low users, sessions and repeat usage."</em> Defensible and correct. But
        <strong>Sri Lanka is never examined</strong>. He lists it among the countries with the
        strongest sign-up completion &mdash; a positive &mdash; and nowhere records that 261 Sri
        Lankan users have produced <strong>zero</strong> coaching and zero reading adopters. That is
        the single largest fact in the dataset and it is absent.""",
        a1_pri="""(1) <strong>Coaching</strong>, correctly identified as the retention engine, with a
        good instinct behind it: <em>"the Coaching feature instigates a feedback loop that could
        actually improve teaching performance over time... teachers will keep coming back."</em>
        (2) <strong>Onboarding</strong> &mdash; the unregistered, flow_sent and template-failed pool,
        which he sizes correctly at 206 and calls <em>"a low-hanging fruit that should be addressed at
        priority"</em>. Both picks are reasonable; the second is the same lever Vaneeza chose. What is
        missing is any cohort or acquisition analysis at all &mdash; no spike work, no 14 November, and
        no observation that the source field is "direct" for every user.""",
        a1_exp="""Three, well conceived as product ideas. Simplify WhatsApp onboarding to quick-reply
        buttons; let a raw voice note over 20 seconds route straight into coaching without multi-step
        commands (a genuinely good one); and a shareable coaching badge to drive peer referral. But
        the <strong>success metrics and kill criteria are mostly not measurable</strong>: success is
        <em>"Increase in Registration completion rate"</em> with no threshold, and the kill criteria
        are <em>"Registration rate falls below the existing threshold"</em> and
        <em>"Voice note failure rate is high or errors in detection"</em>. Only the third carries a
        number (&lt;5% of badges shared). A kill criterion without a number does not stop work.""",
        a2="""<strong>The weakest Assignment 2 of the fifteen, and the brief's tracker is absent.</strong>
        It is four prose steps with no dates, no phasing, no owners and no exit metrics. The content
        inside them is not unreasonable &mdash; monitor pipeline health daily and intervene below
        threshold, have the field team approach administrators <em>"with multiple active teachers"</em>
        (a sensible targeting rule), ensure on-ground execution quality at school sessions &mdash; but
        none of it is assigned to anyone or dated, and there is nothing a growth associate could be
        handed. His stakeholder section is the strongest part: teachers via bite-sized WhatsApp with
        <em>"onboarding under 2 minutes"</em>, administrators via monthly impact dashboards, district
        officials via quarterly briefings and policy roundtables.""",
        a2_k="""Defined only in words: an invitation rate (school-specific invites or WhatsApp shares
        per active teacher per week) multiplied by a conversion rate (invited teachers who register
        and run a session within 7 days). The structure is right and the definition is honest about
        counting activation rather than registration. But there is no arithmetic toward 0.20, no
        statement of what the current base would imply, and no instrument to collect either input.""",
        a2_breaks="""Two, both plausible: administrators blocking school-wide rollouts, answered by
        empowering teachers to run 15-minute peer check-ins instead of a top-down assembly, which is a
        good de-escalation; and low peer-to-peer invitations, answered by the shareable badge. Neither
        carries an early warning or a threshold, so nothing in the plan would tell him a breakpoint had
        been reached.""",
        a3_prob="45%, with an honest acknowledgement that the silence may be stonewalling.",
        a3="""Directionally sound and better than his Assignment 2. Week 1 works the DEO, pilot
        principals and lower-level procurement officers in parallel. Week 2 targets the Deputy DEO
        with a <em>"Phase 2 Scaling Roadmap for 200 Schools," framed around their upcoming provincial
        academic targets</em>, with a specific and well-chosen ask &mdash; to place the expansion on
        the agenda for the provincial budget review meeting. Week 3 escalates to provincial advisors.
        <br><br>Two things read as pressure rather than facilitation. The week-3 heading is
        <strong>"External Multi-Stakeholder Pressure"</strong>, and weeks 4-5 are
        <em>"daily on-ground presence at the DEO &amp; Procurement offices"</em>. Against a government
        sponsor who has already gone quiet for six weeks, daily physical presence is as likely to
        harden the silence as to break it.""",
        a3_email="""<strong>It contains an unfilled placeholder and an unsupported claim, and neither
        should reach a district officer.</strong> The body reads
        <em>"Teachers completed over <strong>xxx</strong> lesson planning and coaching sessions during
        the pilot period"</em> &mdash; the number was never filled in. And the next line claims
        <em>"visible improvements in student literacy metrics"</em>, which nothing in the supplied data
        supports; there are reading assessments, but no measured improvement.
        <br><br>The rest is well judged: it credits the DEO's leadership, frames our own readiness
        around <em>his</em> stated vision for 200 schools, acknowledges the pressure his office is
        under during the budget cycle, and closes with an easy two-option ask &mdash; ten minutes on a
        call or a drop-in. Had the two figures been handled honestly this would be a solid email.""",
        a3_internal="""Short but genuinely candid, and the candour is the best thing in it:
        <em>"He could possibly be preoccupied with the provincial budgetary cycle but it is just as
        likely that we are being stonewalled."</em> Very few candidates were willing to put that in
        writing. 45% is a defensible number. What is missing is everything around it &mdash; no gating
        events in either direction, no statement of what would move it, and a support request that is a
        single line (<em>"Escalation to Provincial stakeholders in case District management continues
        to stall"</em>) with no trigger, no named person and no deadline.""",
        reflection="""<strong>Comfortably his strongest deliverable, and a genuinely good story.</strong>
        At a B2B retail startup his team pushed lines-per-bill through monthly cash incentives to lift
        average order value. LPB rose; order value barely moved. <em>"On a routine market visit with
        the sales team, I realised that the sales reps were adding extremely low-value products
        (Matches/sachets) to increase the LPB and unlock the cash incentive."</em> His fix is
        structural rather than motivational: cap LPB credit for SKUs below a value threshold, coach
        reps toward higher-value SKUs, and <strong>club both metrics together so the incentive only
        unlocks on both</strong>. That is a precise diagnosis of a gamed metric, spotted in the field
        rather than in a dashboard, and fixed at the mechanism.""",
        verified="""Both embedded tables are exact to the row, including the figures Rimsha got wrong:
        lesson-plan users at 2.58 average active days and presentation users at 3.02 are the true
        values. Coaching completion at ~75% is right (74.6%), and his ~57% repeat is right on the
        stricter definition (20 of 35 adopters completed two or more). The registration-state table
        reconciles exactly. <strong>One figure is overstated:</strong> he gives coaching users an
        average lifespan of <em>"~16 days"</em>; the true value is 12.5, or 13.0 among completers.
        <br><br><strong>No AI-use disclosure appears anywhere</strong>, and the brief asks for one.
        His prose does not read as AI-generated, so this is recorded as an instruction breach rather
        than as undisclosed AI. <strong>Two required deliverables are missing outright</strong> &mdash;
        Assignment 1's supporting workbook and Assignment 2's tracker.""",
        thin="""<strong>The score is about completeness and consistency, not about arithmetic.</strong>
        His numbers are accurate; there are simply not enough of them, and the ones he has are not
        reconciled with each other. His feature table and his stated priority disagree about whether
        coaching matters, because the table measures it with the wrong column.
        <br><br><strong>Two of the brief's named deliverables do not exist.</strong> Assignment 1 asks
        for supporting workings and Assignment 2 asks for a tracker; neither was submitted, and
        Assignment 2 in consequence has no dates, no owners and no exit metrics.
        <br><br><strong>Sri Lanka is never analysed</strong>, so the pool's largest finding is absent,
        and there is no cohort work at all, so 14 November never appears.
        <br><br><strong>The DEO email would need to be rewritten before it could be sent</strong>
        &mdash; an unfilled "xxx" and a literacy-improvement claim we cannot evidence.
        <br><br>For a role whose first task is to defend numbers in a room and hand an operating plan
        to a growth associate, an accurate but partial analysis with no plan artefact behind it does
        not clear the bar. <strong>The reflection says there is real field judgment here; this
        submission does not show enough of it.</strong>""",
        probes=[
            "Your feature table says General Chat and Lesson Plans have the strongest engagement, and two paragraphs later you make Coaching the top priority. Which is it, and what does audio_coaching_sessions actually count?",
            "Assignment 2 asked for a tracker and Assignment 1 for supporting workings. Talk me through what you would have put in each, and who owns day 12 of your 60-day plan.",
            "Your DEO email says teachers completed over 'xxx' sessions and reports visible improvements in student literacy. Where would each of those numbers have come from?",
        ],
    ),
]
