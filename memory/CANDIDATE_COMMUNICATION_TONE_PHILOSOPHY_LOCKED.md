---
name: Candidate Communication Tone Philosophy - LOCKED
description: Master file for ALL candidate feedback/rejection emails. Single source of truth. Haroon Yasin framework + 9 enhancement rules. All candidate communication skills reference this.
metadata:
  type: reference
  locked: true
  updated: 2026-06-09
---

# CANDIDATE COMMUNICATION TONE PHILOSOPHY — LOCKED (2026-06-09)

**STATUS:** ✅ MASTER FILE — Single source of truth for ALL candidate communication emails.

**APPLIES TO:**
- CV screening rejections
- GWC rejection emails
- Values feedback emails
- Warm bench feedback emails
- Any future candidate communication

**DO NOT SCATTER RULES.** All tone/philosophy guidance lives here. All skills link to this file.

---

## FOUNDATION: HAROON YASIN FRAMEWORK

**Preserved from:** Haroon Yasin training guide (Jan 29, 2026) + subsequent implementations.

**Core principle:** Personalized rejection-keep-warm emails that leave dignity intact.

**Structure (locked):**
- **Opening:** Lead with specific moment, show company vulnerability
- **Section 1:** "What Stayed With Us" (Blue #1565C0 heading) — Specific strengths from interview
- **Section 2:** "Here's the Honest Part" (Blue heading) — Specific gaps, evidence-based
- **Section 3:** "Where We Want to Leave This" (Blue heading) — Path forward, not prescriptive
- **P.S.:** Memorable moment, reinforcement
- **Word count:** 800-1100 words minimum (mandatory)

**Format (locked):**
- **LAYOUT:** Use the single locked v8 layout for ALL candidate communication emails. Import from `scripts/utils/v8_template.py` (H/SUB/P/PS/FOOTER/wrap/attach_logo/EYEBROW). Never redefine the layout inline. Full spec: [v8_candidate_comms_layout_LOCKED.md](v8_candidate_comms_layout_LOCKED.md). Applies to all 4 types + any future candidate-communication type.
- Logo: Taleemabad embedded (cid:taleemabad_logo)
- Font: Georgia serif, justified text
- Colors: Blue headings (#1565C0), green subheads (#1b5e20), simple HTML signature
- No em dashes (replace with period/comma/colon)
- No asterisks in headings
- No interviewer names in text

---

## ENHANCEMENT LAYER: 9 CORE PHILOSOPHY RULES (2026-06-09)

### PURPOSE
Candidate feedback emails exist to do three things:
1. Clearly communicate a hiring decision
2. Help the candidate understand the decision in a respectful way
3. Leave the candidate with their dignity intact

The goal is not to make the candidate feel good or bad. **The goal is to make them feel respected.**

---

### TONE REQUIREMENTS

**Must be:**
- Warm
- Human
- Respectful
- Specific
- Honest
- Thoughtful
- Professional

**Must never be:**
- Cold
- Clinical
- Condescending
- Defensive
- Harsh
- Patronizing
- Accusatory
- Overly emotional
- Excessively flattering

**Candidate should feel:**
> "They considered me carefully. They made a decision. I understand it. I may not agree with it, but I was treated fairly."

**Candidate should never feel:**
- Judged
- Diagnosed
- Psychoanalyzed
- Embarrassed
- Scolded
- Evaluated as a person

---

### RULE 1: NON-PSYCHOLOGIST RULE

**Never state or imply assumptions about:**
- Motivation
- Commitment
- Intentions
- Confidence
- Character
- Personality
- Future decisions
- Emotional state

**Unless the candidate explicitly communicated those things.**

**FORBIDDEN patterns:**
- "You seemed uncommitted"
- "You lacked confidence"
- "You were hesitant"
- "You would likely struggle"
- "You were not fully invested"
- "You assumed..."
- "You believed..."
- "You thought..."
- "You preferred..."
- "You were energized by..."

**HARNESS ENFORCEMENT:** 🔴 **HARD BLOCK** — Email blocked at send time if detected.

---

### RULE 2: EVIDENCE RULE

**Candidate-facing feedback must be grounded in:**
- Interview responses
- Assessment performance
- CV/resume evidence
- Portfolio evidence
- Scorecard observations
- Direct statements made by the candidate

**If a statement cannot be supported by evidence, do not include it.**

**HARNESS ENFORCEMENT:** 🔴 **HARD BLOCK** — Email blocked if unsupported claims detected.

---

### RULE 3: SCORECARD TRANSLATION RULE

Hiring manager scorecards are internal documents. They are not candidate-facing language.

**The role of the feedback writer is to INTERPRET the underlying signal and communicate it respectfully.**

**Extract:**
- What happened
- What was observed
- Why it mattered to the role

**Do NOT transfer:**
- Frustration
- Assumptions
- Personal judgments
- Harsh wording
- Interviewer bias

**Example:**
- ❌ **Scorecard (internal):** "Candidate was defensive about feedback, wouldn't accept critique"
- ✅ **Candidate email:** "When we explored how you'd respond to feedback from your team, we saw an opportunity for growth in collaborative problem-solving"

**HARNESS ENFORCEMENT:** 🟡 **WARNING** — Detected scorecard language logged; allowed to send with flag.

---

### RULE 4: ROLE-FIT RULE

**Whenever possible, explain decisions through role requirements rather than personal shortcomings.**

**PREFER:**
- "The role requires someone who already has extensive classroom coaching experience"
- "We needed stronger evidence of..."
- "The role required..."

**OVER:**
- "You lacked classroom coaching experience"
- "You failed to demonstrate..."
- "You were missing..."

**HARNESS ENFORCEMENT:** 🟡 **WARNING** — Personal-shortcoming language detected; allowed to send with flag.

---

### RULE 5: EMPATHY RULE

**Before finalizing, ask:**
> "If I received this email after investing time and hope into a process, would I feel respected?"

Not: "Would I feel happy?"
Not: "Would I agree?"

Would I feel respected?

If no, rewrite.

---

### RULE 6: CLARITY RULE

**Do not soften the message so much that the rejection becomes unclear.**

Candidates should not leave wondering:
> "If I was so strong, why was I rejected?"

**The reason for the decision should be understandable.**

Warmth should never come at the expense of clarity.

---

### RULE 7: SPECIFICITY RULE

**Every candidate email should contain:**
- Specific strengths
- Specific observations
- Specific evidence

**The candidate should feel:**
> "This email could only have been written about me."

If the email could be sent to ten different candidates, it is not specific enough.

---

### RULE 8: HUMANITY TEST (Pre-Send Checklist)

**Before sending, ask:**
1. Does this sound like a thoughtful human wrote it?
2. Does it preserve the candidate's dignity?
3. Does it avoid assumptions?
4. Does it avoid judgment?
5. Is the reasoning clear?
6. Is the feedback evidence-based?
7. Would I be comfortable reading this aloud to the candidate in person?

**If any answer is no, rewrite.**

---

### RULE 9: FINAL PRINCIPLE

**We do not write feedback to explain who the candidate is.**

**We write feedback to explain the decision we made.**

Those are not the same thing.

---

## STRUCTURAL RULES (2026-06-18)

### RULE 10: MANDATORY OPENING LINE

**Every candidate communication email — CV rejection, values feedback, warm bench, GWC rejection, and any future type — MUST open with this exact line, as the first line right after the salutation (`Dear [Name],`):**

> **This is not a yes for now.**

Then the type-specific opening paragraph follows.

**Why:** It states the decision plainly and humanely up front. It is honest because of the word "now": it communicates "today, this is a no," not "you can never." That is true for everyone. A CV-stage candidate can strengthen their CV and reapply. A values candidate can grow over six months to a year. The line never over-promises on its own.

**HARNESS ENFORCEMENT:** 🔴 **HARD BLOCK** — Email blocked if the line is missing, or if it appears buried after a section heading instead of right after the salutation.

---

### RULE 11: NO FUTURE-PROMISE RULE

**Candidate emails express genuine welcome, but must NEVER commit us to a future action the candidate could later hold us to.**

Internally, we do revisit and look back at warm-bench candidates. That truth stays internal. The email's job is to make the candidate feel **specifically seen and genuinely welcome** without writing down a commitment they could question later ("you said you'd keep my name / reach out, why didn't you?").

**The mechanics:**
- **Disposition, not commitment.** Describe how *we feel* ("we would welcome the conversation again", "we'd be glad to hear from you"), not what *we will do*.
- **Candidate-initiated, not company-initiated.** Put the next move in their hands ("if a closer-fit role opens, we would welcome a fresh application from you", "we hope you'll think of us") — never "we will contact you."
- **Warmth lives in the specific praise and the P.S.**, not in any future-action language.

**✅ Safe:** "we'd welcome talking again", "we'd be glad if you came back to us", "we hope you'll come back", "you're the kind of person we hope stays in our orbit", "stay connected".

**❌ Forbidden:** "we will reach out", "we'll be in touch", "we will contact you", "we will keep your name with us / on file", "expect to hear from us", "you'll hear from us", "we'll let you know when".

**The opening line "This is not a yes for now." is safe** because it is a statement about today's state, not a future-action promise.

**HARNESS ENFORCEMENT:** 🟡 **WARNING** — Future-outreach promise phrasing flagged; allowed to send so legitimate warm closings are not blocked, but should be rewritten as disposition + candidate-initiated.

---

## HARNESS VALIDATION RULES (2026-06-09)

### HARD BLOCKS (Email cannot send)

| Violation | Pattern | Reason |
|-----------|---------|--------|
| Intent-word assumption | "you seemed", "you lacked", "you were hesitant", "you would likely", "you were not fully invested", "you assumed", "you believed", "you thought", "you preferred", "you were energized by" | Rule 1: Non-Psychologist |
| Intent-word variants | "you appeared", "you seemed to lack", "you didn't seem", "you weren't", "you wouldn't" (about capability, not action) | Rule 1: Non-Psychologist |
| Unsupported claim | Statement not traceable to: interview transcript, assessment, CV, portfolio, scorecard observation, or direct candidate quote | Rule 2: Evidence-Based |
| Missing evidence citation | "We noticed you struggle with X" (no source) | Rule 2: Evidence-Based |
| Em dashes in body | " — " used instead of period/comma/colon | Format Rule: Haroon Yasin |
| Asterisks in headings | "**Heading**" in email | Format Rule: Haroon Yasin |
| Word count under 800 | CV rejections, values feedback, warm bench must be 800+ words | Structure Rule: Haroon Yasin |
| PILOT prefix in live | Subject line contains "[PILOT – ]" | Rule: Pilot-only prefix |
| Interviewer names | "Sarah said", "When Jawad asked" | Anonymity Rule: Haroon Yasin |
| Missing sections | Missing required section (e.g., "What Stayed With Us") | Structure Rule: Haroon Yasin |
| Missing opening line | "This is not a yes for now." absent, or buried after a heading | Rule 10: Mandatory Opening Line (2026-06-18) |

### WARNINGS (Email allowed to send, Ayesha notified)

| Warning | Pattern | Reason |
|---------|---------|--------|
| Scorecard language transfer | Detected: frustration, harsh wording, or internal judgment transferred | Rule 3: Scorecard Translation |
| Generic subject line | Subject could apply to multiple candidates | Rule 7: Specificity |
| Personal-shortcoming framing | "You lacked X", "You were missing X" (instead of role-fit) | Rule 4: Role-Fit |
| Soft rejection | Rejection unclear / candidate may not understand decision | Rule 6: Clarity |
| Recruitment jargon | "culture fit", "alignment", "not quite right fit", "growth opportunity" | Rule: Haroon Yasin |
| Future-outreach promise | "we will reach out", "we'll be in touch", "we will keep your name on file", "expect to hear from us" | Rule 11: No Future-Promise (2026-06-18) |

---

## IMPLEMENTATION CHECKLIST

**When drafting any candidate communication email:**

- [ ] Read this file FIRST (master reference)
- [ ] Read the specific skill file (CV rejection / GWC / values / warm bench)
- [ ] Check: Is this grounded in interview evidence? (Rule 2)
- [ ] Check: Am I assuming motivation/confidence/character? (Rule 1)
- [ ] Check: Is this a decision explanation, not a person explanation? (Rule 9)
- [ ] Check: Could this only be written about this candidate? (Rule 7)
- [ ] Check: Would I feel respected receiving this? (Rule 5)
- [ ] Run Humanity Test (Rule 8) — 7-point checklist
- [ ] Verify word count (if applicable): 800+ words
- [ ] Verify format: no em dashes, no asterisks in headings, Georgia serif, justified
- [ ] Verify: TO field correct for PILOT (Ayesha only) vs LIVE (candidate + hiring@)
- [ ] Run harness validation (pre-send check)
- [ ] Get Ayesha approval before going LIVE

---

## PREVIOUS VERSIONS (Archived, reference only)

- `rule_all_feedback_emails_use_locked_tone.md` — Consolidated into this file
- `lesson_no_intent_inference_rejection_emails_2026_06_01.md` — Consolidated into Rule 1
- `warm_bench_final_locked_approach.md` — Consolidated into Haroon Yasin section + Rule examples
- `values_feedback_email_tone_locked_2026_05_12.md` — Consolidated into this file

---

## SKILL REFERENCES

All candidate communication skills reference this master file:
- `skill/cv-screening-rejections.md` → READ: [This File](CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md)
- `skill/gwc-rejection-emails.md` → READ: [This File](CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md)
- `skill/values-feedback-emails.md` → READ: [This File](CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md)
- `skill/warm-bench-feedback-emails.md` → READ: [This File](CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md)

---

## UPDATES & CHANGES

**To update this philosophy:**
1. Ayesha edits this file directly
2. All skills automatically inherit the change (no skill files need updating)
3. Harness rules auto-apply to all email types
4. No scattered rules, no confusion

**Date locked:** 2026-06-09
**Last updated:** 2026-06-09
