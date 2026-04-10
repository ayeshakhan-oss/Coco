# Coco's Skills — Master Index

**Last Updated:** 2026-04-10

This file indexes all of Coco's core skills for Taleemabad hiring operations. Each skill has a dedicated .md file in the `skills/` directory with detailed SOPs, non-negotiable rules, checklists, and reference implementations.

---

## Meta-Skill: General Discipline

**File:** [skills/general-discipline.md](skills/general-discipline.md)

**Status:** ✓ Locked in (2026-04-10)

**Description:** 10 core non-negotiable SOPs that apply to ALL work across all skills. Foundation of partnership and quality.

**Key Rules:**
1. No fabrication, no assumptions
2. Always use Taleemabad context
3. Pilot sharing rule (Ayesha + Jawwad only, never candidate)
4. Approval before sending anything
5. Calendar restrictions
6. Email restrictions
7. Memory and session review mandatory
8. Verification, QA, and discipline
9. Read all provided material thoroughly
10. Core work principle (verify, don't rush, use memory, follow SOPs)

---

## Skill 1: CV Screening / Resume Screening

**File:** [skills/cv-screening.md](skills/cv-screening.md)

**Status:** ✓ Locked in (2026-04-10)

**Pipeline Position:** Entry point — candidate CVs come in

**Objective:** Evaluate all candidate profiles against JD with full manual review and accurate ranking. No shortcuts on reading.

**Key Requirements:**
- 7-step manual review process (read JD → review all profiles → read resume fully → check candidate questions → assess exp → competitor exp → maintain format)
- Minimum CV reading capacity: 14,000–15,000 characters (do not flag before this threshold)
- New candidate info columns: Expected Salary, City, Willing to Relocate (Y/N)
- Email format: Header → 4 stat boxes → Key Observation → Shortlisted (hyperlinked names, descriptions, gaps) → Maybe → Special Flags → Footer
- Skills + Experience = TOP criteria for ranking (not competitor experience alone)
- Non-negotiable: read EVERY profile, state both total AND relevant experience separately, no assumptions, no demographic filtering
- Approval before sending (PILOT → approval → LIVE)

**Reference Email:** Initial Screening — Soul Architect / Conversational UX Designer (2026-04-06)

---

## Skill 2: Case Study Evaluation

**File:** [skills/case-study-evaluation.md](skills/case-study-evaluation.md)

**Status:** ✓ Locked in (2026-04-10)

**Pipeline Position:** After Values Call — if candidate passes values, they receive case study

**Objective:** Track submissions, assess quality, identify missing parts, keep Ayesha proactively informed.

**Key Requirements:**
- 8-step process (check Markaz → check submission status → check Gmail → download → read assignment → read submission → evaluate → flag AI/weak effort)
- Check BOTH Markaz AND Gmail (critical: don't rely on one source only)
- Automation: Auto-flag incomplete submissions to Ayesha same day/next morning
- Weekly proactive reporting: who submitted, who's overdue, who needs follow-up (without being asked)
- Read full submission one-by-one (no batching, no skipping sections)
- Identify missing parts specifically (name exactly what's missing)
- Flag AI-generated answers and weak effort

---

## Skill 3: Values Feedback Emails

**File:** [skills/values-feedback-emails.md](skills/values-feedback-emails.md)

**Status:** ✓ Locked in (2026-04-10)

**Pipeline Position:** After Values Interview — candidates who fail values round get feedback email

**Objective:** Write rejection feedback emails for candidates who fail values round. Personalized, emotionally careful, evidence-based.

**Key Requirements:**
- Word count: 800–1100 words (800 minimum mandatory, no exceptions)
- 3 required sections: What We Liked Most About You / Where We Found Ourselves Sitting With Questions / What We Think You Should Do Next
- Specific evidence from their values interview (not generic feedback)
- v8 HTML design: blue #1565c0 headings, green #1b5e20 subheadings, Georgia serif, justified text
- Feedback widget required at end of body
- Pilot rule: CRITICAL — send ONLY to Ayesha Khan + Jawwad Ali, NEVER include candidate in pilot
- No em dashes (replace with period/comma/colon)
- "We" voice throughout (never "I"), they/them pronouns (gender-neutral)
- Approval before live send (PILOT first, approval, then PILOT_MODE = False)
- Safe_sendmail bouncer (never smtplib directly)

---

## Skill 4: Values Scorecard Scoring

**File:** [skills/values-scorecard-scoring.md](skills/values-scorecard-scoring.md)

**Status:** ✓ Documented (2026-04-10)

**Pipeline Position:** During Values Interview — interviewer scores candidate real-time

**Objective:** Evaluate candidate's alignment with Taleemabad's 6 core values using a structured rating system. Produce PASS/OUT verdict and GWC assessment.

**The 6 Values:**
1. Don't Walk Away
2. All for One
3. Continuously Improve
4. Courageous Conversations
5. Don't Hold On Too Tight
6. Practice Joy

**Key Requirements:**
- Rating system: + (exhibits) / +/- (inconsistent) / - (does not exhibit)
- Pass/Out logic: PASS = zero minuses AND ≤2 +/- | OUT = any minus OR ≥3 +/-
- GWC assessment (for PASS candidates only): Gets it? Wants it? Capacity? (all 3 must be YES)
- 4 evidence columns per value: Deep-Dive, Curve-Ball, Micro-Case, Rating
- Markaz-compatible JSON schema (exact format required or invisible on UI)
- No blank columns (state "Not directly evident in interview" if not observed)
- Never assess GWC if candidate OUT

---

## Skill 5: Decision Briefs

**File:** [skills/decision-briefs.md](skills/decision-briefs.md)

**Status:** ✓ Documented (2026-04-10)

**Pipeline Position:** After all interview rounds complete — present final recommendations to hiring manager

**Objective:** Summarize hiring recommendations and candidate verdicts after CV → case study → values → debrief are complete.

**Key Requirements:**
- 4-part structure: Header & Stat Boxes → Leading Candidates (top recommendations) → Pipeline Summary (grouped by status) → Debrief Schedule & Next Steps
- Inline HTML email (no PDF attachment)
- 4 stat boxes at top (candidates screened, values interviews conducted, shortlisted, decision status)
- Every candidate name hyperlinked to Google Drive CV (audit all sections)
- Verdict labels must match approved list exactly (no "OFFER OUT" unless offer confirmed)
- DB status ≠ actual status (flag anomalies, never assert DB as truth)
- GWC explicitly stated for values PASS candidates
- Email recipients: TO = hiring manager, CC = hiring@taleemabad.com + ayesha.khan@taleemabad.com
- Approval before sending (PILOT → approval → LIVE)

---

## Skill 6: Candidate Rejections (CV-Stage)

**File:** [skills/candidate-rejections.md](skills/candidate-rejections.md)

**Status:** ✓ Documented (2026-04-10)

**Pipeline Position:** CV screening stage — candidates who don't advance to values interview

**Objective:** Reject candidates during CV screening phase with warm, specific, reflective feedback tied to their actual CV.

**Key Requirements:**
- 800+ words (minimum 800)
- Warm, reflective tone (not diagnostic)
- Specific CV evidence (don't make up observations)
- 3 sections: What we appreciated → Where we found questions → What to do next
- No em dashes, "we" voice, they/them pronouns
- v8 HTML design, feedback widget required
- Safe_sendmail bouncer, approval before sending (PILOT first)

**Note:** For candidates who passed values but weren't selected for current role, see **Skill 7: Warm Bench Feedback Email** instead.

---

## Skill 7: Warm Bench Feedback Email

**File:** [skills/warm-bench-feedback-email.md](skills/warm-bench-feedback-email.md)

**Status:** ✓ Documented (2026-04-10)

**Pipeline Position:** After values interview + case study + debrief — candidates who cleared values with good GWC but weren't selected for THIS role

**Objective:** Send warm, storytelling-based feedback to candidates who passed values interview but weren't selected for the current role. Signal they remain on warm bench for future suitable roles.

**Key Requirements:**
- 800–1,000 words (minimum 800)
- Warm, affectionate, almost like a thoughtful letter
- Quote specific examples from their values interview
- Reference values scorecard evidence
- Reference GWC assessment (explain their GWC score)
- Gently explain why role didn't advance (focus on role needs, not their gaps)
- Clearly state they may be reconsidered for future roles (SPECIFIC role/function/timeline, not vague)
- v8 HTML design, feedback widget required
- Safe_sendmail bouncer, approval before sending (PILOT first)
- NO em dashes, "we" voice, they/them pronouns

---

## Skill 9: Attendance Reports

**File:** [skills/attendance-reports.md](skills/attendance-reports.md)

**Status:** ✓ Documented (2026-04-10)

**Objective:** Daily attendance report showing where Taleemabad's OPL+OWT employees are (onsite, leave, WFH, out of office, etc.).

**Key Requirements:**
- Scope: OPL+OWT employees only (84 active as of 2026-04-09, static payroll total)
- Data sources: Markaz (leave records) + Teams Presence (announcements) + sign-in records + user feedback
- 7 sections: Onsite, On Leave, WFH (unlogged), WFH — Confirmed (permanent WFH), Out of Office, Arriving Later, Flagged (zero record)
- 8 stat boxes showing count for each section (TOTAL must always = 84, the static payroll)
- Flagged section includes status notes (RWP Team, on severance, last month, no record)
- Email format: Header + 8 colored stat boxes + 2-column onsite grid + tables for other categories
- Recipients: Ayesha Khan + Jawwad Ali + Aymen Abid
- Verification formula: Sum of all sections must = 84 before sending

---

## Skill 10: Database Queries

**File:** [skills/database-queries.md](skills/database-queries.md)

**Status:** ✓ Documented (2026-04-10)

**Objective:** Access Taleemabad's candidate, job, budget, and employee data from Neon PostgreSQL for CV screening, attendance, case study evaluation, and hiring decisions.

**Key Requirements:**
- Type: PostgreSQL (Neon serverless, read-only via MCP)
- 6 common query types: Candidate CV data, Application status & pipeline, JD & budget, Values scorecard data, Leave & attendance, Employee roster & payroll
- Connection via .mcp.json (DO NOT commit, in .gitignore)
- Schema: docs/schema.md (must be read first)
- Audit logging: ALL queries must call log_db_query() from scripts/utils/audit_log.py (logged to logs/read_audit.log)
- Minimum reading capacity: 14,000–15,000 characters for Base64-decoded CV PDFs
- Never assume data consistency; verify before using
- Base64 decoding required for resume_data fields

---

## Skill 11: Report Generation

**File:** [skills/report-generation.md](skills/report-generation.md)

**Status:** ✓ No changes required (2026-04-10)

**Objective:** Format and generate hiring reports (CV screening, case study evaluation, decision briefs, etc.) in user-approved format.

**Current Methodology:** Fine, no updates needed.

---

## Skill 12: Email Notifications

**File:** [skills/email-notification.md](skills/email-notification.md)

**Status:** ✓ Existing (may need refresh)

**Objective:** Send completed reports and notifications to hiring managers and HR stakeholders.

**Current Method:** Gmail API or SMTP, safe_sendmail bouncer, logged to email_audit.log.

---

## Skills Status Summary (as of 2026-04-10)

| # | Skill | Status | Locked | Updated |
|---|-------|--------|--------|---------|
| Meta | General Discipline | ✓ | Yes | 2026-04-10 |
| 1 | CV Screening | ✓ | Yes | 2026-04-10 |
| 2 | Case Study Evaluation | ✓ | Yes | 2026-04-10 |
| 3 | Values Feedback Emails | ✓ | Yes | 2026-04-10 |
| 4 | Values Scorecard Scoring | ✓ | Yes | 2026-04-10 |
| 5 | Decision Briefs | ✓ | Yes | 2026-04-10 |
| 6 | Candidate Rejections (CV-Stage) | ✓ | Yes | 2026-04-10 |
| 7 | Warm Bench Feedback Email | ✓ | Yes | 2026-04-10 |
| 8 | Attendance Reports | ✓ | Yes | 2026-04-10 |
| 9 | Database Queries | ✓ | Yes | 2026-04-10 |
| 10 | Report Generation | ✓ | No (no changes) | 2026-04-10 |
| 11 | Email Notifications | ✓ | Existing | (pending refresh) |

---

## How to Use This Index

1. **Find a skill:** Search this file for skill name
2. **Read full SOP:** Click the file link (e.g., [skills/cv-screening.md](skills/cv-screening.md))
3. **Quick reference:** Check MEMORY.md for "Skill SOP: [Name]" files
4. **All skills follow:** General Discipline SOP (10 core non-negotiable rules apply to every skill)

---

## Key Principles (Apply to ALL Skills)

- **Memory first:** Read MEMORY.md before starting any task
- **Approval always:** Ask explicitly before sending anything externally
- **Quality first:** Verify, QA, discipline before submitting
- **Specific evidence:** Never assume or fabricate data
- **Pilot then live:** Test with Ayesha + Jawwad first, then approve before going live

---

**Created:** 2026-04-10 | **Maintained by:** Coco | **For:** Taleemabad Talent Acquisition
