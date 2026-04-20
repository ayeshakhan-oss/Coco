---
name: Talent Sourcing SOP
description: Proactively search for experienced passive candidates on LinkedIn, GitHub, org team pages, and conference speaker lists. Present candidate slate, draft personalized LinkedIn DMs for Ayesha to send manually. Only add to Markaz after confirmed interest. 3-layer search strategy (Org team pages → Targeted Google → LinkedIn via Google). Updated 2026-04-16 (Noah's skill adapted for Coco).
type: reference
---

## Objective

Find experienced professionals who are NOT actively applying. Search relevant platforms using a 3-layer strategy, surface a candidate slate, draft personalized LinkedIn DMs for Ayesha to send manually. Only add to Markaz once a candidate confirms interest via Ayesha.

---

## SOP Steps (7-Step Process)

### Step 0: Intake

Before searching, collect from Ayesha:

1. Role title (exact)
2. Top 3-5 must-have skills or experiences
3. Seniority level (e.g., "8+ years", "senior", "10+ years")
4. How many candidates to surface? (default: 10-15)

Then fetch the JD from Markaz:
```sql
SELECT id, title, jd_text, required_skills, department
FROM jobs
WHERE title ILIKE '%[role]%' AND status = 'published'
LIMIT 1;
```

Log this database read with `log_db_query()`.

---

### Step 1: Resolve Platform Set (Internal Decision)

Based on the role category, automatically select platforms to search:

| Role Category | Roles | Tier 1 (Fetch First) | Tier 2 (Search) |
|---------------|-------|---------------------|-----------------|
| **Technical** | Odoo Developer, Full Stack Lead | GitHub user search, org team pages | LinkedIn via Google, Devex job listings |
| **Digital Learning** | Instructional Systems Lead, Training Manager | Org team pages (ITA, TCF, Zindagi), conference speaker lists | LinkedIn via Google, Medium |
| **Fundraising / BD** | Fundraising Lead, Partnerships Manager | Org team pages (TCF, AKF, PPAF), The Org, conference speaker lists | LinkedIn via Google |
| **Growth / UX** | Soul Architect, Program Manager, Product Manager | Medium, Substack, org team pages | LinkedIn via Google |
| **Impact / M&E** | M&E Lead, Monitoring & Evaluation Manager | Org team pages, academic profiles, conference speaker lists | LinkedIn via Google |
| **Default** | Any other role | LinkedIn via Google | -- |

**No user-facing step.** Coco resolves this internally based on job title and department.

---

### Step 2: Run 3-Layer Searches

Execute ALL three layers. Do not skip Layer 1.

#### Layer 1: Org Team Pages (WebFetch Directly)

Direct WebFetch of organization team pages. These are not blocked and often have the highest-quality candidate names + current roles.

```
# Pakistan education & development orgs
WebFetch: https://itacec.org/team/
WebFetch: https://theorg.com/org/idara-e-taleem-o-aagahi
WebFetch: https://www.tcf.org.pk/about-us/our-people/
WebFetch: https://www.zindagitrust.org/leadership-board
WebFetch: https://www.ppaf.org.pk/team
WebFetch: https://www.akdn.org/our-agencies/aga-khan-foundation/pakistan

# Conference speaker lists (active professionals who present publicly)
WebFetch: https://pakistanlearningfestival.com/plf-islamabad-2024/
WebFetch: https://pakistanlearningfestival.com/profiles/resource_persons_and_institutions-clf/

# Technical roles (GitHub user search)
WebFetch: https://github.com/search?q=[skill]+location%3APakistan&type=users
```

Log each search with `log_sourcing_action(platform="[Name]", query="[URL]", results_found=[N], context="org_team_page")`.

#### Layer 2: Targeted Google Searches

Most reliable pattern for Pakistani development sector: **org name + title, NOT LinkedIn site: query**.

**Fundraising / BD roles:**
```
"[org name]" "fundraising" OR "partnerships" OR "resource mobilization" staff Islamabad
"Citizens Foundation" OR "PPAF" OR "Zindagi Trust" "Vice President" OR "Manager" fundraising Pakistan
"TCF" OR "ITA" OR "Alif Ailaan" "head of" OR "director" partnerships OR development Pakistan
"DAI Pakistan" OR "Chemonics Pakistan" OR "RTI Pakistan" OR "Palladium Pakistan" partnerships education staff
```

**Education / Learning roles:**
```
"[org name]" "instructional design" OR "learning design" staff OR team Pakistan
"ITA" OR "TCF" OR "Teach For Pakistan" "manager" OR "lead" learning design curriculum
```

**Impact / M&E roles:**
```
"MEAL" OR "M&E" "lead" OR "manager" Pakistan USAID OR FCDO education Islamabad
"monitoring evaluation" "senior" Pakistan NGO education Islamabad 2024 2025
```

Log each search with `log_sourcing_action(platform="Google", query="[search string]", results_found=[N], context="targeted_google")`.

#### Layer 3: LinkedIn via Google (Catch-all)

**IMPORTANT:** LinkedIn blocks direct WebFetch (returns 999 error). Use Google site: queries ONLY.

Lower yield for Pakistani professionals but still run 3–4 queries as a sweep:

```
site:linkedin.com/in "[Job Title]" Pakistan
site:linkedin.com/in "[Job Title]" "[Primary Skill]" Karachi OR Lahore OR Islamabad
site:linkedin.com/in "[Skill 1]" "[Skill 2]" Pakistan EdTech OR education OR nonprofit
```

Log each search with `log_sourcing_action(platform="LinkedIn (Google)", query="[search string]", results_found=[N], context="linkedin_google")`.

---

### Step 3: Extract Candidate Profiles

For each promising result, extract:

- Full name
- Current role title
- Current company / organization
- Location (city, Pakistan)
- Key experience relevant to the role (2–3 bullet points)
- Platform (GitHub / LinkedIn / Org site / Conference list) + profile URL
- 1-sentence "why relevant" note (specific, never generic)

**Do not guess.** If information is missing, write "Not mentioned" in the profile.

---

### Step 4: Present Candidate Slate to Ayesha

Format:

```
## Talent Slate — [Role Title] — [Date]

Searched: [List platforms used] | Queries run: [N] | Results reviewed: [N] | Candidates surfaced: [N]

| # | Name | Current Role | Company | Location | Why Relevant | Profile |
|---|------|-------------|---------|----------|-------------|---------|
| 1 | Muhammad Abdullah | Senior Partnerships Manager | PPAF | Islamabad | 7 years fundraising + resource mobilization in education sector. Launched 3 major fund initiatives. | [linkedin.com/in/...](https://linkedin.com/in/...) |
```

**Rules:**
- Profile column MUST contain actual URLs, never placeholder text
- "Why Relevant" MUST be specific — actual experience, never generic phrases
- Never suppress a candidate — show everyone found, let Ayesha decide
- Location default: Pakistan-based only

---

### Step 5: Draft LinkedIn DMs

For each candidate Ayesha approves, write a personalized LinkedIn DM (150–200 words max).

**DM Template:**

```
Hi [First Name],

[1 specific observation about their work — NEVER generic "I came across your profile"]

I'm Ayesha, People & Culture team at Taleemabad — we're building AI-powered tools 
to improve learning quality for teachers and students across Pakistan. We're looking 
for a [Role Title] who can [core impact in 1 sentence].

Given your background in [specific experience], I think you'd find the challenge 
interesting -- and the mission even more so.

Would you be open to a 20-minute conversation to explore? No pressure at all 
if the timing isn't right.

Warm regards,
Ayesha Khan
People & Culture | Taleemabad
```

**Non-Negotiables:**
- Personalized opening (specific from profile, NOT generic)
- Mission-first paragraph
- Soft ask ("explore", "conversation", NOT "apply", "interview")
- 150–200 words max
- No em dashes (use ` -- `)
- Sign as Ayesha Khan (never "Coco")
- Ayesha sends manually (Coco drafts only)

---

### Step 6: Save Output File

Save to: `output/sourcing/[role-slug]-[YYYY-MM-DD].md`

Contains:
1. Search summary (platforms, queries, results reviewed)
2. Full candidate slate table
3. Full DM drafts per approved candidate (copy-paste ready)

---

### Step 7: Add Confirmed Candidate to Markaz

**ONLY after Ayesha confirms:** "[Name] confirmed interest"

1. Get job ID from Markaz
2. Run `scripts/sourcing/insert_sourced_candidate.py`
3. Script inserts into `candidates` and `applications` tables
4. Return candidate ID and application ID to Ayesha

---

## Non-Negotiable Rules

1. **Never add to Markaz before confirmed interest** — Most important rule
2. **Ayesha sends DMs manually** — Coco drafts only
3. **Layer 1 (org pages) always first** — Highest quality sources
4. **LinkedIn direct WebFetch fails** — Use Google site: queries ONLY
5. **Audit log every search and DB access** — Use `log_sourcing_action()` and `log_db_query()`
6. **Pakistan-based by default** — Diaspora only if explicitly requested
7. **No data fabrication** — Write "Not mentioned" if missing
8. **Personalization is mandatory** — Every DM opening must reference something specific

---

## Commitment

I, Coco, commit to following this SOP exactly for all talent sourcing work.

**Date Locked In:** 2026-04-16  
**Adapted From:** Noah's talent-sourcing SKILL.md  
**Reference:** This SOP file (talent_sourcing.md)
