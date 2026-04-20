# Report Generation Integration Guide

**Status:** LOCKED FORMAT SYSTEM READY FOR DEPLOYMENT  
**Created:** 2026-04-20  
**Files Created:**
- `scripts/utils/report_memory_loader.py` — Load locked specs
- `scripts/utils/report_validator.py` — Enforce format
- `scripts/utils/report_generator.py` — Orchestrate generation

---

## How It Works

### The Three-Component System

```
1. MEMORY LOADER (report_memory_loader.py)
   ├─ Loads locked report specifications
   ├─ Hard-codes specs in Python (survives forever)
   └─ Creates system prompts with rules embedded

2. VALIDATOR (report_validator.py)
   ├─ Checks HTML output against spec
   ├─ Finds format violations
   └─ Blocks sending if broken

3. GENERATOR (report_generator.py)
   ├─ Orchestrates full pipeline
   ├─ Loads spec → Create prompt → Validate → Request approval
   └─ Ensures locked format across all generations
```

### The Generation Flow

```
User asks: "Generate screening report for Job 26"
                    ↓
Load spec from memory (LOCKED_SCREENING_REPORT_SPEC)
                    ↓
Create system prompt with rules embedded
                    ↓
Send to Claude with locked specifications
                    ↓
Claude generates HTML with rules in prompt
                    ↓
Validate output against spec
    ├─ If valid: ✓ Continue
    └─ If invalid: ✗ Block, regenerate
                    ↓
Request PILOT approval before sending
                    ↓
Send via safe_sendmail after approval
```

**Result:** Format locked forever. Thousands of generations, same structure.

---

## Using the System: Three Approaches

### APPROACH 1: Simple Usage (Recommended for Quick Scripts)

```python
from scripts.utils.report_generator import generate_report_with_locked_format

# Generate report with specifications locked in
config = generate_report_with_locked_format(
    report_type='screening_report',
    position='Soul Architect',
    job_id=26,
    candidates=[
        {'name': 'Muhammad Abdullah', 'match': 95, ...},
        {'name': 'Zikra Fiaz', 'match': 92, ...},
        # ... more candidates
    ],
    shortlisted_count=5,
    maybe_count=7
)

# Get the generation prompt to send to Claude
prompt = config['generation_instructions']
print(prompt)  # This has ALL locked rules embedded

# After Claude generates HTML:
try:
    config['validate'](generated_html)  # Validate
    print("✓ Format valid, safe to send")
except ValidationError as e:
    print(f"✗ Format violation: {e}")
    # Regenerate
```

---

### APPROACH 2: Full Pipeline (For Complex Scripts)

```python
from scripts.utils.report_generator import ReportGenerationPipeline

# Create pipeline
pipeline = ReportGenerationPipeline('screening_report')

# Step 1: Get generation prompt
data = {
    'position': 'Soul Architect',
    'job_id': 26,
    'candidates': candidates_list,
    'total_screened': 42,
    'shortlisted_count': 5,
    'maybe_count': 7,
    'no_hire_count': 30
}

prompt = pipeline.step1_get_generation_prompt(data)

# Step 2: Send prompt to Claude, get HTML back
generated_html = claude_api.call(prompt)  # Your Claude API call

# Step 3: Set generated HTML
pipeline.step2_set_generated_html(generated_html)

# Step 4: Validate
if not pipeline.step3_validate():
    print(pipeline.step4_get_validation_report())
    # Don't proceed if validation fails
    return

# Step 5: Request approval
pipeline.step5_request_approval(recipient='ayesha.khan@taleemabad.com')

# Step 6: Send after approval confirmed
if approval_confirmed:
    pipeline.step6_send_live(approval_confirmed=True)
    safe_sendmail(smtp, sender, recipients, generated_html)
```

---

### APPROACH 3: Template Integration (For Template Engines)

```python
from scripts.utils.report_memory_loader import create_system_prompt, load_report_spec

# Load spec
spec = load_report_spec('decision_brief')

# Get system prompt with rules embedded
system_prompt = create_system_prompt(spec)

# Pass to your template engine (Jinja2, Mako, etc.)
context = {
    'spec': spec,
    'system_prompt': system_prompt,
    'position': 'Field Coordinator',
    'candidates': candidates_data,
    'rules': spec['global_rules']
}

html = template.render(**context)

# Validate output
from scripts.utils.report_validator import validate_before_send
validate_before_send(html, 'decision_brief')
```

---

## Integration into Existing Scripts

### Before (Current — Format Drifts)

```python
# send_job26_screening_report_final.py
SHORTLIST = [
    {'name': 'Muhammad Abdullah', 'match': '95%', ...},
    # Hardcoded, format not locked
]

# Problem: If format is corrected tomorrow, this script still hardcodes old format
```

### After (With Locked Format System)

```python
# send_job26_screening_report_final.py (UPDATED)
from scripts.utils.report_generator import generate_report_with_locked_format
from scripts.utils.report_validator import validate_before_send
from scripts.utils.safe_send import safe_sendmail

# Load locked specifications
config = generate_report_with_locked_format(
    report_type='screening_report',
    position='Soul Architect',
    job_id=26,
    candidates=CANDIDATES_LIST,
    shortlisted_count=5,
    maybe_count=7
)

# Get generation prompt with rules embedded
generation_prompt = config['generation_instructions']

# Generate HTML (using Claude API or template)
generated_html = generate_html_with_prompt(generation_prompt, data)

# Validate before sending (BLOCKS if broken)
try:
    config['validate'](generated_html)
    print("✓ Format valid")
except ValidationError:
    print("✗ Format violation — not sending")
    return

# Send via safe_sendmail
safe_sendmail(smtp, sender, recipients, generated_html)

# Result: Format LOCKED. No drift. Forever.
```

---

## Step-by-Step: Update an Existing Script

### 1. Identify the Script
```bash
# Example: Job 26 screening report
C:\Agent Coco\scripts\jobs\job26\send_job26_screening_report_final.py
```

### 2. Add Imports
```python
from scripts.utils.report_generator import generate_report_with_locked_format
from scripts.utils.report_validator import validate_before_send, ValidationError
from scripts.utils.safe_send import safe_sendmail
```

### 3. Load Locked Specifications
```python
config = generate_report_with_locked_format(
    report_type='screening_report',
    position=JOB_TITLE,
    job_id=JOB_ID,
    candidates=your_candidates_list
)
```

### 4. Get Generation Instructions
```python
generation_instructions = config['generation_instructions']
# Pass this to Claude or template engine
```

### 5. Validate Output
```python
try:
    config['validate'](generated_html)
except ValidationError as e:
    print(f"Format violation: {e}")
    return
```

### 6. Send Safely
```python
safe_sendmail(smtp, sender, [recipient], generated_html)
```

---

## Testing the System

### Test 1: Load Specifications

```python
from scripts.utils.report_memory_loader import load_report_spec

spec = load_report_spec('screening_report')
print(f"Spec loaded: {spec['name']}")
print(f"Locked: {spec['locked_format']}")
# Output: Spec loaded: Initial Screening Report
#         Locked: True
```

### Test 2: Create System Prompt

```python
from scripts.utils.report_memory_loader import create_system_prompt, load_report_spec

spec = load_report_spec('decision_brief')
prompt = create_system_prompt(spec)
print(prompt[:500])  # First 500 chars
# Output: "You are generating a Coco Decision Brief Report..."
#         "LOCKED FORMAT SPECIFICATION..."
```

### Test 3: Validate HTML

```python
from scripts.utils.report_validator import ReportValidator

validator = ReportValidator('screening_report')

# Good HTML (will pass)
good_html = """
<div style="background:#1a2a3a;color:white;">
  <p>PEOPLE & CULTURE · INITIAL SCREENING REPORT</p>
  <p style="font-family:Georgia,serif;">...</p>
</div>
"""
violations = validator.validate(good_html)
print(f"Violations: {len(violations)}")  # 0

# Bad HTML (will fail)
bad_html = "<p>Some random content</p>"
violations = validator.validate(bad_html)
print(f"Violations: {len(violations)}")  # Multiple violations found
```

### Test 4: Full Pipeline

```python
from scripts.utils.report_generator import ReportGenerationPipeline

pipeline = ReportGenerationPipeline('screening_report')

# Get prompt
data = {'position': 'Test', 'job_id': 99, 'candidates': []}
prompt = pipeline.step1_get_generation_prompt(data)
print(f"Prompt length: {len(prompt)} chars")

# Simulate generation
html = "<html><body>...</body></html>"
pipeline.step2_set_generated_html(html)

# Validate
result = pipeline.step3_validate()
print(f"Valid: {result}")

# Get report
report = pipeline.step4_get_validation_report()
print(report)
```

---

## Key Features

### ✓ Format LOCKED Forever
Specifications are hard-coded in Python. No memory drift. No format regression.

### ✓ Validation ENFORCED
Every report validated before sending. Broken format = blocked.

### ✓ Rules EMBEDDED in Prompt
Claude receives locked rules in generation instructions. No guessing.

### ✓ Approval REQUIRED
PILOT mode first. No LIVE send without approval.

### ✓ Scalable
Works for 1 report or 1,000,000 reports. Format never drifts.

### ✓ Backward Compatible
Can update existing scripts without breaking them.

---

## Configuration Details

### Screening Report Spec (LOCKED)

```python
SCREENING_REPORT_SPEC = {
    'type': 'initial_screening',
    'locked_format': True,
    'sections': {
        'header': {required: True, background_color: '#1a2a3a', ...},
        'stat_boxes': {required: True, count: 4, colors: [red, blue, yellow, gray]},
        'key_observation': {required: True, sentences: 2-3},
        'shortlisted_candidates': {required: True, count: 5},
        'maybe_table': {required: True, count: 7},
        'footer': {required: True}
    },
    'global_rules': {
        'font_family': 'Georgia, serif',
        'heading_color': '#1565c0',
        'text_alignment': 'justify',
        'all_names_hyperlinked': True,
        'html_only': True,
        'no_fabrication': True
    }
}
```

### Decision Brief Spec (LOCKED)

```python
DECISION_BRIEF_SPEC = {
    'type': 'decision_brief',
    'locked_format': True,
    'sections': {
        'header': {...},
        'stat_boxes': {...},
        'where_we_are': {...},
        'debrief_schedule': {required: True, actual_dates_only: True},
        'leading_candidates': {required: True, probes_required: True},
        'footer': {...}
    },
    'global_rules': {
        'font_family': 'Georgia, serif',
        'no_scores': True,
        'no_fabrication': True,
        'all_names_hyperlinked': True,
        'actual_dates_only': True
    }
}
```

---

## Troubleshooting

### "ValidationError: Stat boxes... found 3, expected 4"

**Problem:** Generated report has wrong number of stat boxes  
**Solution:** Check that system prompt was passed to Claude. Stat box count is in LOCKED_SCREENING_REPORT_SPEC.

### "ValidationError: Font not Georgia serif throughout"

**Problem:** Generated report uses different font  
**Solution:** Ensure 'Georgia, serif' is in the HTML style attributes.

### "ValidationError: Google Drive CV links missing"

**Problem:** Candidate names not hyperlinked to Drive  
**Solution:** All names must include `<a href="[GOOGLE_DRIVE_LINK]">Name</a>` tags.

### "Output appears to be PDF"

**Problem:** Generator created PDF instead of HTML  
**Solution:** Ensure HTML output format only. No PDF attachments.

---

## Deployment Checklist

- [ ] Copy 3 files to scripts/utils/:
  - [ ] report_memory_loader.py
  - [ ] report_validator.py
  - [ ] report_generator.py

- [ ] Test each file:
  - [ ] `python report_memory_loader.py` (should print summaries)
  - [ ] `python report_validator.py` (should initialize validators)
  - [ ] `python report_generator.py` (should initialize generators)

- [ ] Update existing send_*.py scripts:
  - [ ] Add imports
  - [ ] Load locked specs
  - [ ] Validate output
  - [ ] Block if broken

- [ ] Test on real report generation:
  - [ ] Generate screening report
  - [ ] Generate decision brief
  - [ ] Verify format matches

- [ ] Document in CLAUDE.md:
  - [ ] Add reference to report generation system
  - [ ] Document locked formats
  - [ ] Add usage examples

---

## Result: Format LOCKED Forever

**Before:** Memory grows, execution drifts, format regression  
**After:** Format in code, locked in place, validated before send

**Guaranteed:** Same structure across all generations, forever.

---

## Next Steps

1. Copy the 3 files to `scripts/utils/`
2. Run tests to verify installation
3. Update one script (Job 26) as proof of concept
4. Test end-to-end
5. Update remaining scripts incrementally
6. Document in CLAUDE.md as standard practice

---

## Contact / Questions

If format drifts again after deployment:
1. Check `report_memory_loader.py` — is spec loaded?
2. Check `report_validator.py` — did validation run?
3. Check prompt injection — did system prompt reach Claude?

**Goal:** Zero format regressions, forever.
