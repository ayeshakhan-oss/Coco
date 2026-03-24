"""Job 26 — Final score update: add Taimoor + Ammar Khan to shortlist"""
import psycopg2

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb", "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd", "sslmode": "require",
}

UPDATES = {
    1259: (62, "shortlist",
        "CONSIDER | Tier C (62). Muhammad Taimoor — Conversational UX Designer profile. "
        "MSc Computer Science with focus on Human-Centered Systems & Digital Products (Univ. of Gujrat). "
        "Explicitly lists Conversational UX and Prompt-Based UX Exploration as skills, alongside AI-Assisted Design. "
        "4 years UX experience: SaaS, marketplace, telehealth, and language translation app (cross-cultural). "
        "Gap: no behavioral science training; conversational UX is evidenced in skills/degree but actual "
        "work is e-commerce/SaaS UX. Fits 'Conversational UX Designer' and 'HCI' profiles the JD targets."),
    974:  (55, "shortlist",
        "CONSIDER | Tier C (55). Muhammad Ammar Khan — AI Interaction / Behavioral Designer profile. "
        "Profile explicitly states: 'focused on how people emotionally and culturally interact with digital systems; "
        "interested in human-AI relationships, behavior-driven design, and culturally responsive experiences.' "
        "Daily AI tool user (ChatGPT, Gemini, Runway, Claude). Analyses how tone, wording, and structure "
        "change user perception — behavioral design language. "
        "Gap: SZABIST CS graduate 2025, limited formal experience. JD says 'we don't care about the degree' — "
        "profile intent and AI fluency are genuine. Fits 'AI Interaction Designer' and 'Behavioral Designer' profiles."),
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()
    try:
        for app_id, (score, rec, summary) in UPDATES.items():
            cur.execute("""
                UPDATE applications
                SET ai_overall_score = %s, ai_jd_score = %s,
                    ai_recommendation = %s, ai_screening_summary = %s,
                    ai_screened_at = NOW()
                WHERE id = %s AND job_id = 26
            """, (round(score/10,1), round(score/10,1), rec, summary, app_id))
            print(f"  [{app_id}] score={score} rec={rec}")
        conn.commit()
        print("Done.")
    except Exception as e:
        conn.rollback(); print(f"ERROR: {e}"); raise
    finally:
        cur.close(); conn.close()

if __name__ == "__main__":
    main()
