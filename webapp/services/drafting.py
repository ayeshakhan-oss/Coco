"""AI drafting engine.

Flow: build prompt -> LLM returns content-only JSON -> render to v8 HTML ->
evaluate_email() -> if HARD-BLOCKs, feed them back and retry (<=3) -> return the
best draft. The model never auto-sends; a human reviews and approves.

Client selection (auto):
  1. ANTHROPIC_API_KEY set  -> AnthropicDrafter (api key) — the production path.
  2. else, non-production    -> AnthropicDrafter (local Claude Code OAuth token),
                                best-effort so we can verify real output locally.
  3. else                    -> StubDrafter (deterministic, offline).
A live-call failure on (2) degrades to the stub for that request.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Optional

from ..config import get_settings
from ..prompts.draft_prompt import build_user_prompt
from ..prompts.tone_rules import system_prompt
from ..reuse import SECTION_HEADINGS, evaluate_email
from . import rendering

log = logging.getLogger("webapp.drafting")

MAX_ATTEMPTS = 3


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
    s = get_settings()
    if s.anthropic_api_key:
        return AnthropicDrafter(s.anthropic_model, api_key=s.anthropic_api_key)
    if not s.is_production:
        token = _load_oauth_token()
        if token:
            log.warning(
                "No ANTHROPIC_API_KEY; using the local Claude Code OAuth token for "
                "drafting (DEV ONLY — a deployed service needs ANTHROPIC_API_KEY)."
            )
            return AnthropicDrafter(s.anthropic_model, auth_token=token)
    log.warning("No Anthropic credential available — using StubDrafter.")
    return StubDrafter()


def generate_draft(*, scorecard: Optional[dict], first_name: str, role: str, app_id, email_type: str) -> dict:
    """Generate + self-correct a draft. Returns a dict with the rendered body,
    title, full HTML, eval result, attempts, and which drafter was used."""
    system = system_prompt(email_type)
    user = build_user_prompt(scorecard=scorecard, first_name=first_name, role=role, email_type=email_type)

    drafter = get_drafter()
    prior: Optional[list[dict]] = None
    best = None

    for attempt in range(MAX_ATTEMPTS):
        try:
            content = drafter.draft(
                system=system, user=user, email_type=email_type,
                first_name=first_name, role=role, prior_violations=prior, attempt=attempt,
            )
        except Exception as exc:  # live-call failure -> degrade to stub for this request
            log.warning("Drafter %s failed (%s); falling back to StubDrafter.", drafter.name, exc)
            drafter = StubDrafter()
            content = drafter.draft(
                system=system, user=user, email_type=email_type,
                first_name=first_name, role=role, prior_violations=prior, attempt=attempt,
            )

        body_html = rendering.render_body(
            content, email_type=email_type, candidate_name=first_name, role=role, app_id=app_id
        )
        title_line = rendering.title_for(content, email_type)
        full_html = rendering.wrap_full(body_html, title_line=title_line, role=role, email_type=email_type)
        result = evaluate_email(full_html, title_line, email_type, pilot_mode=True)

        best = {
            "content": content,
            "body_html": body_html,
            "title_line": title_line,
            "full_html": full_html,
            "eval": result,
            "attempts": attempt + 1,
            "drafter_used": drafter.name,
        }
        hard = [v for v in result["violations"] if v["severity"] == "HARD_BLOCK"]
        if not hard:
            break
        prior = hard  # feed the hard blocks back for the next attempt

    return best
