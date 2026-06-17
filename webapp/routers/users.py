"""User management (Super Admin only): the allowlist + role assignment."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..config import get_settings
from ..db import get_db
from ..deps import require_super_admin
from ..schemas import UserCreate, UserOut, UserUpdate
from ..services import users as users_svc
from ..services.users import VALID_ROLES

router = APIRouter(prefix="/api/users", tags=["users"])


def _validate_email(email: str) -> str:
    email = email.strip().lower()
    domain = get_settings().allowed_domain.lower()
    if not email.endswith("@" + domain):
        raise HTTPException(400, f"Email must be @{domain}")
    return email


def _validate_role(role: str) -> str:
    if role not in VALID_ROLES:
        raise HTTPException(400, f"Role must be one of {VALID_ROLES}")
    return role


@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _admin: dict = Depends(require_super_admin)):
    return users_svc.list_users(db)


@router.post("", response_model=UserOut, status_code=201)
def create_user(body: UserCreate, db: Session = Depends(get_db), _admin: dict = Depends(require_super_admin)):
    email = _validate_email(body.email)
    role = _validate_role(body.app_role)
    if users_svc.get_by_email(db, email):
        raise HTTPException(409, "A user with that email already exists")
    return users_svc.create_user(
        db, email=email, app_role=role, first_name=body.first_name, last_name=body.last_name
    )


@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: str,
    body: UserUpdate,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_super_admin),
):
    user = users_svc.get_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    new_role = _validate_role(body.app_role) if body.app_role is not None else None

    # Lockout protection: don't remove the last active super admin (by demotion
    # or deactivation), and don't let an admin lock themselves out.
    demoting = user.app_role == "super_admin" and new_role is not None and new_role != "super_admin"
    deactivating = body.active is False and user.active
    if (demoting or (deactivating and user.app_role == "super_admin")) and users_svc.count_active_super_admins(db) <= 1:
        raise HTTPException(400, "Cannot remove the last active super admin")
    if deactivating and user.id == admin.get("id"):
        raise HTTPException(400, "You cannot deactivate your own account")

    return users_svc.update_user(db, user, app_role=new_role, active=body.active)
