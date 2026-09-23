"""The locked KCD evaluation rules (Skill 02, component: kcd-evaluation).

Pure: no model, no database. The scale, the verdict bands, the GWC threshold,
the conditional rule and the incomplete-submission handling live here and are
tested directly.

SOURCE OF TRUTH: .claude/skills/02_candidate-evaluation/kcd-evaluation.md.

⚠️ ONE THING THE SOP STILL DOES NOT SETTLE, AND ONE NOW SETTLED:

   1. THE CRITERIA. The SOP names the framework "Knowledge, Capacity, Design"
      and then refers to a "default 6 criteria" that is enumerated nowhere in
      this repository. The three below are the framework's own three named
      components -- the minimal reading of what the SOP actually specifies --
      weighted equally because it gives no weights. A per-job framework may
      override both. If Ayesha's six exist somewhere, they replace DIMENSIONS
      and nothing else changes.

   2. THE BOTTOM OF THE SCALE. ✅ SETTLED 2026-09-23 (Ayesha): the scale runs
      0 to 5 WITH A REAL ZERO, and kcd-evaluation.md has been updated to match.
      It previously bottomed out at 1 with 0 reserved for "not submitted",
      which is the anchor floor CLAUDE.md Rule 27 forbids: a 20% floor under
      every dimension, and on the RM round that put all 25 candidates above a
      published bar.

      The SOP's underlying worry -- that weak work would "look identical to
      unsubmitted" -- is already answered structurally and not by the scale:
      an incomplete submission is pulled out of the ranking entirely, marked
      with an asterisk and never ranked against a complete one (see
      `rank_results`). A zero on a dimension of a submitted case study and a
      candidate who submitted nothing are never in the same list.

🔒 TERMINOLOGY. "KCD" is an internal name only. Any report or email that leaves
   this team says "case study" (memory/feedback_terminology.md, Ayesha
   2026-04-02).
"""

from __future__ import annotations

import logging
from typing import Iterable, Optional

log = logging.getLogger("webapp.kcd_evaluation")

# ⚠️ A derivation, not a quote -- see the module docstring. Equal weights
# because the SOP gives none; a role-specific framework may override them.
DIMENSIONS = (
    {
        "key": "knowledge",
        "label": "Knowledge",
        "weight": 34,
        "asks": "Do they understand the domain, the data and what the question "
                "actually was?",
    },
    {
        "key": "capacity",
        "label": "Capacity",
        "weight": 33,
        "asks": "Could they carry this out? Is the reasoning theirs, and does it "
                "hold up?",
    },
    {
        "key": "design",
        "label": "Design",
        "weight": 33,
        "asks": "Is what they built well shaped for the problem, and did they "
                "say what it costs?",
    },
)

#: Halves are REQUIRED by the SOP: "Use fractional scores (4.5, 3.5) for
#: candidates between whole numbers". Whole numbers only would compress
#: differences the SOP says are meaningful.
SCORES = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)
_MAX = 5.0
_KEYS = {d["key"] for d in DIMENSIONS}

#: Verdict bands, exactly as the SOP states them.
STRONG_HIRE = "strong_hire"
HIRE = "hire"
CONDITIONAL = "conditional"
BORDERLINE = "borderline"
NOT_RECOMMENDED = "not_recommended"
VERDICTS = (STRONG_HIRE, HIRE, CONDITIONAL, BORDERLINE, NOT_RECOMMENDED)

_BANDS = (
    (85.0, STRONG_HIRE),
    (70.0, HIRE),
    (55.0, CONDITIONAL),
    (40.0, BORDERLINE),
)

#: "60%+ advances to GWC. State explicitly in report and Pipeline
#: Recommendations." Kept as a constant so the number cannot drift between the
#: computation and the sentence a reader sees.
GWC_ADVANCEMENT_THRESHOLD = 60.0

#: Caps the SOP states outright. Both are written as rules BEFORE scoring and
#: applied without discretion, which is the fix Rule 27 prescribes.
CAP_INSIGHT_WITHOUT_EVIDENCE = 3.0
CAP_EVIDENCE_WITHOUT_INTERPRETATION = 3.0


class KCDEvaluationError(ValueError):
    """The evaluation does not match the locked shape."""


def validate_scores(scores: dict) -> None:
    keys = set(scores)
    if keys != _KEYS:
        missing, extra = sorted(_KEYS - keys), sorted(keys - _KEYS)
        raise KCDEvaluationError(f"missing {missing}, unexpected {extra}")
    for k, v in scores.items():
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise KCDEvaluationError(f"{k}: score must be a number, got {v!r}")
        if float(v) not in SCORES:
            raise KCDEvaluationError(
                f"{k}: score must be a whole or half step from 0 to 5, got {v!r}"
            )


def weighted_total(scores: dict, weights: Optional[dict] = None) -> float:
    """The percentage. A role-specific framework may supply its own weights;
    they must cover exactly the same dimensions and sum to 100."""
    validate_scores(scores)
    if weights is None:
        weights = {d["key"]: d["weight"] for d in DIMENSIONS}
    else:
        if set(weights) != _KEYS:
            raise KCDEvaluationError(
                f"weights must cover exactly {sorted(_KEYS)}, got {sorted(weights)}"
            )
        if round(sum(weights.values()), 6) != 100:
            raise KCDEvaluationError(
                f"weights must sum to 100, got {sum(weights.values())}"
            )
    return round(sum(float(scores[k]) / _MAX * weights[k] for k in _KEYS), 2)


def verdict(total: float) -> str:
    for floor, label in _BANDS:
        if total >= floor:
            return label
    return NOT_RECOMMENDED


def advances_to_gwc(total: float) -> bool:
    """The SOP's advancement rule, as a function rather than a sentence a
    report might restate with a different number."""
    return total >= GWC_ADVANCEMENT_THRESHOLD


def apply_caps(scores: dict, *, insight_without_evidence: Iterable[str] = (),
               evidence_without_interpretation: Iterable[str] = ()) -> dict:
    """The SOP's two caps: "Insight without evidence = cap at 3" and "Evidence
    without interpretation = cap at 3".

    Applied mechanically rather than left to judgement, which is Rule 27's own
    prescription ("write the benchmark's caps as rules BEFORE scoring and apply
    them without discretion"). A cap is a CEILING, never a floor: it can only
    lower a score, never raise one that already sits below it
    (memory/lesson_marking_cap_is_a_ceiling_2026_09_11.md, where a candidate
    was marked BELOW a cap and rejected live at 62 before being recalibrated to
    72 on her own appeal).
    """
    validate_scores(scores)
    capped = dict(scores)
    for keys, cap in (
        (insight_without_evidence, CAP_INSIGHT_WITHOUT_EVIDENCE),
        (evidence_without_interpretation, CAP_EVIDENCE_WITHOUT_INTERPRETATION),
    ):
        for key in keys:
            if key not in _KEYS:
                raise KCDEvaluationError(f"cannot cap unknown dimension {key!r}")
            capped[key] = min(float(capped[key]), cap)
    return capped


def validate_conditional(verdict_label: str, condition: Optional[str]) -> None:
    """A CONDITIONAL verdict must say what the condition IS.

    The SOP's own Common Mistakes table: "No conditional statement --
    CONDITIONAL verdicts not actionable -- State: 'Condition: [specific
    thing]'". A conditional with no condition is a hedge, not a decision.
    """
    if verdict_label != CONDITIONAL:
        return
    if not isinstance(condition, str) or not condition.strip():
        raise KCDEvaluationError(
            "a CONDITIONAL verdict must state its condition explicitly; without "
            "one it is not actionable"
        )


# --------------------------------------------------------------------------
# Incomplete submissions
# --------------------------------------------------------------------------


def format_incomplete_score(total: float) -> str:
    """The SOP's own notation: an asterisk and a plain statement that the
    number is a floor. Kept here so every report renders it identically."""
    return f"{total:.1f}%* — incomplete submission, a floor and not a capability read"


def rank_results(results: list[dict]) -> dict:
    """Split a cohort into a ranking and a separate incomplete section.

    The SOP is unambiguous: an incomplete submission is "excluded from main
    ranking entirely", handled in its own section, and "never ranked above a
    full submission". Returning one merged list sorted by total would break
    that the first time a strong partial outscored a weak complete one, so the
    two never share a list at all.

    Each result needs `total` and `incomplete`; anything else is carried
    through untouched.
    """
    for r in results:
        if "total" not in r or "incomplete" not in r:
            raise KCDEvaluationError(
                "every result needs 'total' and 'incomplete' to be ranked"
            )

    ranked = sorted(
        (r for r in results if not r["incomplete"]), key=lambda r: -r["total"]
    )
    incomplete = sorted(
        (r for r in results if r["incomplete"]), key=lambda r: -r["total"]
    )
    return {
        "ranked": ranked,
        "incomplete": incomplete,
        "note": (
            f"{len(incomplete)} incomplete submission(s) are listed separately and "
            "are not ranked. Their scores are floors, not capability reads."
        ) if incomplete else None,
    }


# --------------------------------------------------------------------------
# Cross-check with Noah
# --------------------------------------------------------------------------

ALIGNED_DELTA = 5.0
DIVERGENT_DELTA = 10.0


def cross_check(ours: float, theirs: Optional[float]) -> dict:
    """Compare our total against Noah's on the same candidate.

    The SOP: aligned within 5 points, proceed; diverging by more than 10, flag
    to Ayesha before any live send. The 5-to-10 gap it leaves unnamed is
    reported as `review` rather than quietly rounded into one of the two.
    """
    if theirs is None:
        return {"status": "not_available", "delta": None,
                "note": "No second evaluation to compare against."}
    delta = round(abs(ours - theirs), 2)
    if delta <= ALIGNED_DELTA:
        status, note = "aligned", "Within 5 points. Proceed."
    elif delta > DIVERGENT_DELTA:
        status, note = "divergent", (
            "More than 10 points apart. Flag to Ayesha before anything goes out."
        )
    else:
        status, note = "review", (
            "Between 5 and 10 points apart. The SOP does not name this range; "
            "worth a look before proceeding."
        )
    return {"status": status, "delta": delta, "note": note}
