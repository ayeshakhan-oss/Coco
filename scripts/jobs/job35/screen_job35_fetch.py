"""
Job 35 — Junior Research Associate – Impact & Policy
Screens all 291 applications: fetches CVs, parses PDFs (with OCR fallback),
keyword-scores against JD, saves results to Neon DB.
"""

import os, sys, base64, io, re, json, time
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# ── DB ────────────────────────────────────────────────────────────────────────
DB_CONN = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

# ── PDF parsing ───────────────────────────────────────────────────────────────
def parse_pdf_bytes(pdf_bytes):
    """Extract text from PDF bytes. Falls back to OCR for scanned PDFs."""
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
            import fitz
            import pytesseract
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

# Hard skills / tools
TOOLS_T4   = ["stata", "r studio", "rstudio", "r programming", "python", "pandas", "numpy", "scipy"]
TOOLS_T3   = ["spss", "eviews", "matlab", "sql", "tableau", "power bi", "nvivo"]
TOOLS_T2   = ["excel", "google sheets", "microsoft excel", "ms excel", "advanced excel", "pivot table"]

# Research methods
METHODS_HI = ["regression", "econometric", "causal inference", "difference in differences", "diff-in-diff",
               "randomized control", "rct", "propensity score", "fixed effects", "panel data",
               "logit", "probit", "ols", "multivariate", "sampling design", "pre-analysis plan",
               "theory of change", "logframe", "indicator framework", "baseline survey", "endline survey",
               "mixed methods", "qualitative coding", "thematic analysis", "focus group", "key informant"]
METHODS_LO = ["survey", "data collection", "data cleaning", "data entry", "descriptive statistics",
               "data analysis", "data visualization", "chi-square", "t-test", "mean", "standard deviation"]

# Research experience signals
RA_WORK    = ["research assistant", "research associate", "ra position", "ra at", "ra,", "r.a.",
               "field researcher", "enumerator", "data collector", "survey enumerator"]
THESIS     = ["thesis", "dissertation", "final year project", "fyp", "research paper", "published",
               "working paper", "journal", "conference paper", "capstone project"]

# High-signal research orgs
ORGS_ELITE = ["cerp", "j-pal", "jpal", "ipa ", "idinsight", "world bank", "ifpri", "igi", "igc",
               "ideas pakistan", "sdpi", "pide", "lahore school of economics", "lse pakistan",
               "iods", "action aid", "oxfam research", "development economics"]
ORGS_GOOD  = ["unicef", "undp", "fcdo", "dfid", "usaid", "giz", "aga khan", "akesp",
               "teach for pakistan", "tcf", "read foundation", "alif ailaan", "sabaq",
               "taleemabad", "edtech", "education trust", "pakistan education"]

# Top universities (research-oriented)
UNI_ELITE  = ["lums", "iba karachi", "iba lahore", "nust", "agu", "agha khan university",
               "university of cambridge", "university of oxford", "lse london", "harvard",
               "columbia", "yale", "stanford", "chicago", "mit", "kfupm", "kcl", "ucl",
               "university of toronto", "melbourne", "sydney", "anu"]
UNI_GOOD   = ["forman christian", "fccu", "gcu lahore", "government college", "qau", "quaid-i-azam",
               "pu lahore", "karachi university", "mu lahore", "comsats", "szabist", "iiu islamabad",
               "bahria university", "bnu", "beaconhouse", "ucp", "pmas arid",
               "university of agriculture", "fast nuces", "ned university", "uet"]

# Degree fields
DEGREE_HI  = ["economics", "econometrics", "statistics", "data science", "quantitative",
               "public policy", "development studies", "social policy", "research methods"]
DEGREE_MED = ["social sciences", "sociology", "political science", "education", "psychology",
               "anthropology", "geography", "public administration", "international development",
               "international relations", "environmental studies"]
DEGREE_LOW = ["business administration", "mba", "bba", "management", "marketing", "finance",
               "accounting", "engineering", "computer science", "information technology"]

# Reporting/communication
REPORTING  = ["policy brief", "policy note", "research report", "technical report", "executive summary",
               "data visualization", "dashboard", "infographic", "presentation", "grant proposal",
               "m&e framework", "monitoring evaluation", "kpi", "logframe", "indicator"]

# Red flags
RED_FLAGS  = ["sales executive", "marketing manager", "business development", "customer service",
               "retail", "hr manager", "procurement officer", "supply chain", "mechanical engineer",
               "electrical engineer", "civil engineer", "software developer", "web developer",
               "graphic designer", "fashion", "textile"]


def kw(text, words):
    """Count how many keywords appear in text."""
    return sum(1 for w in words if w in text)


# ── Scoring engine ────────────────────────────────────────────────────────────

def score_candidate(cv_text):
    """
    Returns (total_score_0_100, dimension_scores_dict, summary_str)
    7 dimensions, weighted as per screening framework.
    """
    t = cv_text  # already lowercased

    # ── Red flag check ────────────────────────────────────────────────────────
    red = kw(t, RED_FLAGS)
    if red >= 2:
        return 20.0, {}, "Red flag: unrelated professional background"

    # ── Dimension 1: Functional Match (quantitative research) — 25% ──────────
    methods_hi = kw(t, METHODS_HI)
    methods_lo = kw(t, METHODS_LO)
    tools_pts  = 4 if kw(t, TOOLS_T4) else (3 if kw(t, TOOLS_T3) else (2 if kw(t, TOOLS_T2) else 0))

    func_raw = 0
    if methods_hi >= 4:           func_raw = 4
    elif methods_hi >= 2:         func_raw = 3
    elif methods_hi >= 1:         func_raw = 3 if tools_pts >= 3 else 2
    elif methods_lo >= 3:         func_raw = 2
    elif methods_lo >= 1:         func_raw = 1
    func_raw = min(4, max(func_raw, tools_pts - 1))  # tool proficiency lifts floor

    # ── Dimension 2: Demonstrated Outcomes (thesis/RA work) — 20% ────────────
    ra = kw(t, RA_WORK)
    th = kw(t, THESIS)
    orgs_e = kw(t, ORGS_ELITE)
    orgs_g = kw(t, ORGS_GOOD)

    outcome_raw = 0
    if ra >= 1 and orgs_e >= 1:   outcome_raw = 4
    elif ra >= 2:                  outcome_raw = 4
    elif ra >= 1 and th >= 1:      outcome_raw = 4
    elif ra >= 1:                  outcome_raw = 3
    elif th >= 2:                  outcome_raw = 3
    elif th >= 1:                  outcome_raw = 2
    elif methods_hi >= 2:          outcome_raw = 2
    else:                          outcome_raw = 1

    # ── Dimension 3: Environment Fit (education/dev sector, Pakistan) — 15% ──
    env_raw = 0
    if orgs_e >= 1:                env_raw = 4
    elif orgs_g >= 2:              env_raw = 4
    elif orgs_g >= 1:              env_raw = 3
    elif any(w in t for w in ["education", "school", "pakistan", "social sector", "ngo", "nonprofit"]):
        env_raw = 2
    else:                          env_raw = 1

    # ── Dimension 4: Ownership & Execution — 15% ─────────────────────────────
    own_signals = ["independently", "designed", "led", "managed", "developed", "created",
                   "built", "implemented", "organized", "coordinated", "supervised"]
    own_count = kw(t, own_signals)
    thesis_independent = th >= 1 and methods_hi >= 1

    own_raw = 0
    if thesis_independent and ra >= 1:  own_raw = 4
    elif thesis_independent:             own_raw = 3
    elif ra >= 1 and own_count >= 2:     own_raw = 3
    elif own_count >= 3:                 own_raw = 2
    elif own_count >= 1 or ra >= 1:      own_raw = 2
    else:                                own_raw = 1

    # ── Dimension 5: Stakeholder & Communication — 10% ───────────────────────
    rep = kw(t, REPORTING)
    comm_signals = ["communicated", "presented", "briefed", "reported", "written", "authored",
                    "facilitated", "stakeholder", "workshop", "training"]
    comm_count = kw(t, comm_signals)

    comm_raw = 0
    if rep >= 3:                   comm_raw = 4
    elif rep >= 2:                 comm_raw = 3
    elif rep >= 1 or comm_count >= 3: comm_raw = 2
    else:                          comm_raw = 1

    # ── Dimension 6: Hard Skills / Technical — 10% ───────────────────────────
    hard_raw = tools_pts  # 0–4 from tools scoring above

    # ── Dimension 7: Growth & Leadership Potential — 5% ──────────────────────
    uni_e = kw(t, UNI_ELITE)
    uni_g = kw(t, UNI_GOOD)
    deg_h = kw(t, DEGREE_HI)
    deg_m = kw(t, DEGREE_MED)

    growth_raw = 0
    if uni_e >= 1 and deg_h >= 1:   growth_raw = 4
    elif uni_e >= 1:                 growth_raw = 3
    elif uni_g >= 1 and deg_h >= 1:  growth_raw = 3
    elif uni_g >= 1:                 growth_raw = 2
    elif deg_h >= 1:                 growth_raw = 2
    elif deg_m >= 1:                 growth_raw = 1
    else:                            growth_raw = 1

    # ── Weighted total ────────────────────────────────────────────────────────
    dims = {
        "functional":  func_raw,
        "outcomes":    outcome_raw,
        "environment": env_raw,
        "ownership":   own_raw,
        "communication": comm_raw,
        "hard_skills": hard_raw,
        "growth":      growth_raw,
    }
    weights = {
        "functional": 0.25, "outcomes": 0.20, "environment": 0.15,
        "ownership": 0.15, "communication": 0.10, "hard_skills": 0.10, "growth": 0.05,
    }
    raw_weighted = sum(dims[d] * weights[d] for d in dims)
    score = (raw_weighted / 4.0) * 100

    # ── Must-have penalty ─────────────────────────────────────────────────────
    missing_mh = 0
    if tools_pts == 0 and methods_hi == 0 and methods_lo < 2:
        missing_mh += 1   # No quantitative exposure at all
    if kw(t, DEGREE_HI + DEGREE_MED) == 0:
        missing_mh += 1   # Completely unrelated degree

    score = score * (0.85 ** missing_mh)

    # ── Summary string ────────────────────────────────────────────────────────
    tool_str = (
        "Stata/R/Python" if kw(t, TOOLS_T4) else
        "SPSS/SQL/Tableau" if kw(t, TOOLS_T3) else
        "Excel" if kw(t, TOOLS_T2) else "No tools mentioned"
    )
    org_str = ""
    for org in ORGS_ELITE:
        if org in t:
            org_str = org.upper() + " experience"
            break
    if not org_str:
        for org in ORGS_GOOD:
            if org in t:
                org_str = org.upper() + " exposure"
                break

    summary = (
        f"Tools: {tool_str} | "
        f"Methods: {methods_hi} hi/{methods_lo} lo | "
        f"RA work: {'Yes' if ra else 'No'} | "
        f"Thesis: {'Yes' if th else 'No'}"
        + (f" | {org_str}" if org_str else "")
        + (f" | MISSING MH: {missing_mh}" if missing_mh else "")
    )

    return round(score, 1), dims, summary


def tier(score):
    if score >= 85:  return "Tier A"
    if score >= 70:  return "Tier B"
    if score >= 55:  return "Tier C"
    return "No-Hire"


def budget_fit(salary_text):
    """Simple budget check — salary PKR 150K–200K."""
    nums = re.findall(r'[\d,]+', salary_text.replace(" ", ""))
    amounts = []
    for n in nums:
        try:
            v = int(n.replace(",", ""))
            if 10000 <= v <= 2000000:
                amounts.append(v)
        except Exception:
            pass
    if not amounts:
        return "Not mentioned", "unknown"
    avg = sum(amounts) / len(amounts)
    if avg <= 200000:
        return f"PKR {amounts[0]:,}", "in_budget"
    elif avg <= 230000:
        return f"PKR {amounts[0]:,}", "borderline"
    else:
        return f"PKR {amounts[0]:,}", "over_budget"


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    import psycopg2
    conn = psycopg2.connect(DB_CONN)
    cur  = conn.cursor()

    print("Fetching applications for Job 35...")
    cur.execute("""
        SELECT a.id AS app_id, a.candidate_id,
               c.resume_data, c.email
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = 35
        ORDER BY a.id
    """)
    rows = cur.fetchall()
    print(f"Total applications: {len(rows)}")

    results = []
    failed  = []

    for i, (app_id, cand_id, resume_b64, email) in enumerate(rows, 1):
        sys.stdout.write(f"\r  Processing {i}/{len(rows)}...")
        sys.stdout.flush()

        cv_text = ""
        if resume_b64:
            try:
                pdf_bytes = base64.b64decode(resume_b64)
                cv_text   = parse_pdf_bytes(pdf_bytes)
            except Exception as e:
                failed.append((app_id, str(e)))
                cv_text = ""

        if not cv_text.strip():
            score_val = 10.0
            dims      = {}
            summary   = "CV unreadable or missing"
        else:
            score_val, dims, summary = score_candidate(cv_text)

        t = tier(score_val)

        # ai_recommendation only accepts 'shortlist' or 'discard'
        rec = "shortlist" if score_val >= 55 else "discard"
        # DB columns ai_overall_score and ai_jd_score are 0–10 scale
        db_score = round(score_val / 10.0, 2)

        # Write back to DB
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

    # ── Print summary ─────────────────────────────────────────────────────────
    results.sort(key=lambda x: x["score"], reverse=True)

    tier_counts = {"Tier A": 0, "Tier B": 0, "Tier C": 0, "No-Hire": 0}
    for r in results:
        tier_counts[r["tier"]] += 1

    print(f"\n{'='*70}")
    print(f"JOB 35 — Junior Research Associate – Impact & Policy")
    print(f"Total screened: {len(results)}")
    print(f"Tier A (85+):  {tier_counts['Tier A']}")
    print(f"Tier B (70-84):{tier_counts['Tier B']}")
    print(f"Tier C (55-69):{tier_counts['Tier C']}")
    print(f"No-Hire (<55): {tier_counts['No-Hire']}")
    print(f"{'='*70}")

    print(f"\nTOP 40 CANDIDATES:")
    print(f"{'Rank':<5} {'AppID':<8} {'Score':<7} {'Tier':<10} Summary")
    print("-" * 100)
    for rank, r in enumerate(results[:40], 1):
        print(f"{rank:<5} {r['app_id']:<8} {r['score']:<7} {r['tier']:<10} {r['summary'][:80]}")

    # Save results to JSON for report script
    out_path = os.path.join(os.path.dirname(__file__), "output", "job35_screening_results.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to: {out_path}")


if __name__ == "__main__":
    main()
