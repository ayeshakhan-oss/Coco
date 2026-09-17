"""Values-scorecard draft lifecycle: generate -> read -> edit -> submit.

`webapp/services/values_scoring.py` holds the locked, pure scoring rules (the
PASS/OUT rule and the Markaz payload shape are non-negotiable and tested
exhaustively there). This router is the only code in the app that writes to
`public.applications` -- a live Markaz hiring record -- so the submit
endpoint is the most safety-critical path in this service. Every rule below
is enforced server-side; none of them are optional and none of them may be
satisfied only by the frontend.

  1. `require_approver`, never `get_current_user`/`require_editor`, gates
     submission. Writing a values scorecard is a permanent hiring record and
     Ayesha set this gate deliberately, matching the bar for sending a
     candidate email.
  2. The payload is rebuilt from the draft's current columns with
     `build_markaz_payload` and re-validated with `validate_markaz_payload`
     immediately before the write. The stored draft row is never trusted as
     already-valid, however it got there.
  3. A draft that is already `submitted` returns 409 -- a double-click can't
     overwrite a live hiring record twice.
  4. The exact payload is logged verbatim before the write.
  5. The UPDATE targets exactly one `application_id`; the affected row count
     is asserted to be exactly 1, and the transaction is rolled back
     otherwise. A write that silently touched 0 or 2 rows fails loudly
     instead of appearing to succeed.
  6. On success `approved_by`, `approved_at`, `submitted_at`, `status`, and
     the exact `markaz_payload` sent are all recorded on the draft row, in
     the SAME transaction as the Markaz write (so a failure after the
     Markaz UPDATE but before the draft update rolls back both).
  7. There is no auto-submit path for any role -- a human calls this
     endpoint, always through the approver gate above.

`public.applications` is Markaz's table, not Coco's: the UPDATE below touches
ONLY the `values_scorecard` column of the one target row. It never inserts,
deletes, or touches any other column.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user, require_approver, require_editor
from ..models import ValuesScorecardDraft
from ..schemas import (
    ValuesScorecardEdit,
    ValuesScorecardGenerateRequest,
    ValuesScorecardOut,
)
from ..services import reads
from ..services.drafting import DraftingUnavailable
from ..services.values_scoring import (
    ValuesScorecardError,
    TranscriptTooShort,
    build_markaz_payload,
    score_transcript,
    tally,
    validate_markaz_payload,
    validate_values,
    verdict,
)

log = logging.getLogger("webapp.values_scorecards")

router = APIRouter(prefix="/api/values-scorecards", tags=["values-scorecards"])


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _draft_or_404(db: Session, draft_id: str) -> ValuesScorecardDraft:
    draft = db.get(ValuesScorecardDraft, draft_id)
    if not draft:
        raise HTTPException(404, "Values scorecard draft not found")
    return draft


def _draft_out(draft: ValuesScorecardDraft) -> dict:
    """Shape a draft row for the API. tally/verdict are always RECOMPUTED
    from the draft's current values_json rather than cached, so they can
    never drift from the ratings actually stored on the row (including after
    a PATCH edit)."""
    ratings = [v.get("rating") for v in draft.values_json]
    return {
        "id": draft.id,
        "application_id": draft.application_id,
        "candidate_name": draft.candidate_name,
        "host": draft.host,
        "transcript_sha256": draft.transcript_sha256,
        "values": draft.values_json,
        "gwc": draft.gwc,
        "final_comments": draft.final_comments,
        "proceed": draft.proceed,
        "tally": tally(ratings),
        "verdict": verdict(ratings),
        "status": draft.status,
        "model": draft.model_name,
        "created_by": draft.created_by,
        "created_at": draft.created_at,
        "approved_by": draft.approved_by,
        "approved_at": draft.approved_at,
        "submitted_at": draft.submitted_at,
        "markaz_payload": draft.markaz_payload,
    }


@router.post("/generate", response_model=ValuesScorecardOut)
def generate(
    body: ValuesScorecardGenerateRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    app_row = reads.get_application(db, body.application_id)
    if not app_row:
        raise HTTPException(404, "Application not found")

    candidate_name = " ".join(
        p for p in [app_row.get("first_name"), app_row.get("last_name")] if p
    ).strip() or "the candidate"
    role = (app_row.get("job_title") or "the role").strip()

    try:
        scored = score_transcript(
            transcript=body.transcript, candidate_name=candidate_name, role=role
        )
    except TranscriptTooShort as exc:
        raise HTTPException(422, str(exc)) from exc
    except DraftingUnavailable as exc:
        raise HTTPException(503, f"Scoring unavailable: {exc}") from exc
    except ValuesScorecardError as exc:
        # Both model attempts came back malformed -- refuse rather than
        # persist a scorecard that failed the locked shape check.
        raise HTTPException(422, f"Model returned a malformed scorecard: {exc}") from exc

    t = scored["tally"]
    final_comments = (
        f"{scored['verdict']} - {t['plus']}(+) / {t['plus_minus']}(+/-) / {t['minus']}(-)"
    )

    draft = ValuesScorecardDraft(
        application_id=body.application_id,
        candidate_name=candidate_name,
        host=body.host,
        # Only the hash is stored -- the transcript is interview content
        # about a named person and does not need a second home once scored.
        transcript_sha256=hashlib.sha256(body.transcript.encode("utf-8")).hexdigest(),
        values_json=scored["values"],
        final_comments=final_comments,
        proceed=(scored["verdict"] == "PASS"),
        gwc=scored["gwc"],
        status="draft",
        model_name=scored["model"],
        created_by=user.get("id") or "",
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return _draft_out(draft)


@router.get("/{draft_id}", response_model=ValuesScorecardOut)
def get_draft(
    draft_id: str,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    draft = _draft_or_404(db, draft_id)
    return _draft_out(draft)


@router.patch("/{draft_id}", response_model=ValuesScorecardOut)
def edit_draft(
    draft_id: str,
    body: ValuesScorecardEdit,
    db: Session = Depends(get_db),
    _user: dict = Depends(require_editor),
):
    draft = _draft_or_404(db, draft_id)
    if draft.status == "submitted":
        raise HTTPException(409, "This scorecard has already been submitted to Markaz")

    if body.values is not None:
        validate_values(body.values)  # locked shape: 6 canonical values, no blank evidence
        draft.values_json = body.values

        ratings = [v["rating"] for v in body.values]
        new_verdict = verdict(ratings)  # recomputed from the EDITED ratings, never trusted

        if new_verdict == "OUT":
            # GWC is never a back door around a failing values round.
            draft.gwc = None

        if body.proceed is None:
            draft.proceed = new_verdict == "PASS"

    if body.final_comments is not None:
        draft.final_comments = body.final_comments

    if body.proceed is not None:
        draft.proceed = body.proceed

    db.commit()
    db.refresh(draft)
    return _draft_out(draft)


@router.post("/{draft_id}/submit", response_model=ValuesScorecardOut)
def submit(
    draft_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(require_approver),
):
    draft = _draft_or_404(db, draft_id)
    if draft.status == "submitted":
        # A double-click (or a retried request) must never overwrite an
        # already-live Markaz record a second time.
        raise HTTPException(409, "This scorecard has already been submitted to Markaz")

    # Rebuild the payload from the draft's CURRENT columns and validate it
    # immediately before the write -- never trust that a stored draft is
    # already valid, however it got there.
    payload = build_markaz_payload(
        candidate_name=draft.candidate_name,
        host=draft.host,
        values=draft.values_json,
        final_comments=draft.final_comments,
        proceed=draft.proceed,
    )
    validate_markaz_payload(payload)

    log.info(
        "values_scorecard submit: draft_id=%s application_id=%s payload=%s",
        draft.id, draft.application_id, json.dumps(payload),
    )

    # public.applications is Markaz's table, not Coco's: touch ONLY the
    # values_scorecard column of the ONE target row. Never insert, delete,
    # or touch any other column.
    result = db.execute(
        text("UPDATE applications SET values_scorecard = :payload::jsonb WHERE id = :app_id"),
        {"payload": json.dumps(payload), "app_id": draft.application_id},
    )
    if result.rowcount != 1:
        db.rollback()
        raise HTTPException(
            500,
            f"Expected to update exactly 1 application row (id={draft.application_id}), "
            f"got {result.rowcount}. Rolled back; nothing was written.",
        )

    now = _utcnow()
    draft.status = "submitted"
    draft.approved_by = user.get("id")
    draft.approved_at = now
    draft.submitted_at = now
    draft.markaz_payload = payload

    db.commit()
    db.refresh(draft)
    return _draft_out(draft)
