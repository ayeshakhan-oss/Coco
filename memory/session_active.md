---
name: Active Session Scratchpad
description: Live notes for the current session. Wiped at session start by UserPromptSubmit hook. Summarized into lessons_learned.md by Stop hook.
type: project
---

# Active Session — 2026-05-15

## Task
Lock exploratory call invite approach + comprehensive template/tone index for ALL email types (2026-05-15)

## Decisions Made
1. Created locked_exploratory_call_invite_approach.md with design spec + body text + links + workflow locked
2. Updated locked_templates_index.md to be comprehensive single source of truth for ALL email types
3. Confirmed all 4 interview invites (values, exploratory, case study, warm bench) use universal locked template
4. Confirmed tone rule applies to ALL feedback/rejection emails (values, warm bench, GWC, screening)
5. All templates + tones now in MEMORY.md index + GitHub with hyperlinks

## Mistakes / Corrections
None — workflow clean from pilot → approval → live send

## Files Modified
- scripts/send_exploratory_call_batch_live.py (added allow_candidate_addresses() call)
- memory/locked_exploratory_call_invite_approach.md (created)
- memory/locked_templates_index.md (comprehensive update)
- memory/MEMORY.md (added references)
- .claude/skills/06_candidate-invites/SKILL.md (verified locked design for all 4 types)

## Pre-Send Checks
- [x] Self-QA 8-item checklist run (4/4 candidates sent live)
- [x] Template read side-by-side (universal template verified for all types)
- [x] Word count verified (body text locked)
- [x] Pilot sent to Ayesha (batch_pilot.py) → approved → live sent
