# Deploying Coco to Railway

Single Railway service: a Docker image where **FastAPI serves both the API and
the built React SPA** from one origin (so the SSO cookie has no cross-site
friction). Database is Neon Postgres.

## Architecture

```
Railway service (Dockerfile)
  ├─ stage 1: node builds frontend/ -> frontend/dist
  └─ stage 2: python runs uvicorn webapp.main:app
        ├─ /api/*, /healthz, /readyz, /docs   -> FastAPI
        └─ everything else                    -> React SPA (frontend/dist)
  preDeploy: alembic upgrade head    (against DATABASE_URL)
  healthcheck: /healthz
Neon Postgres  <- DATABASE_URL (pooled -pooler endpoint)
```

## Before you deploy

1. **Phase 0 (security) before making the repo public.** Rotate the Neon
   password and scrub git history (the old password is in 84 files + history).
   The image itself only copies the clean `scripts/` modules, and all secrets
   come from Railway env vars — but the *repo* must be cleaned before it is
   public.
2. Have the **rotated, pooled** Neon connection string ready.

## Steps

1. Create a Railway project and add a service from this repo (or `railway up`
   from the repo root). Railway auto-detects `Dockerfile` / `railway.json`.
2. Set the environment variables below in the Railway service.
3. Deploy. `preDeployCommand` runs `alembic upgrade head` (creates app_users +
   communications if a fresh DB); the service starts uvicorn; Railway probes
   `/healthz`.
4. Open the service URL.

## Environment variables

| Var | Required | Notes |
|-----|----------|-------|
| `DATABASE_URL` | yes | Neon **pooled** (`-pooler`) URL, rotated. |
| `APP_ENV` | yes | `production` once SSO is wired. See auth note below. |
| `SESSION_SECRET` | yes | Long random string (session cookie signing). |
| `ANTHROPIC_API_KEY` | for drafting | Anthropic **Console** key (the Claude.ai subscription token can't power a backend). Without it the drafter falls back to the stub. |
| `ANTHROPIC_MODEL` | no | Defaults to `claude-opus-4-8`. |
| `GOOGLE_OAUTH_CLIENT_ID` / `GOOGLE_OAUTH_CLIENT_SECRET` | for SSO | From Google Cloud (Phase 3). |
| `OAUTH_REDIRECT_URI` | for SSO | `https://<your-railway-domain>/auth/google/callback`. |
| `ALLOWED_DOMAIN` | no | Defaults to `taleemabad.com`. |
| `FRONTEND_ORIGIN` | no | Single-service deploy = same origin; set to the Railway URL. |
| `EMAIL_SENDER` | for sending | `hiring@taleemabad.com`. |
| `EMAIL_PASSWORD` | for sending | Gmail app password. Without it, send endpoints return 503 (drafting/preview still work). |

## ⚠️ Auth note (read before exposing the URL)

The app's auth is a **dev stub until SSO (Phase 3) lands**:
- `APP_ENV=production` ⇒ every API call returns **401** (the stub refuses) — the
  app is locked until real SSO is wired. Deploy this way only once SSO exists.
- Any other `APP_ENV` (e.g. `staging`) ⇒ the **dev stub** treats every visitor
  as an approver. Use this only behind a private/obscure URL while setting up,
  and **wire SSO before any real candidate data is acted on.**

Recommended order: deploy as `staging` to confirm infra (build, DB, health),
then complete Phase 3 (SSO) and flip to `production`.

## Notes

- **Single uvicorn worker** is intentional: the send pipeline serializes on an
  in-process lock (`safe_send.ALLOWED_EXTERNAL` is a process-global set). Scale
  with replicas only after that is made per-request.
- `logs/` is ephemeral on Railway; the `communications` table is the durable
  audit, not the log file.
- Migrations use `DATABASE_URL`; if PgBouncer prepared-statement errors appear,
  point `preDeployCommand` at the Neon **direct** (non-pooled) host.
