---
name: Why CV screening kept looking like it stopped midway (2026-09-23 / 2026-09-25)
description: Two causes behind one complaint. A Railway redeploy killed a fifty-minute run because the loop had no retry, and the page then showed a stale 67 for a real 236. Then a SILENT REFUSAL read as work undone: 81 unreadable CVs counted as unscreened for ever. A refusal is a result; write it down.
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

---

# Part 2 (2026-09-25): the same complaint, a different cause

Ayesha ran the position again and asked why **81 of 411 were "still to be
screened"**. They were not. The run of 08:56-09:14 UTC attempted all 174 that
were left, screened 93 and refused 81. The position was finished.

## Refusing was right. Refusing SILENTLY was the defect.

A candidate whose CV cannot be read gets no `cv_screens` row, deliberately
(Rule 32: a model asked to judge an empty page still answers). But with **no
row of any kind**, "could not be read" and "not looked at yet" were the same
state to every reader. So a finished position reported 81 outstanding for ever
and offered a button that would re-read 81 unreadable files and change nothing.

🔑 **A refusal is a RESULT. If you do not write it down, it reads as work you
have not done.** Any code that declines to act on an input needs somewhere to
say so, or the absence gets interpreted as a backlog. This is the general form
and it is worth looking for elsewhere in the app.

## What the 81 actually were

Checked with the server's own extractor, then confirmed a second time by the
backfill running through `_screen_and_store` itself. Both agreed exactly:

| | |
|---|---|
| **43** | no resume stored in Markaz at all |
| **26** | file extracts to under 250 words (one was 117) |
| **12** | extraction fails outright: JPEG, PNG, legacy `.doc` (OLE2 header `\xd0\xcf\x11\xe0`) |

~20% of the position, close to the 1-in-6 Rule 32 already records.

## Rules

- **Record a refusal** (`coco.cv_screen_skips`, migration 0015) with the
  reason verbatim, a coarse `kind` for grouping, and **the Markaz filename** —
  what somebody chasing a missing CV actually needs.
- **A skip is DELETED, never superseded**, when the candidate later screens.
  `cv_screens` keeps history because a retired score still says what we once
  believed; a skip says only what is true now.
- **Do not record an UNEXPECTED failure as a skip.** That is a bug, not a
  statement about someone's document, and parking it as "could not be read"
  launders it into a candidate-facing state where nobody looks again.
- **Known-unreadable leaves the run.** `retry_skipped` is the only way back in,
  for after the files are fixed. Re-reading a JPEG costs real time and changes
  nothing.
- **Backfill through the real code path** (`_screen_and_store`), never by
  copying the message strings into a script — that guarantees drift.
- ⚠️ **`MIN_SCREENABLE_WORDS` is checked BEFORE the model call**, so a re-run
  over unreadable CVs costs zero model spend. Worth knowing before worrying
  about the cost of a retry.

## Notes

- The SQL probe suite (`test_router_sql_executes.py`) **caught the new table
  not existing** before anything shipped. It earns its keep.
- ⚠️ Two network-dependent nugget tests (`test_nugget_writes`,
  `test_screening_runs_sql`) each failed **once** and passed on every re-run.
  They probe the live Neon HTTPS endpoint; a transient error trips them. Not a
  regression, but they are flaky under a full-suite run.
