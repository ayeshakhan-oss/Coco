---
name: RM below-70 marked-scripts sheet (2026-09-08)
description: Exam-style marked script sheet for the 8 RM internal candidates below the published 70% bar; also records that the tracker's own Scores tab still holds the superseded first pass.
type: project
---

# RM internal case study — marked scripts for the 8 below 70%

Ayesha, 2026-09-08: mark them "like you're checking an exam" — per-question score, what's good,
what's missing — for visibility and transparency, since these are internal staff being rejected.

**Sheet:** `1tSl69wejsDdOBHppfqQXOpCC1HEdhCXNTBltcaNBt8k`
"RM Case Study - Marked Scripts (below 70%)" — Summary tab + one tab per candidate.
**Builder:** `scripts/reports/build_rm_marked_scripts_sheet.py` (rerunnable; creates a NEW
spreadsheet each run, so edit in place or delete the old one rather than re-running blindly).

Each candidate tab: name/code, total vs the 70 bar, Q10 band, link to their anonymised script,
examiner's overall comment, an explicit **What's good** block and **What's missing** block, the
**marking caps that fired** with their benchmark wording, then a Q1–Q10 table with max, awarded,
the 0–5 anchor, what they wrote, and what would have scored higher.

| Code | Name | Total | Caps |
|---|---|---|---|
| RM-14 | Rida Abbas | 56 | C2, C6 |
| RM-07 | Khadija Akbar | 59 | C1b, C2 |
| RM-21 | Areej Noshad | 60 | C1a, C4 |
| RM-11 | Hafsa Bashir | 62 | C1a, C4 |
| RM-01 | Sana Nawaz | 63 | C1, C2 |
| RM-20 | Toseef ur Rehman | 63 | C1b, C2 |
| RM-18 | Javeria Nayyab | 64 | C1b, C2 |
| RM-12 | Muhammad Salman | 65 | C1b, C6 |

## 🔴 The tracker's Scores tab is STALE and contradicts the live result
Sheet `1xtQxfblMXmA5IpnvnABkK5bvmhPMK5_Q6Z1wDiI59A8` tab **Scores** still holds the **superseded
first pass**: mean 88.3, **nobody below 70**, Javeria Nayyab ranked 9th on 91.5. The strict
re-mark (mean 75.0, 8 below 70) was emailed but **never written back to the sheet**. Deltas run
from -27.5 (Javeria) to +0.5 (Danish). Anyone opening that tab reads the wrong scores.
**Rule: when a re-mark supersedes a pass, update every artefact that carries the old numbers, not
just the report.** Decide with Ayesha whether to overwrite the tab or archive it as "Scores
(superseded first pass)".

## Marking mechanics worth reusing
- Marks are the **0–5 anchor converted pro-rata** to the case's own printed points
  (Q1 10, Q2 15, Q3 10, Q4 15, Q5 10, Q6 10, Q7 10, Q8 10, Q9 10 = 100). Q10 has no printed
  points and is **banded only**, in no total.
- **Verify twice in code**: marks must sum to the stated total AND anchors×points must reproduce
  it. Both reconcile for all 8.
- Caps are applied **mechanically from the benchmark text**, never by feel — C1a/C1b (below-grade
  misread, verdict-driving vs not), C2 (Q4 no arithmetic), C3 (drops a Very High activity),
  C4 (cuts 15pp, never prices the +25%), C5 (Q7 refuses to choose), C6 (required element absent),
  C7 (not attempted). Publishing the cap wording next to the mark is what makes a rejection
  defensible to an internal candidate.
- Source data (`strict_scores.json`, `qbq.json`, `roster.json`) copied into `output/rm_marking/`
  so the sheet no longer depends on a session temp directory.
- `googleapiclient.discovery.build` clashes with a local `build()` — import it as `gbuild`.

Related: [[project_rm_internal_case_study_round_2026_09_02]] ·
[[lesson_scoring_anchor_floor_inflation_2026_09_02]] ·
[[project_rm_internal_case_study_tracker_2026_08_31]]
