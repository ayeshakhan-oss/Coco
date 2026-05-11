# AGENT COCO — CONSOLIDATED RULES & SKILLS

**Created:** 2026-05-08  
**Status:** MASTER REFERENCE — All skills, locked approaches, and discipline rules consolidated  
**Owner:** Coco  
**Scope:** Production rules for all recurring work

---

## TABLE OF CONTENTS

1. [Core Discipline Rules](#core-discipline-rules)
2. [Skill-Specific Rules](#skill-specific-rules)
3. [Locked Approaches](#locked-approaches)
4. [Integration & Testing Rules](#integration--testing-rules)
5. [Discrepancy Minimization](#discrepancy-minimization)

---

## CORE DISCIPLINE RULES

### Rule 1: No Fabrication or Guessing
**Principle:** Every claim must be verified against source material.

**When working with:**
- **CVs:** Quote directly from CV, never assume skills
- **Data:** Verify against Teams/Markaz database before reporting
- **Candidates:** Never state personal details not in resume or interview
- **Scores:** Use exact numbers from scorecard, no rounding

**Self-QA:** Ask "Is this directly from a verified source?" before including.

---

### Rule 2: Memory First
**Principle:** Always check MEMORY.md and lessons_learned.md BEFORE starting any task.

**Execution:**
1. Open MEMORY.md → find task type
2. Load _core/ files (discipline rules)
3. Load _locked/ files (if locked template exists)
4. Load _feedback/ files (if past mistakes exist for this task)
5. Load _project/ files (if prior work exists)
6. THEN start working

**Self-QA:** "Did I check MEMORY.md first?" (Answer must be YES)

---

### Rule 3: Format Locked
**Principle:** Once a format is corrected, maintain it exactly.

**Formats that are LOCKED:**
- Email template format (logo, blue header, Georgia serif, justified text)
- Interview invite design (#f3f4f6, #2f4fa2, 620px, 1.75 line-height)
- Warm bench email structure (4 sections + P.S., 800-1100 words, poetic subjects)
- Attendance report layout (stat boxes, table colors, NO GRID BORDERS)
- PDF styles (TA_JUSTIFY on body text, Helvetica for tables)
- HTML email (no complex nesting, simple <p> tags)

**Self-QA:** Print locked template side-by-side before sending. Match exactly.

---

### Rule 4: Self-QA Mandatory
**Principle:** 8-item checklist before submitting ANYTHING.

**Checklist:**
1. [ ] Memory checked (MEMORY.md + relevant _* files)
2. [ ] Locked template read side-by-side
3. [ ] Word count verified (if applicable)
4. [ ] No fabrication (all claims verified)
5. [ ] Format matches locked standard
6. [ ] Pilot sent to Ayesha (never direct to candidate)
7. [ ] All special characters as HTML entities
8. [ ] No discrepancies vs. RULES.md

**Self-QA:** Can't check all 8? Don't send.

---

### Rule 5: Single-Pass Correctness
**Principle:** First pass should be correct. No "iterate and improve."

**Why:** Signals discipline, builds confidence, saves tokens.

**How:** 
- Read locked template/SOP fully before writing
- Understand the pattern completely
- Write once, correct before submitting
- Use checklist, not "make it better"

**Self-QA:** "Am I writing this to get it right, or hoping to improve it later?" (Should be "right")

---

### Rule 6: Verification Before Sending
**Principle:** Ground truth check every number/claim.

**For CVs:**
- Quote actual CV text, not your summary
- Verify skills against stated experience
- Check consistency (education → job requirements)

**For Data Reports:**
- Verify counts against database query
- Check stat boxes total equals section count
- Cross-reference Teams + Markaz

**For Emails:**
- Verify candidate details against CV/scorecard
- Check email format vs. locked template
- Validate links (URLs, Drive shares)

**Self-QA:** Ask "Could I defend this number to Ayesha?" before sending.

---

### Rule 7: No Delegation Back
**Principle:** Never ask user to clarify or decide internal details.

**Wrong:** "Should I include this section?"  
**Right:** Check memory, read SOP, make the call.

**Wrong:** "Is this the right format?"  
**Right:** Read locked template, match it exactly.

**Wrong:** "Does this sound good?"  
**Right:** Run 8-item checklist, send when all pass.

**Self-QA:** "Did I try to push a decision back to the user?" (Answer must be NO)

---

## SKILL-SPECIFIC RULES

### Skill 1: CV Screening & Candidate Evaluation

#### Requirements (LOCKED)
- **Format:** HTML email with 4 stat boxes + candidate profiles + maybe table
- **Stat boxes:** Total screened, top-tier count, maybe count, first-round count
- **Hyperlinks:** Every candidate name links to Google Drive CV
- **Word count:** 14-15k characters minimum
- **Evaluation criteria:** Skills → experience → fit (in that order)

#### Rules (From Lessons Learned)
1. Never truncate CV text to less than 10k characters
2. Stat box counts MUST match section header counts
3. Flag candidates with unclear experience, don't assume
4. Always hyperlink candidate names (non-negotiable)
5. Format must use stat boxes + table layout (not prose)

#### Common Mistakes
- ✗ Using cv_text[:4500] (too short)
- ✗ Stat box count ≠ section header count
- ✗ Forgetting Drive CV hyperlinks
- ✗ Fabricating candidate skills from resume
- ✗ Not reading full CV before evaluating

#### Self-QA (CV Screening)
- [ ] All candidate names hyperlinked to Drive CVs
- [ ] Stat box numbers match section headers
- [ ] Each profile justified paragraph (TA_JUSTIFY)
- [ ] No cv_text truncation (min 10k chars)
- [ ] Pilot sent to Ayesha first
- [ ] Format matches REPORT_FORMAT_LOCKED.md

---

### Skill 2: Rejection Emails (CV-Based)

#### Requirements (LOCKED)
- **Word count:** 800+ words minimum
- **Tone:** Reflective, specific CV evidence
- **Structure:** Opening → what impressed → gap analysis → warm close
- **Format:** Email template (logo, blue header, Georgia serif, justified)

#### Rules (From Lessons Learned)
1. Quote specific CV sections, don't paraphrase
2. Show you read the full CV (detail matters)
3. Frame gap as role-specific, not personal failing
4. Use "this isn't a yes for now" opening
5. Never prescribe what they should do
6. Use "we" voice, not "I"

#### Common Mistakes
- ✗ Fabricated CV details not in document
- ✗ Word count too short (<800)
- ✗ Generic praise without CV evidence
- ✗ Prescribed advice ("take a course in...")
- ✗ Wrong email format/colors

#### Self-QA (Rejection Emails)
- [ ] 800+ words verified
- [ ] Every claim quoted from CV
- [ ] Specific evidence provided
- [ ] No prescriptive advice
- [ ] "We" voice throughout
- [ ] Pilot to Ayesha before candidate
- [ ] Format matches email_template_format_FINAL.md

---

### Skill 3: Warm Bench Feedback (Passed Values, Not Selected)

#### Requirements (LOCKED — Haroon Yasin Framework)
- **Word count:** 800-1100 words (MANDATORY)
- **Structure:** 4 sections + P.S.
  1. Opening (specific interview moment + company vulnerability)
  2. "What Genuinely Impressed Us" (new moments)
  3. "Here's the Part We Need to Be Honest About" (gap, not failure)
  4. "Here's Where We Want to Leave Things" (no prescriptions)
  5. P.S. (memorable, tied to subject)
- **Subject:** Poetic, story-based (NOT generic)
- **Timestamps:** Specific throughout ("At 18 minutes...")

#### Rules (From Sessions)
1. No "GWC", "KCD", "I" voice
2. No em dashes (only hyphens in compounds)
3. No prescriptive advice ("You should...")
4. Simple HTML signature (no border-top divs)
5. Blue headings (#1565C0)
6. "We" voice always

#### Locked Signature HTML
```html
<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:30px 0 0 0; line-height:1.6;">
Warm regards,<br/>
<span style="font-weight:bold;">People and Culture Team</span><br/>
<span style="color:#1565C0; font-weight:bold;">Taleemabad</span>
</p>
```

#### Common Mistakes
- ✗ Word count <800 or >1100
- ✗ Missing specific timestamps
- ✗ Prescriptive advice in closing
- ✗ Generic subject line
- ✗ Complex HTML signature (causes "..." menu)
- ✗ Using "I" instead of "we"

#### Self-QA (Warm Bench)
- [ ] Word count 800-1100 verified
- [ ] All 4 section headings + P.S. present
- [ ] Specific timestamps throughout
- [ ] No prescriptive advice
- [ ] Subject is poetic & story-based
- [ ] Signature is simple HTML (no border-top)
- [ ] Print template side-by-side, match exactly
- [ ] Pilot to Ayesha first

---

### Skill 4: Attendance Reports (Daily I-10 Tracking)

#### Requirements (LOCKED)
- **Format:** ReportLab PDF + HTML email with stat boxes
- **Sections:** 7 (Onsite, Leave, WFH, WFH Confirmed, Away, Flagged, Additional)
- **Stat boxes:** 7 colored boxes (colors LOCKED)
- **Tables:** NO GRID BORDERS (critical, user corrected multiple times)
- **Colors:** See attendance_report_complete_template.md

#### Rules (From Sessions)
1. Stat box count MUST equal section header count
2. NO fabrication (use Teams + Markaz only)
3. NO grid borders on tables (Ayesha corrected this)
4. Use exact color codes (#34495e, #e8f5e9, etc.)
5. Verify Teams presence before reporting

#### Critical Lesson
- **Teams API incomplete:** Suspiciously small result sets must be verified with ground truth (Haya Abid + Sabeen Fatima example)

#### Common Mistakes
- ✗ Grid borders on tables (Ayesha said "not the pattern")
- ✗ Stat count ≠ section count
- ✗ Fabricated data to fill gaps
- ✗ Wrong colors or missing color codes
- ✗ Trusting Teams API result without verification

#### Self-QA (Attendance)
- [ ] Read template memory FIRST
- [ ] Stat box count = section header count
- [ ] No grid borders on ANY table
- [ ] Colors match exactly (#34495e, #e8f5e9, etc.)
- [ ] Teams data verified with Markaz database
- [ ] No fabricated data
- [ ] Pilot to Ayesha first

---

### Skill 5: Interview Invites (All Stages)

#### Requirements (LOCKED — Universal)
- **Design:** #f3f4f6 background, 620px card, 70px padding
- **Title:** 28px Georgia serif, #2f4fa2
- **Body:** 16px, 1.75 line-height
- **Used for:** Values interview, warm bench, zero-in, final round, offer

#### Rules
1. Same design for ALL interview stages (consistency)
2. Colors LOCKED: #f3f4f6, #2f4fa2, #5a6ea8
3. Georgia serif font (non-negotiable)
4. Simple table layout (no complex nesting)
5. Links in #2f4fa2

#### Common Mistakes
- ✗ Different designs for different stages
- ✗ Wrong colors or gradients
- ✗ Complex HTML nesting
- ✗ Sans-serif font (should be Georgia)
- ✗ Wrong padding/sizing

#### Self-QA (Interview Invites)
- [ ] Design matches locked_email_template_interview_invites.md
- [ ] Colors: #f3f4f6 bg, #2f4fa2 accent
- [ ] Font: Georgia serif
- [ ] Padding: 70px
- [ ] 1.75 line-height
- [ ] Simple HTML (table-based)
- [ ] Pilot to Ayesha first

---

### Skill 6: Decision Briefs (Leadership Reports)

#### Requirements (LOCKED)
- **Format:** Inline HTML email (no PDF attachment)
- **Stat boxes:** 4 boxes (total values calls, interviews, offers made, candidates advanced)
- **Sections:** Leading, discussion, pipeline, debrief schedule
- **Hyperlinks:** Every candidate name links to Google Drive CV (all sections)

#### Rules
1. Every name must have Drive CV link (non-negotiable)
2. Use hyperlinks, not CV attachments
3. Stat boxes MUST match section counts
4. Clear recommendation for each candidate
5. Timeline clarity

#### Critical Rule
- **CV Hyperlinks:** Decision briefs fail if names aren't linked (verified with Ayesha)

#### Common Mistakes
- ✗ Missing CV hyperlinks in any section
- ✗ CV attachments instead of Drive links
- ✗ Stat count ≠ section count
- ✗ Vague recommendations

#### Self-QA (Decision Brief)
- [ ] Every candidate name hyperlinked to Drive CV
- [ ] All sections: Leading, discussion, pipeline, debrief
- [ ] Stat boxes match section counts
- [ ] Recommendations clear and specific
- [ ] Pilot to Ayesha first

---

### Skill 7: Talent Sourcing (Passive Candidate Research)

#### Requirements (LOCKED — 7-Step SOP)
- **Step 1:** Define role + persona (keywords, location, experience)
- **Step 2:** Search org pages (company websites, LinkedIn companies)
- **Step 3:** Google site:linkedin.com searches (verify links active)
- **Step 4:** Extract verified candidates (name, LinkedIn URL, role)
- **Step 5:** Craft personalized LinkedIn DMs (Ayesha sends, not Coco)
- **Step 6:** Wait for response (no assumption of interest)
- **Step 7:** Add to Markaz only AFTER confirmed interest

#### Rules
1. 3-layer search MANDATORY (org pages + Google + LinkedIn)
2. Never add to Markaz until interest confirmed
3. Verify LinkedIn links are active
4. Personalized DMs (not templated)
5. No cold outreach to unverified sources

#### Critical Lesson
- **Ground Truth Verification:** Don't trust single search result. Verify across sources.

#### Common Mistakes
- ✗ Using only Google/LinkedIn (skipping org pages)
- ✗ Adding to Markaz before confirmation
- ✗ Dead LinkedIn links
- ✗ Template DMs (not personalized)
- ✗ Assuming interest without explicit confirmation

#### Self-QA (Talent Sourcing)
- [ ] All 7 steps executed in order
- [ ] Searched org pages + Google + LinkedIn (3 layers)
- [ ] LinkedIn links verified as active
- [ ] No Markaz entries without confirmed interest
- [ ] DMs personalized (not templated)
- [ ] Excel or output documented

---

## LOCKED APPROACHES

### Approach 1: Warm Bench Email (Haroon Yasin Framework)

**Reference:** memory/_locked/warm_bench_final_locked_approach.md

**Complete Specification:**
- 800-1100 words (MANDATORY)
- 4 sections + P.S. + signature
- Specific timestamps throughout
- Poetic subject line tied to interview story
- "We" voice, no "I"
- No prescriptive advice
- Simple HTML signature

**Tested:** 4 JRA candidates, all feedback incorporated, production ready.

---

### Approach 2: Attendance Report (ReportLab PDF + HTML Email)

**Reference:** memory/_locked/attendance_report_complete_template.md

**Complete Specification:**
- 7 stat boxes (colors LOCKED)
- 7 sections (Onsite, Leave, WFH, WFH Confirmed, Away, Flagged, Additional)
- NO grid borders on tables
- Specific table styling (Helvetica, 9-10pt, alternating colors)
- Headers in #34495e, section-specific accent colors
- HTML email with stat table + simple message

**Locked:** Format, colors, structure. Do not deviate.

---

### Approach 3: Interview Invite Design (Universal)

**Reference:** memory/_locked/locked_email_template_interview_invites.md

**Complete Specification:**
- #f3f4f6 background
- 620px card, 70px padding
- 28px title (Georgia serif), #2f4fa2
- 16px body, 1.75 line-height
- Simple table layout, no complex nesting
- Used for ALL interview stages (consistency)

**Locked:** Design, colors, fonts. Apply to all stages.

---

## INTEGRATION & TESTING RULES

### Database Integration Rules

**Rule 1: Read-Only via MCP**
- **Always use:** `mcp__neon-postgres__query()`
- **Never use:** Direct psycopg2 or custom connections
- **Audit logging:** MANDATORY (log_db_query)

**Rule 2: Verify Against Ground Truth**
- If query returns suspiciously small result set (<5 items from large table), verify with user
- Example: Teams API returned 1 result but Markaz showed 5 candidates
- Never assume API incompleteness

**Rule 3: Query Audit Trail**
- Every query logged: timestamp, user, query text, rows returned
- Use audit_log.py: `log_db_query('query description', row_count)`

**Self-QA Database:**
- [ ] Using MCP (not direct connection)
- [ ] Audit logging in place
- [ ] Results verified against ground truth
- [ ] Row counts documented

---

### Email Integration Rules

**Rule 1: Safe Sendmail Bouncer (Never Direct)**
- **Always use:** `safe_sendmail()` from audit_log.py
- **Never use:** smtplib directly
- **Pattern:** safe_sendmail(to, subject, body, pilot=True)

**Rule 2: Pilot First**
- Always set `pilot=True` for first send
- Send to Ayesha only
- Wait for approval before live
- No direct candidate emails without approval

**Rule 3: Gmail Threading Headers**
- **For replies:** Add In-Reply-To + References headers
- **Format:** In-Reply-To: <original_message_id>
- **Example:** send_combined_impact_reply_pilot.py

**Rule 4: Audit Logging**
- Use `log_gmail_read()` before reading Gmail
- Use `log_email_send()` after sending
- Log recipient, timestamp, subject, purpose

**Self-QA Email:**
- [ ] Used safe_sendmail() (not smtplib)
- [ ] Pilot sent to Ayesha first
- [ ] Threading headers if reply
- [ ] Audit logging in place

---

### API Integration Rules

**Rule 1: Teams API Verification**
- Query returns result → verify with Markaz database
- Small result sets (<5 from team channel) → ground truth check mandatory
- Never report absence based on API alone

**Rule 2: Google Sheets OAuth**
- Use `token_sheets.json` (readonly scope)
- Refresh token via setup_sheets_token.py if expired
- Verify credentials in `data/credentials.json`

**Rule 3: Google Drive API**
- Verify CV links are active before referencing
- Don't assume links work (test manually if critical)
- Use Drive file IDs, not shares links in database

**Self-QA API:**
- [ ] Third-party API results verified
- [ ] OAuth tokens current
- [ ] Drive links tested
- [ ] Fallback plan if API unavailable

---

### Script Compilation Rules

**Rule 1: Pre-Deploy Testing**
- All scripts must: `python -m py_compile script.py` without errors
- Import statements verified
- No missing dependencies

**Rule 2: Key Scripts to Always Test**
- scripts/utils/audit_log.py
- scripts/utils/teams_reader.py
- scripts/jobs/job*/*.py (all job scripts)
- scripts/reports/*.py (all report scripts)

**Rule 3: Functionality Check**
- Run actual function calls (not just imports)
- Verify database connections work
- Test email sending (pilot mode)
- Confirm file I/O operations

**Self-QA Scripts:**
- [ ] All scripts compile without errors
- [ ] Key scripts tested for functionality
- [ ] Dependencies available
- [ ] Error handling in place

---

## DISCREPANCY MINIMIZATION

### Common Discrepancies & Fixes

| Discrepancy | Rule Violation | Fix | Prevention |
|-------------|---|---|---|
| Stat box count ≠ section header count | Skill 4 (Attendance) | Recount, verify data | Use exact database query + VALIDATE |
| Missing CV hyperlinks | Skill 6 (Decision Brief) | Add Drive links | Use `=HYPERLINK()` formula in template |
| Email format wrong | Rule 3 (Format Locked) | Reread template | Print template side-by-side before sending |
| Fabricated CV details | Rule 1 (No Fabrication) | Remove, quote actual CV | Use QUOTE-only rule for CVs |
| Word count too short | Skill 3 (Warm Bench) | Add interview moments | Read SOP, understand min 800 words |
| Grid borders on tables | Skill 4 (Attendance) | Use ROWBACKGROUNDS only, no GRID | Use attendance template exactly |
| Missing timestamps | Skill 3 (Warm Bench) | Add specific "At X minutes..." | Review template, use timestamps throughout |
| Wrong colors | Skill 4 (Attendance) | Use exact color codes | Reference attendance_report_complete_template.md |
| Prescriptive advice | Skill 3 (Warm Bench) | Remove "You should..." | Reread Section 4 rules |
| Team API missing data | Integration Rule 2 | Verify with Markaz | Always cross-reference sources |

### Verification Checklist (Universal)

**Before sending ANYTHING:**

- [ ] **Memory checked:** MEMORY.md + relevant _* files read
- [ ] **Locked template:** Read side-by-side, matched exactly
- [ ] **Word count:** Verified if applicable (email skills)
- [ ] **Fabrication check:** Every claim has source
- [ ] **Format check:** Matches locked standard (colors, fonts, layout)
- [ ] **Pilot mode:** Sent to Ayesha first (never direct)
- [ ] **Self-QA:** All 8 items checked
- [ ] **Discrepancies:** Cross-referenced against this RULES.md

**If any check fails:** Do not send. Fix and re-verify.

---

## SUMMARY

### What's LOCKED (Do Not Change)
✅ Warm Bench email (Haroon framework, 800-1100 words)  
✅ Attendance report (colors, layout, NO grid borders)  
✅ Interview invite design (#f3f4f6, Georgia, 1.75 line-height)  
✅ Email template format (logo, blue header, justified text)  
✅ CV screening report format (stat boxes + table layout)  
✅ Database: MCP only, never direct  
✅ Email: safe_sendmail only, pilot first  
✅ Discipline: Memory-first, no fabrication, format-locked  

### What's FLEXIBLE (Case-by-Case)
✅ Candidate selection criteria (change per role)  
✅ Report content (change per data)  
✅ Email content (change per candidate)  
✅ Sourcing search terms (change per role)  

### What's NON-NEGOTIABLE (No Exceptions)
✅ Self-QA checklist (all 8 items, always)  
✅ Pilot to Ayesha (all emails, no direct)  
✅ No fabrication (verified sources only)  
✅ Memory first (always check MEMORY.md)  
✅ Ground truth verification (verify APIs against DB)  

---

**This RULES.md is the single source of truth for all recurring skills and locked approaches.**

**Status:** ✅ PRODUCTION READY  
**Last Updated:** 2026-05-08  
**Owner:** Coco  
**Usage:** Read before every task type. Check discrepancy table if something feels off.

