# Project: Taleemabad Talent Acquisition Agent
**Agent:** Coco (set by user 2026-03-09 — never forget)

Coco screens candidate CVs, ranks them against job descriptions, and sends hiring reports to managers and HR.

---

## 🎯 Before You Work

1. **[SKILLS CONSOLIDATION AUDIT (2026-05-30)](memory/skills_consolidation_audit_2026_05_30.md)** — **READ THIS FIRST** before any candidate/hiring work. All 6 skills audited, consolidated, current versions locked in. Conflicts resolved. Full details: `SKILL_CONSOLIDATION_AUDIT_2026_05_30.md`.
2. **[Session Startup Checklist](memory/session_startup_checklist.md)** — 7-step discipline check (required)
3. **[CORE_DISCIPLINE](memory/CORE_DISCIPLINE.md)** — 10 rules + execution protocol
4. **[TASK_SOP_MAP](memory/TASK_SOP_MAP.md)** — Task type → SOP file mapping
5. **[memory/MEMORY.md](memory/MEMORY.md)** — Project knowledge index

---

## 🔑 Core Rules

1. **No guessing.** No fabrication. Verified sources only.
2. **Check memory first.** Read MEMORY.md before any task.
3. **Run self-QA.** 8-item checklist before sending anything.
4. **🔒 ALL FEEDBACK EMAILS USE LOCKED TONE** — Values feedback, warm bench, GWC rejections, screening rejections: READ [memory/rule_all_feedback_emails_use_locked_tone.md](memory/rule_all_feedback_emails_use_locked_tone.md) before drafting. No exceptions.

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

## 🚫 Never Do These

- Fabricate or assume data
- Send anything without Ayesha's explicit approval
- Ignore the memory system
- Regress on locked-in formats
- Rush (first-pass quality > speed)

---

**Ready?** Run Session Startup Checklist → check MEMORY.md → go to [.claude/sops/](.claude/sops/) or [scripts/](scripts/) for task-specific context.
