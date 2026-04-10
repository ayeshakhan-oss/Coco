---
name: Values Scorecard Scoring SOP
description: Evaluate candidates on 6 core values using +/+/-/- ratings. PASS/OUT logic. GWC assessment. Markaz-compatible JSON schema required.
type: feedback
---

## Objective

Evaluate a candidate's alignment with Taleemabad's 6 core values during the values interview, using a structured rating system that produces a clear PASS/OUT verdict and GWC assessment for candidates who pass.

**System:** People Analyzer (Markaz integration)

---

## The 6 Values to Assess

1. **Don't Walk Away** — commitment to mission and communities; persistence through difficulty
2. **All for One** — team collaboration; lifting teammates; showing up for the collective
3. **Continuously Improve** — growth mindset; seeking feedback; helping team develop better ways of working
4. **Courageous Conversations** — ability to have hard conversations; honesty; pushing back on group dynamics
5. **Don't Hold On Too Tight** — flexibility; adaptability; letting go of being right; learning from mistakes
6. **Practice Joy** — bringing energy and warmth; finding lightness in hard work; sustaining teams emotionally

---

## The Rating System (3 Options Per Value)

For each value, assign ONE of these ratings:

- **+** (Plus) = Candidate exhibits this value clearly. Evidence is specific, compelling, and directly observed in the interview.

- **+/-** (Plus-Minus) = Candidate is inconsistent on this value. Some moments show it, some moments don't. Or the evidence is present but weak/unclear.

- **-** (Minus) = Candidate does NOT exhibit this value. Evidence is absent or contradicts the value. Or candidate actively demonstrated the opposite.

---

## The Pass/Out Logic (NON-NEGOTIABLE)

**PASS:** Zero minuses AND ≤2 plus-minuses

Acceptable combinations:
- 6 pluses = automatic PASS
- 5 pluses + 1 plus-minus = PASS
- 4 pluses + 2 plus-minuses = PASS
- Any configuration with zero minuses and ≤2 plus-minuses = PASS

**OUT:** Any minus OR ≥3 plus-minuses

Automatic OUT conditions:
- Even one minus = OUT (regardless of other ratings)
- Three or more plus-minuses = OUT (even with no minuses)

---

## GWC Assessment (Gets it / Wants it / Capacity)

**When:** Only evaluated for candidates who PASS the values round.

**Three questions to answer (all must be YES):**

1. **Gets it** — Does the candidate demonstrate understanding of Taleemabad's mission and values? Do they "get" what we're doing?

2. **Wants it** — Does the candidate genuinely want to work here? Is this a real fit, or are they just looking for a job?

3. **Capacity** — Does the candidate have the actual capacity (bandwidth, skill, maturity) to show up on these values day-to-day in the role?

**If all 3 = YES:** Candidate is READY for Right Seat interview.

**If any = NO:** Candidate is CONDITIONAL — flag for specific GWC probe or reassessment before Right Seat.

---

## The Scorecard Structure (4 Evidence Columns)

For each value, populate ALL FOUR columns:

1. **Deep-Dive Evidence** — a substantial moment from the interview where the value was tested or demonstrated. Usually from a structured question. Cite specific quote or behavior.

2. **Curve-Ball Evidence** — a moment where the interviewer asked an unexpected or challenging question. How did the candidate respond? What did this reveal about their value alignment?

3. **Micro-Case Evidence** — a small moment, gesture, or comment that revealed the value. Can be a brief exchange, not necessarily a long story.

4. **Rating** — assign +, +/-, or - based on the weight of all three evidence types.

**Key rule:** Never leave evidence blank. Every value must have observations in all three columns, even if one column has less substantial evidence. If not observed, state "Not directly evident in interview."

---

## Step-by-Step Scoring Process

1. **Before the interview:** Read the JD and candidate CV. Know the role deeply.

2. **During the interview:** Take live notes on each of the 6 values. Don't wait until the end — capture moments as they happen. Mark which type of evidence each observation falls into (Deep-Dive, Curve-Ball, Micro-Case).

3. **After the interview (same day, while fresh):** Open the Markaz scorecard template.

4. **For each of the 6 values:**
   - Review your interview notes
   - Extract the most compelling Deep-Dive moment (1–2 sentences)
   - Extract a Curve-Ball moment if one occurred (1 sentence)
   - Note any Micro-Case moments (1 sentence)
   - Assign a rating: + or +/- or -

5. **After scoring all 6 values:** Count your ratings.
   - Zero minuses AND ≤2 plus-minuses? → PASS
   - Any minus OR ≥3 plus-minuses? → OUT

6. **If PASS:** Assess GWC.
   - Gets it? YES/NO
   - Wants it? YES/NO
   - Capacity? YES/NO
   - Document 1–2 reasons per answer

7. **Final Verdict:** Input into Markaz:
   - Status: "Passed Values" (if PASS) OR "Did Not Pass Values" (if OUT)
   - GWC field: YES or CONDITIONAL (with specific probe/reason)
   - Submit scorecard with exact Markaz-compatible JSON schema

---

## The Markaz JSON Schema (NON-NEGOTIABLE)

**CRITICAL:** Wrong schema = data in DB but invisible on Markaz UI.

**Exact format required:**
```json
{
  "date": "2026-04-10",
  "host": "Ayesha Khan",
  "candidateName": "Muhammad Junaid",
  "noteTaker": "Coco",
  "values": [
    {
      "name": "Don't Walk Away",
      "deepDive": "...",
      "curveBall": "...",
      "microCase": "...",
      "rating": "+"
    },
    ...
  ],
  "finalComments": "PASS / CONDITIONAL / OUT",
  "proceedToRightSeat": true or false
}
```

**Use this format verbatim.** Do not modify field names or structure.

---

## Non-Negotiable Rules

1. **Every value must have 3 evidence columns filled** — no blank columns. If you didn't observe something, state "Not directly evident in interview" rather than leaving it blank.

2. **Evidence must be specific to the interview** — not assumptions about the candidate's background. Cite actual moments.

3. **Ratings are binary per evidence type, holistic per value** — Deep-Dive alone doesn't make a +. All three columns inform the final rating.

4. **Minus = OUT, always** — no exceptions. One minus overrides 5 pluses.

5. **GWC only after PASS** — don't assess GWC if the candidate OUT. GWC is not a back-door to override an OUT verdict.

6. **GWC must be YES on all 3 questions** — not 2 out of 3. All three must be YES to proceed to Right Seat.

7. **Document reasons for CONDITIONAL GWC** — if any GWC answer is NO, state the specific probe or reassessment needed (e.g., "Conditional on alignment check: does candidate understand salary expectations?" or "Needs direct conversation about remote vs. in-person commitment").

8. **Markaz schema must be exact** — use People Analyzer's format exactly. Wrong schema = data in DB but invisible on Markaz UI.

9. **Never assess GWC if OUT** — OUT is final. GWC only for PASS candidates moving to Right Seat.

10. **Count before submitting** — verify: zero minuses + ≤2 plus-minuses = PASS? If not, double-check ratings before submitting.

---

## Common Mistakes

1. **Rating too high on incomplete evidence** — "I didn't see this value tested, but I assume they have it." Rating: -. You can only rate + based on observed evidence.

2. **Confusing + with +/-** — a candidate shows a value once but inconsistently. That's +/-, not +. Reserve + for consistent, clear evidence.

3. **Letting one strong value override a weak one** — "They're amazing at Continuously Improve, so I'll give them a + on Courageous Conversations too." Each value stands alone. Rate each independently.

4. **Ignoring a minus with "but they passed other values"** — One minus = OUT. Period. This is non-negotiable.

5. **Assessing GWC before finalizing the PASS/OUT verdict** — finalize ratings first, then check logic. Only assess GWC if PASS is confirmed.

6. **Leaving GWC blank** — if PASS, you must assess all 3 questions. Blank GWC = incomplete scorecard.

7. **Rating based on CV background, not interview evidence** — "They have 10 years of experience, so +" is wrong. Rate based on what you observed in the interview, not the resume.

8. **Plus-minus inflation** — +/- should be ~20–30% of your ratings. If you're rating 4+ plus-minuses per candidate, your threshold is too low.

9. **Evidence that's too vague** — "They showed good teamwork" is not evidence. "When asked about a time they supported a teammate, they described absorbing a colleague's work during a crisis" is evidence.

10. **Submitting before double-checking the pass/out logic** — before hitting submit, verify: count minuses (should be 0) + count plus-minuses (should be ≤2) = PASS. If any minus or ≥3 plus-minuses = OUT. Don't submit without this verification.

---

## Pre-Submission Checklist

- [ ] All 6 values scored (ratings assigned)
- [ ] All 4 evidence columns filled per value (no blanks)
- [ ] Evidence is specific to interview (not assumptions)
- [ ] Minuses counted (should be 0 for PASS)
- [ ] Plus-minuses counted (should be ≤2 for PASS)
- [ ] Pass/Out logic verified (zero minuses AND ≤2 +/- = PASS)
- [ ] If PASS: GWC assessed (all 3 questions answered: Gets it? Wants it? Capacity?)
- [ ] If CONDITIONAL GWC: specific probe documented
- [ ] Markaz JSON schema exact (no field name deviations)
- [ ] "proceedToRightSeat": true (if PASS) or false (if OUT)
- [ ] finalComments field complete: "PASS" / "CONDITIONAL" / "OUT"
- [ ] Ready to submit to Markaz

---

## Reference

**Full rules + examples:** memory/values_scoring.md
**Markaz schema spec:** memory/feedback_values_scorecard_schema.md
**Interview format:** Values interview conducted by Ayesha Khan or Jawwad Ali
**Next step after PASS:** GWC interview (Right Seat call)

---

## Commitment (Coco, 2026-04-10)

I will score every candidate on all 6 values with specific evidence. I will apply pass/out logic correctly (zero minuses AND ≤2 +/- = PASS, any minus OR ≥3 +/- = OUT). I will assess GWC only for PASS candidates. I will use exact Markaz JSON schema. I will verify before submitting.
