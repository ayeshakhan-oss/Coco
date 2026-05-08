---
name: Attendance Report — Payroll Total Calculation (2026-04-09)
description: TOTAL headcount must be OPL+OWT payroll employees (84), not sum of attendance categories. Fixed critical calculation error.
type: project
---

## Issue Identified (2026-04-09)

**Problem:** Attendance report showed TOTAL = 76 (yesterday it was 84). User asked why the total was dropping.

**Root cause:** I was incorrectly calculating TOTAL as:
- TOTAL = onsite + on_leave + WFH_unlogged + WFH_confirmed + OOO + arriving_later
- This gave 56 + 7 + 2 + 9 + 1 + 1 = **76**

**Correct logic:** TOTAL should be the **payroll headcount**, not the sum of attendance statuses:
- TOTAL = All active employees in OPL + OWT payroll entities = **84** (static)
- Then show WHERE those 84 people are today (the 76 accounted + 8 unaccounted)

## Solution Applied

Verified via database query:
```sql
SELECT COUNT(*) as total FROM users u
JOIN employee_profiles ep ON u.id = ep.user_id
WHERE u.status = 'active'
AND u.deleted_at IS NULL
AND u.archived_at IS NULL
AND ep.payroll_entity IN ('OPL', 'OWT')
-- Result: 84
```

Updated script: `scripts/reports/attendance_9apr2026_exact.py`
- Set `PAYROLL_TOTAL = 84` (hardcoded, verified from DB)
- Changed: `TOTAL = PAYROLL_TOTAL` (not sum of categories)

## Current Breakdown (9 April 2026)
- **Total Payroll**: 84 (OPL+OWT)
- **Onsite**: 56
- **On Leave**: 7
- **WFH (unlogged)**: 2
- **WFH — Confirmed**: 9
- **Out of Office**: 1
- **Arriving Later**: 1
- **Accounted for**: 76
- **Unaccounted for**: 8

## Key Rule for Future Reports
**The TOTAL stat box always shows payroll headcount**, not today's attendance. Attendance is a breakdown of WHERE the payroll people are, not a count of them. The 8-person gap indicates missing data or people not categorized in any attendance status.

## Reference Script
`scripts/reports/attendance_9apr2026_exact.py` — includes Sabeena Abbasi in WFH — Confirmed, Ali Sipra in onsite.
