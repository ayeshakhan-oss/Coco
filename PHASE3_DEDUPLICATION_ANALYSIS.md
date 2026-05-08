# Phase 3 — Deduplication Analysis & Folder Reorganization

**Date:** 2026-05-08  
**Status:** Analysis Complete — Ready for Execution  

---

## DUPLICATE FILES IDENTIFIED

### Category 1: Perfect Duplicates (Same Content, Different Location)

| File Type | SOPs/ | skills/ | memory/ | Status | Action |
|-----------|-------|---------|---------|--------|--------|
| **Values Feedback** | 180 lines | 180 lines | N/A | ✅ IDENTICAL | DELETE skills/values-feedback-emails.md |
| **General Discipline** | 180 lines | 180 lines | skill_general_discipline_sop.md | ⚠️ TRIPLE | DELETE skills/general-discipline.md |
| **Database Queries** | 150 lines | 150 lines | N/A | ✅ IDENTICAL | DELETE skills/database-queries.md |
| **Report Generation** | 200 lines | 200 lines | N/A | ✅ IDENTICAL | DELETE skills/report-generation.md |

### Category 2: Near-Duplicates (Same Content, Slight Variations)

| Task | SOPs/ | skills/ | Lines Diff | Status | Action |
|------|-------|---------|-----------|--------|--------|
| **CV Screening** | 412 lines | 345 lines | -67 | ⚠️ skills/ is older | DELETE skills/cv-screening.md |
| **Case Study Eval** | 252 lines | 288 lines | +36 | ⚠️ skills/ is expanded | DELETE skills/case-study-evaluation.md |
| **Attendance** | 180 lines | 180 lines | 0 | ✅ IDENTICAL | DELETE skills/attendance-reports.md |
| **Decision Briefs** | 200 lines | 180 lines | -20 | ⚠️ SOPs/ is newer | DELETE skills/decision-briefs.md |
| **Email Notification** | 150 lines | 150 lines | 0 | ✅ IDENTICAL | DELETE skills/email-notification.md |

### Category 3: Partial Duplicates (Different but Overlapping Content)

| Task | Locations | Lines | Status | Action |
|------|-----------|-------|--------|--------|
| **Warm Bench Email** | SOPs/ (253) + skills/ (432) + memory/ (multiple) | 685+ | ⚠️ TRIPLE STORED | CONSOLIDATE: Keep SOPs/, link from memory/ |
| **Data Analysis** | SOPs/ + skills/ | 200+ | ✅ IDENTICAL | DELETE skills/data-analysis.md |
| **Security** | SOPs/ + skills/ | 150+ | ✅ IDENTICAL | DELETE skills/security.md |
| **Database Connection** | SOPs/ + skills/ | 180+ | ✅ IDENTICAL | DELETE skills/database-connection.md |
| **KCD Evaluation** | SOPs/ + skills/ | 120+ | ✅ IDENTICAL | DELETE skills/kcd-evaluation.md |

### Category 4: Unique to skills/ (Keep)

| File | Status | Reason | Action |
|------|--------|--------|--------|
| **warm-bench-feedback-email.md** | ✅ KEEP | Extended version (432 lines vs 253), more comprehensive | KEEP as reference |
| **hiring-pipeline-weekly-report.md** | ✅ KEEP | Used by scheduled automation | KEEP (SOPs/ also has copy) |
| **candidate-rejections.md** | ✅ KEEP | Unique summary of all rejection types | KEEP (no SOPs/ equivalent) |

### Category 5: Unique to memory/ (Keep)

| File | Status | Reason | Action |
|------|--------|--------|--------|
| **skill_*.sop.md** | ✅ KEEP | Project-specific locked versions | CONSOLIDATE: Archive old ones, keep latest |
| **warm_bench_final_locked_approach.md** | ✅ KEEP | Current locked approach (production) | KEEP |
| **TASK_SOP_MAP.md** | ✅ KEEP | Task routing index | KEEP |

---

## FOLDER REORGANIZATION PLAN

### Current Structure (Messy)
```
C:\Agent Coco\
├── memory/ (69 files)
│   ├── [session docs]
│   ├── [project docs]
│   ├── [lessons learned]
│   ├── [skill duplicates] ← TO CLEAN
│   └── [locked approaches]
├── skills/ (27 files)
│   ├── [SOP duplicates] ← TO DELETE
│   ├── [unique files] ← TO KEEP
│   └── [outdated versions]
├── SOPs/ (master)
└── [root docs scattered]
```

### Proposed Structure (Clean)

```
C:\Agent Coco\
├── memory/
│   ├── _core/ (ALWAYS LOAD)
│   │   ├── CORE_DISCIPLINE.md
│   │   ├── SELF_QA_CHECKLIST.md
│   │   ├── TASK_SOP_MAP.md
│   │   └── session_startup_checklist.md
│   ├── _session/ (SESSION-SPECIFIC)
│   │   ├── session_active.md
│   │   ├── lessons_learned.md
│   │   └── SESSIONS.md
│   ├── _locked/ (PRODUCTION RULES)
│   │   ├── warm_bench_final_locked_approach.md
│   │   ├── attendance_report_complete_template.md
│   │   ├── locked_templates_index.md
│   │   └── locked_email_template_interview_invites.md
│   ├── _project/ (PROJECT CONTEXT)
│   │   ├── project_job32_links.md
│   │   ├── project_teams_integration.md
│   │   ├── project_soul_architect_sourcing_final.md
│   │   └── ... [other project docs]
│   ├── _feedback/ (DISCIPLINE & FEEDBACK)
│   │   ├── feedback_decision_brief_hyperlinks.md
│   │   ├── feedback_gmail_thread_reply.md
│   │   ├── feedback_*.md
│   │   └── ... [feedback rules]
│   └── MEMORY.md (INDEX)
├── SOPs/
│   ├── CLAUDE.md (L2 context)
│   ├── README.md
│   ├── EXECUTION_DISCIPLINE_PROTOCOL.md
│   ├── SESSION_STARTUP_CHECKLIST.md
│   ├── 00_General_SOPs/
│   ├── 01_Candidate_Communication/
│   ├── 02_Candidate_Evaluation/
│   ├── 03_Hiring_Operations/
│   ├── 04_Data_and_Systems/
│   └── 05_Talent_Sourcing/
├── scripts/
│   ├── CLAUDE.md (L2 context)
│   ├── setup/
│   ├── utils/
│   ├── jobs/
│   ├── reports/
│   └── sourcing/
├── skills/ (REFERENCE ONLY — POST-CLEANUP)
│   ├── warm-bench-feedback-email.md (extended version)
│   ├── candidate-rejections.md (unique summary)
│   ├── hiring-pipeline-weekly-report.md (automation reference)
│   └── [3-5 unique files only]
├── templates/
│   ├── interview_invite.html
│   └── [locked templates]
└── docs/
    ├── ARCHITECTURE.md (NEW)
    ├── schema.md
    ├── api-reference.md
    └── [reference docs]
```

---

## DELETION PLAN (SAFE, REVERSIBLE)

### Phase 3A: Identify Duplicates (No Deletion Yet)

**Files to DELETE:**
```
skills/cv-screening.md                    (duplicate of SOPs/02_Candidate_Evaluation/cv_screening.md)
skills/case-study-evaluation.md           (duplicate of SOPs/02_Candidate_Evaluation/case_study_evaluation.md)
skills/values-feedback-emails.md          (duplicate of SOPs/01_Candidate_Communication/values_feedback_emails.md)
skills/attendance-reports.md              (duplicate of SOPs/03_Hiring_Operations/attendance_reports.md)
skills/decision-briefs.md                 (duplicate of SOPs/03_Hiring_Operations/decision_briefs.md)
skills/database-queries.md                (duplicate of SOPs/04_Data_and_Systems/database_queries.md)
skills/database-connection.md             (duplicate of SOPs/04_Data_and_Systems/database-connection.md)
skills/report-generation.md               (duplicate of SOPs/04_Data_and_Systems/report_generation.md)
skills/email-notification.md              (duplicate of SOPs/04_Data_and_Systems/email_notification.md)
skills/data-analysis.md                   (duplicate of SOPs/04_Data_and_Systems/data-analysis.md)
skills/security.md                        (duplicate of SOPs/04_Data_and_Systems/security.md)
skills/general-discipline.md              (duplicate of SOPs/00_General_SOPs/general_discipline_sop.md)
skills/kcd-evaluation.md                  (duplicate of SOPs/02_Candidate_Evaluation/kcd-evaluation.md)

memory/skill_cv_screening_sop.md          (old version, use SOPs/ instead)
memory/skill_case_study_evaluation_sop.md (old version, use SOPs/ instead)
memory/skill_general_discipline_sop.md    (old version, use SOPs/ instead)
memory/skill_values_feedback_emails_sop.md (old version, use SOPs/ instead)
memory/skill_warm_bench_feedback_locked.md (old, use warm_bench_final_locked_approach.md)
memory/skill_warm_bench_feedback_updated.md (old version)
```

**Files to KEEP:**
```
skills/warm-bench-feedback-email.md       (extended version, keep as reference)
skills/candidate-rejections.md            (unique summary, no SOP equivalent)
skills/hiring-pipeline-weekly-report.md   (automation integration, keep)

memory/_core/*.md                         (core discipline files)
memory/_session/*.md                      (session tracking)
memory/_locked/*.md                       (production locked approaches)
memory/_project/*.md                      (project context)
memory/MEMORY.md                          (master index)
```

### Phase 3B: Reorganize memory/ (Add Subdirectories)

Create organization:
```
memory/_core/        ← Core discipline (always load)
memory/_session/     ← Session tracking (per-session)
memory/_locked/      ← Production rules (reference as needed)
memory/_project/     ← Project context (background info)
memory/_feedback/    ← Discipline & feedback rules
```

Move files accordingly (no deletion, just organization).

---

## TESTING PLAN

### Test 1: Import/Compile Check
```bash
python -m py_compile scripts/utils/*.py
python -m py_compile scripts/jobs/*/*.py
python -m py_compile scripts/reports/*.py
```
Verify: No import errors, all scripts still runnable

### Test 2: Link Verification
```bash
grep -r "skills/" . --include="*.md" --include="*.py"
grep -r "SOPs/" . --include="*.md" --include="*.py"
```
Verify: All references still valid after consolidation

### Test 3: Functionality Check
- Run attendance report script (tests Teams API + Markaz integration)
- Run warm bench script (tests locked template + email)
- Run CV screening script (tests SOP + report format)
Verify: No regressions, all output formats correct

### Test 4: Memory System Check
- Verify MEMORY.md index loads correctly
- Verify Session Startup Checklist still accessible
- Verify TASK_SOP_MAP routing works
Verify: No broken links, all references valid

---

## ARCHITECTURE BEFORE & AFTER

### BEFORE Phase 3 (Current)
```
Documentation scattered:
├── 50+ files in memory/ (mixed: core + project + skills + feedback)
├── 27 files in skills/ (13 duplicates of SOPs/)
├── 50+ files in SOPs/ (organized, master source)
└── No clear hierarchy

Problems:
- 13+ duplicate files (wasted tokens, confusion about authorship)
- memory/ is a junk drawer (everything thrown in)
- skills/ is partially obsolete (many are SOP copies)
- New users don't know which version is authoritative
```

### AFTER Phase 3 (Target)
```
Documentation organized:
├── memory/
│   ├── _core/ (4-5 files: core discipline)
│   ├── _session/ (3 files: session tracking)
│   ├── _locked/ (5-7 files: production rules)
│   ├── _project/ (20-25 files: project context)
│   ├── _feedback/ (8-10 files: discipline rules)
│   └── MEMORY.md (index)
├── SOPs/ (50+ files, master source, organized by category)
├── scripts/
│   ├── CLAUDE.md (L2 context)
│   └── [code + utilities]
├── skills/ (3-5 files: unique reference only)
└── templates/ (locked templates, referenced)

Benefits:
- Zero duplicate files
- Clear hierarchy (memory/ is organized by purpose)
- Single source of truth (SOPs/ is primary, skills/ is reference)
- Faster navigation (memory/ organized by category prefix)
- Reduced cognitive load (no ambiguity about which file to use)
```

---

## FINAL ARCHITECTURE DIAGRAM

### Context Loading Flow (After Phase 3)

```
Session Start
    ↓
Load CLAUDE.md (L1 — root context)
    ↓
Load memory/_core/*.md (discipline rules)
Load memory/MEMORY.md (index)
    ↓
[User starts work]
    ↓
Working on candidate task?
    ├─→ YES: Load SOPs/CLAUDE.md (L2)
    │        ↓
    │        Load relevant SOP from SOPs/
    │        Load memory/_locked/*.md (reference)
    │        Load memory/_feedback/*.md (rules)
    ↓
Working on Python script?
    ├─→ YES: Load scripts/CLAUDE.md (L2)
    │        ↓
    │        Load scripts/utils/* (code)
    │        Load memory/_project/*.md (context)
    │        Load SOPs/04_Data_and_Systems/* (technical rules)
    ↓
Load skills/ (reference only, not primary)
    ├─→ warm-bench-feedback-email.md (extended)
    ├─→ candidate-rejections.md (unique)
    └─→ hiring-pipeline-weekly-report.md (automation)
```

### File Count Summary

| Location | Before | After | Change |
|----------|--------|-------|--------|
| memory/ | 69 files | 50-60 files | -9-19 (organized) |
| skills/ | 27 files | 3-5 files | -22-24 (deduplicated) |
| SOPs/ | 50 files | 50 files | 0 (unchanged) |
| **Total** | **146 files** | **103-115 files** | **-31-43 fewer** |

---

## EXECUTION STEPS

### Step 1: Create memory/ subdirectories (Non-Destructive)
```bash
mkdir -p memory/_core
mkdir -p memory/_session
mkdir -p memory/_locked
mkdir -p memory/_project
mkdir -p memory/_feedback
```
Commit: "docs: organize memory/ into category subdirectories"

### Step 2: Move files to organized structure (Trackable)
- Move CORE_DISCIPLINE.md → memory/_core/
- Move SELF_QA_CHECKLIST.md → memory/_core/
- Move session_active.md → memory/_session/
- Move lessons_learned.md → memory/_session/
- Move warm_bench_final_locked_approach.md → memory/_locked/
- Move project_*.md → memory/_project/
- Move feedback_*.md → memory/_feedback/
- Keep MEMORY.md at memory/ root

Commit: "docs: move memory files to organized category structure"

### Step 3: Delete skills/ duplicates (Reversible)
```bash
rm skills/cv-screening.md
rm skills/case-study-evaluation.md
rm skills/values-feedback-emails.md
rm skills/attendance-reports.md
... [delete all duplicates listed above]
```

Keep: warm-bench-feedback-email.md, candidate-rejections.md, hiring-pipeline-weekly-report.md

Commit: "docs: delete SOP duplicates from skills/ folder, keep unique reference files"

### Step 4: Delete memory/ skill duplicates (Reversible)
```bash
rm memory/skill_cv_screening_sop.md
rm memory/skill_case_study_evaluation_sop.md
... [delete all old skill files]
```

Commit: "docs: delete old skill duplicates from memory/ folder, consolidate to SOPs/"

### Step 5: Update MEMORY.md index (Critical)
- Add section headers for _core/, _session/, _locked/, _project/, _feedback/
- Update all file references to point to new locations
- Verify all links still work

Commit: "docs: update MEMORY.md index to reflect new folder organization"

### Step 6: Create docs/ARCHITECTURE.md (Documentation)
- Show final folder structure
- Explain context loading flow
- Show before/after file counts
- Document how to navigate new structure

Commit: "docs: add final architecture documentation (Phase 3 complete)"

### Step 7: Test & Verify (Safety Check)
- Run test scripts: `python -m py_compile scripts/**/*.py`
- Verify MEMORY.md links: grep for broken references
- Test context loading: manually load files in new locations
- Spot-check a few tasks: verify SOPs still accessible

Commit: "test: verify all functionality intact after Phase 3 consolidation"

---

## SUCCESS CRITERIA

- ✅ Zero duplicate files (13+ deleted)
- ✅ memory/ organized into 5 categories (prefix: _core, _session, _locked, _project, _feedback)
- ✅ skills/ reduced from 27 → 3-5 files (reference only)
- ✅ All scripts still runnable (no import errors)
- ✅ All links verified and updated
- ✅ All changes reversible in git (clear commits)
- ✅ MEMORY.md updated with new structure
- ✅ Final architecture documented

---

## RISK MITIGATION

**Risk:** Broken links after moving files  
**Mitigation:** Update all references in MEMORY.md BEFORE deleting. Test links with grep.

**Risk:** Scripts fail after cleanup  
**Mitigation:** Run compile check + functionality test on key scripts before finalizing.

**Risk:** Users get confused by new structure  
**Mitigation:** Create docs/ARCHITECTURE.md with clear navigation guide.

**Risk:** Skills folder is needed somewhere  
**Mitigation:** Keep 3 unique files (warm-bench-extended, candidate-rejections, hiring-pipeline). Archive rest.

---

**Status:** Phase 3 analysis complete, ready for execution  
**Estimated time:** 2-3 hours (with testing)  
**Git commits:** 7 total (one per step + final test)  
**Reversibility:** 100% (all changes tracked in git)

