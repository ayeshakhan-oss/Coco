"""
Job 26 — Write human-judgement scores to DB for all 42 candidates
Soul Architect / Conversational UX Designer
"""
import psycopg2

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb", "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd", "sslmode": "require",
}

# Format: app_id -> (score_0_100, summary)
# ai_overall_score and ai_jd_score stored on 0–10 scale (divide by 10)
# ai_recommendation: 'shortlist' if score >= 55, else 'discard'

CANDIDATES = {

    # ── TIER B — SHORTLIST ──────────────────────────────────────────────────
    1315: (82,
        "RECOMMEND · Tier B (82). Danyal Haroon — strongest candidate in pool. Psychology BSc + "
        "Wharton behavioral economics training. AI tool fluency (ChatGPT, Midjourney, Notion AI). "
        "Blog/newsletter writing demonstrates voice and behavioral storytelling. Total exp ~3 yrs; "
        "relevant (behavioral science + conversational UX writing) ~2 yrs. Meets JD minimum. "
        "Flag: no formal UX design portfolio — growth candidate for the writing/behavior side."),

    1318: (78,
        "RECOMMEND · Tier B (78). Hulalah Khan — UX designer with behavioral science lens. UX "
        "portfolio includes chatbot flows and user journey mapping. Qualitative research background "
        "(user interviews, usability testing). Writing samples show clear, structured voice. "
        "Total exp ~3 yrs; relevant (UX + conversational design) ~2.5 yrs. "
        "Flag: no explicit AI tool adoption mentioned — ask in interview."),

    974: (72,
        "INTERVIEW · Tier B (72). Muhammad Ammar Khan — product design + UX research background. "
        "Conversational UI work (chatbot flows) visible in portfolio. Understands user mental models. "
        "Total exp ~2.5 yrs; relevant (conversational UX + qualitative methods) ~2 yrs. "
        "Meets JD minimum on experience. Slightly junior on behavioral science theory depth."),

    # ── TIER C — CONSIDER ───────────────────────────────────────────────────
    1294: (65,
        "CONSIDER · Tier C (65). Asad Nawaz — UX designer with content strategy exposure. "
        "Experience spans user research, information architecture, and copywriting for digital "
        "products. Behavioral science knowledge is applied rather than theoretical. Total exp ~4 yrs; "
        "relevant (UX writing + conversational content) ~2 yrs. Good profile but thinner on "
        "behavioral science credentials compared to top-tier candidates."),

    980: (63,
        "CONSIDER · Tier C (63). Aisha Bashir — content designer/UX writer with education sector "
        "background. Ed-tech product experience is a plus for this role context. Writing samples "
        "demonstrate clear, user-friendly tone. Total exp ~3 yrs; relevant (UX writing + content "
        "design) ~2 yrs. Gap: no behavioral science framework or AI tool usage mentioned."),

    1259: (58,
        "CONSIDER · Tier C (58). Muhammad Taimoor — UI/UX designer with some content writing "
        "experience. User journey and wireframing skills present. Total exp ~2 yrs; relevant "
        "(UX + writing overlap) ~1 yr. Below JD minimum on behavioral science and AI tool depth. "
        "Worth a first conversation if top-tier shortlist is small."),

    # ── NO-HIRE (BORDERLINE) ────────────────────────────────────────────────
    1322: (52,
        "NO-HIRE (borderline 52). Rimsha Faisal — junior UX designer. Portfolio shows visual UI "
        "work; limited evidence of conversational design, behavioral science, or AI tools. "
        "Total exp ~1.5 yrs; relevant exp insufficient for this role. Does not meet JD minimum."),

    # ── NO-HIRE — UI/UX DESIGNERS (WRONG DOMAIN) ───────────────────────────
    1285: (47,
        "NO-HIRE (47). Hamza Ahmed — experienced UI/UX designer with agency background. Strong "
        "visual design skills but no behavioral science, conversational AI, or content/writing "
        "dimension visible. Domain mismatch for this role."),

    1326: (45,
        "NO-HIRE (45). Faizan Ullah — UI/UX designer with product design focus. Solid design "
        "process experience but no behavioral science framework, conversational design work, "
        "or AI tools. Profile does not match Soul Architect requirements."),

    1260: (45,
        "NO-HIRE (45). Arslan Saleem — UI/UX designer. Good visual portfolio but role requires "
        "behavioral science depth, conversational UX, and AI fluency — none of these are evident "
        "in this CV. Not a fit for this specific position."),

    1311: (43,
        "NO-HIRE (43). Ghulam Qadir — UX/product designer with reasonable length CV. Design "
        "thinking skills present but no behavioral science, conversational AI design, or writing "
        "specialty. Domain mismatch."),

    1287: (42,
        "NO-HIRE (42). Muhammad Jaffer — UI/UX designer. Portfolio-focused profile; no evidence "
        "of behavioral science training, conversational design, or AI tool usage relevant to "
        "a Soul Architect role."),

    1313: (40,
        "NO-HIRE (40). Aaqib Khan — UI/UX designer. Decent design skills but profile does not "
        "include behavioral science, conversational UX, or AI writing tools. Not aligned with "
        "JD requirements."),

    1320: (38,
        "NO-HIRE (38). Nain Tara — UX designer/researcher. User research background is a mild "
        "positive but no conversational AI design, behavioral science theory, or content writing "
        "dimension present. Does not meet JD fit requirements."),

    1319: (36,
        "NO-HIRE (36). Talal Hassan Khan — UI designer with some UX. Visual-heavy profile; "
        "no behavioral science, conversational design, or AI fluency. Domain mismatch."),

    1289: (38,
        "NO-HIRE (38). Hassan Bin Tariq — product/UX designer. No evidence of behavioral science "
        "framework, conversational AI design, or content writing aligned to this role."),

    1279: (37,
        "NO-HIRE (37). Muhammad Taufeeq — UI/UX designer. Standard design portfolio with no "
        "behavioral science, conversational UX, or AI tool adoption. Not a fit for Soul Architect."),

    1309: (35,
        "NO-HIRE (35). Asma Butt — UX researcher. Research skills are present but no behavioral "
        "science depth, conversational design, or AI writing tool experience. Does not meet JD."),

    1301: (35,
        "NO-HIRE (35). Manahil Ahmed — UX designer. Profile shows standard UI/UX skills without "
        "the behavioral science, conversational AI, or content creation dimensions this role needs."),

    1263: (35,
        "NO-HIRE (35). Ahmad Hamdan Akram — UX designer. No behavioral science, conversational "
        "design, or AI tool experience visible. Wrong specialist profile for this role."),

    1302: (32,
        "NO-HIRE (32). Zehra Rashid — UX/content design. Some content writing exposure but no "
        "behavioral science framework or AI tool fluency. Insufficient match for Soul Architect."),

    1316: (33,
        "NO-HIRE (33). Hamza Jamal — UI/UX designer. Design skills present but no behavioral "
        "science, conversational AI, or writing specialty relevant to this role."),

    1307: (30,
        "NO-HIRE (30). Zikra Fiaz — UX designer. Junior profile with limited evidence of "
        "conversational design, behavioral science, or AI tools. Does not meet JD minimum."),

    1277: (30,
        "NO-HIRE (30). Muhammad Abdullah Safdar — graphic/UI designer. No relevant behavioral "
        "science, conversational UX, or AI writing dimension. Domain mismatch."),

    1044: (28,
        "NO-HIRE (28). Ameer Hamza Tariq — UI designer. Junior profile; no behavioral science, "
        "conversational design, or AI tools. Does not meet minimum requirements."),

    1286: (28,
        "NO-HIRE (28). Sanaullah Mukhtar — UX designer. Brief profile; no behavioral science, "
        "conversational AI design, or content writing specialty visible."),

    1300: (28,
        "NO-HIRE (28). Muhammad Ali — designer profile. No evidence of behavioral science, "
        "conversational UX, or AI tool usage relevant to Soul Architect role."),

    1273: (28,
        "NO-HIRE (28). Zia Ullah — UI/UX designer. Standard visual design profile; "
        "no match on behavioral science, conversational design, or AI fluency."),

    1328: (27,
        "NO-HIRE (27). Hadia Sajjad — UX designer. Short profile; no behavioral science, "
        "conversational AI, or content writing specialty. Does not meet JD requirements."),

    1291: (25,
        "NO-HIRE (25). Sameen Ali — designer. Limited experience; no behavioral science, "
        "conversational design, or AI tools evident. Not a fit."),

    1304: (25,
        "NO-HIRE (25). Saad Imran — junior designer. Thin profile; no behavioral science, "
        "conversational UX, or AI tool adoption. Below minimum requirements."),

    1270: (25,
        "NO-HIRE (25). UIxFly (Moheed) — freelance UI designer. No behavioral science, "
        "conversational design, or AI writing tools. Does not meet JD requirements."),

    1268: (25,
        "NO-HIRE (25). Muhammad Wasi Haider — UI designer. Standard design profile; "
        "no relevant behavioral science or conversational AI design experience."),

    1284: (22,
        "NO-HIRE (22). Syed Manan Ali — junior designer profile. Very limited experience; "
        "no match on any core JD requirements for Soul Architect."),

    1297: (22,
        "NO-HIRE (22). Saad Sajid — junior profile. No behavioral science, conversational design, "
        "or AI tools. Does not meet minimum experience or skill requirements."),

    1272: (20,
        "NO-HIRE (20). Muhammad Ibrahim Khan — junior designer. Very brief profile; "
        "no alignment to behavioral science, conversational UX, or AI tool requirements."),

    1290: (20,
        "NO-HIRE (20). Majid Raffique — brief profile. No behavioral science, conversational "
        "design, or AI fluency evident. Not suitable for this role."),

    1296: (18,
        "NO-HIRE (18). Muhammad Ali — very limited profile. No evidence of any core JD dimensions "
        "for Soul Architect. Screened out at initial pass."),

    # ── NO-HIRE — THIN PROFILE ──────────────────────────────────────────────
    976: (15,
        "NO-HIRE (15). Sholmiyat Adnan — minimal CV content. No behavioral science, conversational "
        "design, AI tools, or relevant experience for this role."),

    # ── NO-HIRE — BLANK / PLACEHOLDER APPLICATIONS ─────────────────────────
    1314: (5,
        "NO-HIRE (5). Incomplete application — no CV or profile information submitted (placeholder "
        "profile). Could not be assessed against Soul Architect requirements."),

    1305: (5,
        "NO-HIRE (5). Incomplete application — no CV or profile information submitted (placeholder "
        "profile). Could not be assessed against Soul Architect requirements."),

    1262: (5,
        "NO-HIRE (5). Incomplete application — no CV or profile information submitted (placeholder "
        "profile). Could not be assessed against Soul Architect requirements."),
}


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    try:
        updated = 0
        shortlisted = 0
        discarded = 0

        for app_id, (score, summary) in CANDIDATES.items():
            score_db = round(score / 10, 1)  # convert 0–100 to 0–10 scale
            recommendation = 'shortlist' if score >= 55 else 'discard'

            cur.execute("""
                UPDATE applications
                SET ai_overall_score   = %s,
                    ai_jd_score        = %s,
                    ai_recommendation  = %s,
                    ai_screening_summary = %s,
                    ai_screened_at     = NOW()
                WHERE id = %s AND job_id = 26
            """, (score_db, score_db, recommendation, summary, app_id))

            rows_affected = cur.rowcount
            if rows_affected == 0:
                print(f"  WARNING: app_id {app_id} not found or not job 26 — skipped")
            else:
                updated += 1
                if recommendation == 'shortlist':
                    shortlisted += 1
                else:
                    discarded += 1

        conn.commit()
        print(f"Done. {updated} candidates updated.")
        print(f"  Shortlisted (score ≥55): {shortlisted}")
        print(f"  Discarded  (score <55):  {discarded}")

    except Exception as e:
        conn.rollback()
        print(f"ERROR — rolled back: {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
