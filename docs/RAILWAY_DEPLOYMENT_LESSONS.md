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

## Incident log

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
