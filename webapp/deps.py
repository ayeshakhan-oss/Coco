"""Auth + role dependencies.

Roles (ascending power): viewer < editor < approver < super_admin.
- viewer:      read-only
- editor:      + generate/edit/submit drafts
- approver:    + approve & send
- super_admin: + manage users (all powers)

Login is allowlist-only: a valid session cookie maps to an app_users row; if the
user isn't found or is inactive, access is refused. (The SSO callback only issues
a session for emails already present + active — see routers/auth.py.)
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from .config import get_settings
from .db import get_db
from .security import SESSION_COOKIE, verify_session_token
from .services import users as users_svc

ROLE_LEVEL = {"viewer": 0, "editor": 1, "approver": 2, "super_admin": 3}

# Dev identity used in non-production when AUTH_DEV_BYPASS is on and there's no
# session cookie. Super admin so local dev can exercise everything.
_DEV_USER = {
    "id": "appuser-seed-jawwad",
    "email": "jawwad.ali@taleemabad.com",
    "first_name": "Jawwad",
    "last_name": "Ali",
    "app_role": "super_admin",
}


def get_current_user(request: Request, db: Session = Depends(get_db)) -> dict:
    settings = get_settings()

    token = request.cookies.get(SESSION_COOKIE)
    if token:
        claims = verify_session_token(token)
        if claims:
            user = users_svc.get_by_id(db, claims.get("sub", ""))
            if user and user.active:
                return {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "app_role": user.app_role,
                }
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session user not found or inactive")

    if not settings.is_production and settings.auth_dev_bypass:
        return dict(_DEV_USER)

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")


def _require_role(minimum: str):
    def dep(user: dict = Depends(get_current_user)) -> dict:
        if ROLE_LEVEL.get(user.get("app_role", "viewer"), 0) < ROLE_LEVEL[minimum]:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Requires {minimum} role or higher")
        return user

    return dep


require_editor = _require_role("editor")
require_approver = _require_role("approver")
require_super_admin = _require_role("super_admin")
