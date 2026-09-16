"""Unit tests for the Nugget screening read layer.

These tables belong to Nugget (Aymen's agent). The guard below is the
mechanical reason Coco cannot write to them, so it is tested against
deliberately bad SQL rather than only against the happy path.

Run:  python -m pytest webapp/tests/test_nugget_reads.py
"""

from __future__ import annotations

import pytest

from webapp.services.nugget_reads import (
    TIER_ORDER,
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


def test_shape_summary_handles_empty():
    assert shape_summary([]) == {"tiers": [], "scored": 0, "unusable": 0, "total": 0}


def test_is_valid_tier_accepts_published_tiers_only():
    for t in ("P1", "P2", "P3", "P4", "MANUAL_REVIEW", "UNUSABLE"):
        assert is_valid_tier(t) is True
    for t in ("p1", "OK", "", "P5", "DROP TABLE", None):
        assert is_valid_tier(t) is False
