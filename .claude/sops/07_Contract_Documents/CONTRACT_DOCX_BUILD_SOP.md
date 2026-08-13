# SOP: Building & Sending Contract Documents

**Category:** 07 — Contract Documents · **Skill:** [07_contract-drafting](../../skills/07_contract-drafting/SKILL.md)
**Locked:** 2026-08-13 · **Applies to:** every contract, NDA and addendum, all four entities, all
document types. **Only the template and email content change between cases — this process does not.**

---

## Why this SOP exists

The first Fellow package (Muhammad Shayan) took **six review rounds**. The content was right in
round one. Everything after that was layout and process defects I could not see, because
`python-docx` reads text and properties, not rendered pages, and there is no Word or LibreOffice
on this machine. Ayesha caught each one by screenshot.

Every rule below is one of those defects, now enforced in code.

---

# The 14 Rules

## 🔴 RULE 1 — Structural verification is NOT visual verification
Passing the validator means contents and properties are correct. It does **not** mean the page
looks right. Never claim a formatting fix is done on structural evidence alone; state the
limitation and ask Ayesha to eyeball it. If a layout defect recurs after a "fix", the diagnosis
was wrong — find the cause in the XML, don't tweak a value and re-send hopefully.

## RULE 2 — Diagnose in the XML, fix the cause
| Symptom | Cause | Fix |
|---|---|---|
| Narrow text column | heading `right_indent` ~5.3" | `right_indent = 0` on heading + clones |
| Stray lone bullet | empty paragraph with `numPr` | `clear_trailing_orphan_bullet()` — never delete |
| One line alone on a page | in-body `sectPr` = `NEW_PAGE` | `make_sections_continuous()` |
| Each new item on its own page | `deepcopy` duplicated `sectPr` | `strip_section_break()` on clones |
| Heading loses bold in PDF | bold inherited from style | set `run.bold = True` |
| Heading stranded at page foot | no `keep_with_next` | `apply_heading_formatting()` |

## RULE 3 — Clones carry baggage
`deepcopy` inherits numbering, section breaks and indents. Strip and reset all three, every time.
Use `add_bullet_after()`, which does it for you.

## RULE 4 — Masters are copied, never modified
Work in `output/contracts/<Full Name>/`. Populated documents hold CNIC and salary — **PII, never
committed**; `output/` stays untracked.

## RULE 5 — Template artefacts are not contract wording
`Mr./Mrs.` → the real salutation (**always ask, never infer from a name**). `(joining date)` →
delete after filling, and flag the removal.

## RULE 6 — Never invent a field
Entity, type, CNIC, name spelling, salutation, designation, dates, compensation, legal wording.
Missing or ambiguous → **leave it visibly open and ask**. A pilot with two flagged open fields is
correct; a guessed salary split is not.

## RULE 7 — Capture paragraph objects before editing
Deletions and insertions shift indices. Grab every target as an object first, edit, then delete.

## RULE 8 — Package contents depend on the engagement
| Engagement | Documents |
|---|---|
| Paid fellowship / permanent | Contract **+** NDA |
| **Volunteer / unpaid fellowship** | **NDA ONLY — never a contract** |
| Unpaid → paid transition | **Contract only** (NDA already signed) |
| Addendum (same-team promotion) | Addendum only |

**Confirm paid vs volunteer before building.** Never infer it from a role title. Fellow → Fellow
NDA; permanent → Permanent NDA; never swapped. An NDA takes name + joining date + current date and
**nothing else** — a CNIC in an NDA is a hard block.

## RULE 9 — Headings: explicit bold + keep_with_next (+ verify in the PDF)
Bold on the **run**, not the style. `keep_with_next` on every heading and its block, **capped at
~10 paragraphs** or a long section gets shunted wholesale to a new page. Some headings are styled
`normal` and are only visually headings — detect by shape (short, fully bold, no trailing full
stop). Then **verify page placement in the PDF**, not just the property.

⚠️ **`keep_with_next` binds a paragraph only to the immediately NEXT one.** An empty spacer
between a heading and its content absorbs it and the content still breaks away — that is how
"OFFER ACCEPTANCE:" was stranded at the foot of page 5. Set it across the **whole chain**
(spacers included) and run the block to the **next heading**, not to the first blank line.

⚠️ **Check ALL of a heading's content, not just its first paragraph** — a first-paragraph-only
check reported that same defect as PASS. Use:
`python scripts/evals/verify_pdf_layout.py "output/contracts/<Name>"`

## RULE 10 — Header labels Date: / CNIC: / Name: are bold; their values are not

## RULE 11 — Candidate documents go out as PDF, never Word
Convert with `scripts/utils/docx_to_pdf_drive.py`. The temporary Google Doc is deleted; the
attachment is a real `.pdf`. **Drive re-flows the document** — verify the text survived, then have
Ayesha eyeball it.

## RULE 12 — The pilot IS the email
A pilot must be **byte-identical to what the candidate receives** — same body, same formatting,
same thread. **Never** put a pilot banner, "nothing has gone to X", flags or open questions inside
the email body. Those go in chat.

## RULE 13 — Match the thread you are replying into
Pull the original from Ayesha's Sent folder over IMAP and mirror its exact formatting and
signature. Thread the pilot too (In-Reply-To + References) so she reviews it in context. Check the
original's **CC list** before going live and confirm recipients — never add them silently.
If a threaded reply repeats locked wording, Gmail collapses it behind a "…" expander; break the
match with a zero-width space (`&#8203;`) inside the repeated lines.

## RULE 14 — Nothing reaches a candidate without Ayesha's explicit approval
Pilot to Ayesha only, no CC. Approval for one send never carries to the next.

---

## Procedure

1. **Confirm entity → situation → contract type.** Never assume. Open the matching sub-skill.
2. **Confirm paid vs volunteer** and therefore which documents the package contains.
3. Collect every missing field. Ask for the JD. Ask for the salutation.
4. `open_master()` → work on the copy.
5. Extract the master's fill spots programmatically before editing.
6. Capture paragraph objects to delete/replace (Rule 7).
7. Fill run-level with `fill_paragraph()`; highlights clear automatically.
8. Apply the document type's clause rules.
9. JD under **Annexure-A inside the contract**.
10. `bold_header_labels()` → `apply_heading_formatting()` → `clear_trailing_orphan_bullet()`
    → `make_sections_continuous()` → deletions.
11. `to_pdf()`.
12. **Run the validator.** Fix every hard block.
13. Diff against the master — only fill fields, sanctioned clause changes and the JD may differ.
14. Verify in the PDF: page count, content present, headings with their content.
15. Pilot to Ayesha: what changed, what is open and why, and **that layout was not visually
    verified**.
16. Wait for approval. Then send.

---

## Code

| Purpose | File |
|---|---|
| Shared document mechanics | `scripts/contracts/contract_builder.py` |
| Reference build | `scripts/contracts/build_fellow_muhammad_shayan.py` |
| PDF conversion | `scripts/utils/docx_to_pdf_drive.py` |
| Validator (CLI) | `scripts/evals/contract_docx_eval.py` |
| Send-time block | `scripts/hooks/pre_contract_send_hook.py` |
| PDF layout verifier | `scripts/evals/verify_pdf_layout.py` |
| Harness regression | `scripts/evals/test_contract_eval.py` |

**Never hand-roll docx edits.** Use `contract_builder.py` — each helper exists because something
went wrong without it.

---

## Harness layers

| Layer | Component | Behaviour |
|---|---|---|
| Prompt-time | `prompt_submit_hook.py` | injects these rules on contract keywords |
| Build-time | `contract_docx_eval.py` | 13 rule families, exit 2 on violation |
| Send-time | `pre_contract_send_hook.py` | **blocks** a failing send |
| Regression | `test_contract_eval.py` | proves the validator still catches a raw master |

---

**Owner:** Coco · **Updated:** 2026-08-13
