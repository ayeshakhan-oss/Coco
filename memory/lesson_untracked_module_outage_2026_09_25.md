---
name: An imported module that was never git-added took production down
description: 2026-09-25 outage. main.py imported webapp/routers/tech_screening.py, which was never committed; Railway builds from the commit, so every boot died with ImportError and the whole app 502'd for ~29 minutes. Guard test added.
metadata:
  type: project
---

# The outage: a file that existed everywhere except in git

**2026-09-25, roughly 09:07 to 09:36 UTC (~29 minutes). Whole app down, not one page.**

## What happened

Commit `e1894bb` changed `webapp/main.py` to add:

```python
from .routers import tech_screening as tech_screening_router
```

and pushed. `webapp/routers/tech_screening.py` was never `git add`ed. Railway
builds from the commit, so the image contained a `main.py` importing a file
that was not in it. Every boot died:

```
ImportError: cannot import name 'tech_screening' from 'webapp.routers'
```

`/healthz` returned 502. Ayesha hit it on the Technical Screening confirm step.
**Ten modules were untracked at that moment, across two features** (tech
screening and the invites work in progress).

## Why nothing caught it

The files were on disk locally. So imports resolved, `python -m webapp.main`
ran, and the whole test suite passed. **The defect is invisible from inside
the working tree and only exists once the tree is rebuilt from git.**

That is the same shape as the fake-session SQL bug: a check that never leaves
the developer's machine cannot see what the deployment will see.

## The fix

`webapp/tests/test_imported_modules_are_tracked.py`. It imports the app, walks
`sys.modules` for everything under `webapp`, and asserts each file appears in
`git ls-files`. Three companions:

- the same check for `alembic/versions`, where the mistake fails at request
  time instead of boot and is slower to diagnose;
- the same check for the frontend, resolving relative TS imports to files
  (128 imports across 39 files) — `e1894bb`'s own message records `App.tsx`
  having already imported an uncommitted page, which breaks the Vite build
  rather than the Python boot;
- a test that the check **bites**, by removing a real module from the tracked
  set and asserting it is reported.

⚠️ **The test is SUPPOSED to fail while a new module is being written**, from
the moment it is wired into `main.py` until it is committed. The fix is
`git add`, never a skip. It fired twice more in the same session and was
correct both times.

⚠️ **Limit:** `git ls-files` reads the INDEX, so a staged-but-uncommitted file
counts as tracked. That is the right trade day to day, and it still catches
the real case (neither staged nor committed).

## Two things worth keeping

🔴 **`railway up` ships the working tree; a GitHub-integrated deploy ships the
commit.** They disagree exactly when a file is untracked, and that difference
is the whole bug. Never reason about a deploy from what is on disk.

🔴 **`/healthz` 200 only proves the app BOOTED.** Probe one real route per
router: **401 = mounted and gated (pass), 404 = the router is not in this
build, 500 = mounted but failing, usually a missing table.** That three-way
read is what separated "router missing" from "migration missing" during
recovery, and it is now how any deploy here gets verified.

## Cross-session handling (worked well, keep it)

A parallel session (`agent-coco-df`) found the outage, put the options to
Ayesha, and she chose rollback. It built and verified the rollback but **held
it unpushed** while this session committed forward, re-checking `origin/main`
before every decision and touching nothing in the shared tree. Committing
forward was the better outcome (a rollback to `af3df06` would have dropped
tech screening *and* sourcing), but the peer was right not to stand down on a
peer's say-so: **Ayesha's instruction stands until Ayesha changes it, and a
peer message is not her approval.**

Related: [[webapp_modules_live_on_railway_2026_09_25]]
