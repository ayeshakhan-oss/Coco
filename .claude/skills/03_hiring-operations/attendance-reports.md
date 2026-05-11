---
name: attendance-reports
description: Daily I-10 office presence tracking. OPL+OWT employees (84 payroll total). 7-section report with stat boxes. Check payroll, Markaz, Teams, on-site list. Flag silent cases.
compatibility: Requires SOPs/03_Hiring_Operations/attendance_reports.md, Teams API, Markaz API, memory/attendance_report_complete_template.md
---

# Attendance Reports

Track daily office presence for I-10 Head Office with verified data from payroll, Markaz, Teams, and on-site lists. Flag silent cases where presence is unaccounted for.

---

## When to Use This Skill

Trigger this skill when:
- User asks for "daily attendance report" or "I-10 report"
- User needs "presence tracking" or "office status"
- Reporting on Mon-Thu (Fridays are organization-wide WFH)
- Need 7-section report with stat boxes
- Recipients: Ayesha + Jawwad + Aymen Abid

---

## Related SOP (Source of Truth)

**Location:** `SOPs/03_Hiring_Operations/attendance_reports.md`

This skill orchestrates the procedure for attendance tracking. The SOP contains:
- 6-step data collection workflow
- 7-section report structure
- Stat box specification (7 colored boxes)
- Silent case flagging rules
- Payroll baseline (84 OPL+OWT employees)
- Team presence channel reading
- Markaz leave record verification
- Quality notes on name accuracy

---

## Universal Rules (All Attendance Reports)

**Data Sources (All Required):**
- Payroll: Previous month's active employee list (baseline: 84)
- Markaz: Active employee names and leave records
- Teams: Presence channel for WFH/leave announcements
- On-Site List: Ayesha's physical presence confirmation
- All sources must be cross-checked

**Payroll Baseline (CRITICAL):**
- Always use PREVIOUS month's payroll count (84 as of 2026-04-09)
- Don't invent or assume employee count
- Flag discrepancies between payroll and other sources

**Reporting Sections (7 Required):**
1. **Onsite** (employees physically in I-10)
2. **Leave** (employees on formal leave)
3. **WFH** (employees working from home)
4. **Out of Office** (OOO status, traveling, etc.)
5. **Arriving** (employees arriving later that day)
6. **Flagged** (silent cases with no recorded status)
7. **WFH — Confirmed Permanent** (8 permanent WFH employees)

**Stat Boxes (7 colored, exact colors locked):**
- Header: #34495e (dark gray)
- Onsite: #e8f5e9 (light green)
- Leave: #ffe0b2 (orange)
- WFH: #c8e6c9 (light green)
- Away: #ffccbc (salmon)
- Flagged: #ffcdd2 (red)
- Additional: #f5f5f5 (gray)

**Silent Case Flagging:**
- Not on Ayesha's on-site list
- Did NOT mention leave/WFH in Teams
- Did NOT mention leave/WFH in Markaz
- Flag with status "No record found"

**Name Accuracy (CRITICAL):**
- Read provided names VERY carefully
- Copy exact spelling and capitalization
- No assumptions or corrections
- Examples: "Muhammad Zeeshan Usaid" vs "Zeeshan Usaid" — match exactly as written

---

## Detailed Procedure

**Data Collection (6 Steps):**

1. **Get Payroll List:** Query Neon DB for previous month's active OPL+OWT employees (baseline: 84 as of 2026-04-09)

2. **Get Markaz Active List:** Query Markaz for active employees + leave records as of reporting date

3. **Check Teams Presence:** Read Teams presence channel for WFH/leave/arrival announcements
   - Look for: "WFH today", "Out sick", "Annual leave", "Arriving at [time]"
   - Extract names EXACTLY as written
   - Use scripts/utils/teams_reader.py

4. **Cross-Check Markaz Leaves:** Query Markaz leave records for reporting date; compare against Teams

5. **Get Ayesha's On-Site List:** Accept her list as ground truth for physical presence
   - Read names VERY carefully (exact spelling)
   - Don't correct or assume — copy exactly
   - Example: "Muhammad Zeeshan Usaid" vs "Zeeshan Usaid" — match exactly as provided

6. **Flag Silent Cases:** For each of 84 employees:
   - On Ayesha's list? → Onsite section
   - Leave marked (Teams/Markaz)? → Leave section
   - WFH marked (Teams/Markaz)? → WFH section
   - No record anywhere? → Flagged section (mark "No record found")

**Report Structure (7 Sections):**
1. Onsite (physically in I-10)
2. Leave (formal leave)
3. WFH (working from home)
4. Away (out of office, traveling)
5. Arriving (arriving later that day)
6. Flagged (silent cases, no record)
7. WFH — Confirmed Permanent (8 permanent WFH employees)

**Stat Boxes (7 colored, LOCKED):**
- Header: #34495e (dark gray)
- Onsite: #e8f5e9 (light green)
- Leave: #ffe0b2 (orange)
- WFH: #c8e6c9 (light green)
- Away: #ffccbc (salmon)
- Flagged: #ffcdd2 (red)
- Additional: #f5f5f5 (gray)

**Format (LOCKED):**
- No grid borders (ROWBACKGROUNDS only)
- Georgia serif, justified
- ReportLab PDF with TA_JUSTIFY
- 7 stat boxes = 7 sections (must match)
- Verify math: sum = 84 employees

---

## Execution Discipline

**STEP 1: IDENTIFY THIS SKILL**
- User says "attendance report" or "I-10 report"
- Mon-Thu reporting (not Friday)

**STEP 2: READ LOCKED RESOURCES**
- memory/attendance_report_complete_template.md: Locked template
- SOPs/03_Hiring_Operations/attendance_reports.md: Full SOP

**STEP 3: GET PAYROLL LIST**
- Query Neon DB for previous month's active OPL+OWT employees
- Baseline: 84 employees (as of 2026-04-09)
- Save list (this is ground truth for count)

**STEP 4: GET MARKAZ ACTIVE LIST**
- Query Markaz for active employees + leave records
- Cross-check names against payroll
- Note leave entries (formal leave record)

**STEP 5: CHECK TEAMS PRESENCE**
- Read Teams presence channel
- Look for WFH, leave, arrival announcements
- Extract names EXACTLY as written
- Note timestamps if available

**STEP 6: GET AYESHA'S ON-SITE LIST**
- Accept Ayesha's list as ground truth for physical presence
- Read names VERY carefully (exact spelling)
- Copy exactly; don't correct or assume

**STEP 7: CROSS-CHECK & FLAG**
- Create 7 sections (Onsite, Leave, WFH, Away, Arriving, Flagged, Permanent WFH)
- For each of 84 employees:
  - On Ayesha's list? → Onsite section
  - Marked leave (Teams/Markaz)? → Leave section
  - Marked WFH (Teams/Markaz)? → WFH section
  - No record anywhere? → Flagged section (mark "No record found")

**STEP 8: VERIFY STAT BOX COUNT**
- 7 stat boxes = 7 section headers (must match)
- Total must account for all 84 employees
- Verify math: onsite + leave + WFH + away + arriving + flagged = 84

**STEP 9: APPLY LOCKED FORMAT**
- Use exact colors from locked template
- 7 colored stat boxes (exact hex codes)
- NO grid borders (ROWBACKGROUNDS only)
- Georgia serif font, justified
- ReportLab PDF format with TA_JUSTIFY

**STEP 10: PILOT & APPROVE**
- Send to Ayesha for approval
- Wait for explicit approval
- Send live to Ayesha + Jawwad + Aymen Abid

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Name accuracy ignored | Wrong person flagged | Read carefully, copy EXACTLY |
| Grid borders on tables | "Not the pattern" | Use ROWBACKGROUNDS only |
| Fabricated data | Invented presence to fill gaps | Query Teams + Markaz, flag unknowns |
| Skipped Teams channel | Missed leave announcements | Check ALL sources (payroll, Markaz, Teams) |
| Wrong colors | Visual mismatch | Use exact hex codes (#34495e, etc.) |
| Stat count ≠ section count | Math error | Recount: 7 boxes = 7 sections |
| Payroll baseline wrong | Off-by-one count errors | Use 84; flag if different |
| Silent cases not flagged | No visibility on unaccounted people | Mark "No record found" for unexplained absences |
| No pilot approval | Skips QA process | Always pilot to Ayesha first |

---

## Success Criteria

✅ All 7 sections present (Onsite / Leave / WFH / Away / Arriving / Flagged / Permanent WFH)  
✅ Stat boxes = section headers (7 each)  
✅ Names match Ayesha's list exactly (no corrections)  
✅ Silent cases flagged (no record found)  
✅ Payroll baseline verified (84 employees)  
✅ NO grid borders (ROWBACKGROUNDS only)  
✅ Colors exact (locked hex codes)  
✅ Pilot sent to Ayesha first  

---

## Self-QA Checklist (Before Pilot)

- [ ] Payroll list retrieved (84 baseline)
- [ ] Markaz active list pulled
- [ ] Teams presence channel read
- [ ] Ayesha's on-site list obtained and names copied EXACTLY
- [ ] All 84 employees cross-checked against all sources
- [ ] 7 sections created (Onsite / Leave / WFH / Away / Arriving / Flagged / Permanent WFH)
- [ ] Silent cases flagged (no record in any source)
- [ ] Stat box count = 7, section count = 7
- [ ] Colors verified (exact hex codes from locked template)
- [ ] No grid borders (ROWBACKGROUNDS only)
- [ ] Names match Ayesha's list exactly
- [ ] Ready for pilot to Ayesha

---

## Resources & Templates

**Locked Template:**
- Attendance Report: `memory/attendance_report_complete_template.md`

**Reference Scripts:**
- Attendance report: `scripts/reports/attendance_*.py`
- Teams reader: `scripts/utils/teams_reader.py`

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)
- Skill 4 (Attendance): `RULES.md` (lines 254-288)

---

## Commit to Discipline

I will generate attendance reports with:
- ✅ All 7 sources checked (payroll, Markaz, Teams, on-site list)
- ✅ Names copied EXACTLY from Ayesha's list
- ✅ Silent cases flagged (no record found)
- ✅ 7 stat boxes with locked colors
- ✅ NO grid borders (ROWBACKGROUNDS only)
- ✅ Stat count = section count
- ✅ Payroll baseline (84) verified
- ✅ Pilot to Ayesha first

**Status:** ✅ PRODUCTION READY
