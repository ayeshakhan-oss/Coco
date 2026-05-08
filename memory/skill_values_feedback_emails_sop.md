---
name: Skill SOP: Values Feedback Emails (2026-04-10 Update)
description: Rejection feedback emails for candidates who fail values interview. 800-1100 words mandatory. v8 design. Pilot to Ayesha + Jawad only, never candidate.
type: feedback
---

## Overview
Write personalized rejection feedback emails for candidates who failed values interview. Evidence-based, emotionally careful, specific to their interview.

## Word Count (CRITICAL)

- **Minimum: 800 words** — Mandatory, cannot be lower
- **Target: 800–1100 words** — Optimal range
- Count words before sending

## Structure (3 Required Sections)

1. **What We Liked Most About You** — 2–3 specific strengths from their values interview
2. **Where We Found Ourselves Sitting With Questions** — 2–3 values gaps, evidence-based from interview
3. **What We Think You Should Do Next** — Actionable advice tied to gaps

Plus: Opening, P.S. box, footer

## Non-Negotiable Rules

1. **800-word minimum** — Count. No exceptions.
2. **Specific interview evidence** — Every observation cited from their actual interview.
3. **No em dashes** — Replace " — " with period/comma/colon.
4. **"We" voice** — Never "I".
5. **They/them pronouns** — Gender-neutral always.
6. **v8 HTML design** — Blue headings, green subheadings, Georgia serif, justified.
7. **Feedback widget required** — Include at end of body.
8. **Pilot to Ayesha + Jawad ONLY** — Never candidate. PILOT_MODE = True.
9. **Approval before live** — Pilot first, approval, then live.
10. **Safe_sendmail bouncer** — Never smtplib directly.

## Pilot Rule (CRITICAL)

When Ayesha says "pilot this":

**Send ONLY to:**
- ayesha.khan@taleemabad.com
- jawwad.ali@taleemabad.com

**NEVER include:**
- Candidate email
- Hiring manager
- hiring@
- Any other recipient

**After approval:** Switch PILOT_MODE = False, go live to candidate (TO) + hiring@ + ayesha@ (CC)

## Reference

**Full SOP:** skills/values-feedback-emails.md
**Detailed rules:** memory/feedback_email_rules.md
**Implementation:** scripts/jobs/job36/send_job36_values_feedback_junaid_jawad_formatted.py

Commitment: 800+ words, specific evidence, v8 design, pilot to Ayesha+Jawad only, approval before live, safe_sendmail bouncer, feedback widget included.
