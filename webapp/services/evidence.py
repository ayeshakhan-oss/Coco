"""App-owned communication-evidence overrides + read helpers.

This module is the ONLY writer of manual overrides on `comm_evidence`
(mark-sent / ignore). It is strictly read-only with respect to Gmail and the
send pipeline — it never imports `sending.py`/`safe_send.py`.

Manual "mark sent" records a human attestation that a candidate was
communicated with OUTSIDE Coco. It is NOT a send: it never creates a
`communications` row and never touches the eval gate.
"""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _application_keys(db: Session, application_id: int) -> Optional[tuple[int, Optional[int]]]:
    """Return (candidate_id, job_id) for an application, or None if not found."""
    row = db.execute(
        text("SELECT candidate_id, job_id FROM applications WHERE id = :id"),
        {"id": application_id},
    ).mappings().first()
    return (row["candidate_id"], row["job_id"]) if row else None


def _ensure_row(db: Session, application_id: int) -> bool:
    """Create a bare comm_evidence row for an application if absent. Returns
    False if the application doesn't exist."""
    keys = _application_keys(db, application_id)
    if keys is None:
        return False
    candidate_id, job_id = keys
    db.execute(
        text(
            """
            INSERT INTO comm_evidence (id, application_id, candidate_id, job_id, gmail_status)
            VALUES ('ev-' || replace(gen_random_uuid()::text, '-', ''),
                    :app_id, :cand_id, :job_id, 'not_checked')
            ON CONFLICT (application_id) DO NOTHING
            """
        ),
        {"app_id": application_id, "cand_id": candidate_id, "job_id": job_id},
    )
    return True


def mark_sent(
    db: Session, application_id: int, user_id: str, reason: Optional[str] = None
) -> bool:
    if not _ensure_row(db, application_id):
        return False
    db.execute(
        text(
            """
            UPDATE comm_evidence
            SET marked_sent_by = :uid, marked_sent_at = :ts, marked_sent_reason = :reason,
                updated_at = :ts
            WHERE application_id = :app_id
            """
        ),
        {"uid": user_id, "ts": _utcnow(), "reason": reason, "app_id": application_id},
    )
    db.commit()
    return True


def clear_mark(db: Session, application_id: int) -> bool:
    res = db.execute(
        text(
            """
            UPDATE comm_evidence
            SET marked_sent_by = NULL, marked_sent_at = NULL, marked_sent_reason = NULL,
                updated_at = :ts
            WHERE application_id = :app_id
            """
        ),
        {"ts": _utcnow(), "app_id": application_id},
    )
    db.commit()
    return res.rowcount > 0


def set_ignore(db: Session, application_id: int, user_id: str, ignored: bool) -> bool:
    if not _ensure_row(db, application_id):
        return False
    db.execute(
        text(
            """
            UPDATE comm_evidence
            SET ignored = :ignored,
                ignored_by = CASE WHEN :ignored THEN :uid ELSE NULL END,
                ignored_at = CASE WHEN :ignored THEN :ts ELSE NULL END,
                updated_at = :ts
            WHERE application_id = :app_id
            """
        ),
        {"ignored": ignored, "uid": user_id, "ts": _utcnow(), "app_id": application_id},
    )
    db.commit()
    return True


def bulk_mark_sent(
    db: Session, application_ids: list[int], user_id: str, reason: Optional[str] = None
) -> int:
    """Mark many candidates as manually sent in one transaction. Returns count."""
    n = 0
    ts = _utcnow()
    for app_id in application_ids:
        if not _ensure_row(db, app_id):
            continue
        db.execute(
            text(
                "UPDATE comm_evidence SET marked_sent_by=:uid, marked_sent_at=:ts, "
                "marked_sent_reason=:reason, updated_at=:ts WHERE application_id=:app_id"
            ),
            {"uid": user_id, "ts": ts, "reason": reason, "app_id": app_id},
        )
        n += 1
    db.commit()
    return n


def bulk_set_ignore(
    db: Session, application_ids: list[int], user_id: str, ignored: bool
) -> int:
    """Ignore / un-ignore many candidates in one transaction. Returns count."""
    n = 0
    ts = _utcnow()
    for app_id in application_ids:
        if not _ensure_row(db, app_id):
            continue
        db.execute(
            text(
                "UPDATE comm_evidence SET ignored=:ignored, "
                "ignored_by = CASE WHEN :ignored THEN :uid ELSE NULL END, "
                "ignored_at = CASE WHEN :ignored THEN :ts ELSE NULL END, "
                "updated_at=:ts WHERE application_id=:app_id"
            ),
            {"ignored": ignored, "uid": user_id, "ts": ts, "app_id": app_id},
        )
        n += 1
    db.commit()
    return n


def get_match(db: Session, application_id: int) -> dict:
    """The Gmail/override evidence for one application (drives the match modal).
    Returns a default 'not_checked' shape if no evidence row exists yet."""
    row = db.execute(
        text(
            """
            SELECT gmail_status, match_method, matched_message_id, gmail_thread_id,
                   internal_date, matched_subject, matched_to, matched_snippet,
                   uncertain_reason, marked_sent_at, marked_sent_by, marked_sent_reason,
                   ignored, ignored_at, checked_at
            FROM comm_evidence WHERE application_id = :app_id
            """
        ),
        {"app_id": application_id},
    ).mappings().first()
    if not row:
        return {"gmail_status": "not_checked"}
    return dict(row)


def get_sync_status(db: Session) -> dict:
    """Latest sync run + 'last synced' time for the dashboard indicator."""
    last_ok = db.execute(
        text(
            "SELECT max(finished_at) AS ts FROM gmail_sync_runs WHERE status IN ('ok','partial')"
        )
    ).mappings().first()
    latest = db.execute(
        text(
            """
            SELECT status, trigger, messages_scanned, candidates_evaluated,
                   found_count, uncertain_count, none_count, started_at, finished_at,
                   error_detail
            FROM gmail_sync_runs
            ORDER BY started_at DESC
            LIMIT 1
            """
        )
    ).mappings().first()
    out: dict = {"last_sync_at": last_ok["ts"] if last_ok else None}
    if latest:
        out.update(dict(latest))
    return out
