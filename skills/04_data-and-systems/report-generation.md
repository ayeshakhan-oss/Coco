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

## Detailed Procedure

**Step 1: Locate Locked Template**
- Find relevant locked template file in memory/:
  - CV screening: `REPORT_FORMAT_LOCKED.md`
  - Attendance reports: `memory/attendance_report_complete_template.md`
  - Decision briefs: `memory/feedback_decision_brief_hyperlinks.md`
  - Warm bench emails: `memory/warm_bench_final_locked_approach.md`
- Open template side-by-side with current task
- Study format, colors, fonts, structure BEFORE starting

**Step 2: Gather Verified Data**
- Source 1: Database query via MCP (`mcp__neon-postgres__query()`)
- Source 2: User-provided input (CSV, spreadsheet, email)
- Cross-reference sources — flag discrepancies
- Mark any missing data as "Not mentioned" (never fabricate)

**Step 3: Build Report Structure (By Type)**
- **ReportLab PDFs:** Use Table with ROWBACKGROUNDS, no grid borders, TA_JUSTIFY for body text, locked colors
- **HTML Emails:** Use inline HTML (no PDF), Georgia serif, justified alignment, locked color scheme
- **Dynamic Data:** Insert candidate names, scores, dates dynamically from verified sources
- Match template exactly — no variations

**Step 4: Format & Typography**
- PDF body text: `TA_JUSTIFY` alignment
- Email body: Georgia serif, justified
- No em dashes (replace with period, comma, or semicolon)
- No special characters (use HTML entities like `&mdash;`, `&nbsp;`)
- Hyperlinks: test 2-3 to verify they load

**Step 5: Data Insertion**
- For candidate names: hyperlink to Google Drive CV if required
- For scores: use exact values from database (not rounded)
- For dates: format consistently (YYYY-MM-DD)
- For currency: match existing format (PKR/USD with specific precision)

**Step 6: Generate Output**
- **PDF:** Use ReportLab with `doc.build(elements)` → save to `output/YYYY-MM-DD-[name].pdf`
- **HTML:** Build as inline HTML string → save to `output/YYYY-MM-DD-[name].html`
- **Excel:** Save candidate data to `.xlsx` with multiple sheets if needed

**Step 7: Quality Audit**
- Colors match locked template (sample 2-3 stat boxes)
- Fonts correct (Georgia serif for email, specific font for PDF)
- Spacing consistent (margins, padding, line-height)
- No fabricated data
- All names hyperlinked (if required)

**Step 8: Pilot & Approval**
- Send pilot version to Ayesha only (not live recipients)
- Wait for approval or requested changes
- After approval: set `pilot=False` and send to live recipients

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
