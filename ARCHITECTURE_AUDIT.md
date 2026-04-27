# Architecture Audit — Coco Project (2026-04-20)

**Lens:** AI Agent Primer — Progressive Disclosure Pattern  
**Status:** MESSY — Multiple violations of clean architecture  
**Target:** Single entry point (CLAUDE.md) → nested navigation → lazy loading

---

## PRIMER PRINCIPLES (Quick Recap)

1. **Drawing Room Pattern:** CLAUDE.md is the only file users see upfront. Everything else is deeper.
2. **Progressive Disclosure:** Load info on-demand, not all at once. No 19,200 token upfront load.
3. **Lazy Loading:** Memory → Skills → Docs load only when user needs them.
4. **Clean Root:** Only essentials at root. Everything else nested + hidden.
5. **Single Source of Truth:** No duplicates. No "working files" scattered everywhere.

---

## CURRENT STATE ANALYSIS

### ROOT DIRECTORY — 28 files (SHOULD BE 5-8)

**✅ REQUIRED (Keep at root)**
- CLAUDE.md ← Drawing room (entry point, ONLY router)
- SESSIONS.md ← Session history (users may check)
- REPORT_FORMAT_LOCKED.md ← Critical locked format
- requirements.txt ← Python dependencies
- .env / .gitignore ← Configuration (hidden)
- .mcp.json ← MCP config (hidden)

**⚠️ QUESTIONABLE**
- skills.md ← Master index (OK? or should be in docs/)

**❌ UNWANTED (Archive or delete)**
- ANALYSIS_SUMMARY.txt ← Old analysis (replaced by CLAUDE.md)
- DEPLOYMENT_READY.txt ← Status notice (belongs in SESSIONS.md)
- FORMAT_LOCK_SUMMARY_2026-04-20.txt ← Duplicate of REPORT_FORMAT_LOCKED.md
- VISUAL_DIAGRAMS.txt ← Diagrams (should be in docs/)
- token*.json (4 files) ← **SECURITY RISK** — credentials should be in .env only
- send_soul_architect_pilot_*.py ← Script (should be in scripts/jobs/job26/)
- soul_architect_*.* (5 files) ← Outputs (should be in output/)
- CLAUDE.md.old-full, memory.md.old-broken ← Archives (belong in archive/)

---

## CRITICAL PROBLEM AREAS

### 1. CREDENTIALS LEAK (SECURITY RISK) 🔴

**Files at root:**
```
token.json
token_gmail.json
token_gmail_labels.json
token_sheets.json
data/credentials.json
```

**Issue:** OAuth tokens exposed at root. If git history is public, credentials are leaked.

**Fix:** Move ALL to .env file (single source of truth for secrets)
```
# In .env:
GMAIL_TOKEN=...
SHEETS_TOKEN=...
# etc.

# Then add to .gitignore:
token*.json
data/credentials.json
```

---

### 2. TEMP/ FOLDER (8 working files scattered)

```
Temp/cv_*.txt              ← Individual CV extracts
Temp/*_invite_check.txt    ← Screening intermediate
Temp/extraction_summary.txt ← Processing output
```

**Should be:** Either in `scripts/jobs/[job-id]/` or archived.

---

### 3. DATA/ FOLDER (confused purpose)

```
data/credentials.json      ← Credentials (move to .env)
data/job32_*.json         ← Outputs (move to output/job32/)
data/job36_*.json         ← Outputs (move to output/job36/)
data/nain_tara_cv.txt     ← Individual CV (move to scripts/jobs/)
```

**Should be:** Deleted after consolidation.

---

### 4. SOUL_ARCHITECT_CVS_DECODED/ (orphaned folder)

Extracted CV files with no clear home. Should be in `scripts/jobs/job26/` or archived.

---

### 5. OUTPUT/ FOLDER (mixed purposes)

```
output/
├─ job26_screening_results.json    ← FINAL (keep)
├─ job32_merged.json               ← INTERMEDIATE (move to scripts/jobs/job32/)
├─ extracted_cvs.json              ← INTERMEDIATE (move to scripts/jobs/job26/)
├─ zain_ocr.txt                    ← CV TEXT (move to scripts/jobs/job32/)
├─ nano_banana_creative_brief.txt  ← CV TEXT (move to scripts/jobs/job32/)
└─ sourcing/                       ← CORRECT (keep as-is)
```

**Should be:** Only FINAL reports in output/. Intermediate in scripts/jobs/[id]/.

---

## CLEAN ARCHITECTURE TARGET

```
Coco/
├─ CLAUDE.md                    ← Drawing room entry point ONLY
├─ SESSIONS.md
├─ REPORT_FORMAT_LOCKED.md
├─ requirements.txt
├─ .env                         ← Credentials ONLY (hidden)
├─ .gitignore
├─ .mcp.json
│
├─ memory/                      ← Lazy load on-demand
│  ├─ MEMORY.md
│  ├─ session_startup_checklist.md
│  └─ (9 other files)
│
├─ docs/                        ← Reference docs (lazy load)
│  ├─ TEAM_ONBOARDING_CHECKLIST.md
│  ├─ schema.md
│  └─ VISUAL_DIAGRAMS.txt
│
├─ SOPs/                        ← Skills (lazy load)
│  └─ (5 categories of SOPs)
│
├─ context/
├─ config/
├─ scripts/                     ← Implementation
│  ├─ jobs/
│  │  ├─ job26/
│  │  │  ├─ scripts/
│  │  │  ├─ outputs/          ← Job-specific outputs
│  │  │  └─ extracted_cvs/    ← Working files
│  │  ├─ job32/
│  │  └─ job36/
│  ├─ reports/
│  ├─ sourcing/
│  └─ utils/
│
├─ output/                      ← FINAL REPORTS ONLY
│  ├─ job26/
│  ├─ job32/
│  ├─ job36/
│  └─ sourcing/
│
└─ archive/                     ← Historical (never touched)
   ├─ 2026-04-20-cleanup/
   └─ (organized by date)
```

---

## CLEANUP ROADMAP

### PHASE 1: SECURITY (15 min) — CRITICAL
- [ ] Move token*.json secrets to .env
- [ ] Move data/credentials.json to .env
- [ ] Delete token*.json from root
- [ ] Update .gitignore to exclude credentials

### PHASE 2: Archive Status Files (10 min)
- [ ] ANALYSIS_SUMMARY.txt → archive/
- [ ] DEPLOYMENT_READY.txt → archive/
- [ ] FORMAT_LOCK_SUMMARY_2026-04-20.txt → archive/
- [ ] CLAUDE.md.old-full → archive/2026-04-20-cleanup/
- [ ] memory.md.old-broken → archive/2026-04-20-cleanup/

### PHASE 3: Relocate Working Files (30 min)
- [ ] Temp/ folder → scripts/jobs/[id]/ or archive/
- [ ] data/ folder → appropriate destinations or archive/
- [ ] soul_architect_cvs_decoded/ → scripts/jobs/job26/ or archive/
- [ ] soul_architect_* outputs → scripts/jobs/job26/outputs/

### PHASE 4: Consolidate Output/ (20 min)
- [ ] Organize by job: output/job26/, output/job32/, output/job36/
- [ ] Move intermediate files to scripts/jobs/[id]/
- [ ] Keep only FINAL REPORTS in output/

### PHASE 5: Verify & Commit (15 min)
- [ ] Check CLAUDE.md still works (links valid)
- [ ] Verify no credentials at root
- [ ] Verify scripts/ imports still work
- [ ] Commit changes

**Total Time:** ~2.5 hours  
**Difficulty:** LOW (mostly moving files)  
**Risk:** MEDIUM (must not break imports, must handle credentials carefully)

---

## WHAT THIS ACHIEVES (vs. Primer)

| Principle | Now | After |
|-----------|-----|-------|
| **Entry Point** | 28 confusing files at root | ONLY CLAUDE.md visible |
| **Progressive Disclosure** | OK (memory/SOPs work) | Better (root is clean) |
| **Token Cost (upfront)** | Higher (navigate clutter) | Lower (clear path) |
| **User Experience** | "Where do I start?" | "Open CLAUDE.md" |
| **Security** | Credentials leaked | Credentials in .env only |
| **Maintainability** | Hard (scattered files) | Easy (organized structure) |

---

## SUCCESS CRITERIA

✅ **Root directory:** 8 files (CLAUDE.md, SESSIONS.md, REPORT_FORMAT_LOCKED.md, requirements.txt, .env, .gitignore, .mcp.json, skills.md)  
✅ **No credentials at root:** All secrets in .env  
✅ **Organized scripts/:** jobs/, reports/, sourcing/, utils/  
✅ **Organized output/:** Only FINAL reports, organized by job  
✅ **Archived clutter:** All old/working files in archive/  
✅ **All links work:** CLAUDE.md still navigates correctly  

---

**Ready to execute Phases 1-5?** This will take ~2.5 hours and make the project dramatically cleaner.
