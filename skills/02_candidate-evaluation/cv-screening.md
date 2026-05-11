---
name: cv-screening
description: Manual CV screening against JD with multi-criterion evaluation, accurate ranking, Google Drive CV hyperlinks. 14k-15k character reading minimum. All CVs read, no shortcuts.
compatibility: Requires SOPs/02_Candidate_Evaluation/cv_screening.md, REPORT_FORMAT_LOCKED.md, RULES.md Skill 1
---

# CV Screening

Screen all candidate CVs manually and thoroughly against the job description with accurate ranking and hyperlinked candidate profiles.

---

## When to Use This Skill

Trigger this skill when:
- User asks to "screen candidates for [position]"
- All applications received for a position
- Need to evaluate CVs against JD
- Need to produce screening report with ranking
- Google Drive CV hyperlinks required
- All candidates read manually (no keyword-only filtering)

---

## Related SOP (Source of Truth)

**Location:** `SOPs/02_Candidate_Evaluation/cv_screening.md`

This skill orchestrates the detailed procedure for CV screening. The SOP contains:
- 7-step screening process
- Multi-criterion evaluation framework
- Reading capacity requirements (14k-15k characters minimum)
- Google Drive CV upload and hyperlink workflow
- Report format locked specification
- Execution discipline protocol
- 8-item self-QA checklist
- Common mistakes (17 items)

---

## Universal Rules (All CV Screening)

**Manual Reading (Non-Negotiable):**
- Every CV must be read manually by human judgment
- NO keyword scanning only
- NO skipping profiles
- Minimum reading capacity: 14,000-15,000 characters per resume
- Never truncate CVs to <10k characters

**Evaluation Criteria (Priority Order):**
1. **Skills** — What can they do? (TOP priority)
2. **Experience** — Have they done similar work? (TOP priority)
3. **Fit** — Does this match our needs? (Supporting)

**Experience Assessment:**
- State BOTH total experience AND relevant experience separately
- Do NOT conflate impressive company name with actual relevant experience
- Prioritize relevant experience alignment over company prestige

**Report Format (LOCKED):**
- Format locked after first approval
- NO regressions (format maintained exactly after approval)
- NO variations or improvements to locked format
- Stat boxes (4): Total / Shortlisted / Maybe / No Hire
- Georgia serif font throughout
- Blue section headings with underlines
- Shortlisted profiles with hyperlinks

**Google Drive Hyperlinks (Mandatory):**
- Every shortlisted candidate CV uploaded to Google Drive
- Every candidate name hyperlinked to shareable Drive link
- All links tested and verified before sending
- No missing links, no placeholder text

**Database Verification:**
- Flag discrepancies with Markaz status (don't assume status is correct)
- Verify candidate details from profile questions (Expected Salary, City, Relocate)
- Cross-reference if data seems inconsistent

---

## Detailed Procedure

**Preparation:**
1. Read JD thoroughly (understand role deeply, core requirements, must-haves vs nice-to-haves)
2. Confirm evaluation criteria with hiring manager (3-5 specific criteria, or use skills/experience/fit)
3. Find reference report format (locked in for consistency)

**CV Screening Workflow:**
1. Query Markaz: pull all candidate profiles for role
2. For each candidate: download and read CV in FULL (minimum 14k-15k characters)
   - Identify 2-3 genuine strengths
   - Identify 1-2 honest gaps
   - State BOTH total experience AND relevant experience separately
3. Evaluate against criteria: skills (priority 1) → experience (priority 1) → fit (priority 2)
4. Capture profile data: Expected Salary, City, Relocate status, App ID
5. Create ranking: shortlist (top matches), maybe (borderline), no-hire (screened out)

**Google Drive CV Upload & Hyperlinks:**
- Fetch base64-encoded PDFs from Markaz (candidates.resume_data)
- Decode and save as PDF files locally
- OAuth authenticate with Google Drive (browser-based flow)
- Upload each PDF with descriptive filename
- Set permissions to shareable (anyone with link can view)
- Extract shareable links: `https://drive.google.com/file/d/[ID]/view`
- Save to JSON mapping: candidate_name → URL

**Report Structure:**
- Header: Dark navy (#1a2a3a), "People & Culture", job title, subtitle
- 4 Stat Boxes: Total applications, Shortlisted, Maybe, No Hire (must equal 4 sections)
- Key Observation: 2-3 sentence observation about candidate pool
- Shortlisted Candidates: Name (hyperlinked) | Ranking | Match % | Strengths | Gap | Profile data
- Maybe Section: Table with Name (hyperlinked) | Match % | Note
- All names hyperlinked to Google Drive CVs

**Verification Before Sending:**
- Stat boxes math verified (sum = total)
- Every shortlisted name hyperlinked to Drive CV
- Every maybe name hyperlinked to Drive CV
- Test 2-3 links (verify they load)
- Format matches reference exactly (fonts, colors, spacing)

---

## Execution Discipline

**STEP 1: IDENTIFY THIS SKILL**
- User says "screen CVs" or "evaluate candidates for [position]"
- Need to produce screening report with ranking

**STEP 2: READ LOCKED RESOURCES**
- RULES.md: Skill 1 (CV Screening, lines 137-167)
- memory/REPORT_FORMAT_LOCKED.md: Report format locked
- SOPs/02_Candidate_Evaluation/cv_screening.md: Full SOP

**STEP 3: CONFIRM EVALUATION CRITERIA**
- Read JD thoroughly (understand role deeply)
- Identify 3-5 specific evaluation criteria (or use skills/experience/fit)
- Confirm criteria with hiring manager if multi-criterion scoring

**STEP 4: READ EVERY CV MANUALLY**
- Download from Markaz database
- Read fully (don't skim; minimum 14k-15k chars per CV)
- Note both total AND relevant experience separately
- Identify 2-3 genuine strengths per candidate
- Flag honest gaps or concerns

**STEP 5: ASSESS AGAINST JD**
- Map candidate experience to JD requirements
- Identify must-haves vs nice-to-haves alignment
- Don't rely on company name; read actual role
- Score each criterion (or create shortlist/maybe/no-hire tiers)

**STEP 6: CAPTURE PROFILE DATA**
- Expected Salary (from profile questions)
- City / Current location (from profile questions)
- Willingness to Relocate (Y/N from profile questions)
- DB status (check for discrepancies)
- Application ID

**STEP 7: UPLOAD CVs TO GOOGLE DRIVE**
- Fetch base64-encoded PDFs from Markaz database
- Decode and save as PDF files locally
- Authenticate with Google Drive via OAuth 2.0
- Upload each PDF with descriptive filename
- Set permissions to shareable (anyone with link can view)
- Extract Google Drive shareable links

**STEP 8: STRUCTURE REPORT**
- Header: Dark navy (#1a2a3a), "People & Culture", job title
- 4 stat boxes: Total applications, Shortlisted, Maybe, No Hire
- Key Observation: 2-3 sentence observation about candidate pool
- Shortlisted Candidates: ranked, match %, JD evidence, profile fields
- Maybe section: table with candidate, match %, note
- All names hyperlinked to Google Drive CVs

**STEP 9: RUN SELF-QA CHECKLIST**
- All 8 items must pass before sending

**STEP 10: PILOT & APPROVE**
- Send to Ayesha for approval
- Wait for explicit approval
- Send live after approval

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Keyword scanning only | Misses actual fit assessment | Read every CV manually in full |
| Skipping CVs | Unfair evaluation | Read all profiles completely |
| Conflating total & relevant exp | Misrepresents candidate | State BOTH separately |
| Company name as experience | Assumes role from org | Read actual job description in CV |
| Missing profile data | Report incomplete | Capture Salary / City / Relocate |
| Vague gaps | No specific evidence | Cite concrete CV/JD mismatch |
| No Google Drive hyperlinks | Names not clickable | Upload all CVs, extract links, hyperlink |
| Math errors in stat boxes | Wrong totals | Verify: shortlist + maybe + no-hire = total |
| Format regression | Approved format forgotten | Lock format after approval, maintain exactly |
| DB status not verified | False discrepancies missed | Flag when DB status doesn't match CV evidence |

---

## Success Criteria

✅ Every CV read manually and in full (14k-15k char minimum)  
✅ Both total AND relevant experience stated separately  
✅ Evaluated by criteria: skills → experience → fit  
✅ Expected Salary, City, Relocate captured for all  
✅ All shortlisted + maybe CVs uploaded to Google Drive  
✅ Every candidate name hyperlinked to Drive CV  
✅ Report format matches locked template exactly  
✅ Stat boxes math verified (sum = total)  
✅ DB discrepancies flagged  
✅ All 8-item checklist items pass  

---

## Self-QA Checklist (Before Sending)

- [ ] All CVs on Markaz opened and read manually (no keyword scanner only)
- [ ] Minimum 14k-15k character reading per CV confirmed
- [ ] Candidate profile questions read (Salary, City, Relocate captured)
- [ ] Total experience AND relevant experience stated separately for each
- [ ] Evaluation criteria applied (skills → experience → fit)
- [ ] All shortlisted + maybe CVs fetched, decoded, and saved locally
- [ ] Google Drive OAuth authentication completed
- [ ] All CVs uploaded to Google Drive, shareable links extracted
- [ ] AUDIT: Every name in Shortlisted section hyperlinked
- [ ] AUDIT: Every name in Maybe section hyperlinked
- [ ] AUDIT: Test 2-3 links by clicking to verify they load
- [ ] Report format matches reference exactly (header, stat boxes, fonts, colors)
- [ ] Stat boxes created and totals verified
- [ ] Key Observation written (patterns, insights)
- [ ] All 8-item self-QA items pass

---

## Resources & Templates

**Locked Templates:**
- Report Format: `memory/REPORT_FORMAT_LOCKED.md`
- Reference Implementation: Job 26 Soul Architect (April 6, 2026)

**Reference Scripts:**
- CV hyperlink workflow: `scripts/jobs/job26/oauth_upload_cvs.py`

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)
- Skill 1 (CV Screening): `RULES.md` (lines 137-167)

---

## Commit to Discipline

I will screen CVs with:
- ✅ Manual reading of every CV (14k-15k char minimum)
- ✅ Both total AND relevant experience stated separately
- ✅ Criteria applied (skills → experience → fit)
- ✅ Expected Salary, City, Relocate data captured
- ✅ All CVs uploaded to Google Drive
- ✅ Every name hyperlinked (Shortlist + Maybe)
- ✅ Report format locked and maintained
- ✅ All 8-item checklist passing

**Status:** ✅ PRODUCTION READY
