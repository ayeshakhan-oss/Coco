---
name: Task to SOP Mapping
description: Automatic reference for each task type. Shows what SOP to read, what template to use, and what checklist to run. Single source of truth for task setup.
type: feedback
---

# TASK → SOP → TEMPLATE MAPPING

**Purpose:** When you get a task, use this map to find: required SOP + locked template + checklist  
**Status:** LOCKED IN — updated as new tasks/SOPs are created  
**Owner:** Coco + Ayesha

---

## Quick Reference Table

| When You See This Task | Read This SOP | Template | Checklist |
|---|---|---|---|
| **CV Screening** | [cv_screening.md](../SOPs/02_Candidate_Evaluation/cv_screening.md) | [REPORT_FORMAT_LOCKED.md](../REPORT_FORMAT_LOCKED.md) | [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) |
| **Rejection Email** | [cv_rejection_emails.md](../SOPs/01_Candidate_Communication/cv_rejection_emails.md) | ✅ [interview_invite.html](../templates/interview_invite.html) | [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) |
| **Values Feedback Email** | [values_feedback_emails.md](../SOPs/01_Candidate_Communication/values_feedback_emails.md) | ✅ [interview_invite.html](../templates/interview_invite.html) | [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) |
| **Interview Invite (Any Stage)** | [interview_invite.md](../SOPs/01_Candidate_Communication/) | ✅ [interview_invite.html](../templates/interview_invite.html) | [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) |
| **Attendance Report** | [attendance_reports.md](../SOPs/03_Hiring_Operations/attendance_reports.md) | ⏳ attendance_report.html (TBD) | [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) |
| **Decision Brief** | [hiring_decision_brief.md](../SOPs/03_Hiring_Operations/hiring_decision_brief.md) | ⏳ decision_brief.html (TBD) | [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) |
| **Case Study Evaluation** | [case_study_evaluation.md](../SOPs/02_Candidate_Evaluation/case_study_evaluation.md) | (No template) | [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) |
| **Talent Sourcing** | [talent_sourcing.md](../SOPs/05_Talent_Sourcing/talent_sourcing.md) | (Output: markdown + Excel) | [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) |

---

## Detailed Workflow for Each Task

### 1. CV Screening

**Task:** "Screen CVs for [Position Name]"

**Required Steps:**
1. Read: [SOPs/02_Candidate_Evaluation/cv_screening.md](../SOPs/02_Candidate_Evaluation/cv_screening.md)
2. Reference: [REPORT_FORMAT_LOCKED.md](../REPORT_FORMAT_LOCKED.md) — locked HTML format (no deviations)
3. Run: [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) before sending
4. Output: HTML email with stat boxes + candidate profiles + hyperlinked CVs on Google Drive

**Key Locked-In Standards:**
- Gmail-safe HTML table layout
- 4 stat boxes (screened, shortlisted, maybe, rejected counts)
- Candidate profiles with key metrics
- ALL candidate names hyperlinked to Google Drive CVs
- No asterisks in headings
- Justified Georgia text, 1.75 line-height

---

### 2. Rejection Email

**Task:** "Write rejection emails for [Candidate Names]"

**Required Steps:**
1. Read: [SOPs/01_Candidate_Communication/cv_rejection_emails.md](../SOPs/01_Candidate_Communication/cv_rejection_emails.md)
2. Reference: [templates/interview_invite.html](../templates/interview_invite.html) — locked universal template
3. Run: [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) before sending
4. Output: Inline HTML email (no attachments)

**Key Locked-In Standards:**
- Logo at top
- Small blue header
- Large blue position title
- Smaller subtitle
- **BLUE horizontal line divider**
- Justified Georgia text, #2f4fa2 accent color
- No internal jargon or process names
- No interviewer/reviewer names
- Warm tone (even in rejection)

---

### 3. Values Feedback Email

**Task:** "Write values feedback for [Candidate Names]"

**Required Steps:**
1. Read: [SOPs/01_Candidate_Communication/values_feedback_emails.md](../SOPs/01_Candidate_Communication/values_feedback_emails.md)
2. Reference: [templates/interview_invite.html](../templates/interview_invite.html) — locked universal template
3. Run: [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) before sending
4. Output: Inline HTML email (no attachments)

**Key Locked-In Standards:**
- Same template as rejection email
- 800-1100 words minimum (800 word floor)
- Specific interview transcript evidence required
- Values-focused feedback, not skills feedback
- Warm tone
- **PILOT ONLY first:** Send to ayesha.khan@taleemabad.com + jawwad.ali@taleemabad.com
- Never send directly to candidate without approval

---

### 4. Interview Invite (All Stages)

**Task:** "Send interview invite for [Candidate] — [Stage: values/warm bench/zero-in/final]"

**Required Steps:**
1. Read: Relevant SOP from SOPs/01_Candidate_Communication/
2. Reference: [templates/interview_invite.html](../templates/interview_invite.html) — locked universal template (ALL stages use this)
3. Run: [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) before sending
4. Output: Inline HTML email (no attachments)

**Key Locked-In Standards:**
- Universal template for ALL invite stages (values, warm bench, zero-in, final, offer)
- Design specification LOCKED:
  - Background: #f3f4f6 (light gray)
  - Card width: 620px
  - Card padding: 70px
  - Title/accent color: #2f4fa2 (dark blue)
  - Header color: #4b6cb7
  - Subtitle color: #5a6ea8
  - Font: Georgia serif
  - Line-height: 1.75
- NO deviations to this design
- All invites must match this exact specification

---

### 5. Attendance Report

**Task:** "Generate attendance report for [Date]"

**Required Steps:**
1. Read: [SOPs/03_Hiring_Operations/attendance_reports.md](../SOPs/03_Hiring_Operations/attendance_reports.md)
2. Reference: [templates/attendance_report.html](../templates/attendance_report.html) — locked format
3. Run: [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) before sending
4. Output: PDF + HTML email

**Key Locked-In Standards:**
- 10-section structure (onsite, leave, WFH, WFH-Confirmed, OOO, arriving, unaccounted, NIETE, etc.)
- Colored stat boxes (#34495e header, #e8f5e9 onsite, #ffe0b2 leave, etc.)
- 2-column onsite grid (NO borders/grid lines)
- Name | Status table format
- Payroll total = 84 (OPL + OWT headcount)
- Data sourced from Teams API + Markaz leave_requests table
- ReportLab PDF with justified text

---

### 6. Decision Brief

**Task:** "Write decision brief for [Position Name]"

**Required Steps:**
1. Read: [SOPs/03_Hiring_Operations/hiring_decision_brief.md](../SOPs/03_Hiring_Operations/hiring_decision_brief.md)
2. Reference: [templates/decision_brief.html](../templates/decision_brief.html) — locked format
3. Run: [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) before sending
4. Output: Inline HTML email (NO PDF attachment)

**Key Locked-In Standards:**
- 4 stat boxes (total values calls, leading candidates, discussion, pipeline)
- Leading Candidates section with profiles
- Discussion section with recommendation
- Pipeline section (other strong candidates)
- Debrief Schedule section
- ALL candidate names must be hyperlinked to Google Drive CVs
- Every name in every section must have a CV link
- Inline HTML format (no PDF)

---

### 7. Case Study Evaluation

**Task:** "Evaluate case study for [Candidate Name]"

**Required Steps:**
1. Read: [SOPs/02_Candidate_Evaluation/case_study_evaluation.md](../SOPs/02_Candidate_Evaluation/case_study_evaluation.md)
2. Reference: (No HTML template for this task)
3. Run: [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) before sending
4. Output: Evaluation report (text or markdown)

**Key Locked-In Standards:**
- 8-step evaluation process
- Check Markaz AND Gmail for submission
- Read full submission (no truncation)
- Flag AI-generated work (if detected)
- Flag weak/incomplete effort
- Weekly proactive reporting to hiring manager

---

### 8. Talent Sourcing

**Task:** "Source candidates for [Position Name]"

**Required Steps:**
1. Read: [SOPs/05_Talent_Sourcing/talent_sourcing.md](../SOPs/05_Talent_Sourcing/talent_sourcing.md)
2. Reference: (No HTML template — output is markdown + Excel)
3. Run: [SELF_QA_CHECKLIST.md](SELF_QA_CHECKLIST.md) before sending
4. Output: Excel file + markdown sourcing report

**Key Locked-In Standards:**
- 7-step systematic sourcing process
- 3-layer search strategy (org pages → Google → LinkedIn)
- Verified LinkedIn links (site:linkedin.com Google search)
- Platform selection by role (where to find your target persona)
- Personalized LinkedIn DMs (drafted by Coco, sent by Ayesha)
- Excel output with candidate details
- Markaz integration ONLY after confirmed interest
- Tags format: {sourced_by, sourcing_run, profile_url}

---

## How to Use This Map

**When Ayesha assigns a task:**

1. **Find the task type** in the left column
2. **Read the SOP** listed (right side)
3. **Locate the template** (or note if none)
4. **Open the SELF_QA_CHECKLIST** and keep it visible
5. **Work through the SOP** using verified sources only
6. **Complete the output** in the locked format
7. **Run the 8-item checklist** 
8. **Show checklist results** to Ayesha
9. **Submit for review** (do NOT send external yet)

---

## Adding New Tasks

When a new task type emerges:
1. Create a new SOP in SOPs/
2. If needs a template: create HTML file in templates/
3. Add new row to the table above
4. Update MEMORY.md to link to this map
5. Commit changes to git

---

**Established:** 2026-04-28 (Phase 1 consolidation)  
**Status:** LOCKED IN — updated as new SOPs are created  
**Owner:** Coco + Ayesha
