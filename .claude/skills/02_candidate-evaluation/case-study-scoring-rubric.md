---
name: case-study-scoring-rubric
description: Benchmark-anchored scoring rubric and evaluation report spec for growth case studies. Extends case-study-evaluation.md (which covers tracking/completeness only). Use when scoring submissions and recommending proceed/don't-proceed to debrief.
---

# Case Study Scoring Rubric & Report Spec

**Status:** DRAFT — pending Ayesha's QA (2026-08-16)
**Companion:** [case-study-evaluation.md](case-study-evaluation.md) covers *tracking and
completeness*. This file covers *scoring and the recommendation*. Read both.
**Benchmark:** [docs/case_studies/benchmarks/smg_execution_sprint_benchmark.md](../../../docs/case_studies/benchmarks/smg_execution_sprint_benchmark.md)

---

## Rule 0 — The benchmark is written before submissions are read

Scoring calibrates to whoever is read first. Build and QA the benchmark **before** opening any
submission. If a submission has already been seen (it happens — Ayesha may send one early),
say so explicitly in the report so the bar can be judged accordingly, and derive benchmark
figures from the source data rather than from that candidate's work.

## Rule 1 — Every score cites evidence

A dimension score with no quoted line, slide number or figure behind it is not a score, it is
an impression. Cite the location.

## Rule 2 — Verify every number against source data

The benchmark contains a verified ground-truth table. Check candidate figures against it.
Distinguish three cases, they are not the same thing:
- **Wrong** — contradicted by the data. Serious.
- **Definitional** — different but defensible denominator (e.g. all users vs registered users).
  Note it; do not penalise.
- **Fabricated** — a figure that does not exist in the dataset and cannot be derived. Disqualifying.

## Rule 3 — Score reasoning, not agreement

A candidate reaching a different conclusion with a real argument scores as high as one who
matches the benchmark. Never mark down for disagreeing with us.

---

## The six dimensions

Each scored 1–5. Weighted total out of 100.

| # | Dimension | Weight | What it reads |
|---|---|---|---|
| 1 | **Data judgment** | 20% | A1 — did they find the real signal or the loudest one |
| 2 | **Execution specificity** | 25% | A2 — who does what, when, through which channel |
| 3 | **Stakeholder craft** | 20% | A3 email + the layered engagement in A2 |
| 4 | **Commercial honesty** | 15% | A3 internal update — real probability, real ask |
| 5 | **Decision discipline** | 10% | Kill criteria, contingencies, labelled assumptions |
| 6 | **Signal & self-awareness** | 10% | Reflection + AI disclosure quality |

### Anchors

**1. Data judgment**
- **5** — Separates activity from value using numbers. Catches at least one structural trap
  (registration as vanity metric / spike concentration / missing attribution). Sizes small bases
  before planning against them.
- **3** — Correct arithmetic, sensible segmentation, conclusions defensible but conventional.
  Reports what the data says without interrogating what it cannot say.
- **1** — Restates totals as achievement. Ranks on registration or user counts. Numbers wrong or
  absent.

**2. Execution specificity**
- **5** — Named owners, channels, sequencing and weekly exit metrics. A tracker that could be
  used on Monday. Identifies which transition actually stalls and concentrates effort there.
- **3** — A plausible phased plan with metrics, but generic actions ("engage stakeholders",
  "drive adoption") that would fit any company.
- **1** — Strategy restated as plan. No owners, no dates, no tracker, or a tracker that is a
  formatted table with nothing to enter.

**3. Stakeholder craft**
- **5** — The email would land well with a real government official: acknowledges the situation
  without demanding explanation, makes an easy ask, removes work from their desk. Layered
  engagement distinguishes what each layer gets from what each layer gives.
- **3** — Professional, appropriately brief, but generic — could be sent to any stalled contact.
- **1** — Pushy, wounded, or a chase. Uses the deadline or the competitor as pressure. Ignores
  the six weeks of silence entirely.

**4. Commercial honesty**
- **5** — A specific probability with gating events in *both* directions, a concrete ask of the
  Head of Growth, and something uncomfortable said plainly.
- **3** — A probability with reasoning, a reasonable ask, no real discomfort.
- **1** — Optimism as forecast. No number, or a number with nothing behind it. Asks for
  "support".

**5. Decision discipline**
- **5** — Kill criteria that would genuinely stop work, not soften it. Assumptions labelled
  inline. Contingencies tied to named early warnings.
- **3** — Kill criteria present but soft ("if it underperforms, we will iterate").
- **1** — Absent, or success metrics with no failure condition.

**6. Signal & self-awareness**
- **5** — Reflection is specific, costly to admit, and shows early detection with a real
  consequence. AI disclosed per deliverable, distinguishing AI work from own judgment.
- **3** — A real story told generically. AI disclosed once, vaguely.
- **1** — Generic or borrowed reflection. No AI disclosure on obviously AI-assisted work.

---

## Flags — override the score

Recorded separately; a flag can outrank a high total.

| Flag | Severity | Meaning |
|---|---|---|
| **Fabricated data** | Disqualifying | Figures not derivable from the dataset |
| **Undisclosed AI** | Serious | Fluent generic prose, no disclosure, brief explicitly asked |
| **Materially incomplete** | Serious | A required deliverable missing entirely |
| **Instruction breach** | Note | Over page/slide limits, wrong format, duplicated slides |
| **Consent blindness** | Note | A2 shares classroom recordings with administrators without consent |

---

## Bands

| Total | Band | Action |
|---|---|---|
| 80+ | Strong yes | Proceed to debrief; probe the excellence markers they missed |
| 65–79 | Yes | Proceed; debrief targets the weakest dimension |
| 50–64 | Borderline | Proceed only if pool is thin; state what the debrief must resolve |
| <50 | No | Do not proceed; give the specific reason |

**Never force a fixed shortlist size.** If only three clear the bar, recommend three and say so.
A ranking presented as a selection misleads the reader.

---

## Report spec

HTML email, locked screening-report format ([REPORT_FORMAT_LOCKED.md](../../../REPORT_FORMAT_LOCKED.md)).

**Structure:**
1. **Four stat boxes** — submitted / scored / recommended / flagged
2. **Pool verdict, first and blunt** — honest read on quality before any individual profile
   (see `candor_weak_pool_verdict_2026_07_21`)
3. **Ranked table** — name (hyperlinked to submission), total, six dimension scores, band, flags
4. **Per-candidate deep dive:**
   - What stands out — the specific thing, quoted
   - What is thin — named, not hedged
   - Score by dimension with evidence
   - **Proceed to case-study debrief: yes / no**, with the reason
   - **Three debrief probes** — the specific questions that would resolve the remaining doubt
5. **Method note** — benchmark used, what was verified, what could not be accessed

**Pilot to Ayesha before any wider circulation.**
