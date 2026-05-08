# Agent Memory Management System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reliable, tiered memory management system for Agent Coco with automated hooks, lessons-learned tracking, and a unified memory architecture so the agent's context is always rich, concise, and accurate across sessions.

**Architecture:** Three-tier memory (active/session → curated/project → archive/history) synced by hooks. A `Stop` hook summarizes each session into `lessons_learned.md`. A `UserPromptSubmit` hook injects the most relevant memory sections into every new conversation. Memory files stay under token budgets via append-then-prune rules.

**Tech Stack:** Python 3, Claude Code hooks (settings.json), Markdown files, JSON structured logs, existing `C:\Agent Coco\memory\` directory structure.

---

## Current State Analysis (Critical Gaps)

1. **Split memory** — `C:\Agent Coco\memory\` (curated, 16 files) vs `C:\Users\Dell\.claude\projects\c--Agent-Coco\memory\` (historical, 64 files). No sync. CLAUDE.md points to curated; context injection reads historical.
2. **No hooks** — `.claude/settings.json` has zero hooks. All memory updates are manual.
3. **Stale session.md** — hasn't been updated since Apr 14; SESSIONS.md is current but separate.
4. **Pre-consolidation duplicates** — `general_non_negotiable_sops.md` and `execution_discipline_protocol.md` still exist alongside their consolidated replacement `CORE_DISCIPLINE.md`.
5. **Critical warm bench files missing from curated location** — referenced in CLAUDE.md but only exist in historical location.
6. **No lessons-learned file** — lessons are scattered across ad-hoc files; no structured, searchable log.

---

## File Structure

### New files to create:
- `C:\Agent Coco\memory\lessons_learned.md` — Structured append-only log: date + task + mistake + rule-learned
- `C:\Agent Coco\memory\session_active.md` — Current session scratchpad (wiped and re-created each session)
- `C:\Agent Coco\scripts\memory\session_stop_hook.py` — Stop hook: summarizes session into lessons_learned.md, updates MEMORY.md index
- `C:\Agent Coco\scripts\memory\prompt_submit_hook.py` — UserPromptSubmit hook: injects top-N relevant memory sections based on keywords
- `C:\Agent Coco\scripts\memory\memory_sync.py` — One-time sync: copies missing files from historical → curated, deduplicates

### Files to modify:
- `C:\Agent Coco\.claude\settings.json` — Add Stop + UserPromptSubmit hooks
- `C:\Agent Coco\memory\MEMORY.md` — Add entry for lessons_learned.md; remove stale entries
- `C:\Agent Coco\CLAUDE.md` — Update memory section to reference new system; remove duplicate file references

### Files to delete after sync:
- `C:\Agent Coco\memory\general_non_negotiable_sops.md` (superseded by CORE_DISCIPLINE.md)
- `C:\Agent Coco\memory\execution_discipline_protocol.md` (superseded by CORE_DISCIPLINE.md)

---

## Task 1: Sync the Two Memory Locations

**Goal:** Merge historical location into curated location so there is ONE source of truth at `C:\Agent Coco\memory\`.

**Files:**
- Create: `C:\Agent Coco\scripts\memory\memory_sync.py`

- [ ] **Step 1: Write the sync script**

```python
# scripts/memory/memory_sync.py
"""One-time sync: copies files from historical memory location to curated location.
Skips files that already exist. Prints a report of what was copied vs skipped."""

from pathlib import Path
import shutil

HISTORICAL = Path.home() / ".claude" / "projects" / "C--Agent-Coco" / "memory"
CURATED = Path("C:/Agent Coco/memory")

def sync():
    if not HISTORICAL.exists():
        print(f"Historical path not found: {HISTORICAL}")
        return

    copied = []
    skipped = []

    for src in sorted(HISTORICAL.glob("*.md")):
        dst = CURATED / src.name
        if dst.exists():
            skipped.append(src.name)
        else:
            shutil.copy2(src, dst)
            copied.append(src.name)

    print(f"\nCopied ({len(copied)} files):")
    for f in copied:
        print(f"  + {f}")
    print(f"\nSkipped ({len(skipped)} files — already exist in curated):")
    for f in skipped:
        print(f"  ~ {f}")

if __name__ == "__main__":
    sync()
```

- [ ] **Step 2: Run the sync**

```bash
cd "C:\Agent Coco"
python scripts/memory/memory_sync.py
```

Expected output: list of copied files (warm_bench files, attendance variants, etc.) and skipped files.

- [ ] **Step 3: Verify warm bench files now in curated location**

```bash
ls "C:\Agent Coco\memory\warm_bench*"
```

Expected: `warm_bench_final_locked_approach.md` and `warm_bench_session_may5_2026_complete_learnings.md` present.

- [ ] **Step 4: Delete pre-consolidation duplicates**

```bash
rm "C:\Agent Coco\memory\general_non_negotiable_sops.md"
rm "C:\Agent Coco\memory\execution_discipline_protocol.md"
```

- [ ] **Step 5: Commit**

```bash
git -C "C:\Agent Coco" add memory/ scripts/memory/memory_sync.py
git -C "C:\Agent Coco" commit -m "feat: sync memory locations, remove pre-consolidation duplicates"
```

---

## Task 2: Create the Lessons-Learned Log

**Goal:** A structured, searchable file that accumulates rules learned from mistakes across all sessions.

**Files:**
- Create: `C:\Agent Coco\memory\lessons_learned.md`

- [ ] **Step 1: Create the file with seed entries from existing knowledge**

```markdown
---
name: Lessons Learned Log
description: Structured append-only log of mistakes, corrections, and rules. Updated by Stop hook after each session.
type: project
max_entries: 50
---

# Lessons Learned — Agent Coco

> **Format:** `## YYYY-MM-DD — [Task Type]` then bullets: Mistake, Correction, Rule.
> **Limit:** 50 entries max. When exceeded, summarize oldest 25 into "Archived Rules" section below.

## 2026-04-14 — CV Screening
- **Mistake:** Fabricated candidate details not present in CV
- **Correction:** Halted, re-read CV, corrected report
- **Rule:** No claim about a candidate goes in the report without a direct quote or line from their CV

## 2026-04-15 — Teams API Query
- **Mistake:** Teams query returned 1 message; assumed "no data" and missed 2 leave announcements (Haya Abid, Sabeen Fatima)
- **Correction:** Cross-checked with Ayesha who confirmed the leaves
- **Rule:** Suspiciously small result sets (< 5 items from a team channel) must be verified with a second source before reporting

## 2026-04-20 — Attendance Report
- **Mistake:** Skipped reading attendance template memory; generated report with grid borders, wrong colors, wrong stat count
- **Correction:** Re-read `attendance_report_complete_template.md`, regenerated from scratch
- **Rule:** Read the locked template memory file BEFORE writing any code for attendance reports

## 2026-05-05 — Warm Bench Emails
- **Mistake:** Mahnoor's email deviated from locked template (word count, signature format)
- **Correction:** Re-ran against `warm_bench_final_locked_approach.md` side-by-side
- **Rule:** Print the locked template next to the draft before sending; never send from memory alone

---

## Archived Rules
<!-- Condensed from entries older than 60 days -->
- Never use cv_text[:4500] — minimum 10k chars for CV truncation (2026-04-08)
- Every name in every decision brief section must have a Drive CV hyperlink (2026-04-08)
- Replying in-thread requires In-Reply-To + References headers (2026-04-08)
- status='offer' in DB is a pipeline stage, NOT a sent offer — never assert (2026-04-08)
- ALL ReportLab PDFs must use TA_JUSTIFY on body paragraph styles (2026-04-03)
```

- [ ] **Step 2: Add entry to MEMORY.md index**

Open `C:\Agent Coco\memory\MEMORY.md` and add under the main index:

```markdown
- [Lessons Learned Log](lessons_learned.md) — Structured append-only log: date, task, mistake, correction, rule. Updated by Stop hook. Max 50 entries.
```

- [ ] **Step 3: Commit**

```bash
git -C "C:\Agent Coco" add memory/lessons_learned.md memory/MEMORY.md
git -C "C:\Agent Coco" commit -m "feat: add structured lessons_learned.md with seed entries"
```

---

## Task 3: Create the Session Active Scratchpad

**Goal:** A live scratchpad that Coco writes to during a session. Wiped at session start, summarized at session end.

**Files:**
- Create: `C:\Agent Coco\memory\session_active.md`

- [ ] **Step 1: Create session_active.md template**

```markdown
---
name: Active Session Scratchpad
description: Live notes for the current session. Wiped at session start by UserPromptSubmit hook. Summarized into lessons_learned.md by Stop hook.
type: project
---

# Active Session — [DATE]

## Task
[What Coco is working on this session]

## Decisions Made
<!-- Append as you work: "Chose X over Y because Z" -->

## Mistakes / Corrections
<!-- Append when a correction happens: "Mistake: X. Correction: Y." -->

## Files Modified
<!-- List every file touched: path + reason -->

## Pre-Send Checks
<!-- Check off before any email send -->
- [ ] Self-QA 8-item checklist run
- [ ] Template read side-by-side
- [ ] Word count verified
- [ ] Pilot sent to Ayesha (not candidate directly)
```

- [ ] **Step 2: Add to MEMORY.md index**

```markdown
- [Active Session Scratchpad](session_active.md) — Live notes for current session: task, decisions, mistakes, files modified. Wiped at session start.
```

- [ ] **Step 3: Commit**

```bash
git -C "C:\Agent Coco" add memory/session_active.md memory/MEMORY.md
git -C "C:\Agent Coco" commit -m "feat: add session_active.md scratchpad template"
```

---

## Task 4: Build the Stop Hook (Session Summarizer)

**Goal:** When Claude Code finishes a session, auto-summarize into lessons_learned.md and update session_active.md header with date.

**Files:**
- Create: `C:\Agent Coco\scripts\memory\session_stop_hook.py`

- [ ] **Step 1: Write the Stop hook script**

```python
# scripts/memory/session_stop_hook.py
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

MEMORY_DIR = Path("C:/Agent Coco/memory")
LESSONS_FILE = MEMORY_DIR / "lessons_learned.md"
SESSION_FILE = MEMORY_DIR / "session_active.md"
MAX_ENTRIES = 50


def read_session_mistakes() -> list[dict]:
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


def append_to_lessons(entries: list[dict], task_type: str = "General"):
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
```

- [ ] **Step 2: Test standalone**

```bash
cd "C:\Agent Coco"
python scripts/memory/session_stop_hook.py
```

Expected: `[memory] No mistakes/corrections found in session scratchpad` and `[memory] Reset session_active.md for 2026-05-08`

- [ ] **Step 3: Test with mock data** — manually add a mistake to session_active.md then re-run

Edit `C:\Agent Coco\memory\session_active.md` Mistakes section:
```
- Mistake: Used wrong template. Correction: Re-read locked template file before regenerating.
```

Then:
```bash
python scripts/memory/session_stop_hook.py
```

Expected: `[memory] Appended 1 lesson entries for 2026-05-08`

Verify `lessons_learned.md` has the new entry.

- [ ] **Step 4: Commit**

```bash
git -C "C:\Agent Coco" add scripts/memory/session_stop_hook.py
git -C "C:\Agent Coco" commit -m "feat: add Stop hook script to summarize session into lessons_learned.md"
```

---

## Task 5: Build the UserPromptSubmit Hook (Context Injector)

**Goal:** At the start of every new prompt, inject the 3-5 most relevant memory files based on keywords in the user's message.

**Files:**
- Create: `C:\Agent Coco\scripts\memory\prompt_submit_hook.py`

- [ ] **Step 1: Write the hook script**

```python
# scripts/memory/prompt_submit_hook.py
"""
Claude Code UserPromptSubmit hook.
Reads the user's prompt from stdin (JSON), detects keywords,
and injects relevant memory file contents into the context
by printing to stdout (Claude Code reads this as additional context).

Keyword → memory file mapping is defined in KEYWORD_MAP below.
"""

import sys
import json
from pathlib import Path

MEMORY_DIR = Path("C:/Agent Coco/memory")

# Keyword patterns → memory files to inject (in priority order)
KEYWORD_MAP = [
    (["warm bench", "warmbenck", "jra", "haroon"], [
        "warm_bench_final_locked_approach.md",
        "warm_bench_session_may5_2026_complete_learnings.md",
    ]),
    (["cv", "screen", "screening", "candidate", "resume"], [
        "skill_cv_screening_sop.md",
    ]),
    (["rejection", "reject", "feedback email"], [
        "skill_values_feedback_emails_sop.md",
    ]),
    (["attendance", "onsite", "wfh", "leave"], [
        "attendance_report_complete_template.md",
    ]),
    (["decision brief", "brief", "hiring decision"], [
        "project_job36_decision_brief.md",
        "project_job32_decision_brief_format.md",
    ]),
    (["interview", "invite", "calendar"], [
        "locked_email_template_interview_invites.md",
    ]),
    (["talent", "source", "sourcing", "linkedin"], [
        "coco_talent_sourcing_skill.md",
    ]),
    (["lesson", "mistake", "error", "wrong"], [
        "lessons_learned.md",
    ]),
]

# Files always injected (small, critical)
ALWAYS_INJECT = [
    "session_active.md",
]

MAX_FILE_CHARS = 3000  # Truncate long files to stay within context budget


def detect_relevant_files(prompt: str) -> list[str]:
    prompt_lower = prompt.lower()
    files = list(ALWAYS_INJECT)

    for keywords, memory_files in KEYWORD_MAP:
        if any(kw in prompt_lower for kw in keywords):
            for f in memory_files:
                if f not in files:
                    files.append(f)

    return files


def inject_memory(files: list[str]) -> str:
    """Read and concatenate memory files. Return formatted injection block."""
    blocks = []
    for filename in files:
        path = MEMORY_DIR / filename
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if len(content) > MAX_FILE_CHARS:
            content = content[:MAX_FILE_CHARS] + "\n\n[...truncated for context budget...]"
        blocks.append(f"<!-- MEMORY: {filename} -->\n{content}\n<!-- END MEMORY: {filename} -->")

    if not blocks:
        return ""

    return "\n\n".join(blocks)


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}

    prompt = data.get("prompt", "")
    if not prompt:
        return  # No prompt, nothing to inject

    relevant_files = detect_relevant_files(prompt)
    injection = inject_memory(relevant_files)

    if injection:
        # Claude Code reads stdout of UserPromptSubmit hook as additional context
        print(injection)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test standalone**

```bash
cd "C:\Agent Coco"
echo '{"prompt": "send warm bench feedback email to Mahnoor"}' | python scripts/memory/prompt_submit_hook.py
```

Expected: prints content blocks from `session_active.md`, `warm_bench_final_locked_approach.md`, `warm_bench_session_may5_2026_complete_learnings.md`

- [ ] **Step 3: Test with CV screening prompt**

```bash
echo '{"prompt": "screen these CVs for job 32"}' | python scripts/memory/prompt_submit_hook.py
```

Expected: prints `session_active.md` + `skill_cv_screening_sop.md` content.

- [ ] **Step 4: Commit**

```bash
git -C "C:\Agent Coco" add scripts/memory/prompt_submit_hook.py
git -C "C:\Agent Coco" commit -m "feat: add UserPromptSubmit hook for keyword-based memory injection"
```

---

## Task 6: Wire Up Hooks in settings.json

**Goal:** Register both hooks in `.claude/settings.json` so Claude Code triggers them automatically.

**Files:**
- Modify: `C:\Agent Coco\.claude\settings.json`

- [ ] **Step 1: Read current settings.json**

Current content (from exploration):
```json
{
  "enabledPlugins": ["superpowers", "context7", "skill-creator"]
}
```

- [ ] **Step 2: Add hooks configuration**

Replace with:
```json
{
  "enabledPlugins": ["superpowers", "context7", "skill-creator"],
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python \"C:/Agent Coco/scripts/memory/session_stop_hook.py\""
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python \"C:/Agent Coco/scripts/memory/prompt_submit_hook.py\""
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 3: Verify JSON is valid**

```bash
python -c "import json; json.load(open('C:/Agent Coco/.claude/settings.json'))"
```

Expected: no output (valid JSON).

- [ ] **Step 4: Commit**

```bash
git -C "C:\Agent Coco" add .claude/settings.json
git -C "C:\Agent Coco" commit -m "feat: register Stop + UserPromptSubmit memory hooks in settings.json"
```

---

## Task 7: Update CLAUDE.md to Reflect New System

**Goal:** CLAUDE.md should point to the new memory architecture so Coco knows to use it from the first line.

**Files:**
- Modify: `C:\Agent Coco\CLAUDE.md`

- [ ] **Step 1: Add memory architecture note to CLAUDE.md**

In the "Before You Do Anything" section, add after the current 4-item checklist:

```markdown
5. **[lessons_learned.md](memory/lessons_learned.md)** — Structured log of past mistakes + rules. Read if task type matches a past failure.
6. **[session_active.md](memory/session_active.md)** — Live scratchpad: write decisions, mistakes, files touched. Stop hook summarizes this.
```

Also update the "Memory System" note (or add one) explaining:
```markdown
## 🧠 Memory System (Three Tiers)

| Tier | File | Purpose | Updated by |
|------|------|---------|------------|
| Active | memory/session_active.md | Current session notes | Coco during work |
| Curated | memory/MEMORY.md + *.md | Project knowledge | Coco after sessions |
| History | memory/lessons_learned.md | Mistake→rule log | Stop hook automatically |

**Hooks active:** UserPromptSubmit injects relevant memory files automatically. Stop hook summarizes session into lessons_learned.md.
```

- [ ] **Step 2: Commit**

```bash
git -C "C:\Agent Coco" add CLAUDE.md
git -C "C:\Agent Coco" commit -m "docs: update CLAUDE.md with three-tier memory system documentation"
```

---

## Verification

End-to-end test sequence:

1. **Open a new Claude Code session** in `C:\Agent Coco`
2. **Type:** `"I need to send a warm bench feedback email"`
3. **Verify:** UserPromptSubmit hook fires and warm bench memory files appear in context (look for `<!-- MEMORY: warm_bench_final_locked_approach.md -->` in the injected context)
4. **During session:** Write a mock mistake to `session_active.md` in the Mistakes section
5. **End the session** (type `/exit` or close)
6. **Verify:** Stop hook fires and new entry appears in `lessons_learned.md` with today's date
7. **Check `session_active.md`** — should be reset to blank template for next session

---

## Key Files Reference

| File | Path | Role |
|------|------|------|
| Lessons Learned | `C:\Agent Coco\memory\lessons_learned.md` | Structured mistake→rule log |
| Session Scratchpad | `C:\Agent Coco\memory\session_active.md` | Live per-session notes |
| Stop Hook | `C:\Agent Coco\scripts\memory\session_stop_hook.py` | End-of-session summarizer |
| Prompt Hook | `C:\Agent Coco\scripts\memory\prompt_submit_hook.py` | Context injector |
| Settings | `C:\Agent Coco\.claude\settings.json` | Hook registration |
| Memory Sync | `C:\Agent Coco\scripts\memory\memory_sync.py` | One-time historical sync |
