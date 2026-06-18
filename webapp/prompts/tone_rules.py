"""System prompt for the AI drafter.

The system prompt is the locked tone master file verbatim
(memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md) plus a strict output
contract. The required section headings per email type are imported from the
eval harness (single source of truth) so the prompt and the validator can never
disagree.
"""

from __future__ import annotations

import os
from functools import lru_cache

from ..reuse import SECTION_HEADINGS

_TONE_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "memory",
    "CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md",
)


@lru_cache
def _tone_master() -> str:
    try:
        with open(_TONE_FILE, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return "(tone master file unavailable — apply evidence-based, dignified, non-psychologist feedback)"


_OUTPUT_CONTRACT = """
========================================================================
OUTPUT CONTRACT (STRICT)
========================================================================
You are drafting ONE candidate-communication email. Return ONLY valid JSON
(no markdown fences, no prose around it) with EXACTLY this shape:

{
  "title_line": "short human subject line, NO '[PILOT' prefix",
  "greeting": "Dear <FirstName>,",
  "opening": ["one or two opening paragraphs, plain text"],
  "sections": [
    { "subhead": null, "paragraphs": ["para", "para", ...] }
  ],
  "ps": "the P.S. text WITHOUT the 'P.S.' label"
}

- Provide EXACTLY one object in "sections" for each required heading below,
  IN THE SAME ORDER. Do NOT include the heading text yourself — only the
  paragraphs (and an optional short "subhead"). The system applies the exact
  heading.
- Required headings for this email type (in order):
{headings}

HARD RULES (the email is automatically REJECTED if any is violated):
- At least 800 words total across greeting + opening + all paragraphs + ps.
- The FIRST item in "opening" MUST be exactly: "This is not a yes for now."
  (verbatim, its own paragraph, right after the greeting, for EVERY email type).
- NO future-outreach promise. Do NOT write "we will reach out", "we'll be in
  touch", "we will contact you", "we will keep your name on file", or "expect to
  hear from us". Express welcome as disposition + candidate-initiated instead:
  "if a closer-fit role opens, we would welcome a fresh application from you".
- NO em dashes. Use periods, commas, or colons.
- NEVER infer intent or internal state. Forbidden phrasings include
  "you seemed", "you lacked", "you assumed", "you believed", "you preferred",
  "you were energized", "you would likely", "you appeared". State what was
  observed or what is uncertain, never what the candidate felt or intended.
- NO internal jargon: do not write "GWC", "KCD", "warm bench", "values
  scorecard", or "case study".
- NO interviewer or staff names anywhere in the email.
- Ground every strength and every concern in the scorecard evidence provided.
  No generic recruiting abstractions ("strong candidate", "great fit").
- Use "we"/"us" for the company and "you" for the candidate. Warm, specific,
  dignified. The candidate should feel considered carefully and treated fairly.
========================================================================
"""


@lru_cache
def system_prompt(email_type: str) -> str:
    required = SECTION_HEADINGS.get(email_type, {}).get("required", [])
    headings = "\n".join(f"    {i + 1}. {h}" for i, h in enumerate(required))
    contract = _OUTPUT_CONTRACT.replace("{headings}", headings or "    (none)")
    return _tone_master() + "\n\n" + contract
