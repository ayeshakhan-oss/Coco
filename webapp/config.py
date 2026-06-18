"""Typed application configuration, loaded from environment / .env.

Uses pydantic-settings. Secrets are NEVER hardcoded — every value comes from
the environment (Railway env vars in production, a local .env in development).

During early phases, integration-specific secrets (Google OAuth, Anthropic,
email) are Optional so the skeleton can boot and serve /healthz without them.
Each feature validates the settings it needs when it is wired up.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Runtime ---
    app_env: str = "development"

    # --- Database (Neon Postgres) — use the POOLED (-pooler) connection string ---
    database_url: Optional[str] = None

    # --- Anthropic (Claude API) — used by the AI drafting service (Phase 5) ---
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-opus-4-8"

    # --- Google Workspace SSO (Phase 3) ---
    google_oauth_client_id: Optional[str] = None
    google_oauth_client_secret: Optional[str] = None
    oauth_redirect_uri: Optional[str] = None
    allowed_domain: str = "taleemabad.com"

    # --- Session cookie signing (set a long random value in production) ---
    session_secret: str = "dev-insecure-secret-change-me-0123456789abcdef"
    session_max_age_seconds: int = 60 * 60 * 12  # 12h

    # Dev stub auto-login (NON-production only; always off in production).
    # Set AUTH_DEV_BYPASS=false to force the real Google SSO login on localhost.
    auth_dev_bypass: bool = True

    # --- Frontend origin (for CORS + post-login redirect) ---
    frontend_origin: str = "http://localhost:5173"

    # --- Outbound email (Phase 6) ---
    email_sender: str = "hiring@taleemabad.com"
    email_password: Optional[str] = None
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587

    # --- Gmail evidence sync (read-only) ---
    # The mailbox whose Sent folder is searched for comms evidence (all candidate
    # comms are sent FROM this address, so its Sent is a superset incl. hiring@).
    gmail_sync_user: str = "ayesha.khan@taleemabad.com"
    # Full authorized-user JSON (client_id/secret/refresh_token/token_uri/scopes)
    # for a one-time gmail.readonly offline-consent grant. Set as a Railway secret.
    gmail_oauth_token_json: Optional[str] = None
    # Local-dev fallback: an authorized-user token file (gitignored).
    gmail_token_file: str = ".claude/config/token_gmail.json"
    # Shared secret so the scheduler (Railway cron) can trigger a sync without a
    # session cookie, via the X-Sync-Token header.
    sync_trigger_secret: Optional[str] = None

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() in {"production", "prod"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
