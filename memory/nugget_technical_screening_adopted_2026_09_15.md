---
name: Nugget Technical Screening — Read + Documented (2026-09-15)
description: Nugget's technical screening is a LIVE engine in the shared Markaz Neon DB (public.nugget_screening_*), owned by Aymen Abid, not a skill file to import. Coco documents the method in Skill 02 and reads results READ-ONLY via scripts/screening/read_nugget_screening.py. Three defects found and written up for Aymen.
type: project
---

# Nugget Technical Screening — Adopted as READ + DOCUMENT (2026-09-15)

## What happened

Ayesha asked to "import the skills of Agent Nugget and deploy them on our live version", then
specified **technical screening**. The assumption on both sides was that this meant porting a
markdown skill file from Nugget's repo, the way Coco adopted Noah's talent-sourcing skill in
April 2026.

**It did not.** Nugget's technical screening is a live production subsystem already writing to
the same Neon database Coco reads. There was nothing to import. Importing would have duplicated
a working system against the same tables.

🔑 **LESSON: before porting a capability from a sibling agent, check whether it already exists in
shared infrastructure.** The repo was never the source of truth here; the database was. Five
turns went into hunting a GitHub repo (`Jaw901/Nugget` 404s, six guessed names missed) for a
system that was already reachable from a SQL prompt.

## What it actually is

Eight tables in the **`public`** schema: `nugget_screening_rubrics`, `_runs`, `_run_items`,
`_evals`, `_reports`, `_resume_cache`, `_run_events`, `nugget_sessions`.

⚠️ A **`nugget_deg`** schema holds the same 12 table names and is **completely empty**. Query
`public`. Reading `nugget_deg` and concluding "no screening exists" would be a false negative.

**Owner:** aymen.abid@taleemabad.com. **Live as of:** runs on 2026-09-14.
**Volume:** 3 active rubrics, 6 runs, 2,087 run items, 863 evals, 1,011 cached resumes.

| Job | Role | Scored | Unusable | Avg |
|---|---|---|---|---|
| 38 | AI Engineer Lead | 612 | 57 (8.5%) | 44.0% |
| 37 | Lead Analytics Engineer | 54 | 6 (10.0%) | 32.7% |
| 13 | Full Stack Developer | 19 | 48 (71.6%) | 10.2% |

## The decision (Ayesha, 2026-09-15)

**Read it + document the method.** Not import, not rebuild.

- Method documented at
  [.claude/skills/02_candidate-evaluation/technical-screening.md](../.claude/skills/02_candidate-evaluation/technical-screening.md)
- Read path at `scripts/screening/read_nugget_screening.py` (verified working on all three
  code paths)
- 🔒 **READ ONLY.** The script refuses any statement that is not a SELECT. Rubric changes,
  re-runs and tier changes are Aymen's.

## What Coco can learn from this rubric

Nugget's rubric does NOT have the anchor-floor defect that inflated Coco's RM case-study round
(see [lesson_scoring_anchor_floor_inflation_2026_09_02.md](lesson_scoring_anchor_floor_inflation_2026_09_02.md)):

- Anchors run **0 to 5 with a real, written zero** ("The CV does not mention the must-have skills
  at all"), and the scoring rule is explicit: *"An absent skill scores 0, not a middling guess."*
- Confirmed in the data: Job 38's 612 scored candidates average 44.0% across the full 0 to 100
  range, 378 of 612 in the bottom tier. The scale is genuinely used.
- **Do not "correct" these scores upward for looking harsh.** Coco's instinct to do exactly that
  is what caused the RM inflation.

Two more transferable ideas:
- **Dimension gates on the top tier.** P1 needs `must_have_skills >= 4` AND `stack_match >= 3`,
  so a strong aggregate cannot hide a critical weakness.
- **`is_current` / `superseded_by` on every eval.** A re-mark retires the old score natively.
  Coco had to do this by hand on the RM round and missed three artefacts.

## Three defects found and written up

Full evidence: [docs/nugget_screening_defects_2026_09_15.md](../docs/nugget_screening_defects_2026_09_15.md).
Ayesha is passing these to Aymen; Coco did not contact him.

1. **Every `claude-opus-5` run failed in bulk at $0.00 recorded cost** (245/269, 602/645,
   377/436). Every `claude-haiku-4-5` run completed clean with real spend. Zero cost plus mass
   failure means it died before a billable call, so it is a model-id or API problem, not
   quality. Same shape as Coco's `ANTHROPIC_MODEL` Railway override.
   Also: the Job 13 Opus run is recorded `completed` while losing 86% of its items.
2. **Job 13 never got most of its CVs.** 48 of 67 evals have `resume_type = null` and
   `resume_chars = 0`; the 18 that parsed average 1,313 chars against ~5,300 on Jobs 37 and 38.
   A retrieval failure, not a weak pool. **Job 13's numbers are unusable for hiring decisions.**
3. **`resume_health` is decoupled from actual extraction.** Job 38's 10 `pdf-vision` evals
   average health 85.5 on **21 characters**, clearing the `min_resume_health: 60` gate and
   getting scored. App 2271 contradicts itself on one row: `tier_reason` says no extractable
   text, `verdict` describes the CV's contents in detail.

🔴 **The rule that follows: `UNUSABLE` is an extraction failure, never a rejection.** A candidate
whose CV would not open looks identical, in the tier column, to one who was read and found
unsuitable. If screening output ever feeds rejection letters, the first group gets rejected for a
document nobody opened.
