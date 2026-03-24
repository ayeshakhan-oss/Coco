"""
Fetches and parses CV text for top 30 Job 35 candidates.
Extracts: university, degree, current role / last org, key signals.
Outputs enriched JSON.
"""
import os, sys, base64, io, re, json
import psycopg2

DB_CONN = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

TOP_APP_IDS = [
    1729, 1514, 1445, 1899, 1569, 1369, 1592, 1734, 1902, 1730,
    1771, 1663, 1820, 1829, 1649, 1532, 1550, 1512, 1665, 1402,
    1696, 1641, 1765, 1487, 1534, 1456, 1944, 1880, 1854, 1725,
    1855, 1490, 1848, 1558,   # 34 Tier A + top Tier B
]

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
        except Exception:
            pass
    return text


def extract_university(text):
    t = text.lower()
    unis = [
        ("LUMS", "lums"), ("IBA Karachi", "iba karachi"), ("NUST", "nust"),
        ("FAST-NUCES", "fast nuces"), ("QAU", "quaid-i-azam"), ("QAU", "qau islamabad"),
        ("Forman Christian (FCCU)", "forman christian"), ("GCU Lahore", "government college university"),
        ("UCP", "university of central punjab"), ("COMSATS", "comsats"),
        ("SZABIST", "szabist"), ("IIU Islamabad", "international islamic university"),
        ("Bahria University", "bahria university"), ("BNU", "beaconhouse national"),
        ("PMAS Arid", "pmas arid"), ("Karachi University", "university of karachi"),
        ("PU Lahore", "university of the punjab"), ("UET", "university of engineering"),
        ("NED University", "ned university"), ("Aga Khan University", "aga khan university"),
        ("LUMS", "lahore university of management"),
        ("Oxford", "university of oxford"), ("Cambridge", "university of cambridge"),
        ("LSE", "london school of economics"), ("UCL", "university college london"),
        ("Lahore School of Economics", "lahore school of economics"),
        ("PIDE", "pakistan institute of development"),
        ("University of Agriculture", "university of agriculture"),
    ]
    for name, keyword in unis:
        if keyword in t:
            return name
    # fallback: look for "university of X"
    m = re.search(r'university of ([\w\s]+)', t)
    if m:
        return "University of " + m.group(1).strip().title()[:30]
    return "Not specified"


def extract_degree(text):
    t = text.lower()
    degrees = [
        ("PhD", ["phd", "ph.d", "doctor of philosophy"]),
        ("MS/MPhil", ["mphil", "m.phil", "master of science", "ms economics", "ms public policy",
                       "ms development", "ms statistics", "ms social", "masters in"]),
        ("MBA", ["mba", "master of business"]),
        ("BS Economics", ["bs economics", "bsc economics", "bachelor of economics", "economics hons"]),
        ("BS Statistics", ["bs statistics", "bsc statistics", "bachelor of statistics"]),
        ("BS Public Policy", ["bs public policy", "bachelor of policy"]),
        ("BS Social Sciences", ["bs social sciences", "bsc social", "bachelor of social science"]),
        ("BS Development Studies", ["development studies", "bs development"]),
        ("BA/BS (Social Science)", ["ba economics", "ba sociology", "ba political", "bs sociology",
                                     "bs political", "ba social", "bsc social"]),
        ("BS Computer Science", ["bs computer", "bsc computer", "bs cs"]),
    ]
    for label, patterns in degrees:
        for p in patterns:
            if re.search(p, t):
                return label
    if "bachelor" in t: return "Bachelor's (field unclear)"
    if "master" in t:   return "Master's (field unclear)"
    return "Degree not specified"


def extract_current_role(text):
    """Extract first likely current/recent role or university line."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    role_keywords = ["research assistant", "ra ", "intern", "analyst", "associate",
                     "officer", "coordinator", "consultant", "manager", "student",
                     "graduate", "fellow", "lecturer", "teacher", "executive"]
    for line in lines[:30]:
        ll = line.lower()
        if any(k in ll for k in role_keywords) and len(line) > 8 and len(line) < 80:
            return line.strip()
    # fallback: second non-empty line
    for line in lines[1:10]:
        if len(line) > 10 and not any(c in line for c in ['@', 'http', '+92', '03']):
            return line.strip()[:80]
    return "Not specified"


def extract_orgs(text):
    t = text.lower()
    elite = ["cerp", "j-pal", "jpal", "ipa ", "idinsight", "world bank", "ifpri",
             "igi ", "igc ", "lahore school of economics", "pide", "ideas pakistan"]
    good  = ["unicef", "undp", "fcdo", "dfid", "usaid", "giz", "aga khan",
             "teach for pakistan", "tcf", "read foundation", "sabaq", "taleemabad"]
    found = []
    for o in elite:
        if o in t: found.append(o.strip().upper())
    for o in good:
        if o in t and o.strip().upper() not in found: found.append(o.strip().upper())
    return ", ".join(found[:3]) if found else ""


def main():
    conn = psycopg2.connect(DB_CONN)
    cur  = conn.cursor()

    placeholders = ",".join(["%s"] * len(TOP_APP_IDS))
    cur.execute(f"""
        SELECT a.id, c.first_name, c.last_name, c.email,
               a.ai_overall_score, a.ai_jd_analysis, a.ai_screening_summary,
               c.resume_data
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.id IN ({placeholders})
        ORDER BY a.ai_overall_score DESC
    """, TOP_APP_IDS)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    results = []
    seen_cand = set()

    for i, (app_id, fn, ln, email, score, tier, summary, resume_b64) in enumerate(rows, 1):
        # Deduplicate by email
        if email in seen_cand:
            continue
        seen_cand.add(email)

        sys.stdout.write(f"\r  Parsing {i}/{len(rows)}: {fn} {ln}...")
        sys.stdout.flush()

        cv_text = ""
        if resume_b64:
            try:
                pdf_bytes = base64.b64decode(resume_b64)
                cv_text   = parse_pdf_bytes(pdf_bytes)
            except Exception as e:
                cv_text = ""

        uni    = extract_university(cv_text) if cv_text else "Not parsed"
        degree = extract_degree(cv_text)     if cv_text else "Not parsed"
        role   = extract_current_role(cv_text) if cv_text else "Not parsed"
        orgs   = extract_orgs(cv_text)       if cv_text else ""

        name = f"{fn.strip().title()} {ln.strip().title()}".strip()
        results.append({
            "app_id":  app_id,
            "name":    name,
            "email":   email,
            "score":   float(score) * 10,   # convert back to 0-100
            "tier":    tier,
            "summary": summary,
            "university": uni,
            "degree":     degree,
            "current_role": role[:80],
            "org_signal":   orgs,
        })

    print(f"\n\nDone. {len(results)} unique candidates enriched.\n")
    print(f"{'#':<4} {'Name':<30} {'Score':<7} {'Tier':<10} {'Degree':<25} {'Uni':<30} {'Orgs'}")
    print("-" * 130)
    for i, r in enumerate(results, 1):
        print(f"{i:<4} {r['name']:<30} {r['score']:<7} {r['tier']:<10} {r['degree']:<25} {r['university']:<30} {r['org_signal']}")

    out_path = os.path.join(os.path.dirname(__file__), "output", "job35_top30_enriched.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to: {out_path}")


if __name__ == "__main__":
    main()
