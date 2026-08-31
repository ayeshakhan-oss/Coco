---
name: SMG Case Study Evaluation — Round 2 (2026-08-24)
description: Job 42 SMG round-2 case-study evaluation (6 new submitters scored, 1 not assessable), the sent-vs-submitted reconciliation that found 2 never-nudged non-submitters, and the dataset-column trap that split the pool.
type: project
---

# Job 42 SMG — Case Study Round 2 (2026-08-24)

Six candidates submitted after the 18 August report and had never been scored. Same benchmark,
same rubric, same weights, so the two rounds are directly comparable.

| # | Candidate | App | Score | Band | Proceed |
|---|---|---|---|---|---|
| 1 | Furqan Afzal | 4145 | 93 | Strong yes | Yes |
| 2 | Hania Khan | 4035 | 90 | Strong yes | Yes |
| 3 | Shafaq Syed | 4137 | 75 | Yes | Yes |
| 4 | Lamis Maniar | 4062 | 73 | Yes | Yes |
| 5 | Kanooz Ahmed Siddiqui | 4111 | 62 | Borderline | No — pool is not thin |
| — | Muhammad Ahmad Taj | 3971 | — | Not assessable | Files never arrived |
| 6 | Rimsha Taj | 3956 | 45 | No | No |

Report: `scripts/reports/send_smg_case_study_evaluation_round2_pilot.py` (2 parts, piloted to
Ayesha 24 Aug). Submissions archived one subfolder per candidate under the SMG Drive folder
`1mkrVspKtD1QLFK277dmPPirCP_lHglJA`.

## 🔴 The dataset trap that split the pool

The master dataset carries **two different coaching columns**:
`audio_coaching_sessions` sums to **1** across all 546 users; `coaching_started` sums to **118**
across 35 adopters (88 completed). A candidate who reads the first concludes the flagship feature
is dead. Rimsha did, and recommended deprioritising coaching in favour of lesson plans and
presentations — the two convenience utilities.

**Second trap, same submission:** a ratio whose numerator and denominator describe different
populations. Her "presentation users average 11.1 active days" is
`AVERAGE(PK_total_active_days/PK_presentation_sessions, SL_.../SL_...)`. Because presentations are
the *least*-used feature, the smallest denominator produces the biggest number — **the metric ranks
features in inverse order of their actual use**. True value 3.02. Always check that a per-user
figure actually has users on both sides of the divide.

## Verification method — do this again

Rule 2 says check candidate figures against the benchmark's ground-truth table. Better: the raw
`01_master_user_dataset` (546 rows) was **recovered from a candidate's own workbook**
(Kanooz's `Assignment 1 - Analysis.xlsx`, tab `01_master_user_dataset`), revalidated against every
benchmark figure — all reproduced exactly — and then used to recompute every candidate's headline
number from source. The raw CSVs are **not in the repo** and the case-study Google Doc only carries
a *Dataset Description* tab, so a candidate workbook is currently the only local route to the data.
Worth storing the CSVs properly.

Parsing notes: `completed_registration` is `'t'`/`'f'`, not boolean. `registration_state` says
`completed` for **240** rows while the flag is true for **239** — Hania was the only candidate in
either round to find and reconcile that.

## 🔴 Reconciliation finding — two candidates never chased

Diffing every "Lets proceed with the Case Study for Senior Manager Growth" dispatch against every
submission notification: **18 real SMG invitees, 16 submitted, 2 never did** —
**Muhammad Zeshan Nawaz (3921)** and **Muhammad Bilal Sadiq (4051)**, both sent 7 August, both
never nudged, both still sitting in Markaz as `shortlisted` so they read as live in every pipeline
view. Everyone else was either chased or submitted. **Always run the sent-vs-submitted diff before
declaring a round complete** — "who is left" is not visible from the submission side alone.

## Submissions arrive four different ways

Markaz **file upload** (Rimsha, Shafaq) → notification carries the attachments.
Markaz **link submission** (Kanooz, Furqan, Lamis) → notification has **no attachments**; the links
live in `applications.case_study_submission` and must be pulled from Neon, then fetched from Drive.
**Email only** (Hania, after a portal failure) → **no Markaz record at all**, `case_study_status`
still null on the second-highest scorer in the round.
**Neither** (Ahmad Taj) → note says "attached ZIP file", but Markaz accepts Word/Excel only, so the
upload failed silently and nothing exists anywhere.

Extends [[markaz_submissions_arrive_by_email_2026_08_17]]: the mailbox is the first place to look,
but for link submissions the **database** is the only place the link exists.

## Scoring notes worth keeping

- **Assignment 3 spread the scores again**, exactly as in round 1. Analysis quality bunches; the
  stalled-deal work does not. Kanooz's DEO email never mentions the five-week deadline the entire
  scenario turns on. Rimsha put the deal at 70% because "we are continuously engaged on WhatsApp".
- **A missing deliverable is expensive and should be.** Hania has no reflective response; it moved
  her from roughly 96 to 90 and off the top of the ranking.
- **Score the candidate, flag our own failures separately.** Shafaq stated three times that the
  per-user dataset was not supplied, and Furqan independently reported the dataset tab looked
  missing from the same doc on 22 Aug. Her Data score is 2 **with the caveat stated in the report**
  that if this is our distribution failure it should be revisited. Do not silently penalise a
  candidate for a problem that may be ours.
- **Duplicate applications** distort counts: Hania 4037, Lamis 4063, Kanooz 3811 all sit in
  `rejected` alongside their live records.

## Round 3 (2026-08-30) — one more scored, three blocked

| Candidate | App | Score | Band | Note |
|---|---|---|---|---|
| **Vaneeza Tashfeen Baig** | 4033 | **82** | Strong yes | Submitted 25 Aug; 3rd of 15 overall |
| Ali Wajdan Khan | 3977 | — | Blocked | Submitted 29 Aug; Doc link shared with **nobody** |
| Muhammad Ahmad Taj | 3971 | — | Blocked | Still missing 11 days on |
| Khushal Khan | 4134 | — | Blocked | 3 access requests for the **brief itself** |

Report: `scripts/reports/send_smg_case_study_evaluation_round3_pilot.py` (single part, piloted
2026-08-30).

**Vaneeza's standout move — matched maturity.** She noticed **157 of Sri Lanka's 261 users signed
up in the final 8 days** and refused to compare a six-week-old market with a two-week-old one, so
she re-ran the whole PK/SL comparison restricted to 14+ days of tenure. Every figure exact
(41%/3.6/6.2/16.5% vs 47%/2.0/3.8/0%). The benchmark only flags right-censoring as a caveat; she
made it the argument. She also sized the **206 stalled registrations** (180 `flow_sent` + 26
`template_send_failed` = 38% of base) as a growth lever with its own experiment — nobody else did.

🔴 **Her one real error is a grouping artefact worth reusing as a test.** She bundled 14 Nov,
26 Nov and 11 Dec as "three high-conversion days" (226 users, 64% reg, 10.2% coaching — all
arithmetically correct) and concluded the days produced better-quality users. Day-level:
**14 Nov = 23 coaching adopters, 26 Nov = 0, 11 Dec = 0.** Grouping averaged a two-thirds
concentration into a blended rate and hid the most actionable fact in the dataset. *When a
candidate groups cohorts, always re-split them.*

🔴 **The submission step is the failure point, not the candidates.** Three of the last five SMG
submissions were unreadable on arrival, each for a different reason: a **ZIP** Markaz will not
accept (Ahmad Taj), a **Drive link shared with nobody** (Ali Wajdan — Ayesha's own account gets
404, anonymous 401), and a **portal upload that failed** and came by email with no Markaz record
(Hania). A fourth candidate could not open the brief at all (Khushal). Recommend candidates upload
Word/Excel directly or email hiring@ as standard.

## Round 4 (2026-08-31) — both blockers cleared, and the top score arrived last

| Candidate | App | Score | Band |
|---|---|---|---|
| **Khushal Kakar** | 4134 | **98** | Strong yes — top of the batch, ties Shahmir |
| Ali Wajdan Khan | 3977 | **49** | No |

Consolidated 9-candidate report: `scripts/reports/send_smg_case_study_evaluation_combined_pilot.py`
(3 parts, imports write-ups from the round-2/3/4 scripts so nothing is retyped) +
`scripts/reports/smg_round4_candidates.py`. Final order: Khushal 98 · Furqan 93 · Hania 90 ·
Vaneeza 82 · Shafaq 75 · Lamis 73 · Kanooz 62 · Ali Wajdan 49 · Rimsha 45.

🔴 **The best submission came from the candidate our own process obstructed most.** Khushal spent
two days unable to open the brief (three Google Docs access requests) and still returned six
deliverables inside the time-box, including a **9,004-formula workbook with a QA & Reconciliation
tab** — the only candidate in any round who checked the dataset against itself before analysing
it. It independently surfaced the 240-vs-239 registration mismatch, a 3-session chat gap, and a
mislabelled aggregate field. **Never let an access failure stand in for a quality signal.**

🔴 **Two new reusable analytical tests**, both from this round:
- *Did they define their metric and label its limits?* Khushal: "7-day persistence proxy… not
  strict D7 retention", with the reason (master data has first/last dates, no daily activity log).
- *Did they check eligibility before calling a cohort a failure?* The 11 Dec cohort has **zero**
  users with 7 observable days. Khushal refused to label it; that is correct, not cautious.

**Ali Wajdan (49) is a completeness failure, not an arithmetic one.** His two embedded tables are
exact to the row (including the 2.58 / 3.02 active-day figures Rimsha got wrong). But: **no
workbook and no tracker** (both named in the brief), no cohort work, Sri Lanka never analysed, and
his feature table (measured via `audio_coaching_sessions` = 1) contradicts his own priority section
(measured via `coaching_started` = 118) with no reconciliation. His DEO email ships an unfilled
**"xxx"** placeholder and claims "visible improvements in student literacy metrics" that the data
cannot support. No AI disclosure. His reflection (sales reps gaming lines-per-bill with
matches/sachets, fixed by capping low-value SKUs and clubbing both metrics) is genuinely strong —
the judgment is there, the submission does not show it.

🔴 **Five of nine SMG submissions hit an access or format failure on arrival.** ZIP Markaz won't
accept · Drive link shared with nobody · portal upload failed → email only, no Markaz record ·
portal won't take multiple files · candidate locked out of the brief. **Recommend: let candidates
upload Word/Excel directly, or copy hiring@ as standard.**

## Debrief invites — BATCH 2 LIVE (2026-08-31)

Six above-70 candidates from the new batch invited: **Khushal Kakar 98 · Furqan Afzal 93 ·
Hania Khan 90 · Vaneeza Tashfeen Baig 82 · Shafaq Syed 75 · Lamis Maniar 73.** Not invited:
Kanooz 62, Ali Wajdan 49, Rimsha 45. Booking link
`https://calendar.app.google/VXJ1qxddrMVakeFAA` (Ayesha 2026-08-31 — a DIFFERENT link from
batch 1's `we2Xc2uoYA1x3c1s9`; never reuse a booking link across batches).
Script `scripts/send_case_study_debrief_smg_batch2_pilot.py`, body copy cloned verbatim from
the 18 Aug batch-1 send. Cc waqas.tanveer@ + ayesha.khan@ + hiring@ + ali.sipra@, confirmed by
Ayesha. Verified after send: exactly 1 invite per recipient in Sent Mail, 0 bounces.

🔴 **Markaz names are unreliable for BOTH halves of a name — check the candidate's own
evidence.** Two conflicts in this batch of six:
- **Khushal**: Markaz says "Khushal Khan" *and so does his uploaded CV filename*
  (`Khushal_Khan_SMGrowth_Taleemabad.pdf`), but he signs himself **Khushal Kakar** in all
  three of his own emails including 30 Aug. Went live as **Kakar** (flagged to Ayesha in the
  pilot; she approved the pilot carrying that name without correcting it).
- **Vaneeza**: her Gmail display name reads "Veniza Baig", but Markaz *and* her CV filename
  both say "Vaneeza...Baig". Two self-entered sources beat a display name → **Vaneeza**.
  Resolved without asking.
**Rule: a display name and a CV filename are both self-authored and can disagree. When they
do, say which one you used and why, and flag it before a live send.** Extends the earlier
Arooj Khalid/"Khali" truncation lesson.

**Reusable pre-send check for any invite batch:** per-recipient IMAP scan of Sent Mail for the
invite's own subject line BEFORE drafting (confirmed none of the six had ever received a
debrief invite) and again AFTER sending (confirmed exactly one each). Catches both duplicate
sends and silent omissions.

Related: [[reference_interview_completion_evidence_2026_08_29]] ·
[[project_smg_case_study_evaluation_2026_08_17]] ·
[[feedback_benchmark_and_report_hygiene_2026_08_17]] ·
[[markaz_submissions_arrive_by_email_2026_08_17]] · [[candor_weak_pool_verdict_2026_07_21]]
