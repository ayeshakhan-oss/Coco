"""Draft lifecycle endpoints: AI generate, read, edit, re-eval, preview.

Approve/send live in Phase 6. The eval is always re-run server-side on the
freshly rendered HTML — the client's pass/fail is never trusted.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import ROLE_LEVEL, get_current_user, require_approver, require_editor
from ..reuse import EMAIL_TYPES, LOGO_PATH, evaluate_email
from ..schemas import (
    CommunicationOut,
    DraftUpdate,
    EvalResult,
    GenerateRequest,
    GenerateResponse,
    SendRequest,
    SendResponse,
)
from ..services import communications as comm_svc
from ..services import drafting, reads, rendering, sending
from ..services.scorecard import normalize_gwc_scorecard, normalize_values_scorecard

router = APIRouter(prefix="/api/communications", tags=["communications"])


def _scorecard_for(raw: dict, email_type: str) -> Optional[dict]:
    if email_type == "gwc_rejection":
        return normalize_gwc_scorecard(raw.get("gwc_scorecard"))
    # values_feedback / warm_bench / cv_rejection lean on the values scorecard
    return normalize_values_scorecard(raw.get("values_scorecard"))


@router.post("/generate", response_model=GenerateResponse)
def generate(
    body: GenerateRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    if body.email_type not in EMAIL_TYPES:
        raise HTTPException(400, f"email_type must be one of {EMAIL_TYPES}")

    app_row = reads.get_application(db, body.application_id)
    if not app_row:
        raise HTTPException(404, "Application not found")

    raw = reads.get_scorecards_raw(db, body.application_id) or {}
    scorecard = _scorecard_for(raw, body.email_type)

    # Candidate name from the candidates table — NEVER scorecard.candidateName.
    first_name = (app_row.get("first_name") or "there").strip()
    role = (body.role_title or app_row.get("job_title") or "the role").strip()

    drafted = drafting.generate_draft(
        scorecard=scorecard,
        first_name=first_name,
        role=role,
        app_id=body.application_id,
        email_type=body.email_type,
    )

    comm = comm_svc.create_draft(
        db,
        application_id=body.application_id,
        candidate_id=app_row["candidate_id"],
        job_id=app_row.get("job_pk"),
        email_type=body.email_type,
        title_line=drafted["title_line"],
        role_title=role,
        body_html=drafted["body_html"],
        draft_content=rendering.attach_headings(drafted["content"], body.email_type),
        word_count=drafted["eval"]["word_count"],
        eval_result=drafted["eval"],
        eval_passed=drafted["eval"]["passed"],
        created_by=user.get("id"),
    )

    return {
        "communication": comm,
        "eval": drafted["eval"],
        "attempts": drafted["attempts"],
        "drafter_used": drafted["drafter_used"],
    }


@router.get("", response_model=list[CommunicationOut])
def list_comms(
    status: Optional[str] = Query(None),
    candidate_id: Optional[int] = Query(None),
    mine: bool = Query(False),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    return comm_svc.list_communications(
        db,
        status=status,
        candidate_id=candidate_id,
        created_by=user.get("id") if mine else None,
    )


@router.get("/{comm_id}", response_model=CommunicationOut)
def get_comm(comm_id: str, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    comm = comm_svc.get(db, comm_id)
    if not comm:
        raise HTTPException(404, "Communication not found")
    return comm


@router.put("/{comm_id}", response_model=GenerateResponse)
def update_comm(
    comm_id: str,
    body: DraftUpdate,
    db: Session = Depends(get_db),
    _user: dict = Depends(require_editor),
):
    comm = comm_svc.get(db, comm_id)
    if not comm:
        raise HTTPException(404, "Communication not found")
    if comm.status in ("sent",):
        raise HTTPException(409, "A sent communication cannot be edited")

    app_row = reads.get_application(db, comm.application_id) if comm.application_id else None
    first_name = (app_row.get("first_name") if app_row else None) or "there"
    role = (
        body.role_title
        or comm.role_title
        or (app_row.get("job_title") if app_row else None)
        or "the role"
    )
    content = rendering.attach_headings(body.content, comm.email_type)
    body_html = rendering.render_body(
        content, email_type=comm.email_type, candidate_name=first_name, role=role,
        app_id=comm.application_id,
    )
    full_html = rendering.wrap_full(
        body_html, title_line=body.title_line, role=role, email_type=comm.email_type
    )
    result = evaluate_email(full_html, body.title_line, comm.email_type, pilot_mode=True)
    comm = comm_svc.update_content(
        db, comm,
        body_html=body_html,
        draft_content=content,
        title_line=body.title_line,
        role_title=role,
        word_count=result["word_count"],
        eval_result=result,
        eval_passed=result["passed"],
    )
    return {"communication": comm, "eval": result, "attempts": 0, "drafter_used": "human"}


@router.post("/{comm_id}/eval", response_model=EvalResult)
def reeval(
    comm_id: str,
    mode: str = Query("pilot"),
    db: Session = Depends(get_db),
    _user: dict = Depends(require_editor),
):
    comm = comm_svc.get(db, comm_id)
    if not comm:
        raise HTTPException(404, "Communication not found")
    full_html = rendering.wrap_full(
        comm.body_html or "", title_line=comm.title_line or "", role=comm.role_title or "the role",
        email_type=comm.email_type,
    )
    return evaluate_email(full_html, comm.title_line or "", comm.email_type, pilot_mode=(mode != "live"))


@router.get("/{comm_id}/preview", response_class=HTMLResponse)
def preview(comm_id: str, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    comm = comm_svc.get(db, comm_id)
    if not comm:
        raise HTTPException(404, "Communication not found")
    full_html = rendering.wrap_full(
        comm.body_html or "", title_line=comm.title_line or "", role=comm.role_title or "the role",
        email_type=comm.email_type,
    )
    return HTMLResponse(rendering.preview_html(full_html))


def _gate_or_422(comm) -> dict:
    """Re-render stored content and refuse if any HARD-BLOCK is present."""
    full_html = rendering.wrap_full(
        comm.body_html or "", title_line=comm.title_line or "",
        role=comm.role_title or "the role", email_type=comm.email_type,
    )
    result = evaluate_email(full_html, comm.title_line or "", comm.email_type, pilot_mode=True)
    hard = [v for v in result["violations"] if v["severity"] == "HARD_BLOCK"]
    if hard:
        raise HTTPException(422, detail={"message": "Resolve hard blocks first", "violations": hard})
    return result


@router.post("/{comm_id}/submit", response_model=CommunicationOut)
def submit_for_review(comm_id: str, db: Session = Depends(get_db), _user: dict = Depends(require_editor)):
    comm = comm_svc.get(db, comm_id)
    if not comm:
        raise HTTPException(404, "Communication not found")
    if comm.status != "draft":
        raise HTTPException(409, f"Only a draft can be submitted (status={comm.status})")
    _gate_or_422(comm)
    return comm_svc.submit(db, comm)


@router.post("/{comm_id}/approve", response_model=CommunicationOut)
def approve(comm_id: str, db: Session = Depends(get_db), user: dict = Depends(require_approver)):
    comm = comm_svc.get(db, comm_id)
    if not comm:
        raise HTTPException(404, "Communication not found")
    if comm.status != "in_review":
        raise HTTPException(409, f"Only an in-review draft can be approved (status={comm.status})")
    _gate_or_422(comm)  # re-evaluate server-side; never trust a stale pass
    return comm_svc.approve(db, comm, user.get("id"))


@router.post("/{comm_id}/request-changes", response_model=CommunicationOut)
def request_changes(comm_id: str, db: Session = Depends(get_db), _user: dict = Depends(require_approver)):
    comm = comm_svc.get(db, comm_id)
    if not comm:
        raise HTTPException(404, "Communication not found")
    if comm.status != "in_review":
        raise HTTPException(409, f"Only an in-review draft can be returned (status={comm.status})")
    return comm_svc.request_changes(db, comm)


@router.post("/{comm_id}/send", response_model=SendResponse)
def send(
    comm_id: str,
    body: SendRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    comm = comm_svc.get(db, comm_id)
    if not comm:
        raise HTTPException(404, "Communication not found")

    mode = body.mode
    if mode not in ("pilot", "live"):
        raise HTTPException(400, "mode must be 'pilot' or 'live'")

    app_row = reads.get_application(db, comm.application_id) if comm.application_id else None
    first_name = (app_row.get("first_name") if app_row else None) or "there"
    candidate_email = app_row.get("email") if app_row else None

    if mode == "live":
        if ROLE_LEVEL.get(user.get("app_role", "viewer"), 0) < ROLE_LEVEL["approver"]:
            raise HTTPException(403, "Only an approver can send live")
        if comm.status != "approved":
            raise HTTPException(409, "A communication must be approved before a live send")

    try:
        result = sending.send_communication(
            comm, mode=mode, first_name=first_name, candidate_email=candidate_email
        )
    except sending.SendBlocked as e:
        raise HTTPException(422, detail={"message": "Blocked by validation", "violations": e.violations})
    except sending.SendNotConfigured as e:
        raise HTTPException(503, str(e))
    except Exception as e:  # transport / SMTP / security error
        if mode == "live":
            comm_svc.mark_failed(db, comm, str(e))
        raise HTTPException(502, f"Send failed: {e}")

    if mode == "live":
        comm = comm_svc.mark_sent(
            db, comm,
            sent_to=result["recipients"],
            message_id=result["message_id"],
            rendered_html=result["full_html"],
        )
    return {
        "communication": comm,
        "mode": mode,
        "subject": result["subject"],
        "recipients": result["recipients"],
        "message_id": result["message_id"],
    }


# Logo for in-browser email previews (the real email embeds it as a cid).
asset_router = APIRouter(prefix="/api/assets", tags=["assets"])


@asset_router.get("/logo.png")
def logo():
    return FileResponse(LOGO_PATH, media_type="image/png")
