# 🔒 LESSON — Anchor floors inflate scores until the scale cannot fail anyone (2026-09-02)

**What happened.** I scored all 25 RM case studies and reported that every one cleared the
published 70% bar (mean 88.3). Ayesha asked "why are they all above 70, were they actually
that good?" and then told me to re-read all 25 line by line. She was right. A strict re-mark
against the SAME benchmark moved the mean to 75.0 and put 8 of 25 below the line.

## The tell — check this on every scored pool BEFORE reporting
Across 25 submissions I never used the bottom half of the scale. Per-question LOWEST mark
given, out of 25 candidates:

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 |
|----|----|----|----|----|----|----|----|----|
| 40%| 40%| **75%** | 60% | **70%** | 60% | **70%** | 60% | **70%** |

**On four of nine questions the WORST answer of 25 still scored 70%.** A question whose
weakest answer earns 70% is not measuring anything. Run this check as a matter of course:
`min(anchor) per question`. If the floor across a large pool is above ~40%, the scale is broken.

**The contradiction that proves it:** I reported that only 6 of 25 read the central data
correctly and 12 made a factual error — yet the data question averaged 85% and its floor was
11/15. Getting the core analytic task WRONG cost ~2 marks in 15. If a stated finding and a
question's mean distribution contradict each other, the marking is wrong, not the finding.

## The three causes
1. **Anchor floor of 1, not 0.** Benchmark anchors written as 5/3/1 convert to 100/60/**20**%.
   Nine questions x a guaranteed 20% floor = ~20 points of free base before anything true is
   written. **Always define and use a real 0.**
2. **Credited structure and method over correctness.** A well-organised answer built on a
   misreading scored like a correct one.
3. **Never applied the benchmark's own caps.** The key said plainly that no arithmetic on the
   capacity question is a bottom anchor and that a factual error against the case data is
   serious. I treated both as deductions of a mark or two.

## The rule going forward
- **Convert anchors on the full 0-5 scale** (5=100, 4=80, 3=60, 2=40, 1=20, 0=0).
- **Write the caps as mechanical rules BEFORE scoring**, derived from the benchmark's own
  wording, and apply them by rule not by feel. Record which cap fired on each candidate.
- **Tick each required element individually** rather than judging an answer as a whole. This is
  what surfaced missing escalation triggers, absent source columns and 3-column stakeholder
  grids where 5 were required.
- **Split "wrong" from "different".** A misreading that DRIVES the verdict caps the question; a
  misreading whose verdict survives on other evidence costs one anchor level. Decide this rule
  in advance and apply it to everyone. (I had to split mine mid-pass and re-checked the earlier
  candidates against the new rule.)
- **A high mean from a single unmoderated marker is a red flag, not a finding.** Say so, and
  offer a second reader on a sample.

## Also confirmed this round
- Atomic + utf-8 + `ensure_ascii=True` score writes. A cp1252 `write_text` error truncated
  scores.json to 0 bytes and lost 7 records. Pattern: `mkstemp` in the same dir + `os.replace`.
- **Text-overlap sweeps need the pasted case brief stripped first.** RM-11 and RM-21 shared
  17.6% of 8-grams purely because both pasted the entire brief into their submission; that also
  inflated their apparent overlap with four others. The real signal was elsewhere and much
  quieter: two submissions sharing only 0.76% of 8-grams, but with distinctive phrases in
  MATCHING structural positions and identical derived figures. Look at WHERE the shared strings
  sit, not just how many there are.

See also [[project_rm_internal_case_study_round_2026_09_02]] ·
[[feedback_benchmark_and_report_hygiene_2026_08_17]] · [[candor_weak_pool_verdict_2026_07_21]]
