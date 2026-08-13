# Sub-skill: Fellow (Internship) Contracts

Sub-skill of [Skill 07 — Contract Drafting](SKILL.md). Read the master workflow + [TEMPLATE_MAP.md](TEMPLATE_MAP.md) first. Mirrors `Contracts\Fellow\`.

---

## The Fellow rule (hard)

Interns are called **Fellows**. A Fellow/internship engagement gets:
1. The approved **Fellow Project-Based contract** — `Contracts\Fellow\Template - Project-based Employment Contract.docx` (OPL letterhead, intentional)
2. The **Fellow NDA** — `Contracts\Fellow\Template - NDA Fellow Employee.docx` ("Part Time - Fellowship")

**NEVER the Permanent Employee NDA for a Fellow. NEVER the Fellow NDA for a permanent employee.**

Entity is still confirmed per case (never assumed) — the engagement runs on this contract regardless, per Ayesha 2026-08-12.

## Contract — fill fields (yellow-highlighted)

Header: Current date, CNIC, Name · Effective date of joining · Mr./Mrs. NAME + CNIC (parties clause) · **Term: start DATE, MONTH, YEAR → end DATE, MONTH, YEAR** · duration XYZ · Employer signatory name + designation · Acceptance: NAME + CNIC · **Direct Report to: xyz**.
**Fixed (never touch):** unlimited trust-based leaves; lunch clause; 30-day termination notice; no-permanency clause.

## 🔒 Fellow clause deletions — MANDATORY (Ayesha 2026-08-13)

Fellows do NOT get these. **Delete all five from every Fellow contract** (paras 30–33 + 35 in the master):
1. "The company will cover any travel incurred for business purposes."
2. The technical-equipment / asset-damage / handover clause.
3. The In-patient (IPD) Medical Coverage clause.
4. "No travel or daily allowances will be furnished…"
5. The probationary 13 weeks / 3 months clause. ← **overrides the old "probation is fixed" rule for Fellows only**

Keep in-house lunch. **The 30-day notice and no-permanency clauses stay.**

## 🔒 Fellow leave terms — REPLACE the unlimited-leave clause (Ayesha 2026-08-13)

Delete "The Employee is entitled to Unlimited trust-based leaves." and put this in its place
(main clause as a list item, the two conditions nested under it as "o" sub-items):

> The fellow is entitled to annual leave of 3 working days for the course of the period accumulating on a monthly basis, and medical leave of 3 working days.
> - Medical Leaves can be availed for a maximum limit of 03 days it will be effective from the joining date, only for sickness or any other medical purposes.
> - Only unpaid leaves can be granted if the balance is exhausted.

## 🔒 Annexure-A layout — three separate defects, fix all three

1. **Heading right-indent ~5.3"** on "Job Description: Key Responsibilities:" collapses the JD into a narrow column. Set `right_indent = 0` on the heading AND every bullet (clones inherit it).
2. **Heading must break onto two lines** — "Job Description:" / "Key Responsibilities:".
3. **Trailing empty auto-numbered paragraph** (last para of the master) renders as a stray lone bullet. `strip_numbering()` it — do NOT delete it, it may carry section properties.

Sub-items must nest **deeper than the parent list indent** (~1.18"), not at a shallow fixed value.

## 🔒 The page-gap trap — section breaks (2026-08-13)

The master carries **six in-body section breaks, all `NEW_PAGE`**. They strand single lines on
otherwise blank pages. Every section has identical page setup, so set all but the last to
`WD_SECTION.CONTINUOUS` and the text flows normally.

⚠️ **Cloning hazard:** several master paragraphs carry a `sectPr` in their `pPr`. A `deepcopy`
duplicates it, so every cloned paragraph starts its own page. **Always `strip_section_break()`
on a clone** — alongside `strip_numbering()`.

## 🔒 Heading formatting (2026-08-13)

`apply_heading_formatting()` in `scripts/contracts/build_fellow_muhammad_shayan.py`:
- sets **`run.bold = True`** explicitly (style-inherited bold does not survive Drive's PDF conversion)
- sets **`keep_with_next`** on each heading + its block (all but the last paragraph), capped at ~10
  paragraphs so long sections are not shunted to a new page
- also catches `normal`-styled visual headings (short, fully bold, no trailing full stop)
- skips the master's stray one-word `AND` Heading-1 fragment

Then **verify in the PDF** that each heading and its first content paragraph share a page.

## ✅ Harness (added 2026-08-13)

- **Validator:** `scripts/evals/contract_docx_eval.py --dir "output/contracts/<Name>" --type fellow`
- **Blocking hook:** `scripts/hooks/pre_contract_send_hook.py` (PreToolUse/Bash, registered in `.claude/settings.json`) — blocks any contract send whose package fails the eval.
- Run the validator before every pilot. It encodes all 10 defect families from this session.

⚠️ **No Word or LibreOffice on this machine** — the validator checks document *structure*, not
rendered appearance. Structural checks passing is NOT proof the page looks right. Say so when
reporting, and ask Ayesha to eyeball layout changes.

**Compensation table:** Fellows get **Total Earnings only**. Delete the `Base Salary: PKR XYZ` / `Medical: PKR XYZ` / `Others: PKR XYZ` lines from the cell.

**Salutation:** replace the template's `Mr./Mrs.` with the actual salutation — it is a drafting option, not contract wording.

**Annexure-A formatting trap:** the master's "Job Description: Key Responsibilities:" paragraph carries a **~5.3" right indent** that collapses the JD into a narrow column. Reset `right_indent = 0` on that heading AND on every bullet (bullets cloned from it inherit the defect).

**Reference build:** `scripts/contracts/build_fellow_muhammad_shayan.py` — working run-level fill + deletion implementation.

## Fellow NDA — fill fields

FELLOW NAME (opening + printed name) · JOINING DATE · CURRENT DATE (employer signature). **Nothing else** — never add CNIC, designation, dates, or any field the template doesn't have.

## Required information (ask only what's missing)

Full legal name + salutation (always ask, never infer) · CNIC · fellowship role/designation · **START date AND END date + duration — both mandatory, double-checked** · Direct Report to · employer signatory · **JD (ask Ayesha every time)** → under **Annexure-A inside the same document**.

## Procedure

1. Confirm entity + Fellow engagement → copy both masters to `output/contracts/<Full Name>/`:
   - `Contract - <Full Name> - Fellow.docx`
   - `NDA - <Full Name> - Fellow.docx`
2. Fill ONLY yellow fields in each; clear highlighting on filled runs.
3. JD under Annexure-A in the contract.
4. Run BOTH validation checklists in [SKILL.md](SKILL.md) — explicit second pass on start/end dates.
5. Package = contract + Fellow NDA together, always.
6. Fellow/Project-Based joining email: ⏳ template pending — flag until shared.
7. Show Ayesha the complete package. No send without explicit approval.
