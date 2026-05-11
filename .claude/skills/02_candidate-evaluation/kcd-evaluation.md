---
name: kcd-evaluation
description: Case study evaluation using Knowledge, Capacity, Design framework. 8-step evaluation with scorecard data, detailed assessment reports, integrity checks. Cross-check with Noah.
compatibility: Requires SOPs/02_Candidate_Evaluation/kcd-evaluation.md, Markaz API, Gmail access, evaluation framework
---

# KCD Evaluation

Evaluate case study submissions using Knowledge, Capacity, Design framework with detailed assessment reports, integrity checks, and cross-check with Noah's evaluations.

---

## When to Use This Skill

Trigger this skill when:
- User asks to "evaluate KCD submissions" or "case study solutions"
- Case study files available for candidates in Markaz
- Need to score using 5-point scale per criterion
- Need to produce detailed assessment report
- Need to identify integrity flags and AI-generation signals
- Cross-check needed with Noah's peer evaluation

---

## Related SOP (Source of Truth)

**Location:** `SOPs/02_Candidate_Evaluation/kcd-evaluation.md`

This skill orchestrates the detailed procedure for KCD case study evaluation. The SOP contains:
- Core philosophy (honesty of method, not outputs)
- 12-step workflow
- Prerequisites (assignment, datasets, framework, ideal answer)
- Scoring scale (1-5 per criterion, fractional scores required)
- Integrity checks (content dump, mirror problem, foundational misread)
- Incomplete submission handling
- Report format specification
- Verdict labels and thresholds
- Default scoring criteria
- Coco + Noah calibration standards
- 60%+ GWC advancement threshold
- Framework override rule

---

## Universal Rules (All KCD Evaluation)

**Core Philosophy:**
- Evaluate honesty of METHOD, not just outputs
- Look for how candidate arrived at conclusions
- Assess trustworthiness of judgment (not just correctness)
- Prefer strong reasoning with minor errors over correct output with weak reasoning

**Evaluation Data (Required):**
- Assignment prompt (what candidates were asked)
- Raw datasets (understand shape, columns, patterns)
- Ideal/reference answer (calibration benchmark)
- Candidate submissions (from Markaz + Gmail)
- Role-specific evaluation framework (if available)

**Scoring Scale:**
- 5 = Exceptional (original insight grounded in specific data)
- 4 = Strong (correct and thoughtful, minor gaps)
- 3 = Adequate (correct but surface-level)
- 2 = Weak (missed key patterns, AI as content generator)
- 1 = Absent or fundamentally wrong
- 0 = Not submitted (incomplete submissions only)

**Scoring Rules (Non-Negotiable):**
- Use fractional scores (4.5, 3.5, 1.5) for candidates between whole numbers
- Strong reasoning + minor data errors = high score (4-5)
- Weak reasoning + correct output = lower score (2-3)
- Insight without evidence = cap at 3
- Evidence without interpretation = cap at 3

**Verdict Thresholds:**
- 85%+ = STRONG HIRE
- 70-84% = HIRE
- 55-69% = CONDITIONAL (must state condition explicitly)
- 40-54% = BORDERLINE
- <40% = NOT RECOMMENDED

**GWC Advancement Threshold:**
- 60%+ advances to GWC
- State explicitly in report and Pipeline Recommendations

**Integrity Checks (Mandatory):**
- Content dump (emoji, markdown, generic language, off-topic research)
- Mirror problem (identical stats/phrases across candidates = likely same AI prompt)
- Foundational misread (wrong anchor figure or key variable early on)

**Incomplete Submission Handling:**
- Exclude from main ranking entirely
- Separate section: "Incomplete Submission — [Name]"
- Score marked with asterisk: "52%* — incomplete, not a capability read"
- Note: "score is floor, not ceiling" if strong signals present
- Never rank partial submission above full submission

---

## Detailed Procedure

**Prerequisites (Read in Order):**
1. Read Assignment: what candidates were asked, what datasets, what deliverable
2. Read Datasets Yourself: open every CSV, understand shape/patterns/anomalies
3. Read Evaluation Framework: use role-specific CLAUDE.md (or default 6 criteria)
4. Read Ideal Answer: gold standard for this assignment

**Collect Submissions:**
1. Source A — Gmail: Search `subject:New Case Study Submission [Role]`
   - Download attached files (PDF/Word/Excel)
   - Extract using gmail.users.messages.attachments().get()
2. Source B — Markaz DB: Query case_study_submission field (written text)
3. Google Sheets: Some submissions are Sheet URLs (read via Sheets API)
4. Cross-reference both; note "awaiting submission" if missing

**Evaluate (Per Candidate):**
1. Extract text from submission (preserve structure)
2. Read FULL submission (no skimming)
3. Score 1-5 per criterion (use fractional scores: 4.5, 3.5, etc.)
   - 5: exceptional insight grounded in data
   - 4: strong, correct, thoughtful
   - 3: adequate, surface-level
   - 2: weak, missed patterns, AI content-gen
   - 1: absent/wrong
   - 0: not submitted (incomplete only)
4. Apply weights from framework; calculate final %

**Integrity Checks (Mandatory):**
- Content dump: emoji, markdown, generic language, off-topic research
- Mirror problem: identical stats/phrases across candidates (likely same AI prompt)
- Foundational misread: key anchor figure/variable wrong early on

**Incomplete Submission Handling:**
- Exclude from main ranking
- Separate section: "Incomplete Submission — [Name]"
- Score marked with asterisk: "52%* — incomplete, not a capability read"
- Note: "score is floor, not ceiling"

**Report Generation:**
- HTML email (inline, not PDF)
- Per-candidate block: verdict + score + confidence + tagline + narrative + gap + conditional clause + GWC probes + integrity flag
- Narrative: tie observations to exercises (E1/E2/E3...) with specific evidence/quotes
- Cross-candidate comparative analysis (2-3 sentences on cohort patterns)

**Cross-Check with Noah (If Applicable):**
- If Noah's pilot available: read before finalizing
- Document score deltas
- Aligned (≤5%): proceed
- Diverging (>10%): flag to Ayesha before live send

---

## Execution Discipline

**STEP 1: PULL CANDIDATE LIST**
- Query Markaz applications table for role
- Get app IDs, emails, current status
- Use Gmail as authoritative source for submission status
- Note: DB status often stale; verify via Gmail

**STEP 2: COLLECT SUBMISSIONS**
- Source A — Gmail: Search `subject:New Case Study Submission [Role]`
- Download attached files (PDF, Word, Excel)
- Source B — Markaz DB: `case_study_submission` field (written text)
- Google Sheets: Some candidates submit tracker as Sheet URL
- Cross-reference both sources; note "awaiting submission" if missing

**STEP 3: EXTRACT TEXT**
- Parse each file to readable plain text
- Preserve structure (headings, lists, tables)
- Name files clearly by candidate name

**STEP 4: READ EVALUATION MATERIALS (In Order)**
- Read Assignment: what were candidates asked? what datasets? what deliverable?
- Read Datasets Yourself: open every CSV, understand shape, patterns, anomalies
- Read Framework: if role-specific CLAUDE.md exists, use it (primary scoring guide)
- Read Ideal Answer: gold standard for this specific assignment

**STEP 5: READ CANDIDATE SUBMISSIONS**
- Only after completing Step 4, open submissions one at a time
- Read fully (no skimming)
- Note: specific IDs/values cited? path from observation to conclusion? verifiable claims? AI signals?

**STEP 5B: IDENTIFY INCOMPLETE SUBMISSIONS**
- Scan all submissions for completeness BEFORE scoring
- Pull incomplete candidates out immediately
- Note which exercises missing
- Handle separately (see Incomplete Submission Handling above)

**STEP 6: SCORE EACH CANDIDATE**
- Apply scoring scale (1-5 per criterion)
- Use fractional scores (4.5, 3.5, etc.)
- Strong reasoning + minor errors = high score
- Weak reasoning + correct output = lower score
- Apply weights from framework; calculate final percentage

**STEP 7: INTEGRITY CHECK (Mandatory)**
- Content dump? (emoji, markdown, generic, off-topic)
- Mirror problem? (identical stats/phrases across candidates)
- Foundational misread? (wrong anchor figure early on)
- Flag any signals found

**STEP 7B: HANDLE INCOMPLETE SUBMISSIONS**
- Exclude from main ranking entirely
- Separate section with asterisk on score
- Note: "score is floor, not ceiling"
- Supplementary assessment recommendation instead of verdict

**STEP 8: BUILD REPORT**
- HTML email format (not PDF attachment)
- Per-candidate: verdict + score, confidence level, 1-line tagline, narrative, gap, conditional clause, GWC guide, integrity flag
- Narrative: tie observations to specific exercises (E1, E2, E3...)
- Quote exact lines where signals strong
- Cross-candidate comparative analysis (2-3 sentences on cohort)

**STEP 9: CROSS-CHECK WITH NOAH**
- If Noah's pilot available: read before finalising Coco's scores
- Document score deltas per candidate
- Aligned (≤5% delta): proceed to send
- Diverging (>10%): flag to Ayesha before going live

**STEP 10: PILOT & APPROVE**
- Send to Ayesha + Jawad (pilot mode)
- Wait for explicit approval
- Send live after approval

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Only Google or Gmail submissions | Misses submissions from other source | Check BOTH Markaz + Gmail |
| Didn't read ideal answer | Lack calibration on what good looks like | Read gold standard before candidates |
| Didn't read datasets | Can't evaluate data honesty | Open CSVs, understand patterns yourself |
| Whole numbers only (no fractions) | Compresses meaningful differences | Use 4.5, 3.5, fractional scores |
| Score 0 for weak work | Looks identical to unsubmitted | Use 1 for weak; 0 only for missing |
| Paraphrase instead of quote | Loses signal in exact wording | Quote exact lines when strong |
| No transfer skill naming | Hidden sector-gap penalties | Explicitly name what transfers/doesn't |
| Vague confidence levels | Verdict stands alone | Add "high confidence in X, uncertain on Y" |
| No conditional statement | CONDITIONAL verdicts not actionable | State: "Condition: [specific thing]" |
| No GWC probe questions | Panel can't use guides | Write 3-4 probing questions per candidate |

---

## Success Criteria

✅ All evaluation materials read (assignment, datasets, framework, ideal answer)  
✅ All submissions read fully (no skimming)  
✅ Fractional scores used (4.5, 3.5, etc.)  
✅ Integrity checks completed  
✅ Incomplete submissions handled separately  
✅ Verdicts labeled (STRONG HIRE / HIRE / CONDITIONAL / BORDERLINE / NOT RECOMMENDED)  
✅ GWC advancement threshold stated (60%+)  
✅ CONDITIONAL verdicts have explicit conditions  
✅ GWC conversation guides (3-4 questions per candidate)  
✅ Cross-check with Noah completed  

---

## Self-QA Checklist (Before Pilot)

- [ ] Collected submissions from both Gmail + Markaz
- [ ] Extracted text from all submissions
- [ ] Read assignment prompt in full
- [ ] Read all datasets (understand shape, patterns)
- [ ] Read evaluation framework (or default criteria)
- [ ] Read ideal/reference answer (calibration)
- [ ] Read each candidate submission fully
- [ ] Identified incomplete submissions (pulled out before scoring)
- [ ] Scored each candidate (1-5 per criterion, fractional allowed)
- [ ] Integrity checks completed (content dump, mirror, misread)
- [ ] Report built with verdict + score + confidence + tagline + narrative
- [ ] Narratives tied to specific exercises (E1/E2/E3...)
- [ ] Quotes included (exact lines, not paraphrased)
- [ ] Gap clearly labeled, separate paragraph
- [ ] CONDITIONAL verdicts have explicit conditions
- [ ] GWC conversation guides written (3-4 questions per candidate)
- [ ] Incomplete submissions in separate section with asterisk
- [ ] Cross-candidate comparative analysis included
- [ ] Cross-check with Noah completed (if applicable)
- [ ] All findings ready for pilot approval

---

## Resources & Templates

**Locked SOP:**
- Full KCD Evaluation: `SOPs/02_Candidate_Evaluation/kcd-evaluation.md`

**Calibration References:**
- Soul Architect (March 2026): Aaqib Khan (94%), Zikra Fiaz (93%), Nain Tara (88%)
- Job 32 Fundraising (March 2026): Mizhgan Kirmani (83%), Hamdan Ahmad (52%*), Zain Ul Abideen (74%)

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)

---

## Commit to Discipline

I will evaluate KCD submissions with:
- ✅ All evaluation materials read (assignment, datasets, framework, ideal answer)
- ✅ Every submission read fully (no skimming)
- ✅ Fractional scores used (4.5, 3.5, etc.)
- ✅ Honesty of method assessed (not just outputs)
- ✅ Integrity checks completed (content dump, mirror, misread)
- ✅ Incomplete submissions handled separately
- ✅ CONDITIONAL verdicts with explicit conditions
- ✅ GWC guides (3-4 probing questions per candidate)
- ✅ Cross-check with Noah completed
- ✅ All checklist items passing

**Status:** ✅ PRODUCTION READY
