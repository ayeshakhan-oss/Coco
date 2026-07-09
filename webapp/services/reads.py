"""Read queries against the (read-only) Talent-Acquisition tables, plus the
app-owned `communications` + `comm_evidence` tables, to drive the dashboard.

Three orthogonal facts are computed, then a single display label is derived:

  - base_bucket  : the LEGACY classification (unchanged) — awaiting_scorecard /
                   needs_comms / in_progress / sent — from scorecard presence +
                   our own `communications` rows. Kept byte-for-byte for the
                   `scored`/`sent` regression guarantees.
  - gmail_status : not_checked / none / found / uncertain — from `comm_evidence`
                   (Gmail Sent evidence; written by the read-only sync feature).
  - comm_required + days_waiting : derived from `applications.status` and
                   `applied_at` (the agreed "waiting clock"; CV-stage rejections
                   need comms even with no scorecard).

`derive_display_status` (the pure function below) and the SQL `displayed` CTE
encode the SAME precedence — keep them in sync. The only paths to "Sent" are an
app-sent comm, a Gmail `found` match, or a manual override; never Markaz alone.

`communication_history` (Markaz's own email log) is surfaced as *context*
(prior_platform_comms count + the History/Detail view), never as a "sent" flag.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session


def _ensure_app_tables(db: Session) -> None:
    """Re-create the app-owned evidence tables if they're missing. A Neon
    restore/branch-swap can drop them while leaving alembic stamped (see
    docs/RAILWAY_DEPLOYMENT_LESSONS.md) — this lets reads self-heal at runtime.
    Delegates to the shared, DURABLE (committing) helper so reads, the sync
    service, and the refresh endpoint all recover the same way."""
    from ..db import ensure_app_tables

    ensure_app_tables()


def _heal_exec(db: Session, sql: str, params: Optional[dict] = None):
    """Execute a read; if it fails because an app-owned table is missing,
    recreate the tables and retry once (so a DB reset can't blank the dashboard)."""
    try:
        return db.execute(text(sql), params or {})
    except (ProgrammingError, OperationalError) as e:
        msg = str(e).lower()
        if "comm_evidence" in msg or "gmail_sync_runs" in msg or "does not exist" in msg:
            db.rollback()
            _ensure_app_tables(db)
            return db.execute(text(sql), params or {})
        raise

DISPLAY_STATUSES = (
    "sent",
    "ignored",
    "needs_review",
    "in_progress",
    "high_priority",
    "needs_comms",
    "awaiting_scorecard",
)

# `applications.status` values that require a candidate communication, and the
# email type each maps to (editor may override the type in the draft editor).
_COMM_REQUIRED_STATUSES = ("rejected", "warm_bench", "consider_other_roles")
_WARM_BENCH_STATUSES = ("warm_bench", "consider_other_roles")


def compute_comm_required(status: Optional[str]) -> bool:
    return status in _COMM_REQUIRED_STATUSES


def infer_required_email_type(
    status: Optional[str], values_filled: bool, gwc_filled: bool
) -> Optional[str]:
    if status == "rejected":
        if gwc_filled:
            return "gwc_rejection"
        if values_filled:
            return "values_feedback"
        return "cv_rejection"
    if status in _WARM_BENCH_STATUSES:
        return "warm_bench"
    return None


def compute_is_high_priority(
    *,
    comm_required: bool,
    active_count: int,
    sent_count: int,
    manual_marked: bool,
    gmail_status: str,
    ignored: bool,
    days_waiting: Optional[int],
    markaz_comms: int = 0,
) -> bool:
    """High priority = needs comms, NO evidence (incl. no Markaz log), not in
    progress/ignored, >7 days. Both Gmail and Markaz are referenced."""
    return bool(
        comm_required
        and active_count == 0
        and sent_count == 0
        and not manual_marked
        and gmail_status not in ("found", "uncertain")
        and (markaz_comms or 0) == 0
        and not ignored
        and (days_waiting or 0) > 7
    )


_STAGE_DISPLAY = {
    "shortlisted": "shortlisted",
    "gwc_scheduled": "interview_scheduled",
    "case_study_sent": "case_study",
}


def derive_display_status(
    *,
    sent_count: int,
    active_count: int,
    gmail_status: str,
    manual_marked: bool,
    comm_required: bool,
    is_high_priority: bool,
    markaz_comms: int = 0,
    ignored: bool = False,
    status: Optional[str] = None,
) -> str:
    """Pure derivation — MUST match the SQL `displayed` CTE precedence below.
    A deliberate app-send or manual mark is always Sent. External evidence
    (Gmail-found / Markaz log) counts as Sent ONLY when a rejection/feedback is
    actually required (comm_required); for a not-yet-decided candidate an email
    on record is an interview INVITE, so they stay 'awaiting_scorecard'."""
    if sent_count > 0 or manual_marked:
        return "sent"
    if comm_required and (gmail_status == "found" or (markaz_comms or 0) > 0):
        return "sent"
    if ignored:
        return "ignored"
    if comm_required and gmail_status == "uncertain":
        return "needs_review"
    if active_count > 0:
        return "in_progress"
    if comm_required and is_high_priority:
        return "high_priority"
    if comm_required:
        return "needs_comms"
    # Not decided yet -> mirror the Markaz pipeline stage.
    return _STAGE_DISPLAY.get(status or "", "awaiting_scorecard")


# ── Shared CTE chain ─────────────────────────────────────────────────────────
# `base` + `classified` are the LEGACY logic, unchanged (regression-safe).
# `enriched` + `flagged` + `displayed` add the Gmail-evidence + comm-required
# dimensions on top, without altering `bucket`.
_CLASSIFIED_CTE = """
WITH base AS (
  SELECT
    a.id AS application_id,
    a.candidate_id,
    c.first_name, c.last_name, c.email,
    j.id AS job_pk, j.job_id AS job_code, j.title AS job_title, j.job_status,
    a.status,
    a.applied_at,
    (a.values_scorecard IS NOT NULL) AS values_filled,
    (a.gwc_scorecard IS NOT NULL) AS gwc_filled,
    a.values_interview_result,
    COALESCE(a.values_interview_date, a.gwc_interview_date) AS scorecard_date,
    COALESCE(a.values_interviewer_name, a.gwc_interviewer_name) AS interviewer,
    COALESCE(s.sent_count, 0) AS sent_count,
    COALESCE(s.active_count, 0) AS active_count,
    s.last_sent_at,
    jsonb_array_length(COALESCE(a.communication_history, '[]'::jsonb)) AS prior_platform_comms
  FROM applications a
  JOIN candidates c ON c.id = a.candidate_id
  JOIN jobs j ON j.id = a.job_id
  LEFT JOIN LATERAL (
    SELECT
      count(*) FILTER (WHERE cm.status = 'sent') AS sent_count,
      count(*) FILTER (WHERE cm.status IN ('draft','in_review','approved')) AS active_count,
      max(cm.sent_at) FILTER (WHERE cm.status = 'sent') AS last_sent_at
    FROM communications cm
    WHERE cm.application_id = a.id
  ) s ON true
),
classified AS (
  SELECT base.*,
    CASE
      WHEN NOT (values_filled OR gwc_filled) THEN 'awaiting_scorecard'
      WHEN sent_count > 0 THEN 'sent'
      WHEN active_count > 0 THEN 'in_progress'
      ELSE 'needs_comms'
    END AS bucket
  FROM base
)
"""

_ENRICHED_CTE = (
    _CLASSIFIED_CTE
    + """
, enriched AS (
  SELECT classified.*,
    EXTRACT(DAY FROM (now() - applied_at))::int AS days_waiting,
    COALESCE(ev.gmail_status, 'not_checked') AS gmail_status,
    ev.match_method, ev.matched_message_id, ev.gmail_thread_id, ev.internal_date,
    ev.matched_subject, ev.matched_to, ev.matched_snippet, ev.uncertain_reason,
    ev.marked_sent_at, ev.marked_sent_by, ev.marked_sent_reason,
    (ev.marked_sent_at IS NOT NULL) AS manual_marked,
    COALESCE(ev.ignored, false) AS ignored,
    ev.checked_at AS evidence_checked_at,
    (status = 'rejected' OR status IN ('warm_bench','consider_other_roles')) AS comm_required,
    CASE
      WHEN status = 'rejected' AND gwc_filled THEN 'gwc_rejection'
      WHEN status = 'rejected' AND values_filled THEN 'values_feedback'
      WHEN status = 'rejected' THEN 'cv_rejection'
      WHEN status IN ('warm_bench','consider_other_roles') THEN 'warm_bench'
      ELSE NULL
    END AS required_email_type
  FROM classified
  LEFT JOIN coco.comm_evidence ev ON ev.application_id = classified.application_id
),
flagged AS (
  SELECT enriched.*,
    -- Evidence = ANY of: app-sent / manual override / Gmail match / Markaz log.
    -- BOTH Gmail and Markaz are always referenced (prior_platform_comms is the
    -- Markaz communication_history count) — see RAILWAY_DEPLOYMENT_LESSONS.md.
    (sent_count > 0 OR manual_marked OR gmail_status = 'found' OR prior_platform_comms > 0) AS has_evidence,
    (comm_required AND active_count = 0 AND sent_count = 0 AND NOT manual_marked
       AND gmail_status NOT IN ('found','uncertain') AND prior_platform_comms = 0
       AND NOT ignored AND COALESCE(days_waiting, 0) > 7) AS is_high_priority,
    (comm_required OR sent_count > 0 OR active_count > 0
       OR status IN ('shortlisted','gwc_scheduled','case_study_sent','P2')) AS comms_relevant
  FROM enriched
),
displayed AS (
  SELECT flagged.*,
    CASE
      -- A deliberate app-send or a human "mark sent" is always Sent.
      WHEN sent_count > 0 OR manual_marked THEN 'sent'
      -- External evidence (Gmail / Markaz log) counts as Sent ONLY for candidates
      -- who actually need a rejection/feedback. For a not-yet-decided candidate
      -- (shortlisted, scheduled, etc.) an email on record is an interview INVITE,
      -- not their decision — so they stay "Awaiting scorecard", not "Sent".
      WHEN comm_required AND (gmail_status = 'found' OR prior_platform_comms > 0) THEN 'sent'
      WHEN ignored THEN 'ignored'
      WHEN comm_required AND gmail_status = 'uncertain' THEN 'needs_review'
      WHEN active_count > 0 THEN 'in_progress'
      WHEN comm_required AND is_high_priority THEN 'high_priority'
      WHEN comm_required THEN 'needs_comms'
      -- Not decided yet: mirror the Markaz pipeline stage instead of a generic
      -- label, so an invited/shortlisted candidate reads "Shortlisted", never "Sent".
      WHEN status = 'shortlisted' THEN 'shortlisted'
      WHEN status = 'gwc_scheduled' THEN 'interview_scheduled'
      WHEN status = 'case_study_sent' THEN 'case_study'
      ELSE 'awaiting_scorecard'
    END AS display_status
  FROM flagged
)
"""
)

# Filter predicates over the `displayed` CTE. Legacy values (all/scored/sent/
# in_progress/awaiting_scorecard) keep their original meaning; the new values
# scope to the comms-relevant population.
_BUCKET_PREDICATE = """
  CASE :bucket
    WHEN 'all' THEN true
    WHEN 'relevant' THEN comms_relevant
    WHEN 'scored' THEN (values_filled OR gwc_filled)
    WHEN 'sent' THEN (sent_count > 0)
    WHEN 'already_sent' THEN (display_status = 'sent')
    WHEN 'needs_comms' THEN (comms_relevant AND comm_required AND active_count = 0
        AND NOT has_evidence AND gmail_status <> 'uncertain' AND NOT ignored)
    WHEN 'high_priority' THEN is_high_priority
    WHEN 'needs_review' THEN (comms_relevant AND gmail_status = 'uncertain'
        AND sent_count = 0 AND NOT manual_marked AND NOT ignored)
    WHEN 'in_progress' THEN (active_count > 0 AND sent_count = 0)
    WHEN 'awaiting_scorecard' THEN (comms_relevant AND display_status = 'awaiting_scorecard')
    WHEN 'ignored' THEN (comms_relevant AND ignored)
    ELSE display_status = :bucket
  END
"""


def list_queue(
    db: Session,
    bucket: str = "relevant",
    job_pk: Optional[int] = None,
    q: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    # Build WHERE conditionally so we never pass an untyped NULL bind param
    # (psycopg3 can't infer the type of `:p IS NULL OR col = :p`).
    conditions = [_BUCKET_PREDICATE]
    params: dict = {"bucket": bucket, "limit": limit, "offset": offset}
    if job_pk is not None:
        conditions.append("job_pk = :job_pk")
        params["job_pk"] = job_pk
    if q:
        conditions.append(
            "(lower(coalesce(first_name,'') || ' ' || coalesce(last_name,'')) LIKE :qpat"
            " OR lower(coalesce(email,'')) LIKE :qpat)"
        )
        params["qpat"] = f"%{q.lower()}%"

    where = " AND ".join(c.strip() for c in conditions)
    sql = (
        _ENRICHED_CTE
        + f"""
SELECT * FROM displayed
WHERE {where}
ORDER BY is_high_priority DESC,
         (display_status = 'needs_comms') DESC,
         days_waiting DESC NULLS LAST,
         scorecard_date DESC NULLS LAST,
         application_id DESC
LIMIT :limit OFFSET :offset
"""
    )
    rows = _heal_exec(db, sql, params).mappings().all()
    return [dict(r) for r in rows]


def positions_summary(db: Session) -> list[dict]:
    """Per-position rollup for the queue's top level: positions with at least one
    comms-relevant candidate, with display-status counts + last Gmail sync."""
    sql = _ENRICHED_CTE + """
SELECT job_pk, job_code, job_title,
  count(*) FILTER (WHERE display_status IN ('needs_comms','high_priority')) AS needs_comms,
  count(*) FILTER (WHERE display_status = 'high_priority') AS high_priority,
  count(*) FILTER (WHERE display_status = 'in_progress') AS in_progress,
  count(*) FILTER (WHERE display_status = 'sent') AS sent,
  count(*) FILTER (WHERE display_status = 'needs_review') AS needs_review,
  count(*) FILTER (WHERE display_status = 'shortlisted') AS shortlisted,
  count(*) FILTER (WHERE display_status = 'awaiting_scorecard') AS awaiting_scorecard,
  count(*) FILTER (WHERE values_filled OR gwc_filled) AS scored,
  count(*) AS total,
  max(evidence_checked_at) AS last_gmail_sync_at
FROM displayed
WHERE comms_relevant
GROUP BY job_pk, job_code, job_title
ORDER BY high_priority DESC, needs_comms DESC, total DESC
"""
    rows = _heal_exec(db, sql).mappings().all()
    return [dict(r) for r in rows]


def queue_stats(db: Session) -> dict:
    sql = _ENRICHED_CTE + """
SELECT
  count(*) FILTER (WHERE display_status IN ('needs_comms','high_priority')) AS needs_comms,
  count(*) FILTER (WHERE display_status = 'high_priority') AS high_priority,
  count(*) FILTER (WHERE display_status = 'in_progress') AS in_progress,
  count(*) FILTER (WHERE display_status = 'sent') AS sent,
  count(*) FILTER (WHERE display_status = 'needs_review') AS needs_review,
  count(*) FILTER (WHERE display_status = 'shortlisted') AS shortlisted,
  count(*) FILTER (WHERE display_status = 'awaiting_scorecard') AS awaiting_scorecard,
  count(*) FILTER (WHERE display_status = 'ignored') AS ignored,
  count(*) FILTER (WHERE values_filled OR gwc_filled) AS scored,
  count(*) AS total
FROM displayed
WHERE comms_relevant
"""
    row = _heal_exec(db, sql).mappings().first()
    r = dict(row) if row else {}
    # Overall volume (whole Markaz, not just comms-relevant) for the dashboard strip.
    o = db.execute(
        text(
            """
            SELECT
              (SELECT count(*) FROM applications) AS total_applications,
              (SELECT count(*) FROM candidates) AS total_candidates,
              (SELECT count(*) FROM jobs WHERE job_status = 'Active') AS open_positions
            """
        )
    ).mappings().first() or {}
    return {
        "needs_comms": int(r.get("needs_comms", 0) or 0),
        "high_priority": int(r.get("high_priority", 0) or 0),
        "in_progress": int(r.get("in_progress", 0) or 0),
        "sent": int(r.get("sent", 0) or 0),
        "needs_review": int(r.get("needs_review", 0) or 0),
        "shortlisted": int(r.get("shortlisted", 0) or 0),
        "awaiting_scorecard": int(r.get("awaiting_scorecard", 0) or 0),
        "ignored": int(r.get("ignored", 0) or 0),
        "scored": int(r.get("scored", 0) or 0),
        "total": int(r.get("total", 0) or 0),
        "total_applications": int(o.get("total_applications", 0) or 0),
        "total_candidates": int(o.get("total_candidates", 0) or 0),
        "open_positions": int(o.get("open_positions", 0) or 0),
    }


def last_sync_at(db: Session) -> Optional[str]:
    """Most recent successful Gmail sync finish time (for the 'last synced' chip)."""
    sql = """
    SELECT max(finished_at) AS ts
    FROM coco.gmail_sync_runs
    WHERE status IN ('ok','partial')
    """
    row = _heal_exec(db, sql).mappings().first()
    return row["ts"] if row and row["ts"] else None


def get_application(db: Session, application_id: int) -> Optional[dict]:
    """Single-application detail: the enriched row + detail-only columns
    (phone, stage, interview dates, Markaz communication_history)."""
    sql = _ENRICHED_CTE + """
    SELECT d.*,
      c.phone, a.stage,
      a.values_interview_date, a.values_interviewer_name,
      a.gwc_interview_result, a.gwc_interview_date, a.gwc_interviewer_name,
      a.communication_history
    FROM displayed d
    JOIN applications a ON a.id = d.application_id
    JOIN candidates c ON c.id = d.candidate_id
    WHERE d.application_id = :app_id
    """
    row = _heal_exec(db, sql, {"app_id": application_id}).mappings().first()
    return dict(row) if row else None


def get_scorecards_raw(db: Session, application_id: int) -> Optional[dict]:
    sql = """
    SELECT values_scorecard, gwc_scorecard
    FROM applications WHERE id = :app_id
    """
    row = db.execute(text(sql), {"app_id": application_id}).mappings().first()
    return dict(row) if row else None


def hiring_manager_email(db: Session, job_pk: Optional[int]) -> Optional[str]:
    """Email of the hiring manager for a job (Markaz jobs.hiring_manager -> users.id
    -> users.email). Used to CC the hiring manager on LIVE candidate sends."""
    if not job_pk:
        return None
    row = _heal_exec(
        db,
        "SELECT lower(u.email) AS email FROM jobs j JOIN users u ON u.id = j.hiring_manager "
        "WHERE j.id = :j AND u.email IS NOT NULL",
        {"j": job_pk},
    ).mappings().first()
    return row["email"] if row and row["email"] else None


def list_jobs(db: Session, active_only: bool = True) -> list[dict]:
    sql = """
    SELECT j.id AS job_pk, j.job_id AS job_code, j.title, j.job_status, j.department
    FROM jobs j
    {where}
    ORDER BY j.title
    """.format(where="WHERE j.job_status = 'Active'" if active_only else "")
    rows = db.execute(text(sql)).mappings().all()
    return [dict(r) for r in rows]
