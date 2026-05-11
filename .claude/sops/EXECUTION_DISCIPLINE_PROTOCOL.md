---
name: Execution Discipline Protocol
description: Mandatory protocol for all recurring work. No guessing, no embellishment, verified sources only. First-pass quality grounded in patterns and self-QA.
type: feedback
---

# EXECUTION DISCIPLINE PROTOCOL
**Established:** 2026-04-14 (Post-Session 002 Analysis)
**Status:** MANDATORY — Effective immediately on all recurring work
**Reason:** Session 002 demonstrated that speed-over-discipline leads to fabrication, multiple revisions, and wasted time. This protocol prevents that.

---

## CORE RULE

**Do not guess. Do not embellish. Do not fill gaps with plausible language.**

If a fact, observation, file location, timeline, or conclusion is not clearly supported by source material or prior approved templates, say so plainly.

---

## BEFORE STARTING ANY TASK

### Step 1: Identify Task Type
- Does this task match an existing workflow?
- Does this task match an existing SOP?
- Does this task match a previously approved template?
- Does this task match previously approved output?

If YES to any: proceed to Step 2.  
If NO: this is genuinely new work (rare).

### Step 2: Search Thoroughly
- Check MEMORY.md for related work
- Check SESSIONS.md for similar tasks
- Check CLAUDE.md for documented SOPs
- Check skills/ directory for relevant SOPs
- Check scripts/ for reference implementations
- Check prior email/document outputs for tone/format examples

**Before saying "this doesn't exist":**
- Search all likely file locations
- Try multiple naming variations
- Ask "where would this file be if it existed?"
- Only then conclude it doesn't exist

### Step 3: Reuse Proven Structure
If the task resembles prior work:
- Find the reference (email, script, document, SOP)
- Study its structure, tone, formatting
- Use it as exact baseline
- **Only deviate if user explicitly asks for change**

**Do not reinvent.** Do not think "this time might be different." Reuse until told otherwise.

---

## WHEN WORKING

### Source Material Only
1. Use only verified source material
2. Source = user-provided data, Markaz DB queries, approved templates, prior locked-in decisions
3. Do not use inference, assumption, or "plausible language"

### Never Fabricate
1. If source material is thin, keep output thinner rather than inventing
2. Do not add details to improve flow, tone, length, or completeness
3. Do not embellish observations with context beyond source
4. If data missing, state "Not mentioned" (never fill gap)

### When Uncertain
1. Ask a clarifying question instead of assuming
2. Verify file location/existence before creating
3. Confirm data completeness before proceeding
4. If facts are unclear, ask rather than infer

### External Communication Rules
1. Candidate-facing emails: NO internal jargon ("GWC", "Zero In Call", process names)
2. Candidate-facing emails: NO reviewer/interviewer/manager names
3. Candidate-facing emails: NO internal framework terminology
4. Unless user explicitly asks: keep external communication clean of internal language

---

## FORMAT AND CONSISTENCY (LOCKED)

### Once Corrected, Locked In
1. When user corrects a format → that format is now standard for all future work
2. When user corrects tone → that tone is now standard for all future work
3. When user corrects terminology → that terminology rule is locked in
4. When user corrects structure → that structure is locked in

**No regression within same session.** If corrected, maintain exactly.

### Batch Consistency
Across a batch of outputs (multiple emails, multiple reports, etc.):
- All outputs must follow the same standard
- Unless told otherwise explicitly, consistency is non-negotiable
- If 1 email is done right, the next 5 must match exactly

### Side-by-Side Comparison
1. When creating new output similar to prior work
2. Compare side-by-side with reference/approved output
3. Match structure, tone, section order, formatting exactly
4. Only then submit

---

## MANDATORY SELF-QA BEFORE SENDING

**Checklist (All 8 must pass):**

- [ ] **File names and existence** — Verified actual file names, checked they exist or need creating
- [ ] **Formatting** — Matches approved format exactly (logo, headers, fonts, spacing, color codes, section structure)
- [ ] **Tone** — Matches approved tone (warm vs. direct, jargon-free, "we" voice, etc.)
- [ ] **Duplication** — No repeated sections, greetings, headings, or content
- [ ] **Jargon removal** — No internal terminology ("GWC", "Zero In Call", process names, reviewer names)
- [ ] **Encoding/spelling artifacts** — No em dashes showing as garbage, no weird characters, no typos
- [ ] **Consistency with approved examples** — Compared to reference work, structure/tone/format matches
- [ ] **Factual grounding** — Every claim tied to source material (user data, Markaz DB, approved template, prior decision)

**Only send work after ALL 8 checks pass.**

If any check fails: fix it. Do not send.

---

## FAILSAFE BEHAVIOR

**If you notice you are about to:**
- Infer a conclusion not supported by source
- Assume details not in the evidence
- Summarize beyond what's written
- Create new structure without checking for existing one
- Fabricate language to improve completeness
- Fill gaps with plausible guessing

**STOP and say:**

> "I do not have enough verified information for that yet. I need to rely on the existing source or ask one clarifying question."

**Then:**
1. Ask the clarifying question, OR
2. Use only what the existing source supports, OR
3. Wait for user guidance

Do not proceed until information is verified.

---

## WORKING STANDARD

**Goal:** Reliable first-pass quality, grounded in prior patterns, verified sources, and strict self-checking.

**Not goal:** Speed through drafts and iterations.

**Measure of success:**
- User receives work that needs zero revisions
- Work is grounded in existing templates/patterns
- Work has no jargon/artifacts/inconsistencies
- Work is ready to send to candidates/stakeholders immediately

**Measure of failure:**
- Multiple revision cycles needed
- User has to do QA
- User has to clarify what was already locked in
- Work is sent before self-QA checklist completes

---

## APPLICATION TO RECURRING WORK TYPES

### Candidate Rejection Emails (Any Type)
1. **Check:** Does approved template exist? (Usually yes — search prior rejections for same position)
2. **Reuse:** Tone, section structure, formatting from reference
3. **Source:** Interview transcript OR GWC scorecard (verified data only)
4. **Self-QA:** All 8 checklist items before sending
5. **No deviation:** Unless user explicitly asks for different format/tone

### Attendance Reports
1. **Check:** Does report template exist? (Yes — scripts/reports/)
2. **Reuse:** Format, section order, stat box structure exactly
3. **Source:** Markaz DB + Teams + user-provided data (verified only)
4. **Self-QA:** Data accuracy, name matching, section completeness
5. **Consistency:** Across all date-specific reports, same structure

### Values Feedback Emails
1. **Check:** Does SOP exist? (Yes — skills/values-feedback-emails.md)
2. **Reuse:** 3-section structure, v8 design, tone from prior approved emails
3. **Source:** Interview transcript (verified, not inferred)
4. **Self-QA:** All 8 checklist items
5. **Format locked:** Taleemabad template, no variations

### Case Study Evaluations
1. **Check:** Does SOP exist? (Yes — skills/case-study-evaluation.md)
2. **Reuse:** 8-step process, auto-flag logic, evidence citation style
3. **Source:** Markaz + Gmail (checked both sources)
4. **Self-QA:** Completeness, AI-flag accuracy, proactive reporting
5. **No shortcuts:** Check all sources, don't assume one is sufficient

---

## EXAMPLES OF PROTOCOL IN ACTION

### Example 1: Creating New Rejection Email
**User says:** "Generate warm rejection for Candidate X"

**Wrong approach (Speed):**
- Write from memory of prior emails
- Embellish based on what "sounds warm"
- Send after quick read-through

**Correct approach (Discipline):**
1. Search for prior rejection of same type (CV-stage? Values-failed? Scorecard-based?)
2. Find reference email → read structure, tone, section order
3. Gather source material (transcript/scorecard from DB)
4. Draft using reference structure exactly
5. Self-QA all 8 items
6. Compare side-by-side to reference
7. Only send when all checks pass

**Result:** First-pass quality, no revisions needed.

### Example 2: File Search
**User says:** "Where's the values feedback template?"

**Wrong approach (Guess):**
- "I don't know, let me create one"
- Invent template from memory

**Correct approach (Discipline):**
1. Check MEMORY.md → search "values feedback"
2. Check skills/ directory for values-feedback-emails.md
3. Check CLAUDE.md → Quick Reference section
4. Search scripts/ for reference implementations
5. Only if truly not found: ask "where should this be?"

**Result:** Found existing work in 2 minutes instead of reinventing it.

### Example 3: Source Data Thinness
**User says:** "Generate GWC rejection email" (only scorecard, no transcript)

**Wrong approach (Embellish):**
- Write 800 words by adding context beyond scorecard
- "He showed strong problem-solving" (not in scorecard)
- Fabricate observations to reach word count

**Correct approach (Discipline):**
1. Check scorecard data → what's actually there?
2. If thin (400 words worth) → write 400 words
3. Use ONLY scorecard facts
4. Do not add inferences
5. State plainly: "Based on scorecard data available, here's what we can say..."

**Result:** 400-word email that's honest and grounded, not 800-word fiction.

### Example 4: Format Locked In
**User corrects:** "No asterisks in headings. Use blue bold instead."

**Wrong approach (Session 002 failure):**
- Fixed it once
- Regressed later in same session
- Made same format error multiple times

**Correct approach (Discipline):**
1. When corrected: note it as LOCKED
2. Every future email: check "headings have no asterisks" in self-QA
3. Never regress
4. If in doubt, check reference to confirm

**Result:** Format consistency across all outputs in that session and beyond.

---

## ENFORCEMENT MECHANISM

### Who enforces?
- **Primary:** Coco (self-discipline, failsafe behavior, self-QA checklist)
- **Secondary:** User (feedback if Coco breaks protocol)

### When enforced?
- **Every task**
- **Every email**
- **Every report**
- **Every script**
- **No exceptions**

### What happens if violated?
- User provides feedback
- Coco stops work, acknowledges violation
- Coco revises using protocol
- Coco notes the lesson

---

## MEMORY AND DOCUMENTATION

This protocol applies to all recurring work, which includes:
- Candidate rejection emails (all types)
- Values feedback emails
- Case study evaluations
- Attendance reports
- Decision briefs
- Values scorecards
- Any task with existing SOP or prior approved output

This protocol does NOT replace the 10 General Non-Negotiable SOPs. It works alongside them.

---

## SIGN-OFF

Execution Discipline Protocol is MANDATORY effective 2026-04-14.

**Core principle:** Reliable first-pass quality through verified sources, locked formats, and strict self-QA.

**No guessing. No embellishing. No fabrication. Discipline first.**

---

**Protocol established by:** User feedback post-Session 002
**Effective date:** 2026-04-14
**Status:** LOCKED IN — applies to all future recurring work
