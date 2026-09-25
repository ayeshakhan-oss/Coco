"""Turning a model's dimension scores into a tier. Pure functions, no I/O.

Every rule here is read from the rubric row itself (`dimensions`, `thresholds`,
`hard_filters`, `manual_review_rules`), never hardcoded, because Nugget stores
one rubric per job and they differ. This module only knows the SHAPE.

🔴 THE SCORE IS COMPUTED HERE, NEVER READ OFF THE MODEL. `cv_screening.screen_cv`
already works this way and says why: a model asked for a total will produce one
whether or not it follows from its own per-dimension scores. The model supplies
raw 0-5 scores and evidence; the weighting, the percentage, the gates and the
tier are arithmetic.

🔴 THE BOTTOM OF THE SCALE IS REAL. A 0 anchor means absence. Coco's own RM
case-study round put all 25 submissions above a published 70% bar because its
anchors started at 1, which floors every dimension at a fifth of its weight
(memory/lesson_scoring_anchor_floor_inflation_2026_09_02.md). Nugget's rubrics
say "An absent skill scores 0, not a middling guess" and its live data bears
that out: 612 scored candidates on Job 38 average 44.0% across the full range.
Do not add a floor here.
"""

from __future__ import annotations

from typing import Any, Optional

# Published tier order, shared with nugget_reads.TIER_ORDER.
TIER_ORDER = ("P1", "P2", "P3", "P4", "MANUAL_REVIEW", "UNUSABLE")

# Tiers that carry no meaningful percentage.
UNSCORED_TIERS = ("MANUAL_REVIEW", "UNUSABLE")

CONFIDENCE_VALUES = ("high", "medium", "low")


class TieringError(ValueError):
    """The model's output does not fit the rubric it was scored against."""


def dimension_keys(rubric: dict) -> list[str]:
    return [d["key"] for d in rubric.get("dimensions") or []]


def score_dimensions(rubric: dict, raw_scores: dict) -> tuple[dict, float, float]:
    """Weight the model's 0-5 scores against the rubric.

    Returns (dimension_scores, total, max_score) where `dimension_scores`
    matches the shape Nugget stores: one entry per dimension carrying `raw`,
    `weight`, `weighted` and the model's `evidence`.

    Raises rather than defaulting a missing dimension to 0: a rubric dimension
    the model did not answer is a malformed response, and silently scoring it
    absent would look identical to a candidate who genuinely lacks the skill.
    """
    dims = rubric.get("dimensions") or []
    if not dims:
        raise TieringError("rubric has no dimensions")

    out: dict[str, dict] = {}
    total = 0.0
    weight_total = 0.0

    for dim in dims:
        key = dim["key"]
        if key not in raw_scores:
            raise TieringError(f"model did not score the dimension {key!r}")
        entry = raw_scores[key]
        # Accept either a bare number or {"raw": n, "evidence": [...]}.
        if isinstance(entry, dict):
            raw = entry.get("raw", entry.get("score"))
            evidence = entry.get("evidence") or []
        else:
            raw = entry
            evidence = []
        try:
            raw = int(raw)
        except (TypeError, ValueError) as exc:
            raise TieringError(f"dimension {key!r} scored {entry!r}, not 0-5") from exc
        if not 0 <= raw <= 5:
            raise TieringError(f"dimension {key!r} scored {raw}, outside 0-5")

        weight = float(dim.get("weight") or 0)
        weighted = raw * weight
        total += weighted
        weight_total += weight * 5
        out[key] = {
            "raw": raw,
            "weight": weight,
            "weighted": round(weighted, 4),
            "evidence": list(evidence)[:6],
        }

    max_score = float(rubric.get("max_score") or 0) or weight_total
    return out, round(total, 4), max_score


def score_percent(total: float, max_score: float, *, weight_total: float = 0.0) -> float:
    """Percentage of the rubric's maximum.

    `max_score` on every live rubric is 100 while the raw weighted total maxes
    out at sum(weight)*5, so the two are different scales and dividing by the
    wrong one silently compresses every score. Normalise through the weights.
    """
    denominator = weight_total or max_score
    if denominator <= 0:
        return 0.0
    return round(min(100.0, max(0.0, total / denominator * 100.0)), 2)


def evaluate_hard_filters(rubric: dict, flags: Any) -> tuple[list[dict], Optional[str]]:
    """Normalise the model's hard-filter verdicts and decide whether any rejects.

    Each filter reports `pass`, `fail` or `unknown`. The wording in Nugget's
    rubrics is deliberately protective and is preserved here as behaviour:

      * "Report a hard filter as unknown when the CV is silent. Silence is not a
        refusal, and it must never read as one." -> an unknown NEVER rejects
        unless the rubric's own `on_unknown` says so.
      * University tier: "Never fail on this. It is a tie-breaker between
        comparable candidates and nothing more." -> such a filter carries
        action `flag`, and a flag never changes the tier.

    Returns (normalised flags, rejection reason or None).
    """
    declared = {f["key"]: f for f in (rubric.get("hard_filters") or [])}
    reported: dict[str, Any] = {}
    if isinstance(flags, dict):
        reported = flags
    elif isinstance(flags, list):
        for item in flags:
            if isinstance(item, dict) and "key" in item:
                reported[item["key"]] = item.get("result", item.get("status"))

    out: list[dict] = []
    reject_reason: Optional[str] = None

    for key, spec in declared.items():
        raw = reported.get(key)
        if isinstance(raw, dict):
            result = raw.get("result") or raw.get("status")
            note = raw.get("note") or raw.get("reason")
        else:
            result = raw
            note = None
        result = (result or "unknown").lower()
        if result not in ("pass", "fail", "unknown"):
            result = "unknown"

        action = (spec.get("action") or "flag").lower()
        on_unknown = (spec.get("on_unknown") or "unknown").lower()

        effective = result
        if result == "unknown" and on_unknown in ("pass", "fail"):
            effective = on_unknown

        out.append(
            {
                "key": key,
                "label": spec.get("label") or key,
                "result": result,
                "effective": effective,
                "action": action,
                "note": note,
            }
        )

        if action == "reject" and effective == "fail" and reject_reason is None:
            reject_reason = spec.get("label") or key

    return out, reject_reason


def _gate_passes(gate: Optional[dict], dimension_scores: dict) -> tuple[bool, Optional[str]]:
    """A threshold gate: minimum raw scores on named dimensions.

    Gates exist so a strong aggregate cannot mask a critical weakness, e.g.
    `p1: {min_dimension: {must_have_skills: 4, stack_match: 3}}`.
    """
    if not gate:
        return True, None
    minimums = gate.get("min_dimension") or {}
    for key, minimum in minimums.items():
        got = dimension_scores.get(key, {}).get("raw")
        if got is None or got < minimum:
            label = key.replace("_", " ")
            return False, f"{label} scored {got if got is not None else 'nothing'}, below the {minimum} this tier requires"
    return True, None


def assign_tier(
    *,
    rubric: dict,
    dimension_scores: dict,
    pct: float,
    hard_filter_reject: Optional[str] = None,
) -> tuple[str, str]:
    """(tier, tier_reason). The reason is written for a human to read."""
    if hard_filter_reject:
        return "P4", (
            f"Did not meet a required condition for this role: {hard_filter_reject}."
        )

    thresholds = rubric.get("thresholds") or {}
    gates = thresholds.get("gates") or {}

    for tier in ("p1", "p2", "p3"):
        bar = thresholds.get(tier)
        if bar is None:
            continue
        if pct < float(bar):
            continue
        ok, why_not = _gate_passes(gates.get(tier), dimension_scores)
        if ok:
            return tier.upper(), (
                f"Scored {pct:g}%, at or above the {tier.upper()} bar of {bar:g}."
            )
        # Met the percentage but failed the gate: fall through to the next
        # tier down, and say so rather than reporting a bare number.
        return _below(thresholds, gates, dimension_scores, pct, blocked=(tier.upper(), why_not))

    lowest = thresholds.get("p3")
    if lowest is not None:
        return "P4", f"Scored {pct:g}%, below the P3 bar of {float(lowest):g}."
    return "P4", f"Scored {pct:g}%."


def _below(thresholds, gates, dimension_scores, pct, *, blocked) -> tuple[str, str]:
    """Next tier down after a gate blocked a higher one."""
    blocked_tier, why_not = blocked
    order = [t for t in ("p1", "p2", "p3") if thresholds.get(t) is not None]
    try:
        start = order.index(blocked_tier.lower()) + 1
    except ValueError:
        start = len(order)

    for tier in order[start:]:
        bar = float(thresholds[tier])
        if pct < bar:
            continue
        ok, _ = _gate_passes(gates.get(tier), dimension_scores)
        if ok:
            return tier.upper(), (
                f"Scored {pct:g}%, which reaches {blocked_tier}, but {why_not}. "
                f"Placed at {tier.upper()}."
            )
    return "P4", (
        f"Scored {pct:g}%, which reaches {blocked_tier}, but {why_not}."
    )


# --------------------------------------------------------------------------
# Resume health
# --------------------------------------------------------------------------

# Below this many characters a CV is treated as unreadable rather than weak.
# Nugget's rubrics carry their own `manual_review_rules.min_resume_chars`
# (500 on every live rubric); this is the floor for "there is nothing here".
HARD_UNUSABLE_CHARS = 120

# Coco's own lesson: count WORDS, not characters. The pypdf letter-spacing
# defect produces a 20,089-character "CV" containing 15 real words, which every
# character-based check passes (CLAUDE.md Rule 32).
MIN_HEALTHY_WORDS = 250


def resume_health(text: Optional[str]) -> tuple[int, list[str]]:
    """0-100 with the reasons. Cheap, deterministic, no model call.

    🔴 This decides whether a candidate is SCORED or sent to a human, so it
    must never flatter a broken extraction. Nugget's own data shows what
    happens when it does: a live eval carries `resume_health` 85.5 on 21
    extracted characters (docs/nugget_screening_defects_2026_09_15.md).
    """
    if not text or not text.strip():
        return 0, ["no text could be extracted from the uploaded file"]

    stripped = text.strip()
    words = stripped.split()
    issues: list[str] = []
    health = 100

    if len(stripped) < HARD_UNUSABLE_CHARS:
        return 0, [f"only {len(stripped)} characters extracted"]

    if len(words) < MIN_HEALTHY_WORDS:
        # Proportional, so 240 words is not treated like 15.
        shortfall = 1 - (len(words) / MIN_HEALTHY_WORDS)
        health -= int(60 * shortfall)
        issues.append(f"only {len(words)} words extracted")

    # The letter-spacing signature: many characters, very few words.
    if words:
        avg_word = sum(len(w) for w in words) / len(words)
        if avg_word > 20:
            health -= 40
            issues.append(
                f"average word length {avg_word:.0f} characters, which is the "
                "signature of a PDF that extracted one letter per token"
            )

    alpha = sum(c.isalpha() or c.isspace() for c in stripped)
    if alpha / len(stripped) < 0.6:
        health -= 25
        issues.append("under 60 percent of the extracted text is letters")

    return max(0, min(100, health)), issues


def route_unscorable(
    *, health: int, chars: int, rules: Optional[dict]
) -> Optional[tuple[str, str]]:
    """(tier, reason) when a CV must not be scored at all, else None.

    🔴 UNUSABLE and MANUAL_REVIEW are NEVER rejections. Both mean a human has
    to open the actual document. They carry no percentage, and reporting either
    as a weak candidate is the defect this function exists to prevent.
    """
    rules = rules or {}
    min_chars = int(rules.get("min_resume_chars") or 500)
    min_health = int(rules.get("min_resume_health") or 60)

    if health == 0 or chars < HARD_UNUSABLE_CHARS:
        return "UNUSABLE", (
            "The uploaded CV could not be read, so this application has not been "
            "scored. It needs a person to open the file."
        )
    if chars < min_chars:
        return "MANUAL_REVIEW", (
            f"Only {chars} characters could be extracted, below the {min_chars} "
            "this rubric requires before scoring. It needs a person to read it."
        )
    if health < min_health:
        return "MANUAL_REVIEW", (
            f"Extracted text scored {health} for readability, below the "
            f"{min_health} this rubric requires. It needs a person to read it."
        )
    return None
