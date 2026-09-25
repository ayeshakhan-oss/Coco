"""The skill library, read from the files that actually shipped.

Coco's method lives in `.claude/skills/<NN_name>/`: one `SKILL.md` per skill
and a file per sub-skill beside it. Claude Code reads those from the repo. This
module makes the same files visible to the running app, so a sub-skill is
something Railway HAS rather than something the repo has.

🔴 WHY THIS EXISTS. Until 2026-09-25 the Docker image copied only skills 01 and
   02. **29 of the 46 sub-skill files did not exist in production at all** —
   including `03_operations/attendance-reports.md` and
   `06_candidate-invites/SKILL.md`, which their services name as SOURCE OF
   TRUTH in a docstring. The module tiles said "live" while most of the method
   behind them was absent from the server.

🔴 THE LIST IS WALKED, NEVER HARDCODED. A hardcoded inventory drifts the moment
   somebody adds a file, and drifts silently, which is the failure this is
   fixing. `discover()` reads whatever is on disk, so an unshipped folder shows
   up as missing rather than as nothing.

🔴 STATUS IS HONEST, PER FILE. A sub-skill is `wired` only when a real page in
   this app implements it. Everything else is `reference` (guidance the app
   serves but does not execute) or `claude_code_only` (deliberately not on the
   server). Calling all 46 "live features" would be the same overclaim in a
   new place.

⚠️ 19 of the 46 files have NO YAML frontmatter, all of Skill 07 among them, so
   the title falls back to the first `# heading` and then to the filename. A
   parser that required frontmatter would drop a third of the library.
"""

from __future__ import annotations

import os
import re
from typing import Optional

try:  # PyYAML ships with the app, but the library must not fail without it.
    import yaml
except Exception:  # pragma: no cover
    yaml = None

_HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.normpath(os.path.join(_HERE, "..", "..", ".claude", "skills"))

#: Vendored third-party design guidance. Local-only by decision (CLAUDE.md
#: Rule 9 bars it from the locked candidate layouts), so it is not part of
#: Coco's method and is not served.
EXCLUDED_DIRS = {"ui-ux-pro-max"}

WIRED = "wired"
REFERENCE = "reference"
CLAUDE_CODE_ONLY = "claude_code_only"

#: sub-skill file -> the page in THIS app that implements it. Anything absent
#: from here is reference or Claude-Code-only; nothing is assumed wired.
#: `test_skills_registry.py` asserts every route below is one the SPA serves,
#: so a renamed page cannot leave a dead link advertised as a feature.
IMPLEMENTED_BY: dict[str, tuple[str, str]] = {
    # 01 — the five types the webapp can actually draft (`reuse.EMAIL_TYPES`).
    "01_candidate-communication/01_candidate-rejections.md": ("/queue", "CV rejection letters"),
    "01_candidate-communication/02_values-feedback-emails.md": ("/queue", "Values feedback letters"),
    "01_candidate-communication/03_warm-bench-feedback-email.md": ("/queue", "Warm bench letters"),
    "01_candidate-communication/04_gwc-rejection-emails.md": ("/queue", "GWC rejection letters"),
    "01_candidate-communication/08_case-study-outcome-email.md": ("/queue", "Case study outcome letters"),
    # 02 — every component has a page.
    "02_candidate-evaluation/cv-screening.md": ("/cv-screening", "CV screening"),
    "02_candidate-evaluation/case-study-evaluation.md": ("/case-study-tracking", "Case study tracking"),
    "02_candidate-evaluation/case-study-scoring-rubric.md": ("/case-studies", "Case study scoring"),
    "02_candidate-evaluation/kcd-evaluation.md": ("/kcd-evaluations", "KCD evaluation"),
    "02_candidate-evaluation/values-scorecard-scoring.md": ("/values-scorecards", "Values scorecards"),
    "02_candidate-evaluation/technical-screening.md": ("/tech-screening", "Technical screening"),
    # 03 — three of five.
    "03_operations/attendance-reports.md": ("/attendance", "Daily attendance"),
    "03_operations/decision-briefs.md": ("/decision-brief", "Decision briefs"),
    "03_operations/hiring-decision-brief.md": ("/hiring-brief", "Hiring funnel"),
    # 04 — the health page is the surface for all of it.
    "04_data-and-systems/database-queries.md": ("/system", "Table health"),
    "04_data-and-systems/database-connection.md": ("/system", "Connection status"),
    "04_data-and-systems/email-notification.md": ("/system", "Send configuration"),
    "04_data-and-systems/security.md": ("/system", "Credential status"),
    "04_data-and-systems/data-analysis.md": ("/system", "Recent activity"),
    # 05
    "05_talent-sourcing/talent-sourcing.md": ("/sourcing", "The sourcing pool"),
    # 06
    "06_candidate-invites/SKILL.md": ("/invites", "All seven invite types"),
}

#: Deliberately NOT on the server, with the reason. Being explicit stops each
#: of these being rediscovered as a gap every few weeks.
NOT_ON_SERVER: dict[str, str] = {
    "03_operations/meeting-notes-tracker-sheet.md": (
        "Stays in Claude Code by Ayesha's decision: it writes to her own "
        "Google Sheets with her personal OAuth token, which does not go on "
        "the server."
    ),
    "03_operations/hiring-pipeline-weekly-report.md": (
        "Not moved: Ayesha's call that the skill is not completely developed "
        "yet."
    ),
    "01_candidate-communication/05_warm-hold-decision-pending-email.md": (
        "Sent from a Claude Code script. Not one of the five types the webapp "
        "can draft."
    ),
    "01_candidate-communication/06_case-study-update-email.md": (
        "Sent from a Claude Code script. Not one of the five types the webapp "
        "can draft."
    ),
    "01_candidate-communication/07_internal-announcement-email.md": (
        "Sent from a Claude Code script, and its audience is staff rather "
        "than candidates."
    ),
}

_FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
_H1 = re.compile(r"^#\s+(.+?)\s*$", re.M)


def _frontmatter(text: str) -> dict:
    """Parsed frontmatter, or {} — never an exception.

    A bare `word: ` inside an unquoted description is a mapping delimiter and
    silently kills the block (CLAUDE.md Rule 27), and 19 files have no
    frontmatter at all. Either way the caller falls back to a heading.
    """
    match = _FM.match(text)
    if not match or yaml is None:
        return {}
    try:
        data = yaml.safe_load(match.group(1))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _strip_md(value: str) -> str:
    """Plain text for a title or blurb: no emphasis, links kept as their words."""
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value or "")
    value = re.sub(r"[*_`#]+", "", value)
    return " ".join(value.split())


def _prettify_slug(value: str) -> str:
    """'06_candidate-invites' -> 'Candidate invites'.

    Several frontmatter `name:` values are the folder slug rather than a
    human title, and `_strip_md` treats an underscore as emphasis, which
    turned that one into '06candidate-invites'.
    """
    value = re.sub(r"^\d+[_-]", "", value.strip())
    value = value.replace("-", " ").replace("_", " ")
    value = " ".join(value.split())
    return value[:1].upper() + value[1:] if value else value


def _title_of(text: str, fm: dict, filename: str) -> str:
    name = str(fm.get("name") or "").strip()
    if name:
        # A slug-shaped name is a filename, not a title.
        if re.fullmatch(r"[\w-]+", name) and (" " not in name):
            return _prettify_slug(name)
        return _strip_md(name)
    heading = _H1.search(text)
    if heading:
        return _strip_md(heading.group(1))
    stem = os.path.splitext(filename)[0]
    stem = re.sub(r"^\d+[_-]", "", stem).replace("-", " ").replace("_", " ")
    return stem.strip().capitalize() or filename


def _summary_of(text: str, fm: dict) -> str:
    desc = str(fm.get("description") or "").strip()
    if desc:
        return _strip_md(desc)[:400]
    # First real paragraph after the frontmatter and the first heading.
    body = _FM.sub("", text, count=1)
    for block in body.split("\n\n"):
        line = _strip_md(block)
        if len(line) > 40 and not line.startswith(("|", ">", "-")):
            return line[:400]
    return ""


def _skill_label(dirname: str) -> tuple[Optional[str], str]:
    """('01', 'Candidate communication') from '01_candidate-communication'."""
    match = re.match(r"^(\d+)[_-](.+)$", dirname)
    if not match:
        return None, dirname.replace("-", " ").replace("_", " ").strip().capitalize()
    number, rest = match.group(1), match.group(2)
    return number, rest.replace("-", " ").replace("_", " ").strip().capitalize()


def status_for(rel_path: str) -> tuple[str, Optional[str], Optional[str]]:
    """(status, route, note) for one sub-skill file."""
    if rel_path in IMPLEMENTED_BY:
        route, label = IMPLEMENTED_BY[rel_path]
        return WIRED, route, label
    if rel_path in NOT_ON_SERVER:
        return CLAUDE_CODE_ONLY, None, NOT_ON_SERVER[rel_path]
    return REFERENCE, None, None


def discover(root: Optional[str] = None) -> list[dict]:
    """Every skill and sub-skill present on disk, in folder order.

    Returns [] when the directory is absent rather than raising, so a
    misconfigured image degrades to an empty library and the router can say so
    plainly instead of returning a 500.
    """
    base = root or SKILLS_DIR
    if not os.path.isdir(base):
        return []

    skills = []
    for dirname in sorted(os.listdir(base)):
        path = os.path.join(base, dirname)
        if not os.path.isdir(path) or dirname in EXCLUDED_DIRS:
            continue
        number, label = _skill_label(dirname)

        files = []
        for filename in sorted(os.listdir(path)):
            if not filename.lower().endswith(".md"):
                continue
            full = os.path.join(path, filename)
            try:
                text = open(full, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            fm = _frontmatter(text)
            rel = f"{dirname}/{filename}"
            status, route, note = status_for(rel)
            files.append({
                "path": rel,
                "filename": filename,
                "title": _title_of(text, fm, filename),
                "summary": _summary_of(text, fm),
                "is_overview": filename.upper() == "SKILL.MD",
                "status": status,
                "route": route,
                "note": note,
                "words": len(text.split()),
                "has_frontmatter": bool(fm),
            })

        if not files:
            continue
        overview = next((f for f in files if f["is_overview"]), None)
        subs = [f for f in files if not f["is_overview"]]
        skills.append({
            "id": dirname,
            "number": number,
            "label": overview["title"] if overview else label,
            "summary": overview["summary"] if overview else "",
            "sub_skills": subs,
            "overview": overview,
            # Counted over ALL files, overview included. For Skill 06 the
            # overview is where the seven invite types are actually defined,
            # so excluding it reported that skill as 0 wired.
            "counts": {
                "total": len(files),
                "wired": sum(1 for f in files if f["status"] == WIRED),
                "reference": sum(1 for f in files if f["status"] == REFERENCE),
                "claude_code_only": sum(
                    1 for f in files if f["status"] == CLAUDE_CODE_ONLY
                ),
            },
        })
    return skills


def read_file(rel_path: str, root: Optional[str] = None) -> Optional[str]:
    """The body of one sub-skill, or None.

    🔴 `rel_path` comes from a URL, so it is resolved and then checked to be
    INSIDE the skills directory. Without that, `../../.env` is a request for
    the environment file: `.claude/` also holds OAuth tokens, which is the
    whole reason the image excludes it by default.
    """
    base = os.path.realpath(root or SKILLS_DIR)
    target = os.path.realpath(os.path.join(base, rel_path))
    if os.path.commonpath([base, target]) != base:
        return None
    if not target.lower().endswith(".md") or not os.path.isfile(target):
        return None
    try:
        return open(target, encoding="utf-8", errors="replace").read()
    except OSError:
        return None


def summarise(skills: list[dict]) -> dict:
    subs = [f for s in skills for f in s["sub_skills"]]
    subs += [s["overview"] for s in skills if s.get("overview")]
    return {
        "skills": len(skills),
        "sub_skills": len(subs),
        "wired": sum(1 for f in subs if f["status"] == WIRED),
        "reference": sum(1 for f in subs if f["status"] == REFERENCE),
        "claude_code_only": sum(1 for f in subs if f["status"] == CLAUDE_CODE_ONLY),
        "shipped": bool(skills),
    }
