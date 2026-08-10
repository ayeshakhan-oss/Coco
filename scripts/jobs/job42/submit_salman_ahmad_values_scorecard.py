# -*- coding: utf-8 -*-
"""Submit Salman Ahmad's values scorecard (OUT) to Markaz.
Target: application 3943 ONLY (Job 42 - Senior Manager Growth, candidate 3189).
Approved by Ayesha 2026-08-10 ("submit his scorecard on markaz and mark no").
Guards: exact app id + job id, values_scorecard IS NULL (no overwrite), row-count assert.
Values failed -> status 'rejected' (per feedback_values_scorecard_schema.md)."""
import os, json
import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

APP_ID = 3943
JOB_ID = 42

scorecard = {
    "date": "Aug 10, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "Coco (AI P&C Assistant)",
    "candidateName": "Salman Ahmad",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+/-",
            "deepDive": "The about-to-quit-but-stayed question was answered with a 2007-08 job-offer choice in Australia: weighing Embarcadero against AECOM and choosing AECOM for the Fortune-500 brand and career advancement despite lower pay. A career-selection story - the 'about to quit but decided to stay' element was never addressed, so persistence through difficulty went undemonstrated.",
            "curveBall": "Second probe (question wording cut off in the transcript at 7:55): volunteer field research for the Department of Environment while GM at NUST - collecting plastic-waste statistics in 'a sewage kind of a place' outside his own background. Genuine willingness to do unglamorous work, though a one-off without an adversity arc.",
            "microCase": "Not directly evident in interview. Rating +/-: one real if modest evidence point (the environmental fieldwork); the deep-dive story did not demonstrate the value."
        },
        {
            "name": "All for One & One for All",
            "rating": "+/-",
            "deepDive": "Covered-a-mistake-without-being-asked: an honest, direct 'No, I haven't. I'll be honest with you' - he covers when asked, and even then filters it: 'you have to weigh things up... if that cover up is actually harmful for the company in the long run.' The honesty is creditable; instinctive, unprompted backing of a teammate was not evidenced.",
            "curveBall": "Quiet-voices probe - his best moment on this value: at NUST (40 reports, 8 program managers) he noticed a hardworking introvert who never claimed credit and publicly attributed a tight-deadline achievement to her in front of the team. Specific and believable.",
            "microCase": "Which-peer-do-you-hype: generic at first ('I like people who are optimistic... take challenges head on'); when pushed for a person, described an account executive whose virtue was connections and hitting enrollment targets - closer to admiring a high performer than lifting someone up. Rating +/-: one genuine surfacing example against an explicit no on unprompted cover and a performance-based hype answer."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Concrete and recent: an online data-analytics training (with HP), deliberately refreshing data-warehouse/dashboard skills he had last used ~15 years ago, tied to a use: 'so you can make your decisions more easily.'",
            "curveBall": "Not separately tested - single structured question for this value this call (interview-design note).",
            "microCase": "Unprompted in the intro: reads Angela Duckworth's research on grit as a leisure habit; later, 'you cannot wear one kind of leadership hat all the time... you have to adjust yourself' - a learning-oriented view of his own style. Rating +: specific, current, self-driven upskilling plus an unprompted learning habit, consistent across the call."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Hardest-feedback-given stayed generalized - 'there has been many instances' - then coaching Hashoo Foundation staff on corporate communication etiquette and an NLC training on autocratic-vs-democratic styles. Trainer-room corrections delivered 'very diplomatic[ally]'; no single hard, personally risky conversation was narrated.",
            "curveBall": "Feedback-received-that-proved-true: genuine and self-aware - early-career feedback that he trusted everyone 'just like your family members'; he accepted it and built calibrated trust. Receiving feedback with openness: evidenced.",
            "microCase": "At the close he politely challenged Taleemabad's own hiring sequence (hire the SMG before their two GM reports) - a small, constructive push-back delivered to the interviewer directly, and he took the rationale gracefully ('fair enough'). Rating +/-: the receiving side is real; the giving side stayed generic and diplomacy-first, which is the harder half of this value."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "Handed-over-a-project question was answered with a process-disruption story: replacing Hashoo Foundation's manual payment-voucher process with QuickPay online payments - 'There has to be a disruption. You cannot go with the status quo.' Fits the let-go-of-old-practices half of the definition as read out, concrete and outcome-bearing.",
            "curveBall": "Not separately tested (single-probe value this call; interview-design note).",
            "microCase": "Not directly evident in interview. Rating +/-: clear evidence of abandoning a legacy process; the question's personal dimension - handing over something of HIS OWN - went unaddressed, so letting go of ownership/control is untested."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Silly-ritual question: strong, lived answer - personally organized Hashoo Foundation's first drum circle, narrated its arc vividly (reluctance, then twenty minutes in everyone jumping and chasing the rhythm), read the effect ('freshened up their mind... gave them a kick'), and brought them back six months later. Plus a second concrete teamwork game (funnel-and-marble relay for mutual support).",
            "curveBall": "Emoji question: thumbs up - 'even though you hit a brick wall or a showstopper... always thumbs up.' Thin on its own but consistent with the rest.",
            "microCase": "Easy, warm rapport in the small talk (morning walks, the blue-and-burgundy bird), and unprompted, generous appreciation of the hiring process at the close. Rating +: self-initiated, repeated joy rituals with observed team impact - the clearest value of his interview."
        }
    ],
    "finalComments": "OUT - 2(+) / 4(+/-) / 0(-). Rule applied: three or more plus-minuses = OUT even with zero minuses. A near-miss profile rather than a values clash: the recurring pattern was answering hard behavioral questions by pivoting to adjacent, safer stories (quit-but-stayed answered with a job-offer choice; hand-over answered with process modernization; hardest-feedback-given answered with training-room corrections), leaving too little direct evidence to rate + on four values. Strongest demonstrations: Practice Joy (self-organized, repeated drum-circle ritual with observed team impact) and Continuously Improve Our Craft (recent data-analytics refresher plus an unprompted learning habit). GWC: not assessed (OUT - GWC is only evaluated after a PASS per SOP). TRANSCRIPT CAVEAT: Fathom flipped several speaker attributions (parts of his answers around 11:14-14:00 are credited to the interviewer) and the second Don't-Walk-Away question at 7:55 is cut mid-sentence; scored on reconstructable substance per the fairness rule. FLAGS: (1) two 'I'm not being racist, but...' framings within 38 minutes - (a) avoided joining Embarcadero citing 'a lot of Indian influence on that company... being a Pakistani... your immediate boss, who's going to be that'; (b) on Hashoo staff: 'it's their background... the way of communication is not very polished' - his words as spoken, recorded without inference of intent, but the recurrence is worth weighing for a stakeholder-facing growth role; (2) consistent with screening flags: 20+ years, GM/COO-level history, asked PKR 550k at screening against the 350-400k band - the interview matched that shape (advisory posture, consultant war stories); (3) his hiring-sequence suggestion (onboard the SMG before hiring the two GM reports) was thoughtful strategic input - no bearing on the values verdict. Detailed values feedback email to follow per the candidate-communication process.",
    "proceedToRightSeat": "No"
}


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=60)
    r.raise_for_status()
    return r.json()["rows"]


# Step 0: pre-submission verification (duplicate + no-overwrite guard)
pre = q("""SELECT a.id, a.job_id, a.status, a.values_scorecard IS NOT NULL AS has_sc, a.updated_at
           FROM applications a WHERE a.candidate_id = 3189 ORDER BY a.updated_at DESC""")
print("Pre-check (all apps for candidate 3189):")
for r in pre:
    print(" ", r)
assert any(r["id"] == APP_ID and r["job_id"] == JOB_ID and not r["has_sc"] for r in pre), \
    "Guard failed: app 3943 not found empty on job 42 - ABORTING"
most_recent = pre[0]
assert most_recent["id"] == APP_ID, \
    f"Guard failed: most recently updated app for this candidate is {most_recent['id']}, not {APP_ID} - check which record Markaz UI shows"

rows = q("""UPDATE applications
            SET values_scorecard = $1::jsonb,
                values_interview_result = 'fail',
                values_interview_score = 2,
                values_interview_date = '2026-08-10',
                values_interviewer_name = 'Ayesha Khan',
                status = 'rejected',
                updated_at = NOW()
            WHERE id = $2 AND job_id = $3 AND values_scorecard IS NULL
            RETURNING id, status, values_interview_result, values_interview_score""",
         [json.dumps(scorecard), APP_ID, JOB_ID])

assert len(rows) == 1, f"Expected exactly 1 row updated, got {len(rows)} - INVESTIGATE"
print("\nSubmitted:", rows[0])

verify = q("SELECT values_scorecard->>'candidateName' AS name, values_scorecard->>'proceedToRightSeat' AS proceed, jsonb_array_length(values_scorecard->'values') AS n_values, status FROM applications WHERE id = $1", [APP_ID])
print("Verify:", verify[0])
