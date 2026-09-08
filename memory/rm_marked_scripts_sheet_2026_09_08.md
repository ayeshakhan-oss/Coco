---
name: RM below-70 marked-scripts sheet (2026-09-08)
description: Exam-style marked script sheet for the 8 RM internal candidates below the published 70% bar; also records that the tracker's own Scores tab still holds the superseded first pass.
type: project
---

# RM internal case study — marked scripts for the 8 below 70%

Ayesha, 2026-09-08: mark them "like you're checking an exam" — per-question score, what's good,
what's missing — for visibility and transparency, since these are internal staff being rejected.

**Sheet:** `1tSl69wejsDdOBHppfqQXOpCC1HEdhCXNTBltcaNBt8k`
"RM Case Study - Marked Scripts (below 70%)" — Summary tab + one tab per candidate.
**Builder:** `scripts/reports/build_rm_marked_scripts_sheet.py` (rerunnable; creates a NEW
spreadsheet each run, so edit in place or delete the old one rather than re-running blindly).

Each candidate tab: name/code, total vs the 70 bar, Q10 band, link to their anonymised script,
examiner's overall comment, an explicit **What's good** block and **What's missing** block, the
**marking caps that fired** with their benchmark wording, then a Q1–Q10 table with max, awarded,
the 0–5 anchor, what they wrote, and what would have scored higher.

| Code | Name | Total | Caps |
|---|---|---|---|
| RM-14 | Rida Abbas | 56 | C2, C6 |
| RM-07 | Khadija Akbar | 59 | C1b, C2 |
| RM-21 | Areej Noshad | 60 | C1a, C4 |
| RM-11 | Hafsa Bashir | 62 | C1a, C4 |
| RM-01 | Sana Nawaz | 63 | C1, C2 |
| RM-20 | Toseef ur Rehman | 63 | C1b, C2 |
| RM-18 | Javeria Nayyab | 64 | C1b, C2 |
| RM-12 | Muhammad Salman | 65 | C1b, C6 |

## 🔴 The tracker's Scores tab is STALE and contradicts the live result
Sheet `1xtQxfblMXmA5IpnvnABkK5bvmhPMK5_Q6Z1wDiI59A8` tab **Scores** still holds the **superseded
first pass**: mean 88.3, **nobody below 70**, Javeria Nayyab ranked 9th on 91.5. The strict
re-mark (mean 75.0, 8 below 70) was emailed but **never written back to the sheet**. Deltas run
from -27.5 (Javeria) to +0.5 (Danish). Anyone opening that tab reads the wrong scores.
**Rule: when a re-mark supersedes a pass, update every artefact that carries the old numbers, not
just the report.** Decide with Ayesha whether to overwrite the tab or archive it as "Scores
(superseded first pass)".

## Marking mechanics worth reusing
- Marks are the **0–5 anchor converted pro-rata** to the case's own printed points
  (Q1 10, Q2 15, Q3 10, Q4 15, Q5 10, Q6 10, Q7 10, Q8 10, Q9 10 = 100). Q10 has no printed
  points and is **banded only**, in no total.
- **Verify twice in code**: marks must sum to the stated total AND anchors×points must reproduce
  it. Both reconcile for all 8.
- Caps are applied **mechanically from the benchmark text**, never by feel — C1a/C1b (below-grade
  misread, verdict-driving vs not), C2 (Q4 no arithmetic), C3 (drops a Very High activity),
  C4 (cuts 15pp, never prices the +25%), C5 (Q7 refuses to choose), C6 (required element absent),
  C7 (not attempted). Publishing the cap wording next to the mark is what makes a rejection
  defensible to an internal candidate.
- Source data (`strict_scores.json`, `qbq.json`, `roster.json`) copied into `output/rm_marking/`
  so the sheet no longer depends on a session temp directory.
- `googleapiclient.discovery.build` clashes with a local `build()` — import it as `gbuild`.

Related: [[project_rm_internal_case_study_round_2026_09_02]] ·
[[lesson_scoring_anchor_floor_inflation_2026_09_02]] ·
[[project_rm_internal_case_study_tracker_2026_08_31]]

## Feedback emails to the 8 (Skill 01 type #8, RM variant)

Script: `scripts/send_rm_case_study_outcome_pilot.py` (`--check` gate only, `--only <name>`,
`--live` after approval). Individual workbooks: `scripts/reports/build_rm_individual_feedback_sheets.py`.
Pilot to Ayesha 2026-09-08, 8 letters, 358 words each, two attachments per letter.

**One identical letter for all eight, by design.** Ayesha supplied the wording herself. These
are colleagues who sit near each other and will compare emails: one consistent letter plus an
individualised attachment is fairer and easier to defend than eight letters of varying warmth.
**All personalisation lives in the attached marked script**, which is far more specific than
prose would be.

**Two locked rules deliberately switched off, flagged as module constants so nothing is silent:**
- `RULE10_OPENING = False` — type #8 mandates "This is not a yes for now." as the first line.
  Her wording opens with thanks; it is still an unambiguous no by paragraph two.
- `MIN_WORDS = 250` — types 1-4 and #8 require 800+. The 800 minimum exists so a rejection
  carries real feedback; here the feedback is the attached script.
**When a rule is overridden on the user's instruction, encode it as a named flag with the
reason, never by deleting the check.**

🔴 **Gate lesson: "your score" is not the same as a score.** The type-8 gate blocks the
candidate's own number appearing in the body. Ayesha's wording says the sheet "shows your score
against the different areas", which the blanket `your score|your total` pattern wrongly blocked.
Narrowed to catch a printed *figure* (`you scored \d`, `your score of \d`, `NN/100`) while
allowing a reference to the attachment. **Match the intent of the rule, not its keyword.**

**Privacy:** each individual workbook is asserted at build time to contain no other candidate's
name or code, and all 8 exported .xlsx were re-checked after export. The master marked-scripts
sheet has all 8 side by side and must never be sent to a candidate.

**Attachments per letter:** benchmark answer key PDF (exported from Ayesha's Doc
`1pCwMsjq6RY6jhTZubTdif6np5jsboocBVk-2pZIE9_g`) + that person's own .xlsx from
`output/rm_marking/individual/`. Private Drive folder `1eqrwZerEU6fj8cuibHqXWgJLvF1jJQrx`,
deliberately NOT link-shared.

**No booking URL is used.** Ayesha: "they can book their own if they need to." The offer of a
twenty minute slot stands with no link, because internal colleagues share a calendar system.
No link was invented.

## SENT LIVE 2026-09-08 — all 8, verified

CC (Ayesha, verbatim): `asma.zaheer@niete.edu.pk`, `bilal@niete.edu.pk`,
`ayesha.khan@taleemabad.com`, `hiring@taleemabad.com`, `ali.sipra@taleemabad.com`.
Note `bilal@niete.edu.pk` was **given in full**, not resolved from the repo — a bare "bilal"
grep once returned 11 addresses including a live candidate (Rule 20).

**Pre-send scan proved 0 prior live sends** to all 8 addresses; **post-send scan proved exactly
one clean-subject copy each**, 5 CC, 2 attachments, own .xlsx only, no other candidate's file
attached to anyone. Run both halves of that scan on every batch (Rule 22) — a send loop's own
console output cannot detect a duplicate or a mis-attached file.

**Live-send asserts added to the script** and worth copying: recipient must end `@niete.edu.pk`,
no `[PILOT` in the subject, and the attachment filename must contain the recipient's own name.
That last one is the cheap guard against sending someone else's marked script.

🔴 **Still open:** the tracker's Scores tab still shows the superseded first pass. The 8 have now
been told they were below 70 while that tab shows all 25 above it.

## Full documentation folder (2026-09-08)

Ayesha: one place for all the round's documentation, **named originals, all 25, not the
anonymised copies**.

**Folder:** `1hIhLcu9TSLVptef9STFKZQ6CQ6lMebVn` "RM Internal Hiring 2026 - Full Documentation"
**Index sheet:** `1_-H0hLYj0pujY-9Jfw8zEhXtPTdhGFBuJGMtfQhZ-bo` (lives inside the folder)
**Builder:** `scripts/reports/build_rm_documentation_folder.py`

25 named subfolders, 53 files, 7 round documents linked. Index has two tabs: **Round Documents**
(benchmark answer key Doc + PDF, evaluation report, marked scripts, individual feedback
workbooks, tracker, and the anonymised set) and **Submissions** (all 25 by score, with outcome
against the 70% bar and a hyperlink to every file they sent).

🔴 **This folder is NAMED and is the hiring record, not an evaluator pack.** The index carries a
standing note pointing anyone who needs an evaluator set at the anonymised folder instead. Not
link-shared.

**Re-pulling originals:** they were never cached locally, only the anonymised copies were. Swept
the mailbox **by SENDER ADDRESS with no subject filter** (a subject filter is how Bushra's second
file was nearly missed the first time) into `output/rm_marking/originals/`, resumable with a
`_pulled.json` checkpoint. **Bushra Karim (RM-08) sent Drive links, not attachments** - hers were
fetched from Drive, and her shared folder contained duplicates of the two files she also linked
directly, so dedupe by filename. Khadija (3 files, submitted twice) and Sana (3 files, two resume
versions) keep both versions in the record deliberately.

### Version labelling, and how it was proved (2026-09-08)
🔴 **In both multi-version cases the UN-SUFFIXED file was the EARLIER one**, which is the
opposite of what a reader assumes. Both are now labelled in Drive and locally, and the index
sheet's hyperlink labels were patched to match:

| Was | Now |
|---|---|
| `Khadija Akbar -  RM Case Study.pdf` | `... (27 Aug - SUPERSEDED).pdf` |
| `Khadija Akbar -  RM Case Study_1_.pdf` | `... (28 Aug - SCORED).pdf` |
| `Sana Nawaz-Resume New Updated_01.pdf` | `... (28 Aug 22-18 - SUPERSEDED).pdf` |
| `Final Updated Sana Nawaz-Resume_02.pdf` | `... (28 Aug 22-23 - CURRENT).pdf` |

**Khadija's 28 Aug version IS the one that was scored** - proved three ways rather than assumed:
byte size of the anonymised marked copy (196,310) matches the 28 Aug file (196,802) not the
27 Aug one (317,205); extracted text is **47,728 chars, a 100.00% match** to 28 Aug versus 99.62%
to 27 Aug; and the 27 Aug file carries **10 words the marked copy lacks** (`jawad`, `commented`,
`screenshot`, `shared`, `updated`...) that look like review annotations she cleaned up. Every
specific thing the marking commentary credited her with is present in the scored text.

**Reusable check for "was the right version scored?":** compare the anonymised/marked copy
against each original by (a) file size, (b) normalised-text similarity, and (c) **set difference
of words** - the last is the sharpest, because the correct source has *zero* words the marked
copy lacks. Then confirm the marking's own claims appear in that text.

**Renaming a file in Drive keeps its ID**, so hyperlinks keep working, but any sheet using the
old filename as its link LABEL goes stale. Patch those cells in the same pass.


### Index sheet: folder links + a stale-link catch (2026-09-08)
Added on Ayesha's instruction: the documentation folder's **own link** on Round Documents, and a
**Folder column** on Submissions so each candidate's whole subfolder opens in one click (25 links).

🔴 **Ayesha caught a stale link I had put in the index.** The row labelled "Benchmark answer key,
PDF" pointed at `1D_CTT66MCw8rx4ilja_50s2Im4mkaWGZ`, whose real filename is
**"RM Case Study - Benchmark Answer Key (Rev 2, DRAFT for QA).pdf"** - a superseded draft. It now
points at `1ouFEBtT_OQrm-TolbnxAKZBzTOnD5piD`, the current export and the exact PDF the 8
candidates received. The builder carries a comment so the draft ID cannot creep back.

**Standing rule: a link is not verified until the file NAME behind it has been read.** A Drive ID
copied from memory or an older note can point at a draft, and the label in the sheet will still
look right. Resolve every `fileId` to its name and print it. All 8 Round Documents links are now
resolved and confirmed.


### 🔴 The superseded first pass is still live in THREE places (2026-09-08)
Ayesha caught the second one. The strict re-mark (mean 75, 8 below 70) replaced the first pass
(mean 88.3, nobody below 70), but the old numbers were never retired from the artefacts:

1. **Tracker "Scores" tab** - still the first pass. Still unfixed.
2. **Google Doc `1suHQOhKzAjjBe26uPjSpHkl0EoSVBGqkhtReqjs8QMc`** - titled "RM Case Study -
   Evaluation Report (all 25)", but its text reads *"Mean 88.3 | Range 70-100"* and *"the bar no
   longer separates anyone"*. I linked it in the documentation index as THE evaluation report.
   Wrong. Now relabelled in the index as **SUPERSEDED, do not use to judge this round**, kept
   only for the record.
3. **Benchmark PDF `1D_CTT66MCw8rx4ilja_50s2Im4mkaWGZ`** - "(Rev 2, DRAFT for QA)".

**The correct live artefacts are the two PDFs emailed 2 Sep**, now uploaded into the
documentation folder:
- `RM Case Study - Candidate Detail (all 25).pdf` -> `1yIp7QfmwON9Y88GreQICYR-Qyl12WMHx`
  (15 pages; contains "below the 70", Rida Abbas, 56; does NOT contain 88.3)
- `RM Case Study - Question-by-Question Analysis (below 70).pdf` -> `1zmxfnpks8PypT_XropE7NrcxYblK-Gh9`
  (44 pages, all 8 named)

**Rule, twice-learned this week: when a re-mark supersedes a pass, retire the old numbers
everywhere the same day - sheet tabs, Docs, PDFs, index links - or relabel them SUPERSEDED in
place. A correct-looking title is not evidence of correct content: open the file and grep for a
figure that only the superseded version contains** (here, `88.3`).


### 🔴 The real fix: rewrite the artefact, do not re-point the link (2026-09-08)
Ayesha had to tell me the evaluation report was wrong **three times**. Twice I moved a link
instead of fixing the thing the link pointed at. That is the lesson.

Doc `1suHQOhKzAjjBe26uPjSpHkl0EoSVBGqkhtReqjs8QMc` was titled "RM Case Study - Evaluation Report
(all 25)" and opened *"Mean 88.3 | Range 70-100"*, *"the bar no longer separates anyone"*, with
Javeria 91.5 / Khadija 86 / Sana 83 / Hafsa 80 / Salman 74.5 / Rida 73 / Areej 70. First-pass
numbers. So was `docs/case_studies/rm_evaluation_report_2026_09_02.md`, the markdown it was
generated from.

**Rewritten IN PLACE** by `scripts/reports/rewrite_rm_evaluation_report_doc.py` from
`strict_scores.json`: mean 75.0, range 56-100, 8 of 25 below the bar, a section explaining why
this version supersedes the first, the full results table with Met/Below, and per-candidate
detail with per-question marks, strengths, gaps and the caps that fired. Drive
`files().update()` with `mimeType: application/vnd.google-apps.document` replaces a Doc's
content **while keeping its ID**, so every link already shared now resolves to the truth.
The repo markdown is stamped SUPERSEDED pointing at the Doc.

**Why in place matters:** the URL was already circulating. A new file would have left the wrong
numbers live at a link people hold. The index no longer needs a SUPERSEDED warning row, so it
was deleted.

**Rule: when a re-mark supersedes a pass, rewrite every artefact that carries the old numbers
the same day.** Re-pointing an index is not a fix, it just moves which wrong thing is one click
away. And verify by reading the content back and asserting a figure only the superseded version
contains is now ABSENT (here `Mean 88.3`), not just that the new one is present.
