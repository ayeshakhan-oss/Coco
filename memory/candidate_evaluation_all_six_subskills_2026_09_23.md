---
name: Candidate Evaluation — all six sub-skills live (2026-09-23)
description: CV screening, case-study tracking and KCD built and deployed, completing the module. Records the two data traps that shaped them (jobs.jd_text is empty on 31 of 32 jobs; Markaz records no case-study SEND at all) and the two places a locked SOP had to be overruled by CLAUDE.md Rule 27.
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

⚠️ **The SOP files themselves are unchanged.** The code and the SOP now disagree on
the scale, deliberately: rewriting a locked SOP is Ayesha's call. This needs her
decision — see the open questions below.

**`kcd-evaluation.md` also refers to a "default 6 criteria" that is enumerated
nowhere in the repository.** I used the framework's own three named components
(Knowledge / Capacity / Design), equally weighted because the SOP gives no weights,
and said so in the module docstring rather than presenting it as locked. A per-job
framework can already override both. If Ayesha's six exist, they replace `DIMENSIONS`
and nothing else changes.

**`cv-screening.md`** ranks its three criteria (skills and experience top, fit
supporting) but never weights them, and names three tiers without numeric
boundaries. 40/40/20 and 70/50 are single named constants, flagged as derivations.

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

1. **The KCD scale.** Code says 0-5 with a real zero; `kcd-evaluation.md` still says
   1-5. One of them should change.
2. **The "default 6 criteria"** for KCD — do they exist?
3. **CV screening's weights (40/40/20) and tier boundaries (70/50)** — derivations,
   not quotes.
4. `memory/REPORT_FORMAT_LOCKED.md` is referenced by the CV-screening SOP and
   `MEMORY.md` and **does not exist in the repo**.

See [lesson_tests_must_not_touch_production_2026_09_22.md](lesson_tests_must_not_touch_production_2026_09_22.md)
for the DDL hazard fixed at the start of this session.
