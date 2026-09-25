---
name: Active Session Scratchpad
description: Live notes for the current session. Wiped at session start by UserPromptSubmit hook. Summarized into lessons_learned.md by Stop hook.
type: project
---

# Active Session — 2026-09-25

## Task
Three separate defects Ayesha hit in sequence, all reported as "screening is
broken", all different underneath.

1. **CV screening stopped midway** (job 17 CPD Coach). A Railway redeploy
   killed a fifty-minute run; the client loop had no retry. Fixed, deployed.
2. **"Still 81 to be screened"** on a position that was finished. Refusals were
   never recorded, so "could not be read" and "not looked at yet" were the same
   state. Fixed, deployed, 81 backfilled.
3. **Technical screening failed all 20 candidates** and blamed their CVs. The
   rubric's `output_schema` was never sent to the model. Fixed, deployed,
   verified against the live model.

Plus a **full production outage** (30 min) from a commit that shipped a
`main.py` importing files that were never committed.

## Decisions Made
- Built the rollback for the outage, verified it (tree byte-identical to
  af3df06, backend booting, tsc clean), and held it UNPUSHED when the peer
  session said its real fix was imminent. Ayesha had instructed a rollback; a
  peer cannot override that, so the condition was "push it if nothing lands
  shortly". The peer's fix landed, so she got the app back WITH the feature.
- Declined to add a CLAUDE.md rule because a peer asked. CLAUDE.md is Ayesha's
  standing instruction to every future session; a peer cannot authorise a
  change to it in either direction. Put the wording to her instead.
- Recorded the seven-block finding in memory rather than duplicating the peer's
  note on nugget-web — one finding, one file.

## Mistakes / Corrections
- **My first fix for the schema bug reproduced the original error.** I read
  `content[0].input` of the tool reply. Haiku answers a forced tool in SEVEN
  blocks, one per top-level property, so the first block is `{"extracted": ...}`
  alone and looks exactly like a refusal to score. Caught only because I re-ran
  end to end against the live model instead of trusting the fix.
- **Assumed truncation before measuring.** The JSON errors at char ~11,000
  looked like a max_tokens cut. `stop_reason` was `end_turn` at 2,912 tokens.
  The dimension order also disproved it: `must_have_skills` is FIRST, and a
  truncated reply drops the last thing, not the first.
- A test assertion of mine used the wrong operator precedence and reported a
  TypeError while the code under test was correct.
- Two of my early frontend tests asserted my own arithmetic rather than the
  code's contract, and had to be corrected to the real behaviour.

## Files Modified
- `frontend/src/lib/screenAll.ts` (+ `.test.ts`, new) — retry loop, `failed` channel
- `frontend/src/pages/CVScreeningPage.tsx`, `TechScreeningPage.tsx`
- `frontend/src/lib/types.ts`, `api.ts`, `package.json` (vitest added)
- `webapp/services/screening_runs.py`, `drafting.py`, `schemas.py`, `models.py`, `db.py`
- `webapp/routers/cv_screening.py`
- `alembic/versions/0015_cv_screen_skips.py` (applied)
- `webapp/tests/test_cv_screening_router.py`, `test_tech_screening_contract.py` (new)
- `scripts/jobs/backfill_cv_screen_skips.py` (new)
- memory: `lesson_long_runs_must_survive_redeploys_2026_09_23.md`,
  `lesson_structured_output_contract_2026_09_25.md`

Commits: d9c8264, 925afcf, 79a4c0d, d53c216, aef5973 (+ peer's bbd92d6 for the outage).

## Open for Ayesha
- Whether the seven-block / stored-schema finding becomes a CLAUDE.md rule.
- **`nugget-web` has no source in any repository** — all 11 deployments, none
  from git, and it is the only implementation that has ever scored a full
  position (669 candidates, 14 Sep). Ask Aymen for the source.
- A pre-push hook for the tracked-modules test (peer's recommendation).
- Two sessions sharing one working tree: a broad `git add` swept this session's
  files into the peer's commit.

## Pre-Send Checks
- [x] No candidate emails sent this session — code only
