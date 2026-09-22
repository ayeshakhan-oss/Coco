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

import logging
from typing import Optional

log = logging.getLogger("webapp.case_study_scoring")

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


# --------------------------------------------------------------------------
# Model call: submission + benchmark -> scored dimensions. The rules above
# never leave the model's hands; everything below runs its output back
# through them before anything is trusted.
# --------------------------------------------------------------------------


def _validate_evidence(evidence: dict) -> None:
    """Every dimension must carry a non-empty evidence citation (Rule 1 of the
    rubric: "A dimension score with no quoted line, slide number or figure
    behind it is not a score, it is an impression"). A blank or
    whitespace-only citation is rejected exactly like a malformed score, and
    a response is never repaired to add one."""
    keys = set(evidence)
    if keys != _KEYS:
        missing, extra = sorted(_KEYS - keys), sorted(keys - _KEYS)
        raise CaseStudyScoringError(
            f"evidence: missing {missing}, unexpected {extra}"
        )
    for k, v in evidence.items():
        if not isinstance(v, str) or not v.strip():
            raise CaseStudyScoringError(
                f"{k}: evidence citation is blank. Rule 1 requires a quoted "
                "line, slide number or figure behind every score."
            )


def _validate_flags(flags) -> list:
    """`flags` is optional (most submissions carry none) but, when present,
    must be a list drawn only from the locked FLAGS vocabulary -- never an
    invented flag name riding along into the band computation."""
    if flags is None:
        return []
    if not isinstance(flags, list):
        raise CaseStudyScoringError(f"'flags' must be a list, got {type(flags).__name__}")
    unknown = [f for f in flags if f not in FLAGS]
    if unknown:
        raise CaseStudyScoringError(
            f"unknown flag(s) {unknown}; must be among {sorted(FLAGS)}"
        )
    return flags


def _call_model(*, corpus: str, benchmark_body: str, candidate_name: str, role: str) -> tuple:
    """One model call: submission + benchmark in, raw parsed JSON out.

    Module-level (not a method) so tests can monkeypatch it directly and never
    make a real Anthropic call. Reuses webapp.services.drafting.get_drafter(),
    the existing client with its model-fallback chain, rather than building a
    second client. Imported locally to avoid a module-level import cycle,
    exactly like values_scoring._call_model: case_study_prompt.py (imported
    here) reads DIMENSIONS/FLAGS/SCORES from this module, so the import has
    to happen after this module is fully defined.

    Returns (parsed_json, model_name). Raises whatever the drafter raises
    (DraftingUnavailable, an Anthropic SDK error, a JSON parse error from a
    non-JSON reply) -- none of that is swallowed here.
    """
    from . import drafting
    from ..prompts import case_study_prompt

    drafter = drafting.get_drafter()
    system = case_study_prompt.system_prompt()
    user = case_study_prompt.build_user_prompt(
        corpus=corpus, benchmark_body=benchmark_body,
        candidate_name=candidate_name, role=role,
    )
    parsed = drafter.draft(
        system=system,
        user=user,
        email_type="case_study_scoring",
        first_name=candidate_name,
        role=role,
        prior_violations=None,
        attempt=0,
    )
    model_name = getattr(drafter, "model", None) or getattr(drafter, "name", "unknown")
    return parsed, model_name


def score_submission(*, corpus: str, benchmark_body: str, candidate_name: str, role: str) -> dict:
    """Turn a candidate's case-study submission into a scored, banded result.

    Calls the model, validates its response against the locked shape
    (validate_scores + _validate_evidence + _validate_flags), and NEVER
    repairs a malformed response: a response that fails validation --
    including a response that is not even parseable JSON, which surfaces as a
    plain ValueError out of _call_model/drafting rather than a
    CaseStudyScoringError -- is retried once with a fresh model call (not a
    repair of the old one), and if the second attempt is also malformed this
    raises CaseStudyScoringError (never a bare ValueError) rather than
    coercing, guessing, or filling in a blank field.

    The total and the band are ALWAYS computed here by weighted_total() and
    band(), never taken from the model even if it volunteers one (the output
    contract tells it not to; this function does not trust that instruction
    either) -- nothing here ever reads a "total" or "band" key off the parsed
    response, so a model returning an inflated total is simply ignored. A
    "fabricated_data" flag forces band() to "disqualified" regardless of the
    total, exactly like the pure rule above.

    Returns {"scores": {...}, "evidence": {...}, "flags": [...],
    "total": float, "band": str, "model": str}.
    """
    last_error: Optional[CaseStudyScoringError] = None
    attempts = 2  # one retry, per the rule: malformed -> retry once -> raise
    for attempt in range(attempts):
        try:
            # The call itself is inside the try: a response that is not even
            # parseable JSON (a plain ValueError out of drafting._parse_json,
            # raised before this ever reaches CaseStudyScoringError territory)
            # is exactly as "malformed" as a well-formed JSON object with the
            # wrong shape, and must be retried the same way.
            parsed, model_name = _call_model(
                corpus=corpus, benchmark_body=benchmark_body,
                candidate_name=candidate_name, role=role,
            )
            if not isinstance(parsed, dict):
                raise CaseStudyScoringError(
                    f"model response was not a JSON object, got {type(parsed).__name__}"
                )
            scores = parsed.get("scores")
            if not isinstance(scores, dict):
                raise CaseStudyScoringError("model response has no 'scores' object")
            validate_scores(scores)  # the shape/range check on the scores themselves

            evidence = parsed.get("evidence")
            if not isinstance(evidence, dict):
                raise CaseStudyScoringError("model response has no 'evidence' object")
            _validate_evidence(evidence)  # Rule 1: no blank citation, ever

            flags = _validate_flags(parsed.get("flags"))
        except CaseStudyScoringError as exc:
            last_error = exc
            log.warning(
                "score_submission: malformed model response for %r "
                "(attempt %d/%d): %s", candidate_name, attempt + 1, attempts, exc,
            )
            continue
        except ValueError as exc:
            # CaseStudyScoringError IS a ValueError, but that branch is caught
            # above, so anything landing here is a DIFFERENT ValueError: most
            # commonly drafting._parse_json's "LLM did not return parseable
            # JSON" when the model's text is not JSON at all. Wrap it so the
            # caller only ever has one exception type to handle, and keep the
            # original exception visible via __cause__ for debugging.
            wrapped = CaseStudyScoringError(
                f"model response was not parseable JSON: {exc}"
            )
            wrapped.__cause__ = exc
            last_error = wrapped
            log.warning(
                "score_submission: model call/parse failed for %r "
                "(attempt %d/%d): %s", candidate_name, attempt + 1, attempts, exc,
            )
            continue

        total = weighted_total(scores)
        computed_band = band(total, flags)
        return {
            "scores": scores,
            "evidence": evidence,
            "flags": flags,
            "total": total,
            "band": computed_band,
            "model": model_name,
        }

    # Both attempts were malformed. Never silently repair; raise the last
    # validation error so the caller sees exactly what was wrong.
    raise last_error
