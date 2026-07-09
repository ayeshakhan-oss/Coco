---
name: CV Rejection = Written Application Only (LOCKED 2026-07-09)
description: A CV/application-stage rejection had NO interview/call/conversation. Never fabricate one. Ground everything in the written application. Also Rule 12 collective "we" voice. Harness-enforced.
type: feedback
---

# CV Rejection: No Fabricated Interview / Conversation (LOCKED 2026-07-09)

**Mistake (found by Ayesha 2026-07-09):** CV-rejection drafts referenced a
conversation/interview that never happened — e.g. "we reviewed your background
across multiple **conversations and assessments**", "an honest reflection on
what **we observed**". A CV rejection is for a candidate screened out at the
**application stage**: there was NO interview, call, conversation, meeting, or
assessment. The tone framework (Haroon) was built for *post-interview*
rejections, so `cv_rejection` inherited interview language and the model invented
an interaction.

**Correction / Rule 13 (LOCKED):** For `cv_rejection`, ground EVERYTHING in the
written application only — "your application", "your CV", "the experience you
described", "your materials". NEVER reference or imply an interaction:
- Forbidden: "conversation(s)", "we spoke", "spoke with", "we met", "met with
  you", "our discussion", "we discussed", "our meeting", "our call", "our time
  together", "across conversations and assessments", "what we observed [in you]".
- Allowed: referencing the interview **stage they did not reach** ("we've decided
  not to move you forward to the interview stage") — a stage, not a conversation.
- Warm bench / GWC / values feedback DID have an interview and MAY reference it —
  this rule is `cv_rejection`-only.

**Also locked same day — Rule 12 (collective "we" voice):** candidate emails
speak as Taleemabad ("we"/"our"/"us"), never "I"/"my"/"me". A decision is the
organisation's, not one person's.

**Enforcement (so it can't recur):**
- **Harness HARD BLOCK** — `check_cv_no_interaction()` (cv_rejection only) +
  `check_first_person_singular()` in `scripts/evals/candidate_communication_eval.py`.
  Because they're hard blocks, the drafting self-correction loop auto-rewrites a
  slip before the user ever sees it.
- **Drafting prompt** — `webapp/prompts/tone_rules.py`: a CV-stage note ("no
  interaction ever happened, ground in the written application") is appended for
  `cv_rejection`, and a prominent "we-voice only" hard rule for all types.
- **Master philosophy** — Rules 12 + 13 added to
  [[CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED]] (single source of truth) +
  CLAUDE.md core rules 11 + 12. Commit `fb5c672`.
