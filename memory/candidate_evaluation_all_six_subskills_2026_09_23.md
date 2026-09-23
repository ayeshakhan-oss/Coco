---
name: Candidate Evaluation — all six sub-skills live (2026-09-23)
description: CV screening, case-study tracking and KCD built and deployed, completing the module. Records the CALIBRATION that stopped a 367-candidate run (the screen would have rejected 8 of the 16 people we actually hired, so never set a threshold from one class), that an extraction failure is not a weak candidate, the four production defects a green suite let through, the data traps (jobs.jd_text empty on 31 of 32 jobs; Markaz records no case-study SEND), and that production can only reach Haiku 4.5.
type: project
---

# Candidate Evaluation: all six sub-skills live (2026-09-22/23)

Live at `https://coco-production-bcc8.up.railway.app`, commit `1da533a+dirty`,
alembic `0014_kcd_evaluations`. 518 tests. Zero `built:false` left in the bundle.

| Sub-skill | Route | Built |
|---|---|---|
| Technical Screening | `/evaluations` | Phase 1, read-only from Nugget |
| CV Screening | `/cv-screening` | **new** |
| Case Study Evaluation (tracking) | `/case-study-tracking` | **new** |
| Case Study Scoring | `/case-studies` | Phase 3 |
| KCD Evaluation | `/kcd-evaluations` | **new** |
| Values Scorecards | `/values-scorecards` | Phase 2 |

New tables: `coco.cv_screens` (0012), `coco.case_study_probes` (0013),
`coco.kcd_evaluations` (0014). Every migration was applied over the Neon HTTPS
`/sql` endpoint with **each CHECK constraint probed by a deliberately bad row**
before `alembic_version` was stamped. Markaz unchanged at 219 scorecards throughout.

---

## 🔴 Two data traps that would each have shipped a wrong answer

**1. `jobs.jd_text` is the obvious JD column and it is empty.** Measured across all
32 live jobs: `jd_text` is populated on **ONE** and averages **211 characters**;
`jobs.description` is populated on **31**. Screening a CV against `jd_text` would
have screened it against nothing and produced a confident, evidenced, meaningless
result.

`description` is Google-Docs HTML with inline styling on nearly every tag, and job
43 is **3,300,555 characters** of it. `webapp/services/job_description.py` strips it
to readable text and **removes base64 `data:` URIs BEFORE stripping tags** — the
payload lives inside an attribute, so tag-stripping first leaves megabytes of it
behind as text. Verified on all 32: 31 readable at 2,072-17,693 chars, job 43 down
to 6,006, and the one refusal is job 30 "Hackathon 2026" whose description is 14
characters.

**2. Markaz records no case-study SEND anywhere.** I expected the opposite of what I
found, in both directions:

- The **submitted** side is trustworthy. `case_study_status` is populated on 116 of
  4,509 applications and agrees with the four evidence columns on **every one**,
  zero disagreements. (Rule 18 warns this field is unreliable; for *submission* it
  is not. Rule 18's real point is about the **sent** event.)
- The **sent** side does not exist. There is no `case_study_sent_at` column, and
  `public.candidate_communications` holds **16 typed rows in the entire table**:
  per job it reports 0 sends against 4 to 17 submissions. Case studies go out by
  email from Ayesha's mailbox and the record is in Gmail, nowhere else.

A tracker built on those fields reports **"0 sent, 17 submitted"** and a reader
concludes the pool was never contacted. So the status vocabulary has four values and
**deliberately no `not_sent`**: no submission and no findable send is
`no_record_of_a_send`, a statement about our records rather than about the candidate.
The database CHECK constraint was probed with a literal `'not_sent'` and rejected it.
The summary returns `unproven_absence` as a number and the page prints it as a
sentence, not a footnote.

Finding a send costs a mailbox round trip per candidate, so it is probed on demand
and stored. **The IMAP search is on RECIPIENT, with the subject matched in Python
against whitespace-normalised text** — a subject gets reworded between batches and
Markaz's carry double spaces ("Growth  Manager"), which a raw substring test misses.
An address cannot be reworded.

---

## 🔴 Where a locked SOP had to be overruled, and how that was handled

Both are the anchor-floor defect of CLAUDE.md Rule 27, and in both the SOP predates
it (May 2026 vs 2026-09-02).

**`kcd-evaluation.md`** says *"1 = Absent or fundamentally wrong"*, reserves 0 for
"not submitted", and its Common Mistakes table instructs *"use 1 for weak; 0 only
for missing"*. That is a 20% floor under every dimension. The code runs **0 to 5 in
half steps with a real zero**.

The SOP's actual worry — that weak work would *"look identical to unsubmitted"* — is
answered **structurally** instead: an incomplete submission is pulled out of the
ranking entirely and rendered with the SOP's own asterisk and floor caveat, so a zero
on a submitted case study and a candidate who submitted nothing are never in the same
list. `rank_results` returns **two lists, not one sorted list**, because a single list
breaks the rule the first time a strong partial outscores a weak complete.

✅ **SETTLED 2026-09-23.** Ayesha chose "update the document", so
`kcd-evaluation.md` now bottoms out at a real 0 in all seven places it stated the
scale, with the reasoning and the structural answer recorded in the file. The
code and the SOP agree again. I did NOT edit it until she said so: rewriting a
locked SOP is her call, and the code carrying the correct behaviour while the
document is wrong is the safer of the two states to sit in meanwhile.

**`kcd-evaluation.md` also refers to a "default 6 criteria" that is enumerated
nowhere in the repository.** I used the framework's own three named components
(Knowledge / Capacity / Design), equally weighted because the SOP gives no weights,
and said so in the module docstring rather than presenting it as locked. A per-job
framework can already override both. If Ayesha's six exist, they replace `DIMENSIONS`
and nothing else changes.

**`cv-screening.md`** ranks its three criteria (skills and experience top, fit
supporting) but never weights them, and names three tiers without numeric
boundaries. 40/40/20 was flagged as a derivation and Ayesha confirmed it ("fine
as is"). The tier boundaries started as an invented 70/50 and are now **50/35,
calibrated against real hiring outcomes** — see the calibration section below,
which is the part of this file worth reading twice.

---

## What each new module refuses to do

Every one refuses rather than degrades, which is Rule 29 made mechanical:

- **CV screening** refuses with no CV text, no readable JD, or no model credential.
  Total and relevant experience are validated as **two separate figures** with
  relevant asserted to be a subset of total, because conflating them is the SOP's own
  named mistake.
- **Tracking** records an unreadable submission as `corpus_error`, never as a
  zero-length corpus, and a mailbox that will not open leaves `send_found` false
  without that hardening into "not sent".
- **Completeness refuses to guess.** With no required parts configured it reports
  `known: false`, because deriving the required sections from the submission's own
  headings would mark every submission complete by construction.
- **KCD** refuses a CONDITIONAL verdict with no condition (API *and* a database CHECK
  constraint), refuses a score with no evidence, and computes the verdict, total and
  GWC decision itself rather than accepting them from the client.

**Every flag carries its evidence.** A flag a human cannot check is an accusation,
not a signal. The cohort mirror check returns the shared text and **names no cause**:
two candidates quoting the same paragraph of the assignment are indistinguishable
from two sharing an assistant.

🔒 **Ayesha, 2026-09-15: "cv screening and technical screening are both separate so
you shouldn't mix their sops/rubrics/rules."** Made mechanical —
`test_cv_screening_borrows_nothing_from_nugget` scans the service for Nugget's rubric
vocabulary and for an import of its reader, and was **proven to fail** against a
planted violation.

---

## Two defects I introduced and caught before they shipped

- The tracking upsert relied on `probed_at`'s **server default, which only fires on
  INSERT**, so a re-probe would have kept the original timestamp and the row would
  have claimed to be fresher than it was. That is the one thing a reader trusts the
  column for. `test_a_reprobe_advances_probed_at` was proven to fail against the
  original.
- `CVScreen.is_current` was left to its column default, which is `None` on the object
  until flush. Set explicitly.

🔑 **A column default is not an object default.** Both bugs are the same mistake.

---

## Still open, needing Ayesha

1. **KCD's "default 6 criteria"** -- do they exist? I used the framework's own
   three named components and said so.
2. `memory/REPORT_FORMAT_LOCKED.md` is referenced by the CV-screening SOP and
   by MEMORY.md and **does not exist in the repo**.
3. **35 candidate letters drafted since 2026-09-14** are still unreviewed. She
   asked to regenerate them "once the model is fixed"; the model cannot be
   fixed (Haiku is all we have), so regenerating would produce different output
   from the same model at real cost. Raised, not acted on.
4. **The whole-position run has not happened yet.** The button exists and the
   bands are calibrated; nobody has pressed it.

SETTLED since this file was written: the KCD scale (0-5 real zero, SOP updated
2026-09-23), the CV-screening bands (calibrated, below), and the CV-screening
weights (Ayesha: "fine as is").

---

## 🔴 THE CALIBRATION, AND WHY A THRESHOLD IS NEVER A GUESS (2026-09-23)

Ayesha asked for a whole position to be screened. Before running 367 candidates
I scored the **16 people Taleemabad actually hired or made an offer to** for CPD
Coach. **The screen would have rejected 8 of them.** That stopped the run.

Then the half I had not done: a random **20 of the 141 rejected**, on identical
code, because a line drawn from successes alone can pass everybody and you
would not find out until a whole position had been screened.

| | hired / offered | rejected |
|---|---|---|
| mean | **54.0%** | **35.0%** |
| median | 52% | 34% |
| range | 32-80 | 12-76 |
| at or above 70% (my original line) | **3 of 14** | 1 of 16 |
| at or above 50% | **9 of 14** | 2 of 16 |

**A 19-point gap: the screen genuinely separates the two groups.** What was
wrong was the boundary I invented. At 70% it would have screened out **11 of
the 14 people we hired**. 50 is the line that best separates them; 35 sits at
the rejected cohort's own mean, so almost nobody we hired lands in `no_hire`.

Both cohorts' real scores are now **regression tests** in
`webapp/tests/test_cv_screening.py`, including one asserting the 19-point gap
has not collapsed, because a line low enough to pass everyone would satisfy
"keeps the hires" and be worthless.

🔑 **The rule: never set a scoring threshold from one class.** Score the people
who succeeded AND the people who were rejected, on the same code, and look at
the gap before touching a boundary.

⚠️ **Even at the best possible line this misses 5 of 14 people we hired.** It is
a PRIORITISATION tool. `no_hire` means "read last", never "rejected", and that
is written into the code rather than left as an understanding.

## 🔴 AN EXTRACTION FAILURE IS NOT A WEAK CANDIDATE

Three of the eight misses were CVs that barely parsed: **117, 238 and 296
words**. Hina Fatima Jafri was HIRED; her CV extracts to 788 characters and came
back 36% `no_hire`, and re-running the identical input gave her 6.5 relevant
years one time and 0.2 the next. **A model asked to judge an empty page still
answers.**

`cv_text.MIN_USABLE_CHARS = 400` asks "is there text at all" and was never the
bar for screening somebody out. `cv_screening.MIN_SCREENABLE_WORDS = 250` now
REFUSES below it and says plainly it is an extraction failure needing a human.

**Counted in WORDS, not characters** — the pypdf letter-spacing defect produces
20,089 characters carrying 15 words and sails past any character floor. Roughly
**1 CV in 6 cannot be read at all** (2 of 16 hired, 4 of 20 rejected).

## Screening a whole position

`POST /api/cv-screening/screen-batch` does a few candidates per request; the
page loops on `remaining` with a progress bar and a Stop. One request cannot do
a position: each CV is a ~15 second model call, so 74 candidates is ~20 minutes
and 367 is over an hour.

🔑 **The batch is driven by a CURSOR (`after`), not by "next unscreened".** A
candidate whose CV cannot be read never gets a screen row, so a next-unscreened
query hands back the same person for ever. Skipped candidates are RETURNED and
counted, never silently dropped. Each candidate commits as it finishes, so
stopping loses nothing and resuming continues from there.

## 🔴 Four production defects Ayesha found or that her screenshot exposed

All four shipped past a green suite. All four are the same root mistake: **I
wrote the tests from what I assumed the data looked like instead of from the
data.**

1. **`applications.created_at` does not exist** (the column is `applied_at`).
   Both new pages returned a 500 on every request. **19 router tests passed
   anyway, because a fake session never sends SQL to Postgres.**
   `webapp/tests/test_router_sql_executes.py` now wraps every module-level SQL
   constant on all six evaluation routers in `SELECT * FROM (...) LIMIT 0` and
   executes it against the real schema, and is proven to fail on the exact
   broken statement.
2. **Every job picker showed ONE job.** `reads.list_jobs` defaulted to
   `active_only=True` and exactly 1 of 32 jobs is `Active` (CPD Coach). Every
   position anyone screens, scores or tracks is `Closed`. Now all positions,
   live ones first, with the status shown.
3. **Salary / City / Relocate were blank for every candidate.** I handled a list
   of dicts and a flat `{question: answer}` dict; the ONLY shape Markaz uses is
   `{"1763029445610": {"question": ..., "answer": ...}}`. 0/410 before, 367/410
   after.
4. **A travel question was being read as the candidate's city.** CPD Coach asks
   "Willingness to travel in your assigned region (regions may include certain
   city areas...)"; a loose `city` match claimed it for 332 of 410 and printed
   "Yes I am willing to travel" as their city. That job has no city question at
   all -- its location field is **Address**. Each profile field now carries
   EXCLUDE terms and each question is claimed by at most one field.

## ⚠️ Production runs on Haiku 4.5, and cannot run on anything else

CLAUDE.md Rule 30 said "Now Sonnet 5". Probed against Railway's own credential
with 1-token calls: **`claude-sonnet-5` and `claude-opus-5` both return 429
`rate_limit_error`; only `claude-haiku-4-5-20251001` answers.** Ayesha confirmed
the plan does not give us Sonnet or Opus. Rule 30 is corrected in place.

The code default was `claude-opus-4-8`, a **retired id**, so an unset
`ANTHROPIC_MODEL` burned two failed calls before landing on the model that
works. It is now Haiku 4.5, with `claude-sonnet-5` first in the fallback chain.

🔴 **The consequence that matters: the semantic tone reviewer -- the thing that
enforces the candidate-letter tone rules by meaning rather than by word list --
runs on the smallest model we have. Read every letter yourself.**

## Two smaller things worth keeping

- **The model inferred gender from a name.** The first live screen wrote "she
  has secondary teaching experience" with nothing in the CV saying so. The
  prompt now forbids it and requires "they" or the candidate's name.
- **A `_Skip` exception, not a return code**, is what lets one unscreenable
  candidate be recorded and skipped without aborting a batch of 74, while the
  single-candidate endpoint turns the same thing into a clear 422.
