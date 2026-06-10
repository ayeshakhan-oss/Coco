---
name: values-feedback-emails
description: Rejection feedback emails for candidates who fail values interview. 800-1100 words mandatory. v8 HTML design. Pilot to Ayesha + Jawad only. Evidence-based feedback with 3 required sections.
compatibility: Requires memory/feedback_email_rules.md, RULES.md Skill 2, locked email template
---

# Values Feedback Emails

Send personalized rejection emails to candidates who fail the values interview with evidence-based feedback and growth-oriented guidance.

---

## 📖 READ FIRST: Master Tone Philosophy

**All candidate communication must follow the principles in:**
[CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md](../../../memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md)

**🔒 LOCKED LAYOUT (2026-06-10):** Import the visual layout from `scripts/utils/v8_template.py` (`H/SUB/P/PS/FOOTER/wrap/attach_logo/EYEBROW`). NEVER redefine the card/header/footer/helpers inline. Same layout for ALL candidate comms. Full spec: [v8_candidate_comms_layout_LOCKED.md](../../../memory/v8_candidate_comms_layout_LOCKED.md). Reference impl: `scripts/send_cpd_coach_values_feedback_syeda_2026_06_10_pilot.py`.

This skill describes HOW to structure the email. The master file describes THE TONE PHILOSOPHY and rules that govern WHAT you write.

**Key rules that the harness enforces (HARD BLOCKS):**
- **Rule 1:** No psychologizing ("you seemed", "you lacked", "you would likely struggle", etc.)
- **Rule 2:** Evidence-based only (every statement traceable to interview/assessment/CV/scorecard observation)
- **Rule 3:** Scorecard translation (interpret, don't transfer frustration/harsh wording)
- **Rule 4:** Role-fit explanation (not personal shortcomings)
- **Rule 7:** Specificity (email could only be written about this candidate)

**Warnings (allowed to send, Ayesha notified):**
- Generic subject lines
- Recruiting jargon ("strong candidate", "excellent fit", etc.)

Before drafting, read the master file. The harness validates these at send time.

---

## When to Use This Skill

Trigger this skill when:
- Candidate completed values interview
- Candidate did not pass values round (failed assessment)
- User needs to send feedback email with specific interview evidence
- Email must be 800-1100 words with 3 required sections
- Pilot approval required before sending to candidate

---

## Related SOP (Source of Truth)

**Location:** `SOPs/01_Candidate_Communication/values_feedback_emails.md`

This skill orchestrates the detailed procedure for writing and sending values feedback emails. The SOP contains:
- Complete word count requirements (800-1100 mandatory)
- 3-section structure (What We Liked / Questions / What To Do Next)
- Tone and voice rules (we/them, no em dashes)
- v8 HTML design specification
- Pilot rule (Ayesha + Jawad only, never candidate in pilot)
- Feedback widget integration
- Pre-send checklist (14 items)

---

## Universal Rules (All Values Feedback)

**Word Count:**
- Minimum: 800 words (mandatory, non-negotiable)
- Target: 800-1100 words (optimal range)
- Count before sending; expand if below 800

**Structure (3 Required Sections):**
1. What We Liked Most About You (2-3 specific strengths from interview)
2. Where We Found Ourselves Sitting With Questions (2-3 values gaps, with evidence)
3. What We Think You Should Do Next (actionable advice)

**Tone & Voice:**
- "We" voice (never "I")
- They/them pronouns (gender-neutral always)
- Emotionally careful, warm, considerate
- Specific evidence from interview (never generic)
- No em dashes (replace with period, comma, colon)

**Format:**
- v8 HTML design: blue #1565c0 headings, green #1b5e20 subheadings, Georgia serif, justified
- Feedback widget required (mandatory)
- P.S. box with encouragement
- No asterisks in section headings

**Pilot Rule (STRICT):**
- Send ONLY to: ayesha.khan@taleemabad.com + jawwad.ali@taleemabad.com
- NEVER include candidate email in pilot
- Subject line: "[PILOT — Candidate Name] [Original Subject]"
- Wait for explicit approval before going live

---

## Detailed Procedure

**Word Count & Structure:**
- Minimum 800 words (mandatory), target 800-1100
- 3 required sections: What We Liked / Questions / Next Steps
- P.S. box included (encouraging)

**Pre-Drafting:**
- Read full values interview notes (document specific moments/quotes)
- Identify 2-3 genuine strengths and 2-3 honest gaps
- Quote actual interview moments (never assume)

**Drafting (Single-Pass):**
1. Opening: Thank candidate by name, warm rejection + context
2. Section 1 "What We Liked Most About You" (2-3 strengths with specific interview evidence, 100-150 words)
3. Section 2 "Where We Found Ourselves Sitting With Questions" (2-3 gaps with interview evidence, 100-150 words)
4. Section 3 "What We Think You Should Do Next" (actionable advice, not prescriptive, 100-150 words)
5. P.S. box: encouraging sign-off (specific to candidate)
6. No em dashes (replace all " — " with period, comma, or colon)
7. "We" voice throughout (never "I"), they/them pronouns (never gendered)

**HTML Design (v8):**
- Blue #1565c0 headings, green #1b5e20 subheadings
- Georgia serif, justified text
- Use H()/SUB()/P()/PS() helpers
- No asterisks in section headings

**Feedback Widget:**
- Add at end of body: `feedback_widget(candidate_name, role, app_id, "Application Feedback")`

**Pilot & Approval:**
- Set PILOT_MODE = True
- Send to ayesha.khan@taleemabad.com + jawwad.ali@taleemabad.com ONLY
- Wait for explicit approval
- User says "go live" → set PILOT_MODE = False
- Send to candidate (TO) + hiring@taleemabad.com + ayesha.khan@taleemabad.com (CC)

---

## Execution Discipline

**STEP 1: IDENTIFY THIS SKILL**
- User says "send values feedback" or "values interview rejection"
- Candidate failed values assessment (not passed)

**STEP 2: READ LOCKED RESOURCES**
- RULES.md: Skill 2 (Rejection Emails, lines 170-201)
- memory/feedback_email_rules.md: Complete tone guidance
- memory/email_template_format_FINAL.md: v8 design locked

**STEP 3: READ SOURCE MATERIAL**
- Full values interview notes (document specific moments/quotes)
- Identify 2-3 genuine strengths and 2-3 honest gaps
- Only use observations from actual interview (never assume)

**STEP 4: WRITE ONCE, CORRECTLY**
- Single-pass correctness (no iteration)
- Evidence in every section (quote actual interview moments)
- "We" voice, they/them pronouns throughout
- 3 sections required (don't merge or skip)

**STEP 5: VERIFY STRUCTURE**
- Opening thanks candidate by name, warm rejection
- Section 1: What We Liked (2-3 strengths with specific interview evidence)
- Section 2: Where We Found Questions (2-3 gaps with interview evidence)
- Section 3: What To Do Next (actionable advice)
- P.S. box included (encouraging, specific)
- Closing: warm sign-off

**STEP 6: APPLY v8 FORMAT**
- Blue headings (#1565c0)
- Green subheadings (#1b5e20)
- Georgia serif, justified text
- No em dashes (search and replace " — " with period/comma)
- No asterisks in section headings

**STEP 7: RUN SELF-QA CHECKLIST**
- All 14 items must pass before sending pilot

**STEP 8: PILOT & APPROVE**
- Send pilot to Ayesha + Jawad ONLY
- Wait for explicit approval
- User says "go live"
- Send to candidate (TO) + hiring@taleemabad.com (CC)

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Word count <800 | Lacks depth, feels rushed | Expand with specific interview moments |
| No interview evidence | Generic, sounds AI-generated | Quote actual interview moments/quotes |
| "I" voice | Breaks consistency | Use "we" (People & Culture team) |
| Em dashes in body | Looks AI-generated | Replace with period, comma, or colon |
| Missing sections | Incomplete feedback structure | All 3 required (Liked/Questions/Next) |
| Sending to candidate in pilot | Violates approval process | Pilot ONLY to Ayesha+Jawad |
| Wrong HTML format | Misaligned with v8 design | Use H()/SUB()/P()/PS() helpers |
| No feedback widget | Missing engagement mechanism | Add widget code before final send |
| Vague gap identification | "You need to work on communication" | Cite specific interview moment as evidence |
| Skipping P.S. box | Missing encouragement element | Include warm P.S. specific to candidate |

---

## Success Criteria

✅ Email is 800-1100 words (verified count)  
✅ 3 required sections present (Liked / Questions / Next)  
✅ Every observation cites interview moment  
✅ "We" voice, they/them pronouns throughout  
✅ No em dashes (all replaced)  
✅ v8 HTML design applied (blue headings, Georgia serif, justified)  
✅ Feedback widget included  
✅ P.S. box included and encouraging  
✅ Pilot sent to Ayesha + Jawad (never direct to candidate)  
✅ All 14-item checklist items pass  

---

## Self-QA Checklist (Before Pilot)

- [ ] Email written and word count ≥800 (verified)
- [ ] Word count ≤1100 (or justified if longer)
- [ ] Section 1: What We Liked (2-3 strengths with specific interview evidence)
- [ ] Section 2: Where We Found Questions (2-3 gaps with interview evidence)
- [ ] Section 3: What To Do Next (actionable advice)
- [ ] P.S. box included (encouraging, specific to candidate)
- [ ] No em dashes (searched and replaced all " — ")
- [ ] "We" voice throughout (no "I")
- [ ] They/them pronouns (no gendered pronouns)
- [ ] v8 HTML format (blue headings, green subheadings, Georgia serif, justified)
- [ ] Feedback widget code added
- [ ] Subject line simple and descriptive
- [ ] PILOT_MODE = True (will send to Ayesha + Jawad only)
- [ ] Ready for pilot and approval request

---

## Resources & Templates

**Locked Templates:**
- Email Design: `memory/email_template_format_FINAL.md`
- Feedback Rules: `memory/feedback_email_rules.md`

**Reference Scripts:**
- Values feedback example: `scripts/jobs/job36/send_job36_values_feedback_junaid_jawad_formatted.py`

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)
- Skill 2 (Rejection Emails): `RULES.md` (lines 170-201)

---

## Commit to Discipline

I will send values feedback emails with:
- ✅ 800-1100 words (verified count)
- ✅ 3 required sections (Liked / Questions / Next)
- ✅ Specific interview evidence (never generic)
- ✅ "We" voice, they/them pronouns
- ✅ v8 HTML design (locked format)
- ✅ Feedback widget included
- ✅ Pilot to Ayesha + Jawad (never direct)
- ✅ All 14-item checklist passing

**Status:** ✅ PRODUCTION READY
