---
name: Attendance Report 14 April 2026 — Finalized Process & Learnings
description: Session finalization of attendance report for April 14, 2026 (Tuesday). Includes Teams integration, NIETE section, exact name matching requirement, and final report structure.
type: project
---

## Key Learnings from 14 April 2026 Attendance Report

### Name Matching — CRITICAL
**Rule:** Names in ONSITE list MUST exactly match names in ALL_PAYROLL.
- Issue: "Zeeshan Usaid" (ONSITE) vs "Muhammad Zeeshan Usaid" (ALL_PAYROLL) caused him to be flagged as missing
- Fix: Use full payroll names in all attendance categories
- Impact: Prevents false flagging of present employees

### Teams Integration — Confirmed Working
- Check presence channel via `scripts/utils/teams_reader.py` — get_presence_updates()
- Messages captured: arriving late, not feeling well, exam schedules, out sick
- Mapping Teams messages to attendance categories:
  - "Running a bit late" → PARTIAL (Arriving Later)
  - "Not feeling well / WFH" → WFH_NO_MARKAZ
  - "Out sick" → ON_LEAVE (Sick Leave) — NOT OUT_OF_OFFICE
  - "Exam schedule, half-day leave" → ON_LEAVE with specific dates

### Attendance Categories — Final Structure (14 Apr 2026)
1. **Onsite Today** — 2-column name-only grid, alternating row colors (light green/white)
2. **Arriving Later — Teams Update** — Name|Status table
3. **On Leave** — Name|Status table (includes sick leave, half-days)
4. **Working From Home** — Name|Status table (conditional not-feeling-well)
5. **WFH — Confirmed** — Name|Status table (8 permanent arrangements)
6. **Out of Office** — Name|Status table (currently empty on 14 Apr)
7. **Flagged — No Attendance Record** — Name|Status table (auto-computed exclusions)
8. **Archived/Parked (NIETE)** — Name|Status table, purple header, includes "Onsite I-10" notes
9. **Additional in Attendance — Not OPL+OWT** — Name|Status table (blue header)

### Permanent Exclusions from Flagged
- Alishba Anam (NEVER_FLAG set)
- Razia Kausar (NEVER_FLAG set)
- Reason: User directive 2026-04-14 — never add again

### Special Notes Categories
- Qurat-ul-ain Amjad (ARCHIVED_NIETE): "Not available second half (Teams)" — exam day
- Momina Tariq (ON_LEAVE): "Half-day Leave — Exams (Apr 14 & 17), unavailable after 1pm"
- Mahrah Ashraf (ON_LEAVE): "Sick Leave (Teams)" — moved from OUT_OF_OFFICE per user clarification

### Stat Boxes — 7 Total (NOT 8)
1. Total Active
2. Onsite Today
3. On Leave
4. WFH
5. WFH Confirmed
6. Arriving Later
7. Flagged

### Footer Structure
- 2-column layout: left = organization/contact/date, right = "Compiled by Coco, Nugget & Noah"
- Font: 8px gray (#666666)
- Border: 0.5mm #e0e0e0

### Script Location
`scripts/reports/attendance_14apr2026.py` — FINAL pattern, copy for future dates

### Recipients
TO: ayesha.khan@taleemabad.com (via safe_sendmail)
Never CC to full team without explicit approval

### Next Steps for Future Reports
1. Pull Teams presence channel (last 24h)
2. Cross-reference with user's on-site check
3. Update categories in script (use full payroll names exactly)
4. Regenerate PDF
5. Verify flagged section for accuracy
6. Send to Ayesha only (unless otherwise instructed)
