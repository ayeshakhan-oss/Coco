---
name: Active Session Scratchpad
description: Live notes for the current session. Wiped at session start by UserPromptSubmit hook. Summarized into lessons_learned.md by Stop hook.
type: project
---

# Active Session — 2026-07-09

## Task
Web app: fix CV-rejection drafts fabricating interviews; enforce collective "we" voice; lock both in harness + docs. (Also this session: coco-schema DB fix, Gmail-API sending, fit-to-width preview, bulk draft/approve/pilot.)

## Decisions Made
- CV rejection = written application ONLY (Rule 13). Collective "we" voice, never "I" (Rule 12). Both harness HARD BLOCKS.

## Mistakes / Corrections
- **Mistake:** CV-rejection drafts referenced interviews/conversations that never happened ("across multiple conversations and assessments", "what we observed"). CV rejections are application-stage — no interview occurred. Also drafts slipped into first-person "I".
- **Correction:** Added `check_cv_no_interaction` (cv_rejection HARD BLOCK) + `check_first_person_singular` (HARD BLOCK) to the eval harness; CV-stage + we-voice notes to the drafting prompt (`webapp/prompts/tone_rules.py`); Rules 12 + 13 to the tone master file + CLAUDE.md. Commit fb5c672.
- **Rule:** A `cv_rejection` must ground everything in the written application — never reference/imply an interview, call, or conversation (referencing the interview STAGE not reached is fine). Every candidate email uses "we"/"our"/"us", never "I"/"my"/"me". Harness-enforced so the retry loop auto-corrects.

## Files Modified
- scripts/evals/candidate_communication_eval.py, webapp/prompts/tone_rules.py, memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md, CLAUDE.md, memory/MEMORY.md, memory/lesson_cv_rejection_no_interaction_2026_07_09.md

## Pre-Send Checks
- [ ] Self-QA 8-item checklist run
- [ ] Template read side-by-side
- [ ] Word count verified
- [ ] Pilot sent to Ayesha (not candidate directly)
