---
name: decision-briefs
description: Final hiring recommendations after all interview rounds. 4-part inline HTML email. Hyperlinked CVs. Verdict labels. DB status ≠ truth.
compatibility: Requires SOPs/03_Hiring_Operations/decision_briefs.md, RULES.md Skill 6, Google Drive CV links
---

# Decision Briefs

Send final hiring recommendations to stakeholders after all interview rounds with hyperlinked CVs, verdict labels, and pipeline summary.

---

## When to Use This Skill

Trigger this skill when:
- User says "send decision brief" or "final recommendations"
- All interview rounds complete (CV → case study → values → debrief)
- Need to summarize verdicts for hiring manager
- Format: inline HTML email (no PDF)
- Recipients: Ayesha + hiring manager

---

## Related SOP (Source of Truth)

**Location:** `SOPs/03_Hiring_Operations/decision_briefs.md`

This skill orchestrates the procedure for decision briefs. The SOP contains:
- 4-part structure (Header, Leading, Pipeline, Debrief Schedule)
- Stat box specification (4 colored boxes)
- Verdict label rules (exact labels)
- Hyperlink requirement (every name linked to Google Drive CV)
- Pipeline grouping (VALUES PASS, VALUES OUT, CASE STUDY OUT, OVERDUE, NOT INTERVIEWED)
- Debrief schedule format
- Format specification (inline HTML, no PDF)

---

## Universal Rules (All Decision Briefs)

**Email Format:**
- Inline HTML (no PDF attachment)
- Dark navy header (#1a2a3a)
- Blue section headings
- Georgia serif, justified
- No asterisks in headings

**4-Part Structure (Required):**
1. Header & Stat Boxes (4 colored boxes)
2. Leading Candidates (strongest recommendations)
3. Pipeline Summary (all other candidates, grouped by status)
4. Debrief Schedule & Next Steps

**Stat Boxes (4 required):**
- Total candidates screened (red/pink)
- Total values calls conducted (blue)
- Total shortlisted (yellow/orange)
- Decision status (gray)

**Verdict Labels (EXACT):**
- "PANEL DECISION" (decision made)
- "DEBRIEF CONFIRMED" (debrief completed, verdict set)
- "DEBRIEF SCHEDULED" (debrief date set)
- "OVERDUE" (debrief not yet scheduled)

**Hyperlinks (Non-Negotiable):**
- EVERY candidate name must be hyperlinked to Google Drive CV
- Sections: Leading, Pipeline (all groups), Debrief Schedule
- No plain text names; all clickable

**Database Status Warning:**
- DB status ≠ truth (status may be outdated)
- Use interview evidence, not DB status
- Flag discrepancies if found

---

## Detailed Procedure

**Data Preparation:**
1. Query Markaz for all candidates (pull CV links, case study scores, values verdicts, debrief status)
2. Upload CVs to Google Drive (if not done) and extract shareable links
3. Organize candidates by status (leading, values pass pending, values out, case study out, overdue, not interviewed)

**Build 4-Part Report:**

**Part A: Header & Stat Boxes**
- Dark navy (#1a2a3a) header
- 4 stat boxes: Total screened | Values calls | Shortlisted | Decision status

**Part B: Leading Candidates (Top Recommendations)**
- Per candidate:
  - Name (hyperlinked to Google Drive CV)
  - Current role & company
  - 2-3 key strengths (tied to JD)
  - Case study performance (Tier + score)
  - Values assessment (PASS or CONDITIONAL)
  - Debrief verdict (use exact label: PANEL DECISION / DEBRIEF CONFIRMED / DEBRIEF SCHEDULED / OVERDUE)
  - Recommendation (clear next action)

**Part C: Pipeline Summary (5 Groups)**
1. VALUES PASS but debrief pending — names (hyperlinked), case study score, debrief date
2. VALUES OUT — names (hyperlinked), specific gap, case study tier
3. CASE STUDY OUT / Did Not Advance — names (hyperlinked), tier, reason
4. OVERDUE / Pending Submission — names, timeline, follow-up status
5. NOT INTERVIEWED — names (hyperlinked), screening verdict, reason not advanced

**Part D: Debrief Schedule & Next Steps**
- Candidates with debrief dates scheduled
- Format: "Name — [Date] [Time] via Teams"
- Include Teams link if available

**HTML Format:**
- Inline HTML (no PDF)
- Blue section headings
- Georgia serif, justified
- No asterisks in headings

**Hyperlink Audit (CRITICAL):**
- Every candidate name in Leading: hyperlinked
- Every candidate name in Pipeline (all 5 groups): hyperlinked
- Every candidate name in Debrief Schedule: hyperlinked
- Test 2-3 links (verify they load)

---

## Execution Discipline

**STEP 1: IDENTIFY THIS SKILL**
- User says "decision brief" or "final hiring recommendations"
- All interviews complete (CV → case study → values → debrief)

**STEP 2: READ LOCKED RESOURCES**
- SOPs/03_Hiring_Operations/decision_briefs.md: Full SOP
- RULES.md: Skill 6 (Decision Brief, lines 324-354)
- memory/feedback_decision_brief_hyperlinks.md: Hyperlink requirements

**STEP 3: GATHER CANDIDATE DATA**
- Query Markaz for all candidates
- Get CV links (upload to Google Drive if not yet done)
- Extract: case study scores, values verdicts, debrief status

**STEP 4: IDENTIFY LEADING CANDIDATES**
- Select strongest recommendations (Tier 1, high scores)
- Get their: CV link, strengths, case study tier, values verdict, debrief verdict
- Prepare: specific examples from their work

**STEP 5: GROUP PIPELINE CANDIDATES**
- Group 1: VALUES PASS but debrief pending
- Group 2: VALUES OUT (specific gap noted)
- Group 3: CASE STUDY OUT
- Group 4: OVERDUE / Pending submission
- Group 5: NOT INTERVIEWED

**STEP 6: BUILD HEADER & STAT BOXES**
- Dark navy header (#1a2a3a)
- 4 stat boxes: Total screened, Values calls, Shortlisted, Decision status
- Stat count = 4 sections below (required)

**STEP 7: BUILD LEADING CANDIDATES SECTION**
- Per candidate:
  - Name (hyperlinked to Google Drive CV)
  - Current role & company
  - Key strengths (2-3 bullets)
  - Case study performance (tier + score)
  - Values assessment (PASS or CONDITIONAL)
  - Debrief verdict (use exact label)
  - Recommendation (clear next action)

**STEP 8: BUILD PIPELINE SUMMARY**
- 5 groups (VALUES PASS pending, VALUES OUT, CASE STUDY OUT, OVERDUE, NOT INTERVIEWED)
- Each candidate: name (hyperlinked), case study tier, reason/status
- Example: "Muhammad Hassan (Tier 1, 84%) — Debrief scheduled 2026-04-15"

**STEP 9: BUILD DEBRIEF SCHEDULE**
- List candidates with debrief dates scheduled
- Format: "Name — [Date] [Time] via Teams"
- Include Teams link if available

**STEP 10: VERIFY HYPERLINKS**
- AUDIT: Every candidate name in Leading section hyperlinked
- AUDIT: Every candidate name in Pipeline groups hyperlinked
- AUDIT: Every candidate name in Debrief Schedule hyperlinked
- Test 2-3 links by clicking

**STEP 11: RUN SELF-QA CHECKLIST**
- All items must pass before sending

**STEP 12: PILOT & APPROVE**
- Send to Ayesha for approval
- Wait for explicit approval
- Send live after approval

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Missing hyperlinks | Names not clickable | Hyperlink every name to Drive CV |
| Wrong verdict labels | Inconsistency with spec | Use exact: PANEL DECISION / DEBRIEF CONFIRMED / etc. |
| Stat count ≠ 4 | Math mismatch | Create exactly 4 stat boxes |
| PDF attachment | Wrong format | Use inline HTML, no PDF |
| Trusted DB status | Status may be outdated | Use interview evidence, flag discrepancies |
| Plain text names | Not linked | Every name must be hyperlinked |
| Missing pipeline groups | Incomplete summary | All 5 groups required (VALUES PASS, OUT, CASE OUT, OVERDUE, NOT INTERVIEWED) |
| Vague debrief verdict | Ambiguous | Use exact label (PANEL DECISION, DEBRIEF CONFIRMED, etc.) |
| No next step | Actionless | Include clear recommendation per candidate |

---

## Success Criteria

✅ 4-part structure present (Header, Leading, Pipeline, Debrief Schedule)  
✅ 4 stat boxes (and 4 sections below)  
✅ Every candidate name hyperlinked to Google Drive CV  
✅ Verdict labels exact (PANEL DECISION / DEBRIEF CONFIRMED / DEBRIEF SCHEDULED / OVERDUE)  
✅ Pipeline grouped by status (5 groups)  
✅ Case study tiers and scores included  
✅ Debrief schedule with dates/times  
✅ Inline HTML format (no PDF)  
✅ All 11-item checklist items pass  

---

## Self-QA Checklist (Before Pilot)

- [ ] Markaz candidate data pulled
- [ ] CV links uploaded to Google Drive
- [ ] Leading candidates identified and selected
- [ ] Header built with dark navy (#1a2a3a)
- [ ] 4 stat boxes created (Total screened, Values calls, Shortlisted, Decision status)
- [ ] Leading section: 3-5 candidates with strengths, case study, values, debrief verdict
- [ ] Pipeline summary: 5 groups created (VALUES PASS, VALUES OUT, CASE STUDY OUT, OVERDUE, NOT INTERVIEWED)
- [ ] Debrief schedule: dates and Teams links listed
- [ ] AUDIT: Every name in Leading section hyperlinked
- [ ] AUDIT: Every name in Pipeline section hyperlinked
- [ ] AUDIT: Every name in Debrief section hyperlinked
- [ ] All verdict labels exact (use PANEL DECISION, DEBRIEF CONFIRMED, etc.)
- [ ] Inline HTML format (no PDF)
- [ ] Ready for Ayesha approval

---

## Resources & Templates

**Locked SOP:**
- Decision Briefs: `SOPs/03_Hiring_Operations/decision_briefs.md`

**Hyperlink Reference:**
- CV Hyperlink Completeness: `memory/feedback_decision_brief_hyperlinks.md`

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)
- Skill 6 (Decision Brief): `RULES.md` (lines 324-354)

---

## Commit to Discipline

I will send decision briefs with:
- ✅ 4-part structure (Header, Leading, Pipeline, Schedule)
- ✅ Every candidate name hyperlinked to Google Drive CV
- ✅ 4 stat boxes (matching 4 sections)
- ✅ Exact verdict labels (PANEL DECISION / DEBRIEF CONFIRMED / etc.)
- ✅ Pipeline grouped by status (5 groups)
- ✅ Inline HTML format (no PDF)
- ✅ Clear next steps per candidate
- ✅ All 14-item checklist passing

**Status:** ✅ PRODUCTION READY
