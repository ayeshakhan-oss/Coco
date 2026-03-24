"""
Deep CV + Application Answer parser for Job 26 — Soul Architect / Conversational UX Designer
Reads actual PDF resume text + JD screening answers for top 13 shortlisted candidates.
Outputs full analysis to console and JSON.
"""

import os, sys, base64, io, json, re
import psycopg2

DB_CONN = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

TOP_APP_IDS = [1315, 1318, 1309, 1273, 1322, 1277, 1285,
               1319, 1263, 1328, 1279, 1260, 1287,
               974, 1044]  # surprise JD-match candidates

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

def clean(t):
    return re.sub(r'\s+', ' ', t).strip()

def safe_print(text):
    """Print with unicode safety — replace unencodable chars."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', errors='replace').decode('ascii'))

def main():
    conn = psycopg2.connect(DB_CONN)
    cur  = conn.cursor()

    placeholders = ",".join(["%s"] * len(TOP_APP_IDS))
    cur.execute(f"""
        SELECT a.id, c.first_name, c.last_name, c.email, c.location,
               a.ai_overall_score, a.ai_jd_analysis,
               a.canned_answers, a.custom_answers,
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

    for app_id, fn, ln, email, loc, score, tier, canned, custom, resume_b64 in rows:
        name = f"{(fn or '').strip()} {(ln or '').strip()}".strip()
        safe_print(f"\n{'='*80}")
        safe_print(f"APP {app_id} | {name} | Score: {score} | Tier: {tier} | Location: {loc}")
        safe_print(f"{'='*80}")

        # ── Salary ──────────────────────────────────────────────────────────────
        exp_sal = "Not mentioned"
        curr_sal = "Not mentioned"
        relocate = "Not mentioned"
        if canned:
            exp_sal  = (canned.get("desiredSalary") or {}).get("answer") or "Not mentioned"
            curr_sal = (canned.get("currentSalary") or {}).get("answer") or "Not mentioned"
            relocate = (canned.get("willingToRelocate") or {}).get("answer") or "Not mentioned"
        safe_print(f"Expected Salary : {exp_sal}")
        safe_print(f"Current Salary  : {curr_sal}")
        safe_print(f"Relocate        : {relocate}")

        # ── JD Screening Answers ────────────────────────────────────────────────
        q_answers = []
        if custom:
            for k in sorted(custom.keys()):
                q   = custom[k].get("question", "")
                ans = custom[k].get("answer", "").strip()
                q_answers.append((q, ans))

        safe_print(f"\n--- JD SCREENING ANSWERS ({len(q_answers)} questions) ---")
        for i, (q, a) in enumerate(q_answers, 1):
            safe_print(f"Q{i}: {q[:100]}")
            safe_print(f"A{i}: {a[:800]}")
            safe_print("")

        # ── CV Text ─────────────────────────────────────────────────────────────
        cv_text = ""
        if resume_b64:
            try:
                pdf_bytes = base64.b64decode(resume_b64)
                cv_text   = parse_pdf_bytes(pdf_bytes)
            except Exception as e:
                safe_print(f"[CV parse error: {e}]")

        safe_print(f"\n--- CV TEXT (first 3000 chars) ---")
        if cv_text.strip():
            safe_print(cv_text[:3000])
        else:
            safe_print("[No CV text extracted]")

        results.append({
            "app_id":      app_id,
            "name":        name,
            "score":       float(score),
            "tier":        tier,
            "location":    loc or "",
            "exp_salary":  exp_sal,
            "curr_salary": curr_sal,
            "relocate":    relocate,
            "jd_answers":  [{"q": q, "a": a[:1000]} for q, a in q_answers],
            "cv_excerpt":  clean(cv_text[:5000]) if cv_text else "",
        })

    out = os.path.join(os.path.dirname(__file__), "output", "job26_deep_parse.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    safe_print(f"\n\nSaved to: {out}")

if __name__ == "__main__":
    main()
