---
name: talent-sourcing
description: Proactively search for experienced passive candidates via org pages, Google, LinkedIn. Build persona briefs from panel transcripts. Draft personalized LinkedIn DMs. Track candidates in sourcing sheet. Add confirmed-interested candidates to Markaz. Trigger when user says "source candidates for [role]", "find people for [role]", "build a candidate slate", or "run a talent search".
compatibility: Requires Google Sheets API, Markaz Postgres, WebFetch tool, persona brief methodology from panel transcripts
---

# Talent Sourcing — Comprehensive Passive Candidate Pipeline

End-to-end systematic sourcing: search → persona brief → candidate slate → personalized outreach → sheet tracking → Markaz insertion (after interest confirmed).

---

## When to Use This Skill

Trigger this skill when:
- User says "source candidates for [role]"
- User requests "find people for [position]" or "build a candidate slate"
- User wants to run a passive talent search
- User asks "who should we be approaching for [role]"

---

## The Workflow (Overview)

```
Step 0 (Intake) → Step 0.5 (Persona Brief) → Step 0.8 (Create Sheet)
→ Step 1 (Platform Selection) → Step 2 (3-Layer Search)
→ Step 3 (Extract Profiles) → Step 4 (Present Slate)
→ Step 4.5 (Add to Sheet) → [Ayesha approves]
→ Step 5 (Draft DMs) → Step 5.5 (Mark Pending)
→ [Ayesha sends, candidate responds]
→ Step 7 (Add Confirmed to Markaz)
```

**Critical Rule:** Markaz is ONLY touched after confirmed interest. Never speculatively.

---

## Non-Negotiable Rules

1. **Never add to Markaz before confirmed interest** — the whole point is to contact first, get a YES, then add. Premature additions pollute the pipeline.

2. **Sourcing sheet is the source of truth** — all candidates tracked from Identified → Confirmed → In Markaz. Status updates mandatory.

3. **Persona brief comes first** — before running a single search, understand what KIND of person passes the panel. The JD tells you skills; the persona tells you who will actually succeed.

4. **All 3 layers required** — Layer 1 (org pages), Layer 2 (Google), Layer 3 (LinkedIn verify). Skip none.

5. **DMs are personalized** — never templated. Reference their specific work, project, or experience trajectory.

6. **Ayesha sends manually** — no API integration for LinkedIn DMs. Coco drafts, Ayesha sends, Coco updates sheet when she reports back.

7. **Location: Pakistan-based default** — source diaspora only if explicitly requested.

8. **Platform selection by role** — don't search all platforms equally. Use the role-based selection table to focus Tier 1 (highest yield) first.

9. **Deduplication before slate** — check sheet for existing candidates before presenting new ones.

10. **Source tracking always** — every candidate in Markaz must have `source='LinkedIn - Sourced'` and `tags.profile_url` with actual profile link.

---

## Detailed Procedure (9 Steps)

### STEP 0: Intake
Collect before you search:
1. **Role title** (exact)
2. **Top 3-5 must-have skills** or experiences
3. **Seniority level** (e.g. "8+ years", "senior", "mid-level")
4. **Target candidate count** (default: 10-15 for slate)
5. **Sourcing sheet ID** (ask: "Do you have a Talent Sourcing tracker sheet?" If not: create one using sourcing-sheet-helper.js)

Then read the JD from Markaz:
```sql
SELECT id, title, jd_text, required_skills, department
FROM jobs
WHERE title ILIKE '%[role]%' AND status = 'published'
LIMIT 1;
```

### STEP 0.5: Build Persona Brief (CRITICAL)
**Do this before running a single search query.**

The JD tells you WHAT skills. The persona brief tells you WHO passes the panel. These are different.

If a panel transcript or interview debrief is available, extract:

| Dimension | What to look for in transcript |
|-----------|------|
| **Signal detection** | Did the panel probe forward-looking thinking? Pattern recognition? Market awareness before the fact? |
| **Strategic translation** | Did they test whether technical/functional knowledge gets converted into business decisions? |
| **Leadership advisory** | Did they ask for examples of advising senior leadership and being right? |
| **Intellectual curiosity** | Did they probe how the candidate collects and connects information? |
| **Qualification + range** | What credential/background combination did panel describe as "rare in Pakistan"? |

Write a **3-5 line persona brief** at the top of your search output. Example:

> "Looking for ACCA/ACA-qualified finance professional who has crossed from pure finance into strategic/operational leadership. Must demonstrate forward-looking pattern detection — not just reporting what happened but advising on what's about to happen. Development/NGO sector experience valued but not sufficient alone. Key signal: has this person ever changed a senior leader's decision through their own analysis?"

**Profile markers that signal a match:**
- Finance title PLUS operations/COO/commercial/strategy responsibility
- Career trajectory showing lateral growth into business roles (not just vertical promotion)
- Consulting or advisory firm background (trained to advise, not execute)
- Founded or co-founded anything (entrepreneurial pattern detection)
- Language in bio: "business strategy", "market entry", "product pricing", "new venture" (in a finance profile)
- Has presented to boards, investors, or donors (not just prepared the deck)

**Profile markers that signal poor fit:**
- Pure compliance/audit/donor reporting focus with no strategic evidence
- Manager-level with no advisory track record
- Only backward-looking language ("managed accounts", "filed reports", "ensured compliance")
- Entire career in one narrow function/sector

### STEP 0.8: Create/Verify Sourcing Sheet
Before running searches, set up a Google Sheet to track this role's candidates:

```javascript
const helper = require('tools/sourcing-sheet-helper');
const result = await helper.getOrCreateRoleSheet(
  spreadsheetId,    // From intake
  'product_designer', // Role slug (lowercase, hyphens)
  'Product Designer' // Role title (display)
);
console.log(`✓ Sheet ready: ${result.sheetUrl}`);
```

Announce to user: "Sourcing sheet created: [URL]. All candidates will be tracked here. Status updates: Identified → DM Pending → DM Sent → Responded → Confirmed → In Markaz"

### STEP 1: Resolve Platform Set
Based on the role, select which platforms to search (resolve internally — don't ask user):

| Role Category | Tier 1 (fetch first) | Tier 2 (search) |
|---|---|---|
| **Technical** (Odoo Dev, Full Stack Lead) | GitHub user search, org team pages | LinkedIn via Google |
| **Digital Learning** (ISL, Training Manager) | Org team pages (ITA, TCF, Zindagi), conference speaker lists | LinkedIn via Google, Medium |
| **Fundraising / BD** | Org team pages (TCF, AKF, PPAF), The Org, conference lists | LinkedIn via Google |
| **Finance / Ops** (CFO, Head of Finance) | Org team pages (PPAF, AKF, DAI, Chemonics, ITA), The Org, USAID partner pages | LinkedIn via Google |
| **Growth / UX** (Soul Architect, PM) | Medium, Substack, org team pages | LinkedIn via Google |
| **Impact / M&E** | Org team pages, academic profiles, conference speaker lists | LinkedIn via Google |
| **Default** | LinkedIn via Google | — |

**Critical platform notes:**
- LinkedIn blocks direct WebFetch (returns 999 error). Use Google `site:linkedin.com` for snippets only.
- Org team pages (tcf.org.pk/team, itacec.org/team, theorg.com/org/[name]) ARE fetchable via WebFetch.
- theorg.com has org charts for Pakistan nonprofits — often has names + titles not on LinkedIn.
- Conference speaker lists (Pakistan Learning Festival, Pakistan Development Forum) are fetchable.

### STEP 2: Run Searches (3-Layer Strategy)
Run ALL three layers. Do not skip Layer 1 — it produces the highest-quality results for dev sector roles.

**Layer 1: Org Team Pages (WebFetch directly, always do this first)**

For Fundraising/BD/Learning/Impact roles, fetch directly:
- WebFetch: https://itacec.org/team/
- WebFetch: https://theorg.com/org/idara-e-taleem-o-aagahi
- WebFetch: https://www.tcf.org.pk/about-us/our-people/
- WebFetch: https://www.zindagitrust.org/leadership-board
- WebFetch: https://www.ppaf.org.pk/team
- WebFetch: https://www.akdn.org/our-agencies/aga-khan-foundation/pakistan
- WebFetch: https://pakistanlearningfestival.com/plf-islamabad-2024/

For Technical roles, fetch GitHub user search:
- WebFetch: https://github.com/search?q=[skill]+location%3APakistan&type=users

**Layer 2: Targeted Google Searches**

Most reliable pattern for Pakistani dev sector is **org name + title**, NOT LinkedIn site: queries.

Examples by role:
- **Fundraising:** `"[org name]" "fundraising" OR "partnerships" OR "resource mobilization" staff Islamabad`
- **Education:** `"ITA" OR "TCF" OR "Teach For Pakistan" "manager" OR "lead" learning design curriculum`
- **Finance/Ops:** `"ACCA" OR "ACA" "head of finance" OR "CFO" OR "finance director" Pakistan NGO Islamabad`
- **Impact/M&E:** `"MEAL" OR "M&E" "lead" OR "manager" Pakistan USAID OR FCDO education Islamabad`

After finding names via Layer 1, run name-based Google searches for richer background:
- `"[Full Name]" "[Org Name]" experience OR background OR profile`
- `"[Full Name]" Pakistan [skill] OR [sector]`

**Layer 3: LinkedIn via Google (catch-all, lower yield)**

Lower yield for Pakistani profiles but still worth 3-4 queries:
- `site:linkedin.com/in "[Job Title]" Pakistan`
- `site:linkedin.com/in "[Skill 1]" "[Skill 2]" Pakistan EdTech OR nonprofit`
- Role-specific examples: `site:linkedin.com/in "Fundraising" "manager" OR "lead" Pakistan nonprofit`

### STEP 3: Extract Candidate Profiles
For each promising result, extract:
- **Full name**
- **Current role title**
- **Current company**
- **Location** (city)
- **Key experience** relevant to role (2-3 bullet points)
- **Platform + profile URL**
- **1-sentence "why relevant"** note (reference their specific experience, not generic phrases)

### STEP 4: Present Candidate Slate
Show the slate BEFORE drafting anything. Format:

```
## Talent Slate — [Role Title] — [Date]

Persona brief: [3-line summary]

Searched: [platforms] | Queries run: [N] | Results reviewed: [N] | Surfaced: [N]

| # | Name | Current Role | Company | Location | Why Relevant | Panel Fit Signal | Profile |
|---|------|-------------|---------|----------|-------------|-----------------|--------|
| 1 | ... | ... | ... | ... | ... | ... | [URL] |
| 2 | ... | ... | ... | ... | ... | ... | [URL] |

Who should I draft DMs for?
("All", "1 and 3", "Skip 4 -- rest are fine", "None of these -- search again")
```

**Column definitions:**
- **Why Relevant** — sector/skill match to JD (what they've actually done)
- **Panel Fit Signal** — one specific evidence point mapping to the persona (e.g., "Finance → COO trajectory at AKF", "Advisory firm = trained to brief leadership", "Founded practice = entrepreneurial pattern")

**Rules:**
- Profile column must contain actual URLs, never placeholder text
- Never suppress a candidate — show everyone found, let Ayesha decide
- Flag any candidate where Panel Fit Signal is weak or absent

### STEP 4.5: Add Candidates to Sheet
Before asking Ayesha for approval, write all candidates to the sourcing sheet:

```javascript
const { newCandidates, skippedCount } = await helper.checkDuplicates(
  spreadsheetId,
  sheetName,
  allCandidatesFound
);

if (skippedCount > 0) {
  console.log(`⚠ ${skippedCount} candidates already tracked, skipping duplicates`);
}

const added = await helper.addCandidatesToSheet(
  spreadsheetId,
  sheetName,
  newCandidatesOnly
);
console.log(`✓ Added ${added.rowsAdded} candidates to sourcing sheet`);
```

Present updated slate:
```
Talent Slate — [Role Title] — [Date]
Added to sheet: [X] candidates (Status: Identified, DM Sent: No)
Skipped: [Y] candidates (already being outreached)
[Show remaining candidates only]
```

### STEP 5: Draft LinkedIn DMs
For each candidate Ayesha approves, write a personalized LinkedIn DM (150-200 words max).

**DM Structure:**
```
Hi [First Name],

[1 specific observation about their work — a project, their career trajectory, or something from their profile that directly signals why they are right for this role. NEVER use generic phrases like "I came across your profile."]

I'm Ayesha, part of the People & Culture team at Taleemabad -- we're building AI-powered tools to improve learning quality for teachers and students across Pakistan. We're looking for a [Role Title] who can [core impact of the role in 1 sentence].

Given your background in [specific experience from their profile], I think you'd find the challenge interesting -- and the mission even more so.

Would you be open to a 20-minute conversation to explore? No pressure at all if the timing isn't right.

Warm regards,
Ayesha Khan
People & Culture | Taleemabad
```

**DM Rules (non-negotiable):**
- ALWAYS personalize opening line with something specific from their profile
- Mission-first — Taleemabad's impact before role description
- Soft ask only: "explore", "conversation" — never "apply", "interview", "opportunity"
- 150-200 words max
- No em dashes (use `--` instead)
- Never mention salary in first outreach
- Sign as Ayesha, not Coco

### STEP 5.5: Mark DMs as Pending
When Ayesha confirms which candidates to DM, update the sheet:

```javascript
const approved = [
  { linkedinUrl: 'https://linkedin.com/in/abc123', name: 'Alice' },
  { linkedinUrl: 'https://linkedin.com/in/def456', name: 'Bob' }
];

for (const candidate of approved) {
  await helper.updateCandidateStatus(
    spreadsheetId,
    sheetName,
    candidate.linkedinUrl,
    { status: 'DM Pending', dmSent: 'Awaiting Ayesha' }
  );
  console.log(`✓ ${candidate.name}: marked DM Pending`);
}
```

### STEP 6: Save Output File
After presenting slate and drafting DMs, save to:
```
output/sourcing/[role-slug]-[YYYY-MM-DD].md
```

File contains:
1. Search summary (platforms, queries, results reviewed)
2. Full candidate slate table
3. Full DM draft per approved candidate (copy-paste ready for LinkedIn)

Ayesha copies each DM to LinkedIn manually.

### STEP 7: Add Confirmed Candidate to Markaz
When Ayesha says: "[Name] confirmed interest, add them for [Role]"

**Step 7a: Update Sheet Status**
```javascript
await helper.updateCandidateStatus(
  spreadsheetId,
  sheetName,
  candidate.linkedinUrl,
  {
    status: 'Confirmed',
    response: 'Interested - added to Markaz',
    dmSent: 'Yes'
  }
);
console.log(`✓ ${candidate.name}: marked Confirmed`);
```

**Step 7b: Add to Markaz**
Get the job ID:
```sql
SELECT id FROM jobs
WHERE title ILIKE '%[role]%' AND status = 'published'
LIMIT 1;
```

Run insert script:
```javascript
const { Client } = require('pg');
const candidate = {
  first_name: '[First]',
  last_name: '[Last]',
  email: null, // usually null for LinkedIn sourced
  phone: null,
  position: '[Role Title]',
  skills: ['skill1', 'skill2'],
  source: 'LinkedIn - Sourced',
  location: '[City]',
  current_position: '[Their current title]',
  current_company: '[Their current company]',
  tags: {
    sourced_by: 'coco',
    sourcing_run: '[YYYY-MM-DD]',
    profile_url: '[linkedin.com/in/...]'
  }
};

// Insert candidate, then insert application with status='new'
```

After running, confirm IDs back to Ayesha:
```
Added to Markaz:
- Candidate ID: [X]
- Application ID: [Y]
- Status: new
```

---

## Execution Checklist

- [ ] Intake: role title, skills, seniority, count, sheet ID
- [ ] Read JD from Markaz
- [ ] Persona brief built (from panel transcript or by inference)
- [ ] Sourcing sheet created/verified
- [ ] Platform set resolved (Tier 1 first)
- [ ] Layer 1 (org pages) searched
- [ ] Layer 2 (Google) searched
- [ ] Layer 3 (LinkedIn via Google) searched
- [ ] Candidates extracted (full name, role, company, location, experience, URL)
- [ ] Candidate slate presented (with Panel Fit Signal column)
- [ ] Deduplication checked (checkDuplicates)
- [ ] New candidates added to sheet
- [ ] Ayesha approves which to DM
- [ ] DMs drafted (personalized, 150-200 words, mission-first)
- [ ] DM Pending status marked in sheet
- [ ] [Ayesha sends DMs, candidate responds]
- [ ] Ayesha confirms interest
- [ ] Sheet status updated to Confirmed
- [ ] Candidate inserted to Markaz with source='LinkedIn - Sourced'
- [ ] Profile URL tagged in candidate record
- [ ] Output file saved (sourcing/[role-slug]-[date].md)

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Skipping persona brief | Choose wrong candidates (skills ≠ interview fit) | Extract from panel transcript; build before searching |
| Using only one search layer | Incomplete results | Use all 3 layers; Layer 1 (org pages) first |
| Adding to Markaz early | Pollutes pipeline with unqualified leads | Wait ONLY after "confirmed interest" from Ayesha |
| Template DMs | Low response, looks mass-distributed | Personalize every DM; reference their specific work |
| No deduplication | Candidate appears twice in different rounds | Run checkDuplicates before presenting slate |
| Platform overload | Wasted effort searching 10 platforms equally | Use role-based Tier 1/Tier 2 selection; focus first |
| Weak panel fit signals | Ayesha wonders why candidate was chosen | Reference observable evidence from their profile |
| Forgetting source tracking | Can't measure sourcing effectiveness | Always set source='LinkedIn - Sourced' + tags.profile_url |
| DM longer than 200 words | Low read rate, LinkedIn cuts off | Keep DMs tight (150-200 max) |
| Skipping sheet updates | No pipeline visibility | Update sheet at every step: Identified → Pending → Confirmed |

---

## Success Criteria

✅ Persona brief built from panel transcript before any search  
✅ All 3 layers searched (org pages first, Google second, LinkedIn last)  
✅ Deduplication check passed (no existing candidates in slate)  
✅ 10-15 candidates in slate (or target count approved by Ayesha)  
✅ Every candidate has Panel Fit Signal (observable evidence)  
✅ Candidates added to sourcing sheet (Status: Identified)  
✅ DMs personalized (reference their specific work/project)  
✅ DMs 150-200 words max (no em dashes)  
✅ DM Pending status marked in sheet  
✅ Output file saved (sourcing/[role-slug]-[date].md)  
✅ No Markaz entries until confirmed interest  
✅ Confirmed candidates added with source='LinkedIn - Sourced' + profile URL  

---

## Self-QA Checklist (Before Presenting Slate to Ayesha)

- [ ] Intake completed: role title, seniority, skills, target count, sheet ID
- [ ] JD read from Markaz
- [ ] Persona brief written (3-5 lines, observable behaviors, profile markers)
- [ ] Sourcing sheet created and URL confirmed
- [ ] Platform set resolved (Tier 1 platforms identified)
- [ ] Layer 1 (org pages) searched completely
- [ ] Layer 2 (Google targeted searches) completed
- [ ] Layer 3 (LinkedIn via Google) completed (3-4 queries)
- [ ] Deduplication check run (checkDuplicates function)
- [ ] Candidates extracted with all fields (name, role, company, location, URL, why relevant)
- [ ] Candidate slate formatted with Panel Fit Signal column
- [ ] Candidates added to sourcing sheet (Status: Identified)
- [ ] At least 1 example candidate has clear Panel Fit Signal evidence
- [ ] No generic phrases in "Why Relevant" column (specific experiences only)
- [ ] All URLs are real LinkedIn profiles (not placeholders)
- [ ] Persona brief visible at top of slate
- [ ] Ready to present to Ayesha for approval

**Before Sending DMs to Ayesha:**
- [ ] DMs drafted for approved candidates
- [ ] Each DM personalized (reference specific project/work)
- [ ] DMs 150-200 words each
- [ ] No em dashes (use -- instead)
- [ ] Mission-first framing (Taleemabad's impact mentioned)
- [ ] Soft ask ("explore", "conversation", not "apply")
- [ ] Signed by Ayesha (not Coco)
- [ ] DM Pending status marked in sheet for each candidate
- [ ] Output file saved with full table + DM drafts

**Before Adding to Markaz:**
- [ ] Ayesha confirmed: "[Name] replied positively / confirmed interest"
- [ ] Sheet status updated to Confirmed
- [ ] Candidate inserted to Markaz (email: null, status: new)
- [ ] Source set to 'LinkedIn - Sourced'
- [ ] Tags include: sourced_by, sourcing_run, profile_url
- [ ] Candidate ID and Application ID confirmed back to Ayesha

---

## Infrastructure & Setup

**Required Setup:**
1. Create Google Sheet for candidate tracking (auto-created per role via helper.js)
2. Get spreadsheet ID from Google Sheets URL
3. Set environment variable or pass SPREADSHEET_ID to sourcing-sheet-helper

**Google Sheets Helper** (`tools/sourcing-sheet-helper.js`):
- `getOrCreateRoleSheet(spreadsheetId, roleSlug, roleTitle)` — Creates role-specific sheet for tracking
- `checkDuplicates(spreadsheetId, sheetName, candidates)` — Deduplication by URL + name + company/role
- `addCandidatesToSheet(spreadsheetId, sheetName, candidates)` — Batch add with auto-formatting
- `updateCandidateStatus(spreadsheetId, sheetName, linkedinUrl, statusObj)` — Update Status/DM Sent/Response columns
- `getCandidatesByStatus(spreadsheetId, sheetName, status)` — Filter candidates by status

**Markaz Integration** (`tools/insert-confirmed-candidate.js`):
- Node.js script for candidate + application insertion after confirmed interest
- Read: markaz-db MCP (read only)
- Write: Direct Postgres connection (MARKAZ_WRITE_URL)
- Sets: source='LinkedIn - Sourced', tags.profile_url, tags.sourcing_run
- Status: new (ready for CV screening)

**Setup Guide:** See `tools/SOURCING_SHEET_SETUP.md` for complete initialization + workflow

---

## Resources & References

**SOP History:**
- Noah's original: `memory/noah_skill_talent_sourcing_original.md`
- Coco's adoption: `memory/coco_talent_sourcing_skill.md`
- Detailed steps: `memory/talent_sourcing_7steps_complete.md`

**Example Sourcing Runs:**
- Soul Architect (April 2026): `memory/project_soul_architect_sourcing_final.md`
- Step-by-step walkthrough: `memory/talent_sourcing_steps_explained.md`

---

## Skill Status

**Updated:** 2026-06-03  
**Version:** 2.0 (Noah's comprehensive approach + Coco adaptations)  
**Status:** ✅ PRODUCTION READY FOR TESTING

Improvements in this version:
- ✅ Persona brief methodology (observable behaviors + profile markers)
- ✅ Sourcing sheet integration (full pipeline tracking)
- ✅ Platform selection by role (Tier 1 → Tier 2 strategy)
- ✅ Deduplication checks (checkDuplicates function)
- ✅ Better DM rules (150-200 words, mission-first, personalization)
- ✅ Sheet status tracking (Identified → Pending → Confirmed → In Markaz)
- ✅ Comprehensive execution checklist
- ✅ Better failure modes and common mistakes
