"""Unit tests for the Nugget screening read layer.

These tables belong to Nugget (Aymen's agent). The guard below is the
mechanical reason Coco cannot write to them, so it is tested against
deliberately bad SQL rather than only against the happy path.

Run:  python -m pytest webapp/tests/test_nugget_reads.py
"""

from __future__ import annotations

import pytest

from webapp.services.nugget_reads import assert_read_only


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
