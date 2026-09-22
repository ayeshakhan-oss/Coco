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


# Folder-level COPY covers any file inside, but not a RENAME. These modules
# read one specific file by path at runtime and raise if it is missing, so the
# filename itself is load-bearing.
SOP_FILES_READ_AT_RUNTIME = [
    ".claude/skills/02_candidate-evaluation/cv-screening.md",
    ".claude/skills/02_candidate-evaluation/case-study-scoring-rubric.md",
]


def test_sop_files_read_at_runtime_exist_and_are_inside_a_copied_dir():
    dockerfile = _read("Dockerfile")
    for rel in SOP_FILES_READ_AT_RUNTIME:
        assert os.path.isfile(os.path.join(ROOT, rel)), (
            f"{rel} is read at runtime by a prompt module and is missing on disk"
        )
        parent = os.path.dirname(rel)
        assert f"COPY {parent}/ {parent}/" in dockerfile, (
            f"{rel} would not reach the image: no COPY for {parent}/"
        )


def test_the_cv_screening_prompt_actually_resolves_its_sop():
    """The path is built with os.path.join and '..' hops from the prompt
    module. A wrong number of hops resolves to a real-looking path that does
    not exist, and the failure only appears at the first screen."""
    from webapp.prompts import cv_screening_prompt

    system = cv_screening_prompt.system_prompt()
    assert "# The SOP, verbatim" in system
    assert "Minimum reading capacity" in system, "the SOP body did not make it in"
    assert len(cv_screening_prompt.sop_sha256()) == 64
