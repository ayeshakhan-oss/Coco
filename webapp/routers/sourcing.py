"""Talent sourcing: the pool, outreach state, and the gate into Markaz.

`webapp/services/sourcing.py` holds the rules. This router is the only code
that writes them.

WHAT IS HERE AND WHAT IS NOT. The skill's 3-layer web search stays in Claude
Code, because it drives a LOCAL headless browser against a SearXNG instance
answering an anti-bot proof-of-work, and the built-in web search is
effectively blind to Pakistani LinkedIn
(memory/sourcing_fundraising_partnerships_2026_09_08.md). Everything after the
search lives here: the pool, who was contacted, who replied, and who may be
put into Markaz.

🔴 THE CORE RULE IS ENFORCED TWICE. `sourcing.may_push_to_markaz` refuses in
   the API with a reason a person can read, and
   `ck_sourced_markaz_needs_confirmed_interest` refuses in the database even
   if a bug gets past the first. "Markaz is ONLY touched after confirmed
   interest. Never speculatively."

🔴 PUSHING TO MARKAZ IS APPROVER-GATED AND REFUSES ON A POSSIBLE DUPLICATE. It
   creates a real record in somebody else's system, and Markaz already carries
   298 duplicate (candidate, job) pairs. A retroactive add must be searched by
   NAME AND PHONE, not just the email it was invited on
   (memory/MEMORY.md, "RULE -- retroactive candidate adds").
"""

from __future__ import annotations

import datetime as dt
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user, require_approver, require_editor
from ..models import SourcedCandidate
from ..schemas import (
    SourcedCandidateOut,
    SourcingOutreachUpdate,
    SourcingPushRequest,
    SourcingSummaryOut,
)
from ..services import sourcing as src

log = logging.getLogger("webapp.routers.sourcing")

router = APIRouter(prefix="/api/sourcing", tags=["sourcing"])


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _out(row: SourcedCandidate) -> SourcedCandidateOut:
    return SourcedCandidateOut(
        id=row.id,
        name=row.name,
        organization=row.organization,
        title=row.title,
        location=row.location,
        linkedin_url=row.linkedin_url,
        years=row.years,
        years_note=row.years_note,
        verification_state=row.verification_state,
        verification_note=row.verification_note,
        is_verified=src.is_verified(row.verification_state),
        tier=row.tier,
        confidence=row.confidence,
        outreach_state=row.outreach_state,
        contacted_at=row.contacted_at,
        contacted_by=row.contacted_by,
        reply_note=row.reply_note,
        markaz_application_id=row.markaz_application_id,
        job_id=row.job_id,
        role_label=row.role_label,
        source=row.source,
        notes=row.notes,
        blocked_from_markaz=src.may_push_to_markaz({
            "markaz_application_id": row.markaz_application_id,
            "outreach_state": row.outreach_state,
            "name": row.name,
        }),
    )


def _row_dict(row: SourcedCandidate) -> dict:
    return {
        "verification_state": row.verification_state,
        "outreach_state": row.outreach_state,
        "markaz_application_id": row.markaz_application_id,
        "name": row.name,
    }


@router.get("/pool", response_model=list[SourcedCandidateOut])
def pool(
    job_id: Optional[int] = Query(None),
    outreach_state: Optional[str] = Query(None),
    verification_state: Optional[str] = Query(None),
    limit: int = Query(500, ge=1, le=2000),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    # Validate BEFORE touching the database: a bad filter is a bad request
    # whatever the database is doing, and a 400 should not depend on a query
    # succeeding first.
    if outreach_state and outreach_state not in src.OUTREACH_STATES:
        raise HTTPException(
            400,
            f"unknown outreach state {outreach_state!r}; must be one of "
            f"{list(src.OUTREACH_STATES)}",
        )
    if verification_state and verification_state not in src.VERIFICATION_STATES:
        raise HTTPException(
            400,
            f"unknown verification state {verification_state!r}; must be one of "
            f"{list(src.VERIFICATION_STATES)}",
        )

    q = db.query(SourcedCandidate)
    if job_id is not None:
        q = q.filter(SourcedCandidate.job_id == job_id)
    if outreach_state:
        q = q.filter(SourcedCandidate.outreach_state == outreach_state)
    if verification_state:
        q = q.filter(SourcedCandidate.verification_state == verification_state)
    rows = q.order_by(SourcedCandidate.name).limit(limit).all()
    return [_out(r) for r in rows]


@router.get("/summary", response_model=SourcingSummaryOut)
def summary(
    job_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    q = db.query(SourcedCandidate)
    if job_id is not None:
        q = q.filter(SourcedCandidate.job_id == job_id)
    rows = [_row_dict(r) for r in q.all()]
    return SourcingSummaryOut(**src.summarise(rows))


@router.patch("/{sourced_id}", response_model=SourcedCandidateOut)
def update_outreach(
    sourced_id: str,
    body: SourcingOutreachUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """Record what happened: contacted, replied, not interested.

    Recording a reply is an EDIT. Putting somebody into Markaz on the back of
    it is a decision, and needs an approver.
    """
    row = db.get(SourcedCandidate, sourced_id)
    if not row:
        raise HTTPException(404, "Sourced candidate not found")

    if body.outreach_state is not None:
        if body.outreach_state not in src.OUTREACH_STATES:
            raise HTTPException(
                400,
                f"unknown outreach state {body.outreach_state!r}; must be one of "
                f"{list(src.OUTREACH_STATES)}",
            )
        # Moving somebody OFF "interested" while they sit in Markaz would
        # break the database constraint, so say why rather than 500.
        if row.markaz_application_id and body.outreach_state != src.INTERESTED:
            raise HTTPException(
                409,
                f"{row.name} is already in Markaz as application "
                f"{row.markaz_application_id}, so their outreach state cannot be "
                "moved away from confirmed interest. Remove them from Markaz first.",
            )
        row.outreach_state = body.outreach_state
        if body.outreach_state == src.CONTACTED and not row.contacted_at:
            row.contacted_at = _utcnow()
            row.contacted_by = user.get("id") or ""

    if body.reply_note is not None:
        row.reply_note = body.reply_note.strip() or None
    if body.notes is not None:
        row.notes = body.notes.strip() or None
    row.updated_at = _utcnow()

    db.commit()
    db.refresh(row)
    return _out(row)


# Somebody already in Markaz under any of the identifiers we hold. Searched by
# NAME as well as email, because an invitee may exist under an older address
# (memory: "RULE -- retroactive candidate adds").
_EXISTING_SQL = text(
    """
    SELECT c.id AS candidate_id, c.first_name, c.last_name, c.email,
           a.id AS application_id, a.job_id
    FROM candidates c
    LEFT JOIN applications a ON a.candidate_id = c.id
    WHERE (:email <> '' AND lower(c.email) = lower(:email))
       OR lower(trim(coalesce(c.first_name,'') || ' ' || coalesce(c.last_name,'')))
          = lower(trim(:name))
    LIMIT 25
    """
)


@router.post("/{sourced_id}/push-to-markaz", response_model=SourcedCandidateOut)
def push_to_markaz(
    sourced_id: str,
    body: SourcingPushRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_approver),
):
    """Record that a sourced person has entered Markaz.

    Gated on confirmed interest, twice over. This records the LINK to an
    existing Markaz application rather than creating candidate and application
    rows itself: Markaz already carries 298 duplicate (candidate, job) pairs,
    and adding another from here -- usually without an email address -- would
    make that worse in somebody else's system. The person is created in Markaz
    by hand, and their application id recorded here so the sourcing pool knows
    they have moved on.
    """
    row = db.get(SourcedCandidate, sourced_id)
    if not row:
        raise HTTPException(404, "Sourced candidate not found")

    blocked = src.may_push_to_markaz(_row_dict(row))
    if blocked:
        raise HTTPException(409, f"Cannot put {row.name} into Markaz: {blocked}")

    exists = db.execute(
        _EXISTING_SQL, {"email": (body.email or "").strip(), "name": row.name}
    ).mappings().all()
    match = next((e for e in exists if e["application_id"] == body.application_id), None)
    if match is None:
        near = ", ".join(
            f"{e['first_name']} {e['last_name']} (application {e['application_id']})"
            for e in exists[:5]
        )
        raise HTTPException(
            404,
            f"Application {body.application_id} is not a Markaz record for "
            f"{row.name}. "
            + (f"Records that do look like them: {near}." if near
               else "Nothing in Markaz matches that name or email yet, so create "
                    "them there first."),
        )

    row.markaz_application_id = body.application_id
    row.pushed_at = _utcnow()
    row.pushed_by = user.get("id") or ""
    row.updated_at = _utcnow()
    db.commit()
    db.refresh(row)
    log.info(
        "sourcing: %s linked to Markaz application %s by %s",
        row.name, body.application_id, user.get("email"),
    )
    return _out(row)
