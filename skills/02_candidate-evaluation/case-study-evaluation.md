---
name: case-study-evaluation
description: Track case study submissions, assess quality, identify missing parts, proactive weekly reporting. Check Markaz AND Gmail. Auto-flag incomplete submissions.
compatibility: Requires SOPs/02_Candidate_Evaluation/case_study_evaluation.md, Markaz API, Gmail access
---

# Case Study Evaluation

Track case study submissions, evaluate quality and completeness, auto-flag incomplete submissions, and provide proactive weekly status reports.

---

## When to Use This Skill

Trigger this skill when:
- User needs to "check case study submissions"
- User asks for "case study status" or progress tracking
- Candidates have been sent case study (48-hour deadline)
- Need to identify missing parts and quality concerns
- Need proactive weekly reporting to Ayesha

---

## Related SOP (Source of Truth)

**Location:** `SOPs/02_Candidate_Evaluation/case_study_evaluation.md`

This skill orchestrates the detailed procedure for tracking and evaluating case studies. The SOP contains:
- 8-step evaluation process
- Automation requirements (auto-flag incomplete)
- Weekly proactive reporting format
- Quality assessment criteria
- AI-detection indicators
- Non-negotiable rules (check both sources, read full submission, etc.)
- Pre-send checklist
- Common mistakes (8 items)

---

## Universal Rules (All Case Study Evaluation)

**Source Verification (CRITICAL):**
- Check BOTH Markaz AND Gmail (never one source only)
- Markaz: Candidate Communication section for submission
- Gmail: Search for "New Case Study Submission" + candidate name
- Candidates may submit via either channel (or both)

**Submission Processing:**
- Download submission (PDF, doc, spreadsheet, or Markaz form text)
- Read original assignment prompt FIRST (understand what was asked)
- Then read candidate submission in full (no skipping sections)
- Assess quality AND completeness separately

**Completeness Assessment:**
- Identify if any required section is missing or blank
- Note specific gaps (e.g., "Exercise 3 not submitted")
- Flag immediately if incomplete (don't wait for weekly report)

**Quality Assessment:**
- Evaluate depth of thinking (not just surface answers)
- Flag AI-use indicators (generic tone, boilerplate structure, lack of specificity)
- Flag weak effort (shallow answers, minimal engagement)
- Note in report if applicable

**Auto-Flag Automation:**
- When incomplete: send email to Ayesha immediately
- Subject: "[Candidate Name] Case Study Submitted — Missing Parts"
- Include list of missing/incomplete sections

**Weekly Reporting:**
- Send every week without being asked (proactive)
- Report: Submitted this week, Overdue, Needs Follow-up
- Include quality flags (AI, weak effort) where relevant

---

## Detailed Procedure

**Step 1: Check Both Sources (CRITICAL):**
- Markaz: Open each candidate profile → Candidate Communication section → check submission
- Gmail: Search hiring@ inbox for "New Case Study Submission" + candidate name + role
- Note submission timestamps
- Candidates may submit via Markaz, email, or both

**Step 2: Download & Organize:**
- Retrieve submission (PDF, doc, xlsx, or Markaz form text)
- Save locally for review
- Name files clearly by candidate name

**Step 3: Assess Completeness:**
- Read original assignment prompt FIRST (understand what was asked, expected deliverables, sections required)
- Then read candidate submission in FULL (no skimming)
- Check: all sections addressed? all exercises submitted? any blanks?

**Step 4: Auto-Flag Incomplete Submissions:**
- If any required section missing or blank: send email to Ayesha immediately
- Subject: "[Candidate Name] Case Study Submitted — Missing Parts"
- Body: List missing/incomplete sections specifically
- Don't wait for weekly report (flag immediately)

**Step 5: Assess Quality:**
- Evaluate: depth of thinking, clarity, completeness
- Flag AI-use indicators (generic tone, boilerplate structure, lack of specificity)
- Flag weak effort (surface answers, minimal engagement)
- Document findings

**Step 6: Weekly Proactive Report (Every Week, No Ask):**
- **Submitted This Week:** names, app IDs, roles, quality flags
- **Overdue:** names, days overdue, recommendation for follow-up
- **Needs Follow-up:** reason (incomplete, AI flagged, quality concerns)
- Send to Ayesha every week without being asked

---

## Execution Discipline

**STEP 1: IDENTIFY THIS SKILL**
- User says "check case study submissions" or "case study status"
- Regular weekly reporting needed

**STEP 2: READ LOCKED RESOURCES**
- SOPs/02_Candidate_Evaluation/case_study_evaluation.md: Full SOP
- Markaz: Check applications for current status
- Gmail: Search for case study notifications

**STEP 3: CHECK BOTH SOURCES**
- Markaz: Open each candidate profile → Candidate Communication section
- Check if submission present, submission timestamp
- Gmail: Search hiring@ inbox for "New Case Study Submission" + role
- Note candidates in both sources

**STEP 4: DOWNLOAD SUBMISSIONS**
- Retrieve each submission (PDF, doc, xlsx, or form text)
- Save locally for detailed review
- Have submission ready before evaluation

**STEP 5: READ ORIGINAL ASSIGNMENT**
- Pull original case study prompt sent to candidate
- Understand exact questions asked
- Understand expected deliverables
- Understand required sections/exercises

**STEP 6: READ CANDIDATE SUBMISSION FULLY**
- Open and read in full (don't skim)
- Read all pages, all documents
- For multiple candidates: read each one sequentially
- Take notes on quality and completeness observations

**STEP 7: ASSESS COMPLETENESS**
- Check: all required sections addressed?
- Check: all exercises submitted?
- Check: no blank/incomplete parts?
- If incomplete, note specifically what's missing

**STEP 8: ASSESS QUALITY**
- Evaluate: depth of thinking
- Evaluate: clarity of answers
- Evaluate: completeness of response
- Flag AI-use indicators (generic, boilerplate, lack of specificity)
- Flag weak effort (surface answers, minimal engagement)

**STEP 9: AUTO-FLAG IF INCOMPLETE**
- If any section missing: send email to Ayesha immediately
- Subject: "[Candidate Name] Case Study Submitted — Missing Parts"
- List missing parts specifically
- Body: Candidate name, App ID, role, list of missing sections

**STEP 10: BUILD WEEKLY REPORT**
- Submitted this week (5 entries): names, app IDs, roles, quality notes
- Overdue (3 entries): names, app IDs, days overdue, recommendation
- Needs follow-up (2 entries): names, app IDs, reason for follow-up
- Send to Ayesha every week without asking

**STEP 11: PROACTIVE MONITORING**
- Run this skill weekly (Monday or Friday)
- Don't wait for user to ask
- Keep Ayesha informed proactively

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Checking only Markaz | Misses email submissions | Check BOTH Markaz + Gmail |
| Skimming submission | Miss quality/completeness gaps | Read full submission, all sections |
| Not knowing assignment | Can't evaluate answers | Read original prompt first |
| Mixing quality & completeness | Different assessments | Assess BOTH separately |
| Forgetting to flag incomplete | Wastes downstream time | Email Ayesha immediately, don't wait |
| No weekly reporting | Only report when asked | Proactive reporting is standard |
| Vague AI detection | Unspecific flags | Cite concrete indicators (language, structure) |
| Assuming best | Miss weak effort | Be honest in assessment |

---

## Success Criteria

✅ Both Markaz and Gmail checked for submissions  
✅ Original assignment read before evaluation  
✅ Submission read in full (all sections)  
✅ Completeness assessed (all parts present?)  
✅ Quality assessed (depth, clarity, thinking)  
✅ AI-use indicators noted (if relevant)  
✅ Incomplete submissions flagged to Ayesha immediately  
✅ Weekly proactive report sent (without being asked)  

---

## Self-QA Checklist (Before Weekly Report)

- [ ] Both Markaz and Gmail checked for submissions
- [ ] Original assignment prompt read and understood
- [ ] Each submission downloaded and ready for review
- [ ] Each submission read in full (all pages, all sections)
- [ ] Quality assessment complete (depth, clarity, thinking)
- [ ] Completeness assessment complete (all parts addressed?)
- [ ] AI-use indicators noted (if relevant)
- [ ] Weak effort flagged (if applicable)
- [ ] Incomplete submissions: email sent to Ayesha immediately
- [ ] Complete submissions: added to weekly report
- [ ] Weekly report ready (Submitted / Overdue / Needs Follow-up sections)
- [ ] Ready to send proactive report to Ayesha

---

## Resources & Templates

**Locked SOP:**
- Case Study Evaluation: `SOPs/02_Candidate_Evaluation/case_study_evaluation.md`

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)

---

## Commit to Discipline

I will evaluate case studies with:
- ✅ Both Markaz and Gmail checked (never one source only)
- ✅ Original assignment read before evaluation
- ✅ Full submission reading (no skimming)
- ✅ Quality and completeness assessed separately
- ✅ Incomplete submissions flagged to Ayesha immediately
- ✅ Proactive weekly reporting (without being asked)
- ✅ AI-use and weak effort honestly noted
- ✅ All 8-item checklist items passing

**Status:** ✅ PRODUCTION READY
