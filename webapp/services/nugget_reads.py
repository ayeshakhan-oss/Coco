"""Read-only access to Nugget's screening results.

Technical roles are screened by Nugget (Aymen Abid's agent), which owns the
`public.nugget_screening_*` tables. Coco reads them and never writes: rubric
changes, re-runs and tier changes go to Aymen.

See .claude/skills/02_candidate-evaluation/technical-screening.md.
"""

from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

# The `nugget_deg` schema holds the same table names and is EMPTY. Always public.
SCHEMA = "public"

READ_ONLY_PREFIXES = ("select", "with")


def assert_read_only(sql: str) -> None:
    """Raise unless `sql` is a plain read. These are not Coco's tables."""
    stripped = sql.lstrip().lower()
    if not stripped.startswith(READ_ONLY_PREFIXES):
        raise PermissionError(
            "nugget_reads is READ ONLY: public.nugget_screening_* belongs to Nugget."
        )


def _rows(db: Session, sql: str, **params: Any) -> list[dict]:
    assert_read_only(sql)
    result = db.execute(text(sql), params)
    return [dict(r) for r in result.mappings()]


def list_screened_jobs(db: Session) -> list[dict]:
    """Every job Nugget holds a rubric for, with current eval counts."""
    return _rows(
        db,
        f"""
        SELECT r.job_id,
               j.title AS job_title,
               r.version AS rubric_version,
               r.status  AS rubric_status,
               r.seniority,
               COUNT(*) FILTER (WHERE e.status = 'scored')   AS scored,
               COUNT(*) FILTER (WHERE e.status = 'unusable') AS unusable,
               MAX(e.evaluated_at) AS last_run_at
        FROM {SCHEMA}.nugget_screening_rubrics r
        LEFT JOIN {SCHEMA}.jobs j ON j.id = r.job_id
        LEFT JOIN {SCHEMA}.nugget_screening_evals e
               ON e.job_id = r.job_id AND e.is_current
        GROUP BY r.job_id, j.title, r.version, r.status, r.seniority
        ORDER BY scored DESC
        """,
    )


# Published tier order. UNUSABLE is last and is NOT a ranking position: it means
# the CV could not be read, so it is never a rejection and never a zero score.
TIER_ORDER = ("P1", "P2", "P3", "P4", "MANUAL_REVIEW", "UNUSABLE")


def shape_summary(rows: list[dict]) -> dict:
    """Order tier buckets and separate unusable from scored. Pure."""
    by_tier = {r["tier"]: r for r in rows}
    tiers: list[dict] = []
    scored = 0
    unusable = 0

    for tier in TIER_ORDER:
        row = by_tier.get(tier)
        if row is None:
            continue
        is_unusable = row.get("status") == "unusable"
        n = int(row.get("n") or 0)
        if is_unusable:
            unusable += n
        else:
            scored += n
        tiers.append(
            {
                "tier": tier,
                "status": row.get("status"),
                "n": n,
                # An average over unreadable documents is noise, not a score.
                "avg_pct": None if is_unusable else row.get("avg_pct"),
                "min_pct": None if is_unusable else row.get("min_pct"),
                "max_pct": None if is_unusable else row.get("max_pct"),
                "is_unusable": is_unusable,
            }
        )

    return {"tiers": tiers, "scored": scored, "unusable": unusable, "total": scored + unusable}


def job_summary(db: Session, job_id: int) -> dict:
    rows = _rows(
        db,
        f"""
        SELECT tier, status, COUNT(*) AS n,
               ROUND(AVG(score_pct), 1) AS avg_pct,
               MIN(score_pct) AS min_pct,
               MAX(score_pct) AS max_pct
        FROM {SCHEMA}.nugget_screening_evals
        WHERE job_id = :job_id AND is_current
        GROUP BY tier, status
        """,
        job_id=job_id,
    )
    return shape_summary(rows)


def is_valid_tier(tier: Any) -> bool:
    """Exact match against the published tiers. Case-sensitive on purpose: the
    value is interpolated nowhere, but an unknown tier should 400, not return []."""
    return isinstance(tier, str) and tier in TIER_ORDER


def candidates_for_job(
    db: Session,
    job_id: int,
    tier: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    rows = _rows(
        db,
        f"""
        SELECT application_id, candidate_id, candidate_name, candidate_email,
               score_pct, tier, tier_reason, confidence, resume_health, status
        FROM {SCHEMA}.nugget_screening_evals
        WHERE job_id = :job_id AND is_current
          AND (:tier::text IS NULL OR tier = :tier::text)
        ORDER BY (status = 'unusable'), score_pct DESC NULLS LAST
        LIMIT :limit OFFSET :offset
        """,
        job_id=job_id,
        tier=tier,
        limit=limit,
        offset=offset,
    )
    for r in rows:
        r["is_unusable"] = r.pop("status") == "unusable"
        if r["is_unusable"]:
            r["score_pct"] = None  # never show 0.00 for a document nobody could read
    return rows


def evaluation_for_application(db: Session, application_id: int) -> Optional[dict]:
    rows = _rows(
        db,
        f"""
        SELECT e.application_id, e.candidate_id, e.candidate_name, e.candidate_email,
               e.score_pct, e.tier, e.tier_reason, e.confidence, e.resume_health,
               e.status, e.dimension_scores, e.strengths, e.gaps,
               e.hard_filter_flags, e.verdict, e.rubric_version, e.model, e.evaluated_at
        FROM {SCHEMA}.nugget_screening_evals e
        WHERE e.application_id = :application_id AND e.is_current
        LIMIT 1
        """,
        application_id=application_id,
    )
    if not rows:
        return None
    row = rows[0]
    row["is_unusable"] = row.pop("status") == "unusable"
    if row["is_unusable"]:
        row["score_pct"] = None
    return row
