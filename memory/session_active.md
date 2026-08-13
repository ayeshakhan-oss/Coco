---
name: Active Session Scratchpad
description: Live notes for the current session. Wiped at session start by UserPromptSubmit hook. Summarized into lessons_learned.md by Stop hook.
type: project
---

# Active Session — 2026-08-13

## Task
Values scorecards for Syed Basit Hussain (Job 42 SMG) and Marzia Hasnain (Job 41 GM-Karachi), both PASS 5+/1±/0−, both submitted to Markaz after Ayesha's approval. Then a Job-42 audit: values-passers vs case studies sent, and hunting missed values scorecards.

## Decisions Made
- Basit had no Markaz record (one of the 5 sourced values-invitees invisible to Markaz) → Ayesha approved creating candidate 3350 + application 4142 retroactively with his CV PDF uploaded, then filling the scorecard.
- Marzia: Markaz spelling is "Marzia" (Ayesha confirmed) though Fathom transcript says "Merzia" — used the Markaz spelling in the scorecard.
- Both submitted with proceedToRightSeat "Yes" but GWC probes written into finalComments (Basit: Gets-it/Wants-it; Marzia: all three, B2G capacity untested).
- Audit used all three sources (Markaz + logs/email_audit.log + read-only IMAP into Ayesha's mailbox) rather than Markaz alone.

## Mistakes / Corrections
- **MISTAKE:** In the first audit report I listed Ali Ahmed as "interviewed Tue 11 Aug, unscored" purely because a calendar booking existed. Ayesha then asked me to check her email, which showed **he cancelled his own appointment 43 minutes before the slot** — no interview ever happened, so no scorecard was missed. **RULE: a calendar booking is NOT evidence an interview happened; always check for cancellations before asserting an interview took place.**
- **MISTAKE (tooling):** my first cancellation sweep used Gmail IMAP `SUBJECT "cancel"` and returned 0 hits even though "Appointment canceled: ..." mails existed — Gmail IMAP does not stem-match. **RULE: search `"canceled"` AND `"cancelled"` as exact words.**
- Hina Rehman left genuinely ambiguous rather than asserted either way: booking never cancelled and the invite was re-sent with a notetaker 10 min into the slot, but no candidate-named Fathom recap exists (all other scored candidates have one). Flagged for Ayesha to confirm instead of guessing.

## Files Modified
- scripts/jobs/job42/add_syed_basit_and_submit_scorecard.py (new)
- scripts/jobs/job41/submit_marzia_hasnain_values_scorecard.py (new)
- memory/values_scorecard_syed_basit_smg_2026_08_13.md (new)
- memory/values_scorecard_marzia_hasnain_gm_karachi_2026_08_13.md (new)
- memory/audit_job42_smg_scorecards_vs_case_studies_2026_08_13.md (new)
- MEMORY.md index (compacted; new entries added)
- Commits b428236, a56abb6 pushed to main

## Pre-Send Checks
- [x] Self-QA run on both scorecards (schema exact, 6 values, all 3 evidence columns, PASS/OUT logic verified)
- [x] Locked layout shown in chat in full before any DB write
- [x] Guarded writes (duplicate checks, no-overwrite guard, row-count asserts)
- [x] Ayesha's explicit approval before each Markaz write
- [ ] No candidate emails sent this session
