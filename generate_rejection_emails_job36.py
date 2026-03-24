"""
Generate rejection emails for all Job 36 rejected candidates (Field Coordinator, R&I).
- Cat B (138): CV extracted → specific email via Claude API
- Cat C (15): pre-screened with notes → warm email via Claude API
- Cat A (8):  no CV, real email → generic template (flagged)
- Special (2): unreadable/wrong doc → generic (flagged)

Saves each email to output/rejection_emails_job36/[APP_ID]_[NAME].txt
"""

import json, os, re, time
import anthropic

# ─── Config ───────────────────────────────────────────────────────────────────
CONFIG_PATH  = "C:/Users/Dell/.claude/config.json"
CV_DIR       = "c:/My First Agent/output/cv_texts_job36_rejected/"
OUTPUT_DIR   = "c:/My First Agent/output/rejection_emails_job36/"
SUMMARY_JSON = os.path.join(CV_DIR, "_summary.json")
MODEL        = "claude-haiku-4-5-20251001"

# Unreadable / wrong document — send generic but flag
GENERIC_FLAG_IDS = {
    1485: "CV was a blank CamScanner scan — no readable content",
    1869: "File uploaded was an internal Taleemabad values scorecard, not a candidate CV — possible data issue, flag to HR",
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── API key ──────────────────────────────────────────────────────────────────
with open(CONFIG_PATH) as f:
    _cfg = json.load(f)
API_KEY = _cfg["primaryApiKey"]
client = anthropic.Anthropic(api_key=API_KEY)

# ─── JD summary (for prompt context) ─────────────────────────────────────────
JD_SUMMARY = """
POSITION: Field Coordinator, Research & Impact Studies
TEAM: Impact & Policy, Taleemabad
LOCATION: Islamabad/Rawalpindi (regular field visits to government schools, occasional provincial travel)
CONTRACT: 24 months, contractual/in-person

WHAT THE ROLE DOES:
• Primary coordination focal point between Taleemabad and external survey/evaluation firms
• Field governance & quality assurance: spot-checks, enumerator observation, sampling plan adherence
• Daily data quality monitoring: dashboards, completion rates, anomaly flagging
• Enumerator training oversight at baseline and endline
• Government & school coordination: district approvals, scheduling, access management
• Field operations tracking: coverage vs sampling targets, escalation, contingency plans
• Documentation & reporting: live trackers, risk logs, weekly structured updates
• Ethics & compliance: consent procedures, child protection, research ethics standards

MINIMUM REQUIREMENTS:
• 1–3 years of experience in field research, M&E, or education program implementation
• Experience managing third-party vendors or survey firms
• Ability to read and enforce a sampling plan
• Comfort pushing back when field standards slip
• Islamabad/Rawalpindi based (or willing to relocate)

WHAT TALEEMABAD IS:
Pakistani EdTech working at intersection of product, policy and public systems. AI coaching
system Rumi, learning platform reaching 140,000+ students across 600+ schools in 4 provinces.
Implementation partners: MoFEPT and Balochistan.
"""

# ─── Cat C — pre-screened candidates (specific rejection notes already exist) ──
CAT_C = [
    {"app_id":1450,"name":"Naveen Shariff","email":"naveenshariff73@gmail.com",
     "location":"Karachi","salary":"220000",
     "notes":"TCF intern with basic Kobo tools exposure — entry-level only. Very limited field coordination evidence; no enumerator management or survey firm oversight at any meaningful scale. Karachi-based — relocation to Islamabad required. Salary ask (PKR 220K) is disproportionate relative to experience level."},
    {"app_id":1453,"name":"Abid Hussain","email":"abidqaisrani5@gmail.com",
     "location":"Rawalpindi","salary":"60K-100K",
     "notes":"IT and product support background (L2 Support Specialist at Techvity, IT intern at CARE International). Less than 1 year of any development-sector work, all at intern or junior support level. No M&E experience, no enumerator management, no education sector field coordination. Does not meet the minimum 2–3 years relevant field coordination experience required for this role."},
    {"app_id":1454,"name":"Shahid Kamal","email":"shahid.kaamal@gmail.com",
     "location":"Islamabad","salary":"150000",
     "notes":"M&E Officer (Karishma Ali Foundation) and LUMS RA background shows field M&E experience, but the scale of operations is unclear and the role appears closer to NGO grant management than front-line field coordination. Insufficient evidence of managing large-scale enumerator teams, survey firm oversight, or data quality governance at the level this role requires."},
    {"app_id":1477,"name":"Sadia Siddique","email":"sadich61@gmail.com",
     "location":"Islamabad","salary":"150000",
     "notes":"HR and data analyst background — entirely desk-based. No field coordination, no M&E, no education sector experience. CV shows no evidence of enumerator management, survey work, or school-based data collection."},
    {"app_id":1489,"name":"Muhammad Qasi","email":"qasee.khundian@gmail.com",
     "location":"Gilgit","salary":"100000",
     "notes":"Small-scale KII (Key Informant Interview) researcher based in Gilgit-Baltistan. No field team management at any meaningful scale, no enumerator supervision, no education sector context. Does not meet minimum requirements for operational field coordination at the level this role demands."},
    {"app_id":1495,"name":"Shabbir Hussain","email":"shabbir.dani@gmail.com",
     "location":"Ghanche","salary":"90000",
     "notes":"PhD Sociology with community mobilization and public health research background. Field experience limited to social mobilization (AKRSP, 5 months) and academic research at university level. No education sector M&E, no enumerator management, no survey firm oversight. Gilgit-Baltistan based — relocation to Islamabad required. Profile better suited to public health or community development roles."},
    {"app_id":1528,"name":"Muhammad Afzaal","email":"m.afzal36@yahoo.com",
     "location":"Islamabad","salary":"130000",
     "notes":"Community mobilizer background (USAID community work). Kobo/ODK listed in skills section only, without any CV evidence of actual field deployment. No enumerator supervision, no education sector experience."},
    {"app_id":1545,"name":"PARIYAL FAZAL SHAH","email":"pariyalfazal@gmail.com",
     "location":"Islamabad","salary":"200000",
     "notes":"Only 2 years of experience as an M&R (Monitoring & Reporting) analyst — desk-based role focused on internal reporting, not operational field coordination. No evidence of enumerator management, survey firm oversight, or school-based data collection at scale. Does not meet the minimum experience bar for this role."},
    {"app_id":1556,"name":"Sana Mehboob","email":"sanamehboob42@gmail.com",
     "location":"Islamabad","salary":"80K minimum",
     "notes":"District M&E Officer at Balochistan Rural Support Programme (~20 months) in WASH and rural community development — not education sector M&E. No evidence of managing school-based field research, enumerator teams, or education data quality oversight. Social mobilizer and community trainer background does not translate to the operational field coordination this role requires."},
    {"app_id":1600,"name":"Adil Javed","email":"adiljaved371@gmail.com",
     "location":"Mardan","salary":"80000",
     "notes":"Tehsil Monitoring Officer at WHO (5 years) — health/polio campaign monitoring, not education sector M&E. No school-based field research experience, no enumerator team management, no survey firm oversight. KPK-based (Mardan) — relocation to Islamabad required. Construction project supervisor background indicates further mismatch."},
    {"app_id":1608,"name":"Afaq Ahmad","email":"afaqa4851@gmail.com",
     "location":"Islamabad","salary":"85000",
     "notes":"Entry-level social mobilizer and WWF field assistant with approximately 14 months total experience. No education sector M&E, no enumerator management, no survey firm oversight. BS Forestry background. Gilgit-Baltistan based — relocation to Islamabad required. Does not meet minimum experience requirements for this role."},
    {"app_id":1633,"name":"Midhat Fatima","email":"midhatfatima22@gmail.com",
     "location":"Islamabad","salary":"90000",
     "notes":"Public health surveyor with intern-level experience only. No education M&E, no field team management, no enumerator supervision experience. Entirely health-sector focused."},
    {"app_id":1639,"name":"Wajeeha rehber","email":"wajiha.rehberali@gmail.com",
     "location":"Islamabad","salary":"95000",
     "notes":"Sociology research background with 6-month field evaluation (US Embassy project) and ~14 months as research assistant. No evidence of managing large-scale enumerator teams, survey firm oversight, or school-based education data governance. Experience is primarily academic research and human rights advocacy, not operational field coordination at the scale this role requires."},
    {"app_id":1674,"name":"Amina Jabin","email":"aminajabin229@gmail.com",
     "location":"Rawalpindi","salary":"50000",
     "notes":"Entirely teaching background — Class Teacher, Subject Teacher, and Volunteer Teacher at primary and secondary schools (Chitral/Rawalpindi). MPhil in Education (NUML). No M&E experience, no field coordination, no data collection or research role. This role requires operational field research coordination, not teaching expertise. Chitral-based — relocation to Islamabad required."},
    {"app_id":1802,"name":"syeda farzana ali shah","email":"farzanaali77@hotmail.com",
     "location":"Islamabad","salary":"300000",
     "notes":"25+ years of experience in child protection, safeguarding, and gender programming — an entirely different domain from field research coordination. No M&E, no field data governance, no education sector research background. Expected salary PKR 300K is also over budget for this role."},
]

# ─── Cat A — no CV, real email → generic ──────────────────────────────────────
CAT_A = [
    {"app_id":1538,"name":"Shakila","email":"ambroali161@gmail.com","location":"Muzaffer abad","salary":"Nil"},
    {"app_id":1547,"name":"Anila","email":"aniladad786@gmail.com","location":"Gilgit","salary":"100000"},
    {"app_id":1593,"name":"Zainab","email":"zainabsajjad122@gmail.com","location":"Peshawar","salary":"150000"},
    {"app_id":1653,"name":"Mahnoor","email":"mahnoor.iqbal0009@gmail.com","location":"Peshawar","salary":"105000"},
    {"app_id":1669,"name":"Zarghuna","email":"zarghuna.rahman06@gmail.com","location":"Islamabad","salary":"100000"},
    {"app_id":1837,"name":"Hunza","email":"hunzausman66@gmail.com","location":"Mirpur Khas","salary":"90000"},
    {"app_id":1955,"name":"ADNAN","email":"adnanaliaup2018@gmail.com","location":"Peshawar","salary":"60000"},
    {"app_id":1956,"name":"Amna","email":"amna12arshad@gmail.com","location":"Lahore","salary":"70000"},
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def first_name(full_name):
    """Extract a usable first name — title-case the first token."""
    parts = full_name.strip().split()
    if not parts:
        return "there"
    fn = parts[0].title()
    # Handle all-caps names like "ADNAN", "PARIYAL"
    return fn

def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)

def read_cv_text(app_id, name):
    """Read the extracted CV text file for a Cat B candidate."""
    fname = f"{app_id}_{safe_filename(name)}.txt"
    path = os.path.join(CV_DIR, fname)
    if not os.path.exists(path):
        # Try a partial match
        for f in os.listdir(CV_DIR):
            if f.startswith(f"{app_id}_"):
                path = os.path.join(CV_DIR, f)
                break
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    # Skip the metadata header (before the === line)
    if "=" * 10 in content:
        idx = content.index("=" * 10)
        return content[idx + content[idx:].index("\n") + 1:].strip()
    return content

def call_api(prompt, max_tokens=1200):
    """Call Claude API with retry on rate limit."""
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.content[0].text
        except anthropic.RateLimitError:
            print(f"  Rate limit hit, waiting 30s (attempt {attempt+1})...")
            time.sleep(30)
        except Exception as e:
            print(f"  API error: {e}")
            time.sleep(5)
    return None

def generate_email_cat_b(cand, cv_text):
    """Generate a warm, specific rejection email from CV text."""
    is_generic_flag = cand["app_id"] in GENERIC_FLAG_IDS

    if is_generic_flag or not cv_text or len(cv_text.strip()) < 100:
        return None  # Signal to use generic template

    prompt = f"""You are Coco, the AI recruitment assistant at Taleemabad, a Pakistani EdTech organisation.

Write a warm, empathetic, and honest rejection email for a candidate who applied for the role below.
The email must be at minimum 500 words. It should feel genuinely human — not a form letter.

ROLE: Field Coordinator, Research & Impact Studies

JD REQUIREMENTS:
{JD_SUMMARY}

CANDIDATE DETAILS:
Name: {cand['name']}
Location: {cand.get('location') or 'Not mentioned'}
Current role: {cand.get('current_role') or 'Not mentioned'}
Current company: {cand.get('current_company') or 'Not mentioned'}
Expected salary: PKR {cand.get('salary') or 'Not mentioned'}

CV TEXT (read this carefully — base the email on what you actually see here):
---
{cv_text[:4000]}
---

INSTRUCTIONS:
1. Address the candidate by first name: {first_name(cand['name'])}
2. Open warmly — acknowledge the effort of applying and that you genuinely reviewed their profile
3. Be specific: mention 1–2 actual things from their CV (role title, organisation, type of work)
4. Explain honestly, kindly, and specifically WHY they didn't progress — be direct about the gap(s) without being harsh
   Common gaps for this role: not enough operational field coordination experience (vs desk/academic/community work),
   no enumerator team management, no survey firm oversight, health sector only, teaching background only,
   below the 1–3 year relevant experience bar, relocation required but logistics unclear, etc.
5. Do NOT make up skills or experience they don't have. Only reference what is in the CV text.
6. Affirm what was genuinely good about their application (if anything honest to say)
7. Encourage them to keep applying to Taleemabad for roles better suited to their strengths
8. End warmly — no clichés like "we wish you all the best in your future endeavours"
9. Sign off as:
   Warm regards,
   Team Taleemabad

   Coco — AI Assistant | Taleemabad Talent Acquisition

FORMAT: Plain text email. Start with: Subject: Re: Your Application for Field Coordinator, Research & Impact Studies

Do NOT include any meta-commentary, just write the email.
"""
    return call_api(prompt, max_tokens=1400)


def generate_email_cat_c(cand):
    """Generate a warm email from existing screening notes."""
    prompt = f"""You are Coco, the AI recruitment assistant at Taleemabad, a Pakistani EdTech organisation.

Write a warm, empathetic, and honest rejection email for a candidate who applied for the role below.
The email must be at minimum 500 words. It should feel genuinely human — not a form letter.

ROLE: Field Coordinator, Research & Impact Studies

JD REQUIREMENTS:
{JD_SUMMARY}

CANDIDATE DETAILS:
Name: {cand['name']}
Location: {cand.get('location') or 'Not mentioned'}
Expected salary: PKR {cand.get('salary') or 'Not mentioned'}

REVIEWER NOTES (honest assessment from the person who read this CV — use this to ground the email):
{cand['notes']}

INSTRUCTIONS:
1. Address the candidate by first name: {first_name(cand['name'])}
2. Open warmly — acknowledge the effort of applying and that you genuinely reviewed their profile
3. Be specific: reference the actual background/experience in the notes (organisation names, type of work)
4. Explain honestly and kindly the gap(s) — translate the reviewer notes into warm, direct human language
5. Affirm anything genuinely strong from the notes
6. Encourage them to keep an eye on Taleemabad openings suited to their strengths
7. End warmly — avoid hollow phrases like "we wish you all the best in your future endeavours"
8. Sign off:
   Warm regards,
   Team Taleemabad

   Coco — AI Assistant | Taleemabad Talent Acquisition

FORMAT: Plain text email. Start with: Subject: Re: Your Application for Field Coordinator, Research & Impact Studies

Do NOT include any meta-commentary. Just write the email.
"""
    return call_api(prompt, max_tokens=1400)


def generate_generic_email(name, flag_note=None):
    """Plain template for Cat A (no CV) and special flagged cases."""
    fn = first_name(name)
    flag_header = ""
    if flag_note:
        flag_header = f"\n*** GENERIC — FLAG: {flag_note} ***\n"

    return f"""Subject: Re: Your Application for Field Coordinator, Research & Impact Studies
{flag_header}
Hi {fn},

Thank you for your interest in the Field Coordinator, Research & Impact Studies position at Taleemabad and for taking the time to apply.

We received a large number of applications for this role, and our team carefully reviewed each submission. After completing our assessment process, we are not able to move your application forward at this stage.

Unfortunately, we were unable to access the full details of your application — either no CV was attached or the file could not be reviewed in our system. As a result, we were not able to conduct a thorough assessment of your profile against the requirements for this role.

The Field Coordinator role requires specific experience in field research coordination, M&E, and education sector implementation, and without being able to review your full profile, we could not make a fair evaluation.

We genuinely want to ensure every applicant is treated respectfully. If you believe your CV was submitted correctly and would like to be considered for future opportunities that match your profile, we encourage you to apply again when a relevant position opens up. You can follow Taleemabad on LinkedIn and our website for upcoming announcements.

We are a small but ambitious team working on one of the most important problems in Pakistan — children's access to quality education. Applications from people who share that commitment always mean a lot to us, even when we are not able to move forward right now.

We wish you the very best in your career journey and hope our paths cross again.

Warm regards,
Team Taleemabad

Coco — AI Assistant | Taleemabad Talent Acquisition
"""


def save_email(app_id, name, content, category, flag=False):
    fname = f"{app_id}_{safe_filename(name)}.txt"
    path = os.path.join(OUTPUT_DIR, fname)
    flag_marker = "*** PILOT — DO NOT SEND YET ***\n"
    cat_marker = f"[CATEGORY: {category}]"
    if flag:
        cat_marker += " [FLAG: GENERIC — SEE NOTE ABOVE]"
    header = f"{flag_marker}{cat_marker}\n{'='*80}\n\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + content)
    return path


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    # Load Cat B summary
    with open(SUMMARY_JSON, encoding="utf-8") as f:
        cat_b_list = json.load(f)

    results = {"ok": [], "generic_flag": [], "api_fail": []}
    total = len(cat_b_list) + len(CAT_C) + len(CAT_A)
    done = 0

    print(f"\n{'='*60}")
    print(f"Job 36 Rejection Emails Generator")
    print(f"Cat B: {len(cat_b_list)} | Cat C: {len(CAT_C)} | Cat A: {len(CAT_A)}")
    print(f"Total: {total}")
    print(f"{'='*60}\n")

    # ── Cat B ──────────────────────────────────────────────────────────────────
    print(f"\n--- CAT B ({len(cat_b_list)} candidates with extracted CVs) ---")
    for i, cand in enumerate(cat_b_list, 1):
        app_id = cand["app_id"]
        name   = cand["name"]
        done += 1
        print(f"[{done}/{total}] Cat B: {name} (app {app_id})...", end=" ", flush=True)

        # Special flag cases
        if app_id in GENERIC_FLAG_IDS:
            note = GENERIC_FLAG_IDS[app_id]
            content = generate_generic_email(name, flag_note=note)
            save_email(app_id, name, content, "B_DATA_ISSUE", flag=True)
            results["generic_flag"].append({"app_id": app_id, "name": name, "note": note})
            print(f"GENERIC FLAG")
            continue

        cv_text = read_cv_text(app_id, name)
        if not cv_text or len(cv_text.strip()) < 80:
            content = generate_generic_email(name, flag_note="CV unreadable or empty")
            save_email(app_id, name, content, "B_UNREADABLE", flag=True)
            results["generic_flag"].append({"app_id": app_id, "name": name, "note": "CV unreadable"})
            print(f"GENERIC FLAG (unreadable)")
            continue

        email_text = generate_email_cat_b(cand, cv_text)
        if email_text:
            save_email(app_id, name, email_text, "B")
            results["ok"].append({"app_id": app_id, "name": name, "cat": "B"})
            print(f"OK ({len(email_text)} chars)")
        else:
            # Fallback to generic
            content = generate_generic_email(name, flag_note="API generation failed — review manually")
            save_email(app_id, name, content, "B_FAIL", flag=True)
            results["api_fail"].append({"app_id": app_id, "name": name})
            print(f"FAIL → generic fallback")

        time.sleep(0.3)  # Gentle rate limit buffer

    # ── Cat C ──────────────────────────────────────────────────────────────────
    print(f"\n--- CAT C ({len(CAT_C)} pre-screened candidates) ---")
    for cand in CAT_C:
        app_id = cand["app_id"]
        name   = cand["name"]
        done += 1
        print(f"[{done}/{total}] Cat C: {name} (app {app_id})...", end=" ", flush=True)

        email_text = generate_email_cat_c(cand)
        if email_text:
            save_email(app_id, name, email_text, "C")
            results["ok"].append({"app_id": app_id, "name": name, "cat": "C"})
            print(f"OK ({len(email_text)} chars)")
        else:
            content = generate_generic_email(name, flag_note="API generation failed — review manually")
            save_email(app_id, name, content, "C_FAIL", flag=True)
            results["api_fail"].append({"app_id": app_id, "name": name})
            print(f"FAIL → generic fallback")

        time.sleep(0.3)

    # ── Cat A ──────────────────────────────────────────────────────────────────
    print(f"\n--- CAT A ({len(CAT_A)} no-CV candidates with real emails) ---")
    for cand in CAT_A:
        app_id = cand["app_id"]
        name   = cand["name"]
        done += 1
        print(f"[{done}/{total}] Cat A: {name} (app {app_id})...", end=" ", flush=True)

        content = generate_generic_email(name, flag_note="No CV submitted — generic email")
        save_email(app_id, name, content, "A_GENERIC", flag=True)
        results["generic_flag"].append({"app_id": app_id, "name": name, "note": "No CV"})
        print("GENERIC")

    # ── Summary ────────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"DONE")
    print(f"  Specific emails generated: {len(results['ok'])}")
    print(f"  Generic/flagged:           {len(results['generic_flag'])}")
    print(f"  API failures:              {len(results['api_fail'])}")
    print(f"  Output: {OUTPUT_DIR}")

    # Save run log
    log = {
        "total": total, "ok": len(results["ok"]),
        "generic_flag": results["generic_flag"],
        "api_fail": results["api_fail"],
    }
    with open(os.path.join(OUTPUT_DIR, "_generation_log.json"), "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    print(f"  Log saved to {OUTPUT_DIR}_generation_log.json")
    print(f"{'='*60}\n")

    if results["api_fail"]:
        print("*** WARNING: The following need manual review (API failed):")
        for x in results["api_fail"]:
            print(f"  App {x['app_id']}: {x['name']}")


if __name__ == "__main__":
    main()
