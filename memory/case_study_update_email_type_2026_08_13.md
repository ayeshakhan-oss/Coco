---
name: Case Study Update — Debrief-Pending Email (Skill 01 type #6, 2026-08-13)
description: New sub-skill of candidate communication for candidates who SUBMITTED a case study and are waiting on a debrief decision. Sibling of Warm Hold type #5; inherits its exemptions (no "not a yes for now" opening, dated promise required, 120-250 words) plus a NEW scoped exemption allowing "case study" as candidate-facing language. Script must never be renamed into a harness-recognised feedback pattern.
type: project
---

# Case Study Update — Debrief-Pending Email (Skill 01, type #6)

**Created 2026-08-13 at Ayesha's request** ("we will use our warm hold decision skill but it will need a slight change or you can make a case study update email skill as a sub skill of candidate communication"). Built as a **separate sub-skill** rather than bending Warm Hold, so each type keeps its own trigger, subject and audit trail.

**Skill file:** `.claude/skills/01_candidate-communication/case-study-update-email.md`
**Script:** `scripts/send_case_study_update_pilot.py`
**Eyebrow key added:** `EYEBROW["case_study_update"]` in `scripts/utils/v8_template.py` → "PEOPLE & CULTURE • INTERVIEW UPDATE"

## What it is
Short status note to a candidate who **already submitted their case study**: thanks for the work, we are still mid-interviews so nothing is decided, and we expect to update you **on the case study debrief interview call by [timeline]** (Ayesha's exact wording 2026-08-13 — say "case study debrief interview call", never just "debrief"). No verdict, no evaluation, no direction hints, no new asks.

## Inherited exemptions (from type #5, Ayesha-sanctioned)
1. NO "This is not a yes for now." opening (no decision exists).
2. Future-promise ban inverted — the dated commitment is the point. Guardrail: if the date will slip, send a fresh note BEFORE it passes.
3. 800-word minimum does not apply — target **120-250 words** (first send: 131).

## 🆕 NEW scoped exemption
**"case study" is permitted candidate-facing language for THIS TYPE ONLY.** The harness lists `case study` as internal jargon; that ban protects candidates from shorthand they were never told. Here it is the candidate's own deliverable, which we personally sent them and which Ayesha names verbatim when she explains the three hiring stages on the values call. Does NOT loosen the jargon ban anywhere else.

## ⚠️ NON-OBVIOUS: script naming can trigger a false HARD BLOCK
`scripts/hooks/pre_send_validation_hook.py` infers email type from the **filename**. Any script containing `warm_bench`, `gwc`, `values`, or `rejection` is validated as an 800-word feedback letter and would HARD BLOCK this 131-word note for word count + missing opening line. Keep the name `send_case_study_update_pilot.py`.

## First use — Job 42 Senior Manager Growth, 2026-08-13
Subject `A Quick Update from Our Side` (sibling of type #5's `A Quick Note from Our Side`, deliberately different so a candidate receiving both does not see the same subject twice). Timeline: **"early next week"** per Ayesha.
4 pilots sent to Ayesha only (no CC) for the 4 dual-source-verified case-study submitters: **Muhammad Arshan Bilal** (app 3884), **Junaid Ali** (3992), **Arooj Khalid** (3868), **Yusra Amjad** (4061). **Awaiting Ayesha's approval before live send** (live = candidate TO + CC ayesha + hiring@, clean subject).

**Open flag raised with Ayesha:** Junaid Ali and Yusra Amjad hold only **blank values scorecard shells** — they submitted case studies with no values evidence on record. See [[audit_job42_smg_scorecards_vs_case_studies_2026_08_13]].
**Diary:** promised update is "early next week" (Mon 18 / Tue 19 Aug) — a follow-up must go out before that passes if the debrief decision slips.

## Related
[[warm_hold_decision_pending_email_type_2026_08_12]] (parent pattern) · case-study submission nudge (sent-but-not-submitted, Skill 06 family): repo memory/case_study_nudge_type_2026_08_10.md · [[CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED]]
