---
name: candidate-evaluation
description: Evaluate candidates across all stages (CV screening, case study evaluation, values interview scoring, KCD evaluation). Produce screening reports with 4 stat boxes, hyperlinked candidate profiles, and structured scoring. All evaluations require verified data, no fabrication, and specific evidence from source material.
compatibility: Requires RULES.md, memory/LOCKED_TEMPLATES_INDEX.md
---

# Candidate Evaluation

Screen, evaluate, and score candidates across CV, case study, values interview, and KCD stages. Produce detailed reports with ranking and recommendations.

---

## When to Use This Skill

Trigger this skill when:
- User asks to "screen candidates for [position]"
- User requests "evaluate case study submissions"
- User wants "values interview scoring" or "KCD evaluation"
- User needs a "screening report" or "candidate ranking"
- Any systematic evaluation requiring evidence-based assessment

---

## Related SOPs

All evaluation SOPs fall under this skill:

1. **CV Screening** — `SOPs/02_Candidate_Evaluation/cv_screening.md`
   - 14-15k character minimum
   - 4 stat boxes: screened, top-tier, maybe, advanced
   - Hyperlinked Google Drive CVs (non-negotiable)
   - Evaluation criteria: skills → experience → fit (priority order)

2. **Case Study Evaluation** — `SOPs/02_Candidate_Evaluation/case_study_evaluation.md`
   - Auto-flag incomplete submissions
   - Check Markaz AND Gmail for all submissions
   - Flag AI-generated or weak effort
   - Weekly proactive reporting

3. **Values Scorecard Scoring** — `SOPs/02_Candidate_Evaluation/values_scorecard_scoring.md`
   - Markaz JSON schema validation
   - Exact format: {date, host, candidateName, values[], finalComments, proceedToRightSeat}
   - Wrong schema = invisible on Markaz UI
   - 5-point scale per value

4. **KCD Evaluation** — `SOPs/02_Candidate_Evaluation/kcd-evaluation.md`
   - Case study evaluation framework
   - Technical assessment criteria
   - Problem-solving approach analysis

---

## Universal Rules (All Evaluation)

**Data Verification:**
- Every claim verified against source (CV, submission, scorecard)
- Quote directly from source, never paraphrase
- No assumptions or fabrication
- Flag unclear items (don't assume)

**Screening Reports:**
- Format: 4 stat boxes + candidate profiles + maybe table
- Stat box numbers MUST match section header counts
- Every candidate name linked to Google Drive CV (non-negotiable)
- 14-15k character minimum (never truncate to <10k)
- Profiles use TA_JUSTIFY (justified text)

**Scoring:**
- Use exact scorecard numbers (no rounding)
- Schema validation: {date, host, candidateName, values[], finalComments, proceedToRightSeat}
- Never modify Markaz data without verification
- Document scoring rationale

**Evaluation Criteria Priority:**
1. Skills → What can they do?
2. Experience → Have they done similar work?
3. Fit → Does this match our needs?

**Self-QA Before Sending:**
- [ ] Memory checked (MEMORY.md)
- [ ] Locked template read side-by-side
- [ ] All candidate names hyperlinked to Drive CVs
- [ ] Stat box numbers match section headers
- [ ] No fabrication (all claims sourced)
- [ ] No CV truncation (min 10k characters)
- [ ] Format matches REPORT_FORMAT_LOCKED.md
- [ ] Pilot sent to Ayesha first

---

## Execution Discipline

**STEP 1: IDENTIFY EVALUATION TYPE**
- Ask if unclear: "CV screening, case study, values scoring, or KCD?"

**STEP 2: READ LOCKED RESOURCES**
- RULES.md: Skill 1 (CV Screening lines 137-167)
- MEMORY.md: Specific evaluation SOP
- Locked template: screening report or scorecard schema

**STEP 3: GATHER SOURCE MATERIAL**
- CV Screening: All CVs (from candidates or Google Drive)
- Case Study: All submissions (from email, portal, Markaz)
- Values Scoring: Interview notes + notes from Markaz
- KCD: Case study submission + rubric

**STEP 4: EVALUATE SYSTEMATICALLY**
- Apply criteria in priority order (skills → experience → fit)
- Document specific evidence for each candidate
- Flag uncertain items (don't assume)
- Score consistently across all candidates

**STEP 5: STRUCTURE REPORT/SCORECARD**
- CV Screening: stat boxes + profiles + maybe table
- Case Study: submission status + auto-flags
- Values Scoring: Markaz JSON with exact schema
- KCD: scoring rubric + rankings

**STEP 6: VERIFY HYPERLINKS & DATA**
- Every candidate name linked to Drive CV
- Stat boxes match section counts
- Schema validated (Markaz)
- All numbers verified against source

**STEP 7: RUN 8-ITEM CHECKLIST**
- All 8 items must pass
- If any fail: fix and re-check

**STEP 8: PILOT & APPROVE**
- Send pilot to Ayesha
- Wait for approval
- Send live after approval

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| CV truncation to <10k chars | Loses context, feels rushed | Never truncate; use full CV (min 10k) |
| Stat count ≠ section count | Math error, looks careless | Recount: verify data matches headers |
| Missing Drive CV hyperlinks | Breaks usability | Use `=HYPERLINK()` formula for all names |
| Fabricated skills from CV | Violates verification rule | Quote directly from CV only |
| Not reading full submission | Missed context | Read complete submission before scoring |
| Rounding scorecard numbers | Loses precision | Use exact numbers from interview |
| Wrong Markaz schema | Data invisible on platform | Use exact: {date, host, candidateName, values[], finalComments, proceedToRightSeat} |
| Generic evaluation | Lacks evidence | Cite specific moments, skills, examples |
| Forgetting to flag incomplete | Wastes time downstream | Auto-flag at evaluation step |
| Sending report without pilot | Skips approval | Always pilot to Ayesha first |

---

## Success Criteria

✅ All candidate names linked to Google Drive CVs  
✅ Stat boxes match section headers (math correct)  
✅ No CV truncation (min 10k characters)  
✅ Every claim sourced from CV or submission  
✅ Evaluation criteria applied in order (skills → experience → fit)  
✅ Unclear items flagged (not assumed)  
✅ Markaz schema validated (if applicable)  
✅ Report format matches locked template  
✅ Pilot sent to Ayesha first  
✅ All 8-item checklist items pass  

---

## Resources & Templates

**Locked Templates:**
- Screening Report: `memory/REPORT_FORMAT_LOCKED.md`
- Locked Templates Index: `memory/_locked/locked_templates_index.md`

**Reference Scripts:**
- Job 26 screening: `scripts/jobs/job26/generate_job26_html_email.py`
- Soul Architect screening: `scripts/jobs/job26/soul_architect_screening_simple.py`

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)
- Skill 1 (CV Screening): `RULES.md` (lines 137-167)

---

## Commit to Discipline

I will evaluate candidates with:
- ✅ Verified data (every claim sourced)
- ✅ No fabrication (quote directly)
- ✅ Full CVs (never truncate <10k)
- ✅ All hyperlinks to Drive CVs
- ✅ Stat boxes matching section counts
- ✅ Criteria applied (skills → experience → fit)
- ✅ Unclear items flagged (not assumed)
- ✅ All 8-item checklist items passing

**Status:** ✅ PRODUCTION READY
