---
name: v8 Candidate Communication Layout - LOCKED
description: The single locked VISUAL LAYOUT for every candidate communication email (CV rejection, values feedback, warm bench, GWC rejection, and any future type). Shared module scripts/utils/v8_template.py is the source of truth.
metadata:
  type: reference
  locked: true
  updated: 2026-06-10
---

# v8 CANDIDATE COMMUNICATION LAYOUT — LOCKED (2026-06-10)

**STATUS:** 🔒 LOCKED by Ayesha 2026-06-10. She approved the Syeda Siddiqa Fatima
values feedback email and asked that its EXACT layout become the standard for ALL
candidate communication emails.

**APPLIES TO (Skill 01 — candidate communication):**
- CV screening rejections
- Values feedback emails
- Warm bench feedback emails
- GWC rejection emails
- **Any future candidate-communication email type we add**

**DOES NOT APPLY TO:** Interview invites (Skill 06) — they keep their own locked
design (#f3f4f6 / #2f4fa2 letter template). Reports, decision briefs, attendance.

---

## SOURCE OF TRUTH: ONE SHARED MODULE

**`scripts/utils/v8_template.py`** — import the layout; never redefine it inline.

```python
from scripts.utils.v8_template import H, SUB, P, PS, FOOTER, wrap, attach_logo, EYEBROW
from scripts.utils.feedback_widget import feedback_widget

body = (
    P("Dear <First Name>,") +
    P("<opening: decision + we'll be honest>") +
    H("<Section 1 heading for this type>") + P("...") +
    H("<Section 2 heading>") + SUB("We share what follows with care...") + P("...") +
    H("<Section 3 heading>") + P("...") +
    PS("<strong>P.S.</strong> ...") +
    FOOTER +
    feedback_widget(name, role, app_id, "Application Feedback")
)
html = wrap(subject_line=SUBJECT, role=ROLE, eyebrow=EYEBROW["values_feedback"], body_html=body)
```

In the `MIMEMultipart("related")` message, call `attach_logo(msg)` to embed the logo.

**Layout vs. content — keep them separate:**
- This module owns the **layout** (font, colors, card, spacing, header, footer, P.S. box).
- It does **NOT** own **section headings or content** — those differ per email type and
  are enforced by the eval harness (scripts/evals/candidate_communication_eval.py).
- Tone/content rules live in [CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md](CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md).

---

## THE LOCKED SPEC (exact values)

**Canvas / card**
- Page background: `#f0f4f0` (soft grey-green behind the card)
- Card: centered, `width=620px` (`max-width:620px`), `border-radius:8px`,
  `box-shadow:0 2px 12px rgba(0,0,0,0.08)`
- Card body padding: `40px 52px 48px 52px`

**Typography**
- Font: `Georgia, serif` everywhere
- Body: `15px`, `line-height:1.8`, color `#1a1a1a`, `text-align:justify`

**Color system**
| Element | Color |
|---|---|
| Primary blue (headings, title, links, header divider) | `#1565c0` |
| Green (SUB subheading + P.S. left border) | `#1b5e20` |
| Body text | `#1a1a1a` |
| Role subtitle | `#5c85c7` |
| P.S. box background | `#f1f8e9` |
| Footer text | `#555` / muted `#aaa` |

**Header block**
- White bg, `2px solid #1565c0` bottom divider
- Embedded logo `cid:taleemabad_logo`, `height:38`, centered (`margin:0 auto`)
- Eyebrow: `11px`, uppercase, `letter-spacing:2px`, blue — from `EYEBROW[type]`.
  Candidate-facing: NO internal jargon (never "GWC"/"KCD"/"scorecard"). Use
  "Application Update" for cv/warm-bench/gwc; "Values Interview" for values feedback.
- Title (subject line): `17px`, bold, blue
- Role subtitle: `12px`, `#5c85c7`

**Body helpers**
- `H(t)`  — section heading: blue `#1565c0`, `17px`, bold, `margin:36px 0 6px 0`
- `SUB(t)`— green `#1b5e20`, bold, `14px`
- `P(t)`  — `15px` Georgia, `line-height:1.8`, justified, `margin:0 0 18px 0`
- `PS(t)` — pale-green box `#f1f8e9`, `4px` green left border, italic, `padding:20px 24px`

**Footer**
- `1px solid #e0e0e0` top border; "Warm regards, People and Culture Team, Taleemabad";
  blue mailto/website links; muted "Sent on behalf of Talent Acquisition Team by Coco."

**Email assembly**
- `MIMEMultipart("related")` → inner `MIMEMultipart("alternative")` with the HTML →
  `attach_logo(msg)` → `safe_sendmail(...)`. Table-based layout only (Gmail-safe).

---

## WHY (so it never drifts)

- One module = no copy-paste divergence between email types.
- Georgia + justified + 1.8 line-height = the warm, letter-like tone the
  communication philosophy requires.
- Embedded `cid:` logo (not a hosted URL) = reliable render in Gmail/Outlook/corporate.
- 620px card + shadow = personal, not a marketing blast.

**Reference implementation:** `scripts/send_cpd_coach_values_feedback_syeda_2026_06_10_pilot.py`
(the email Ayesha approved). Verified byte-identical to the original inline build.

**Gold-standard content example (values feedback):**
`scripts/jobs/job36/send_job36_values_feedback_junaid_jawad_formatted.py`

---

## HARNESS (Layer 1 draft-time templates) — also v8 (2026-06-10)

The 4 locked HTML templates the harness injects at draft time
(`templates/{cv_rejection,values_feedback,warm_bench,gwc_rejection}_template_locked.html`,
injected by `scripts/memory/prompt_submit_hook.py`) are now generated from the v8
module, so what gets injected at draft time == what gets sent.

- **Regenerate after any v8 change:** `python scripts/utils/gen_locked_templates.py`
- Layout is 100% v8; only `[PLACEHOLDERS]` change per email.
- Section headings differ per type (enforced by `scripts/evals/candidate_communication_eval.py`):
  - values_feedback: What We Liked Most About You / Where We Found Ourselves Sitting With Questions / What We Think You Should Do Next
  - warm_bench + gwc_rejection: What Stayed With Us / Here's the Honest Part / Where We Want to Leave This
  - cv_rejection: What we appreciated / Where we found questions / What we think you should do next
