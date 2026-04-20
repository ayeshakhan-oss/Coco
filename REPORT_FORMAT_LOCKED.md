---
name: Screening Report HTML Format (LOCKED)
description: Gmail-safe HTML format for all CV screening reports. Locked after Soul Architect pilot (2026-04-20). All future reports MUST use this exact structure.
type: reference
---

# SCREENING REPORT HTML FORMAT — LOCKED

**Status:** LOCKED (2026-04-20)  
**Reference Report:** soul_architect_screening_pilot_2026-04-20_FINAL.html  
**Reference Email:** April 6, 2026 (3:32 PM) Soul Architect screening to Waqas Tanveer  

## Core Principle

**All future screening reports MUST use this exact HTML structure.** No variations. No improvements. No regressions.

This format has been tested and validated to:
1. Render perfectly in Gmail (no stripping of content)
2. Display all candidate profiles with proper spacing
3. Show all tables (Maybe, Product Manager) without corruption
4. Handle special characters correctly (em-dashes, middle-dots)

## HTML Structure (EXACT)

### Document Setup
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Georgia, serif; font-size: 14px; color: #1a1a1a; max-width: 700px; margin: auto; background: #f0f4f0; padding: 24px 0;">
<table width="700" cellpadding="0" cellspacing="0" style="background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin: 0 auto;">
```

### Header Section
- Dark navy background: `#1a2a3a`
- Three lines of text:
  1. Small gray uppercase: "People &amp; Culture &middot; Initial Screening Report"
  2. Large bold white: "Soul Architect / Conversational UX Designer"
  3. Smaller light blue: "Job 26 &middot; Taleemabad"

### Stat Boxes (4 boxes in row)
- **Box 1 (Red):** `#fce4ec` background, `#c62828` text
- **Box 2 (Blue):** `#e3f0fb` background, `#1565c0` text
- **Box 3 (Yellow):** `#fff8e1` background, `#f57f17` text
- **Box 4 (Gray):** `#f5f5f5` background, `#636e72` text

Each box: 22px number + 11px label text, centered alignment

### Section Headings (consistent across report)
- Font: 15px, bold, blue (`#1565c0`)
- Bottom border: 2px solid `#1565c0`
- Padding: 5px on bottom
- Margin: 28px top, 8px bottom

### Candidate Profile Blocks (repeating for each candidate)
```html
<table width="100%" cellpadding="0" cellspacing="0" 
       style="margin-bottom: 16px; background: #f7f9fc; 
              border-left: 4px solid #c62828; 
              border-radius: 0 6px 6px 0;">
```

**Per candidate:**
1. **Header row** (14px bold): "N. [Name] [#X — TOP PICK or SHORTLIST] [Match %]"
2. **Details row** (11px gray): "App ID: ... | Total exp: ... | Relevant exp: ... | DB status: ..."
3. **Description row** (13px, justified): 2-3 sentences about candidate
4. **Gap row** (12px, brown color `#7b341e`): "Gap: [specific gap]"

### Tables (Maybe & Product Manager)
- Header row: light blue background `#e8f0fb`, bold blue text `#1565c0`
- Alternating rows: white and `#f7f9fc`
- All cells: 1px solid border `#dfe6e9`, 8px 10px padding
- Font: 13px throughout

### Footer Section
- Background: `#f5f5f5`
- Text: 11px, gray (`#999`)
- Top border: 1px solid `#ddd`
- Padding: 20px
- Content: "Taleemabad Talent Acquisition | hiring@taleemabad.com | [DATE] | [MODE]"

## Special Characters (CRITICAL)

**ALL special characters MUST be HTML entities:**
- Em-dash: `&mdash;` (not `—`)
- Middle-dot: `&middot;` (not `·`)
- Ampersand: `&amp;` (not `&`)

This prevents Gmail from rendering Unicode as corrupted text (`â€"` instead of `—`).

## CSS Inline Styles (DO NOT use external stylesheets)

All styling must be inline in `style=""` attributes.

Critical styles:
- `text-align: justify` for paragraphs
- `font-family: Georgia, serif` throughout
- `line-height: 1.7` for readability
- `color: #1a1a1a` for body text
- `color: #1565c0` for headings

## Content Order (MANDATORY)

1. Header (dark navy, 3 lines)
2. Greeting ("Hi [Recipient],")
3. Stat boxes (4 boxes)
4. Key Observation section
5. Shortlisted Candidates section
   - Intro line ("All X read and evaluated...")
   - Repeating candidate blocks (N. Name ... Gap ... DB status warning if needed)
6. Maybe / Consider section (table format)
7. Product Manager Experience section (table format, if applicable)
8. Screening Methodology section
9. Footer

## File Naming Convention

```
soul_architect_screening_pilot_2026-04-20_FINAL.html
[position-slug]_screening_[pilot-or-live]_[YYYY-MM-DD]_FINAL.html
```

Always end with `_FINAL.html` to indicate locked format.

## Generation Process

When generating a new screening report:

1. **Copy the locked HTML template** from `soul_architect_screening_pilot_2026-04-20_FINAL.html`
2. **Replace ONLY the content:**
   - Header: job title, job number, organization
   - Greeting: recipient name
   - Stat boxes: numbers only (keep colors/styles identical)
   - Key Observation: paragraph text
   - Candidate blocks: repeat 5 times, fill with new candidate data
   - Maybe table: repeat rows for each maybe candidate
   - Product Manager table: repeat rows for PM-adjacent candidates
   - Screening Methodology: paragraph text (usually same as original)
   - Footer: date and mode
3. **Verify all special characters** are HTML entities
4. **DO NOT modify:**
   - Any CSS styles
   - Table structure
   - Section heading styles
   - Color values
   - Font sizes
   - Spacing/margins/padding

## Validation Checklist

Before sending ANY screening report:

- [ ] HTML validates (no broken tags)
- [ ] All special characters are HTML entities (`&mdash;`, `&middot;`, `&amp;`)
- [ ] All 5 candidate profiles present and complete
- [ ] Maybe table shows all candidates
- [ ] Product Manager table shows all PM-adjacent candidates (if applicable)
- [ ] Header matches job details
- [ ] Stat box numbers match candidate counts
- [ ] Footer has correct date and mode (PILOT or LIVE)
- [ ] All hyperlinks work (if CVs linked)
- [ ] No divs used (tables only for Gmail safety)
- [ ] Test in Gmail web client before sending to stakeholders

## NO EXCEPTIONS

This format is locked. All future screening reports MUST use this exact HTML structure.

If changes are needed (colors, fonts, spacing), those changes must be:
1. Approved by Ayesha Khan explicitly
2. Tested in Gmail before rolling out
3. Documented in a new "Format Update" section below
4. Applied to ALL future reports immediately (no partial rollouts)

---

## Format Updates

*None yet (2026-04-20)*
