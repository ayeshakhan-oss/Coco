# -*- coding: utf-8 -*-
"""Submit Marzia Hasnain's values scorecard (PASS 5+/1+-/0-) to Markaz.
Target: application 3819 ONLY (Job 41 - Growth Manager Karachi, candidate 3090).
Approved by Ayesha 2026-08-13 ("upload on markaz").
Guards: exact app id + job id + candidate id, values_scorecard IS NULL (no overwrite),
row-count assert. Values pass -> status stays 'shortlisted'.
Uses Neon HTTPS SQL API (port 5432 blocked on this network)."""
import os, json
import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

APP_ID = 3819
JOB_ID = 41
CAND_ID = 3090

scorecard = {
    "date": "Aug 13, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "Coco (AI P&C Assistant)",
    "candidateName": "Marzia Hasnain",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "A direct, on-point almost-quit story: first proper job at Source as a fresh-grad brand strategist - five freelancer team members with their own schedules, six clients, no manager above her. One week in she concluded 'maybe no, this is not my cup of tea.' A friend's push - 'if you leave now, then you've learned nothing... this is how you will learn leadership' - changed her mind. She stayed, learned time management and how to lead people 'who don't want to be led,' and a team member told her at her exit that working with her taught him to be organized.",
            "curveBall": "The ugly-problem probe: a co-strategy-manager's mother died a week before her quarterly research deck was due (100+ slides, primary and secondary research, three weeks left of a three-month timeline). 'Nobody was even willing to take part in it.' She volunteered knowing exactly the workload, worked 12-13-hour days ('my hands shivering almost every day'), and delivered on time. Senior leadership congratulated her; the returning colleague cried and told her 'this is what makes working with the right kind of people valuable.'",
            "microCase": "Took this interview from inside a noisy office celebration rather than reschedule - 'I lined up with these people... let's have it' - and later chose to push through the audio problems ('we're in the flow, so let's try') when offered a reschedule. Rating +: both probes answered with real, first-ask, high-cost incidents; the deep-dive answers the exact question asked."
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": "At KDSP, a new graphic designer - first job ever, from an underprivileged area, weak English, 'extremely innocent' - couldn't parse professional briefs. Marzia sat with her and explained briefs word by word, wrote out the exact copy so 'she could just copy paste,' and when spelling errors still reached the boss, said 'oh, it's my error, I must have made some mistake' while the designer was near tears. Owned that 'back then it felt a little unfair, but... this is the kind of stuff that you leave behind,' and they're still close today.",
            "curveBall": "The hype-a-peer question (after a rephrase): her line manager/associate director, whom she initially doubted ('is she even doing her work?') before realizing 'if the department is running, it's because of that person' - and now openly credits her: 'hats off to her... we don't give our supervisors enough credit.'",
            "microCase": "The ugly-problem story doubles here - she framed the 3-week deck rescue as 'not just for a colleague, but also for my department because we have to answer to that.' Rating +: unprompted covering with a real personal cost, plus genuine upward appreciation with an honest arc from skepticism to respect."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+/-",
            "deepDive": "The professional upskilling answer is intent, not yet practice: she enrolled in a free digital marketing course 'actually just yesterday,' reasoning it's 'the need of the hour' for understanding the digital landscape 'in terms of numerics and numbers and data,' with the first 45-minute lectures planned for Monday. Self-aware framing ('I either sign up for something or I won't do it - if I signed up for it, it's definitely happening'), but there is no completed learning to evidence yet.",
            "curveBall": "Not separately tested - single structured question for this value, and this section carried the worst of the audio problems (question repeated several times; fairness rule applied - the thinness is in the content of her answer to the clear version, not confusion).",
            "microCase": "Unprompted in her intro: a rebuilt daily reading habit ('I force myself, at least 30 minutes every day') and active exploration of new art techniques (clay, mirror work, acrylics, oils) - genuine personal work-in-progress practice, and she volunteered the 1%-better-every-day philosophy herself, 'not just professionally, also in your personal life.' Rating +/-: the personal habits are real and count (personal examples are valid evidence), but the professional-craft evidence is a day-old enrollment with zero lectures completed - present but weak."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": "Received-feedback probe: her first-job manager/mentor told her 'you are not an active listener.' It directly attacked her self-image - 'I've grown up being the therapist-like friend... I was like, what is she talking about?' - and she 'struggled really accepting' it. Then she applied the mentor's techniques, inverted her habit (listen and understand first, notes after, instead of transcribing in a hurry), and credits it with lasting improvement to her contributions and delivery across later jobs.",
            "curveBall": "The giving-feedback side was not probed this call - not directly evident, and not held against her (fairness rule).",
            "microCase": "Comfortable flagging problems to the interviewer in real time - repeatedly and politely surfacing the audio issue rather than nodding through unheard questions, and asking for value definitions to be repeated until she actually understood them. Rating +: a stung-then-owned feedback story with named behavior change and durable results; honest in-call communication habits consistent with it."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "During her probation at the agency, the Shell WePower relaunch brief landed on her own client. Her instinct was to keep it - 'me being me, I like to believe that I'm the kind of person who can just handle it' - but after her supervisor's challenge ('are you sure you're skilled enough to take on such a huge brief?') and a talk with a co-strategy manager with 3+ years in strategy, she concluded 'the truth of the matter is she was definitely more skilled' and handed over the highest-visibility brief she'd been given, then attached herself to learn from how the colleague ran it.",
            "curveBall": "Not separately tested - single structured question for this value.",
            "microCase": "Asked for 'one second to think about this' before answering rather than performing an instant story; also her flexibility through the audio chaos (happy to switch to WhatsApp, reschedule, or push on - 'it's up to you'). Rating +: a genuine relinquishment of a career-boosting project with the ego cost named out loud, ending in learning rather than resentment."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "The silly-ritual question got a lived, repeated practice, not an invention: she keeps a coloring book and color pencils in her desk drawer and has run 10-minute group coloring breaks at two workplaces when anyone was stressed or in a bad mood - 'you're having the worst day, so you take it over, we'll just be there with you while you're doing it.'",
            "curveBall": "The detail that elevates it: she deliberately left the coloring book behind at every workplace when she moved on, 'for anyone to use it while I'm not there' - the ritual outlives her presence.",
            "microCase": "Warmth throughout a technically miserable call - apologizing for the office noise, laughing, 'these are such interesting questions, it's helping me unravel things in my mind,' and heading back to join the office celebration after. Rating +: self-initiated, repeated, and institutionalized joy practice with vivid, specific texture."
        }
    ],
    "finalComments": "PASS - 5(+) / 1(+/-) / 0(-). Zero minuses and one plus-minus (Continuously Improve Our Craft, where the professional evidence was a day-old course enrollment; personal improvement habits are real). Evaluated solely on her own transcript evidence against the value and rating definitions. GWC: Gets it - PROBE (mission understanding untested; her closing questions were practical logistics - remote vs office, location, case-study timing); Wants it - PROBE, untested not negative (why-Taleemabad neither asked nor volunteered; Karachi-based, volunteered she is open to relocating); Capacity - PROBE (the call showed brand strategy, agency delivery and creative/content leadership at Source, KDSP and an agency strategy-manager role; government/B2B partnership hunting - the core of the GM-Karachi role - is untested here; the case study and technical debrief must test the JD's actual verbs). Proceed: CONDITIONAL YES - values PASS; probe all three GWC dimensions at case study + debrief. TRANSCRIPT CAVEAT: persistent audio problems (echo, breaking) forced repeats through values 3-4, and Fathom flipped speaker attributions in several blocks; fairness rule applied - she was never penalized for a garbled or repeated question. FLAGS: (1) salary not discussed - uncollected; (2) remote-for-Karachi communicated on record (remote role, based Sindh/Karachi, no head-office travel); she expects the case study over the coming weekend (48 hours) if she advances; (3) interview-design note: values 3, 5, 6 were single-question and the giving side of Courageous Conversations went untested.",
    "proceedToRightSeat": "Yes"
}


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=60)
    r.raise_for_status()
    return r.json()["rows"]


# Step 0: pre-submission verification (duplicate + no-overwrite guard)
pre = q("""SELECT a.id, a.job_id, a.status, a.values_scorecard IS NOT NULL AS has_sc, a.updated_at
           FROM applications a WHERE a.candidate_id = $1 ORDER BY a.updated_at DESC""", [CAND_ID])
print("Pre-check (all apps for candidate 3090):")
for r in pre:
    print(" ", r)
assert any(r["id"] == APP_ID and r["job_id"] == JOB_ID and not r["has_sc"] for r in pre), \
    "Guard failed: app 3819 not found empty on job 41 - ABORTING"
most_recent = pre[0]
assert most_recent["id"] == APP_ID, \
    f"Guard failed: most recently updated app for this candidate is {most_recent['id']}, not {APP_ID} - check which record Markaz UI shows"

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
print("\nSubmitted:", rows[0])

verify = q("""SELECT values_scorecard->>'candidateName' AS name,
                     values_scorecard->>'proceedToRightSeat' AS proceed,
                     jsonb_array_length(values_scorecard->'values') AS n_values,
                     status, values_interview_result, values_interview_score
              FROM applications WHERE id = $1""", [APP_ID])
print("Verify:", verify[0])
