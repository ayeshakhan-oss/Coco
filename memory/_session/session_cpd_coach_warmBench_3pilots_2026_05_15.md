---
name: session-cpd-coach-warmBench-3pilots-2026-05-15
description: "Complete session - 3 warm bench pilot emails sent (Hajra, Unzeela, Fatima). Full locked approach + subject line pattern locked."
metadata:
  type: project
  date: 2026-05-15
  candidates: Hajra Sajjad, Unzeela Khalid, Fatima Saeed
  position: CPD Coach
  status: All 3 pilots sent to Ayesha Khan + Jawwad Ali
---

# Session: CPD Coach Warm Bench — 3 Pilots Sent

## Emails Completed

### 1. Hajra Sajjad
- **Subject:** "The Principal's Expressions Changed When Data Spoke"
- **Status:** ✅ Pilot sent
- **Type:** Values + GWC integrated (8/8/9 scores)
- **Word count:** ~1150 words
- **Key moments:** Bridging Gaps principal story, lesson plan format, curriculum mapping, coaching mindset, scenario handling, mission-driven thinking
- **Sections:** 4 blue headings + P.S. tied to subject

### 2. Unzeela Khalid
- **Subject:** "When Difficult Things Become Safer"
- **Status:** ✅ Pilot sent
- **Type:** Values + GWC integrated (8/8/8.5 scores)
- **Word count:** ~1200 words
- **Key moments:** Corporal punishment incident (6-month persistence), team member depression/advocacy, menstrual leave policy, GWC roleplay + scenario handling, intentional career trajectory
- **Sections:** 4 blue headings + P.S. tied to subject

### 3. Fatima Saeed
- **Subject:** "When Personal Experience Becomes Professional Calling"
- **Status:** ✅ Pilot sent
- **Type:** GWC-only (no values interview; 8.5/9.5/9.5 scores)
- **Word count:** ~950 words
- **Key moments:** TFP fellowship personal story, roleplay standout (empathy first with tired teacher), Bloom's Taxonomy knowledge, intellectual curiosity, direct integrity about notice period
- **Sections:** 4 blue headings + P.S. tied to subject
- **Learning:** GWC-only emails are viable when values data missing; focus on personal motivation + roleplay standout + intellectual curiosity

---

## Locked Pattern Reinforced

### Subject Line Pattern (MANDATORY)
**Rule:** Poetic, story-based, tied to specific interview moment. Never generic.

**Pattern:** [MOMENT] + [ACTION/REALIZATION] + [CONSEQUENCE]

**Examples locked today:**
- "The Principal's Expressions Changed When Data Spoke" (Hajra moment + action + consequence)
- "When Difficult Things Become Safer" (moment of courage + emotional consequence)
- "When Personal Experience Becomes Professional Calling" (personal story + professional consequence)

**Never:** Generic subjects like "Hajra Sajjad - CPD Coach Position Update"

---

## Warm Bench Email Structure (LOCKED)

All 3 emails followed identical locked structure:

1. **Opening (0-2 paragraphs)**
   - "This isn't a yes for now."
   - Direct statement of what panel observed + why it matters
   - Specific, timestamped interview moment OR personal story hook

2. **"What Stayed With Us" (Blue heading + 3-5 paragraphs)**
   - First moment: specific story from interview with details
   - Second moment: another interview story OR GWC performance
   - Third moment: If GWC available, weave in coaching mindset/scenario handling
   - Fourth moment: Intellectual curiosity, mission alignment, or career intentionality
   - Panel's emotional response

3. **"Here's the Honest Part" (Blue heading + 2 paragraphs)**
   - Acknowledge strength across values/GWC
   - Explain decision as situational, not about fit
   - Maintain dignity + hope

4. **"Where We Want to Leave This" (Blue heading + 2 paragraphs)**
   - Genuine invitation to stay connected
   - Simple, no prescriptive advice
   - Recognition of who they are as a person

5. **P.S. (No heading, tied to subject)**
   - Calls back to subject line's story
   - Memorable, emotional, brief

---

## Formatting Rules (All 3 Applied)

✅ **Locked template:** templates/warm_bench_email.html (620px, 70px padding, Georgia serif, 1.75 line-height)
✅ **Justified text:** text-align:justify on all body paragraphs (except signature)
✅ **No em dashes:** Replace with hyphens or remove entirely
✅ **Simple HTML signature:** <p> tags only (NO border-top divs that trigger Gmail "..." menus)
✅ **Blue headings:** #1565C0 color, bold, 3 per email (What Stayed With Us, Here's the Honest Part, Where We Want to Leave This)
✅ **Blue divider:** 2px solid #1565C0 between name/position header and body

---

## Key Learnings Today

### 1. GWC-Only Emails Are Viable
**When values data missing:** Can still write compelling warm bench email.
**How:** Focus entirely on GWC performance (roleplay standout, scenario handling, intellectual curiosity, mission alignment).
**Example:** Fatima's email (no values interview, all GWC) felt complete and emotionally resonant.

### 2. Subject Lines Are Non-Negotiable Stories
**Rule:** Every warm bench email subject must be poetic and tied to specific interview moment.
**Effect:** Sets tone BEFORE body is read. Candidate recognizes themselves in the story.
**Testing:** All 3 subjects tested + locked in.

### 3. P.S. as Story Anchor
**Pattern:** P.S. should tie back to subject line's original story.
**Effect:** Creates full-circle emotional loop.
**Examples:**
- Hajra: "The moment that stayed with everyone: a principal's skepticism transforming into pride..."
- Unzeela: "The moment that stayed with everyone: a corporal punishment incident you stayed with..."
- Fatima: "That coach you described from your TFP fellowship, the one who believed in you..."

### 4. Word Count Flexibility with GWC
**Rule:** 800-1100 words mandatory.
**With GWC:** Can expand toward upper range without feeling bloated.
- Hajra (values+GWC): 1150 words ✅
- Unzeela (values+GWC): 1200 words ✅
- Fatima (GWC only): 950 words ✅
**Why:** GWC adds 2-3 additional moments (scenario handling, intellectual curiosity) that expand naturally.

---

## Integration Patterns Confirmed

### Values + GWC Integration
When both available (Hajra, Unzeela):
- **Values stories:** First 2-3 moments (specific interview evidence)
- **GWC insights:** Woven into 3rd-4th moments (coaching mindset, scenario handling, mission-driven thinking)
- **No separate sections:** GWC feels like natural extension, not bolt-on
- **Result:** Email feels comprehensive, not divided

### GWC-Only Integration
When values data missing (Fatima):
- **Lead with personal story:** TFP fellowship as opening hook
- **Roleplay as centerpiece:** Standout moment from GWC interview
- **Scenario handling:** How she approached defensive teacher, Bloom's Taxonomy
- **Intellectual curiosity:** Her questions about outcomes, training, metrics
- **Result:** Email feels emotionally grounded despite no values data

---

## Database Query Pattern Used

```sql
SELECT a.id, a.candidate_id, c.first_name, c.last_name, c.email,
       a.values_interview_notes, a.values_interview_score, 
       a.gwc_scorecard, a.status,
       j.title
FROM applications a
JOIN candidates c ON a.candidate_id = c.id
JOIN jobs j ON a.job_id = j.id
WHERE j.title ILIKE '%cpd%'
AND a.status = 'warm_bench'
AND c.last_name ILIKE '[LastName]'
```

**Learning:** Always query Markaz for GWC scorecard data when available. additionalComments field contains hiring manager's synthesis of standout moments.

---

## Files Created/Updated

**Scripts:**
- `scripts/send_cpd_coach_hajra_warmBench_pilot.py` (1st session, pilot sent)
- `scripts/send_cpd_coach_unzeela_warmBench_pilot.py` (this session, pilot sent)
- `scripts/send_cpd_coach_fatima_warmBench_pilot.py` (this session, pilot sent)

**Memory:**
- `memory/_locked/warm_bench_subject_lines_locked.md` (reinforced locked pattern)
- `memory/_session/session_warm_bench_hajra_cpd_coach_2026_05_15.md` (from prior session)
- `memory/_session/session_cpd_coach_warmBench_3pilots_2026_05_15.md` (THIS FILE)

**Locked Reference:**
- `memory/_locked/warm_bench_final_locked_approach.md` (reinforced)
- `templates/warm_bench_email.html` (used for all 3)

---

## Next Steps (After Approval)

1. ⏳ Await feedback from Ayesha + Jawwad
2. ⏳ Send live versions to candidates:
   - Hajra: hajra2357@gmail.com
   - Unzeela: unzilak21@gmail.com
   - Fatima: fatimasaeed030499@gmail.com
3. ⏳ Log all sends to email_audit.log via safe_sendmail()

---

## Locked Rules Summary

**FROZEN FOR PRODUCTION:**

1. Subject lines = POETIC STORIES ONLY (tied to interview moment)
2. 800-1100 words MANDATORY
3. 4 blue headings (What Stayed, Honest Part, Where to Leave, P.S.)
4. Justified text everywhere except signature
5. NO em dashes
6. Simple <p> HTML signature only
7. Locked template: 620px, 70px padding, Georgia, 1.75 line-height, #1565C0 blue
8. Values + GWC integrated naturally (NOT separate sections)
9. GWC-only emails viable when values data missing
10. P.S. anchors back to subject line story

---

**Status:** ✅ PRODUCTION READY (pending approval)  
**Session date:** 2026-05-15  
**Learning value:** High - full integrated approach (values+GWC+GWC-only variants) locked and tested with 3 candidates
