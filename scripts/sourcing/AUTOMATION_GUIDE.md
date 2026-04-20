# Sourcing Automation Suite — Quick Start Guide

## Overview

The Sourcing Automation Suite automates candidate discovery and tier classification. It runs three modules:

1. **Module 1: Search Automation** — GitHub + LinkedIn search (free APIs only)
2. **Module 2: Profile Enrichment** — Email finding, experience scoring, skill extraction
3. **Module 3: Tier Classification + Excel** — Auto-rank T1/T2/T3, generate DM templates

## Installation

```bash
# Install required package
pip install openpyxl
```

## Quick Start

### Run for Soul Architect (50 candidates)

```bash
cd c:\Agent Coco
python scripts/sourcing/runners/run_full_sourcing.py --role soul-architect --target 50
```

### Run for a Different Role

```bash
# First, add role to config/role_profiles.json
# Then run:
python scripts/sourcing/runners/run_full_sourcing.py --role [role-slug] --target 50
```

### Skip Search Phase (Use Existing Data)

```bash
python scripts/sourcing/runners/run_full_sourcing.py --role soul-architect --skip-search
```

## Output

All results saved to: `output/sourcing/automation/[role]/[YYYY-MM-DD]/`

Files generated:
- `[date]-raw-candidates.csv` — Raw search results from GitHub + LinkedIn
- `[date]-enriched.csv` — Enriched with scores, experience, skills
- `[date]-FINAL.xlsx` — Excel file with T1/T2/T3 tabs + DM templates

## Excel Output Format

The final Excel file has **4 sheets:**

1. **Raw Data** — All candidates with metadata
2. **T1 - Senior** — 7+ years experience, GitHub score 70+
3. **T2 - Mid-level** — 5-7 years experience, GitHub score 50+
4. **T3 - Junior** — 3-5 years experience, GitHub score 30+

Each tier sheet includes:
- Name, GitHub URL, LinkedIn URL
- Company, Location, Extracted Skills
- Years of Experience, GitHub Score, Confidence
- **Pre-filled DM Template** (copy-paste ready for LinkedIn)

## DM Templates

Each candidate has a personalized LinkedIn DM template pre-filled in the Excel file.

**How to use:**
1. Open Excel → T1 sheet
2. Find candidate → Copy DM Template column
3. Go to LinkedIn → Find candidate via GitHub/LinkedIn URL
4. Paste DM and send manually (Ayesha sends, never automated)

## Tier Thresholds

Tiers are auto-classified based on:
- **Experience years** (estimated from GitHub activity)
- **GitHub activity score** (0-100: repos + followers + bio relevance)

Current thresholds (configurable in `config/role_profiles.json`):
- **T1:** 7+ years, score 70+
- **T2:** 5+ years, score 50+
- **T3:** 3+ years, score 30+

## Adding Candidates Manually

If you want to add candidates that weren't auto-discovered:

1. Edit `output/sourcing/automation/[role]/[date]-raw-candidates.csv`
2. Add rows with: name, github_url, github_username, location, etc.
3. Run with `--skip-search`:
   ```bash
   python scripts/sourcing/runners/run_full_sourcing.py --role soul-architect --skip-search
   ```

## Troubleshooting

### GitHub API Rate Limit
- Free tier: 60 requests/hour
- Add GitHub token to `.env` (GITHUB_TOKEN=...) for 5,000/hour

### Too Few Candidates
- Module 1 uses GitHub API (slow but reliable)
- Manually add LinkedIn candidates to raw CSV
- Rerun with `--skip-search` for Modules 2-3

### Email Not Found
- Uses free methods (GitHub public email, email-format guessing)
- Email shows "Not found" when unavailable
- You can manually add emails to enriched CSV and regenerate Excel

### Excel File Won't Open
- Ensure openpyxl is installed: `pip install openpyxl`
- Check file path and permissions

## Next Steps After Sourcing

1. **Review Excel** — Check T1/T2/T3 tiers, confidence scores
2. **Send DMs** — Copy templates from Excel, send manually via LinkedIn
3. **Track Interest** — Wait for candidate responses
4. **Add to Markaz** — Once interest confirmed, use `insert_sourced_candidate.py`:
   ```bash
   python scripts/sourcing/insert_sourced_candidate.py \
     --name "Name" \
     --email "email@domain.com" \
     --github-url "https://github.com/..." \
     --job-id [job_id]
   ```

## Configuration

Role profiles are defined in `config/role_profiles.json`. To add a new role:

```json
{
  "new-role-slug": {
    "title": "Role Title",
    "required_skills": ["skill1", "skill2"],
    "location": "Pakistan",
    "github_search_queries": ["query1", "query2"],
    "linkedin_search_queries": ["query1", "query2"],
    "target_count": 50,
    "tier_thresholds": {
      "t1": {"min_years_experience": 7, "min_github_score": 70},
      "t2": {"min_years_experience": 5, "min_github_score": 50},
      "t3": {"min_years_experience": 3, "min_github_score": 30}
    }
  }
}
```

Then run:
```bash
python scripts/sourcing/runners/run_full_sourcing.py --role new-role-slug --target 50
```

## Important Notes

1. **No LinkedIn API** — Uses Google site:linkedin.com queries (manual or limited scraping)
2. **No Email APIs** — Uses free methods only (no Hunter.io, RocketReach)
3. **DMs are manual** — Excel templates generated, but you send via LinkedIn yourself
4. **Markaz insertion** — Only after interest confirmed (never pre-add to pipeline)
5. **Audit logging** — All searches logged to `logs/email_audit.log` for compliance

## Reference

- **Skills:** [talent-sourcing.md](../../SOPs/05_Talent_Sourcing/talent_sourcing.md) — Full 7-step SOP
- **Config:** [role_profiles.json](../../config/role_profiles.json) — Role definitions
- **Insert script:** [insert_sourced_candidate.py](insert_sourced_candidate.py) — Add to Markaz

---

**Questions?** Check CLAUDE.md → Talent Sourcing section for full details.
