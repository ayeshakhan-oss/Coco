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

## 📧 ALL INTERVIEW INVITES (Universal Template)
**File:** [locked_email_template_interview_invites_FINAL_2026_05_13.md](locked_email_template_interview_invites_FINAL_2026_05_13.md)  
**When to use:** ALL interview stage invites — values, warm bench, exploratory, case study, GWC, zero-in, final, offer  
**Format:** Table-based HTML, #f5f5f5 bg, #ffffff card (775px), #e5e7e2 wrapper, #3157b7 title/divider, Georgia serif, 1.85 line-height  
**Design Lock:** 34px logo, 17px body text, blue headers, purple CTA button, justified text  
**Key rules:**
- NO DESIGN DEVIATIONS — Use exact colors, fonts, spacing
- Content-only adaptability (greeting + body change per stage, design fixed)
- All names hyperlinked to Google Drive CVs when applicable
- Pilot to Ayesha FIRST, never direct to candidate

**Covers:** See specific approaches below  
**Last verified:** 2026-05-13

---

## 🔔 EXPLORATORY CALL INVITES
**File:** [locked_exploratory_call_invite_approach.md](locked_exploratory_call_invite_approach.md)  
**When to use:** Candidates without immediate role fit; 30-minute exploratory calls  
**Design:** Universal template above (no deviations)  
**Body Text:** LOCKED word-for-word. Greeting → thankyou → 30-min call description → "Fundraising & Partnerships Overview" link → CTA → P.S.  
**Links:**
- Booking: `https://calendar.app.google/r1Rj1b1UMiAqonDs5` (Google Calendar)
- Document: "Fundraising & Partnerships Overview" (Google Drive)

**Scripts:** `send_exploratory_call_batch_pilot.py` + `send_exploratory_call_batch_live.py`  
**Self-QA:** 8-item checklist before sending  
**Status:** ✅ PRODUCTION READY (tested 4 candidates 2026-05-15)  
**Last verified:** 2026-05-15

---

## 💝 WARM BENCH FEEDBACK INVITES & REJECTIONS
**File:** [warm_bench_final_locked_approach.md](warm_bench_final_locked_approach.md)  
**When to use:** Candidates who cleared values but weren't selected (rejection-keep-warm)  
**Design:** Universal template above (no deviations)  
**Length:** 800–1100 words MANDATORY  
**Structure:** Opening + "What Genuinely Impressed Us" + "Here's the Part We Need to Be Honest About" + "Here's Where We Want to Leave Things" + P.S.  
**Tone:** Warm, observational, specific timestamps, poetic subjects, no prescriptive advice  
**Script:** `scripts/warm_bench_locked.py`  
**Self-QA:** 8-item checklist included  
**Status:** ✅ PRODUCTION READY (tested 4 JRA candidates)  
**Last verified:** 2026-05-05

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

## 💬 TONE RULE — ALL CANDIDATE FEEDBACK EMAILS
**File:** [rule_all_feedback_emails_use_locked_tone.md](rule_all_feedback_emails_use_locked_tone.md)  
**When to use:** BEFORE writing ANY rejection, feedback, or warm-bench email  
**Applies to:** Values feedback, warm bench rejections, GWC rejections, screening rejections, ANY feedback email  
**Tone Guide:** [values_feedback_email_tone_locked_2026_05_12.md](values_feedback_email_tone_locked_2026_05_12.md)  
**Non-Negotiable Requirements:**
- Warm, observational tone (NOT analytical, NOT life-coach)
- No internal jargon (no plus-minus, no "GWC", no framework lingo)
- Specific interview evidence (every observation tied to what they said)
- 800–1100 words minimum
- Georgia serif, 11px, justified
- Pilot to Ayesha + Jawad ONLY (never directly to candidate)
- Run 8-item Self-QA checklist before sending

**Status:** 🔒 LOCKED & NON-NEGOTIABLE (enforced 2026-05-12)  
**Last verified:** 2026-05-12

---

## 💬 VALUES FEEDBACK EMAILS (Interview Stage)
**File:** [skill_values_feedback_emails_sop.md](skill_values_feedback_emails_sop.md)  
**When to use:** Values interview feedback (passed screening, at values stage)  
**Length:** 800–1100 words MINIMUM (800 floor, strict)  
**Design:** v8 (interview evidence + specific quotes required)  
**Tone:** See locked tone guide above (MANDATORY)  
**Key rules:**  
- Always pilot to Ayesha + Jawwad ONLY (never directly to candidate)
- Specific interview evidence required (not generic feedback)
- Run 8-item Self-QA checklist before sending

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

## ⚡ QUICK REFERENCE — ALL EMAIL TYPES & THEIR TEMPLATES

| Email Type | Template File | Tone File | Status |
|------------|---------------|-----------|--------|
| **Interview Invites (ALL)** | locked_email_template_interview_invites_FINAL_2026_05_13.md | N/A (design-locked) | 🔒 LOCKED |
| └─ Values Interview | locked_email_template_interview_invites_FINAL_2026_05_13.md | N/A | ✅ |
| └─ Exploratory Call | locked_exploratory_call_invite_approach.md | N/A | ✅ |
| └─ Warm Bench Invite | warm_bench_final_locked_approach.md | See tone rule below | ✅ |
| └─ Case Study Debrief | locked_email_template_interview_invites_FINAL_2026_05_13.md | N/A | ✅ |
| └─ Zero-In Call | locked_email_template_interview_invites_FINAL_2026_05_13.md | N/A | ✅ |
| **Feedback/Rejection (ALL)** | (see specific types below) | rule_all_feedback_emails_use_locked_tone.md | 🔒 LOCKED |
| └─ Values Feedback | (varies by context) | values_feedback_email_tone_locked_2026_05_12.md | ✅ |
| └─ Warm Bench Rejection | warm_bench_final_locked_approach.md | values_feedback_email_tone_locked_2026_05_12.md | ✅ |
| └─ GWC Rejection | (varies by context) | values_feedback_email_tone_locked_2026_05_12.md | ✅ |
| └─ Screening Rejection | email_template_format_FINAL.md | values_feedback_email_tone_locked_2026_05_12.md | ✅ |

### Reports & Other

| Task | Memory File | Status |
|------|-------------|--------|
| CV Screening Report | REPORT_FORMAT_LOCKED.md | ✅ LOCKED |
| Decision Brief | project_job32_decision_brief_format.md | ✅ LOCKED |
| Attendance Report | attendance_report_complete_template.md | ✅ LOCKED |
| Case Study Eval | skill_case_study_evaluation_sop.md | ✅ LOCKED |
| CV Screening (Step-by-step) | skill_cv_screening_sop.md | ✅ LOCKED |
| Talent Sourcing | talent_sourcing_7steps_complete.md | ✅ LOCKED |

---

## ENFORCEMENT RULE

If you're about to start writing an email, report, or analysis for any of these task types, **READ THE LOCKED TEMPLATE FIRST**. Not reading it = violation of Discipline Enforcement Lockdown Rule 3.

**Non-negotiable.**
