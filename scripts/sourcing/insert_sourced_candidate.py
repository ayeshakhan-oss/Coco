"""
insert_sourced_candidate.py — Add Sourced Candidate to Markaz
==============================================================
Triggered when Ayesha confirms a sourced candidate wants to proceed.

Usage:
    python scripts/sourcing/insert_sourced_candidate.py

Triggered by: "Ayesha: [Name] confirmed interest, add them for [Role]"

This script:
1. Gets job ID from Markaz
2. Inserts candidate into candidates table (email may be null)
3. Inserts application into applications table with status='new'
4. Returns candidate ID + application ID to Ayesha
5. Logs both operations to sourcing_audit.log

Database: Neon PostgreSQL (ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech)
"""

import os
import sys
import json
import psycopg2
from datetime import datetime

# Database connection
DB_CONN = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Audit logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))
from audit_log import log_db_query


def insert_sourced_candidate(
    first_name: str,
    last_name: str,
    position: str,
    skills: list,
    location: str,
    current_position: str,
    current_company: str,
    job_id: int,
    profile_url: str,
    email: str = None,
    phone: str = None,
    sourcing_run_date: str = None
):
    """
    Insert a sourced candidate into Markaz after confirmed interest.

    Args:
        first_name: Candidate first name
        last_name: Candidate last name
        position: Target role title
        skills: List of skills (e.g., ["fundraising", "partnerships"])
        location: City, Pakistan
        current_position: Their current job title
        current_company: Their current employer
        job_id: Job ID from Markaz (jobs table)
        profile_url: LinkedIn/GitHub/org page URL
        email: Email (optional, may be null for LinkedIn sourced)
        phone: Phone (optional)
        sourcing_run_date: YYYY-MM-DD of sourcing run (default: today)

    Returns:
        dict: {"candidate_id": int, "application_id": int}
    """

    if sourcing_run_date is None:
        sourcing_run_date = datetime.now().strftime("%Y-%m-%d")

    conn = psycopg2.connect(DB_CONN)
    cursor = conn.cursor()

    try:
        # Step 1: Check for duplicate by email (skip if email is null)
        candidate_id = None
        if email:
            cursor.execute(
                "SELECT id FROM candidates WHERE email = %s LIMIT 1",
                (email,)
            )
            result = cursor.fetchone()
            if result:
                candidate_id = result[0]
                print(f"[INFO] Candidate already exists: ID {candidate_id}")
                log_db_query(
                    table="candidates",
                    filters=f"email = {email!r}",
                    rows_returned=1,
                    context="sourced_candidate_dedup_check"
                )

        # Step 2: Insert into candidates table if new
        if not candidate_id:
            tags_json = json.dumps({
                "sourced_by": "coco",
                "sourcing_run": sourcing_run_date,
                "profile_url": profile_url
            })

            cursor.execute(
                """
                INSERT INTO candidates
                (first_name, last_name, email, phone, position, skills, source,
                 location, current_position, current_company, tags, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING id
                """,
                (
                    first_name,
                    last_name,
                    email,  # may be null
                    phone,
                    position,
                    skills,  # psycopg2 handles list → TEXT[] conversion
                    "LinkedIn - Sourced",
                    location,
                    current_position,
                    current_company,
                    tags_json
                )
            )
            candidate_id = cursor.fetchone()[0]
            conn.commit()

            print(f"[INFO] Inserted candidate: ID {candidate_id}")
            log_db_query(
                table="candidates",
                filters=f"first_name={first_name!r}, email={email!r}",
                rows_returned=1,
                context="sourced_candidate_insert"
            )

        # Step 3: Insert into applications table
        notes = "Passive sourced candidate -- confirmed interest via LinkedIn DM"
        ai_recommendation = "Sourced candidate -- pending CV review"
        ai_screening_summary = f"Sourced on {sourcing_run_date} from LinkedIn - Sourced. Profile: {profile_url}"

        cursor.execute(
            """
            INSERT INTO applications
            (candidate_id, job_id, status, notes, ai_recommendation, ai_screening_summary, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            RETURNING id
            """,
            (
                candidate_id,
                job_id,
                "new",
                notes,
                ai_recommendation,
                ai_screening_summary
            )
        )
        application_id = cursor.fetchone()[0]
        conn.commit()

        print(f"[INFO] Inserted application: ID {application_id}")
        log_db_query(
            table="applications",
            filters=f"candidate_id={candidate_id}, job_id={job_id}",
            rows_returned=1,
            context="sourced_application_insert"
        )

        # Step 4: Return results
        result = {
            "candidate_id": candidate_id,
            "application_id": application_id,
            "status": "new",
            "source": "LinkedIn - Sourced",
            "sourcing_run": sourcing_run_date
        }

        print(f"\n[SUCCESS] Added to Markaz:")
        print(f"  Candidate ID: {candidate_id}")
        print(f"  Application ID: {application_id}")
        print(f"  Status: new")
        print(f"  Source: LinkedIn - Sourced")
        print(f"  Sourcing Run: {sourcing_run_date}")

        return result

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    """
    Example usage:

    result = insert_sourced_candidate(
        first_name="Muhammad",
        last_name="Hassan",
        position="Instructional Systems Lead",
        skills=["instructional design", "curriculum", "learning management"],
        location="Islamabad",
        current_position="Senior Learning Designer",
        current_company="ITA",
        job_id=42,
        profile_url="https://linkedin.com/in/muhammad-hassan-xyz",
        email=None,  # null for LinkedIn sourced
        phone=None,
        sourcing_run_date="2026-04-20"
    )

    print(json.dumps(result, indent=2))
    """
    print("[INFO] insert_sourced_candidate.py — Ready to add sourced candidates to Markaz")
    print("[INFO] Import this module and call insert_sourced_candidate() with candidate details")
