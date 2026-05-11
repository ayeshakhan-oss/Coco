---
name: Noah's Original Talent Sourcing Skill
description: Noah's exact implementation of talent sourcing from Jaw901/Noah repository. Reference for symmetry with Coco's implementation. Node.js version with database insertion script pattern. Saved 2026-04-16.
type: reference
originSessionId: 50203d1f-d855-41c4-b12a-dba80a622e87
---
# SKILL.md - Noah's Talent Sourcing Implementation

**Source:** https://github.com/Jaw901/Noah/blob/master/.claude/skills/talent-sourcing/SKILL.md  
**Saved:** 2026-04-16  
**Purpose:** Reference implementation for Coco symmetry

---

## Key Infrastructure Elements (For Coco Symmetry)

### 1. Output Folder Structure
```
output/sourcing/[role-slug]-[YYYY-MM-DD].md
```

**Examples from Noah:**
- `output/sourcing/fundraising-lead-2026-04-20.md`
- `output/sourcing/instructional-systems-lead-2026-04-15.md`
- `output/sourcing/m-e-lead-2026-04-18.md`

### 2. Database Insert Script Location & Pattern
**Noah's approach:** Node.js script at `tools/gmail-mcp/sourcing/insert-confirmed-candidate.js`

**Key fields from Noah's insert script:**
```javascript
const candidate = {
  first_name: '',
  last_name: '',
  email: null,          // null for LinkedIn sourced (no dedup check)
  phone: null,
  position: '[Role Title]',
  skills: ['skill1', 'skill2'],
  source: 'LinkedIn - Sourced',           // EXACT SOURCE STRING
  location: '[City]',
  current_position: '[Their current title]',
  current_company: '[Their current company]',
  tags: {
    sourced_by: 'noah',                    // AGENT IDENTIFIER
    sourcing_run: '[YYYY-MM-DD]',          // RUN DATE
    profile_url: '[linkedin.com/in/...]'   // ACTUAL URL
  }
};
```

**Database operations (from Noah's script):**
1. Check for duplicate by email (SKIP if email is null)
2. INSERT into `candidates` table
3. INSERT into `applications` table with status='new'
4. Return both IDs to user

### 3. Source Tracking (Critical)
- **Field:** `candidates.source`
- **Value:** `'LinkedIn - Sourced'` (exact string)
- **Also required:** `tags.profile_url` with actual LinkedIn/GitHub/org page URL

### 4. Markaz Integration Trigger
**Only after:** Jawwad says "[Name] confirmed interest, add them for [Role]"

**Process:**
1. Fetch job ID from Markaz
2. Run insert script
3. Return candidate ID + application ID

### 5. Output File Format (Step 6)
Location: `output/sourcing/[role-slug]-[YYYY-MM-DD].md`

**Contents:**
1. Search summary (platforms, queries, results reviewed)
2. Full candidate slate table
3. Full DM draft per approved candidate (copy-paste ready)

---

## Critical Rules from Noah's Implementation

1. **Never add to Markaz before confirmation** — whole point is to contact first
2. **DM = Jawwad sends manually** — Noah drafts only, never sends
3. **No email = no dedup** — when email is null, skip duplicate check and insert
4. **Source field exact:** `'LinkedIn - Sourced'`
5. **LinkedIn direct WebFetch fails** — always use Google site: queries
6. **Org team pages fetchable** — use these first (tcf.org.pk, itacec.org, theorg.com)
7. **Location default:** Pakistan-based only
8. **Profile URL required** — must store actual LinkedIn/GitHub/org URL in tags

---

## File Path (Noah's Script Reference)
```
tools/gmail-mcp/sourcing/insert-confirmed-candidate.js
```

Run from: `c:\Noah the Agent\tools\gmail-mcp\`
```bash
node sourcing/insert-confirmed-candidate.js
```

---

## Coco Adaptation Strategy

**Symmetry points for Coco:**
1. ✓ Same output folder: `output/sourcing/[role-slug]-[YYYY-MM-DD].md`
2. ✓ Same source field: `'LinkedIn - Sourced'`
3. ✓ Same tags format: `{sourced_by: 'coco', sourcing_run: '[YYYY-MM-DD]', profile_url: '[url]'}`
4. ✓ Python script (psycopg2) instead of Node.js
5. ✓ Same database operations (candidates + applications insert)
6. ✓ Same trigger: confirmed interest before Markaz write

---

**Locked In:** 2026-04-16  
**Status:** Reference for Phase 2 Infrastructure Development
