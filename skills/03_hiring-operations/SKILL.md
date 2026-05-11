---
name: hiring-operations
description: Manage hiring workflow operations including daily I-10 attendance reports, decision briefs to leadership, and weekly hiring pipeline monitoring. All reports require verified data from Teams/Markaz, locked formatting (colors, stat boxes, no grid borders), and pilot approval before sending.
compatibility: Requires RULES.md, memory attendance templates, Teams API, MCP database access
---

# Hiring Operations

Manage operational reporting and workforce tracking: attendance reports, decision briefs, and pipeline monitoring.

---

## Architecture

**This skill is an orchestration layer** that references the detailed SOPs in `SOPs/03_Hiring_Operations/`.

- **SKILL.md (this file):** Master orchestration, universal rules, execution discipline
- **SOPs folder (source of truth):** Detailed procedures for each operational task

When you use this skill, you get:
1. Universal rules and checklist (from this SKILL.md)
2. Detailed procedures (from linked SOPs — the source of truth)

**Important:** SOPs are maintained as the single source of truth. If procedures change, they update in SOPs/ and are automatically reflected here.

---

## When to Use This Skill

Trigger this skill when:
- User asks for "attendance report" or "I-10 report"
- User requests "decision brief" for position
- User wants "pipeline status" or "hiring monitor"
- User needs "workforce tracking" or "onsite coordination"
- Any operational hiring management task

---

## Related SOPs (Source of Truth)

**Location:** `SOPs/03_Hiring_Operations/`

This skill orchestrates the following detailed procedures:

1. **Attendance Reports** — `SOPs/03_Hiring_Operations/attendance_reports.md`
   - Daily I-10 tracking (onsite, leave, WFH)
   - 7 colored stat boxes (colors LOCKED)
   - NO grid borders on tables (critical)
   - ReportLab PDF + HTML email
   - Teams + Markaz verification required

2. **Decision Briefs** — `SOPs/03_Hiring_Operations/decision_briefs.md`
   - Leadership reports (candidate progress)
   - 4 stat boxes: values calls, interviews, offers, advanced
   - All candidate names linked to Drive CVs (non-negotiable)
   - Sections: leading, discussion, pipeline, debrief schedule
   - Inline HTML (no PDF attachment)

3. **Hiring Pipeline Monitor** — `SOPs/03_Hiring_Operations/hiring-pipeline-weekly-report.md`
   - Proactive monitoring (Mon 10:30am + Fri 3pm)
   - Flags candidates stuck 3+ days
   - Checks all open positions (Markaz + Gmail + Calendar)
   - Sends to both Ayesha + Jawad
   - Auto-generates weekly

4. **Hiring Decision Brief** — `SOPs/03_Hiring_Operations/hiring_decision_brief.md`
   - Variant of decision brief for final hiring decisions
   - Structured recommendation format
   - Leadership-ready presentation

---

## Universal Rules (All Operations)

**Data Verification:**
- Teams data verified with Markaz (not assumed)
- Suspiciously small result sets flagged (verify ground truth)
- No fabrication (use verified sources only)
- Database queries logged (MCP only, never direct)

**Formatting (LOCKED):**
- Attendance: 7 stat boxes, colors #34495e, #e8f5e9, #ffe0b2, etc.
- Decision Brief: 4 stat boxes, CV hyperlinks required
- NO GRID BORDERS (Ayesha corrected this repeatedly)
- Stat box count MUST equal section header count
- Table styling: Helvetica, 9-10pt, alternating colors

**Colors (LOCKED):**
- Header: #34495e (dark)
- Onsite: #e8f5e9 (green)
- Leave: #ffe0b2 (orange)
- WFH: #c8e6c9 (light green)
- Away: #ffccbc (salmon)
- Flagged: #ffcdd2 (red)
- Additional: #f5f5f5 (gray)

**Email Format:**
- Attendance: HTML email with stat table
- Decision Brief: Inline HTML (no PDF)
- Pipeline Monitor: Both in-app notification + email
- Simple message + formatted table

**Self-QA Before Sending:**
- [ ] Memory checked (MEMORY.md)
- [ ] Locked template read side-by-side
- [ ] Data verified (Teams + Markaz cross-reference)
- [ ] Stat boxes = section header count
- [ ] Colors match exactly
- [ ] NO grid borders (CRITICAL)
- [ ] All CV names hyperlinked (if decision brief)
- [ ] Pilot sent to Ayesha first

---

## Execution Discipline

**STEP 1: IDENTIFY OPERATION TYPE**
- Attendance report, decision brief, or pipeline monitor?

**STEP 2: READ LOCKED RESOURCES**
- RULES.md: Skill 4 (Attendance lines 254-288)
- RULES.md: Skill 6 (Decision Brief lines 324-354)
- MEMORY.md: Locked template for type
- Attendance template: `memory/_locked/attendance_report_complete_template.md`

**STEP 3: GATHER DATA**
- Attendance: Query Teams + Markaz for presence/leave
- Decision Brief: Markaz candidate data + interview status
- Pipeline: All open positions + candidate stages + calendar

**STEP 4: VERIFY AGAINST GROUND TRUTH**
- Teams result small? Verify with Markaz manually
- Markaz status unclear? Check email/calendar confirmation
- No assumptions (flag discrepancies)

**STEP 5: STRUCTURE REPORT**
- Attendance: stat boxes → sections → tables
- Decision Brief: stat boxes → sections with hyperlinks
- Pipeline: table → sections → analytics

**STEP 6: APPLY EXACT FORMATTING**
- Colors from locked template (copy exactly)
- Stat boxes: 7 for attendance, 4 for decision brief
- NO GRID BORDERS (use ROWBACKGROUNDS only)
- Tables: Helvetica, 9-10pt font, alternating row colors

**STEP 7: VERIFY STRUCTURE**
- Stat count = section header count (math check)
- All CV names linked to Drive (decision brief)
- No grid borders on ANY table
- Colors match locked values exactly

**STEP 8: RUN 8-ITEM CHECKLIST**
- All 8 items must pass

**STEP 9: PILOT & APPROVE**
- Send pilot to Ayesha (+ Jawad for pipeline monitor)
- Wait for approval
- Send live after approval

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Grid borders on tables | "Not the pattern" (Ayesha corrected) | Use ROWBACKGROUNDS only, no GRID |
| Stat count ≠ section count | Math error, inconsistent | Recount and verify data |
| Wrong colors | Visual mismatch | Use exact hex codes (#34495e, etc.) |
| Teams API assumed | Incomplete API results missed staff | Verify with Markaz database |
| Fabricated attendance | No ground truth check | Query Teams + Markaz, flag discrepancies |
| Missing CV hyperlinks | Decision brief unusable | Hyperlink EVERY name in all sections |
| Unclear status language | "TBC/Pending" vague | Use specific: "Calendar not locked", etc. |
| Sending without pilot | Skips approval process | Always pilot to Ayesha first |
| PDF attachment on brief | Wrong format | Use inline HTML, no attachment |
| No audit logging | No record of queries | Log all DB queries (MCP) |

---

## Success Criteria

✅ Data verified (Teams + Markaz cross-checked)  
✅ Stat boxes = section headers (count correct)  
✅ NO grid borders on any table (critical)  
✅ Colors match locked template exactly  
✅ All CV names linked to Drive (decision brief)  
✅ Format matches locked template side-by-side  
✅ Suspicious data flagged (not assumed)  
✅ Pilot sent to Ayesha first  
✅ All 8-item checklist items pass  
✅ Audit logging in place (DB queries)  

---

## Resources & Templates

**Locked Templates:**
- Attendance Report: `memory/_locked/attendance_report_complete_template.md`
- Decision Brief: `RULES.md` (Skill 6)
- Color codes: All in attendance template

**Reference Scripts:**
- Attendance: `scripts/reports/attendance_20apr2026.py`
- Decision Brief: `scripts/jobs/job32/send_job32_report_v10.py`
- Pipeline Monitor: `scripts/reports/weekly_pipeline_monitor.py`

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)
- Skill 4 (Attendance): `RULES.md` (lines 254-288)
- Skill 6 (Decision Brief): `RULES.md` (lines 324-354)

---

## Commit to Discipline

I will manage hiring operations with:
- ✅ Verified data (Teams + Markaz cross-checked)
- ✅ Exact color codes (locked template)
- ✅ NO grid borders (ROWBACKGROUNDS only)
- ✅ Stat count = section count
- ✅ All CV names linked to Drive
- ✅ No fabrication (flag discrepancies)
- ✅ Format matches locked template
- ✅ Audit logging in place

**Status:** ✅ PRODUCTION READY
