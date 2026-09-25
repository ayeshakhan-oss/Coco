"""Candidate invites: configure the links, preview, pilot, send live.

`webapp/services/invites.py` holds the rules, `invite_render.py` the locked
design, `sending.send_invite` the transport. This router is the only code that
writes an invite into the world.

🔴 A BOOKING LINK IS PROVEN, NOT TRUSTED. `POST /links/{id}/verify` fetches the
   URL and stores the page title it actually returned. A live send refuses
   while that is null (CLAUDE.md Rule 24). The reason is concrete: Growth
   Manager runs as Job 39 Lahore and Job 41 Karachi with separate schedules,
   and `scripts/jobs/job39/send_growth_manager_invites_batch.py` sits in the
   job39 folder holding Job 41 constants. Nothing about the filename, the
   folder or the variable name would tell you.

🔴 A LIVE SEND IS APPROVER-GATED AND HAPPENS ONCE. `uq_invite_sends_live_once`
   makes a second live invite of the same type to the same application a
   database error, which is the 2026-08-24 batch discipline (scan Sent Mail
   before and after, because a send loop reports what it TRIED) enforced
   rather than remembered.

🔴 PILOTS GO TO AYESHA, ALONE (Rule 4), AND A LIVE SUBJECT NEVER CARRIES
   "[PILOT" (Rule 7). Both are checked here and again inside `send_invite`,
   because the Layer 3 send-time hook is inert and there is no net below this.
"""

from __future__ import annotations

import datetime as dt
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user, require_approver, require_editor
from ..models import InviteLink, InviteSend
from ..schemas import (
    InviteLinkOut,
    InviteLinkUpsert,
    InvitePreviewOut,
    InvitePreviewRequest,
    InviteSendOut,
    InviteSendRequest,
    InviteTypeOut,
)
from ..services import invite_render as render_svc
from ..services import invites as inv
from ..services import sending

log = logging.getLogger("webapp.routers.invites")

router = APIRouter(prefix="/api/invites", tags=["invites"])


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


# Name and email for the candidate behind an application. Read from the Markaz
# tables, never retyped: a hand-typed address is how an invite spent three
# months going to a "@gamil.com" typo.
_APPLICATION_SQL = text(
    """
    SELECT a.id            AS application_id,
           a.job_id        AS job_id,
           c.id            AS candidate_id,
           c.first_name    AS first_name,
           c.last_name     AS last_name,
           c.email         AS email,
           j.title         AS job_title
    FROM applications a
    JOIN candidates c ON c.id = a.candidate_id
    LEFT JOIN jobs j ON j.id = a.job_id
    WHERE a.id = :application_id
    """
)


def _link_out(row: InviteLink) -> InviteLinkOut:
    matches: Optional[bool] = None
    if row.verified_title and row.expected_title:
        matches = inv.title_mentions(row.verified_title, row.expected_title)
    return InviteLinkOut(
        id=row.id,
        job_id=row.job_id,
        invite_type=row.invite_type,
        label=row.label,
        booking_url=row.booking_url,
        jd_url=row.jd_url,
        prep_url=row.prep_url,
        expected_title=row.expected_title,
        verified_title=row.verified_title,
        verified_at=row.verified_at,
        verify_error=row.verify_error,
        title_matches_expected=matches,
        cc_list=list(row.cc_list or []) or None,
    )


def _send_out(row: InviteSend) -> InviteSendOut:
    return InviteSendOut(
        id=row.id,
        invite_type=row.invite_type,
        application_id=row.application_id,
        candidate_name=row.candidate_name,
        to_address=row.to_address,
        cc_list=list(row.cc_list or []) or None,
        subject=row.subject,
        is_live=row.is_live,
        booking_url=row.booking_url,
        booking_verified_title=row.booking_verified_title,
        sent_at=row.sent_at,
        sent_by=row.sent_by,
    )


def _resolve_link(db: Session, invite_type: str, job_id: Optional[int]) -> Optional[InviteLink]:
    """The job-specific configuration if there is one, otherwise the default.

    The job-specific row winning is the whole point: it is how Lahore and
    Karachi keep two booking schedules without either inheriting the other's.
    """
    if job_id is not None:
        row = (
            db.query(InviteLink)
            .filter(InviteLink.invite_type == invite_type, InviteLink.job_id == job_id)
            .one_or_none()
        )
        if row:
            return row
    return (
        db.query(InviteLink)
        .filter(InviteLink.invite_type == invite_type, InviteLink.job_id.is_(None))
        .one_or_none()
    )


# --------------------------------------------------------------------------
# Types
# --------------------------------------------------------------------------


@router.get("/types", response_model=list[InviteTypeOut])
def list_types(user: dict = Depends(get_current_user)):
    """The seven types and what each one needs.

    Served from the service rather than duplicated in the frontend, so a type
    cannot exist in the picker and not in the gate.
    """
    return [
        InviteTypeOut(
            key=key,
            label=spec["label"],
            confirm=spec["confirm"],
            note=spec["note"],
            required=list(render_svc.REQUIRED[key]),
        )
        for key, spec in inv.INVITE_TYPES.items()
    ]


# --------------------------------------------------------------------------
# Links
# --------------------------------------------------------------------------


@router.get("/links", response_model=list[InviteLinkOut])
def list_links(
    job_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    q = db.query(InviteLink)
    if job_id is not None:
        # Both the job's own rows and the defaults it would fall back to.
        q = q.filter((InviteLink.job_id == job_id) | (InviteLink.job_id.is_(None)))
    return [_link_out(r) for r in q.order_by(InviteLink.invite_type).all()]


@router.post("/links", response_model=InviteLinkOut)
def upsert_link(
    body: InviteLinkUpsert,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    if body.invite_type not in inv.INVITE_TYPES:
        raise HTTPException(400, f"unknown invite type {body.invite_type!r}")
    if body.booking_url and inv.forbids_booking_link(body.invite_type):
        raise HTTPException(
            400,
            f"{inv.INVITE_TYPES[body.invite_type]['label']} has no booking "
            "button by design, so a booking link cannot be configured for it.",
        )

    row = (
        db.query(InviteLink)
        .filter(
            InviteLink.invite_type == body.invite_type,
            InviteLink.job_id.is_(None) if body.job_id is None
            else InviteLink.job_id == body.job_id,
        )
        .one_or_none()
    )
    if row is None:
        row = InviteLink(invite_type=body.invite_type, job_id=body.job_id)
        db.add(row)

    # 🔴 CHANGING A URL DISCARDS ITS PROOF. A verification belongs to the link
    # that was fetched, not to the row. Carrying an old title across an edit is
    # exactly how a Karachi schedule would come to look verified for Lahore.
    changed = (
        (body.booking_url or None) != row.booking_url
        or (body.jd_url or None) != row.jd_url
        or (body.prep_url or None) != row.prep_url
    )
    row.label = body.label
    row.booking_url = body.booking_url or None
    row.jd_url = body.jd_url or None
    row.prep_url = body.prep_url or None
    row.expected_title = body.expected_title or None
    row.cc_list = list(body.cc_list or []) or None
    if changed:
        row.verified_title = None
        row.verified_at = None
        row.verified_by = None
        row.verify_error = None
    row.updated_at = _utcnow()

    db.commit()
    db.refresh(row)
    return _link_out(row)


def _fetch_title(url: str) -> tuple[Optional[str], Optional[str]]:
    """(title, error). Fetches the page and reads its <title>.

    Kept out of the service so the rules stay testable without a network.
    """
    import requests

    try:
        r = requests.get(
            url,
            timeout=20,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (compatible; CocoInviteCheck/1.0)"},
        )
    except requests.RequestException as exc:
        return None, f"could not fetch: {exc}"
    if not r.ok:
        return None, f"fetch returned HTTP {r.status_code}"
    # A Markaz-style SPA answers 200 with its own index.html, so the status
    # code alone proves nothing (CLAUDE.md Rule 18). The title is the evidence.
    title = inv.title_of(r.text)
    if not title:
        return None, "the page returned no <title> to check"
    return title, None


@router.post("/links/{link_id}/verify", response_model=InviteLinkOut)
def verify_link(
    link_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """Fetch the booking link and record the title the page actually returned.

    This is the Rule 24 check made routine. The title is stored whether or not
    it matches `expected_title`: recording what the page said is the evidence,
    and judging the match is a separate, visible step.
    """
    row = db.get(InviteLink, link_id)
    if not row:
        raise HTTPException(404, "Invite link configuration not found")
    if not (row.booking_url or "").strip():
        raise HTTPException(400, "There is no booking link on this configuration to verify.")

    title, error = _fetch_title(row.booking_url)
    row.verified_title = title
    row.verify_error = error
    row.verified_at = _utcnow() if title else None
    row.verified_by = (user.get("id") or "") if title else None
    row.updated_at = _utcnow()
    db.commit()
    db.refresh(row)
    log.info(
        "invites: verified %s for %s -> %r (%s)",
        row.booking_url, row.invite_type, title, error or "ok",
    )
    return _link_out(row)


# --------------------------------------------------------------------------
# Preview and send
# --------------------------------------------------------------------------


def _context_for(db: Session, body, link: Optional[InviteLink]) -> dict:
    """Merge the operator's fields with the configured links and Markaz data.

    Operator-supplied fields win for the free text; the LINKS come from the
    configuration, because a link pasted into a form is exactly the untraceable
    constant this module exists to replace.
    """
    ctx = dict(body.fields or {})
    if link:
        if link.booking_url and not inv.forbids_booking_link(body.invite_type):
            ctx["booking_url"] = link.booking_url
        if link.jd_url:
            ctx.setdefault("jd_url", link.jd_url)
        if link.prep_url:
            ctx.setdefault("prep_url", link.prep_url)

    if body.application_id:
        row = db.execute(
            _APPLICATION_SQL, {"application_id": body.application_id}
        ).mappings().one_or_none()
        if row is None:
            raise HTTPException(404, f"Application {body.application_id} not found")
        first = (row["first_name"] or "").strip()
        last = (row["last_name"] or "").strip()
        ctx.setdefault("first_name", first or last)
        ctx.setdefault("full_name", (first + " " + last).strip())
        ctx.setdefault("position", row["job_title"] or "")
        ctx["_email"] = row["email"]
        ctx["_job_id"] = row["job_id"]
        ctx["_candidate_id"] = row["candidate_id"]
    return ctx


@router.post("/preview", response_model=InvitePreviewOut)
def preview(
    body: InvitePreviewRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Render without sending, and say what a live send would refuse.

    The blockers are returned at preview time on purpose. Finding out that a
    link is unverified at the moment of sending is how a batch gets sent with
    the check skipped.
    """
    if body.invite_type not in inv.INVITE_TYPES:
        raise HTTPException(400, f"unknown invite type {body.invite_type!r}")

    link = _resolve_link(db, body.invite_type, body.job_id)
    ctx = _context_for(db, body, link)
    missing = render_svc.missing_fields(body.invite_type, ctx)
    subject = render_svc.subject_for(body.invite_type, ctx)

    html = ""
    if not missing:
        try:
            html = render_svc.render(body.invite_type, ctx)
        except inv.InviteError as exc:
            raise HTTPException(400, str(exc))

    blockers = inv.check_before_send(
        invite_type=body.invite_type,
        live=True,
        subject=subject,
        candidate_email=ctx.get("_email"),
        booking_url=ctx.get("booking_url"),
        booking_verified_title=link.verified_title if link else None,
    )
    if missing:
        blockers.insert(0, "missing: " + ", ".join(missing))

    warnings: list[str] = []
    if link and link.verified_title and link.expected_title:
        if not inv.title_mentions(link.verified_title, link.expected_title):
            warnings.append(
                f"the booking page is titled {link.verified_title!r}, which does "
                f"not look like {link.expected_title!r}. Check the city and the "
                "role before sending."
            )
    if body.application_id:
        already = (
            db.query(InviteSend)
            .filter(
                InviteSend.application_id == body.application_id,
                InviteSend.invite_type == body.invite_type,
                InviteSend.is_live.is_(True),
            )
            .one_or_none()
        )
        if already:
            warnings.append(
                f"a live {inv.INVITE_TYPES[body.invite_type]['label']} already "
                f"went to this application on "
                f"{already.sent_at:%Y-%m-%d}. Sending again would be a duplicate."
            )
    return InvitePreviewOut(
        invite_type=body.invite_type, subject=subject, body_html=html,
        missing=missing, blockers=blockers, warnings=warnings,
    )


@router.post("/send", response_model=InviteSendOut)
def send(
    body: InviteSendRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """Pilot to Ayesha (editor) or send live to the candidate (approver).

    The role check is INSIDE the handler rather than on the route, because one
    route serves both and a pilot must stay available to an editor. A live
    send is a different act and needs an approver.
    """
    if body.invite_type not in inv.INVITE_TYPES:
        raise HTTPException(400, f"unknown invite type {body.invite_type!r}")
    if body.live and (user.get("role") not in ("approver", "super_admin")):
        raise HTTPException(
            403,
            "Sending an invite to a candidate needs approver rights. You can "
            "send a pilot to Ayesha.",
        )

    link = _resolve_link(db, body.invite_type, body.job_id)
    ctx = _context_for(db, body, link)
    if body.candidate_name:
        ctx.setdefault("full_name", body.candidate_name)
    candidate_email = (body.candidate_email or ctx.get("_email") or "").strip() or None

    subject = (body.subject or "").strip() or render_svc.subject_for(body.invite_type, ctx)
    cc = list(body.cc or (link.cc_list if link else None) or []) if body.live else None

    problems = inv.check_before_send(
        invite_type=body.invite_type,
        live=body.live,
        subject=subject,
        candidate_email=candidate_email,
        booking_url=ctx.get("booking_url"),
        booking_verified_title=link.verified_title if link else None,
        cc=cc,
    )
    if problems:
        raise HTTPException(400, "This invite cannot be sent: " + "; ".join(problems))

    try:
        html = render_svc.render(body.invite_type, ctx)
    except inv.InviteError as exc:
        raise HTTPException(400, str(exc))

    # 🔴 THE DUPLICATE ROW IS WRITTEN BEFORE THE EMAIL LEAVES. If the unique
    # index rejects it, nothing has been sent. Writing the log after the send
    # would let a duplicate go out and only then fail to record it, which is
    # the wrong way round for a guard whose entire job is to prevent a second
    # copy reaching a candidate.
    record = InviteSend(
        application_id=body.application_id,
        candidate_id=ctx.get("_candidate_id"),
        job_id=body.job_id or ctx.get("_job_id"),
        invite_type=body.invite_type,
        candidate_name=ctx.get("full_name") or ctx.get("first_name"),
        to_address=(candidate_email if body.live else inv.PILOT_RECIPIENT),
        cc_list=cc or None,
        subject=subject,
        body_html=html,
        is_live=bool(body.live),
        booking_url=ctx.get("booking_url"),
        booking_verified_title=link.verified_title if link else None,
        sent_by=user.get("id") or "",
    )
    db.add(record)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            409,
            f"A live {inv.INVITE_TYPES[body.invite_type]['label']} has already "
            f"been sent to application {body.application_id}. Nothing was sent.",
        )

    try:
        sending.send_invite(
            invite_type=body.invite_type,
            subject=subject,
            body_html=html,
            live=bool(body.live),
            candidate_email=candidate_email,
            cc=cc,
            booking_url=ctx.get("booking_url"),
            booking_verified_title=link.verified_title if link else None,
            context=f"invite_{body.invite_type}_{'live' if body.live else 'pilot'}"
                    f"_{body.application_id or 'adhoc'}",
        )
    except sending.SendBlocked as exc:
        db.rollback()
        raise HTTPException(
            400,
            "Blocked at the send gate: "
            + "; ".join(v["message"] for v in exc.violations),
        )
    except sending.SendNotConfigured as exc:
        db.rollback()
        raise HTTPException(503, str(exc))
    except Exception:
        # The row is rolled back so a failed send never reads later as a send
        # that happened, and never blocks the retry.
        db.rollback()
        log.exception("invites: send failed for %s", body.invite_type)
        raise HTTPException(502, "The invite could not be sent. Nothing was recorded.")

    db.commit()
    db.refresh(record)
    log.info(
        "invites: %s %s -> %s by %s",
        "LIVE" if body.live else "pilot", body.invite_type,
        record.to_address, user.get("email"),
    )
    return _send_out(record)


@router.get("/sends", response_model=list[InviteSendOut])
def list_sends(
    application_id: Optional[int] = Query(None),
    invite_type: Optional[str] = Query(None),
    live_only: bool = Query(False),
    limit: int = Query(200, ge=1, le=1000),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """What actually went out. The record a send loop's console cannot give."""
    q = db.query(InviteSend)
    if application_id is not None:
        q = q.filter(InviteSend.application_id == application_id)
    if invite_type:
        q = q.filter(InviteSend.invite_type == invite_type)
    if live_only:
        q = q.filter(InviteSend.is_live.is_(True))
    rows = q.order_by(InviteSend.sent_at.desc()).limit(limit).all()
    return [_send_out(r) for r in rows]
