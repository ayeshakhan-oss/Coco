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
- VOICE: write ONLY in the first-person PLURAL, collective voice — "we", "our",
  "us". This message is from Taleemabad as a team, never one individual. NEVER
  use first-person singular anywhere: no "I", "I'm", "I've", "I'll", "I'd",
  "my", "me", "mine", "myself". (e.g. write "we reviewed", "we want to be
  honest", "we noticed" — never "I reviewed", "I want to share", "I know".)
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


_CV_STAGE_NOTE = """
========================================================================
CV / APPLICATION-STAGE REJECTION — NO INTERACTION EVER HAPPENED
========================================================================
This candidate was screened out at the CV / application stage. There was NO
interview, NO phone/video call, NO conversation, NO meeting, and NO assessment
with them. You have ONLY their written application / CV.
- NEVER reference or imply any interview, conversation, call, meeting, or
  discussion WITH the candidate, and never "across conversations and
  assessments", "our conversation", "when we spoke/met", "our time together",
  or "what we observed [in you]". None of that happened — writing it is a
  fabrication and will be rejected.
- Ground EVERYTHING only in what a written application can show: "your
  application", "your CV", "the experience you described", "your materials".
- "What we appreciated" = specific genuine strengths visible in the written
  application. "Where we found questions" = specific gaps/uncertainties in the
  application relative to the role. Honest and concrete, never invented.
- You MAY refer to the interview stage they did not reach (e.g. "we've decided
  not to move forward to the interview stage") — that is about a stage, not a
  conversation that occurred.
========================================================================
"""


@lru_cache
def system_prompt(email_type: str) -> str:
    required = SECTION_HEADINGS.get(email_type, {}).get("required", [])
    headings = "\n".join(f"    {i + 1}. {h}" for i, h in enumerate(required))
    contract = _OUTPUT_CONTRACT.replace("{headings}", headings or "    (none)")
    prompt = _tone_master() + "\n\n" + contract
    if email_type == "cv_rejection":
        prompt += "\n" + _CV_STAGE_NOTE
    return prompt
