"""app_users: allowlist login + user-management CRUD."""

from __future__ import annotations

import datetime as dt
from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import APP_ROLES, AppUser

VALID_ROLES = ("viewer", "editor", "approver", "super_admin")


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def get_by_id(db: Session, user_id: str) -> Optional[AppUser]:
    return db.get(AppUser, user_id)


def get_by_email(db: Session, email: str) -> Optional[AppUser]:
    return db.execute(
        select(AppUser).where(AppUser.email == email.lower())
    ).scalar_one_or_none()


def resolve_login(db: Session, *, google_sub: str, email: str,
                  first_name: Optional[str], last_name: Optional[str]) -> Optional[AppUser]:
    """ALLOWLIST: only an existing, active user may log in. Returns None to deny
    (caller rejects). Updates google_sub + last_login on success. Never creates."""
    user = get_by_email(db, email)
    if user is None or not user.active:
        return None
    user.google_sub = google_sub or user.google_sub
    if not user.first_name and first_name:
        user.first_name = first_name
    if not user.last_name and last_name:
        user.last_name = last_name
    user.last_login_at = _utcnow()
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session) -> list[AppUser]:
    return list(db.execute(select(AppUser).order_by(AppUser.email)).scalars().all())


def create_user(db: Session, *, email: str, app_role: str,
                first_name: Optional[str] = None, last_name: Optional[str] = None) -> AppUser:
    user = AppUser(
        id="appuser-" + uuid4().hex,
        email=email.lower(),
        app_role=app_role,
        first_name=first_name,
        last_name=last_name,
        active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: AppUser, *, app_role: Optional[str] = None,
                active: Optional[bool] = None) -> AppUser:
    if app_role is not None:
        user.app_role = app_role
    if active is not None:
        user.active = active
    db.commit()
    db.refresh(user)
    return user


def count_active_super_admins(db: Session) -> int:
    return len(
        db.execute(
            select(AppUser).where(AppUser.app_role == "super_admin", AppUser.active.is_(True))
        ).scalars().all()
    )
