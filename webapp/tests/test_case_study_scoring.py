"""The locked case-study scoring rules, tested without a model or a database.

The zero is the point: anchoring at 1 floors every dimension at 20% of its weight,
which is the defect that put all 25 RM case studies above the bar (CLAUDE.md Rule 27).
"""

from __future__ import annotations

import pytest

from webapp.services.case_study_scoring import (
    DIMENSIONS,
    SCORES,
    CaseStudyScoringError,
    band,
    validate_scores,
    weighted_total,
)


def _all(n):
    return {d["key"]: n for d in DIMENSIONS}


def test_weights_are_the_locked_six_and_sum_to_100():
    assert [d["weight"] for d in DIMENSIONS] == [20, 25, 20, 15, 10, 10]
    assert sum(d["weight"] for d in DIMENSIONS) == 100
    assert len(DIMENSIONS) == 6


def test_the_scale_has_a_real_zero():
    assert SCORES == (0, 1, 2, 3, 4, 5)
    # THE defect this rubric change exists to remove: all-minimum must be 0, not 20.
    assert weighted_total(_all(0)) == 0.0


def test_conversion_is_linear_on_the_full_scale():
    assert weighted_total(_all(5)) == 100.0
    assert weighted_total(_all(4)) == 80.0
    assert weighted_total(_all(3)) == 60.0
    assert weighted_total(_all(2)) == 40.0
    assert weighted_total(_all(1)) == 20.0


def test_weighting_is_per_dimension_not_flat():
    # Only Execution specificity (weight 25) at full marks.
    scores = _all(0)
    scores["execution_specificity"] = 5
    assert weighted_total(scores) == 25.0


def test_bands_match_the_locked_thresholds():
    assert band(80.0, []) == "strong_yes"
    assert band(95.0, []) == "strong_yes"
    assert band(79.9, []) == "yes"
    assert band(65.0, []) == "yes"
    assert band(64.9, []) == "borderline"
    assert band(50.0, []) == "borderline"
    assert band(49.9, []) == "no"
    assert band(0.0, []) == "no"


def test_fabricated_data_disqualifies_regardless_of_total():
    assert band(100.0, ["fabricated_data"]) == "disqualified"
    assert band(92.0, ["fabricated_data", "undisclosed_ai"]) == "disqualified"
    # A serious-but-not-disqualifying flag does NOT override the band.
    assert band(92.0, ["undisclosed_ai"]) == "strong_yes"


def test_benchmark_table_is_in_the_coco_schema():
    from webapp.models import EvalBenchmark

    assert EvalBenchmark.__table__.schema == "coco"


def test_benchmark_carries_a_qa_gate():
    from webapp.models import EvalBenchmark

    cols = {c.name for c in EvalBenchmark.__table__.columns}
    # Rule 0 is enforced by requiring these before a run may start.
    assert {"qa_approved_at", "qa_approved_by", "status"} <= cols


def test_validate_rejects_a_bad_score_set():
    with pytest.raises(CaseStudyScoringError):
        validate_scores({d["key"]: 3 for d in DIMENSIONS[:5]})     # missing one
    with pytest.raises(CaseStudyScoringError):
        bad = _all(3); bad["data_judgment"] = 6
        validate_scores(bad)                                        # out of range
    with pytest.raises(CaseStudyScoringError):
        bad = _all(3); bad["not_a_dimension"] = 3
        validate_scores(bad)                                        # unknown key
    with pytest.raises(CaseStudyScoringError):
        bad = _all(3); bad["data_judgment"] = 2.5
        validate_scores(bad)                                        # not an integer
    validate_scores(_all(0))                                        # zero is VALID
