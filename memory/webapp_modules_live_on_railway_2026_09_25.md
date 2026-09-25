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
