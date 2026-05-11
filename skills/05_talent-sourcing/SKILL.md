---
name: talent-sourcing
description: Systematic passive candidate sourcing across 3 layers (org pages, Google search, LinkedIn). Find verified mid-level candidates, draft personalized LinkedIn DMs for Ayesha to send, and add to Markaz only after confirmed interest. 7-step SOP with Excel output and no Markaz insertion until explicit confirmation.
compatibility: Requires memory/talent_sourcing_7steps_complete.md, Google/LinkedIn searches, Markaz API, Excel generation
---

# Talent Sourcing

Find passive candidates through systematic 3-layer research, verify LinkedIn links, draft personalized outreach, and add to Markaz only after confirmed interest.

---

## Architecture

**This skill is an orchestration layer** that references the detailed SOPs in `SOPs/05_Talent_Sourcing/`.

- **SKILL.md (this file):** Master orchestration, universal rules, execution discipline
- **SOPs folder (source of truth):** Detailed procedures for passive candidate sourcing

When you use this skill, you get:
1. Universal rules and checklist (from this SKILL.md)
2. Detailed procedures (from linked SOPs — the source of truth)

**Important:** SOPs are maintained as the single source of truth. If procedures change, they update in SOPs/ and are automatically reflected here.

---

## When to Use This Skill

Trigger this skill when:
- User asks to "source candidates for [position]"
- User requests "find talent for [role]" or "passive candidate search"
- User wants "LinkedIn search results" or "candidate list"
- User needs "candidate outreach" or "DM templates"
- Any proactive candidate research and recruitment

---

## Related SOPs

All sourcing work falls under this skill:

**Talent Sourcing** — `SOPs/05_Talent_Sourcing/talent_sourcing.md`

Complete 7-step process:
1. Intake: Role definition, persona, keywords, location
2. Search org pages (company websites, LinkedIn companies)
3. Google site:linkedin.com searches (verified links)
4. Extract verified candidates (name, LinkedIn URL, role)
5. Craft personalized LinkedIn DMs (Ayesha sends, not Coco)
6. Wait for response (no assumption of interest)
7. Add to Markaz ONLY after confirmed interest

---

## Universal Rules (All Sourcing)

**3-Layer Search (MANDATORY):**
- Layer 1: Org pages (company websites, company LinkedIn pages)
- Layer 2: Google site:linkedin.com searches (specific to role + keywords)
- Layer 3: LinkedIn direct verification (ensure links active)
- Never skip layers (all three required)

**Candidate Verification:**
- LinkedIn links must be active (test manually if critical)
- Name + role + experience confirmed across sources
- Location verified (remote/onsite preference)
- No cold outreach to unverified sources

**Markaz Integration (CRITICAL):**
- NEVER add to Markaz before interest confirmed
- Wait for explicit "yes" response
- Document source field: 'LinkedIn - Sourced'
- Add tags: {sourced_by, sourcing_run, profile_url}

**DM Personalization:**
- ALWAYS personalized (not templated)
- Reference specific work or project they mention
- Explain why Taleemabad role fits their background
- Ayesha sends DMs (not Coco)
- One per candidate (no mass outreach)

**Output Format:**
- Excel sheet with: Name, LinkedIn URL, Role, Company, Experience, Tier (1/2/3)
- Sent to Ayesha for review + manual outreach
- Include sourcing methodology (which layers, search terms)
- Document: date, sourcing_run ID, researcher

**Self-QA Before Sending:**
- [ ] Memory checked (MEMORY.md)
- [ ] All 7 steps executed in order
- [ ] Searched org pages + Google + LinkedIn (3 layers)
- [ ] LinkedIn links verified as active
- [ ] No Markaz entries (waiting for confirmation)
- [ ] DMs personalized (not templated)
- [ ] Excel output with all required fields
- [ ] Pilot sent to Ayesha for review

---

## Execution Discipline

**STEP 0: INTAKE**
- Role title: what are we hiring for?
- Persona: who would be ideal? (company type, seniority, skills)
- Keywords: what search terms identify this role?
- Location: where should candidates be?
- Experience level: junior, mid, senior?

**STEP 1: DEFINE SEARCH STRATEGY**
- Read MEMORY.md: `talent_sourcing_7steps_complete.md`
- Read RULES.md: Skill 7 (Talent Sourcing lines 357-392)
- Identify: 3-5 company names or sectors to search
- List: 3-5 LinkedIn search terms for role keywords

**STEP 2: SEARCH ORG PAGES (Layer 1)**
- Google: "[Company Name] LinkedIn people" or company.com/employees
- Find profiles of similar roles at target companies
- Extract: name, title, company, LinkedIn URL

**STEP 3: GOOGLE SITE:LINKEDIN.COM (Layer 2)**
- Query: site:linkedin.com "[keyword1]" "[keyword2]"
- Example: site:linkedin.com "product manager" "SaaS"
- Vary: title, experience, location
- Extract: names and LinkedIn URLs

**STEP 4: VERIFY LINKS (Layer 3)**
- Open each LinkedIn URL (verify link active)
- Confirm: title matches role
- Document: if link dead, mark "link dead"
- Keep only: verified, active links

**STEP 5: EXTRACT VERIFIED CANDIDATES**
- Create row per candidate with:
  - Name
  - LinkedIn URL
  - Current title
  - Current company
  - Years of experience
  - Tier (1=perfect match, 2=good fit, 3=possible fit)
- List: 40-60 candidates minimum

**STEP 6: DRAFT PERSONALIZED DMS**
- Read: candidate's LinkedIn profile fully
- Find: specific project, skill, or experience that connects to role
- Write: DM explaining why role fits THEM (not about company)
- Example: "Hi [Name], I noticed your [specific project] at [Company] — we're building something similar at Taleemabad and think you'd be great fit..."
- Keep DMs: short, personalized, authentic

**STEP 7: ADD TO MARKAZ (AFTER CONFIRMATION)**
- Wait for Ayesha response: "Yes, they replied positively"
- Only then: add to Markaz with source='LinkedIn - Sourced'
- Include: tags {sourced_by: 'Coco', sourcing_run: '[date]', profile_url: '[URL]'}
- Document: date added, confirmation notes

**STEP 8: GENERATE EXCEL OUTPUT**
- Columns: Name, LinkedIn URL, Role, Company, Experience, Tier
- Add sheet: "Sourcing Methodology" (search terms, layers used)
- Send to Ayesha for review
- Include: count summary (total, by tier)

**STEP 9: RUN 8-ITEM CHECKLIST**
- All 7 steps executed (in order)
- 3 layers searched (org + Google + LinkedIn verify)
- Links verified (not dead)
- No premature Markaz entries
- DMs personalized (not templated)
- Excel output complete
- Pilot sent to Ayesha
- Checklist all items pass

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Using only Google or LinkedIn (skipping layers) | Misses sources, incomplete | Use all 3 layers: org pages + Google + LinkedIn |
| Adding to Markaz before interest confirmed | Wastes data, damages trust | Wait for explicit YES response |
| Template DMs (not personalized) | Low response rate, impersonal | Reference specific work/project they did |
| Dead LinkedIn links | Time wasted, bad impression | Test links before sending to Ayesha |
| Assuming interest without response | Premature Markaz entry | Wait for actual reply |
| Missing search methodology documentation | Can't repeat or refine sourcing | Document keywords, sources, date |
| Coco sending DMs (not Ayesha) | Personal outreach should come from hiring manager | Draft DMs for Ayesha to send |
| Small candidate pool | Limited options for Ayesha | Aim for 40-60 minimum per round |
| No tier categorization | Hard to prioritize | Rate candidates: 1 (perfect), 2 (good), 3 (possible) |
| Forgetting to document source | Can't track sourcing effectiveness | Source field: 'LinkedIn - Sourced' |

---

## Success Criteria

✅ All 7 steps executed in order  
✅ 3 layers searched (org pages + Google + LinkedIn)  
✅ LinkedIn links verified as active  
✅ 40-60 candidates minimum (per round)  
✅ Candidates tiered (1/2/3)  
✅ DMs personalized (not templated)  
✅ No premature Markaz entries (wait for confirmation)  
✅ Excel output complete with methodology  
✅ Sent to Ayesha for review  
✅ All 8-item checklist items pass  

---

## Resources & Templates

**Complete SOP:**
- 7 Steps Detailed: `memory/talent_sourcing_7steps_complete.md`
- Step-by-step examples: `memory/talent_sourcing_steps_explained.md`

**Reference Scripts:**
- Soul Architect sourcing: `scripts/sourcing/create_soul_architect_47_verified.py`
- Excel generation: `scripts/sourcing/create_soul_architect_sheet.py`
- Markaz insertion: `scripts/sourcing/insert_sourced_candidate.py`

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)
- Skill 7 (Talent Sourcing): `RULES.md` (lines 357-392)

---

## Commit to Discipline

I will source candidates with:
- ✅ All 7 steps (in order)
- ✅ 3-layer search (org + Google + LinkedIn)
- ✅ Links verified (tested, not dead)
- ✅ No premature Markaz entries (wait for YES)
- ✅ Personalized DMs (not templated)
- ✅ 40-60 candidates minimum
- ✅ Excel output with methodology
- ✅ All 8-item checklist items passing

**Status:** ✅ PRODUCTION READY
