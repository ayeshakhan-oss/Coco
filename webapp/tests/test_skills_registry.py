"""Every sub-skill must ship, be discoverable, and claim only what is true.

Run: python -m pytest webapp/tests/test_skills_registry.py -v

THE DEFECT THIS EXISTS FOR (2026-09-25). The Docker image copied
`.claude/skills/01_candidate-communication/` and
`.claude/skills/02_candidate-evaluation/` and nothing else. **29 of the 46
sub-skill files were absent from production**, including files that their own
service names as SOURCE OF TRUTH in a docstring. Six module tiles read "live"
while most of the method behind them was not on the server.

Nothing caught it because the app never asked for those files at runtime, so
nothing failed. Absence is silent unless something counts.

Three properties:
  1. SHIPPED — every skill folder on disk is re-included in .dockerignore AND
     copied in the Dockerfile.
  2. DISCOVERABLE — every .md on disk appears in the registry.
  3. HONEST — `wired` is only claimed where a real route serves it.
"""

from __future__ import annotations

import os
import pathlib
import re

import pytest

from webapp.services import skills as svc

REPO = pathlib.Path(__file__).resolve().parents[2]
SKILLS = REPO / ".claude" / "skills"


def _skill_dirs() -> list[str]:
    return sorted(
        d.name for d in SKILLS.iterdir()
        if d.is_dir() and d.name not in svc.EXCLUDED_DIRS
    )


def _md_files() -> list[str]:
    out = []
    for d in _skill_dirs():
        for f in sorted((SKILLS / d).rglob("*.md")):
            out.append(f"{d}/{f.relative_to(SKILLS / d).as_posix()}")
    return out


# --------------------------------------------------------------------------
# 1. Shipped
# --------------------------------------------------------------------------


def test_there_are_skills_to_check():
    """A collector finding nothing would make every test below vacuous."""
    assert len(_skill_dirs()) >= 7, _skill_dirs()
    assert len(_md_files()) >= 40, len(_md_files())


@pytest.mark.parametrize("skill_dir", _skill_dirs())
def test_every_skill_folder_is_copied_by_the_dockerfile(skill_dir):
    body = (REPO / "Dockerfile").read_text(encoding="utf-8")
    needle = f"COPY .claude/skills/{skill_dir}/"
    assert needle in body, (
        f"{skill_dir} is not copied into the image, so every sub-skill in it "
        "is absent on Railway. This is the 2026-09-25 defect."
    )


@pytest.mark.parametrize("skill_dir", _skill_dirs())
def test_every_skill_folder_survives_dockerignore(skill_dir):
    """`.claude/*` is excluded wholesale, so each folder needs its own `!`
    re-include or the COPY fails the build outright."""
    body = (REPO / ".dockerignore").read_text(encoding="utf-8")
    assert f"!.claude/skills/{skill_dir}" in body, (
        f"{skill_dir} is not re-included in .dockerignore"
    )


def test_the_vendored_design_skill_is_deliberately_not_shipped():
    """ui-ux-pro-max is third-party guidance and Rule 9 bars it from the
    locked candidate layouts. Excluding it is a decision, so it is asserted
    rather than left to whoever edits the Dockerfile next."""
    assert "ui-ux-pro-max" in svc.EXCLUDED_DIRS
    body = (REPO / "Dockerfile").read_text(encoding="utf-8")
    assert "COPY .claude/skills/ui-ux-pro-max" not in body


def test_the_dockerfile_check_bites():
    """Proof: a folder name that is not copied must be reported."""
    body = (REPO / "Dockerfile").read_text(encoding="utf-8")
    assert "COPY .claude/skills/99_not_a_real_skill/" not in body


# --------------------------------------------------------------------------
# 2. Discoverable
# --------------------------------------------------------------------------


def test_every_markdown_file_on_disk_appears_in_the_registry():
    found = svc.discover()
    listed = {f["path"] for s in found for f in s["sub_skills"]}
    listed |= {s["overview"]["path"] for s in found if s.get("overview")}
    missing = sorted(set(_md_files()) - listed)
    assert not missing, (
        "These sub-skill files exist but the registry does not list them, so "
        "they would not appear in the app:\n  " + "\n  ".join(missing)
    )


def test_the_registry_finds_all_seven_skills():
    found = svc.discover()
    assert {s["id"] for s in found} == set(_skill_dirs())


def test_no_skill_is_listed_with_an_empty_title():
    """19 files have no frontmatter, so the fallback chain has to work."""
    for skill in svc.discover():
        assert skill["label"].strip(), skill["id"]
        for f in skill["sub_skills"]:
            assert f["title"].strip(), f["path"]


def test_a_slug_frontmatter_name_becomes_a_readable_title():
    """`name: 06_candidate-invites` rendered as '06candidate-invites' because
    the markdown stripper treats an underscore as emphasis."""
    assert svc._prettify_slug("06_candidate-invites") == "Candidate invites"
    assert svc._prettify_slug("data-and-systems") == "Data and systems"


def test_frontmatter_that_cannot_be_parsed_never_raises():
    """A bare `word: ` inside an unquoted description silently kills the
    block (Rule 27). The registry must degrade, not crash."""
    assert svc._frontmatter("---\nname: x: y: z\n---\nbody\n") in ({}, {"name": "x: y: z"})
    assert svc._frontmatter("no frontmatter at all") == {}


def test_missing_skills_directory_returns_empty_rather_than_raising():
    assert svc.discover(root=str(REPO / "does" / "not" / "exist")) == []


# --------------------------------------------------------------------------
# 3. Honest
# --------------------------------------------------------------------------


def _spa_routes() -> set[str]:
    body = (REPO / "frontend" / "src" / "App.tsx").read_text(encoding="utf-8")
    return set(re.findall(r'<Route path="(/[^"]*)"', body))


@pytest.mark.parametrize(
    "rel,route",
    sorted((k, v[0]) for k, v in svc.IMPLEMENTED_BY.items()),
)
def test_every_wired_subskill_points_at_a_route_the_app_serves(rel, route):
    """A renamed page must not leave a dead link advertised as a feature."""
    assert route in _spa_routes(), f"{rel} claims {route}, which the SPA does not serve"


@pytest.mark.parametrize("rel", sorted(svc.IMPLEMENTED_BY))
def test_every_wired_subskill_file_actually_exists(rel):
    assert (SKILLS / rel).is_file(), f"{rel} is claimed as wired but is not on disk"


@pytest.mark.parametrize("rel", sorted(svc.NOT_ON_SERVER))
def test_every_claude_code_only_file_exists_and_gives_a_reason(rel):
    assert (SKILLS / rel).is_file(), rel
    assert len(svc.NOT_ON_SERVER[rel]) > 40, (
        f"{rel} is excluded from the server with no real explanation"
    )


def test_a_file_is_never_both_wired_and_excluded():
    assert not (set(svc.IMPLEMENTED_BY) & set(svc.NOT_ON_SERVER))


def test_contract_drafting_is_reported_as_reference_not_as_a_feature():
    """Skill 07 has 12 files and no page in this app. Reporting it as wired
    would be exactly the overclaim this work is fixing."""
    skill = next(s for s in svc.discover() if s["id"] == "07_contract-drafting")
    assert skill["counts"]["wired"] == 0
    assert skill["counts"]["total"] >= 11


def test_the_summary_counts_add_up():
    found = svc.discover()
    s = svc.summarise(found)
    assert s["sub_skills"] == len(_md_files())
    assert s["wired"] + s["reference"] + s["claude_code_only"] == s["sub_skills"]
    assert s["shipped"] is True


# --------------------------------------------------------------------------
# Reading a file cannot escape the skills directory
# --------------------------------------------------------------------------


def test_a_real_subskill_body_can_be_read():
    body = svc.read_file("03_operations/attendance-reports.md")
    assert body and len(body.split()) > 50


@pytest.mark.parametrize(
    "path",
    [
        "../../.env",
        "../config/token_gmail.json",
        "../../webapp/config.py",
        "/etc/passwd",
        "01_candidate-communication/../../config/token_gmail.json",
    ],
)
def test_traversal_out_of_the_skills_directory_is_refused(path):
    """`.claude/` also holds OAuth tokens, so a traversal here reads
    credentials. The path comes straight off a URL."""
    assert svc.read_file(path) is None


def test_only_markdown_is_served():
    assert svc.read_file("05_talent-sourcing") is None
    assert svc.read_file("does/not/exist.md") is None


def test_the_traversal_guard_bites():
    """Proof the refusal above is the guard and not just a missing file: the
    token file it tries to reach is real on this machine when present."""
    target = REPO / ".claude" / "config"
    if not target.is_dir():
        pytest.skip("no .claude/config in this checkout")
    real = next((p for p in target.glob("*.json")), None)
    if real is None:
        pytest.skip("no config file to attempt")
    rel = os.path.relpath(real, SKILLS).replace(os.sep, "/")
    assert svc.read_file(rel) is None, "traversal reached a real config file"


# --------------------------------------------------------------------------
# The counts printed on the home page must match the real files
# --------------------------------------------------------------------------

# The module cards say "8 letter types", "6 evaluation skills" and so on. A
# hardcoded count is exactly the kind of claim that drifts the moment somebody
# adds a file, so each one is checked against what is on disk.


def _home_labels() -> dict[str, str]:
    body = (REPO / "frontend" / "src" / "lib" / "modules.ts").read_text(encoding="utf-8")
    block = body.split("export const SKILL_FOR_MODULE")[1]
    return dict(re.findall(r"'([a-z-]+)':\s*'([^']+)'", block))


def _count_in(label: str) -> int | None:
    m = re.match(r"(\d+)", label)
    return int(m.group(1)) if m else None


def _files_in(skill_dir: str) -> list[str]:
    return [f.name for f in (SKILLS / skill_dir).glob("*.md")]


def test_the_home_page_labels_exist_for_every_live_module():
    labels = _home_labels()
    assert labels, "SKILL_FOR_MODULE did not parse"
    for slug in ("candidate-communication", "candidate-evaluation",
                 "hiring-operations", "data-systems", "candidate-invites"):
        assert slug in labels, slug


@pytest.mark.parametrize(
    "slug,skill_dir",
    [
        ("candidate-evaluation", "02_candidate-evaluation"),
        ("hiring-operations", "03_operations"),
        ("data-systems", "04_data-and-systems"),
    ],
)
def test_component_counts_match_the_files_minus_the_overview(slug, skill_dir):
    """These three are one file per component plus SKILL.md."""
    label = _home_labels()[slug]
    claimed = _count_in(label)
    actual = len(_files_in(skill_dir)) - 1  # SKILL.md is the overview
    assert claimed == actual, f"{slug} says {label!r} but {skill_dir} has {actual}"


def test_the_letter_type_count_matches_the_numbered_type_files():
    """Skill 01 also holds SKILL.md and a benchmark letter, neither of which
    is a type, so the count is the numbered files 01-08."""
    claimed = _count_in(_home_labels()["candidate-communication"])
    numbered = [f for f in _files_in("01_candidate-communication")
                if re.match(r"^0[1-8]_", f)]
    assert claimed == len(numbered), numbered


def test_the_invite_type_count_matches_the_backend_constant():
    """Skill 06's seven types live inside SKILL.md, so the file count cannot
    check this one. The service constant can."""
    from webapp.services.invites import INVITE_TYPES

    claimed = _count_in(_home_labels()["candidate-invites"])
    assert claimed == len(INVITE_TYPES) == 7


def test_the_count_check_bites():
    """Proof: a wrong claim must fail. 02 has 6 components, never 99."""
    actual = len(_files_in("02_candidate-evaluation")) - 1
    assert actual != 99 and _count_in("99 evaluation skills") == 99
