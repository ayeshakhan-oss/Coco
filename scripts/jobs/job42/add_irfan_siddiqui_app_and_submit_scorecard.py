# -*- coding: utf-8 -*-
"""Irfan Siddiqui (Job 42 - Senior Manager Growth): refresh existing candidate 659, create the
Job-42 application, submit his values scorecard (PASS 4+/2+-/0-).
Approved by Ayesha 2026-08-14 ("if his profile isn't already on Markaz, then upload it and
submit his scorecard").

DUPLICATE CHECK RESULT (2026-08-14): he IS already on Markaz as candidate 659
(irfan.m.siddiqui@hotmail.com, phone 3363670513 = CV phone +923363670513, Islamabad;
one prior application: app 759, Job 23 Program Manager, rejected Feb 2026).
So per the duplicate-records SOP: NO new candidate row. This script:
  1. Updates candidate 659 - current email from his 2026 CV (outlook), fresh resume PDF,
     current role/company, LinkedIn (guards: id+phone match; outlook email not used elsewhere)
  2. Inserts the Job-42 application, status 'shortlisted' (guard: no existing app on job 42)
  3. Submits the values scorecard via guarded UPDATE (values_scorecard IS NULL, row-count assert)
Uses Neon HTTPS SQL API (port 5432 blocked on this network)."""
import os, json, base64
import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

JOB_ID = 42
CAND_ID = 659
NEW_EMAIL = "irfanmsiddiqui@outlook.com"
OLD_EMAIL = "irfan.m.siddiqui@hotmail.com"
CV_PATH = r"C:\Users\Dell\Downloads\Irfan S Resume 2026.pdf"


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=120)
    r.raise_for_status()
    return r.json()["rows"]


scorecard = {
    "date": "Aug 14, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "Coco (AI P&C Assistant)",
    "candidateName": "Irfan Siddiqui",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Almost-quit question: mild premise pushback first ('I'm not a quitter... I'd have to really joggle my mind'), then a genuinely personal arc - working while self-financing his education, starting from helping his father's general store; grades began suffering in the quantitative subjects and he named the decision point: 'I realized that if I leave it... this happens to me that I'm quitting education.' Kept working ('I had no other option'), retook the failed subjects, recovered the grades. The arc extends across years: the Pepsi management-training move to the Middle East left his degree incomplete; the program changed under him, adding subjects; he completed them in pieces - a summer course on a one-month vacation, a three-week course on a later return - across relocations and after his daughter was born. A multi-year refusal to let the education go.",
            "curveBall": "Ugly-problem probe - concrete and owned: at Fueling Brains (~2022), Google Business Profile verification for their education centers in Alberta was stuck (physical verification needed, nobody on-site - Alberta winter, COVID lingering - head office in Houston). He arranged the document routing, then escalated to a joint call he assembled (the Google team, the directors including himself, and the academy director) and got Google to make a process exception covering 12 centers: 'It was a kind of a different approach and they didn't used to do that. They made an exception when I made my case.'",
            "microCase": "The self-description in his intro carries the same signal unprompted: started from a general store counter, worked-and-studied, crossed industries (advertising -> FMCG -> EdTech) 'with 100% dedication.' Rating +: two specific instances with personal stakes, named decision points, and outcomes - consistent evidence across both probes."
        },
        {
            "name": "All for One & One for All",
            "rating": "+/-",
            "deepDive": "Covered-a-mistake question answered at role level, not incident level. Riyadh FMCG, 200+ people reporting through his subordinates: 'usually, when there was a mishap or mis-commitment or negative review - yes, it was my job to cover for my team.' The learning arc is genuine (started out penalizing, 'then I slowly and gradually learned... it's better that you inspire others... your team is only as strong as your weakest link') - but the question asked for a time he covered WITHOUT being asked, and no single moment, colleague, or mistake was ever named. 'It was my job to cover' is duty, not the unprompted act the value probes.",
            "curveBall": "Quiet-voices probe, same register: a real management practice - 200+ multinational team, 'I knew them by name' over 3-4 years, weekly cadence plus one-on-ones, and the principle that the silent exceptional performer is his to advocate for ('he's not asking for anything... but it's my job as a manager to understand that if we can do this, A, B, C...'). Credible habitual behavior; zero named instances despite the question asking 'have you EVER...'.",
            "microCase": "Rating +/-: both answers describe systems and philosophy, believably - but across two probes not one specific person or incident appeared. Habitual claims without instances cap at plus-minus."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Recent-upskill question: AI, with an honest motive - when ChatGPT launched, 'you feel like you are falling behind... asking what's the weather is not enough - you need to understand how to learn it.' Tied it to his field (AI x digital marketing), worked across platforms, and completed a named training (transcript garbles it as 'CLOD training' - confirm with him; plausibly a Claude/cloud course). Origin story: COVID lockdown - 'I decided, let's learn something. That's where the journey started, self-learning' - and the register that it 'doesn't have to be about what I do or where I work.' CV corroboration: Google Certified Digital Marketing 2023, HubSpot Academy Online Advertising 2024.",
            "curveBall": "Not separately tested (single-probe value this call; interview-design note). Noted separately: his unprompted candor after hearing of Taleemabad's AI transition - 'just between you and me, I think this is also a fad... 2030 onwards, all of this will also be obsolete' - scored nowhere as a values negative; flagged under GWC Gets-It as a debrief probe.",
            "microCase": "The work-in-progress posture recurs across the call: in Don't Hold On he released his flagship Excel file partly 'because I'll also get to learn how he does that - and he also taught me'; in Courageous Conversations he accepted a bruising appraisal and changed ('nobody's perfect, including you yourself... you have some weaknesses develop with time'); the decade-long education completion; his closing ask about organizations that 'invest in learning.' Rating +: the direct answer alone is moderate (timeline vague, training name garbled - fairness rule applied); the consistency of the learning posture across four separate moments of the call, plus dated 2023/2024 certifications on the CV, lifts it to clear evidence."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Hardest-feedback-GIVEN: he redirected the question in the first breath ('Can I answer if it was the hardest feedback I received and how I had to react?') - allowed if it looped back to giving, which it never did. What he told instead is an excellent RECEIVING story: mid-career FMCG, a new manager arrived from the Africa market with a blunt no-preamble style; the year-end appraisal listed shortcomings he 'wasn't expecting or ready for.' Honest about the sting: 'that night I was really disturbed... really aggravated and not happy at all' (appraisal, increment, bonus attached). The turn: 'the next morning... I was completely calm and completely open, and I thought, what if what he is saying is right?... If I close myself right now, my working relationship will be bad, my mood will be bad, and if my mood is bad then my team will be bad.' Accepted it, worked the gaps, three months later 'the relationship was very good... and when the numbers started getting better, I also realized - he was right.' Complete arc: sting -> resistance -> choice -> change -> verified outcome.",
            "curveBall": "Which-leader-intimidates-you + what feedback would you offer them: 'the leader who's quiet, who doesn't share much, makes me uncomfortable.' The feedback he'd offer stayed hypothetical and soft - signal his own openness, invite them to 'not hold it in' - managing his side of the relationship rather than delivering feedback to them.",
            "microCase": "One live act of candor in the room: telling the recruiter of an AI-heavy organization, unprompted, that he thinks the current AI wave is 'a fad.' Whatever one makes of the opinion, saying it mid-interview is the behavior this value describes. Rating +/-: receiving side is a clear plus - among the best answers of the call; the giving side was actively substituted away and never evidenced beyond hypothesis. One direction of a two-direction value."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "Handed-off-a-project question - the exact shape the value asks for, attachment named rather than airbrushed. The monthly/annual sales report Excel file was HIS signature asset ('I was also really famous' for Excel among peers). A newcomer was visibly better; his manager suggested sharing it; his instinct: 'every fiber in my body said, no - this is your work, he's going to take it away.' He handed it over anyway, for stated reasons: 'he's better than me at this... and I'll also get to learn how he does that.' Outcome, honestly reported: 'He did actually make it better, in all honesty. And not only that, he also taught me how he's doing it. We were working as a team.' His distilled principle: 'Superman is not alone... there are different superpowers. If you work as a team, the sky is the limit.'",
            "curveBall": "Follow-up (how did it feel): acknowledged the anxiety honestly ('actually, yes...') before the transcript degrades; the recoverable close was his decision philosophy - once you decide, 'leave it to Allah' - release, not rumination. Nothing scored on the garbled stretch (fairness rule).",
            "microCase": "Rating +: attachment named, deliberate release for better impact, stayed engaged as a learner, honest about the feeling - with a concrete outcome."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Silly-ritual question (explicitly non-traditional, no food/chai): first credited a real experienced example - his Fueling Brains manager Derek loosening the remote team's Monday meetings ('I would give him credit for that - it changed the entire team's outlook') - and then INVENTED his own on the spot: 'Wacky Wednesday' - mid-week, one team member decides how the day goes; his example: if it's raining in Islamabad, a soundtrack plays while everyone works, 'you get to be yourself.' Meets the constraint, generated live, culturally grounded ('considering our traditions and cultural values').",
            "curveBall": "Emoji question: the high-five - 'this is a happy emoji... it shows that you're not alone. You need someone to do that with.' A joy answer that lands back on togetherness.",
            "microCase": "Warm, easy register throughout - the Karachi/Islamabad 'where am I from' riff, the shared maths-fear laugh with the interviewer, the closing 'it didn't feel like I was sitting in front of...' - comfortable, engaged presence for a full hour. Rating +: generated an original ritual on request, credited others where credit was due, and the personal-joy signal is consistent."
        }
    ],
    "finalComments": "PASS - 4(+) / 2(+/-) / 0(-) (>=3 plus-minus = OUT, not triggered). Evidence pattern: strongest where the story is his own stake (persistence, letting go, receiving hard feedback), weakest where the probe asks for a specific incident involving others (covering a mistake, quiet voices, feedback given) - there he consistently answers at the level of role, system, and philosophy; believable philosophy, but twice it capped a rating at plus-minus. CALIBRATION NOTE (transparency): the verdict-critical rating is Continuously Improve - its direct answer alone is plus-minus-grade (vague timeline, one garbled training name); the plus rests on the learning posture corroborated in four separate moments across the call plus dated CV certifications (Google Digital Marketing 2023, HubSpot 2024). Held at plus-minus it would make the card 3+/3+- = OUT under the rule. Counter-pressure runs the other way: Courageous Conversations has a defensible plus argument (an excellent receiving arc PLUS a live act of candid disagreement in-interview), which would make PASS robust at 5+/1+-. Adjudicated PASS by Ayesha 2026-08-14. TRANSCRIPT NOTE: worst Fathom attribution-flipping to date plus multiple garbled Urdu-English passages - speakers reconstructed from content, fairness reading applied, nothing scored on garbled text; do not take raw Fathom speaker labels at face value. GWC: Gets it - PROBE (sharp process questions - case-study timing, 48-hour window, start date; best ownership signal of the call was proposing unprompted to sync with the outgoing role-holder 'as soon as possible, from Monday,' on her schedule, weekends included; but walked in without having read the JD and asked nothing about mission/model/government-partnerships core; DEBRIEF PROBE: his 'AI is a fad... obsolete by 2030' view vs Taleemabad's AI-first workflows - healthy skepticism or resistance?). Wants it - PROBE (no why-Taleemabad or why-edtech articulated; stated criterion is an organization that 'values people, invests in them'; salary: gave no number, asked our range, readily accepted the 400k ceiling and framed it as 'a starting point, not an end point'; family relocating from Turkey the coming weekend - settled-in-Islamabad signal). Capacity - PROBE (evidenced: BAT Riyadh key accounts/modern trade 2012-2020 with 200-person field team, 6-7% consecutive annual growth, contract negotiations; EdTech SaaS marketing at Fueling Brains 2022-2023 remote; advertising account management Saatchi & Saatchi, FP7 McCANN; currently Miraclus Dubai activations PM. NOT evidenced: Pakistan B2G/government partnerships, institutional deal closure, owned revenue numbers - the SMG JD's core pillars; the case study must carry this test). FLAGS: (1) duplicate-record resolution - he already existed as candidate 659 (prior app 759, Job 23 Program Manager, rejected Feb 2026; phone match confirmed); profile refreshed with 2026 CV and current outlook email (old hotmail on record until 2026-08-14), NO new candidate row created; (2) salary: no number on record, verbal acceptance of <=400k - collect a firm figure at the next stage; (3) interview held on the 14 Aug holiday - noted, nothing scored on it. Next: SMG case study ('Execution Sprint', 48-hour window) - he flagged family arriving over the weekend, expect an extension request (already told him that is fine).",
    "proceedToRightSeat": "Yes"
}


# ---- Step 0: pre-checks ----
cand = q("SELECT id, first_name, last_name, email, phone FROM candidates WHERE id = $1", [CAND_ID])
assert len(cand) == 1 and cand[0]["phone"] == "3363670513" and cand[0]["email"] == OLD_EMAIL, \
    f"Guard failed: candidate 659 does not match expected identity: {cand} - ABORTING"
clash = q("SELECT id FROM candidates WHERE email = $1 AND id <> $2", [NEW_EMAIL, CAND_ID])
assert not clash, f"Guard failed: outlook email already used by candidate(s) {clash} - ABORTING"
dup = q("SELECT id, status FROM applications WHERE candidate_id = $1 AND job_id = $2", [CAND_ID, JOB_ID])
assert not dup, f"Guard failed: candidate {CAND_ID} already has application(s) on job {JOB_ID}: {dup} - ABORTING"

with open(CV_PATH, "rb") as f:
    resume_b64 = base64.b64encode(f.read()).decode("ascii")
print(f"CV loaded: {CV_PATH} ({len(resume_b64)} b64 chars)")

# ---- Step 1: refresh candidate 659 (email from 2026 CV, fresh resume, current role) ----
upd = q("""UPDATE candidates
           SET email = $1,
               resume_data = $2, resume_file_name = $3, resume_mime_type = 'application/pdf',
               location = 'Islamabad, Pakistan',
               current_position = 'Project Manager Activations & Experiential Marketing',
               current_company = 'Miraclus (Dubai)',
               linkedin_url = 'https://www.linkedin.com/in/irfanmsiddiqui',
               education = 'BBA (Honors), IQRA University Karachi (2007-2011); Google Certified Digital Marketing (2023); HubSpot Academy Online Advertising (2024)',
               experience = '18+ years across advertising, FMCG and EdTech. Miraclus Dubai - PM Activations & Experiential Marketing + BD Manager (Mar 2025-date); Fueling Brains (EdTech SaaS, remote) - Project Marketing Manager (Feb 2022-Nov 2023); British American Tobacco Riyadh - Key Accounts Sales, Modern Trade & Shopper Marketing (2012-2020, 200-person field team, 6-7% consecutive annual growth); FP7 McCANN Jeddah - Account Manager (2010-2011); Saatchi & Saatchi Karachi - Account Manager (2007-2009). BAT Growth Academy Graduate, BAT Employee of the Year.',
               updated_at = NOW()
           WHERE id = $4 AND email = $5
           RETURNING id, email, resume_file_name""",
        [NEW_EMAIL, resume_b64, "Irfan S Resume 2026.pdf", CAND_ID, OLD_EMAIL])
assert len(upd) == 1, f"Expected 1 candidate row updated, got {len(upd)} - INVESTIGATE"
print("Candidate refreshed:", upd[0])

# ---- Step 2: application insert ----
app = q("""INSERT INTO applications (candidate_id, job_id, status, stage, notes)
           VALUES ($1, $2, 'shortlisted', 'Applied',
                   'Sourced candidate; values-invited live 2026-08-07 (no Job-42 record at the time; existing candidate 659 from Job 23, Feb 2026). Application created by Coco 2026-08-14 per Ayesha, from 2026 CV + Zero In call of 2026-08-14.')
           RETURNING id, candidate_id, job_id, status""", [CAND_ID, JOB_ID])
APP_ID = app[0]["id"]
print("Application created:", app[0])

# ---- Step 3: scorecard submit ----
rows = q("""UPDATE applications
            SET values_scorecard = $1::jsonb,
                values_interview_result = 'pass',
                values_interview_score = 4,
                values_interview_date = '2026-08-14',
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
