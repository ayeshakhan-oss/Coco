---
name: Internal Announcement Email — Skill 01 Type 7 (2026-08-20)
description: New internal-audience email type added to Skill 01. Staff broadcasts (internal openings, new joiners, new programmes). Candidate rules disapplied; layout + no-em-dash + pilot rules still enforced.
type: project
---

# Internal Announcement Email — Skill 01, Type 7 (added 2026-08-20)

**Requested by Ayesha 2026-08-20.** She asked for an "announcement skill" inside candidate
communication. Clarified with her: the audience is **Taleemabad staff, internal** — not
candidates.

## The key design decision

It lives in Skill 01 (as she asked) but is explicitly declared an **internal type**. The
candidate harness rules exist to protect people outside the org, and applying them here
produces nonsense: an 800-word all-staff email opening "This is not a yes for now." that
refuses to name the person it is announcing.

**Disapplied:** 800-word minimum · "This is not a yes for now." · future-promise ban ·
no-names ban · candidate-jargon ban · feedback widget.
**Still enforced:** no em dashes · v8 imported from `v8_template.py` · collective voice ·
`safe_sendmail()` · pilot to Ayesha first · clean subject live · no fabricated facts.

Target length **150-400 words**. Content varies per send and is written or approved by
Ayesha; only the LAYOUT is locked.

## Files

- Type doc: `.claude/skills/01_candidate-communication/internal-announcement-email.md`
- Script: `scripts/send_internal_announcement_pilot.py`
- `scripts/utils/v8_template.py` — added `EYEBROW["announcement"]` plus two shared helpers,
  **`UL(items)`** (bulleted list) and **`PL(text)`** (left-aligned paragraph). A justified
  list or a justified one-line lead-in reads badly, and Rule 8 forbids redefining helpers
  inline, so they belong in the shared module.
- `scripts/hooks/pre_send_validation_hook.py` — added `announcement` type inference.
  **Non-obvious:** the hook returns early (`if not all([subject, email_type])`) when it
  cannot infer a type, which silently skips the `[PILOT]`-prefix-in-live guard too. Adding
  the inference is what turns that guard back on for this type.

## Traps

- Filename must keep `announcement` and must NEVER contain `warm_bench`, `gwc`, `values` or
  `rejection` — the hook infers type from the filename and would block a 226-word notice for
  failing the 800-word candidate rule.
- `RECIPIENTS` is deliberately **empty**; the script raises rather than send live. Ayesha
  supplies the staff list. Never guess an all-staff alias.
- The eyebrow reads `INTERNAL ANNOUNCEMENT` on purpose: a visible tripwire if it ever lands
  in an external inbox.

## First use — Regional Manager (RM) internal opening

Ayesha wrote the body copy herself. Used **verbatim except one em dash** ("Don't count
yourself out — take the shot!" → "Don't count yourself out. Take the shot."). 226 words.
**v2, same day (Ayesha):** self-assessment flow. The case study now ships WITH the
announcement instead of being sent after a resume screen, so the two-stage flow collapsed
into one deadline. Both links are buttons (JD solid, case study outlined). Eligibility
changed from "2 years of experience in **Education**" to "**Relationship Management**".
Deadline **Thursday 27 Aug 2026, 1:00 PM** = exactly 5 working days from Fri 21 (Ayesha's
own count, verified: 27 Aug 2026 IS a Thursday), preserving the original 5-working-day
case-study window. 243 words.

**LIVE 2026-08-20.** TO `all@niete.edu.pk`; CC ali.sipra@ + hiring@ + ayesha.khan@
(taleemabad.com) + bilal@ + asma.zaheer@ (niete.edu.pk). Clean subject "An Internal
Opportunity: Regional Manager". Ayesha wrote "bilal" with no domain and confirmed
`bilal@niete.edu.pk` when asked. **Never resolve a bare first name from the repo** — the
grep returned 11 different Bilal addresses, one of them a Job-42 candidate.

**Process lesson:** when a stage is removed from a hiring flow, the deadline attached to
the removed stage does not disappear with it. Fold it into the surviving deadline rather
than letting the earlier date stand. Pilot sent to Ayesha 2026-08-20; live list pending.
