"""The locked case-study scoring rules.

Pure: no model, no database. Weights, the 0-5 conversion, the bands and the flag
overrides are non-negotiable, so they live here and are tested directly.

🔒 The scale runs 0-5 WITH A REAL ZERO (Ayesha, 2026-09-22). Anchoring at 1 floors
every dimension at 20% of its weight, which is the defect recorded in CLAUDE.md
Rule 27: it put all 25 RM case studies above the published bar. An absent or wholly
wrong answer scores 0, not a middling guess. The bands are deliberately unchanged,
so totals fall and the bar rises.
"""

from __future__ import annotations

DIMENSIONS = (
    {"key": "data_judgment", "label": "Data judgment", "weight": 20},
    {"key": "execution_specificity", "label": "Execution specificity", "weight": 25},
    {"key": "stakeholder_craft", "label": "Stakeholder craft", "weight": 20},
    {"key": "commercial_honesty", "label": "Commercial honesty", "weight": 15},
    {"key": "decision_discipline", "label": "Decision discipline", "weight": 10},
    {"key": "signal_self_awareness", "label": "Signal & self-awareness", "weight": 10},
)

SCORES = (0, 1, 2, 3, 4, 5)
_MAX = 5

# A flag can outrank a high total. Only `disqualifying` changes the band.
FLAGS = {
    "fabricated_data": "disqualifying",
    "undisclosed_ai": "serious",
    "materially_incomplete": "serious",
    "instruction_breach": "note",
    "consent_blindness": "note",
}

_KEYS = {d["key"] for d in DIMENSIONS}


class CaseStudyScoringError(ValueError):
    """The score set does not match the locked shape."""


def validate_scores(scores: dict) -> None:
    keys = set(scores)
    if keys != _KEYS:
        missing, extra = sorted(_KEYS - keys), sorted(keys - _KEYS)
        raise CaseStudyScoringError(f"missing {missing}, unexpected {extra}")
    for k, v in scores.items():
        # bool is an int subclass; reject it explicitly.
        if isinstance(v, bool) or not isinstance(v, int) or v not in SCORES:
            raise CaseStudyScoringError(f"{k}: score must be an integer in {SCORES}, got {v!r}")


def weighted_total(scores: dict) -> float:
    validate_scores(scores)
    total = sum(scores[d["key"]] / _MAX * d["weight"] for d in DIMENSIONS)
    return round(total, 2)


def band(total: float, flags: list[str]) -> str:
    if any(FLAGS.get(f) == "disqualifying" for f in flags):
        return "disqualified"
    if total >= 80:
        return "strong_yes"
    if total >= 65:
        return "yes"
    if total >= 50:
        return "borderline"
    return "no"
