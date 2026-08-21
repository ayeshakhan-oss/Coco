# Internal Announcement Email (Skill 01, Type 7)

**Added:** 2026-08-20 (requested by Ayesha)
**Status:** LAYOUT LOCKED (v8) · CONTENT VARIES PER SEND — content is written or approved by Ayesha each time
**Audience:** 🔴 **TALEEMABAD STAFF — INTERNAL. NOT CANDIDATES.**

---

## What This Type Is

A short internal email to Taleemabad staff announcing something new:

- an **internal job opening** we want our own people to see first
- a **new joiner** (name, role, team, start date)
- a **new programme, partner or initiative**
- an **org change** worth a broadcast

It is a broadcast, not a decision. It carries no verdict about any individual.

---

## 🔴 Why This Type Sits Apart From Types 1-6

Every other type in Skill 01 is written for someone **outside** the organisation, and the
harness rules exist to protect them. This one goes to colleagues. Applying the candidate rules
here would produce nonsense: an 800-word all-staff email opening "This is not a yes for now."
and refusing to name the person it is announcing.

**Rules that DO NOT apply to this type:**

| Rule | Why it is disapplied |
|---|---|
| 800-word minimum | This is a notice, not a feedback letter. Target **150-400 words**. |
| "This is not a yes for now." opening | No decision is being communicated to anyone. |
| Future-promise ban | Announcing next steps and dates is the entire purpose. |
| No-names ban (interviewers/staff) | Naming the joiner or the hiring contact is often the point. |
| Candidate-jargon ban | Internal readers are colleagues; ordinary internal vocabulary is fine. |
| Feedback widget | No feedback was given. Never attach it. |

**Rules that STILL apply, without exception:**

- **NO EM DASHES.** Use a period, comma, colon or hyphen. (Ayesha's drafts often contain them. Strip them.)
- **v8 layout imported from `scripts/utils/v8_template.py`** (Rule 8). Never redefine the card, header, footer or helpers inline.
- **Collective voice** — People and Culture Team, not one person's "I".
- **`safe_sendmail()` only**, with audit context.
- **Pilot to Ayesha first.** `[PILOT - ]` prefix on the pilot subject, clean subject live (Rule 4, Rule 7).
- **No fabricated facts.** Dates, deadlines, eligibility criteria and links come from Ayesha or a verified document. Never invent a distribution list or an alias we have not confirmed.
- **No "by Coco" sign-off line.**

---

## Structure (flexible, in this order)

1. **Greeting** — "Hi everyone," or as Ayesha words it
2. **The news** — one or two short paragraphs: what is new and why it matters
3. **Detail block** — `UL()` list of the hard facts (role, experience bar, employment type, contract end, start date, team)
4. **Eligibility / who this is for** — `UL()` list, when there are criteria
5. **What happens next** — the ask, the deadline, the process after that
6. **Encouraging close** — one or two lines
7. **v8 FOOTER**

Sections 3, 4 and 5 are optional. A new-joiner announcement uses 1, 2, 3, 6.

---

## Layout & Send Mechanics

- **Eyebrow:** `EYEBROW["announcement"]` → `PEOPLE & CULTURE • INTERNAL ANNOUNCEMENT`. The word *Internal* is deliberate: it is a visible tripwire if this ever lands in an external inbox by mistake.
- **Helpers:** `P` (justified body), `PL` (left-aligned short lines), `UL` (bulleted facts), `FOOTER`, `wrap`, `attach_logo`. `UL` and `PL` were added to `v8_template.py` for this type.
- **Script:** `scripts/send_internal_announcement_pilot.py` — `RECIPIENTS` list + `PILOT_MODE` flag.
- **⚠️ SCRIPT NAMING:** the send hook infers type from the filename. Keep `announcement` in the name and NEVER let it contain `warm_bench`, `gwc`, `values` or `rejection`, or it will be validated as an 800-word candidate feedback letter and HARD BLOCKED.
- **Recipients:** passed per send. There is no hard-coded all-staff list in this script by design.

---

## Self-QA Before Piloting (this type)

- [ ] Audience confirmed internal; no candidate address on the recipient list
- [ ] Every fact (dates, deadline, contract end, criteria, links) came from Ayesha or a verified doc
- [ ] Deadline is in the future and the day-of-week matches the date
- [ ] Any link opens and points where it claims to
- [ ] **No em dashes** (scan the rendered text, not just the source)
- [ ] v8 imported, not redefined; logo CID-embedded
- [ ] No feedback widget; no "by Coco" line
- [ ] `[PILOT - ]` on pilot only; pilot to Ayesha alone
- [ ] Word count 150-400

---

## Send Log

| Date | Announcement | Status |
|---|---|---|
| 2026-08-20 | Regional Manager (RM) internal opening, resumes by Fri 21 Aug 1:00 PM | Pilot sent to Ayesha |
