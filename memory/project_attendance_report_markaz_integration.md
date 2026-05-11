---
name: Attendance Report — Markaz Integration & Pending Leaves (2026-04-14)
description: Integration of Markaz leave_requests database into attendance reports. Queries pending leaves directly from DB. Confirmed 62 total pending leaves. Final report includes pending leaves section.
type: project
---

## Markaz Database Integration — Confirmed Working

### Database Access
- **Host:** ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech
- **Database:** neondb
- **Table:** leave_requests
- **Credentials:** In weekly_pipeline_monitor.py (DB_CONFIG)

### Query Pending Leaves
```python
SELECT u.first_name || ' ' || u.last_name, lr.leave_type, lr.sub_category, 
       lr.start_date, lr.end_date, lr.is_half_day, lr.created_at
FROM leave_requests lr
LEFT JOIN users u ON lr.user_id = u.id
WHERE lr.status = 'pending'
ORDER BY lr.created_at DESC
```

### Pending Leaves Status (14 April 2026)
- **Total pending:** 62 leaves
- **Annual:** 21
- **Medical:** 18
- **Work from Home:** 16
- **Grant:** 7

### Attendance Report Integration
**New Section (10th):** "Pending Leaves/WFH — Submitted, Not Yet Approved"
- Orange header (#ff6f00)
- Light orange rows (#ffe0b2)
- Shows all pending leaves not yet approved in Markaz
- Located before footer in PDF

### Final 14 April Report Structure (10 Sections)
1. Stat Boxes (7)
2. Present Onsite (2-column grid)
3. Arriving Later
4. On Leave
5. Working From Home (conditional)
6. WFH — Confirmed
7. Out of Office
8. Flagged — No Attendance Record
9. Archived/Parked (NIETE)
10. Additional in Attendance — Not OPL+OWT
11. **[NEW] Pending Leaves/WFH** ← Added 2026-04-14

### Approved Leaves Removed from Pending Section
- Mavia — Annual April 1-15 (already approved, in ON_LEAVE)
- Saaim Asif — Annual half-day (approved)

### Script Location
`scripts/reports/attendance_14apr2026.py` — Master template with Markaz integration

### Next Steps
1. Create `scripts/utils/markaz_reader.py` for automated pending leaves queries
2. Wire into weekly_pipeline_monitor.py for auto-flagging
3. Add Markaz API error handling (connection timeouts, auth refresh)
