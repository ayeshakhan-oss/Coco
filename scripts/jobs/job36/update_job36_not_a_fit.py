"""
Job 36 — Mark all non-shortlisted candidates as 'Not a Fit (Decline)'
Status: rejected | rejection_reason: specific where CV was read, profile-based for rest
"""

import psycopg2
import json

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode": "require",
}

JOB_ID = 36
JOB_TITLE = "Field Coordinator – Research & Impact Studies"

# ── Specific reasons for all manually-reviewed CV candidates (discard only) ──
SPECIFIC_REASONS = {

    # ── Ranks 18–20 (shortlist tail, reviewed in full) ──────────────────────
    1454: (  # Shahid Kamal — rank 18, score 65
        "After reading the CV in full: M&E Officer (Karishma Ali Foundation) and LUMS RA background shows "
        "field M&E experience, but the scale of operations is unclear and the role appears closer to NGO "
        "grant management than front-line field coordination. Insufficient evidence of managing large-scale "
        "enumerator teams, survey firm oversight, or data quality governance at the level this role requires. "
        "Scanner overscored by ~24 points relative to actual field coordination depth."
    ),
    1545: (  # Pariyal Fazal Shah — rank 19, score 62
        "After reading the CV in full: Only 2 years of experience as an M&R (Monitoring & Reporting) analyst "
        "— desk-based role focused on internal reporting, not operational field coordination. Scanner "
        "massively overscored at 93.8; human assessment placed at 62. No evidence of enumerator management, "
        "survey firm oversight, or school-based data collection at scale. Does not meet the minimum "
        "experience bar for this role."
    ),
    1450: (  # Naveen Shariff — rank 20, score 59
        "After reading the CV in full: TCF intern with basic Kobo tools exposure — entry-level only. Very "
        "limited field coordination evidence; no enumerator management or survey firm oversight at any "
        "meaningful scale. Karachi-based — relocation to Islamabad required. Salary ask (PKR 220K) is "
        "disproportionate relative to experience level."
    ),

    # ── Named No-Hire candidates (CV read, profiled in report) ──────────────
    1528: (  # Muhammad Afzaal — score 45
        "After reading the CV in full: Community mobilizer background (Peshawar, USAID community work). "
        "No M&E tools used in practice — Kobo/ODK listed in skills section only, without any CV evidence "
        "of actual field deployment. No enumerator supervision, no education sector experience. Scanner "
        "overscored at 86.2; human assessment placed at 45."
    ),
    1633: (  # Midhat Fatima — score 49
        "After reading the CV in full: Public health surveyor with intern-level experience only. No "
        "education M&E, no field team management, no enumerator supervision experience. Entirely "
        "health-sector focused. Scanner overscored at 86.2; human assessment placed at 49."
    ),
    1489: (  # Muhammad Qasi — score 50
        "After reading the CV in full: Small-scale KII (Key Informant Interview) researcher based in "
        "Gilgit-Baltistan. No field team management at any meaningful scale, no enumerator supervision, "
        "no education sector context. Does not meet minimum requirements for operational field "
        "coordination at the level this role demands."
    ),
    1477: (  # Sadia Siddique — score 31
        "After reading the CV in full: HR and data analyst background — entirely desk-based. No field "
        "coordination, no M&E, no education sector experience. CV shows no evidence of enumerator "
        "management, survey work, or school-based data collection. Scanner overscored at 81.2; "
        "human assessment placed at 31."
    ),
    1802: (  # Syeda Farzana Ali Shah — score 39
        "After reading the CV in full: 25+ years of experience in child protection, safeguarding, and "
        "gender programming — an entirely different domain from field research coordination. No M&E, "
        "no field data governance, no education sector research background. Expected salary PKR 300K "
        "is also over budget. Scanner overscored at 83.8; human assessment placed at 39."
    ),

    # ── 7 candidates with CV texts not profiled in the final report ─────────
    1453: (  # Abid Hussain
        "After reading the CV in full: IT and product support background (L2 Support Specialist at Techvity, "
        "IT intern at CARE International). Less than 1 year of any development-sector work, all at intern "
        "or junior support level. No M&E experience, no enumerator management, no education sector "
        "field coordination. Does not meet the minimum 2–3 years relevant field coordination experience "
        "required for this role."
    ),
    1495: (  # Shabbir Hussain
        "After reading the CV in full: PhD Sociology with community mobilization and public health research "
        "background. Field experience limited to social mobilization (AKRSP, 5 months) and academic research "
        "at university level. No education sector M&E, no enumerator management, no survey firm oversight. "
        "Gilgit-Baltistan based — relocation to Islamabad required. Profile better suited to public health "
        "or community development roles."
    ),
    1556: (  # Sana Mehboob
        "After reading the CV in full: District M&E Officer at Balochistan Rural Support Programme (~20 "
        "months) in WASH and rural community development — not education sector M&E. No evidence of "
        "managing school-based field research, enumerator teams, or education data quality oversight. "
        "Social mobilizer and community trainer background does not translate to the operational field "
        "coordination this role requires."
    ),
    1600: (  # Adil Javed
        "After reading the CV in full: Tehsil Monitoring Officer at WHO (5 years) — health/polio "
        "campaign monitoring, not education sector M&E. No school-based field research experience, "
        "no enumerator team management, no survey firm oversight. KPK-based (Mardan) — relocation "
        "to Islamabad required. Construction project supervisor background further indicates a "
        "mismatch with education research coordination."
    ),
    1608: (  # Afaq Ahmad
        "After reading the CV in full: Entry-level social mobilizer and WWF field assistant with "
        "approximately 14 months total experience. No education sector M&E, no enumerator management, "
        "no survey firm oversight. BS Forestry background. Gilgit-Baltistan based — relocation to "
        "Islamabad required. Does not meet minimum experience requirements for this role."
    ),
    1639: (  # Wajeeha Rehber
        "After reading the CV in full: Sociology research background with 6-month field evaluation "
        "(US Embassy project) and ~14 months as research assistant. No evidence of managing "
        "large-scale enumerator teams, survey firm oversight, or school-based education data "
        "governance. Experience is primarily academic research and human rights advocacy, not "
        "operational field coordination at the scale this role requires."
    ),
    1674: (  # Amina Jabin
        "After reading the CV in full: Entirely teaching background — Class Teacher, Subject Teacher, "
        "and Volunteer Teacher at primary and secondary schools (Chitral/Rawalpindi). MPhil in "
        "Education (NUML). No M&E experience, no field coordination, no data collection or research "
        "role. This role requires operational field research coordination, not teaching expertise. "
        "Chitral-based — relocation to Islamabad required."
    ),
}

# ── IDs that were shortlisted (exclude from update) ─────────────────────────
SHORTLIST_IDS = [1602, 1857, 1430, 1864, 1442, 1518, 1839, 1700, 1808,
                 1513, 1789, 1755, 1658, 1720, 1591, 1950, 1624]


def build_reason_for_unreviewed(row):
    """Generate a reason from available DB profile fields for candidates whose CV was not read."""
    name = f"{row['first_name']} {row['last_name']}".strip()
    current_pos = row.get('current_position') or ''
    current_co  = row.get('current_company') or ''
    experience  = row.get('experience') or ''
    location    = row.get('location') or ''
    last_name   = row.get('last_name') or ''

    # Placeholder / quick-apply profiles
    if last_name.lower() in ('applicant', '') and not current_pos and not experience:
        return (
            "Incomplete application — no CV or profile information was submitted. "
            "Could not be assessed against the requirements for the "
            f"{JOB_TITLE} role."
        )

    # Has some profile data — build a specific reason
    parts = []
    if current_pos or current_co:
        role_info = ' at '.join(filter(None, [current_pos, current_co]))
        parts.append(f"Current/recent role: {role_info}.")

    if experience:
        # Truncate long experience blobs
        exp_snippet = experience.strip()[:300].replace('\n', ' ')
        if len(experience) > 300:
            exp_snippet += '...'
        parts.append(f"Experience summary: {exp_snippet}")

    if location:
        parts.append(f"Location: {location.strip()}.")

    profile_summary = ' '.join(parts) if parts else "Minimal profile information provided."

    return (
        f"CV not individually reviewed (outside top-32 screened pool). "
        f"Based on available profile data — {profile_summary} — "
        f"the application did not demonstrate the minimum requirements for the "
        f"{JOB_TITLE} role: 2–3 years of directly relevant education sector "
        f"field coordination experience, enumerator team management, and survey "
        f"firm oversight. Application screened out at initial pass."
    )


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    try:
        # Fetch all discard candidates with their profile data
        cur.execute("""
            SELECT a.id as app_id,
                   c.first_name, c.last_name,
                   c.current_position, c.current_company,
                   c.experience, c.location
            FROM applications a
            JOIN candidates c ON a.candidate_id = c.id
            WHERE a.job_id = %s
              AND a.ai_recommendation = 'discard'
              AND a.id != ALL(%s)
            ORDER BY a.id
        """, (JOB_ID, SHORTLIST_IDS))

        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        candidates = [dict(zip(cols, r)) for r in rows]

        print(f"Total discard candidates to update: {len(candidates)}")

        updated = 0
        for c in candidates:
            app_id = c['app_id']
            reason = SPECIFIC_REASONS.get(app_id) or build_reason_for_unreviewed(c)

            cur.execute("""
                UPDATE applications
                SET status = 'rejected',
                    rejection_reason = %s,
                    ai_screened_at = NOW()
                WHERE id = %s
            """, (reason, app_id))
            updated += 1

        conn.commit()
        print(f"Done. {updated} candidates updated to 'rejected' with rejection reasons.")
        print(f"  - {len(SPECIFIC_REASONS)} had specific reviewed-CV reasons")
        print(f"  - {updated - len(SPECIFIC_REASONS)} had profile-based reasons")

    except Exception as e:
        conn.rollback()
        print(f"ERROR — rolled back: {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
