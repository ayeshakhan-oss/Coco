---
name: RM Internal Hiring 2026 - anonymised case study tracker (2026-08-31)
description: 25 internal RM applicants, case studies anonymised as RM-01..RM-25, uploaded to Drive with a Google Sheet tracker (Master Key + shareable Evaluation tab). Includes the anonymisation method and its verified limits.
type: project
---

# RM (Regional Manager) internal opening - case study tracker

**Announcement:** internal, all@niete.edu.pk, 2026-08-20 (Skill 01 type #7).
Original deadline Thu 27 Aug 1:00 PM was **extended by Ayesha on 25 Aug to Fri 28 Aug 11:59 PM**,
and submissions were **redirected to hr@taleemabad.com**. All 25 landed within the extension.

**Result: 25 submitters**, all NIETE staff. Cross-checked two ways: mailbox sweep of
ayesha.khan@ via read-only IMAP, and the 25 HR acknowledgements (Zeshan x20, Jawwad x5).

## Artifacts
- Sheet: `1xtQxfblMXmA5IpnvnABkK5bvmhPMK5_Q6Z1wDiI59A8` - tabs **Master Key** (code + real name +
  resume, Ayesha only) and **Evaluation (share this)** (code only, no names).
- Drive root `1itkyxaIabK54IdKw7fJU5dMbXznQjlom` -> `Case Studies (Anonymised)` (27 files),
  `Resumes (NAMED - do not share with evaluators)` (24 files).
- Codes RM-01..RM-25 assigned by md5-of-name ordering, so **code order != submission order**.

## Anonymisation method (reusable)
- **PDF:** PyMuPDF `add_redact_annot` + `apply_redactions` (true text removal, layout preserved),
  plus `set_metadata({})`. Never flatten a PDF to text - it destroys tables the rubric scores.
- **DOCX/PPTX:** names are routinely **split across runs** (Shafaq's appeared as `S|hafaq T|ahir`),
  so a naive `document.xml` string replace MISSES them. Join a paragraph's runs, replace on the
  joined string, write back in-run when the match sat inside one run and only collapse to run[0]
  when it spanned runs. Also clear core properties (author/last_modified_by).
- **Redact automatically:** multi-token names, email, email local-part, phone, and bare given/family
  tokens >=4 chars. **Deny-list** `islam din khan ali syed muhammad abdullah anwar` - they collide
  with real case content (Islamabad, stakeholder names).
- 3 docx failed to open in python-docx: `[Content_Types].xml` lacked a `Default Extension` for
  media parts (one literally `.undefined`). Repair = rebuild the zip with the Default added,
  sniffing the content type from magic bytes.

## Verification done (and its limit)
Re-extracted text from all 27 outputs and grepped every alias/email/phone: **0 identifiers left**.
Confirmed all PDFs are text-based (no scans), so the check is not vacuous. Word-diffed every file:
only names removed; docx char deltas are `&apos;`/`&quot;` re-encoding, not content loss.
🔴 **Limit (CLAUDE.md Rule 14):** text extraction cannot see inside **embedded images** - several
PDFs carry 10-47 images (charts/screenshots) that may show a name visually. Not OCR-verified.

## Per-candidate flags
- **Shafaq Tahir (RM-04): NO RESUME.** Both her files are the case study (Word + 15-slide deck).
- **Bushra Karim (RM-08):** submitted as Drive links not attachments; case study is 2 files
  (full response + executive summary).
- **Khadija Akbar (RM-07):** submitted twice; Ayesha directed using the **Fri 28 Aug** version.
- **Ashas Khan (RM-23) / Misbah Iqbal (RM-25):** case study on time, resume only on Mon 31 Aug.
- **Sana Nawaz (RM-01):** later resume version used.
- **Toseef ur Rehman (RM-20):** name/email/phone in a header on all 47 pages (379 redactions).

## Multi-file submitters + the defect it exposed
Only **2 of 25** sent more than one case-study file: **RM-04 Shafaq** (Word + 15-slide deck, the SAME
answer in two formats) and **RM-08 Bushra** (full response + a separate executive summary).
🔴 **Defect caught by Ayesha:** files were uploaded correctly but the sheet hyperlinked only the
FIRST file and merely labelled the cell "(2 files)" - telling the evaluator a second file existed
while giving them no way to open it. Fixed with a dedicated **"Case study - 2nd file"** column on
both tabs, labelled by what the part actually is. **Rule: never signal a file in text without
linking it.** A count column is not a link.
🔴 **Second lesson:** my first mailbox pull filtered on subject (`regional manager|RM|case study`),
which is how Bushra's second message was nearly missed. **Sweep by SENDER ADDRESS, not subject**,
when reconciling submissions - candidates reply with arbitrary subjects.

## Reconciliation done for all 25 (2026-08-31)
- Every message from all 25 addresses re-pulled with NO subject filter. 23 sent exactly 2 files;
  only 2 files excluded, both deliberately superseded versions (Sana's first resume, Khadija's
  27 Aug case study). No third files, no missed links.
- Each anonymised file fingerprinted against its source original: 95.8-100% word overlap, **0
  mix-ups** - no one can be scored on another candidate's work.
- All 51 Drive uploads byte-match local copies; all 51 sheet links resolve; no orphan files.

## Benchmark answer key + QA round 1 (2026-09-02)

Key built 2026-08-31 from the case doc + JD only, no submission read. Source of truth:
`docs/case_studies/benchmarks/rm_regional_manager_benchmark.md`. Three outputs, all updated
IN PLACE so links stay stable: artifact `813231e9-2d45-489e-a2cf-2896d716428e`, PDF Drive
`1D_CTT66MCw8rx4ilja_50s2Im4mkaWGZ`, Doc `1pCwMsjq6RY6jhTZubTdif6np5jsboocBVk-2pZIE9_g`.

**Verified case arithmetic (reusable):** Part B table sums to exactly 115%; the +25% observation
demand adds **+6.25pp** on the HITL base -> real demand **121.25%**, so the required cut is
**21.25pp**, not the 15pp the case states. Student data: "below grade level 34% / at grade level
75%" CANNOT be a composition share (sums to 109% Urban, 110% Rural) - it is a **subgroup pass
rate**, and on that reading both regions reconcile exactly. Implied below-grade share Urban
**19.5%** vs Rural **41.7%** (2.1x), Rural passing 49% of them vs Urban 34%.

### 🔴 Three defects Ayesha caught in QA round 1 - all mine
1. **Arithmetic error in the benchmark itself.** My Q4 table cut **30pp for a 21.25pp problem**
   and kept the +6.25pp OUTSIDE the table, then called the remainder "~15pp headroom". Corrected
   to carry the demand inside the table and close at **98.75%** (121.25 - 22.5). **Lesson: when a
   benchmark contains worked arithmetic, run the sum in code before publishing - I verified the
   case's numbers but never my own answer's numbers.**
2. **Required columns lost in the markdown -> HTML rebuild.** Q1's **"Where from"** and Q8's
   **"what information you will share"** existed in the markdown but were dropped when I compressed
   the tables for the web layout. The published PDF/artifact therefore understated the marking
   criteria on two questions. **Lesson: when a rubric mirrors a question's own required fields,
   the column count is CONTENT, not layout - never drop one to fit a design.** Diff derived formats
   against the source before publishing.
3. **Verdict overstated.** Q2 said a flat "no". Correct framing: Urban leads on *some* indicators
   but evidence is **insufficient to rank overall**.

Also added on her instruction: a training-records information item (the case says completed modules
show as incomplete), a worked four-part example for Q1, an explicit **evidence -> intervention**
decision rule for Q3, and the standing rule that **Very High activities are never paused or
dropped - only redesigned**. Q5/Q6/Q7/Q9/Q10 reviewed, no changes.

**Still open for decision:** Q10 has no printed point value (Q1-Q9 already total 100); donor visit
(10 days) vs Ministry visit (5 days) inconsistency; confirm +25% applies to HITL; confirm scoring on
the case's own allocation rather than the 6-dimension growth rubric. **70% bar was published to
staff in the announcement - treat as a commitment, not adjustable after seeing the pool.**

## Next step
Per CLAUDE.md Rule 17: **write the benchmark answer key and have Ayesha QA it BEFORE reading any
submission.** Nothing has been scored or read for assessment yet - only scanned for names.
