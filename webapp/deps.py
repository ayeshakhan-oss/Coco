"""Auth dependencies.

Authorization order:
1. A valid `coco_session` cookie -> load the live app_users row (role + active
   are honored on every request).
2. No/invalid cookie + NON-production -> dev stub user (lets staging + local dev
   work before/without a login).
3. No/invalid cookie + production -> 401.
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from .config import get_settings
from .db import get_db
from .security import SESSION_COOKIE, verify_session_token
from .services import users as users_svc

# Dev identity used in non-production when there is no session cookie.
_DEV_USER = {
    "id": "appuser-seed-jawwad",
    "email": "jawwad.ali@taleemabad.com",
    "first_name": "Jawwad",
    "last_name": "Ali",
    "app_role": "approver",
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


def require_approver(user: dict = Depends(get_current_user)) -> dict:
    if user.get("app_role") != "approver":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Approver role required")
    return user
