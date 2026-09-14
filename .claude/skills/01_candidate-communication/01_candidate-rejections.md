---
name: Candidate Rejections SOP (CV-Stage)
description: Reject candidates during CV screening with warm, specific feedback on ROLE FIT, tied to their actual CV. 800+ words. Never replays the application or coaches the career. v8 design. Feedback widget required. For warm bench feedback (values-passed candidates), see 03_warm-bench-feedback-email.md.
type: feedback
---

## 🔒 CORE TONE — APPLIES TO THIS AND EVERY CANDIDATE COMMUNICATION

**Read [CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md](../../../memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md) first — the CORE TONE section at the top.** Locked 2026-09-14.

**The one rule:** explain OUR hiring decision; do not evaluate THEM as a person.
**The sentence test:** describe the moment, then say what it meant to US. Never conclude what it means ABOUT THEM.

**Six behaviours that must never appear:** coaching · career direction · grading an answer · person-level judgement · replaying evidence (especially a list of everything they failed to demonstrate) · private-note leakage from the scorecard.

🔴 A disclaimer does not neutralise a prescription. 🔴 A heading is not an instruction. 🔴 Never shorten a letter to make it warmer.

---


## 📖 READ FIRST: Master Tone Philosophy

**All candidate communication must follow the principles in:**
[CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md](../../../memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md)

**🔒 LOCKED LAYOUT (2026-06-10):** Import the visual layout from `scripts/utils/v8_template.py` (`H/SUB/P/PS/FOOTER/wrap/attach_logo/EYEBROW`). NEVER redefine the card/header/footer/helpers inline. Same layout for ALL candidate comms. Full spec: [v8_candidate_comms_layout_LOCKED.md](../../../memory/v8_candidate_comms_layout_LOCKED.md).

This skill describes HOW to structure the email. The master file describes THE TONE PHILOSOPHY and rules that govern WHAT you write.

**Key rules that the harness enforces (HARD BLOCKS):**
- **Rule 1:** No psychologizing ("you seemed", "you lacked", "you would likely struggle", etc.)
- **Rule 2:** Evidence-based only (every statement traceable to CV text)
- **Rule 3:** Scorecard translation (interpret, don't transfer harsh wording)
- **Rule 4:** Role-fit explanation ("The role requires..." not "You lacked...")
- **Rule 7:** Specificity (email could only be written about this candidate)

**Warnings (allowed to send, Ayesha notified):**
- Generic subject lines
- Recruiting jargon ("strong candidate", "excellent fit", etc.)

Before drafting, read the master file. The harness validates these at send time.

---

## Objective

Reject candidates during CV screening phase with specific, warm, reflective feedback tied to their actual CV.

**Note:** For candidates who cleared the values interview but weren't selected for the current role, see **skills/03_warm-bench-feedback-email.md** instead. That is a separate skill.

---

## TYPE 1: CV-STAGE REJECTION (800+ words)

**Purpose:** Reject a candidate at the resume screening stage with specific, warm, reflective feedback tied to their actual CV.

**Prerequisites:**
1. Candidate data verified in Markaz DB (full name, email, app_id, CV text)
2. Full CV has been read thoroughly
3. JD read and understood (you know what we're looking for)
4. User approval obtained before sending

**Steps:**

1. **Verify CV content from database** — pull resume_data from candidates table. Minimum 10,000 chars. Flag if >8,000 chars before generation.

2. **Read full CV carefully** — identify 2–3 genuine strengths and 1–2 honest gaps. Only use observations from actual CV text.

3. **Write subject line** — simple, direct (not story-driven). Examples:
   - "Your background and our hiring decision"
   - "Thank you for your interest in [Role]"
   - Avoid em dashes, flowery language

4. **Opening paragraph** — warm greeting by candidate's name, thank them for time and interest, brief context about the screening process.

5. **Body sections.** 🔒 **The three heading names are LOCKED and unchanged.** What changed on 2026-09-14 is the CONTENT and register inside them.

   **This is feedback on ROLE FIT, not a report on their application.** The goal is that the candidate understands why we are not moving forward *for this particular role*, and finishes reading feeling respected and seen. Three things should be clear to them: they were genuinely reviewed, they understand why this role wasn't the match, and they still feel respected.

   **The most important principle** — talk about what we could or could not ESTABLISH, never about what they lack:
   - ✅ "We weren't able to see enough evidence of having owned growth strategy at an organizational level."
   - ❌ "You have not led growth strategy at an organizational level."

   **Never replay the application.** Use it internally as evidence, then synthesise it into one hiring perspective. Do NOT quote answers back, walk through it question by question, point out individual unanswered questions, write "you were asked X and you answered Y", or reproduce any weak, incomplete or embarrassing response.
   - ✅ "We weren't able to get enough insight into how you've navigated ambiguity, difficult trade-offs, and changing priorities."
   - ❌ "The application asked how you handled ambiguity and you responded 'NAAAAA'."

   **Dignity check:** does the candidate need this detail to understand our decision? If no, leave it out.
   - **What we appreciated:** 2–3 specific strengths from the CV, cited to actual experience. Keep it **short**. Name what is genuinely there and stop; do not interpret every strength back at them or explain why each one matters. That lecture is what makes a rejection read as condescending.
   - **Where we found questions:** what THIS role required and what the application did not make visible. Frame as our requirement, never their deficiency. Write "we could not clearly see X in the application", never "you need to develop X". State explicitly that there may well be experience behind the application showing this more strongly; we simply could not see enough of it here.
   - **What we think you should do next:** despite the heading, this is a **warm close, not a development plan**. Restate plainly what the role needed, acknowledge the breadth they do bring, leave the door open in general terms.

   **Banned in all three sections** (the letter is feedback, not career coaching):
   - telling them what to develop, document, build or spend time on
   - suggesting alternative job titles (e.g. "a Trainer or Coordinator role") — however kindly meant, it reads as *you are not senior enough*
   - any advice inside the P.S.

   **Unanswered application questions are NEVER named.** Do not point out that a question went unanswered. Translate it into what we could not establish: "we weren't able to get enough insight into how you've navigated ambiguity and shifting priorities."

   **One light, optional, application-oriented observation is allowed**, phrased about the application and never about them:
   - ✅ "If you have experiences where you owned strategy and outcomes end-to-end, bringing those forward more clearly in a future application could help us understand that part of your experience."
   - ❌ "Your next step should be to seek a role where you can own an initiative end-to-end."

   **P.S.:** something genuinely nice and specific we noticed about THEM. Not a lecture, not advice, not a role suggestion, not a restatement of the decision.

6. **Closing statement:** "The door remains open. Keep an eye on our careers page at www.taleemabad.com."

7. **Sign-off:** Exact footer: Warm regards, / People and Culture Team / Taleemabad / hiring@taleemabad.com | www.taleemabad.com / Sent on behalf of Talent Acquisition Team by Coco

8. **Feedback widget:** Always include. Parameters: `feedback_widget(candidate_name, role, app_id, "Application Feedback")`

9. **HTML format:** v8 design only. Use helpers: `H()` = blue #1565c0 headings · `SUB()` = green #1b5e20 subheadings · `P()` = Georgia serif 15px/1.8 justified · `PS()` = green italicized P.S. box

10. **Word count:** **Minimum 800 words**, for every feedback letter including this one (Ayesha 2026-09-14, confirmed after briefly trialling 350-550). With coaching and application replay both HARD BLOCKED, the length has to come from being more specific about the candidate's own experience and about exactly what this role needed. **If a letter runs short, add evidence, never guidance.**

11. **Recipients:** TO = candidate email, CC = hiring@taleemabad.com + ayesha.khan@taleemabad.com

12. **Test mode:** Always PILOT = True first (sends to Ayesha + Jawwad only). Ask user for approval on output before switching PILOT = False.

13. **Send:** Call safe_sendmail() bouncer, never smtplib.sendmail() directly. Log context: `f'cv_rejection_{candidate_name}'`

---

## NON-NEGOTIABLE RULES (ALL REJECTION EMAILS)

1. **Tone is "with" not "at"** — write as if reflecting together, not judging. Never use "you failed" or "you lack" phrasing.

2. **No em dashes anywhere** — replace with period, comma, colon, or parentheses. Em dashes look AI-generated.

3. **"We" voice only** — never "I". Never mention Coco or AI in the email body.

4. **They/them pronouns** — always gender-neutral. Never "he/she/his/her".

5. **Specific CV evidence only** — every strength and gap must be tied to actual CV text. Never suggest a skill they demonstrably have. Never make up observations.

6. **No "letter" references** — don't call it "this letter" in the body. Internal framing only.

7. **Never assume data** — if not in CV, state "Not mentioned in your CV" rather than filling in gaps.

8. **CC recipients must be exact** — hiring@taleemabad.com + ayesha.khan@taleemabad.com. No other CCs unless user specifies.

9. **Always ask for approval before sending** — PILOT mode first, user reviews, then live. No exceptions.

10. **Feedback widget is mandatory** — ALL personalised rejections include it. DO NOT include in transactional emails (invites, reminders).

---

## Pre-Send Checklist (Before Pilot)

- [ ] CV read in full, data verified from DB
- [ ] Subject line is simple, no em dashes
- [ ] Opening thanks candidate by name
- [ ] 2–3 genuine strengths cited with specific CV text
- [ ] 1–2 role-fit gaps framed as what we could not establish, never as what they lack
- [ ] No question-by-question replay, no quoted answers, no named unanswered questions
- [ ] P.S. is something nice and specific about them, not a lecture
- [ ] Closing section is a warm note, NOT advice or a development plan
- [ ] Closing: "The door remains open. Keep an eye on our careers page at www.taleemabad.com."
- [ ] Word count ≥800
- [ ] v8 HTML design used (blue headings, green subheadings, Georgia serif, justified)
- [ ] Feedback widget included with correct app_id
- [ ] Sign-off is exact (Warm regards, / People and Culture Team / etc.)
- [ ] Recipients: TO = candidate, CC = hiring@taleemabad.com + ayesha.khan@taleemabad.com
- [ ] PILOT_MODE = True (sends to Ayesha + Jawwad only)
- [ ] safe_sendmail() bouncer used, context logged

---

## Common Mistakes

1. **Sending to candidate directly without pilot** — PILOT_MODE = False immediately. Result: candidate gets email before user review. Do not do this.

2. **Using CV data that doesn't match DB** — candidate's name, email, or experience details wrong. Always query Markaz first.

3. **Assuming experience they don't have** — "Your 15 years in education..." when CV says 8. Read carefully, don't fill gaps.

4. **Tone sounds harsh or diagnostic** — "You don't have enough X" is wrong. "We were looking for more depth in X" is right.

5. **Missing feedback widget** — widget is mandatory for all personalised rejections. Check import: `from scripts.utils.feedback_widget import feedback_widget`

6. **Wrong recipients** — forgetting to CC hiring@taleemabad.com or ayesha.khan@taleemabad.com. Verify CC list before sending.

7. **Word count too low** — minimum 800 words. Count before wrap(). Reach it with more detail about THEIR experience, never with advice or a walk through their answers.

8. **Em dashes in subject or body** — search for " — " and replace with period, comma, or colon.

9. **"I" voice instead of "We"** — "I appreciated" is wrong, "We appreciated" is correct.

10. **Sending without approval** — ALWAYS get user approval on pilot before going live. This is SOP #4 (Approval before everything).

---

## Reference Implementations

**CV-stage rejection, exact format:** scripts/jobs/job36/send_job36_values_feedback_junaid_jawad_formatted.py (shows v8 design structure, H()/SUB()/P()/PS() helpers, feedback_widget integration, safe_sendmail usage, PILOT_MODE pattern)

**Warm bench pattern:** See memory/feedback_email_rules.md for exact closing language per type

---

## Commitment (Coco, 2026-04-10)

I will reject CV-stage candidates with warm, specific feedback tied to their actual CV. I will use v8 design. I will include feedback widget. I will pilot first, get approval, then go live. No em dashes. "We" voice. They/them pronouns. Safe_sendmail bouncer. Verification before sending. For warm bench feedback (values-passed candidates not selected for role), I will use skills/03_warm-bench-feedback-email.md instead.
