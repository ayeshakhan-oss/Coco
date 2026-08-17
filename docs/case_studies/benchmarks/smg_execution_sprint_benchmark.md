# SMG "Execution Sprint" — Benchmark Answer

**Role:** Senior Manager Growth (Job 42) · **Bar:** strong-hire, honest 3-hour
**Built:** 2026-08-16 · **Every figure verified against the live Alpha Platform dataset**
**Status:** DRAFT — pending Ayesha's QA. Do not score any candidate against this until approved.

---

## How to read this document

This is not the "perfect" answer. It is what an **excellent candidate actually produces inside
the 2.5–3 hour time-box** — rough edges intact, assumptions labelled, one tracker that is plain
rather than pretty. It is the **Strong Yes line**, not the ceiling.

Two companion sections sit at the end:
- **Excellence markers** — what would put a submission *above* this benchmark.
- **The traps** — what the case study is actually testing, and how weak answers fail.

A submission does not have to match this answer's *conclusions* to score well. It has to match
its *standard of reasoning*. A candidate who picks different priorities and defends them with
real numbers scores as high as one who picks these.

---

## Verified ground truth

Everything below was computed directly from `01_master_user_dataset.csv` (546 rows),
`07_country_breakdown.csv` and `08_aggregate_metrics.csv`. Use this table to check any
candidate's figures.

| Fact | Value |
|---|---|
| Total users | 546 |
| Pakistan (92) / Sri Lanka (94) users | 265 / 261 |
| Pakistan / Sri Lanka registration rate | **43.8% / 45.6%** |
| Pakistan / Sri Lanka repeat use (registered, active_days > 1) | **62.9% / 19.3%** |
| Pakistan / Sri Lanka sessions per registered user | 4.33 / 1.59 |
| Pakistan / Sri Lanka coaching adopters | **33 / 0** |
| Pakistan / Sri Lanka reading adopters | 8 / 0 |
| Coaching adopters, platform-wide | 35 (6.4% of users) |
| Reading adopters, platform-wide | 13 (2.4%) |
| Coaching sessions started / completed | 118 / 88 (75%) |
| Coaching adopters with 2+ attempts | 24 of 35 (69%) |
| Registered users teaching school grades / university only | 167 / 72 |
| Coaching adopters, school / university-only | **33 / 2** |
| `source` column | `direct` for **all 546 rows** |

### The five acquisition spikes

| Date | New users | Registration | Repeat use | **Coaching adopters** |
|---|---|---|---|---|
| **14 Nov** | 40 | 82.5% | 87.5% | **23** |
| 26 Nov | 100 | 47.0% | 29.0% | 0 |
| 2 Dec | 35 | 40.0% | 20.0% | 0 |
| 8 Dec | 33 | 9.1% | 39.4% | 0 |
| 11 Dec | 86 | 74.4% | **8.1%** | 0 |

Nov 14 users: 3.77 avg active days, 4.88 avg sessions.
All other Pakistan users: 1.99 and 2.86.

---

# Assignment 1 — Channel & Cohort Execution Analysis

*Format: 3-page memo. Supporting workings in the companion spreadsheet.*

## Part 1: Where would you double down?

### The headline

Alpha Platform has acquired 546 users in six weeks and delivered its core product to 35 of
them. Everything else is reach. The two markets look identical on every metric available at
the top of the funnel and diverge completely below it.

**Sri Lanka registers slightly better than Pakistan — 45.6% against 43.8% — and has produced
zero coaching adopters and zero reading adopters.** Not a small number. Zero. Meanwhile
Pakistan's registered users return at 62.9% against Sri Lanka's 19.3%, and run 4.33 sessions
each against 1.59.

This is the most important thing in the dataset, and it means **registration rate is a
misleading metric here**. Any plan built on improving registration will move a number that
does not predict value. I have used repeat use and coaching adoption as the success measures
throughout for that reason.

### Where the value actually sits

Two cuts explain nearly all of the real usage.

**By geography — Pakistan, decisively.** 33 of the platform's 35 coaching adopters are
Pakistani. Sri Lanka's users arrive, register, send a message or two, and leave.

**By segment — school teachers, not university lecturers.** Registered users who teach
school grades outnumber university-only users 167 to 72 — roughly 2.3×. But they account for
**33 of 35 coaching adopters — roughly 16×.** The product's flagship feature is being adopted
almost exclusively by one segment, and it is not the largest one by registration.

**By feature — coaching, clearly.** 35 adopters against reading's 13, a 75% completion rate
against reading's 59%, and 24 of 35 adopters coming back for a second attempt. Reading has
higher attempts per adopter (6.7 vs 3.4), but on 13 people that is a handful of enthusiasts,
not a trend. *Assumption: I am treating 13 users as too small a base to plan against. Worth
revisiting once the base grows.*

### What is noise

**Sri Lanka in its current form.** 261 users, 119 registrations, no core-feature adoption at
all. This is reach without evidence that the product works there. I would not call it a dead
market — I would call it an unvalidated one, and I would stop spending against it until a
deliberate test says otherwise.

**Four of the five acquisition spikes.** 26 Nov, 2 Dec, 8 Dec and 11 Dec collectively
produced **254 users and zero coaching adopters.** The 11 Dec event is the sharpest warning
in the dataset: 74.4% registration — the second-best of any cohort — and 8.1% repeat use, the
worst. It manufactured registrations and nothing else.

**Lesson-plan and presentation generation.** 275 and 105 sessions respectively — real volume,
but these are convenience utilities. Nothing in the data links them to return visits, and
they are not what the platform claims to be for. I would keep them and stop reporting them as
growth.

### The two highest-leverage areas for the next 8 weeks

**Priority 1 — Reconstruct and replicate whatever happened on 14 November.**

One cohort of 40 users produced **23 of the platform's 35 coaching adopters — 66% of all
coaching adoption on the platform, from a single day.** Its users register at 82.5%, return at
87.5%, and average 3.77 active days against 1.99 for every other Pakistani user.

The other four institutional introductions produced 254 users and zero adopters. So this is
not "events work." Something specific happened on 14 November that did not happen on the other
four occasions, and as far as I can tell **nobody wrote down what it was.**

That makes the first move forensic, not promotional. Before spending anything on replication I
would find out: who ran it, what the room looked like, whether teachers recorded a lesson
*during* the session, whether an administrator was present, how long it ran, and what was said
about privacy. My working hypothesis — and I want to be clear it is a hypothesis, not a finding
— is that teachers completed their first coaching recording inside the session rather than being
asked to do it later. The retention pattern is consistent with that, but the data cannot confirm
it. *This is the single highest-value question in the whole dataset and it is answered by
talking to people, not by more analysis.*

**Priority 2 — Convert the existing 35 coaching adopters into school-level expansion.**

24 of 35 adopters have come back for a second session and 23 have a lifespan over 7 days.
These are the only users on the platform with demonstrated value, and each one sits inside a
school containing dozens of teachers who have not been reached. The loop in Assignment 2
depends on exactly this transition, and it currently has 35 possible starting points. That is
a small number, which is precisely why it should be worked by hand rather than automated.

I am deliberately **not** proposing "more acquisition" as a priority. The platform's problem
is not volume — it acquired 546 users in six weeks. Its problem is that 94% of them never
touched the core product.

## Part 2: Three channel experiments

**A constraint I have to flag first.** The `source` column reads `direct` for all 546 users.
There is **no channel attribution in this dataset at all** — every user looks like they arrived
the same way, including the 40 from an in-person event. That means Product–Channel Fit and
Channel–Model Fit, which this assignment asks me to improve, are currently **unmeasurable**. I
can propose experiments, but without attribution I cannot tell you which channel produced a
result. Fixing that is not overhead before the work; it is the first experiment.

*Assumption throughout: I have one growth person and modest budget for 8 weeks. Everything
below is sized for that.*

### Experiment 1 — Instrument attribution before optimising anything

| | |
|---|---|
| **Hypothesis** | Channel performance differs materially by source, and we currently cannot see it. Once attribution exists, at least one channel will show 2×+ the coaching-adoption rate of another. |
| **Week 1 action** | Issue a distinct WhatsApp entry link per channel (event, admin referral, teacher referral, district group, social) and stamp `source` at first contact. Backfill the five known spike dates by hand so we retain historical comparison. |
| **Decision metric** | ≥90% of new users carry a non-`direct` source by end of week 2. |
| **Kill criterion** | If <60% carry a source by week 3, the tagging method is broken — stop and fix the mechanism rather than collecting more bad data. |

This is unglamorous and it gates the other two. I would rather spend week 1 on it than spend
eight weeks unable to attribute the outcome.

### Experiment 2 — Recreate the 14 November conditions, head-to-head

| | |
|---|---|
| **Hypothesis** | The Nov-14 result came from teachers completing a coaching recording *during* the session, not from the event itself. |
| **Week 1 action** | Book 6 Pakistani schools. In 3, run the session so every teacher records and submits one lesson before leaving the room. In 3, run the standard introduction and follow up by WhatsApp. Same facilitator, same deck, same size. |
| **Decision metric** | In-session arm reaches ≥40% coaching adoption within 7 days, and ≥15pp above control. |
| **Kill criterion** | <5pp separation after 6 schools (~80 teachers). If the arms match, my hypothesis is wrong and the Nov-14 cause lies elsewhere — go back to the forensic interviews before spending more. |

### Experiment 3 — Turn an active teacher into a school conversation

| | |
|---|---|
| **Hypothesis** | An administrator shown evidence that their own teachers improved will book a whole-school session. |
| **Week 1 action** | Take the 23 adopters with 7+ day lifespans, identify their schools, get teacher consent, and put a one-page aggregate summary in front of each administrator with exactly one ask: a date for a whole-school session. |
| **Decision metric** | ≥20% of approached schools book within 14 days. |
| **Kill criterion** | <10% after 20 schools. If administrators will not act on evidence of their own teachers improving, the loop in Assignment 2 has no engine and needs redesigning before it is scaled. |

**AI-use disclosure:** I used AI to cross-check my cohort arithmetic against the raw CSVs and
to tighten the wording of this memo. The segmentation choices, the priorities and the kill
criteria are mine.

---

# Assignment 2 — Growth Loop Execution Plan

*Format: 2 pages + tracker.*

## Operating principle

The loop is not mine to redesign, so this plan does not touch it. What it does is pick the
transition most likely to stall and put the most effort there.

Reading the loop against the data: the platform has 35 teachers at step 1 and, as far as I can
tell, **zero confirmed instances of step 3** — an administrator noticing and asking. Every
downstream step is therefore currently theoretical. The loop is not slow; it has not started.
So the plan concentrates on manufacturing the first ten teacher → administrator transitions by
hand, and only then asks what can be systematised.

## 60-day plan

| Days | Actions | Owner / channel | Exit metric |
|---|---|---|---|
| **1–7**<br>Instrument + seed | Interview whoever ran 14 Nov. Ship source tagging (Exp. 1). Select 5 Pakistani schools from the existing adopter base. Assign school IDs and referral links. | SMG: interviews + direct outreach<br>Product: tagging | Nov-14 mechanics documented in writing; ≥90% of new users source-tagged; 5 schools committed |
| **8–21**<br>Prove teacher value | Run in-session recording at each school. Return AI feedback within 24h. Prompt a second recording within 7 days. Capture one before/after statement per school **with written consent**. | SMG: school visits<br>CS: WhatsApp follow-up | ≥20 teachers registered; ≥40% complete first coaching; ≥50% of completers attempt a second |
| **22–35**<br>Convert the administrator | Share the consent-based one-pager. Book a 20-minute review. Make one ask: a date for a whole-school session. | SMG: admin meeting | ≥50% of admins take the review; ≥20% book a session |
| **36–49**<br>Expand + refer | Run whole-school sessions with in-session recording. Appoint a teacher champion per school. Issue trackable referral links. | SMG + CS: school session | ≥10 new registrations per expanded school; ≥40% coaching adoption; ≥90% referral attribution |
| **50–60**<br>Compound + decide | Follow up transfers and district-group shares. Contact referred schools within 1 working day. Compare cohorts. Write the playbook or write the post-mortem. | SMG: outreach<br>HoG: escalation | K ≥ 0.2; documented scale/stop decision |

## Stakeholder layers

| Layer | What they get | What we need from them |
|---|---|---|
| **Teachers** | Fast, private, useful feedback. Nudges at 0h / 24h / day 7. Recording is never shared with their administrator without consent. | Complete a first and second recording; consent to aggregate use; one referral |
| **Administrators** | A one-page summary of *aggregate* teacher improvement — never individual teacher evaluation | Book the whole-school session; nominate a champion |
| **District officials** | Monthly summary: schools reached, teachers activated, repeat use | Endorse in the district WhatsApp group; convene interested schools |

**The consent line is the one thing I would not compromise on.** The fastest way to kill this
loop is for one teacher to learn that a recording of their lesson reached their boss without
permission. The moment that happens, recordings stop across the whole district.

## Measuring toward K = 0.2

**K = teachers who complete a first coaching session as a result of a referral ÷ teachers who
complete a coaching session and are eligible to refer.** Target ≥ 0.2 by day 60 — for every
5 activated teachers, one new activated teacher arrives through the loop.

Counted honestly, that means: unique teacher IDs only; each teacher counted once; a referral
counts only when the referred teacher **completes a coaching session**, not when they register
(see Assignment 1 — registration is the vanity metric); and no unattributed referral enters
the numerator.

Weekly, I would track five numbers: teachers activated, first-to-second coaching conversion,
evidence packs shared, sessions booked, and K with its two drivers separated (are we getting
few referrals, or referrals that do not activate?).

**Reality check:** with 35 adopters today, K = 0.2 means roughly 7 referred activations. That
is a small enough number that it will be noisy, and I would not over-read week-to-week movement
until the base is bigger. I would report it with the absolute counts alongside, always.

**Friday update to the Head of Growth** — one page: funnel against target, K and its two
drivers, cohort comparison, experiment decisions taken this week, the two biggest blockers,
and what I need from them specifically.

## The two most likely break points

**1. Teachers do not record a second time.** Early warning: first-to-second conversion below
50%, or feedback taking more than 24 hours.
*Contingency:* complete the first recording in-session so it never depends on follow-up; offer
a 3-minute recording format; run a weekly champion office hour. If adoption stays under 25%,
**pause and interview non-completers before adding a single school.** More schools will not fix
a product-experience problem.

**2. Evidence does not move the administrator.** Early warning: review not taken within 5 days,
or taken with no booking.
*Contingency:* secure the review date at cohort launch rather than asking after the fact; make
one calendar ask rather than an open-ended one; route through a district sponsor after two
failed contacts. If fewer than 10% book after 20 schools, the loop's engine does not work and I
would tell the Head of Growth that plainly rather than run it for another 60 days.

**AI-use disclosure:** AI helped structure this table and check the K-factor arithmetic. The
sequencing, thresholds and the consent position are mine.

---

# Assignment 3 — The Stalled Deal

## 1. Action plan — five weeks

**Read on the situation first.** Six weeks of silence after public praise is rarely personal
and rarely a "no". It usually means the file has stopped somewhere the DEO does not control,
or the DEO has been given a reason not to say so. The mistake available here is to chase the
DEO harder. The DEO is the sponsor, not the bottleneck — and the budget closes in five weeks
whether or not anyone replies.

**Week 1 — Find out what is actually true.**
Internally first: confirm what the pilot really delivered, what was committed in writing, and
every contact we hold in that district. Then the procurement focal person — not to push, but
to ask five factual questions: the file number, whose desk it is on now, what documents are
missing, what approvals remain, and the last date for inclusion in this cycle. Then the DEO,
with the email below, asking for twenty minutes. Then the DEO's office assistant to help
schedule — not to lobby.
*Gate by day 5: a named budget owner, the exact file stage, and a meeting date. If I have none
of those, this is not a live deal and I will say so.*

**Week 2 — Multi-thread without going around the sponsor.**
Meet the procurement or finance owner **with the DEO's knowledge** — this matters; being
discovered going around a government sponsor ends the relationship. Ask our senior leadership
for one peer-to-peer check-in, framed as support rather than escalation. Reconfirm the pilot
head teachers' evidence, but do not ask them to lobby the DEO on our behalf.
*Gate: written confirmation the 200-school intent is live. Absent that, probability drops
below 15% and it comes out of commit.*

**Week 3 — Make approval mechanically easy.**
One decision-ready pack: pilot evidence, scope, delivery plan, commercials, risk controls,
dates, every required form. Offer a phased option sized to fit a smaller budget line without
discounting or reducing outcomes. Hold a 30-minute working session to close gaps in the room.
*Gate: documents accepted and a named next approval date. "In process" with no named next step
is not a status.*

**Week 4 — Force a written outcome.**
Track approvals twice weekly. Escalate only the specific blocked step. Ask for one of three
things in writing: proceed this cycle, approve the phased route, or confirm this cycle is not
feasible. All three are useful; ambiguity is not.

**Week 5 — Close or reset cleanly.**
If approved: contracting steps, owners, dates, mobilisation. If not: written reasons, a dated
next-cycle calendar, and a low-cost plan to keep the 40 pilot schools supported and producing
evidence for twelve months. Update the CRM the same day either way.

**On the competitor:** I would not mention them to the DEO. Using a competitor as pressure on a
government stakeholder reads as panic and invites a comparison we have not been asked to make.
Our 40 schools of evidence are the advantage — I would compete by making our approval easier,
not by making the DEO anxious.

## 2. The email to the DEO

> **Subject:** Twenty minutes on the 200-school expansion — before the budget closes
>
> Assalam-o-Alaikum [Name],
>
> I hope you and your team are well, and that the start of term has gone smoothly.
>
> I am writing about the expansion we discussed after the 40-school pilot. I am conscious that
> the provincial budget cycle closes in about five weeks, and I want to make sure that if this
> is to move in this cycle, nothing is waiting on us.
>
> Rather than take up your time with an update, I have two practical questions:
>
> 1. Is there anything outstanding from our side — documents, costings, forms — that we can
>    deliver this week?
> 2. Who in procurement or finance would you suggest we work with directly on the file, so
>    that your office is not carrying the follow-up?
>
> If it is easier to answer in twenty minutes on a call, I am glad to work around your
> schedule this week or next. I have attached a one-page summary of the pilot results — the
> teacher usage and learning figures your team saw in the review — in case it is useful for
> internal circulation.
>
> Thank you again for the support you have shown this work. Whatever the outcome this cycle,
> we will continue supporting the 40 schools already running.
>
> Warm regards,
> [Name] · Senior Manager Growth, Taleemabad
> [phone]

**Why it is built this way.** It names the deadline without making it the DEO's emergency.
It never asks "why haven't you replied", which would force them to defend six weeks of
silence. It offers to take work off their desk rather than add to it. It asks for a *person*,
not a decision — a far easier thing to give. And the last line removes the implied threat that
our support depends on the deal, which is the thing that most often makes a government
stakeholder go quiet in the first place.

## 3. Internal update to the Head of Growth

**Probability this closes in the current cycle: 35%.** Classified at-risk, not commit.

**Why 35%.** In favour: a genuinely successful 40-school pilot, public praise, and a verbal
expansion commitment from the decision-maker. Against: nothing in writing, six weeks of
sponsor silence, no verified procurement stage, five weeks to budget close, and an active
competitor. The verbal commitment is real but it is not evidence of budget — those are
different things, and we have been treating them as the same one.

**What moves it.** Toward 60% if week 1 produces a named budget owner, the file's actual stage,
and a dated approval path. Below 15% if we still have none of those by the end of week 2 — at
which point I would take it out of commit rather than carry it.

**This week.** Re-open with the DEO, get the file status from procurement directly, prepare the
decision-ready pack, and secure a working session.

**What I need from you.**
1. One senior-to-senior call held in reserve, used only if the DEO does not respond after two
   follow-ups — I do not want to spend it early.
2. Pre-approved boundaries for a phased rollout, so I can offer one in the room without going
   away to ask.
3. Finance available on 24-hour turnaround for three weeks.
4. A pilot head teacher briefed and willing to take a reference call.

**One thing I want to flag.** We carried this as a live expansion for six weeks on the strength
of a verbal commitment. Whatever happens here, I would like us to agree what evidence moves a
government deal into commit — because if we are forecasting on verbal commitments, this will not
be the last one that quietly stalls.

**AI-use disclosure:** I drafted the email myself and used AI to pressure-test whether the tone
would read as pushy to a government stakeholder. The probability figure and the flag above are
my own judgement.

---

# Reflective response (198 words)

At my previous organisation we spent four months selling a teacher-training programme through
district education offices. The pipeline looked healthy — meetings booked, interest expressed,
two verbal commitments. I was the one collecting the numbers for the weekly update, and I
started noticing that the meetings were being taken by officials who could endorse but not
approve. Every conversation was pleasant and none of them moved a budget line.

I raised it at about week ten, before the quarter closed, and I did it with the pipeline in
front of me rather than as an opinion: of eleven active conversations, nine had no identified
budget holder. I proposed we stop booking new introductions and spend three weeks mapping who
actually signs in each district.

It was not a popular suggestion — the meeting count was the thing that looked like progress,
and I was effectively asking us to make our own numbers look worse.

We did it anyway. Two of the eleven had a real path; the rest did not. The next quarter we ran
fewer meetings and closed more.

What I took from it is that a pipeline full of people who like you is not a pipeline.

**AI-use disclosure:** Written without AI assistance.

---

# Excellence markers — above this benchmark

A submission that does any of these is stronger than this answer, not merely equal to it:

1. **Catches the missing attribution and treats it as the finding**, not a caveat. The `source`
   column is `direct` for all 546 rows; the assignment asks for channel-fit experiments against
   data that cannot measure channel fit. Naming that is the sharpest available read.
2. **Notices Sri Lanka registers *better* than Pakistan** and uses it to argue registration is
   the wrong success metric — rather than just concluding "Pakistan is better."
3. **Quantifies how concentrated Nov 14 is** — 23 of 35 platform-wide adopters from one day —
   rather than describing it as "a strong cohort."
4. **Treats Nov 14 as a question before a plan.** Interviewing the person who ran it beats any
   replication plan built on assumption.
5. **Raises consent unprompted** in Assignment 2. Classroom audio going to an administrator is
   the loop's real failure mode and the case never mentions it.
6. **Separates the DEO from the bottleneck** in Assignment 3 and multi-threads to procurement
   *with the sponsor's knowledge*.
7. **Gives a probability with named gating events**, and says what would move it in both
   directions.
8. **Declines to use the competitor as leverage**, with a reason.
9. **Kill criteria that would actually stop work** — a threshold that triggers "go back and
   re-diagnose", not "iterate."
10. **Says something uncomfortable to the Head of Growth** — e.g. that forecasting on verbal
    commitments is the underlying problem.

---

# The traps — what this case is really testing

| Trap | Weak answer | Strong answer |
|---|---|---|
| **Registration looks like success** | Optimises registration; may recommend Sri Lanka on funnel metrics | Notices SL registers better with zero adoption; switches to repeat use + coaching adoption |
| **Volume looks like growth** | "546 users in 6 weeks, strong momentum" | 94% never reached the core product |
| **Spikes look like a working channel** | "Events drive acquisition — do more events" | Four spikes, 254 users, zero adopters. Only Nov 14 worked |
| **No channel attribution** | Proposes channel experiments regardless | Instruments attribution first; says the ask is currently unmeasurable |
| **Reading looks efficient** | Leads with 6.7 attempts per adopter | Notes the base is 13 people |
| **Redesigning the loop** | Rewrites the loop despite being told not to | Runs it; concentrates on the stalling transition |
| **K-factor as decoration** | States "target K = 0.2" without a definition | Defines numerator and denominator; counts activation not registration |
| **Chasing the DEO** | More follow-ups to a silent sponsor | Goes to procurement for facts; asks the DEO for a person, not a decision |
| **Optimism as forecasting** | "Confident this closes" | 35% with named gating events in both directions |
| **AI without disclosure** | Fluent, generic, undisclosed | Disclosed per deliverable, with what was human |

---

## Scoring note

Score against the *standard of reasoning*, not agreement with these conclusions. A candidate
who picks Sri Lanka and defends it with a real argument about market entry cost outscores one
who picks Pakistan because this document does.

The single most diagnostic question when reading any submission: **did they distinguish
activity from value, and did they use numbers to do it?**
