---
name: Talent Sourcing - 7 Steps Explained with Examples
description: Detailed walkthrough of each step in the talent sourcing SOP. Real-world examples, decision trees, and what to do at each stage.
type: reference
originSessionId: 50203d1f-d855-41c4-b12a-dba80a622e87
---
# Talent Sourcing: 7 Steps Explained

## The Big Picture First

**Goal:** Find people who haven't applied. Search platforms → Show Ayesha the results → Let her pick → Draft DMs → She sends them manually → Wait for interest → Add to Markaz ONLY after they confirm interest.

**Key Mindset:** This is **outbound recruitment** (we're reaching out), NOT **inbound screening** (they applied to us).

---

## STEP 0: INTAKE (5 minutes)

### What You're Doing
Collecting the information needed to search effectively. This is like briefing before a mission — you need to understand what you're looking for.

### What Ayesha Gives You
1. **Role Title** (exact)
   - Example: "Instructional Systems Lead" (NOT "education job" or vague)
   
2. **Top 3-5 Must-Have Skills/Experiences**
   - Example for Instructional Systems Lead:
     - Curriculum design or learning design
     - Experience with Pakistan education sector
     - Team management (5+ years)
     - Adult learning principles
     - EdTech platform familiarity
   
3. **Seniority Level**
   - Example: "8+ years", "Senior", "Head of...", "Director-level"
   
4. **How Many Candidates?**
   - Default: 10-15
   - Ayesha might say: "Find me 12-15 people"

### What YOU Do
1. **Write down all this information** — don't rely on memory
2. **Fetch the JD from Markaz database:**
   ```sql
   SELECT id, title, jd_text, required_skills, department
   FROM jobs
   WHERE title ILIKE '%Instructional Systems%' AND status = 'published'
   LIMIT 1;
   ```
3. **Log this database read** with `log_db_query(table='jobs', filters="title ILIKE '%...'", rows_returned=1, context="talent_sourcing_intake")`

### Example Intake for "Instructional Systems Lead"

```
ROLE: Instructional Systems Lead
JD ID: 47
DEPARTMENT: NIETE

MUST-HAVES:
- Instructional design or curriculum design (5+ years relevant)
- Pakistan education sector experience preferred
- Team leadership experience (managed 3+ people)
- Learning management systems (LMS) familiarity
- Experience designing adult learning programs

SENIORITY: Senior (8-10+ years total, 5+ in education)

TARGET COUNT: 12-15 candidates

---
JD RETRIEVED:
Title: Instructional Systems Lead
Salary Range: PKR 800k - 1.2M
Location: Islamabad HQ
Status: published
```

---

## STEP 1: RESOLVE PLATFORM SET (Internal Decision — 2 minutes)

### What You're Doing
Deciding WHICH platforms to search based on the role. This is automatic — you're not asking Ayesha. You just decide.

### How It Works

**Look at the role title and match it to a category:**

```
Role: "Instructional Systems Lead" 
↓
Category: Digital Learning ← because it's education/training focused
↓
Tier 1 platforms: Org team pages (ITA, TCF, Zindagi), conference speaker lists
Tier 2 platforms: LinkedIn via Google, Medium
```

### The Decision Tree

```
Is it about... → Then use...

TECH (Odoo, Full Stack) 
  ├─ Layer 1: GitHub user search, org team pages
  └─ Layer 2-3: LinkedIn via Google

LEARNING (Instructional Design, Training Manager)
  ├─ Layer 1: Org team pages (ITA, TCF, Zindagi), Pakistan Learning Festival speakers
  └─ Layer 2-3: LinkedIn via Google, Medium

FUNDRAISING/BD (Fundraising Manager, Partnerships)
  ├─ Layer 1: Org team pages (TCF, PPAF, AKF), The Org.com, conference speakers
  └─ Layer 2-3: LinkedIn via Google

GROWTH/UX (Soul Architect, Product Manager)
  ├─ Layer 1: Medium, Substack, org pages
  └─ Layer 2-3: LinkedIn via Google

IMPACT/M&E (M&E Lead, Monitoring Manager)
  ├─ Layer 1: Org pages, academic profiles, conference speakers
  └─ Layer 2-3: LinkedIn via Google

ANYTHING ELSE
  ├─ Layer 1: LinkedIn via Google
  └─ Layer 2-3: (none)
```

### Example Decision for "Instructional Systems Lead"

```
Role: Instructional Systems Lead
↓
Category: Digital Learning
↓
PLATFORMS TO SEARCH:

Layer 1 (Highest quality — do these first):
- https://itacec.org/team/ (ITA Pakistan team)
- https://theorg.com/org/idara-e-taleem-o-aagahi (Idara-e-Taleem)
- https://www.tcf.org.pk/about-us/our-people/ (Citizens Foundation)
- https://www.zindagitrust.org/leadership-board (Zindagi Trust leadership)
- https://pakistanlearningfestival.com/profiles/resource_persons_and_institutions-clf/ (PLF speakers)

Layer 2 (Targeted Google searches):
- "[Org name]" "instructional design" OR "curriculum design" staff Pakistan
- "ITA" OR "TCF" "learning" OR "curriculum" "manager" OR "lead" Pakistan

Layer 3 (LinkedIn via Google catch-all):
- site:linkedin.com/in "instructional design" "lead" Pakistan
- site:linkedin.com/in "curriculum design" Pakistan EdTech
```

**Important:** This decision happens in Coco's head. You don't ask Ayesha. You just do it based on the role title.

---

## STEP 2: RUN 3-LAYER SEARCHES (20-30 minutes)

### The Three Layers (EXECUTE ALL THREE)

#### LAYER 1: Org Team Pages (WebFetch Directly)

**What:** Direct fetch from organization websites. These are NOT blocked. You just visit the URL and read the HTML.

**Why:** Organizations list their actual staff with current titles. High-quality, verified information.

**How:**

```
For each URL in the Tier 1 list:
  1. WebFetch the URL
  2. Extract names + titles + company + location
  3. Log with log_sourcing_action(platform="[Org Name]", query="[URL]", results_found=[N], context="org_team_page")
  4. Note interesting people in a results file
```

**Example:**

```
WebFetch: https://itacec.org/team/
↓
Results found:
- Muhammad Hassan Khan | Head of Learning Design | ITA | Islamabad
- Amina Malik | Senior Instructional Designer | ITA | Lahore
- Fatima Ahmed | Curriculum Lead | ITA | Islamabad
- (7 more names extracted)

Log: log_sourcing_action(platform="ITA Pakistan", query="https://itacec.org/team/", results_found=10, context="org_team_page")
```

**Critical Point:** If a WebFetch returns nothing or fails, log it anyway. Example:
```
WebFetch: https://www.akdn.org/our-agencies/aga-khan-foundation/pakistan
Result: 404 or page structure changed
Log: log_sourcing_action(platform="AKF Pakistan", query="[URL]", results_found=0, context="org_team_page_failed")
```

#### LAYER 2: Targeted Google Searches (15-20 minutes)

**What:** Google searches using specific patterns. We're looking for names + context in articles, websites, job postings.

**Why:** Captures people in articles, press releases, project descriptions that org pages miss.

**Pattern:** `"[Org Name]" "[skill/title]" [additional context]`

**Example Queries for "Instructional Systems Lead":**

```
1. "ITA" "instructional design" staff OR team Pakistan
   → Finds: ITA blog posts, news articles mentioning ITA staff

2. "Teach For Pakistan" OR "TCF" "curriculum design" "manager" OR "lead"
   → Finds: TCF job postings, articles about TCF leadership

3. "learning design" "senior" Pakistan education USAID OR donor-funded
   → Finds: People mentioned in program descriptions

4. "MEAL" OR "monitoring evaluation" Pakistan USAID education Islamabad
   → Finds: References in USAID-funded project pages
```

**How:**

```
For each search query:
  1. Run Google search (or use WebSearch tool)
  2. Review results (top 10-15 only)
  3. Extract candidate names + context + URL
  4. Log with log_sourcing_action(platform="Google", query="[search string]", results_found=[N], context="targeted_google")
```

**Example Result:**

```
Query: "ITA" "instructional design" staff Pakistan
↓
Result #3: "Team | Idara-e-Taleem"
  Found: Rida Hussain, Instructional Designer
  Context: "Rida leads curriculum development for our teacher training program"
  URL: itacec.org/team/rida-hussain

Log: log_sourcing_action(platform="Google", query="\"ITA\" \"instructional design\" staff Pakistan", results_found=12, context="targeted_google")
```

#### LAYER 3: LinkedIn via Google (10-15 minutes)

**What:** Using Google to search LinkedIn profiles. NOT direct LinkedIn access (that gets blocked).

**Why:** Catch-all for people who might not appear on org pages or in press.

**Pattern:** `site:linkedin.com/in "[skill/title]" [location/context]`

**Example Queries:**

```
1. site:linkedin.com/in "instructional design" "lead" OR "manager" Pakistan
2. site:linkedin.com/in "curriculum design" Pakistan EdTech OR education
3. site:linkedin.com/in "MEAL" "lead" Pakistan development
4. site:linkedin.com/in "learning design" Pakistan nonprofit
```

**How:**

```
For each search query:
  1. Run Google search with site:linkedin.com operator
  2. Review results (top 10-15 profiles)
  3. For promising profiles, note the LinkedIn URL
  4. Log with log_sourcing_action(platform="LinkedIn (Google)", query="[search string]", results_found=[N], context="linkedin_google")
```

**Example Result:**

```
Query: site:linkedin.com/in "instructional design" "lead" Pakistan
↓
Result #2: linkedin.com/in/zara-malik-instructional-design/
  Name: Zara Malik
  Title: Learning Experience Lead
  Company: EdTech Startup XYZ
  Location: Karachi

Log: log_sourcing_action(platform="LinkedIn (Google)", query="site:linkedin.com/in \"instructional design\" \"lead\" Pakistan", results_found=8, context="linkedin_google")
```

---

## STEP 3: EXTRACT CANDIDATE PROFILES (10 minutes)

### What You're Doing
For each person found across all 3 layers, pull together their information in a standard format.

### What to Extract (Per Person)

```
Full Name:            [Complete name]
Current Role Title:   [Their actual job title]
Current Company:      [Where they work now]
Location:             [City, Pakistan]
Key Experience:       [2-3 bullet points specific to the job we're sourcing for]
Platform + URL:       [Where you found them: LinkedIn/Org site/Google search result]
Why Relevant:         [1 sentence connecting their experience to our role]
```

### Example Extraction

```
NAME: Muhammad Hassan Khan
ROLE: Head of Learning Design
COMPANY: Idara-e-Taleem Aagahi (ITA)
LOCATION: Islamabad
KEY EXPERIENCE:
  - Led curriculum redesign for 200+ schools (5 years)
  - Trained 150+ teachers in modern pedagogical methods
  - Integrated technology into learning design processes
PLATFORM: Organization Website
URL: https://itacec.org/team/
WHY RELEVANT: "8 years instructional design + curriculum development in Pakistan education sector. Proven track record leading learning programs."
```

### Another Example

```
NAME: Fatima Ahmed
ROLE: Senior Instructional Designer
COMPANY: TCF (Citizens Foundation)
LOCATION: Lahore
KEY EXPERIENCE:
  - Designed curriculum for TCF's reading improvement program
  - Managed team of 5 instructional designers
  - Experience with learning management systems (LMS)
PLATFORM: LinkedIn (via Google)
URL: linkedin.com/in/fatima-ahmed-instructional-design
WHY RELEVANT: "7 years curriculum/instructional design. Team leadership experience. Direct Pakistan education sector background."
```

### Important Rules
- **No guessing.** If you can't find the info, write "Not mentioned"
- **Be specific.** "Strong background in education" is NOT good. "Led curriculum redesign for 200+ schools" IS good.
- **Verify before extracting.** If the website says they work at XYZ, that's verified. Don't assume roles from old LinkedIn profiles.

---

## STEP 4: PRESENT CANDIDATE SLATE TO AYESHA (5 minutes)

### What You're Doing
Showing Ayesha all the candidates you found in a clean table. She decides who to reach out to.

### Format (Exact)

```
## Talent Slate – [Role Title] – [Date]

Searched: [List platforms] | Queries run: [N] | Results reviewed: [N] | Candidates surfaced: [N]

| # | Name | Current Role | Company | Location | Why Relevant | Profile |
|---|------|-------------|---------|----------|-------------|---------|
| 1 | Muhammad Hassan Khan | Head of Learning Design | ITA | Islamabad | 8 years instructional design + curriculum development in Pakistan education. Led training for 150+ teachers. | [itacec.org/team/](https://itacec.org/team/) |
| 2 | Fatima Ahmed | Senior Instructional Designer | TCF | Lahore | 7 years curriculum/instructional design. Team leadership. Direct Pakistan education experience. | [linkedin.com/in/fatima-ahmed](https://linkedin.com/in/fatima-ahmed) |
| 3 | Rida Hussain | Instructional Designer | ITA | Islamabad | Leads curriculum development for teacher training programs. Hands-on experience with learning design. | [itacec.org/team/rida-hussain](https://itacec.org/team/) |
```

### Metadata to Include

```
Searched: Organization team pages (ITA, TCF, Zindagi), Pakistan Learning Festival speakers, LinkedIn via Google
Queries run: 12 (3 org pages + 4 Google searches + 5 LinkedIn)
Results reviewed: 47 (10+12+25 across layers)
Candidates surfaced: 12

**Note:** All Pakistan-based. No diaspora candidates included (per default).
```

### Ayesha's Next Step

She reads the slate and tells you:
- "Draft DMs for all of them" ← YOU draft for everyone
- "Draft for 1, 3, 5" ← YOU draft for those three only
- "Skip 7 and 10, rest are good" ← YOU draft for the rest
- "None of these work, search again with [new criteria]" ← YOU go back to Step 2

---

## STEP 5: DRAFT LINKEDIN DMs (10-15 minutes)

### What You're Doing
Writing a personalized message for EACH candidate that Ayesha will copy-paste into LinkedIn and send manually.

### The Template (Locked)

```
Hi [First Name],

[1 SPECIFIC observation about their work — a project, their trajectory, 
something concrete from their profile that shows they fit the role.
NEVER "I came across your profile" or generic praise.]

I'm Ayesha, People & Culture team at Taleemabad — we're building AI-powered 
tools to improve learning quality for teachers and students across Pakistan. 
We're looking for an [Role Title] who can [the core impact of this role in 1 sentence].

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

### Example DM for Muhammad Hassan Khan

```
Hi Muhammad,

I saw that you've led curriculum redesign across 200+ schools and trained 150+ 
teachers in modern pedagogical approaches — that kind of impact at scale is rare 
in Pakistan's education space.

I'm Ayesha, People & Culture team at Taleemabad — we're building AI-powered 
tools to improve learning quality for teachers and students across Pakistan. 
We're looking for an Instructional Systems Lead who can design the learning 
experience for a national teacher training platform.

Given your track record designing and implementing curriculum programs, I think 
you'd find the challenge interesting -- and the mission even more so.

Would you be open to a 20-minute conversation to explore? No pressure at all 
if the timing isn't right.

Warm regards,
Ayesha Khan
People & Culture | Taleemabad
hiring@taleemabad.com
www.taleemabad.com
```

### DM Non-Negotiables (MUST DO ALL)

✓ **Specific opening** — Reference their actual work (curriculum redesign, 150+ teachers, etc.)  
✗ **NOT** "I came across your profile" or "Strong background"

✓ **Mission paragraph** — Taleemabad + what we're building + the role impact

✓ **Soft ask** — "explore", "conversation", "learn more"  
✗ **NOT** "apply", "interview", "opportunity"

✓ **150-200 words max** — LinkedIn character limits

✓ **No em dashes** — Use ` -- ` or period

✓ **Sign as Ayesha Khan** — Not "Coco" or "AI"

✓ **Ayesha sends manually** — You draft, she sends. No API access to LinkedIn.

### DM Quality Check (Before Saving)

- [ ] Does opening reference something specific and concrete from their profile?
- [ ] Is the mission paragraph about Taleemabad first, role second?
- [ ] Is the ask soft and low-pressure?
- [ ] Is it 150-200 words?
- [ ] No em dashes?
- [ ] No salary mentioned?
- [ ] Signed as Ayesha Khan?

---

## STEP 6: SAVE OUTPUT FILE (2 minutes)

### What You're Doing
Creating a file that Ayesha can reference later. This is the complete record of the sourcing run.

### File Location
```
output/sourcing/[role-slug]-[YYYY-MM-DD].md
```

**Examples:**
```
output/sourcing/instructional-systems-lead-2026-04-16.md
output/sourcing/fundraising-manager-2026-04-17.md
output/sourcing/odoo-developer-2026-04-18.md
```

### File Contents

```
# Talent Sourcing Run – [Role Title]

**Date:** 2026-04-16  
**Role:** Instructional Systems Lead  
**Sourced by:** Coco (on behalf of Ayesha Khan)

---

## Search Summary

**Platforms Searched:**
- Layer 1: Organization team pages (ITA, TCF, Zindagi, PPAF, AKF), Pakistan Learning Festival speakers
- Layer 2: Targeted Google searches (org + skill combos)
- Layer 3: LinkedIn via Google site: queries

**Queries Run:** 12 total
- Layer 1: 5 URLs (org team pages)
- Layer 2: 4 Google searches
- Layer 3: 5 LinkedIn Google searches

**Results Reviewed:** 47 profiles/results
- Layer 1: 10 candidates
- Layer 2: 12 candidates
- Layer 3: 25 profiles

**Final Slate:** 12 candidates

---

## Candidate Slate

| # | Name | Current Role | Company | Location | Why Relevant | Profile |
|---|------|-------------|---------|----------|-------------|---------|
| 1 | Muhammad Hassan Khan | Head of Learning Design | ITA | Islamabad | 8 years instructional design + curriculum development in Pakistan education. Led training for 150+ teachers. | [itacec.org/team/](https://itacec.org/team/) |
...

---

## LinkedIn DMs (Copy-Paste Ready for Ayesha)

### DM #1: Muhammad Hassan Khan

Hi Muhammad,

I saw that you've led curriculum redesign across 200+ schools and trained 150+ 
teachers in modern pedagogical approaches — that kind of impact at scale is rare 
in Pakistan's education space.

I'm Ayesha, People & Culture team at Taleemabad — we're building AI-powered 
tools to improve learning quality for teachers and students across Pakistan. 
We're looking for an Instructional Systems Lead who can design the learning 
experience for a national teacher training platform.

Given your track record designing and implementing curriculum programs, I think 
you'd find the challenge interesting -- and the mission even more so.

Would you be open to a 20-minute conversation to explore? No pressure at all 
if the timing isn't right.

Warm regards,
Ayesha Khan
People & Culture | Taleemabad
hiring@taleemabad.com
www.taleemabad.com

---

### DM #2: Fatima Ahmed

[DM content here]

---

### DM #3: Rida Hussain

[DM content here]

---

**Instructions for Ayesha:**
1. Copy each DM above
2. Go to LinkedIn
3. Search for the person's profile
4. Click "Message"
5. Paste the DM
6. Send

When they respond with interest, let Coco know so they can be added to Markaz.
```

---

## STEP 7: ADD TO MARKAZ (AFTER CONFIRMED INTEREST)

### What You're Doing
ONLY when Ayesha says: "[Name] is interested, add them"

**Important:** You do NOT add candidates speculatively. Wait for interest confirmation.

### The Process

**Trigger:**
```
Ayesha (in Slack or email): "Muhammad Hassan Khan confirmed interest. Add him for Instructional Systems Lead."
```

**What You Do:**

1. **Get the job ID:**
   ```sql
   SELECT id FROM jobs
   WHERE title ILIKE '%Instructional Systems Lead%' AND status = 'published'
   LIMIT 1;
   ```
   Result: job_id = 47

2. **Run the insert script:**
   ```bash
   python scripts/sourcing/insert_sourced_candidate.py \
     --first-name "Muhammad" \
     --last-name "Khan" \
     --position "Instructional Systems Lead" \
     --job-id 47 \
     --location "Islamabad" \
     --current-position "Head of Learning Design" \
     --current-company "ITA" \
     --profile-url "https://itacec.org/team/"
   ```

3. **Script does the following:**
   - Checks for duplicate (only if email exists)
   - Inserts into `candidates` table
   - Inserts into `applications` table with status='new'
   - Logs to audit log
   - Returns IDs

4. **Confirm back to Ayesha:**
   ```
   Added to Markaz:
   - Candidate ID: 12345
   - Application ID: 67890
   - Status: new
   - Source: LinkedIn - Sourced
   - Profile: https://itacec.org/team/
   ```

### Database Fields (What Gets Written)

```
candidates table:
- first_name: "Muhammad"
- last_name: "Khan"
- email: null (usually null for sourced candidates)
- position: "Instructional Systems Lead"
- skills: ["curriculum design", "instructional design", "team leadership"]
- source: "LinkedIn - Sourced"
- location: "Islamabad"
- current_position: "Head of Learning Design"
- current_company: "ITA"
- tags: {
    "sourced_by": "coco",
    "sourcing_run": "2026-04-16",
    "profile_url": "https://itacec.org/team/"
  }

applications table:
- candidate_id: [from candidates table insert]
- job_id: 47
- status: "new"
- notes: "Passive sourced candidate -- confirmed interest via LinkedIn DM."
- ai_screening_summary: "Sourced on 2026-04-16 from https://itacec.org/team/. Muhammad Hassan Khan, Head of Learning Design at ITA. 8 years instructional design + curriculum development."
```

### Why Only After Confirmation?

If you add candidates to Markaz speculatively:
- Pipeline gets polluted with unqualified leads
- Hiring manager sees random names they didn't ask for
- No way to track which sourced candidates actually responded
- You can't tell the difference between "we reached out but no response" vs "interested"

**So the rule is:** Search → Draft DMs → Ayesha sends → Wait for confirmation → THEN add to Markaz.

---

## Summary: The Complete Flow

```
STEP 0: Intake
  ↓ (Ayesha gives you: role, skills, seniority, count)
  
STEP 1: Platform Selection
  ↓ (Coco decides: use org pages? LinkedIn? Medium?)
  
STEP 2: 3-Layer Searches
  ↓ (Layer 1: Org pages | Layer 2: Google | Layer 3: LinkedIn)
  
STEP 3: Extract Profiles
  ↓ (Standardize: name, role, company, location, why relevant, URL)
  
STEP 4: Present Slate
  ↓ (Ayesha sees table: "Draft DMs for #1, #3, #5")
  
STEP 5: Draft DMs
  ↓ (12 personalized messages, copy-paste ready)
  
STEP 6: Save Output
  ↓ (Slate + DMs → output/sourcing/[role]-[date].md)
  
STEP 7: Add to Markaz
  ↓ (ONLY after: Ayesha says "[Name] is interested")
  (Inserts into candidates + applications, status='new')
```

---

## Key Reminders

✅ **Search all 3 layers** — Don't skip Layer 1 (org pages have the best candidates)

✅ **Log everything** — `log_sourcing_action()` for searches, `log_db_query()` for DB reads/writes

✅ **Personalize DMs** — Specific observations, never generic phrases

✅ **Wait for interest** — Don't add to Markaz speculatively

✅ **Ayesha sends manually** — You draft, she sends. No LinkedIn API access.

✓ **Pakistan-based by default** — Diaspora only if she asks

✗ **Never guess data** — Write "Not mentioned" if missing
