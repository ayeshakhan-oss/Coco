"""The benchmark letter must pass the rules it is teaching.

2026-09-17: Ayesha's decision is that the drafter works from the SOPs, the tone
rules and the harness, NOT from a growing library of example letters. So no new
exemplars ship. The one benchmark letter that predates that decision stays, and
this file holds it to the current rules.

Why the check exists at all: four sent letters were extracted from Sent Mail as
candidate exemplars, and one of them - a CV rejection sent on 14 Sep, hours
before the core tone was locked later the same day - failed today's rules:

    Coaching          "what we would encourage you to develop"
    Career direction  "leadership philosophy"
    Grading           "Your response", "We were looking for a"

Shown as the standard it would have taught the drafter to coach while the
harness hard-blocks coaching. **A sent letter is not automatically a good
example: the rules move, the archive does not.** Anything we ever hold up as the
standard has to keep passing, and that has to be mechanical rather than
remembered.

Run: python -m pytest webapp/tests/test_exemplars_are_clean.py
"""

from __future__ import annotations

import os

from scripts.evals.candidate_communication_eval import (
    check_harsh_language,
    check_never_in_a_letter,
    check_tone_categories,
)

_BENCHMARK = os.path.join(
    os.path.dirname(__file__), "..", "..",
    ".claude", "skills", "01_candidate-communication",
    "00_BENCHMARK-approved-letter.md",
)


def _benchmark_letter_only() -> str:
    """Just the letter.

    The file also carries a "what it never does" list and a table of the five
    sentences that had to be repaired, both of which QUOTE banned constructions
    in order to forbid them. Scanning those would flag the file for teaching the
    rules. This is the same span the eval harness reads.
    """
    with open(_BENCHMARK, encoding="utf-8") as f:
        text = f.read()
    assert "## THE LETTER, AS SENT" in text, "benchmark section markers moved"
    return text.split("## THE LETTER, AS SENT", 1)[1].split("## HOW THIS LETTER", 1)[0]


def test_the_benchmark_letter_breaks_no_rule_it_teaches():
    body = _benchmark_letter_only()
    offences = [
        f"{label}: {hits[:4]}"
        for _cat, label, hits in check_tone_categories(body, "warm_bench")
    ]
    harsh = check_harsh_language(body, "warm_bench")[1]
    if harsh:
        offences.append(f"harsh language: {harsh[:120]}")
    never = check_never_in_a_letter(body, "", "warm_bench")[1]
    if never:
        offences.append(f"repeats a confidence: {never[:120]}")

    assert not offences, (
        "the benchmark letter is shown to the drafter as the standard but breaks "
        f"the rules it teaches: {offences}"
    )


def test_the_benchmark_carries_its_anti_copy_warning():
    """Without it, another candidate's story walks into a letter as fabrication."""
    with open(_BENCHMARK, encoding="utf-8") as f:
        head = f.read(2000)
    assert "NOT A TEMPLATE" in head.upper(), "anti-copy warning missing"


def test_no_example_letters_have_crept_back_in():
    """Ayesha 2026-09-17: the drafter follows the SOPs, rules and harness, and we
    do not solve tone problems by adding more example letters. The single
    benchmark predates that and stays; a new exemplars directory does not."""
    strays = os.path.join(
        os.path.dirname(__file__), "..", "..",
        ".claude", "skills", "01_candidate-communication", "exemplars",
    )
    assert not os.path.isdir(strays), (
        "an exemplars directory is back. The decision was to work from the SOPs, "
        "the rules and the harness rather than a library of examples."
    )
