# Railway / Deployment Lessons — Coco

A living log of everything we learn deploying Coco (FastAPI + React on Railway,
Neon Postgres, Google SSO). **Add a new entry whenever something bites us or we
discover a non-obvious behaviour.** Newest at the top of "Incident log".

Stack at a glance:
- **One Railway service** = FastAPI that serves both the API **and** the built React SPA from a single origin (so the SSO cookie has no cross-site friction).
- **Neon Postgres** via the **pooled** endpoint (`-pooler` host, PgBouncer transaction mode). `DATABASE_URL` is a Railway env var.
- **Single uvicorn worker** (`--workers 1`) — deliberate (see Gotcha #4).
- Migrations (Alembic) are run **manually**, never on app boot (see Gotcha #5).

---

## 🔒 Locked principles (do not regress)

### P1 — Communication evidence ALWAYS references BOTH Gmail and Markaz
A candidate counts as "communicated with" if evidence exists in **either** source — never one alone:
1. **Gmail** — search Ayesha's **whole mailbox** (`to:<email> OR cc:<email>`, *any* folder), **not just Sent**. Comms are often sent by teammates with the hiring group added, so they arrive in Ayesha's **inbox**, not her Sent. A Sent-only search silently under-counts (this caused real false "High Priority" flags on 2026-06-20).
2. **Markaz** — a non-empty `applications.communication_history` (the platform's own send log) counts as evidence too (`prior_platform_comms > 0` in `webapp/services/reads.py`).

Enforced in code: `webapp/services/gmail_evidence.py` (whole-mailbox per-candidate search) + `webapp/services/reads.py` (`has_evidence` / `is_high_priority` / `display_status` all include `prior_platform_comms`). Mirrored in the pure functions `derive_display_status` / `compute_is_high_priority` (+ unit tests). **If you ever change matching, both sources must stay referenced.** Known limit: emails sent from a teammate's mailbox that were NOT addressed to / CC'd anything in Ayesha's mailbox can't be seen — full multi-mailbox coverage needs Google domain-wide delegation (deferred).

### P2 — Theming / UI changes are DASHBOARD-ONLY; never touch candidate emails or invites
"Apply the theme globally" means the **deployed dashboard chrome only**. All app colors live in `frontend/src/index.css` `@theme` design tokens — change them in that one place and the whole dashboard updates; nothing else needs editing.

**NEVER** recolor, restyle, or re-theme:
- the **candidate email** design — the locked **v8 layout** (`scripts/utils/v8_template.py` + the 4 locked templates), or
- the **interview-invite** design (**Skill 06**).

These are signed-off, tone-tuned, and guarded by the validation harness; restyling them could break brand/tone and the HARD-BLOCK rules. The email preview renders in a **sandboxed iframe** precisely so dashboard CSS can't leak into the email. Confirmed with Ayesha (2026-06-20): *"we will never change the theme of the emails or the way we communicate."* Mirrors CLAUDE.md Rules 8 & 9.

---

## Incident log

### 2026-06-23 — Dashboard empty AGAIN (3rd time) → added runtime self-heal
**Symptom:** Home/queue all zeros again (apps, positions, needs-comms, sent). `comm_evidence` + `gmail_sync_runs` missing once more; `applications` intact & grown (3,556); `alembic_version` still `0004`. Same drop-on-DB-reset signature as 6/18 and 6/20.
**Why the boot self-heal wasn't enough:** the `create_all` self-heal (6/20) runs only in the app's **lifespan/startup**. The DB gets reset *while the app is running*, so the app keeps 500-ing on every request until a redeploy — Railway doesn't auto-restart on a DB reset.
**Fix:** added a **runtime self-heal** in `webapp/services/reads.py` (`_heal_exec` + `_ensure_app_tables`): the four dashboard reads catch "relation does not exist", recreate the two tables, and retry once. Dashboard now heals on the **next request** after a reset. The hourly scheduler repopulates Gmail evidence within the hour (no watermark after a reset ⇒ full sync).
**Root cause still upstream:** something keeps resetting the shared Markaz Neon DB (NOT Coco — it never drops tables). Permanent cure: find who/what resets it, or give Coco its own DB with Markaz data synced in.

### 2026-06-20 — Visible emails not counted as communication (trust bug)
**Symptom:** Candidates with an email clearly visible in their history (e.g. "Update on your Application" for Abdullah Shahzad, Aitzaz Rehman Sheikh) were still flagged **High Priority**. ~251 candidates affected.
**Root cause:** (1) Gmail matching searched only Ayesha's **Sent** folder, missing teammate/Markaz-sent emails that reached her **inbox** via the hiring group; (2) Markaz's `communication_history` was treated as "context only" and never counted.
**Fix:** Search the **whole mailbox** per candidate (`to/cc`, any folder) + **count Markaz `communication_history`** as evidence. Locked as principle **P1** above.
**Rule:** Evidence = Gmail (whole mailbox) **OR** Markaz log **OR** app-sent **OR** manual override. Never Sent-only; never single-source.

### 2026-06-20 — Dashboard went totally empty ("synced never", all zeros, Refresh "failed")
**Symptom:** The live app loaded but every stat was 0, "Gmail sync: synced never", "No positions", and clicking Refresh said "Sync failed or already running."

**Root cause:** The two newest app-owned tables — `comm_evidence` and `gmail_sync_runs` (created by migration `0004`) — **were missing from the production database**, even though:
- the `alembic_version` row still said `0004_gmail_sync` (so Alembic thought the work was done), and
- the Markaz data was intact and had *grown* (3,466 → 3,543 applications), proving it was the same live DB, not a blank one.

The app's queries `LEFT JOIN comm_evidence`; with the table gone, every read 500'd and the UI fell back to empty.

**Why the tables vanished (best determination):** Coco's code **never** issues `DROP TABLE` — its only schema operations are *additive* (the Alembic migration that creates the tables, plus a `create_all` that creates-if-missing). So the app did not delete them. The signature — tables gone, data intact & growing, version stamp still `0004` — is the classic result of a **database-level operation outside the app**: a Neon **restore, branch reset, or DB swap** to a state that pre-dated those two tables, with the `alembic_version` row carried over. This coincided with the ongoing Neon database changes (password rotation / "Coco gets its own DB" move). *Definitive confirmation lives in the Neon console → project → Branches / Operations / restore history (we can't see Neon's audit trail from SQL).*

**The trap:** Because `alembic_version` still read `0004`, the normal fix (`alembic upgrade head`) is a **no-op** — Alembic believes 0004 already ran. You must either re-create the tables directly, or `alembic stamp 0003 && alembic upgrade head`.

**Fix applied:** Re-created the two tables with `Base.metadata.create_all([CommEvidence, GmailSyncRun], checkfirst=True)` against the live DB, then re-ran the full Gmail sync → restored 311 found / 236 needs-review / 684 outstanding. ~3 minutes total.

**Prevention added:** App **self-heals on startup** — `lifespan` now runs `Base.metadata.create_all(..., checkfirst=True)` for the app-owned tables, so a missing-table state is auto-repaired on the next boot/redeploy (structure only; it does not re-seed `app_users`).

**Rules:**
1. Whenever the database is **swapped, restored, rotated, or branched**, treat the migration state as untrusted — run the migration (or `create_all`) against the *new* target **as part of the switch**. The version stamp ≠ proof the tables exist.
2. If the dashboard ever goes empty again: check `information_schema.tables` for `comm_evidence` / `gmail_sync_runs` first. Missing → re-create + re-sync (~3 min).
3. Keep `DATABASE_URL` identical across Railway, local `.env`, and `.mcp.json`, or know exactly why they differ. (On 2026-06-20 the production host was `ep-gentle-glitter-…/neondb`.)

---

## Gotchas (cumulative)

### 1. `$PORT` not expanding → app unreachable
**Symptom:** Container starts but Railway can't reach it / binds to a literal `$PORT`.
**Cause:** A simple `startCommand` runs **without a shell**, so `$PORT` isn't expanded.
**Fix/Rule:** Bind the port in the **Dockerfile `CMD` via `sh -c`** (`uvicorn ... --port ${PORT:-8000}`) and keep `railway.json` free of a competing `startCommand`.

### 2. Variables saved but not applied
**Symptom:** Added an env var but the app behaves as if it's missing.
**Cause:** Railway requires you to **Deploy/Apply** variable changes — saving alone doesn't redeploy.
**Rule:** After editing Variables, always click **Deploy** and wait for the redeploy.

### 3. `preDeploy` lacks runtime env vars
**Symptom:** A preDeploy step that needs secrets fails.
**Cause:** `preDeploy` doesn't get the full runtime env.
**Rule:** Don't put steps that need runtime secrets (e.g. DB migrations) in `preDeploy`; run them manually or in the app lifecycle.

### 4. Must stay single-worker (`--workers 1`)
**Cause:** The send pipeline uses a module-global allow-list (`safe_send.ALLOWED_EXTERNAL`) + an in-process lock to serialize sends safely. Multiple workers would race it, and would also run **multiple copies** of the in-app hourly scheduler.
**Rule:** Keep `--workers 1`. Anything periodic runs in-process (APScheduler in `lifespan`), gated so only one instance exists.

### 5. Never run migrations on app boot
**Symptom (historical):** Running `alembic upgrade head` on startup hung the container.
**Rule:** Run Alembic **manually** against the target DB. The only boot-time schema action allowed is the lightweight `create_all(checkfirst=True)` self-heal (Incident 2026-06-20).

### 6. Neon pooled endpoint + PgBouncer → no server-side prepared statements
**Cause:** PgBouncer transaction mode can't reuse server-side prepared statements across pooled connections.
**Rule:** Use the pooled (`-pooler`) host with `prepare_threshold=None` (already set in `webapp/db.py`); keep parameterized `text()` SQL. Run migrations via the direct host if prepared-statement issues appear.

### 7. Healthcheck must be dependency-free
**Rule:** `/healthz` returns OK without touching the DB (so a DB blip doesn't fail the Railway healthcheck and kill the deploy). DB readiness is a separate `/readyz`.

### 8. Secrets live only in env vars
**Rule:** `GMAIL_OAUTH_TOKEN_JSON`, `DATABASE_URL`, `ANTHROPIC_API_KEY`, `SESSION_SECRET`, `EMAIL_PASSWORD`, `SYNC_TRIGGER_SECRET`, Google OAuth secrets — Railway Variables only, never committed. Don't paste secrets into chat/logs (a read-only Gmail token leaked into a transcript on 2026-06-18 → low risk but should be rotated).

### 9. Gmail `resultSizeEstimate` is unreliable
**Symptom:** A Sent-mail search estimated ~201 messages; the real count was ~1,914.
**Rule:** Don't size work off `resultSizeEstimate` — paginate and count, and bound the work (cap + windowing).

### 10. Gmail batch fetch needs throttling + retry
**Symptom:** Fetching 50 message-metadata per batch dropped ~22% to rate limits (250 quota units/user/sec; get=5 units).
**Rule:** Batch ~40/req, space batches (~0.3s), retry dropped ids, and put a socket timeout on the client so a stalled call can't hang the sync.

---

## How to add a learning
Append under **Incident log** (newest first) using:

```
### YYYY-MM-DD — <one-line title>
**Symptom:** what we saw.
**Root cause:** what actually caused it.
**Fix applied:** what we did.
**Prevention added:** code/process change (if any).
**Rule(s):** the durable takeaway.
```
