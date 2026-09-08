---
name: Case Study Outcome email type, below the benchmark (2026-09-08)
description: Skill 01 type #8. Rejection for candidates who submitted a case study and scored below the 70% benchmark that gates final interviews. First cohort Job 42 SMG, 5 candidates.
metadata:
  type: project
---

# Skill 01 type #8, Case Study Outcome (Below the Benchmark)

Ayesha 2026-09-08: a new candidate-communication type for people who reached the case-study
stage, **submitted**, and missed the **70% benchmark**. 800 words, evidence from **their own
submission plus the benchmark answer key**, reusable across positions, first built for
**Senior Manager Growth**. "harness this rule or hardblock it."

**Type doc:** [.claude/skills/01_candidate-communication/case-study-outcome-email.md](../.claude/skills/01_candidate-communication/case-study-outcome-email.md)
**Script:** `scripts/send_case_study_outcome_pilot.py` (`--check` gate only, `--only <key>`, `--live`)
**Eyebrow:** `EYEBROW["case_study_outcome"]` = Application Update

## The cohort, verified from the sent reports rather than the repo

17 SMG candidates were scored across 4 rounds, reported to Ayesha in **two batches**.
Five below 70:

| Candidate | App | Score | Greeting used |
|---|---|---|---|
| Kanooz Ahmed Siddiqui | 4111 | 62 | Kanooz |
| Irfan Siddiqui | 4144 | 53 | Irfan |
| Ali Wajdan Khan | 3977 | 49 | Ali |
| Syed Basit Hussain | 4142 | 46 | Basit |
| Rimsha Taj | 3956 | 45 | Rimsha |

🔴 **Why a repo-only scan under-counts.** The batch-1 report Ayesha has open is the **18 Aug
"deep read, all 6 shortlisted"**, which contains only the six who cleared. Irfan and Basit are
in the earlier, thinner **17 Aug "all 8 scored"** report (Sent Mail mid 2654). Batch 2 is the
**31 Aug consolidated report** of 9 (mids 2766-2768), which holds the other three. Reading the
deep read plus the consolidated gives **three** below-70 names, not five. **Always reconcile a
cohort against every sent report, not the latest one.**

Excluded and needing something different: **Arooj Khalid 70** (at the bar, above it) and
**Muhammad Ahmad Taj 3971** (sent the case study, files never arrived, never scored, so not a
below-70 case at all).

⚠️ All five still read `shortlisted` in Markaz. Statuses are stages and were never updated.

## Decisions Ayesha made

1. **State the 70% rule, never the individual score.** The letter says we set a 70% benchmark
   and only candidates who meet it move to final interviews. No `NN/100`, no band, no ranking.
   The rule carries the transparency; the number invites an argument about the marking.
2. **800 words**, evidence from the submission and the benchmark only.
3. Reusable for **all positions** as needed.
4. ⚠️ The SMG **rubric** published bands of 80+ / 65-79 / 50-64 / <50; 70% is Ayesha's hiring
   bar. All five sit below 65 too, so nothing turns on it. Write the number the cohort was told.

## What the harness actually enforces, and where

🔴 **The gate lives INSIDE the send script**, raising `SystemExit` before any SMTP connection.
Deliberate: the Layer 3 `PreToolUse` hook is **inert** (matches `tool_name` against `"send"`
while registered on the `"Bash"` matcher, so it never fires). A block written there does nothing.

17 checks, **every one proven to fire against a deliberately broken draft** before the pilot
went out: sources exist on disk · 800 words · Rule 10 opening line position · 70% rule present ·
no out-of-100 · no band label · 3+ verbatim anchors from that candidate's submission · no other
roster candidate named · no em dash · no first-person singular · 19 intent-words · conversation
references when no interview is verified · interviewer names · jargon · pool comparisons ·
PILOT prefix in live · missing PILOT prefix in pilot.

**A gate that has only ever passed proves nothing.** Test the failures, not just the baseline.

Also registered in the CLI eval: `run_eval.py --type case_study_outcome`. That required
threading `email_type` into `check_jargon()`, which previously blocked the phrase **"case
study"** for every type. `CASE_STUDY_PHRASE_ALLOWED = {case_study_update, case_study_outcome}`
exempts the phrase only, scoped to the two types where the case study is the candidate's own
deliverable. GWC, KCD, warm bench and values scorecard stay blocked everywhere.

## Traps this build hit

- **`.env` has `EMAIL_USER`, not `EMAIL_ADDRESS`.** The script would have raised `KeyError` at
  send time, after the gate had passed. Check env var names against `.env`, not from memory.
- **The evaluation records are full of `&mdash;` and pool rankings** ("the most rigorous in the
  pool", "the weakest Assignment 2 of the fifteen"). Both are forbidden in a candidate letter.
  Content lifted from an internal report needs the em dashes stripped and every placing removed.
- **The CLI eval's `KNOWN_INTERVIEWERS` list contains "Ali" and "Khan"**, which are parts of a
  candidate's own name here. It passed, but that list is a false-positive risk on any candidate
  whose name overlaps it.
- **Cross-contamination is the real risk when writing five letters in one sitting.** The gate
  scans for every other roster name; ambiguous parts ("Ali", "Khan", "Siddiqui") are excluded
  from the scan on purpose, so that guard is not total.

## Name resolution, Rule 22 applied

Per-candidate check of each person's **own** From display name changed two greetings:
**Kanooz signs "Kanooz Siddiqui"** (Markaz stores "Kanooz Ahmed Siddiqui"), and **Basit signs
"Syed Basit"** while our own earlier invite said "Basit Hussain". Syed is a patronymic, same
call as [[project_rm_internal_case_study_round_2026_09_02]] made for Ateeb Ali.

## No conversation references

All five had a **Zero In Call booked**, but a booking is not a held interview, so every letter
grounds in the written submission and mentions no conversation. `INTERVIEW_REFERENCE_ALLOWED`
defaults to `False` and the gate blocks "we spoke", "our conversation", "our call" and similar.
This sidesteps the booking-is-not-an-interview trap entirely.

## Send log

Pilot 2026-09-08, five letters to ayesha.khan@ alone, no CC, verified by per-recipient IMAP
scan **before** drafting (0 prior outcome emails to any of the five) and **after** (exactly one
each, PILOT prefix on all five, 0 sent to a candidate address). Word counts 955 to 1078.

### ✅ LIVE 2026-09-08, all five sent
Ayesha: "go live. in cc keep waqas, ali.sipra, hiring and ayesha.khan."

**LIVE CC (now `LIVE_CC` in the script, and the `--cc` default):** waqas.tanveer@ ·
ali.sipra@ · hiring@ · ayesha.khan@ (identical to the type #6 default list).

🔑 **`safe_sendmail()` BLOCKS external domains** unless `allow_candidate_addresses([...])` is
called first. Candidates are gmail/outlook/live.com, so a live run fails without it. The script
now allowlists **exactly the one candidate being written to**, immediately before that send,
rather than allowlisting the whole batch up front.

Verified after: **1 copy each, CC exact on all 5, no PILOT prefix leaked, 0 duplicates**
(09:01:22 to 09:01:32 PKT-7). Pre-send scan had confirmed 0 prior outcome emails to any of them.

The close went out as written under the assumption Ayesha did not overrule: this process
concluding, no future promise, and no invitation to reapply to Job 42 while it is still open.
Each letter closes on disposition scoped to the kind of work the candidate showed strength in.

Related: [[project_smg_case_study_evaluation_2026_08_17]] ·
[[project_smg_case_study_round2_2026_08_24]] ·
[[case_study_update_email_type_2026_08_13]] ·
[[CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED]] ·
[[lesson_scoring_anchor_floor_inflation_2026_09_02]]

---

## 🔒 TONE STANDARD, added by Ayesha the same day (2026-09-08)

After reading the first pilot she rewrote the tone brief for this type. **The feedback is
shared to be useful, never to justify or defend the rejection decision.** The candidate has
invested significant time; she should finish reading feeling her effort was seen and her work
carefully reviewed. Substance is preserved in full. Warmth comes from respect and constructive
language, **not** from withholding the actual feedback: do not over-soften to the point where
the candidate cannot understand why they missed the benchmark.

**Structure she specified:** clear decision → appreciation for the effort → genuine recognition
of strengths → gently explain the key gaps → what would strengthen the approach → dignity and
encouragement grounded in their actual work.

**BANNED, now HARD BLOCKS in `_gate()` (`HARSH_LANGUAGE` + `CORPORATE_BOILERPLATE`):**
"failure" · "wrong" · **"the honest part"** (the old section heading, renamed to *Where the
Submission Could Have Been Stronger*) · "you failed" · "the problem with your" · "went wrong" ·
"deliberately" · "reverse-engineer" · "selecting assumptions" · "you cannot" · "incapable" ·
"we regret to inform" · "after careful consideration" · "impressive candidate pool".

**PREFER:** "the main gap we identified" · "where the analysis could have been stronger" · "one
area that affected the conclusions" · "an opportunity to strengthen the analysis" · "what we
would encourage you to look at differently".

**The framing sentence she wrote, use it:** *"There were two areas in the analysis that
ultimately affected the overall score, and we want to walk you through them because we think
the context will be more useful than simply sharing the result."* Never "here is where you
went wrong".

**When explaining a technical error:** describe **what happened in the analysis and its effect
on the conclusion**, never the candidate's ability or judgment. Give credit where the reasoning
on top of the error held together.

🔴 **The loop-coefficient trap.** Never imply the candidate chose assumptions to reach a desired
answer. The first draft said *"a target produced by selecting assumptions until the arithmetic
lands on the desired figure"*, which reads as an accusation of bad faith. Correct framing:
each rate is a reasonable planning assumption, **what is missing is a link back to the dataset**,
so the target could not be validated confidently. `deliberately` / `selecting assumptions` /
`until the arithmetic` are now blocked patterns.

🔴 **Never imply the candidate cannot do analysis.** Say it positively ("it is not a statement
about your analytical ability"), not as a double negative ("nothing suggests you cannot"). The
`you cannot` pattern blocks the negative construction, so the positive form is the only way
through, which is the point.

**Removed at her instruction:** any close scoping the candidate to a role where "analysis is
handed to you rather than built by you". Too limiting. Recognise the demonstrated strengths
instead: operational planning, process design, execution, structured thinking, willingness to
surface assumptions. Also avoid pigeonholing phrasing like "sits close to the centre of the
job"; "where that kind of work matters" is enough.

**Final check she requires before every send:** read the letter once from the candidate's
perspective, immediately after a rejection. **If any sentence could reasonably make them feel
accused, embarrassed, belittled, defensive, or as though we are arguing our case against them,
rewrite it.** That pass caught two lines the harness could not: "learnable in an afternoon"
(implies they missed something easy) and the pigeonholing close.

**Length note:** Rimsha's revised letter runs ~1330 words against the 800-1100 target. Full
preservation of the feedback plus the warmer developmental framing costs roughly 280 words.
Flagged to Ayesha rather than cut, since she asked for both.

**Applied so far:** Rimsha's letter fully revised and re-piloted 2026-09-08. The other four
received the **mechanical tone fixes only** (heading rename, two uses of "wrong" rephrased) so
they pass the gate; they have not had the full developmental rewrite.

---

## 🔴 LESSON: "faithful to the evaluation record" is NOT "verified against the submission" (2026-09-08)

Ayesha asked directly: *"have you checked from the case study that all the data in this email
is true, you're not fabricating anything?"* The honest answer at that moment was **no, not
against the submissions**. Every quote and figure had come from the evaluation scripts in the
repo, which are the record of a prior reading. That record is one step removed from the primary
source, and the letters had been piloted twice before anyone checked back.

**She was right to ask. The audit found five defects in five letters.**

### How to actually verify (this worked, reuse it)
1. Submissions are **not** email attachments for SMG (Rule 18 assumes they are). They arrive as
   **Markaz Drive links**; a mailbox scan for attachments returns only logos and `invite.ics`.
2. The per-candidate Drive folder IDs are recorded in the evaluation scripts. Open them with
   **`token_sheets_broad.json`** (Ayesha's own OAuth, full `drive` scope), not the MCP connector.
3. `scripts/evals/fetch_submission_corpora.py` downloads every file and extracts text:
   docx (`body.iter(qn('w:t'))` **plus** tables), pptx (shapes, tables **and** notes), xlsx
   (**both** `data_only=True` for values and `False` for formulas), pdf (PyMuPDF).
   Output: `output/smg_submission_corpora/CORPUS_<Name>.txt` (gitignored).
4. Then audit the **letter**, not the evaluation record: extract every quoted phrase and every
   number from the letter itself and check each against that candidate's corpus.

### What was actually wrong
| # | Candidate | Defect | Fix |
|---|---|---|---|
| 1 | **Rimsha** | 🔴 **FACTUAL.** "the field reads true for **540** of 546". `active_week1` is true for **541**; **540** is `active_day1`. Both fields exist and are adjacent, which is how it crept in. | 541 |
| 2 | Rimsha | Quote read "scoping by Senior **Manager** Growth"; her document says "Senior **Manger** Growth" with bullet separators. The typo had been silently corrected inside quotation marks. | Unquoted and paraphrased. **Never echo a candidate's typo back at them, and never "tidy" text inside quote marks.** |
| 3 | Kanooz | Quote verbatim except her **em dash** became our comma (em dashes are banned in our emails, so the quote could not be reproduced as-is). | Split into two separately verbatim fragments. |
| 4 | Kanooz | `"no better than doing nothing"` was **our own gloss** sitting in quotation marks. | Unquoted. |
| 5 | Irfan | Quote reordered: his text reads "**Of the students formally assessed, 59%** are now reading at or above grade level". | His wording. |

**Nothing was fabricated.** Every figure checked out, and two of the load-bearing criticisms
verified exactly against the raw data: `reading_started` = **87**, `reading_completed` = **51**
(58.6%, so Irfan's 59% really is a completion rate and not a proficiency measure), and his
internal update really does repeat the pilot figures **without** the placeholder disclaimer his
DEO email carried. Ali Wajdan's own correctly-computed table independently reproduces the true
**2.58** and **3.02** per-user active-days that Rimsha's broken ratio inflated to 4.47 and 11.1.

### The durable fix
`_quotes_are_verbatim()` in the send script: **every phrase in quotation marks must appear
verbatim in that candidate's own submission corpus**, or the send HARD BLOCKS. Proven to fire on
both a reworded quote and an invented one. Each candidate declares `corpus="<Name>"`.

**Standing rule: before any candidate letter quotes or cites a submission, fetch the submission
and check the letter against it. An internal evaluation record is evidence of a reading, not a
substitute for the source.** A number that appears in a letter to a candidate is a number they
can check.

### Tone tweaks, round 2 (Ayesha 2026-09-08)

Four phrase-level changes, all about not sounding prosecutorial:

1. **"your submission came in below that mark"** -> **"Your submission did not meet the 70%
   benchmark on this occasion, and so we won't be moving forward with your application for this
   role."** "On this occasion" subtly reinforces that this is not a permanent judgment. Applied
   to the shared `OPENING` and to Rimsha's own opening. Reordered the preceding sentence to
   "Candidates who meet the bar move to the final interviews" so "70% benchmark" is not said twice.
2. **"The analysis rests on the first."** -> **"The analysis appears to have been built using the
   first field."** Less absolute: it allows for reasoning we cannot see from the file.
3. **"Two near identically named columns in the same file is a genuinely easy thing to be caught
   by"** -> **"With two nearly identically named columns sitting in the same file, this is an
   understandable thing to get caught by."** Grammar (near -> nearly) and warmth. The credit
   clause about the reasoning holding together is kept as its own following sentence.
4. Same register applied to Irfan: **"is where the submission ran into trouble"** -> **"The main
   gap we identified sits in the email to the district education officer"**, since "ran into
   trouble" is the same family as the banned "went wrong".

**Principle to carry forward:** state the observation, not a verdict on how it came about.
"The analysis appears to have been built using X" beats "the analysis rests on X"; "an
understandable thing to get caught by" beats "an easy thing to be caught by". Prefer hedged
description of the document over confident description of the candidate.

**Left standing deliberately, flagged for Ayesha:** a few factual absolutes that soften into
vagueness if hedged, and where clarity was also a stated requirement. Kanooz "it never mentions
the budget deadline"; Wajdan "Sri Lanka is never examined" and "never reconciles them". These
describe what is and is not in the document and are each verified true.
