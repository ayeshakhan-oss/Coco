---
title: Six-Skill Consolidation Audit
date: 2026-05-30
status: COMPLETE
---

# SKILL CONSOLIDATION AUDIT — FINAL REPORT

**Audit Date:** 2026-05-30  
**Scope:** All 6 core hiring + candidate skills  
**Status:** ✅ COMPLETE — No conflicts found. All skills ready for production.

---

## SKILL 1: CANDIDATE COMMUNICATION (01_candidate-communication)

### Summary
Handles all candidate rejection and feedback emails across stages: CV rejections, values interview feedback, warm bench feedback, and GWC rejections.

### Architecture
- **Current Location:** `.claude/skills/01_candidate-communication/SKILL.md`
- **Related SOPs (source of truth):** `SOPs/01_Candidate_Communication/` (orchestrated from main skill)
- **Status:** ✅ PRODUCTION READY

### What Stayed the Same
- ✅ Email types (CV rejection, values feedback, warm bench, GWC rejection) — unchanged since inception
- ✅ 800+ word minimum for all types — locked rule
- ✅ "We" voice, they/them pronouns — consistent tone requirement
- ✅ Pilot to Ayesha FIRST (+ Jawad for values) — approval workflow unchanged
- ✅ No em dashes in body — typography rule stable
- ✅ Evidence-based feedback — citation requirement unchanged
- ✅ v8 HTML design for all types — format locked

### What Was Updated
1. **WARM BENCH FRAMEWORK (2026-05-04):**
   - Old approach: Role-specific future flagging ("Consider similar roles at Taleemabad")
   - New approach: Warm welcome for future applications (Haroon Yasin framework)
   - Change: From directive → observational, from prescriptive → warm
   - Memory: `warm_bench_final_locked_approach.md`

2. **LOCKED TONE GUIDE (2026-05-12):**
   - New enforcement rule: ALL feedback emails (values, warm bench, GWC, rejections) MUST follow locked tone
   - Tone rules: Warm, observational, deeply human, NO life-coach language
   - Memory: `rule_all_feedback_emails_use_locked_tone.md` + `values_feedback_email_tone_locked_2026_05_12.md`

3. **SUBJECT LINE PATTERNS (2026-05-15):**
   - Warm bench subjects must be poetic, story-based, tied to specific interview moment
   - ✅ "The Principal's Expressions Changed When Data Spoke" 
   - ❌ "Hajra Sajjad - CPD Coach Position Update"
   - Memory: `warm_bench_subject_lines_locked.md`

### What Was Removed
- ❌ Old role-specific warm bench approach (pre-2026-05-04) — superseded by Haroon framework
- ❌ Generic tone guidance — replaced by locked tone guide (2026-05-12)

### Final Active Workflow
**The 6-Step Process (CURRENT):**
1. **Identify Email Type:** CV rejection, values feedback, warm bench, or GWC rejection
2. **Read Locked Resources:** MEMORY.md + RULES.md + locked tone guide + specific template
3. **Read Source Material:** Full CV, interview notes, or transcript (no skimming)
4. **Write Once, Correctly:** Single-pass correctness with evidence in every section
5. **Run 8-Item Self-QA Checklist:** All items must pass before next step
6. **Pilot & Approve:** Send to Ayesha (+ Jawad for values), wait for approval, then go live

**Non-Negotiable Rules (LOCKED):**
- 800+ words MANDATORY (verified count)
- Every observation cited from CV or interview
- "We" voice (never "I")
- No em dashes (replace with period/comma/colon)
- v8 HTML design (locked format)
- Pilot to Ayesha FIRST (never direct to candidate)
- Warm bench subjects: poetic + story-based
- Locked tone: warm, observational, no prescriptive advice

---

## SKILL 2: CANDIDATE EVALUATION (02_candidate-evaluation)

### Summary
Evaluate candidates across CV screening, case study evaluation, values interview scoring, and KCD evaluation. Produce detailed reports with ranking and recommendations.

### Architecture
- **Current Location:** `.claude/skills/02_candidate-evaluation/SKILL.md`
- **Related SOPs (source of truth):** `SOPs/02_Candidate_Evaluation/` (orchestrated from main skill)
- **Status:** ✅ PRODUCTION READY

### What Stayed the Same
- ✅ 14-15k character minimum for CV screening — locked capacity rule
- ✅ 4 stat boxes + profiles + maybe table format — report structure unchanged
- ✅ All hyperlinks to Google Drive CVs — non-negotiable usability rule
- ✅ Skills → Experience → Fit evaluation priority — consistent methodology
- ✅ No fabrication, all claims sourced — verification discipline constant
- ✅ Pilot to Ayesha first — approval workflow unchanged
- ✅ 8-item self-QA checklist — execution discipline stable

### What Was Updated
1. **MARKAZ DUPLICATE CHECK (Step 0, 2026-05-12):**
   - New requirement: Query all application records BEFORE submitting scorecard
   - Why: Markaz UI shows most recent record; submitting to wrong record leaves form blank
   - Memory: `values_scorecard_duplicate_applications.md`

2. **STAT BOX MATH VERIFICATION (Reinforced 2026-05-12):**
   - Rule: Stat box count MUST equal section header count
   - Example: 4 stat boxes = 4 sections (screened, top-tier, maybe, advanced)
   - Why: Prevents careless errors and ensures data matches headers
   - Enforcement: Math check in self-QA checklist

3. **CV HYPERLINK COMPLETENESS (2026-04-08, 2026-05-12):**
   - Rule: EVERY candidate name in report MUST link to Google Drive CV
   - Audit all before sending (no exceptions)
   - Memory: `feedback_decision_brief_hyperlinks.md`

### What Was Removed
- ❌ Manual CV truncation (pre-2026-04-10) — replaced with "min 10k chars" rule
- ❌ Ambiguous status language (pre-2026-05-12) — use specific language ("Calendar not locked" vs "TBC/Pending")

### Final Active Workflow
**The 8-Step Process (CURRENT):**
1. **Identify Evaluation Type:** CV screening, case study, values scoring, or KCD
2. **Read Locked Resources:** MEMORY.md + RULES.md + locked template
3. **Gather Source Material:** All CVs, submissions, notes (nothing assumed)
4. **Evaluate Systematically:** Skills → Experience → Fit (in order)
5. **Structure Report:** Stat boxes + profiles + maybe table
6. **Verify Hyperlinks & Data:** Every name linked, stat count = section count
7. **Run 8-Item Checklist:** All items must pass
8. **Pilot & Approve:** Send to Ayesha, wait for approval

**Non-Negotiable Rules (LOCKED):**
- 14-15k character MINIMUM (never truncate <10k)
- All candidate names hyperlinked to Drive CVs (non-negotiable)
- Stat boxes = section header count (math verification)
- No fabrication (all claims sourced from CV or submission)
- Evaluation criteria: Skills → Experience → Fit (priority order)
- Markaz Step 0: Query all app records before submitting scorecard
- No CV truncation or skimming (full context required)
- Pilot to Ayesha first

---

## SKILL 3: HIRING OPERATIONS (03_hiring-operations)

### Summary
Manage operational reporting and workforce tracking: attendance reports, decision briefs, and hiring pipeline monitoring.

### Architecture
- **Current Location:** `.claude/skills/03_hiring-operations/SKILL.md`
- **Related SOPs (source of truth):** `SOPs/03_Hiring_Operations/` (orchestrated from main skill)
- **Status:** ✅ PRODUCTION READY

### What Stayed the Same
- ✅ 7 stat boxes for attendance reports — structure unchanged
- ✅ 4 stat boxes for decision briefs — report structure stable
- ✅ All CV names hyperlinked — non-negotiable for decision briefs
- ✅ Teams + Markaz verification required — data accuracy discipline consistent
- ✅ No fabrication (verified sources only) — fundamental rule unchanged
- ✅ Pilot to Ayesha first — approval workflow unchanged
- ✅ 8-item self-QA checklist — execution discipline stable

### What Was Updated
1. **GRID BORDERS RULE (2026-05-12, Repeated):**
   - **CRITICAL FIX:** Ayesha corrected multiple times — use ROWBACKGROUNDS only, NO GRID attribute
   - Why: "Not the pattern" feedback from user. Tables must not have grid borders visible.
   - Memory: Noted in `skill_hiring_operations_sop.md` and Session 004 discipline failures
   - Impact: Affects all attendance and decision brief tables

2. **COLOR CODES LOCKED (2026-05-12):**
   - Exact hex codes frozen (no approximations):
     - Header: #34495e (dark)
     - Onsite: #e8f5e9 (green)
     - Leave: #ffe0b2 (orange)
     - WFH: #c8e6c9 (light green)
     - Away: #ffccbc (salmon)
     - Flagged: #ffcdd2 (red)
     - Additional: #f5f5f5 (gray)
   - Memory: `attendance_report_complete_template.md`

3. **TEAMS API INCOMPLETENESS RULE (2026-04-15, Ongoing):**
   - When Teams returns <5 results, verify with Markaz manually before assuming complete
   - Example: Teams returned 1 leave announcement, but Markaz had 5 pending
   - Why: API may have limits or incomplete coverage
   - Memory: `discipline_failure_teams_api_incomplete.md`

4. **STATUS FIELD CLARIFICATION (2026-05-12):**
   - status='offer' is a STAGE in pipeline, NOT a sent offer
   - Never assert without verification; flag to Ayesha if unclear
   - Memory: `feedback_db_status_vs_pipeline.md`

### What Was Removed
- ❌ Vague status language like "TBC/Pending" — replaced with specific language
- ❌ Grid borders on tables — now explicitly forbidden

### Final Active Workflow
**The 9-Step Process (CURRENT):**
1. **Identify Operation Type:** Attendance report, decision brief, or pipeline monitor
2. **Read Locked Resources:** MEMORY.md + RULES.md + locked template
3. **Gather Data:** Teams + Markaz (cross-verified)
4. **Verify Against Ground Truth:** Small datasets verified manually
5. **Structure Report:** Stat boxes + sections with hyperlinks (if decision brief)
6. **Apply Exact Formatting:** Colors from locked template, ROWBACKGROUNDS only (no grid)
7. **Verify Structure:** Stat count = section count (math check)
8. **Run 8-Item Checklist:** All items must pass
9. **Pilot & Approve:** Send to Ayesha (+ Jawad for pipeline monitor)

**Non-Negotiable Rules (LOCKED):**
- 7 stat boxes for attendance (exact colors locked)
- 4 stat boxes for decision briefs
- NO GRID BORDERS (use ROWBACKGROUNDS only) — CRITICAL
- Stat count = section header count (math verification)
- All CV names linked to Drive (decision briefs only)
- Colors match exactly (#34495e, #e8f5e9, etc.) — no approximations
- Data verified (Teams + Markaz cross-checked)
- Small API results (<5) verified manually with Markaz
- status='offer' is a stage, not a sent offer (flag if unclear)
- Pilot to Ayesha first

---

## SKILL 4: DATA AND SYSTEMS (04_data-and-systems)

### Summary
Manage backend infrastructure for database queries, email systems, reporting, analytics, and security protocols.

### Architecture
- **Current Location:** `.claude/skills/04_data-and-systems/SKILL.md`
- **Related SOPs (source of truth):** `SOPs/04_Data_and_Systems/` (orchestrated from main skill)
- **Status:** ✅ PRODUCTION READY

### What Stayed the Same
- ✅ MCP ONLY (never direct DB connection) — fundamental security rule
- ✅ safe_sendmail() bouncer ONLY (never smtplib) — email security unchanged
- ✅ Audit logging mandatory — accountability discipline constant
- ✅ OAuth tokens current (not expired) — security requirement stable
- ✅ .env protected (.gitignore) — credential management unchanged
- ✅ No hardcoded credentials — security best practice constant
- ✅ 8-item self-QA checklist — execution discipline stable

### What Was Updated
1. **RULE 1.12 (MCP Mandatory, 2026-05-12):**
   - Locked in: Always access Markaz data via `mcp__neon-postgres__query()`
   - Never ask "where is the candidate data?" — use MCP
   - Memory: `general_non_negotiable_sops.md`

2. **RULE 1.13 (Email Via safe_sendmail, 2026-05-12):**
   - Locked in: Always send emails via `safe_sendmail()` from `scripts/utils/safe_send.py`
   - Never use smtplib directly
   - Memory: `general_non_negotiable_sops.md`

3. **SMALL API RESULT VERIFICATION (2026-04-15):**
   - When APIs return suspiciously small result sets (<5), verify with ground truth manually
   - Example: Teams API returned 1 result, but Markaz had 5
   - Why: API limits or incomplete coverage
   - Memory: `discipline_failure_teams_api_incomplete.md`

### What Was Removed
- ❌ Direct database connection patterns — replaced with MCP-only rule
- ❌ smtplib usage examples — replaced with safe_sendmail() pattern

### Final Active Workflow
**The 8-Step Process (CURRENT):**
1. **Identify System Task:** Database query, email system, report generation, analysis, or security
2. **Read System SOP:** MEMORY.md + RULES.md + Integration Rules
3. **Prepare Credentials:** Check .env, verify OAuth tokens current
4. **Write System Code:** MCP query, safe_sendmail, ReportLab, or analysis
5. **Implement Audit Logging:** log_db_query() and log_email_send() calls
6. **Verify Results:** Small datasets verified manually, APIs cross-checked
7. **Test (Local):** Compile, run, verify audit logs
8. **Deploy with Caution:** Pilot first, log all operations, monitor errors

**Non-Negotiable Rules (LOCKED):**
- MCP ONLY (never direct psycopg2) — Rule 1.12
- safe_sendmail() ONLY (never smtplib) — Rule 1.13
- Audit logging MANDATORY (all queries and emails)
- Results verified against ground truth
- OAuth tokens current (not expired)
- .env protected (.gitignore enforced)
- No hardcoded credentials in code
- Error handling implemented
- Fallback plan for API unavailability
- Small API results (<5) verified manually

---

## SKILL 5: TALENT SOURCING (05_talent-sourcing)

### Summary
Find passive candidates through systematic 3-layer research, verify LinkedIn links, draft personalized outreach, and add to Markaz only after confirmed interest.

### Architecture
- **Current Location:** `.claude/skills/05_talent-sourcing/SKILL.md`
- **Related SOPs (source of truth):** `SOPs/05_Talent_Sourcing/` (orchestrated from main skill)
- **Status:** ✅ PRODUCTION READY

### What Stayed the Same
- ✅ 3-layer search (org pages → Google → LinkedIn) — methodology unchanged
- ✅ Personalized DMs ONLY (not templated) — engagement quality requirement constant
- ✅ Ayesha sends DMs (not Coco) — workflow delegation stable
- ✅ 40-60 candidates minimum per round — sourcing volume consistent
- ✅ Excel output with methodology — documentation requirement unchanged
- ✅ Tier categorization (1/2/3) — prioritization system stable
- ✅ Source field: 'LinkedIn - Sourced' — tracking unchanged

### What Was Updated
1. **ADOPTION FROM NOAH (2026-04-16):**
   - Coco officially adopted Noah's talent sourcing skill (Jaw901/Noah repository)
   - All previous Coco sourcing versions superseded
   - New canonical version: `memory/talent_sourcing_7steps_complete.md`
   - Memory: `coco_talent_sourcing_skill.md`

2. **MARKAZ TIMING RULE (CRITICAL, 2026-04-16):**
   - NEVER add to Markaz before interest confirmed
   - Wait for explicit "yes" response from candidate
   - This addresses prior discipline issues (premature insertion)
   - Memory: Locked in via `talent_sourcing_7steps_complete.md` Step 7

### What Was Removed
- ❌ Coco's old sourcing approaches (4+ versions deleted 2026-05-08)
- ❌ Speculative Markaz insertion patterns — now explicitly forbidden

### Final Active Workflow
**The 7-Step Process (CURRENT — ADOPTED FROM NOAH):**
1. **Intake:** Role definition, persona, keywords, location, experience level
2. **Search Org Pages (Layer 1):** Company websites, LinkedIn company pages
3. **Google site:linkedin.com (Layer 2):** Role-specific keywords and location
4. **Verify Links (Layer 3):** Test each LinkedIn URL, mark dead links
5. **Extract Verified Candidates:** Name, URL, title, company, experience, tier (1/2/3)
6. **Draft Personalized DMs:** Ayesha sends (reference specific project/work)
7. **Add to Markaz (AFTER confirmation):** Wait for explicit YES, then insert with source='LinkedIn - Sourced'

**Non-Negotiable Rules (LOCKED):**
- 3-layer search MANDATORY (no skipping layers)
- LinkedIn links verified as active (test before sending)
- 40-60 candidates MINIMUM per round
- Personalized DMs ONLY (not templated)
- Ayesha sends DMs (Coco drafts only)
- NO premature Markaz insertion (wait for confirmation)
- Excel output with methodology
- Candidates tiered (1=perfect, 2=good, 3=possible)
- Source field: 'LinkedIn - Sourced'
- All 7 steps executed in order

---

## SKILL 6: CANDIDATE INVITES (06_candidate-invites)

### Summary
Send interview invites and candidate communication emails for all stages: Values Interview Invite, Case Study Debrief Invite, Exploratory Call Invite, Warm Bench Opportunity Invite.

### Architecture
- **Current Location:** `.claude/skills/06_candidate-invites/SKILL.md`
- **Related Memory:** `memory/locked_email_template_interview_invites_FINAL_2026_05_13.md` (design spec)
- **Status:** 🔒 LOCKED FOR PRODUCTION (2026-05-15)

### What Stayed the Same
- ✅ 4 invite types (values, case study, exploratory, warm bench) — types unchanged
- ✅ Pilot to Ayesha FIRST — approval workflow constant
- ✅ Table-based HTML (Gmail compatibility) — structure requirement stable
- ✅ Logo embedding (CID inline) — technical requirement unchanged
- ✅ All links clickable and tested — link quality requirement constant

### What Was Updated
1. **DESIGN LOCKED PERMANENTLY (2026-05-13):**
   - Design spec frozen: colors, fonts, spacing, layout
   - NO DEVIATIONS PERMITTED going forward
   - Content-only adaptability (greeting + body text change per stage)
   - Memory: `locked_email_template_interview_invites_FINAL_2026_05_13.md`

2. **SKILL CREATED & CONSOLIDATED (2026-05-15):**
   - New unified skill consolidating all 4 invite types
   - Previously scattered across individual scripts
   - Now centralized with locked design spec and README
   - Status: PRODUCTION READY as of 2026-05-15

3. **EXPLORATORY CALL LOCKED (2026-05-15):**
   - Body text locked word-for-word
   - Links locked (booking + Fundraising Overview)
   - Tested 4 candidates successfully
   - Memory: `locked_exploratory_call_invite_approach.md`

### What Was Removed
- ❌ Scattered script implementations — now consolidated in one skill
- ❌ Design flexibility — now 100% locked (content-only changes permitted)

### Final Active Workflow
**The 6-Step Process (CURRENT):**
1. **Select Invite Type:** Values Interview, Case Study Debrief, Exploratory Call, or Warm Bench Opportunity
2. **Gather Required Info:** Candidate name, position, links, context
3. **Customize Script:** Set variables (CANDIDATE_NAME, POSITION, JD_LINK, BOOKING_LINK, etc.)
4. **Generate Pilot Email:** Run script with PILOT_MODE = True
5. **Get Ayesha's Approval:** She reviews design and content
6. **Send Live:** Change PILOT_MODE = False, run script again

**Design Specification (LOCKED — NO DEVIATIONS):**
- **Colors:** #f5f5f5 (page bg), #e5e7e2 (wrapper), #ffffff (card), #3157b7 (headers), #3d63c8 (links), #5b3fc4 (button)
- **Typography:** Georgia serif only (12px label, 24px title, 17px body, 1.85 line-height)
- **Layout:** 775px white card in grey wrapper on light grey background
- **Logo:** 34px, centered, CID-embedded
- **Signature:** Left-aligned, 1px grey divider above
- **Button:** Purple (#5b3fc4), rounded corners (7px), 16px bold Georgia
- **Structure:** Table-based (Gmail compatibility), no div layout

**Non-Negotiable Rules (LOCKED):**
- Design is 100% LOCKED (no deviations) — content changes only
- Pilot to Ayesha FIRST (never direct to candidate)
- Table-based HTML ONLY (Gmail compatibility)
- All links tested before sending pilot
- Logo 34px, centered, CID-embedded (never external src=)
- Georgia serif ONLY (no modern fonts)
- 30-item self-check before sending pilot
- One CTA button per email (never multiple)
- Signature left-aligned (never centered)
- All special chars as HTML entities

---

## CROSS-SKILL DEPENDENCIES

### Shared Resources
| Resource | Used By | Status |
|----------|---------|--------|
| v8 Email Design | Skills 1, 6 | 🔒 LOCKED (2026-05-13) |
| Warm Bench Framework | Skills 1, 6 | 🔒 LOCKED (2026-05-05) |
| Attendance Report Colors | Skill 3 | 🔒 LOCKED (exact hex codes) |
| CV Screening Format | Skill 2 | 🔒 LOCKED (4 stat boxes + profiles) |
| Locked Tone Guide | Skill 1 (all feedback) | 🔒 LOCKED (2026-05-12) |
| 8-Item Self-QA Checklist | All skills | Mandatory for all types |
| Memory-First Protocol | All skills | Rule 1.1 in all skills |
| Verified Data Only | Skills 2, 3, 4 | Core discipline rule |

### Shared Rules
| Rule | Applies To | Source |
|------|-----------|--------|
| No Fabrication | All skills | RULES.md Core Rule 1 |
| Memory-First (Step 1) | All skills | RULES.md Core Rule 2 |
| Verified Sources Only | Skills 2, 3, 4 | RULES.md Core Rule 3 |
| Pilot to Ayesha FIRST | Skills 1, 3, 6 | RULES.md Core Rule 4 |
| 8-Item Self-QA | All skills | RULES.md Core Rule 5 |
| MCP Only (no direct DB) | Skill 4 | Rule 1.12 (2026-05-12) |
| safe_sendmail() Only | Skill 4 | Rule 1.13 (2026-05-12) |

---

## CONFLICTS IDENTIFIED & RESOLVED

### None Found ✅
All six skills have been audited for conflicts. No contradictions exist between:
- Current skill definitions and memory updates
- Multiple versions of the same skill (only current versions kept)
- Cross-skill dependencies and shared resources
- Core discipline rules and skill-specific rules

**Conflicts that WERE resolved in past sessions:**
1. **Warm Bench Approach (2026-05-04)** — Old role-specific → New Haroon framework ✅ RESOLVED
2. **Grid Borders (2026-05-12)** — Repeated corrections → Now explicitly forbidden ✅ RESOLVED
3. **Tone Guidance (2026-05-12)** — Generic → Locked tone guide ✅ RESOLVED
4. **Subject Lines (2026-05-15)** — Generic → Poetic, story-based ✅ RESOLVED
5. **Talent Sourcing Versions (2026-04-16)** — Multiple Coco versions → Single Noah adoption ✅ RESOLVED

---

## FINAL STATUS SUMMARY

| Skill | Current Version | Status | Last Updated | Conflicts |
|-------|-----------------|--------|--------------|-----------|
| **01_candidate-communication** | `.claude/skills/01_candidate-communication/SKILL.md` | ✅ PRODUCTION READY | 2026-05-15 | None |
| **02_candidate-evaluation** | `.claude/skills/02_candidate-evaluation/SKILL.md` | ✅ PRODUCTION READY | 2026-05-15 | None |
| **03_hiring-operations** | `.claude/skills/03_hiring-operations/SKILL.md` | ✅ PRODUCTION READY | 2026-05-15 | None |
| **04_data-and-systems** | `.claude/skills/04_data-and-systems/SKILL.md` | ✅ PRODUCTION READY | 2026-05-15 | None |
| **05_talent-sourcing** | `.claude/skills/05_talent-sourcing/SKILL.md` | ✅ PRODUCTION READY | 2026-05-15 | None |
| **06_candidate-invites** | `.claude/skills/06_candidate-invites/SKILL.md` | 🔒 LOCKED PRODUCTION | 2026-05-15 | None |

---

## ENFORCEMENT RULES (GOING FORWARD)

When you ask for work, I will:

1. ✅ **Check the relevant skill's current version** (from this audit)
2. ✅ **Follow ONLY that version** (ignore all superseded versions)
3. ✅ **Flag ANY conflicts** (if two instructions contradict, I'll pause and ask)
4. ✅ **Apply all locked rules** (design, tone, colors, structure — no deviations)
5. ✅ **Use only current memory files** (delete old versions from context)
6. ✅ **Never mix old templates with new updates** (single version per skill)
7. ✅ **Verify ground truth before assuming** (especially for small API results)
8. ✅ **Run 8-item self-QA** (mandatory for all types before sending)

---

**CONSOLIDATION COMPLETE — Ready for production work.**
