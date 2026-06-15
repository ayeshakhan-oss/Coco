# UI/UX Pro Max Skill — Install Notes (2026-06-15)

**Status:** ✅ Installed & verified. Vendored **local-only** (gitignored) — NOT in the repo.

## What it is
`ui-ux-pro-max` (NextLevelBuilder, MIT, v2.5.0) — design-intelligence skill: 67 UI
styles, 96 color palettes, 57 font pairings, 99 UX guidelines, 25 chart types
across 13 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter,
Tailwind, shadcn/ui, …). Backed by a local CSV search engine (no network calls).
Auto-triggers on UI/UX/web work ("design a landing page", "build a dashboard").

Installed at `.claude/skills/ui-ux-pro-max/`.

## Why it's gitignored (local-only)
It ships a `data/` directory and hyphenated/`.json` files that collide with the
project's protective `.gitignore` rules (`data/` at line 35, `*-*.json` at line 13),
so committing it would silently break the skill. Ignore rule added to `.gitignore`:
`.claude/skills/ui-ux-pro-max/`.

## Reinstall (fresh clone / new machine)
```
cd "c:\Agent Coco"
npx uipro-cli init --ai claude
```

## 🔴 CRITICAL — re-apply Windows patch after every reinstall/update
The shipped `SKILL.md` hardcodes `python3 skills/ui-ux-pro-max/scripts/search.py`.
On our Windows machine `python3` does NOT exist (only `python`, 3.14.x) AND the path
must be `.claude/skills/...` from the project root. `npx uipro-cli init` / `uipro update`
overwrites `SKILL.md`, wiping the fix — so after every reinstall, replace:
`python3 skills/ui-ux-pro-max/scripts/search.py` → `python .claude/skills/ui-ux-pro-max/scripts/search.py`
in `SKILL.md`. (The `#!/usr/bin/env python3` shebangs are harmless — leave them.)

## Guard rule
The locked **v8 candidate-comms layout** and **Skill 06 interview-invite design**
OVERRIDE this skill — see [CLAUDE.md](../CLAUDE.md) Rule 9. Never apply
`ui-ux-pro-max` suggestions to candidate emails. See
[v8_candidate_comms_layout_LOCKED.md](v8_candidate_comms_layout_LOCKED.md).
