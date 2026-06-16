"""app_users lookups + upsert from a verified Google identity."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import AppUser


def get_by_id(db: Session, user_id: str) -> Optional[AppUser]:
    return db.get(AppUser, user_id)


def get_by_email(db: Session, email: str) -> Optional[AppUser]:
    return db.execute(
        select(AppUser).where(AppUser.email == email.lower())
    ).scalar_one_or_none()


def upsert_from_google(
    db: Session,
    *,
    google_sub: str,
    email: str,
    first_name: Optional[str],
    last_name: Optional[str],
) -> AppUser:
    """Match by email so seeded approvers keep their role. New emails become
    drafters. Never downgrades an existing role."""
    email = email.lower()
    user = get_by_email(db, email)
    now = dt.datetime.now(dt.timezone.utc)
    if user is None:
        user = AppUser(
            email=email,
            google_sub=google_sub,
            first_name=first_name,
            last_name=last_name,
            app_role="drafter",
            active=True,
            last_login_at=now,
        )
        db.add(user)
    else:
        user.google_sub = google_sub or user.google_sub
        if not user.first_name and first_name:
            user.first_name = first_name
        if not user.last_name and last_name:
            user.last_name = last_name
        user.last_login_at = now
    db.commit()
    db.refresh(user)
    return user
