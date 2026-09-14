---
name: OPL Permanent Contract Build + Permanent Joining Email (2026-09-12)
description: Ahmad Wajahat GM-Lahore package. Drive's PDF converter IGNORES keep_with_next, so stranded headings can only be found by rendering and measuring. Plus every formatting defect the OPL full-time master ships with, and the new permanent full-time joining email.
type: project
---

# OPL Permanent Contract + Joining Email (2026-09-12)

**Case:** Ahmad Wajahat, Growth Manager Lahore (Job 39, app 3635, cand 2929), OPL full-time
permanent. Start **14 September 2026**. Gross **PKR 240,000/month** inclusive of tax.
CNIC 35200-1568315-5, self-submitted to the Markaz contract-drafting form 2026-09-07.
Signatory **Waqas Tanveer, Head of Growth**. Reports to **Zeest Qureshi, Senior Manager Growth**.
Builder `scripts/contracts/build_gm_opl_package.py` · email `scripts/contracts/send_gm_opl_joining.py`.

---

## 🔴 THE BIG ONE — Drive's PDF converter IGNORES `keep_with_next`

`apply_heading_formatting()` sets `keep_with_next` and the property is genuinely there in the
XML. **Drive does not honour it.** So the property proves nothing, headings still strand at page
feet, and "the flag is set" is exactly the structural-evidence trap Rule 1 warns about.

Worse: it sets the flag on every heading AND its block. In an annexure where each numbered
sub-heading starts a new block, the flag ends up chained across the whole document with no gap,
so the renderer has **no legal break point at all** and breaks wherever it must.

**The only reliable method is render → measure → decide.**
`enforce_no_stranded_headings()` converts to PDF, asks `verify_pdf_layout` which headings
actually got separated, sets an explicit `page_break_before` there, and repeats (breaks reflow
everything after them). Then it **minimises**: an early break often becomes unnecessary once a
later one lands, leaving a half-empty page for nothing.

🔴 **When forcing a break before heading H, walk BACK over any run of consecutive headings.**
Breaking directly before "1. Strategic Storytelling" left **"Key Responsibilities" as the only
line on an otherwise blank page**. And `verify_pdf_layout` **cannot see that**: a heading whose
next paragraph is also a heading has an empty block, so the check is skipped. The builder has to
avoid creating what the verifier is blind to.

---

## Every defect the OPL full-time master ships with

| Defect | Cause in the master | Fix |
|---|---|---|
| Grey boxes behind titles | RUN-level `w:shd fill=D2D2D2` in rPr | `clear_heading_shading()` strips run + paragraph shd and highlight |
| **Three different left edges** | `Heading 1` STYLE carries left_indent 0.44" AND each heading paragraph adds first_line_indent 0.44" on top, so headings sit at 0.89" vs body 0.44" vs header block 0" | `normalise_indents()` - one left edge, one right edge, measured off the master |
| Date block misaligned | `Date:` + tab + `Private & Confidential` + `CNIC:` all in ONE paragraph, 0.44" first-line indent, LEFT tab stop at 5.09". CNIC only reached the margin by wrapping | `fix_header_block()` - CNIC onto its own line, RIGHT tab stop at the body's right edge |
| Ragged right mid-document | master mixes JUSTIFY and LEFT paragraph by paragraph (Data Confidentiality, Intellectual Property, Others are LEFT) | `unify_body_text()` |
| One heading italic | "Health Insurance" is italic, every other title upright | `unify_body_text()` |
| `a)` / `b)` do not line up | the two Validity items carry DIFFERENT indents (left 1621 + hanging vs left 1360 + firstLine 0) | one rule for all `numPr` paragraphs |
| 🔴 python-docx cannot read the file | master ships `w:hanging="261.9999999999999"`; every indent read raises `ValueError: invalid literal for int()` | `sanitise_indent_attrs()` must run FIRST, before anything inspects indents |
| Em dashes | 3 constructions in the JD + my own signature placeholder | explicit reviewed `DASH_FIXES`, each asserted present so a reworded JD fails loudly |
| `I, NAME , the employee` | space before the comma is in the template | cosmetic strip |

**Bullets:** glyph on the body's left edge, text hanging 0.25" in, **separated by a TAB not
spaces** - justification stretches spaces, so a space-separated bullet drifts from its own text.
Justified, like everything else.

---

## The permanent full-time joining email (new)

`joining-emails.md` listed **Permanent Full-Time** as still pending. Ayesha's content rule
(2026-09-11): **state the START DATE, no end date, add 3 months probation.** Everything else
follows Template 4 as closely as a permanent hire allows.

- Template `templates/permanent_joining_design3.html` - the locked Design 3 layout with ONLY the
  project-specific prose parameterised (no `PROJECT_NAME`/`PARTNER_NAME`, buttons block optional).
  Derived from the NIETE file by anchored replacement so the layout is byte-identical.
- 🔴 **No onboarding form exists for a permanent hire.** Only Fellow and NIETE forms exist and the
  skill is explicit that the form differs by programme. Buttons omitted rather than sending a
  Growth Manager to the Fellow form. The WhatsApp link went with it, because the harness requires
  a form link whenever "Click here" appears. **Still owed by Ayesha.**
- 🔴 **Say the CITY.** Growth Manager runs as two live roles; the offer letter said "Growth
  Manager Lahore", so the joining email says it too - subject, hero line, opening sentence and
  the details card. `role_display()` = position + city.
- Subject is IDENTICAL for pilot and live (SOP Rule 12: the pilot IS the email). No `[PILOT]`.

---

## Process lessons

- 🔴 **I did not read `CONTRACT_DOCX_BUILD_SOP.md` before building.** Ayesha called it out and was
  right. Reading the skill and the memory files is not the same as reading the SOP.
- 🔴 **I scanned the EMAIL for em dashes and never the CONTRACT**, where my own placeholder used
  one. Scan every artefact, not the one you were thinking about.
- 🔴 **I left-aligned the Annexure bullets on my own judgement** (to avoid stretched word gaps) in
  an otherwise justified document. That was my call, not hers, and it was wrong.
- 🔴 **A passing structural eval is not proof of appearance.** Every single defect above passed
  `contract_docx_eval.py` as clean. Only rendering to PNG and reading it found them.
- **Don't re-send a pilot on every fix.** Three landed in her inbox in an hour; batch them.
- ⚠️ The formatting-audit workflow spent ~9M subagent tokens and hit the spend limit before the
  completeness critic ran. It largely confirmed fixes already applied. For a single document,
  diagnosing in the XML directly was faster and cheaper than fanning out.

## Repo findings
- 🔴 **`scripts/contracts/` is entirely untracked by git** (0 files). `.gitignore:76 Contracts/`
  also matches it because `core.ignorecase=true` on Windows. No history, no backup, no review for
  the whole contract-build codebase.
- Candidate PII moved out of the build script into gitignored `data/contracts/gm_opl_candidates.json`,
  matching the NIETE discipline. JDs live in `data/contracts/` so the build is reproducible.
- Both GM JDs open with a stray line "Chief Operating Officer - Taleemabad" (copy-paste artefact).
  Excluded from Annexure-A; should be fixed at source since candidates get the link.

## BOTH LIVE (2026-09-12)

| | Ahmad Wajahat | Marzia Hasnain Khandwala |
|---|---|---|
| Role | Growth Manager **Lahore** (Job 39, app 3635) | Growth Manager **Karachi** (Job 41, app 3819) |
| Legal name (CNIC form) | Ahmad Wajahat | **Marzia Hasnain Khandwala** |
| CNIC | 35200-1568315-5 | 42201-4922921-4 |
| Start | 14 Sep 2026 | 16 Sep 2026 |
| Gross | PKR 240,000 | PKR 240,000 |
| Sent | 13:17 PKT | 13:32 PKT |
| Cc | waqas, zeest, hiring@, ayesha | waqas, zeest, hiring@, ayesha, **ali.sipra** |

Both signed by Waqas Tanveer, Head of Growth; both report to Zeest Qureshi, Senior Manager
Growth (confirmed separately for Karachi, not inherited). Delivery verified over IMAP: exactly
one live send each, correct Cc, two PDFs each.

🔴 **FOUR name variants for Marzia** - and the CNIC form produced a surname that appears NOWHERE
else in anything she sent us:

| Source | Name |
|---|---|
| **CNIC form** (the legal name, used in the contract + NDA) | **Marzia Hasnain Khandwala** |
| Markaz record | Marzia Hasnain |
| Her own signature | Marzia Hasnain |
| Gmail display name / email | Merzia Hasnain / merzia.hasnain99@ |

Ayesha confirmed: **use the name submitted in the CNIC form.** The email greeting stays
"Marzia" - what she has always been called. Extends [[project_smg_case_study_round2_2026_08_24]]:
a stored name, a display name and a CV filename can all disagree, and the CNIC form can add a
name none of them have. **Always surface the conflict in the pilot.**

⚠️ Ayesha sends account credentials herself as a reply on the joining thread, minutes after the
joining email (Google + Markaz logins). Not part of the joining email; do not duplicate it.

## Still open
1. **Marzia Hasnain (GM Karachi, app 3819)** - `contract_drafting_full_legal_name` and CNIC are
   BOTH NULL in Markaz and were never emailed. Joins **16 September**. Her `reports_to` is
   deliberately null: Ayesha named Zeest for Lahore only, so the build fails loudly until confirmed.
2. **CC list for the live send.** Ahmad's offer thread carried hiring@ + zeest.qureshi@.
   Never add recipients silently (joining-emails.md rule 9).
3. **What was promised to Ahmad on fuel** - his acceptance cites "as discussed" on a call.
4. Name conflict: CNIC form "Ahmad Wajahat" vs interview doc "Ahmad Wajahat **Sheikh**" vs Gmail
   display name "Wajahat Sheikh Official". Used the CNIC-form value. See [[project_smg_case_study_round2_2026_08_24]].

## Related
[[contract_docx_build_rules_2026_08_13]] · [[contract_docx_defects_and_harness_2026_08_13]] ·
[[gm_lahore_values_invite_ushna_2026_08_24]] (the two-city Growth Manager trap) ·
[[contract_email_design3_standard_2026_08_14]]
