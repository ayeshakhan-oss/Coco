---
name: cv-screening-and-technical-screening-never-merge
description: "Non-negotiable (Ayesha 2026-09-25). Two separate skills, separate tables, separate tier vocabularies. Enforced by webapp/tests/test_screening_skills_stay_separate.py, which reads the AST so comments stay exempt."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7ebbd6b4-eec1-46e1-8ce7-b66c58d70a9f
  modified: 2026-09-24T19:56:31.637Z
---

Ayesha, 2026-09-25: *"the CV screening skill is entirely a separate skill and you don't have to
change anything on that. You cannot merge these two skills, these would remain separate unless I
say so."*

They stay separate **until she says otherwise in those words**. Not inferred from a request that
would be simpler if they merged.

**Why:** they look almost identical from a distance, which is exactly the danger. Both read Markaz
applications, both score a CV against a JD, both end in tiers, so a drifting edit would read as
tidying up. What differs is the part that matters:

| | CV Screening | Technical Screening |
|---|---|---|
| Tables | `coco.cv_screens`, `coco.cv_screen_skips` | `public.nugget_screening_*` |
| Method | Coco's three criteria, skills and experience first | Nugget's weighted rubric plus hard filters |
| Tiers | `shortlist / maybe / no_hire` | `P1-P4 / MANUAL_REVIEW / UNUSABLE` |
| Thresholds | calibrated against people actually hired, see [[candidate_evaluation_all_six_subskills_2026_09_23]] | P1 at or above 85, P2 at or above 70 |
| Router | `routers/cv_screening.py`, `/api/cv-screening` | `routers/tech_screening.py`, `/api/tech-screening` |

A score from one means nothing in the other's vocabulary. Merging them manufactures a number that
looks comparable and is not.

🔒 **The guard: `webapp/tests/test_screening_skills_stay_separate.py`** (38 tests). Neither side
imports the other, names the other's tables in executable code, or uses the other's tier
vocabulary. The routers keep distinct prefixes. The frontend pages do not import each other.

⚠️ **It reads the AST, not raw text.** Comments and docstrings are exempt deliberately: both
modules explain the separation *by naming the other side's tables*, and a gate that punished the
explanation would get the explanation deleted rather than the gate fixed.

**Proven, not assumed.** Per CLAUDE.md Rule 25 the checkers are fed deliberately broken source,
and the real `webapp/services/cv_screening.py` was broken on disk (3 tests failed) then restored
clean. A gate that has only ever passed proves nothing.

Related: Coco's read-only view of Nugget's *results* stays at `routers/evaluations.py`. The
read-only rule against `nugget_screening_*` was lifted on 2026-09-25 so Coco can launch its own
runs through `services/nugget_writes.py`; that lift is about writing runs, not about merging the
two skills. See [[nugget_repo_and_web_app_locations_2026_09_25]].
