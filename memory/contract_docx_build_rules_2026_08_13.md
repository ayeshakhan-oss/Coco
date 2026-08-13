---
name: Contract Build & Send Rules (LOCKED 2026-08-13)
description: 14 rules governing every contract, NDA and addendum build and send. Structural checks are not visual proof. Applies to all entities and document types - only template and email content change.
type: feedback
---

# 🔒 Contract Build & Send Rules — LOCKED 2026-08-13

**Full SOP:** [.claude/sops/07_Contract_Documents/CONTRACT_DOCX_BUILD_SOP.md](../.claude/sops/07_Contract_Documents/CONTRACT_DOCX_BUILD_SOP.md)
**Skill:** [07_contract-drafting](../.claude/skills/07_contract-drafting/SKILL.md)
**Emails:** [joining-emails.md](../.claude/skills/07_contract-drafting/joining-emails.md)

**Origin:** the Muhammad Shayan Fellow package took **6 review rounds**. Content was right in
round 1; everything after was layout and process defects invisible to `python-docx`.

**These apply to ALL contracts, entities and document types. Only the template and the email
content change between cases.**

---

## 🔴 RULE 1 — Structural verification ≠ visual verification
No Word/LibreOffice here. Placeholder scans, diffs and property values check *structure*, never
*appearance*. **Never claim a formatting fix is done on structural evidence alone.** State the
limitation; ask Ayesha to eyeball it. Recurring defect after a "fix" = wrong diagnosis.

## RULE 2 — Diagnose in the XML, fix the cause
| Symptom | Cause | Fix |
|---|---|---|
| Narrow text column | heading `right_indent` ~5.3" | `right_indent = 0` on heading + clones |
| Stray lone bullet | empty para with `numPr` | `clear_trailing_orphan_bullet()`, never delete |
| One line per page | in-body `sectPr` = `NEW_PAGE` | `make_sections_continuous()` |
| Clone on its own page | `deepcopy` duplicated `sectPr` | `strip_section_break()` |
| Bold lost in PDF | bold inherited from style | `run.bold = True` |
| Heading at page foot | no `keep_with_next` | `apply_heading_formatting()` |

## RULE 3 — Clones carry baggage (numbering, section breaks, indents). Strip all three.
## RULE 4 — Masters copied, never modified. `output/` = PII, untracked.
## RULE 5 — Artefacts ≠ wording: `Mr./Mrs.` (ask, never infer) · `(joining date)` (delete, flag).
## RULE 6 — Never invent a field. Leave it visibly open and ask.
## RULE 7 — Capture paragraph objects BEFORE editing; deletions shift indices.

## RULE 8 — Package contents depend on the engagement
| Engagement | Documents |
|---|---|
| Paid fellowship / permanent | Contract **+** NDA |
| **Volunteer / unpaid** | **NDA ONLY — never a contract** |
| Unpaid → paid transition | **Contract only** (NDA already signed) |
| Addendum (same-team promotion) | Addendum only |

Ask paid vs volunteer before building. NDA = name + dates ONLY (CNIC = hard block).

## RULE 9 — Headings: explicit `run.bold` + `keep_with_next`, block capped ~10 paras.
🔴 **`keep_with_next` binds a paragraph ONLY to the immediately next one.** An empty spacer
between a heading and its content absorbs it and the content still breaks away — this is exactly
how "OFFER ACCEPTANCE:" was stranded at the foot of page 5. Set it on the **whole chain**,
spacers included, and run the block to the **next heading**, not to the first blank line
(a signing block's lines are separated by spacers).
🔴 **Verify placement in the PDF, and check ALL block content, not just the first paragraph** —
a first-paragraph-only check gave a false PASS on this defect.
`python scripts/evals/verify_pdf_layout.py "output/contracts/<Name>"`
Some headings are styled `normal` (short, fully bold, no full stop) — detect by shape.
Verify page placement in the PDF, not just the property.

## RULE 10 — Header labels `Date:` / `CNIC:` / `Name:` bold; values normal weight.

## RULE 11 — Candidate documents go out as PDF, never Word.
`scripts/utils/docx_to_pdf_drive.py`. Drive re-flows — verify text survived, then Ayesha eyeballs.

## RULE 12 — The pilot IS the email.
Byte-identical to what the candidate receives. **No pilot banner, flags or open questions inside
the email body** — those go in chat.

## RULE 13 — Match the thread you reply into.
Pull the original from Ayesha's Sent folder over IMAP; mirror formatting + signature verbatim.
Thread the pilot too. Check the original's CC list before live; confirm, never add silently.
Gmail "…" trimming on repeated wording → break with a zero-width space (`&#8203;`).

## RULE 14 — Nothing reaches a candidate without Ayesha's explicit approval. Pilot = Ayesha only, no CC.

## 🔒 RULE 16 — Design 3 is the standard for ALL contract-related emails (2026-08-14)
Chosen by Ayesha after a live bake-off against the plain and single-column variants.
**Template:** `templates/niete_joining_design3.html` · **Sender:** `scripts/contracts/send_niete_email_design3.py`
Variable-driven, so it serves any programme — **never hard-code candidate data**; rendering
fails loudly on an unresolved variable. **Design ≠ content:** wording still comes from the
locked content templates in `joining-emails.md`.

## 🔒 RULE 17 — Emails must be mobile-responsive (2026-08-14)
Never a fixed `width="NNN"` attribute or `width:NNNpx` on the outer table — it pins the layout
and phones zoom out; `max-width` never applies. Use `width="100%"` + `max-width` in CSS with an
`<!--[if mso]>` ghost table for Outlook. Multi-column must stack via **fluid-hybrid**, not by
media query alone (Gmail's app can strip `<style>`).
Check: `python scripts/evals/verify_email_responsive.py --script <send script>` — enforced by the send hook.

## RULE 15 — Email emphasis + dates 🔴 2026-08-13
**Never name the weekday** — `1st of August 2026`, not `Saturday, 1st of August 2026`. This
supersedes the day names in the original template text.
**Always bold what matters:** joining/effective date, compensation figure, duration, designation,
Taleemabad, Orenda, the document name, working hours, probation, and the crux of any caveat
("authentic and verifiable", "will not be covered"). If the candidate will scan for it or act on
it, bold it — err toward more, not less.
**Lists are lists:** a run of distinct items (terms, conditions, "things to know") is a
`<ul><li>` bulleted list, never stacked paragraphs.
**Onboarding form differs by programme:** Fellows form vs NIETE form — harness blocks a mismatch
in both directions.
Harness blocks a weekday name and an unbolded date or compensation figure.

---

## Code — never hand-roll docx edits

| Purpose | File |
|---|---|
| Shared mechanics | `scripts/contracts/contract_builder.py` |
| Reference build | `scripts/contracts/build_fellow_muhammad_shayan.py` |
| PDF conversion | `scripts/utils/docx_to_pdf_drive.py` |
| Validator | `scripts/evals/contract_docx_eval.py` |
| Send-time block | `scripts/hooks/pre_contract_send_hook.py` |
| Regression | `scripts/evals/test_contract_eval.py` |
