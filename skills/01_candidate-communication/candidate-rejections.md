---
name: Candidate Rejections SOP (CV-Stage)
description: Reject candidates during CV screening with warm, specific feedback tied to their actual CV. 800+ words. v8 design. Feedback widget required. For warm bench feedback (values-passed candidates), see warm-bench-feedback-email.md.
type: feedback
---

## Objective

Reject candidates during CV screening phase with specific, warm, reflective feedback tied to their actual CV.

**Note:** For candidates who cleared the values interview but weren't selected for the current role, see **skills/warm-bench-feedback-email.md** instead. That is a separate skill.

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

5. **Body sections (reflective structure):**
   - **What we appreciated:** 2–3 specific strengths from CV (cite actual experience/accomplishments)
   - **Where we found questions:** 1–2 honest gaps in experience or skills (reflective, not diagnostic — "we were looking for..." not "you lack...")
   - **What we think you should do next:** actionable advice tied to the gaps

6. **Closing statement:** "The door remains open. Keep an eye on our careers page at www.taleemabad.com."

7. **Sign-off:** Exact footer: Warm regards, / People and Culture Team / Taleemabad / hiring@taleemabad.com | www.taleemabad.com / Sent on behalf of Talent Acquisition Team by Coco

8. **Feedback widget:** Always include. Parameters: `feedback_widget(candidate_name, role, app_id, "Application Feedback")`

9. **HTML format:** v8 design only. Use helpers: `H()` = blue #1565c0 headings · `SUB()` = green #1b5e20 subheadings · `P()` = Georgia serif 15px/1.8 justified · `PS()` = green italicized P.S. box

10. **Word count:** Minimum 800 words. Verify before wrapping.

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
- [ ] 1–2 honest gaps explained reflectively
- [ ] "What to do next" section is actionable
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

7. **Word count too low** — minimum 800 words. Count before wrap(). Don't send <800w.

8. **Em dashes in subject or body** — search for " — " and replace with period, comma, or colon.

9. **"I" voice instead of "We"** — "I appreciated" is wrong, "We appreciated" is correct.

10. **Sending without approval** — ALWAYS get user approval on pilot before going live. This is SOP #4 (Approval before everything).

---

## Reference Implementations

**CV-stage rejection, exact format:** scripts/jobs/job36/send_job36_values_feedback_junaid_jawad_formatted.py (shows v8 design structure, H()/SUB()/P()/PS() helpers, feedback_widget integration, safe_sendmail usage, PILOT_MODE pattern)

**Warm bench pattern:** See memory/feedback_email_rules.md for exact closing language per type

---

## Commitment (Coco, 2026-04-10)

I will reject CV-stage candidates with warm, specific feedback tied to their actual CV. I will use v8 design. I will include feedback widget. I will pilot first, get approval, then go live. No em dashes. "We" voice. They/them pronouns. Safe_sendmail bouncer. Verification before sending. For warm bench feedback (values-passed candidates not selected for role), I will use skills/warm-bench-feedback-email.md instead.
