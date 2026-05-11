---
name: report-generation
description: Generate reports via ReportLab (PDFs) or HTML templates. Dynamic data insertion. Justified text formatting. Export to spreadsheet/JSON.
compatibility: Requires ReportLab, HTML templates, memory/locked_templates_index.md
---

# Report Generation

Generate reports via ReportLab (PDF) or HTML email templates with dynamic data insertion and proper formatting.

---

## When to Use This Skill

Trigger this skill when:
- User asks to "generate report" or "create PDF"
- Report format is locked (CV screening, attendance, decision brief, etc.)
- Need to insert dynamic data into template
- Output: PDF or HTML email

---

## Related SOP

**Location:** `SOPs/04_Data_and_Systems/report_generation.md`

---

## Universal Rules

**Report Generation (By Type):**
- ReportLab for PDFs (attendance reports, etc.)
- HTML templates for emails (feedback, briefs, etc.)
- Dynamic data insertion (candidate names, scores, etc.)
- Locked template format (no variations)

**Text Formatting (Mandatory):**
- PDF body text: use TA_JUSTIFY (justified alignment)
- Email body: Georgia serif, justified
- No em dashes (replace with period/comma)
- No special characters (use HTML entities)

**Template Lock (Strict):**
- Format locked after approval
- No regressions (format maintained)
- No variations or improvements
- Audit format before sending

**Data Binding:**
- Insert only verified data (from DB or input)
- No fabrication
- Flag missing data (mark "Not mentioned")
- Cross-reference sources

---

## Execution Discipline

1. Find locked template (REPORT_FORMAT_LOCKED.md, etc.)
2. Read template side-by-side
3. Gather verified data (DB query, input file)
4. Insert data into template
5. Verify formatting (colors, fonts, spacing)
6. Generate output (PDF or HTML)
7. Audit before sending
8. Pilot to Ayesha

---

## Success Criteria

✅ Used locked template  
✅ Data verified (not fabricated)  
✅ Format matches template exactly  
✅ Text justified (TA_JUSTIFY for PDF)  
✅ No special character issues  
✅ Pilot sent to Ayesha  

**Status:** ✅ PRODUCTION READY
