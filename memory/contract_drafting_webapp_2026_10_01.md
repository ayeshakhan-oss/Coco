---
name: Contract Drafting on Railway - name the person, not the fields
description: Skill 07 live as a page. Masters stored in the DB (never git), fill fields read from the master itself, 16 of 19 filled from Markaz + the offer thread, PDF via a drive.file scope. Plus the salary line nobody highlighted and the employer field that got the candidate's name.
metadata:
  type: project
---

# Contract Drafting on Railway (2026-10-01)

Ayesha: *"I would just want that I mention the name of the person and the job,
and then you sketch everything on your own."* This is how far that got.

Page `/contracts`, seventh module tile. `webapp/services/contracts.py` (routing
+ field discovery) · `contract_build.py` (fill + validate) ·
`contract_prefill.py` (what we already know) · `offer_evidence.py` (the offer
thread) · `joining_email.py` (the locked wording) · `pdf_convert.py` ·
`routers/contracts.py` · `ContractsPage.tsx`. Tables `coco.contract_masters`
and `coco.contract_builds` (alembic `0018`, applied and stamped).

---

## 🔴 THE SALARY LINE NOBODY HIGHLIGHTED

Filling every **yellow-highlighted** field in the NIETE project contract still
left **five placeholders printed in the document**: the acceptance-line joining
date, and **all four salary lines**. The compensation cell reads

> Total Earnings PKR **XYZ** · Base Salary: PKR **XYZ** · Medical: PKR **XYZ** · Others: PKR **XYZ**

and **only ONE of the four carries highlighting**. Worse, `contract_docx_eval`
reported them as WARNINGs and the wrapper returned `passed=True`, so a contract
reading *"Total Earnings PKR XYZ"* would have been offered for download.

**Fixes, all mechanical:**
- Unhighlighted placeholders are discovered as fields and filled. Occurrences
  already covered by highlighting are **subtracted**, so nothing is asked twice.
- A leftover placeholder is a **HARD BLOCK** in `contract_build.validate`,
  whatever the shared validator calls it, checked across **body, tables,
  headers and footers**.
- Proven against a deliberately broken build: blank the salary lines and it
  refuses with all four named.

🔑 **A field's label is read from its own LINE.** A payslip breakdown is four
figures on four consecutive lines; a lookback window that crossed a newline
read "Base Salary" from the line above and labelled the *Others* figure as base.

---

## 🔴 THE EMPLOYER FIELD GOT THE CANDIDATE'S NAME

The NIETE master has a field literally called **`EMPLOYER NAME DESIGNATION`**.
A plain `\bname\b` rule matched it as the employee's name and filled it with
the **candidate's** name, into the **signature block** where the signing
officer belongs. Found on the first run against the real master.

**The employer rule now runs BEFORE the name rule, and that field is left
blank** — the signatory is never guessed.

---

## What fills itself, and from where

**16 of 19** on the NIETE contract; **3 of 3** (everything) on the Permanent NDA.

| Source | Fields |
|---|---|
| `applications.contract_drafting_*` (the onboarding form the candidate fills in) | full **legal name**, **CNIC** |
| `jobs` | position, hiring manager |
| today | the contract date |
| the **offer letter thread** | compensation, start, end |
| arithmetic | the duration, from the term |

🔒 **THE LEGAL NAME BEATS THE STORED NAME.** Of the **17** who have submitted
the form, **EIGHT typed a different name**: Marzia Hasnain → Marzia Hasnain
**Khandwala**, Raheela → **Bibi** Raheela, Muzzamil Patel → **Muhammad
Muzzammil** Patel. The page says so when they differ. Rule 22 with a better
source than either the display name or the CV filename, because the person
typed it themselves for this purpose.

🔒 **THE SUBMISSION IS THE SIGNAL, NOT THE STATUS.** Hafiza's application still
reads `shortlisted` and she submitted a CNIC and was issued a contract. The
person list is *submitted the form OR offer/hired* (Rule 18).

🔒 **READING THE DOCUMENT IS NOT GUESSING.** Half these fields are written
`XYZ`, but the words before them say what they are: *"bearing CNIC No: X Y Z"*,
*"Total Earnings PKR XYZ"*. Fields carry the 60 characters before them. The
**TAIL** is matched, not the whole run-up: the term reads *"from \<A\> to
\<B\>"* with both fields written identically, and matching anywhere finds
"from" in both.

⚠️ **A money field gets the NUMBER only.** The master already prints "PKR", so
filling "PKR 108,000" yields *"Total Earnings PKR PKR 108,000"*.

---

## 🔴 READING THE OFFER THREAD: NEVER THE FIRST FIGURE

Rule 19 made mechanical. Messages ordered oldest-first, latest labelled figure
proposed, every disagreement reported. **Run against the real mailbox, which
found two gaps the unit tests did not:**

- **Mariam** — the only figure carrying the word "total" was the **first**
  offer at 116,000, while **118,000, 130,000 and 145,000** appear later without
  that word. The same-label check stayed silent. **Any pay figure differing
  from the proposal is now reported.**
- **Hafiza** — base **135,000** against total **108,000**. A part larger than
  the whole means one was read from the wrong place; **neither may be used
  unchecked.**
- **Zia** — one clean figure, **no warnings at all**. That is the other half:
  warnings only work if a clean thread stays quiet.

⚠️ **Offer emails do not say "offer".** The real subject is *"Congratulations
Mariam on Your Selection as a Coach for the NIETE Project!"*. **Search by
ADDRESS, never by subject.** HTML-only mail is stripped **keeping line breaks**,
because the breakdown is one figure per line.

⚠️ Amounts need a currency marker ("we reached 150,000 students" is not pay)
and are rejected near budget/grant/reimbursement/beneficiary words.

---

## PDF: a `drive.file` scope, not full Drive

Attachments are PDF and never Word (joining-emails rule 10, harness-blocked),
and Drive is the only converter on any machine here. The server already had
Ayesha's Google token for Gmail; it just had **no Drive permission**.

🔒 **`drive.file`, NOT `drive`.** It reaches only files the app itself creates:
upload the .docx, convert, export, **delete the temp copy in a `finally`** so a
mid-way failure leaves no filled contract (CNIC + salary) in Drive. The broad
`drive` scope on `token_sheets_broad.json` stays local.

🔴 **The setup script PRINTS the token for a human to paste, and I ran it, so a
live refresh token went into a session transcript.** Second time (see the
2026-06-30 reminder). It was set on Railway via argv without a shell and the
printed copy cleared, but **set it directly next time, never run the printing
script.**

⚠️ **Drive re-flows the document and ignores `keep_with_next`** — Rule 14 still
stands, a human must look at the page.

---

## Masters: in the database, never in git

`Contracts\` stays gitignored. All **8 masters** are uploaded once and stored as
bytes in `coco.contract_masters`, byte-for-byte verified on write. **A changed
field count on re-upload is reported as a re-issue.**

🔴 `coco.contract_builds` deliberately stores **no document and no field
values** — the values *are* the PII. It records who built what for whom and
whether the checks passed. The built file streams back with `no-store`.

---

## Still to build

- The **joining email body** (Design 3 render) and the **Pilot / Send buttons**.
  The rules exist and are tested; nothing is wired to a button yet.
- Three situations have **no approved wording** and are refused, not invented:
  Part-Time, Addendum/promotion, Internal team-move.
- The **entity** is not recorded anywhere in Markaz and stays a dropdown.

Related: [[joining_email_two_links_by_entity_2026_10_01]] ·
[[webapp_modules_live_on_railway_2026_09_25]] ·
[[contract_docx_defects_and_harness_2026_08_13]]
