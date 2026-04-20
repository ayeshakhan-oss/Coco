# Infrastructure Fix Roadmap: Bridging Memory to Execution

## Priority 1: Immediate Fixes (Session-Level)

### Fix 1.1: Create a Memory Loader Function
**Goal:** Load memory files into Claude's system prompt at task start

**Location:** Create `scripts/utils/memory_loader.py`

```python
# memory_loader.py
import os
import json
from pathlib import Path

MEMORY_ROOT = Path.home() / ".claude" / "projects" / "C--Agent-Coco" / "memory"

def load_memory_files(task_type: str) -> dict:
    """
    Load relevant memory files based on task type.
    
    Args:
        task_type: 'email_generation', 'report_generation', 'cv_screening', etc.
    
    Returns:
        dict of {filename: content} with YAML frontmatter parsed
    """
    
    # Define which memory files are relevant for each task
    MEMORY_MAP = {
        'email_generation': [
            'email_template_format_FINAL.md',
            'feedback_email_rules.md',
            'feedback_gmail_thread_reply.md',
        ],
        'gwc_rejection': [
            'email_template_format_FINAL.md',
            'feedback_email_rules.md',
            'hackathon_gwc_all_6_final.md',
            'coco_core_problems_identified.md',
        ],
        'cv_screening': [
            'skill_cv_screening_sop.md',
            'general_non_negotiable_sops.md',
            'execution_discipline_protocol.md',
        ],
        'report_generation': [
            'project_job26_soul_architect_final.md',
            'project_job32_decision_brief_format.md',
            'feedback_decision_brief_hyperlinks.md',
        ],
    }
    
    files_to_load = MEMORY_MAP.get(task_type, [])
    memory_content = {}
    
    for filename in files_to_load:
        filepath = MEMORY_ROOT / filename
        if filepath.exists():
            with open(filepath, 'r') as f:
                content = f.read()
                # Extract just the markdown body (after frontmatter)
                if '---' in content:
                    parts = content.split('---')
                    body = parts[2] if len(parts) > 2 else content
                else:
                    body = content
                memory_content[filename] = body.strip()
    
    return memory_content


def format_memory_as_system_rules(memory_dict: dict) -> str:
    """
    Convert memory dict into system prompt rules format.
    
    Example output:
    
    LOCKED RULES:
    
    [From email_template_format_FINAL.md]
    1. Logo at top
    2. Small blue header...
    ...
    
    TONE RULES:
    [From feedback_email_rules.md]
    - Warm, not harsh
    - "We" voice, never "I"
    ...
    """
    
    sections = []
    sections.append("LOCKED RULES & FORMATS:\n")
    
    for filename, content in memory_dict.items():
        sections.append(f"\n[From {filename}]\n")
        sections.append(content)
        sections.append("\n" + "="*60)
    
    return "\n".join(sections)


def inject_memory_prompt(base_prompt: str, memory_dict: dict) -> str:
    """
    Inject memory content into system prompt.
    
    Usage:
        memory = load_memory_files('email_generation')
        rules = format_memory_as_system_rules(memory)
        system_prompt = inject_memory_prompt(BASE_PROMPT, memory)
    """
    
    rules_section = format_memory_as_system_rules(memory_dict)
    
    return f"""{base_prompt}

---

{rules_section}

---

EXECUTION RULE: You MUST follow every rule above. Before generating any output, review these rules. After generating, validate against every rule. If any violation found, regenerate.
"""
```

### Fix 1.2: Update CLAUDE.md to Reference Memory Injection

**Location:** `C:\Agent Coco\CLAUDE.md`

**Add this section:**
```markdown
## Memory Injection Protocol (2026-04-20 — NEW)

**For all task generation (emails, reports, screening):**

1. **Load Memory** — Call `load_memory_files(task_type)` before generating
2. **Inject Rules** — Convert memory to system prompt via `inject_memory_prompt()`
3. **Generate** — Generate output with locked rules visible in context
4. **Validate** — Check output against all rules before sending
5. **Fail Safe** — If output violates any rule, regenerate (don't send)

This ensures:
- Email formats never drift (locked rules in context)
- Tone stays consistent (rules injected into prompt)
- Screening templates preserved (SOP embedded)
- Corrections actually applied (memory re-loaded per task)

Reference: scripts/utils/memory_loader.py
```

---

## Priority 2: Task-Level Hooks (Generation Time)

### Fix 2.1: Create Format Validation Function

**Location:** Create `scripts/utils/format_validator.py`

```python
# format_validator.py
import re

class FormatValidator:
    """Validate generated content against locked formats."""
    
    @staticmethod
    def validate_email_format(email_html: str, format_spec: str) -> list:
        """
        Check if email HTML matches format_spec requirements.
        
        Returns: list of violations (empty if valid)
        """
        violations = []
        
        # Check required elements
        required = {
            'logo': '<img.*taleemabad_logo',
            'blue_header': 'PEOPLE.*CULTURE.*REJECTION',
            'blue_line': 'border.*#1565c0|1565c0.*border',
            'georgia_font': 'font.*Georgia',
            'justified_text': 'text-align:justify',
            'we_voice': 'We',
            'no_em_dash': email_html.count(' — ') == 0,  # em dash
        }
        
        for key, pattern in required.items():
            if key == 'no_em_dash':
                if not pattern:
                    violations.append(f"Found em-dashes (—) — use hyphens (-) instead")
            elif not re.search(pattern, email_html, re.IGNORECASE):
                violations.append(f"Missing: {key}")
        
        return violations
    
    @staticmethod
    def validate_report_format(report_html: str, report_type: str) -> list:
        """Check if report matches locked format for its type."""
        
        violations = []
        
        if report_type == 'cv_screening':
            required = {
                'stat_boxes': '<div class="stat-box"',
                'candidate_table': '<table',
                'hyperlinks': '<a href=',
                'georgia_font': 'Georgia',
            }
        
        # ... similar checks for other report types
        
        return violations
    
    @staticmethod
    def validate_against_sop(generated_content: str, sop_file: str, step: str) -> list:
        """
        Check if content follows specific SOP step.
        Example: validate_against_sop(email, 'gwc-rejection-emails.md', 'Step 1: Opening')
        """
        # Load SOP step from memory
        # Compare generated content against step requirements
        # Return violations
        pass
```

**Usage in email generation:**
```python
def send_rejection_email(candidate, role):
    # Load memory
    memory = load_memory_files('gwc_rejection')
    
    # Generate email
    email_body = generate_email_body(candidate, role, memory)
    
    # Validate
    violations = FormatValidator.validate_email_format(
        email_body, 
        memory['email_template_format_FINAL.md']
    )
    
    # Enforce
    if violations:
        print("❌ FORMAT VIOLATIONS FOUND:")
        for v in violations:
            print(f"  - {v}")
        raise ValidationError("Email format invalid. Not sending.")
    
    # Send
    return safe_sendmail(email_body)
```

### Fix 2.2: Create Pre-Send Checklist Hook

**Location:** Update `scripts/utils/safe_send.py`

```python
# Add to safe_send.py

def run_pregsend_qa_checklist(content: str, content_type: str) -> bool:
    """
    Run 8-item QA checklist before sending (from Execution Discipline Protocol).
    
    Returns: True if all checks pass, False otherwise
    """
    
    checks = {
        'file_names': "Are all file names/paths correct?",
        'formatting': "Does formatting match locked format?",
        'tone': "Is tone consistent with memory rules?",
        'duplication': "No duplicate sections or candidates?",
        'jargon': "No internal jargon exposed to candidates?",
        'encoding': "No encoding artifacts or corruption?",
        'consistency': "Consistent with prior work (templates, tone, format)?",
        'grounding': "All facts grounded in source material (no fabrication)?",
    }
    
    print(f"\n📋 PRE-SEND QA CHECKLIST ({content_type}):\n")
    
    passed = 0
    for check_name, question in checks.items():
        # In real use: would run programmatic checks
        # For now: expose for manual verification
        print(f"  ☐ {check_name}: {question}")
        passed += 1
    
    return passed == len(checks)

def safe_sendmail_with_qa(
    smtp_server: smtplib.SMTP,
    sender: str,
    recipients: list,
    message: str,
    context: str = "unknown",
    content_type: str = "email",  # NEW
    skip_qa: bool = False,  # NEW
):
    """
    Enhanced safe_sendmail with QA enforcement.
    """
    
    # Run QA checklist
    if not skip_qa:
        qa_result = run_presend_qa_checklist(message, content_type)
        if not qa_result:
            raise QAError("QA checklist not passed. Address violations before sending.")
    
    # Continue with security check + sending
    return safe_sendmail(smtp_server, sender, recipients, message, context)
```

---

## Priority 3: Configuration (Settings)

### Fix 3.1: Update `.claude/settings.local.json`

**Location:** `C:\Agent Coco\.claude\settings.local.json`

```json
{
  "permissions": {
    "allow": [
      // ... existing permissions
    ]
  },
  "enabledMcpServers": ["neon-postgres"],
  "enableAllProjectMcpServers": true,
  "coco_agent_config": {
    "memory_injection_enabled": true,
    "memory_refresh_per_task": true,
    "validation_required_for_send": true,
    "qa_checklist_enforced": true,
    "locked_formats": {
      "email_rejection": "email_template_format_FINAL.md",
      "report_screening": "skill_cv_screening_sop.md#Step8",
      "report_decision_brief": "project_job32_decision_brief_format.md"
    },
    "pre_send_hooks": [
      "format_validator.validate_email_format",
      "safe_send.run_presend_qa_checklist",
      "memory_loader.check_tone_consistency"
    ]
  }
}
```

---

## Priority 4: Script Updates (Isolation Fix)

### Fix 4.1: Template: Memory-Aware Send Script

**Create:** `scripts/jobs/job36/send_job36_rejection_with_memory.py`

```python
"""
Job 36 Rejection Emails — Memory-Aware Version
Uses memory injection to prevent format regression
"""

import sys
sys.path.insert(0, r'c:\Agent Coco')

from scripts.utils.memory_loader import load_memory_files, inject_memory_prompt
from scripts.utils.format_validator import FormatValidator
from scripts.utils.safe_send import safe_sendmail_with_qa
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load memory for task type
MEMORY = load_memory_files('gwc_rejection')
MEMORY_RULES = inject_memory_prompt("", MEMORY)

def generate_rejection_email(candidate_name, gwc_scores, role):
    """
    Generate rejection email with memory-injected rules.
    
    The memory rules are embedded in the generation,
    ensuring format + tone consistency.
    """
    
    # With memory loaded, generation should follow locked format
    # (In real implementation: pass MEMORY_RULES to Claude API or similar)
    
    email_html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="margin:0;padding:0;background-color:#f0f4f0;">
        <!-- Logo (from memory format requirement) -->
        <img src="cid:taleemabad_logo" height="38">
        
        <!-- Blue header (from memory format requirement) -->
        <p style="color:#1565c0;text-transform:uppercase;">PEOPLE & CULTURE • REJECTION DECISION</p>
        
        <!-- Body text (justify + Georgia, from memory) -->
        <p style="text-align:justify;font-family:Georgia,serif;font-size:15px;">
            We're reflecting on your {role} application...
        </p>
        
        <!-- More content... -->
    </body>
    </html>
    """
    
    return email_html

def main():
    # Load candidates
    candidates = [
        {'name': 'Candidate A', 'gwc': {'get': 6, 'want': 7, 'capacity': 5}},
        # ... more candidates
    ]
    
    role = "Product Manager"
    
    for candidate in candidates:
        # Generate email
        email_html = generate_rejection_email(
            candidate['name'],
            candidate['gwc'],
            role
        )
        
        # VALIDATE against locked format (NEW)
        violations = FormatValidator.validate_email_format(
            email_html,
            MEMORY['email_template_format_FINAL.md']
        )
        
        if violations:
            print(f"❌ {candidate['name']}: Format violations found:")
            for v in violations:
                print(f"   - {v}")
            continue  # Don't send
        
        # Send with QA enforcement (NEW)
        print(f"✓ {candidate['name']}: Format valid. Sending...")
        # safe_sendmail_with_qa(..., content_type='gwc_rejection')

if __name__ == "__main__":
    main()
```

---

## Priority 5: Documentation Updates

### Fix 5.1: Create Implementation Guide

**Location:** `C:\Agent Coco\SOPs\00_General_Discipline\03_Memory_Injection_Protocol.md`

```markdown
# SOP: Memory Injection Protocol

**Purpose:** Ensure memory rules are loaded and enforced during all task execution, preventing format/tone drift.

## When to Use
- Before generating any email
- Before creating any report
- Before screening CVs (embedding SOP steps)
- Before sending any candidate communication

## Steps

### Step 1: Identify Task Type
- Email generation → 'email_generation'
- Rejection email → 'gwc_rejection'
- Report generation → 'report_generation'
- CV screening → 'cv_screening'

### Step 2: Load Memory
```python
from scripts.utils.memory_loader import load_memory_files
memory = load_memory_files(task_type)
```

### Step 3: Inject into Prompt/Context
```python
from scripts.utils.memory_loader import inject_memory_prompt
rules = inject_memory_prompt(base_prompt, memory)
# Use 'rules' as system prompt
```

### Step 4: Generate with Rules Loaded
Generate content with locked rules visible in context

### Step 5: Validate Against Rules
```python
from scripts.utils.format_validator import FormatValidator
violations = FormatValidator.validate_email_format(generated_content, memory_spec)
if violations:
    raise ValidationError(f"Format violations: {violations}")
```

### Step 6: Run Pre-Send QA
```python
from scripts.utils.safe_send import run_presend_qa_checklist
qa_passed = run_presend_qa_checklist(generated_content, content_type)
if not qa_passed:
    raise QAError("QA checklist failed")
```

### Step 7: Send via Safe Bouncer
```python
safe_sendmail_with_qa(smtp, sender, recipients, message, context, content_type)
```

## Result
✓ Memory loaded per task (not just at session start)
✓ Rules injected into generation
✓ Output validated before sending
✓ Corrections actually applied
✓ Formats never drift
```

---

## Implementation Timeline

### Week 1: Foundation
- [ ] Create `memory_loader.py`
- [ ] Create `format_validator.py`
- [ ] Update CLAUDE.md with Memory Injection Protocol section
- [ ] Update `.claude/settings.local.json`

### Week 2: Integration
- [ ] Update `safe_send.py` with QA checklist
- [ ] Create reference implementation: `send_job36_rejection_with_memory.py`
- [ ] Create SOP: `03_Memory_Injection_Protocol.md`
- [ ] Test on one task type (e.g., GWC rejections)

### Week 3: Migration
- [ ] Refactor all existing `send_*.py` scripts to use memory loader
- [ ] Add validation to report generation scripts
- [ ] Add pre-send hooks to all email sending

### Week 4: Enforcement
- [ ] Enable QA checklist enforcement in settings
- [ ] Add memory refresh per task in harness
- [ ] Document as mandatory in CLAUDE.md
- [ ] Test on full job workflow (screening → reports → comms)

---

## Success Metrics

After implementation, Coco should:

✓ Load memory rules at task start (not just session start)
✓ Inject rules into generation prompt
✓ Validate output before sending
✓ Apply corrections immediately (not repeat next time)
✓ Never drift on format/tone (rules in context)
✓ Pass 8-item QA checklist consistently

**Verification:**
- Run same task twice → same format both times (not drift)
- Update memory rule → next task applies it (not forgotten)
- Generate rejection email → matches locked format exactly
- Generate report → matches reference format exactly

---

## Risks & Mitigation

| Risk | Mitigation |
|------|-----------|
| Memory loader slows down execution | Cache memory at startup + per-task refresh optional |
| Validation too strict | Make violations non-blocking initially, warnings only |
| Scripts require major refactor | Create wrapper (non-breaking), migrate gradually |
| QA checklist false positives | Start with manual (prompt for confirmation), automate gradually |
| Existing scripts break | Keep old logic working, new logic parallel, switch later |

---

## References
- Current memory system: `/c/Users/Dell/.claude/projects/C--Agent-Coco/memory/`
- CLAUDE.md: `C:\Agent Coco\CLAUDE.md`
- Settings: `C:\Agent Coco\.claude\settings.local.json`
```

---

## Summary

| Component | What | Where | Status |
|-----------|------|-------|--------|
| **Memory Loader** | Load memory per task | scripts/utils/memory_loader.py | To Build |
| **Validator** | Check format before send | scripts/utils/format_validator.py | To Build |
| **QA Checklist** | Enforce 8-item check | Update safe_send.py | To Build |
| **Settings** | Config memory injection | .claude/settings.local.json | To Update |
| **Scripts** | Use memory in send scripts | Refactor send_*.py | To Migrate |
| **SOP** | Document protocol | SOPs/00/03_*.md | To Create |
| **CLAUDE.md** | Reference protocol | C:\Agent Coco\CLAUDE.md | To Update |

---

## The One-Line Fix

**Make memory injection happen at task runtime, not just session start.**
