"""The skill library: every skill and sub-skill the image actually carries.

Read-only. `webapp/services/skills.py` walks the shipped `.claude/skills/`
directory, so this router reports what is in the running image rather than
what the repo happens to contain.

🔴 THE POINT OF SERVING THIS. Before 2026-09-25 the image copied two skill
   folders out of seven, so 29 sub-skill files did not exist on Railway while
   the module tiles all read "live". This endpoint makes the difference
   visible: if a folder stops shipping, the library shows it missing instead
   of showing nothing.

🔴 STATUS PER FILE IS NOT DECORATION. `wired` means a page in this app
   implements that sub-skill, and carries the route. `reference` means the app
   serves the guidance but does not execute it. `claude_code_only` means it is
   deliberately not on the server, with the reason. Marking all of them live
   would repeat the overclaim in a new place.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..deps import get_current_user
from ..services import skills as svc

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("")
def list_skills(user: dict = Depends(get_current_user)):
    """Every skill, its sub-skills, and what each one is wired to."""
    found = svc.discover()
    summary = svc.summarise(found)
    return {
        "summary": summary,
        "skills": found,
        # Said out loud rather than left as an empty list, because "no skills"
        # and "the skills directory did not ship" look identical otherwise and
        # the second one is a deployment fault.
        "error": None if found else (
            "No skill files are present in this build. The image did not copy "
            ".claude/skills/, so the method behind every module is missing "
            "from the server."
        ),
    }


@router.get("/file")
def read_skill_file(path: str, user: dict = Depends(get_current_user)):
    """The markdown body of one sub-skill.

    `path` is the registry's own `path` value, e.g.
    `03_operations/attendance-reports.md`. The service resolves it and refuses
    anything outside the skills directory: `.claude/` also holds OAuth tokens,
    so a traversal here would be a credential read.
    """
    body = svc.read_file(path)
    if body is None:
        raise HTTPException(404, "No such skill file in this build.")
    return {"path": path, "body": body, "words": len(body.split())}
