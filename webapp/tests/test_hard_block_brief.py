"""Every rule that can BLOCK a letter must be a rule the writer was told.

Ayesha, 2026-09-15: "putting hard blocks is not the only solution, you need to
FOLLOW those hard blocks."

She was right, and the cause was structural drift. The harness knew sixteen
blocking rules plus six tone behaviours; the drafting prompt carried a
hand-written subset. A rule added to the harness never reached the writer, so
the writer kept breaking rules nobody had told it about, and every fix was
another block for a defect Ayesha had already found by hand.

HARD_BLOCK_BRIEF is now the single source, injected into both the writer and the
reviewer. This file fails if the two drift apart again: adding a HARD_BLOCK to
the harness without a line for the writer is a test failure, not a discovery
three letters later.

Run: python -m pytest webapp/tests/test_hard_block_brief.py
"""

from __future__ import annotations

import os
import re

from scripts.evals.candidate_communication_eval import (
    COACHING_CATEGORY_LABELS,
    HARD_BLOCK_BRIEF,
    writer_hard_blocks,
)

_EVAL = os.path.join(
    os.path.dirname(__file__), "..", "..", "scripts", "evals",
    "candidate_communication_eval.py",
)


def _emitted_hard_block_rules() -> set[str]:
    """Every rule literal the harness can attach to a HARD_BLOCK, read from source.

    Static, so it sees rules no test happens to trigger. A rule whose name is
    built with an f-string is captured by its literal prefix, which is why the
    brief is matched by prefix rather than by equality.
    """
    with open(_EVAL, encoding="utf-8") as f:
        src = f.read()
    found = set()
    for body in re.findall(r"violations\.append\(\{(.*?)\}\)", src, re.DOTALL):
        if "HARD_BLOCK" not in body:
            continue
        m = re.search(r"'rule':\s*f?['\"](.+?)['\"]", body)
        if m:
            found.add(m.group(1).strip())
    return found


def _is_covered(rule: str) -> bool:
    """A brief entry covers a rule when one is a prefix of the other."""
    return any(
        rule.startswith(name) or name.startswith(rule)
        for name in HARD_BLOCK_BRIEF
    )


def test_every_blocking_rule_is_explained_to_the_writer():
    emitted = _emitted_hard_block_rules()
    assert emitted, "no HARD_BLOCK rules found; the parser has drifted"
    # Word count is handled by the length contract, not the rule brief.
    emitted = {r for r in emitted if not r.lower().startswith("word count")}
    missing = sorted(r for r in emitted if not _is_covered(r))
    assert not missing, (
        "these rules BLOCK a letter but the writer is never told about them, "
        "which is exactly how it kept breaking rules nobody had stated: "
        f"{missing}. Add a line to HARD_BLOCK_BRIEF."
    )


def test_every_tone_behaviour_is_explained_to_the_writer():
    missing = sorted(
        label for label in COACHING_CATEGORY_LABELS.values()
        if not _is_covered(label)
    )
    assert not missing, f"tone behaviours missing from HARD_BLOCK_BRIEF: {missing}"


def test_the_brief_reaches_the_drafting_prompt():
    from webapp.prompts.tone_rules import system_prompt

    for email_type in ("warm_bench", "cv_rejection", "values_feedback", "gwc_rejection"):
        prompt = system_prompt(email_type)
        for line in writer_hard_blocks(email_type).splitlines():
            rule = line.split(":")[0].strip(" -")
            assert rule in prompt, (
                f"{email_type}: the writer is not told about {rule!r}"
            )


def test_cv_only_rules_are_scoped_to_cv_rejection():
    assert "CV rejection" in writer_hard_blocks("cv_rejection")
    assert "CV rejection" not in writer_hard_blocks("warm_bench")
