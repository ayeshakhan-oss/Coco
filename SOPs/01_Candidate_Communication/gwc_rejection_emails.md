---
name: GWC Rejection Emails
description: Warm-tone rejection emails for GWC interview candidates. Based on GWC scorecard data only. 400-450 words acceptable if data is limited. No jargon. No em dashes.
type: feedback
---

# Skill: GWC Rejection Emails
**Skill Number:** Skill 13 (Candidate Communication — GWC Cohort)  
**Locked in:** 2026-04-14  
**SOP Status:** Complete

---

## PURPOSE

Generate warm-tone rejection emails for candidates who participated in GWC (Get It / Want It / Capacity) interviews but were not selected. These emails are based on GWC scorecard data (not interview transcripts) and should be supportive, specific, and honest.

---

## WHEN TO USE THIS SKILL

- Candidate completed values interview (passed)
- Participated in GWC conversation/interview
- Did NOT get selected for the role
- No detailed interview transcript available
- Only GWC scorecard data available for feedback

**Candidates for this skill:** Those with GWC scores (Get It, Want It, Capacity ratings) in Markaz applications.gwc_scorecard field.

---

## SOURCE DATA REQUIREMENTS

### Required Fields (From Markaz DB):
```json
{
  "name": "Candidate Name",
  "getIt": { "score": 6, "evidence": "..." },
  "wantIt": { "score": 8, "evidence": "..." },
  "capacityToDoIt": { "score": 6, "evidence": "..." },
  "additionalComments": "Interviewer's assessment",
  "hiringManager": "Manager name",
  "finalMark": "Yes/No recommendation"
}
```

### What to Extract:
- Candidate name
- GWC scores (0-10 scale for each)
- Interviewer's additional comments
- Hiring manager feedback summary
- Whether they were recommended

### What NOT to Do:
- **NEVER fabricate details** beyond scorecard
- **NEVER invent observations** not in scorecard
- **NEVER add context** beyond GWC data provided
- If data is sparse, stay sparse (400-450 words is acceptable)

---

## EMAIL STRUCTURE (REQUIRED)

### Section 1: Opening (2-3 paragraphs)
- Thank candidate for time
- Acknowledge their engagement
- State decision clearly: "We've decided not to move forward"
- Affirm they deserve directness

**Word count:** 80-120 words  
**Tone:** Warm, respectful, direct

### Section 2: What We Saw (2-3 paragraphs)
- Reference GWC scorecard strengths ONLY
- Cite specific comments from scorecard
- Highlight capability areas shown
- Keep language warm and encouraging
- Use "we" voice (never "I")

**Evidence sources:** 
- GWC scores (Get It, Want It, Capacity)
- Interviewer's additionalComments field
- Hiring manager feedback

**Example:** "Your GWC conversation showed us that you genuinely understand [topic]. We saw evidence of [specific strength from scorecard]."

**Word count:** 150-200 words

### Section 3: The Gap (1-2 paragraphs)
- Identify the gap honestly but warmly
- Reference scorecard evidence
- Frame as "here's where we're at"
- Avoid harsh language
- Acknowledge it's feedback for growth

**Word count:** 100-150 words

### Section 4: What Matters Next (2-3 paragraphs)
- Provide actionable guidance
- Frame based on scorecard scores
- Encourage specific next steps
- Keep warm, mentoring tone
- Focus on growth mindset

**Word count:** 150-200 words

### Section 5: Closing (1-2 paragraphs)
- Affirm their potential
- Warm sign-off
- Keep brief and genuine

**Word count:** 50-100 words

**Total:** 530-770 words (400-450 minimum acceptable if scorecard data limited)

---

## TONE RULES (NON-NEGOTIABLE)

1. **Warm, not harsh** — Never use absolute language ("you failed", "you don't understand")
2. **Mentoring, not dismissive** — Frame as guidance, not judgment
3. **Evidence-based** — Every observation tied to scorecard data
4. **"We" voice** — Never "I", always "we" (team decision)
5. **Honest but encouraging** — Can be direct about gaps; maintain hope
6. **No jargon** — NO "GWC" terminology; NO "Zero In Call"; NO interviewer/peer names
7. **No internal language** — Write as if candidate doesn't know internal frameworks

---

## FORMAT (TALEEMABAD EMAIL TEMPLATE — LOCKED)

**This is NON-NEGOTIABLE. Every GWC rejection email MUST use this format:**

1. **Logo** (Taleemabad) at top
2. **Small blue header** (centered): "PEOPLE & CULTURE • REJECTION DECISION"
3. **Large blue title** (centered, 18pt, bold): "We're reflecting on your [Position] application"
4. **Blue subtitle** (centered, 12pt): [Position name / Hackathon 2026]
5. **Blue horizontal line separator** (2px, #1565c0)
6. **Body text** (justified, Georgia serif, 11pt, leading 16)
7. **Section headings** (blue bold, NO asterisks showing)
8. **No em dashes** (use regular hyphens -)
9. **"We" voice throughout**
10. **NO "Zero In Call" / "GWC" / interviewer/peer names**

**Reference:** email_template_format_FINAL.md

---

## STEP-BY-STEP PROCESS

### Step 1: Check Memory (MANDATORY)
- Read MEMORY.md
- Check if similar work has been done
- Find reference emails in prior projects
- Study their tone and structure

### Step 2: Query Markaz for GWC Data
Extract from scorecard:
- Get It score + evidence
- Want It score + evidence
- Capacity to Do It score + evidence
- Additional comments (hiring manager feedback)
- Final mark (recommended Y/N)

### Step 3: Extract & Verify Data
**Verify:** All fields have data before proceeding. If missing, note "Not mentioned" (never fabricate).

### Step 4: Find Reference Email
- Look for prior GWC rejection email from same position
- OR values feedback email (similar structure)
- Study tone, section structure, evidence use
- Use as template baseline

### Step 5: Draft Opening
- Thank for time and engagement
- State decision clearly
- Keep warm, direct

### Step 6: Draft What We Saw
- Extract 1-2 key strengths from GWC scores
- Quote from additionalComments field directly
- Use warm, encouraging language
- Stay ONLY within scorecard data

### Step 7: Draft The Gap
- Identify 1-2 areas where scores were lower
- Frame as "where we're at" not "where you failed"
- Use scorecard evidence
- Keep honest but warm

### Step 8: Draft What Matters Next
- Give 1-2 actionable next steps
- Base on gap identified
- Tie to scorecard scores if relevant
- Encourage growth mindset

### Step 9: Draft Closing
- Affirm potential
- Warm sign-off
- Keep brief

### Step 10: Internal QA Checklist (BEFORE SENDING)
- [ ] Memory review completed
- [ ] Data extraction verified (all fields filled)
- [ ] Format matches email_template_format_FINAL.md exactly
- [ ] Tone verified (warm, mentoring, no harshness)
- [ ] No jargon (NO "GWC", "Zero In Call", names)
- [ ] No em dashes (all hyphens)
- [ ] No duplicate greetings
- [ ] Word count meets minimum (400+)
- [ ] Evidence-based (every claim tied to scorecard)
- [ ] Only scorecard data used (no fabrication)
- [ ] Compared to reference email (structure matches)
- [ ] Section headings properly formatted (blue bold, no asterisks)
- [ ] "We" voice throughout
- [ ] Closing is warm and genuine

### Step 11: Compare to Reference
Side-by-side comparison with reference email from same position:
- Opening style matches?
- Section structure matches?
- Tone consistency?
- Evidence citation style matches?
- Closing warmth matches?

### Step 12: Submit
Only submit after ALL checklist items pass. Not before.

---

## CRITICAL RULES (NON-NEGOTIABLE)

1. **No fabrication** — Use ONLY scorecard data. Period.
2. **Memory check first** — Mandatory before drafting.
3. **Format exactly** — Taleemabad template, no variations.
4. **Warm tone always** — Never harsh, never dismissive.
5. **Evidence-based** — Everything tied to scorecard.
6. **Internal QA owned** — Don't send until QA checklist complete.
7. **No jargon** — Candidate doesn't know "GWC", "Zero In Call", etc.
8. **Reference comparison** — Always compare to prior similar work.
9. **Single-pass correctness** — Get it right first time, not draft-iterate.
10. **Ask when uncertain** — Don't guess on data or format.

---

## QUICK CHECKLIST (Copy for Each Email)

```
GWC Rejection Email Checklist

Candidate: ________________
Position: ________________
Email: ________________

BEFORE DRAFTING:
- [ ] Memory.md checked
- [ ] Reference email found & reviewed
- [ ] GWC scorecard data extracted (all fields)
- [ ] Data verified complete

AFTER DRAFTING:
- [ ] Format matches template exactly
- [ ] Tone: warm, mentoring, no harshness
- [ ] No jargon (no GWC, Zero In Call, names)
- [ ] No em dashes (all hyphens)
- [ ] No greeting duplication
- [ ] Word count: 400+ words
- [ ] Evidence-based (every claim tied to scorecard)
- [ ] Only scorecard data (no fabrication)
- [ ] Compared to reference email
- [ ] Headings: blue bold, no asterisks
- [ ] "We" voice throughout
- [ ] All section present: Opening → What We Saw → Gap → Next → Closing
- [ ] Closing is warm & genuine

READY TO SEND? [ ] YES (all above checked)
```

---

## TRAINING COMPLETE

This skill is locked in and ready for use. When assigned a GWC rejection email:

1. **Always consult this SOP first**
2. **Follow the 12-step process**
3. **Verify against the QA checklist**
4. **Compare to reference email**
5. **Only send when all checks pass**

No exceptions. No shortcuts. Discipline over speed.

---

**Skill locked:** 2026-04-14  
**Version:** 1.0  
**Status:** Production Ready
