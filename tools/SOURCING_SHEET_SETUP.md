# Sourcing Sheet Setup Guide

## Overview

The sourcing sheet tracks all candidates from discovery through Markaz insertion. It's automatically created when you start a sourcing run for a new role.

---

## Quick Start

### 1. **Create a Master Spreadsheet** (One-Time Setup)

Create a Google Sheet called **"Talent Sourcing Master [Year]"** with one main sheet named "Index" that lists all roles being sourced:

```
Master Spreadsheet: https://docs.google.com/spreadsheets/d/[MASTER_SHEET_ID]/
```

**Index sheet columns:**
- Role Name
- Role Slug (lowercase, hyphens)
- Date Started
- Target Count
- Sheet URL
- Status (Active, Completed, On Hold)

### 2. **Start a New Sourcing Run**

When user says "source candidates for [Role]", the sourcing-sheet-helper automatically:

```javascript
const helper = require('./sourcing-sheet-helper');

const result = await helper.getOrCreateRoleSheet(
  spreadsheetId,     // Master spreadsheet ID
  'product_designer', // Role slug (lowercase, hyphens)
  'Product Designer' // Display title
);

console.log(`✓ Sheet created: ${result.sheetUrl}`);
```

**Output:**
- New sheet named `product_designer` created in master spreadsheet
- Ready for candidate tracking
- Automatically formatted with headers + colors

### 3. **Sheet Structure** (Auto-Created)

Each role sheet has 12 columns:

| Column | Header | Purpose |
|--------|--------|---------|
| A | Name | Full candidate name |
| B | LinkedIn URL | Profile URL (primary dedup key) |
| C | Current Role | Their job title |
| D | Current Company | Where they work now |
| E | Location | City/Country |
| F | Key Experience | 1-2 line summary of relevant experience |
| G | Why Relevant | How they match the JD |
| H | Panel Fit Signal | Observable evidence from profile |
| I | Status | Identified / DM Pending / DM Sent / Responded / Confirmed / In Markaz |
| J | DM Sent | No / Awaiting Ayesha / Yes / [Date] |
| K | Response | Candidate feedback / reply |
| L | Date Added | YYYY-MM-DD |

---

## Step-by-Step Usage During Sourcing

### Phase 1: Search & Identify

**After completing Layer 1/2/3 searches, add candidates to sheet:**

```javascript
const { newCandidates, skippedCount } = await helper.checkDuplicates(
  spreadsheetId,
  'product_designer',
  allCandidatesFound
);

console.log(`✓ Found ${newCandidates.length} new candidates`);
console.log(`⚠ Skipped ${skippedCount} duplicates`);

const added = await helper.addCandidatesToSheet(
  spreadsheetId,
  'product_designer',
  newCandidatesFound
);

console.log(`✓ Added ${added.rowsAdded} candidates to sheet`);
```

**Result:** All candidates added with Status = "Identified", DM Sent = "No"

---

### Phase 2: DM Approval

**When Ayesha picks candidates to DM, mark them as pending:**

```javascript
const approved = [
  { linkedinUrl: 'https://linkedin.com/in/alice-smith', name: 'Alice Smith' },
  { linkedinUrl: 'https://linkedin.com/in/bob-jones', name: 'Bob Jones' }
];

for (const candidate of approved) {
  await helper.updateCandidateStatus(
    spreadsheetId,
    'product_designer',
    candidate.linkedinUrl,
    { status: 'DM Pending', dmSent: 'Awaiting Ayesha' }
  );
}

console.log(`✓ Marked ${approved.length} candidates DM Pending`);
```

**Result:** Status updated to "DM Pending", DM Sent = "Awaiting Ayesha"

---

### Phase 3: DM Sent

**After Ayesha sends DMs, update the sheet:**

```javascript
await helper.updateCandidateStatus(
  spreadsheetId,
  'product_designer',
  'https://linkedin.com/in/alice-smith',
  { 
    status: 'DM Sent', 
    dmSent: '2026-06-03' // Date DM sent
  }
);
```

**Result:** Status = "DM Sent", DM Sent = "2026-06-03"

---

### Phase 4: Response

**When candidate replies, Ayesha tells Coco, and we update the sheet:**

```javascript
await helper.updateCandidateStatus(
  spreadsheetId,
  'product_designer',
  'https://linkedin.com/in/alice-smith',
  { 
    status: 'Responded', 
    response: 'Interested, wants to learn more' 
  }
);
```

**Result:** Status = "Responded", Response = "Interested, wants to learn more"

---

### Phase 5: Confirmed Interest

**When Ayesha confirms: "[Name] confirmed interest, add to Markaz":**

```javascript
// Step 1: Update sheet
await helper.updateCandidateStatus(
  spreadsheetId,
  'product_designer',
  'https://linkedin.com/in/alice-smith',
  {
    status: 'Confirmed',
    response: 'Confirmed interest - added to Markaz',
    dmSent: 'Yes'
  }
);

// Step 2: Insert to Markaz (via insert-confirmed-candidate.js)
const result = await insertConfirmedCandidate(candidate, jobId);

console.log(`✓ Candidate ID: ${result.candidateId}`);
console.log(`✓ Application ID: ${result.applicationId}`);
```

**Result:** Status = "Confirmed", then candidate added to Markaz with source='LinkedIn - Sourced'

---

## Deduplication Logic

**The `checkDuplicates()` function prevents duplicate outreach:**

```javascript
const { newCandidates, skippedCount, duplicates } = await helper.checkDuplicates(
  spreadsheetId,
  'product_designer',
  allCandidatesFromSearch
);
```

**Matching strategy:**
1. LinkedIn URL exact match (primary)
2. Full name exact match (secondary)
3. Company + Current Role combination (tertiary)

**Example:**
- If "Alice Smith" at "Tech Corp" already in sheet → SKIP
- If "https://linkedin.com/in/alice-smith" already in sheet → SKIP
- New candidate with different company/name → ADD

---

## Sheet Status Lifecycle

```
Initial Add
    ↓
[Identified] ← All new candidates start here
    ↓ (Ayesha approves)
[DM Pending] ← Awaiting Ayesha to send LinkedIn DM
    ↓ (Ayesha sends DM)
[DM Sent] ← DM sent on this date
    ↓ (Candidate replies)
[Responded] ← Candidate replied (interested/not interested)
    ↓ (If interested, Ayesha confirms)
[Confirmed] ← Confirmed interest, ready for Markaz
    ↓ (Insert to Markaz)
[In Markaz] ← Candidate ID and Application ID recorded
```

---

## Getting Candidate List by Status

**Retrieve all candidates with a specific status:**

```javascript
const identifiedCandidates = await helper.getCandidatesByStatus(
  spreadsheetId,
  'product_designer',
  'Identified'
);

console.log(`${identifiedCandidates.length} candidates waiting for DM approval`);

identifiedCandidates.forEach(c => {
  console.log(`- ${c.name} (${c.currentCompany}): ${c.panelFitSignal}`);
});
```

**Returns:** Array of candidate objects filtered by status

---

## Integration with Markaz Insertion

**When ready to add confirmed candidate to Markaz:**

```bash
node insert-confirmed-candidate.js \
  --name "Alice Smith" \
  --url "https://linkedin.com/in/alice-smith" \
  --jobId 32 \
  --company "Tech Corp" \
  --position "Senior Product Manager" \
  --location "Islamabad"
```

**Script automatically:**
- Inserts candidate with source='LinkedIn - Sourced'
- Tags with profile_url, sourced_by, sourcing_run
- Creates application with status='new'
- Returns Candidate ID + Application ID

---

## Example: Complete Sourcing Run

### Day 1: Search & Add Candidates

```javascript
const candidates = [
  { name: 'Alice Smith', linkedinUrl: '...', currentRole: '...', ... },
  { name: 'Bob Jones', linkedinUrl: '...', currentRole: '...', ... }
];

const { newCandidates } = await helper.checkDuplicates(
  spreadsheetId, 'product_designer', candidates
);

await helper.addCandidatesToSheet(
  spreadsheetId, 'product_designer', newCandidates
);
// ✓ 2 candidates added with Status: Identified
```

### Day 2: Ayesha Reviews, Picks 1 for DM

```javascript
await helper.updateCandidateStatus(
  spreadsheetId, 'product_designer', 'https://linkedin.com/in/alice-smith',
  { status: 'DM Pending', dmSent: 'Awaiting Ayesha' }
);
// ✓ Alice's status updated to DM Pending
```

### Day 3: Ayesha Sends DM

```javascript
await helper.updateCandidateStatus(
  spreadsheetId, 'product_designer', 'https://linkedin.com/in/alice-smith',
  { status: 'DM Sent', dmSent: '2026-06-03' }
);
// ✓ Alice's status updated to DM Sent
```

### Day 5: Alice Replies

```javascript
await helper.updateCandidateStatus(
  spreadsheetId, 'product_designer', 'https://linkedin.com/in/alice-smith',
  { status: 'Responded', response: 'Very interested! When can we talk?' }
);
// ✓ Alice's status updated to Responded
```

### Day 6: Ayesha Confirms

```
Ayesha: "Alice Smith confirmed interest, add her for Product Designer"

// Update sheet
await helper.updateCandidateStatus(
  spreadsheetId, 'product_designer', 'https://linkedin.com/in/alice-smith',
  { status: 'Confirmed', response: 'Confirmed interest - added to Markaz', dmSent: 'Yes' }
);

// Insert to Markaz
node insert-confirmed-candidate.js \
  --name "Alice Smith" --url "https://linkedin.com/in/alice-smith" \
  --jobId 32 --company "Tech Corp" --position "Senior Product Manager"
  
// ✓ Candidate ID: 5432, Application ID: 8891, Status: new
// ✓ Alice's sheet status: Confirmed
```

---

## Troubleshooting

### **Deduplication Not Working**
- Check: Is LinkedIn URL correct? (exact match required)
- Check: Is candidate name spelled identically? (case-insensitive but exact spelling)
- Solution: Manually review existing sheet rows for similar entries

### **Sheet Not Creating**
- Check: Do you have Google Sheets API credentials configured?
- Check: Does spreadsheetId exist and is it accessible?
- Error message will state specific permission issue

### **Status Update Failed**
- Check: Is LinkedIn URL correct in sheet?
- Check: Is status value valid? (must be exact: "Identified", "DM Pending", "DM Sent", "Responded", "Confirmed", "In Markaz")
- Solution: Run `getCandidatesByStatus()` to verify row data

---

## Sheet Access & Sharing

**Master Spreadsheet Setup:**
1. Create Google Sheet (share with hiring team)
2. Get spreadsheet ID from URL: `docs.google.com/spreadsheets/d/[SHEET_ID]/`
3. Pass SHEET_ID to all sourcing-sheet-helper functions

**Sharing:**
- Ayesha: Editor access (updates Status column)
- Hiring team: Viewer access (track pipeline)
- Coco: Editor access (adds candidates, updates status)

---

## Next Steps

1. **Create Master Spreadsheet** (one-time)
2. **Set SPREADSHEET_ID** in environment or config
3. **Start first sourcing run** → sheet auto-created
4. **Test deduplication** by adding 2 candidates, then same candidate again
5. **Update statuses** as Ayesha confirms DMs, receives responses, confirms interest
6. **Insert to Markaz** when candidate confirmed

**All set!** Sourcing sheet is ready for production use.
