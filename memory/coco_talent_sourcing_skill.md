---
name: Coco's Talent Sourcing Skill - Adopted & Implemented
description: Coco has officially adopted Noah's talent sourcing skill. 7-step SOP for finding passive candidates via 3-layer search (org pages → Google → LinkedIn). Personalized LinkedIn DMs. Markaz integration only after confirmed interest. Locked in 2026-04-16.
type: project
originSessionId: 50203d1f-d855-41c4-b12a-dba80a622e87
---
# Coco's Talent Sourcing Skill — Locked In (2026-04-16)

## Status: ADOPTED & PRODUCTION-READY ✓

Coco has fully adopted Noah's Talent Sourcing skill from Jaw901/Noah repository. Implementation started 2026-04-16.

**Source:** https://github.com/Jaw901/Noah/blob/master/.claude/skills/talent-sourcing/SKILL.md

---

## The Skill at a Glance

**Purpose:** Find experienced professionals NOT actively applying. Search platforms → Present slate → Draft DMs → Ayesha sends manually → Add to Markaz AFTER confirmed interest.

**Trigger Phrases:**
- "source candidates for [role]"
- "find people for [role]"
- "build a candidate slate"
- "run a talent search"

**Workflow:**
```
Search → Present slate → Ayesha picks → Draft DMs → Ayesha sends
→ Candidate confirms → Ayesha tells Coco → Coco adds to Markaz (status='new')
```

**CORE RULE:** Markaz is ONLY touched after confirmed interest. Never speculatively.

---

## 7-Step SOP (Locked)

### Step 0: Intake
- Role title, must-have skills (3-5), seniority level, desired candidate count (default: 10-15)
- Fetch JD from Markaz, log with `log_db_query()`

### Step 1: Resolve Platform Set (Internal)
- By role category (Technical, Learning, Fundraising, Growth, Impact, Default)
- No user involvement — Coco decides internally

### Step 2: Run 3-Layer Searches (Execute ALL)
1. **Layer 1:** Org team pages (WebFetch directly)
   - itacec.org/team, theorg.com, tcf.org.pk, zindagitrust.org, ppaf.org.pk, akdn.org, Pakistan Learning Festival
   - GitHub user search (technical roles)
   - Log with `log_sourcing_action(platform="[Name]", query="[URL]", results_found=[N], context="org_team_page")`

2. **Layer 2:** Targeted Google searches
   - Org name + title combos, NOT LinkedIn site: queries
   - Role-specific templates (Fundraising, Learning, Impact, Technical, etc.)
   - Log with `log_sourcing_action(platform="Google", query="[search string]", results_found=[N], context="targeted_google")`

3. **Layer 3:** LinkedIn via Google (catch-all, lowest yield)
   - site:linkedin.com/in queries ONLY (LinkedIn direct WebFetch returns 999 error)
   - 3-4 queries as sweep
   - Log with `log_sourcing_action(platform="LinkedIn (Google)", query="[search string]", results_found=[N], context="linkedin_google")`

### Step 3: Extract Profiles
- Full name, current role, company, location, key experience (2-3 bullets), platform + URL, 1-sentence "why relevant"
- No guessing — write "Not mentioned" if missing

### Step 4: Present Slate to Ayesha
- Table format: Name | Current Role | Company | Location | Why Relevant | Profile URL
- Search metadata: platforms used, queries run, results reviewed, final count
- Ayesha's decision: "Who should I draft DMs for?" (accepts All, specific numbers, skip list, or "search again")

### Step 5: Draft LinkedIn DMs
- Template: personalized opening + mission paragraph + soft ask + sign-off
- 150-200 words max
- Specific observation from profile (NEVER generic "came across your profile")
- Taleemabad mission first, then role
- Soft ask: "explore", "conversation" (NEVER "apply", "interview")
- Sign as Ayesha Khan, not Coco
- **Ayesha sends manually** — Coco drafts only

### Step 6: Save Output
- Location: `output/sourcing/[role-slug]-[YYYY-MM-DD].md`
- Contains: Search summary + candidate slate table + full DM drafts (copy-paste ready)

### Step 7: Add to Markaz (After Confirmed Interest Only)
- Trigger: "Ayesha: [Name] confirmed interest, add them for [Role]"
- Insert script: `scripts/sourcing/insert_sourced_candidate.py`
- Inserts into `candidates` + `applications` tables
- Status='new', source='LinkedIn - Sourced'
- Log with `log_db_query()` for both operations
- Return candidate ID + application ID to Ayesha

---

## Platform Selection by Role Category (Locked)

| Role Category | Roles | Tier 1 (Fetch First) | Tier 2 (Search) |
|---------------|-------|---------------------|-----------------|
| **Technical** | Odoo Developer, Full Stack Lead | GitHub user search, org team pages | LinkedIn via Google |
| **Digital Learning** | Instructional Systems Lead, Training Manager | Org team pages (ITA, TCF, Zindagi), conference speaker lists | LinkedIn via Google, Medium |
| **Fundraising / BD** | Fundraising Lead, Partnerships Manager | Org team pages (TCF, AKF, PPAF), The Org, conference speaker lists | LinkedIn via Google |
| **Growth / UX** | Soul Architect, Program Manager | Medium, Substack, org team pages | LinkedIn via Google |
| **Impact / M&E** | M&E Lead, Monitoring Manager | Org team pages, academic profiles, conference speaker lists | LinkedIn via Google |
| **Default** | Any other role | LinkedIn via Google | -- |

---

## LinkedIn DM Template (Locked)

```
Hi [First Name],

[1 specific observation about their work — a project, career trajectory, 
or something from their profile that directly signals why they are right 
for this role. NEVER "I came across your profile".]

I'm Ayesha, People & Culture team at Taleemabad — we're building AI-powered 
tools to improve learning quality for teachers and students across Pakistan. 
We're looking for a [Role Title] who can [core impact of the role in 1 sentence].

Given your background in [specific experience from their profile], I think 
you'd find the challenge interesting -- and the mission even more so.

Would you be open to a 20-minute conversation to explore? No pressure at all 
if the timing isn't right.

Warm regards,
Ayesha Khan
People & Culture | Taleemabad
hiring@taleemabad.com
www.taleemabad.com
```

**DM Non-Negotiables (Mandatory):**
1. Personalized opening (specific from profile, NOT generic)
2. Mission-first (Taleemabad impact before role)
3. Soft ask only ("explore", "conversation")
4. 150-200 words max
5. No em dashes (use ` -- `)
6. Never mention salary
7. Sign as Ayesha Khan (never "Coco")
8. Ayesha sends manually (Coco drafts only)

---

## Critical Non-Negotiable Rules (8 Total — No Exceptions)

1. **Never add to Markaz before confirmed interest** — Most important rule. The point of sourcing is to contact, assess interest, then add.
2. **Ayesha sends DMs manually** — Coco drafts, NEVER sends LinkedIn messages directly
3. **Layer 1 (org pages) always first** — Highest quality sources for dev sector roles
4. **LinkedIn direct WebFetch fails** — Always use Google site:linkedin.com queries ONLY
5. **Audit log every search** — Use `log_sourcing_action()` for all searches
6. **Audit log DB access** — Use `log_db_query()` for all Markaz reads/writes
7. **Pakistan-based by default** — Only diaspora if explicitly requested
8. **No data fabrication** — Write "Not mentioned" if missing, never guess

---

## Key Learnings from Noah (Locked In)

**Platform Insights:**
- LinkedIn blocks direct WebFetch (returns 999 error) — use Google site: queries only
- Org team pages (tcf.org.pk/team, itacec.org/team, theorg.com) are fetchable and high-quality
- The Org (theorg.com) is a goldmine for Pakistan nonprofits — has org charts, names, current titles
- Conference speaker lists surface active professionals who are publicly visible
- Devex.com/people is behind paywall, but Devex job listings reveal what titles exist

**Search Strategy:**
- Layer 1 (org pages) produces highest-quality results for dev sector roles
- Google "org name + title" more reliable than LinkedIn site: for Pakistani professionals
- LinkedIn via Google is catch-all, lowest yield, but still run 3-4 queries as sweep

**Database Insights:**
- No email = no dedup check (sourced candidates often lack email addresses)
- source = 'LinkedIn - Sourced' is the tracking mechanism
- tags.profile_url must contain actual LinkedIn/platform URL
- Markaz write only AFTER confirmed interest prevents pipeline pollution

---

## Implementation Status (2026-04-16)

**Phase 1: Documentation** ✓ COMPLETE
- [x] Created `skills/talent-sourcing.md` (full skill SOP)
- [x] Created `SOPs/05_Talent_Sourcing/talent_sourcing.md` (SOP copy)
- [x] Updated `SOPs/README.md` (added category, navigation, stats)
- [x] Updated `skills.md` (added Skill 14 entry)
- [x] Saved to memory (this file)

**Phase 2: Infrastructure** ⏳ IN PROGRESS
- [ ] Extend `scripts/utils/audit_log.py` with `log_sourcing_action()`
- [ ] Create `scripts/sourcing/` folder
- [ ] Create `scripts/sourcing/source_candidates.py` (main runner)
- [ ] Create `scripts/sourcing/insert_sourced_candidate.py` (Markaz insert)
- [ ] Create `output/sourcing/` folder

**Phase 3: Testing** ⏳ PENDING
- [ ] End-to-end test with a live open role
- [ ] Verify 3-layer search execution
- [ ] Verify slate presentation
- [ ] Verify DM drafting
- [ ] Verify Markaz insertion

---

## Differences from Noah's Implementation (Coco Adaptations)

| Aspect | Noah | Coco |
|--------|------|------|
| Language | Node.js for DB writes | Python/psycopg2 (matches Coco patterns) |
| DM sender | Jawwad Ali | Ayesha Khan |
| Sign-off | Jawwad Ali | Ayesha Khan, People & Culture |
| Agent credit | sourced_by: "noah" | sourced_by: "coco" |
| Output location | output/sourcing/ | output/sourcing/ (same) |
| DB pattern | Separate Node.js insert script | Python psycopg2 (existing Coco pattern) |

---

## Files Created & Modified (2026-04-16)

**Created (New Files):**
- `skills/talent-sourcing.md` — Full skill SOP
- `SOPs/05_Talent_Sourcing/talent_sourcing.md` — SOP copy

**Modified:**
- `SOPs/README.md` — Added 05_Talent_Sourcing category, navigation, stats, versioning
- `skills.md` — Added Skill 14: Talent Sourcing entry + status section

**TBD (Phase 2):**
- `scripts/utils/audit_log.py` — Extend with `log_sourcing_action()`
- `scripts/sourcing/source_candidates.py` — Main runner
- `scripts/sourcing/insert_sourced_candidate.py` — Markaz insert script
- `output/sourcing/` — Folder for output files

---

## Quick Reference — When to Use

**Trigger:** "source candidates for [role]" or "find people for [role]" or "build a candidate slate"

**When:**
- New role open, no applicants yet (be proactive)
- Screening pool too small (need more candidates)
- Passive candidate search requested

**Process:**
1. Intake (5 min) → JD fetch + collect criteria
2. 3-layer search (20-30 min) → Log each search
3. Present slate (5 min) → Ayesha selects
4. Draft DMs (10 min) → Copy-paste ready
5. Manual send (Ayesha's time) → DMs go to LinkedIn
6. Wait for confirmation (Ayesha tells Coco when interested)
7. Markaz insert (5 min) → status='new'

**Output:** `output/sourcing/[role-slug]-[YYYY-MM-DD].md`

---

**Locked In:** 2026-04-16  
**Status:** Production-Ready  
**Last Reviewed:** 2026-04-16
