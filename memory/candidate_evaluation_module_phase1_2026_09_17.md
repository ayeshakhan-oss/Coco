---
name: Candidate Evaluation Module — Phase 1 Built (2026-09-17)
description: The webapp's second module is live-ready: a READ-ONLY view over Nugget's screening results. Records the four traps that cost fix rounds (SQLAlchemy cannot parse :name::type, three separate single-live-module hardcodes, MANUAL_REVIEW is an unreadable-CV bucket not a score band, diff review cannot catch a runtime 500).
type: project
---

# Candidate Evaluation module, Phase 1 (2026-09-17)

**Branch:** `feat/candidate-evaluation-phase1`, 16 commits, **not merged, not deployed.**
**Spec:** [docs/specs/2026-09-16-candidate-evaluation-module-design.md](../docs/specs/2026-09-16-candidate-evaluation-module-design.md)
**Plan:** [docs/plans/2026-09-16-candidate-evaluation-phase1.md](../docs/plans/2026-09-16-candidate-evaluation-phase1.md)

Makes the app's `candidate-evaluation` tile live with a read-only view over Nugget's screening
results (3 rubrics, 863 evaluations). Four GET endpoints under `/api/evaluations`, a
`nugget_reads` service, an `EvaluationPage`, and Skill 02 shipped into the Docker image.

**Final state:** 128 tests pass, clean build, all endpoints 200, error paths 400/404/422,
`assert_read_only` never modified, and Nugget's tables unchanged throughout
(evals 863, rubrics 3, runs 6, run_items 2087, reports 2).

---

## 🔴 The four traps, each of which cost a fix round

### 1. SQLAlchemy `text()` cannot parse `:name::type`
The tier filter written as `(:tier::text IS NULL OR tier = :tier::text)` made SQLAlchemy bind
**only `job_id`** and Postgres raise a syntax error at `:`. **The whole candidates endpoint 500'd
on every request** and TWO diff reviews passed it. Probed against the live DB:

| form | binds | Postgres |
|---|---|---|
| `:tier::text` | `['job_id']` | SyntaxError at ":" |
| `CAST(:tier AS text)` | `['job_id','tier']` | **works** |
| bare `:tier` | `['job_id','tier']` | `AmbiguousParameter: could not determine data type` |

**Use `CAST(:name AS type)`.** Both other forms fail, for different reasons. A regression test now
asserts the bind names are recognised and that `"::"` appears in no SQL constant.

### 2. 🔴 A diff review cannot catch a query that only fails at runtime
The 500 above survived a task review AND a scoped re-review, because both read diffs. It was found
by starting the server and curling. **Run the endpoints. Every time.** There is now
`webapp/tests/test_evaluations_api.py` (TestClient over all four endpoints plus the error cases,
`skipif` when `DATABASE_URL` is absent) so this cannot recur silently.

### 3. `MANUAL_REVIEW` is an unreadable-CV bucket, not a low score band
All 12 MANUAL_REVIEW rows across jobs 13 and 38 have `score_pct` **0.00** with average extracted
text of **6 and 10 characters**. The rubric's `manual_review_rules` (`min_resume_chars: 500`,
`min_resume_health: 60`) route candidates there *because the document was unreadable*. Rendering
"0%" against it makes a candidate whose CV never opened look like they scored zero.
**`UNSCORED_TIERS = ("UNUSABLE", "MANUAL_REVIEW")`; both are score-suppressed.**
⚠️ This fix was initially applied to the webapp only and **missed `scripts/screening/read_nugget_screening.py`**,
which kept printing `0%`. When a display rule is decided, apply it to every renderer.

### 4. A "single live module" assumption hides in THREE places
Flipping `modules.ts` status to `'live'` is not enough. `HomePage.tsx`, `components/AppLayout.tsx`
and `ComingSoonPage.tsx` each independently hardcoded `slug === ACTIVE_MODULE`. AppLayout was the
worst: it also rendered ONE hardcoded sub-page list for any live module, so Candidate Evaluation
would have shown Candidate Communication's Queue/Review/History. Modules now carry their own
`route` and sub-page list.

---

## What the whole-branch review caught that per-task reviews did not

Per-task reviews see one diff; the final review saw the branch. It found six Important defects
after five clean task reviews, including `?limit=-1` reaching Postgres as `LIMIT -1` → unhandled
500 (no `ge=1`), and the candidate list silently showing **100 of 669** with no "showing N of M",
so a user would conclude a candidate was never screened. **Do not skip the whole-branch review.**

🔴 It also judged my own rulings, and was right: **accepting zero tests on the DB-backed functions
(Ruling 2) is what let three of those defects through**, and its stated cost had already come due
once as the 500. A cheap integration test at the start would have caught all of it.

⚠️ A reviewer can also be wrong. One finding claimed the `unscored` banner mislabelled its bucket;
it had inferred the meaning from a TypeScript comment. The backend and live API disagree:
`unscored` = 59 on job 13 = 11 MANUAL_REVIEW + 48 UNUSABLE, spanning both buckets, not a subset of
`scored`. **Check a finding against the data before acting on it.** The misleading comment was the
real defect.

## Process notes

- **Two subagents stalled on oversized dispatches** (12 findings across backend + frontend + a full
  restyle; then a 65KB diff with 15 findings to verdict). Neither left partial edits. Split by
  layer and they completed. The "one fix dispatch" guidance has a practical ceiling.
- A fix wave can introduce its own Critical: a failed "Load more" set the same error state the
  initial load used, permanently hiding an already-populated table.

## Not done

**Phase 2 (values scorecard scoring) is not built**, and Ayesha asked for Phases 1 and 2 in one
deploy, so nothing has shipped. Phase 2 needs its own plan. Decision on record: submitting a values
scorecard to Markaz requires the **`approver`** role, the same gate as sending a candidate email.
