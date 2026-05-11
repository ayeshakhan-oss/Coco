---
name: talent-sourcing
description: Systematic passive candidate sourcing across 3 layers (org pages, Google search, LinkedIn). Find verified mid-level candidates. 7-step SOP. Excel output.
compatibility: Requires memory/talent_sourcing_7steps_complete.md, Google/LinkedIn searches, Markaz API, Excel generation
---

# Talent Sourcing

Systematically source passive candidates through 3-layer research (org pages, Google search, LinkedIn verification). Draft personalized outreach for Ayesha.

---

## When to Use This Skill

Trigger this skill when:
- User asks to "source candidates for [position]"
- User requests "find talent for [role]" or "passive search"
- User wants candidate outreach for potential hires
- Excel list needed for Ayesha's review

---

## Related SOP (Source of Truth)

**Location:** `SOPs/05_Talent_Sourcing/talent_sourcing.md`

This skill orchestrates the 7-step passive candidate sourcing process. The SOP contains:
- Complete 7-step workflow (Intake through Markaz)
- 3-layer search strategy
- Candidate verification rules
- DM personalization guidelines
- Excel output format
- Non-negotiable rules (no mass outreach, wait for interest, etc.)

---

## Universal Rules (All Sourcing)

**3-Layer Search (Mandatory):**
- Layer 1: Org pages (company websites, LinkedIn companies)
- Layer 2: Google site:linkedin.com (role-specific searches)
- Layer 3: LinkedIn verification (test links active)
- All three layers required (never skip)

**Candidate Verification:**
- LinkedIn links must be active (test if critical)
- Name + role + experience confirmed
- Location verified
- No unverified sources

**Markaz Integration (CRITICAL):**
- NEVER add to Markaz before interest confirmed
- Wait for "yes" response from Ayesha's outreach
- Only then: add with source='LinkedIn - Sourced'

**DM Personalization:**
- Always personalized (not templated)
- Reference specific work/project
- Explain why role fits THEM
- Ayesha sends (not Coco)
- One per candidate

**Output Format:**
- Excel sheet: Name, LinkedIn URL, Role, Company, Exp, Tier (1/2/3)
- Sent to Ayesha for review + manual outreach
- Include sourcing methodology
- Document date, sourcing_run ID, researcher

---

## Execution Discipline

**STEP 0: INTAKE**
- Role title, persona, keywords, location, experience level

**STEP 1: DEFINE SEARCH STRATEGY**
- Read: memory/talent_sourcing_7steps_complete.md
- Identify: 3-5 target companies/sectors
- List: 3-5 LinkedIn search terms

**STEP 2: SEARCH ORG PAGES (Layer 1)**
- Google: "[Company] LinkedIn people" or company.com/employees
- Extract: names, titles, companies, LinkedIn URLs

**STEP 3: GOOGLE SITE:LINKEDIN.COM (Layer 2)**
- Query: site:linkedin.com "[keyword1]" "[keyword2]"
- Vary title, experience, location
- Extract: names and URLs

**STEP 4: VERIFY LINKS (Layer 3)**
- Open each URL (verify link active)
- Confirm: title matches, profile current
- Keep only: verified, active links

**STEP 5: EXTRACT VERIFIED CANDIDATES**
- Row per candidate: Name, URL, Role, Company, Experience, Tier
- Tier 1 = perfect match
- Tier 2 = good fit
- Tier 3 = possible fit
- Target: 40-60 candidates minimum

**STEP 6: DRAFT PERSONALIZED DMS**
- Read: LinkedIn profile fully
- Find: specific project/skill connecting to role
- Write: DM explaining why role fits THEM
- Keep: short, personalized, authentic

**STEP 7: ADD TO MARKAZ (AFTER CONFIRMATION)**
- Wait for Ayesha response: "They replied positively"
- Only then: add to Markaz
- Source: 'LinkedIn - Sourced'
- Tags: {sourced_by, sourcing_run, profile_url}

**STEP 8: GENERATE EXCEL OUTPUT**
- Columns: Name, URL, Role, Company, Experience, Tier
- Include: Sourcing Methodology sheet
- Count summary (total, by tier)
- Send to Ayesha for review

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Using only one layer | Incomplete search | Use all 3 layers (org + Google + LinkedIn) |
| Adding to Markaz early | Wastes data | Wait for confirmed interest (YES response) |
| Template DMs | Low response rate | Personalize (reference their specific work) |
| Dead links included | Time wasted | Test links before sending to Ayesha |
| Small candidate pool | Limited options | Target 40-60 minimum per round |
| No tier categorization | Hard to prioritize | Rate: 1 (perfect), 2 (good), 3 (possible) |
| Missing source documentation | Can't track effectiveness | Document: keywords, sources, date |

---

## Success Criteria

✅ All 7 steps executed in order  
✅ 3 layers searched (org pages + Google + LinkedIn verify)  
✅ LinkedIn links verified active  
✅ 40-60 candidates minimum  
✅ Candidates tiered (1/2/3)  
✅ DMs personalized (not templated)  
✅ No premature Markaz entries (wait for confirmation)  
✅ Excel output complete with methodology  
✅ Sent to Ayesha for review  

---

## Self-QA Checklist (Before Sending to Ayesha)

- [ ] Intake completed (role, persona, keywords, location)
- [ ] Search strategy defined (3-5 companies, 3-5 search terms)
- [ ] Layer 1 (org pages) searched
- [ ] Layer 2 (Google site:linkedin.com) searched
- [ ] Layer 3 (LinkedIn verify) completed (all links active)
- [ ] 40-60 candidates extracted
- [ ] All candidates tiered (1/2/3)
- [ ] DMs drafted (personalized, not templated)
- [ ] Excel generated (Name, URL, Role, Company, Exp, Tier)
- [ ] Sourcing Methodology sheet included
- [ ] No Markaz entries created (waiting for interest)
- [ ] Ready to send to Ayesha

---

## Resources & Templates

**Complete SOP:**
- 7 Steps Detailed: `memory/talent_sourcing_7steps_complete.md`
- Step Examples: `memory/talent_sourcing_steps_explained.md`

**Reference Scripts:**
- Example: `scripts/sourcing/create_soul_architect_47_verified.py`
- Excel: `scripts/sourcing/create_soul_architect_sheet.py`

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)
- Skill 7 (Talent Sourcing): `RULES.md` (lines 357-392)

---

## Commit to Discipline

I will source candidates with:
- ✅ All 7 steps (in order)
- ✅ 3-layer search (org + Google + LinkedIn verify)
- ✅ Links verified (tested, not dead)
- ✅ No premature Markaz entries (wait for YES)
- ✅ Personalized DMs (not templated)
- ✅ 40-60 candidates minimum
- ✅ Excel output with methodology
- ✅ All checklist items passing

**Status:** ✅ PRODUCTION READY
