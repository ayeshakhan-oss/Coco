---
name: Attendance Report — Permanent WFH Section (2026-04-09)
description: Attendance report includes new "Permanent WFH — Confirmed" section distinct from temporary WFH. 8 permanent WFH employees exclude from onsite count. Updated script with 8 stat boxes.
type: project
---

## Permanent WFH Section (Added 2026-04-09)

**Update:** Attendance report now includes a distinct "Permanent WFH — Confirmed" section for employees on confirmed permanent remote arrangements.

### The 8 Permanent WFH Employees
1. Amina Tayyub
2. Zuhaib Shaikh
3. Ajlal Hasan
4. Zeest Hassan Qureshi
5. Ahwaz Akhtar
6. Shayan Ahmad
7. ABDUL AHAD
8. Zulfiqar Ahmed Mughal

### Design
- Section header: "WFH — Confirmed (8)" with blue background (#1565c0)
- Table: Name | Status columns (status = "Permanent remote arrangement")
- Styling: Same as Remote/Blue sections — navy header, light blue/white alternating rows
- Stat box: Added "WFH Confirmed" as 5th stat box (light blue #e3f2fd), positioned between WFH and Arriving Later
- Total stat boxes: **8** (was 7)

### Key Rule
Permanent WFH employees are **excluded from onsite count** in the filtering logic. They are NOT present at the office.

### Reference Script
`scripts/reports/attendance_9apr2026_exact.py` — final working version with permanent WFH section integrated

### Context
User instruction (2026-04-09): "these people are permanent wfh, you must add this heading" — referring to the 8 employees from the 8 April reference PDF who need their own distinct section to differentiate from temporary WFH (unlogged/not in system) and H-9 office workers.
