"""Planning, launching and executing a technical screening run.

Coco writes into Nugget's tables through `nugget_writes` (see that module for
why the read-only rule was lifted and what replaced it). Nothing here invents a
scoring rule: the rubric row carries its own `system_prompt` and
`output_schema`, so a run Coco executes is scored by exactly the contract
Nugget published for that job.

WHY A RUN IS DRIVEN FROM THE BROWSER.
Each candidate is a model call of roughly twelve seconds, so 369 candidates is
over an hour and no single HTTP request survives that. `work()` does a few
candidates per call and the page loops, reusing `frontend/src/lib/screenAll.ts`
whose retry budget is sized for a Railway redeploy. The durable state is in the
database: `nugget_screening_run_items.state` per candidate, so a lost request
costs one slice, never the run.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from . import cv_text, nugget_writes, pricing, tech_tiering
from .nugget_writes import schema

log = logging.getLogger("webapp.screening_runs")

MODES = ("new_only", "backlog", "window", "rescore", "single")
EFFORTS = ("low", "medium", "high", "xhigh", "max")

# Markaz's own tables are ALWAYS in `public`, whatever NUGGET_SCHEMA says. Only
# the eight nugget_screening_* tables move, and `nugget_worker_test` carries no
# jobs, applications or candidates at all -- so qualifying a Markaz table with
# the configurable schema silently breaks every integration test.
MARKAZ_SCHEMA = "public"

# How many consecutive item failures carrying the same non-retryable cause
# pause the run. Run 21308392 made 369 doomed API calls because nothing
# noticed that the first one had said "the Anthropic account has no credit".
CONSECUTIVE_FAILURE_LIMIT = 5

# Items claimed but not finished within this are handed back. A request killed
# by a redeploy leaves its claim behind, and without this the run would stall
# with work nobody owns. `idx_nsri_stuck` indexes exactly this query.
STUCK_AFTER_MINUTES = 10
MAX_ATTEMPTS = 3

# Used only in the pre-run estimate, for candidates with no cached extraction.
DEFAULT_CV_CHARS = 4000


class RunError(RuntimeError):
    pass


class NoActiveRubric(RunError):
    pass


class RunConflict(RunError):
    """A live run already exists for this job (uq_nsrun_one_active_per_job)."""


def _rows(db: Session, sql: str, **params) -> list[dict]:
    return [dict(r) for r in db.execute(text(sql), params).mappings()]


def _one(db: Session, sql: str, **params) -> Optional[dict]:
    rows = _rows(db, sql, **params)
    return rows[0] if rows else None


# --------------------------------------------------------------------------
# Rubrics
# --------------------------------------------------------------------------


def active_rubric(db: Session, job_id: int) -> Optional[dict]:
    sql = f"""
    SELECT id, job_id, version, status, title, seniority, min_years,
           dimensions, max_score, hard_filters, thresholds,
           manual_review_rules, system_prompt, output_schema, source,
           created_by, activated_at
    FROM {schema()}.nugget_screening_rubrics
    WHERE job_id = :job_id AND status = 'active'
    """
    return _one(db, sql, job_id=job_id)


def rubric_summary(rubric: Optional[dict]) -> Optional[dict]:
    """What step 2 of the wizard shows."""
    if not rubric:
        return None
    thresholds = rubric.get("thresholds") or {}
    return {
        "id": str(rubric["id"]),
        "version": rubric["version"],
        "title": rubric.get("title"),
        "seniority": rubric.get("seniority"),
        "min_years": float(rubric["min_years"]) if rubric.get("min_years") is not None else None,
        "dimensions": [
            {
                "key": d.get("key"),
                "label": d.get("label") or d.get("key"),
                "weight": d.get("weight"),
                "core": d.get("core"),
            }
            for d in (rubric.get("dimensions") or [])
        ],
        "max_score": float(rubric.get("max_score") or 0),
        "thresholds": thresholds,
        "hard_filters": [
            {"key": f.get("key"), "label": f.get("label"), "action": f.get("action")}
            for f in (rubric.get("hard_filters") or [])
        ],
        "source": rubric.get("source"),
        "created_by": rubric.get("created_by"),
        "activated_at": rubric.get("activated_at"),
    }


_ARCHIVE_ACTIVE_RUBRIC = nugget_writes.register(
    "UPDATE {schema}.nugget_screening_rubrics "
    "SET status = 'archived', updated_at = now() "
    "WHERE job_id = :job_id AND status = 'active'"
)

_INSERT_RUBRIC = nugget_writes.register(
    "INSERT INTO {schema}.nugget_screening_rubrics "
    "(job_id, version, status, title, seniority, min_years, jd_source, "
    " jd_snapshot, jd_fetched_at, custom_questions, dimensions, max_score, "
    " hard_filters, thresholds, manual_review_rules, system_prompt, "
    " system_prompt_hash, output_schema, drafted_by_model, source, created_by, "
    " activated_at, activated_by, notes) "
    "VALUES (:job_id, :version, 'active', :title, :seniority, :min_years, "
    " :jd_source, :jd_snapshot, now(), CAST(:custom_questions AS jsonb), "
    " CAST(:dimensions AS jsonb), :max_score, CAST(:hard_filters AS jsonb), "
    " CAST(:thresholds AS jsonb), CAST(:manual_review_rules AS jsonb), "
    " :system_prompt, :system_prompt_hash, CAST(:output_schema AS jsonb), "
    " :drafted_by_model, :source, :created_by, now(), :created_by, :notes) "
    "RETURNING id, version"
)


def publish_rubric(db: Session, *, job_id: int, draft: dict, created_by: str) -> dict:
    """Publish a drafted rubric as the job's active version.

    🔴 ONE TRANSACTION. `uq_nsr_active_per_job` is a partial unique index on
    (job_id) WHERE status='active', so inserting the new row before archiving
    the old one raises. Archiving first and inserting second in SEPARATE
    transactions would leave a job with NO active rubric if the insert failed,
    which reads to every other query as "this job was never screened". The
    caller commits.
    """
    current = active_rubric(db, job_id)
    next_version = (current["version"] + 1) if current else 1

    nugget_writes.execute(db, _ARCHIVE_ACTIVE_RUBRIC, job_id=job_id)

    prompt = draft["system_prompt"]
    row = nugget_writes.execute(
        db,
        _INSERT_RUBRIC,
        job_id=job_id,
        version=next_version,
        title=draft["title"],
        seniority=draft.get("seniority"),
        min_years=draft.get("min_years"),
        jd_source=draft.get("jd_source", "neon_description"),
        jd_snapshot=draft["jd_snapshot"],
        custom_questions=json.dumps(draft.get("custom_questions") or []),
        dimensions=json.dumps(draft["dimensions"]),
        max_score=draft.get("max_score", 100),
        hard_filters=json.dumps(draft.get("hard_filters") or []),
        thresholds=json.dumps(draft["thresholds"]),
        manual_review_rules=json.dumps(
            draft.get("manual_review_rules")
            or {"min_resume_chars": 500, "min_resume_health": 60}
        ),
        system_prompt=prompt,
        system_prompt_hash=hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        output_schema=json.dumps(draft["output_schema"]),
        drafted_by_model=draft.get("drafted_by_model"),
        source=draft.get("source", "llm_drafted"),
        created_by=created_by,
        notes=draft.get("notes"),
    ).mappings().first()
    return {"id": str(row["id"]), "version": row["version"]}


# --------------------------------------------------------------------------
# Planning the pool
# --------------------------------------------------------------------------

# One row per CANDIDATE, not per application: `uq_nse_current_per_job_candidate`
# allows exactly one current evaluation per (job, candidate), so a candidate who
# applied twice must be screened once. The newest application wins and the
# others are counted as merged duplicates, which is the "duplicates merged"
# figure the wizard reports.
_POOL_SQL = """
WITH ranked AS (
  SELECT a.id            AS application_id,
         a.candidate_id,
         a.applied_at,
         c.first_name, c.last_name, c.email,
         (c.resume_data IS NOT NULL AND octet_length(c.resume_data) > 0) AS has_cv,
         ROW_NUMBER() OVER (PARTITION BY a.candidate_id
                            ORDER BY a.applied_at DESC NULLS LAST, a.id DESC) AS rn,
         COUNT(*)     OVER (PARTITION BY a.candidate_id) AS applications_by_candidate
  FROM public.applications a
  JOIN public.candidates  c ON c.id = a.candidate_id
  WHERE a.job_id = :job_id
    AND (CAST(:since AS timestamp) IS NULL OR a.applied_at >= CAST(:since AS timestamp))
    AND (CAST(:until AS timestamp) IS NULL OR a.applied_at <= CAST(:until AS timestamp))
)
SELECT r.application_id, r.candidate_id, r.applied_at, r.first_name,
       r.last_name, r.email, r.has_cv, r.applications_by_candidate,
       (e.id IS NOT NULL) AS already_scored
FROM ranked r
LEFT JOIN {schema}.nugget_screening_evals e
       ON e.job_id = :job_id AND e.candidate_id = r.candidate_id AND e.is_current
WHERE r.rn = 1
ORDER BY r.applied_at DESC NULLS LAST, r.application_id DESC
"""


def _filter_by_mode(rows: list[dict], mode: str) -> list[dict]:
    if mode == "new_only":
        return [r for r in rows if not r["already_scored"]]
    if mode == "rescore":
        return [r for r in rows if r["already_scored"]]
    # backlog / window / single take everyone the window already narrowed.
    return rows


def _avg_cv_chars(db: Session, candidate_ids: list[int]) -> int:
    """Average extracted length, from Nugget's own resume cache where it has
    one. Candidates with no cached extraction are counted at DEFAULT_CV_CHARS
    rather than dropped, so the estimate does not quietly shrink to the
    candidates we happen to know about."""
    if not candidate_ids:
        return DEFAULT_CV_CHARS
    sql = f"""
    SELECT AVG(chars)::int AS avg_chars, COUNT(*) AS n
    FROM {schema()}.nugget_screening_resume_cache
    WHERE candidate_id = ANY(:ids) AND parse_success
    """
    row = _one(db, sql, ids=candidate_ids)
    known_n = int(row["n"] or 0) if row else 0
    known_avg = int(row["avg_chars"] or 0) if row and row["avg_chars"] else 0
    if not known_n or not known_avg:
        return DEFAULT_CV_CHARS
    total = len(candidate_ids)
    unknown_n = max(0, total - known_n)
    return int((known_avg * known_n + DEFAULT_CV_CHARS * unknown_n) / total)


def plan_run(
    db: Session,
    *,
    job_id: int,
    mode: str = "new_only",
    since_days: Optional[int] = None,
    window_from: Optional[datetime] = None,
    window_to: Optional[datetime] = None,
    max_candidates: Optional[int] = None,
    model: str,
    use_batch: bool = False,
) -> dict:
    """Step 3 of the wizard. Reads only: nothing is written until Confirm."""
    if mode not in MODES:
        raise RunError(f"unknown mode {mode!r}")
    rubric = active_rubric(db, job_id)
    if not rubric:
        raise NoActiveRubric(f"job {job_id} has no active rubric")

    since = window_from
    if since_days:
        since = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=since_days)

    rows = _rows(
        db,
        _POOL_SQL.format(schema=schema()),
        job_id=job_id,
        since=since,
        until=window_to,
    )
    eligible = _filter_by_mode(rows, mode)
    if max_candidates:
        eligible = eligible[:max_candidates]

    merged = sum(max(0, r["applications_by_candidate"] - 1) for r in eligible)
    no_cv = sum(1 for r in eligible if not r["has_cv"])
    dates = [r["applied_at"] for r in eligible if r["applied_at"]]

    estimate = pricing.estimate_run_cost(
        model=model,
        candidates=len(eligible),
        system_prompt_chars=len(rubric["system_prompt"] or ""),
        avg_cv_chars=_avg_cv_chars(db, [r["candidate_id"] for r in eligible]),
        batch=use_batch,
    )

    return {
        "job_id": job_id,
        "mode": mode,
        "model": model,
        "use_batch": use_batch,
        "rubric_version": rubric["version"],
        "people": len(eligible),
        "duplicates_merged": merged,
        "no_cv": no_cv,
        "newest_application": max(dates).date().isoformat() if dates else None,
        "oldest_application": min(dates).date().isoformat() if dates else None,
        "already_scored_in_pool": sum(1 for r in eligible if r["already_scored"]),
        **estimate,
        "application_ids": [r["application_id"] for r in eligible],
    }


# --------------------------------------------------------------------------
# Creating the run
# --------------------------------------------------------------------------

_INSERT_RUN = nugget_writes.register(
    "INSERT INTO {schema}.nugget_screening_runs "
    "(job_id, rubric_id, rubric_version, mode, status, window_from, window_to, "
    " since_days, max_candidates, selection, model, effort, concurrency, "
    " use_batch, planned_count, est_input_tokens, est_cached_tokens, "
    " est_output_tokens, est_cost_usd, cost_cap_usd, total_items, requested_by) "
    "VALUES (:job_id, :rubric_id, :rubric_version, :mode, 'queued', :window_from, "
    " :window_to, :since_days, :max_candidates, CAST(:selection AS jsonb), :model, "
    " :effort, :concurrency, :use_batch, :planned_count, :est_input_tokens, "
    " :est_cached_tokens, :est_output_tokens, :est_cost_usd, :cost_cap_usd, "
    " :total_items, :requested_by) "
    "RETURNING id"
)

_INSERT_RUN_ITEM = nugget_writes.register(
    "INSERT INTO {schema}.nugget_screening_run_items "
    "(run_id, application_id, candidate_id, dedup_key, applied_at, priority, state) "
    "VALUES (:run_id, :application_id, :candidate_id, :dedup_key, :applied_at, "
    " :priority, 'pending')"
)

_INSERT_EVENT = nugget_writes.register(
    "INSERT INTO {schema}.nugget_screening_run_events (run_id, level, event, detail) "
    "VALUES (:run_id, :level, :event, CAST(:detail AS jsonb))"
)


def log_event(db: Session, run_id: str, event: str, detail: dict, level: str = "info") -> None:
    nugget_writes.execute(
        db,
        _INSERT_EVENT,
        run_id=run_id,
        level=level,
        event=event,
        detail=json.dumps(detail, default=str),
    )


def live_run_for_job(db: Session, job_id: int) -> Optional[dict]:
    """The run blocking a new one, if any. `uq_nsrun_one_active_per_job` covers
    exactly these four statuses, so the wizard can disable Confirm with a
    reason instead of failing on an integrity error at the last step."""
    sql = f"""
    SELECT id, status, created_at, total_items, done_count
    FROM {schema()}.nugget_screening_runs
    WHERE job_id = :job_id
      AND status IN ('planning', 'queued', 'running', 'paused')
    LIMIT 1
    """
    return _one(db, sql, job_id=job_id)


def create_run(
    db: Session,
    *,
    job_id: int,
    plan: dict,
    requested_by: str,
    effort: str = "medium",
    concurrency: int = 4,
    cost_cap_usd: Optional[float] = None,
) -> str:
    """Step 4. The run and all of its items in ONE transaction; the caller
    commits. A run row with no items would present as a finished screening
    that scored nobody."""
    existing = live_run_for_job(db, job_id)
    if existing:
        raise RunConflict(
            f"job {job_id} already has a {existing['status']} run. Finish or "
            "cancel it before starting another."
        )
    rubric = active_rubric(db, job_id)
    if not rubric:
        raise NoActiveRubric(f"job {job_id} has no active rubric")

    application_ids = plan["application_ids"]
    if not application_ids:
        raise RunError("nobody to screen: the planned pool is empty")

    run_id = nugget_writes.execute(
        db,
        _INSERT_RUN,
        job_id=job_id,
        rubric_id=rubric["id"],
        rubric_version=rubric["version"],
        mode=plan["mode"],
        window_from=plan.get("window_from"),
        window_to=plan.get("window_to"),
        since_days=plan.get("since_days"),
        max_candidates=plan.get("max_candidates"),
        selection=json.dumps({"application_ids": application_ids[:5000]}),
        model=plan["model"],
        effort=effort,
        concurrency=concurrency,
        use_batch=plan.get("use_batch", False),
        planned_count=plan["people"],
        est_input_tokens=plan["est_input_tokens"],
        est_cached_tokens=plan["est_cached_tokens"],
        est_output_tokens=plan["est_output_tokens"],
        est_cost_usd=plan["est_cost_usd"],
        cost_cap_usd=cost_cap_usd,
        total_items=len(application_ids),
        requested_by=requested_by,
    ).scalar()

    detail = _rows(
        db,
        _POOL_SQL.format(schema=schema()),
        job_id=job_id,
        since=None,
        until=None,
    )
    by_app = {r["application_id"]: r for r in detail}
    # Priority ascending in the order the plan produced, which is newest first
    # ("The newest are scored first"). idx_nsri_next orders by (run_id, priority).
    for priority, app_id in enumerate(application_ids):
        row = by_app.get(app_id)
        if not row:
            continue
        nugget_writes.execute(
            db,
            _INSERT_RUN_ITEM,
            run_id=run_id,
            application_id=app_id,
            candidate_id=row["candidate_id"],
            dedup_key=f"{job_id}:{row['candidate_id']}",
            applied_at=row["applied_at"],
            priority=priority,
        )

    log_event(
        db,
        run_id,
        "planned",
        {
            "mode": plan["mode"],
            "items": len(application_ids),
            "est_cost_usd": plan["est_cost_usd"],
            "rubric_version": rubric["version"],
        },
    )
    return str(run_id)


# --------------------------------------------------------------------------
# Executing the run
# --------------------------------------------------------------------------

_REAP_STUCK = nugget_writes.register(
    "UPDATE {schema}.nugget_screening_run_items "
    "SET state = 'pending', claimed_at = NULL, claimed_by = NULL "
    "WHERE run_id = :run_id AND state = 'in_progress' "
    "  AND claimed_at < :cutoff AND attempts < :max_attempts "
    "RETURNING id"
)

# FOR UPDATE SKIP LOCKED is what lets Nugget's own worker keep running against
# these tables at the same time: two claimers never take the same row, and
# neither waits on the other.
_CLAIM_ITEMS = nugget_writes.register(
    "UPDATE {schema}.nugget_screening_run_items SET state = 'in_progress', "
    "  claimed_at = now(), claimed_by = :worker, attempts = attempts + 1 "
    "WHERE id IN ( "
    "  SELECT id FROM {schema}.nugget_screening_run_items "
    "  WHERE run_id = :run_id AND state = 'pending' "
    "  ORDER BY priority, id FOR UPDATE SKIP LOCKED LIMIT :limit) "
    "RETURNING id, application_id, candidate_id, attempts"
)

_FINISH_ITEM = nugget_writes.register(
    "UPDATE {schema}.nugget_screening_run_items "
    "SET state = :state, eval_id = :eval_id, skip_reason = :skip_reason, "
    "    error = :error, finished_at = now() "
    "WHERE id = :item_id"
)

_RELEASE_ITEM = nugget_writes.register(
    "UPDATE {schema}.nugget_screening_run_items "
    "SET state = 'pending', claimed_at = NULL, claimed_by = NULL "
    "WHERE id = :item_id"
)

# Supersession is THREE statements, in this order, and the order is forced by
# `uq_nse_current_per_job_candidate` (UNIQUE (job_id, candidate_id) WHERE
# is_current). Inserting the new evaluation first, the way coco.cv_screens
# does it, raises here: two current rows for one candidate cannot coexist even
# for the length of a transaction. So demote, insert, then link.
_DEMOTE_CURRENT_EVALS = nugget_writes.register(
    "UPDATE {schema}.nugget_screening_evals SET is_current = false "
    "WHERE job_id = :job_id AND candidate_id = :candidate_id AND is_current "
    "RETURNING id"
)

_LINK_SUPERSEDED = nugget_writes.register(
    "UPDATE {schema}.nugget_screening_evals SET superseded_by = :new_id "
    "WHERE id = ANY(:ids)"
)

_INSERT_EVAL = nugget_writes.register(
    "INSERT INTO {schema}.nugget_screening_evals "
    "(job_id, candidate_id, application_id, run_id, rubric_id, rubric_version, "
    " candidate_email, candidate_name, applied_at, total_score, max_score, "
    " score_pct, dimension_scores, extracted, strengths, gaps, "
    " hard_filter_flags, verdict, confidence, tier, tier_reason, tiered_at, "
    " tiered_thresholds, resume_health, resume_issues, resume_chars, "
    " resume_type, resume_truncated, prior_context_used, status, error, model, "
    " effort, input_tokens, cache_read_tokens, cache_creation_tokens, "
    " output_tokens, cost_usd, latency_ms, is_current, evaluated_at) "
    "VALUES (:job_id, :candidate_id, :application_id, :run_id, :rubric_id, "
    " :rubric_version, :candidate_email, :candidate_name, :applied_at, "
    " :total_score, :max_score, :score_pct, CAST(:dimension_scores AS jsonb), "
    " CAST(:extracted AS jsonb), CAST(:strengths AS jsonb), "
    " CAST(:gaps AS jsonb), CAST(:hard_filter_flags AS jsonb), :verdict, "
    " :confidence, :tier, :tier_reason, now(), CAST(:tiered_thresholds AS jsonb), "
    " :resume_health, :resume_issues, :resume_chars, :resume_type, "
    " :resume_truncated, false, :status, :error, :model, :effort, "
    " :input_tokens, :cache_read_tokens, :cache_creation_tokens, "
    " :output_tokens, :cost_usd, :latency_ms, true, now()) "
    "RETURNING id"
)

_CACHE_RESUME = nugget_writes.register(
    "INSERT INTO {schema}.nugget_screening_resume_cache "
    "(candidate_id, source_hash, text, chars, truncated, parse_type, "
    " parse_success, parse_error, health, issues, parsed_at) "
    "VALUES (:candidate_id, :source_hash, :text, :chars, :truncated, "
    " :parse_type, :parse_success, :parse_error, :health, :issues, now()) "
    "ON CONFLICT (candidate_id) DO UPDATE SET "
    " source_hash = EXCLUDED.source_hash, text = EXCLUDED.text, "
    " chars = EXCLUDED.chars, truncated = EXCLUDED.truncated, "
    " parse_type = EXCLUDED.parse_type, parse_success = EXCLUDED.parse_success, "
    " parse_error = EXCLUDED.parse_error, health = EXCLUDED.health, "
    " issues = EXCLUDED.issues, parsed_at = now()"
)

_START_RUN = nugget_writes.register(
    "UPDATE {schema}.nugget_screening_runs "
    "SET status = 'running', started_at = COALESCE(started_at, now()), "
    "    heartbeat_at = now(), worker_id = :worker "
    "WHERE id = :run_id AND status IN ('queued', 'running')"
)

_BUMP_RUN = nugget_writes.register(
    "UPDATE {schema}.nugget_screening_runs SET "
    " done_count = done_count + :done, ok_count = ok_count + :ok, "
    " unusable_count = unusable_count + :unusable, "
    " failed_count = failed_count + :failed, "
    " skipped_count = skipped_count + :skipped, "
    " input_tokens = input_tokens + :input_tokens, "
    " cache_read_tokens = cache_read_tokens + :cache_read_tokens, "
    " cache_creation_tokens = cache_creation_tokens + :cache_creation_tokens, "
    " output_tokens = output_tokens + :output_tokens, "
    " actual_cost_usd = actual_cost_usd + :cost_usd, heartbeat_at = now() "
    "WHERE id = :run_id"
)

_SET_RUN_STATUS = nugget_writes.register(
    "UPDATE {schema}.nugget_screening_runs "
    "SET status = :status, pause_reason = :pause_reason, error = :error, "
    "    finished_at = CASE WHEN :terminal THEN now() ELSE finished_at END, "
    "    heartbeat_at = now() "
    "WHERE id = :run_id"
)

_REQUEST_CANCEL = nugget_writes.register(
    "UPDATE {schema}.nugget_screening_runs SET cancel_requested = true "
    "WHERE id = :run_id"
)

_CANCEL_PENDING_ITEMS = nugget_writes.register(
    "UPDATE {schema}.nugget_screening_run_items SET state = 'cancelled', "
    " finished_at = now() WHERE run_id = :run_id AND state = 'pending'"
)


def get_run(db: Session, run_id: str) -> Optional[dict]:
    sql = f"""
    SELECT r.id, r.job_id, r.rubric_id, r.rubric_version, r.mode, r.status,
           r.cancel_requested, r.pause_reason, r.model, r.effort, r.use_batch,
           r.planned_count, r.total_items, r.done_count, r.ok_count,
           r.unusable_count, r.failed_count, r.skipped_count,
           r.est_cost_usd, r.cost_cap_usd, r.actual_cost_usd, r.requested_by,
           r.created_at, r.started_at, r.finished_at, r.error, j.title AS job_title
    FROM {schema()}.nugget_screening_runs r
    LEFT JOIN {MARKAZ_SCHEMA}.jobs j ON j.id = r.job_id
    WHERE r.id = :run_id
    """
    return _one(db, sql, run_id=run_id)


def runs_for_job(db: Session, job_id: int, limit: int = 10) -> list[dict]:
    sql = f"""
    SELECT id, status, mode, model, total_items, done_count, ok_count,
           unusable_count, failed_count, actual_cost_usd, created_at, finished_at
    FROM {schema()}.nugget_screening_runs
    WHERE job_id = :job_id ORDER BY created_at DESC LIMIT :limit
    """
    return _rows(db, sql, job_id=job_id, limit=limit)


def remaining_items(db: Session, run_id: str) -> int:
    sql = f"""
    SELECT COUNT(*) AS n FROM {schema()}.nugget_screening_run_items
    WHERE run_id = :run_id AND state IN ('pending', 'in_progress')
    """
    row = _one(db, sql, run_id=run_id)
    return int(row["n"]) if row else 0


def last_warning(db: Session, run_id: str) -> Optional[str]:
    sql = f"""
    SELECT event, detail FROM {schema()}.nugget_screening_run_events
    WHERE run_id = :run_id AND level IN ('warn', 'error')
    ORDER BY created_at DESC LIMIT 1
    """
    row = _one(db, sql, run_id=run_id)
    if not row:
        return None
    detail = row["detail"] or {}
    return detail.get("error") or row["event"]


def _set_status(
    db: Session,
    run_id: str,
    status: str,
    *,
    pause_reason: Optional[str] = None,
    error: Optional[str] = None,
    terminal: bool = False,
) -> None:
    nugget_writes.execute(
        db,
        _SET_RUN_STATUS,
        run_id=run_id,
        status=status,
        pause_reason=pause_reason,
        error=error,
        terminal=terminal,
    )


def request_cancel(db: Session, run_id: str) -> None:
    nugget_writes.execute(db, _REQUEST_CANCEL, run_id=run_id)
    nugget_writes.execute(db, _CANCEL_PENDING_ITEMS, run_id=run_id)
    _set_status(db, run_id, "cancelled", terminal=True)
    log_event(db, run_id, "cancelled", {"by": "user"}, level="warn")


# --------------------------------------------------------------------------
# Scoring one candidate
# --------------------------------------------------------------------------

_CANDIDATE_SQL = """
SELECT a.id AS application_id, a.candidate_id, a.applied_at, a.cover_letter,
       a.custom_answers, a.canned_answers,
       c.first_name, c.last_name, c.email,
       c.resume_data, c.resume_file_name, c.resume_mime_type
FROM public.applications a
JOIN public.candidates c ON c.id = a.candidate_id
WHERE a.id = :application_id
"""


def _is_fatal_api_error(exc: Exception) -> Optional[str]:
    """A cause that will not fix itself, so the run should stop.

    🔴 THIS IS THE LESSON FROM RUN 21308392. Every one of its 369 items failed
    with "The Anthropic account has no credit", each one a separate API call
    made after the first had already given the answer. An exhausted balance,
    a bad key and a revoked permission are all conditions of the ACCOUNT, not
    of the candidate, and retrying them 368 more times helps nobody.
    """
    status = getattr(exc, "status_code", None)
    if status in (401, 403):
        return "the Anthropic credential was rejected"
    message = (str(getattr(exc, "message", "")) or str(exc)).lower()
    for needle, human in (
        ("credit balance", "the Anthropic account has no credit"),
        ("insufficient", "the Anthropic account has no credit"),
        ("billing", "the Anthropic account has a billing problem"),
        ("quota", "the Anthropic account is out of quota"),
        ("authentication", "the Anthropic credential was rejected"),
        ("permission", "the Anthropic credential lacks permission"),
    ):
        if needle in message:
            return human
    return None


def _call_model(
    *, system_prompt: str, user_prompt: str, output_schema: Optional[dict] = None,
) -> tuple[dict, str, dict, int]:
    """One scoring call. Module-level so tests monkeypatch it and never spend
    money. Reuses drafting.get_drafter() rather than building a second client,
    the same way cv_screening, values_scoring and case_study_scoring do.

    The rubric's system prompt is identical for every candidate in a run and
    goes through `_cacheable_system`, so after the first call it bills at the
    cache-read rate. That is where the estimate's cache saving comes from.

    🔴 THE SCHEMA IS SENT, NOT MERELY STORED. This used to call `draft()`, the
    candidate-letter path, passing the system prompt and nothing else. The
    rubric's `output_schema` was loaded, hashed and written to the run, and
    never transmitted to the model. On 2026-09-25 the model duly answered in a
    shape of its own -- every rubric dimension present but TOP-LEVEL rather
    than under `dimensions` -- and all twenty candidates failed on a reader
    that found an empty object. Forcing the schema as a tool makes the shape a
    fact. `output_schema=None` keeps the old prose path for any caller that
    genuinely has no contract.
    """
    from . import drafting

    drafter = drafting.get_drafter()
    if isinstance(drafter, drafting.StubDrafter):
        raise drafting.DraftingUnavailable(
            "No Anthropic credential configured: get_drafter() returned the "
            "offline StubDrafter, whose output is an email-shaped placeholder, "
            "never a screening evaluation. Set ANTHROPIC_API_KEY or "
            "ANTHROPIC_AUTH_TOKEN."
        )
    started = time.monotonic()
    if output_schema:
        parsed = drafter.structured(
            system=system_prompt, user=user_prompt, schema=output_schema,
            tool_name="submit_screening",
        )
    else:
        parsed = drafter.draft(
            system=system_prompt,
            user=user_prompt,
            email_type="technical_screening",
            first_name="",
            role="",
            prior_violations=None,
            attempt=0,
        )
    latency_ms = int((time.monotonic() - started) * 1000)
    usage = (drafter.calls or [{}])[-1]
    model_name = getattr(drafter, "model", None) or "unknown"
    return parsed, model_name, usage, latency_ms


def normalise_dimensions(parsed: dict, rubric: dict) -> dict:
    """The dimension scores, wherever the model put them.

    Defence in depth behind the forced schema, and a direct record of the
    2026-09-25 failure: the model returned `must_have_skills`,
    `responsibility_alignment`, `stack_match`, `technical_breadth` and
    `experience_depth` as top-level keys, so `parsed["dimensions"]` was empty
    and the run reported that it had not scored the first one.

    Nothing is invented here. A key is lifted only when the rubric names it and
    the nested object does not already carry it, and lifting is logged, because
    a shape drifting back is worth knowing about rather than papering over.
    """
    dims = parsed.get("dimensions")
    dims = dict(dims) if isinstance(dims, dict) else {}
    lifted = []
    for spec in rubric.get("dimensions") or []:
        key = spec.get("key")
        if key and key not in dims and key in parsed:
            dims[key] = parsed[key]
            lifted.append(key)
    if lifted:
        log.warning(
            "Model returned %d dimension(s) at the top level instead of under "
            "'dimensions': %s. Lifted them; the output schema should have "
            "prevented this.", len(lifted), ", ".join(lifted),
        )
    return dims


def build_user_prompt(*, cv: str, row: dict, rubric: dict) -> str:
    """The candidate's own material. The rubric's system prompt already carries
    the job description, the dimensions, the anchors and the rules, so this
    adds nothing but evidence."""
    name = " ".join(x for x in (row.get("first_name"), row.get("last_name")) if x)
    answers = []
    for field in ("custom_answers", "canned_answers"):
        value = row.get(field)
        if isinstance(value, dict):
            for entry in value.values():
                if isinstance(entry, dict) and entry.get("question"):
                    answers.append(f"Q: {entry['question']}\nA: {entry.get('answer') or ''}")
    parts = [f"Candidate: {name or 'not given'}", "", "# The candidate's CV", "", cv]
    if row.get("cover_letter"):
        parts += ["", "# Cover letter", "", str(row["cover_letter"])]
    if answers:
        parts += ["", "# Application answers", "", "\n\n".join(answers[:12])]
    parts += [
        "",
        "---",
        "Score this candidate against the rubric in your instructions and reply "
        "with the JSON object it describes. Candidate name as a JSON string, "
        f"for your reference only: {json.dumps(name)}.",
    ]
    return "\n".join(parts)


def _strip_nul(text: Optional[str]) -> Optional[str]:
    """Remove NUL (0x00) bytes from extracted CV text.

    PostgreSQL `text` cannot hold 0x00 at all, so a single stray NUL from a PDF
    parser makes the resume-cache INSERT raise DataError and takes that
    candidate down with it. One of the twenty in run aef6ed75 died exactly this
    way, and it was reported to Ayesha as a CV that could not be read.

    Stripping is safe: a NUL carries no meaning in extracted prose, it is
    parser debris. It is removed rather than replaced so character offsets in
    quoted evidence do not shift.
    """
    if text is None:
        return None
    return text.replace("\x00", "")


def _resume_for(db: Session, row: dict) -> tuple[Optional[str], dict]:
    """Extracted CV text plus the health record, using Nugget's resume cache.

    The cache is keyed by candidate and carries a `source_hash`, so re-running
    a job does not re-parse a file that has not changed. A cache entry whose
    hash no longer matches is re-extracted rather than trusted.
    """
    data = row.get("resume_data")
    if not data:
        meta = {
            "chars": 0, "health": 0, "issues": ["no CV was uploaded"],
            "type": None, "truncated": False, "parse_success": False,
            "parse_error": "no CV was uploaded",
        }
        return None, meta

    source_hash = hashlib.sha256(
        data if isinstance(data, (bytes, bytearray)) else str(data).encode("utf-8")
    ).hexdigest()

    cached = _one(
        db,
        f"""SELECT text, chars, truncated, parse_type, parse_success,
                   parse_error, health, issues
            FROM {schema()}.nugget_screening_resume_cache
            WHERE candidate_id = :cid AND source_hash = :h""",
        cid=row["candidate_id"],
        h=source_hash,
    )
    if cached and cached["parse_success"] and cached["text"]:
        return cached["text"], {
            "chars": cached["chars"], "health": cached["health"] or 0,
            "issues": list(cached["issues"] or []), "type": cached["parse_type"],
            "truncated": cached["truncated"], "parse_success": True,
            "parse_error": None,
        }

    text_value: Optional[str] = None
    parse_error: Optional[str] = None
    try:
        text_value = _strip_nul(
            cv_text.extract(
                data,
                mime_type=row.get("resume_mime_type"),
                file_name=row.get("resume_file_name"),
            )
        )
    except cv_text.CVUnreadable as exc:
        parse_error = str(exc)

    health, issues = tech_tiering.resume_health(text_value)
    meta = {
        "chars": len(text_value or ""),
        "health": health,
        "issues": issues or ([parse_error] if parse_error else []),
        "type": (row.get("resume_file_name") or "").rsplit(".", 1)[-1].lower() or None,
        "truncated": False,
        "parse_success": bool(text_value),
        "parse_error": parse_error,
    }
    nugget_writes.execute(
        db,
        _CACHE_RESUME,
        candidate_id=row["candidate_id"],
        source_hash=source_hash,
        text=text_value,
        chars=meta["chars"],
        truncated=False,
        parse_type=meta["type"],
        parse_success=meta["parse_success"],
        parse_error=parse_error,
        health=health,
        issues=meta["issues"],
    )
    return text_value, meta


def _write_eval(db: Session, **fields) -> str:
    """Insert one evaluation, superseding the candidate's previous one.

    Three statements in one transaction, in this order, because
    `uq_nse_current_per_job_candidate` forbids two current rows for the same
    (job, candidate) even momentarily.
    """
    demoted = [
        r["id"]
        for r in nugget_writes.execute(
            db,
            _DEMOTE_CURRENT_EVALS,
            job_id=fields["job_id"],
            candidate_id=fields["candidate_id"],
        ).mappings()
    ]
    new_id = nugget_writes.execute(db, _INSERT_EVAL, **fields).scalar()
    if demoted:
        nugget_writes.execute(db, _LINK_SUPERSEDED, new_id=new_id, ids=demoted)
    return str(new_id)


def score_one(db: Session, *, run: dict, rubric: dict, application_id: int) -> dict:
    """Screen one candidate and write the evaluation. Raises on a model failure
    so the caller can decide whether the run should continue."""
    row = _one(db, _CANDIDATE_SQL, application_id=application_id)
    if not row:
        return {"outcome": "skipped", "reason": "application not found"}

    cv, meta = _resume_for(db, row)
    name = " ".join(x for x in (row.get("first_name"), row.get("last_name")) if x)

    common = dict(
        job_id=run["job_id"],
        candidate_id=row["candidate_id"],
        application_id=application_id,
        run_id=run["id"],
        rubric_id=rubric["id"],
        rubric_version=rubric["version"],
        candidate_email=row.get("email"),
        candidate_name=name or None,
        applied_at=row.get("applied_at"),
        max_score=float(rubric.get("max_score") or 100),
        resume_health=meta["health"],
        resume_issues=meta["issues"],
        resume_chars=meta["chars"],
        resume_type=meta["type"],
        resume_truncated=meta["truncated"],
        model=run["model"],
        effort=run["effort"],
        tiered_thresholds=json.dumps(rubric.get("thresholds") or {}),
    )

    # 🔴 An unreadable CV is a DOCUMENT problem. It is never a rejection and
    # never a zero: it carries no score at all and waits for a person.
    unscorable = tech_tiering.route_unscorable(
        health=meta["health"],
        chars=meta["chars"],
        rules=rubric.get("manual_review_rules"),
    )
    if unscorable or not cv:
        tier, reason = unscorable or (
            "UNUSABLE",
            "No CV was uploaded with this application, so it has not been scored.",
        )
        eval_id = _write_eval(
            db,
            **common,
            total_score=None,
            score_pct=None,
            dimension_scores=json.dumps({}),
            extracted=json.dumps({}),
            strengths=json.dumps([]),
            gaps=json.dumps([]),
            hard_filter_flags=json.dumps([]),
            verdict=reason,
            confidence=None,
            tier=tier,
            tier_reason=reason,
            status="unusable",
            error=meta.get("parse_error"),
            input_tokens=0, cache_read_tokens=0, cache_creation_tokens=0,
            output_tokens=0, cost_usd=0, latency_ms=0,
        )
        return {"outcome": "unusable", "eval_id": eval_id, "tier": tier,
                "candidate_name": name, "reason": reason, "cost_usd": 0.0,
                "usage": {}}

    parsed, model_name, usage, latency_ms = _call_model(
        system_prompt=rubric["system_prompt"],
        user_prompt=build_user_prompt(cv=cv, row=row, rubric=rubric),
        output_schema=rubric.get("output_schema"),
    )

    dimension_scores, total, max_score = tech_tiering.score_dimensions(
        rubric, normalise_dimensions(parsed, rubric)
    )
    weight_total = sum(float(d.get("weight") or 0) for d in rubric["dimensions"]) * 5
    pct = tech_tiering.score_percent(total, max_score, weight_total=weight_total)
    flags, reject = tech_tiering.evaluate_hard_filters(rubric, parsed.get("hard_filters"))
    tier, tier_reason = tech_tiering.assign_tier(
        rubric=rubric, dimension_scores=dimension_scores, pct=pct,
        hard_filter_reject=reject,
    )
    confidence = (parsed.get("confidence") or "medium").lower()
    if confidence not in tech_tiering.CONFIDENCE_VALUES:
        confidence = "medium"

    cost = pricing.cost_of_call({**usage, "model": model_name},
                               batch=bool(run.get("use_batch")))
    eval_id = _write_eval(
        db,
        **{**common, "model": model_name},
        total_score=total,
        score_pct=pct,
        dimension_scores=json.dumps(dimension_scores),
        extracted=json.dumps(parsed.get("extracted") or {}),
        strengths=json.dumps(list(parsed.get("strengths") or [])[:6]),
        gaps=json.dumps(list(parsed.get("gaps") or [])[:6]),
        hard_filter_flags=json.dumps(flags),
        verdict=(parsed.get("verdict") or None),
        confidence=confidence,
        tier=tier,
        tier_reason=tier_reason,
        status="scored",
        error=None,
        input_tokens=usage.get("input_tokens") or 0,
        cache_read_tokens=usage.get("cache_read") or 0,
        cache_creation_tokens=usage.get("cache_write") or 0,
        output_tokens=usage.get("output_tokens") or 0,
        cost_usd=cost,
        latency_ms=latency_ms,
    )
    return {
        "outcome": "scored", "eval_id": eval_id, "tier": tier,
        "score_pct": pct, "candidate_name": name, "reason": tier_reason,
        "cost_usd": cost, "usage": usage,
    }


def work(
    db: Session,
    *,
    run_id: str,
    worker: str,
    limit: int = 3,
) -> dict:
    """Do one slice of a run.

    Returns the shape `frontend/src/lib/screenAll.ts` already consumes
    (`screened`, `skipped`, `last_application_id`, `remaining`) so that loop is
    reused verbatim rather than reimplemented -- it carries a five-minute retry
    budget written after a fifty-minute run died to a Railway redeploy.

    Commits per candidate. A request that dies mid-slice loses at most the item
    in flight, and the reaper hands that back after STUCK_AFTER_MINUTES.
    """
    run = get_run(db, run_id)
    if not run:
        raise RunError("no such run")
    if run["status"] in ("completed", "cancelled", "failed"):
        return _slice_result(db, run_id, [], [], None)
    if run["cancel_requested"]:
        request_cancel(db, run_id)
        db.commit()
        return _slice_result(db, run_id, [], [], None)

    rubric = _one(
        db,
        f"""SELECT id, job_id, version, dimensions, max_score, hard_filters,
                   thresholds, manual_review_rules, system_prompt
            FROM {schema()}.nugget_screening_rubrics WHERE id = :rid""",
        rid=run["rubric_id"],
    )
    if not rubric:
        _set_status(db, run_id, "failed", error="the run's rubric is missing",
                    terminal=True)
        db.commit()
        raise RunError("the run's rubric is missing")

    nugget_writes.execute(db, _START_RUN, run_id=run_id, worker=worker)

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=STUCK_AFTER_MINUTES)
    reaped = list(
        nugget_writes.execute(
            db, _REAP_STUCK, run_id=run_id, cutoff=cutoff, max_attempts=MAX_ATTEMPTS
        ).mappings()
    )
    if reaped:
        log_event(db, run_id, "reaped", {"items": len(reaped)}, level="warn")
    db.commit()

    claimed = list(
        nugget_writes.execute(
            db, _CLAIM_ITEMS, run_id=run_id, worker=worker, limit=limit
        ).mappings()
    )
    db.commit()

    screened: list[dict] = []
    skipped: list[dict] = []
    # Kept apart from `skipped` all the way to the screen. A skip is a document
    # problem; a failure is ours.
    failed: list[dict] = []
    last_app: Optional[int] = None
    consecutive_fatal = 0
    fatal_reason: Optional[str] = None

    for item in claimed:
        app_id = item["application_id"]
        last_app = app_id
        try:
            result = score_one(db, run=run, rubric=rubric, application_id=app_id)
        except Exception as exc:  # noqa: BLE001
            db.rollback()
            fatal = _is_fatal_api_error(exc)
            if fatal:
                consecutive_fatal += 1
                fatal_reason = fatal
                # Hand the item back: it was never the item's fault.
                nugget_writes.execute(db, _RELEASE_ITEM, item_id=item["id"])
                log_event(db, run_id, "item_failed",
                          {"application_id": app_id, "error": fatal}, level="error")
                db.commit()
                if consecutive_fatal >= CONSECUTIVE_FAILURE_LIMIT:
                    break
                continue
            log.exception("screening failed for application %s", app_id)
            nugget_writes.execute(
                db, _FINISH_ITEM, item_id=item["id"], state="failed",
                eval_id=None, skip_reason=None,
                error=f"{type(exc).__name__}: {exc}"[:500],
            )
            # The counter, and the money. Neither used to be recorded here, so
            # a run in which every candidate failed displayed FAILED 0 and
            # SPENT $0.00 while twenty model calls had been made and billed.
            # A cost of zero for work we paid for is the kind of number people
            # trust.
            _bump(db, run_id, failed=1,
                  usage=getattr(exc, "usage", None) or {},
                  cost=float(getattr(exc, "cost_usd", 0.0) or 0.0))
            log_event(db, run_id, "item_failed",
                      {"application_id": app_id, "error": str(exc)[:300]},
                      level="error")
            db.commit()
            # 🔴 FAILED, NEVER "could not be read". These are two different
            # facts about two different people's work: one needs somebody to
            # open a document, the other needs an engineer. Merging them into
            # `skipped` sent Ayesha to chase twenty CVs that were perfectly
            # readable while the actual defect was ours.
            failed.append({"application_id": app_id,
                           "reason": f"{type(exc).__name__}: {exc}"[:200]})
            continue

        consecutive_fatal = 0
        outcome = result["outcome"]
        if outcome == "skipped":
            nugget_writes.execute(
                db, _FINISH_ITEM, item_id=item["id"], state="skipped",
                eval_id=None, skip_reason=result["reason"], error=None,
            )
            _bump(db, run_id, skipped=1)
            db.commit()
            skipped.append({"application_id": app_id, "reason": result["reason"]})
            continue

        nugget_writes.execute(
            db, _FINISH_ITEM, item_id=item["id"], state="done",
            eval_id=result["eval_id"], skip_reason=None, error=None,
        )
        _bump(
            db, run_id,
            ok=1 if outcome == "scored" else 0,
            unusable=1 if outcome == "unusable" else 0,
            usage=result.get("usage") or {},
            cost=result.get("cost_usd") or 0.0,
        )
        db.commit()
        if outcome == "unusable":
            skipped.append({"application_id": app_id, "reason": result["reason"],
                            "candidate_name": result.get("candidate_name"),
                            "tier": result.get("tier")})
        else:
            screened.append({"application_id": app_id,
                             "candidate_name": result.get("candidate_name"),
                             "tier": result["tier"],
                             "score_pct": result.get("score_pct")})

    if consecutive_fatal >= CONSECUTIVE_FAILURE_LIMIT and fatal_reason:
        _set_status(db, run_id, "paused", pause_reason="rate_limit",
                    error=f"Paused after {consecutive_fatal} consecutive failures: "
                          f"{fatal_reason}. No candidate was at fault and nothing "
                          f"was marked failed. Fix the cause and resume.")
        log_event(db, run_id, "paused",
                  {"reason": fatal_reason, "consecutive": consecutive_fatal},
                  level="error")
        db.commit()
        return _slice_result(db, run_id, screened, skipped, last_app, failed)

    _check_cap_and_finish(db, run_id)
    db.commit()
    return _slice_result(db, run_id, screened, skipped, last_app, failed)


def _bump(db, run_id, *, ok=0, unusable=0, failed=0, skipped=0, usage=None, cost=0.0):
    usage = usage or {}
    nugget_writes.execute(
        db, _BUMP_RUN, run_id=run_id,
        done=ok + unusable + failed + skipped,
        ok=ok, unusable=unusable, failed=failed, skipped=skipped,
        input_tokens=usage.get("input_tokens") or 0,
        cache_read_tokens=usage.get("cache_read") or 0,
        cache_creation_tokens=usage.get("cache_write") or 0,
        output_tokens=usage.get("output_tokens") or 0,
        cost_usd=cost or 0.0,
    )


def _check_cap_and_finish(db: Session, run_id: str) -> None:
    run = get_run(db, run_id)
    if not run or run["status"] not in ("running", "queued"):
        return
    cap = run.get("cost_cap_usd")
    if cap is not None and float(run["actual_cost_usd"] or 0) >= float(cap):
        _set_status(db, run_id, "paused", pause_reason="cost_cap",
                    error=f"Paused at the ${float(cap):.2f} cost cap.")
        log_event(db, run_id, "paused",
                  {"reason": "cost_cap", "spent": float(run["actual_cost_usd"])},
                  level="warn")
        return
    if remaining_items(db, run_id) == 0:
        # 🔴 A run that scored nobody is not a completed screening. Run
        # 167c8357 was recorded "completed" having scored 43 of 645, and had
        # to be corrected by hand the next day.
        if int(run["ok_count"] or 0) == 0 and int(run["total_items"] or 0) > 0:
            _set_status(db, run_id, "failed", terminal=True,
                        error=f"All {run['total_items']} candidates failed to score.")
            return
        _set_status(db, run_id, "completed", terminal=True)


def _slice_result(db, run_id, screened, skipped, last_app, failed=None) -> dict:
    run = get_run(db, run_id)
    return {
        "run_id": str(run_id),
        "screened": screened,
        # Could not be read: a person must open the document.
        "skipped": skipped,
        # Failed: the screener broke. An engineer must look.
        "failed": failed or [],
        "last_application_id": last_app,
        "remaining": remaining_items(db, run_id),
        "status": run["status"] if run else "unknown",
        "run": run_progress(run, db=db) if run else None,
    }


def run_progress(run: dict, *, db: Optional[Session] = None) -> dict:
    total = int(run["total_items"] or 0)
    done = int(run["done_count"] or 0)
    return {
        "id": str(run["id"]),
        "job_id": run["job_id"],
        "job_title": run.get("job_title"),
        "status": run["status"],
        "mode": run["mode"],
        "model": run["model"],
        "rubric_version": run["rubric_version"],
        "pause_reason": run.get("pause_reason"),
        "total": total,
        "done": done,
        "scored": int(run["ok_count"] or 0),
        "failed": int(run["failed_count"] or 0),
        "skipped": int(run["skipped_count"] or 0),
        "unusable": int(run["unusable_count"] or 0),
        "percent": round(done / total * 100, 1) if total else 0.0,
        "est_cost_usd": float(run["est_cost_usd"] or 0),
        "actual_cost_usd": float(run["actual_cost_usd"] or 0),
        "cost_cap_usd": float(run["cost_cap_usd"]) if run.get("cost_cap_usd") is not None else None,
        "requested_by": run.get("requested_by"),
        "created_at": run.get("created_at"),
        "started_at": run.get("started_at"),
        "finished_at": run.get("finished_at"),
        "error": run.get("error"),
        "last_warning": last_warning(db, run["id"]) if db is not None else None,
    }
