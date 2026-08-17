---
name: SMG Case Study Evaluation + GM Pipeline State (2026-08-17)
description: Job 42 SMG case-study benchmark, rubric and all-8 evaluation; plus the GM Karachi/Lahore debrief + submission state, the Markaz-email-mirroring discovery, and the field-staleness problem.
type: project
---

# Job 42 SMG — Case Study Benchmark, Rubric & Evaluation (2026-08-17)

## What was built

| Artefact | Path |
|---|---|
| Benchmark answer key | [docs/case_studies/benchmarks/smg_execution_sprint_benchmark.md](../docs/case_studies/benchmarks/smg_execution_sprint_benchmark.md) |
| Scoring rubric + report spec | [.claude/skills/02_candidate-evaluation/case-study-scoring-rubric.md](../.claude/skills/02_candidate-evaluation/case-study-scoring-rubric.md) |
| Benchmark send script | `scripts/reports/send_smg_benchmark_pilot.py` |
| Evaluation report script | `scripts/reports/send_smg_case_study_evaluation_pilot.py` |

**Order is non-negotiable:** benchmark written and QA'd → *then* submissions read → then scored.
Rule 0 of the rubric. I broke it once (read Umar's before writing the key, because Ayesha sent
it early) and disclosed it in the report.

**Rubric:** 6 dimensions, 1–5, weighted — Data 20% · **Execution 25%** · Stakeholder 20% ·
Commercial 15% · Discipline 10% · Signal 10%. Execution carries most because the JD leads with
hands-on execution (2IC, 40–60% travel). Bands: 80+ strong yes / 65–79 yes / 50–64 borderline /
<50 no. **Never force a fixed shortlist size.**

## Final scores (all 8, verified against raw CSVs)

| # | Candidate | App | Score | Band |
|---|---|---|---|---|
| 1 | Shahmir Hashmat | 3911 | 98* | Strong yes |
| 2 | Muhammad Arshan Bilal | 3884 | 94 | Strong yes |
| 3 | Yusra Amjad | 4061 | 89 | Strong yes |
| 4 | Umar Zahid | 3902 | 78 | Yes |
| 5 | Junaid Ali | 3992 | 74 | Yes |
| 6 | Arooj Khalid | 3868 | 70 | Yes |
| 7 | Irfan Siddiqui | 4144 | 53 | Borderline |
| 8 | Syed Basit Hussain | 4142 | 46 | No |

\* provisional — Shahmir's reflection is a `.m4a` voice note that cannot be transcribed here, so
1 of 6 dimensions is unassessed.

**No candidate fabricated data.** Every headline figure recomputed from the CSVs and matched.

## Findings candidates produced that the benchmark missed

Deliberately **not** added to the benchmark (Ayesha: "benchmark doesn't need candidate's
response" — it destroys reusability). Recorded here instead:

- **22.9% of coaching sessions fail** (27/118), median 38 min of audio lost vs 36 min on
  completed — not a length limit. *Shahmir*
- **No Sinhala or Tamil reading passage exists** — all 87 assessments `en`/`ur`. *Shahmir*
- **52.1% of registered Sri Lankan users teach university only** vs 6.9% in Pakistan — the
  *causal* reason for zero coaching adoption (no class to record). *Junaid*
- **Sri Lankan registrations complete in a median 4.2 min (p90 11 min)** vs Pakistan's 37.2 min
  and highly variable — signature of a pre-loaded list. Corroborated: registration doubles
  engagement in PK, changes nothing in LK. *Yusra*
- **Lesson-plan users adopt coaching at 12.9% vs 6.4% base** (22/170). *Arooj*
- **PK registration funnel failure states**: 23 template-never-delivered, 52 flow-abandoned.
  *Irfan*
- Methodological: `active_day1`/`active_week1` are ~99% true and useless; the dataset ends
  16 Dec so the 11 Dec cohort is right-censored. *Arshan, Shahmir*

## Two scoring corrections worth remembering

1. **Never conclude a deliverable is missing from a converted copy.** I scored Umar's execution
   4 and flagged his tracker as possibly absent — it existed, five tabs, arguably the best in the
   pool. I had only seen a **PDF of the analysis sheet**. Corrected to 5, total 73 → 78.
2. **Content can live somewhere other than the named deliverable.** Irfan's three experiments
   looked missing (two empty slides) but were in his workbook. Packaging failure ≠ missing work.

---

# GM Karachi / Lahore pipeline state (as of 2026-08-17)

## GM Karachi (job 41) — 156 apps, 9 values-interviewed, 7 pass / 2 fail

Case studies in (4): Waqas Hassan, Muneeb Arif, Huda Shaikh, Marzia Hasnain.
Outstanding (3): **Zirghaam Ahmad, Zubair Hussain, Syeda Masooma Asif.**
Values fail: Muhammad Huzaifa Wakil, Yashfeen Zahid (rejected).

**Sent live 2026-08-17:**
- Case-study nudges → Zubair Hussain, Zirghaam Ahmad (`scripts/send_case_study_nudge_zubair_zirghaam_pilot.py`)
- Debrief invites → Muneeb Arif, Marzia Hasnain, Huda Shaikh
  (`scripts/send_case_study_debrief_gm_karachi_batch3_pilot.py`)
  Booking link `https://calendar.app.google/SzQgacaWQqnLEQ449` — extracted from the live
  7 Aug Waqas Hassan send, never fabricated.

## GM Lahore (job 39) — fully worked through
All 4 submitters (Salman Tariq, Ahmad Wajahat, Abdul Wahab, Muhammad Waqas) were invited and
booked. Only **Abdul Wahab's** debrief has completion evidence (meeting report, 13 Aug).
**Hafiz Osama** — values pass 28 Jul, case study sent 4 Aug, **still not submitted (13 days)**.

## 🔴 Open items
1. **Zirghaam was sent the WRONG brief.** His 7 Aug email carries the SMG Execution Sprint doc
   (`1Ygsscl6…`); he has no SMG application. He also **replied 8 Aug** asking to submit after
   12 Aug (family, Northern Areas, patchy internet) and **nobody answered him**. Ayesha chose to
   send the standard nudge anyway. The correct GM brief still needs sending.
2. **Masooma** not yet nudged. **Hafiz Osama** not yet nudged.
3. **App 3871 "Ayesha Khan" (ayesha.khan@taleemabad.com) is a test record inside job 41** —
   delete so it stops inflating pipeline counts.
4. Zubair Hussain's Zero In Call was **cancelled 13 Aug** — unclear by whom.

## 🔴 Markaz field staleness — do not trust these fields
- `case_study_status` stays **null** when Markaz sends a case study → four candidates looked
  "never sent" when they had been. **Always cross-check the mailbox.**
- `gwc_interview_date` is null and `interview_steps` "Not Started" for **all 8** GM submitters,
  including Abdul Wahab whose debrief demonstrably happened.
- Two Lahore candidates still read `case_study_sent` after submitting.
- Markaz subject lines contain **double spaces** ("Growth  Manager") — keyword searches miss them.

Related: [[markaz_submissions_arrive_by_email_2026_08_17]] ·
[[feedback_benchmark_and_report_hygiene_2026_08_17]] ·
[[case_study_nudge_type_2026_08_10]] · [[reference_ayesha_mailbox_imap_2026_08_10]]
