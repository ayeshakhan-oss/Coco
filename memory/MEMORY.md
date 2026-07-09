# MEMORY INDEX — Coco (Real Files Only)

**Last Updated:** 2026-06-08  
**Status:** HOOKS & HARNESS COMPLETE — Automated validation harness implemented for all 4 email types. 5 phases complete, all code live, settings.json wired. Prevents 5 historical regressions. 300-600x faster validation. Production ready.

---

## 🔴 CRITICAL LEARNING — PILOT RECIPIENTS (2026-06-08)
- **[CRITICAL: PILOT RECIPIENTS ONLY AYESHA (2026-06-08)](CRITICAL_LEARNING_pilot_recipients_only_ayesha_2026_06_08.md)** — 🔒 **ABSOLUTE RULE:** When sending [PILOT – ] emails, TO = ayesha.khan@taleemabad.com ONLY. No CC. No hiring@. No other recipients. This was a discipline failure on 2026-06-08. Add HARD BLOCK to harness. Never deviate.

## 🔒 LOCKED — OPENING LINE + NO FUTURE-PROMISE (2026-06-18)
- **[Mandatory Opening Line + No Future-Promise (2026-06-18)](mandatory_opening_line_no_future_promise_2026_06_18.md)** — All 4 candidate-comms emails MUST open with `This is not a yes for now.` (first line after salutation; harness HARD BLOCK). No future-outreach promises ("we will reach out / keep your name on file") — express welcome as disposition + candidate-initiated (harness WARNING). Wired into harness, templates, CLAUDE.md Rule 10, master philosophy Rules 10-11, SKILL.md, RULES.md, webapp.

## 🆕 NEW — KEEP-IN-TOUCH NOTE (invite type #5, 2026-06-19)
- **[Keep-in-Touch Note — invite type #5 (2026-06-19)](keep_in_touch_note_type_2026_06_19.md)** — Post-conversation warm hold: we already spoke, the role is being revisited, the candidate is still in our thinking. Lives under **Skill 06 (candidate invites)**, NOT rejection/feedback — so the "This is not a yes for now." opener does NOT apply. **TWO HARD RULES:** (1) NO booking button / no links — we are not asking them to schedule anything yet; (2) NO promise or commitment — no "we will reach out", no hard date, no outcome mention; honest + conditional only (a soft "hopefully in July" hope is OK if the user asks). Script: `scripts/send_keep_in_touch_pilot.py` (parameterized `CANDIDATES` list, pilots to Ayesha, sends individual live emails). First use: 5 Job 32 fundraising exploratory-call candidates (Falah, Kanooz, Nirmal, Mushahid, Saadia), sent live 2026-06-19.

---

## 🔴 MUST READ THESE FIRST (Session Start + Every Task)

### Core Discipline (_core/)
- [CORE_DISCIPLINE.md](_core/CORE_DISCIPLINE.md) — **SINGLE SOURCE:** All 10 rules + execution protocol. Read before any task.
- [SELF_QA_CHECKLIST.md](_core/SELF_QA_CHECKLIST.md) — **8 ITEMS REQUIRED:** Run before submitting ANY work.
- [TASK_SOP_MAP.md](_core/TASK_SOP_MAP.md) — **TASK REFERENCE:** Maps each task to its SOP + template + checklist.
- [Session Startup Checklist](_core/session_startup_checklist.md) — 7-step check (run at session start)

### Non-Negotiable Rules (2026-05-12 + 2026-05-30 UPDATES)
- **[RULE — All Feedback Emails Use Locked Tone](rule_all_feedback_emails_use_locked_tone.md)** — 🔒 VALUES FEEDBACK + WARM BENCH + GWC REJECTIONS + ALL CANDIDATE EMAILS must follow locked tone. No exceptions. Read before ANY rejection/feedback email.
- **[WARM BENCH EMAILS — LOCKED RULES (2026-05-30)](warm_bench_locked_rules_2026_05_30.md)** — 🔒 CRITICAL CORRECTIONS. Never mention interviewer names. Never use internal jargon (GWC, values, scorecard). Use exact heading format. Start with "This is not a yes for now." Reference: Fatima Saeed email (May 15). **READ BEFORE EVERY WARM BENCH EMAIL.**
- **[CANDIDATE COMMUNICATION QUALITY REVIEW PROTOCOL (2026-05-30)](candidate_communication_quality_review_protocol_2026_05_30.md)** — 🔒 10-point checklist + Haroon Yasin balance rule. Balance praise specificity with decision specificity. Avoid generic labels. No "good candidate"—use character observations. **RUN BEFORE SENDING ANY CANDIDATE EMAIL.**
- **[AVOID RECRUITING ABSTRACTIONS (2026-05-30)](candidate_communication_avoid_recruiting_abstractions_2026_05_30.md)** — 🔒 CRITICAL. Replace all generic recruiting phrases ("good candidate", "strong profile", "not a good fit") with observed behaviors and concrete realities. Candidate must feel "They SAW me" not "They SCORED me." **APPLIES TO ALL CANDIDATE EMAILS.**
- **[NO INTENT INFERENCE IN REJECTION EMAILS (2026-06-01)](lesson_no_intent_inference_rejection_emails_2026_06_01.md)** — 🔒 CRITICAL PRINCIPLE. Never tell candidates what they assumed, believed, thought, preferred, or were energized by. Use observations + unanswered questions instead. Replace "you assumed X" with "what left us uncertain was X". Eliminates mind-reading, keeps emails mentoring not prosecutorial. **SCAN FOR INTENT-WORDS BEFORE EVERY REJECTION EMAIL.**
- **[CV REJECTION = APPLICATION ONLY + "WE" VOICE (2026-07-09)](lesson_cv_rejection_no_interaction_2026_07_09.md)** — 🔒 CRITICAL. Rule 13: a `cv_rejection` had NO interview/call/conversation — never fabricate one ("conversations and assessments", "we spoke", "what we observed"); ground everything in the written application. Rule 12: collective "we" voice, never "I"/"my"/"me". Both harness HARD BLOCKS + drafting prompt. **APPLIES TO EVERY CV REJECTION.**
- **[EVIDENCE-BASED REJECTION RATIONALE — HAROON YASIN BALANCE RULE (2026-06-01)](lesson_evidence_based_rejection_rationale_2026_06_01.md)** — 🔒 COMPLEMENTARY TO INTENT-INFERENCE RULE. Praise specificity must approximately equal decision specificity. For every detailed praise example, provide equally detailed gap example. Use "Can you show me?" test: if candidate can't point to exact moment that led to decision, rationale is too abstract. Rewrite with concrete behaviors, not mental state assumptions.

---

## SESSION TRACKING (Per-Session)

### Active Session & Lessons (_session/)
- [Lessons Learned Log](_session/lessons_learned.md) — Structured append-only log: date, task, mistake, correction, rule. Updated by Stop hook. Max 50 entries.
- [Active Session Scratchpad](_session/session_active.md) — Live notes for current session: task, decisions, mistakes, files modified. Wiped at session start.
- **[Session — CPD Coach Warm Bench COMPLETE (2026-05-15)](_session/session_cpd_coach_warmBench_complete_2026_05_15.md)** — All 3 emails processed: Hajra (values+GWC) + Unzeela (values+GWC, jargon corrected) + Fatima (GWC-only). Hajra live sent successfully. Unzeela pilot already sent (prior session). Fatima ready for live send. Subject lines locked: "The Principal's Expressions Changed When Data Spoke" (Hajra), "When Difficult Things Become Safer" (Unzeela), "When Personal Experience Becomes Professional Calling" (Fatima). Key learning: remove internal jargon (GWC terminology, scorecard language) from warm bench emails — use observational tone only. All locked formatting enforced. Status: ✅ PRODUCTION READY.

---

## 🎯 SKILLS (Production Ready)

### Candidate Communication — MASTER INDEX (2026-06-08) 🔒
- **[CANDIDATE COMMUNICATION LOCKED INDEX (2026-06-08)](CANDIDATE_COMMUNICATION_LOCKED_INDEX_2026_06_08.md)** — 🔒 **START HERE FOR ALL CANDIDATE EMAILS.** Single source of truth for GWC rejections, warm bench, values feedback, all candidate communication. Points to correct locked versions ONLY. Supersedes all old/duplicate versions. Clarifies potential confusion points (where does P.S. go? which template? what colors?). Reference case: Hira Abbasi (2026-06-08). **No more confusion. No more back-and-forth.**

### 🔒 LOCKED LAYOUT (2026-06-10) — applies to ALL candidate communication
- **[v8 Candidate Comms Layout — LOCKED (2026-06-10)](v8_candidate_comms_layout_LOCKED.md)** — 🔒 **THE visual layout for every candidate communication email** (CV rejection, values feedback, warm bench, GWC, + any future type). Single shared module `scripts/utils/v8_template.py` (H/SUB/P/PS/FOOTER/wrap/attach_logo/EYEBROW). Never redefine inline. Spec: #f0f4f0 canvas, 620px card, Georgia 15px/1.8 justified, #1565c0 blue + #1b5e20 green, embedded cid logo, P.S. box. Ayesha approved via Syeda values feedback (2026-06-10). NOT for Skill 06 invites. Reference impl: send_cpd_coach_values_feedback_syeda_2026_06_10_pilot.py.

### Sub-Resources (Use via Master Index Above)
- **[GWC REJECTION LOCKED APPROACH (2026-06-08)](gwc_rejection_locked_approach_2026_06_08.md)** — Complete locked approach for GWC rejections using warm bench structure.
- **[WARM BENCH LOCKED RULES (2026-05-30)](warm_bench_locked_rules_2026_05_30.md)** — 13 locked rules for warm bench emails.
- **[P.S. SECTION STYLING LOCKED (2026-06-08)](ps_section_styling_locked_2026_06_08.md)** — Premium personal styling for postscript sections (ALL candidate emails).

### Individual Skills
- **[06_candidate-invites (2026-05-14)](../skills/06_candidate-invites/SKILL.md)** — Universal skill for ALL interview invites + opportunity emails. 4 types: Values Interview Invite, Case Study Debrief Invite, Exploratory Call Invite, Warm Bench Opportunity Invite. Design 100% locked (see locked templates). Reference scripts: send_values_interview_pilot.py, send_case_study_debrief_pilot.py, send_exploratory_call_pilot.py, send_warm_bench_invite_pilot.py. Workflow: customize script → pilot to Ayesha → approval → live send.

### Third-Party Skills
- **[UI/UX Pro Max — Install Notes (2026-06-15)](ui_ux_pro_max_skill_install.md)** — General UI/UX design-intelligence skill (NextLevelBuilder, MIT). Installed at `.claude/skills/ui-ux-pro-max/`, **vendored local-only (gitignored)** — reinstall via `npx uipro-cli init --ai claude`. 🔴 CRITICAL: every reinstall wipes the Windows `python3`→`python` + path patch in `SKILL.md` — re-apply it. Locked v8/invite designs OVERRIDE it (CLAUDE.md Rule 9). Local CSV engine, no network calls.

---

## 🎯 MASTER REFERENCE (NEW — 2026-05-08)

### Consolidated Rules & Skills
- **[RULES.md](../RULES.md)** — **MASTER REFERENCE** (20.8 KB). Consolidates all 7 skills, locked approaches, discipline rules, and integration requirements into single authoritative source. Read this instead of scattered files. Includes:
  - 7 Core Discipline Rules
  - 7 Skill-Specific Rules (CV Screening, Rejection Emails, Warm Bench, Attendance Reports, Interview Invites, Decision Briefs, Talent Sourcing)
  - Locked Approaches (exact specs for each skill)
  - Integration & Testing Rules
  - Discrepancy Minimization table

---

## 🛡️ AUTOMATION & VALIDATION (2026-06-08 — THREE-LAYER SYSTEM)

### Three-Layer Pre-Draft Enforcement (Solves Ayesha's Feedback)
- **[THREE-LAYER PRE-DRAFT ENFORCEMENT (2026-06-08)](three_layer_pre_draft_enforcement_2026_06_08.md)** — ✅ COMPLETE. Prevents bad drafts at SOURCE, not at send time. **LAYER 1 (Draft Time):** UserPromptSubmit hook auto-injects locked template HTML + pre-flight checklist when "draft gwc rejection" detected. Can't create custom HTML (template is right there). **LAYER 2 (Pre-Draft Gate):** Mandatory checklist blocks drafting until all items acknowledged (master index read, template read, locked approach understood, 7 BLOCKs acknowledged). **LAYER 3 (Send Time):** PreToolUse hook catches violations. 4 locked templates created (GWC, warm bench, values, CV). Prevents deviation by design. **[Enhanced Hook](scripts/memory/prompt_submit_hook.py)** | **[Pre-Flight Checklist](pre_draft_checklist_2026_06_08.md)**

### Send-Time Validation (Layer 3)
- **[HOOKS & HARNESS IMPLEMENTATION (2026-06-08)](hooks_and_harness_implementation_2026_06_08.md)** — ✅ PHASE 1. Automated validation for all 4 email types (GWC, CV, warm bench, values). 5 phases: eval engine (10 checks), pre-send hook, memory injection (4 new triggers), missing lesson file, CLI tool. 7 HARD BLOCKs block sends. 3 WARNINGs logged. PreToolUse hook wired in settings.json. Prevents 5 historical regressions (PILOT prefix, intent-words, em dashes, word count, names). 300-600x faster validation. **[Impact Analysis](scripts/evals/BEFORE_AND_AFTER_REPORT.md)** | **[Technical Docs](scripts/evals/EVAL_HARNESS_IMPLEMENTATION.md)**

---

## PRODUCTION RULES (Locked & Reference)

### Locked Approaches & Templates (_locked/)
- [Warm Bench Final Locked Approach](_locked/warm_bench_final_locked_approach.md) — Haroon Yasin framework, 800-1100 words, poetic subjects, locked approach.
- **[🔒 Warm Bench Subject Lines - Locked Pattern (2026-05-15)](_locked/warm_bench_subject_lines_locked.md)** — CRITICAL. Subject lines must be poetic, story-based, tied to specific interview moment. Examples: "The Principal's Expressions Changed When Data Spoke" (✅) vs "Hajra Sajjad - CPD Coach Position Update" (❌). Pattern: [MOMENT] + [ACTION/REALIZATION] + [CONSEQUENCE]. Status: 🔒 LOCKED IN.
- [Attendance Report Complete Template](_locked/attendance_report_complete_template.md) — Stat boxes, colors, table structure, PDF/HTML format locked.
- **[🔒 Locked Exploratory Call Invite (2026-05-15)](locked_exploratory_call_invite_approach.md)** — 30-minute calls for candidates without immediate role fit. Body text locked word-for-word. Links (booking + Fundraising Overview doc) locked. Design locked to universal template. Scripts: send_exploratory_call_batch_pilot.py + send_exploratory_call_batch_live.py. Tested with 4 candidates 2026-05-15. Status: ✅ PRODUCTION READY.
- **[🔒 LOCKED Email Template — INTERVIEW INVITES / Skill 06 (2026-05-13, scope narrowed 2026-06-10)](locked_email_template_interview_invites_FINAL_2026_05_13.md)** — INVITES & opportunity emails ONLY (values/case-study/GWC/exploratory invites, round/final/offer, warm bench OPPORTUNITY invites). Design: 775px white card in #e5e7e2 wrapper on #f5f5f5 bg, 34px logo, 17px body, 1.85 line-height. **No longer covers rejections/feedback** — those use the v8 layout (see v8_candidate_comms_layout_LOCKED.md). Conflict resolved by Ayesha 2026-06-10.
- [Values Feedback Email Tone — LOCKED (2026-05-12)](values_feedback_email_tone_locked_2026_05_12.md) — Complete tone guide. Warm, observational, deeply human. NO life-coach language. No internal jargon. 800+ words mandatory. Self-QA checklist included.
- [Locked Templates Index](_locked/locked_templates_index.md) — Quick reference to all locked formats.

---

## SYSTEM ARCHITECTURE & OPTIMIZATION

### Progressive Disclosure Documentation
- [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) — Final architecture after Phase 3. Before/after file counts, context loading flow, single source of truth hierarchy.

### Project Cleanup & Consolidation
- [Project Cleanup Complete (2026-05-08)](../CLEANUP_COMPLETE_2026_05_08.md) — *(DELETED — superseded by RULES.md)* 
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
- [Values Scorecard Duplicate Applications (2026-05-12)](_feedback/values_scorecard_duplicate_applications.md) — **MANDATORY Step 0:** Query all app records before submitting. Markaz UI shows most recent. Submit to correct record or form stays blank. SOP + SQL pattern included.

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
2. Go to RULES.md (root) → Find skill section
3. Read exact locked specifications for that skill
4. Load SOPs/CLAUDE.md (L2 context if needed)
5. Load relevant locked template from _locked/ (if applicable)
6. Check _feedback/ for relevant rules/lessons (feedback docs)
7. Run SELF_QA_CHECKLIST before sending

**When Writing Code:**
1. Load scripts/CLAUDE.md (L2 context)
2. Read relevant data/systems section from RULES.md
3. Load _project/ context (if task-specific)
4. Check scripts/utils/ and scripts/jobs/ for similar code

**When Stuck:**
1. Search _feedback/ for discipline rules / lessons learned
2. Search _project/ for prior work on similar task
3. Check _locked/ for locked approaches that might apply
4. Check RULES.md discrepancy table for common issues

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

**PRIMARY: RULES.md (root)** — All 7 skills, locked specs, discipline rules consolidated.

**SECONDARY: SOPs/** — Skill procedure definitions (reference material).

**TERTIARY: memory/** — Project context, feedback, lessons learned.

After Phase 3 consolidation:
- ✅ RULES.md created (20.8 KB master reference)
- ✅ 21 irrelevant files deleted (audit docs, drafts, duplicates)
- ✅ Zero regressions: all Python scripts compile, integrations tested
- ✅ Single source of truth hierarchy established

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
**Status:** ACTIVE — Phase 3 COMPLETE. RULES.md created. Consolidated all skills. Deleted 21 irrelevant files. Single source of truth established (RULES.md). Zero regressions.  
**Last Action:** Commit 2 (docs: delete irrelevant audit and draft files). Phase 3 testing complete.

