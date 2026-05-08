---
name: Candidate Feedback Email Rules
description: Standing rules for all candidate feedback emails, values scorecards, and interview feedback writeups
type: feedback
---

Rules confirmed by user 2026-03-25. Apply to every feedback email, values scorecard, and interview feedback writeup without exception.

**Rule 1: Never mention the interviewer's name**
Never name the interviewer in any feedback email. The candidate's name is fine. Interview date is fine. But the interviewer's name must never appear.

**Why:** Privacy/internal policy — the candidate does not need to know who evaluated them.

**How to apply:** Before sending any feedback email, scan for interviewer names and remove them. Replace with neutral phrasing like "during your interview" or "during the conversation."

---

**Rule 2: Never imply we only accepted professional-context examples**
Never write or imply that a candidate's answer was weak because it was personal rather than professional. We consider both personal and professional examples equally. The weakness should be assessed on whether the example answered the question clearly, directly, and strongly — not on whether it came from personal or professional life.

**Never say:**
- "we were looking for a professional context"
- "the example was personal, not professional"
- "we needed a workplace example"
- "the absence of a professional episode"

**Instead:** Assess whether the example was specific enough, high-stakes enough, or directly answered the question — regardless of its context.

**Why:** User confirmed we evaluate both contexts. Implying otherwise is factually wrong and unfair to the candidate.

**How to apply:** When writing about gaps in a values dimension, focus on the quality and depth of the example — was it specific? Did it show a real decision point? Did it demonstrate the value directly? — not whether it came from work or personal life.

---

**Rule 3: HTML formatting rules for feedback emails**

A. Main headings (e.g. "What We Liked Most About You", "Where We Found Ourselves Sitting With Questions") must be bold, visually distinct. Use blue (#1565c0) for main headings.

B. Subheadings / support lines must be visually distinct from body text. Style in green (#1b5e20), bold.

C. Approved colors only: Blue, Green, Red. No other colors.

D. Overall email must feel warm, polished, pleasant to read, slightly designed — not plain or text-heavy. Use font-family Georgia or similar serif. Max-width 640px. Line-height 1.7.

**Why:** User finds plain text emails too basic and AI-looking. HTML formatting makes emails feel more thoughtful and brand-appropriate.

**How to apply:** Always write feedback emails in HTML. Use the structure: serif font, green bold headings, blue bold sublines, standard body paragraphs. Check before finalising: headings styled? sublines styled? colors approved only? visually warm and polished?

---

---

**Rule 4: No dashes or "letter" references (confirmed 2026-03-25)**
- Never use " —" (em dash) in feedback emails. It looks AI-generated. Replace with a period, comma, or colon depending on context.
- Never refer to the email as a "letter" in the body text. That is internal framing only.

**Why:** User confirmed these patterns make the writing feel robotic and impersonal.

**How to apply:** Before finalising, scan for " —" and replace. Scan for "letter" and remove or rewrite.

---

**Rule 5: Tone — considerate, open-handed, emotionally careful (confirmed 2026-03-25)**
The decision must be clear and direct. But all feedback must feel respectful, human, and supportive — not heavy or evaluative.

**Specific requirements:**
- Avoid absolute or harsh phrasing. Never say things like "makes it impossible", "a direct no disqualifies", "this was a miss". Use reflective language instead: "we found ourselves wondering", "we sat with a question here", "this left us uncertain".
- Add brief emotional cushioning before the gap section — acknowledge that receiving this kind of feedback takes courage before diving into what didn't come through.
- Write WITH the candidate, not AT them. The reader should feel understood and valued, not judged.
- The goal: candidate leaves feeling more capable than when they walked in, not discouraged.

**Why:** User confirmed 2026-03-25 — warmth and emotional care are non-negotiable. Feedback should encourage growth, not cause conflict or hurt sentiments.

**How to apply:** Before finalising any gap paragraph, re-read it as if you are the candidate. If it feels heavy, clinical, or evaluative, rewrite it with softer, more reflective language. Check that emotional cushioning exists before the gap section opens.

---

**Rule 5: Warm bench vs values-failed closing language**
- **Warm bench candidates** (passed values, ranked 2nd/3rd): say we are keeping them in our pipeline and will reach out proactively.
- **Values-failed candidates**: do NOT promise pipeline or proactive outreach. Instead say the door is open IF they reflect and grow — the candidate comes back to us. Use language like: "The areas we have named above are genuinely closable with time and reflection. Should you work through them and find yourself drawn back to our mission, we would welcome that conversation with a genuinely open mind."

**Why:** Warm bench is a specific status. Values-failed candidates have not earned that promise. But we still keep the door open warmly.

---

**Current confirmed design (v6, 2026-03-25):**
- Header: white background, blue text, blue bottom border, Taleemabad logo (CID)
- Main headings: blue (#1565c0)
- Subheadings: green (#1b5e20)
- Body text: justified, Georgia serif, 15px, line-height 1.8
- P.S. block: light green background, green left border
- Footer: "Taleemabad" in blue

---

**Three Candidate Email Types (confirmed 2026-03-25)**

**Type 1: Generic Rejection (initial screening / CV not shortlisted)**
- Minimum 500 words
- Sent to candidates whose resume did not make it past the initial screening round
- Tone: warm, respectful, specific to what was in their CV
- No need for values scorecard — based on CV read only
- Reference script: generate_rejection_emails_job36.py · send_job36_rejection_pilot.py

**Type 2: Values Failed Email (did not clear values round)**
- 800-1100 words
- Sent to candidates who attended the values interview but did not pass
- Based on values scorecard — must quote specific moments from the interview
- Closing: door is open if they grow and come back (NOT warm bench promise)
- Reference script: send_job36_values_feedback_pilot.py (v8 confirmed final design)
- Full design spec: see above in this file

**Type 3: Warm Bench Email (values fit, not moving forward right now)**
Three scenarios:
  a. Cleared values but hiring paused or not the right fit for this position
  b. Went to GWC round but ranked 2nd/3rd/4th/5th — keeping in pipeline
  c. Cleared values, sent case study, case study did not meet the bar — keeping in pipeline because values passed
- For scenario (c): SOP and philosophy to be provided by user before drafting
- Closing: proactive pipeline promise — "we will reach out when the right role opens"
- Tone: warmer and more forward-looking than values-failed emails

**Why:** User confirmed 2026-03-25 — these three types cover all candidate rejection/thank-you scenarios. Template and formatting stay consistent across all types; only content and closing language change.

---

**Pre-send checklist (mandatory):**
- [ ] Removed interviewer name?
- [ ] No implication that personal examples were unacceptable?
- [ ] Tone considerate and open-handed — no absolute/harsh phrases?
- [ ] Brief emotional cushioning before gap section?
- [ ] Main headings in blue, subheadings in green?
- [ ] Only approved colors used (blue, green, red)?
- [ ] Text justified?
- [ ] Closing uses correct warm-bench vs values-failed language?
- [ ] Email looks polished and pleasant, not plain?
