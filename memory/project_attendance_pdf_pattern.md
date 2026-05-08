---
name: Attendance Report PDF — Exact Pattern & Colors (Reference: 8 Apr 2026)
description: ReportLab PDF format for I-10 attendance reports. Stat boxes with specific colors, 2-column onsite grid, Name|Status tables. MUST match exactly.
type: project
---

## PDF Format (Confirmed 2026-04-09)

**Reference:** Temp/Attendance Record 8 Apr 2026 (1).pdf

### Header
- Dark navy background (#1a2a3a)
- Top line: "PEOPLE & CULTURE · ATTENDANCE MONITOR" (gray, small)
- Title: "I-10 Head Office Attendance Record" (white, bold, large ~24px)
- Subtitle: "9 April 2026 (Thursday) · Onsite Day (Mon–Thu)" (light blue #90caf9)
- Padding: 14mm around

### Stat Boxes (7 boxes in 1 row)
Each box has colored background + bordered grid:
1. **Total Active** — light gray (#f5f5f5)
2. **Onsite Today** — light green (#e8f5e9)
3. **On Leave** — light orange (#fff3e0)
4. **WFH** — light brown (#fff8f0)
5. **Arriving Later** — light yellow (#fffde7)
6. **Remote** — light blue (#e3f2fd)
7. **Flagged** — light pink (#ffebee)

Each box: big bold number (24px) + small label below, centered, 8mm padding, 0.5mm border in #e0e0e0

### Onsite Section
- Header: green background (#1a7a4a), white text "Present Onsite — I-10 Head Office (55)", 8mm padding, 8mm left padding
- Grid: **2 columns** showing names only (no status)
- Alternating rows: light green (#e8f5e9) / white
- Padding: 7mm all sides
- Border: 0.5mm #e0e0e0

### Other Sections (Arriving Later, On Leave, WFH, Remote, Flagged)
- Header: colored bar matching category:
  - Arriving Later: orange (#e65100)
  - On Leave: orange (#e65100)
  - WFH: brown (#7b341e)
  - Remote: blue (#1565c0)
  - Flagged: red (#c62828)
- Header: white bold text, 8mm padding, 8mm left padding
- Table: 2 columns (Name | Status)
  - Header row: dark navy (#1a2a3a), white text
  - Data rows: alternating light gray (#f9f9f9) / white
  - Padding: 6mm, 8mm left
  - Border: 0.5mm #e0e0e0

### Footer
- Two-column layout:
  - Left: "Taleemabad People & Culture · hiring@taleemabad.com · [DATE]"
  - Right: "Compiled by Coco, Nugget & Noah · People & Culture AI Assistants"
- Font: 8px gray (#999999)
- Border: 0.5mm #e0e0e0

### Reference Script
`scripts/reports/attendance_9apr2026_correct.py` — matches 8 April pattern exactly.

### Key Rules
- NO colored stat boxes at corners — individual boxes in a row
- Onsite is NAME-ONLY 2-column grid, NOT Name|Status table
- All section headers use solid colored bars (not outlined)
- Stat box numbers 24px, labels 8px
- Title 24px bold white, subtitle 11px light blue
- Always use these exact colors — DO NOT deviate
