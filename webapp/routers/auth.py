"""Google SSO endpoints."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

from ..config import get_settings
from ..db import get_db
from ..security import (
    SESSION_COOKIE,
    STATE_COOKIE,
    AuthError,
    build_auth_url,
    create_session_token,
    exchange_code,
    new_state,
    verify_google_id_token,
)
from ..services import users as users_svc

log = logging.getLogger("webapp.auth")
router = APIRouter(prefix="/auth", tags=["auth"])


def _login_url(error: str | None = None) -> str:
    base = get_settings().frontend_origin.rstrip("/")
    target = f"{base}/login" if base not in ("", "/") else "/login"
    return f"{target}?error={error}" if error else target


def _home_url() -> str:
    base = get_settings().frontend_origin.rstrip("/")
    return base or "/"


@router.get("/google/login")
def google_login():
    settings = get_settings()
    if not settings.google_oauth_client_id:
        return RedirectResponse(_login_url("sso_not_configured"))
    state = new_state()
    resp = RedirectResponse(build_auth_url(state))
    resp.set_cookie(
        STATE_COOKIE, state, max_age=300, httponly=True,
        secure=settings.is_production, samesite="lax", path="/",
    )
    return resp


@router.get("/google/callback")
def google_callback(
    request: Request,
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db),
):
    settings = get_settings()
    if request.cookies.get(STATE_COOKIE) != state:
        return RedirectResponse(_login_url("bad_state"))

    try:
        token_resp = exchange_code(code)
        id_token_str = token_resp.get("id_token")
        if not id_token_str:
            raise AuthError("No id_token in token response")
        info = verify_google_id_token(id_token_str)
    except AuthError as e:
        log.warning("SSO denied: %s", e)
        return RedirectResponse(_login_url("denied"))
    except Exception as e:  # network / google errors
        log.error("SSO callback error: %s", e)
        return RedirectResponse(_login_url("error"))

    # ALLOWLIST: only a pre-added, active user may log in.
    user = users_svc.resolve_login(
        db,
        google_sub=info.get("sub", ""),
        email=info["email"],
        first_name=info.get("given_name"),
        last_name=info.get("family_name"),
    )
    if user is None:
        log.warning("SSO login denied (not on allowlist): %s", info.get("email"))
        return RedirectResponse(_login_url("not_authorized"))
    session = create_session_token(
        user_id=user.id, email=user.email, app_role=user.app_role,
        first_name=user.first_name, last_name=user.last_name,
    )
    resp = RedirectResponse(_home_url())
    resp.set_cookie(
        SESSION_COOKIE, session, max_age=settings.session_max_age_seconds,
        httponly=True, secure=settings.is_production, samesite="lax", path="/",
    )
    resp.delete_cookie(STATE_COOKIE, path="/")
    return resp


@router.post("/logout")
def logout():
    resp = Response(status_code=204)
    resp.delete_cookie(SESSION_COOKIE, path="/")
    return resp


@router.get("/logout")
def logout_redirect():
    # Convenience for a plain <a href> sign-out link: clear the cookie + bounce
    # back to the login page.
    resp = RedirectResponse(_login_url())
    resp.delete_cookie(SESSION_COOKIE, path="/")
    return resp
