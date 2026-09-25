"""Drafting a screening rubric from a job description.

A rubric decides how every candidate for a role is judged, so this prompt is
built the same way `cv_screening_prompt` is: the procedure and the protective
wording are read from the locked SOP file at runtime and shipped verbatim into
the prompt, and a missing SOP RAISES rather than degrading.

🔴 WHY THE SOP MUST BE IN THE PROMPT. Without it the model invents a rubric
that looks right and quietly drops the parts that protect candidates: that an
absent skill scores 0 rather than a middling guess, that silence in a CV is
never a refusal, that university tier can never fail anyone, and that the
subject is a document rather than a person. Those sentences are the difference
between a rubric that is structurally valid and one that is safe to score
hundreds of people with.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from functools import lru_cache

log = logging.getLogger("webapp.rubric_drafting_prompt")

_SOP_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", ".claude", "skills",
    "02_candidate-evaluation", "technical-screening.md",
)


class RubricPromptUnavailable(RuntimeError):
    """The technical-screening SOP could not be read. Refuse to draft."""


@lru_cache
def _sop_text() -> str:
    try:
        with open(_SOP_FILE, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        log.error("technical-screening SOP unreadable at %s: %s", _SOP_FILE, exc)
        raise RubricPromptUnavailable(
            f"cannot read the technical-screening SOP at {_SOP_FILE}: {exc}. "
            "Refusing to draft a rubric without the rules that protect "
            "candidates from it."
        ) from exc


@lru_cache
def sop_sha256() -> str:
    return hashlib.sha256(_sop_text().encode("utf-8")).hexdigest()


@lru_cache
def system_prompt() -> str:
    return f"""You are drafting a SCREENING RUBRIC for one role at Taleemabad, \
an education non-profit in Pakistan.

You are not screening anyone. You are writing the instrument that will be used
to screen every applicant to this role, so a person will read your draft and
approve it before it scores anybody.

# What you produce

Five dimensions. Each is scored 0 to 5 and carries a weight. The weights set
what this role actually needs, so they are not all equal: on comparable roles
the must-have skills carry roughly half the total weight and the softest
dimension carries a fraction of it.

# The rules that matter most

1. THE BOTTOM OF THE SCALE IS REAL. The 0 anchor must describe ABSENCE, in
   plain words, for every dimension. Never write a 0 anchor that describes a
   weak-but-present skill. Anchoring the bottom at 1 floors every dimension at
   a fifth of its weight, and a floor like that once put an entire cohort of 25
   candidates above a published bar.
2. ANCHORS DESCRIBE EVIDENCE, NOT QUALITY WORDS. "Has most of the named stack
   hands-on, one component missing" is an anchor. "Good" is not.
3. HARD FILTERS ARE PROTECTIVE. Each carries a `rule` written so that silence
   in a CV produces `unknown`, never `fail`. Say so inside the rule text
   itself. A filter about where someone lives must fail only where the
   candidate says they cannot or will not work there. A filter about education
   or university must use action "flag" and never "reject".
4. YOU ARE DESCRIBING A DOCUMENT, NOT RANKING A PERSON. No anchor, rule or
   label may reference or imply gender, age, ethnicity, religion, marital
   status, nationality, or a candidate's name or photograph.
5. NO EM DASHES anywhere in what you write. Hyphens in compounds only.

# Output contract

Reply with ONE JSON object and nothing else. No prose before or after, no
markdown fence.

{{
  "title": "<the role title>",
  "seniority": "junior" | "mid" | "senior" | "lead" | "exec",
  "min_years": <number, the relevant-experience floor this JD implies>,
  "dimensions": [
    {{
      "key": "<lower_snake_case>",
      "label": "<short human label>",
      "weight": <integer 1-10>,
      "core": <true for the dimensions this role cannot do without>,
      "max": 5,
      "anchors": {{
        "0": "<absence, stated plainly>",
        "1": "...", "2": "...", "3": "...", "4": "...",
        "5": "<the strongest realistic evidence>"
      }},
      "look_for": ["<3 to 4 concrete evidence cues>"],
      "common_gaps": ["<3 failure patterns a screener should recognise>"]
    }}
  ],
  "hard_filters": [
    {{
      "key": "<lower_snake_case>",
      "label": "<short label>",
      "rule": "<how to judge it, including what counts as unknown>",
      "action": "reject" | "flag",
      "on_unknown": "flag"
    }}
  ],
  "thresholds": {{
    "p1": 85, "p2": 70, "p3": 50, "basis": "absolute",
    "gates": {{
      "p1": {{"min_dimension": {{"<core key>": 4}}}},
      "p2": {{"min_dimension": {{"<core key>": 2}}}}
    }}
  }}
}}

Exactly five dimensions. The `gates` exist so a strong total cannot hide a
critical weakness, and they must name CORE dimensions only.

# The screening SOP, verbatim

{_sop_text()}
"""


def build_user_prompt(*, job_title: str, department: str | None,
                      location: str | None, job_description: str) -> str:
    return f"""Draft the screening rubric for this role.

ROLE: {job_title}
DEPARTMENT: {department or 'not stated'}
LOCATION: {location or 'not stated'}

--- JOB DESCRIPTION ---
{job_description}
--- END JOB DESCRIPTION ---

Reply with the JSON object described in your instructions. Role title as a
JSON string, for your reference: {json.dumps(job_title)}.
"""
