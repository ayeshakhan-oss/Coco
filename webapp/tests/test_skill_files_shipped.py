"""Guard: every skill folder the app expects is actually COPYed into the image.

The failure this prevents is silent. A .dockerignore negation without a matching
COPY builds clean, the folder is absent at runtime, and the readers in
tone_rules.py swallow the OSError and return "". The only symptom is worse output.
"""

from __future__ import annotations

import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EXPECTED_SKILL_DIRS = [
    ".claude/skills/01_candidate-communication",
    ".claude/skills/02_candidate-evaluation",
]


def _read(rel: str) -> str:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def test_expected_skill_dirs_exist_on_disk():
    for d in EXPECTED_SKILL_DIRS:
        assert os.path.isdir(os.path.join(ROOT, d)), f"missing on disk: {d}"


def test_expected_skill_dirs_are_copied_into_the_image():
    dockerfile = _read("Dockerfile")
    for d in EXPECTED_SKILL_DIRS:
        assert f"COPY {d}/ {d}/" in dockerfile, f"no COPY line for {d}"


def test_expected_skill_dirs_are_reincluded_in_dockerignore():
    ignore = _read(".dockerignore")
    lines = [ln.strip() for ln in ignore.splitlines()]
    assert ".claude/skills/*" in lines, "the exclude line disappeared"
    star_at = lines.index(".claude/skills/*")
    for d in EXPECTED_SKILL_DIRS:
        negation = f"!{d}"
        assert negation in lines, f"no re-inclusion for {d}"
        # A negation BEFORE the exclude does nothing. Order is load-bearing.
        assert lines.index(negation) > star_at, f"{negation} must come after .claude/skills/*"
