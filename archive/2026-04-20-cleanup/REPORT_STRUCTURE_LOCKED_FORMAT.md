# REPORT STRUCTURE — LOCKED FORMAT SPECIFICATION

**Created:** 2026-04-20  
**Based on:** Memory files from /c/Users/Dell/.claude/projects/C--Agent-Coco/memory/  
**Status:** COMPLETE — All locked formats documented, ready for implementation

---

## TWO REPORT TYPES IN COCO

There are **two distinct report types** with different structures:

1. **Initial Screening Report** (CV Screening)
2. **Decision Brief Report** (Final Candidates & Decision View)

---

---

# REPORT TYPE 1: INITIAL SCREENING REPORT

## Purpose
Evaluate candidate CVs against Job Description. Manual review of all profiles. Rank by JD match + relevant experience.

## When Used
- After JD posted, before interviews
- After CV collection, before candidate phone calls
- For all positions (no exceptions)

---

## LOCKED FORMAT STRUCTURE

### SECTION 1: Email Header (MANDATORY)

**Style:**
- Dark navy background: `#1a2a3a`
- Centered, uppercase text
- Georgia serif font, white text

**Content:**
```
[Logo: Taleemabad]

PEOPLE & CULTURE · INITIAL SCREENING REPORT

[JOB TITLE — Large, White, Bold]

Job [X] · Taleemabad
```

**Example:**
```
PEOPLE & CULTURE · INITIAL SCREENING REPORT

Soul Architect / Conversational UX Designer

Job 26 · Taleemabad
```

---

### SECTION 2: Stat Boxes (MANDATORY)

**Count:** Exactly 4 boxes  
**Colors:** Red, Blue, Yellow, Gray  
**Layout:** Horizontal row with equal spacing

**Box 1 (Red):** Total Candidates Screened
```
42
Total Screened
```

**Box 2 (Blue):** Shortlisted Candidates
```
5
Shortlisted
```

**Box 3 (Yellow):** Maybe Pool
```
7
Maybe / Consider
```

**Box 4 (Gray):** No Hire
```
30
No Hire
```

**HTML Implementation:**
```html
<div style="background:#f44336;color:white;padding:20px;margin:10px;text-align:center;border-radius:8px;">
  <div style="font-size:36px;font-weight:bold;">42</div>
  <div style="font-size:14px;">Total Screened</div>
</div>
```

---

### SECTION 3: Key Observation (MANDATORY)

**What:** 2-3 sentence insight about the candidate pool  
**Tone:** Blue section heading, justified text, Georgia serif  
**Purpose:** Summarize patterns (e.g., "Strong design background across cohort, but limited product exposure")

**Format:**
```
[BLUE HEADING: Key Observation]

[Justified paragraph, Georgia serif, 15px font]
[2-3 sentences about cohort trends, strengths, gaps]
```

**Example:**
```
Key Observation

This cohort shows strong product instincts balanced with practical experience. 
Most candidates have 5-7 years of relevant work, with clear evidence of iterative 
problem-solving on real user challenges. Gap: limited formal behavioral science 
or psychology background across the pool.
```

---

### SECTION 4: Shortlisted Candidates (MANDATORY)

**Count:** Usually 5 candidates (can vary)  
**Format:** Individual profiles, NOT a table  
**Per Candidate:**

```
[NUMBER]. [NAME — HYPERLINKED to Google Drive CV] | [RANKING] | [SCORE %]

App ID: ####  |  Total exp: ~X yrs  |  Relevant exp: ~X yrs  |  Expected Salary: [amount]  |  City: [location]  |  Relocate: [Y/N]  |  DB status: [status]

[3-4 sentence Description paragraph with evidence from CV]

[Gap paragraph addressing weaknesses or areas for development]
```

**Full Example:**
```
1. Muhammad Abdullah Safdar — #1 TOP PICK — 95%

App ID: 1277  |  Total exp: ~5 yrs  |  Relevant exp: ~4 yrs  |  Expected Salary: Not mentioned  |  City: Karachi  |  Relocate: Yes  |  DB status: shortlisted

Strongest combined signal across all criteria. Product-minded builder with deep 
human-centered design foundation and clear comfort navigating ambiguity. Background 
demonstrates iterative problem-solving on real user challenges. Ready for immediate impact.

None identified. Complete profile.
```

**Ranking Labels (Locked):**
- `#1 TOP PICK`
- `#2 TOP PICK`
- `#3 TOP PICK`
- `SHORTLIST`
- (More can be added, but maintain order)

**Score Range:** 78% – 95% (percentage based on JD match)

**Colors:**
- TOP PICK candidates: Verdict text in red (`#c62828`)
- SHORTLIST candidates: Verdict text in blue (`#1565c0`)

---

### SECTION 5: Maybe / Consider Candidates (MANDATORY)

**Format:** TABLE (not individual profiles)  
**Columns:** Candidate | Match % | Note

**HTML Table Structure:**
```
┌─────────────────────────────┬────────────┬───────────────────────┐
│ Candidate                   │  Match %   │ Note                  │
├─────────────────────────────┼────────────┼───────────────────────┤
│ Ahmad Hamdan Akram          │   62%      │ Builder orientation...│
│ Muhammad Ammar Khan         │   58%      │ Shows builder...      │
│ Aisha Bashir                │   55%      │ Product mindset...    │
└─────────────────────────────┴────────────┴───────────────────────┘
```

**Notes Column:** 1-2 sentence reasoning (why they're in Maybe pool)

---

### SECTION 6: Footer (MANDATORY)

**Format:**
```
Taleemabad Talent Acquisition  |  hiring@taleemabad.com  |  [Date]
```

**Font:** Georgia serif, 13px, gray text (`#555`)

---

## KEY RULES (Non-Negotiable)

1. **Format is LOCKED** — Exact match to reference format (April 6, 2026 Job 26 email)
2. **No PDF** — Always HTML email, not PDF attachment
3. **Stat boxes are required** — 4 boxes, exact colors, exact layout
4. **All names hyperlinked** — Every candidate name must link to Google Drive CV
5. **Georgia serif throughout** — No sans-serif fonts
6. **Blue headings** — All section headings in blue (#1565c0)
7. **Justified text** — All body paragraphs use text-align: justify
8. **Both experience fields required** — "Total exp: ~X yrs | Relevant exp: ~X yrs"
9. **All candidate info required** — Expected Salary, City, Relocate Y/N for each
10. **Gaps must be balanced** — Every shortlisted candidate gets strength + gap paragraph

---

## CHECKLIST BEFORE SENDING

- [ ] Header matches reference exactly (logo, navy bg, uppercase title)
- [ ] Stat boxes are 4, colored correctly, math verified
- [ ] Key Observation is 2-3 sentences, blue heading
- [ ] Shortlisted candidates: each has all 5 data fields
- [ ] Shortlisted candidates: each has description + gap paragraph
- [ ] Shortlisted candidates: names hyperlinked to Google Drive
- [ ] Maybe table: 3 columns (name, match %, note)
- [ ] Maybe candidates: names hyperlinked
- [ ] Footer with date added
- [ ] Georgia serif font throughout
- [ ] All section headings in blue (#1565c0)
- [ ] Body text is justified
- [ ] No PDF — HTML email only
- [ ] PILOT mode enabled (ask Ayesha before live)

---

---

# REPORT TYPE 2: DECISION BRIEF REPORT

## Purpose
Summarize final candidates after interviews, values calls, case studies. Provide decision-ready pipeline view with probing strategy.

## When Used
- After initial screening, candidates interviewed
- After values interviews completed
- When making shortlist decisions
- For final candidate selection review

---

## LOCKED FORMAT STRUCTURE

### SECTION 1: Header Block (MANDATORY)

**Style:**
- Dark navy background: `#1a2a3a`
- White text, centered
- Georgia serif font

**Content:**
```
[Logo: Taleemabad]

Final Candidates & Decision View

[POSITION TITLE]
```

**Example:**
```
Final Candidates & Decision View

Field Coordinator, Research & Impact Studies
```

---

### SECTION 2: Stat Boxes (MANDATORY)

**Count:** 4-5 boxes (depends on pipeline stage)  
**Colors:** Pastel (light backgrounds with dark text)  
**Layout:** Horizontal row

**Common Boxes:**
```
Box 1: Values Invites Sent
Box 2: Values Calls Completed
Box 3: Cleared / Offers Sent
Box 4: Debriefs This Week
Box 5 (Optional): Values Failed — OUT
```

**Example Numbers:**
```
15          8           3           2
Total       Values      Cleared     Debriefs
Applied     Completed   Values      This Week
```

---

### SECTION 3: Where We Are (MANDATORY)

**What:** Free-prose paragraph describing current pipeline state  
**Tone:** Professional, summary, no jargon  
**Purpose:** Provide context before detailed candidate blocks

**Format:**
```
[Blue Heading: Where We Are]

[Justified paragraph, Georgia serif]
[2-4 sentences about pipeline status, decisions pending, next steps]
```

**Example:**
```
Where We Are

We've completed initial interviews with 8 candidates and values calls with 6. 
Three have cleared values and are debrief-ready. Two debriefs are scheduled for 
this week. We're waiting on case study submissions from two strong candidates 
before final decisions.
```

---

### SECTION 4: Debrief Schedule (MANDATORY)

**Format:** TABLE  
**Columns:** Candidate (hyperlinked) | Date | Status | Notes

**HTML Table:**
```
┌──────────────────────┬─────────────────┬──────────────────┬──────────┐
│ Candidate            │ Date            │ Status           │ Notes    │
├──────────────────────┼─────────────────┼──────────────────┼──────────┤
│ Muhammad Hassan      │ 2026-04-22      │ Confirmed        │ —        │
│ Aisha Rahman         │ 2026-04-23      │ Pending confirm  │ —        │
│ Hassan Zafar         │ —               │ Case study in    │ Debrief  │
└──────────────────────┴─────────────────┴──────────────────┴──────────┘
```

**Status Values (Locked):**
- `DEBRIEF TODAY`
- `DEBRIEF CONFIRMED`
- `CASE STUDY IN` (waiting for debrief)
- `CASE STUDY SENT` (waiting for submission)
- `PANEL DECISION` (already debriefed, decision pending)
- `VALUES PASS` (values interview cleared)
- `OVERDUE` (action overdue)
- `NOT INTERVIEWED`

**Row Colors:**
- Green background: Confirmed debriefs
- Yellow background: Pending confirmations
- Gray background: Administrative (no debrief needed yet)

---

### SECTION 5: Leading Candidates (MANDATORY)

**What:** 2-4 top candidates with signal + probing strategy  
**Format:** Individual blocks (not table)  
**Per Candidate:**

```
[Name — hyperlinked to CV] | [Verdict Badge]

Debrief: [Date/Status]  
[Italic tagline about candidate]

[Signal paragraph — evidence from interviews/case study, 3-4 sentences]

At debrief, probe: [Dark red text, specific questions based on gaps]
- Question 1?
- Question 2?
- Question 3?
```

**Full Example:**
```
Muhammad Hassan | DEBRIEF CONFIRMED

Debrief: 2026-04-22, 2pm  
*Strong execution orientation with clear product thinking*

Values interview showed solid alignment across all criteria, particularly 
on continuous improvement and not holding on too tight. Case study was well-structured 
with clear recommendations. Team fit seems strong based on peer feedback. 
Question: depth on handling ambiguous situations.

At debrief, probe:
- Tell us about a time you had to make a decision with incomplete information
- How do you balance speed vs. perfectionism when building?
- What's a time you changed your mind on a product decision?
```

**Verdict Badges (Locked):**
- `DEBRIEF CONFIRMED`
- `DEBRIEF TODAY`
- `PANEL DECISION`
- `VALUES PASS`
- `CASE STUDY IN`

---

### SECTION 6: Discussion Candidates (OPTIONAL)

**What:** Candidates still under review or with flags  
**Format:** Same block format as Leading Candidates

**When to include:**
- Strong candidates needing more evaluation
- Candidates with concerns requiring probing
- Finalists tied for selection

**Example:**
```
Aisha Rahman | CASE STUDY IN

Status: Awaiting case study submission  
*Product mindset evident, strong communication skills*

...
```

---

### SECTION 7: Also in Pipeline (OPTIONAL)

**What:** All other candidates with status  
**Format:** TABLE  
**Columns:** Candidate (hyperlinked) | Status

**Example:**
```
┌──────────────────────┬─────────────────┐
│ Candidate            │ Status          │
├──────────────────────┼─────────────────┤
│ Hassan Zafar         │ Not interviewed  │
│ Rabia Zafar          │ Values failed    │
│ Muhammad Junaid      │ On hold          │
└──────────────────────┴─────────────────┘
```

---

### SECTION 8: Footer (MANDATORY)

**Format:**
```
[Optional Note section if needed]

Compiled by Coco  |  Taleemabad Talent Acquisition  |  [Date]
```

---

## KEY RULES (Non-Negotiable)

1. **Verdict labels are LOCKED** — Use exact labels from locked list only
2. **All names hyperlinked** — Every candidate name must link to Google Drive CV
3. **No scores** — Do NOT include numeric scores or ratings
4. **No PDF** — Always HTML email, never PDF attachment
5. **Probing questions required** — Every leading candidate needs "At debrief, probe:"
6. **Judgment-led** — Narrative format (not status tables), shows decision thinking
7. **Georgia serif throughout** — No sans-serif fonts
8. **Debrief dates only** — Show actual dates, no "Today/Tomorrow/This week" relative dates
9. **All names with CVs** — Audit every section before sending (Leading, Discussion, Pipeline)
10. **Inline HTML** — No PDF, no separate CV attachments

---

## CRITICAL: CV HYPERLINK AUDIT

**BEFORE SENDING any decision brief:**

1. List EVERY candidate name that appears anywhere:
   - Debrief Schedule: names + dates
   - Leading Candidates: each name
   - Discussion Candidates: each name
   - Also in Pipeline: each name

2. Cross-check against Google Drive CV links:
   - All names must have shareable Drive links
   - If name missing link, fetch CV from DB and upload

3. Example audit:
   ```
   ✓ Muhammad Hassan — Drive link confirmed
   ✓ Aisha Rahman — Drive link confirmed
   ✗ Hassan Zafar — MISSING — Upload CV, get link
   ✗ Rabia Zafar — Not in DB, cannot link (label bold only)
   ✓ Muhammad Junaid — Drive link confirmed
   ```

4. Do NOT send if any candidate name has no link/attribution
   - Either provide link or clearly label as "no CV available"

---

## CHECKLIST BEFORE SENDING

- [ ] Header matches reference exactly (navy bg, position title)
- [ ] Stat boxes: 4-5 boxes, correct count, math verified
- [ ] Where We Are: 2-4 sentences, blue heading, justified text
- [ ] Debrief Schedule: table complete, dates are actual (not relative)
- [ ] Leading Candidates: each has name (linked), verdict, date, signal paragraph, probes
- [ ] Discussion Candidates: same format as Leading (if applicable)
- [ ] Also in Pipeline: table complete (if applicable)
- [ ] ALL candidate names hyperlinked to Google Drive CVs
- [ ] No scores or ratings present
- [ ] No PDF — HTML email only
- [ ] Georgia serif font throughout
- [ ] All headings in blue (#1565c0)
- [ ] Body text justified
- [ ] Footer with date added
- [ ] PILOT mode enabled (ask Ayesha before live)

---

---

# MEMORY-BASED GENERATION PROMPT

**To be used when generating reports via Claude:**

```
You are generating a Coco report. Follow these rules EXACTLY.

REPORT TYPE: [Initial Screening / Decision Brief]

LOCKED FORMAT RULES:
1. Header: Dark navy (#1a2a3a), white text, centered, uppercase
2. Stat boxes: Exactly [4/5] boxes, [specific colors], equal spacing
3. Section headings: Blue (#1565c0), Georgia serif, no asterisks
4. Body text: Georgia serif, justified alignment (text-align: justify)
5. All candidate names: HYPERLINKED to Google Drive CVs
6. No PDF: HTML email format only
7. Footer: Include date, "Taleemabad Talent Acquisition"

[IF SCREENING]:
- Include Key Observation (2-3 sentences)
- Include Shortlisted (5 candidates) with description + gap paragraphs
- Include Maybe table (7 candidates) with name/match/note
- All data fields: Salary, City, Relocate Y/N, DB status

[IF DECISION BRIEF]:
- Include Where We Are (2-4 sentences)
- Include Debrief Schedule (table with actual dates, not relative)
- Include Leading Candidates (blocks with verdict + probes)
- Do NOT include scores
- All verdict labels from locked list only
- Audit ALL names for Drive links before sending

BEFORE SENDING:
- Verify stat box math
- Verify all names hyperlinked
- Verify no PDF (HTML only)
- Verify format matches locked structure exactly
- Run 8-item QA checklist
- Ask for approval before sending (PILOT → approval → LIVE)
```

---

## FILES REFERENCED

**Memory Files:**
- `/c/Users/Dell/.claude/projects/C--Agent-Coco/memory/skill_cv_screening_sop.md`
- `/c/Users/Dell/.claude/projects/C--Agent-Coco/memory/project_job32_decision_brief_format.md`
- `/c/Users/Dell/.claude/projects/C--Agent-Coco/memory/project_job36_decision_brief.md`
- `/c/Users/Dell/.claude/projects/C--Agent-Coco/memory/feedback_decision_brief_hyperlinks.md`
- `/c/Users/Dell/.claude/projects/C--Agent-Coco/memory/project_job26_soul_architect_final.md`

**Example Scripts:**
- `C:\Agent Coco\scripts\jobs\job26\send_job26_screening_report_final.py` (Screening example)
- `C:\Agent Coco\scripts\jobs\job36\send_job36_decision_brief_pilot.py` (Decision Brief example)
- `C:\Agent Coco\scripts\jobs\combined\send_combined_impact_reply_pilot.py` (Multi-position brief)

---

## STATUS: READY FOR IMPLEMENTATION

All report structures are now documented, locked, and ready for memory injection system integration.

**Next Step:** Build memory_loader.py to load this specification per task, inject it into generation prompt, and validate output before sending.
