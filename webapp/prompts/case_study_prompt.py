"""System + user prompt for scoring a candidate's case-study submission
against a QA'd benchmark answer key.

The six dimensions, the 0-5 scale and the flag vocabulary are read from
webapp.services.case_study_scoring (the locked pure rules, computed in code
and never taken from the model); the anchors and Rules 0-3 are read from the
rubric SOP file
(.claude/skills/02_candidate-evaluation/case-study-scoring-rubric.md), the
same "read a locked SOP file, cache it, ship it into the prompt" pattern
webapp/prompts/values_prompt.py and webapp/prompts/tone_rules.py use.

CRITICAL DIFFERENCE FROM tone_rules.py: that module swallows OSError on a
missing/unreadable file and returns "", and that silent degradation shipped a
prompt with no tone rules to production for weeks, undetected (see
memory/webapp_evidence_routing_per_email_type_2026_09_14.md and neighbouring
lessons). This module does the opposite on purpose: it LOGS AT ERROR when the
rubric file is missing or unreadable, and system_prompt() RAISES rather than
silently building a scoring prompt with no anchors in it. A case-study score
written against an undefined rubric is worse than no score.
"""

from __future__ import annotations

import hashlib
import logging
import os
from functools import lru_cache

from ..services.case_study_scoring import DIMENSIONS, FLAGS, SCORES

log = logging.getLogger("webapp.case_study_prompt")

_RUBRIC_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    ".claude",
    "skills",
    "02_candidate-evaluation",
    "case-study-scoring-rubric.md",
)


class CaseStudyPromptUnavailable(RuntimeError):
    """The case-study scoring rubric could not be read. Refuse to build a prompt."""


@lru_cache
def _rubric_text() -> str:
    """The case-study scoring rubric SOP, verbatim. Raises rather than degrading silently."""
    try:
        with open(_RUBRIC_FILE, encoding="utf-8") as f:
            text = f.read().strip()
    except OSError as exc:
        log.error("Cannot read the case-study scoring rubric at %s: %s", _RUBRIC_FILE, exc)
        raise CaseStudyPromptUnavailable(
            f"The case-study scoring rubric is missing or unreadable ({_RUBRIC_FILE}). "
            "Refusing to build a case-study scoring prompt with no anchors in it."
        ) from exc
    if not text:
        log.error("The case-study scoring rubric at %s is empty.", _RUBRIC_FILE)
        raise CaseStudyPromptUnavailable(
            f"The case-study scoring rubric at {_RUBRIC_FILE} is empty. Refusing to "
            "build a case-study scoring prompt with no anchors in it."
        )
    return text


_SYSTEM_TEMPLATE = """You are scoring a candidate's case-study submission for a
Taleemabad growth role against a QA'd benchmark answer key, using ONLY what
actually appears in the submission and the benchmark you are given. Never
invent, assume, or fill in from the candidate's CV, reputation, or any other
round.

========================================================================
THE RUBRIC FOR THIS SCORING TASK, VERBATIM
========================================================================
{rubric}
========================================================================

========================================================================
THREE RULES THAT ARE EASY TO GET WRONG. FOLLOW THEM EXACTLY.
========================================================================
RULE 1 -- EVERY SCORE CITES EVIDENCE.
A dimension score with no quoted line, slide number or figure behind it is
not a score, it is an impression. Every "evidence" field in your response
must name the specific place in the submission the score comes from: quote
the line, name the slide or section, or cite the figure. Never leave one
blank, and never write a generic sentence with nothing pinned to the
submission.

RULE 2 -- THREE DISTINCT NUMBER PROBLEMS. DO NOT COLLAPSE THEM.
When a candidate's figure disagrees with the benchmark's ground truth, decide
which of these three it is, because they are not the same thing:
  - WRONG -- the figure is contradicted by the data. Serious; explain what
    the data actually shows.
  - DEFINITIONAL -- a different but defensible denominator or scope (for
    example, all users versus registered users). Note it in your evidence.
    Do NOT penalise it.
  - FABRICATED -- a figure that does not exist in the dataset and cannot be
    derived from it. This is disqualifying: set the "fabricated_data" flag.
Never mark a definitional choice down as if it were wrong, and never call a
figure fabricated just because it disagrees with the benchmark.

RULE 3 -- SCORE REASONING, NOT AGREEMENT.
A candidate who reaches a different conclusion from the benchmark, but backs
it with a real argument grounded in the data, scores exactly as high as a
candidate who reached the benchmark's own conclusion. Never mark a
submission down because it disagrees with us. Score the quality of the
reasoning, not whether it matches the answer key.
========================================================================

========================================================================
THE SIX DIMENSIONS AND THE 0-5 SCALE
========================================================================
Score each dimension on this scale, with a REAL ZERO -- an absent or wholly
wrong answer scores 0, never a middling guess:
{scores}

Dimensions, in this exact order:
{dimension_list}

Flags available (attach a flag only when its condition is actually met; most
submissions carry none):
{flag_list}
========================================================================

========================================================================
OUTPUT CONTRACT (STRICT)
========================================================================
Return ONLY valid JSON (no markdown fences, no prose before or after it) with
EXACTLY this shape:

{{
  "scores": {{
{score_key_lines}
  }},
  "evidence": {{
{evidence_key_lines}
  }},
  "flags": ["<zero or more of: {flag_keys}>"]
}}

RULES YOU MUST FOLLOW:
- DO NOT compute or include a total, a weighted score, or a band
  ("strong_yes"/"yes"/"borderline"/"no"/"disqualified") anywhere in your
  response. The total and the band are computed in code from your six
  scores and your flags, and are never taken from you: if you include one it
  will simply be ignored.
- "scores" must have EXACTLY these six keys, each an integer from {scores},
  never a float, never a string, never omitted.
- "evidence" must have EXACTLY these six keys, each a non-empty string
  citing a quoted line, a slide or section, or a figure from the submission
  (Rule 1 above). A blank or whitespace-only evidence string is rejected.
- "flags" is a list containing zero or more of: {flag_keys}. Omit a flag
  unless its condition is actually met. Never invent a flag to be cautious.
========================================================================
"""


def rubric_sha256() -> str:
    """SHA-256 (hex) of the rubric text actually embedded in `system_prompt()`.

    The rubric file is mutable and unversioned, so two scoring runs on
    either side of an anchor edit are otherwise indistinguishable once
    persisted -- this is what makes "which rubric text produced this score"
    answerable later, the same audit reasoning
    `ValuesScorecardDraft.transcript_sha256` exists for. Reads the same
    `lru_cache`d text `system_prompt()` embeds, so a call right after
    building a system prompt always reports the text that prompt actually
    carried.
    """
    return hashlib.sha256(_rubric_text().encode("utf-8")).hexdigest()


def system_prompt() -> str:
    """The full system prompt: the rubric, the dimensions, the three
    easy-to-miss rules, and the strict JSON output contract. Raises
    CaseStudyPromptUnavailable if the rubric file cannot be read."""
    dimension_list = "\n".join(
        f"    {i + 1}. {d['key']} ({d['label']}, weight {d['weight']}%)"
        for i, d in enumerate(DIMENSIONS)
    )
    score_key_lines = ",\n".join(f'    "{d["key"]}": <0-5 integer>' for d in DIMENSIONS)
    evidence_key_lines = ",\n".join(
        f'    "{d["key"]}": "<quoted line, slide/section or figure>"' for d in DIMENSIONS
    )
    flag_list = "\n".join(f"    - {name} ({severity})" for name, severity in FLAGS.items())
    return _SYSTEM_TEMPLATE.format(
        rubric=_rubric_text(),
        scores=", ".join(str(s) for s in SCORES),
        dimension_list=dimension_list,
        flag_list=flag_list,
        score_key_lines=score_key_lines,
        evidence_key_lines=evidence_key_lines,
        flag_keys=", ".join(FLAGS.keys()),
    )


def build_user_prompt(*, corpus: str, benchmark_body: str, candidate_name: str, role: str) -> str:
    """The per-candidate call: who this is, the benchmark answer key, and the
    submission corpus to score."""
    return (
        f"Candidate: {candidate_name}\n"
        f"Role: {role}\n\n"
        "Benchmark answer key, QA'd before any submission was read:\n"
        "========================================================================\n"
        f"{benchmark_body}\n"
        "========================================================================\n\n"
        "Candidate's submission, verbatim:\n"
        "========================================================================\n"
        f"{corpus}\n"
        "========================================================================\n\n"
        "Score this submission on the six dimensions above, using only what is "
        "actually in the submission and the benchmark. Remember Rule 3: score "
        "the reasoning, not agreement with the benchmark's own conclusion. "
        "Return ONLY the JSON specified in the system prompt: no total, no "
        "band, no markdown fences, no commentary."
    )
