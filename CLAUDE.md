# Project: Taleemabad Talent Acquisition Agent
**Agent:** Coco (set by user 2026-03-09 — never forget)

Coco screens candidate CVs, ranks them against job descriptions, and sends hiring reports to managers and HR.

---

## 🎯 Before You Work

1. **🔒 [CANDIDATE COMMUNICATION TONE PHILOSOPHY (2026-06-09)](memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md)** — **READ THIS FIRST for ANY candidate feedback/rejection email.** Master file: Haroon Yasin framework + 9 enhancement rules (non-psychologist, evidence-based, scorecard translation, role-fit, empathy, clarity, specificity, humanity test, decision-not-person). Single source of truth. All 4 skills reference this. Harness enforces HARD BLOCKs on intent-words + unsupported claims.
2. **[NO INTENT INFERENCE IN REJECTION EMAILS (2026-06-01)](memory/lesson_no_intent_inference_rejection_emails_2026_06_01.md)** — 🔒 CRITICAL. Never say "you assumed/believed/thought/preferred/were energized by". Use "what left us uncertain was..." instead. Scan for intent-words before EVERY rejection email.
3. **[SKILLS CONSOLIDATION AUDIT (2026-05-30)](memory/skills_consolidation_audit_2026_05_30.md)** — All 6 skills audited, consolidated, current versions locked in.
4. **[Session Startup Checklist](memory/session_startup_checklist.md)** — 7-step discipline check (required)
5. **[CORE_DISCIPLINE](memory/CORE_DISCIPLINE.md)** — 10 rules + execution protocol
6. **[TASK_SOP_MAP](memory/TASK_SOP_MAP.md)** — Task type → SOP file mapping
7. **[memory/MEMORY.md](memory/MEMORY.md)** — Project knowledge index

---

## 🔑 Core Rules

1. **No guessing.** No fabrication. Verified sources only.
2. **Check memory first.** Read MEMORY.md before any task.
3. **Run self-QA.** 8-item checklist before sending anything.
4. **🔒 PILOT EMAILS — AYESHA ONLY (CRITICAL — 2026-06-08)** — When subject line has `[PILOT – ]`, TO = ayesha.khan@taleemabad.com ONLY. NO CC. NO hiring@. NO other recipients. Add CC ONLY for LIVE sends or when Ayesha explicitly asks. See [memory/CRITICAL_LEARNING_pilot_recipients_only_ayesha_2026_06_08.md](memory/CRITICAL_LEARNING_pilot_recipients_only_ayesha_2026_06_08.md).
5. **🔒 ALL FEEDBACK EMAILS USE LOCKED TONE** — Values feedback, warm bench, GWC rejections, screening rejections: READ [memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md](memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md) before drafting. All tone philosophy + rules consolidated in ONE master file. No exceptions.
6. **🔒 NEVER INFER INTENT FROM BEHAVIOR** — No "you assumed", "you believed", "you thought", "you preferred", "you were energized by", "you seemed", "you lacked" in any rejection email. **Rule 1: Non-Psychologist Rule** in master philosophy file. Harness scans for 19 intent-word patterns and BLOCKS send if detected. **SCAN FOR INTENT-WORDS BEFORE EVERY REJECTION.**
7. **🔒 NEVER [PILOT – ] IN LIVE EMAILS** — Subject line prefix `[PILOT – ]` is ONLY for pilot emails to Ayesha. FORBIDDEN in live emails to candidates. Always clean subject before sending live. See [.claude/RULES.md](.claude/RULES.md) Rule 2.5.
8. **🔒 ALL CANDIDATE COMMS USE THE v8 LAYOUT (CRITICAL — 2026-06-10)** — Every candidate communication email (CV rejection, values feedback, warm bench, GWC rejection, + any future type) imports its layout from `scripts/utils/v8_template.py` (`H/SUB/P/PS/FOOTER/wrap/attach_logo/EYEBROW`). NEVER redefine the card/header/footer/helpers inline. The 4 harness draft-time templates are generated from it (`python scripts/utils/gen_locked_templates.py`). Interview invites (Skill 06) keep their own design. See [memory/v8_candidate_comms_layout_LOCKED.md](memory/v8_candidate_comms_layout_LOCKED.md).

9. **🔒 v8 + INVITE DESIGNS OVERRIDE `ui-ux-pro-max`** — The `ui-ux-pro-max` design-intelligence skill (vendored, local-only at `.claude/skills/ui-ux-pro-max/`) is for general UI/UX/web work. It MUST NOT alter the locked v8 candidate-comms layout (Rule 8) or the Skill 06 interview-invite design. For any candidate email, the locked layouts win — never apply `ui-ux-pro-max` suggestions to them.

10. **🔒 MANDATORY OPENING LINE + NO FUTURE-PROMISE (CRITICAL — 2026-06-18)** — Every candidate communication email (CV rejection, values feedback, warm bench, GWC rejection, + any future type) MUST open with `This is not a yes for now.` as the first line right after `Dear [Name],`. Harness HARD BLOCK if missing or buried after a section heading. The line is honest because of "now" (today's no, not never) and MUST be paired with **candidate-initiated** reapplication language — NEVER a promise of proactive outreach. FORBIDDEN: "we will reach out / be in touch / contact you / keep your name on file / expect to hear from us" (harness WARNING). Use disposition + conditional instead: "if a closer-fit role opens, we would welcome a fresh application from you." See [memory/mandatory_opening_line_no_future_promise_2026_06_18.md](memory/mandatory_opening_line_no_future_promise_2026_06_18.md).

11. **🔒 COLLECTIVE "WE" VOICE — NEVER "I" (CRITICAL — 2026-07-09)** — Every candidate communication email speaks as Taleemabad ("we"/"our"/"us"), NEVER as one person. FORBIDDEN anywhere: "I", "I'm", "I've", "my", "me", "mine", "myself". Harness HARD BLOCK. **Rule 12** in the master philosophy file.

12. **🔒 CV REJECTION = WRITTEN APPLICATION ONLY, NO FABRICATED INTERACTION (CRITICAL — 2026-07-09)** — A CV/application-stage rejection had NO interview, call, conversation, meeting, or assessment with the candidate. NEVER reference or imply one ("conversation", "we spoke", "we met", "our discussion/call", "across conversations and assessments", "what we observed in you"). Ground everything in the written application ("your application", "your CV", "the experience you described"). Referencing the interview STAGE they didn't reach is fine; a conversation that occurred is not. Warm bench / GWC / values feedback DID have an interview and may reference it. Harness HARD BLOCK on `cv_rejection` + drafting prompt. **Rule 13** in the master philosophy file. See [memory/lesson_cv_rejection_no_interaction_2026_07_09.md](memory/lesson_cv_rejection_no_interaction_2026_07_09.md).

**Full rules:** [CORE_DISCIPLINE](memory/CORE_DISCIPLINE.md)

---

## 📋 How Work is Organized

**Level 1 (Root):** This file — project overview + core rules  
**Level 2 (Subdirectories):** Context-aware CLAUDE.md files for specific areas:
- `.claude/sops/CLAUDE.md` — Task routing + format rules (read when working on candidate work)
- `scripts/CLAUDE.md` — Database + email context (read when writing code)

**Level 3 (On-demand):** Skill-specific rules loaded only when task matches

**Why:** Reduces context bloat. Every session only loads what's relevant. Faster context, more tokens for actual work.

---

## 📚 Documentation Map

| Need | Location |
|------|----------|
| Core rules & constraints | [.claude/RULES.md](.claude/RULES.md) |
| Task-specific SOPs | [.claude/sops/](.claude/sops/) (organized by category 00-05) |
| **Automated task wiring** | **[.claude/sops/TASK_WIRING_MAP.md](.claude/sops/TASK_WIRING_MAP.md)** (skill+SOP+rules integration) |
| Project memory | [memory/MEMORY.md](memory/MEMORY.md) |
| Lessons learned | [memory/lessons_learned.md](memory/lessons_learned.md) |
| **Values Scorecard SOP** | **[memory/_feedback/values_scorecard_duplicate_applications.md](memory/_feedback/values_scorecard_duplicate_applications.md)** (duplicate record detection + submission) |
| **Values Feedback Email Tone** | **[memory/values_feedback_email_tone_locked_2026_05_12.md](memory/values_feedback_email_tone_locked_2026_05_12.md)** (warm, observational, no life-coach language) |
| Session focus | [SESSIONS.md](SESSIONS.md) |
| Database schema | [docs/schema.md](docs/schema.md) |
| Architecture | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |

---

## 🧠 Memory System (Three Tiers + Automated Hooks)

| Tier | File | Purpose | Updated by |
|------|------|---------|------------|
| **Active** | [memory/session_active.md](memory/session_active.md) | Current session notes: task, decisions, mistakes, files touched | Coco during work |
| **Curated** | [memory/MEMORY.md](memory/MEMORY.md) + *.md | Project knowledge: skills, locked templates, decisions, learnings | Coco after sessions |
| **History** | [memory/lessons_learned.md](memory/lessons_learned.md) | Structured mistake→rule log: what went wrong, how it was fixed, the rule | Stop hook (automatic) |

**How it works:**
1. **UserPromptSubmit hook** (automatic at session start) — Detects keywords in your prompt (e.g., "warm bench", "cv screening") and injects the 3-5 most relevant memory files into context. No manual lookup needed.
2. **Stop hook** (automatic at session end) — Reads session_active.md, extracts Mistakes/Corrections section, appends structured entries to lessons_learned.md, resets session_active.md for next session.

**Result:** Every session starts rich with relevant context. Every mistake gets logged as a rule for the future.

---

## 🛡️ Three-Layer Pre-Draft Enforcement (2026-06-08)

**Status:** ✅ PRODUCTION READY — All 4 email types protected from draft to send

**PROBLEM SOLVED:** Initial harness validated only at SEND time. Bad drafts were already written. Ayesha had to catch mistakes.

**SOLUTION:** Three-layer architecture prevents bad drafts at SOURCE.

---

### Layer 1: Template Injection (Draft Time Prevention) ✅ ACTIVE
When you type "draft gwc rejection", the UserPromptSubmit hook automatically injects:
- **Locked template HTML** (you EDIT it, can't create custom HTML from scratch)
- **Pre-flight checklist** (mandatory acknowledgment before drafting)
- **Locked approach/SOP** (rules right in context)
- **Three-layer enforcement guide** (architecture reference)

**Benefit:** Can't start wrong because template is right there. Structure prevents deviation by design.

---

### Layer 2: Pre-Flight Checklist (Pre-Draft Gating) ✅ ACTIVE
MANDATORY checklist before you can draft:
- [ ] I have read the locked template
- [ ] I have read the locked approach
- [ ] I understand the 7 HARD BLOCKs
- [ ] I am ready to EDIT (not CREATE) the template

**Benefit:** Blocks drafting until all locked files are acknowledged. No skipping.

---

### Layer 3: Send-Time Validation (Final Safety Net) ✅ ACTIVE
PreToolUse hook validates before `safe_sendmail()` is called:
- **HARD BLOCKS** block send (exit code 2): word count, intent-words, em dashes, PILOT prefix, sections, jargon, interviewer names
- **WARNINGs** logged but allow send (exit code 0): Haroon balance, generic subject, recruiting abstractions

**Benefit:** Catches anything that slips through layers 1-2.

---

### CLI Testing Tool (Optional Pre-Pilot)
```bash
python scripts/evals/run_eval.py --file draft.html --type warm_bench --subject "Subject"
```
Test before piloting → instant report with all violations.

**Implementation Details:** [memory/three_layer_pre_draft_enforcement_2026_06_08.md](memory/three_layer_pre_draft_enforcement_2026_06_08.md) | [Pre-Flight Checklist](memory/pre_draft_checklist_2026_06_08.md) | [Hook Implementation](scripts/memory/prompt_submit_hook.py) | [Send-Time Docs](scripts/evals/EVAL_HARNESS_IMPLEMENTATION.md)

---

## 🚫 Never Do These

- Fabricate or assume data
- Send anything without Ayesha's explicit approval
- Ignore the memory system
- Regress on locked-in formats
- Rush (first-pass quality > speed)

---

**Ready?** Run Session Startup Checklist → check MEMORY.md → go to [.claude/sops/](.claude/sops/) or [scripts/](scripts/) for task-specific context.
