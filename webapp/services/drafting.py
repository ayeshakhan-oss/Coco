"""AI drafting engine.

Flow: build prompt -> LLM returns content-only JSON -> render to v8 HTML ->
evaluate_email() -> if HARD-BLOCKs, feed them back and retry (<=3) -> return the
best draft. The model never auto-sends; a human reviews and approves.

Client selection (auto):
  1. ANTHROPIC_API_KEY set     -> AnthropicDrafter (Console api key).
  2. ANTHROPIC_AUTH_TOKEN set  -> AnthropicDrafter (OAuth bearer token). Works in
                                  production; the token must be supplied by env
                                  var because the container has no ~/.claude.
  3. else, non-production      -> AnthropicDrafter (local Claude Code OAuth token
                                  from ~/.claude/.credentials.json), best-effort.
  4. else, non-production      -> StubDrafter (deterministic, offline).
  5. else (production, none)   -> DraftingUnavailable.

NEVER return StubDrafter in production. Its filler reads like a real letter (it
even fabricates an interview conversation) and it pads by repeating a paragraph
until the 800-word rule is satisfied, so it can PASS the eval and be mistaken for
a genuine draft. In production a credential failure yields an EMPTY scaffold plus
an explicit error instead, so the human is never handed an invented letter.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Optional

from ..config import get_settings
from ..prompts.draft_prompt import MissingEvidence, build_user_prompt
from ..prompts.tone_rules import system_prompt
from ..reuse import SECTION_HEADINGS, evaluate_email
from . import rendering

log = logging.getLogger("webapp.drafting")

MAX_ATTEMPTS = 3


class DraftingUnavailable(RuntimeError):
    """No usable drafting credential, or the live call failed in production.

    Raised instead of quietly substituting StubDrafter, whose output is
    indistinguishable from a real letter to a reader.
    """


def _blank_content(email_type: str, first_name: str) -> dict:
    """An EMPTY scaffold: correct shape, no invented prose.

    Used in production when the model is unreachable. The editor still gets an
    editable row (so a human can write the letter by hand) but nothing is
    fabricated, and the eval fails on word count until real text is supplied.
    """
    required = SECTION_HEADINGS.get(email_type, {}).get("required", [])
    return {
        "title_line": rendering._DEFAULT_TITLE.get(email_type, "A note from us"),
        "greeting": f"Dear {first_name},",
        "opening": [],
        "sections": [{"subhead": None, "paragraphs": []} for _ in required],
        "ps": "",
    }


def _parse_json(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Strip markdown fences if present, then grab the outermost {...}.
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        return json.loads(m.group(0))
    raise ValueError("LLM did not return parseable JSON")


def _fix_instruction(prior_violations: list[dict]) -> str:
    bullets = "\n".join(f"  - {v['rule']}: {v['detail']}" for v in prior_violations)
    return (
        "\n\nYour previous draft was REJECTED for these hard violations. "
        "Revise and return the full JSON again, fixing every one:\n" + bullets
    )


# The mandatory opening line (locked 2026-06-18) — must mirror the eval's
# REQUIRED_OPENING_LINE in scripts/evals/candidate_communication_eval.py.
REQUIRED_OPENING_LINE = "This is not a yes for now."
_REQUIRED_OPENING_NORM = "this is not a yes for now"


def _strip_em_dashes(s):
    """Replace the em dash (U+2014, a HARD_BLOCK) with a comma. Leaves the en
    dash (U+2013) untouched — it legitimately appears in role titles like
    'Deputy Manager – Admin Ops' and is NOT blocked."""
    if not isinstance(s, str):
        return s
    return re.sub(r"\s*—\s*", ", ", s)


def _normalize_content(content: dict) -> dict:
    """Deterministically satisfy the two mechanical HARD_BLOCK rules BEFORE the
    eval, instead of hoping the model fixes them across retries:
      1. the mandatory opening line is the first opening paragraph, and
      2. there are no em dashes anywhere.
    This is why a generated draft should never hand the user these two blocks."""
    # 1. Mandatory opening line — ensure the phrase is present in the opening.
    opening = content.get("opening")
    if isinstance(opening, str):
        opening = [opening]
    elif not isinstance(opening, list):
        opening = []
    opening = [p for p in opening if isinstance(p, str)]

    def _norm(s: str) -> str:
        return re.sub(r"[^a-z ]", "", s.lower()).strip()

    if not any(_REQUIRED_OPENING_NORM in _norm(p) for p in opening):
        opening = [REQUIRED_OPENING_LINE] + opening
    content["opening"] = opening

    # 2. Strip em dashes from every text field (subject/title, greeting, opening,
    #    section sub-heads + paragraphs, P.S.).
    content["title_line"] = _strip_em_dashes(content.get("title_line"))
    content["greeting"] = _strip_em_dashes(content.get("greeting"))
    content["opening"] = [_strip_em_dashes(p) for p in content["opening"]]
    content["ps"] = _strip_em_dashes(content.get("ps"))
    sections = content.get("sections") or []
    for sec in sections:
        if isinstance(sec, dict):
            sec["subhead"] = _strip_em_dashes(sec.get("subhead"))
            sec["paragraphs"] = [
                _strip_em_dashes(p) for p in (sec.get("paragraphs") or []) if isinstance(p, str)
            ]
    content["sections"] = sections
    return content


class StubDrafter:
    """Deterministic, offline drafter. Produces compliant, evidence-shaped filler
    so the full pipeline (render + eval + persistence) can be verified without a key."""

    name = "stub"

    def draft(self, *, system, user, email_type, first_name, role, prior_violations=None, attempt=0) -> dict:
        required = SECTION_HEADINGS.get(email_type, {}).get("required", [])
        para = (
            f"Across the conversation about the {role} work, we returned to the "
            "specifics of what you described rather than to impressions, and we want "
            "this note to reflect that same care. We looked at the examples you walked "
            "us through, the way you framed the trade offs, and the reasoning you "
            "offered when the questions grew harder, and we have tried to set down "
            "what we noticed in plain terms so that it is useful to you well beyond "
            "this one process."
        )
        # Respond to a word-count HARD-BLOCK by expanding on retry, so the
        # self-correction loop is exercised and converges.
        paras_per_section = 2 + attempt
        sections = []
        for _ in required:
            sections.append({"subhead": None, "paragraphs": [para] * paras_per_section})
        return {
            "title_line": rendering._DEFAULT_TITLE.get(email_type, "A note from us"),
            "greeting": f"Dear {first_name},",
            "opening": [
                f"Thank you for the time and thought you gave to the {role} "
                "conversation. We want to be specific about what we saw, because a "
                "general note would not honor the effort you put in.",
                para,
            ],
            "sections": sections,
            "ps": (
                "We kept coming back to one part of the conversation in particular, "
                "and we hope the reflection above is useful to you wherever you go next."
            ),
        }


class AnthropicDrafter:
    name = "anthropic"

    # Models this process has already found unusable, remembered ACROSS
    # requests. get_drafter() builds a fresh drafter per request, so without
    # this every single draft re-probed the rate-limited model and paid the
    # SDK's 429 backoff again before failing over. One generate does up to ten
    # model calls; that is how a request runs long enough for the edge proxy to
    # give up and return 502 with no line in the access log, because uvicorn
    # only logs a request once it completes.
    _unusable: set = set()

    def __init__(self, model: str, api_key: Optional[str] = None, auth_token: Optional[str] = None):
        from anthropic import Anthropic

        self.model = model
        self.degraded_from: Optional[str] = None
        self.mode = "api_key" if api_key else "oauth"
        # Fail over fast. The default (2 retries with backoff, honouring a
        # retry-after that can be a minute) is right for a transient blip and
        # badly wrong for a model whose quota is gone and which we are about to
        # abandon anyway. Our own fallback list is the retry that matters.
        opts = {"max_retries": 1, "timeout": 90.0}
        if api_key:
            self.client = Anthropic(api_key=api_key, **opts)
        else:
            self.client = Anthropic(
                auth_token=auth_token,
                default_headers={"anthropic-beta": "oauth-2025-04-20"},
                **opts,
            )
        # Skip straight past anything this process already knows is dead.
        if model in self._unusable:
            for candidate in self._FALLBACK_MODELS:
                if candidate not in self._unusable:
                    log.info("Model %r already known unusable; starting on %r.",
                             model, candidate)
                    self.degraded_from = model
                    self.model = candidate
                    break

    # Tried in order if the configured model name is not one this account can
    # serve. ANTHROPIC_MODEL is set by hand on Railway, so a typo or a retired
    # id would otherwise turn every draft into an empty scaffold with only a
    # generic "unavailable" note - a confusing failure for the person clicking
    # Generate, and one they cannot diagnose.
    _FALLBACK_MODELS = ("claude-sonnet-4-5", "claude-haiku-4-5-20251001")

    @staticmethod
    def _is_unknown_model(exc: Exception) -> bool:
        msg = str(exc).lower()
        return "model" in msg and any(
            k in msg for k in ("not_found", "not found", "404", "invalid_request")
        )

    @staticmethod
    def _is_rate_limited(exc: Exception) -> bool:
        msg = str(exc).lower()
        return "rate_limit" in msg or "429" in msg or "too many requests" in msg

    @classmethod
    def _should_fall_back(cls, exc: Exception) -> bool:
        """Try the next model, rather than hand back an empty letter.

        A rate limit counts. The drafting credential is a Claude Code
        subscription token whose Sonnet and Opus quota can be exhausted while
        Haiku still answers, which is exactly what happened the night
        ANTHROPIC_MODEL was moved to Sonnet: every model call 429'd and Ayesha
        got a 92-word scaffold with no explanation.

        A weaker letter that says so beats no letter at all. Anything else (an
        outage, a bad request, an auth failure) still surfaces untouched.
        """
        return cls._is_unknown_model(exc) or cls._is_rate_limited(exc)

    def draft(self, *, system, user, email_type, first_name, role, prior_violations=None, attempt=0) -> dict:
        content = user
        if prior_violations:
            content = user + _fix_instruction(prior_violations)

        tried: list[str] = []
        for model in (self.model, *self._FALLBACK_MODELS):
            if model in tried:
                continue
            tried.append(model)
            try:
                msg = self.client.messages.create(
                    model=model,
                    max_tokens=4096,
                    system=system,
                    messages=[{"role": "user", "content": content}],
                )
            except Exception as exc:  # noqa: BLE001
                if self._should_fall_back(exc) and model != self._FALLBACK_MODELS[-1]:
                    log.error("Model %r unusable (%s); falling back.", model, exc)
                    # Remember for every later request in this process, so the
                    # next draft does not pay this probe again.
                    type(self)._unusable.add(model)
                    continue
                raise
            if model != self.model:
                # Say so loudly AND on the draft itself: a silent downgrade is
                # how you end up writing candidate letters on a weaker model
                # without knowing it, which had already happened once when
                # ANTHROPIC_MODEL quietly overrode the Opus default with Haiku.
                log.error("Drafting on FALLBACK model %r; configured %r was unusable.",
                          model, self.model)
                self.degraded_from = self.model
                self.model = model
            text = "".join(b.text for b in msg.content if getattr(b, "type", None) == "text")
            return _parse_json(text)
        raise DraftingUnavailable(f"No servable model among {tried}")


def _load_oauth_token() -> Optional[str]:
    path = os.path.join(os.path.expanduser("~"), ".claude", ".credentials.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return (data.get("claudeAiOauth") or {}).get("accessToken")
    except Exception:
        return None


def get_drafter():
    """Pick a drafter from the available credentials. See the module docstring.

    Raises DraftingUnavailable in production when nothing is configured — never
    falls back to StubDrafter there.
    """
    s = get_settings()

    if s.anthropic_api_key:
        log.info("Drafting via Anthropic Console API key.")
        return AnthropicDrafter(s.anthropic_model, api_key=s.anthropic_api_key)

    # OAuth bearer token from the environment. Unlike the local-file path below
    # this works in production, since the container has no ~/.claude directory.
    if s.anthropic_auth_token:
        log.info("Drafting via ANTHROPIC_AUTH_TOKEN (OAuth bearer).")
        return AnthropicDrafter(s.anthropic_model, auth_token=s.anthropic_auth_token)

    if not s.is_production:
        token = _load_oauth_token()
        if token:
            log.warning(
                "No ANTHROPIC_API_KEY/ANTHROPIC_AUTH_TOKEN; using the local Claude "
                "Code OAuth token for drafting (DEV ONLY)."
            )
            return AnthropicDrafter(s.anthropic_model, auth_token=token)
        log.warning("No Anthropic credential available — using StubDrafter (dev only).")
        return StubDrafter()

    raise DraftingUnavailable(
        "No Anthropic credential configured. Set ANTHROPIC_API_KEY (Console key) "
        "or ANTHROPIC_AUTH_TOKEN (OAuth token) on the service."
    )



_REVIEWER_SYSTEM = """
You are the final reviewer of a candidate rejection letter before a human sees
it. You are not writing a new letter. You are finding and repairing sentences
that break the rules below, and returning the SAME letter with those sentences
rewritten.

Regular-expression checks run before you and catch known phrasings. They cannot
catch a rephrasing, which is why you exist. Judge the MEANING of every sentence,
not its wording.

========================================================================
THE SIX BEHAVIOURS YOU MUST REMOVE
========================================================================
1. COACHING - telling the candidate what to do, build, learn, develop, gain,
   demonstrate next time, or pursue. Includes conditionals ("if you were to...",
   "once you have...", "that would change the picture") and includes naming HOW
   the gap could be closed. A disclaimer such as "that's your choice, not ours
   to prescribe" does NOT make it acceptable.

2. CAREER DIRECTION - telling them which roles, functions, sectors or paths
   suit them. "If a role opens where X matters more than Y, we'd welcome your
   application" is career direction: it tells them where they belong.

3. GRADING AN ANSWER - assessing the quality of what they said. "Your answer
   stayed at the relationship level", "when we pressed for tactics", "when we
   pushed back", "it stayed generic", "the details thinned out".

4. PERSON-LEVEL JUDGEMENT - claims about who they are, what motivates them,
   their readiness, character or future behaviour. "That's who you are",
   "it reveals something important about who you are", "you're coachable",
   "you don't detach from hard things", "genuinely pulled toward", "that's
   rare", "will take you far". Praise counts: describing what stayed with us is
   fine, certifying the person is not.

5. REPLAYING EVIDENCE - narrating a question or scenario we posed and then
   saying what was missing from the answer. THE WORST FORM is a list of
   everything they failed to demonstrate:
     "No specific approach to reading the room. No concrete tactic for building
      leverage. No sense of how you would navigate someone who has power."
   That is an improvement checklist for their next interview. Replace the whole
   passage with ONE synthesised sentence about what we needed and could not
   establish, and STOP there.

6. PRIVATE-NOTE LEAKAGE - the hiring manager's internal wording reaching the
   candidate. "Wants out of a night-shift job" becoming "you're ready to move on
   from a demanding remote role" is leakage even though the words changed.

========================================================================
WHAT THE LETTER MAY SAY
========================================================================
- What genuinely stayed with us, including the candidate's own stories and
  their own quoted words. Keep these. They are what make the letter personal.
- What THIS ROLE requires, and why that matters to Taleemabad.
- What we were not able to establish strongly enough through the process.
- Where our decision landed, and warmth at the close.

Preferred constructions: "For this role we needed...", "We weren't able to
establish...", "We came away wanting to understand...", "What remained unclear
to us was...", "Ultimately this is where our decision landed."

========================================================================
HOW TO REPAIR
========================================================================
- Rewrite the offending SENTENCE. Do not delete the paragraph and do not
  shorten the letter: keep the structure, the headings, the depth and the word
  count. If removing a checklist leaves the paragraph thin, use that space to
  explain why the requirement matters to the role.
- Keep every quotation of the candidate's own words exactly as it is.
- Keep the collective "we" voice. No em dashes. Do not touch the opening line
  "This is not a yes for now."
- Change nothing that does not break a rule.

========================================================================
HOW TO REVIEW: A SWEEP, NOT A SPOT CHECK
========================================================================
The automated checks catch roughly ONE defect in FIVE. Measured on a real
letter: they reported 1 phrase and a careful human read found 5. Do not review
by scanning for the flagged phrases. Go through EVERY sentence.

For each sentence, ask ONE question:

    Does this describe a moment and what it meant to US,
    or does it conclude something ABOUT THEM?

The second is always wrong, including when it is warm, generous or true.

PAY SPECIAL ATTENTION TO THE LAST SECTION AND THE P.S. Every letter that has
ever slipped, slipped there. Write them off last and read them twice.

THESE ALL REACHED A HUMAN REVIEWER. NONE CONTAINS A BANNED WORD:
  "Most people would have let someone else handle it"      compares them to people
  "that's the kind of person who holds space for people"   certifies them
  "you're exactly the kind of person we want to build with" certifies them
  "that's someone who means what they say"                 certifies them
  "you've proven you can learn hard things"                a verdict, though kind
  "tells us you have genuine capacity to develop"          a verdict on ability
  "whether that's growth, strategy, or relationship..."    names their lane
  "we'd be happy to have a conversation with our leadership" a promise to keep
  "that kind of clarity about your own misstep"            grades the moment back

Each was a rewrite of a phrase already on the block list. Expect the next one
to be a rewrite too. Judge the MEANING.

WHAT GOOD LOOKS LIKE (from the approved letter, for the shape only, never the
content): "It stayed with us because the problem was not yours to fix and there
was no credit attached to fixing it." · "What stayed with us was that you
carried something on behalf of people who were not in the room to carry it
themselves." · "This is a statement about what we needed to see for this role,
not about what you are able to do."

Each names a moment, then OUR reading of it, and stops before the verdict.

========================================================================
WHAT TO RETURN: ONLY THE SENTENCES YOU ARE CHANGING
========================================================================
Do NOT return the letter. Return a list of edits.

{"edits": [
   {"find": "<the offending sentence, copied EXACTLY, character for character>",
    "replace": "<your rewrite>",
    "why": "<which of the seven behaviours it broke>"}
]}

RULES FOR "find":
- Copy it EXACTLY from the letter you were given. Same words, same spelling,
  same punctuation, same capitalisation. If it does not match exactly, the edit
  is discarded and the defect ships.
- One sentence, or two if they only make sense together. Never a whole
  paragraph.
- It must appear only ONCE in the letter. If the sentence is repeated, include
  a few surrounding words to make it unique.

RULES FOR "replace":
- Same length or longer. NEVER shorter: a letter must not lose substance to
  gain safety. If cutting a verdict leaves the paragraph thin, use the space to
  say what the role required and why.
- Keep the candidate's quoted words untouched. Keep the collective "we".
  No em dashes.

Return {"edits": []} if the letter genuinely breaks none of the rules. An empty
list is a real answer and is better than inventing a change.
"""


_REVIEWED_TYPES = ("cv_rejection", "values_feedback", "warm_bench", "gwc_rejection",
                   "case_study_outcome")


def _letter_as_text(content: dict) -> str:
    """The letter as plain prose for the reviewer to read.

    Handing it raw JSON made it answer in JSON shape, reproducing all ~1,000
    words to change two sentences. That is a heavy load for a small model and
    every re-emission is a chance to drop or mangle something. It reads prose
    and returns only the sentences it wants changed.
    """
    parts = [content.get("greeting", "")]
    parts += [p for p in (content.get("opening") or []) if p]
    for sec in content.get("sections") or []:
        if not isinstance(sec, dict):
            continue
        if sec.get("subhead"):
            parts.append(sec["subhead"])
        parts += [p for p in (sec.get("paragraphs") or []) if p]
    if content.get("ps"):
        parts.append("P.S. " + content["ps"])
    return "\n\n".join(parts)


def _apply_edits(content: dict, edits: list) -> tuple:
    """Apply find/replace edits to the letter's text fields, deterministically.

    Returns (new_content, applied, skipped). An edit whose "find" does not
    appear EXACTLY once is discarded rather than guessed at: a fuzzy match would
    let the reviewer rewrite a sentence it did not mean to touch, and a silent
    near-miss is worse than a defect we can still see.
    """
    import copy

    out = copy.deepcopy(content)
    applied = skipped = 0

    def _fields():
        """Every editable string, as (get, set) pairs."""
        for i, p in enumerate(out.get("opening") or []):
            if isinstance(p, str):
                yield p, lambda v, i=i: out["opening"].__setitem__(i, v)
        for sec in out.get("sections") or []:
            if not isinstance(sec, dict):
                continue
            for i, p in enumerate(sec.get("paragraphs") or []):
                if isinstance(p, str):
                    yield p, lambda v, s=sec, i=i: s["paragraphs"].__setitem__(i, v)
        if isinstance(out.get("ps"), str):
            yield out["ps"], lambda v: out.__setitem__("ps", v)

    for edit in edits:
        if not isinstance(edit, dict):
            skipped += 1
            continue
        find, repl = edit.get("find"), edit.get("replace")
        if not isinstance(find, str) or not isinstance(repl, str) or not find.strip():
            skipped += 1
            continue
        hits = [(text, setter) for text, setter in _fields() if find in text]
        if len(hits) != 1 or hits[0][0].count(find) != 1:
            # Absent, or ambiguous. Either way we will not guess.
            skipped += 1
            continue
        text, setter = hits[0]
        setter(text.replace(find, repl, 1))
        applied += 1
    return out, applied, skipped


def _review_pass(drafter, content: dict, *, email_type: str, first_name: str,
                 role: str, harness_hits: Optional[str] = None) -> dict:
    """Second model pass: judge the letter by MEANING and repair it.

    The regex harness enforces spellings. It cannot see a rephrasing, so a
    letter can pass every pattern and still coach, grade or judge. Measured on
    one real draft: the harness reported 3 phrases and the letter contained 11
    more violations of the same rules, none of them matchable.

    Returns (content, status). status is "applied", "skipped" or
    "failed: <reason>". A failed review must never lose the draft, but it must
    never be silent either: the caller surfaces the failure as a WARNING so a
    reviewer can see that the semantic pass did not run. Three separate checks
    today silently verified nothing; this one says so.
    """
    if email_type not in _REVIEWED_TYPES:
        return content, "skipped"
    try:
        user = (
            "Review this letter. Return ONLY the edits.\n\n"
            f"Candidate first name: {first_name}\nRole: {role}\n\n"
            + _letter_as_text(content)
        )
        if harness_hits:
            user += (
                "\n\nThe automated checks already flagged these, and there are "
                "likely more they cannot see:\n" + harness_hits
            )
        repaired = drafter.draft(
            system=_REVIEWER_SYSTEM, user=user, email_type=email_type,
            first_name=first_name, role=role, prior_violations=None, attempt=0,
        )
        if isinstance(repaired, dict) and isinstance(repaired.get("edits"), list):
            edited, applied, skipped = _apply_edits(content, repaired["edits"])
            if skipped:
                log.warning("Review pass: %d edit(s) applied, %d discarded "
                            "(the quoted sentence did not match).", applied, skipped)
            if not applied:
                return content, "skipped" if not repaired["edits"] else (
                    "failed: no edit matched the letter text")
            return _normalize_content(edited), "applied"
        # The older contract returned the whole letter. Still honour it.
        if isinstance(repaired, dict) and repaired.get("sections"):
            return _normalize_content(repaired), "applied"
        log.warning("Review pass returned an unusable shape; keeping the draft.")
        return content, "failed: the reviewer returned an unusable shape"
    except Exception as exc:  # noqa: BLE001 - never lose a draft to the reviewer
        log.warning("Review pass failed (%s); keeping the draft.", exc)
        return content, f"failed: {type(exc).__name__}"


_TRANSLATOR_SYSTEM = """You translate a hiring manager's PRIVATE interview note
into neutral decision rationale that is safe to build a candidate letter on.

WHY THIS EXISTS
Hiring managers write these notes fast, for colleagues, in blunt shorthand. They
are not writing to the candidate. The letter we build may be forwarded,
screenshotted or posted publicly. Your job is to carry the SUBSTANCE across and
leave the WORDING behind.

THE HARD RULE
Use completely different words. Never reuse a distinctive phrase, label or image
from the note. If the note says "wants out of a remote night-shift job", you do
NOT write "night shift", "remote role" or "wants out"; you write that we were not
able to understand what was drawing them toward this particular mission. If the
note says "his one government-adjacent example doesn't translate", you do NOT
write "government-adjacent" or "translate"; you write that we needed direct
experience inside education and government systems and could not establish
enough of it.

WHAT TO KEEP
- What the role required and where the evidence fell short, stated as OUR
  limitation: "we needed X", "we were not able to establish Y".
- What was genuinely strong, in warm plain terms.

WHAT TO DROP ENTIRELY
- Pass/fail verdicts, scores, symbols, counts (PASS, 5(+), 1(+/-), marks).
- Internal vocabulary: GWC, Get It / Want It / Capacity, warm bench, right seat,
  values scorecard, KCD, probe, role-play, curve ball, micro-case.
- Judgements of the person: motivation, character, readiness, coachability.
- Anything about their current employer or personal circumstances.
- Any moment that serves nothing the candidate can use ("misread my question",
  "struggled to track the conversation", "bad connection").
- Colleague-to-colleague instructions ("probe at debrief", "confirm on travel").

Write 3 to 6 plain sentences. Collective "we". No em dashes. No headings.

Return ONLY valid JSON: {"rationale": "..."}
"""


def _leaks_from(candidate_text: str, raw_note: str) -> bool:
    """True when candidate_text still shares a 4-content-word run with the note.
    The same measure the send gate uses, so the translation is verified against
    the rule it exists to satisfy."""
    from scripts.evals.candidate_communication_eval import _content_words, _LEAK_NGRAM

    a, b = _content_words(candidate_text), _content_words(raw_note)
    if len(a) < _LEAK_NGRAM or len(b) < _LEAK_NGRAM:
        return False
    grams = {" ".join(b[i:i + _LEAK_NGRAM]) for i in range(len(b) - _LEAK_NGRAM + 1)}
    return any(" ".join(a[i:i + _LEAK_NGRAM]) in grams
               for i in range(len(a) - _LEAK_NGRAM + 1))


# A note translates to the same rationale every time, and Ayesha regenerates a
# draft several times while iterating. Cache per (note, role) so a regeneration
# costs no extra model call: the drafting credential is rate limited, and every
# 429 means a dropped note and a thinner letter.
_NOTE_CACHE: dict[tuple[str, str], str] = {}


def _translate_note(drafter, raw: str, *, role: str) -> Optional[str]:
    """One manager note -> neutral rationale, verified not to echo the original.

    Returns None if the model is unreachable or will not stop echoing, and the
    caller then keeps the raw note (today's behaviour) rather than losing the
    decision rationale altogether.
    """
    if not raw or not raw.strip():
        return None
    key = (raw.strip(), role)
    if key in _NOTE_CACHE:
        return _NOTE_CACHE[key]
    for attempt in range(2):
        try:
            user = (
                f"Role: {role}\n\n"
                f"The hiring manager's private note:\n{raw}"
            )
            if attempt:
                user += (
                    "\n\nYour previous attempt reused wording from the note. "
                    "Rewrite it again using entirely different words."
                )
            out = drafter.draft(
                system=_TRANSLATOR_SYSTEM, user=user, email_type="translation",
                first_name="", role=role, prior_violations=None, attempt=attempt,
            )
            text = (out or {}).get("rationale", "").strip()
            if not text:
                continue
            if _leaks_from(text, raw):
                log.warning("Note translation still echoed the note (attempt %d).", attempt + 1)
                continue
            _NOTE_CACHE[key] = text
            return text
        except Exception as exc:  # noqa: BLE001 - never lose a draft to this
            log.warning("Note translation failed (%s).", exc)
            return None
    return None


_MANAGER_NOTE_FIELDS = ("final_comments", "additional_comments")


def _soften_manager_notes(drafter, scorecard: Optional[dict], *, role: str) -> Optional[dict]:
    """Replace the hiring manager's raw editorial with a translated version
    BEFORE the drafter ever sees it.

    This is the structural fix for a loop that could not converge. The drafter
    was handed the manager's blunt note verbatim as its evidence and then
    forbidden by the send gate from reusing any four consecutive content words
    of it. Each retry produced a WHOLE NEW LETTER that avoided the one phrase it
    had been told about and echoed somewhere else instead: three attempts,
    three different leaks, three hard blocks in front of a human
    ("one government-adjacent example", then "remote night shift job").

    A model cannot reliably avoid echoing a text it is reading. So it no longer
    reads it. The per-value deep dive / curve ball / micro-case notes are left
    UNTOUCHED: those record the candidate's own stories and quoted words, which
    are what make the letter personal, and the leakage gate never covered them.

    Returns (scorecard, warnings). If a note cannot be translated the field is
    DROPPED, never passed through raw: falling back to the raw note would
    reinstate exactly the failure this function exists to remove, and a letter
    that is slightly less specific beats a letter that quotes the hiring
    manager at the candidate. The drop is reported so nobody mistakes a thinner
    letter for the model's own judgement.
    """
    warnings: list[str] = []
    if not scorecard:
        return scorecard, warnings
    out = dict(scorecard)
    if out.get("kind") == "values_and_gwc":
        out["values"], w1 = _soften_manager_notes(drafter, out.get("values"), role=role)
        out["gwc"], w2 = _soften_manager_notes(drafter, out.get("gwc"), role=role)
        return out, w1 + w2
    for field in _MANAGER_NOTE_FIELDS:
        raw = out.get(field)
        if isinstance(raw, str) and raw.strip():
            translated = _translate_note(drafter, raw, role=role)
            if translated:
                out[field] = translated
            else:
                out.pop(field, None)
                log.warning("Dropped the raw manager note (%s); translation unavailable.", field)
                warnings.append(field)
    return out, warnings


def _corpus_from_evidence(ev: Optional[dict]) -> Optional[str]:
    """The candidate's own words, for the CV-grounding gate. None when there is
    no CV evidence (non-CV types), which stands the gate down."""
    if not ev:
        return None
    parts = [ev.get("cv_text") or "", ev.get("cover_letter") or ""]
    for key in ("custom_answers", "canned_answers"):
        value = ev.get(key)
        if value:
            parts.append(value if isinstance(value, str) else json.dumps(value))
    corpus = "\n".join(p for p in parts if p).strip()
    return corpus or None


def generate_draft(*, scorecard: Optional[dict], first_name: str, role: str, app_id,
                   email_type: str, cv_evidence: Optional[dict] = None,
                   scorecard_text: Optional[str] = None) -> dict:
    """Generate + self-correct a draft. Returns a dict with the rendered body,
    title, full HTML, eval result, attempts, and which drafter was used.

    Raises MissingEvidence (propagated from build_user_prompt) when this email
    type has no evidence to stand on. The caller must surface that, never draft.

    `scorecard_text` is the hiring manager's own free-text notes. It is passed
    here ONLY so the scorecard-leakage gate runs at DRAFT time, where the retry
    loop and the review pass can still repair the sentence. Without it the check
    stands down silently, the stored eval reads "passed", and the letter blocks
    at SEND instead — which is how "his one government-adjacent example doesn't
    translate" reached a finished warm-bench draft (comm-b0e84207, app 3869).
    EVERY gate must be handed the SAME inputs; see _first_name_for() in the
    router for the same lesson learned on a different argument.
    """
    drafter = get_drafter()

    # Translate the hiring manager's blunt internal note BEFORE the drafter sees
    # it. Handing over the raw note and then forbidding any four-word echo of it
    # is an instruction that cannot converge: each retry wrote a fresh letter
    # that dodged the one flagged phrase and echoed a different one.
    scorecard, untranslated = _soften_manager_notes(drafter, scorecard, role=role)

    system = system_prompt(email_type)
    user = build_user_prompt(scorecard=scorecard, first_name=first_name, role=role,
                             email_type=email_type, cv_evidence=cv_evidence)

    prior: Optional[list[dict]] = None
    best = None

    for attempt in range(MAX_ATTEMPTS):
        try:
            content = drafter.draft(
                system=system, user=user, email_type=email_type,
                first_name=first_name, role=role, prior_violations=prior, attempt=attempt,
            )
        except Exception as exc:
            # NEVER substitute invented prose for a failed call, in ANY
            # environment. The stub's filler reads like a real letter ("Across
            # the conversation about the ... work, we returned to the specifics
            # of what you described") and can pass the eval for every type that
            # has no grounding check. This used to be gated on is_production,
            # which reads app_env and DEFAULTS TO "development" — so a Railway
            # service missing APP_ENV=production would have silently served stub
            # letters. Hand back an empty scaffold instead: visibly empty, still
            # editable by hand, impossible to mistake for a drafted letter.
            log.error("Drafter %s failed (%s); returning an empty scaffold.", drafter.name, exc)
            content = _blank_content(email_type, first_name)
            drafter_name = f"unavailable ({type(exc).__name__})"
        else:
            drafter_name = drafter.name

        # Deterministically satisfy the two mechanical hard-blocks (mandatory
        # opening line + no em dashes) so the user never has to fix them by hand.
        content = _normalize_content(content)

        def _render_and_check(c):
            body = rendering.render_body(
                c, email_type=email_type, candidate_name=first_name, role=role, app_id=app_id
            )
            title = rendering.title_for(c, email_type)
            full = rendering.wrap_full(body, title_line=title, role=role, email_type=email_type)
            return body, title, full, evaluate_email(
                full, title, email_type, pilot_mode=True,
                cv_corpus=_corpus_from_evidence(cv_evidence),
                scorecard_text=scorecard_text,
                candidate_name=first_name, role=role,
            )

        body_html, title_line, full_html, result = _render_and_check(content)

        # REVIEW PASS. The regex harness enforces spellings; it cannot see a
        # rephrasing. Measured on one real draft: the harness reported 3 phrases
        # while the letter contained 11 more violations of the same rules, none
        # of them matchable ("pushed back" vs the pattern's "pushed you",
        # "pulled toward" vs "pulling toward"), plus a whole paragraph listing
        # everything the candidate failed to demonstrate, which contains no
        # forbidden word at all. A second model pass judges by MEANING and
        # repairs the sentences. Skipped when the model is unreachable.
        if not drafter_name.startswith("unavailable"):
            hits = "\n".join(
                f"  - {v['rule']}: {v['detail']}"
                for v in result["violations"] if v["severity"] == "HARD_BLOCK"
            )
            reviewed, review_status = _review_pass(
                drafter, content, email_type=email_type, first_name=first_name,
                role=role, harness_hits=hits or None,
            )
            if review_status.startswith("failed"):
                # Say so on the draft itself. A letter that skipped the semantic
                # review looks identical to one that passed it.
                result["violations"].append({
                    "rule": "Semantic review did not run",
                    "severity": "WARNING",
                    "detail": (f"The second-pass reviewer {review_status}. The regex "
                               f"checks cannot see a rephrasing, so this draft has NOT "
                               f"been judged for coaching, grading or person-level "
                               f"judgement by meaning. Read it yourself before sending."),
                })
            if reviewed is not content:
                r_body, r_title, r_full, r_result = _render_and_check(reviewed)
                # Keep the review only if it did not make things worse.
                def _hard(res):
                    return sum(1 for v in res["violations"] if v["severity"] == "HARD_BLOCK")
                if _hard(r_result) <= _hard(result):
                    content, body_html, title_line, full_html, result = (
                        reviewed, r_body, r_title, r_full, r_result
                    )
                    log.info("Review pass applied: %d -> %d hard blocks.",
                             _hard(result), _hard(r_result))

        candidate = {
            "content": content,
            "body_html": body_html,
            "title_line": title_line,
            "full_html": full_html,
            "eval": result,
            "attempts": attempt + 1,
            "drafter_used": drafter_name,
        }
        # Keep the LEAST-BAD attempt, not merely the last one. Attempt 3 can be
        # worse than attempt 2: fixing one violation regularly introduces
        # another (a draft cut to satisfy a tone rule falls under 800 words).
        def _hard_count(r):
            return sum(1 for v in r["violations"] if v["severity"] == "HARD_BLOCK")

        if best is None or _hard_count(result) < _hard_count(best["eval"]):
            best = candidate
        # An empty scaffold can never satisfy the 800-word rule; retrying would
        # just burn two more failing calls. Stop and let the human write it.
        if drafter_name.startswith("unavailable"):
            break
        hard = [v for v in result["violations"] if v["severity"] == "HARD_BLOCK"]
        if not hard:
            break
        prior = hard  # feed the hard blocks back for the next attempt

    # Say so when every attempt failed. Handing back a broken draft with no
    # signal reads as "here is your letter" when it means "I could not write one".
    degraded = getattr(drafter, "degraded_from", None)
    if best and degraded:
        best["eval"]["violations"].append({
            "rule": "Written by a fallback model",
            "severity": "WARNING",
            "detail": (
                f"The configured model ({degraded}) could not be used for this "
                f"draft, so it was written by {drafter.model} instead. On a "
                f"Claude Code subscription token the Sonnet and Opus quota can "
                f"run out while Haiku still answers. The tone judgement is "
                f"weaker on the smaller model, so read this letter closely."
            ),
        })

    if best and untranslated:
        best["eval"]["violations"].append({
            "rule": "Hiring manager's summary was left out",
            "severity": "WARNING",
            "detail": (
                "The manager's own summary note could not be translated into "
                "candidate-safe wording, so it was withheld from the writer "
                "rather than passed through raw. This letter was written from "
                "the interview observations alone and may be less specific "
                "about the decision. Read it before sending."
            ),
        })

    if best and _hard_count(best["eval"]) > 0:
        best["retries_exhausted"] = True
        log.warning(
            "Drafting %s: %d attempts, still %d hard block(s); returning the least-bad.",
            email_type, best["attempts"], _hard_count(best["eval"]),
        )

    return best
