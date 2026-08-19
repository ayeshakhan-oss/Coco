# NIETE CPD Coach Contracts — 19 August 2026 Batch

**Skill:** [07_contract-drafting](../.claude/skills/07_contract-drafting/SKILL.md) ·
**Build rules:** [contract_docx_build_rules_2026_08_13.md](contract_docx_build_rules_2026_08_13.md) ·
**Email:** Template 4 content + Design 3 layout

---

## 🔒 RULE — two clauses REMOVED from EVERY NIETE contract (Ayesha 2026-08-19)

- ~~"In-house Lunch will be provided, or an allowance in lieu."~~
- ~~"The company will cover any travel incurred for business purposes."~~

Standing instruction for **any** NIETE contract, not a per-candidate tweak. Implemented in
`scripts/contracts/build_niete_cpd_coaches.py` as `P_DROP_CLAUSES` (master paragraph indices
29 and 30).

**Mechanics that matter (repeat these if another clause is ever removed):**

1. The clauses sit **ahead of every fill index** (`P_LEAVES=34`, `P_TERMINATION_LAST=69`,
   `p[87]`, `p[91]`, `p[95]`, `P_ANNEXURE_JD=97`). Capture the paragraphs as **objects up
   front**, delete them only **after** all index-based fills — deleting first shifts every
   later index (Build Rule 7).
2. Confirm the target paragraph carries **no `sectPr`** before deleting, or pagination breaks
   (Build Rule 2). Both of these are plain bullets — safe.
3. Deletion is guarded by an **assertion on the master's exact wording**: if the master ever
   changes, the build fails loudly instead of silently deleting the wrong paragraph.
4. The **master is never modified** — removal happens at build time on the copy.
5. Verify the removal in the **PDF**, not just the .docx — the PDF is what gets attached.
   Normalise whitespace when grepping extracted PDF text; `pypdf` inserts stray spaces and
   naive substring checks report false misses.

**Retained neighbours — do not remove by accident:** technical-equipment/asset-damage, IPD
medical coverage, no-travel-or-daily-allowances, probation 13 weeks, the hyperlinked "Leaves"
clause, authenticity clause.

⚠️ **Hina Fatima Jafri and Noor Ul Ain Rana** received their contracts on 13 Aug 2026, *before*
this change, and still have both clauses. Not reissued as of 2026-08-19.

---

## The batch

CNICs are deliberately **not** recorded here — this file is tracked in git. Pull them from
Markaz `applications.contract_drafting_cnic_number` for the app ID listed.

| Candidate | Markaz | Term | Gross monthly | Reports to | Status |
|---|---|---|---|---|---|
| Syeda Mariam Abbas Naqvi | app 3843 / cand 19 | 24 Aug → 31 Dec 2026 | PKR 116,000 | Abdul Waheed | ✅ LIVE |
| Naima Javed | app 3857 / cand 3122 | 26 Aug → 31 Dec 2026 | PKR 127,000 | Anam Masood | ✅ LIVE |
| Hafiza Iqra Bashir | app 3873 / cand 1698 | 1 Sep → 31 Dec 2026 | PKR 108,000 | Abdul Waheed | pilot sent |

All three: `Ms.` · NIETE project-based master · Contract **+** Permanent Employee NDA · PDFs ·
signatory Ali Sipra, COO · designation `CPD - Coach` · compensation split **90% base / 9%
medical / 1% other** of gross (the ratio set by the 13 Aug batch).

Build scripts: `scripts/contracts/build_niete_cpd_{mariam_naqvi,naima_javed,hafiza_iqra}.py` —
each overrides `base.CURRENT_DATE/START/END/DURATION` then delegates to
`build_niete_cpd_coaches.build_contract` / `build_nda`, so the shared clause rules apply
automatically.

⚠️ **All three were still `shortlisted` in Markaz after their contracts went out** — status
updates pending Ayesha's go-ahead.

---

## 🔴 The salary number is the NEGOTIATED number, never the first offer

Every one of these three had a compensation conversation after the Markaz offer letter. Read the
**whole thread to the end** before taking a figure:

- **Mariam** — offered 116,000, countered at 130,000, Ayesha held, she accepted 18 Aug.
- **Hafiza** — offered 108,000, countered at 135,000–140,000, Ayesha held on internal
  equity/compensation-matrix grounds, she accepted "the offer as shared" 19 Aug.
- **Naima** — offered 127,000, **no counter**; her acceptance is *implicit* — she submitted her
  CNIC through the Markaz contract-drafting form the next day, which is exactly what the offer
  letter asked for. There is no "I accept" email. Say so rather than implying a written yes.

---

## Returning vs external hires

The Template 4 returning-member sentence is **conditional** — always confirm, never infer from
the role.

- **Mariam = returning** (previously CPD Coach in Quetta; experience letter issued 17 Mar 2026;
  her own word was "rejoining"). Sentence **included**.
- **Naima = external** (ran a private school in E11).
- **Hafiza = external** (Teach For Pakistan). ⚠️ Her earlier Markaz record (app 2124, Field
  Coordinator) is an **application, not an engagement** — a prior application never makes
  someone a returning team member.

Design 3 had no slot for the sentence; `{{RETURNING_SENTENCE}}` was added as an optional block
that drops out entirely when absent → [niete_design3_returning_member_2026_08_19.md](niete_design3_returning_member_2026_08_19.md).

---

## Gotchas hit this session

- 🔴 **`scripts/evals/contract_docx_eval.py --type` defaults to `fellow`.** A project-based
  contract validated without `--type project` throws **11 false HARD BLOCKs** (demands Fellow
  leave entitlements, demands removal of clauses project-based contracts must keep). The Fellow
  and NIETE masters are near-identical, so the validator cannot infer type. **Always pass the
  real type.** A clean/blocked result means nothing otherwise.
- 🔴 **The claude.ai Gmail connector is not necessarily Ayesha's mailbox** — in this session it
  was authenticated as `salman.iqbal@`, so the first search for Mariam's offer letter came back
  empty. Offer letters live in **ayesha.khan@ via read-only IMAP**. Never read a null result from
  that connector as "no such email"; check whose mailbox you are in.
- Console encoding: pipe `sys.stdout` through a UTF-8 `TextIOWrapper` before printing email or
  docx text on this machine, or cp1252 raises `UnicodeEncodeError` mid-run.
- Markaz `contract_drafting_full_legal_name` arrives ALL-CAPS for some candidates
  ("SYEDA MARIAM ABBAS NAQVI"). Precedent (Ayesha on Hina, 13 Aug) is to **title-case it** in the
  documents.
- **Verify CC addresses before a live send.** A quick IMAP occurrence count catches a typo'd
  address before it becomes a bounced or misdirected contract.

---

## 🔴 Repo hygiene defect found 2026-08-19 (NOT fixed — needs Ayesha's call)

`.gitignore` line 76 is `Contracts/` — **unanchored**, and with `core.ignorecase=true` on Windows
it also matches **`scripts/contracts/`**. Consequence: the entire Skill 07 build/send toolchain
has **never been committed** — including the clause-removal rule above, which currently lives only
in an untracked file.

It cannot simply be un-ignored: those scripts **hardcode candidate CNICs and salaries**, so
tracking them as-is would write PII into git history permanently.

**Recommended fix (needs approval):** anchor the pattern to `/Contracts/` so it only matches the
root masters folder, **and** refactor the build scripts to read candidate PII from Markaz or an
untracked data file instead of hardcoding it — then the code can be versioned safely.
