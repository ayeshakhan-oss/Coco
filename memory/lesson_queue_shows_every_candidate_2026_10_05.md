---
name: lesson_queue_shows_every_candidate_2026_10_05
description: The Candidate Queue's "All" hid 216 of 416 CPD Coach candidates (comms-only filter + silent 200-row cap); fixed for every position, every Markaz status labelled, unknown statuses shown raw.
metadata:
  type: project
---

# The queue's "All" was not all (2026-10-05)

**Trigger.** Ayesha, on `/queue?job=17` (CPD Coach): *"a lot of people are missing
from here"*, then *"it should show all regardless of anything otherwise we have
false data."*

**Measured against Markaz (Neon, read-only):** CPD Coach had **416** applications;
the page could show at most **200**. Two independent causes:

1. **"All" was the `relevant` bucket**, i.e. `comms_relevant`: only rejected /
   warm_bench / consider_other_roles / shortlisted / gwc_scheduled /
   case_study_sent / P2, or anyone with a `communications` row. That hid **151**
   on CPD Coach (134 new, 11 hired, 5 offer, 1 applied). The positions overview
   used the same filter, so a position with only new applicants never appeared.
2. **A silent 200-row cap.** `api.candidates` sent `limit=200` with no paging
   and no count. 265 qualified, so **65 more** vanished, the most recent
   applicants first (sort is high-priority then longest-waiting). Search went
   through the same cap.

**Fix (live: `8cb9b14`, then `3506f5b`):**
- "All" = bucket `all` (every application). Router default `all`, `limit` 500
  (max 1000). The `relevant` bucket still exists for old links.
- The client pages until a short page returns; the count shows beside the tabs.
- Position cards count every application ("N candidates in total").
- **Every Markaz status gets its own label:** `hired`, `offer`, `withdrawn`,
  `not_screened` (new + applied). Before, they would have read "Awaiting
  scorecard", which is false data too.
- **A status Markaz adds later** maps to `unrecognised` and the badge shows
  Markaz's own word ("Check status in Markaz"). Only NULL / '' / `P2` fall to
  `awaiting_scorecard`.
- SQL `displayed` CTE and Python `derive_display_status` / `_STAGE_DISPLAY` are
  kept in step by `test_the_sql_and_python_stage_maps_agree`.

**Verified:** CPD Coach returns 416 = Markaz; all of Markaz returns 4,515 = the
`applications` table, 0 `unrecognised` today. Railway `/healthz` reported each
commit. ⚠️ The signed-in page was **not rendered** (Google SSO, no local bypass),
so Ayesha was asked to eyeball it (Rule 39).

**Why it matters / how to apply:**
- **A filter labelled "All" must be all.** If a view scopes a population, its
  label says so. Hiding people by default reads as "they do not exist".
- **Never cap a list without showing the count.** A `limit` with no total is a
  silent truncation; page, or say "showing X of Y".
- **Every enum value from someone else's system needs an explicit branch, and
  the fallback must show the raw value, never borrow one of our labels.**
- ⚠️ Pre-existing, unrelated: `test_evaluations_api.py::test_job_candidates_endpoint_returns_paged_object_with_total`
  hardcodes a live Nugget count (378) and now sees 336. Fails with or without
  this change.
- ⚠️ `git stash` in this shared tree stashes the OTHER session's changes too.
  Do not use it to A/B a test; it popped back cleanly here, but check
  `git status` count before and after if you ever must.

Related: [[lesson_render_the_page_to_see_it_2026_10_01]] · [[lesson_untracked_module_outage_2026_09_25]]
