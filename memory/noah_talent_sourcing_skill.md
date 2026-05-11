---
name: Noah's Talent Sourcing Skill - Complete Mechanism
description: How Noah (Jawwad's agent) proactively sources experienced passive candidates from LinkedIn, GitHub, Medium, org team pages, and conference lists. 3-layer search strategy + personalized LinkedIn DMs + Markaz integration only after confirmed interest.
type: reference
originSessionId: 50203d1f-d855-41c4-b12a-dba80a622e87
---
# Noah's Talent Sourcing Skill — Complete Mechanism

**GitHub:** https://github.com/Jaw901/Noah/blob/master/.claude/skills/talent-sourcing/SKILL.md

## Core Purpose
Find experienced professionals NOT actively applying. Search platforms → Present slate → Draft LinkedIn DMs (Jawwad sends manually) → Add to Markaz only AFTER confirmed interest.

## Workflow
```
Search → Present slate → Jawwad picks → Noah drafts LinkedIn DMs
→ Jawwad sends manually → Candidate confirms interest
→ Jawwad tells Noah → Noah adds to Markaz (status='new')
```

**Critical Rule:** Markaz is ONLY touched after confirmed interest. Never at search stage.

## Step-by-Step Process

### Step 0: Intake
Collect before searching:
1. Role title (exact)
2. Top 3-5 must-have skills/experiences
3. Seniority level (e.g., "8+ years", "senior")
4. How many candidates to surface? (default: 10-15)

Then fetch JD from Markaz:
```sql
SELECT id, title, jd_text, required_skills, department
FROM jobs WHERE title ILIKE '%[role]%' AND status = 'published' LIMIT 1;
```

### Step 1: Resolve Platform Set (internally — no user exposure)

**Platform selection by role category:**

| Role Category | Examples | Tier 1 (fetch first) | Tier 2 (search) |
|---------------|----------|---------------------|-----------------|
| Technical | Odoo Developer, Full Stack Lead | GitHub user search, org team pages | LinkedIn via Google |
| Digital Learning | Instructional Systems Lead, Training Manager | Org team pages (ITA, TCF, Zindagi), conference speaker lists | LinkedIn via Google, Medium |
| Fundraising / BD | Fundraising Lead/Manager | Org team pages (TCF, AKF, PPAF), The Org, conference lists | LinkedIn via Google |
| Growth / UX | Soul Architect, Program Manager | Medium, Substack, org team pages | LinkedIn via Google |
| Impact | M&E Lead | Org team pages, academic profiles, conference lists | LinkedIn via Google |
| Default | Any other | LinkedIn via Google | -- |

### Step 2: Run Searches (3-Layer Strategy)

**Critical Learning (2026-04-04):**
- LinkedIn blocks direct WebFetch (returns 999 error). Use Google site:linkedin.com only.
- Google site:linkedin.com for Pakistani professionals returns sparse results.
- **Org team pages** (tcf.org.pk/team, itacec.org/team, theorg.com) ARE fetchable — use first.
- **The Org** (theorg.com) has org charts for Pakistan nonprofits — highest-quality names + titles.
- **Conference speaker lists** are fetchable and surface active professionals.
- Devex.com/people is behind paywall. Devex job listings are accessible.

#### Layer 1: Org Team Pages (WebFetch directly — always do this first)

```
# Pakistan education & development orgs
https://itacec.org/team/
https://theorg.com/org/idara-e-taleem-o-aagahi
https://www.tcf.org.pk/about-us/our-people/
https://www.zindagitrust.org/leadership-board
https://www.ppaf.org.pk/team
https://www.akdn.org/our-agencies/aga-khan-foundation/pakistan

# Conference speaker lists (active professionals who present)
https://pakistanlearningfestival.com/plf-islamabad-2024/
https://pakistanlearningfestival.com/profiles/resource_persons_and_institutions-clf/
```

For technical roles:
```
https://github.com/search?q=[skill]+location%3APakistan&type=users
```

#### Layer 2: Targeted Google Searches (org name + title combos)

Most reliable pattern: **org name + title, not LinkedIn site: query**.

Examples:
```
# Fundraising / BD
"[org name]" "fundraising" OR "partnerships" OR "resource mobilization" staff Islamabad
"Citizens Foundation" OR "PPAF" OR "Zindagi Trust" "Vice President" OR "Manager" fundraising Pakistan

# Education / Training
"[org name]" "instructional design" OR "learning design" staff OR team Pakistan
"ITA" OR "TCF" OR "Teach For Pakistan" "manager" OR "lead" learning design curriculum

# Impact / M&E
"MEAL" OR "M&E" "lead" OR "manager" Pakistan USAID OR FCDO education Islamabad
"DAI Pakistan" OR "Chemonics Pakistan" OR "RTI Pakistan" partnerships education staff
```

#### Layer 3: LinkedIn via Google (catch-all, lowest yield)

```
site:linkedin.com/in "[Job Title]" Pakistan
site:linkedin.com/in "[Skill 1]" "[Skill 2]" Pakistan EdTech OR education OR nonprofit

# Fundraising
site:linkedin.com/in "Fundraising" "manager" OR "lead" Pakistan nonprofit OR NGO
site:linkedin.com/in "resource mobilization" "manager" Pakistan education

# M&E Lead
site:linkedin.com/in "M&E" OR "MEAL" "lead" OR "manager" Pakistan NGO OR development

# Odoo Developer
site:linkedin.com/in "Odoo" "head" OR "lead" OR "principal" Pakistan

# Full Stack Lead
site:linkedin.com/in "Full Stack" "lead" OR "head" Pakistan
site:linkedin.com/in "React" "Node" "senior" Pakistan EdTech OR startup
```

### Step 3: Extract Candidate Profiles

For each promising result:
- Full name
- Current role title
- Current company
- Location (city)
- Key experience relevant to role (2-3 bullets)
- Platform + profile URL
- 1-sentence "why relevant" note

### Step 4: Present Candidate Slate

Format:
```
## Talent Slate – [Role Title] – [Date]
Searched: [platforms] | Queries run: [N] | Results reviewed: [N] | Surfaced: [N]

| # | Name | Current Role | Company | Location | Why Relevant | Profile |
|---|------|-------------|---------|----------|-------------|---------|
| 1 | ... | ... | ... | ... | ... | [URL] |
```

**Rules:**
- Profile column = actual URLs, never placeholders
- "Why Relevant" = specific experience, not generic phrases
- Never suppress candidates — show everyone, let Jawwad decide
- Location default = Pakistan-based. Diaspora only if explicitly requested.

### Step 5: Draft LinkedIn DMs

For each approved candidate: 150-200 words max.

**DM Structure:**
```
Hi [First Name],

[1 specific observation about their work — project, trajectory, or profile signal.
NEVER "I came across your profile"]

I'm Jawwad, People & Culture team at Taleemabad — we're building AI-powered
tools to improve learning quality for teachers and students across Pakistan.
We're looking for a [Role Title] who can [core impact in 1 sentence].

Given your background in [specific experience], I think you'd find the challenge
interesting — and the mission even more so.

Would you be open to a 20-minute conversation to explore? No pressure at all
if the timing isn't right.

Warm regards,
Jawwad Ali
People & Culture | Taleemabad
```

**DM Rules (non-negotiable):**
- ALWAYS personalize opening with something specific from profile
- Mission-first: Taleemabad's impact before role description
- Soft ask: "explore", "conversation" — never "apply", "interview", "opportunity"
- 150-200 words max
- No em dashes (use ` -- ` instead)
- Never mention salary
- Sign as Jawwad Ali, not Noah

### Step 6: Save Output File

Location: `output/sourcing/[role-slug]-[YYYY-MM-DD].md`

Contains:
1. Search summary (platforms, queries, results reviewed)
2. Full candidate slate table
3. Full DM draft per approved candidate (copy-paste ready)

Jawwad copies each DM to LinkedIn manually.

### Step 7: Add Confirmed Candidate to Markaz

Only AFTER Jawwad confirms: "[Name] confirmed interest, add them for [Role]"

1. Get job ID:
```sql
SELECT id FROM jobs
WHERE title ILIKE '%[role]%' AND status = 'published' LIMIT 1;
```

2. Run insert script at `tools/gmail-mcp/sourcing/insert-confirmed-candidate.js`:
   - Inserts candidate (first_name, last_name, email=null, position, skills, source='LinkedIn - Sourced', location, current_position, current_company, tags)
   - Inserts application (candidate_id, job_id, status='new', with notes and profile_url)
   - Skips duplicate check if email is null

3. Confirm IDs back to Jawwad

## Critical Non-Negotiables

- **MCP read-only** — markaz-db MCP uses noah_readonly. All writes via Node.js script.
- **No email = no dedup** — when email is null, skip duplicate check.
- **Location default** — Pakistan-based only. Diaspora only if explicitly requested.
- **Never add before confirmation** — whole point is to contact first.
- **DM = Jawwad sends manually** — Noah drafts, never sends. No API available.
- **Source tracking** — always set `candidates.source = 'LinkedIn - Sourced'` and `tags.profile_url`.

## Key Learnings

1. **LinkedIn direct WebFetch fails** (999 error) — use Google site: queries instead
2. **Org team pages are fetchable and high-quality** — prioritize them
3. **The Org (theorg.com)** is goldmine for Pakistan nonprofits
4. **Conference speaker lists** surface active, publicly visible professionals
5. **Email often null** — many sourced candidates have no email. Script handles this.
6. **Markaz timing is critical** — only after confirmed interest, never speculatively.

---

**Source:** Jaw901/Noah repository, .claude/skills/talent-sourcing/SKILL.md
