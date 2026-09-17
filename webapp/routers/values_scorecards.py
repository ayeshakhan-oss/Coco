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
     candidate email. `GET` is gated on `require_editor` too (never a bare
     signed-in `viewer`) -- a draft carries the candidate's name plus
     verbatim interview evidence.
  2. The status transition IS the double-submit guard: `status='draft' ->
     'submitted'` is flipped with a single conditional UPDATE
     (`WHERE status='draft'`) before anything else happens, and `rowcount`
     is asserted to be exactly 1. Two concurrent submits (a double-click is
     two requests) can never both pass -- whichever request's UPDATE
     actually flips the row is the only one allowed to build and write the
     Markaz payload; an interleaved second request's UPDATE matches zero
     rows (Postgres re-evaluates the WHERE clause against the committed row
     after any blocking row lock releases) and 409s, never silently
     overwriting.
  3. The payload is rebuilt from the draft's current columns with
     `build_markaz_payload` and re-validated with `validate_markaz_payload`
     immediately before the write. The stored draft row is never trusted as
     already-valid, however it got there. `proceed` and the verdict/tally
     prefix of `final_comments` are re-derived from the draft's CURRENT
     ratings at this point too, never taken as-is from the row -- see
     `edit_draft` for why both can otherwise drift.
  4. Before the write, the CURRENT `public.applications` row for the target
     `application_id` is read (`FOR UPDATE`, same transaction). If
     `values_scorecard` is already populated, the submit refuses (409)
     unless the caller explicitly passes `overwrite=True`; on an explicit
     overwrite, the prior value is preserved on the draft row
     (`replaced_payload`) rather than being silently destroyed.
  5. Before the write, the target application is checked against every
     `public.applications` row sharing its `(candidate_id, job_id)`: if a
     NEWER application exists for the same pair, the submit refuses (409)
     naming the newer id rather than writing to a stale duplicate (Markaz's
     UI displays the most recently updated record of a pair, so writing to
     an older one appears to silently fail). Skipped when either id is
     null.
  6. The exact payload is logged verbatim before the write.
  7. The UPDATE targets exactly one `application_id`; the affected row count
     is asserted to be exactly 1, and the transaction is rolled back
     otherwise. A write that silently touched 0 or 2 rows fails loudly
     instead of appearing to succeed.
  8. On success `approved_by` (id + email, for a readable audit trail),
     `approved_at`, `submitted_at`, `status`, `proceed`, `final_comments`,
     and the exact `markaz_payload` sent (plus `replaced_payload` on an
     overwrite) are all recorded on the draft row, in the SAME transaction
     as the Markaz write and the status-flip UPDATE (so a failure at any
     point rolls back all of it).
  9. There is no auto-submit path for any role -- a human calls this
     endpoint, always through the approver gate above.

`public.applications` is Markaz's table, not Coco's -- referenced everywhere
as `public.applications` (not the bare, `search_path`-dependent name): the
UPDATE below touches ONLY the `values_scorecard` column of the one target
row. It never inserts, deletes, or touches any other column.
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
from ..deps import require_approver, require_editor
from ..models import ValuesScorecardDraft
from ..schemas import (
    ValuesScorecardEdit,
    ValuesScorecardGenerateRequest,
    ValuesScorecardOut,
    ValuesScorecardSubmitRequest,
)
from ..services import reads
from ..services.drafting import DraftingUnavailable
from ..services.values_scoring import (
    ValuesScorecardError,
    TranscriptTooShort,
    build_markaz_payload,
    recompute_final_comments,
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
        "replaced_payload": draft.replaced_payload,
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
    except Exception as exc:
        # An unexpected model/SDK failure (timeout, anthropic.APIError, ...)
        # is not a predictable input error -- surface it as 503 like
        # DraftingUnavailable, never as an uncaught 500 with a stack trace.
        log.exception(
            "generate: unexpected scoring failure for application %s",
            body.application_id,
        )
        raise HTTPException(503, f"Scoring unavailable: {exc}") from exc

    ratings = [v["rating"] for v in scored["values"]]
    # proceed is DERIVED from the computed verdict, never client-supplied --
    # there is no client input for it on this endpoint, but this keeps the
    # rule visibly true here too rather than only in edit_draft/submit.
    proceed = scored["verdict"] == "PASS"

    draft = ValuesScorecardDraft(
        application_id=body.application_id,
        candidate_name=candidate_name,
        host=body.host,
        # Only the hash is stored -- the transcript is interview content
        # about a named person and does not need a second home once scored.
        transcript_sha256=hashlib.sha256(body.transcript.encode("utf-8")).hexdigest(),
        values_json=scored["values"],
        final_comments=recompute_final_comments(ratings, ""),
        proceed=proceed,
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
    # A draft carries the candidate's name plus verbatim interview evidence
    # -- gated on require_editor (anyone who can create a draft can read it),
    # never a bare signed-in viewer.
    _user: dict = Depends(require_editor),
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

    try:
        if body.values is not None:
            validate_values(body.values)  # locked shape: 6 canonical values, no blank evidence
            draft.values_json = body.values
    except ValuesScorecardError as exc:
        raise HTTPException(422, str(exc)) from exc

    ratings = [v["rating"] for v in draft.values_json]
    current_verdict = verdict(ratings)  # recomputed from the CURRENT ratings, never trusted

    if body.values is not None and current_verdict == "OUT":
        # GWC is never a back door around a failing values round.
        draft.gwc = None

    # final_comments must never assert a verdict/tally that disagrees with
    # the ratings actually on the row. Recompute the prefix whenever the
    # ratings changed and the caller didn't supply fresh text; when the
    # caller DID supply text, keep their narrative but the verdict/tally
    # leading it is still the one computed here, never their claim.
    if body.final_comments is not None:
        draft.final_comments = recompute_final_comments(ratings, body.final_comments)
    elif body.values is not None:
        draft.final_comments = recompute_final_comments(ratings, draft.final_comments)

    # proceed is DERIVED, never a client override of a failing verdict. A
    # client may set it False at will (e.g. GWC failed even though values
    # passed); it may NEVER force True on an OUT scorecard -- that would let
    # an editor permanently record "Yes" in Markaz for a candidate the
    # locked rule failed.
    if body.proceed is None:
        draft.proceed = current_verdict == "PASS"
    elif body.proceed and current_verdict != "PASS":
        log.warning(
            "edit_draft: refusing client proceed=True on an OUT scorecard "
            "for draft %s; GWC/manual override is not a back door around a "
            "failing values round.", draft_id,
        )
        draft.proceed = False
    else:
        draft.proceed = body.proceed

    db.commit()
    db.refresh(draft)
    return _draft_out(draft)


@router.post("/{draft_id}/submit", response_model=ValuesScorecardOut)
def submit(
    draft_id: str,
    body: ValuesScorecardSubmitRequest = ValuesScorecardSubmitRequest(),
    db: Session = Depends(get_db),
    user: dict = Depends(require_approver),
):
    draft = _draft_or_404(db, draft_id)
    if draft.status == "submitted":
        # A prior, already-committed submission. Refuse before touching
        # anything else -- this is the fast, common case, not the guard (see
        # below): the guard is the conditional UPDATE, which is what
        # actually stops a *concurrent* double-click.
        raise HTTPException(409, "This scorecard has already been submitted to Markaz")

    # --- CRITICAL 1: the guard IS the atomic transition, not this prior read.
    # Two concurrent submits (a double-click is two requests) must never both
    # proceed. Flip draft.status FIRST with a single conditional UPDATE gated
    # on status='draft'; only the request whose UPDATE actually matches a row
    # may go on to build and write the Markaz payload. Under Postgres READ
    # COMMITTED, an interleaved second request's UPDATE blocks on the row
    # lock, then re-evaluates its WHERE clause against the now-committed (or
    # rolled-back) row -- so it either correctly sees rowcount==0 (already
    # submitted) or correctly proceeds (the first request rolled back).
    flip = db.execute(
        text(
            "UPDATE coco.values_scorecard_drafts "
            "SET status = 'submitted' WHERE id = :id AND status = 'draft'"
        ),
        {"id": draft_id},
    )
    if flip.rowcount != 1:
        db.rollback()
        raise HTTPException(409, "This scorecard has already been submitted to Markaz")

    try:
        ratings = [v["rating"] for v in draft.values_json]
        current_verdict = verdict(ratings)

        # --- CRITICAL 2: proceed can never be forced True on a failing
        # verdict. edit_draft already enforces this at edit time, but it is
        # re-derived here too, defensively, immediately before the write
        # that makes it a permanent Markaz record.
        proceed = bool(draft.proceed) and current_verdict == "PASS"
        if draft.proceed and current_verdict != "PASS":
            log.warning(
                "submit: draft %s carries proceed=True against an OUT "
                "verdict; clamping to False before writing to Markaz.",
                draft_id,
            )

        # --- CRITICAL 3: never let a stale string assert a verdict/tally
        # that disagrees with the CURRENT ratings (e.g. "PASS - 6(+)..."
        # sitting beside proceedToRightSeat: "No").
        final_comments = recompute_final_comments(ratings, draft.final_comments)

        # Rebuild the payload from the draft's CURRENT columns and validate
        # it immediately before the write -- never trust that a stored draft
        # is already valid, however it got there.
        payload = build_markaz_payload(
            candidate_name=draft.candidate_name,
            host=draft.host,
            values=draft.values_json,
            final_comments=final_comments,
            proceed=proceed,
        )
        validate_markaz_payload(payload)
    except ValuesScorecardError as exc:
        db.rollback()
        raise HTTPException(422, str(exc)) from exc

    # --- CRITICAL 4 + 5: read the CURRENT public.applications row for this
    # target, in the SAME transaction, before writing.
    current_row = db.execute(
        text(
            "SELECT values_scorecard, candidate_id, job_id "
            "FROM public.applications WHERE id = :app_id FOR UPDATE"
        ),
        {"app_id": draft.application_id},
    ).mappings().first()
    if current_row is None:
        db.rollback()
        raise HTTPException(404, f"Application {draft.application_id} not found")

    # CRITICAL 5: refuse to write to a stale duplicate. Markaz's UI displays
    # the most recently updated application for a (candidate_id, job_id)
    # pair; writing to an older duplicate of the same pair appears to
    # silently fail (the UI never shows it). Skipped when either id is null.
    candidate_id, job_id = current_row["candidate_id"], current_row["job_id"]
    if candidate_id is not None and job_id is not None:
        newer_id = db.execute(
            text(
                "SELECT id FROM public.applications "
                "WHERE candidate_id = :cid AND job_id = :jid "
                "ORDER BY updated_at DESC LIMIT 1"
            ),
            {"cid": candidate_id, "jid": job_id},
        ).scalar()
        if newer_id is not None and newer_id != draft.application_id:
            db.rollback()
            raise HTTPException(
                409,
                f"Application {draft.application_id} is not the most recently "
                f"updated application for this candidate/job pair -- "
                f"application {newer_id} is newer. Retarget the draft to "
                f"{newer_id} rather than writing to a stale duplicate.",
            )

    # CRITICAL 4: never silently destroy an existing, human-written Markaz
    # scorecard. Refuse unless the caller explicitly opted into overwriting
    # it; when they do, keep the prior value rather than losing it.
    replaced_payload = None
    if current_row["values_scorecard"] is not None:
        if not body.overwrite:
            db.rollback()
            raise HTTPException(
                409,
                f"Application {draft.application_id} already has a values "
                "scorecard in Markaz. Resubmit with overwrite=true to "
                "replace it deliberately.",
            )
        replaced_payload = current_row["values_scorecard"]

    log.info(
        "values_scorecard submit: draft_id=%s application_id=%s payload=%s",
        draft.id, draft.application_id, json.dumps(payload),
    )

    # public.applications is Markaz's table, not Coco's: touch ONLY the
    # values_scorecard column of the ONE target row. Never insert, delete,
    # or touch any other column.
    result = db.execute(
        text("UPDATE public.applications SET values_scorecard = :payload::jsonb WHERE id = :app_id"),
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
    draft.proceed = proceed
    draft.final_comments = final_comments
    # id + email so an audit trail is readable directly in SQL, no join.
    draft.approved_by = f"{user.get('id') or ''} {user.get('email') or ''}".strip()
    draft.approved_at = now
    draft.submitted_at = now
    draft.markaz_payload = payload
    if replaced_payload is not None:
        draft.replaced_payload = replaced_payload

    db.commit()
    db.refresh(draft)
    return _draft_out(draft)
