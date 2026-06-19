---
name: Active Session Scratchpad
description: Live notes for the current session. Wiped at session start by UserPromptSubmit hook. Summarized into lessons_learned.md by Stop hook.
type: project
---

# Active Session — 2026-06-19

## Task
Created a NEW reusable candidate-communication type: the **Keep-in-Touch Note** (invite type #5 under Skill 06). Purpose: after an initial conversation (e.g. exploratory call), when the role/decision is being revisited and we need time, tell the candidate honestly that they are still in our thinking — without promising a timeline or outcome. First use: 5 Job 32 (Fundraising & Partnerships Manager) exploratory-call candidates.

## Decisions Made
- Belongs to Skill 06 (candidate invites), NOT Skill 01 — so the "This is not a yes for now." opener does not apply.
- Name chosen by user: **Keep-in-Touch Note**.
- TWO hard rules for the type: (1) NO booking button / no links; (2) NO promise/commitment (no "we will reach out", no outcome mention).
- For THIS batch only, user asked to add a soft "hopefully in July" hope, and to remove the "we don't know the outcome" line. Applied.
- Subject (user pick): "A Note to Stay Connected — [Name]".
- Recipients (user-named): Falah, Kanooz, Nirmal, Mushahid, Saadia (5 of the 8 invited).

## Mistakes / Corrections
- Initially added the index line only to the auto-memory MEMORY.md; corrected by also adding it to the project repo's memory/MEMORY.md.

## Files Modified
- scripts/send_keep_in_touch_pilot.py (NEW — parameterized CANDIDATES list; pilot loops renders to Ayesha; live sends individual emails)
- .claude/skills/06_candidate-invites/SKILL.md (added type #5 + description)
- memory/keep_in_touch_note_type_2026_06_19.md (NEW — locked spec)
- memory/MEMORY.md (index entry)
- logs/email_audit.log (5 live sends recorded)

## Pre-Send Checks
- [x] Self-QA checklist run
- [x] Template read side-by-side (cloned from send_exploratory_call_pilot.py)
- [x] Pilot sent to Ayesha first (all 5 renders), approved, then live
- [x] Live: 5 individual emails, CC = ayesha + hiring@ + sabeena; verified in audit log
