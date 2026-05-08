# AGGRESSIVE CLEANUP PLAN — Agent Coco Project
**Date:** 2026-05-08  
**Risk Level:** LOW (nothing functionality-critical is deleted)  
**Estimated Savings:** 12.4 MB + 2-3k tokens per session  
**Execution Time:** 2-3 hours

---

## PART A: FILES TO DELETE (NO CONSOLIDATION)

### Section A1: Archive Folder — `archive/2026-04-20-cleanup/` (212 KB)

**ENTIRE FOLDER DELETE:** `C:\Agent Coco\archive\2026-04-20-cleanup\`

**Contents Being Deleted:**
```
archive/2026-04-20-cleanup/
├── add_15_marketing_profiles.py (obsolete)
├── create_15_marketing_profiles_final.py (obsolete)
├── create_15_profiles_complete.py (obsolete)
├── create_candidates_file.py (obsolete)
├── create_marketing_specialists_excel.py (obsolete)
├── INFRASTRUCTURE_FIX_ROADMAP.md (diagnostics from April 20, now consolidated)
├── job26_cv_links.json (historical snapshot, not used)
├── MEMORY_LEAKAGE_ANALYSIS.md (diagnostics, consolidated into lessons_learned.md)
├── MEMORY_LEAKAGE_INDEX.md (diagnostics, consolidated)
├── QUICK_DIAGNOSIS.md (one-off diagnostic)
├── README.md (local folder README)
├── REPORT_GENERATION_INTEGRATION_GUIDE.md (superseded by current patterns)
├── REPORT_LOCKING_SYSTEM_READY.md (historical milestone doc)
├── REPORT_STRUCTURE_LOCKED_FORMAT.md (superseded by REPORT_FORMAT_LOCKED.md in root)
├── SCREENING_REPORT_FORMAT_LOCKED_2026-04-20.md (superseded)
├── SOUL_ARCHITECT_PILOT_READY_TO_SEND.md (historical)
└── SOUL_ARCHITECT_SCREENING_PILOT_SUMMARY.md (historical)
```

**WHY DELETE:**
- Explicitly archived folder from April 20 cleanup
- All diagnostic learnings consolidated into `memory/lessons_learned.md` and `memory/CORE_DISCIPLINE.md`
- Scripts are pre-Job26/Job32 era, no longer used
- No active code references this folder
- Git already excludes `archive/` in `.gitignore` (soft cleanup)

**FUNCTIONALITY IMPACT:** NONE  
**GIT IMPACT:** None (already excluded)  
**MEMORY IMPACT:** None (lessons captured elsewhere)

---

### Section A2: Temp Folder — `Temp/` (6.5 MB - DELETE 90%)

**ENTIRE FOLDER DELETE:** `C:\Agent Coco\Temp\` (EXCEPT `Guide to Feedback/`)

**Contents Being Deleted:**
```
Temp/
├── attendace 8 april 2026 (typo, old file)
├── Attendance/ (duplicate PDFs of attendance reports)
├── Attendance_Record_*.pdf (8 versions, superseded by automated reports)
├── Case Study/ (old case study submissions, archives exist)
├── Case Study Submission/ (renamed version of above)
├── case-studies/ (3 MB — old job folders: Field Coordinator, Fundraising Manager)
├── cv_*.txt (test extraction files from Apr 14 testing)
├── Field Coordinator/ (complete old job project, 1.5 MB)
├── Google Sheet Integration/ (old OAuth template files, we have new setup)
├── Fundraising & Partnerships Manager/ (old job project, 800 KB)
└── [various PDFs and docs from April 2026]
```

**KEEP ONLY:**
```
Temp/
└── Guide to Feedback/ (dated May 5 2026, recent, appears active)
```

**WHY DELETE:**
- `.gitignore` excludes `Temp/`, so folder is not version-controlled anyway
- Old case study submissions have archives in `output/case-studies/` (if needed)
- Field Coordinator and Fundraising Manager are completed jobs; no active scripts reference them
- Attendance PDFs have been superseded by automated report generation
- Google Sheet Integration files are old templates; we now have production setup in `scripts/setup/setup_sheets_token.py`
- CSV test files are debugging artifacts from April 14

**FUNCTIONALITY IMPACT:** NONE (Temp is temporary by definition)  
**GIT IMPACT:** None (excluded)  
**DATA IMPACT:** Old job data is archived if needed; no live data loss

---

### Section A3: Dead Python Scripts — `scripts/jobs/job32/` (150 KB)

**DELETE THESE:**
```
scripts/jobs/job32/
├── send_job32_report_v2.py ← DEAD (v10 is current)
├── send_job32_report_v3.py ← DEAD
├── send_job32_report_v4.py ← DEAD
├── send_job32_report_v5.py ← DEAD
├── send_job32_report_v6.py ← DEAD
├── send_job32_report_v7.py ← DEAD
├── send_job32_report_v8.py ← DEAD
├── send_job32_report_v9.py ← DEAD
├── send_job32_report_pdf.py ← DEAD (superseded by v10.py format)
├── send_job32_shortlist_summary.py ← DEAD (subsumed into v10)
└── send_job32_case_study_report.py ← DEAD (subsumed into v10)
```

**KEEP THESE:**
```
scripts/jobs/job32/
├── send_job32_report_v10.py ← LIVE (current, actively used)
├── send_job32_values_invite.py ← LIVE (interview invites)
├── send_job32_decision_brief_pilot.py ← LIVE (decision briefs)
├── fetch_job32_zeroin_status.py ← LIVE (polling for status)
└── [other active job32 scripts]
```

**WHY DELETE:**
- v2-v9 are explicit iterations; v10 supersedes all
- v2-v9 changes are tracked in git; old files not needed
- No active scripts import from v2-v9
- Grep confirms v10 is referenced in automation, not older versions
- Pattern: each version was a pilot iteration before settling on v10

**FUNCTIONALITY IMPACT:** NONE (only v10 is executed)  
**GIT IMPACT:** Git history preserved; deletion is clean  
**SAFETY:** v10 is in active use (confirmed by recent git commits)

---

### Section A4: Dead Python Scripts — `scripts/jobs/job36/` (50 KB)

**DELETE THESE:**
```
scripts/jobs/job36/
├── send_job36_kcd_report.py ← DEAD (v4 is current)
├── send_job36_kcd_report_v2.py ← DEAD
├── send_job36_kcd_report_v3.py ← DEAD
├── send_job36_rejection_pilot.py ← DEAD (new_batch.py is current)
├── send_job36_rejection_pilot_v2.py ← DEAD
├── send_job36_debrief_invite_pilot.py ← DEAD (live.py is current)
├── send_job36_decision_brief_pilot.py ← DEAD (v3 is current)
├── send_job36_decision_brief_pilot_v2.py ← DEAD
└── [other v1/v2 variants]
```

**KEEP THESE:**
```
scripts/jobs/job36/
├── send_job36_kcd_report_v4.py ← LIVE
├── send_job36_rejection_new_batch.py ← LIVE
├── send_job36_debrief_invite_live.py ← LIVE
├── send_job36_decision_brief_v3.py ← LIVE
└── [other active scripts]
```

**WHY DELETE:**
- Pattern: pilot_*.py → v2.py → v3.py → live.py or final version
- Older variants are deprecated; only latest used in automation
- Git history preserves all versions
- Grep confirms only final versions are called

**FUNCTIONALITY IMPACT:** NONE (only current versions are executed)  
**GIT IMPACT:** Git history preserved  
**SAFETY:** Current versions confirmed in use

---

### Section A5: Data Snapshots (200 KB) — MOVE to `archive/data-snapshots/`

**MOVE THESE TO ARCHIVE (not delete, preserve for reference):**
```
data/
├── job32_new_candidates.json ← Historical snapshot from Job 32 screening
├── job32_new_cvtext.json ← Historical snapshot
├── job36_prescreened.json ← Historical snapshot
├── job36_top25_cvtext.json ← Historical snapshot  
├── job36_case_study_gmail_check.json ← One-off check result
└── extracted/all_candidates_cvs.json ← Historical extraction

output/
├── job32_cvs.json (if not actively used)
├── job32_merged.json (if not actively used — verify one is live)
├── job32_scores.json (if v2 is current)
└── [other versioned JSON snapshots]
```

**WHY MOVE (not delete):**
- These are historical snapshots from completed jobs
- No active scripts read from `data/job32_new_*.json` (verify with grep)
- If needed for reference, they're preserved in archive
- Clearing `data/` folder speeds up directory scans
- Active data should be read directly from Markaz DB or fresh exports

**FUNCTIONALITY IMPACT:** NONE (if scripts use fresh data)  
**GIT IMPACT:** Moving to archive keeps them versioned  
**SAFETY:** Archive preserves them for forensics if needed

---

## PART B: FILES TO CONSOLIDATE (MERGE & DELETE)

### Section B1: Talent Sourcing Memory (4 files → 1 file)

**CONSOLIDATE INTO:** `memory/talent_sourcing_7steps_complete.md` (PRIMARY)

**DELETE THESE:**
```
memory/
├── talent_sourcing_steps_explained.md (duplicate explanation of same 7 steps)
├── coco_talent_sourcing_skill.md (duplicate: "Coco adopted Noah's approach")
├── noah_talent_sourcing_skill.md (duplicate: original Noah docs)
└── noah_skill_talent_sourcing_original.md (duplicate: another Noah version)
```

**WHY CONSOLIDATE:**
- All 4 files document the same 7-step process
- `talent_sourcing_7steps_complete.md` is most comprehensive
- Other 3 files repeat the same information with minor wording differences
- Memory index `MEMORY.md` should reference only the canonical version
- Reduces cognitive load when reading talent sourcing docs

**VERIFICATION:**
- Grep confirms no scripts or code imports specific functions from these files
- MEMORY.md can point to single canonical file
- Session notes don't reference specific file names (they reference "talent sourcing SOP")

**CONSOLIDATION STEPS:**
1. Verify `talent_sourcing_7steps_complete.md` contains all info from other 4
2. Add footnote in canonical file: "Supersedes [list other 3 files]"
3. Delete 4 duplicate files

**FUNCTIONALITY IMPACT:** NONE (single source of truth)  
**MEMORY IMPACT:** Cleaner index  
**GIT IMPACT:** Deletion + footnote in surviving file

---

### Section B2: Hackathon GWC Rejection Emails (6 files → 1 file)

**CONSOLIDATE INTO:** `memory/hackathon_gwc_all_6_final.md` (PRIMARY)

**DELETE THESE:**
```
memory/
├── hackathon_gwc_ali_jawad_final.md (individual email for Ali)
├── hackathon_gwc_umair_solangi_final.md (individual email for Umair)
├── hackathon_gwc_sultan_sheharyar_final.md (individual email for Sultan)
├── hackathon_gwc_ali_jawad_warm.md (pre-consolidation iteration, outdated)
├── hackathon_gwc_final_warm_tone.md (mid-consolidation iteration, outdated)
└── [any other GWC drafts]
```

**KEEP ONLY:**
```
memory/
└── hackathon_gwc_all_6_final.md (contains all 6 candidate details + final PDF location)
```

**WHY CONSOLIDATE:**
- Individual files were created during drafting phase
- `hackathon_gwc_all_6_final.md` is the final, unified version with all 6 candidates
- No active scripts reference individual files
- Individual files serve no purpose now that consolidation is complete
- MEMORY.md should point to single canonical file

**FUNCTIONALITY IMPACT:** NONE (consolidated file has everything)  
**SESSION IMPACT:** Cleaner memory structure  
**GIT IMPACT:** Deletion + pointer to consolidated file

---

### Section B3: Email Template Format Files (2 files → 1 file)

**CONSOLIDATE INTO:** `memory/email_template_format_FINAL.md` (PRIMARY)

**DELETE THESE:**
```
memory/
└── email_template_format_exact.md (superseded by FINAL version)
```

**WHY CONSOLIDATE:**
- FINAL version supersedes exact version
- Only one is needed for reference
- No active scripts reference the old file

**VERIFICATION:**
- Confirm FINAL.md has all info from exact.md
- Grep confirms no code imports specific file name

**FUNCTIONALITY IMPACT:** NONE  
**GIT IMPACT:** Clean deletion

---

### Section B4: Attendance Report Documentation (8 files → 2 files)

**CONSOLIDATE INTO:**
1. `memory/attendance_report_complete_template.md` (template + format)
2. `memory/attendance_report_discipline_session004.md` (lessons learned)

**DELETE THESE:**
```
memory/
├── project_attendance_report_format.md (duplicate: format info)
├── project_attendance_14apr2026_finalized.md (duplicate: finalized format, now in complete_template.md)
├── project_attendance_report_markaz_integration.md (can fold into template)
├── project_attendance_payroll_total.md (specific learning, move to discipline file)
├── project_attendance_permanent_wfh.md (specific rule, move to template)
├── project_attendance_pdf_pattern.md (duplicate: PDF pattern info in template)
└── [any other attendance-specific files]
```

**WHY CONSOLIDATE:**
- Multiple files document overlapping attendance topics
- Template file should contain: format, colors, structure, data sources, WFH rules, payroll calculation, PDF pattern
- Discipline file should contain: lessons learned from April 20 session, what not to do
- Reduces redundancy; single source of truth for template

**FUNCTIONALITY IMPACT:** NONE (same data, fewer files)  
**SESSION IMPACT:** Cleaner memory  
**GIT IMPACT:** Merge content + delete duplicates

---

## PART C: FILES TO KEEP (WITH JUSTIFICATION)

### C1: Core Functionality Scripts (All Production Scripts)

**KEEP ALL:** `scripts/` (except dead versions listed in A3, A4)

**Justification:**
- Contains all active job reporting, invitations, database operations
- No redundancy here; each script serves a specific function
- Job32, Job36, Job35, Job26 have active scripts that execute daily/weekly
- Cron jobs reference these scripts

**No Changes Needed**

---

### C2: SOPs & Skills (All Files)

**KEEP ALL:** `SOPs/` and `skills/`

**Justification:**
- Every SOP is actively referenced in CLAUDE.md or session work
- No duplicates or dead files
- Core to project operations
- User explicitly relies on SOP structure

**No Changes Needed**

---

### C3: Core Memory Files (All Kept)

**KEEP ALL:**
- `memory/MEMORY.md` (index)
- `memory/CORE_DISCIPLINE.md` (10 rules)
- `memory/SELF_QA_CHECKLIST.md` (8-item checklist)
- `memory/lessons_learned.md` (session summaries)
- `memory/session_active.md` (scratchpad)
- `memory/session_startup_checklist.md` (discipline)

**Justification:**
- These are active system files referenced in every session
- No consolidation needed
- Core to Coco's execution discipline

**No Changes Needed**

---

### C4: Project-Specific Memory Files (Selectively Keep)

**KEEP:**
- `memory/project_job26_soul_architect_final.md` (Job 26 completed, reference archive)
- `memory/project_job32_*.md` (Job 32 still active)
- `memory/project_job36_*.md` (Job 36 still active)
- `memory/project_hiring_pipeline_monitor.md` (active system)
- `memory/project_teams_integration.md` (active system)
- `memory/project_security_hardening.md` (active security rules)

**Justification:**
- These track active or recently-completed projects
- No duplicates among these
- Referenced in MEMORY.md index
- Safe to keep as historical record

**No Changes Needed**

---

### C5: Skill Memory Files (All Kept)

**KEEP ALL:**
- `memory/skill_cv_screening_sop.md`
- `memory/skill_case_study_evaluation_sop.md`
- `memory/skill_general_discipline_sop.md`
- `memory/warm_bench_final_locked_approach.md`
- `memory/locked_skill_warm_bench_interview_invite.md`

**Justification:**
- Each documents a locked-in skill/approach
- No redundancy
- Actively referenced before tasks
- MEMORY.md index references all

**No Changes Needed**

---

### C6: Feedback Memory Files (All Kept)

**KEEP ALL:**
- `memory/feedback_*.md` (all 8 files on specific topics)

**Justification:**
- Each documents a specific lesson or constraint
- No consolidation needed
- Actively referenced for specific scenarios

**No Changes Needed**

---

### C7: Git & Config Files (All Kept)

**KEEP ALL:**
- `.git/` (version history)
- `.gitignore` (exclusion rules)
- `CLAUDE.md` (project instructions)
- `.claude/settings.json` (Claude Code config)
- `.claude/settings.local.json` (local overrides)

**Justification:**
- Core project infrastructure
- No changes needed
- Git history is preserved

**No Changes Needed**

---

### C8: Output Folder (Selective Keep)

**KEEP:**
- `output/sourcing/` (active talent sourcing)
- `output/job32/` (active job)
- `output/job36/` (active job)
- `output/job35/` (active job)
- `output/cv_texts_job*/` (CV data for active jobs)
- 1 sample screening PDF from each job (for reference)

**DELETE or ARCHIVE:**
- Historical job PDFs from completed jobs (Job 26, Job 17, etc.)
- Old `output/extracted_cvs.json` and similar one-off extractions
- Duplicate screening results (e.g., job32_cvs.json vs job32_merged.json — keep only current)

**VERIFICATION NEEDED BEFORE DELETION:**
```bash
grep -r "job26_cvs\|job26_merged\|job32_cvs\|job32_merged" scripts/
```
This tells us which version is actually referenced.

**Justification:**
- Active jobs need their data
- Historical job data can be archived
- Duplicates confuse future work

---

### C9: Data Folder (Selective Keep)

**KEEP:**
- `data/credentials.json` (NEW OAuth credentials)
- `data/gmail_token.json` (Gmail auth)
- `data/inbox_scan_results.json` (may be active)

**MOVE to ARCHIVE:**
- `data/job32_new_candidates.json` (historical)
- `data/job32_new_cvtext.json` (historical)
- `data/job36_prescreened.json` (historical)
- `data/job36_top25_cvtext.json` (historical)
- `data/job36_case_study_gmail_check.json` (one-off check)
- `data/extracted/all_candidates_cvs.json` (historical)
- `data/remaining_candidates.json` (unclear if active — verify with grep)

**VERIFICATION NEEDED:**
```bash
grep -r "job32_new_candidates\|job36_prescreened\|remaining_candidates" scripts/
```
If no matches, safe to archive.

**Justification:**
- Data folder should contain only active/current data
- Historical snapshots preserved in archive
- Cleans up directory for active work

---

## PART D: EXECUTION ORDER & SAFETY

### Phase 1: Safe Deletions (No Verification Needed) — 45 min
1. Delete `archive/2026-04-20-cleanup/` (212 KB)
2. Delete `Temp/` (keep `Guide to Feedback/`) (6.5 MB)
3. Delete job32 v2-v9 scripts (150 KB)
4. Delete job36 pilot scripts (50 KB)

**Total Immediate Savings:** 6.9 MB

---

### Phase 2: Consolidations (Merge & Delete) — 1 hour
1. Consolidate talent sourcing memory (4→1)
2. Consolidate hackathon GWC memory (6→1)
3. Consolidate email template format (2→1)
4. Consolidate attendance docs (8→2)

**Total Savings:** 110 KB + cognitive load

---

### Phase 3: Conditional Moves (Requires Verification) — 30 min
1. Run grep to confirm job32/job36 JSON usage
2. Run grep to confirm data/ file usage
3. Move unused data files to `archive/data-snapshots/`
4. Move old job output folders to `archive/completed-jobs/`

**Total Savings:** 5 MB (conditional)

---

### Phase 4: Git Cleanup — 10 min
1. Stage all deletions: `git add -A`
2. Create single commit: `git commit -m "cleanup: remove dead files and consolidate docs"`
3. Verify nothing broke: `git log --oneline` (last 3 commits)

---

## SAFETY CHECKLIST

**Before Execution:**
- [ ] Backup current state: `git stash`
- [ ] Confirm no unsaved work in active sessions
- [ ] Verify all scripts to delete are NOT in active automation/cron

**During Execution:**
- [ ] Run Phase 1 → verify project still works
- [ ] Run Phase 2 → update memory references
- [ ] Run Phase 3 → after grep verification only
- [ ] Run Phase 4 → final commit

**After Execution:**
- [ ] Test key scripts: `python scripts/jobs/job32/send_job32_report_v10.py --dry-run`
- [ ] Verify MEMORY.md index is updated
- [ ] Confirm git log shows clean history
- [ ] No functionality regression

---

## FINAL SUMMARY

| Phase | Action | Files | Savings | Risk | Time |
|-------|--------|-------|---------|------|------|
| **1** | Safe deletes | ~180 | 6.9 MB | ZERO | 45 min |
| **2** | Consolidate | 20 | 110 KB | ZERO | 1 hour |
| **3** | Conditional moves | ~25 | 5 MB | LOW | 30 min |
| **4** | Git commit | 1 | — | ZERO | 10 min |
| **TOTAL** | — | **~225** | **12.0 MB** | **LOW** | **2.5 hours** |

**Token Savings:** ~2-3k tokens per session (cognitive load + index size)  
**Functionality Impact:** NONE (all deletions are dead code or duplicates)  
**Git Preservation:** Full history preserved; clean commit audit trail

---

## READY TO EXECUTE?

Reply with:
- ✅ **APPROVED** — Execute all phases
- 🟡 **MODIFIED** — [list specific changes]
- ❌ **HOLD** — Review more before proceeding
