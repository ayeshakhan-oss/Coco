# Google Sheets Template — Talent Sourcing Master

## Quick Setup (5 minutes)

### Step 1: Create Master Spreadsheet

1. Go to **Google Sheets** (sheets.google.com)
2. Click **"+ Create new spreadsheet"**
3. Name it: `Talent Sourcing Master 2026`
4. Click "Create"

### Step 2: Set Up Index Sheet

In the first sheet (rename to "Index"), create these columns:

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Role Name | Role Slug | Date Started | Target Count | Sheet URL | Status |
| Fundraising & Partnerships Manager | fundraising-partnerships-manager | 2026-06-03 | 15 | [Will auto-fill] | Active |
| Full Stack Lead | full-stack-lead | [Date] | 10 | [Will auto-fill] | Active |

**Format Index sheet:**
- Header row: Bold + blue background (#1F4E78)
- Column widths: Auto-fit

### Step 3: Get Your Spreadsheet ID

1. Copy the URL from your browser
2. Extract the ID from this part: `docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`

**Example:**
```
URL: https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0j/edit#gid=0
ID:  1a2b3c4d5e6f7g8h9i0j
```

### Step 4: Share with Coco

1. Click **"Share"** button (top right)
2. Add email: `[coco-service-account-or-email]`
3. Give **Editor** access
4. Click "Share"

---

## Automatic Sheet Creation

When you ask Coco to "source candidates for [Role]", the sourcing-sheet-helper automatically:

1. **Creates** a new sheet named `[role-slug]` inside your master spreadsheet
2. **Adds** column headers (Name, LinkedIn URL, Current Role, Company, Location, Key Experience, Why Relevant, Panel Fit Signal, Status, DM Sent, Response, Date Added)
3. **Formats** the header row (blue background, bold text)
4. **Updates** Index sheet with sheet URL

**You don't need to do anything** — just provide the Spreadsheet ID once at the start.

---

## Example Master Spreadsheet Structure

After running 3 sourcing projects, your master spreadsheet looks like:

### Sheet 1: "Index"
| Role Name | Role Slug | Date Started | Target Count | Sheet URL | Status |
|-----------|-----------|-------------|--------------|-----------|--------|
| Fundraising & Partnerships Manager | fundraising-partnerships-manager | 2026-06-03 | 15 | [URL to fundraising-partnerships-manager sheet] | Completed |
| Full Stack Lead | full-stack-lead | 2026-06-04 | 10 | [URL to full-stack-lead sheet] | Active |
| Product Designer | product-designer | 2026-06-05 | 12 | [URL to product-designer sheet] | Active |

### Sheet 2: "fundraising-partnerships-manager"
| Name | LinkedIn URL | Current Role | Company | Location | Key Experience | Why Relevant | Panel Fit Signal | Status | DM Sent | Response | Date Added |
|------|---|---|---|---|---|---|---|---|---|---|---|
| Zia Akhter Abbas | https://linkedin.com/in/... | President & CEO | TCF | Islamabad | 10+ years global resource mobilization | ... | "Led TCF's global resource mobilisation efforts for 10 years" | Confirmed | Yes | Confirmed interest - added to Markaz | 2026-06-03 |
| Zahra Ahmed | https://linkedin.com/in/... | Board Member | Teach For Pakistan | Islamabad | 3 years head of partnerships | ... | "Spearheading corporate and government partnership development" | DM Sent | Yes | Interested, wants to learn more | 2026-06-03 |
| Akhtar Iqbal | https://linkedin.com/in/... | CEO | AKF Pakistan | Islamabad | Manages €35M EU program | ... | "Manages €35M EU bilateral program + multilateral partnerships" | Identified | No | | 2026-06-03 |

### Sheet 3: "full-stack-lead"
(Similar format, different candidates)

---

## Setting Environment Variable (Optional)

Once you have your Spreadsheet ID, you can set it as an environment variable so you don't have to provide it each time:

**On Mac/Linux:**
```bash
export TALENT_SOURCING_SPREADSHEET_ID="1a2b3c4d5e6f7g8h9i0j"
```

**On Windows (PowerShell):**
```powershell
$env:TALENT_SOURCING_SPREADSHEET_ID="1a2b3c4d5e6f7g8h9i0j"
```

**In .env file (if using dotenv):**
```
TALENT_SOURCING_SPREADSHEET_ID=1a2b3c4d5e6f7g8h9i0j
```

Then in sourcing-sheet-helper calls:
```javascript
const spreadsheetId = process.env.TALENT_SOURCING_SPREADSHEET_ID;
```

---

## Workflow with Sheets

### Day 1: Start Sourcing
```
You: "Source candidates for Fundraising & Partnerships Manager"

Coco:
1. Creates new sheet "fundraising-partnerships-manager" in your master spreadsheet
2. Runs 3-layer search
3. Adds 7 candidates with Status: "Identified"
4. Shows you the candidate slate
5. Updates Index sheet with sheet URL

Your master spreadsheet now has:
- Sheet "Index" with new row linking to fundraising-partnerships-manager sheet
- Sheet "fundraising-partnerships-manager" with 7 candidates ready for review
```

### Day 2: DM Approval
```
You: "Which ones should I DM?"

You select: Alice, Bob, Carol

Coco:
1. Updates their Status to "DM Pending"
2. Updates DM Sent to "Awaiting Ayesha"

Sheet now shows:
- Alice, Bob, Carol: Status = "DM Pending"
- David, Eva, Frank, Grace: Status = "Identified"
```

### Day 3: DMs Sent
```
Coco updates sheet:
- Alice, Bob, Carol: Status = "DM Sent", DM Sent = "2026-06-04"
```

### Day 5: Responses Arrive
```
You: "Alice and Bob replied interested"

Coco:
1. Updates Alice: Status = "Responded", Response = "Interested in learning more"
2. Updates Bob: Status = "Responded", Response = "Very interested!"

Sheet now shows their replies
```

### Day 6: Confirm Interest
```
You: "Alice confirmed interest, add her to Markaz for Fundraising & Partnerships Manager job"

Coco:
1. Updates Alice: Status = "Confirmed"
2. Inserts to Markaz: Candidate ID 5432, Application ID 8891
3. Confirms: "✓ Alice Smith added to Markaz (ID 5432)"

Sheet now shows Alice: Status = "Confirmed"
```

---

## Summary

- **Setup time:** 5 minutes (create sheet, get ID, share)
- **Per-role sheets:** Auto-created by sourcing-sheet-helper.js
- **No manual column creation:** Headers added automatically
- **Full tracking:** Identified → DM Pending → DM Sent → Responded → Confirmed → In Markaz
- **Reusable:** Master spreadsheet tracks all sourcing projects

---

## Next Steps

1. **Create** the Google Sheet above
2. **Get** the Spreadsheet ID
3. **Tell Coco:** "My Talent Sourcing spreadsheet ID is: [ID]"
4. **Start sourcing:** "Source candidates for [Role]"

Done! Coco handles the rest.
