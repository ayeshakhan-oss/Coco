"""
Job 26 — Soul Architect / Conversational UX Designer
Screens all 42 applications: fetches CVs, parses PDFs (with OCR fallback),
keyword-scores against JD, saves results to Neon DB.
"""

import os, sys, base64, io, re, json
import psycopg2

DB_CONN = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

# ── PDF parsing ───────────────────────────────────────────────────────────────
def parse_pdf_bytes(pdf_bytes):
    text = ""
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    except Exception:
        pass

    if len(text.strip()) < 80:
        try:
            import fitz, pytesseract
            from PIL import Image
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in doc:
                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text += pytesseract.image_to_string(img) + "\n"
        except Exception as e:
            text = text or f"[OCR failed: {e}]"

    return text.lower()


# ── Keyword lists ─────────────────────────────────────────────────────────────

# Core disciplines (Dimension 1 — Functional Match)
DISCIPLINE_HI = [
    "behavioral science", "behavioural science", "behavior science",
    "anthropology", "ethnography", "ethnographic",
    "sociolinguistics", "linguistics", "cognitive science", "cognitive psychology",
    "conversation design", "conversational ux", "conversational design",
    "ux research", "user research", "ux design", "user experience design",
    "human-computer interaction", "hci", "design thinking",
    "psychology", "social psychology", "organizational psychology",
]
DISCIPLINE_MED = [
    "sociology", "social science", "human sciences", "communication studies",
    "media studies", "journalism", "education psychology",
    "development studies", "public policy", "international development",
    "gender studies", "cultural studies",
]

# AI & prompt engineering fluency (Dimension 6 — Hard Skills)
AI_TOOLS_HI = [
    "prompt engineering", "chatgpt", "claude", "gpt-4", "gpt4", "openai",
    "langchain", "llm", "large language model", "anthropic", "ai agent",
    "rag", "retrieval augmented", "fine-tun", "llama", "gemini", "mistral",
    "hugging face", "ai tools", "generative ai",
]
AI_TOOLS_MED = [
    "chatbot", "conversational ai", "voicebot", "virtual assistant",
    "dialogflow", "rasa", "botpress", "twilio", "whatsapp bot",
    "nlp", "natural language processing", "natural language understanding",
    "speech recognition", "voice interface",
]

# Qualitative research (Dimension 2 — Demonstrated Outcomes)
QUAL_HI = [
    "ethnography", "ethnographic", "grounded theory", "discourse analysis",
    "thematic analysis", "qualitative coding", "nvivo", "atlas.ti",
    "key informant interview", "in-depth interview", "focus group",
    "phenomenological", "narrative inquiry", "case study research",
    "participant observation", "field research", "action research",
]
QUAL_MED = [
    "qualitative research", "qualitative methods", "qualitative study",
    "interview", "user interview", "user testing", "usability testing",
    "diary study", "contextual inquiry", "co-design", "participatory",
    "human-centered", "human centred",
]

# Writing & communication signals (Dimension 5)
WRITING_HI = [
    "published", "publication", "journal article", "research paper",
    "white paper", "manifesto", "policy brief", "essay",
    "newsletter", "blog", "substack", "thesis", "dissertation",
    "authored", "co-authored", "ghostwritten", "copywriting",
    "ux writing", "content strategy", "technical writing",
]
WRITING_MED = [
    "report", "article", "wrote", "writing", "storytelling", "narrative",
    "communication", "documentation", "facilitated", "workshop", "presentation",
    "stakeholder", "briefed", "presented",
]

# Education sector signals (Dimension 3 — Environment Fit)
EDUCATION_SECTOR = [
    "teacher", "school", "classroom", "pedagogy", "curriculum", "learning",
    "student", "education sector", "edtech", "ed-tech", "educational technology",
    "teach for pakistan", "tcf", "the citizens foundation", "read foundation",
    "sabaq", "taleemabad", "aga khan", "school principal",
    "mep", "ministry of education", "sed", "med", "education policy",
]
PAKISTAN_SIGNALS = [
    "pakistan", "islamabad", "lahore", "karachi", "peshawar", "urdu",
    "south asia", "pakistani", "psc", "undp pakistan", "unicef pakistan",
]
CROSS_CULTURAL = [
    "cross-cultural", "cross cultural", "multicultural", "multi-cultural",
    "cultural diversity", "global", "international", "sri lanka", "latin america",
    "hofstede", "cultural adaptation", "localization", "localisation",
]

# Ownership / execution signals (Dimension 4)
OWNERSHIP = [
    "independently", "solo", "single-handedly", "led", "designed",
    "built", "created", "developed", "launched", "implemented", "owned",
    "founded", "initiated", "managed", "delivered", "established",
]

# High-signal organisations
ORGS_ELITE = [
    "world bank", "unicef", "undp", "fcdo", "dfid", "usaid", "giz",
    "stanford", "mit", "harvard", "oxford", "cambridge", "yale", "columbia",
    "google", "microsoft", "meta", "amazon", "anthropic", "openai",
    "ideo", "mckinsey", "bcg", "monitor deloitte",
    "j-pal", "jpal", "ipa ", "idinsight", "cerp",
]
ORGS_GOOD = [
    "aga khan", "akesp", "taleemabad", "sabaq", "teach for pakistan",
    "british council", "ifc", "un women", "unwomen", "wfp",
    "care international", "plan international", "save the children",
    "acumen", "ashoka", "endeavor",
]

# Scholarships
SCHOLARSHIPS = ["fulbright", "chevening", "erasmus", "rhodes", "gates cambridge", "aga khan scholarship"]

# Elite universities
UNI_ELITE = [
    "lums", "iba karachi", "iba lahore", "nust", "agha khan university",
    "cambridge", "oxford", "harvard", "stanford", "lse", "ucl", "kcl",
    "columbia", "yale", "mit", "toronto", "melbourne", "anu", "sciences po",
    "iit ", "bits pilani",
]
UNI_GOOD = [
    "forman christian", "fccu", "gcu lahore", "qau", "quaid-i-azam",
    "pu lahore", "comsats", "szabist", "iiu islamabad", "bahria university",
    "bnu", "beaconhouse", "ucp", "fast nuces", "ned university",
    "karachi university", "lahore university",
]

# Red flags — completely unrelated backgrounds
RED_FLAGS = [
    "mechanical engineer", "electrical engineer", "civil engineer",
    "supply chain", "procurement officer", "retail manager", "warehouse",
    "fashion designer", "textile", "chef", "cook",
]


def kw(text, words):
    return sum(1 for w in words if w in text)


# ── Scoring engine ─────────────────────────────────────────────────────────────
def score_candidate(cv_text):
    t = cv_text  # already lowercased

    # Red flag check
    if kw(t, RED_FLAGS) >= 2:
        return 15.0, {}, "Red flag: completely unrelated background"

    # ── Dim 1: Functional Match — 25% ─────────────────────────────────────────
    disc_hi  = kw(t, DISCIPLINE_HI)
    disc_med = kw(t, DISCIPLINE_MED)
    ai_hi    = kw(t, AI_TOOLS_HI)
    ai_med   = kw(t, AI_TOOLS_MED)

    func_raw = 0
    if disc_hi >= 3 and ai_hi >= 1:    func_raw = 4
    elif disc_hi >= 2:                  func_raw = 4 if ai_hi else 3
    elif disc_hi >= 1 and ai_hi >= 1:   func_raw = 3
    elif disc_hi >= 1:                  func_raw = 2
    elif disc_med >= 2 and ai_med >= 1: func_raw = 2
    elif disc_med >= 1 or ai_hi >= 1:   func_raw = 1
    else:                               func_raw = 0

    # ── Dim 2: Demonstrated Outcomes — 20% ────────────────────────────────────
    qual_hi  = kw(t, QUAL_HI)
    qual_med = kw(t, QUAL_MED)
    write_hi = kw(t, WRITING_HI)
    orgs_e   = kw(t, ORGS_ELITE)
    orgs_g   = kw(t, ORGS_GOOD)

    outcome_raw = 0
    if qual_hi >= 2 and write_hi >= 1:  outcome_raw = 4
    elif qual_hi >= 1 and orgs_e >= 1:  outcome_raw = 4
    elif qual_hi >= 2:                   outcome_raw = 3
    elif qual_hi >= 1 and write_hi >= 1: outcome_raw = 3
    elif qual_hi >= 1 or (qual_med >= 2 and write_hi >= 1): outcome_raw = 2
    elif qual_med >= 1 or write_hi >= 1: outcome_raw = 1
    else:                                outcome_raw = 0

    # ── Dim 3: Environment Fit — 15% ──────────────────────────────────────────
    edu   = kw(t, EDUCATION_SECTOR)
    pak   = kw(t, PAKISTAN_SIGNALS)
    cross = kw(t, CROSS_CULTURAL)

    env_raw = 0
    if edu >= 2 and pak >= 1:     env_raw = 4
    elif edu >= 1 and pak >= 1:   env_raw = 3
    elif edu >= 2 or cross >= 2:  env_raw = 3
    elif edu >= 1 or pak >= 1:    env_raw = 2
    elif cross >= 1:              env_raw = 1
    else:                         env_raw = 1

    # ── Dim 4: Ownership & Execution — 15% ────────────────────────────────────
    own_count = kw(t, OWNERSHIP)
    own_raw = 0
    if own_count >= 5:            own_raw = 4
    elif own_count >= 3:          own_raw = 3
    elif own_count >= 2:          own_raw = 2
    elif own_count >= 1:          own_raw = 1
    else:                         own_raw = 1

    # ── Dim 5: Stakeholder & Communication — 10% ──────────────────────────────
    write_med = kw(t, WRITING_MED)
    comm_raw = 0
    if write_hi >= 3:                           comm_raw = 4
    elif write_hi >= 2:                         comm_raw = 3
    elif write_hi >= 1 or write_med >= 3:       comm_raw = 2
    else:                                        comm_raw = 1

    # ── Dim 6: Hard Skills / Technical — 10% ──────────────────────────────────
    hard_raw = 0
    if ai_hi >= 3:                           hard_raw = 4
    elif ai_hi >= 2:                         hard_raw = 3
    elif ai_hi >= 1 and ai_med >= 1:         hard_raw = 3
    elif ai_hi >= 1 or ai_med >= 2:          hard_raw = 2
    elif ai_med >= 1:                        hard_raw = 1
    else:                                    hard_raw = 0

    # ── Dim 7: Growth & Leadership Potential — 5% ─────────────────────────────
    uni_e  = kw(t, UNI_ELITE)
    uni_g  = kw(t, UNI_GOOD)
    scholar = kw(t, SCHOLARSHIPS)

    growth_raw = 0
    if scholar >= 1 or (uni_e >= 1 and disc_hi >= 1): growth_raw = 4
    elif uni_e >= 1:                                    growth_raw = 3
    elif uni_g >= 1 and disc_hi >= 1:                   growth_raw = 3
    elif uni_g >= 1:                                     growth_raw = 2
    else:                                                growth_raw = 1

    # ── Weighted total ─────────────────────────────────────────────────────────
    dims = {
        "functional":    func_raw,
        "outcomes":      outcome_raw,
        "environment":   env_raw,
        "ownership":     own_raw,
        "communication": comm_raw,
        "hard_skills":   hard_raw,
        "growth":        growth_raw,
    }
    weights = {
        "functional": 0.25, "outcomes": 0.20, "environment": 0.15,
        "ownership": 0.15, "communication": 0.10, "hard_skills": 0.10, "growth": 0.05,
    }
    raw_weighted = sum(dims[d] * weights[d] for d in dims)
    score = (raw_weighted / 4.0) * 100

    # ── Must-have penalties ────────────────────────────────────────────────────
    missing_mh = 0
    # Must-have 1: some human sciences background
    if disc_hi == 0 and disc_med == 0:
        missing_mh += 1
    # Must-have 2: some qualitative research OR AI tools fluency (at least one)
    if qual_hi == 0 and qual_med == 0 and ai_hi == 0 and ai_med == 0:
        missing_mh += 1

    score = score * (0.85 ** missing_mh)

    # ── Summary string ─────────────────────────────────────────────────────────
    ai_str = (
        "Prompt eng/LLM" if ai_hi >= 2 else
        "ChatGPT/Claude" if ai_hi >= 1 else
        "Chatbot tools"  if ai_med >= 1 else
        "No AI tools"
    )
    disc_str = ""
    for d in DISCIPLINE_HI:
        if d in t:
            disc_str = d.title()
            break
    if not disc_str:
        for d in DISCIPLINE_MED:
            if d in t:
                disc_str = d.title()
                break

    org_str = ""
    for org in ORGS_ELITE:
        if org in t:
            org_str = org.upper()
            break
    if not org_str:
        for org in ORGS_GOOD:
            if org in t:
                org_str = org.upper()
                break

    summary = (
        f"Discipline: {disc_str or 'Not evident'} | "
        f"Qual research: {qual_hi} hi/{qual_med} lo | "
        f"AI tools: {ai_str} | "
        f"Writing: {write_hi} hi"
        + (f" | Org: {org_str}" if org_str else "")
        + (f" | MISSING MH: {missing_mh}" if missing_mh else "")
    )

    return round(score, 1), dims, summary


def tier(score):
    if score >= 85: return "Tier A"
    if score >= 70: return "Tier B"
    if score >= 55: return "Tier C"
    return "No-Hire"


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    conn = psycopg2.connect(DB_CONN)
    cur  = conn.cursor()

    print("Fetching applications for Job 26 — Soul Architect...")
    cur.execute("""
        SELECT a.id AS app_id, a.candidate_id,
               c.resume_data, c.first_name, c.last_name, c.email
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = 26
        ORDER BY a.id
    """)
    rows = cur.fetchall()
    print(f"Total applications: {len(rows)}")

    results = []
    failed  = []

    for i, (app_id, cand_id, resume_b64, fname, lname, email) in enumerate(rows, 1):
        sys.stdout.write(f"\r  Processing {i}/{len(rows)}...")
        sys.stdout.flush()

        cv_text = ""
        if resume_b64:
            try:
                pdf_bytes = base64.b64decode(resume_b64)
                cv_text   = parse_pdf_bytes(pdf_bytes)
            except Exception as e:
                failed.append((app_id, str(e)))

        if not cv_text.strip():
            score_val = 10.0
            dims      = {}
            summary   = "CV unreadable or missing"
        else:
            score_val, dims, summary = score_candidate(cv_text)

        t   = tier(score_val)
        rec = "shortlist" if score_val >= 55 else "discard"
        db_score = round(score_val / 10.0, 2)

        cur.execute("""
            UPDATE applications SET
                ai_overall_score      = %s,
                ai_jd_score           = %s,
                ai_jd_analysis        = %s,
                ai_recommendation     = %s,
                ai_screening_summary  = %s,
                ai_screened_at        = NOW()
            WHERE id = %s
        """, (db_score, db_score, t, rec, summary[:500], app_id))

        results.append({
            "app_id":    app_id,
            "cand_id":   cand_id,
            "name":      f"{fname or ''} {lname or ''}".strip(),
            "email":     email or "",
            "score":     score_val,
            "tier":      t,
            "summary":   summary,
            "dims":      dims,
        })

    conn.commit()
    cur.close()
    conn.close()

    print(f"\n\nDone. {len(failed)} parse failures.")

    results.sort(key=lambda x: x["score"], reverse=True)

    tier_counts = {"Tier A": 0, "Tier B": 0, "Tier C": 0, "No-Hire": 0}
    for r in results:
        tier_counts[r["tier"]] += 1

    print(f"\n{'='*70}")
    print(f"JOB 26 — Soul Architect / Conversational UX Designer")
    print(f"Total screened: {len(results)}")
    print(f"Tier A (85+):   {tier_counts['Tier A']}")
    print(f"Tier B (70-84): {tier_counts['Tier B']}")
    print(f"Tier C (55-69): {tier_counts['Tier C']}")
    print(f"No-Hire (<55):  {tier_counts['No-Hire']}")
    print(f"{'='*70}")

    print(f"\nALL CANDIDATES RANKED:")
    print(f"{'Rank':<5} {'AppID':<8} {'Name':<25} {'Score':<7} {'Tier':<10} Summary")
    print("-" * 110)
    for rank, r in enumerate(results, 1):
        print(f"{rank:<5} {r['app_id']:<8} {r['name']:<25} {r['score']:<7} {r['tier']:<10} {r['summary'][:60]}")

    out_path = os.path.join(os.path.dirname(__file__), "output", "job26_screening_results.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to: {out_path}")


if __name__ == "__main__":
    main()
