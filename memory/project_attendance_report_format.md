---
name: I-10 Head Office Attendance Record — Confirmed Format
description: Final approved format for the weekly onsite attendance report. HTML email. Reference script: scripts/reports/attendance_8apr2026.py
type: project
---

Attendance monitoring introduced 2026-04-08. Context: WFH allowed on Fridays, Mon–Thu are onsite days. This report monitors compliance and flags unaccounted employees.

**Why:** Leadership wants to track onsite attendance during the initial WFH policy rollout. Report sent each onsite day (Mon–Thu) to Ayesha, Jawwad, and Aymen Abid.

**How to apply:**
- Reference script: `scripts/reports/attendance_8apr2026.py` — confirmed final format, approved 8 Apr 2026
- Recipients: ayesha.khan@ (TO), jawwad.ali@ + aymen.abid@ (CC)
- Subject: "I-10 Head Office Attendance Record — [Date]"
- Data sources: (1) Ayesha's sign-in sheet in `temp/` folder, (2) Markaz DB leave_requests table, (3) Teams channel updates
- Entities in scope: OPL + OWT active employees only. Exclude NIETE Balochistan, OPL-RWP, Taleemabad Inc.
- Do NOT mention OPL/OWT in the email — internal use only. Use "I-10 Head Office" throughout.

**Email format (confirmed final):**
- Dark navy header (#1a2a3a): "PEOPLE & CULTURE · ATTENDANCE MONITOR" (small caps) + "I-10 Head Office Attendance Record" (bold white) + date + "Onsite Day (Mon–Thu)"
- Stat boxes: Total Active · Onsite Today · On Leave · WFH · Arriving Later · Remote · ⚑ Flagged
- Sections (in order): Present Onsite · Arriving Later · On Leave · Working From Home · Remote · ⚑ Flagged
- Tables: 2 columns only — Name + Status (no Entity, no Department)
- Section headings: solid colored bar (background color, white text) — NOT `<p>` tags (gets stripped)

**Section logic:**
- **Onsite**: confirmed on sign-in sheet
- **Arriving Later**: mentioned on Teams they are coming but not yet seen
- **On Leave**: approved on Markaz OR mentioned on Teams (note if not on Markaz)
- **WFH**: mentioned on Teams channel (note if not logged on Markaz)
- **Remote**: confirmed remote arrangement (no sign-in expected)
- **⚑ Flagged**: not on sheet + no Markaz record + no Teams update = completely unaccounted

**NIETE field staff** (Iffat, Tehniat, Summaya, Raheela, Sohaib): remove from report entirely — field-based, not expected at I-10.
