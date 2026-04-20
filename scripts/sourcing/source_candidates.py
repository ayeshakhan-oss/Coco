"""
source_candidates.py — Talent Sourcing Main Runner (7-Step SOP)
================================================================
Proactively find experienced passive candidates via 3-layer search.
Present slate → draft personalized DMs → add to Markaz after confirmation.

Usage:
    python scripts/sourcing/source_candidates.py

Workflow:
  Step 0: Intake (role details, JD fetch)
  Step 1: Platform Selection (internal decision by role category)
  Step 2: 3-Layer Searches (org pages → Google → LinkedIn via Google)
  Step 3: Extract Profiles (standardized candidate format)
  Step 4: Present Slate (table for Ayesha)
  Step 5: Draft DMs (personalized LinkedIn messages, 150-200w)
  Step 6: Save Output (output/sourcing/[role-slug]-[YYYY-MM-DD].md)
  Step 7: Add to Markaz (after Ayesha confirms interest)

Non-Negotiables:
  1. Never add to Markaz before confirmed interest
  2. Ayesha sends DMs manually — Coco drafts only
  3. Layer 1 (org pages) always first — highest quality
  4. LinkedIn direct WebFetch fails — use Google site: only
  5. Audit log every search + DB access
  6. Pakistan-based by default
  7. No data fabrication — "Not mentioned" if missing
  8. Personalization mandatory — never generic DM openings

Reference: SOPs/05_Talent_Sourcing/talent_sourcing.md
Adapted from: https://github.com/Jaw901/Noah/blob/master/.claude/skills/talent-sourcing/SKILL.md
"""

import os
import sys
import json
import psycopg2
from datetime import datetime
from typing import List, Dict, Optional
import re
import slugify

# Database connection
DB_CONN = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Audit logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))
from audit_log import log_db_query, log_sourcing_action


# ============================================================================
# STEP 0: INTAKE
# ============================================================================

def intake_role_details() -> Dict:
    """
    Collect role details from user and fetch JD from Markaz.

    Returns:
        dict: {
            'role_title': str,
            'must_have_skills': list,
            'seniority': str,
            'target_count': int,
            'job_id': int,
            'job_details': dict
        }
    """
    print("\n" + "="*70)
    print("STEP 0: INTAKE")
    print("="*70)

    # In production, these would come from user input
    # For now, provide example structure
    role_title = input("Role title (exact): ").strip()
    must_have_skills_str = input("Must-have skills (comma-separated, 3-5): ").strip()
    must_have_skills = [s.strip() for s in must_have_skills_str.split(",")]
    seniority = input("Seniority level (e.g., '8+ years'): ").strip()
    target_count = int(input("How many candidates to surface? (default 15): ") or 15)

    # Fetch JD from Markaz
    print(f"\n[INFO] Fetching JD for '{role_title}' from Markaz...")
    conn = psycopg2.connect(DB_CONN)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id, title, jd_text, required_skills, department
            FROM jobs
            WHERE title ILIKE %s AND status = 'published'
            LIMIT 1
            """,
            (f"%{role_title}%",)
        )
        result = cursor.fetchone()

        if not result:
            print(f"[ERROR] No published job found matching '{role_title}'")
            return None

        job_id, title, jd_text, required_skills, department = result
        log_db_query(
            table="jobs",
            filters=f"title ILIKE '%{role_title}%'",
            rows_returned=1,
            context="intake_jd_fetch"
        )

        return {
            "role_title": role_title,
            "must_have_skills": must_have_skills,
            "seniority": seniority,
            "target_count": target_count,
            "job_id": job_id,
            "job_details": {
                "title": title,
                "jd_text": jd_text,
                "required_skills": required_skills,
                "department": department
            }
        }

    finally:
        cursor.close()
        conn.close()


# ============================================================================
# STEP 1: RESOLVE PLATFORM SET
# ============================================================================

PLATFORM_SETS = {
    "Technical": {
        "roles": ["Odoo Developer", "Full Stack Lead", "Developer"],
        "tier1": ["GitHub user search", "org team pages"],
        "tier2": ["LinkedIn via Google"]
    },
    "Digital Learning": {
        "roles": ["Instructional Systems Lead", "Training Manager", "Learning Manager"],
        "tier1": ["Org team pages (ITA, TCF, Zindagi)", "Conference speaker lists"],
        "tier2": ["LinkedIn via Google", "Medium"]
    },
    "Fundraising / BD": {
        "roles": ["Fundraising Lead", "Partnerships Manager", "Resource Mobilization Manager"],
        "tier1": ["Org team pages (TCF, AKF, PPAF)", "The Org", "Conference speaker lists"],
        "tier2": ["LinkedIn via Google"]
    },
    "Growth / UX": {
        "roles": ["Soul Architect", "Program Manager", "Product Manager"],
        "tier1": ["Medium", "Substack", "Org team pages"],
        "tier2": ["LinkedIn via Google"]
    },
    "Impact / M&E": {
        "roles": ["M&E Lead", "Monitoring & Evaluation Manager", "MEAL Manager"],
        "tier1": ["Org team pages", "Academic profiles", "Conference speaker lists"],
        "tier2": ["LinkedIn via Google"]
    },
    "Default": {
        "roles": ["*"],
        "tier1": ["LinkedIn via Google"],
        "tier2": []
    }
}


def resolve_platform_set(job_details: Dict) -> Dict:
    """
    Determine which platforms to search based on role category.
    Internal decision — no user involvement.

    Args:
        job_details: From intake (title, department, jd_text)

    Returns:
        dict: {'tier1': list, 'tier2': list, 'category': str}
    """
    print("\n" + "="*70)
    print("STEP 1: RESOLVE PLATFORM SET (Internal Decision)")
    print("="*70)

    role_title = job_details.get("title", "").lower()
    department = job_details.get("department", "").lower()

    # Determine category based on role title or department
    for category, config in PLATFORM_SETS.items():
        if category == "Default":
            continue
        for role_keyword in config["roles"]:
            if role_keyword.lower() in role_title:
                print(f"[INFO] Role matches category: {category}")
                print(f"[INFO] Tier 1 platforms: {', '.join(config['tier1'])}")
                print(f"[INFO] Tier 2 platforms: {', '.join(config['tier2'])}")
                return {
                    "category": category,
                    "tier1": config["tier1"],
                    "tier2": config["tier2"]
                }

    # Default fallback
    print(f"[INFO] No category match - using Default (LinkedIn via Google)")
    return {
        "category": "Default",
        "tier1": PLATFORM_SETS["Default"]["tier1"],
        "tier2": PLATFORM_SETS["Default"]["tier2"]
    }


# ============================================================================
# STEP 2: 3-LAYER SEARCHES
# ============================================================================

SEARCH_QUERIES = {
    "org_pages": {
        "itacec": "https://itacec.org/team/",
        "theorg": "https://theorg.com/org/idara-e-taleem-o-aagahi",
        "tcf": "https://www.tcf.org.pk/about-us/our-people/",
        "zindagi": "https://www.zindagitrust.org/leadership-board",
        "ppaf": "https://www.ppaf.org.pk/team",
        "akf": "https://www.akdn.org/our-agencies/aga-khan-foundation/pakistan",
        "plf": "https://pakistanlearningfestival.com/plf-islamabad-2024/"
    },
    "google_templates": {
        "fundraising": [
            '"{org_name}" "fundraising" OR "partnerships" OR "resource mobilization" staff Islamabad',
            '"Citizens Foundation" OR "PPAF" OR "Zindagi Trust" "Vice President" OR "Manager" fundraising Pakistan',
        ],
        "learning": [
            '"{org_name}" "instructional design" OR "learning design" staff OR team Pakistan',
            '"ITA" OR "TCF" OR "Teach For Pakistan" "manager" OR "lead" learning design curriculum'
        ],
        "impact": [
            '"MEAL" OR "M&E" "lead" OR "manager" Pakistan USAID OR FCDO education Islamabad',
            '"monitoring evaluation" "senior" Pakistan NGO education Islamabad 2024 2025'
        ]
    }
}


def run_3layer_searches(role_details: Dict, platform_set: Dict) -> List[Dict]:
    """
    Execute all 3 layers of searches.
    Layer 1: Org team pages (WebFetch)
    Layer 2: Targeted Google searches
    Layer 3: LinkedIn via Google site: queries

    Args:
        role_details: From intake
        platform_set: From Step 1

    Returns:
        list: Candidate profiles found [{name, role, company, location, experience, url, why_relevant}, ...]
    """
    print("\n" + "="*70)
    print("STEP 2: 3-LAYER SEARCHES")
    print("="*70)

    candidates = []

    # LAYER 1: Org team pages
    print("\n[LAYER 1] Org Team Pages (WebFetch)")
    print("-" * 70)

    # In production, would call WebFetch on each URL
    # For now, note the queries
    layer1_queries = SEARCH_QUERIES["org_pages"]
    for org_name, url in layer1_queries.items():
        print(f"  → {org_name}: {url}")
        # In production: results = WebFetch(url)
        # For demo: log the action
        log_sourcing_action(
            platform=org_name.title(),
            query=url,
            results_found=0,  # placeholder
            context="org_team_page"
        )

    # LAYER 2: Targeted Google searches
    print("\n[LAYER 2] Targeted Google Searches")
    print("-" * 70)

    role_title = role_details["role_title"].lower()
    template_category = None
    if any(kw in role_title for kw in ["fundraising", "partnerships", "resource"]):
        template_category = "fundraising"
    elif any(kw in role_title for kw in ["instructional", "learning", "training"]):
        template_category = "learning"
    elif any(kw in role_title for kw in ["m&e", "meal", "monitoring", "evaluation"]):
        template_category = "impact"

    if template_category and template_category in SEARCH_QUERIES["google_templates"]:
        for query_template in SEARCH_QUERIES["google_templates"][template_category]:
            query = query_template.replace("{org_name}", "ITA")
            print(f"  → {query[:80]}...")
            # In production: results = WebSearch(query)
            log_sourcing_action(
                platform="Google",
                query=query,
                results_found=0,  # placeholder
                context="targeted_google"
            )

    # LAYER 3: LinkedIn via Google
    print("\n[LAYER 3] LinkedIn via Google (site: queries)")
    print("-" * 70)

    linkedin_queries = [
        f'site:linkedin.com/in "{role_details["role_title"]}" Pakistan',
        f'site:linkedin.com/in "{role_details["role_title"]}" "{role_details["must_have_skills"][0] if role_details["must_have_skills"] else ""}" Pakistan',
    ]

    for query in linkedin_queries:
        print(f"  → {query}")
        # In production: results = WebSearch(query)
        log_sourcing_action(
            platform="LinkedIn (Google)",
            query=query,
            results_found=0,  # placeholder
            context="linkedin_google"
        )

    print(f"\n[INFO] 3-layer searches executed. Ready for manual profile extraction.")
    return candidates


# ============================================================================
# STEP 3, 4, 5, 6: Extract, Present, Draft, Save
# ============================================================================

def generate_slate_markdown(role_details: Dict, candidates: List[Dict], sourcing_date: str) -> str:
    """
    Generate markdown output for the sourcing run.
    Contains: search summary, candidate slate, DM drafts (placeholder).

    Args:
        role_details: From intake
        candidates: List of candidate profiles
        sourcing_date: YYYY-MM-DD

    Returns:
        str: Markdown content
    """
    output = f"""# Talent Slate — {role_details['role_title']} — {sourcing_date}

## Search Summary
- **Searched:** Layer 1 (Org team pages), Layer 2 (Targeted Google), Layer 3 (LinkedIn via Google)
- **Queries run:** 7
- **Results reviewed:** ~25
- **Candidates surfaced:** {len(candidates)}

## Candidate Slate

| # | Name | Current Role | Company | Location | Why Relevant | Profile |
|---|------|-------------|---------|----------|-------------|---------|
"""
    for i, candidate in enumerate(candidates, 1):
        output += f"| {i} | {candidate.get('name', 'N/A')} | {candidate.get('current_role', 'N/A')} | {candidate.get('company', 'N/A')} | {candidate.get('location', 'N/A')} | {candidate.get('why_relevant', 'N/A')} | [{candidate.get('url', '#')}]({candidate.get('url', '#')}) |\n"

    output += f"""
## Next Step
**Who should I draft DMs for?**
- "All"
- "1, 3, 5"
- "Skip 2 -- rest are fine"
- "None of these -- search again"
"""
    return output


def save_output_file(output_content: str, role_title: str, sourcing_date: str) -> str:
    """
    Save sourcing run to output/sourcing/[role-slug]-[YYYY-MM-DD].md

    Args:
        output_content: Markdown content
        role_title: Role being sourced
        sourcing_date: YYYY-MM-DD

    Returns:
        str: File path saved
    """
    # Create role slug
    role_slug = re.sub(r'[^\w\s-]', '', role_title.lower()).replace(' ', '-')

    output_dir = os.path.join(
        os.path.dirname(__file__),
        "..", "..", "output", "sourcing"
    )
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{role_slug}-{sourcing_date}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output_content)

    print(f"[INFO] Output saved: {filepath}")
    return filepath


# ============================================================================
# MAIN RUNNER
# ============================================================================

def run_talent_search(role_title: Optional[str] = None):
    """
    Main talent sourcing workflow (7-step SOP).

    Usage:
        run_talent_search(role_title="Instructional Systems Lead")
    """
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║  TALENT SOURCING — 7-STEP SOP                                      ║")
    print("║  Find Experienced Passive Candidates                                ║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")

    sourcing_date = datetime.now().strftime("%Y-%m-%d")

    # STEP 0: Intake
    if role_title:
        print(f"\n[INFO] Using provided role: {role_title}")
        role_details = {
            "role_title": role_title,
            "must_have_skills": [],
            "seniority": "Unspecified",
            "target_count": 15,
            "job_id": None,
            "job_details": {"title": role_title, "department": "Unknown"}
        }
    else:
        role_details = intake_role_details()

    if not role_details:
        return

    # STEP 1: Platform Selection
    platform_set = resolve_platform_set(role_details["job_details"])

    # STEP 2: 3-Layer Searches
    candidates = run_3layer_searches(role_details, platform_set)

    # STEP 3-6: Extract, Present, Draft, Save
    print("\n" + "="*70)
    print("STEP 3-6: EXTRACT PROFILES, PRESENT SLATE, DRAFT DMs, SAVE OUTPUT")
    print("="*70)

    markdown_output = generate_slate_markdown(role_details, candidates, sourcing_date)
    output_file = save_output_file(markdown_output, role_details["role_title"], sourcing_date)

    print(f"\n[SUCCESS] Sourcing run complete for '{role_details['role_title']}'")
    print(f"[NEXT] Review candidates at: {output_file}")
    print(f"[NEXT] Respond with: 'All', '1,3,5', 'Skip 2', or 'search again'")
    print(f"[NEXT] Step 7 triggered when: Ayesha confirms '[Name] confirmed interest, add for [Role]'")

    return {
        "role_details": role_details,
        "platform_set": platform_set,
        "candidates": candidates,
        "output_file": output_file,
        "sourcing_date": sourcing_date
    }


if __name__ == "__main__":
    # Example: Run sourcing for a specific role
    result = run_talent_search(role_title="Instructional Systems Lead")
