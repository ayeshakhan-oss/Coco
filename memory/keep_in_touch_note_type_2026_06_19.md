---
name: Keep-in-Touch Note — candidate-invite type #5 (2026-06-19)
description: Post-conversation warm-hold note. We already spoke, role is being revisited, candidate still in our thinking — no booking button, no promise of timeline/outcome. Skill 06.
type: project
---

# Keep-in-Touch Note (Skill 06 — invite type #5)

**Locked 2026-06-19.** A reusable candidate-communication type for the recurring
situation: *we had an initial conversation, we now need time to think, and we want
to circle back later.* It exists so a still-warm candidate is never left reading our
silence as a "no."

## When to use
- We have ALREADY spoken with the candidate (e.g. an exploratory call), and
- The role or decision is being revisited / paused, and
- We want to be honest that they are still in our thinking — without committing to
  when we will move, or to any outcome.

First real use: Job 32 (Fundraising & Partnerships Manager) candidates who had
exploratory calls in May–June 2026; role being revisited in mid-2026.

## What makes it different from the other 4 invite types
This belongs to the invite family (positive, forward-looking, uses the locked invite
design), NOT the rejection/feedback family. So the Skill 01 "This is not a yes for
now." opener does NOT apply. But two HARD rules are unique to this type:

1. **NO calendar booking button, NO booking/document links.** We are explicitly not
   asking them to schedule anything yet. Body flows straight to the signature. (All
   other invite types end in a purple booking button — this one must not.)
2. **NO promise or commitment.** This was the user's central instruction. The team
   genuinely intends to be in touch again but is "not sure when, not sure of the
   outcome," and does not want candidates "counting on" anything.
   - FORBIDDEN: "we will reach out / be in touch / contact you", hard dates
     ("by early July"), any outcome guarantee.
   - USE instead: honest + conditional — "when we have more clarity, we would
     genuinely welcome the chance to be back in touch."

   This mirrors the spirit of the [[mandatory_opening_line_no_future_promise_2026_06_18]]
   no-future-promise rule, even though that rule's hard-block is scoped to rejection emails.

## Design
LOCKED invite template, button removed. See
[[locked_email_template_interview_invites_FINAL_2026_05_13]]:
- Eyebrow: `TALENT ACQUISITION • KEEPING IN TOUCH`
- Title: `Keeping in Touch` · Subtitle: `An honest note on where things stand`
- Subject (default, user's pick): `Still very much in our thinking — [Name]`
- Georgia serif, #f5f5f5 page / #e5e7e2 wrapper / 775px white card, CID logo,
  left-aligned signature. No em dashes in body.

## Recipients & send flow
- Recipients are NEVER hardcoded — send only to people we actually spoke with, named
  by the user. Files show who was *invited* to a call, not who *attended* — confirm.
- Script: `scripts/send_keep_in_touch_pilot.py` holds a `CANDIDATES` list
  (`{"name","email"}`). Refuses to send if empty.
- **Pilot:** `PILOT_MODE=True` → one sample render to Ayesha only, no CC.
- **Live:** `PILOT_MODE=False` → loops the list, one INDIVIDUAL email per candidate
  (never a shared To/CC that exposes the group). Live CC = ayesha, hiring@,
  sabeena.abbasi (Job 32 hiring manager). Sender = ayesha.khan. safe_sendmail +
  allow_candidate_addresses per Rule 1.13. Context: `keep_in_touch_note_live_<name>`.

## Reference
- Script: `scripts/send_keep_in_touch_pilot.py`
- Skill: `.claude/skills/06_candidate-invites/SKILL.md` (type #5)
- Sibling reference: `scripts/send_exploratory_call_pilot.py`
