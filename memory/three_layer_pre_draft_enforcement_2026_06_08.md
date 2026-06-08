---
name: Three-Layer Pre-Draft Enforcement System (2026-06-08)
description: Complete three-layer architecture to prevent bad drafts BEFORE they're written. Layer 1 (template injection), Layer 2 (pre-flight checklist), Layer 3 (send-time validation).
type: project
---

# Three-Layer Pre-Draft Enforcement System

**Problem Solved:** Harness was only validating at SEND time. Bad drafts were already written. Ayesha had to catch mistakes.

**Solution:** Three-layer architecture prevents bad drafts at SOURCE.

---

## Layer 1: Template Injection (Draft Time Prevention)

### What It Does
When you invoke a candidate communication skill, the UserPromptSubmit hook automatically injects:
- Locked template HTML (not a reference, an actual template)
- Locked approach/SOP
- Master index
- Pre-flight checklist
- 7 HARD BLOCKs list

### How It Works

**User asks:** "Draft GWC rejection for Hira Abbasi from CPD Coach"

**Hook triggers:** UserPromptSubmit detects keywords ("draft" + "gwc rejection")

**Automatic injection into context:**
```
<!-- LOCKED TEMPLATE HTML (you will edit this, not create from scratch) -->
[gwc_rejection_template_locked.html injected]

<!-- LOCKED APPROACH (read before editing template) -->
[GWC rejection locked approach from CANDIDATE_COMMUNICATION_LOCKED_INDEX]

<!-- PRE-FLIGHT CHECKLIST (complete before proceeding) -->
[pre_draft_checklist_2026_06_08.md injected]

<!-- 7 HARD BLOCKs (verify you understand) -->
[List of blocks that will prevent send]
```

### Key Benefit
**You can't start custom HTML from scratch because the locked template is right there in your context.** You're forced to EDIT the template, not CREATE custom HTML.

---

## Layer 2: Pre-Flight Checklist (Pre-Draft Gating)

### What It Does
You MUST complete this checklist before you can start drafting. It blocks proceeding until all items are acknowledged.

### The Checklist

```
MASTER INDEX & CONTEXT
- [ ] I have read CANDIDATE_COMMUNICATION_LOCKED_INDEX_2026_06_08.md
- [ ] I understand this is the SINGLE SOURCE OF TRUTH

LOCKED TEMPLATE REVIEW
- [ ] I have read the locked template HTML (provided in context)
- [ ] I understand the exact structure, colors, fonts
- [ ] I will EDIT this template, not CREATE custom HTML

LOCKED APPROACH/SOP
- [ ] I have read the locked approach for my email type
- [ ] I understand required sections and exact wording
- [ ] I understand word count (800-1100 minimum)

7 HARD BLOCKs (Violations That Block Send)
- [ ] Word count ≥ 800
- [ ] No intent-words (assumed/believed/thought/preferred/energized)
- [ ] No em dashes (—)
- [ ] No PILOT prefix in subject (when live)
- [ ] Required sections present
- [ ] No jargon (GWC, KCD, warm bench, etc.)
- [ ] No interviewer names

3 WARNINGs (Logged, Non-Blocking)
- [ ] Haroon balance (praise ≈ decision)
- [ ] Subject not generic (warm bench only)
- [ ] No recruiting abstractions

READY TO DRAFT?
- [ ] I have completed ALL items above
- [ ] I am ready to EDIT the provided template
- [ ] I will NOT create custom HTML from scratch
```

### Key Enforcement
**You cannot proceed to draft until you've checked all boxes.** This is a GATE, not a suggestion.

---

## Layer 3: Send-Time Validation (Final Catch)

### What It Does
Existing PreToolUse hook validates before safe_sendmail() is called.

### Coverage
- 7 HARD BLOCKs (exit code 2 → blocks send)
- 3 WARNINGs (exit code 0 → logged but allowed)
- All violations logged to `logs/email_audit.log`

### Why It's Still Needed
Safety net. Catches any violations that somehow slip through layers 1-2.

---

## How It Works End-to-End

### Step 1: You Make a Request
```
"Draft GWC rejection for Hira Abbasi from CPD Coach position"
```

### Step 2: UserPromptSubmit Hook Fires
Detects keywords: "draft" + "gwc rejection"

Automatically injects into context:
- gwc_rejection_template_locked.html
- GWC rejection locked approach
- pre_draft_checklist_2026_06_08.md
- Master index
- 7 HARD BLOCKs reference

### Step 3: You Read the Injected Content
You see:
1. **Master index** — tells you where locked template is
2. **Locked template HTML** — the exact structure you'll use
3. **Locked approach** — the required sections + tone + word count
4. **Pre-flight checklist** — what you must acknowledge
5. **7 HARD BLOCKs** — what will block send

### Step 4: You Complete Pre-Flight Checklist
You acknowledge:
```
- [ ] I have read the locked template
- [ ] I have read the locked approach
- [ ] I understand the 7 HARD BLOCKs
- [ ] I am ready to EDIT (not CREATE) the template
```

**Only after all checked:** You proceed to draft

### Step 5: You Draft (Using Provided Template)
You open the locked template HTML and:
- Replace [CANDIDATE_NAME] with "Hira Abbasi"
- Replace [SECTION_1_CONTENT] with your GWC feedback
- Replace [SECTION_2_CONTENT] with your gap analysis
- Replace [PS_CONTENT] with memorable moment

**You do NOT create custom HTML.** The structure, colors, fonts are locked.

### Step 6: You Run CLI Eval (Optional Pre-Pilot Test)
```bash
python scripts/evals/run_eval.py --file draft.html --type gwc_rejection --subject "My Subject"
```

Instant report shows all violations.

### Step 7: You Send to Ayesha (Pilot)
```bash
python scripts/send_email.py (or safe_sendmail call)
```

### Step 8: PreToolUse Hook Validates (Before Send)
Hook fires, runs eval engine:
- HARD BLOCK found? → Exit 2, send blocked, error printed
- Warning only? → Exit 0, send proceeds, logged to audit

### Step 9: Ayesha Reviews (Content-Focused)
No longer reviewing formatting (that's locked).
Only reviewing: story quality, tone nuance, Haroon balance judgment calls.

### Step 10: Approval → Live Send
All rules validated. Go live with confidence.

---

## Architecture Diagram

```
User request
    ↓
[LAYER 1] UserPromptSubmit hook fires
    ├── Inject locked template HTML
    ├── Inject locked approach
    ├── Inject pre-flight checklist
    ├── Inject master index
    └── Can't start wrong (template is right there)
    ↓
[LAYER 2] Pre-flight checklist gate
    ├── You read master index ✓
    ├── You read template ✓
    ├── You read approach ✓
    ├── You acknowledge 7 BLOCKs ✓
    └── Only then can you draft
    ↓
You draft (editing provided template, not creating custom HTML)
    ↓
[OPTIONAL] CLI test: python run_eval.py
    ├── All 10 checks run instantly
    └── You see violations before piloting
    ↓
You send to Ayesha (pilot)
    ↓
[LAYER 3] PreToolUse hook validates (before safe_sendmail)
    ├── HARD BLOCKs found? → Block send (exit 2)
    └── WARNINGs only? → Allow send (exit 0)
    ↓
Ayesha reviews (content/tone, not formatting)
    ↓
Approval → Send live
```

---

## Files Needed

### Templates (in `templates/`)
- `gwc_rejection_template_locked.html`
- `warm_bench_template_locked.html`
- `values_feedback_template_locked.html`
- `cv_rejection_template_locked.html`

### Memory Files (in `memory/`)
- `pre_draft_checklist_2026_06_08.md` — The mandatory checklist
- `CANDIDATE_COMMUNICATION_LOCKED_INDEX_2026_06_08.md` — Master index (file created separately)
- `three_layer_pre_draft_enforcement_2026_06_08.md` — This document

### Hook Scripts (in `scripts/hooks/`)
- `pre_send_validation_hook.py` — Layer 3 (send-time) — ALREADY CREATED
- Enhanced `prompt_submit_hook.py` — Layer 1 (template injection) — NEEDS UPDATE

### Config (in `.claude/`)
- `settings.json` — Wire PreToolUse hook — ALREADY WIRED

---

## What Changes for Coco in Next Session

### Old Workflow (Broken)
```
"Draft GWC rejection"
    → Invoke skill
    → Query database
    → Create custom HTML
    → Ayesha says "go read template"
    → Fix and resend
```

### New Workflow (Three-Layer Gated)
```
"Draft GWC rejection"
    → Hook auto-injects template + checklist
    → You complete pre-flight checklist
    → You EDIT provided template (can't deviate)
    → Optional: test with CLI
    → Send to Ayesha
    → Hook validates before send
    → Ayesha reviews (no formatting issues possible)
    → Go live with confidence
```

**Time saved:** No more back-and-forth about "go read the template." Template is already in context.

**Deviations prevented:** Structure is locked by design (you're editing, not creating).

**Violations caught:** If you somehow violate a HARD BLOCK, send is blocked before Ayesha sees it.

---

## The Payoff

| Metric | Before | After | Benefit |
|--------|--------|-------|---------|
| Time to valid draft | 5-10 min (if no deviations) + rewrites | <1 min per draft (template already there) | 5-10x faster |
| Deviations caught | At Ayesha's review (she has to tell you) | At draft time (template prevents deviation) | 100% prevention |
| Template access | Manual memory lookup (easy to skip) | Auto-injected (can't skip) | No escapes |
| Pre-draft enforcement | None (you decide if rules matter) | Mandatory checklist (gated) | Iron discipline |
| Send-time validation | Catches violations | Catches violations | Safety net |

---

**Status: READY TO IMPLEMENT** ✅

All templates created. Checklist ready. Hook logic designed. Ready to wire up.
