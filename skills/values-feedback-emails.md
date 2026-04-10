---
name: Values Feedback Emails SOP
description: Rejection feedback emails for candidates who fail values interview. 800-1100 words mandatory. v8 design. Pilot to Ayesha + Jawad only.
type: feedback
---

## Objective

Write rejection feedback emails for candidates who fail the values round. These emails are **personalized, emotionally careful, and evidence-based** — not generic rejections. They show what we observed in their interview and what they should work on.

---

## Word Count Requirement (NON-NEGOTIABLE)

- **Minimum: 800 words** (mandatory, cannot be lower)
- **Target: 800–1100 words** (optimal range)
- Count words before sending. If <800, expand until you reach 800.

---

## SOP (Existing Process)

All existing SOPs and steps from **memory/feedback_email_rules.md** apply. Including:

- **Type 2: Values Failed Feedback** (800–1100 words)
  - Tone: considerate, open-handed, emotionally careful
  - No em dashes anywhere (replace with period, comma, or colon)
  - "We" voice throughout (never "I")
  - They/them pronouns always (gender-neutral)
  - Three required sections:
    1. What We Liked Most About You
    2. Where We Found Ourselves Sitting With Questions
    3. What We Think You Should Do Next
  - Specific evidence from their values interview (not generic)
  - P.S. box with encouragement
  - v8 HTML design: blue #1565c0 headings, green #1b5e20 subheadings, Georgia serif, justified text

- **Structure:**
  - Header block (dark navy, "People & Culture", role, "Values Interview")
  - Greeting: "Dear [Candidate Name],"
  - Opening paragraph: warm rejection + context
  - Section 1: What We Liked (2–3 specific strengths from interview)
  - Section 2: Where We Found Questions (2–3 values where they were weak, with evidence)
  - Section 3: What To Do Next (actionable advice)
  - P.S. box: encouraging sign-off
  - Footer: "Warm regards, / People and Culture Team / Taleemabad / hiring@taleemabad.com | www.taleemabad.com / Sent on behalf of Talent Acquisition Team by Coco"

- **Reference:** memory/feedback_email_rules.md (full detailed rules)

---

## Pilot Rule for This Skill

**When Ayesha says "pilot this":**

Send **only to:**
- ayesha.khan@taleemabad.com
- jawwad.ali@taleemabad.com

**NEVER include in pilot:**
- The candidate's email (junaidjadee912@gmail.com, etc.)
- Hiring manager
- hiring@taleemabad.com
- Any other recipients

**Pilot subject line:** "[PILOT — Candidate Name] [Your Original Subject]"

Example: "[PILOT — Muhammad Junaid] Your commitment, your experience, and what we need to see next"

**After pilot approval:**
1. Ayesha reviews and approves
2. Switch PILOT_MODE = False in script
3. Send live to: candidate (TO) + hiring@taleemabad.com + ayesha.khan@taleemabad.com (CC)
4. Never send without explicit approval after pilot

---

## Non-Negotiable Rules

1. **800-word minimum is mandatory** — Count words. No exceptions. If below 800, expand.

2. **Word count 800–1100 optimal** — Stay within this range. Don't go over 1100 unless absolutely necessary.

3. **Specific evidence from interview** — Every observation must cite something the candidate said or did in their values interview. Not assumptions. Not generic patterns.

4. **No em dashes** — Replace " — " with period, comma, or colon. Dashes look AI-generated.

5. **"We" voice throughout** — Never "I". Always "we" (People & Culture team perspective).

6. **They/them pronouns** — Gender-neutral always. Never "he/she/his/her".

7. **Three required sections** — What We Liked / Where We Found Questions / What To Do Next. Don't skip or merge.

8. **v8 HTML design** — Blue headings, green subheadings, Georgia serif, justified text. Match existing format.

9. **Pilot rule strict** — Pilots go ONLY to Ayesha + Jawad. Never candidate. Never other recipients.

10. **Feedback widget required** — Include at end of body: `feedback_widget(candidate_name, role, app_id, "Application Feedback")`

11. **Approval before live send** — Always pilot first, get approval, then go live. No exceptions.

---

## Pre-Send Checklist

- [ ] Email written and word count ≥800 (verified)
- [ ] Email word count ≤1100 (or justified if longer)
- [ ] Read values interview notes for specific evidence
- [ ] Section 1: What We Liked (2–3 specific strengths, cited)
- [ ] Section 2: Where We Found Questions (2–3 values gaps, evidence-based)
- [ ] Section 3: What To Do Next (actionable advice, not generic)
- [ ] P.S. box included (encouraging, specific to candidate)
- [ ] No em dashes anywhere (searched and replaced)
- [ ] "We" voice throughout (no "I")
- [ ] They/them pronouns used (no gendered pronouns)
- [ ] v8 HTML design applied (blue headings, Georgia serif, justified)
- [ ] Feedback widget code added
- [ ] Subject line simple, descriptive, story-driven
- [ ] PILOT_MODE = True (will send to Ayesha + Jawad only)
- [ ] Recipients verified: TO = candidate, CC = hiring@taleemabad.com + ayesha.khan@taleemabad.com (for live send)
- [ ] Ready to send pilot and ask for approval

---

## Common Mistakes

1. **Below 800 words** — Sent email with only 650 words. Rejected. Expand to at least 800.

2. **No specific interview evidence** — "You showed good communication" without citing what they said. Too generic. Find actual quote or moment from interview.

3. **Em dashes in body** — "You didn't show — and we noticed" looks AI-generated. Replace with period or comma.

4. **"I" voice** — "I appreciated your openness" should be "We appreciated your openness".

5. **Gendered pronouns** — "He showed good thinking" should be "They showed good thinking".

6. **Missing section** — Only 2 sections instead of 3. All 3 required (What We Liked / Questions / What To Do Next).

7. **Including candidate in pilot** — PILOT_MODE=True but email went to candidate's email address. Critical error.

8. **Sending without pilot** — Went straight to live without Ayesha review. Never do this.

9. **No feedback widget** — Forgot to append feedback_widget code. Add before wrapping HTML.

10. **Wrong format** — Sent as plain text instead of v8 HTML. Use H()/SUB()/P()/PS() helpers.

---

## Reference

**Full feedback email rules:** memory/feedback_email_rules.md
- Complete tone guidance
- All 3 email types (CV-stage rejection, values failed, warm bench)
- HTML design (v8 final)
- Pre-send checklist
- Examples

**Existing implementation:** scripts/jobs/job36/send_job36_values_feedback_junaid_jawad_formatted.py
- v8 design structure
- H()/SUB()/P()/PS() HTML helpers
- Feedback widget integration
- Safe_sendmail bouncer
- PILOT_MODE pattern

**Email design reference:** send_job32_values_invite.py (different skill, but shows v8 format)

---

## Commitment (Coco, 2026-04-10)

I will write values feedback emails with:
- Minimum 800 words (verified count)
- Specific interview evidence in every section
- "We" voice, they/them pronouns, no em dashes
- v8 HTML design
- Feedback widget included
- Pilot to Ayesha + Jawad ONLY, never candidate in pilot
- Approval before live send
- Safe_sendmail bouncer used
- All recipients verified before sending
