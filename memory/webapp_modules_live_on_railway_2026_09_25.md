---
name: All six webapp modules are live on Railway (Skills 06 and 04 shipped)
description: 2026-09-25. Candidate Invites (Skill 06) and Data & Systems (Skill 04) went live, completing all six modules. Booking links are now proved by fetching the page title; duplicate live invites are a database constraint.
metadata:
  type: project
---

# All six modules live (2026-09-25)

`frontend/src/lib/modules.ts` — every module now `status: 'live'`:

| Module | Route | Skill |
|---|---|---|
| Candidate Communication | `/queue` | 01 |
| Candidate Evaluation | `/evaluations` | 02 |
| Hiring Operations | `/attendance` | 03 |
| **Data & Systems** | `/system` | **04 (new)** |
| Talent Sourcing | `/sourcing` | 05 |
| **Candidate Invites** | `/invites` | **06 (new)** |

Verified live on `2377ecc8`: every router probes **401** (mounted and gated),
none 404 or 500.

---

## Skill 06 — Candidate Invites

`webapp/services/invites.py` (rules) · `invite_render.py` (locked design) ·
`webapp/routers/invites.py` · `sending.send_invite` · `SourcingPage`-style
page at `frontend/src/pages/InvitesPage.tsx`. Tables `coco.invite_links` and
`coco.invite_sends` (alembic `0017_candidate_invites`, applied and stamped).

**The design is a PORT, not a new one** — taken from the locked template as
actually built in `scripts/jobs/job39/send_growth_manager_invites_batch.py`.
Eight design tokens are asserted in tests so a redesign cannot arrive by
accident.

### 🔴 A booking link is now PROVED, not trusted

The Rule 24 trap made mechanical. `coco.invite_links` stores each URL with
`verified_title` — the page title a fetch **actually returned** — plus
`verified_at` and an `expected_title` to compare against. **A live send
refuses while `verified_title` is null**, and editing the URL discards the old
proof, because a verification belongs to the link that was fetched, not to the
row. A job-specific row beats the type-level default, which is how Job 39
Lahore and Job 41 Karachi keep separate schedules.

### 🔴 The four gates, each proved against an invite built to break it

1. **A pilot goes to Ayesha alone.** `recipients_for` builds a pilot's list
   from nothing rather than filtering the live one, so a CC cannot survive by
   being forgotten (Rule 4).
2. **`[PILOT` in a live subject is refused** (Rule 7). Its *absence* in a
   pilot is not an error, because a threaded pilot must not carry it.
3. **An unverified booking link blocks a live send** (Rule 24).
4. **Keep-in-Touch and Assessment Center carry no booking button**, and the
   renderer *refuses* one rather than dropping it silently. The Interview
   Reminder never invents a Meet link: without a verified one it points at the
   calendar invitation instead of shipping a button that could strand someone.

### 🔴 Duplicate sends are a database constraint

`uq_invite_sends_live_once` — one live invite of one type per application,
partial index so pilots are excluded. This is the 2026-08-24 batch discipline
(scan Sent Mail before and after, because a send loop reports what it TRIED)
enforced instead of remembered. **The log row is flushed BEFORE the email
leaves**, so a duplicate is refused while nothing has been sent; a failed send
rolls back rather than reading later as a send that happened.

### 🔴 `evaluate_email` is deliberately NOT run on invites

It validates 800-word decision letters and would HARD_BLOCK every 200-word
invite for failing rules never written for this kind of email. Invites go
through their own gate, in the router and again inside `send_invite`.

A missing field **refuses the render** rather than emitting a placeholder, and
every operator field is HTML-escaped.

⚠️ **UNRESOLVED, for Ayesha:** the locked shell carries `width="775"` on the
card, which **Rule 16 forbids** (a phone zooms out instead of reflowing). Rule
16 is from August; this design was locked in May. Changing a locked
candidate-facing design is her call, so the port is faithful and the conflict
is flagged, not quietly resolved.

⚠️ **Nothing has been sent through it yet.** A pilot to Ayesha is the real
test, and `coco.invite_links` is empty until booking links are configured.

---

## Skill 04 — Data & Systems

`webapp/services/system_health.py` · `webapp/routers/system.py` ·
`frontend/src/pages/SystemPage.tsx`. Two GETs, **no write method**, asserted.

Skill 04 is infrastructure, not a candidate workflow, so "live" means a page
that answers *is Coco healthy, and if not, where*: every `coco` table with
row counts and an explicit **missing** (Markaz's Replit push has dropped them
before), which integrations are configured, and everything Coco has sent
(letters *and* invites — separate tables, either alone looks complete).

🔴 **Known gaps are listed, not hidden, and the count shows even when green** —
inert Layer 3 hook, dead Calendar OAuth, migrations not run on deploy. A page
that only ever shows green teaches people the absence of an alarm means
everything works.

🔴 **No secret value leaves the router.** Tested by feeding it settings full of
recognisable fake secrets and asserting none appear, plus the other half: that
it still reports what is configured. `"configured"` means *the app could use
it*, never *it works* — a token can be present and expired.

🔑 **`inspect.getsource` lies under pytest here.** The completeness test ties
`COCO_TABLES` to what `ensure_app_tables` creates, but `conftest`'s DDL guard
**patches** `ensure_app_tables`, so `getsource` returned the wrapper and the
test silently compared against nothing. It reads `db.py` from disk instead.

---

## Counts

842 offline tests pass; the 27 network-bound SQL-execution probes pass.
🔑 **Three test files hit Neon over HTTPS and take ~35s per statement**
(`test_router_sql_executes`, `test_screening_runs_sql`, `test_evaluations_api`)
— ignore them for a fast loop, run them before shipping router SQL.

Related: [[lesson_untracked_module_outage_2026_09_25]]

---

## The sub-skills were NOT live, only the module titles were (same day)

Ayesha, looking at the skills tree in her editor: *"you have to ensure that all
these sub skills of the main skills are made live on Railway. I don't want you
to just make the main skill live over there as a title and not make the sub
skills live."* She was right, and it was worse than a UI gap.

### 🔴 The image copied 2 of the 7 skill folders

`Dockerfile` carried only `01_candidate-communication` and
`02_candidate-evaluation`. **29 of the 46 sub-skill files did not exist on
Railway at all** — everything in `03_operations`, `04_data-and-systems`,
`05_talent-sourcing`, `06_candidate-invites` and `07_contract-drafting`.

Several of those files are named **SOURCE OF TRUTH** in the docstring of the
service that implements them (`attendance.py`, `decision_brief.py`,
`hiring_funnel.py`, `invites.py`, `sourcing.py`), so the citation pointed at a
file the server did not have. Six module tiles read "live" while most of the
method behind them was absent.

**Nothing caught it because the app never asked for those files at runtime, so
nothing failed. Absence is silent unless something counts it.**

### The fix

- All seven folders ship. `ui-ux-pro-max` is the deliberate exception:
  vendored third-party design guidance, and Rule 9 bars it from the locked
  candidate layouts.
- `webapp/services/skills.py` **walks** the directory instead of holding a
  list, because a hardcoded inventory drifts the moment somebody adds a file,
  which is the failure being fixed.
- `GET /api/skills` + a `/skills` page: every sub-skill listed, readable in
  place, each with an honest status.

### 🔒 Status is per file, and "live" is not one word

**21 wired** (a page here does the work, and the route is carried) ·
**20 reference** (the guidance ships and is readable; Claude Code follows it) ·
**5 Claude-Code-only**, each with its reason recorded in `NOT_ON_SERVER`.
Marking all 46 as features would be the same overclaim in a new place.

### 🔑 `/healthz` now answers "did the method ship?"

`{"skills": 7, "sub_skills": 46}`, verified live on `98eaf320`. **A route probe
proves a router mounted and says nothing about the files behind it** — that is
precisely how this went unnoticed. Counts only: the endpoint is
unauthenticated and skill files carry internal hiring method. A zero is the
alarm, so the helper swallows everything rather than throwing.

### Still open, deliberately

- **Skill 07 (12 files) has no page at all.** Contract drafting reads the
  approved masters in `Contracts\`, which is gitignored and cannot ship, so
  it is reference-only until Ayesha decides otherwise.
- **Letter types 05, 06 and 07 are not webapp draft types** — `EMAIL_TYPES`
  holds five. They are Claude Code scripts.
- `03_operations/meeting-notes-tracker-sheet.md` and
  `hiring-pipeline-weekly-report.md` stay off the server by her own earlier
  decisions.

🔑 **No Docker on this machine**, so the image cannot be built locally. The
`.dockerignore` mechanism is proven instead by 01/02 already working in
production and by the build failing loudly on a missing re-include
(`failed to compute cache key`), plus the healthz counts measured after deploy.
