"""The prompt must not answer the same question two different ways.

2026-09-17. Ayesha asked what prompt fires when she clicks Draft, because
letters written offline hit the standard and letters written by the app did not.
Measuring it answered the question: the prompt was telling Haiku three different
things about length at once.

    per-type SOPs    "800-1100 words MANDATORY"        ELEVEN places
    output contract  "at least 800 words"              one
    rule card        "700 to 800, NEVER more than 800" one

The model was following the majority. It was obeying us; we were contradicting
ourselves, and every letter landing at 988-1144 words was the predictable
result. A bigger model hides this. A small one cannot, and Haiku is what the
credential serves.

These tests fail if a second answer ever appears. Without them the next rule
change reintroduces the same bug silently, and it surfaces three letters later
as "the model is ignoring the rules".

Run: python -m pytest webapp/tests/test_prompt_coherence.py
"""

from __future__ import annotations

import re

import pytest

from webapp.prompts import tone_rules as t
from webapp.reuse import EMAIL_TYPES

# A band ("800 to 1,100 words", "800-1100 words") or a bare floor/ceiling
# ("at least 800 words", "no more than 800 words").
_BAND = re.compile(
    r"\b(\d{3,4})\s*(?:to|-|–|—)\s*([\d,]{3,5})\s*words?\b", re.IGNORECASE)
_SINGLE = re.compile(
    r"\b(?:at least|minimum(?: of)?|no more than|not exceed|under|over|max(?:imum)?(?: of)?)"
    r"\s+([\d,]{3,5})\s*words?\b", re.IGNORECASE)


def _norm(n: str) -> int:
    return int(n.replace(",", ""))


def _show(claims) -> list:
    """Sortable rendering. A bare floor carries None as its upper bound, which
    is not orderable against an int, so the assertion message itself used to
    raise a TypeError and hide the very mismatch it was reporting."""
    return sorted((lo, hi if hi is not None else -1) for lo, hi in claims)


def _length_claims(prompt: str) -> set:
    """Every distinct length instruction, normalised so that '800 to 1,100',
    '800-1100' and '800 TO 1,100' count as one claim and not three."""
    claims = {(_norm(a), _norm(b)) for a, b in _BAND.findall(prompt)}
    claims |= {(_norm(n), None) for n in _SINGLE.findall(prompt)}
    return claims


@pytest.mark.parametrize("email_type", EMAIL_TYPES)
def test_the_prompt_states_one_length_rule(email_type):
    claims = _length_claims(t.system_prompt(email_type))
    assert len(claims) <= 1, (
        f"{email_type}: the prompt gives {len(claims)} different length rules "
        f"{sorted(claims)}. A model resolves that by majority, not by which one "
        f"we meant. State it once, in LENGTH_RULE."
    )


@pytest.mark.parametrize("email_type", EMAIL_TYPES)
def test_the_stated_length_is_the_one_constant(email_type):
    claims = _length_claims(t.system_prompt(email_type))
    if not claims:
        pytest.skip(f"{email_type} states no length")
    expected = _length_claims(t.LENGTH_RULE)
    assert claims == expected, (
        f"{email_type} says {sorted(claims)} but LENGTH_RULE says "
        f"{sorted(expected)}. Every component interpolates the constant."
    )


@pytest.mark.parametrize("email_type", EMAIL_TYPES)
def test_the_sops_carry_no_length_rule_of_their_own(email_type):
    """The SOPs are craft guidance. The length is stated in exactly one place,
    and eleven SOP statements are what drowned it out."""
    sops = t._type_sops(email_type)
    assert not _length_claims(sops), (
        f"{email_type}: the distilled SOPs still state a length "
        f"{sorted(_length_claims(sops))}. _strip_operational should drop it."
    )


@pytest.mark.parametrize("email_type", EMAIL_TYPES)
def test_the_sops_carry_no_operations(email_type):
    """The writer returns JSON. It cannot send, pilot, approve or open a file,
    and asking it to skip that material costs more than removing it."""
    sops = t._type_sops(email_type)
    noise = {
        "send scripts": r"PILOT_MODE|safe_sendmail|smtplib|\.py\b",
        "file paths": r"scripts/|\.claude/|memory/",
        "recipients": r"@taleemabad\.com|@niete\.edu\.pk|hiring@",
    }
    found = {k: len(re.findall(v, sops, re.I)) for k, v in noise.items()}
    found = {k: n for k, n in found.items() if n}
    assert not found, f"{email_type}: operations left in the SOPs: {found}"


@pytest.mark.parametrize("email_type", EMAIL_TYPES)
def test_the_prompt_stays_inside_its_budget(email_type):
    """A long instruction block loses its middle, and the middle is where the
    craft guidance sits. This is a ratchet: it may come down, never up."""
    size = len(t.system_prompt(email_type))
    assert size <= 90_000, (
        f"{email_type} prompt is {size:,} chars (~{size // 4:,} tokens). "
        f"It was 88,627 on 17 Sep and the direction of travel is down."
    )


# ---------------------------------------------------------------------------
# EVERY STAGE, not just the writer.
#
# 2026-09-18. The reviewer prompt carried "These letters must not exceed 800
# words" - the ceiling trialled on 15 Sep and reverted on the 17th - for as long
# as it did because every test above inspects t.system_prompt() and nothing
# else. So the writer was told 800-1,100 while the reviewer, which edits the
# letter afterwards, was told to cut below 800, which is also the harness's own
# HARD-BLOCK floor. Exactly the bug this file exists to prevent, one stage over.
#
# Any new stage prompt must be registered below or the last test here fails.
# ---------------------------------------------------------------------------

def _stage_prompts() -> dict:
    from webapp.services import drafting as d

    prompts = {
        "review": d._REVIEWER_SYSTEM,
        "translate": d._TRANSLATOR_SYSTEM,
        "plan": d.PLANNER_SYSTEM,
    }
    for email_type in EMAIL_TYPES:
        prompts[f"write:{email_type}"] = t.system_prompt(email_type)
    return prompts


@pytest.mark.parametrize("stage", sorted(_stage_prompts()))
def test_every_stage_states_the_same_one_length_rule(stage):
    claims = _length_claims(_stage_prompts()[stage])
    assert len(claims) <= 1, (
        f"{stage}: this prompt gives {len(claims)} different length rules "
        f"{_show(claims)}."
    )
    if claims:
        assert claims == _length_claims(t.LENGTH_RULE), (
            f"{stage} says {_show(claims)} but LENGTH_RULE says "
            f"{_show(_length_claims(t.LENGTH_RULE))}. One stage contradicting "
            f"another is invisible to the writer-only tests above."
        )


def test_no_stage_prompt_escapes_these_checks():
    """A prompt that no test inspects is a prompt free to contradict the others."""
    from webapp.services import drafting as d

    declared = {
        name for name, value in vars(d).items()
        if name.endswith("_SYSTEM") and isinstance(value, str)
    }
    registered = {"_REVIEWER_SYSTEM", "_TRANSLATOR_SYSTEM", "PLANNER_SYSTEM"}
    assert declared == registered, (
        f"unregistered system prompt(s): {sorted(declared - registered)}. "
        f"Add them to _stage_prompts() so the coherence rules apply to them too."
    )


@pytest.mark.parametrize("email_type", t._FEEDBACK_TYPES)
def test_the_block_list_and_rule_card_are_last(email_type):
    """Recency is the cheapest lever available on a small model, so the rules
    that block a letter are the last thing it reads."""
    prompt = t.system_prompt(email_type)
    assert "THESE WILL BLOCK YOUR LETTER" in prompt
    assert "THE WHOLE JOB, IN TWENTY LINES" in prompt
    tail = prompt[-6000:]
    assert "THESE WILL BLOCK YOUR LETTER" in tail, (
        "the block list has drifted away from the end of the prompt"
    )
