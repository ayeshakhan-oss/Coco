# Warm Hold — Decision-Pending Update Emails (Type 5)

**Added:** 2026-08-12 (requested by Ayesha)
**Status:** 🔒 PRODUCTION READY — content locked, first live send requires pilot approval as always

---

## What This Type Is

A short, honest **status update** to a candidate who has already been interviewed but for whom **no decision has been made yet**, because we are still collecting notes/inputs from the panel. It tells them three things:

1. Thank you — we haven't forgotten you.
2. We have not decided yet; we are still gathering notes from everyone who was part of the conversation.
3. We will reach out **by [a stated date, e.g. "next week"]** with the update on their interview.

**This is NOT a decision email.** It carries no verdict, no feedback, no evaluation. Its only job is to prevent post-interview silence from being read as rejection, and to put a date on when they'll hear from us.

---

## When to Use (vs. the neighbouring types)

| Situation | Use |
|---|---|
| Interviewed, decision pending, we CAN commit to a short timeline ("by next week") | **THIS type** |
| Exploratory/early conversation, role being revisited, NO reliable timeline | Keep-in-Touch Note (Skill 06, type #5 — forbids dates/promises) |
| Decision made: no, but keep warm | Warm Bench Feedback (800-1100 words) |
| Decision made: rejection with feedback | CV Rejection / Values Feedback / GWC Rejection |

**Rule of thumb:** if you cannot name a date you are confident we will honour, this is the wrong type — use the Keep-in-Touch Note instead.

---

## Exemptions From the Universal Candidate-Comms Rules (Ayesha, 2026-08-12)

These two exemptions apply to THIS TYPE ONLY and exist because this email communicates a *pending* decision, not a decision:

1. **NO "This is not a yes for now." opening line.** That locked opening (CLAUDE.md Rule 10) belongs to decision emails. Here no decision exists; opening with it would be false and alarming. Open with thanks + honesty about where things stand.
2. **The future-promise ban is deliberately inverted.** The entire point of this email is a dated commitment: "you can expect to hear from us by [DATE]." This is the ONE candidate-comms type where "we will reach out" language is required, per Ayesha's explicit instruction (2026-08-12).
   - **Guardrail:** only commit to a date we will actually honour. If the date risks slipping, widen it ("by the end of next week"). If it slips anyway, send a fresh hold note BEFORE the promised date passes — a broken promise here is worse than no email.
3. **The 800-word minimum does NOT apply.** That rule is for feedback emails. This is a status note: **target 120-250 words**. Longer starts to read like a hidden verdict.

**Everything else still applies:** collective "we" voice (never "I"), they/them, no em dashes, no internal jargon (values/GWC/scorecard/case study), no interviewer names, no fabrication, no "[PILOT - ]" prefix in live sends, no "by Coco" sign-off line, v8 layout imported from `scripts/utils/v8_template.py` (Rule 8), pilot to Ayesha before any live send.

**Content bans specific to this type:**
- ❌ NO feedback or evaluation of the interview ("you did well", "we were impressed") — it inflates or deflates hope before the decision exists.
- ❌ NO hints of direction ("things are looking good", "it's very competitive right now").
- ❌ NO apology theatrics ("we're so sorry for the delay") — honest and matter-of-fact beats grovelling.
- ❌ NO request for more materials/actions from the candidate — this email asks nothing of them.

---

## 🔒 LOCKED GENERIC TEMPLATE (Ayesha's wording, approved 2026-08-12)

This is a **generic template — used verbatim for ANY position**. Only the placeholders change per send: `[Candidate Name]`, `[Role Name]`, `[Day/Date]`. Do NOT personalize, expand, or add lines. One approved edit vs. Ayesha's original draft: "I hope you're doing well" → "We hope you're doing well" (Rule 12 — collective "we"; Ayesha approved 2026-08-12). Sign-off keeps her "Warmly," attributed to the team (never an individual's name).

```
Hi [Candidate Name],

We hope you're doing well.

Thank you again for taking the time to interview with us for the
[Role Name] position. It was great getting to know more about your
experience and background.

We're currently wrapping up a few internal discussions and consolidating
feedback from the interview process before we make a final decision. We
wanted to keep you in the loop and let you know that we expect to share
an update with you by [Day/Date].

Thank you for your patience and for your continued interest in joining
Taleemabad. We really appreciate the time and effort you've invested in
the process.

Warmly,
People and Culture Team
Taleemabad
hiring@taleemabad.com | www.taleemabad.com
```

Word count of body: ~115 words. Content is LOCKED — placeholders only.

**Subject (🔒 LOCKED, Ayesha 2026-08-12 — same for every position):**
`A Quick Note from Our Side`
Pilot version: `[PILOT - ] A Quick Note from Our Side`

---

## Layout & Send Mechanics

- **Layout:** v8 candidate-comms layout via `scripts/utils/v8_template.py` (`H/SUB/P/PS/FOOTER/wrap/attach_logo/EYEBROW`) — same as all Skill 01 types. Header eyebrow: `PEOPLE & CULTURE • INTERVIEW UPDATE`. NO feedback widget (nothing to rate — no feedback was given).
- **Script:** `scripts/send_decision_pending_update_pilot.py` (create on first use from the v8 imports; CANDIDATES list + PILOT_MODE flag, same pattern as other Skill 01 scripts).
- **Pilot:** PILOT_MODE=True → Ayesha ONLY, no CC, `[PILOT - ]` prefix.
- **Live (after approval):** candidate (TO) + CC ayesha.khan@ + hiring@. Clean subject.
- **Send via `safe_sendmail()` only.**

---

## Self-QA Before Piloting (this type)

- [ ] Date stated is one we will actually honour (confirmed with Ayesha)
- [ ] Locked generic template used VERBATIM — only [Candidate Name] / [Role Name] / [Day/Date] filled; no added or personalized lines
- [ ] Opens with thanks + honesty; does NOT open with "This is not a yes for now."
- [ ] "We" voice; no "I"; no em dashes; no jargon; no interviewer names
- [ ] v8 layout imported (not redefined inline); logo CID-embedded
- [ ] Subject plain-honest; [PILOT - ] prefix in pilot only
- [ ] Pilot goes to Ayesha only
