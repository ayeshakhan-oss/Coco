# MEMORY INDEX — Coco (Real Files Only)

**Last Updated:** 2026-05-08  
**Status:** PHASE 3 COMPLETE — Progressive disclosure + de-duplication + reorganization. Deleted 19 duplicate files (13 from skills/, 6 from memory/). Organized memory/ into 5 categories (_core, _session, _locked, _project, _feedback). Single source of truth = SOPs/. Zero regressions.

---

## 🔴 MUST READ THESE FIRST (Session Start + Every Task)

### Core Discipline (_core/)
- [CORE_DISCIPLINE.md](_core/CORE_DISCIPLINE.md) — **SINGLE SOURCE:** All 10 rules + execution protocol. Read before any task.
- [SELF_QA_CHECKLIST.md](_core/SELF_QA_CHECKLIST.md) — **8 ITEMS REQUIRED:** Run before submitting ANY work.
- [TASK_SOP_MAP.md](_core/TASK_SOP_MAP.md) — **TASK REFERENCE:** Maps each task to its SOP + template + checklist.
- [Session Startup Checklist](_core/session_startup_checklist.md) — 7-step check (run at session start)

---

## SESSION TRACKING (Per-Session)

### Active Session & Lessons (_session/)
- [Lessons Learned Log](_session/lessons_learned.md) — Structured append-only log: date, task, mistake, correction, rule. Updated by Stop hook. Max 50 entries.
- [Active Session Scratchpad](_session/session_active.md) — Live notes for current session: task, decisions, mistakes, files modified. Wiped at session start.

---

## PRODUCTION RULES (Locked & Reference)

### Locked Approaches & Templates (_locked/)
- [Warm Bench Final Locked Approach](_locked/warm_bench_final_locked_approach.md) — Haroon Yasin framework, 800-1100 words, poetic subjects, locked approach.
- [Attendance Report Complete Template](_locked/attendance_report_complete_template.md) — Stat boxes, colors, table structure, PDF/HTML format locked.
- [Locked Email Template Interview Invites](_locked/locked_email_template_interview_invites.md) — Universal interview invite design (all stages), colors #f3f4f6, #2f4fa2, Georgia serif.
- [Locked Templates Index](_locked/locked_templates_index.md) — Quick reference to all locked formats.

---

## SYSTEM ARCHITECTURE & OPTIMIZATION

### Progressive Disclosure Documentation
- [DOCUMENTATION_AUDIT_AND_REFACTOR_PLAN.md](../DOCUMENTATION_AUDIT_AND_REFACTOR_PLAN.md) — Comprehensive 5-phase refactor plan + audit findings (Phase 1-2 complete).
- [PROGRESSIVE_DISCLOSURE_SUMMARY.md](../PROGRESSIVE_DISCLOSURE_SUMMARY.md) — Before/after comparison, token impact analysis, success metrics.
- [DOCUMENTATION_AUDIT_FINDINGS.md](../DOCUMENTATION_AUDIT_FINDINGS.md) — Redundancy analysis, 20+ duplicate files identified, solutions implemented.
- [DOCUMENTATION_STRUCTURE_BEFORE_AFTER.md](../DOCUMENTATION_STRUCTURE_BEFORE_AFTER.md) — Visual folder structure diagrams + context loading patterns.
- [PHASE3_DEDUPLICATION_ANALYSIS.md](../PHASE3_DEDUPLICATION_ANALYSIS.md) — Phase 3 detailed plan (reorganization + testing).

### Project Cleanup & Consolidation
- [Project Cleanup Complete (2026-05-08)](../CLEANUP_COMPLETE_2026_05_08.md) — 3-phase cleanup: Phase 1 (deleted 6.9 MB dead files), Phase 2 (consolidated 20 memory files → 4 canonical), Phase 3 (archived 5.2 MB historical data). Git commits preserved, zero functionality lost.
- [System Consolidation Complete](_project/system_consolidation_2026_04_28.md) — Major refactor: consolidated discipline docs, extracted templates to code, created task mapping. (April 28 snapshot)

---

## DISCIPLINE & FEEDBACK RULES (_feedback/)

### Problems Identified & Fixed
- [Coco Core Problems Identified](_feedback/coco_core_problems_identified.md) — 10 systemic discipline issues + solutions locked in (Session 002 analysis).
- [Teams API Incompleteness](_feedback/discipline_failure_teams_api_incomplete.md) — When APIs return suspiciously small results, verify with ground truth.
- [Discipline Enforcement Lockdown](_feedback/discipline_enforcement_lockdown.md) — 5 non-negotiable rules to stop leakage (memory-first, verification, templates, single-pass, no delegation).
- [Coco Delegation Discipline](_feedback/coco_delegation_discipline.md) — Never delegate tasks back to user. Check memory FIRST.

### Format & Integration Rules
- [Decision Brief CV Hyperlinks](_feedback/feedback_decision_brief_hyperlinks.md) — Every candidate name must link to Google Drive CV.
- [Gmail Thread Replies](_feedback/feedback_gmail_thread_reply.md) — In-Reply-To + References headers required for proper threading.
- [PDF Formatting](_feedback/feedback_pdf_formatting.md) — All ReportLab PDFs must use TA_JUSTIFY on body text.
- [Terminology Standards](_feedback/feedback_terminology.md) — Never "KCD" in reports; never "TBC/Pending" — use specific language.
- [Bulk Rejection CV Truncation](_feedback/feedback_bulk_rejection_cv_truncation.md) — Minimum 10k chars, never cv_text[:4500], flag long CVs.
- [DB Status vs Pipeline Reality](_feedback/feedback_db_status_vs_pipeline.md) — status='offer' is a stage, NOT a sent offer. Never assert without verification.
- [Values Scorecard Schema](_feedback/feedback_values_scorecard_schema.md) — Markaz JSON schema exact format required.

---

## PROJECT CONTEXT (_project/)

### Infrastructure & Integration
- [Teams Integration](_project/project_teams_integration.md) — Microsoft Graph API setup, Presence channel reading, known issues.
- [Project Security Hardening](_project/project_security_hardening.md) — safe_sendmail bouncer, read audit, token monitor, scope auditor, git data cleanup.

### Content & Articles
- [Rejection Feedback Article](_project/project_article_rejection_feedback.md) — LinkedIn/Medium article on personalized rejections (draft complete, awaiting publication).

### Completed Work
- [Soul Architect Talent Sourcing (Phase 3)](_project/project_soul_architect_sourcing_final.md) — 47 verified candidates sourced, Excel sent to Ayesha.

### Job-Specific Context
- [Job 32 Fundraising Links](_project/project_job32_links.md) — JD Google Doc + Calendar booking link for values invites.
- [Job 17 CPD Coach](_project/project_job17_cpd_coach.md) — Warm bench candidate context.
- [Job 26 Soul Architect Final](_project/project_job26_soul_architect_final.md) — 42 candidates screened, 15 top-tier, complete report.
- [Job 36 Decision Brief](_project/project_job36_decision_brief.md) — Final candidates & decision view approved format.
- [Job 36 New Batch](_project/project_job36_new_batch.md) — 19 screened, 15 emails generated, pilot sent.

### Hiring & Pipeline
- [Hiring Pipeline Monitor](_project/project_hiring_pipeline_monitor.md) — Proactive system runs Mon 10:30am + Fri 3pm, monitors all open positions, flags candidates stuck 3+ days.

---

## OPERATIONAL DUTIES

- [Proactive SOP Maintenance](_feedback/proactive_sop_maintenance_duty.md) — Automatic duty: copy new SOPs to SOPs folder, update README, commit to git.

---

## HOW TO USE THIS INDEX

### Navigation by Purpose

**At Session Start:**
1. Load CORE_DISCIPLINE.md from _core/
2. Run Session Startup Checklist (also in _core/)
3. Check Active Session Scratchpad for current task

**When Starting a Task:**
1. Check TASK_SOP_MAP in _core/ → Find your task type
2. Go to SOPs/ folder, load SOPs/CLAUDE.md (L2 context)
3. Read the exact SOP for your task
4. Load relevant locked template from _locked/ (if applicable)
5. Check _feedback/ for relevant rules/lessons (feedback docs)
6. Run SELF_QA_CHECKLIST before sending

**When Writing Code:**
1. Load scripts/CLAUDE.md (L2 context)
2. Read relevant data/systems SOP from SOPs/04_Data_and_Systems/
3. Load _project/ context (if task-specific)
4. Check scripts/utils/ and scripts/jobs/ for similar code

**When Stuck:**
1. Search _feedback/ for discipline rules / lessons learned
2. Search _project/ for prior work on similar task
3. Check _locked/ for locked approaches that might apply

### Folder Structure (Organized by Purpose)

```
memory/
├── _core/              (ALWAYS LOAD) — 4 files
│   ├── CORE_DISCIPLINE.md
│   ├── SELF_QA_CHECKLIST.md
│   ├── TASK_SOP_MAP.md
│   └── session_startup_checklist.md
├── _session/           (PER-SESSION) — 2 files
│   ├── session_active.md (live scratchpad)
│   └── lessons_learned.md (mistake log)
├── _locked/            (REFERENCE) — 5 files
│   ├── warm_bench_final_locked_approach.md
│   ├── attendance_report_complete_template.md
│   ├── locked_email_template_interview_invites.md
│   ├── locked_templates_index.md
│   └── locked_skill_warm_bench_interview_invite.md
├── _feedback/          (DISCIPLINE + RULES) — 15 files
│   ├── feedback_*.md (7 files)
│   ├── discipline_*.md (3 files)
│   ├── coco_*.md (3 files)
│   └── proactive_sop_maintenance_duty.md
├── _project/           (PROJECT CONTEXT) — 12 files
│   ├── project_*.md (all project-specific context)
│   └── system_consolidation_2026_04_28.md
└── MEMORY.md           (THIS FILE — Master Index)
```

---

## SINGLE SOURCE OF TRUTH

**SOPs/ is the PRIMARY source for all procedures and standards.**

After Phase 3 de-duplication:
- ✅ Zero duplicate files (deleted 19 duplicates)
- ✅ memory/ is pure reference/project-specific (no duplicate SOPs)
- ✅ skills/ contains only unique/extended reference files (5 files)
- ✅ SOPs/ is the ONLY place with master procedure definitions

---

## HOW TO ADD TO MEMORY

When learning something new:
1. Decide which category it belongs to (_core, _session, _locked, _feedback, _project)
2. Create new file with clear name
3. Add entry to relevant section of this MEMORY.md
4. Commit with message explaining why it's stored
5. If it's a duplicate of existing file, consolidate instead of creating new

**Rule:** Every entry in this index points to a REAL file in memory/. No phantoms. No duplicates.

---

**Owner:** Coco  
**Status:** ACTIVE — Phase 3 COMPLETE. Reorganized, de-duplicated, single source of truth established (SOPs/).  
**Last Action:** Deleted 19 duplicate files (13 from skills/, 6 from memory/). Reorganized memory/ into 5 categories. Updated index paths.
