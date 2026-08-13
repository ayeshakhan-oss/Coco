# Case Study Update — Debrief-Pending Email (Skill 01, Type 6)

**Added:** 2026-08-13 (requested by Ayesha)
**Status:** 🔒 CONTENT LOCKED after first pilot approval — first live send requires pilot approval as always
**Parent pattern:** [Warm Hold — Decision-Pending Update (Type 5)](warm-hold-decision-pending-email.md). This is its sibling, NOT a replacement. Same family, same exemptions, different trigger and different subject line.

---

## What This Type Is

A short, honest **status update** to a candidate who has **already submitted their case study** and is now waiting to hear whether they get a debrief. It tells them three things:

1. Thank you for doing the case study — we know it cost you real time.
2. We are still running interviews for this role, so no decision exists yet.
3. We expect to update them **on the case study debrief by [a stated date]**.

**This is NOT a decision email and NOT an evaluation of their case study.** It carries no verdict, no feedback, no score, no hint of direction. Its only job is to stop post-submission silence from being read as rejection, and to put a date on when they will hear.

---

## When to Use (vs. the neighbouring types)

| Situation | Use |
|---|---|
| **Case study submitted**, debrief decision pending, we can name a short timeline | **THIS type** |
| Interviewed (values call), decision pending, no case study involved | Warm Hold — Decision-Pending Update (Type 5) |
| Case study **sent but not submitted**, needs a gentle chase | Case-Study Submission Nudge (Skill 06 family) |
| Exploratory conversation, no reliable timeline | Keep-in-Touch Note (Skill 06, type #5 — forbids dates) |
| Decision made | CV Rejection / Values Feedback / Warm Bench / GWC Rejection |

**Rule of thumb (inherited):** if you cannot name a date we will actually honour, do not send this. Widen the window instead ("by the end of next week") or send nothing.

---

## Exemptions From the Universal Candidate-Comms Rules

Inherited wholesale from Type 5 (Ayesha sanctioned those exemptions 2026-08-12; this type is the same "pending, not decided" situation, extended by her on 2026-08-13):

1. **NO "This is not a yes for now." opening line.** No decision exists; that line would be false and alarming. Open with thanks.
2. **The future-promise ban is deliberately inverted.** A dated commitment is the entire point: "we expect to share an update with you by [DATE]". **Guardrail:** if the date is going to slip, send a fresh note BEFORE it passes. A broken promise here is worse than no email.
3. **The 800-word minimum does NOT apply.** Target **120-250 words**. Longer reads like a hidden verdict.
4. **NEW, scoped to this type — "case study" is permitted candidate-facing language.** The harness lists `case study` as internal jargon (that ban protects candidates from shorthand they were never told). It does not apply here: this candidate was personally sent a case study, completed it, and submitted it. It is *their* deliverable, and Ayesha names it verbatim on the values call when she explains the three stages. "Case study debrief" is likewise language candidates have already heard from us. **This exemption is scoped to Type 6 only** and does not loosen the jargon ban anywhere else.

**Everything else still applies:** collective "we" voice (never "I"/"my"/"me"), they/them, no em dashes, no interviewer names, no fabrication, no `[PILOT - ]` prefix in live sends, no "by Coco" sign-off line, v8 layout imported from `scripts/utils/v8_template.py` (Rule 8), pilot to Ayesha only before any live send.

**Content bans specific to this type:**
- ❌ NO evaluation of the case study ("strong submission", "we were impressed", "well structured") — it pre-empts the actual assessment.
- ❌ NO hints of direction ("looking good", "it's very competitive").
- ❌ NO apology theatrics ("so sorry for the long delay").
- ❌ NO new asks — this email requests nothing of them. If we need something, that is a different email.
- ❌ NO mention of other candidates, volumes, or where they sit in a pack.

---

## 🔒 LOCKED GENERIC TEMPLATE

Generic for ANY position. Only `[Greeting Name]`, `[Role Name]` and `[Timeline]` change per send. Do not personalize, expand, or add lines.

```
Hi [Greeting Name],

We hope you're doing well.

Thank you for taking the time to complete and submit your case study for
the [Role Name] position. We know that work takes real time and thought
alongside everything else you have on, and we are grateful you gave it to us.

We are currently still in the middle of interviews for this role, so we
wanted to keep you in the loop rather than leave you waiting in silence.
We expect to share an update with you on the case study debrief by
[Timeline].

Thank you for your patience and for your continued interest in joining
Taleemabad. We really appreciate the time and effort you have invested in
the process.

Warmly,
People and Culture Team
Taleemabad
hiring@taleemabad.com | www.taleemabad.com
```

Body word count: ~135 words (inside the 120-250 target).

**Subject (proposed, confirm at first pilot):**
`A Quick Update from Our Side`
Pilot version: `[PILOT - ] A Quick Update from Our Side`

Deliberately a sibling of Type 5's locked `A Quick Note from Our Side` rather than identical, so a candidate who receives both does not see the same subject twice.

---

## Layout & Send Mechanics

- **Layout:** v8 via `scripts/utils/v8_template.py` (`P/FOOTER/wrap/attach_logo/EYEBROW`). Eyebrow key: `EYEBROW["case_study_update"]` → `PEOPLE & CULTURE • INTERVIEW UPDATE`. NO section headings (`H`/`SUB`) — this is a short note, not a feedback letter. NO feedback widget (no feedback was given).
- **Script:** `scripts/send_case_study_update_pilot.py` — `CANDIDATES` list + `PILOT_MODE` flag, same pattern as other Skill 01 scripts.
- **⚠️ SCRIPT NAMING (non-obvious, important):** the send-time hook (`scripts/hooks/pre_send_validation_hook.py`) infers the email type from the **filename**, and any script whose name contains `warm_bench`, `gwc`, `values`, or `rejection` is validated as a *feedback* email — which HARD BLOCKS it for being under 800 words and missing the "This is not a yes for now." opening. Keep this type's script named `send_case_study_update_pilot.py`. Do NOT rename it into one of those patterns.
- **Pilot:** `PILOT_MODE=True` → **Ayesha ONLY, no CC**, `[PILOT - ]` prefix (CLAUDE.md Rule 4).
- **Live (after approval):** candidate (TO) + CC ayesha.khan@ + hiring@. Clean subject.
- **Send via `safe_sendmail()` only.**

---

## Self-QA Before Piloting (this type)

- [ ] Candidate has genuinely **submitted** a case study (verified in Markaz AND mailbox, per the dual-source rule) — never send this to someone who has not submitted
- [ ] Timeline stated is one we will actually honour, confirmed with Ayesha
- [ ] Locked template used verbatim; only greeting name, role and timeline filled
- [ ] Opens with thanks; does NOT open with "This is not a yes for now."
- [ ] No evaluation of the case study, no direction hints, no new asks
- [ ] "We" voice; no "I"; no em dashes; no interviewer names
- [ ] Word count 120-250
- [ ] v8 layout imported (not redefined inline); logo CID-embedded
- [ ] `[PILOT - ]` prefix in pilot only; pilot to Ayesha alone
- [ ] Diary the promised date so a follow-up goes out BEFORE it passes if it slips
