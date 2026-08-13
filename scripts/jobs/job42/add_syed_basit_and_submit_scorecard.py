# -*- coding: utf-8 -*-
"""Create Syed Basit Hussain's Markaz record (Job 42 - Senior Manager Growth) and submit his
values scorecard (PASS 5+/1+-/0-). Approved by Ayesha 2026-08-13 ("upload his profile ... and
then submit his scorecard").

He was values-invited live on 2026-08-07 with NO Markaz application record (one of the 5
missing sourced candidates). This script:
  1. Inserts the candidate (profile fields from his CV; resume PDF base64 from Downloads)
     - guard: abort if email already exists
  2. Inserts the application on job 42, status 'shortlisted' (mirrors other values-passers)
     - guard: abort if candidate already has an app on job 42
  3. Fills the values scorecard via guarded UPDATE (values_scorecard IS NULL, row-count assert)
Uses Neon HTTPS SQL API (port 5432 blocked on this network)."""
import os, json, base64
import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

JOB_ID = 42
EMAIL = "syed.basit89@gmail.com"
CV_PATH = r"C:\Users\Dell\Downloads\CV of SYED BASIT HUSSAIN 2026.pdf"


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=120)
    r.raise_for_status()
    return r.json()["rows"]


scorecard = {
    "date": "Aug 13, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "Coco (AI P&C Assistant)",
    "candidateName": "Syed Basit Hussain",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Asked for an almost-quit moment, he reframed honestly - 'backing out is not an option. I always find a way' - and gave sustained-persistence evidence instead: a year-long GIZ SDG-financing advisory convincing government and private sector to record SDG implementation (built a logging system; ~100 women entrepreneurs trained in Multan), and three years at LUMS raising against escalating targets (200M -> 300M -> 500M PKR, 'which I achieved') while donors pushed back with 'why don't we fund 100 school-going children' instead of one LUMS student at 1.6-1.8M per semester.",
            "curveBall": "The ugly-problem-nobody-owned probe landed his strongest story: the Islamabad/Peshawar fundraising region was not in his LUMS mandate - he proposed it himself, his supervisor was skeptical ('I don't think Islamabad can give this kind of funding'), and he built the northern donor network from zero prospect meetings to ~60 small- and large-ticket donors by the time he left.",
            "microCase": "Describes his Saturday Margalla hike as a non-negotiable ritual - 'If I skip that, I feel like I'm an addict' - small, but consistent with a persistence temperament. Rating +: no literal almost-quit moment, but the curve-ball answer is a textbook self-initiated ownership of an unowned hard problem, with concrete stakes and outcome."
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": "Covered his stewardship team's dropped follow-up with a major donor CEO (~100M rupee commitment): discovered the team had made no contact for a month, and told his director 'there was a little mishap FROM ME' rather than naming the team. Then personally repaired it - apologized to the CEO, sent a box of chocolates, and had him speaking at the Leaders at LUMS session within a couple of weeks. Explicitly chose not to scold or scream at the team; the team later took him to a restaurant to thank him.",
            "curveBall": "Quiet-voices question: Asma, a data associate of five years with outstanding work who never asked for promotion while juniors were promoted around her. He was not her boss - the director challenged him on exactly that ('are you her boss?') - but he pushed a special case and she was promoted within two months. 'That's my proud feeling.'",
            "microCase": "On handing donor stewardship to his junior team: framed it as trust and shared responsibility ('you have to go along with them'), not delegation of grunt work. Rating +: both probes answered with real, named, first-ask incidents - absorbing blame publicly and advocating upward for someone with no voice."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+/-",
            "deepDive": "Recent upskilling is real but the thinnest evidence of his six values: 'recently got this AI training,' participation in a mass online AI hackathon (with a Guinness World Record certificate for attendance numbers), and a described practice of using AI as a brainstorming partner for his proposal/report/script writing rather than copy-paste. The training itself is unnamed in-call and the application described stays at the workflow-preference level.",
            "curveBall": "Not separately tested - single structured question for this value this call (interview-design note).",
            "microCase": "The donkey-cart-to-cars analogy ('if you are not in that ship, you will be left behind') shows a genuine adapt-or-obsolesce mindset; he also engaged thoughtfully with Taleemabad's own AI transition unprompted. Rating +/-: evidence present and honest but light on specifics for a plus - no named course in-call, no before/after outcome, and a mass-participation hackathon is a low-signal credential."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": "At GIZ, publicly challenged the Secretary of the Planning & Development Board in a meeting about national SDG claims: 'Sir, with all due respect - where are the SDGs?... You've done it on the white pages; it doesn't happen on the ground level,' backing it with field evidence (brick kilns and rice-husk burning still operating in Multan/D.G. Khan). He paid a real price - 'after that, I didn't get a meeting with him... not to mess with the Secretary' - and still stands by it: 'But it was true.'",
            "curveBall": "The receiving-feedback side was not probed in this interview - not directly evident, and not held against him (fairness rule).",
            "microCase": "He volunteered the consequence of the confrontation himself rather than sanitizing the story - reads as honest, not performative. Rating +: a high-stakes, upward, evidence-backed hard conversation with a named cost he owned."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "At his consulting firm, proposal winners also got the implementation work and the extra money attached to it. His director assigned him a UNICEF WASH-sector proposal (M&E component - his own specialty); he judged that an environment-specialist colleague 'would do more justice to it,' handed it over, and offered her the M&E write-up support instead - forgoing the monetary benefit. Says this happened multiple times.",
            "curveBall": "Not separately tested - single structured question for this value this call (interview-design note).",
            "microCase": "No defensiveness in the handover framing - 'why don't you work on it, because you're the expert' - release framed as the project's gain, not his loss. Rating +: one concrete, first-ask instance with genuine personal cost (money and credit) attached."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Answered the hypothetical silly-ritual question with rituals he has actually run: weekly boardroom sketch sessions (handed out papers; people drew cartoons and characters over several weeks), later evolved into a Friday 4-5pm happy hour with antakshari and hangman.",
            "curveBall": "The question's 'nothing traditional' constraint arrived garbled in the transcript, but his sketch-session answer is genuinely outside-the-box regardless - no penalty, no bonus needed (fairness rule).",
            "microCase": "Warm rapport throughout - the hiking exchange at the open, laughing at the chocolate-apology story while honestly owning 'I was losing my mind' in the moment. Rating +: lived practice, not invention on the spot; specific formats, iterated over weeks."
        }
    ],
    "finalComments": "PASS - 5(+) / 1(+/-) / 0(-). Zero minuses and one plus-minus (Continuously Improve Our Craft, where evidence was real but thin). Evaluated solely on his own transcript evidence against the value and rating definitions. GWC: Gets it - PROBE (mission understanding never really tested; he saved 'mostly technical' questions for the next round); Wants it - PROBE, untested not negative (why-Taleemabad neither asked nor volunteered; currently freelancing on UNICEF/World Bank/UNDP proposals, so the pull toward a full-time in-house role needs one direct question at debrief); Capacity - GOOD (donor and government partnership hunting: GIZ public-private SDG financing, LUMS institutional fundraising against 200-500M targets, multilateral proposal work, building a partnership region from scratch, managing a junior team). Proceed: CONDITIONAL YES - values PASS; probe Gets-it and Wants-it at case-study debrief. TRANSCRIPT CAVEAT: heavy Urdu-English code-switching and Fathom garble in several passages (LUMS donor figures, silly-ritual question intro); fairness rule applied - nothing scored against him on a garbled passage. FLAGS: (1) self-reported fundraising figures (500M PKR target achieved, ~60 donors, one ~100M donor) are unverifiable from the transcript - plausible for a LUMS regional resource-development role, worth confirming at reference stage; (2) salary not discussed - uncollected; (3) record created retroactively by Coco on 2026-08-13: he was values-invited live on 2026-08-07 as a sourced candidate with no Markaz application at the time.",
    "proceedToRightSeat": "Yes"
}

# ---- Step 1: candidate insert (guard: email must not exist) ----
existing = q("SELECT id FROM candidates WHERE lower(email) = lower($1)", [EMAIL])
assert not existing, f"Guard failed: candidate already exists with email {EMAIL}: {existing} - ABORTING"

with open(CV_PATH, "rb") as f:
    resume_b64 = base64.b64encode(f.read()).decode("ascii")
print(f"CV read: {len(resume_b64)} base64 chars")

cand = q("""INSERT INTO candidates
        (first_name, last_name, email, phone, resume_data, resume_file_name, resume_mime_type,
         position, location, current_position, current_company, education, experience, source)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
        RETURNING id, first_name, last_name, email""",
        ["Syed Basit", "Hussain", EMAIL, "03294373193",
         resume_b64, "CV of SYED BASIT HUSSAIN 2026.pdf", "application/pdf",
         "Senior Manager Growth",
         "Islamabad, Pakistan",
         "Consultant/Proposal Writer (Freelance)",
         "Freelance (prev. LUMS - Partnerships Specialist)",
         "Master in Project Management, SZABIST Islamabad (2014-2015); BBA, COMSATS Islamabad (2010-2014)",
         "8+ years in business development, donor coordination, M&E and partnerships. Freelance consultant/proposal writer for UNICEF, World Bank, UNDP (Apr 2026-date); Partnerships Specialist, LUMS (Nov 2022-Apr 2026) - CSR fundraising, donor networking, Raiser's Edge CRM; Business Development/Project Coordinator, Associates in Development (2020-2022) - WB national energy survey, BMGF/Kantar nutrition and financial-inclusion surveys, NDRMF DRM; Technical Advisor Private Sector Engagement, GIZ (2018-2019) - public-private SDG financing; Senior BD Executive, AiD (2016-2018); Jr. Program Associate, ADMC (2014-2016).",
         "manual"])
CAND_ID = cand[0]["id"]
print("Candidate created:", cand[0])

# ---- Step 2: application insert (guard: no existing app on job 42) ----
dup = q("SELECT id FROM applications WHERE candidate_id = $1 AND job_id = $2", [CAND_ID, JOB_ID])
assert not dup, f"Guard failed: candidate {CAND_ID} already has application(s) on job {JOB_ID}: {dup} - ABORTING"

app = q("""INSERT INTO applications (candidate_id, job_id, status, stage, notes)
           VALUES ($1, $2, 'shortlisted', 'Applied',
                   'Sourced candidate; values-invited live 2026-08-07 (no Markaz record at the time). Record created by Coco 2026-08-13 per Ayesha, from CV + Zero In call of 2026-08-13.')
           RETURNING id, candidate_id, job_id, status""", [CAND_ID, JOB_ID])
APP_ID = app[0]["id"]
print("Application created:", app[0])

# ---- Step 3: scorecard submit (guard: values_scorecard IS NULL, row-count assert) ----
rows = q("""UPDATE applications
            SET values_scorecard = $1::jsonb,
                values_interview_result = 'pass',
                values_interview_score = 5,
                values_interview_date = '2026-08-13',
                values_interviewer_name = 'Ayesha Khan',
                updated_at = NOW()
            WHERE id = $2 AND job_id = $3 AND candidate_id = $4 AND values_scorecard IS NULL
            RETURNING id, status, values_interview_result, values_interview_score""",
         [json.dumps(scorecard), APP_ID, JOB_ID, CAND_ID])
assert len(rows) == 1, f"Expected exactly 1 row updated, got {len(rows)} - INVESTIGATE"
print("Scorecard submitted:", rows[0])

verify = q("""SELECT a.id AS app_id, c.id AS cand_id, c.first_name, c.last_name, c.email,
                     length(c.resume_data) AS resume_len, c.resume_file_name,
                     a.status, a.values_interview_result, a.values_interview_score,
                     a.values_scorecard->>'candidateName' AS sc_name,
                     a.values_scorecard->>'proceedToRightSeat' AS proceed,
                     jsonb_array_length(a.values_scorecard->'values') AS n_values
              FROM applications a JOIN candidates c ON c.id = a.candidate_id
              WHERE a.id = $1""", [APP_ID])
print("Verify:", json.dumps(verify[0], indent=2))
