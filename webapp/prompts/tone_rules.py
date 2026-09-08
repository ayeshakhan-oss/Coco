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
- NO harsh, judgmental or adversarial language. FORBIDDEN: "failure", "wrong",
  "the honest part", "you failed", "the problem with your", "went wrong",
  "you cannot", "incapable", "deliberately", "selecting assumptions". The letter
  exists to be USEFUL to the candidate, never to justify or defend the decision.
  PREFER: "the main gap we identified", "where the analysis could have been
  stronger", "one area that affected the conclusions", "what we would encourage
  you to look at differently".
- NO corporate rejection boilerplate: "we regret to inform", "after careful
  consideration", "impressive candidate pool", "strong field of candidates".
- Describe the WORK and its effect on the conclusion, never the candidate's
  ability, judgment or motive. "The analysis appears to have been built using X"
  beats "the analysis rests on X". Give credit where the reasoning held together.
- NEVER infer intent or internal state. Forbidden phrasings include
  "you seemed", "you lacked", "you assumed", "you believed", "you preferred",
  "you were energized", "you would likely", "you appeared". State what was
  observed or what is uncertain, never what the candidate felt or intended.
- NO internal jargon: do not write "GWC", "KCD", "warm bench", or "values
  scorecard". ("case study" is allowed ONLY for the case_study_outcome type,
  where it is the candidate's own deliverable.)
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


_CASE_STUDY_OUTCOME_NOTE = """
========================================================================
CASE STUDY OUTCOME — SUBMITTED, BELOW THE 70% BENCHMARK
========================================================================
This candidate reached the case-study stage, SUBMITTED their work, and scored
below the 70% benchmark that gates the final interviews. It is a decision email.

EVIDENCE — exactly two sources, nothing else:
  1. the candidate's OWN submission (their figures, their sentences, their files)
  2. the benchmark answer key, written and QA'd BEFORE any submission was opened
Never a panel opinion, never an inference about why they did something.

THE RULE IS STATED, THE SCORE IS NOT:
- Say that we set a 70% benchmark and that candidates who meet it move to the
  final interviews, so the outcome reads as one threshold applied evenly.
- Phrase the decision as: their submission "did not meet the 70% benchmark on
  this occasion". The words "on this occasion" matter: this is not permanent.
- NEVER print their score, band or ranking. No "62/100", no "borderline", no
  placing, and no comparison with anybody else's submission.

QUOTING:
- Anything inside quotation marks MUST be the candidate's exact words. Do not
  tidy, reorder or correct a typo inside a quote. If their wording cannot be
  reproduced exactly, paraphrase it WITHOUT quotation marks instead.

NO CONVERSATION:
- Ground everything in the written submission. Do not reference an interview,
  call, conversation or meeting unless one is verified. A booked call is not a
  held interview.

The word "case study" IS permitted here. It is the candidate's own deliverable
and we invited them to produce it.
========================================================================
"""


@lru_cache
def system_prompt(email_type: str) -> str:
    required = SECTION_HEADINGS.get(email_type, {}).get("required", [])
    # a heading slot may be a list of accepted alternatives; instruct the first,
    # which is the canonical wording for a fresh draft.
    canonical = [h[0] if isinstance(h, (list, tuple)) else h for h in required]
    headings = "\n".join(f"    {i + 1}. {h}" for i, h in enumerate(canonical))
    contract = _OUTPUT_CONTRACT.replace("{headings}", headings or "    (none)")
    prompt = _tone_master() + "\n\n" + contract
    if email_type == "cv_rejection":
        prompt += "\n" + _CV_STAGE_NOTE
    if email_type == "case_study_outcome":
        prompt += "\n" + _CASE_STUDY_OUTCOME_NOTE
    return prompt
