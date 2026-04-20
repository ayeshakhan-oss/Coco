# Memory Leakage Analysis: Why Coco Forgets Formats, Tone & Templates

**Date:** 2026-04-20  
**Issue:** Agent forgets report structures, email tone, screening templates, and formatting rules—even after corrections.  
**Root Cause:** CRITICAL INFRASTRUCTURE GAP — No programmatic link between scripts and memory system.

---

## EXECUTIVE SUMMARY

**The Problem:**
- Memory exists ✓ (in `/c/Users/Dell/.claude/projects/C--Agent-Coco/memory/`)
- SOPs exist ✓ (in `C:\Agent Coco\skills/*.md` and `C:\Agent Coco\SOPs/`)
- CLAUDE.md exists ✓ (locked-in rules documented)
- **BUT:** Python scripts and Claude during task execution have **ZERO programmatic access** to this information

**Why Coco Forgets:**
1. **Scripts are isolated** — Send scripts (`send_job26_*.py`, `send_gwc_*.py`) contain hardcoded data, no memory loading
2. **No prompt injection** — Claude receives no context about locked formats/tone when generating content
3. **No runtime reference** — When Coco generates an email body or report, it doesn't consult memory files
4. **Memory is session-only** — Loaded at conversation start, but not available to:
   - Python scripts executing independently
   - Task generation systems
   - Template rendering engines

---

## CURRENT ARCHITECTURE (What Exists)

### ✓ Memory System (Session-Level)
```
Location: /c/Users/Dell/.claude/projects/C--Agent-Coco/memory/
Files: 25+ markdown files with locked-in rules
Index: MEMORY.md (loaded into Claude context at session start)
Type: YAML frontmatter format with rule + Why + How to Apply
Access: Manual — Claude reads at session start only
```

**Memory Types:**
- `email_template_format_FINAL.md` — Email structure locked
- `feedback_*.md` — Formatting/tone rules (PDF justify, no em dashes, etc.)
- `execution_discipline_protocol.md` — Work discipline
- `hackathon_gwc_*_final.md` — Specific project outputs (emails, analysis)

### ✓ Skills/SOPs (Document-Level)
```
Location: C:\Agent Coco\skills/*.md and C:\Agent Coco\SOPs/*/
Files: CV screening, GWC rejection emails, case studies, values feedback, etc.
Type: Markdown with step-by-step procedures
Access: Manual — Claude reads before starting task
Example: cv-screening.md (8-step SOP with format locking rule)
```

### ✓ CLAUDE.md (Project Instructions)
```
Location: C:\Agent Coco\CLAUDE.md
Type: Master project instructions + current focus + locked rules
Content: Execution discipline, screening standards, email preferences, SOP references
Access: Loads at start of conversation
```

### ✗ Python Scripts (ISOLATED)
```
Location: C:\Agent Coco\scripts/jobs/*/send_*.py
Structure: Hardcoded data, no memory loading
Example: send_job26_screening_report_final.py
- Lines 24-65: Hardcoded SHORTLIST data
- No imports from memory system
- No format validation against SOP
- No tone checking against locked email format

Problem: Script runs independently of memory/SOP system
```

### ✗ Settings/Hooks (CONFIGURED BUT UNUSED)
```
Location: C:\Agent Coco\.claude\settings.local.json
Type: Claude Code harness config
Current: Only specific Bash permissions allowed
Missing: No hooks to:
  - Load memory before task execution
  - Validate format against SOP before sending
  - Inject locked formats into prompt
```

---

## THE CORE PROBLEM: THREE LEAKAGE POINTS

### **LEAKAGE #1: Scripts Run in Isolation**

Scripts (`send_*.py`) hardcode content and execute without consulting memory:

```python
# send_job26_screening_report_final.py (Line 24-65)
SHORTLIST = [
    {'id': 1064, 'name': 'Muhammad Abdullah...', 'match': '95%', ...}
    # Hardcoded. No SOP reference. No format validation.
]

# Missing:
# - No import of CLAUDE.md rules
# - No reference to skills/cv-screening.md
# - No check against email_template_format_FINAL.md
# - No validation against job26_soul_architect_final.md memory
```

**Impact:** When user says "fix the format", the correction lives in memory but script still hardcodes old format.

---

### **LEAKAGE #2: No Memory Loader in Task Generation**

When Coco generates a report or email, it:

1. ✓ Reads memory at session start
2. ✓ References memory in responses to user
3. ✗ **Does NOT** load memory into prompt when generating task content

**Example:** Generating a CV screening report:
- User: "Screen these 50 CVs for Job 36"
- Coco should: Load memory + SOP + CLAUDE.md + locked format + prior reference
- Coco actually: Generates based on conversation context alone
- **Result:** Format drifts, tone shifts, template forgotten

---

### **LEAKAGE #3: No Hook System for Format Enforcement**

`.claude/settings.local.json` has permission hooks but NOT:
- Pre-generation format validators
- Memory context injection before writing emails
- Post-generation checklist runners
- SOP compliance checks

Missing hooks like:
```json
{
  "hooks": {
    "beforeEmailGeneration": "load_memory_context(['email_template_format_FINAL.md', 'feedback_email_rules.md'])",
    "beforeReportGeneration": "load_sop('cv-screening.md', 'Step 8: Format Locking')",
    "afterGeneration": "run_8_item_qa_checklist()"
  }
}
```

---

## SYMPTOMS: How This Manifests

### **Symptom 1: Format Regression**
- User corrects email format (locked)
- Next email: Old format returns
- Why: Memory has update, but no mechanism injects it into generation prompt

### **Symptom 2: Tone Shift**
- GWC rejection email tone locked as "warm, mentoring"
- Next batch: Becomes clinical, loses warmth
- Why: `feedback_email_rules.md` exists but not loaded during generation

### **Symptom 3: Template Forgotten**
- User provides "reference format" (Job 26 screening)
- Next job screening: Different structure, wrong order
- Why: Memory has `project_job26_soul_architect_final.md` but Claude doesn't inject it into generation context

### **Symptom 4: SOP Steps Skipped**
- CV screening SOP has 8 steps (read JD, read CVs, assess experience, etc.)
- User returns: "You didn't read the full CV again"
- Why: `skills/cv-screening.md` is a document but not embedded in Claude's generation instructions

---

## TECHNICAL ROOT CAUSE

### **Disconnection 1: Session vs Runtime**
Memory loads at **session start** but is needed at **task runtime**:

```
Session Start:
├─ MEMORY.md loads into context ✓
├─ User asks for task
└─ Claude reads memory ✓

Task Execution (Email Generation):
├─ Claude generates email body
├─ NO memory re-injection ✗
├─ User receives output with format drift
└─ Memory stays fresh, output stale ✗
```

### **Disconnection 2: Conversation vs Code**
Memory is accessible to **conversation** but not to **Python scripts**:

```
Conversation:
├─ Claude has memory context
├─ Can reference "locked format"
└─ User sees correct reasoning ✓

Python Script Execution:
├─ Script runs with hardcoded data
├─ No link to memory or SOP files
├─ Generates output independent of constraints
└─ Output may violate locked format ✗
```

### **Disconnection 3: Documentation vs Enforcement**
Rules are **documented** but not **enforced**:

```
memory/email_template_format_FINAL.md ← Rule written
CLAUDE.md ← Rule emphasized
skills/gwc-rejection-emails.md ← Rule defined
        ↓
        ✗ No system enforces compliance
        ↓
Output ignores rule anyway
```

---

## WHAT SHOULD EXIST (But Doesn't)

### **Missing: Memory Injection System**
A mechanism that loads memory into every generation task:

```python
# Missing in current architecture:

def generate_email_with_memory(candidate, role):
    # Load memory context
    memory = load_memory([
        'email_template_format_FINAL.md',
        'feedback_email_rules.md',
        f'project_{role}_final.md'  # Reference format
    ])
    
    # Inject into prompt
    system_prompt = f"""
    You are Coco generating a rejection email.
    
    LOCKED FORMAT (non-negotiable):
    {memory['email_template_format_FINAL.md']}
    
    TONE RULES:
    {memory['feedback_email_rules.md']}
    
    REFERENCE (use as exact baseline):
    {memory[f'project_{role}_final.md']}
    
    Generate email following ALL above rules exactly.
    """
    
    return generate_with_prompt(system_prompt, candidate)
```

### **Missing: Pre-Send Validation**
Scripts should validate before sending:

```python
# Missing in current scripts:

def safe_send_with_validation(email_body, role, format_type):
    # Load expected format
    expected_format = load_memory(f'{format_type}_format.md')
    
    # Validate
    checks = [
        has_correct_header(email_body, expected_format),
        has_locked_tone(email_body, expected_format),
        has_required_sections(email_body, expected_format),
        # 8-item QA checklist from Execution Discipline Protocol
    ]
    
    if not all(checks):
        raise ValidationError(f"Format violation. Expected:\n{expected_format}")
    
    return safe_sendmail(email_body)
```

### **Missing: SOP Embedding**
SOPs should be embedded in Claude's system instructions:

```
Missing from system prompt at task start:
1. Load current CLAUDE.md
2. Load relevant SOP file (skills/*)
3. Load locked-in memory (feedback_*.md)
4. Inject as system rules (not conversational context)
5. Add to mandatory checklist before sending
```

---

## WHERE THE LEAKAGE OCCURS

### **During Report Generation:**
1. User: "Generate a CV screening report for Job 36"
2. Claude reads memory at start ✓
3. Claude generates report from conversation context ✗
4. Report format drifts from `project_job32_decision_brief_format.md`
5. User: "This doesn't match the Job 32 format you used before"
6. Memory updated, but next time → same drift (cycle repeats)

### **During Email Writing:**
1. User: "Draft rejection emails for Job 36 candidates"
2. Claude has `email_template_format_FINAL.md` in memory ✓
3. Claude generates email text ✗ (not injected into generation instructions)
4. Email missing blue header, has em dashes, wrong tone
5. User corrects; Coco reads correction into memory
6. Next batch of emails → same mistakes (no enforcement mechanism)

### **During Script Execution:**
1. Python script `send_job26_screening_report_final.py` runs
2. Script hardcodes SHORTLIST and formatting
3. Script has NO link to `skills/cv-screening.md` or memory
4. User sees output that violates locked format
5. User corrects in memory
6. Script still runs with old hardcoded logic (isolated)

---

## IMPACT ASSESSMENT

### **What This Explains:**
✓ Report structure forgotten (no SOP injection into generation)  
✓ Email tone drifts (no locked rules in generation prompt)  
✓ Screening templates revert (no memory-based validation)  
✓ Format regressions same day (correction in memory, not in execution)  
✓ Scripts run independently (no memory loader)  
✓ Hardcoded data ignored corrections (scripts isolated from memory)

### **What This Does NOT Explain:**
- Individual capability issues (Claude can generate correct formats if instructed)
- User misunderstanding (Coco has rules, just not injected)
- Laziness or skipping (architecture prevents proper enforcement, not user choice)

---

## RECOMMENDATION

The agent's memory system is **well-organized** but **disconnected from execution**.

Fix needed: **Memory Injection + Enforcement Infrastructure**

1. **System Prompt Injection** — Load memory files into prompt at task start
2. **Pre-Send Validation** — Check output against locked rules before delivery
3. **SOP Embedding** — Inject relevant SOP steps into generation instructions
4. **Hook System** — Configure `.claude/settings.local.json` to enforce checks
5. **Script Integration** — Make Python scripts memory-aware (load + validate)

Without this, memory will continue to grow (more rules documented) while execution continues to forget (rules not injected).

---

## FILES AUDIT

### Memory Files Exist (Good):
- `email_template_format_FINAL.md` — Email structure
- `execution_discipline_protocol.md` — Work discipline + 8-item QA checklist
- `feedback_email_rules.md` — Tone + voice rules
- `feedback_pdf_formatting.md` — PDF format rules
- `project_job26_soul_architect_final.md` — Reference format
- `hackathon_gwc_all_6_final.md` — Sample output

### Scripts Are Isolated (Problem):
- `send_job26_screening_report_final.py` — Hardcoded, no memory link
- `send_gwc_warm_tone_v8.py` — Hardcoded, no SOP reference
- `send_job36_report_pdf.py` — No validation against `email_template_format_FINAL.md`
- All scripts: Zero imports from memory system

### Hooks Not Configured (Problem):
- `.claude/settings.local.json` — Only permission allowlists, no enforcement hooks
- No pre-generation memory injection
- No post-generation validation
- No SOP compliance checks

---

## CONCLUSION

**Coco doesn't have a memory problem. Coco has a memory-injection problem.**

The memory system is sophisticated and well-maintained. The execution system is disconnected from it. Rules are documented but not enforced. Corrections are saved but not applied to future tasks.

**Solution:** Bridge the gap with system prompt injection, validation hooks, and SOP embedding. Make the agent load and enforce memory at task runtime, not just at session start.
