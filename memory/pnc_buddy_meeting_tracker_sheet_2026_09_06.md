---
name: P&C Buddy Meeting Tracker Sheet (LOCKED 2026-09-06)
description: Ayesha's meeting-notes tracker Google Sheet, one tab per P&C Buddy counterpart. Locks the format rule learned over four rejected passes - a tracker is a task list, minutes live in hover notes.
type: project
---

# P&C Buddy Tracker Sheet — meeting notes tracker (LOCKED 2026-09-06)

**Spreadsheet:** `17eb8v55YQOKIiqpd3c2Bq6dDM8_6Wu9EzgsKh0WHr6w` — "P&C Buddy Tracker Sheet"
**Owner:** ayesha.khan@taleemabad.com (created with `.claude/config/token_sheets_broad.json`,
which is Ayesha's own OAuth user token, not a service account)
**Builder:** [scripts/pnc/build_pnc_buddy_tracker_sheet.py](../scripts/pnc/build_pnc_buddy_tracker_sheet.py)
**First tab:** `Sabeena` (one tab per counterpart; Sabeena Abbasi sponsors Impact & Policy,
Fundraising and Standards & Evals)

This is **separate from** the P&C Buddy Google **Doc** `1CWPHvRdTtAwJ3gdHyVdwP1MWzA2C4NwM1ZimtNCiylI`
(see [pnc_buddy_tracker_project_2026_08_19.md](pnc_buddy_tracker_project_2026_08_19.md)). The Doc
is the four-theme narrative tracker. This Sheet is the actionable meeting follow-up list.

---

## 🔴 THE FORMAT RULE — a tracker is a TASK LIST

**Learned over FOUR passes on this one sheet.** Ayesha rejected, in order:

1. One row per task, with the topic label and the minutes **repeated** on every row → "there's
   too much of repetition"
2. Topic blocks with the minutes written **once per block** as a paragraph → "its still too
   much. compress more"
3. Topic blocks with a **one-line summary column** → "i guess its better to have tasks only"
4. ✅ **Accepted:** tasks only.

**The accepted shape:**

| Col | | |
|-----|---|---|
| A | Date | hyperlinked to the meeting recording on the first row of each meeting |
| B | Topic | shown **once** per block, blank on the rows beneath; carries the hover note |
| C | Task | short imperative, one per row |
| D | Owner | |
| E | Priority | CRITICAL / High / Medium |
| F | Done | real tick box |

**The full unabridged minutes survive ONLY as a hover NOTE on the topic cell**
(`updateCells` with `fields: 'note'`). That keeps the meeting record at zero visual cost.

**Apply this to any tracker or notes artefact for Ayesha, not just this sheet. Do not put
narrative prose in a cell. Default to less.**

---

## Build / update mechanics

- **Bare run creates and aborts if a sheet of that name already exists** — never make a second
  one. `--update` rewrites the `Sabeena` tab in place so the link stays stable.
- `--update` wipes **values AND notes** first via `updateCells` with
  `fields: 'userEnteredValue,note'`. A `values().clear()` alone leaves stale hover notes behind.
- Uses the raw `googleapiclient` sheets/drive v4 clients. **`gspread` is NOT installed in
  `.venv`** — do not import it.
- Ticking `Done` strikes through and greys A:E via a `=$F2=TRUE` custom-formula rule; a second
  rule highlights `CRITICAL`. Checkbox validation and both rules extend 60 rows past the data so
  future meetings inherit them.
- ⚠️ **Column indices shift whenever a column is dropped.** After any layout change, re-check
  every conditional-format range, the `setDataValidation` range and the `=$F2` formula.
- Console printing of the ⚠ glyph fails under Windows cp1252. Encode to ASCII with `replace`
  when verifying from a terminal; it is a console limitation, never a data problem.
- Structural API checks confirm values, notes, rules and validation — they **do not confirm
  appearance**. Ask Ayesha to eyeball it. See [[contract_docx_build_rules_2026_08_13]].

## Content discipline

Minutes are built from a **Fathom auto-transcript**, which is lossy — garbled Urdu/English,
switched pronouns, mangled names. Every uncertain item is flagged inline with ⚠ rather than
guessed. Open ⚠ items on the Sabeena tab as of 2026-09-06: the salary figure "at least 400 to
450" has **no units stated**; the coaching-support name is **Zaheb or Zohaib**; the tracker owner
**Momina vs Momna Tariq** may be two different people; the Nawal passage switches between he/she
and Nawal/Namal.

🔴 The **no-personal-names** rule that governs the Fundraising capability doc set does **not**
apply here. That rule is scoped to shareable P&C working documents. This is Ayesha's private
follow-up tracker and names are the entire point.

---

## Now a skill (2026-09-08)

Skill **`03_hiring-operations` was renamed to `03_operations`** at Ayesha's request (drop
"hiring", keep the `03_` prefix so the numbering convention across the seven skills holds).
This tracker is **component #5** of it:
[.claude/skills/03_operations/meeting-notes-tracker-sheet.md](../.claude/skills/03_operations/meeting-notes-tracker-sheet.md).
`SKILL.md` opens with a **"Skills in Operations"** table so invoking Operations lists all five
component names. References updated in `.claude/sops/CLAUDE.md`, `.claude/sops/TASK_WIRING_MAP.md`,
`.claude/SKILL_CONSOLIDATION_AUDIT_2026_05_30.md`, `memory/architecture_consolidation_complete.md`,
`memory/skills_consolidation_audit_2026_05_30.md`, `memory/discipline_one_master_file_per_skill.md`.

**Builder generalised the same day:** data is now `TABS = {tab_name: [meeting, ...]}` where each
meeting is `{'date', 'recording', 'topics'}`, so a tab accumulates meetings (newest first, date
shown once per meeting with a thick rule between meetings) and a new counterpart is just a new
key (`--update` creates the tab). 🔴 **`--update` still rewrites each listed tab in full, so every
past meeting must stay in `TABS` or it is erased. There is no append mode.**
