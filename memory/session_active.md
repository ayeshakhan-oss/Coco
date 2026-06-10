---
name: Active Session Scratchpad
description: Live notes for the current session. Wiped at session start by UserPromptSubmit hook. Summarized into lessons_learned.md by Stop hook.
type: project
---

# Active Session — 2026-06-10

## Task
1. Drafted + piloted values feedback email for Syeda Siddiqa Fatima (CPD Coach, Job 17, app 308, cand 266). Pilot sent to Ayesha only. Awaiting go-live.
2. Ayesha: make this email's layout the standard for ALL candidate communication (+ future types).
3. "Update the layout in the harness" + save to memory/MEMORY.md/CLAUDE.md + update skills + push to GitHub.

## Decisions Made
- Created scripts/utils/v8_template.py = single shared layout module (H/SUB/P/PS/FOOTER/wrap/attach_logo/EYEBROW). Byte-identical to approved Syeda email.
- Layout vs content separation: module owns layout; section headings/content stay per-type and harness-enforced.
- Resolved template conflict: the 2026-05-13 "ALL candidate comms" template was actually the Skill 06 INVITE template over-claiming scope. Narrowed it to invites only (preserved Skill 06); feedback/rejection -> v8.
- Updated the harness both ways: (a) regenerated the 4 Layer-1 draft-time templates from v8 via new generator scripts/utils/gen_locked_templates.py (they were an older non-v8 layout); (b) added check_v8_layout() WARNING to send-time eval. Verified v8 email passes 0 violations; non-v8 triggers warning.

## Mistakes / Corrections
(none)

## Files Modified
- scripts/utils/v8_template.py (new — shared layout module)
- scripts/utils/gen_locked_templates.py (new — regenerates harness templates from v8)
- templates/{cv_rejection,values_feedback,warm_bench,gwc_rejection}_template_locked.html (regenerated to v8)
- scripts/evals/candidate_communication_eval.py (added v8 layout WARNING check)
- scripts/send_cpd_coach_values_feedback_syeda_2026_06_10_pilot.py (imports module)
- memory/v8_candidate_comms_layout_LOCKED.md (new + harness section)
- memory/MEMORY.md (pointer + narrowed old-template entry)
- memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md (Format block layout line)
- memory/locked_email_template_interview_invites_FINAL_2026_05_13.md (scope narrowed to invites)
- memory/locked_templates_index.md (feedback/rejection design pointers -> v8)
- CLAUDE.md (Core Rule 8 — v8 layout)
- .claude/skills/01_candidate-communication/{candidate-rejections,values-feedback-emails,warm-bench-feedback-email,gwc-rejection-emails}.md (LOCKED LAYOUT line)

## Pre-Send Checks
- [x] Self-QA checklist run (eval: PASS, 1000 words, 0 violations)
- [x] Template read side-by-side (job36 v8 reference)
- [x] Word count verified (1000)
- [x] Pilot sent to Ayesha only

## Push
- Pending: git commit + push to GitHub (this turn).
