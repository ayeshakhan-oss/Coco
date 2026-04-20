---
name: Decision Brief — CV Hyperlink Completeness
description: Rule established 2026-04-08. EVERY candidate name in decision brief (all sections) must have a hyperlink to their CV on Google Drive. Audit before sending.
type: feedback
---

# DECISION BRIEF — CV HYPERLINK COMPLETENESS
**Established:** 2026-04-08  
**Status:** MANDATORY — All future decision briefs  
**Why:** Hiring manager needs 1-click access to CVs from decision brief, not separate attachment hunt

---

## THE RULE

In every decision brief, **every candidate name must be hyperlinked** to their CV on Google Drive.

### Applies to ALL sections:
- [ ] **Leading candidates** section — all names linked
- [ ] **Discussion** section — all names linked
- [ ] **Pipeline recommendations** section — all names linked
- [ ] **Debrief schedule** section — all names linked

### No exceptions:
- Not mentioned in "Maybe" table? Still get linked if name appears anywhere
- Not shortlisted? Still get linked if name appears anywhere
- Over budget? Still get linked if name appears anywhere

---

## HOW TO IMPLEMENT

### Step 1: Upload CVs to Google Drive
```
/Hiring/[Job Name]/
├─ Candidate Name 1.pdf
├─ Candidate Name 2.pdf
└─ Candidate Name 3.pdf
```

### Step 2: Generate shareable links
```
https://drive.google.com/file/d/[FILE_ID]/view?usp=sharing
```

### Step 3: In decision brief HTML, use this pattern
```html
<a href="https://drive.google.com/file/d/FILE_ID/view?usp=sharing">
  Candidate Name
</a>
```

### Step 4: Before sending — AUDIT
- [ ] Every name in Leading section: hyperlinked? Click test one.
- [ ] Every name in Discussion section: hyperlinked? Click test one.
- [ ] Every name in Pipeline section: hyperlinked? Click test one.
- [ ] Every name in Debrief section: hyperlinked? Click test one.
- [ ] All links return 200 (working)? Try clicking 2–3 random links.

---

## WHAT HAPPENS WITHOUT HYPERLINKS

- Hiring manager gets PDF with 15 candidate names
- No way to quickly pull up a CV without manual search/download
- Slows hiring decision process
- Looks unprofessional

## WHAT HAPPENS WITH COMPLETE HYPERLINKS

- Hiring manager clicks name → CV opens in new tab
- 1-click research for each candidate
- Fast, professional, seamless workflow

---

## REFERENCE SCRIPTS

- **Job 32:** `send_job32_decision_brief_pilot.py` (inline HTML with cv_link() helper)
- **Job 36:** Similar pattern used

---

## AUDIT TEMPLATE

Before sending decision brief, run this checklist:

```
DECISION BRIEF HYPERLINK AUDIT

[ ] Section 1: Leading Candidates
    [ ] Name 1: hyperlinked?
    [ ] Name 2: hyperlinked?
    [ ] Name 3: hyperlinked?

[ ] Section 2: Discussion / Panel Notes
    [ ] Name 1: hyperlinked?
    [ ] Name 2: hyperlinked?
    [ ] [All names]: hyperlinked?

[ ] Section 3: Pipeline Recommendations
    [ ] Name 1: hyperlinked?
    [ ] Name 2: hyperlinked?
    [ ] [All names]: hyperlinked?

[ ] Section 4: Debrief Schedule
    [ ] Name 1: hyperlinked?
    [ ] Name 2: hyperlinked?
    [ ] [All names]: hyperlinked?

[ ] FINAL: Click 5 random links to verify working
    [ ] Link 1: working?
    [ ] Link 2: working?
    [ ] Link 3: working?
    [ ] Link 4: working?
    [ ] Link 5: working?

Result: ✅ Ready to send OR ❌ Fix and retry
```

---

**Owner:** Coco  
**Status:** LOCKED IN — Applied to all future decision briefs
