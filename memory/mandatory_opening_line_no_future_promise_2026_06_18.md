---
name: Mandatory Opening Line + No Future-Promise — LOCKED
description: All 4 candidate-communication emails open with "This is not a yes for now." (HARD BLOCK). No future-outreach promises (WARNING). Locked 2026-06-18.
metadata:
  type: reference
  locked: true
  updated: 2026-06-18
---

# Mandatory Opening Line + No Future-Promise — LOCKED (2026-06-18)

**STATUS:** ✅ LOCKED. Wired into the harness, the 4 locked templates, CLAUDE.md (Rule 10), the master tone philosophy (Rules 10-11), SKILL.md, RULES.md, and the webapp output contract.

**Set by:** Jawwad (2026-06-18).

---

## RULE 10 — MANDATORY OPENING LINE

Every candidate communication email — **CV rejection, values feedback, warm bench, GWC rejection**, and any future type — MUST open with this exact line as the **first line right after `Dear [Name],`**, before the type-specific opening paragraph:

> **This is not a yes for now.**

**Why it is honest (not over-promising):** the word "now" does the work. It says "today, this is a no", not "you can never". That is true for every candidate. A CV-stage applicant can strengthen their CV and reapply. A values candidate can grow over six months to a year. The line never promises anything on its own.

**Harness:** 🔴 HARD BLOCK — `check_opening_line()` in `scripts/evals/candidate_communication_eval.py`. Fails if the phrase is missing OR appears buried after a section heading instead of right after the salutation.

---

## RULE 11 — NO FUTURE-PROMISE

Candidate emails express genuine welcome but **never commit us to a future action the candidate could later hold us to.**

Internally we DO revisit warm-bench candidates. That truth stays internal. The email makes them feel specifically seen and welcome — without writing a commitment they could question later ("you said you'd keep my name / reach out, why didn't you?").

**Mechanics:**
- **Disposition, not commitment** — how we feel ("we would welcome the conversation again"), not what we will do.
- **Candidate-initiated, not company-initiated** — put the next move in their hands ("if a closer-fit role opens, we would welcome a fresh application from you"), never "we will contact you".
- **Warmth lives in the specific praise + the P.S.**, not in future-action language.

**✅ Safe:** "we'd welcome talking again", "we'd be glad if you came back to us", "we hope you'll come back", "you're the kind of person we hope stays in our orbit", "stay connected".

**❌ Forbidden:** "we will reach out", "we'll be in touch", "we will contact you", "we will keep your name with us / on file", "expect to hear from us", "you'll hear from us", "we'll let you know when".

**Harness:** 🟡 WARNING — `check_future_promise()` (flags, does not block, so legitimate warm closings are not killed).

---

## CANONICAL CLOSE (copy this pattern)

> "We would genuinely like to stay connected. If a role opens that fits where your strengths sit, we would welcome the conversation again, and we would be glad if you came back to us. This is not a polite closing line. We mean it."

---

## AUDIT (2026-06-18)

No current email made a hard outreach promise. The dominant pattern was already safe ("if an opportunity aligns... we'd welcome talking again"). Retired the soft-retention phrase **"we will keep your name with us"** (and "keep in view") from `send_bilal_ahmed_warm_bench_pilot.py` and the dummy comms. Older JRA scripts predate the harness and were left as-is.

## RELATED

- Master philosophy: [[CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED]] (Rules 10-11)
- Layout: [[v8_candidate_comms_layout_LOCKED]]
- Harness: `scripts/evals/candidate_communication_eval.py` · Templates: `scripts/utils/gen_locked_templates.py`
