"""
Generate personalised CV-stage rejection emails for all Job 35 rejected candidates.
Job 35: Junior Research Associate, Impact & Policy

Rules:
- Minimum 800 words per email
- "We" voice throughout, never "I"
- They/them pronouns for all candidates
- No em dashes anywhere
- Specific to each candidate's actual CV content
- Honest about the gap, warm in tone
- No hollow closings
- Sign-off: Warm regards, / People and Culture Team / Taleemabad
- Never mention Coco or AI in the email body

Run extract_cv_text_job35_all_rejected.py first.
"""

import os, json, re, time
import anthropic

CONFIG_PATH = "C:/Users/Dell/.claude/config.json"
CV_DIR      = "c:/Agent Coco/output/cv_texts_job35_rejected/"
OUTPUT_DIR  = "c:/Agent Coco/output/rejection_emails_job35/"

MODEL = "claude-haiku-4-5-20251001"

with open(CONFIG_PATH) as f:
    _cfg = json.load(f)
API_KEY = _cfg["primaryApiKey"]
client = anthropic.Anthropic(api_key=API_KEY)

os.makedirs(OUTPUT_DIR, exist_ok=True)

JD_SUMMARY = """
POSITION: Junior Research Associate, Impact & Policy
TEAM: Impact & Policy, Taleemabad
LOCATION: Islamabad (in-person)
CONTRACT: Full-time, permanent

WHAT THE ROLE DOES:
- Quantitative and qualitative research in support of Taleemabad's education impact work
- Data collection, cleaning, and analysis of school-level education outcomes
- Supporting the design of impact evaluations, surveys, and field monitoring tools
- Generating evidence for decision-makers in Pakistan's public education system
- Literature reviews, policy briefs, and evidence synthesis for internal and external audiences
- Field data collection at government schools and coordination with school teams

MINIMUM REQUIREMENTS:
- Bachelor's or Master's in economics, development studies, statistics, social sciences, or a related field
- 1 to 2 years of experience in research, M&E, or data analysis in education, development, or a related domain
- Demonstrated quantitative skills: SPSS, Stata, R, or Python for data analysis
- Familiarity with impact evaluation methods (regression, difference-in-differences, RCT design is a plus)
- Experience designing or implementing field surveys, ideally in an education or development context
- Strong written communication for reporting to non-specialist audiences
"""


def first_name(full_name):
    return full_name.strip().split()[0].title()


def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


def read_cv(app_id, name):
    fname = f"{app_id}_{safe_filename(name)}.txt"
    path = os.path.join(CV_DIR, fname)
    if not os.path.exists(path):
        for f in os.listdir(CV_DIR):
            if f.startswith(f"{app_id}_"):
                path = os.path.join(CV_DIR, f)
                break
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if "=" * 10 in content:
        idx = content.index("=" * 10)
        return content[idx + content[idx:].index("\n") + 1:].strip()
    return content


def generate_email(cand, cv_text):
    prompt = f"""You are a member of Taleemabad's People and Culture team writing a personalised rejection email to a candidate who applied for a role.

STRICT RULES — follow every one of these without exception:
1. MINIMUM 800 WORDS. Do not go below this under any circumstances. This is the most important rule.
2. Use "we" voice throughout. Never use "I".
3. Use they/them pronouns for the candidate. Never use he/she/his/her.
4. No em dashes anywhere. Use commas, colons, or periods instead.
5. Be specific: reference actual content from the candidate's CV including real role titles, real organisations, real types of work, and real skills or tools mentioned.
6. Never make up or assume anything not in the CV.
7. Structure the email in 3 clear sections:
   - What we noticed in your application (acknowledge genuine strengths with specifics)
   - Where the fit did not come together (explain the gap honestly, clearly, without being harsh)
   - What we think could serve you well (concrete, honest forward direction — not generic advice)
8. Acknowledge what is genuinely strong in their profile before explaining the gap.
9. Suggest a specific, honest direction forward.
10. Do not use hollow phrases like "we wish you all the best in your future endeavours" or "keep applying."
11. Do not refer to this email as a "letter."
12. Never mention AI, Coco, or any automated system.
13. You may optionally add a P.S. line at the end (1-2 sentences) that picks up one specific detail from their CV and reflects on it warmly. This is not required but adds humanity if there is something worth noting.
14. End with exactly this sign-off (preserve formatting, add after the P.S. if included):

Warm regards,
People and Culture Team
Taleemabad
hiring@taleemabad.com | www.taleemabad.com

Sent on behalf of Talent Acquisition Team by Coco

ROLE BEING HIRED FOR:
{JD_SUMMARY}

CANDIDATE:
Name: {cand['name']}
First name to use in greeting: {first_name(cand['name'])}
Location: {cand.get('location', 'Not mentioned')}

CV TEXT (read carefully, base the email only on what is actually here):
---
{cv_text[:4500]}
---

FORMAT: Plain text. Start with:
Subject: Your Application for Junior Research Associate, Impact & Policy

Then write the email body starting with: Dear {first_name(cand['name'])},

Do not include any meta-commentary. Write only the email.
"""
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.content[0].text
        except anthropic.RateLimitError:
            print(f"  Rate limit, waiting 30s (attempt {attempt+1})...")
            time.sleep(30)
        except Exception as e:
            print(f"  API error: {e}")
            time.sleep(5)
    return None


def main():
    # Load candidate list from summary JSON
    summary_path = os.path.join(CV_DIR, "_summary.json")
    if not os.path.exists(summary_path):
        print("ERROR: Run extract_cv_text_job35_all_rejected.py first.")
        return

    with open(summary_path, encoding="utf-8") as f:
        candidates = json.load(f)

    # Only process candidates with readable CVs
    readable = [c for c in candidates if c["readable"]]
    unreadable = [c for c in candidates if not c["readable"]]

    print(f"\n{'='*60}")
    print(f"Job 35 Rejection Email Generation")
    print(f"  Total candidates: {len(candidates)}")
    print(f"  Readable CVs:     {len(readable)}")
    print(f"  Unreadable/skip:  {len(unreadable)}")
    print(f"{'='*60}\n")

    results = {"ok": [], "fail": [], "skipped": []}

    for u in unreadable:
        results["skipped"].append({"app_id": u["app_id"], "name": u["name"], "reason": "CV unreadable"})

    for i, cand in enumerate(readable, 1):
        app_id = cand["app_id"]
        name   = cand["name"]
        email  = cand["email"]

        # Skip if already generated
        out_path = f"{OUTPUT_DIR}/{app_id}_{safe_filename(name)}.txt"
        if os.path.exists(out_path):
            print(f"[{i}/{len(readable)}] {name} — SKIP (already generated)")
            results["ok"].append({"app_id": app_id, "name": name})
            continue

        print(f"[{i}/{len(readable)}] {name} (app {app_id})...", end=" ", flush=True)

        cv_text = read_cv(app_id, name)
        if not cv_text or len(cv_text.strip()) < 80:
            print("SKIP — CV too short")
            results["fail"].append({"app_id": app_id, "name": name, "reason": "CV too short"})
            continue

        email_text = generate_email(cand, cv_text)
        if email_text:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(f"*** PILOT — DO NOT SEND YET ***\n")
                f.write(f"TO: {email}\n")
                f.write(f"CC: hiring@taleemabad.com | ayesha.khan@taleemabad.com\n")
                f.write("=" * 80 + "\n\n")
                f.write(email_text)
            results["ok"].append({"app_id": app_id, "name": name})
            wc = len(email_text.split())
            print(f"OK ({wc} words)")
        else:
            results["fail"].append({"app_id": app_id, "name": name, "reason": "API failed"})
            print("FAIL")

        time.sleep(0.4)

    print(f"\n{'='*60}")
    print(f"DONE")
    print(f"  Generated:  {len(results['ok'])}")
    print(f"  Failed:     {len(results['fail'])}")
    print(f"  Skipped:    {len(results['skipped'])}")
    print(f"  Output:     {OUTPUT_DIR}")
    print(f"{'='*60}\n")

    with open(f"{OUTPUT_DIR}/_generation_log.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
