---
name: Role-Closure Note — candidate-invite family (2026-07-23)
description: Post-exploratory-call closure. We spoke, promised a July follow-up, and now need to close the loop honestly because the need went away (business needs changed / not hiring). Skill 06 family. Sequel to Keep-in-Touch.
type: project
---

# Role-Closure Note (Skill 06 invite family — closure sequel to Keep-in-Touch)

**First use: 2026-07-23.** Job 32 fundraising & partnerships exploratory-call pool.
Sequel to the [[keep_in_touch_note_type_2026_06_19]] note (2026-06-19) that told these
candidates we hoped to be back in touch in July. This note honours that July word and
closes the loop when the opening did not materialise.

## When to use
- We already had an exploratory conversation with the candidate, AND
- We told them we would follow up (a soft July commitment), AND
- The need has now gone away (business needs shifted / not hiring in that area for now),
  so there is nothing to invite them to. Close the loop warmly instead of going silent.

## Family & rules
Belongs to the Skill 06 INVITE family (locked invite design), NOT the rejection/feedback
family. So the four-type harness hard-blocks do NOT apply: no "This is not a yes for now."
opener, no 800-word floor, no required section headings. (Same carve-out as Keep-in-Touch.)

Universal candidate-comm rules DO apply and were all verified clean via the real harness
check functions (scripts/evals/candidate_communication_eval.py):
- Rule 1 no intent-inference, Rule 12 collective "we" voice (no I/my/me),
- no em dashes, no internal jargon, no interviewer names,
- no recruiting abstractions, no future-outreach promise (candidate-initiated redirect only).
Validator used: scratchpad/validate_closure.py (imports build_html + the check_* fns).

## Locked content decisions (Ayesha, 2026-07-23)
1. **No defined role/level.** It was an EXPLORATORY call about fundraising & partnerships
   generally while weighing team expansion. NEVER imply a specific vacancy ("... Manager
   role") or level. Say "the exploratory conversation we had earlier about fundraising and
   partnerships." Subject: "An update on our conversation, [First]". Header: "An Update from Us".
2. **Reason = need went away, not internal fill.** Do NOT say we filled it internally.
   Say: "we were exploring people across fundraising and partnerships ... since then, our
   business needs have shifted, and we do not expect to be hiring in this area for now."
3. **"earlier"**, not "earlier this year".
4. Per-person reflection = genuine strengths + gentle role-fit color, framed as "the work we
   were exploring leaned toward X" (past tense, decision-not-person). Internal data STRIPPED:
   levels/ratings (1A/2B, "junior"), salary/compensation figures, internal role labels.
5. Body text justified (text-align: justify). No booking button. One link only: website.
6. Redirect is candidate-initiated: "we would genuinely welcome seeing your name come through
   ... what is currently open on our website at taleemabad.com." Never "we will reach out."

## Send flow (as executed)
- Script: `scripts/send_role_closure_pilot.py` (per-candidate `reflection`; shared P1/P2/P4/P5).
- Pilot: PILOT_MODE=True -> one render per candidate to ayesha.khan ONLY, no CC.
- Live: PILOT_MODE=False -> one INDIVIDUAL email per candidate (never shared To/CC),
  CC = ayesha, hiring@, sabeena.abbasi. Sender = ayesha.khan. Context role_closure_note_live_<name>.
- Script restored to PILOT_MODE=True after the live send (pilot-safe default).

## Recipients (LIVE sent 2026-07-23)
Five candidates from the Job 32 exploratory-call pool: Kanooz, Nirmal, Mushahid, Saadia,
Falah. (Email addresses live in the send script + logs/email_audit.log, not duplicated
here — memory files stay PII-free.) Rabia Abbas had the exploratory invite but was NOT on
the keep-in-touch / closure list.
