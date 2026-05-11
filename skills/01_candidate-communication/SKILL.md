---
name: candidate-communication
description: Handle all candidate rejection and feedback emails. Covers CV rejections, values interview feedback, warm bench feedback, and GWC rejections. All emails require 800+ words (if feedback), evidence-based feedback, v8 HTML design, and pilot approval before sending.
compatibility: Requires memory/feedback_email_rules.md, locked templates, RULES.md
---

# Candidate Communication

Send personalized rejection and feedback emails to candidates across all interview stages.

---

## Architecture

**This skill is an orchestration layer** that references the detailed SOPs in `SOPs/01_Candidate_Communication/`. 

- **SKILL.md (this file):** Master orchestration, universal rules, execution discipline
- **SOPs folder (source of truth):** Detailed procedures for each email type

When you use this skill, you get:
1. Universal rules and checklist (from this SKILL.md)
2. Detailed procedures (from linked SOPs — the source of truth)

**Important:** SOPs are maintained as the single source of truth. If procedures change, they update in SOPs/ and are automatically reflected here.

---

## When to Use This Skill

Trigger this skill when:
- User asks to "send rejection email to [candidate]"
- User wants to "write feedback for [candidate]"
- User requests "warm bench email" or "values feedback"
- User needs "GWC rejection" or interview stage feedback
- Any candidate communication requiring evidence-based, personalized feedback

---

## Related SOPs (Source of Truth)

**Location:** `SOPs/01_Candidate_Communication/`

This skill orchestrates the following detailed procedures:

All these SOPs fall under this skill:

1. **CV Rejection Emails** — `SOPs/01_Candidate_Communication/cv_rejection_emails.md`
   - 800+ words, CV-based evidence
   - Structure: opening → impressed → gap → close
   - Format: v8 HTML template

2. **Values Feedback Emails** — `SOPs/01_Candidate_Communication/values_feedback_emails.md`
   - 800-1100 words MANDATORY
   - 3 sections: What We Liked / Questions / Next Steps
   - Interview evidence required, no em dashes

3. **Warm Bench Feedback** — `SOPs/01_Candidate_Communication/warm_bench_feedback_email.md`
   - 800-1100 words (Haroon Yasin framework)
   - 4 sections + P.S., poetic subject line
   - Specific timestamps, no prescriptive advice

4. **GWC Rejection Emails** — `SOPs/01_Candidate_Communication/gwc_rejection_emails.md`
   - Warm-tone rejections for GWC-cleared candidates
   - Interview transcript analysis
   - No "GWC" or "KCD" terminology

---

## Universal Rules (All Communication)

**Word Count:**
- Minimum: 800 words (non-negotiable)
- Target: 800-1100 words (optimal)
- Verify count before sending

**Tone & Voice:**
- "We" voice (never "I")
- They/them pronouns (gender-neutral)
- Emotionally careful, warm
- Specific evidence from interview (never generic)

**Format:**
- v8 HTML design (blue headings, Georgia serif, justified)
- No em dashes (replace with period/comma/colon)
- Feedback widget required
- Logo, header block, footer with signature

**Pilot Rule (STRICT):**
- Always pilot to Ayesha first
- For values feedback: pilot to Ayesha + Jawad ONLY
- Never include candidate in pilot
- Wait for approval before going live
- Subject line: "[PILOT – Candidate Name] [Original Subject]"

**Self-QA Before Sending:**
- [ ] Memory checked (MEMORY.md)
- [ ] Locked template read side-by-side
- [ ] Word count verified (800+ for all types)
- [ ] Every claim cited from CV or interview
- [ ] Format matches locked standard
- [ ] Pilot sent to Ayesha (never direct)
- [ ] All special characters as HTML entities
- [ ] No discrepancies vs RULES.md

---

## Execution Discipline

**STEP 1: IDENTIFY EMAIL TYPE**
- Ask if unclear: "What type of feedback email?"
- Options: CV rejection, values feedback, warm bench, GWC rejection

**STEP 2: READ LOCKED RESOURCES**
- RULES.md: Core Discipline Rules 1-7
- RULES.md: Skill-Specific Rules (Skill 2 or 3)
- MEMORY.md: Specific SOP for that email type
- Locked template: v8 design or Haroon framework

**STEP 3: READ SOURCE MATERIAL**
- Full CV (for CV rejections)
- Full values interview notes (for values feedback)
- Full GWC interview transcript (for GWC rejections)
- Find specific moments/quotes to cite

**STEP 4: WRITE ONCE, CORRECTLY**
- Single-pass correctness (no iteration)
- Evidence in every section (not generic)
- No fabrication (quote actual text)
- Maintain "we" voice, they/them pronouns

**STEP 5: RUN 8-ITEM CHECKLIST**
- All 8 items must pass
- If any fail: fix and re-check
- Don't send without all 8 passing

**STEP 6: PILOT & APPROVE**
- Send pilot to Ayesha (+ Jawad for values feedback)
- Wait for explicit approval
- Switch PILOT_MODE = False
- Send live to candidate (TO) + hiring@taleemabad.com (CC)

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Word count <800 | Lacks depth, feels generic | Expand with specific moments, reach 800 |
| Generic praise | "You showed good skills" without evidence | Quote actual CV or interview moment |
| No interview citations | Looks AI-generated | Include specific quotes, timestamps, moments |
| "I" voice | Breaks consistency | Use "we" (People & Culture team) |
| Em dashes in body | Looks AI-generated | Replace with period, comma, or colon |
| Missing sections | Incomplete feedback | Include all 3 (likes/questions/next) |
| Sending to candidate in pilot | Violates approval process | Pilot ONLY to Ayesha/Jawad |
| Wrong HTML format | Misaligned with locked design | Print template, match exactly |
| Prescriptive advice | "You should take a course..." | Frame as observation, not prescription |
| No feedback widget | Missing engagement mechanism | Add widget code before final send |

---

## Success Criteria

✅ Email is 800+ words (verified count)  
✅ Every observation cites CV or interview moment  
✅ "We" voice, they/them pronouns throughout  
✅ No em dashes (replace with period/comma/colon)  
✅ HTML matches v8 locked design  
✅ Pilot sent to Ayesha first  
✅ All 8-item checklist items pass  
✅ No generic language or assumptions  
✅ Feedback widget included  

---

## Resources & Templates

**Locked Templates:**
- v8 Email Design: `memory/_locked/locked_templates_index.md`
- Warm Bench Framework: `memory/_locked/warm_bench_final_locked_approach.md`
- Interview Invite Design: `memory/_locked/locked_email_template_interview_invites.md`

**Reference Scripts:**
- Job 36 values feedback: `scripts/jobs/job36/send_job36_values_feedback_junaid_jawad_formatted.py`
- Warm bench: `scripts/warm_bench_locked.py`

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)
- Skill 2 (Rejection Emails): `RULES.md` (lines 170-201)
- Skill 3 (Warm Bench): `RULES.md` (lines 204-251)

---

## Commit to Discipline

I will send candidate communication emails with:
- ✅ 800+ words (verified count)
- ✅ Specific interview or CV evidence (never generic)
- ✅ "We" voice, they/them pronouns
- ✅ v8 HTML design (locked format)
- ✅ Pilot to Ayesha first (never direct)
- ✅ All 8-item checklist items passing
- ✅ Feedback widget included
- ✅ No em dashes, no fabrication, no prescriptive advice

**Status:** ✅ PRODUCTION READY
