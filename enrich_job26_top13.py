"""
Job 26 — Soul Architect / Conversational UX Designer
Enriches top 13 candidates: extracts university, degree, current role, org signals, AI tools used.
"""
import os, sys, base64, io, re, json
import psycopg2

DB_CONN = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

TOP_APP_IDS = [
    1315, 1318, 1309, 1273, 1322, 1277, 1285,
    1319, 1263, 1279, 1328, 1260, 1287,
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
        ("LUMS", "lums"), ("LUMS", "lahore university of management"),
        ("IBA Karachi", "iba karachi"), ("IBA", "institute of business administration"),
        ("NUST", "nust"), ("FAST-NUCES", "fast nuces"), ("FAST-NUCES", "nuces"),
        ("QAU", "quaid-i-azam"), ("QAU", "qau islamabad"),
        ("Forman Christian (FCCU)", "forman christian"),
        ("GCU Lahore", "government college university"),
        ("UCP", "university of central punjab"),
        ("COMSATS", "comsats"), ("SZABIST", "szabist"),
        ("IIU Islamabad", "international islamic university"),
        ("Bahria University", "bahria university"),
        ("BNU", "beaconhouse national"),
        ("Karachi University", "university of karachi"),
        ("PU Lahore", "university of the punjab"),
        ("NED University", "ned university"),
        ("Aga Khan University", "aga khan university"),
        ("Oxford", "university of oxford"), ("Cambridge", "university of cambridge"),
        ("LSE", "london school of economics"), ("UCL", "university college london"),
        ("Sciences Po", "sciences po"),
        ("UET", "university of engineering and technology"),
        ("Air University", "air university"),
        ("Indus Valley", "indus valley"),
        ("NCA", "national college of arts"), ("NCA", "nca lahore"),
        ("SZABIST", "shaheed zulfikar ali bhutto"),
    ]
    for name, keyword in unis:
        if keyword in t:
            return name
    m = re.search(r'university of ([\w\s]+)', t)
    if m:
        return "University of " + m.group(1).strip().title()[:30]
    return "Not specified"


def extract_degree(text):
    t = text.lower()
    degrees = [
        ("PhD", ["phd", "ph.d", "doctor of philosophy"]),
        ("MS/MPhil Psychology", ["ms psychology", "mphil psychology", "master of psychology", "masters psychology"]),
        ("MS/MPhil Anthropology", ["ms anthropology", "mphil anthropology", "master of anthropology"]),
        ("MS/MPhil Cognitive Science", ["ms cognitive", "mphil cognitive", "master of cognitive"]),
        ("MS/MPhil HCI", ["ms hci", "mphil hci", "human-computer interaction", "ms interaction design"]),
        ("MS/MPhil (Social Science)", ["ms sociology", "ms social", "mphil social", "ms communication", "ms linguistics"]),
        ("MS/MA", ["master of science", "master of arts", "msc ", "m.sc", "ms ", "m.s.", "mphil", "m.phil", "masters in"]),
        ("MBA", ["mba", "master of business"]),
        ("BS Psychology", ["bs psychology", "bsc psychology", "bachelor of psychology", "psychology hons"]),
        ("BS Anthropology", ["bs anthropology", "bsc anthropology", "bachelor of anthropology"]),
        ("BS Cognitive Science", ["bs cognitive", "bachelor of cognitive"]),
        ("BS Linguistics", ["bs linguistics", "bsc linguistics", "bachelor of linguistics"]),
        ("BS Design / HCI", ["bs design", "bsc design", "bachelor of design", "bs interaction", "bs ux",
                              "bs visual communication", "bachelor of fine arts", "bfa", "be design"]),
        ("BS Social Sciences", ["bs social sciences", "bsc social", "bachelor of social science", "bs sociology",
                                  "ba sociology", "bs communication", "ba communication"]),
        ("BS (Other)", ["bachelor", "bs ", "b.s.", "ba ", "b.a.", "bsc "]),
    ]
    for label, patterns in degrees:
        for p in patterns:
            if re.search(p, t):
                return label
    if "bachelor" in t: return "Bachelor's (field unclear)"
    if "master" in t:   return "Master's (field unclear)"
    return "Degree not specified"


def extract_current_role(text):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    role_keywords = [
        "ux", "ui", "designer", "researcher", "strategist", "consultant",
        "writer", "analyst", "lead", "manager", "intern", "associate",
        "officer", "coordinator", "fellow", "founder", "freelance",
        "product", "conversational", "content", "brand", "creative",
        "psychologist", "therapist", "educator", "lecturer", "teacher",
    ]
    for line in lines[:30]:
        ll = line.lower()
        if any(k in ll for k in role_keywords) and 8 < len(line) < 80:
            return line.strip()
    for line in lines[1:10]:
        if len(line) > 10 and not any(c in line for c in ['@', 'http', '+92', '03', 'linkedin']):
            return line.strip()[:80]
    return "Not specified"


def extract_ai_tools(text):
    t = text.lower()
    tools = {
        "ChatGPT": ["chatgpt", "chat gpt"],
        "Claude": ["claude", "anthropic"],
        "GPT-4": ["gpt-4", "gpt4", "openai"],
        "Prompt Engineering": ["prompt engineering", "prompt engineer"],
        "LangChain": ["langchain", "lang chain"],
        "Midjourney": ["midjourney", "mid journey"],
        "Figma": ["figma"],
        "Dialogflow": ["dialogflow", "dialog flow"],
        "Rasa": ["rasa"],
        "Botpress": ["botpress"],
        "Notion AI": ["notion ai"],
        "GitHub Copilot": ["copilot", "github copilot"],
        "LLM/AI agents": ["llm", "large language model", "ai agent", "generative ai"],
    }
    found = [label for label, keywords in tools.items() if any(k in t for k in keywords)]
    return ", ".join(found[:5]) if found else "None mentioned"


def extract_orgs(text):
    t = text.lower()
    signals = {
        "World Bank": "world bank", "UNICEF": "unicef", "UNDP": "undp",
        "FCDO": "fcdo", "USAID": "usaid", "GIZ": "giz",
        "Google": "google", "Microsoft": "microsoft", "Meta": "meta",
        "Anthropic": "anthropic", "OpenAI": "openai",
        "Taleemabad": "taleemabad", "TCF": "the citizens foundation",
        "Teach For Pakistan": "teach for pakistan",
        "Aga Khan": "aga khan", "British Council": "british council",
        "IDEO": "ideo", "Acumen": "acumen", "Ashoka": "ashoka",
        "McKinsey": "mckinsey", "BCG": "bcg",
    }
    found = [label for label, kw in signals.items() if kw in t]
    return ", ".join(found[:4]) if found else ""


def extract_writing_signal(text):
    t = text.lower()
    signals = []
    if any(k in t for k in ["published", "publication", "journal", "conference paper"]): signals.append("Published")
    if any(k in t for k in ["thesis", "dissertation"]): signals.append("Thesis")
    if any(k in t for k in ["blog", "substack", "newsletter", "medium.com"]): signals.append("Blog/Newsletter")
    if any(k in t for k in ["ux writing", "content design", "copywriting"]): signals.append("UX Writing")
    if any(k in t for k in ["ethnograph", "field research", "participant observation"]): signals.append("Ethnography")
    if any(k in t for k in ["fulbright", "chevening", "erasmus", "rhodes"]): signals.append("Scholarship")
    return ", ".join(signals) if signals else ""


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
    seen = set()

    for i, (app_id, fn, ln, email, score, tier_label, summary, resume_b64) in enumerate(rows, 1):
        if email in seen:
            continue
        seen.add(email)

        sys.stdout.write(f"\r  Parsing {i}/{len(rows)}: {fn} {ln}...")
        sys.stdout.flush()

        cv_text = ""
        if resume_b64:
            try:
                pdf_bytes = base64.b64decode(resume_b64)
                cv_text   = parse_pdf_bytes(pdf_bytes)
            except Exception:
                pass

        uni      = extract_university(cv_text)    if cv_text else "Not parsed"
        degree   = extract_degree(cv_text)        if cv_text else "Not parsed"
        role     = extract_current_role(cv_text)  if cv_text else "Not parsed"
        ai_tools = extract_ai_tools(cv_text)      if cv_text else "Not parsed"
        orgs     = extract_orgs(cv_text)          if cv_text else ""
        writing  = extract_writing_signal(cv_text) if cv_text else ""

        name = f"{(fn or '').strip().title()} {(ln or '').strip().title()}".strip()
        results.append({
            "app_id":       app_id,
            "name":         name,
            "email":        email or "",
            "score":        round(float(score) * 10, 1),
            "tier":         tier_label,
            "summary":      summary or "",
            "university":   uni,
            "degree":       degree,
            "current_role": role[:80],
            "ai_tools":     ai_tools,
            "org_signal":   orgs,
            "writing":      writing,
        })

    print(f"\n\nDone. {len(results)} candidates enriched.\n")
    print(f"{'#':<4} {'Name':<26} {'Score':<7} {'Tier':<10} {'Degree':<28} {'Uni':<25} {'AI Tools':<25} {'Writing'}")
    print("-" * 145)
    for i, r in enumerate(results, 1):
        print(f"{i:<4} {r['name']:<26} {r['score']:<7} {r['tier']:<10} {r['degree']:<28} {r['university']:<25} {r['ai_tools']:<25} {r['writing']}")

    out_path = os.path.join(os.path.dirname(__file__), "output", "job26_top13_enriched.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to: {out_path}")


if __name__ == "__main__":
    main()
