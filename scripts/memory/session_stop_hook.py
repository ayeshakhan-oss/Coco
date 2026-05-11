"""
Claude Code Stop hook.
Reads session_active.md, extracts Mistakes/Corrections section,
appends structured entries to lessons_learned.md, resets session_active.md header.

Claude Code passes hook data via stdin as JSON. This script reads stdin
but also works standalone for testing.
"""

import sys
import json
from pathlib import Path
from datetime import date

MEMORY_DIR = Path("c:/Agent Coco/memory")
LESSONS_FILE = MEMORY_DIR / "lessons_learned.md"
SESSION_FILE = MEMORY_DIR / "session_active.md"
MAX_ENTRIES = 50


def read_session_mistakes():
    """Extract mistake/correction pairs from session_active.md."""
    if not SESSION_FILE.exists():
        return []

    content = SESSION_FILE.read_text(encoding="utf-8")

    # Find the Mistakes / Corrections section
    if "## Mistakes / Corrections" not in content:
        return []

    section = content.split("## Mistakes / Corrections")[1]
    if "##" in section:
        section = section.split("##")[0]

    entries = []
    for line in section.strip().splitlines():
        line = line.strip()
        if line.startswith("- ") and "Mistake:" in line and "Correction:" in line:
            parts = line[2:].split(". Correction:")
            if len(parts) == 2:
                mistake = parts[0].replace("Mistake:", "").strip()
                correction = parts[1].strip()
                entries.append({"mistake": mistake, "correction": correction})
    return entries


def append_to_lessons(entries, task_type="General"):
    """Append new entries to lessons_learned.md."""
    if not entries:
        return

    today = date.today().strftime("%Y-%m-%d")
    new_block = f"\n## {today} — {task_type}\n"
    for e in entries:
        new_block += f"- **Mistake:** {e['mistake']}\n"
        new_block += f"- **Correction:** {e['correction']}\n"
        new_block += f"- **Rule:** [Coco: add rule summary here]\n\n"

    content = LESSONS_FILE.read_text(encoding="utf-8")
    # Insert after the header block, before "## Archived Rules"
    if "## Archived Rules" in content:
        content = content.replace("## Archived Rules", new_block + "## Archived Rules")
    else:
        content += new_block

    LESSONS_FILE.write_text(content, encoding="utf-8")
    print(f"[memory] Appended {len(entries)} lesson entries for {today}")


def reset_session_scratchpad():
    """Wipe session_active.md and reset with today's date header."""
    today = date.today().strftime("%Y-%m-%d")
    template = f"""---
name: Active Session Scratchpad
description: Live notes for the current session. Wiped at session start by UserPromptSubmit hook. Summarized into lessons_learned.md by Stop hook.
type: project
---

# Active Session — {today}

## Task
[What Coco is working on this session]

## Decisions Made

## Mistakes / Corrections

## Files Modified

## Pre-Send Checks
- [ ] Self-QA 8-item checklist run
- [ ] Template read side-by-side
- [ ] Word count verified
- [ ] Pilot sent to Ayesha (not candidate directly)
"""
    SESSION_FILE.write_text(template, encoding="utf-8")
    print(f"[memory] Reset session_active.md for {today}")


def main():
    # Read stdin hook data (may be empty if run standalone)
    try:
        hook_data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    except Exception:
        hook_data = {}

    task_type = hook_data.get("task_type", "General")

    mistakes = read_session_mistakes()
    if mistakes:
        append_to_lessons(mistakes, task_type)
    else:
        print("[memory] No mistakes/corrections found in session scratchpad")

    reset_session_scratchpad()


if __name__ == "__main__":
    main()
