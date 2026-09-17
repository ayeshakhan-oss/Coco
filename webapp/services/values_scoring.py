"""The locked values-scoring rules.

Pure: no database, no model call. The pass/out rule and the Markaz payload shape are
non-negotiable, so they live here and are tested exhaustively rather than being trusted
to an LLM.

Schema note: the value names and the string "Yes"/"No" below are what all 219 existing
scorecards in public.applications.values_scorecard use, verified 2026-09-17. An earlier
version of the skill file documented shorter names and a boolean; those appear in 1 to 5
records each and are drift, not the standard.
"""

from __future__ import annotations

# Canonical order matters: Markaz renders the values in array order.
VALUE_NAMES = (
    "Don't Walk Away from Hard Things",
    "All for One & One for All",
    "Continuously Improve Our Craft",
    "Have Courageous Conversations",
    "Don't Hold On Too Tight",
    "Practice Joy",
)

RATINGS = ("+", "+/-", "-")

NOT_OBSERVED = "Not directly evident in interview."

_EVIDENCE_FIELDS = ("deepDive", "curveBall", "microCase")


class ValuesScorecardError(ValueError):
    """The scorecard does not match the locked shape."""


def tally(ratings: list[str]) -> dict:
    return {
        "plus": ratings.count("+"),
        "plus_minus": ratings.count("+/-"),
        "minus": ratings.count("-"),
    }


def verdict(ratings: list[str]) -> str:
    """PASS = zero minuses AND at most two plus-minuses. Everything else is OUT."""
    t = tally(ratings)
    return "PASS" if (t["minus"] == 0 and t["plus_minus"] <= 2) else "OUT"


def validate_values(values: list[dict]) -> None:
    if len(values) != len(VALUE_NAMES):
        raise ValuesScorecardError(
            f"expected {len(VALUE_NAMES)} values, got {len(values)}"
        )
    for i, (expected_name, v) in enumerate(zip(VALUE_NAMES, values)):
        if v.get("name") != expected_name:
            raise ValuesScorecardError(
                f"value {i} must be {expected_name!r}, got {v.get('name')!r}. "
                "The canonical names are the ones Markaz already holds."
            )
        if v.get("rating") not in RATINGS:
            raise ValuesScorecardError(
                f"{expected_name}: rating must be one of {RATINGS}, got {v.get('rating')!r}"
            )
        for f in _EVIDENCE_FIELDS:
            if not str(v.get(f, "")).strip():
                raise ValuesScorecardError(
                    f"{expected_name}: {f} is blank. Use NOT_OBSERVED if it was not seen."
                )
