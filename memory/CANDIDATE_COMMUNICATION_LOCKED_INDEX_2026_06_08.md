---
name: Candidate Communication — Locked Index (2026-06-08)
description: Single source of truth for all candidate feedback/rejection email approaches. Points to correct locked versions ONLY. Supersedes all prior versions. Use this index before any candidate email task.
type: reference
metadata:
  status: PRODUCTION LOCKED
  updatedDate: 2026-06-08
---

# Candidate Communication — Master Locked Index (2026-06-08)

**Status:** 🔒 LOCKED — This is the ONLY index you need. All other versions are superseded.

---

## For GWC Rejection Emails (CURRENT)

**Use:** `memory/gwc_rejection_locked_approach_2026_06_08.md`

**What:** Complete locked approach using warm bench structure (opening, 3 sections, P.S.).

**Key requirements:**
- Opening: "This is not a yes for now"
- Sections: "What Stayed With Us" → "Here's the Honest Part" → "Where We Want to Leave This"
- P.S. with premium styling (see below)
- Haroon Yasin balance rule
- Frame as "circumstances mismatch" not "commitment judgment"
- Template: `templates/warm_bench_email.html`
- Colors: #1565C0, #f3f4f6, #555
- 800+ words MANDATORY

**Execution:**
1. Load gwc_rejection_locked_approach_2026_06_08.md
2. Follow 11-item checklist
3. No back-and-forth needed

---

## For Warm Bench Emails (CURRENT)

**Use:** `memory/warm_bench_locked_rules_2026_05_30.md` + `memory/warm_bench_locked_final_2026_05_30.md`

**What:** 13 locked rules for warm bench emails (candidates cleared values + GWC, not selected for current role).

**Key requirements:**
- Opening: "This is not a yes for now"
- Sections: "What Stayed With Us" → "Here's the Honest Part" → "Where We Want to Leave This"
- No interviewer names
- No internal jargon (GWC, values, scorecard)
- Poetic subject line (tied to specific interview moment)
- P.S. with premium styling (see below)
- 800-1100 words MANDATORY
- Template: `templates/warm_bench_email.html`

**Reference case:** Fatima Saeed email (May 15, 2026)

---

## For P.S. Section Styling (ALL EMAILS — CURRENT)

**Use:** `memory/ps_section_styling_locked_2026_06_08.md`

**What:** Premium personal styling for postscript sections. Applies to warm bench, GWC, values feedback, screening rejections, ALL candidate communication emails.

**Key specifications:**
- Font size: 15px (90-95% of body)
- Color: #555 (dark gray, not black)
- Style: ITALIC (critical)
- Bold "P.S." label
- Top margin: 30px (generous whitespace)
- Line height: 1.8 (breathable)
- No borders, colors, callout boxes
- Goal: Feel like handwritten note added after formal email

**Template implementation:**
- `templates/warm_bench_email.html` has separate P.S. section with `{ps_content}` placeholder
- P.S. appears AFTER body content, BEFORE signature
- Signature is separate table row

---

## For Values Feedback Emails

**Use:** `.claude/skills/01_candidate-communication/` + `memory/rule_all_feedback_emails_use_locked_tone.md`

**What:** Rejection feedback for values interview failures. 800-1100 words mandatory.

**Key requirements:**
- Same P.S. styling as above
- Three sections: "What We Liked Most" → "Where We Found Questions" → "What You Should Do Next"
- Pilot to Ayesha + Jawad ONLY
- v8 HTML design (blue headings, Georgia serif, justified)
- Feedback widget required

---

## For All Candidate Communication Emails (UNIVERSAL RULES)

**Use:** `memory/warm_bench_locked_rules_2026_05_30.md` + `memory/lesson_no_intent_inference_rejection_emails_2026_06_01.md` + `memory/candidate_communication_avoid_recruiting_abstractions_2026_05_30.md`

**Key rules:**
1. **No intent inference** — Never say "you assumed/believed/thought/preferred". Use observations + questions.
2. **No recruiting abstractions** — Never "good candidate", "strong profile". Describe observed behaviors.
3. **Haroon Yasin balance** — Praise specificity ≈ decision specificity.
4. **Observable behaviors only** — Cite specific moments, not impressions.
5. **"We" voice** — Never "I".
6. **No em dashes** — Replace with periods, commas, colons.
7. **No jargon** — No "GWC", "values", "scorecard", interviewer names.
8. **800+ words MANDATORY** — For all feedback emails.
9. **P.S. styling** — Premium personal style (see P.S. section above).
10. **Pilot to Ayesha first** — Never direct to candidate. Wait for approval.

---

## Template Reference

**Single template for warm bench + GWC rejections:**
- File: `templates/warm_bench_email.html`
- Placeholders: `{candidate_name}`, `{position}`, `{body_content}`, `{ps_content}`
- Design locked: Colors #1565C0, #f3f4f6, #555, #5B8DBE, #7986CB
- Structure: Logo → Header → Title → Subtitle → Divider → Body → P.S. → Signature
- Font: Georgia serif, justified, 70px padding, 620px width
- Logo: cid:logo_taleemabad (embedded, 48x48px)
- HTML entities: `&amp;`, `&bull;` (never raw UTF-8)

---

## What NOT to Use (SUPERSEDED VERSIONS)

**Do NOT use:**
- ❌ `memory/gwc_rejection_update_2026_05_30.md` — OLD, superseded
- ❌ `memory/skill_warm_bench_feedback_locked.md` — OLD, superseded
- ❌ `memory/skill_warm_bench_feedback_updated.md` — OLD, superseded
- ❌ `memory/warm_bench_final_locked_approach.md` (in root) — OLD, superseded
- ❌ `memory/session_warm_bench_template_lock_2026_04_27.md` — OLD, session notes only
- ❌ `memory/_locked/warm_bench_final_locked_approach.md` — OLD, superseded
- ❌ Hackathon GWC files (session-specific, not generalizable)

**Use instead:**
- ✅ `gwc_rejection_locked_approach_2026_06_08.md` (NEW)
- ✅ `warm_bench_locked_rules_2026_05_30.md` (CURRENT)
- ✅ `ps_section_styling_locked_2026_06_08.md` (NEW)

---

## Execution Workflow

**When asked to send candidate feedback/rejection email:**

1. **Identify email type:** GWC rejection? Warm bench? Values feedback? Screening rejection?
2. **Load correct file:**
   - GWC rejection → `gwc_rejection_locked_approach_2026_06_08.md`
   - Warm bench → `warm_bench_locked_rules_2026_05_30.md`
   - Values feedback → Skills folder + tone guide
3. **Check P.S. styling:** `ps_section_styling_locked_2026_06_08.md` (applies to ALL)
4. **Check universal rules:** Intent inference, abstractions, Haroon Yasin, em dashes, jargon
5. **Use template:** `templates/warm_bench_email.html` with locked placeholders
6. **Run checklist:** 11-item checklist (GWC) or equivalent for other types
7. **Pilot to Ayesha only** → Approval → Live send

---

## Potential Confusion Points (CLARIFIED)

**Q: Should I use warm bench structure for GWC rejections?**
A: YES. GWC rejections use warm bench structure (opening "This is not a yes for now", 3 sections, P.S.). See gwc_rejection_locked_approach_2026_06_08.md.

**Q: Where does P.S. go?**
A: AFTER body content, BEFORE signature. 30px top margin. See ps_section_styling_locked_2026_06_08.md.

**Q: What's the template file?**
A: `templates/warm_bench_email.html` (single template for warm bench + GWC). Has placeholders: `{candidate_name}`, `{position}`, `{body_content}`, `{ps_content}`.

**Q: What colors should I use?**
A: #1565C0 (dark blue headings), #f3f4f6 (background), #555 (P.S. text), #5B8DBE (label), #7986CB (subtitle). See template.

**Q: HTML entities—what do I use?**
A: `&amp;` for & and `&bull;` for •. Never raw UTF-8 characters.

**Q: How long should emails be?**
A: 800+ words MANDATORY. Count before sending.

**Q: Should I mention interviewer names?**
A: NO. Use "your interview" or "when we asked you about..." instead.

**Q: Can I use em dashes?**
A: NO. Replace " — " with periods, commas, or colons.

**Q: Should P.S. be in a box or colored?**
A: NO. Pure text, italic, #555 color, no borders or styling. Premium simplicity.

---

## Reference Case (FINAL VERSION)

**Hira Abbasi email (2026-06-08):**
- GWC rejection using warm bench structure
- Locked approach + locked template + locked P.S. styling
- Final version approved by Ayesha
- Available at: `scripts/send_hira_abbasi_gwc_rejection_v3.py`

---

## Status

✅ **LOCKED (2026-06-08)** — Final, production-ready.

All candidate communication emails should follow this index.

No more confusion. No more back-and-forth.

---

**Created:** 2026-06-08  
**By:** Coco (Ayesha's final feedback integrated)  
**Approved by:** Ayesha Khan
