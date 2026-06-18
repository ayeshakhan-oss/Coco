"""FastAPI application entrypoint.

Run locally:
    uvicorn webapp.main:app --reload --port 8000
"""

from __future__ import annotations

import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .db import check_db
from .deps import get_current_user
from .routers import auth as auth_router
from .routers import candidates as candidates_router
from .routers import communications as communications_router
from .routers import gmail_sync as gmail_sync_router
from .routers import users as users_router
from .schemas import CurrentUserOut

settings = get_settings()

app = FastAPI(
    title="Coco — Candidate Communication",
    version="0.1.0",
    description="Team tool for drafting, reviewing, approving and sending "
    "evidence-based candidate-communication emails.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz", tags=["health"])
def healthz() -> dict:
    """Liveness probe — no external dependencies (used by Railway healthcheck)."""
    return {"status": "ok", "service": "coco-backend", "env": settings.app_env}


@app.get("/readyz", tags=["health"])
def readyz() -> dict:
    """Readiness probe — verifies the database is reachable."""
    db_ok = check_db()
    return {"status": "ok" if db_ok else "degraded", "database": db_ok}


@app.get("/api/me", response_model=CurrentUserOut, tags=["auth"])
def me(user: dict = Depends(get_current_user)) -> dict:
    """The signed-in user + role (drives the frontend's RoleGate).

    Until SSO is wired (Phase 3) this returns the dev user outside production.
    """
    return user


app.include_router(auth_router.router)
app.include_router(candidates_router.router)
app.include_router(communications_router.router)
app.include_router(communications_router.asset_router)
app.include_router(gmail_sync_router.router)
app.include_router(users_router.router)

# --- Serve the built React SPA (single-service deploy) ---
# In production the frontend is built to frontend/dist and served from the same
# origin as the API (so the SSO httpOnly cookie has no cross-site friction).
# Mounted last so all /api, /healthz, /docs routes above take precedence.
_DIST = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
_RESERVED = {"healthz", "readyz", "openapi.json", "docs", "redoc"}

if os.path.isdir(_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(_DIST, "assets")), name="spa-assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa_fallback(full_path: str):
        # Never let the SPA shadow the API or health/docs routes.
        if full_path.startswith(("api/", "auth/")) or full_path in _RESERVED:
            raise HTTPException(status_code=404, detail="Not found")
        candidate = os.path.join(_DIST, full_path)
        if full_path and os.path.isfile(candidate):
            return FileResponse(candidate)
        return FileResponse(os.path.join(_DIST, "index.html"))

