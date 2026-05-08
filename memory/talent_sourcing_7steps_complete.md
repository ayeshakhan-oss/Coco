---
name: Talent Sourcing — 7-Step Complete Reference
description: Complete 7-step SOP for talent sourcing. Intake → Platform Resolution → 3-Layer Searches → Extract → Present → Draft DMs → Save Output → Add to Markaz. All non-negotiables, examples, and infrastructure locked in. 2026-04-16.
type: project
originSessionId: 50203d1f-d855-41c4-b12a-dba80a622e87
---
# Talent Sourcing — Complete 7-Step Reference

**Status:** PHASE 2 INFRASTRUCTURE COMPLETE ✓  
**Date Locked In:** 2026-04-16  
**Next Phase:** Phase 3 — End-to-End Testing  
**Adapted From:** Noah (Jaw901/Noah repository)

---

## OVERVIEW

**Purpose:** Find experienced professionals NOT actively applying. Search → Present slate → Draft DMs → Ayesha sends manually → Add to Markaz after confirmed interest.

**Workflow:**
```
Step 0 (Intake) → Step 1 (Platform Select) → Step 2 (3-Layer Search)
→ Step 3 (Extract) → Step 4 (Present) → Step 5 (Draft DMs)
→ Step 6 (Save) → Step 7 (Add to Markaz after confirmation)
```

---

## 7 STEPS — DETAILED

### STEP 0: INTAKE (5 minutes)

**Collect from Ayesha:**
1. Role title (exact)
2. Top 3-5 must-have skills/experiences
3. Seniority level (e.g., "8+ years", "senior")
4. How many candidates? (default 15)

**Fetch from Markaz:**
```sql
SELECT id, title, jd_text, required_skills, department
FROM jobs
WHERE title ILIKE '%[role]%' AND status = 'published'
LIMIT 1;
```

**Log:** `log_db_query(table='jobs', filters="title ILIKE '%...'", rows_returned=1, context='intake_jd_fetch')`

**Output:** Role details + JD summary

**Rule:** Never guess — use actual Markaz data

---

### STEP 1: PLATFORM RESOLUTION (2 minutes)

**Internal decision** based on role category (no user involvement):

| Role Category | Roles | Tier 1 (Fetch First) | Tier 2 (Search) |
|---|---|---|---|
| **Technical** | Odoo Developer, Full Stack Lead | GitHub user search, org team pages | LinkedIn via Google |
| **Digital Learning** | Instructional Systems Lead, Training Manager | Org team pages (ITA, TCF, Zindagi), conference speaker lists | LinkedIn via Google, Medium |
| **Fundraising / BD** | Fundraising Lead, Partnerships Manager | Org team pages (TCF, AKF, PPAF), The Org, conference lists | LinkedIn via Google |
| **Growth / UX** | Soul Architect, Program Manager | Medium, Substack, org team pages | LinkedIn via Google |
| **Impact / M&E** | M&E Lead, Monitoring & Evaluation Manager | Org team pages, academic profiles, conference lists | LinkedIn via Google |
| **Default** | Any other | LinkedIn via Google | -- |

**Output:** Selected platforms (Tier 1 + Tier 2)

**Rule:** Layer 1 (org pages) ALWAYS first — highest quality

---

### STEP 2: 3-LAYER SEARCHES (25 minutes)

**LAYER 1: Org Team Pages (WebFetch directly)**

```
# Education & development orgs
https://itacec.org/team/
https://theorg.com/org/idara-e-taleem-o-aagahi
https://www.tcf.org.pk/about-us/our-people/
https://www.zindagitrust.org/leadership-board
https://www.ppaf.org.pk/team
https://www.akdn.org/our-agencies/aga-khan-foundation/pakistan

# Conference speaker lists
https://pakistanlearningfestival.com/plf-islamabad-2024/
https://pakistanlearningfestival.com/profiles/resource_persons_and_institutions-clf/

# Technical roles
https://github.com/search?q=[skill]+location%3APakistan&type=users
```

**Log:** `log_sourcing_action(platform="[Name]", query="[URL]", results_found=[N], context="org_team_page")`

---

**LAYER 2: Targeted Google Searches (NOT LinkedIn site:)**

**Fundraising / BD:**
```
"[org name]" "fundraising" OR "partnerships" OR "resource mobilization" staff Islamabad
"Citizens Foundation" OR "PPAF" OR "Zindagi Trust" "Vice President" OR "Manager" fundraising Pakistan
"TCF" OR "ITA" OR "Alif Ailaan" "head of" OR "director" partnerships OR development Pakistan
"DAI Pakistan" OR "Chemonics Pakistan" OR "RTI Pakistan" partnerships education staff
```

**Learning / Training:**
```
"[org name]" "instructional design" OR "learning design" staff OR team Pakistan
"ITA" OR "TCF" OR "Teach For Pakistan" "manager" OR "lead" learning design curriculum
```

**Impact / M&E:**
```
"MEAL" OR "M&E" "lead" OR "manager" Pakistan USAID OR FCDO education Islamabad
"monitoring evaluation" "senior" Pakistan NGO education Islamabad 2024 2025
```

**Log:** `log_sourcing_action(platform="Google", query="[search string]", results_found=[N], context="targeted_google")`

---

**LAYER 3: LinkedIn via Google (Catch-all, lowest yield)**

```
site:linkedin.com/in "[Job Title]" Pakistan
site:linkedin.com/in "[Job Title]" "[Primary Skill]" Karachi OR Lahore OR Islamabad
site:linkedin.com/in "[Skill 1]" "[Skill 2]" Pakistan EdTech OR education OR nonprofit
```

**Log:** `log_sourcing_action(platform="LinkedIn (Google)", query="[search string]", results_found=[N], context="linkedin_google")`

**Rules:**
- LinkedIn direct WebFetch FAILS (999 error) — ALWAYS use Google site: only
- Pakistan-based by default — diaspora only if explicitly requested
- RUN ALL THREE LAYERS — don't skip

**Output:** ~25-50 results reviewed

---

### STEP 3: EXTRACT CANDIDATE PROFILES (10 minutes)

**For each promising result:**
- Full name
- Current role title
- Current company/organization
- Location (city)
- Key experience relevant to role (2-3 bullets)
- Platform + actual URL
- 1-sentence "why relevant" note (specific, NEVER generic)

**Example:**
```
Name: Muhammad Hassan Khan
Current Role: Senior Learning Designer
Company: ITA (Idara-e-Taleem-o-Aagahi)
Location: Islamabad
Experience:
  • 8+ years instructional design and curriculum development
  • Led implementation of LMS for 500+ educators across Pakistan
  • Designed competency frameworks for teacher training programs
Platform: LinkedIn
URL: https://linkedin.com/in/muhammad-hassan-khan-xyz
Why Relevant: Deep curriculum expertise + learning systems experience directly matches our need for systemic education impact
```

**Rules:**
- No guessing — write "Not mentioned" if missing
- Specific experience, NEVER generic
- Real URLs only

**Output:** Structured candidate profiles

---

### STEP 4: PRESENT CANDIDATE SLATE TO AYESHA (5 minutes)

**Format:**

```
## Talent Slate — [Role Title] — [Date]

Searched: [platforms] | Queries run: [N] | Results reviewed: [N] | Surfaced: [N]

| # | Name | Current Role | Company | Location | Why Relevant | Profile |
|---|------|-------------|---------|----------|-------------|---------|
| 1 | Muhammad Hassan Khan | Senior Learning Designer | ITA | Islamabad | 8 years curriculum design + learning systems. Led 5 major EdTech implementations. | [linkedin.com/in/...](https://linkedin.com/in/...) |
| 2 | Fatima Ali | Training Director | TCF | Lahore | 10+ years teacher training design. Structured nationwide professional development. | [linkedin.com/in/...](https://linkedin.com/in/...) |

**Who should I draft DMs for?**
- "All"
- "1 and 3"
- "Skip 4 -- rest are fine"
- "None of these -- search again"
```

**Rules:**
- Show EVERYONE found — let Ayesha decide
- Profile column = ACTUAL URLs (not placeholders)
- "Why Relevant" = specific experience (not generic)
- Never suppress a candidate

**Output:** Approved list for DM drafting

---

### STEP 5: DRAFT PERSONALIZED LINKEDIN DMs (10-15 minutes)

**Template (150-200 words max):**

```
Hi [First Name],

[1 specific observation about their work — a project, career trajectory, or 
something from their profile that directly signals why they're right for this role.
NEVER use "I came across your profile" or generic phrases.]

I'm Ayesha, People & Culture team at Taleemabad — we're building AI-powered 
tools to improve learning quality for teachers and students across Pakistan. 
We're looking for a [Role Title] who can [core impact of the role in 1 sentence].

Given your background in [specific experience from their profile], I think you'd 
find the challenge interesting -- and the mission even more so.

Would you be open to a 20-minute conversation to explore? No pressure at all 
if the timing isn't right.

Warm regards,
Ayesha Khan
People & Culture | Taleemabad
hiring@taleemabad.com
www.taleemabad.com
```

**Non-Negotiables:**
1. Personalized opening (specific from profile, NOT generic)
2. Mission-first paragraph (Taleemabad impact before role)
3. Soft ask ONLY ("explore", "conversation" — NEVER "apply", "interview", "opportunity")
4. 150-200 words max
5. No em dashes (use ` -- `)
6. Never mention salary in first outreach
7. Sign as Ayesha Khan, NEVER "Coco"
8. **Ayesha sends manually** — Coco drafts only, never sends LinkedIn DMs

**Output:** Copy-paste ready DMs

---

### STEP 6: SAVE OUTPUT FILE (2 minutes)

**Location:** `output/sourcing/[role-slug]-[YYYY-MM-DD].md`

**Examples:**
- `output/sourcing/instructional-systems-lead-2026-04-20.md`
- `output/sourcing/fundraising-lead-2026-04-22.md`
- `output/sourcing/m-e-lead-2026-04-18.md`

**File contains:**
1. Search summary (platforms, queries run, results reviewed)
2. Full candidate slate table
3. Full DM draft per approved candidate (copy-paste ready)

**Output:** Markdown file saved locally, ready for Ayesha's manual LinkedIn sends

---

### STEP 7: ADD CONFIRMED CANDIDATE TO MARKAZ (5 minutes)

**Triggered by:** Ayesha says "[Name] confirmed interest, add them for [Role]"

**Process:**
1. Fetch job ID: `SELECT id FROM jobs WHERE title ILIKE '%[role]%' LIMIT 1`
2. Run: `python scripts/sourcing/insert_sourced_candidate.py`
3. Script inserts into `candidates` table
4. Script inserts into `applications` table (status='new')
5. Log operations: `log_db_query()`
6. Return candidate ID + application ID to Ayesha

**Database fields (candidates table):**
```
first_name, last_name
email (null for LinkedIn sourced)
position = '[Role Title]'
skills = ['skill1', 'skill2']
source = 'LinkedIn - Sourced'  ← EXACT STRING
location, current_position, current_company
tags = {
  "sourced_by": "coco",
  "sourcing_run": "YYYY-MM-DD",
  "profile_url": "[actual LinkedIn/GitHub/org URL]"
}
```

**Database fields (applications table):**
```
candidate_id
job_id
status = 'new'
notes = 'Passive sourced candidate -- confirmed interest via LinkedIn DM'
ai_recommendation = 'Sourced candidate -- pending CV review'
ai_screening_summary = 'Sourced on YYYY-MM-DD from LinkedIn - Sourced. Profile: [URL]'
```

**Rules:**
- ONLY after confirmed interest — NEVER before
- Ayesha tells Coco first
- Log both database operations via `log_db_query()`
- No email = no dedup check (email may be null)

**Output:** Candidate ID + Application ID confirmed back to Ayesha

---

## 8 CRITICAL NON-NEGOTIABLES

1. **Never add to Markaz before confirmed interest** — Most important. Whole point is to contact first, assess interest, THEN add.
2. **Ayesha sends DMs manually** — Coco drafts only. NEVER send LinkedIn messages directly.
3. **Layer 1 (org pages) always first** — Highest quality sources for dev sector roles.
4. **LinkedIn direct WebFetch fails** — Returns 999 error. ALWAYS use Google site:linkedin.com queries only.
5. **Audit log every search** — Use `log_sourcing_action()` for all platform searches.
6. **Audit log all DB access** — Use `log_db_query()` for all Markaz reads/writes.
7. **Pakistan-based by default** — Only surface diaspora if explicitly requested by Ayesha.
8. **No data fabrication** — Write "Not mentioned" if missing. NEVER guess or fill gaps.

---

## INFRASTRUCTURE CREATED (PHASE 2)

### Audit Logging
- **File:** `scripts/utils/audit_log.py`
- **New function:** `log_sourcing_action(platform, query, results_found, context)`
- **Log file:** `logs/sourcing_audit.log`
- **Pattern:** Matches existing `log_db_query()` format

### Database Insertion
- **File:** `scripts/sourcing/insert_sourced_candidate.py`
- **Purpose:** Add confirmed candidate to Markaz (Step 7)
- **Function:** `insert_sourced_candidate(first_name, last_name, position, skills, location, current_position, current_company, job_id, profile_url, email=None, phone=None, sourcing_run_date=None)`
- **Returns:** `{candidate_id, application_id, status, source, sourcing_run}`
- **Logs:** Both `candidates` and `applications` insert operations

### Main Runner
- **File:** `scripts/sourcing/source_candidates.py`
- **Purpose:** Execute Steps 0-6 of 7-step SOP
- **Functions:**
  - `intake_role_details()` — Step 0
  - `resolve_platform_set(job_details)` — Step 1
  - `run_3layer_searches(role_details, platform_set)` — Step 2
  - `generate_slate_markdown(role_details, candidates, sourcing_date)` — Steps 3-4
  - `save_output_file(output_content, role_title, sourcing_date)` — Step 6
  - `run_talent_search(role_title)` — Main entry point

### Output Directory
- **Location:** `output/sourcing/`
- **Format:** `[role-slug]-[YYYY-MM-DD].md`
- **Contains:** Search summary + candidate slate table + DM drafts

---

## SYMMETRY WITH NOAH

| Element | Noah Pattern | Coco Implementation |
|---------|---|---|
| Output folder | `output/sourcing/[role-slug]-[YYYY-MM-DD].md` | ✓ Same structure |
| DB insert | Node.js script | Python psycopg2 (matches Coco patterns) |
| Source field | `'LinkedIn - Sourced'` | ✓ Exact same string |
| Tags | `{sourced_by: 'noah', sourcing_run, profile_url}` | `{sourced_by: 'coco', sourcing_run, profile_url}` |
| Operations | INSERT candidates + applications | ✓ Same structure |
| Status | `status='new'` | ✓ Same |
| Trigger | "Jawwad: [Name] confirmed interest" | "Ayesha: [Name] confirmed interest" |

---

## NEXT PHASE: PHASE 3 — END-TO-END TESTING

**What we'll do:**
1. Identify a live open role in Markaz
2. Run full 7-step process from start to finish
3. Test each script (source_candidates.py, insert_sourced_candidate.py)
4. Verify audit logging (sourcing_audit.log + read_audit.log)
5. Confirm output file generation
6. Test Markaz insertion with real database

**Expected deliverables:**
- ✓ Markdown output file with candidate slate + DMs
- ✓ sourcing_audit.log entries for all searches
- ✓ read_audit.log entry for JD fetch
- ✓ Successful Markaz insertion (test only, no real candidate added)
- ✓ Confirmation IDs returned

---

**Status:** LOCKED IN 2026-04-16  
**Next Review:** After Phase 3 testing  
**Remember:** Follow 8 non-negotiables ALWAYS. No exceptions.
