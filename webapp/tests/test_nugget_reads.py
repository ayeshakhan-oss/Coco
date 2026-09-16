"""Unit tests for the Nugget screening read layer.

These tables belong to Nugget (Aymen's agent). The guard below is the
mechanical reason Coco cannot write to them, so it is tested against
deliberately bad SQL rather than only against the happy path.

Run:  python -m pytest webapp/tests/test_nugget_reads.py
"""

from __future__ import annotations

import pytest

from sqlalchemy import text

import webapp.services.nugget_reads as nugget_reads
from webapp.services.nugget_reads import (
    CANDIDATES_FOR_JOB_SQL,
    EVALUATION_FOR_APPLICATION_SQL,
    JOB_SUMMARY_SQL,
    LIST_SCREENED_JOBS_SQL,
    TIER_ORDER,
    UNSCORED_TIERS,
    _mark_unusable,
    assert_read_only,
    is_valid_tier,
    shape_summary,
)


def test_read_only_guard_blocks_writes():
    bad = [
        "UPDATE public.nugget_screening_evals SET tier='P1'",
        "DELETE FROM public.nugget_screening_runs",
        "INSERT INTO public.nugget_screening_rubrics (job_id) VALUES (1)",
        "DROP TABLE public.nugget_screening_evals",
        "  update  public.nugget_screening_evals SET tier='P1'",
        "\n\tTRUNCATE public.nugget_screening_evals",
    ]
    for sql in bad:
        with pytest.raises(PermissionError):
            assert_read_only(sql)


def test_read_only_guard_allows_reads():
    for sql in ("SELECT 1", "  select 1", "\nWITH x AS (SELECT 1) SELECT * FROM x"):
        assert_read_only(sql) is None


def test_read_only_guard_blocks_write_nested_in_a_cte():
    # Starts with WITH, opens like a read, but the CTE body is a DELETE.
    bad = "WITH x AS (DELETE FROM public.nugget_screening_evals RETURNING *) SELECT * FROM x"
    with pytest.raises(PermissionError):
        assert_read_only(bad)


def test_read_only_guard_blocks_select_into():
    # Starts with SELECT but is DDL: creates a new table from the query result.
    bad = "SELECT * INTO shadow FROM public.nugget_screening_evals"
    with pytest.raises(PermissionError):
        assert_read_only(bad)


def test_read_only_guard_blocks_multi_statement_sql():
    bad = "SELECT 1; DROP TABLE public.nugget_screening_evals;"
    with pytest.raises(PermissionError):
        assert_read_only(bad)


def test_read_only_guard_strips_comments_so_they_cannot_hide_a_keyword():
    # A keyword or semicolon that only exists inside a SQL comment is inert
    # (Postgres never executes it), so it must not cause a false block.
    assert assert_read_only("SELECT 1 -- historical note: used to DROP TABLE here") is None
    assert assert_read_only("SELECT /* was: DELETE FROM x; */ 1") is None


def test_read_only_guard_allows_a_single_trailing_semicolon():
    assert assert_read_only("SELECT 1;") is None
    assert assert_read_only("  WITH x AS (SELECT 1) SELECT * FROM x ;  ") is None


def test_read_only_guard_allows_the_real_call_sites():
    # Representative strings for the four queries this module actually issues
    # (list_screened_jobs, job_summary, candidates_for_job,
    # evaluation_for_application), so hardening the guard can't silently break
    # a real call site.
    real_queries = [
        """
        SELECT r.job_id,
               j.title AS job_title,
               r.version AS rubric_version,
               r.status  AS rubric_status,
               r.seniority,
               COUNT(*) FILTER (WHERE e.status = 'scored')   AS scored,
               COUNT(*) FILTER (WHERE e.status = 'unusable') AS unusable,
               MAX(e.evaluated_at) AS last_run_at
        FROM public.nugget_screening_rubrics r
        LEFT JOIN public.jobs j ON j.id = r.job_id
        LEFT JOIN public.nugget_screening_evals e
               ON e.job_id = r.job_id AND e.is_current
        GROUP BY r.job_id, j.title, r.version, r.status, r.seniority
        ORDER BY scored DESC
        """,
        """
        SELECT tier, status, COUNT(*) AS n,
               ROUND(AVG(score_pct), 1) AS avg_pct,
               MIN(score_pct) AS min_pct,
               MAX(score_pct) AS max_pct
        FROM public.nugget_screening_evals
        WHERE job_id = :job_id AND is_current
        GROUP BY tier, status
        """,
        """
        SELECT application_id, candidate_id, candidate_name, candidate_email,
               score_pct, tier, tier_reason, confidence, resume_health, status
        FROM public.nugget_screening_evals
        WHERE job_id = :job_id AND is_current
          AND (:tier::text IS NULL OR tier = :tier::text)
        ORDER BY (status = 'unusable'), score_pct DESC NULLS LAST
        LIMIT :limit OFFSET :offset
        """,
        """
        SELECT e.application_id, e.candidate_id, e.candidate_name, e.candidate_email,
               e.score_pct, e.tier, e.tier_reason, e.confidence, e.resume_health,
               e.status, e.dimension_scores, e.strengths, e.gaps,
               e.hard_filter_flags, e.verdict, e.rubric_version, e.model, e.evaluated_at
        FROM public.nugget_screening_evals e
        WHERE e.application_id = :application_id AND e.is_current
        LIMIT 1
        """,
    ]
    for sql in real_queries:
        assert assert_read_only(sql) is None


def test_query_bind_params_are_all_recognised_by_sqlalchemy():
    """Regression test for a real production bug: `:tier::text` compiles in
    Postgres but SQLAlchemy's `text()` bind-parameter regex does not
    recognise a name immediately followed by `::`, so `tier` silently never
    became a bind parameter and psycopg raised a SyntaxError on every call to
    /api/evaluations/jobs/{job_id}/candidates, with or without ?tier=. This
    asserts against the SAME module-level SQL constants the functions
    actually execute (imported directly, not pasted here), so it can't drift
    the way a copy of the SQL could, and it would have caught the bug without
    needing a live database.
    """
    assert set(text(LIST_SCREENED_JOBS_SQL).compile().bind_names.values()) == set()
    assert set(text(JOB_SUMMARY_SQL).compile().bind_names.values()) == {"job_id"}
    assert set(text(CANDIDATES_FOR_JOB_SQL).compile().bind_names.values()) == {
        "job_id",
        "tier",
        "limit",
        "offset",
    }
    assert set(text(EVALUATION_FOR_APPLICATION_SQL).compile().bind_names.values()) == {
        "application_id"
    }


def test_candidates_for_job_sql_does_not_use_the_bare_cast_operator():
    # `::` is the specific pattern that broke SQLAlchemy's bind-parameter
    # parsing (see test above). Assert the fixed query never reintroduces it,
    # so a future "simplification" back to `:tier::text` fails immediately
    # instead of shipping a 500 on every /candidates request again.
    assert "::" not in CANDIDATES_FOR_JOB_SQL


def test_shape_summary_orders_tiers_and_separates_unusable():
    rows = [
        {"tier": "P4", "status": "scored", "n": 378, "avg_pct": 29.1, "min_pct": 0.0, "max_pct": 53.0},
        {"tier": "UNUSABLE", "status": "unusable", "n": 57, "avg_pct": 0.0, "min_pct": 0.0, "max_pct": 0.0},
        {"tier": "P1", "status": "scored", "n": 26, "avg_pct": 93.5, "min_pct": 85.0, "max_pct": 100.0},
    ]
    out = shape_summary(rows)

    # Tiers come back in published order, not query order.
    assert [t["tier"] for t in out["tiers"]] == ["P1", "P4", "UNUSABLE"]
    assert [t["tier"] for t in out["tiers"]] == [t for t in TIER_ORDER if t in {"P1", "P4", "UNUSABLE"}]

    # UNUSABLE is flagged so the UI can never render it as a rejection.
    unusable = [t for t in out["tiers"] if t["is_unusable"]]
    assert len(unusable) == 1 and unusable[0]["tier"] == "UNUSABLE"

    # UNUSABLE is excluded from the scored count but present in the total.
    assert out["scored"] == 404
    assert out["unusable"] == 57
    assert out["total"] == 461


def test_shape_summary_suppresses_meaningless_averages_for_unusable():
    rows = [{"tier": "UNUSABLE", "status": "unusable", "n": 6, "avg_pct": 0.0, "min_pct": 0.0, "max_pct": 0.0}]
    out = shape_summary(rows)
    # A 0.0 average on unreadable CVs is noise, not a score. Never show it.
    assert out["tiers"][0]["avg_pct"] is None
    assert out["tiers"][0]["min_pct"] is None
    assert out["tiers"][0]["max_pct"] is None


def test_shape_summary_suppresses_manual_review_scores_but_still_counts_them_as_scored():
    # MANUAL_REVIEW's status is 'scored' (the rubric routed it there because the
    # extracted text fell below the readability floor, not because it lost
    # points), so it must land in `scored`, not `unusable`, and the existing
    # scored/unusable/total totals must not shift. Its avg/min/max must still
    # be suppressed like UNUSABLE's, because a 0.00 on an unreadable document
    # is noise, not a measurement.
    rows = [
        {"tier": "P4", "status": "scored", "n": 378, "avg_pct": 29.1, "min_pct": 0.0, "max_pct": 53.0},
        {"tier": "MANUAL_REVIEW", "status": "scored", "n": 12, "avg_pct": 0.0, "min_pct": 0.0, "max_pct": 0.0},
        {"tier": "UNUSABLE", "status": "unusable", "n": 57, "avg_pct": 0.0, "min_pct": 0.0, "max_pct": 0.0},
    ]
    out = shape_summary(rows)

    manual_review = next(t for t in out["tiers"] if t["tier"] == "MANUAL_REVIEW")
    assert manual_review["avg_pct"] is None
    assert manual_review["min_pct"] is None
    assert manual_review["max_pct"] is None
    assert manual_review["is_unscored"] is True
    # is_unusable keeps its own meaning: MANUAL_REVIEW is not the unusable status.
    assert manual_review["is_unusable"] is False

    unusable = next(t for t in out["tiers"] if t["tier"] == "UNUSABLE")
    assert unusable["is_unscored"] is True
    assert unusable["is_unusable"] is True

    p4 = next(t for t in out["tiers"] if t["tier"] == "P4")
    assert p4["is_unscored"] is False
    assert p4["avg_pct"] == 29.1

    # MANUAL_REVIEW's status is 'scored', so it counts toward `scored`, not
    # `unusable`; totals are unchanged from the pre-existing shape.
    assert out["scored"] == 378 + 12
    assert out["unusable"] == 57
    assert out["total"] == 378 + 12 + 57
    assert "MANUAL_REVIEW" in UNSCORED_TIERS


def test_shape_summary_handles_empty():
    # `unscored` (finding 5) is now part of the returned shape.
    assert shape_summary([]) == {
        "tiers": [],
        "scored": 0,
        "unusable": 0,
        "unscored": 0,
        "total": 0,
    }


def test_is_valid_tier_accepts_published_tiers_only():
    for t in ("P1", "P2", "P3", "P4", "MANUAL_REVIEW", "UNUSABLE"):
        assert is_valid_tier(t) is True
    for t in ("p1", "OK", "", "P5", "DROP TABLE", None):
        assert is_valid_tier(t) is False


def _flatten_routes(routes):
    """This FastAPI build wraps every `include_router()` call in an
    `_IncludedRouter` shim that has no `.path`/`.methods` of its own; the real
    `APIRoute` objects live on `original_router.routes`. Recurse through those
    shims so route introspection sees the same flat list `app.routes` gave in
    older FastAPI versions.
    """
    flat = []
    for r in routes:
        if hasattr(r, "path"):
            flat.append(r)
        nested = getattr(r, "original_router", None)
        if nested is not None:
            flat.extend(_flatten_routes(nested.routes))
    return flat


def test_evaluations_router_is_mounted_and_read_only():
    from webapp.main import app

    routes = _flatten_routes(app.routes)
    paths = {r.path for r in routes}
    assert "/api/evaluations/jobs" in paths
    assert "/api/evaluations/jobs/{job_id}/summary" in paths
    assert "/api/evaluations/jobs/{job_id}/candidates" in paths
    assert "/api/evaluations/applications/{application_id}" in paths

    # Read-only surface: no POST/PUT/PATCH/DELETE anywhere under /api/evaluations.
    for r in routes:
        if r.path.startswith("/api/evaluations"):
            assert set(getattr(r, "methods", set())) <= {"GET", "HEAD", "OPTIONS"}


# ---------------------------------------------------------------------------
# 8a. `is_current` invariant: the single most important constraint in this
# module (only ever read the CURRENT eval per application), and, until now,
# untested. Checked against every module-level `..._SQL` constant so a new
# query added later is covered automatically, not just the four existing ones.
# ---------------------------------------------------------------------------


def test_every_eval_reading_sql_constant_filters_on_is_current():
    sql_constants = {
        name: value
        for name, value in vars(nugget_reads).items()
        if name.isupper() and name.endswith("_SQL") and isinstance(value, str)
    }
    # Guard against the invariant test itself silently checking nothing.
    assert len(sql_constants) >= 4
    for name, sql in sql_constants.items():
        assert "is_current" in sql, f"{name} does not filter on is_current"


# ---------------------------------------------------------------------------
# 8b. Direct tests for `_mark_unusable` (finding-adjacent: this is the
# function both `candidates_for_job` and `evaluation_for_application` rely on
# to make sure UNUSABLE/MANUAL_REVIEW rows never render as a 0.00 score).
# ---------------------------------------------------------------------------


def test_mark_unusable_on_an_unusable_row():
    row = {"tier": "UNUSABLE", "status": "unusable", "score_pct": 0.0}
    out = _mark_unusable(dict(row))
    assert out["is_unusable"] is True
    assert out["is_unscored"] is True
    assert out["score_pct"] is None
    assert "status" not in out  # popped, not just overwritten


def test_mark_unusable_on_a_manual_review_row():
    # status='scored' in the DB, but MANUAL_REVIEW is in UNSCORED_TIERS: the
    # rubric routed it here because the extracted text fell below the
    # readability floor, not because it scored low.
    row = {"tier": "MANUAL_REVIEW", "status": "scored", "score_pct": 0.0}
    out = _mark_unusable(dict(row))
    assert out["is_unusable"] is False
    assert out["is_unscored"] is True
    assert out["score_pct"] is None


def test_mark_unusable_on_a_normal_scored_row():
    row = {"tier": "P2", "status": "scored", "score_pct": 71.4}
    out = _mark_unusable(dict(row))
    assert out["is_unusable"] is False
    assert out["is_unscored"] is False
    assert out["score_pct"] == 71.4


# ---------------------------------------------------------------------------
# 8c. `shape_summary` — finding 4 (a tier appearing with both statuses must
# not lose a row; a tier outside TIER_ORDER must not be dropped).
# ---------------------------------------------------------------------------


def test_shape_summary_aggregates_a_tier_that_appears_with_both_statuses():
    # JOB_SUMMARY_SQL groups by (tier, status), so a tier can legitimately
    # arrive as two rows. The old `{r["tier"]: r for r in rows}` dict-keying
    # let the second row silently overwrite the first.
    rows = [
        {"tier": "P4", "status": "scored", "n": 300, "avg_pct": 40.0, "min_pct": 10.0, "max_pct": 90.0},
        {"tier": "P4", "status": "unusable", "n": 20, "avg_pct": 0.0, "min_pct": 0.0, "max_pct": 0.0},
    ]
    out = shape_summary(rows)

    p4 = next(t for t in out["tiers"] if t["tier"] == "P4")
    # Both rows' counts must survive in the tier bucket...
    assert p4["n"] == 320
    # ...and in the top-level scored/unusable split, split by each ROW's own
    # status (not lost because they share a tier).
    assert out["scored"] == 300
    assert out["unusable"] == 20
    assert out["total"] == 320
    # A tier that is partly unusable is flagged unusable/unscored so its
    # average (now mixing readable and unreadable documents) never renders.
    assert p4["is_unusable"] is True
    assert p4["is_unscored"] is True
    assert p4["avg_pct"] is None


def test_shape_summary_keeps_a_tier_outside_tier_order_visible():
    rows = [
        {"tier": "P1", "status": "scored", "n": 5, "avg_pct": 95.0, "min_pct": 90.0, "max_pct": 100.0},
        {"tier": "SOME_NEW_TIER", "status": "scored", "n": 3, "avg_pct": 60.0, "min_pct": 55.0, "max_pct": 65.0},
    ]
    out = shape_summary(rows)

    tier_names = [t["tier"] for t in out["tiers"]]
    assert "SOME_NEW_TIER" in tier_names, "unknown tier must not be dropped"
    # Known tiers keep their published order; the unknown tier is appended
    # after them rather than interleaved or silently discarded.
    assert tier_names == ["P1", "SOME_NEW_TIER"]
    assert out["scored"] == 8
    assert out["total"] == 8


# ---------------------------------------------------------------------------
# Finding 5: `unscored` is a distinct, additional count (MANUAL_REVIEW rows
# count toward `scored`, as before, but must also be visible as `unscored`).
# ---------------------------------------------------------------------------


def test_shape_summary_reports_unscored_separately_from_scored():
    rows = [
        {"tier": "P4", "status": "scored", "n": 300, "avg_pct": 40.0, "min_pct": 10.0, "max_pct": 90.0},
        {"tier": "MANUAL_REVIEW", "status": "scored", "n": 11, "avg_pct": 0.0, "min_pct": 0.0, "max_pct": 0.0},
        {"tier": "UNUSABLE", "status": "unusable", "n": 6, "avg_pct": 0.0, "min_pct": 0.0, "max_pct": 0.0},
    ]
    out = shape_summary(rows)

    # `scored` keeps its existing (misleading-but-unchanged) meaning: it
    # still includes MANUAL_REVIEW because that row's status is 'scored'.
    assert out["scored"] == 300 + 11
    assert out["unusable"] == 6
    # `unscored` makes the 11 unreadable-but-"scored" rows visible without
    # changing what `scored`/`unusable` mean.
    assert out["unscored"] == 11 + 6
