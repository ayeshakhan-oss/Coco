"""Gmail evidence + manual-override endpoints.

- Sync status (last run + 'last synced' time) for the dashboard.
- Per-candidate Gmail match (drives the 'View Gmail match' modal).
- Manual "mark sent" (approver) — a human attests a comm was sent outside Coco.
- Reversible "ignore" (editor) — for shortlisted-but-never-scheduled candidates.

The refresh/sync trigger lives in the Phase-3 Gmail service and is registered
here when that module is present.
"""

from __future__ import annotations

import datetime as dt
import secrets
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..config import get_settings
from ..db import get_db
from ..deps import ROLE_LEVEL, get_current_user, require_approver, require_editor
from ..schemas import (
    BulkIgnoreRequest,
    BulkMarkSentRequest,
    BulkResult,
    GmailMatch,
    GmailSyncStatusOut,
    IgnoreRequest,
    MarkSentRequest,
    TimelineItem,
)
from ..services import evidence

router = APIRouter(prefix="/api", tags=["gmail-sync"])


@router.get("/gmail-sync/status", response_model=GmailSyncStatusOut)
def gmail_sync_status(
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return evidence.get_sync_status(db)


def _authorize_sync(request: Request, db: Session, x_sync_token: Optional[str]) -> tuple[str, Optional[str]]:
    """Allow either the cron shared-secret header OR an editor+ session.
    Returns (trigger, triggered_by)."""
    settings = get_settings()
    if x_sync_token and settings.sync_trigger_secret and secrets.compare_digest(
        x_sync_token, settings.sync_trigger_secret
    ):
        return "scheduled", None
    user = get_current_user(request, db)
    if ROLE_LEVEL.get(user.get("app_role", "viewer"), 0) < ROLE_LEVEL["editor"]:
        raise HTTPException(403, "Requires editor role or higher")
    return "manual", user["id"]


@router.post("/gmail-sync/refresh", response_model=GmailSyncStatusOut)
def gmail_sync_refresh(
    request: Request,
    full: bool = Query(False),
    x_sync_token: Optional[str] = Header(None, alias="X-Sync-Token"),
    db: Session = Depends(get_db),
):
    trigger, triggered_by = _authorize_sync(request, db, x_sync_token)

    # Concurrency guard: refuse if a sync started in the last 15 minutes is still running.
    busy = db.execute(
        text(
            "SELECT 1 FROM gmail_sync_runs WHERE status='running' "
            "AND started_at > now() - interval '15 minutes' LIMIT 1"
        )
    ).first()
    if busy:
        raise HTTPException(409, "A Gmail sync is already running. Try again shortly.")

    # Lazy import so the app boots even if Google libs aren't present.
    from ..services import gmail_evidence

    gmail_evidence.run_sync(db, full=full, trigger=trigger, triggered_by=triggered_by)
    return evidence.get_sync_status(db)


# NOTE: bulk routes MUST be declared before the /candidates/{application_id}/...
# routes, or FastAPI captures the literal "bulk" segment as application_id (422).
@router.post("/candidates/bulk/mark-sent", response_model=BulkResult)
def bulk_mark_sent(
    body: BulkMarkSentRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_approver),
):
    n = evidence.bulk_mark_sent(db, body.application_ids, user["id"], body.reason)
    return {"updated": n}


@router.post("/candidates/bulk/ignore", response_model=BulkResult)
def bulk_ignore(
    body: BulkIgnoreRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    n = evidence.bulk_set_ignore(db, body.application_ids, user["id"], body.ignored)
    return {"updated": n}


@router.get("/candidates/{application_id}/gmail-match", response_model=GmailMatch)
def gmail_match(
    application_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return evidence.get_match(db, application_id)


@router.get("/candidates/{application_id}/timeline", response_model=list[TimelineItem])
def candidate_timeline(
    application_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    items = evidence.build_timeline(db, application_id)
    if items is None:
        raise HTTPException(404, "Application not found")
    return items


@router.post("/candidates/{application_id}/mark-sent", response_model=GmailMatch)
def mark_sent(
    application_id: int,
    body: MarkSentRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_approver),
):
    ok = evidence.mark_sent(db, application_id, user["id"], body.reason)
    if not ok:
        raise HTTPException(404, "Application not found")
    return evidence.get_match(db, application_id)


@router.delete("/candidates/{application_id}/mark-sent", response_model=GmailMatch)
def clear_mark_sent(
    application_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(require_approver),
):
    evidence.clear_mark(db, application_id)
    return evidence.get_match(db, application_id)


@router.post("/candidates/{application_id}/ignore", response_model=GmailMatch)
def set_ignore(
    application_id: int,
    body: IgnoreRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    ok = evidence.set_ignore(db, application_id, user["id"], body.ignored)
    if not ok:
        raise HTTPException(404, "Application not found")
    return evidence.get_match(db, application_id)
