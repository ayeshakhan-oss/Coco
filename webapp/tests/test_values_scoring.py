"""The non-negotiable values-scoring rules, tested without an LLM or a database.

PASS is zero minuses AND at most two plus-minuses. Everything else is OUT. This is
computed in code and never left to a model, so it is tested exhaustively here.
"""

from __future__ import annotations

import itertools

import pytest

from webapp.services.values_scoring import (
    MARKAZ_KEYS,
    NOT_OBSERVED,
    RATINGS,
    VALUE_NAMES,
    ValuesScorecardError,
    build_markaz_payload,
    tally,
    validate_markaz_payload,
    validate_values,
    verdict,
)


def _values(ratings):
    return [
        {"name": n, "deepDive": "d", "curveBall": "c", "microCase": "m", "rating": r}
        for n, r in zip(VALUE_NAMES, ratings)
    ]


def test_canonical_names_and_ratings():
    assert VALUE_NAMES == (
        "Don't Walk Away from Hard Things",
        "All for One & One for All",
        "Continuously Improve Our Craft",
        "Have Courageous Conversations",
        "Don't Hold On Too Tight",
        "Practice Joy",
    )
    assert RATINGS == ("+", "+/-", "-")


def test_verdict_exhaustively_over_every_possible_scorecard():
    # All 3^6 = 729 combinations. The rule must hold for every one.
    for combo in itertools.product(RATINGS, repeat=6):
        got = verdict(list(combo))
        minuses = combo.count("-")
        plus_minuses = combo.count("+/-")
        expected = "PASS" if (minuses == 0 and plus_minuses <= 2) else "OUT"
        assert got == expected, f"{combo}: got {got}, expected {expected}"


def test_verdict_named_cases():
    assert verdict(["+"] * 6) == "PASS"
    assert verdict(["+", "+", "+", "+", "+", "+/-"]) == "PASS"
    assert verdict(["+", "+", "+", "+", "+/-", "+/-"]) == "PASS"
    # Three plus-minuses is OUT even with no minus.
    assert verdict(["+", "+", "+", "+/-", "+/-", "+/-"]) == "OUT"
    # A single minus is OUT regardless of everything else.
    assert verdict(["+", "+", "+", "+", "+", "-"]) == "OUT"


def test_tally():
    assert tally(["+", "+", "+/-", "-", "+", "+/-"]) == {"plus": 3, "plus_minus": 2, "minus": 1}


def test_validate_rejects_wrong_shape():
    with pytest.raises(ValuesScorecardError):
        validate_values(_values(["+"] * 5)[:5])            # only five values
    with pytest.raises(ValuesScorecardError):
        bad = _values(["+"] * 6); bad[0]["name"] = "Don't Walk Away"
        validate_values(bad)                                # the OLD skill-file name
    with pytest.raises(ValuesScorecardError):
        bad = _values(["+"] * 6); bad[2], bad[3] = bad[3], bad[2]
        validate_values(bad)                                # out of canonical order
    with pytest.raises(ValuesScorecardError):
        bad = _values(["+"] * 6); bad[1]["rating"] = "++"
        validate_values(bad)                                # invalid rating token
    with pytest.raises(ValuesScorecardError):
        bad = _values(["+"] * 6); bad[4]["curveBall"] = "   "
        validate_values(bad)                                # blank evidence


def test_validate_accepts_the_not_observed_sentinel():
    ok = _values(["+"] * 6)
    ok[3]["curveBall"] = NOT_OBSERVED
    validate_values(ok)  # must not raise


def _ok_values():
    return [
        {"name": n, "deepDive": "d", "curveBall": "c", "microCase": "m", "rating": "+"}
        for n in VALUE_NAMES
    ]


def test_payload_shape_matches_the_live_records():
    p = build_markaz_payload(
        candidate_name="Muhammad Junaid",
        host="Ayesha Khan",
        values=_ok_values(),
        final_comments="PASS - 6(+) / 0(+/-) / 0(-)",
        proceed=True,
        date="Aug 14, 2026",
    )
    assert set(p) == MARKAZ_KEYS
    assert p["candidateName"] == "Muhammad Junaid"
    assert p["noteTaker"] == "Coco (AI P&C Assistant)"
    assert p["date"] == "Aug 14, 2026"
    # The live records store a STRING, not a boolean. 215 of 219.
    assert p["proceedToRightSeat"] == "Yes"
    assert isinstance(p["proceedToRightSeat"], str)
    assert [v["name"] for v in p["values"]] == list(VALUE_NAMES)


def test_proceed_false_is_the_string_no():
    p = build_markaz_payload(
        candidate_name="X", host="Ayesha Khan", values=_ok_values(),
        final_comments="OUT", proceed=False,
    )
    assert p["proceedToRightSeat"] == "No"


def test_payload_rejects_a_boolean_proceed_value():
    p = build_markaz_payload(
        candidate_name="X", host="Ayesha Khan", values=_ok_values(),
        final_comments="PASS", proceed=True,
    )
    p["proceedToRightSeat"] = True          # the shape the old skill file documented
    with pytest.raises(ValuesScorecardError):
        validate_markaz_payload(p)


def test_payload_rejects_extra_or_missing_keys():
    p = build_markaz_payload(
        candidate_name="X", host="Ayesha Khan", values=_ok_values(),
        final_comments="PASS", proceed=True,
    )
    with pytest.raises(ValuesScorecardError):
        validate_markaz_payload({**p, "extra": 1})
    with pytest.raises(ValuesScorecardError):
        validate_markaz_payload({k: v for k, v in p.items() if k != "noteTaker"})


def test_draft_table_lives_in_the_coco_schema():
    """public is inside Markaz's Replit schema-push blast radius; coco is not."""
    from webapp.models import ValuesScorecardDraft

    assert ValuesScorecardDraft.__table__.schema == "coco"
