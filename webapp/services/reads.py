"""Read queries against the (read-only) Talent-Acquisition tables, plus the
app-owned `communications` table, to drive the dashboard.

Bucket logic (the user's headline requirement):
  - awaiting_scorecard : no values_scorecard and no gwc_scorecard
  - needs_comms        : scorecard filled AND no communication of any type yet
  - in_progress        : scorecard filled AND a draft/in_review/approved comm exists
  - sent               : scorecard filled AND a sent comm exists
  - scored             : any of needs_comms/in_progress/sent (has a scorecard)

`communication_history` (the Markaz platform's own email log) is surfaced as
*context* (prior_platform_comms count + the History view), never as a
rejection/feedback "sent" flag — those are ambiguous template types.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

# Shared CTE: classify every application into a bucket.
_CLASSIFIED_CTE = """
WITH base AS (
  SELECT
    a.id AS application_id,
    a.candidate_id,
    c.first_name, c.last_name, c.email,
    j.id AS job_pk, j.job_id AS job_code, j.title AS job_title, j.job_status,
    a.status,
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

_BUCKET_PREDICATE = """
  CASE :bucket
    WHEN 'all' THEN true
    WHEN 'scored' THEN (values_filled OR gwc_filled)
    ELSE bucket = :bucket
  END
"""


def list_queue(
    db: Session,
    bucket: str = "scored",
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
        _CLASSIFIED_CTE
        + f"""
SELECT * FROM classified
WHERE {where}
ORDER BY scorecard_date DESC NULLS LAST, application_id DESC
LIMIT :limit OFFSET :offset
"""
    )
    rows = db.execute(text(sql), params).mappings().all()
    return [dict(r) for r in rows]


def positions_summary(db: Session) -> list[dict]:
    """Per-position rollup for the queue's top level: only positions that have at
    least one scorecard-filled candidate, with bucket counts."""
    sql = _CLASSIFIED_CTE + """
SELECT job_pk, job_code, job_title,
  count(*) FILTER (WHERE bucket = 'needs_comms') AS needs_comms,
  count(*) FILTER (WHERE bucket = 'in_progress') AS in_progress,
  count(*) FILTER (WHERE bucket = 'sent') AS sent,
  count(*) FILTER (WHERE bucket IN ('needs_comms','in_progress','sent')) AS scored
FROM classified
GROUP BY job_pk, job_code, job_title
HAVING count(*) FILTER (WHERE bucket IN ('needs_comms','in_progress','sent')) > 0
ORDER BY needs_comms DESC, scored DESC
"""
    rows = db.execute(text(sql)).mappings().all()
    return [dict(r) for r in rows]


def queue_stats(db: Session) -> dict:
    sql = _CLASSIFIED_CTE + "SELECT bucket, count(*) AS n FROM classified GROUP BY bucket"
    rows = db.execute(text(sql)).mappings().all()
    counts = {r["bucket"]: int(r["n"]) for r in rows}
    needs = counts.get("needs_comms", 0)
    in_progress = counts.get("in_progress", 0)
    sent = counts.get("sent", 0)
    awaiting = counts.get("awaiting_scorecard", 0)
    return {
        "needs_comms": needs,
        "in_progress": in_progress,
        "sent": sent,
        "awaiting_scorecard": awaiting,
        "scored": needs + in_progress + sent,
        "total": needs + in_progress + sent + awaiting,
    }


def get_application(db: Session, application_id: int) -> Optional[dict]:
    sql = """
    SELECT
      a.id AS application_id, a.candidate_id,
      c.first_name, c.last_name, c.email, c.phone,
      j.id AS job_pk, j.job_id AS job_code, j.title AS job_title, j.job_status,
      a.status, a.stage,
      (a.values_scorecard IS NOT NULL) AS values_filled,
      (a.gwc_scorecard IS NOT NULL) AS gwc_filled,
      a.values_interview_result, a.values_interview_date, a.values_interviewer_name,
      a.gwc_interview_result, a.gwc_interview_date, a.gwc_interviewer_name,
      a.communication_history
    FROM applications a
    JOIN candidates c ON c.id = a.candidate_id
    JOIN jobs j ON j.id = a.job_id
    WHERE a.id = :app_id
    """
    row = db.execute(text(sql), {"app_id": application_id}).mappings().first()
    return dict(row) if row else None


def get_scorecards_raw(db: Session, application_id: int) -> Optional[dict]:
    sql = """
    SELECT values_scorecard, gwc_scorecard
    FROM applications WHERE id = :app_id
    """
    row = db.execute(text(sql), {"app_id": application_id}).mappings().first()
    return dict(row) if row else None


def list_jobs(db: Session, active_only: bool = True) -> list[dict]:
    sql = """
    SELECT j.id AS job_pk, j.job_id AS job_code, j.title, j.job_status, j.department
    FROM jobs j
    {where}
    ORDER BY j.title
    """.format(where="WHERE j.job_status = 'Active'" if active_only else "")
    rows = db.execute(text(sql)).mappings().all()
    return [dict(r) for r in rows]
