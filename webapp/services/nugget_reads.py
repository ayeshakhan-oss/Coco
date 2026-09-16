"""Read-only access to Nugget's screening results.

Technical roles are screened by Nugget (Aymen Abid's agent), which owns the
`public.nugget_screening_*` tables. Coco reads them and never writes: rubric
changes, re-runs and tier changes go to Aymen.

See .claude/skills/02_candidate-evaluation/technical-screening.md.
"""

from __future__ import annotations

import re
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

# The `nugget_deg` schema holds the same table names and is EMPTY. Always public.
SCHEMA = "public"

READ_ONLY_PREFIXES = ("select", "with")

# Strip SQL comments before any check runs, so a keyword or semicolon sitting
# inside a comment can't produce a false block, and so a comment can't be used
# to try to hide text from the checks below.
_COMMENT_RE = re.compile(r"/\*.*?\*/|--[^\n]*", re.DOTALL)

# Anywhere in the statement, case-insensitive, word-bounded. INTO is included
# to catch `SELECT ... INTO new_table`, which is DDL despite starting SELECT.
_FORBIDDEN_KEYWORDS_RE = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|GRANT|REVOKE|COPY|MERGE|INTO)\b",
    re.IGNORECASE,
)


def assert_read_only(sql: str) -> None:
    """Raise unless `sql` is a plain read.

    This is a defence-in-depth STRING check, not a database-level guarantee. It:
      1. strips `/* */` and `--` comments so they can't hide a keyword or a
         semicolon from the checks below;
      2. rejects the statement outright if it contains a `;` other than a
         single optional trailing one (multi-statement SQL is refused);
      3. requires the statement to open with SELECT or WITH;
      4. rejects INSERT/UPDATE/DELETE/DROP/TRUNCATE/ALTER/CREATE/GRANT/REVOKE/
         COPY/MERGE/INTO anywhere in the statement, so a write or DDL clause
         nested inside a CTE (`WITH x AS (DELETE ... RETURNING *) SELECT ...`)
         or appended after the leading SELECT (`SELECT * INTO shadow FROM ...`)
         is also caught.

    What it does NOT guarantee: it cannot see through a stored procedure or
    function call that itself writes, and it is a string check, not a parser,
    so it can still be fooled by SQL this simple pattern-matching can't parse.
    The durable guarantee is a read-only database role on the connection Coco
    uses against `public.nugget_screening_*`; this guard is a second,
    application-layer line of defence, not a substitute for that role.
    """
    without_comments = _COMMENT_RE.sub(" ", sql)
    trimmed = without_comments.strip()
    if trimmed.endswith(";"):
        trimmed = trimmed[:-1].rstrip()
    if ";" in trimmed:
        raise PermissionError(
            "nugget_reads is READ ONLY: multi-statement SQL is rejected."
        )

    stripped = trimmed.lstrip().lower()
    if not stripped.startswith(READ_ONLY_PREFIXES):
        raise PermissionError(
            "nugget_reads is READ ONLY: public.nugget_screening_* belongs to Nugget."
        )

    if _FORBIDDEN_KEYWORDS_RE.search(trimmed):
        raise PermissionError(
            "nugget_reads is READ ONLY: statement contains a write/DDL keyword."
        )


def _rows(db: Session, sql: str, **params: Any) -> list[dict]:
    assert_read_only(sql)
    result = db.execute(text(sql), params)
    return [dict(r) for r in result.mappings()]


# The four queries this module issues, as module-level constants so both the
# functions below and the regression tests read the exact same SQL — a test
# that only compares against a pasted duplicate can silently drift from the
# real query and stop catching anything.
LIST_SCREENED_JOBS_SQL = f"""
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
"""


def list_screened_jobs(db: Session) -> list[dict]:
    """Every job Nugget holds a rubric for, with current eval counts."""
    return _rows(db, LIST_SCREENED_JOBS_SQL)


# Published tier order. UNUSABLE is last and is NOT a ranking position: it means
# the CV could not be read, so it is never a rejection and never a zero score.
TIER_ORDER = ("P1", "P2", "P3", "P4", "MANUAL_REVIEW", "UNUSABLE")

# Tiers whose score is meaningless and must never render as a percentage.
# UNUSABLE: the CV could not be extracted at all. MANUAL_REVIEW: the rubric's
# `manual_review_rules` (min_resume_chars / min_resume_health) routed the
# candidate here precisely because the extracted text fell below the
# readability floor, not because they scored low, so score_pct/avg_pct sit at
# 0.00 as an artefact, not a measurement. Both need a human to open the actual
# document rather than trust the number.
UNSCORED_TIERS = ("UNUSABLE", "MANUAL_REVIEW")


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
        is_unscored = is_unusable or tier in UNSCORED_TIERS
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
                # An average over unreadable/below-floor documents is noise, not a score.
                "avg_pct": None if is_unscored else row.get("avg_pct"),
                "min_pct": None if is_unscored else row.get("min_pct"),
                "max_pct": None if is_unscored else row.get("max_pct"),
                "is_unusable": is_unusable,
                "is_unscored": is_unscored,
            }
        )

    return {"tiers": tiers, "scored": scored, "unusable": unusable, "total": scored + unusable}


JOB_SUMMARY_SQL = f"""
SELECT tier, status, COUNT(*) AS n,
       ROUND(AVG(score_pct), 1) AS avg_pct,
       MIN(score_pct) AS min_pct,
       MAX(score_pct) AS max_pct
FROM {SCHEMA}.nugget_screening_evals
WHERE job_id = :job_id AND is_current
GROUP BY tier, status
"""


def job_summary(db: Session, job_id: int) -> dict:
    rows = _rows(db, JOB_SUMMARY_SQL, job_id=job_id)
    return shape_summary(rows)


def _mark_unusable(row: dict) -> dict:
    """Convert the raw `status` column into `is_unusable`, and null out
    `score_pct` whenever the row is unscored (unusable OR a tier in
    UNSCORED_TIERS, e.g. MANUAL_REVIEW) so a document nobody could read, or
    one that never cleared the readability floor, never renders as a 0.00
    score. Shared by `candidates_for_job` and `evaluation_for_application` so
    the suppression rule can't drift between the two call sites."""
    row["is_unusable"] = row.pop("status") == "unusable"
    row["is_unscored"] = row["is_unusable"] or row.get("tier") in UNSCORED_TIERS
    if row["is_unscored"]:
        row["score_pct"] = None
    return row


def is_valid_tier(tier: Any) -> bool:
    """Exact match against the published tiers. Case-sensitive on purpose: the
    value is interpolated nowhere, but an unknown tier should 400, not return []."""
    return isinstance(tier, str) and tier in TIER_ORDER


# NOTE: the tier filter uses CAST(:tier AS text), not `:tier::text`. SQLAlchemy's
# text() parses bind parameters with a regex that does not recognise a name
# immediately followed by Postgres's `::` cast operator — `:tier::text` reads
# as literal text to SQLAlchemy, `tier` is never registered as a bind, and
# psycopg then raises a SyntaxError at the bare `:` at execution time. A bare
# `:tier IS NULL` doesn't work either: with no cast, psycopg can't infer the
# parameter's type and raises AmbiguousParameter. CAST(:tier AS text) is the
# one form both SQLAlchemy and Postgres accept — do not "simplify" this back
# to `::`.
CANDIDATES_FOR_JOB_SQL = f"""
SELECT application_id, candidate_id, candidate_name, candidate_email,
       score_pct, tier, tier_reason, confidence, resume_health, status
FROM {SCHEMA}.nugget_screening_evals
WHERE job_id = :job_id AND is_current
  AND (CAST(:tier AS text) IS NULL OR tier = CAST(:tier AS text))
ORDER BY (status = 'unusable'), score_pct DESC NULLS LAST
LIMIT :limit OFFSET :offset
"""


def candidates_for_job(
    db: Session,
    job_id: int,
    tier: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    rows = _rows(
        db,
        CANDIDATES_FOR_JOB_SQL,
        job_id=job_id,
        tier=tier,
        limit=limit,
        offset=offset,
    )
    return [_mark_unusable(r) for r in rows]


EVALUATION_FOR_APPLICATION_SQL = f"""
SELECT e.application_id, e.candidate_id, e.candidate_name, e.candidate_email,
       e.score_pct, e.tier, e.tier_reason, e.confidence, e.resume_health,
       e.status, e.dimension_scores, e.strengths, e.gaps,
       e.hard_filter_flags, e.verdict, e.rubric_version, e.model, e.evaluated_at
FROM {SCHEMA}.nugget_screening_evals e
WHERE e.application_id = :application_id AND e.is_current
LIMIT 1
"""


def evaluation_for_application(db: Session, application_id: int) -> Optional[dict]:
    rows = _rows(db, EVALUATION_FOR_APPLICATION_SQL, application_id=application_id)
    if not rows:
        return None
    return _mark_unusable(rows[0])
