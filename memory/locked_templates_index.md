---
name: LOCKED TEMPLATES INDEX
description: Single reference for all locked/finalized report formats. Keep this open while working.
type: reference
originSessionId: d4a807e5-380e-4bc6-ac7a-c252d64a81bd
---
# LOCKED TEMPLATES INDEX
**READ THIS FIRST before any report/email task.** If a format is listed here, it's LOCKED — no variations.

---

## 📋 CV SCREENING REPORTS
**File:** [../../../Agent%20Coco/REPORT_FORMAT_LOCKED.md](../../../Agent%20Coco/REPORT_FORMAT_LOCKED.md)  
**When to use:** Multi-candidate CV screening for any position  
**Format:** HTML table-based, Gmail-safe. 4 stat boxes, 5-candidate profiles, Maybe table, PM table.  
**Template file:** soul_architect_screening_pilot_2026-04-20_FINAL.html  
**Key rules:** All special chars as HTML entities. No exceptions.  
**Last verified:** 2026-04-20

---

## 📧 REJECTION EMAILS (Bulk)
**File:** [email_template_format_FINAL.md](email_template_format_FINAL.md)  
**When to use:** Rejection emails for screened-out candidates  
**Format:** Logo, small blue header, LARGE blue position title, smaller subtitle, BLUE horizontal line, justified Georgia text  
**Key rules:**  
- NO ASTERISKS in headings
- NO EM DASHES (use dashes only)
- Justified text (TA_JUSTIFY in ReportLab)
- No interviewer names in body
- No jargon/internal lingo

**Last verified:** 2026-04-14

---

## 💬 VALUES FEEDBACK EMAILS
**File:** [skill_values_feedback_emails_sop.md](skill_values_feedback_emails_sop.md)  
**When to use:** Values interview feedback (passed screening, at values stage)  
**Length:** 800–1100 words MINIMUM (800 floor, strict)  
**Design:** v8 (interview evidence + specific quotes required)  
**Key rules:**  
- Always pilot to Ayesha + Jawwad ONLY (never directly to candidate)
- Specific interview evidence required (not generic feedback)
- Email format: Same as rejection emails above

**Last verified:** 2026-04-10

---

## 📊 DECISION BRIEF REPORTS
**File:** [project_job32_decision_brief_format.md](project_job32_decision_brief_format.md)  
**When to use:** Final candidates + hiring decision brief  
**Format:** Inline HTML email (NO PDF attachment)  
**Content:** 4 stat boxes (total positions, leading candidates, short panel, decision timeline). All candidate names cv_link().  
**Key rules:**  
- CVs uploaded to Google Drive, hyperlinked in email
- Every name must have a Drive link (Leading, Discussion, Pipeline, Debrief Schedule)
- Audit all hyperlinks before sending
- No PDF attachment

**Reference:** send_job32_decision_brief_pilot.py  
**Last verified:** 2026-04-06

---

## 🎯 ATTENDANCE REPORTS
**File:** [attendance_report_complete_template.md](attendance_report_complete_template.md)  
**When to use:** Daily I-10 onsite/WFH/leave attendance  
**Format:** ReportLab PDF, 7 colored stat boxes (or 8 with WFH-Confirmed), 2-column onsite grid, Name|Status tables  
**Key rules:**  
- Header color: #34495e (dark blue-grey)
- Onsite: #e8f5e9 (light green)
- Leave: #ffe0b2 (light orange)
- WFH-Confirmed: #e3f2fd (light blue)
- NO GRID BORDERS (table only)
- Email stat table format included
- Stat count must match section headers

**Data sources:**  
- Teams for presence updates
- Markaz for pending leaves
- Calendar for bookings

**Recipients:** Ayesha + Jawwad + Aymen Abid

**Reference:** attendance_8apr2026.py  
**Last verified:** 2026-04-20

---

## 📝 CASE STUDY EVALUATION
**File:** [skill_case_study_evaluation_sop.md](skill_case_study_evaluation_sop.md)  
**When to use:** Evaluating case study submissions  
**Process:** 8-step SOP with automation  
**Key rules:**  
- Auto-flag incomplete submissions
- Check Markaz AND Gmail (both sources)
- Read full submission before scoring
- Flag AI/weak effort
- Weekly proactive reporting

**Last verified:** 2026-04-10

---

## 🔍 CV SCREENING (Step-by-step)
**File:** [skill_cv_screening_sop.md](skill_cv_screening_sop.md)  
**When to use:** Initial candidate CV review for any position  
**Process:** 8-step multi-criterion evaluation  
**Capacity:** 14k–15k characters (format limit)  
**Key rules:**  
- Skills + experience = top criteria
- Email format with stat boxes
- All candidate names hyperlinked to Google Drive CVs
- Expected Salary, City, Relocate fields required
- 8-item self-QA checklist before sending
- Format locking discipline mandatory

**Reference:** Job 26 finalized workflow  
**Last verified:** 2026-04-15

---

## 🎬 TALENT SOURCING (7 Steps)
**File:** [talent_sourcing_7steps_complete.md](talent_sourcing_7steps_complete.md)  
**When to use:** Finding passive candidates via Google/LinkedIn searches  
**Process:** 7-step SOP (Intake → Add to Markaz)  
**Output:** Excel sheet with verified candidates + LinkedIn links  
**Key rules:**  
- 3-layer search: org pages → Google → LinkedIn
- Verify LinkedIn links via site:linkedin.com Google queries
- Personalized DMs for Ayesha to send (not Coco)
- Markaz integration ONLY after confirmed interest
- Phase 3 (end-to-end test) COMPLETE and production-ready

**Reference:** Soul_Architect_47_Verified_Candidates_FINAL_2026-04-17.xlsx  
**Last verified:** 2026-04-17

---

## ⚡ QUICK REFERENCE

| Task | Memory File | Status |
|------|-------------|--------|
| CV Screening Report | REPORT_FORMAT_LOCKED.md | ✅ LOCKED |
| Rejection Email | email_template_format_FINAL.md | ✅ LOCKED |
| Values Feedback | skill_values_feedback_emails_sop.md | ✅ LOCKED |
| Decision Brief | project_job32_decision_brief_format.md | ✅ LOCKED |
| Attendance Report | attendance_report_complete_template.md | ✅ LOCKED |
| Case Study Eval | skill_case_study_evaluation_sop.md | ✅ LOCKED |
| CV Screening (Step-by-step) | skill_cv_screening_sop.md | ✅ LOCKED |
| Talent Sourcing | talent_sourcing_7steps_complete.md | ✅ LOCKED |

---

## ENFORCEMENT RULE

If you're about to start writing an email, report, or analysis for any of these task types, **READ THE LOCKED TEMPLATE FIRST**. Not reading it = violation of Discipline Enforcement Lockdown Rule 3.

**Non-negotiable.**
