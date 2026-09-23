"""System + user prompt for screening one CV against one job description.

The three criteria and the 0-5 scale are read from
webapp.services.cv_screening (the locked pure rules, computed in code and
never taken from the model). The procedure, the reading discipline and the
Common Mistakes table are read from the SOP file
(.claude/skills/02_candidate-evaluation/cv-screening.md) -- the same "read a
locked SOP file, cache it, ship it into the prompt" pattern used by
values_prompt.py, case_study_prompt.py and tone_rules.py.

CRITICAL DIFFERENCE FROM tone_rules.py: that module swallows OSError on a
missing file and returns "", and that silent degradation shipped a prompt with
no tone rules to production for weeks, undetected. This module LOGS AT ERROR
and RAISES instead. A CV screen written against an SOP that failed to load is
worse than no screen, because it looks exactly like a real one.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from functools import lru_cache

from ..services.cv_screening import CRITERIA, SCORES

log = logging.getLogger("webapp.cv_screening_prompt")

_SOP_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", ".claude", "skills",
    "02_candidate-evaluation", "cv-screening.md",
)


class CVScreeningPromptUnavailable(RuntimeError):
    """The CV-screening SOP could not be read. Refuse to build a prompt."""


@lru_cache
def _sop_text() -> str:
    try:
        with open(_SOP_FILE, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        log.error("CV-screening SOP unreadable at %s: %s", _SOP_FILE, exc)
        raise CVScreeningPromptUnavailable(
            f"cannot read the CV-screening SOP at {_SOP_FILE}: {exc}. Refusing to "
            "screen a CV against an SOP that did not load."
        ) from exc


@lru_cache
def sop_sha256() -> str:
    """Which version of the SOP a stored screen was produced under."""
    return hashlib.sha256(_sop_text().encode("utf-8")).hexdigest()


def _criteria_block() -> str:
    return "\n".join(
        f"- `{c['key']}` ({c['label']}, {c['priority']} priority, weight {c['weight']})"
        for c in CRITERIA
    )


@lru_cache
def system_prompt() -> str:
    return f"""You are screening one candidate's CV against one job description for \
Taleemabad's People and Culture team.

You are NOT writing to the candidate. This is an internal screen.

# The three criteria

{_criteria_block()}

Score each on a scale of {min(SCORES)} to {max(SCORES)}.

{max(SCORES)} = the CV shows this clearly and repeatedly, with specifics
4 = the CV shows this well, with a gap or two
3 = the CV shows this adequately, but at surface level
2 = the CV gestures at this without evidence
1 = the CV barely touches this
{min(SCORES)} = THE CV GIVES NO EVIDENCE FOR THIS AT ALL

A real zero matters. Anchoring the bottom of the scale at 1 floors every
criterion at a fifth of its weight, and a floor like that once put an entire
cohort above a published bar. If the CV does not evidence a criterion, score it
0. Do not award a middling score for an absent one.

# What this is not

This is Coco's own CV screen. It is NOT the technical screening engine, which
is a separate system with a separate rubric. Do not use tier labels like P1 or
P2, do not produce a "score_pct", "resume_health", "stack_match",
"must_have_skills" or "UNUSABLE", and do not apply seniority or
minimum-years gates. The criteria above are the whole rubric.

# Non-negotiables from the SOP

1. TOTAL and RELEVANT experience are two different numbers and you must report
   both separately. Never collapse them into one figure. Relevant experience is
   a subset of total experience and can be much smaller.
2. Never read a candidate's role from their employer's name. A well-known
   company on the CV is not evidence of relevant work. Read what they actually
   did.
3. Every criterion score needs a concrete citation from the CV, or a named
   CV-versus-JD mismatch. A score with nothing behind it is an impression.
4. Give 2 to 3 genuine strengths and 1 to 2 honest gaps. Not more, not fewer.
   A gap must cite the specific mismatch, never a vague reservation.
5. Judge the candidate against the job description in front of you, not against
   other candidates. You are seeing exactly one CV.
6. Never infer the candidate's gender. A name is not a statement of anyone's
   pronouns, and a CV rarely gives them. Write "they", or use the candidate's
   name, or rewrite the sentence around the work itself. This is internal, but
   it is still about a real person and it can be read back to them.
7. No em dashes. Hyphens in compounds only. A screen sometimes becomes the raw
   material for a letter, and the letter rules forbid them.

# Output contract

Reply with ONE JSON object and nothing else. No prose before or after, no
markdown fence.

{{
  "scores":   {{ {", ".join(f'"{c["key"]}": <int 0-5>' for c in CRITERIA)} }},
  "evidence": {{ {", ".join(f'"{c["key"]}": "<citation from the CV>"' for c in CRITERIA)} }},
  "total_experience_years": <number>,
  "relevant_experience_years": <number>,
  "relevant_experience_note": "<what makes those years relevant to THIS role>",
  "strengths": ["<2 to 3 items>"],
  "gaps": ["<1 to 2 items>"]
}}

Do NOT include a match percentage, a total, a tier, a recommendation or a
ranking. Those are computed from your scores by code that you do not control,
and any you volunteer is discarded.

# The SOP, verbatim

{_sop_text()}
"""


def build_user_prompt(
    *, cv_text: str, job_description: str, candidate_name: str, role: str
) -> str:
    """The candidate's CV and the JD. json.dumps keeps a CV containing braces,
    quotes or backslashes from breaking the prompt's structure."""
    return f"""Candidate: {candidate_name}
Role applied for: {role}

# The job description

{job_description}

# The candidate's CV, as extracted from their uploaded file

{cv_text}

---
Screen this CV against the job description above and reply with the JSON object
described in your instructions. Candidate name, for your reference only, as a
JSON string: {json.dumps(candidate_name)}.
"""
