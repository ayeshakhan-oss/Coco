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

    def __init__(self, model: str, api_key: Optional[str] = None, auth_token: Optional[str] = None):
        from anthropic import Anthropic

        self.model = model
        self.mode = "api_key" if api_key else "oauth"
        if api_key:
            self.client = Anthropic(api_key=api_key)
        else:
            # Local-dev only: reuse the Claude Code subscription token.
            self.client = Anthropic(
                auth_token=auth_token,
                default_headers={"anthropic-beta": "oauth-2025-04-20"},
            )

    def draft(self, *, system, user, email_type, first_name, role, prior_violations=None, attempt=0) -> dict:
        content = user
        if prior_violations:
            content = user + _fix_instruction(prior_violations)
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": content}],
        )
        text = "".join(b.text for b in msg.content if getattr(b, "type", None) == "text")
        return _parse_json(text)


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
                   email_type: str, cv_evidence: Optional[dict] = None) -> dict:
    """Generate + self-correct a draft. Returns a dict with the rendered body,
    title, full HTML, eval result, attempts, and which drafter was used.

    Raises MissingEvidence (propagated from build_user_prompt) when this email
    type has no evidence to stand on. The caller must surface that, never draft.
    """
    system = system_prompt(email_type)
    user = build_user_prompt(scorecard=scorecard, first_name=first_name, role=role,
                             email_type=email_type, cv_evidence=cv_evidence)

    drafter = get_drafter()
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

        body_html = rendering.render_body(
            content, email_type=email_type, candidate_name=first_name, role=role, app_id=app_id
        )
        title_line = rendering.title_for(content, email_type)
        full_html = rendering.wrap_full(body_html, title_line=title_line, role=role, email_type=email_type)
        result = evaluate_email(
            full_html, title_line, email_type, pilot_mode=True,
            cv_corpus=_corpus_from_evidence(cv_evidence),
            candidate_name=first_name, role=role,
        )

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
    if best and _hard_count(best["eval"]) > 0:
        best["retries_exhausted"] = True
        log.warning(
            "Drafting %s: %d attempts, still %d hard block(s); returning the least-bad.",
            email_type, best["attempts"], _hard_count(best["eval"]),
        )

    return best
