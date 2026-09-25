"""System health (Skill 04, Data and Systems).

Skill 04 is infrastructure: how the database is reached, how mail is sent,
how tokens are held and what is audited. It has no candidate workflow, so
"live" for it means one page that answers whether Coco is healthy and, when it
is not, says where.

🔴 READ-ONLY. There is no write method on this router, and a test asserts it.
   A health surface that can change things is a new way to break production
   during an incident, which is the worst possible moment.

🔴 NO SECRET VALUE LEAVES THIS ROUTER. Credentials are reported as booleans
   and descriptions. A health page gets screenshotted more than any other, and
   a token in a screenshot is a token that has to be re-minted.

🔴 THE AUDIT VIEW ANSWERS "WHAT DID COCO SEND". Both halves of it: the
   candidate letters in `communications` and the invites in
   `coco.invite_sends`, which are separate tables and would otherwise each
   look like the whole picture.
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..config import get_settings
from ..db import get_db
from ..deps import get_current_user, require_editor
from ..services import system_health as health

log = logging.getLogger("webapp.routers.system")

router = APIRouter(prefix="/api/system", tags=["system"])


# Candidate letters and invites are different tables with different lifecycles.
# Unioned here so the page cannot show one and imply it is everything.
_ACTIVITY_SQL = text(
    """
    SELECT 'letter'                      AS kind,
           c.email_type                  AS what,
           trim(coalesce(cand.first_name,'') || ' ' || coalesce(cand.last_name,''))
                                         AS who,
           c.sent_at                     AS at,
           TRUE                          AS is_live
    FROM communications c
    LEFT JOIN candidates cand ON cand.id = c.candidate_id
    WHERE c.sent_at IS NOT NULL
    UNION ALL
    SELECT 'invite'                      AS kind,
           s.invite_type                 AS what,
           s.candidate_name              AS who,
           s.sent_at                     AS at,
           s.is_live                     AS is_live
    FROM coco.invite_sends s
    ORDER BY at DESC
    LIMIT :limit
    """
)

_SYNC_SQL = text(
    """
    SELECT started_at, finished_at, status, messages_scanned,
           candidates_evaluated, found_count
    FROM coco.gmail_sync_runs
    ORDER BY started_at DESC
    LIMIT 1
    """
)


@router.get("/health")
def system_health(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """What is configured, what exists, and what is known to be broken."""
    settings = get_settings()
    tables = health.table_health(db)
    integrations = health.integration_status(settings)
    return {
        "summary": health.summarise(tables, integrations),
        "tables": tables,
        "integrations": integrations,
        "known_gaps": health.KNOWN_GAPS,
    }


@router.get("/activity")
def recent_activity(
    limit: int = Query(25, ge=1, le=200),
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """Everything Coco has sent, letters and invites together.

    Editor-gated rather than open to viewers: it names candidates alongside
    what they were sent, which is the whole pipeline in one list.
    """
    items: list[dict] = []
    try:
        for row in db.execute(_ACTIVITY_SQL, {"limit": limit}).mappings().all():
            items.append({
                "kind": row["kind"],
                "what": row["what"],
                "who": row["who"],
                "at": row["at"],
                "is_live": bool(row["is_live"]),
            })
    except Exception as exc:
        # A missing invite_sends table must not blank the whole page. Say so
        # instead, and let the tables panel explain why.
        log.warning("system: activity query failed: %s", exc)
        return {"items": [], "error": (
            "Could not read the activity log. If a table is listed as missing "
            "above, that is why."
        ), "last_sync": None}

    last_sync: Optional[dict] = None
    try:
        row = db.execute(_SYNC_SQL).mappings().one_or_none()
        if row:
            last_sync = {
                "started_at": row["started_at"],
                "finished_at": row["finished_at"],
                "status": row["status"],
                "messages_scanned": row["messages_scanned"],
                "candidates_evaluated": row["candidates_evaluated"],
                "found_count": row["found_count"],
            }
    except Exception:
        last_sync = None

    return {"items": items, "error": None, "last_sync": last_sync}
