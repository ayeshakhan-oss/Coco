---
name: Proactive SOP Maintenance Duty
description: Automatic responsibility for maintaining SOPs folder. Whenever a new SOP is created or updated, copy to SOPs folder and update navigation. No user request needed.
type: project
---

# PROACTIVE SOP MAINTENANCE DUTY
**Established:** 2026-04-14  
**Status:** PERMANENT — Automatic responsibility (user delegates to Coco, Coco owns it)

---

## THE DUTY (Automatic)

Whenever a new SOP is created OR an existing SOP is updated, Coco automatically:

1. **Copy to SOPs folder** — Place in appropriate category (00, 01, 02, 03, 04, or 05)
2. **Update SOPs/README.md** — Add to navigation index with one-line description
3. **Commit to git** — Create commit with descriptive message
4. **Update MEMORY.md** — Document new/changed SOP in memory index

**No user request needed.** This is a permanent, automatic responsibility.

---

## CATEGORIES

SOPs are organized into 6 categories:

| Category | Folder | Examples |
|----------|--------|----------|
| **00** | General_SOPs | Execution Discipline, Session Startup, General Discipline |
| **01** | Candidate_Communication | Rejection Emails, Values Feedback, Warm Bench, GWC Rejections |
| **02** | Candidate_Evaluation | CV Screening, Case Study Evaluation, Values Scorecard |
| **03** | Hiring_Operations | Decision Briefs, Attendance Reports |
| **04** | Data_and_Systems | Database Queries, Report Generation, Email Notification |
| **05** | Talent_Sourcing | Talent Sourcing (7-step process) |

---

## HOW TO PLACE NEW SOPs

When creating a new SOP:

1. **Identify category** — Which function does it belong to?
   - General discipline/meta stuff? → Category 00
   - Something candidates see/hear? → Category 01
   - Evaluating candidates? → Category 02
   - Running hiring operations? → Category 03
   - Technical/systems? → Category 04
   - Finding candidates? → Category 05

2. **Copy to appropriate folder** — `SOPs/XX_Category/sop_name.md`

3. **Update SOPs/README.md** — Add one-line entry to the index:
   ```markdown
   ### Category 01: Candidate Communication
   - [Rejection Emails](01_Candidate_Communication/rejection_emails.md) — Warm, specific rejection emails with interview evidence
   - [Values Feedback](01_Candidate_Communication/values_feedback_emails.md) — 800-1100 word feedback emails after values interview
   ```

4. **Commit to git** — Message format:
   ```
   feat: Add/update SOP [Name] — [one-line description]
   ```

5. **Update MEMORY.md** — Add entry to memory index (if it's a significant update/new learning)

---

## THE OWNER

- **Primary:** Coco (auto-executes this duty)
- **Approval:** User confirms SOP is "locked in" before Coco archives old version
- **Git access:** Coco commits on user's behalf (via safe commit protocol)

---

## EXAMPLES

### Example 1: New SOP Created
**Scenario:** User asks Coco to create "Warm Hold Email" SOP

**Coco's action:**
1. Create skills/warm_hold_email.md (working copy)
2. User reviews and approves
3. Coco automatically:
   - Copies to `SOPs/01_Candidate_Communication/warm_hold_email.md`
   - Updates `SOPs/README.md` with new entry
   - Creates git commit: "feat: Add SOP Warm Hold Email — for passed values, not-selected candidates"
   - Adds entry to MEMORY.md (if major new learning)

### Example 2: Existing SOP Updated
**Scenario:** Format correction to rejection emails

**Coco's action:**
1. Update `SOPs/01_Candidate_Communication/candidate_rejections.md`
2. Commits: "fix: Update Rejection Email SOP — blue bold headings, no asterisks (format locked)"
3. Updates MEMORY.md to note the correction

---

## NON-NEGOTIABLE RULES

- **Never skip the copy step.** Both locations must stay in sync.
- **Never let SOPs/README.md fall out of date.** If a SOP is added/changed, index is updated automatically.
- **Never delete old SOPs without user approval.** Archive them, don't delete.
- **Commits must be descriptive.** Other team members (Noah, future agents) need to understand what changed.

---

## STATUS

This is a **PERMANENT DUTY**. It's not a project task with an end date. It's a standard operating responsibility that applies to all future SOP work.

**Owner:** Coco  
**Status:** ACTIVE — Applies to all future SOPs
