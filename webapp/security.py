"""Google SSO helpers + signed session cookie.

Flow: /auth/google/login redirects to Google (auth code) -> Google redirects to
/auth/google/callback -> we exchange the code, VERIFY the ID token server-side
(signature + issuer + audience), independently assert email_verified + the
@taleemabad.com domain (the `hd` param is only a hint), upsert the app_user, and
issue a signed httpOnly session cookie (JWT). Subsequent requests are authorized
from that cookie.
"""

from __future__ import annotations

import datetime as dt
import secrets
from urllib.parse import urlencode

import httpx
import jwt

from .config import get_settings

SESSION_COOKIE = "coco_session"
STATE_COOKIE = "coco_oauth_state"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


class AuthError(Exception):
    pass


def new_state() -> str:
    return secrets.token_urlsafe(24)


def build_auth_url(state: str) -> str:
    s = get_settings()
    params = {
        "response_type": "code",
        "client_id": s.google_oauth_client_id or "",
        "redirect_uri": s.oauth_redirect_uri or "",
        "scope": "openid email profile",
        "state": state,
        "hd": s.allowed_domain,
        "access_type": "online",
        "prompt": "select_account",
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


def exchange_code(code: str) -> dict:
    s = get_settings()
    resp = httpx.post(
        GOOGLE_TOKEN_URL,
        data={
            "code": code,
            "client_id": s.google_oauth_client_id,
            "client_secret": s.google_oauth_client_secret,
            "redirect_uri": s.oauth_redirect_uri,
            "grant_type": "authorization_code",
        },
        timeout=10,
    )
    if resp.status_code != 200:
        raise AuthError(f"Token exchange failed: {resp.status_code} {resp.text}")
    return resp.json()


def verify_google_id_token(id_token_str: str) -> dict:
    """Verify signature/issuer/audience with Google, then enforce the domain.

    Imports the google transport lazily so the app imports cleanly even if the
    optional `requests` dependency is absent and SSO is unconfigured."""
    from google.auth.transport import requests as google_requests
    from google.oauth2 import id_token as google_id_token

    s = get_settings()
    info = google_id_token.verify_oauth2_token(
        id_token_str, google_requests.Request(), s.google_oauth_client_id
    )
    assert_allowed_identity(info)
    return info


def assert_allowed_identity(info: dict) -> None:
    s = get_settings()
    if not info.get("email_verified"):
        raise AuthError("Email not verified")
    email = (info.get("email") or "").lower()
    if not email.endswith("@" + s.allowed_domain.lower()):
        raise AuthError(f"Only @{s.allowed_domain} accounts are allowed")
    hd = info.get("hd")
    if hd and hd.lower() != s.allowed_domain.lower():
        raise AuthError("Account is not in the allowed Workspace domain")


def create_session_token(*, user_id: str, email: str, app_role: str,
                         first_name: str | None = None, last_name: str | None = None) -> str:
    s = get_settings()
    now = dt.datetime.now(dt.timezone.utc)
    payload = {
        "sub": user_id,
        "email": email,
        "app_role": app_role,
        "first_name": first_name,
        "last_name": last_name,
        "iat": now,
        "exp": now + dt.timedelta(seconds=s.session_max_age_seconds),
    }
    return jwt.encode(payload, s.session_secret, algorithm="HS256")


def verify_session_token(token: str) -> dict | None:
    s = get_settings()
    try:
        return jwt.decode(token, s.session_secret, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None
