"""The locked CV-screening rules (Skill 02, component: cv-screening).

Pure: no model, no database. The criteria, the 0-5 conversion, the tiers and the
refusal conditions live here and are tested directly.

SOURCE OF TRUTH: .claude/skills/02_candidate-evaluation/cv-screening.md and
memory/skill_cv_screening_sop.md -- Coco's own SOP, and ONLY that.

🔒 THIS IS NOT TECHNICAL SCREENING. Nugget's engine (public.nugget_screening_*,
   read-only through services/nugget_reads.py) scores TECHNICAL roles against
   its own rubric: must_have_skills / stack_match / seniority gates, P1-P4
   tiers, score_pct, resume_health, UNUSABLE. None of that vocabulary appears
   here and none of it may be imported here. Ayesha, 2026-09-15: "cv screening
   and technical screening are both separate so you shouldn't mix their
   sops/rubrics/rules." Coco's CV screening has its own three criteria and its
   own shortlist / maybe / no-hire tiers.

🔒 The scale runs 0-5 WITH A REAL ZERO (CLAUDE.md Rule 27). Anchoring at 1 floors
   every criterion at 20% of its weight, which is the defect that put all 25 RM
   case studies above the published bar. A criterion the CV gives no evidence
   for scores 0, not a middling guess.
"""

from __future__ import annotations

import logging
from typing import Optional

log = logging.getLogger("webapp.cv_screening")

# The SOP states the priority order and nothing more:
#   1. Skills      -- "What can they do?"        (TOP priority)
#   2. Experience  -- "Have they done similar?"  (TOP priority)
#   3. Fit         -- "Does this match our needs?" (Supporting)
#
# ⚠️ THE NUMBERS ARE A DERIVATION, NOT A QUOTE. The SOP ranks the three criteria
# but never weights them. 40/40/20 is the smallest reading of "two top, one
# supporting" and is flagged for Ayesha rather than presented as locked. Change
# it here and the match % moves everywhere; nothing else hardcodes a weight.
CRITERIA = (
    {"key": "skills", "label": "Skills", "weight": 40, "priority": "top"},
    {"key": "experience", "label": "Experience", "weight": 40, "priority": "top"},
    {"key": "fit", "label": "Fit", "weight": 20, "priority": "supporting"},
)

SCORES = (0, 1, 2, 3, 4, 5)
_MAX = 5
_KEYS = {c["key"] for c in CRITERIA}

# The SOP names three tiers -- shortlist ("top matches"), maybe ("borderline"),
# no-hire ("screened out") -- without numeric boundaries.
# ⚠️ ALSO A DERIVATION, flagged for Ayesha with the weights above.
TIER_SHORTLIST_MIN = 70.0
TIER_MAYBE_MIN = 50.0

# The SOP's reading floor: "Minimum reading capacity: 14,000-15,000 characters
# per resume" and "Never truncate CVs to <10k characters"
# (memory/feedback_bulk_rejection_cv_truncation.md). A CV shorter than the limit
# is passed whole; a longer one is cut at READ_LIMIT, never below TRUNCATION_FLOOR.
READ_LIMIT = 15_000
TRUNCATION_FLOOR = 10_000


class CVScreeningError(ValueError):
    """The screening result does not match the locked shape."""


def validate_scores(scores: dict) -> None:
    keys = set(scores)
    if keys != _KEYS:
        missing, extra = sorted(_KEYS - keys), sorted(keys - _KEYS)
        raise CVScreeningError(f"missing {missing}, unexpected {extra}")
    for k, v in scores.items():
        # bool is an int subclass; reject it explicitly.
        if isinstance(v, bool) or not isinstance(v, int) or v not in SCORES:
            raise CVScreeningError(f"{k}: score must be an integer in {SCORES}, got {v!r}")


def match_percent(scores: dict) -> float:
    """The report's "Match %". Computed here, never taken from the model."""
    validate_scores(scores)
    return round(sum(scores[c["key"]] / _MAX * c["weight"] for c in CRITERIA), 2)


def tier(match: float) -> str:
    """shortlist / maybe / no_hire. Computed here, never taken from the model."""
    if match >= TIER_SHORTLIST_MIN:
        return "shortlist"
    if match >= TIER_MAYBE_MIN:
        return "maybe"
    return "no_hire"


def cv_for_prompt(cv_text: str) -> tuple[str, bool]:
    """Return (text to send, was_truncated).

    The SOP forbids truncating a CV below 10,000 characters, because a screen
    written from the first few hundred characters is the defect that sent 27 CV
    rejections live written from a name and a role title (CLAUDE.md Rule 29).
    """
    if len(cv_text) <= READ_LIMIT:
        return cv_text, False
    return cv_text[:READ_LIMIT], True


def _validate_evidence(evidence: dict) -> None:
    """Every criterion carries a citation from the CV itself.

    The SOP's own "Common Mistakes" table lists "Vague gaps -- no specific
    evidence" with the fix "cite concrete CV/JD mismatch". A criterion scored
    with nothing quoted behind it is an impression, not a screen.
    """
    keys = set(evidence)
    if keys != _KEYS:
        missing, extra = sorted(_KEYS - keys), sorted(keys - _KEYS)
        raise CVScreeningError(f"evidence: missing {missing}, unexpected {extra}")
    for k, v in evidence.items():
        if not isinstance(v, str) or not v.strip():
            raise CVScreeningError(
                f"{k}: evidence citation is blank. Every criterion needs a "
                "concrete line from the CV or a named CV/JD mismatch behind it."
            )


def _validate_experience(parsed: dict) -> dict:
    """Total and relevant experience are TWO separate numbers, always.

    The SOP says this three times, and its Common Mistakes table names
    "Conflating total & relevant exp" as misrepresenting the candidate. A single
    "5 years" is the exact failure: it reads as five relevant years when it may
    be five total and one relevant.
    """
    out = {}
    for key in ("total_experience_years", "relevant_experience_years"):
        v = parsed.get(key)
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise CVScreeningError(
                f"{key} must be a number -- the SOP requires total AND relevant "
                f"experience stated separately, got {v!r}"
            )
        if v < 0:
            raise CVScreeningError(f"{key} cannot be negative, got {v!r}")
        out[key] = round(float(v), 1)

    if out["relevant_experience_years"] > out["total_experience_years"]:
        raise CVScreeningError(
            f"relevant experience ({out['relevant_experience_years']}y) exceeds total "
            f"({out['total_experience_years']}y); relevant is a SUBSET of total"
        )

    note = parsed.get("relevant_experience_note")
    if not isinstance(note, str) or not note.strip():
        raise CVScreeningError(
            "relevant_experience_note is blank: say what makes the relevant years "
            "relevant. The SOP forbids reading a role from the employer's name."
        )
    out["relevant_experience_note"] = note.strip()
    return out


def _validate_list(parsed: dict, key: str, lo: int, hi: int) -> list[str]:
    """The SOP asks for 2-3 genuine strengths and 1-2 honest gaps per candidate."""
    v = parsed.get(key)
    if not isinstance(v, list):
        raise CVScreeningError(f"'{key}' must be a list, got {type(v).__name__}")
    items = [s.strip() for s in v if isinstance(s, str) and s.strip()]
    if len(items) != len(v):
        raise CVScreeningError(f"'{key}' contains a blank or non-string entry")
    if not lo <= len(items) <= hi:
        raise CVScreeningError(f"'{key}' must have {lo}-{hi} entries, got {len(items)}")
    return items


# --------------------------------------------------------------------------
# Model call: CV + job description -> scored criteria. The rules above never
# leave the model's hands; everything below runs its output back through them
# before anything is trusted.
# --------------------------------------------------------------------------


def _call_model(*, cv_text: str, job_description: str, candidate_name: str, role: str) -> tuple:
    """One model call: CV + JD in, raw parsed JSON out.

    Module-level (not a method) so tests can monkeypatch it directly and never
    make a real Anthropic call. Reuses drafting.get_drafter() rather than
    building a second client, exactly like values_scoring and
    case_study_scoring. Imported locally because cv_screening_prompt reads
    CRITERIA/SCORES from this module.
    """
    from . import drafting
    from ..prompts import cv_screening_prompt

    drafter = drafting.get_drafter()
    if isinstance(drafter, drafting.StubDrafter):
        # StubDrafter.draft() returns an EMAIL-shaped dict, never a screen.
        # Refuse up front rather than burn two attempts on a guaranteed
        # validation failure and surface it as a confusing 422.
        raise drafting.DraftingUnavailable(
            "No Anthropic credential configured: get_drafter() returned the "
            "offline StubDrafter, whose output is an email-shaped placeholder, "
            "never a CV screen. Set ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN."
        )
    text, truncated = cv_for_prompt(cv_text)
    parsed = drafter.draft(
        system=cv_screening_prompt.system_prompt(),
        user=cv_screening_prompt.build_user_prompt(
            cv_text=text, job_description=job_description,
            candidate_name=candidate_name, role=role,
        ),
        email_type="cv_screening",
        first_name=candidate_name,
        role=role,
        prior_violations=None,
        attempt=0,
    )
    model_name = getattr(drafter, "model", None) or getattr(drafter, "name", "unknown")
    return parsed, model_name, cv_screening_prompt.sop_sha256(), truncated


def screen_cv(
    *,
    cv_text: str,
    job_description: str,
    candidate_name: str,
    role: str,
) -> dict:
    """Screen one CV against one job description.

    REFUSES rather than degrades. An empty CV or an empty JD raises before any
    model call: a screen written without the CV is the defect that sent 27 CV
    rejections live from nothing but a first name and a role title (CLAUDE.md
    Rule 29), and a screen with no JD has nothing to screen AGAINST.

    A malformed model response is retried once with a FRESH call (never a
    repair of the old one) and then raises. Nothing is coerced, defaulted or
    filled in.

    `match` and `tier` are ALWAYS computed here from the criterion scores and
    are never read off the model's response, even if it volunteers them.
    """
    if not cv_text or not cv_text.strip():
        raise CVScreeningError(
            "no CV text: refusing to screen. A CV screen must be grounded in the "
            "candidate's actual CV, never in a name and a role title."
        )
    if not job_description or not job_description.strip():
        raise CVScreeningError(
            "no job description: refusing to screen. The SOP's first step is "
            "'Read JD thoroughly'; there is nothing to screen against without it."
        )

    last_error: Optional[CVScreeningError] = None
    attempts = 2
    for attempt in range(attempts):
        try:
            parsed, model_name, sop_hash, truncated = _call_model(
                cv_text=cv_text, job_description=job_description,
                candidate_name=candidate_name, role=role,
            )
            if not isinstance(parsed, dict):
                raise CVScreeningError(
                    f"model response was not a JSON object, got {type(parsed).__name__}"
                )
            scores = parsed.get("scores")
            if not isinstance(scores, dict):
                raise CVScreeningError("model response has no 'scores' object")
            validate_scores(scores)

            evidence = parsed.get("evidence")
            if not isinstance(evidence, dict):
                raise CVScreeningError("model response has no 'evidence' object")
            _validate_evidence(evidence)

            experience = _validate_experience(parsed)
            strengths = _validate_list(parsed, "strengths", 2, 3)
            gaps = _validate_list(parsed, "gaps", 1, 2)
        except CVScreeningError as exc:
            last_error = exc
            log.warning(
                "screen_cv: malformed model response for %r (attempt %d/%d): %s",
                candidate_name, attempt + 1, attempts, exc,
            )
            continue
        except ValueError as exc:
            # CVScreeningError IS a ValueError but is caught above, so anything
            # here is a different one -- most often drafting._parse_json's "did
            # not return parseable JSON". Just as malformed; retried the same way.
            wrapped = CVScreeningError(f"model response was not parseable JSON: {exc}")
            wrapped.__cause__ = exc
            last_error = wrapped
            log.warning(
                "screen_cv: unparseable model response for %r (attempt %d/%d): %s",
                candidate_name, attempt + 1, attempts, exc,
            )
            continue

        match = match_percent(scores)
        return {
            "scores": scores,
            "evidence": evidence,
            "strengths": strengths,
            "gaps": gaps,
            **experience,
            "match": match,
            "tier": tier(match),
            "model": model_name,
            "sop_sha256": sop_hash,
            "cv_chars": len(cv_text),
            "cv_truncated": truncated,
        }

    assert last_error is not None
    raise last_error
