"""System + user prompt for scoring a values-interview transcript.

The six canonical values and their definitions are read from the SOP file
(.claude/skills/02_candidate-evaluation/values-scorecard-scoring.md), the same
"read a locked SOP file, cache it, ship it into the prompt" pattern
webapp/prompts/tone_rules.py uses for the tone master.

CRITICAL DIFFERENCE FROM tone_rules.py: that module swallows OSError on a
missing/unreadable file and returns "", and that silent degradation shipped a
prompt with no tone rules to production for weeks, undetected (see
memory/webapp_evidence_routing_per_email_type_2026_09_14.md and neighbouring
lessons). This module does the opposite on purpose: it LOGS AT ERROR when the
SOP file is missing or unreadable, and `system_prompt()` RAISES rather than
silently building a scoring prompt with no value definitions in it. A values
scorecard written against undefined values is worse than no scorecard.
"""

from __future__ import annotations

import logging
import os
from functools import lru_cache

from ..services.values_scoring import NOT_OBSERVED, RATINGS, VALUE_NAMES

log = logging.getLogger("webapp.values_prompt")

_SOP_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    ".claude",
    "skills",
    "02_candidate-evaluation",
    "values-scorecard-scoring.md",
)


class ValuesPromptUnavailable(RuntimeError):
    """The values-scoring SOP could not be read. Refuse to build a prompt."""


@lru_cache
def _sop_text() -> str:
    """The values-scoring SOP, verbatim. Raises rather than degrading silently."""
    try:
        with open(_SOP_FILE, encoding="utf-8") as f:
            text = f.read().strip()
    except OSError as exc:
        log.error("Cannot read the values-scoring SOP at %s: %s", _SOP_FILE, exc)
        raise ValuesPromptUnavailable(
            f"The values-scoring SOP is missing or unreadable ({_SOP_FILE}). "
            "Refusing to build a values-scoring prompt with no value "
            "definitions in it."
        ) from exc
    if not text:
        log.error("The values-scoring SOP at %s is empty.", _SOP_FILE)
        raise ValuesPromptUnavailable(
            f"The values-scoring SOP at {_SOP_FILE} is empty. Refusing to build "
            "a values-scoring prompt with no value definitions in it."
        )
    return text


_SYSTEM_TEMPLATE = """You are scoring a Taleemabad values interview transcript
against Taleemabad's six core values, using ONLY what actually appears in the
transcript you are given. Never invent, assume, or fill in from a candidate's
CV or reputation: score what was said in this interview, and nothing else.

========================================================================
THE SOP FOR THIS SCORING TASK, VERBATIM
========================================================================
{sop}
========================================================================

========================================================================
OUTPUT CONTRACT (STRICT)
========================================================================
Return ONLY valid JSON (no markdown fences, no prose before or after it) with
EXACTLY this shape:

{{
  "values": [
    {{
      "name": "<the canonical value name, exactly as given, in this order>",
      "deepDive": "<evidence quoted or closely paraphrased from the transcript>",
      "curveBall": "<evidence quoted or closely paraphrased from the transcript>",
      "microCase": "<evidence quoted or closely paraphrased from the transcript>",
      "rating": "<one of: {ratings}>"
    }}
    ... exactly six entries, one per value, in this exact order:
{value_list}
  ],
  "gwc": {{"gets_it": "Yes"|"No", "wants_it": "Yes"|"No", "capacity": "Yes"|"No"}}
}}

RULES YOU MUST FOLLOW:
- DO NOT compute or include a verdict, a "PASS"/"OUT" label, a pass/fail
  recommendation, or any tally of ratings anywhere in your response. The
  verdict is computed in code from your six ratings and is never taken from
  you: if you include one it will simply be ignored.
- Provide ALL THREE evidence fields (deepDive, curveBall, microCase) for EVERY
  value. Never leave one blank.
- Evidence MUST be grounded in the transcript you were given: quote it
  directly or paraphrase it closely. Never invent, assume, or infer evidence
  that is not actually in the transcript.
- If a value genuinely was not observed in the transcript, write exactly this
  sentence in that field, character for character: "{not_observed}"
  Do not guess at evidence to avoid using this sentence.
- "rating" must be exactly one of these tokens: {ratings}. No other symbol,
  word, or number.
- Only include the "gwc" (Gets it / Wants it / Capacity) object if you believe
  this candidate would PASS the values round (zero minus ratings and at most
  two plus-minus ratings). If you believe the candidate would be OUT, omit the
  "gwc" key entirely rather than including a placeholder. GWC is never a
  back-door around a failing values scorecard.
- Each gwc field must be exactly "Yes" or "No", never a longer sentence, never
  a maybe.
========================================================================
"""


def system_prompt() -> str:
    """The full system prompt: the SOP, the value definitions, and the strict
    JSON output contract. Raises ValuesPromptUnavailable if the SOP file that
    carries the value definitions cannot be read."""
    value_list = "\n".join(f"    {i + 1}. {name}" for i, name in enumerate(VALUE_NAMES))
    return _SYSTEM_TEMPLATE.format(
        sop=_sop_text(),
        ratings=", ".join(RATINGS),
        value_list=value_list,
        not_observed=NOT_OBSERVED,
    )


def build_user_prompt(*, transcript: str, candidate_name: str, role: str) -> str:
    """The per-candidate call: who this is, and the transcript to score."""
    return (
        f"Candidate: {candidate_name}\n"
        f"Role: {role}\n\n"
        "Interview transcript, verbatim:\n"
        "========================================================================\n"
        f"{transcript}\n"
        "========================================================================\n\n"
        "Score this candidate on the six values above, using only what is "
        "actually in this transcript. Return ONLY the JSON specified in the "
        "system prompt: no verdict, no markdown fences, no commentary."
    )
