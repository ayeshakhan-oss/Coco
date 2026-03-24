"""
Job 26 — Update revised human-judgement scores after full JD re-read.
Shortlist drops from 6 to 2 genuine matches.
"""
import psycopg2

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb", "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd", "sslmode": "require",
}

REVISIONS = {
    1315: (73, "shortlist",
        "RECOMMEND | Tier B (73). Danyal Haroon — strongest match in pool. "
        "LUMS CS + MA Digital Media (Manchester), dissertation on AI chatbot interfaces. "
        "Heavy AI tool user (ChatGPT, Claude, Gemini) — meets daily-use requirement. "
        "UX at HBL (18-city focus groups, qualitative research) and AIO AI platform. "
        "Strong writer; understands human-AI interaction academically and practically. "
        "Gap: behavioral science training is adjacent (MA coursework) not primary — not a trained "
        "psychologist or anthropologist. Closest genuine match in the pool."),

    980:  (65, "shortlist",
        "RECOMMEND | Tier C (65). Aisha Bashir — 10 years creating educational content at Taleemabad "
        "(script writing, content ideation, lesson planning, team supervision). "
        "Deep practical understanding of teacher psychology from years of educational media production. "
        "Strong writer and creative director. MPhil Art & Design (Indus Valley). "
        "Gap: no AI tool fluency evidenced; no formal behavioral science or qualitative research training. "
        "Taleemabad-native context and creative writing ability make her worth interviewing. "
        "Interview focus: assess AI readiness and research thinking."),

    1318: (48, "discard",
        "NO-HIRE (48, revised from 78). Hulalah Khan — strong behavioral science foundation "
        "(LUMS Sociology-Anthropology + Psychology minor, CGPA 3.5) and qualitative research training, "
        "but missing the critical AI tool fluency requirement (must-have per JD). "
        "Current role is counselling and teaching — no evidence of AI tool usage, prompt writing, "
        "or conversational design. Skills listed (SPSS, R-Studio, Canva) are traditional "
        "research/design tools. Early-career profile without the implementation layer this role demands. "
        "Behavioural science theory is present; the ability to translate that into AI product behaviour is not."),

    974:  (38, "discard",
        "NO-HIRE (38, revised from 72). Muhammad Ammar Khan — AI tool fluency is present "
        "(ChatGPT, Gemini, Claude) but this is the only JD must-have met. "
        "No behavioral science, anthropology, or human sciences background. "
        "No qualitative research experience. No evidence of persuasive or manifesto-style writing. "
        "CS graduate (SZABIST 2025) with freelance UX interest. Fails on 4/5 must-haves."),

    1294: (42, "discard",
        "NO-HIRE (42, revised from 65). Asad Nawaz — experienced AI product designer "
        "(Vyro.ai 100M+ downloads, Qlu.ai, Addo AI) with strong execution credentials. "
        "But this role is NOT primarily a product design role — it requires behavioral science training, "
        "ethnographic research, philosophical thinking about human-AI relationships, and persuasive writing. "
        "Asad has none of these. Electrical Engineering background + fintech/SaaS domain. "
        "Screened out on core JD requirements despite impressive design portfolio."),

    1259: (40, "discard",
        "NO-HIRE (40, revised from 58). Muhammad Taimoor — lists Conversational UX as a skill "
        "but actual work is marketplace/SaaS/e-commerce UI design with no behavioral science, "
        "no qualitative research, no persuasive writing, and no AI tool usage evidenced beyond standard tools. "
        "Does not meet the human sciences or writing must-haves for this role."),
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()
    try:
        for app_id, (score, rec, summary) in REVISIONS.items():
            cur.execute("""
                UPDATE applications
                SET ai_overall_score = %s,
                    ai_jd_score = %s,
                    ai_recommendation = %s,
                    ai_screening_summary = %s,
                    ai_screened_at = NOW()
                WHERE id = %s AND job_id = 26
            """, (round(score/10, 1), round(score/10, 1), rec, summary, app_id))
            print(f"  [{app_id}] score={score} rec={rec}")
        conn.commit()
        print("Done. 6 records updated.")
    except Exception as e:
        conn.rollback()
        print(f"ERROR: {e}"); raise
    finally:
        cur.close(); conn.close()

if __name__ == "__main__":
    main()
