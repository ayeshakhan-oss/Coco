---
name: A long run must survive a redeploy, and its progress must never be stale (2026-09-23)
description: CV screening stopped at 236 of 410 because Railway redeployed under it and the loop had no retry; the page then said 67, because the stat boxes were only refreshed on the success path.
type: project
---

# A long run must survive a redeploy, and its progress must never be stale

**2026-09-23. Ayesha: "its screening on railway now but not screening all the
profiles. the screening process stops midway."**

## What actually happened

CPD Coach, job 17, 410 applications. The run went cleanly for fifty minutes at
about five candidates a minute and stopped dead at **19:12:55 UTC with 236 of
410 done**. Nothing was wrong with the screening.

The evidence that settled it, in order:

1. **The container had started at 19:15:16 UTC and logged nothing since** —
   one minute before her screenshot. `railway logs -d --json` carries the
   timestamps; the plain output does not.
2. **`railway deployment list --json` showed three deploys inside that one
   run:** 18:46, 19:10 and 19:13 UTC. The 19:13 one killed the request in
   flight.
3. **The database had the run's own shape:** a per-minute histogram of
   `coco.cv_screens.created_at` showed five a minute from 18:23 to 19:12:55,
   then nothing. The 18:46 deploy is visible in it too, as a four-minute hole
   between application 900 and 903.

🔑 **The database is the run's flight recorder.** `date_trunc('minute',
created_at)` with min/max of the cursor column reconstructs a run exactly:
when it started, its rate, where it stalled, where it died. Reach for that
before theorising.

## Three defects, not one

**(a) One dead request ended the run.** The client loop had no retry, so a
redeploy, a phone changing network, a sleeping laptop and a stray 502 all cost
the whole run. Fixed in `frontend/src/lib/screenAll.ts`: ten attempts over five
minutes, because that is how long a redeploy takes to come back. 401/403/404/422
still stop at once. Retrying is safe because the server commits each candidate
as it finishes and **the cursor only advances on success**, so a retry re-asks
from the last confirmed position and the server's own unscreened query excludes
anyone the dead request had already committed.

**(b) The error was invisible.** The run reported failures as
`screenError` with `id: -1`, and that state is rendered only against a row
whose `application_id` matches. **-1 matches no row**, so the panel simply
vanished and the run looked like it had stopped for no reason. 🔴 **An error
written to a slot that renders conditionally is not an error the user sees.**

**(c) The page said 67 when the database held 236.** The stat boxes were
refreshed once, after the loop, **inside the `try`** — so the one path that
most needed fresh numbers, the failure path, never refreshed them at all. She
was looking at a count from when the page was opened, 169 candidates stale.
🔴 **Put the progress refresh on every path, not the happy one.** A run that
did 58% of the work should never look like one that did 16%.

## Rules

- **A client-side loop that runs for more than a few minutes against Railway
  MUST retry transient failures.** Deploys land on top of runs; on this day
  three did. Budget the retry to span a redeploy (~5 min), not a blink.
- **Never advance a cursor on a failed request.** Re-ask from the last
  confirmed position and let the server's own "not yet done" query deduplicate.
- **Report the outcome of a long run out loud** — finished, stopped, or failed
  with how far it got — in the run's own panel.
- **Refresh progress in a `finally`, or after every batch.** Never only on
  success.
- **Extract the loop so the failure can be tested.** Reproducing this by hand
  needed a fifty-minute run and a deploy at the right moment. The loop now
  takes its dependencies injected and has 12 vitest tests; **5 of them were run
  against the old behaviour and fail**, because a gate that has only ever
  passed proves nothing (Rule 25).

## Notes for next time

- `vitest` now exists in `frontend/` (`npm test`). It did not before.
- ⚠️ **Check for a peer session before deploying.** `ListAgents` showed
  `agent-coco-64` busy and mid-`railway up`; it pushed twice while this fix was
  being written. Fetch before assuming what a push will carry.
- Unreadable CVs keep a position from ever reaching zero unscreened. That is
  correct (Rule 32) but it must be *said*, or the leftover count looks like a
  bug.
