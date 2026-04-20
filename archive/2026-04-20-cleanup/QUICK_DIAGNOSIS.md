# Quick Diagnosis: Why Coco Forgets Formats & Tone

## The Problem in 30 Seconds

```
Memory exists ✓              Scripts are isolated ✗
Rules documented ✓           Rules not injected ✗
Corrections saved ✓          Corrections not enforced ✗
History tracked ✓            History not consulted ✗

Result: Agent forgets same rules repeatedly
        even after corrections
```

---

## Three Leakage Points

### 1. **Scripts Run in Isolation**
```
send_job26_screening_report_final.py
├─ Hardcoded SHORTLIST data (line 24-65)
├─ Hardcoded HTML formatting
├─ Zero imports from memory or SOP
└─ Problem: Even if memory updated, script still hardcoded
```

### 2. **No Memory Injection into Generation**
```
Task: "Generate rejection email"
     ↓
Claude context loaded at session start ✓
     ↓
Claude generates from conversation alone ✗
     ↓
Output ignores email_template_format_FINAL.md
     ↓
User sees format drift
```

### 3. **No Enforcement Hooks**
```
.claude/settings.local.json
├─ Permission rules: YES
├─ Format enforcement: NO
├─ Pre-send validation: NO
├─ Memory injection: NO
└─ Problem: Rules exist but nothing enforces them
```

---

## Real Example: Format Regression

**Day 1:**
```
User: "Wrong format — should have blue header like Job 32"
Coco: Corrects format
Memory: Updated email_template_format_FINAL.md ✓
```

**Day 2:**
```
User: "Generate Job 35 rejection emails"
Coco: Reads memory at session start ✓
      Generates email without injecting locked format ✗
      Output has wrong format again
User: "You just fixed this yesterday!"
```

**Why it repeats:**
- Memory was updated (day 1)
- But no mechanism injects memory into email generation (day 2)
- Claude has memory context (background knowledge)
- But email body generation doesn't use it (foreground task)
- Result: Rules known but not applied

---

## What Needs to Change

### **Current Flow (Broken):**
```
Session Start
    ↓
Load MEMORY.md ✓
    ↓
Claude reads memory ✓
    ↓
User asks for task
    ↓
Claude generates WITHOUT re-injecting memory ✗
    ↓
Output ignores locked rules
    ↓
User corrects, memory updated
    ↓
Next task: Same cycle repeats ✗
```

### **Needed Flow (Fixed):**
```
Session Start
    ↓
Load MEMORY.md + CLAUDE.md + relevant SOP

User asks for task (e.g., "reject emails")
    ↓
Load task-specific memory:
├─ email_template_format_FINAL.md
├─ feedback_email_rules.md
├─ project_[role]_final.md (reference format)
└─ Inject into system prompt ← KEY FIX
    ↓
Generate with locked rules in context
    ↓
Validate against rules BEFORE sending
    ↓
Output matches locked format
```

---

## Files That Should Be Connected But Aren't

| File | Location | Used? | Problem |
|------|----------|-------|---------|
| `email_template_format_FINAL.md` | Memory | No | Not injected into generation |
| `feedback_email_rules.md` | Memory | No | Not loaded during email writing |
| `execution_discipline_protocol.md` | Memory | No | 8-item QA checklist not enforced |
| `cv-screening.md` | Skills/ | No | 8-step SOP not embedded in prompts |
| `send_job26_*.py` | Scripts | Hardcoded | No link to memory or SOP |
| `CLAUDE.md` | Root | Loads at start | Not re-injected per task |
| `.claude/settings.local.json` | Config | Permissions only | No enforcement hooks |

---

## The Fix (Short Version)

### **What needs to happen:**

1. **Memory Loader** — Load `email_template_format_FINAL.md` + `feedback_*.md` + relevant SOP into prompt BEFORE task generation
2. **Prompt Injection** — Embed locked rules as system instructions, not conversational context
3. **Validation Hook** — Check output against locked format BEFORE sending
4. **SOP Embedding** — When user says "screen CVs", auto-inject `skills/cv-screening.md` Step 8 (format locking rule)
5. **Script Integration** — Make `send_*.py` scripts memory-aware (load rules, validate output)

### **Why this works:**
- Memory goes from "background knowledge" → "execution constraint"
- Rules go from "documented" → "enforced"
- Corrections go from "saved" → "applied"

---

## Who's Responsible?

| Component | Owner | Issue |
|-----------|-------|-------|
| Memory files | User + Coco | Well-maintained, good index ✓ |
| SOP documentation | User + Coco | Complete and clear ✓ |
| CLAUDE.md rules | User | Comprehensive ✓ |
| **Memory injection system** | **Needs building** | **Architecture gap** ✗ |
| **Validation hooks** | **Needs building** | **Missing entirely** ✗ |
| **Script integration** | **Needs building** | **Isolated scripts** ✗ |

**Not a user problem. Not a Coco capability problem. Infrastructure gap.**

---

## Bottom Line

Your memory system is **world-class**. Your execution system is **disconnected from it**.

The agent documents rules perfectly but executes without consulting the documentation. It's like having a detailed instruction manual that nobody reads during the task.

**Solution: Make the agent READ the manual during task execution, not just at the start.**
