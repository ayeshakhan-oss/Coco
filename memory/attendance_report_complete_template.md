---
name: Attendance Report Template (Complete)
description: Full ReportLab PDF + HTML email template for daily I-10 attendance reports. Colors, layouts, stat boxes, tables—everything locked in.
type: reference
---

# Attendance Report — Complete Template (LOCKED)

**User:** Ayesha Khan  
**Report Date:** Daily (20 April 2026 is reference example)  
**Format:** ReportLab PDF + HTML email with stat boxes  
**Status:** FINAL—do not deviate

---

## STAT BOX COUNTS & COLORS

| Category | Count | Color Code | RGB |
|----------|-------|-----------|-----|
| Total Active | 84 | #f5f5f5 | Light gray |
| Onsite Today | 52 | #e8f5e9 | Light green |
| On Leave | 6 | #ffe0b2 | Light orange |
| WFH | 12 | #e3f2fd | Light blue |
| WFH Confirmed | 7 | #f3e5f5 | Light purple |
| Additional | 6 | #f3e5f5 | Light purple |
| Flagged | 1 | #ffebee | Light red |

**Note:** Counts change per day; structure/colors remain identical.

---

## HEADER & TITLE COLORS (LOCKED)

| Element | Color Code | Purpose |
|---------|-----------|---------|
| Header bar | #34495e | Dark slate (top "PEOPLE & CULTURE ATTENDANCE MONITOR") |
| Title section | #34495e | Dark slate (title + date) |
| Table headers | #34495e | Dark slate (all section headers: Onsite, Leave, WFH, etc.) |

**Onsite section header:** #2e7a4f (dark green)  
**Leave section header:** #f57c00 (orange)  
**WFH section header:** #1565c0 (dark blue) — Teams-announced people
**WFH Confirmed header:** #1565c0 (dark blue)  
**Away section header:** #7b68ee (medium purple) — NEW (2026-04-20)
**Flagged header:** #c62828 (dark red)  
**Additional header:** #6a1b9a (dark purple)

---

## TABLE STYLING RULES (CRITICAL)

### Onsite Table (2-column layout)
- **Font:** Helvetica-Bold, 10pt
- **Grid:** NONE (no borders)
- **Row colors:** White, #e8f5e9 (alternating)
- **Padding:** 8px left/right, 6px top/bottom
- **Alignment:** LEFT

### Leave/WFH/Flagged/Additional Tables
- **Font:** Helvetica-Bold header, 9pt body
- **Grid:** NONE (no borders)
- **Header row:** Dark background (#34495e), white text
- **Row colors (data rows):** White + section color (alternating)
  - Leave: white + #ffe0b2
  - WFH: white + #e3f2fd
  - Flagged: white + #ffebee
  - Additional: white + #f3e5f5
- **Padding:** 8px left/right, 6px top/bottom
- **Alignment:** LEFT

**CRITICAL:** NO GRID LINES on ANY table. User has corrected this multiple times.

---

## STAT BOX LAYOUT (HTML EMAIL)

```html
<table style="width: 100%; border-collapse: collapse;">
  <tr>
    <td style="padding: 20px; text-align: center; background-color: #f5f5f5;">
      <div style="font-size: 24px; font-weight: bold;">84</div>
      <div style="font-size: 12px;">Total Active</div>
    </td>
    <!-- Repeat for each stat box with matching color codes above -->
  </tr>
</table>
```

**Email body:** "Hi Ayesha, This is today's attendance report." (simple, no embellishment)

---

## PDF STRUCTURE (REPORTLAB)

1. **Header table** (1 row): "PEOPLE & CULTURE · ATTENDANCE MONITOR"
2. **Title table** (3 rows): Title + date info
3. **Spacer** (0.12 inch)
4. **Stat boxes table** (1 row, 7 columns): All 7 stat boxes with colors
5. **Spacer** (0.18 inch)
6. **Onsite section** (header + 2-column grid of names)
7. **Spacer** (0.12 inch)
8. **Leave section** (header + 2-column table: Name | Status)
9. **Spacer** (0.12 inch)
10. **WFH section** (header + 2-column table: Name | Teams announcement status) — TEAMS-ANNOUNCED people only
11. **Spacer** (0.12 inch)
12. **WFH Confirmed section** (header + 2-column table: Name | Permanent remote arrangement)
13. **Spacer** (0.12 inch)
14. **Away section** (header + 2-column table: Name | Reason) — NEW (2026-04-20)
15. **Spacer** (0.12 inch)
16. **Flagged section** (header + 2-column table: Name | No attendance record)
17. **Spacer** (0.12 inch)
18. **Additional section** (header + 2-column table: Name | NIETE status)
19. **Spacer** (0.12 inch)
20. **Footer** (gray text, size 8)

---

## KEY DISCIPLINE RULES (FROM CORRECTIONS)

1. **No fabrication.** Use ONLY verified data from user.
2. **Stat box count ↔ section header count must match.** If stat says "52 Onsite", section header MUST say "(52)".
3. **Table grid borders = banned.** User corrected this twice. Use ROWBACKGROUNDS only.
4. **Header color #34495e** across all sections (title, table headers).
5. **Onsite color #2e7a4f** for Onsite section header specifically.
6. **Email body minimal:** Just greeting + stat table in HTML. No bullet points, no verbose summary.

---

## DATA CATEGORIES (ALWAYS IN THIS ORDER)

1. Onsite (verified list from user — OPL+OWT only)
2. On Leave (verified leave names + leave reason in Status column)
3. WFH (verified Teams announcements: "Working remotely", "WFH", etc. + reason)
4. WFH Confirmed (7 permanent remote workers + "Permanent remote arrangement")
5. Away (special activities like fundraising, conferences, etc.)
6. Flagged (no attendance record)
7. Additional (NIETE archived/parked, onsite I-10)

**Math check:** Onsite + Leave + WFH (announced) + WFH Confirmed + Away + Flagged + Additional = 84 total.
**Note:** WFH stat box = all WFH (dynamic + permanent). WFH section = only announced on Teams.

---

## COMMON ERRORS TO AVOID (PAST FAILURES)

| Error | Correction |
|-------|-----------|
| Forgot to update section headers when data changed | Always sync stat box count with section header count |
| Grid borders on tables | Remove all GRID styling; use only ROWBACKGROUNDS |
| Header color mismatch | Use #34495e for main header + title + all table headers |
| Fabricated WFH/Flagged lists | Wait for user to provide verified data; calculate remainder only |
| Onsite stat showing total (57) instead of OPL+OWT only (51) | Keep separate; user provides verified list |
| Email body too verbose | Simplify to: "Hi Ayesha, This is today's attendance report." + stat table |

---

## SCRIPT LOCATIONS

- **PDF generation:** `scripts/reports/attendance_20apr_final.py`
- **Email send:** `scripts/reports/send_attendance_20apr.py`
- **Output PDF:** `Attendance_20Apr2026_I10.pdf` (root)

---

## NEXT TIME (TOMORROW)

**Step 1:** Read this memory file first.  
**Step 2:** User will provide data (onsite list, leave names, WFH Confirmed, flagged/additional).  
**Step 3:** Update stat values and data lists in script.  
**Step 4:** Run PDF generation → send email.  
**Step 5:** DO NOT skip this memory file.

---

**Last Updated:** 2026-04-20 (Final)  
**Locked by:** Ayesha (user), Coco (agent)  
**Status:** FINAL—includes Away section, WFH (Teams-announced), full structure. Ready for production.

**April 20, 2026 Reference Report:**
- Onsite: 47 (OPL+OWT, NIETE removed)
- On Leave: 6
- WFH (announced): 7 
- WFH Confirmed: 7
- Away: 1 (Haroon Yasin — fundraising)
- Flagged: 1
- Additional: 6 (NIETE)
- **Total: 84**
