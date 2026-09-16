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
