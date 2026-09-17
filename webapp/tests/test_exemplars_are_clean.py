"""An exemplar must pass the rules it is teaching.

2026-09-17: the four letters Ayesha has actually sent were extracted from Sent
Mail to become the drafter's exemplars, replacing the single warm-bench
benchmark that was standing in for all four types. Three were clean. The fourth,
a CV rejection sent on 14 Sep, was drafted BEFORE the core tone was locked later
that same day, and fails today's rules:

    Coaching          "what we would encourage you to develop"
    Career direction  "leadership philosophy"
    Grading           "Your response", "We were looking for a"

It was dropped. Had it shipped, the drafter would have been shown a coaching
letter as the standard while being hard-blocked for coaching — the strongest
possible mixed signal, and exactly the kind of contradiction that made the app
ignore its own rules in the first place.

A sent letter is not automatically a good exemplar. The rules move; the archive
does not. This file makes that check mechanical rather than remembered.

Run: python -m pytest webapp/tests/test_exemplars_are_clean.py
"""

from __future__ import annotations

import os
import re

import pytest

from scripts.evals.candidate_communication_eval import (
    check_harsh_language,
    check_never_in_a_letter,
    check_tone_categories,
)

_EXEMPLAR_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..",
    ".claude", "skills", "01_candidate-communication", "exemplars",
)
_BENCHMARK = os.path.join(
    os.path.dirname(__file__), "..", "..",
    ".claude", "skills", "01_candidate-communication",
    "00_BENCHMARK-approved-letter.md",
)


def _letter_bodies(path: str) -> str:
    """The prose of the exemplar, without our own framing.

    The anti-copy warning legitimately names banned constructions in order to
    forbid them, so scanning it would flag every file. Only the letter text
    below the first `---` divider is the exemplar itself.
    """
    with open(path, encoding="utf-8") as f:
        text = f.read()
    parts = text.split("\n---\n")
    return "\n".join(parts[1:]) if len(parts) > 1 else text


def _exemplar_files():
    if not os.path.isdir(_EXEMPLAR_DIR):
        return []
    return [
        os.path.join(_EXEMPLAR_DIR, n)
        for n in sorted(os.listdir(_EXEMPLAR_DIR))
        if n.endswith(".md")
    ]


def test_at_least_one_exemplar_ships():
    assert _exemplar_files(), (
        "no exemplars found; the drafter would fall back to deriving the "
        "standard from rules alone, which is what it was doing badly"
    )


@pytest.mark.parametrize("path", _exemplar_files() or [None])
def test_exemplar_breaks_no_tone_rule(path):
    if path is None:
        pytest.skip("no exemplars")
    email_type = os.path.splitext(os.path.basename(path))[0]
    body = _letter_bodies(path)

    offences = []
    for _cat, label, hits in check_tone_categories(body, email_type):
        offences.append(f"{label}: {hits[:4]}")
    harsh = check_harsh_language(body, email_type)[1]
    if harsh:
        offences.append(f"harsh language: {harsh[:120]}")
    never = check_never_in_a_letter(body, "", email_type)[1]
    if never:
        offences.append(f"repeats a confidence: {never[:120]}")

    assert not offences, (
        f"{os.path.basename(path)} is shown to the drafter as the standard but "
        f"breaks the rules it is teaching: {offences}. A sent letter is not "
        f"automatically a good exemplar - the rules move, the archive does not."
    )


def test_the_benchmark_letter_also_passes():
    """The original benchmark is held to the same bar as the new exemplars.

    Only the letter is scanned. The file also carries a "what it never does"
    list and a table of the five sentences that had to be repaired, both of
    which QUOTE the banned constructions in order to forbid them. The same span
    the eval harness reads is the right one.
    """
    with open(_BENCHMARK, encoding="utf-8") as f:
        text = f.read()
    assert "## THE LETTER, AS SENT" in text, "benchmark markers moved"
    body = text.split("## THE LETTER, AS SENT", 1)[1].split("## HOW THIS LETTER", 1)[0]
    offences = [f"{label}: {hits[:4]}"
                for _c, label, hits in check_tone_categories(body, "warm_bench")]
    assert not offences, f"the benchmark letter itself breaks: {offences}"


def test_exemplars_carry_the_anti_copy_warning():
    """An exemplar without it invites another candidate's story into a letter."""
    for path in _exemplar_files():
        with open(path, encoding="utf-8") as f:
            head = f.read(1200)
        assert re.search(r"COPY THE MOVES.{0,40}NEVER THE CONTENT", head, re.I), (
            f"{os.path.basename(path)} is missing the anti-copy warning"
        )
