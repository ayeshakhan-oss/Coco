"""
Generate CV-stage rejection emails for Job 36 new batch (15 candidates with readable CVs).
4 LinkedIn temp accounts skipped — no real email address.

Rules:
- Minimum 500 words per email
- "We" voice throughout, never "I"
- They/them pronouns for all candidates
- No em dashes anywhere
- Specific to each candidate's actual CV content
- Honest about the gap, warm in tone
- No hollow closings
- Sign-off: Warm regards, / People and Culture Team / Taleemabad /
  hiring@taleemabad.com | www.taleemabad.com / Sent on behalf of Talent Acquisition Team by Coco
- Never mention Coco or AI in the email body
"""

import os, json, re, time
import anthropic

CONFIG_PATH  = "C:/Users/Dell/.claude/config.json"
CV_DIR       = "c:/Agent Coco/output/cv_texts_job36_new_batch/"
OUTPUT_DIR   = "c:/Agent Coco/output/rejection_emails_job36_new_batch/"

MODEL = "claude-haiku-4-5-20251001"

with open(CONFIG_PATH) as f:
    _cfg = json.load(f)
API_KEY = _cfg["primaryApiKey"]
client = anthropic.Anthropic(api_key=API_KEY)

os.makedirs(OUTPUT_DIR, exist_ok=True)

JD_SUMMARY = """
POSITION: Field Coordinator, Research & Impact Studies
TEAM: Impact & Policy, Taleemabad
LOCATION: Islamabad/Rawalpindi (regular field visits to government schools, occasional provincial travel)
CONTRACT: 24 months, contractual/in-person

WHAT THE ROLE DOES:
- Primary coordination focal point between Taleemabad and external survey/evaluation firms
- Field governance and quality assurance: spot-checks, enumerator observation, sampling plan adherence
- Daily data quality monitoring: dashboards, completion rates, anomaly flagging
- Enumerator training oversight at baseline and endline
- Government and school coordination: district approvals, scheduling, access management
- Field operations tracking: coverage vs sampling targets, escalation, contingency plans
- Documentation and reporting: live trackers, risk logs, weekly structured updates
- Ethics and compliance: consent procedures, child protection, research ethics standards

MINIMUM REQUIREMENTS:
- 1 to 3 years of experience in field research, M&E, or education program implementation
- Experience managing third-party vendors or survey firms
- Ability to read and enforce a sampling plan
- Comfort pushing back when field standards slip
- Islamabad/Rawalpindi based (or willing to relocate)
"""

# 15 candidates with readable CVs — 4 LinkedIn temp accounts excluded
CANDIDATES = [
    {"app_id": 2124, "name": "Hafiza Iqra Bashir",       "email": "hafizaiqrabashir@hotmail.com",          "location": "Islamabad"},
    {"app_id": 2122, "name": "Ali Haider Baloch",         "email": "alihaiderbaloch1512@gmail.com",          "location": "Islamabad"},
    {"app_id": 2119, "name": "Hassan Tahir",              "email": "hasstahir395@gmail.com",                 "location": "Islamabad"},
    {"app_id": 2108, "name": "Hiba Ahmed",                "email": "hibaahmed7604@gmail.com",                "location": "Rawalpindi"},
    {"app_id": 2106, "name": "Faris Meher Ali",           "email": "farismeherali@gmail.com",                "location": "Lahore"},
    {"app_id": 2105, "name": "Hamza Khan",                "email": "hamzasikhan@gmail.com",                  "location": "Islamabad"},
    {"app_id": 2103, "name": "Attiqua Urfa",              "email": "Attiqua.urfaabdullah786@gmail.com",      "location": "Lahore"},
    {"app_id": 2090, "name": "Mehreen Tariq",             "email": "26020521@lums.edu.pk",                   "location": "Lahore"},
    {"app_id": 2079, "name": "Umme Farwa",                "email": "ummef127@gmail.com",                     "location": "Islamabad"},
    {"app_id": 2061, "name": "Easha Imtiaz",              "email": "eashaimtiaz4@gmail.com",                 "location": "Lahore"},
    {"app_id": 2053, "name": "Hamza Sattar",              "email": "sattarh630@gmail.com",                   "location": "Attock"},
    {"app_id": 2050, "name": "Anosha Umer",               "email": "anoshaumer19@gmail.com",                 "location": "Lahore"},
    {"app_id": 2029, "name": "Syed Muhammad Ali Abbas",   "email": "26100287@lums.edu.pk",                   "location": "Lahore"},
    {"app_id": 2024, "name": "Mohid Naveed Sufi",         "email": "mohidsufi@gmail.com",                    "location": "Peshawar"},
    {"app_id": 2022, "name": "Maheen Sughra",             "email": "sughra.maheenn@gmail.com",               "location": "Islamabad"},
]


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
    prompt = f"""You are a member of Taleemabad's People and Culture team writing a rejection email to a candidate who applied for a role.

STRICT RULES — follow every one of these without exception:
1. Minimum 500 words. Do not go below this under any circumstances.
2. Use "we" voice throughout. Never use "I".
3. Use they/them pronouns for the candidate. Never use he/she/his/her.
4. No em dashes anywhere. Use commas, colons, or periods instead.
5. Be specific: reference actual content from the candidate's CV (real role titles, real organisations, real type of work).
6. Never make up or assume anything not in the CV.
7. Explain the gap honestly and clearly. Be direct but warm. Not harsh, not vague.
8. Acknowledge what is genuinely strong in their profile.
9. Suggest a direction forward if there is an honest one to give.
10. Do not use hollow phrases like "we wish you all the best in your future endeavours" or "keep applying."
11. Do not refer to this email as a "letter."
12. Never mention AI, Coco, or any automated system.
13. End with exactly this sign-off (preserve formatting):

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
Location: {cand['location']}

CV TEXT (read carefully, base the email only on what is actually here):
---
{cv_text[:4000]}
---

FORMAT: Plain text. Start with:
Subject: Your Application for Field Coordinator, Research & Impact Studies

Then write the email body starting with: Hi {first_name(cand['name'])},

Do not include any meta-commentary. Write only the email.
"""
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=1500,
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
    print(f"\n{'='*60}")
    print(f"Job 36 New Batch Rejection Emails — {len(CANDIDATES)} candidates")
    print(f"{'='*60}\n")

    results = {"ok": [], "fail": []}

    for i, cand in enumerate(CANDIDATES, 1):
        app_id = cand["app_id"]
        name   = cand["name"]
        print(f"[{i}/{len(CANDIDATES)}] {name} (app {app_id})...", end=" ", flush=True)

        cv_text = read_cv(app_id, name)
        if not cv_text or len(cv_text.strip()) < 80:
            print("SKIP — CV unreadable")
            results["fail"].append({"app_id": app_id, "name": name, "reason": "CV unreadable"})
            continue

        email_text = generate_email(cand, cv_text)
        if email_text:
            fname = f"{OUTPUT_DIR}/{app_id}_{safe_filename(name)}.txt"
            with open(fname, "w", encoding="utf-8") as f:
                f.write(f"*** PILOT — DO NOT SEND YET ***\n")
                f.write(f"TO: {cand['email']}\n")
                f.write(f"CC: hiring@taleemabad.com | ayesha.khan@taleemabad.com\n")
                f.write("=" * 80 + "\n\n")
                f.write(email_text)
            results["ok"].append({"app_id": app_id, "name": name})
            print(f"OK ({len(email_text)} chars)")
        else:
            results["fail"].append({"app_id": app_id, "name": name, "reason": "API failed"})
            print("FAIL")

        time.sleep(0.3)

    print(f"\n{'='*60}")
    print(f"DONE")
    print(f"  Generated:  {len(results['ok'])}")
    print(f"  Failed:     {len(results['fail'])}")
    print(f"  Output:     {OUTPUT_DIR}")
    print(f"{'='*60}\n")

    with open(f"{OUTPUT_DIR}/_generation_log.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
