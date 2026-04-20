---
name: talent-sourcing
description: Proactively search for experienced passive candidates on LinkedIn, GitHub, Medium, and other platforms. Draft personalized LinkedIn DMs. Add confirmed-interested candidates to Markaz. Trigger when user says "source candidates", "find people for [role]", "build a candidate slate", or "run a talent search".
source: https://github.com/Jaw901/Noah/blob/master/.claude/skills/talent-sourcing/SKILL.md
saved: 2026-04-16
purpose: Reference implementation for Coco symmetry
---

# Skill: Talent Sourcing

## Purpose
Find experienced professionals who are NOT actively applying. Search relevant platforms, surface a candidate slate, draft personalized LinkedIn DMs for Jawwad to send manually. Only add to Markaz once a candidate confirms interest.

## Trigger Phrases
- `/talent-sourcing`
- "source candidates for [role]"
- "find people for [role]"
- "build a candidate slate for [role]"
- "run a talent search"
- "who should we be approaching for [role]"

---

## Flow Overview

```
Search → Present slate → Jawwad picks → Noah drafts LinkedIn DMs
→ Jawwad sends manually → Candidate confirms interest
→ Jawwad tells Noah → Noah adds to Markaz (status = 'new')
```

Markaz is ONLY touched after confirmed interest. Never at the search stage.

---

## Step 0 – Intake

Before searching, collect:

```
1. Role title (exact)
2. Top 3-5 must-have skills or experiences
3. Seniority level (e.g. "8+ years", "senior", "10+ years")
4. How many candidates to surface? (default: 10-15)
```

Then read the JD from Markaz:
```sql
SELECT id, title, jd_text, required_skills, department
FROM jobs
WHERE title ILIKE '%[role]%' AND status = 'published'
LIMIT 1;
```

---

## Step 1 – Resolve Platform Set

Based on the role, select platforms to search (resolve internally -- not user-facing):

| Role Category | Roles | Tier 1 (fetch first) | Tier 2 (search) |
|---------------|-------|---------------------|-----------------|
| Technical | Odoo Developer, Full Stack Lead | GitHub user search, org team pages | LinkedIn via Google |
| Digital Learning | Instructional Systems Lead, Training Manager | Org team pages (ITA, TCF, Zindagi), conference speaker lists | LinkedIn via Google, Medium |
| Fundraising / BD | Fundraising Lead/Manager | Org team pages (TCF, AKF, PPAF), The Org, conference speaker lists | LinkedIn via Google |
| Growth / UX | Soul Architect, Program Manager | Medium, Substack, org team pages | LinkedIn via Google |
| Impact | M&E Lead | Org team pages, academic profiles, conference speaker lists | LinkedIn via Google |
| Default | Any other | LinkedIn via Google | -- |

**Critical platform notes (learned from live run 2026-04-04):**
- LinkedIn blocks direct WebFetch (returns 999 error). Use Google site:linkedin.com queries for snippets only.
- Google site:linkedin.com queries for Pakistani professionals return sparse results. Do NOT rely on LinkedIn alone.
- **Org team pages** (tcf.org.pk/team, itacec.org/team, theorg.com/org/[name]) ARE fetchable via WebFetch -- use these first for dev sector roles.
- **The Org** (theorg.com) has org charts for Pakistan nonprofits -- directly fetchable and often has names + titles not on LinkedIn.
- **Conference speaker lists** (Pakistan Learning Festival, Pakistan Development Forum) are fetchable and surface active professionals.
- **Devex.com/people** profiles are behind a paywall. Devex job listings are accessible and reveal what titles exist in the market.

---

## Step 2 – Run Searches (3-Layer Strategy)

Run all three layers. Do not skip Layer 1 -- it produces the highest-quality results for dev sector roles.

### Layer 1 – Org Team Pages (WebFetch directly, always do this first)

For **Fundraising / BD / Learning / Impact roles**, fetch these pages directly. These are not blocked.

```
# Pakistan education & development orgs -- team pages
WebFetch: https://itacec.org/team/
WebFetch: https://theorg.com/org/idara-e-taleem-o-aagahi
WebFetch: https://www.tcf.org.pk/about-us/our-people/  (or /team/)
WebFetch: https://www.zindagitrust.org/leadership-board
WebFetch: https://www.ppaf.org.pk/team  (PPAF -- Pakistan Poverty Alleviation Fund)

# AKF Pakistan (Aga Khan Foundation) -- leadership page
WebFetch: https://www.akdn.org/our-agencies/aga-khan-foundation/pakistan

# Conference speaker lists (active professionals who show up and present)
WebFetch: https://pakistanlearningfestival.com/plf-islamabad-2024/
WebFetch: https://pakistanlearningfestival.com/profiles/resource_persons_and_institutions-clf/
```

For **Technical roles**, fetch GitHub user search:
```
WebFetch: https://github.com/search?q=[skill]+location%3APakistan&type=users
```

### Layer 2 – Targeted Google Searches (find names via org + title combos)

The most reliable Google pattern for Pakistani dev sector is org name + title, not LinkedIn site: query.

```
# Fundraising / BD roles
"[org name]" "fundraising" OR "partnerships" OR "resource mobilization" staff Islamabad
"Citizens Foundation" OR "PPAF" OR "Zindagi Trust" "Vice President" OR "Manager" fundraising Pakistan
"TCF" OR "ITA" OR "Alif Ailaan" "head of" OR "director" partnerships OR development Pakistan

# Education / Training roles
"[org name]" "instructional design" OR "learning design" staff OR team Pakistan
"ITA" OR "TCF" OR "Teach For Pakistan" "manager" OR "lead" learning design curriculum

# Impact / M&E roles
"MEAL" OR "M&E" "lead" OR "manager" Pakistan USAID OR FCDO education Islamabad
"monitoring evaluation" "senior" Pakistan NGO education Islamabad 2024 2025

# USAID implementing partners (goldmine for experienced dev sector professionals)
"DAI Pakistan" OR "Chemonics Pakistan" OR "RTI Pakistan" OR "Palladium Pakistan" partnerships education staff
```

### Layer 3 – LinkedIn via Google (catch-all, do last)

Lower yield for Pakistani profiles but still worth running 3-4 queries as a sweep.

```
site:linkedin.com/in "[Job Title]" Pakistan
site:linkedin.com/in "[Job Title]" "[Primary Skill]" Karachi OR Lahore OR Islamabad
site:linkedin.com/in "[Skill 1]" "[Skill 2]" Pakistan EdTech OR education OR nonprofit
```

Role-specific examples:
```
# Fundraising
site:linkedin.com/in "Fundraising" "manager" OR "lead" Pakistan nonprofit OR NGO
site:linkedin.com/in "resource mobilization" "manager" Pakistan education

# M&E Lead
site:linkedin.com/in "M&E" OR "MEAL" "lead" OR "manager" Pakistan NGO OR development
site:linkedin.com/in "monitoring evaluation" Pakistan education OR EdTech

# Odoo Developer
site:linkedin.com/in "Odoo" "head" OR "lead" OR "principal" Pakistan
site:linkedin.com/in "Odoo Developer" "senior" Pakistan

# Instructional Systems Lead
site:linkedin.com/in "instructional design" "lead" OR "head" Pakistan
site:linkedin.com/in "learning design" OR "curriculum design" Pakistan EdTech

# Full Stack Lead
site:linkedin.com/in "Full Stack" "lead" OR "head" Pakistan
site:linkedin.com/in "React" "Node" "senior" Pakistan EdTech OR startup
```

### Follow-up: Name-based Google search (after finding names in Layers 1-2)

Once names are found via org pages or conference lists, Google each name for richer background:
```
"[Full Name]" "[Org Name]" experience OR background OR profile
"[Full Name]" Pakistan fundraising OR partnerships OR development
```

---

## Step 3 – Extract Candidate Profiles

For each promising result, extract:
- Full name
- Current role title
- Current company
- Location (city)
- Key experience relevant to the role (2-3 bullet points)
- Platform + profile URL
- 1-sentence "why relevant" note

---

## Step 4 – Present Candidate Slate

Show the slate before drafting anything. Format:

```
## Talent Slate – [Role Title] – [Date]
Searched: [platforms] | Queries run: [N] | Results reviewed: [N] | Surfaced: [N]

| # | Name | Current Role | Company | Location | Why Relevant | Profile |
|---|------|-------------|---------|----------|-------------|---------|
| 1 | ... | ... | ... | ... | ... | [URL] |
| 2 | ... | ... | ... | ... | ... | [URL] |

Who should I draft DMs for?
("All", "1 and 3", "Skip 4 -- rest are fine", "None of these -- search again")
```

**Rules:**
- Profile column must contain actual URLs, never placeholder text
- "Why Relevant" must be specific – actual experience, not generic phrases
- Never suppress a candidate – show everyone found, let Jawwad decide
- Location default is Pakistan-based. Surface diaspora candidates only if Jawwad requests.

---

## Step 5 – Draft LinkedIn DMs

For each candidate Jawwad approves, write a personalized LinkedIn DM (150-200 words max).

### DM Structure

```
Hi [First Name],

[1 specific observation about their work – a project, their career trajectory, or
something from their profile that directly signals why they are right for this role.
NEVER use generic phrases like "I came across your profile."]

I'm Jawwad, part of the People & Culture team at Taleemabad -- we're building
AI-powered tools to improve learning quality for teachers and students across
Pakistan. We're looking for a [Role Title] who can [core impact of the role in
1 sentence].

Given your background in [specific experience from their profile], I think you'd
find the challenge interesting -- and the mission even more so.

Would you be open to a 20-minute conversation to explore? No pressure at all if
the timing isn't right.

Warm regards,
Jawwad Ali
People & Culture | Taleemabad
```

### DM Rules (non-negotiable)
- ALWAYS personalize the opening line with something specific from the profile
- Mission-first – Taleemabad's impact before the role description
- Soft ask only: "explore", "conversation" – never "apply", "interview", "opportunity"
- 150-200 words max (LinkedIn character limits)
- No em dashes anywhere (use ` -- ` instead)
- Never mention salary in first outreach
- Sign as Jawwad Ali, not Noah

---

## Step 6 – Save Output File

After presenting the slate and drafting DMs, save to:
```
output/sourcing/[role-slug]-[YYYY-MM-DD].md
```

File contains:
1. Search summary (platforms, queries, results reviewed)
2. Full candidate slate table
3. Full DM draft per approved candidate (copy-paste ready for LinkedIn)

Jawwad copies each DM to LinkedIn manually.

---

## Step 7 – Add Confirmed Candidate to Markaz

When Jawwad says: "[Name] confirmed interest, add them for [Role]"

### First, get the job ID:
```sql
SELECT id FROM jobs
WHERE title ILIKE '%[role]%' AND status = 'published'
LIMIT 1;
```

### Run insert script at `tools/gmail-mcp/sourcing/insert-confirmed-candidate.js`:

```javascript
const { Client } = require('pg');
const { MARKAZ_WRITE_URL } = require('../db-config');

const candidate = {
  first_name: '',
  last_name: '',
  email: null,          // usually null for LinkedIn sourced
  phone: null,
  position: '[Role Title]',
  skills: ['skill1', 'skill2'],
  source: 'LinkedIn - Sourced',
  location: '[City]',
  current_position: '[Their current title]',
  current_company: '[Their current company]',
  tags: {
    sourced_by: 'noah',
    sourcing_run: '[YYYY-MM-DD]',
    profile_url: '[linkedin.com/in/...]'
  }
};
const jobId = [job_id_from_markaz];

async function run() {
  const client = new Client({ connectionString: MARKAZ_WRITE_URL });
  await client.connect();

  // Check for duplicate by email (skip if email is null)
  let candidateId;
  if (candidate.email) {
    const existing = await client.query(
      'SELECT id FROM candidates WHERE email = $1', [candidate.email]
    );
    if (existing.rows.length > 0) {
      candidateId = existing.rows[0].id;
      console.log(`Candidate already exists: ID ${candidateId}`);
    }
  }

  if (!candidateId) {
    const result = await client.query(
      `INSERT INTO candidates
        (first_name, last_name, email, phone, position, skills, source,
         location, current_position, current_company, tags)
       VALUES ($1,$2,$3,$4,$5,$6::text[],$7,$8,$9,$10,$11::jsonb)
       RETURNING id`,
      [
        candidate.first_name, candidate.last_name, candidate.email,
        candidate.phone, candidate.position, candidate.skills,
        candidate.source, candidate.location, candidate.current_position,
        candidate.current_company, JSON.stringify(candidate.tags)
      ]
    );
    candidateId = result.rows[0].id;
    console.log(`Inserted candidate: ID ${candidateId}`);
  }

  const appResult = await client.query(
    `INSERT INTO applications
      (candidate_id, job_id, status, notes, ai_recommendation, ai_screening_summary)
     VALUES ($1,$2,'new',$3,$4,$5)
     RETURNING id`,
    [
      candidateId, jobId,
      'Passive sourced candidate -- confirmed interest via LinkedIn DM.',
      'Sourced candidate -- pending CV review',
      `Sourced on ${candidate.tags.sourcing_run} from ${candidate.source}. Profile: ${candidate.tags.profile_url}`
    ]
  );
  console.log(`Inserted application: ID ${appResult.rows[0].id}`);
  await client.end();
}

run().catch(console.error);
```

**Run from:** `c:\Noah the Agent\tools\gmail-mcp\`
```bash
node sourcing/insert-confirmed-candidate.js
```

After running, confirm IDs back to Jawwad:
```
Added to Markaz:
- Candidate ID: [X]
- Application ID: [Y]
- Status: new
```

---

## Important Notes

- **MCP is read-only** – `markaz-db` MCP uses `noah_readonly`. All writes via the Node.js script above.
- **No email = no deduplication** – when email is null, skip the duplicate check. Accept the insert.
- **Location default** – Pakistan-based only. Surface diaspora only if Jawwad explicitly requests.
- **Never add to Markaz before confirmation** – the whole point of this skill is to contact first. Premature Markaz inserts pollute the pipeline with unqualified leads.
- **DM = Jawwad sends manually** – Noah drafts, never sends LinkedIn DMs. There is no API for this.
- **Source tracking** – always set `candidates.source = 'LinkedIn - Sourced'` and `tags.profile_url` with the actual profile link.
