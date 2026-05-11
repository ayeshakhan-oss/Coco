---
name: Discipline Enforcement Lockdown
description: Non-negotiable pre-task protocol to prevent memory skip, template drift, and fabrication
type: feedback
originSessionId: d4a807e5-380e-4bc6-ac7a-c252d64a81bd
---
# DISCIPLINE ENFORCEMENT LOCKDOWN
**Set: 2026-04-25** | **Severity: CRITICAL** | **Violation: Immediate stop + user notification**

---

## RULE 1: MEMORY-FIRST DISCIPLINE
**Before starting ANY task:** Memory check is STEP 1, not optional.
- [ ] Read [MEMORY.md](MEMORY.md) index
- [ ] Search for existing SOP/template for this task type
- [ ] Read the relevant memory file(s) — do NOT skip
- [ ] If memory exists for this exact task (by position/job/type), use it as the baseline

**Why:** Template drift, fabrication, and duplicated work happened because I skipped memory and rewrote from scratch (values feedback, attendance reports). Same day lock-in was forgotten by next task.

**How to apply:** If starting CV screening, rejection emails, attendance reports, decision briefs, or case study evals — search memory FIRST. If file exists, read it before writing anything. Non-negotiable.

**Violation consequence:** Stop immediately and re-read memory before continuing.

---

## RULE 2: VERIFICATION BEFORE SENDING
**Never assume.** Verify against ground truth before reporting/sending anything.
- [ ] For attendance: Verify Teams announcements against calendar, Gmail, Markaz directly
- [ ] For CV screening: Verify candidate names exist in system before including
- [ ] For email: Verify recipient addresses in approved list (Taleemabad or pipeline)
- [ ] For reports: Verify data totals match source (payroll count = OPL+OWT, not sum)
- [ ] For any external API result: Flag if result seems incomplete (small dataset = red flag)

**Why:** Fabrication of attendance data, missed Teams announcements (Haya Abid, Sabeen Fatima), payroll count errors happened because I assumed instead of checking ground truth.

**How to apply:** Before writing final output, always cross-check at least 2 sources. Never send on first-pass.

**Violation consequence:** Pause work, verify with user or source, then continue.

---

## RULE 3: LOCKED TEMPLATES — KEEP IN VIEW
**Once a format is locked, it stays locked.** No drift.
- [ ] Before starting task: Open [LOCKED_TEMPLATES_INDEX.md](locked_templates_index.md)
- [ ] Keep this file visible while working
- [ ] If you find yourself rewriting a template, you've violated this rule
- [ ] Reference the exact template file — do not rewrite

**Why:** Values feedback, attendance reports, and decision briefs drifted in format because I didn't reference the locked template while working. By next task, forgot the lock-in completely.

**How to apply:** Pin the templates index. If you finish a task and mark it done in the next session, re-read the locked template FIRST.

**Violation consequence:** Revert to the locked version, do not send custom variation.

---

## RULE 4: SINGLE-PASS CORRECTNESS
**Fast ≠ correct.** Never trade accuracy for speed.
- [ ] Self-QA checklist before sending (8 items, in Execution Discipline Protocol)
- [ ] If you skip QA because "this seems straightforward," you will introduce errors
- [ ] Pressure to move fast → fabrication. Every time.

**Why:** Attendance PDF color mismatches, grid borders, payload totals — all from speed-over-accuracy.

**How to apply:** Always run the 8-item self-QA. Always.

**Violation consequence:** User reviews and rejects. Do it right first time.

---

## RULE 5: NO DELEGATION BACK TO USER
**Own the execution end-to-end.** Never ask clarifying questions instead of searching memory.
- If unsure about format: Search memory for that task type
- If unsure about data: Query the source (Gmail, Markaz, Calendar)
- If unsure about decision: Check CLAUDE.md for that position/task
- Only ask user if memory + sources genuinely conflict or are missing

**Why:** Asked for clarification on attendance format even though it was locked in memory. User had to repeat.

**How to apply:** Check memory FIRST. If not there, query source. Only ask as last resort.

**Violation consequence:** Waste of user time. Not acceptable.

---

## ENFORCEMENT

**THIS IS NON-NEGOTIABLE.** Violations stop work immediately:
1. Memory skip before task → STOP, read memory first
2. Assumption without verification → STOP, verify against ground truth
3. Template rewrite instead of reference → STOP, use locked template
4. Skip self-QA before sending → STOP, run checklist
5. Ask user instead of checking memory → STOP, search memory first

**Locked in:** 2026-04-25 after Coco analysis of 4 prior sessions of failures.

Each rule targets a specific failure pattern. All 5 rules must be followed on every task.
