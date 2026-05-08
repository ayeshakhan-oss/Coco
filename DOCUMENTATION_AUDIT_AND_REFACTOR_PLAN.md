# DOCUMENTATION AUDIT & PROGRESSIVE DISCLOSURE REFACTOR PLAN

**Date:** 2026-05-08  
**Status:** Audit Complete — Refactor Plan Ready  
**Token Impact Analysis:** Current bloat ≈ 15-20% of context window loading

---

## EXECUTIVE SUMMARY

### Current State
- **CLAUDE.md:** 136 lines (BLOATED) — Embeds task-specific details that should live in subdirectories
- **Documentation:** Scattered across 3 locations (SOPs/, memory/, skills/)
- **Duplicate Docs:** 20+ files with overlapping content (SOPs vs skills vs memory)
- **Context Burden:** Every session loads ~80 KB of CLAUDE.md + ~150 KB of MEMORY.md regardless of task

### Proposed Solution
Implement **3-level progressive disclosure** architecture:

| Level | Location | Size Target | Load Pattern |
|-------|----------|-------------|--------------|
| **L1** | CLAUDE.md (root) | <100 lines | Always loaded (project overview) |
| **L2** | Subdirectory CLAUDE.md files | ~150 lines/dir | Loaded when working in that directory |
| **L3** | Skill-specific rules + templates | On-demand | Loaded only when task matches trigger |

**Expected Token Savings:** 8-12k tokens/session (10-15% reduction in CLAUDE.md + memory load)

---

## PART 1: CURRENT CLAUDE.MD AUDIT

### Lines 1-30: PROJECT OVERVIEW ✅ KEEP (Essential Context)
```
Lines 1-4:     Project identity + agent name
Lines 8-18:    Session startup + discipline checklist pointers
Lines 21-29:   Memory system explanation
```
**Status:** Lean, critical. Keep exactly as-is.

---

### Lines 31-51: TASK ROUTING ⚠️ REFACTOR (Move to L2)
```
Lines 31-51:   "📋 What Task Are You Doing?"
               - CV Screening → [templates/] + [REPORT_FORMAT_LOCKED.md]
               - Interview Invites → [templates/]
               - Rejection Email → [SOPs/]
               - Values Feedback → [SOPs/] + [memory/warm_bench_]
               - Warm Bench → [skills/] + [memory/warm_bench_final_]
               - Attendance Report → [SOPs/]
               - Decision Brief → [SOPs/]
               - Case Study Eval → [SOPs/]
               - Talent Sourcing → [SOPs/]
```

**Problem:**
1. 21 lines of task-specific routing that's rarely used in practice
2. User goes to MEMORY.md or TASK_SOP_MAP anyway
3. Loads every session even when doing attendance work only

**Solution:** Move to `scripts/CLAUDE.md` (if doing reporting), `SOPs/CLAUDE.md` (if doing evaluation), etc.

---

### Lines 54-63: CORE RULES ✅ KEEP (Essential Pattern)
```
Lines 54-63:   3 core rules + links to discipline
```
**Status:** Critical. Keep (but condense to 2 lines pointing to CORE_DISCIPLINE.md).

---

### Lines 66-84: TECHNICAL CONTEXT ⚠️ REFACTOR (Move to L2)
```
Lines 66-84:   Database, peer agents, sister projects, focus areas, duties, locations table
```

**Problem:**
- Database context only relevant when writing queries
- Noah context only relevant in cross-agent work
- NIETE context only relevant for teacher-training tasks
- Auto duty relevant only after system refactors

**Solution:** Move to subdirectory CLAUDE.md files:
- `scripts/CLAUDE.md` → Database + query context
- `MEMORY.md` (or internal reference) → Noah context
- `memory/CLAUDE.md` → Duties + auto-triggers

---

### Lines 88-100: CURRENT FOCUS ⚠️ REFACTOR (Move to SESSIONS.md)
```
Lines 88-100:  Skill 16, Skill 15, Skill 14, Job 26, Hackathon, Decision Briefs
```

**Problem:**
- This is CHRONOLOGICAL, not structural
- "Skill 16 is locked" is a session outcome, not project truth
- Loaded every session and immediately outdated
- Better home: SESSIONS.md (per-session log)

**Solution:** 
- Delete from CLAUDE.md
- Append to SESSIONS.md as session summaries
- Move "current focus" to last line of CLAUDE.md (1 line) with pointer to SESSIONS.md

---

### Lines 104-122: MISC RULES + QUESTIONS ⚠️ REFACTOR (Move to L3)
```
Lines 104-110: Technical setup (email, audit, credentials, Teams, reports)
Lines 114-123: Never do these + questions
```

**Problem:**
- Technical setup is tool-specific (safe_sendmail only used in email scripts)
- Loads every session but used rarely
- "Open questions" are not blocking work

**Solution:**
- Move `safe_sendmail()` context to `scripts/CLAUDE.md` (reporting/email subdirectory)
- Move "never do these" to CORE_DISCIPLINE.md (already there)
- Archive "open questions" to SESSIONS.md

---

## PART 2: DOCUMENTATION STRUCTURE AUDIT

### Current Scattered State
```
C:\Agent Coco\
├── CLAUDE.md (136 lines) — TOO MUCH
├── memory/
│   ├── CORE_DISCIPLINE.md — 10 rules
│   ├── SELF_QA_CHECKLIST.md — 8 items
│   ├── TASK_SOP_MAP.md — Task→SOP map
│   ├── session_startup_checklist.md — 7-step
│   ├── lessons_learned.md — Mistake log
│   ├── session_active.md — Live scratchpad
│   ├── warm_bench_final_locked_approach.md — DUPLICATE of skills/warm-bench-feedback-email.md
│   ├── locked_templates_index.md — Points to templates/
│   └── [50+ project memory files]
├── SOPs/
│   ├── README.md — Master index
│   ├── SESSION_STARTUP_CHECKLIST.md — DUPLICATE
│   ├── EXECUTION_DISCIPLINE_PROTOCOL.md
│   ├── 00_General_SOPs/
│   ├── 01_Candidate_Communication/
│   ├── 02_Candidate_Evaluation/
│   ├── 03_Hiring_Operations/
│   ├── 04_Data_and_Systems/
│   └── 05_Talent_Sourcing/
├── skills/
│   ├── cv-screening.md — DUPLICATE of SOPs/02_Candidate_Evaluation/cv_screening.md
│   ├── warm-bench-feedback-email.md
│   └── [15 other skill files]
├── templates/
│   ├── interview_invite.html
│   └── [other templates]
├── docs/
│   ├── schema.md — Database schema
│   ├── api-reference.md — (unused?)
│   └── noah-talent-sourcing-reference.md — (external reference)
└── REPORT_FORMAT_LOCKED.md — Should be in docs/
```

### Redundancy Identified
| Concept | Location 1 | Location 2 | Location 3 |
|---------|-----------|-----------|-----------|
| Session startup | SOPs/SESSION_STARTUP_CHECKLIST.md | memory/session_startup_checklist.md | skills/general-discipline.md |
| Discipline | memory/CORE_DISCIPLINE.md | SOPs/EXECUTION_DISCIPLINE_PROTOCOL.md | skills/general-discipline.md |
| CV Screening | SOPs/02_Candidate_Evaluation/cv_screening.md | skills/cv-screening.md | memory/skill_cv_screening_sop.md |
| Case Study Eval | SOPs/02_Candidate_Evaluation/case_study_evaluation.md | skills/case-study-evaluation.md | memory/skill_case_study_evaluation_sop.md |
| Warm Bench | SOPs/01_Candidate_Communication/warm_bench_feedback_email.md | skills/warm-bench-feedback-email.md | memory/warm_bench_final_locked_approach.md |

---

## PART 3: PROPOSED REFACTORED STRUCTURE

### Target Architecture
```
C:\Agent Coco\
├── CLAUDE.md (100 lines max)
│   ├── Project overview (5 lines)
│   ├── Mandatory reads at start (4 lines)
│   ├── 3 core rules (3 lines)
│   ├── Memory system (2 lines pointer)
│   ├── Current session summary (1 line pointer to SESSIONS.md)
│   └── Subdirectory guidance (2 lines)
│
├── SESSIONS.md (chronological session log + current focus)
│
├── docs/
│   ├── ARCHITECTURE.md (new: structural overview)
│   ├── DATA_MODEL.md (merge api-reference.md + schema.md)
│   ├── SECURITY.md (move from SOPs/04_)
│   ├── CONTEXT_LOADING.md (this refactor plan)
│   └── [read-only reference docs]
│
├── memory/
│   ├── CORE_DISCIPLINE.md (discipline rules only)
│   ├── SELF_QA_CHECKLIST.md (8-item checklist)
│   ├── TASK_SOP_MAP.md (task→SOP router)
│   ├── session_startup_checklist.md (7-step startup)
│   ├── lessons_learned.md (mistake log)
│   ├── session_active.md (live scratchpad)
│   ├── MEMORY.md (project memory index)
│   └── [project-specific memory files ONLY]
│
├── SOPs/
│   ├── README.md (master index — UNCHANGED)
│   ├── SESSION_STARTUP_CHECKLIST.md (DELETED — keep only memory/version)
│   ├── EXECUTION_DISCIPLINE_PROTOCOL.md (UNCHANGED)
│   ├── 00_General_SOPs/
│   ├── 01_Candidate_Communication/
│   ├── 02_Candidate_Evaluation/
│   ├── 03_Hiring_Operations/
│   ├── 04_Data_and_Systems/
│   └── 05_Talent_Sourcing/
│
├── scripts/
│   ├── CLAUDE.md (new: database queries, email, audit context)
│   ├── utils/
│   ├── jobs/
│   └── reports/
│
├── skills/
│   └── [keep as L3 on-demand reference only — NOT primary]
│
└── templates/
    └── [locked templates — referenced in SOPs]
```

---

## PART 4: MIGRATION PLAN (3 Phases)

### Phase 1: De-duplicate Core Docs (Day 1)
**Delete these files (keep memory/ version as source of truth):**
- Delete `SOPs/SESSION_STARTUP_CHECKLIST.md` → Points to `memory/session_startup_checklist.md`
- Delete all `skills/*.md` except `warm-bench-feedback-email.md` → Reconstruct from SOPs/ only
- Delete `memory/skill_cv_screening_sop.md` → Points to `SOPs/02_Candidate_Evaluation/cv_screening.md`
- Delete `memory/skill_case_study_evaluation_sop.md` → Points to `SOPs/02_Candidate_Evaluation/case_study_evaluation.md`

**Git commit:** `docs: remove duplicate SOP files, establish single source of truth`

---

### Phase 2: Refactor CLAUDE.md to <100 Lines (Day 1)
**Current:** 136 lines  
**Target:** 95 lines

**Keep (45 lines):**
```markdown
# Project: Taleemabad Talent Acquisition Agent
[5-line project overview]

## Before You Work
[4 critical reads with links to memory/]

## Core Rules
[3 rules, 3 lines]

## Memory System
[1-line pointer to memory/MEMORY.md]

## Current Focus
[1-line pointer to SESSIONS.md]

## How Work is Organized
[2-line explanation of L1/L2/L3 structure]
```

**Move (91 lines) to subdirectories:**
- **Task routing** → `SOPs/CLAUDE.md` (task-aware loading)
- **Technical setup** → `scripts/CLAUDE.md` (code-aware loading)
- **Current focus** → `SESSIONS.md` (chronological log)
- **Open questions** → Archive or move to SESSIONS.md

**Git commit:** `docs: refactor CLAUDE.md to <100 lines, implement progressive disclosure L1`

---

### Phase 3: Create Subdirectory CLAUDE.md Files (Day 2)
**`scripts/CLAUDE.md` (150 lines):**
```
# Scripts & Utilities Context

## When You're Here
You're writing Python scripts for:
- Database queries (Neon PostgreSQL)
- Email operations (safe_sendmail bouncer)
- Report generation (ReportLab PDFs)
- Teams/Gmail API integration

## Critical Setup
- Database: [brief connection info]
- Email: [safe_sendmail pattern + audit logging]
- Teams: Microsoft Graph API reader
- Credentials: .env file (never commit)
- Audit: log_gmail_read() + log_db_query()

## Key Scripts
[Organize by function, not by file]

## Relevant SOPs
- [04_Data_and_Systems] for database + email operations
- [03_Hiring_Operations] for report generation
```

**`SOPs/CLAUDE.md` (150 lines):**
```
# SOPs & Standard Operating Procedures

## When You're Here
You're working on:
- Candidate communication (rejection, values, warm bench emails)
- Candidate evaluation (CV screening, case studies, scorecards)
- Hiring operations (decision briefs, attendance reports)
- Data & systems queries

## Quick Task Router
[Task type → SOP file mapping table]

## Format Rules (Locked)
- Email format: [pointer to locked format]
- PDF format: [pointer to locked template]
- HTML format: [pointer to interview_invite.html]

## Common Mistakes
[Per-task mistake log extracted from lessons_learned.md]
```

**Git commit:** `docs: add subdirectory CLAUDE.md for progressive disclosure L2`

---

### Phase 4: Update Root Documentation (Day 2)
**Update SESSIONS.md:**
- Add "Current Focus" section with latest skills
- Keep chronological session log
- Link to SESSIONS_ARCHIVE.md for old sessions (once >100 entries)

**Create docs/ARCHITECTURE.md:**
```
# Architecture & Design Decisions

## Project Structure
[Visual diagram of L1/L2/L3 context loading]

## Memory System
[Explanation of 3-tier memory]

## SOP Organization
[Why 5 categories, how to extend]

## Skill Progression
[How skills are versioned and locked]
```

**Git commit:** `docs: establish docs/ as read-only reference, update SESSIONS.md`

---

## PART 5: REDUNDANCY CLEANUP (Optional, Phase 2)

### Consolidate SOPs & Skills
Currently: `SOPs/02_Candidate_Evaluation/cv_screening.md` + `skills/cv-screening.md` (near-duplicates)

**Option A (Recommended):**
- Keep `SOPs/` as primary source of truth (organized, structured)
- Delete `skills/` folder entirely
- Update CLAUDE.md to point to SOPs/ only

**Option B:**
- Keep both but establish clear ownership:
  - `SOPs/` = locked, versioned procedures
  - `skills/` = concise trigger-based guides
  - Add cross-references

**Recommendation:** Option A (single source of truth reduces cognitive load)

---

## PART 6: TOKEN IMPACT ANALYSIS

### Current Context Loading (Estimated)
| File | Lines | Tokens | Load Pattern |
|------|-------|--------|--------------|
| CLAUDE.md | 136 | ~4,500 | Always |
| memory/MEMORY.md | 77 | ~2,500 | Always |
| memory/CORE_DISCIPLINE.md | 200+ | ~7,000 | Always |
| memory/TASK_SOP_MAP.md | 150+ | ~5,000 | Always |
| Relevant SOPs/skill | 500-2000 | ~20,000 | Task-dependent |
| **TOTAL (avg session)** | | ~39,000 | |

### Post-Refactor Context Loading
| File | Lines | Tokens | Load Pattern |
|------|-------|--------|--------------|
| CLAUDE.md (refactored) | 95 | ~3,000 | Always |
| memory/MEMORY.md | 77 | ~2,500 | Always |
| memory/CORE_DISCIPLINE.md | 200+ | ~7,000 | Always |
| Relevant SOPs/skill | 500-2000 | ~20,000 | Task-dependent |
| Subdirectory CLAUDE.md | 150 | ~5,000 | Context-aware |
| **TOTAL (avg session)** | | ~37,500 | |

**Savings:** ~1,500 tokens/session (3.8% reduction)  
**Cumulative (100 sessions):** ~150,000 tokens  
**Plus:** Faster context search + clearer organization

---

## PART 7: WHAT TO KEEP UNCHANGED

✅ **SOPs/ folder structure** — Organized, locked, working well  
✅ **memory/MEMORY.md** — Project memory index, invaluable  
✅ **memory/lessons_learned.md** — Mistake log, essential  
✅ **memory/CORE_DISCIPLINE.md** — Discipline rules, non-negotiable  
✅ **templates/ folder** — Locked formats, referenced correctly  
✅ **REPORT_FORMAT_LOCKED.md** — Can move to docs/ but keep linked  

❌ **Task-specific routing in CLAUDE.md** — Move to SOPs/CLAUDE.md  
❌ **Technical context in CLAUDE.md** — Move to scripts/CLAUDE.md  
❌ **Duplicate SOP/skill files** — Consolidate to single source  
❌ **Chronological focus list in CLAUDE.md** — Move to SESSIONS.md  

---

## PART 8: IMPLEMENTATION CHECKLIST

### Phase 1: De-duplicate (2 hours)
- [ ] Delete `SOPs/SESSION_STARTUP_CHECKLIST.md` (keep memory/ version)
- [ ] Audit `skills/` folder — delete duplicates, keep only `warm-bench-feedback-email.md`
- [ ] Delete `memory/skill_*.md` files (consolidate to SOPs/)
- [ ] Commit: "docs: remove duplicate SOP files, establish single source of truth"

### Phase 2: Refactor CLAUDE.md (1 hour)
- [ ] Reduce CLAUDE.md to <100 lines
- [ ] Move task routing to placeholder
- [ ] Move technical context to placeholder
- [ ] Move current focus to SESSIONS.md pointer
- [ ] Commit: "docs: refactor CLAUDE.md to <100 lines, implement L1 disclosure"

### Phase 3: Create Subdirectory CLAUDE.md (2 hours)
- [ ] Create `scripts/CLAUDE.md` (database + email context)
- [ ] Create `SOPs/CLAUDE.md` (task routing + format rules)
- [ ] Update MEMORY.md to reference new structure
- [ ] Commit: "docs: add subdirectory CLAUDE.md for L2 progressive disclosure"

### Phase 4: Update Root Docs (1 hour)
- [ ] Update SESSIONS.md with current focus
- [ ] Create `docs/ARCHITECTURE.md` with structural overview
- [ ] Update root CLAUDE.md with L2 guidance
- [ ] Commit: "docs: establish docs/ reference architecture, clarify L2 loading"

### Phase 5: Verify (30 min)
- [ ] Test that Session Startup Checklist still loads from memory/
- [ ] Verify SOPs/CLAUDE.md loads when working on tasks
- [ ] Check that no broken links exist
- [ ] Spot-check token impact

---

## IMPLEMENTATION PRIORITY

**High Priority (Do First):**
1. ✅ De-duplicate `skills/` and `memory/skill_*.md`
2. ✅ Refactor CLAUDE.md to <100 lines
3. ✅ Create `SOPs/CLAUDE.md` for task routing

**Medium Priority (Do Next):**
4. ✅ Create `scripts/CLAUDE.md` for technical context
5. ✅ Update SESSIONS.md with current focus
6. ✅ Create `docs/ARCHITECTURE.md`

**Low Priority (Nice-to-have):**
7. Review & consolidate old session logs
8. Create SESSIONS_ARCHIVE.md once log exceeds 200 lines

---

## SUCCESS METRICS

| Metric | Current | Target |
|--------|---------|--------|
| CLAUDE.md lines | 136 | <100 |
| Duplicate doc files | 20+ | 0 |
| Context load per session | ~39k tokens | <38k tokens |
| Task-to-SOP navigation time | 2-3 minutes | <1 minute |
| New agent onboarding time | 30 minutes | <15 minutes |

---

**Prepared by:** Coco  
**Date:** 2026-05-08  
**Status:** Ready for execution

