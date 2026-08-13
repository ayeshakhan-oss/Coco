---
name: Task Wiring Map
description: Automated workflow routing. For each task type, the exact files to check in order, before executing.
type: project
---

# Task Wiring Map — Automated Workflow

When you ask me to do a task, I automatically follow this wiring. No asking you what to check — I know the exact sequence.

---

## Example: Draft Values Feedback Email (Candidate Failed Values)

**You say:** "Draft a values feedback email for Muhammad Junaid — he failed values."

**I automatically:**

1. ✅ **Check .claude/RULES.md** — Any hard constraints on feedback emails?
2. ✅ **Check .claude/sops/00_General_SOPs/general_non_negotiable_sops.md** — Rule 1.11: Check Markaz first
3. ✅ **Open Markaz** → Search Muhammad Junaid → Job title → Current status → Prior feedback
4. ✅ **Check .claude/sops/CLAUDE.md** → Task router → "Reject candidate (values)" row
5. ✅ **Check .claude/skills/01_candidate-communication/values-feedback-emails.md** → Read "When to Use", "Universal Rules", "Detailed Procedure", "Execution Discipline"
6. ✅ **Check memory/email_template_format_FINAL.md** → Logo, blue header, Georgia text, NO asterisks
7. ✅ **Check memory/skill_values_feedback_emails_sop.md** → 800-1100 words mandatory, v8 design, pilot to Ayesha+Jawad
8. ✅ **Check memory/warm_bench_session_may5_2026_complete_learnings.md** → Subject line rules, section headings, language rules
9. ✅ **Check memory/SELF_QA_CHECKLIST.md** → Pre-send QA (8 items)
10. ✅ **Draft email** following all locked rules and procedures
11. ✅ **Run self-QA** before showing you

**Result:** Complete email draft, ready for your review. No back-and-forth.

---

## Task Wiring Map (All Task Types)

| Task | Step 1: Rules | Step 2: SOP/Skill | Step 3: Template | Step 4: Memory | Step 5: Execute |
|------|---------------|------------------|------------------|----------------|-----------------|
| **Draft values feedback email** | .claude/RULES.md | .claude/skills/01_candidate-communication/values-feedback-emails.md | email_template_format_FINAL.md | skill_values_feedback_emails_sop.md + warm_bench_session_may5_2026 | Check Markaz → Draft → Self-QA |
| **Draft GWC rejection email** | .claude/RULES.md + Rule 1.11 | .claude/skills/01_candidate-communication/gwc-rejection-emails.md | email_template_format_FINAL.md | warm_bench_final_locked_approach.md (warm tone) | Check Markaz → Draft → Self-QA |
| **Draft warm bench feedback** | .claude/RULES.md + Rule 1.11 | .claude/skills/01_candidate-communication/warm-bench-feedback-email.md | warm_bench_final_locked_approach.md | warm_bench_session_may5_2026 (word count, subjects, P.S.) | Check Markaz → Draft (800-1100w) → Self-QA |
| **Draft CV rejection email** | .claude/RULES.md + Rule 1.11 | .claude/skills/01_candidate-communication/candidate-rejections.md | email_template_format_FINAL.md | feedback_bulk_rejection_cv_truncation.md | Check Markaz → Draft → Self-QA |
| **Screen CVs against JD** | .claude/RULES.md | .claude/skills/02_candidate-evaluation/cv-screening.md | REPORT_FORMAT_LOCKED.md | skill_cv_screening_sop.md | Verify JD → Screen → Self-QA |
| **Evaluate case study** | .claude/RULES.md + Rule 1.11 | .claude/skills/02_candidate-evaluation/case-study-evaluation.md | N/A | skill_case_study_evaluation_sop.md | Check Markaz → Eval → Flag incomplete → Report |
| **Score values interview** | .claude/RULES.md + Rule 1.11 | .claude/skills/02_candidate-evaluation/values-scorecard-scoring.md | N/A (Markaz form) | feedback_values_scorecard_schema.md | Check Markaz → Score → Submit to Markaz |
| **Send interview invite** | .claude/RULES.md + 1.4 (approval) | N/A (universal) | locked_email_template_interview_invites.md | locked_email_template_interview_invites.md (18-point checklist) | Check calendar → Draft → Approval → Send |
| **Create decision brief** | .claude/RULES.md + Rule 1.11 | .claude/skills/03_hiring-operations/decision-briefs.md | N/A (custom) | feedback_decision_brief_hyperlinks.md (CV links mandatory) | Check Markaz → Draft → Verify all names linked → Self-QA |
| **Generate attendance report** | .claude/RULES.md | .claude/skills/03_hiring-operations/attendance-reports.md | attendance_report_complete_template.md | attendance_report_complete_template.md (colors, sections, no grid) | Query Teams/Markaz → Build → Self-QA |
| **Talent sourcing** | .claude/RULES.md | .claude/skills/05_talent-sourcing/talent-sourcing.md | N/A (process-based) | talent_sourcing_7steps_complete.md | Execute 7 steps → Verify links → Excel → Add to Markaz |
| **Draft contract / NDA / addendum / offer documents** | .claude/RULES.md + Rule 1.4 (approval) | .claude/skills/07_contract-drafting/SKILL.md | .claude/skills/07_contract-drafting/TEMPLATE_MAP.md + Contracts\ masters | skill07_contract_drafting_locked_2026_08_12.md | Confirm entity+type → Collect details+JD → Populate copy → Validate → Package (contract+NDA) → Show Ayesha |

---

## Universal Wiring Rules (All Tasks)

**BEFORE ANY TASK, ALWAYS:**
1. ✅ Check Rule 1.11 (Markaz check required for candidate feedback tasks)
2. ✅ Check Rule 1.4 (Approval before sending — ask explicitly)
3. ✅ Check Rule 1.7 (Memory review — read relevant prior context)
4. ✅ Read the **Detailed Procedure** section of the skill file (100-150 lines)
5. ✅ Read the **Execution Discipline** section (step-by-step pattern)
6. ✅ Read locked templates side-by-side
7. ✅ Run **Self-QA checklist** (8 items) before showing you draft
8. ✅ Flag any contradictions between Markaz record and your request

**NEVER:**
- Ask you "where is X?" when it's in Markaz or memory
- Skip Markaz check (Rule 1.11)
- Send without explicit approval (Rule 1.4)
- Ignore locked templates
- Rush through QA

---

## How This Works in Practice

**Scenario 1: You ask to draft a values feedback email**

Me (internally):
1. Load .claude/RULES.md + Rule 1.11
2. Open Markaz → Find candidate → Verify job and status
3. Load .claude/skills/01_candidate-communication/values-feedback-emails.md
4. Load memory/email_template_format_FINAL.md + memory/warm_bench_session_may5_2026
5. Draft email
6. Run 8-item Self-QA
7. Show you the draft: "Here's the email. Ready to pilot to Ayesha+Jawad?"

**No:** "Where is the candidate's scorecard?" or "Which values did they fail?"
**Yes:** "I checked Markaz — they failed [specific values]. Here's the email."

---

**Scenario 2: You ask to screen CVs**

Me (internally):
1. Load .claude/RULES.md
2. Load .claude/skills/02_candidate-evaluation/cv-screening.md
3. Load memory/REPORT_FORMAT_LOCKED.md
4. Load memory/skill_cv_screening_sop.md
5. Verify JD provided
6. Screen candidates
7. Build HTML report
8. Run Self-QA (stat box count, hyperlinks, etc.)
9. Show you the report: "Ready to send to you for review?"

**No:** "What's the JD?" (you already told me)
**Yes:** "I found 42 candidates. Top 5 shortlisted with profiles. Here's the report."

---

## Contract / NDA / Addendum tasks (added 2026-08-13)

**Trigger words:** contract · NDA · addendum · fellow · joining package · offer document ·
appointment letter · annexure

| Step | File |
|---|---|
| 1. Rules injected automatically | `memory/contract_docx_build_rules_2026_08_13.md` (prompt hook) |
| 2. Build SOP | [.claude/sops/07_Contract_Documents/CONTRACT_DOCX_BUILD_SOP.md](07_Contract_Documents/CONTRACT_DOCX_BUILD_SOP.md) |
| 3. Skill + routing | [.claude/skills/07_contract-drafting/SKILL.md](../skills/07_contract-drafting/SKILL.md) → entity sub-skill |
| 4. Template map | [TEMPLATE_MAP.md](../skills/07_contract-drafting/TEMPLATE_MAP.md) |
| 5. Validate before pilot | `python scripts/evals/contract_docx_eval.py --dir "output/contracts/<Name>" --type fellow` |
| 6. Send-time block | `scripts/hooks/pre_contract_send_hook.py` (PreToolUse) |
| 7. Harness regression | `python scripts/evals/test_contract_eval.py` |

**Never:** claim a layout fix is verified without a human eye on the page — there is no
renderer on this machine. **Never:** invent a field. **Never:** send without Ayesha's approval.

---

## Status

✅ **WIRING LOCKED IN**
- Task → Files mapping is explicit and automated
- No ambiguity about what to check
- No asking for context already in Markaz or memory
- Repeatable, disciplined workflow for every task type

**Commitment:** When you mention a task, I automatically follow this wiring. You get a complete, verified output without back-and-forth.

---

**Updated:** 2026-05-12  
**Owner:** Coco
