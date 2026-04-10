---
name: Warm Bench Feedback Email
description: Rejection emails for candidates who passed values + had good GWC but weren't selected for current role. Signal future opportunity. 800-1000 words. Storytelling tone. Separate from CV-stage rejections.
type: feedback
---

## Objective

Send thoughtful, warm feedback to candidates who cleared the values interview stage and demonstrated strong alignment/GWC, but were not selected for the current role. Signal that they are valued, remain on the warm bench, and may be reconsidered for future suitable roles.

**When to send:** After final debrief/panel decision is made; candidate is OUT for current role but not permanently rejected.

**Tone:** Warm, affectionate, human, storytelling-based—almost like a thoughtful personal letter.

---

## Candidate Criteria

Send a warm bench email when:

1. **Cleared values interview** — candidate passed the values round (Values PASS, not OUT)
2. **Strong GWC or relevant strength** — either GWC was YES on all 3 questions, OR they showed exceptional strength in a domain we know we'll need again
3. **Not selected for THIS role** — but not permanently rejected from organization
4. **May fit future roles** — specific enough that you can reference when/what type of role

**Do NOT send if:**
- Candidate failed values (send CV-stage rejection instead)
- Candidate is permanently out-of-consideration (e.g., salary misalignment, location, visa issues)
- No realistic future role for them

---

## Content Structure (5 Sections)

### 1. Opening (1 paragraph, warm greeting)

Address candidate by name. Thank them for their time and energy through the interview process. Set emotional tone: thoughtful, respectful, human.

Example:
```
Hi [Name],

I wanted to reach out personally to say thank you. Over the past few weeks, 
we've had the privilege of getting to know you through our screening and values 
conversations, and I've been reflecting on what you brought to those exchanges.
```

---

### 2. What We Saw (2–3 paragraphs, evidence-based storytelling)

**Cite specific moments from values interview.** Quote their own words or reference specific examples they shared. Show that you listened deeply and remembered.

**Include:** Values scorecard observations — which values they clearly demonstrated, specific moments that showed their alignment.

Example:
```
In your values conversation, when we asked about a time you'd pushed back on 
a team decision, you told us about [specific situation]. The way you described 
your approach—balancing directness with care—showed us real strength in 
Courageous Conversations. You didn't just say you valued it; we saw it in 
how you think about team dynamics.

Your reflection on [another moment] also highlighted something important to us: 
you're someone who learns from feedback. You didn't frame mistakes as external; 
you owned them and articulated what you'd do differently. That's Continuously 
Improve in action.
```

---

### 3. GWC & Fit Assessment (1–2 paragraphs, transparent and honest)

Explain what the GWC assessment showed. Be specific about what "yes" or "conditional" meant. Reference the Markaz scorecard if applicable.

Gently explain why this role didn't move forward, WITHOUT making it about their fit. Focus on: "the current role's constraints," "different priorities," "timing," NOT "you weren't strong enough."

Example:
```
Our GWC conversation surfaced something clear: you understand our mission deeply, 
you're genuinely energized by our work, and you have the capacity to show up on 
our values daily. That's the full Yes across the board.

Where this role didn't advance isn't about your strengths—it's about the specific 
needs of this position and the team composition we're building right now. We were 
looking for [specific technical/contextual requirement] as a lead strength, and 
while you have this background, we needed someone with deeper [domain] experience 
for this particular cycle.
```

---

### 4. The Warm Bench Signal (1–2 paragraphs, future-focused)

**This is the key section.** Signal clearly and specifically that they're not permanently out.

Mention the TYPE of future role they'd be strong for, or the timeline when relevant roles open. Make it specific enough to feel real, not generic.

Example:
```
Here's what I want you to know: we're not closing the door. In fact, we're 
keeping it open deliberately.

We're actively building out our [specific function/team] over the next 6–9 months, 
and your background in [area] combined with your values alignment makes you someone 
we'd want to revisit when those conversations start. I'm going to flag your name 
in our internal talent pool, and when we start sourcing for roles that match your 
strengths, we'll reach out proactively.

Keep an eye on our careers page (www.taleemabad.com/careers), but also know that 
you'll hear from us directly when opportunities align.
```

---

### 5. Closing (1 short paragraph)

Warm, encouraging, human. Not a generic "best of luck" but something that acknowledges their worth.

Example:
```
Thank you again for investing your energy in getting to know us. Your thoughtfulness 
and integrity came through in every conversation, and that matters. We're thinking 
of you as we build the team we need.

In the meantime, if you come across insights or opportunities that feel relevant 
to what we're doing, we'd love to hear from you.
```

---

## Format & Design

**Word count:** 800–1,000 words (minimum 800)

**HTML design:** v8 design only
- Blue headings (#1565c0)
- Green subheadings (#1b5e20)
- Georgia serif body, 15px/1.8, justified (TA_JUSTIFY)
- White background, structured tables for organization
- CID logo inline if appropriate

**Sign-off (exact):**
```
Warm regards,
People and Culture Team
Taleemabad
hiring@taleemabad.com | www.taleemabad.com
Sent on behalf of Talent Acquisition Team by Coco
```

---

## Non-Negotiable Rules

1. **No em dashes anywhere** — replace with period, comma, colon, or parentheses. Dashes look AI-generated.

2. **"We" voice only** — never "I". Never mention Coco or AI in body.

3. **They/them pronouns for all candidates** — always gender-neutral, never "he/she/his/her".

4. **Specific interview evidence required** — quote or closely paraphrase their own words. Never assume or generalize.

5. **GWC transparency** — explain what their GWC was and what it means. If CONDITIONAL, state the condition clearly.

6. **Future role is SPECIFIC** — not vague "we'll keep you in mind." State actual function/timeline/domain if possible. If unknown, say: "When hiring resumes for [function] in [timeframe]."

7. **Feedback widget mandatory** — all personalised emails include it. Import: `from scripts.utils.feedback_widget import feedback_widget`. Append before wrap().

8. **Recipients (exact):** TO = candidate email, CC = hiring@taleemabad.com + ayesha.khan@taleemabad.com

9. **Pilot mode ALWAYS first** — PILOT_MODE = True sends to Ayesha + Jawwad only. Never go live without approval.

10. **Safe_sendmail bouncer required** — never call smtplib.sendmail() directly. Context log: `warm_bench_{candidate_name}`

---

## Pre-Send Checklist

- [ ] Candidate cleared values interview (Values PASS confirmed)
- [ ] GWC data reviewed from Markaz scorecard
- [ ] Values scorecard evidence extracted (quote specific moments)
- [ ] Opening thanks candidate by name, warm greeting
- [ ] "What We Saw" section quotes actual interview examples (not assumptions)
- [ ] GWC assessment explained clearly (YES on all 3? CONDITIONAL on what?)
- [ ] Reason for not selecting THIS role explained gently (not about their fit)
- [ ] Future role is SPECIFIC: function/domain/timeline mentioned
- [ ] Closing is warm and encouraging (not generic)
- [ ] Word count ≥800 (target 800–1000)
- [ ] v8 HTML design applied (blue headings, Georgia serif, justified)
- [ ] No em dashes anywhere (search + replace " — " with period/comma)
- [ ] "We" voice throughout (never "I")
- [ ] They/them pronouns only (no he/she/his/her)
- [ ] Feedback widget included with correct app_id
- [ ] Sign-off is exact (Warm regards, / People and Culture Team / etc.)
- [ ] Recipients: TO = candidate, CC = hiring@ + ayesha.khan@
- [ ] PILOT_MODE = True (sends to Ayesha + Jawwad only)
- [ ] safe_sendmail() bouncer used, context logged
- [ ] Ready to ask Ayesha for approval before going live

---

## Common Mistakes

1. **Vague future promise** — "We'll reach out if something comes up" is too soft. State actual role type/timeline.

2. **Making it about their weakness** — "You didn't have enough [skill]" sounds like rejection. Focus on role needs, not their gaps.

3. **Forgetting GWC reference** — GWC assessment was done; cite it. Readers (hiring manager/Ayesha) will want to see you tracked it.

4. **Too formal or cold** — warm bench should feel like a personal letter, not a transactional email. Add warmth.

5. **Not quoting their examples** — generic "you showed teamwork" is weak. Quote their actual story from the interview.

6. **Missing feedback widget** — widget is mandatory. Check import: `from scripts.utils.feedback_widget import feedback_widget`

7. **Wrong recipients** — forgetting to CC hiring@ or ayesha.khan@. Verify CC list before sending.

8. **Word count too low** — minimum 800. Count before wrap(). Don't send <800w.

9. **Sending live without pilot** — PILOT_MODE = False immediately. Goes straight to candidate without Ayesha review. Do not do this.

10. **Em dashes in subject/body** — search for " — " and replace with period, comma, or colon.

---

## Differences from CV-Stage Rejection

| Aspect | CV-Stage Rejection | Warm Bench Email |
|--------|-------------------|------------------|
| **When sent** | During screening phase | After values round, before final panel decision |
| **Word count** | 800+ words | 800–1,000 words |
| **Tone** | Warm, reflective, appreciative of effort | Warm, affectionate, storytelling, almost like a personal letter |
| **Evidence source** | CV text only | Values interview + GWC scorecard |
| **Focus** | Skills/experience gaps + strengths from CV | Interview moments + values alignment + GWC assessment |
| **Closing promise** | "Door remains open. Keep an eye on careers page." | "We're flagging you for future [specific role/function]. We'll reach out proactively." |
| **Signal strength** | Generic (applies to all candidates) | Specific (signals real future opportunity) |

---

## Reference Implementations

**Warm bench pattern + tone:** Similar structure to values feedback email but future-focused closing. See skills/values-feedback-emails.md for v8 design details.

**GWC reference:** Markaz scorecard values + GWC assessment should be cited explicitly. See skills/values-scorecard-scoring.md for GWC structure.

**Safe_sendmail usage:** All sends use scripts/utils/safe_sendmail.py bouncer. PILOT_MODE = True sends to Ayesha + Jawwad only.

---

## Commitment (Coco, 2026-04-10)

I will send warm bench emails only to candidates who cleared values with strong GWC. I will quote their actual interview examples. I will reference their GWC assessment. I will specify the future role/function/timeline. I will use v8 design. I will include feedback widget. I will pilot first, get approval, then go live. No em dashes. "We" voice. They/them pronouns. Safe_sendmail bouncer. Word count verified before sending.
