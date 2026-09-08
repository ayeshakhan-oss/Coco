# Meeting Notes Tracker Sheet

**Skill 03 (Operations) — component #5**
**Status:** 🔒 LOCKED 2026-09-06 (format settled after four rejected passes)
**Owner of the artefact:** Ayesha
**Builder:** [scripts/pnc/build_pnc_buddy_tracker_sheet.py](../../../scripts/pnc/build_pnc_buddy_tracker_sheet.py)
**Memory:** [memory/pnc_buddy_meeting_tracker_sheet_2026_09_06.md](../../../memory/pnc_buddy_meeting_tracker_sheet_2026_09_06.md)
**Root rule:** CLAUDE.md Rule 23

---

## What this is

Ayesha runs 1:1s as **People & Culture Buddy** for four themes (Impact & Policy,
Fundraising, Standards & Evals, Growth). This skill turns each of those meetings into an
actionable follow-up list in a Google Sheet.

**Spreadsheet:** `17eb8v55YQOKIiqpd3c2Bq6dDM8_6Wu9EzgsKh0WHr6w` — "P&C Buddy Tracker Sheet"
**Owner:** ayesha.khan@taleemabad.com
**Structure:** one **tab per counterpart** (first tab `Sabeena`); each tab accumulates
every meeting held with that person, newest at the top.

Not to be confused with the four-theme narrative P&C Buddy **Google Doc**
`1CWPHvRdTtAwJ3gdHyVdwP1MWzA2C4NwM1ZimtNCiylI`. That one is prose. This one is tasks.

---

## 🔴 THE FORMAT RULE — a tracker is a TASK LIST

Ayesha rejected three richer layouts before accepting this one. Do not reinvent them:

| Pass | What was built | Her response |
|------|----------------|--------------|
| 1 | One row per task, topic + minutes **repeated** on every row | "theres too much of repitition" |
| 2 | Topic blocks, paragraph minutes written **once per block** | "its still too much. compress more" |
| 3 | Topic blocks + a **one-line summary column** | "i guess its better to have tasks only" |
| 4 | ✅ Tasks only | accepted |

**The locked layout:**

| Col | Field | Behaviour |
|-----|-------|-----------|
| A | Date | shown **once per meeting**, hyperlinked to that meeting's recording |
| B | Topic | shown **once per topic block**, blank beneath; **carries the hover note** |
| C | Task | short imperative, one per row |
| D | Owner | who does it |
| E | Priority | `CRITICAL` / `High` / `Medium`; CRITICAL auto-reddens |
| F | Done | real tick box; ticking strikes through and greys A:E |

**The full unabridged minutes live ONLY as a hover note on the topic cell**
(`updateCells` with `fields: 'note'`). That preserves the record at zero visual cost.

**Never put narrative prose in a cell for Ayesha. When unsure, ship less.**

---

## How to add a meeting

1. **Get the transcript.** Fathom auto-transcripts are lossy: garbled Urdu/English,
   switched pronouns, mangled names. Also take Ayesha's own in-meeting notes if she
   pasted them; her notes set the priorities, the transcript fills in the detail.
2. **Group into topics.** One topic per thread of discussion, labelled
   `Person | subject` (e.g. `Usman | salary`) or just `Subject` where no person owns it.
3. **Write the tasks.** Short imperatives. One action per row. Assign an owner even when
   it is not Ayesha (items owned by the counterpart are tracked, not actioned).
4. **Write the hover note.** The full minutes for that topic, including everything that
   did not become a task.
5. **Flag every uncertainty inline with `⚠`.** Never resolve a garbled name, figure or
   pronoun by guessing. State what the transcript actually said.
6. **Prepend** a dict to that person's list in `TABS` in the builder:
   ```python
   {'date': '2026-09-11',
    'recording': 'https://fathom.video/share/...',
    'topics': SABEENA_2026_09_11}
   ```
7. Run `python scripts/pnc/build_pnc_buddy_tracker_sheet.py --update`
8. **Verify via the API** (values, notes, checkbox validation, both conditional rules) and
   then **ask Ayesha to eyeball it** — see the hard limit below.

**A new counterpart** is just a new key in `TABS`; `--update` creates the tab if missing.

---

## ⚠️ Traps, all of them paid for

- **`--update` rewrites each listed tab in full.** Every past meeting must stay in `TABS`
  or it is erased from the sheet. There is no append mode.
- **A bare run refuses to create a second sheet of the same name** and exits. Never work
  around it by creating a duplicate; the link Ayesha has must stay stable.
- **Wiping must clear values AND notes.** `values().clear()` leaves stale hover notes
  behind, which then contradict the tasks. Use `updateCells` with
  `fields: 'userEnteredValue,note'`.
- **`gspread` is NOT installed in `.venv`.** Use the raw `googleapiclient` sheets/drive v4
  clients. Do not add the dependency.
- **Dropping or adding a column shifts every index.** After any layout change re-check
  each conditional-format range, the `setDataValidation` range, and the `=$F2=TRUE`
  formula. They are all silently wrong otherwise.
- **Printing `⚠` to a Windows console fails** under cp1252. Encode to ASCII with
  `replace` when verifying from a terminal. It is a console limit, never a data problem.
- **Structural checks are not visual proof** (CLAUDE.md Rule 14). The API confirms values,
  notes, rules and validation. It cannot confirm appearance. Say so, and ask Ayesha to
  look.
- **The no-personal-names rule does not apply here.** That rule is scoped to shareable
  P&C working documents like the Fundraising capability set. This is Ayesha's private
  follow-up tracker; names are the entire point.

---

## Open ⚠ items on the Sabeena tab (as of 2026-09-06)

| Item | What is unresolved |
|------|--------------------|
| Usman's salary figure | "at least 400 to 450" — **units never stated** in the transcript |
| Coaching support name | heard as **Zaheb** or **Zohaib** |
| Standards & Evals tracker owner | **Momina** vs **Momna Tariq** may be two different people |
| Nawal passage | transcript switches between he/she and between Nawal/Namal |

Resolve these with Ayesha rather than picking a reading.
