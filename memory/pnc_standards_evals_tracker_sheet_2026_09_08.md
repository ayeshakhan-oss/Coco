---
name: standards-evals-tracker-sheet-formatting
description: Standards and Evals Tracker (Sabeena's sheet) formatting pass, plus the two reusable Sheets lessons - never set an explicit row height on a wrapped cell, and how to get real visual proof of a Sheet
metadata:
  type: project
---

# Standards and Evals Tracker — formatting pass (2026-09-08)

Ayesha asked me to beautify the **Standards and Evals Tracker**, the sheet behind the
**Standards & Evals** theme of her P&C Buddy work. See [[pnc-buddy-tracker-project]].

- **Spreadsheet:** `1gF5-Ng7iNbFtS0SVSZ83bFxEDIZGvJpA6_PI1aU7mXY`, single tab `Sheet1`
- **Owner: `sabeena.abbasi@taleemabad.com`. Ayesha is only an EDITOR.** Sameer Sheikh
  (`sameer.sheikh@taleemabad.com`) was editing it the same day. It is a live doc belonging
  to someone else's team.
- **Builder:** `scripts/pnc/beautify_standards_evals_tracker.py` (`--dry-run`, `--revert`)

## Layout the sheet uses

`A Goals | B Owner | C+ one column per fortnight` (C header = `27-Aug-2026 - 10-Sep-2026`).
The goal is named **once per block** and left blank on the rows beneath, with one row per
owner — the same shape Ayesha accepted for the P&C Buddy tracker. It grows **rightward**
one column per fortnight, which is why the formatting freezes `A:B` rather than just row 1.

Two goal blocks at the time of the pass: Standards/FICO (Unsa, Momna) and Coaching
(Sameer, Ahwaz). Momna's and Ahwaz's fortnight cells were empty.

## What "beautify" meant here

Because the tracker is Sabeena's and per the tracker rule (a task list, not a write-up),
every write was **formatting only** — no value edits, no added rows/columns/status fields,
verified afterwards by asserting the 5 rows were byte-identical. Blocks are detected from
non-blank column A, so the script survives new goals being added.

Applied: frozen header row + `A:B`; `#2F4FA2` header band, white bold; goal names bold
navy; body wrapped and **top**-aligned (was bottom, which looked broken with multi-line
paragraphs); column C widened 173px → 470px; **gridlines ON**; one `SOLID_MEDIUM` rule
above each goal block as a separator.

## 🔴 Lesson 3 — a shared background across rows reads as a merged cell

The first pass hid the gridlines and gave each goal block one continuous `#F6F8FB` tint.
Ayesha's response: *"you've done something wrong. you were not supposed to merge Unsa and
Momna and Sameer & Ahwaz. please keep the option of colums and rows."* **Nothing had been
merged** and no value had changed (asserted byte-identical) — but two owner rows sharing an
unbroken background with no line between them *looks* merged, and that is what counts.

**Rule:** on a sheet other people type into, row and column separation beats prettiness.
Do not hide gridlines and do not span a background tint across rows. Group with a single
heavier rule above the block, plus the label in column A, and nothing else. When a "tidy"
formatting choice could be mistaken for a structural change to someone's data, it is the
wrong choice. Reach for `sheets(merges)` in the verification pass so "no merged ranges" is
provable, not just asserted.

## 🔴 Lesson 1 — never set an explicit row height on a wrapped cell

`autoResizeDimensions` on ROWS reported `pixelSize: 21` for rows holding 200-character
wrapped paragraphs. **That 21 is not a bug and not a failure to resize:** Sheets stores the
default height in `rowMetadata` and auto-fits wrapped content at *render* time. I read the
21 as "auto-resize didn't work", added a 30px minimum-height floor to stop owner-only rows
looking like slivers, and thereby **pinned the tall paragraph rows at 30px and clipped
them**. Fixed by removing the floor entirely and re-running.

**Rule:** leave body rows with no explicit `pixelSize`. Only a header row gets a fixed
height. A stored height of 21 on a WRAP cell means auto-fit is working.

## 🔑 Lesson 2 — real visual proof for a Google Sheet

Rule 14 (structural checks are not visual proof) is liftable for Sheets, the same way
Rule 24(c) lifts it for Docs and Slides. There is no Excel/LibreOffice on this machine, but:

    GET https://docs.google.com/spreadsheets/d/<id>/export
        ?format=pdf&gid=<sheetId>&size=A4&portrait=false&fitw=true
        &gridlines=false&printtitle=false&sheetnames=false

with an `AuthorizedSession(creds)`, then render with **PyMuPDF** (`fitz`, installed in
`.venv`) at `dpi=160` and Read the PNG. That is how the clipped rows were caught — a
`rowMetadata` read alone said everything was fine. The PDF cannot show freeze panes or
hidden gridlines, so assert those from `gridProperties` separately.

## Flagged to Ayesha, not changed

- Trailing spaces in the stored values: `'Owner '` (B1) and `'Coaching '` (A4).
- Momna and Ahwaz have owner rows but empty fortnight cells — unclear whether the block's
  paragraph covers both owners or they genuinely have nothing listed. Not ours to resolve.
