# -*- coding: utf-8 -*-
"""Submit Huda Shaikh's values scorecard (PASS) to Markaz.
Target: application 3803 ONLY (Job 41 - Growth Manager Karachi, candidate 3075).
Approved by Ayesha 2026-08-10 ("submit her scorecard, shes a yes on values").
Guards: exact app id + job id, values_scorecard IS NULL (no overwrite), row-count assert.
Values passed -> status stays 'shortlisted'."""
import os, json
import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

APP_ID = 3803
JOB_ID = 41

scorecard = {
    "date": "Aug 10, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "Coco (AI P&C Assistant)",
    "candidateName": "Huda Shaikh",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Bake-sale story (personal example - valid per SOP): sick on the Friday and contemplating dropping out, she 'pulled myself out of the bed' for a 10 p.m. grocery run and prepped that night until her hands hurt from chopping chocolate. Sunday brought cascading failures - gas outage confining baking to a 7-9 a.m. window, a malfunctioning oven knob (stood beside the oven in the heat 30-40 minutes), then total electricity failure. Response was composed and resourceful: a deliberate rest ('there was nothing I could do... so I decided to give myself some rest'), borrowed an electric oven via her mother's friend, recalculated when the generator could not carry the voltage, considered arriving late rather than quitting - and when power returned, ran two ovens in parallel and delivered a successful bake sale.",
            "curveBall": "Ugly-problem probe: at AKU research & grant management, a promotion left ~25 grants to redistribute, mostly onto one colleague (7-8 large grants in a week). Huda flagged the unfairness; when her manager then reassigned five of those grants to HER out of the blue, she took them - a week of back-to-back onboarding meetings and chasing hard-to-catch principal investigators on top of her full load. Managed them and concluded several.",
            "microCase": "Her reasoning under pressure - 'the larger portfolio I have, the more chances I have of... learning more' - reframing an absorbed burden as growth rather than grievance. Rating +: almost-quit moment named, turning point named, sustained through cascading obstacles; real workload absorbed in the second story."
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": "Covered-a-mistake question: she transparently negotiated a substitution ('instead of covering for a mistake, I can tell you how I stood up for one of my team members. Is that fine?' - interviewer approved). The story: a newly joined colleague, blocked by a finance approver who ignored a week of reminders then raised last-minute objections on a Friday evening, was 'on the verge of crying.' Unprompted, Huda took over the fight - told finance the delay was 'also their fault' and would hurt the whole organization's submission, and strategically brought in her manager because 'in Pakistan... they don't take you seriously if you're on a junior level.' Approval secured; 'my colleague was able to spend her weekend in peace.'",
            "curveBall": "Quiet-voices probe: her under-resourced Alzheimer's-study field team, borrowing space from a high-intensity infant-mortality project, demotivated and unable to get concerns through to the PI. She gave them a structured hearing, was honest about the constraints, and committed: 'if things escalate, I would be on their side to support them.'",
            "microCase": "The grants story doubles here - she raised the unfair-distribution concern for her friend BEFORE it had anything to do with her own workload. Rating +: three separate instances of unprompted advocacy with personal friction accepted. The literal covered-a-mistake behavior went untested (substitution approved in-call) - optional debrief probe."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Two to three months of rigorous, self-organized case-interview practice - alone, with siblings, and with a practice partner - deliberately building structured problem decomposition, framework mapping, and answer-first communication ('the answer is provided first, and then you get the background'). Candid that it was for another company's process; the skill itself is squarely relevant to a growth role.",
            "curveBall": "Not separately tested - single structured question for this value this call (interview-design note).",
            "microCase": "The call was saturated with learning orientation: self-taught baker from a makeshift patila oven, an embroidery class last month, annotating a book for the first time - and she designed a growth-mindset training around exactly this belief ('learning something new isn't restricted by age'). Rating +: deliberate, recent, methodical upskilling plus an unusually consistent learning register."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": "Hardest-feedback-given: upward, to her own manager - about behavior toward a teammate that the teammate himself had not complained about but the team could see affecting the dynamic. She raised it herself in their next one-on-one, framed it with care ('I know this isn't something you're doing intentionally... it is something you can work on'), and offered to help by flagging recurrences. The manager appreciated it and worked on it. She declined to name the specific behavior to the interviewer - discretion about a third party, not evasion; the arc (context, delivery, reception, outcome) was complete.",
            "curveBall": "Feedback-received-that-stung: her manager called out that Huda was bypassing her for the more experienced other manager. She owned it in the moment ('I realized that is what I've been doing'), explained the time-pressure rationale honestly, accepted the loop-in process her manager proposed, and changed the behavior.",
            "microCase": "Her mission-drift question at the close - asking how Taleemabad keeps impact from becoming 'a shield that they can show to people' - a courageous question to put to an interviewer. Rating +: both directions evidenced with specific incidents and outcomes."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "The six-month professional-development training module she built and delivered to 18 team leads. When the organization planned to expand it to field sites, she named her first instinct honestly - 'I did think initially that this was something I started... I should be the one leading such a project' - then reasoned through her workload (15-20 grants plus projects), the travel, and her own exhaustion, and deliberately let others lead: 'I thought it would be good to give other people the opportunity to deliver as well,' staying fully available with her materials and support.",
            "curveBall": "Not separately tested (single-probe value this call; interview-design note).",
            "microCase": "Not directly evident beyond the deep-dive. Rating +: the value's exact shape - something that was hers, the attachment named rather than airbrushed, a deliberate release for better impact, support without control."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Silly-ritual question (explicitly non-traditional): the origami-butterfly ritual from her growth-mindset session - paper handed to everyone, tutorial on screen, the whole team fumbling through it together - engineered so people are 'actually enjoying and not just passively consuming,' and tied to a belief (learning has no age limit). Also the AKU travel-goodies tradition and hand-packed cookie baskets she baked for the team on her last day (the food edge brushes the excluded category; the origami core is genuinely outside the box and something she has actually run).",
            "curveBall": "Emoji question not asked this call (single-probe value; interview-design note).",
            "microCase": "The whole opening register - the tres leches cake 'people don't stop eating,' the annotated bookshop novels, the air-dry-clay cactus ring holder - warm, energetic, generous throughout; the interviewer noted at the close how detailed and engaged she was. Rating +: a practiced, purpose-built joy ritual plus consistently warm in-call presence."
        }
    ],
    "finalComments": "PASS - 6(+) / 0(+/-) / 0(-). The cleanest evidence pattern of the values calls scored to date on this job: every answer was a specific incident with the tension named, her action, and the outcome. CALIBRATION NOTE (transparency): the two ratings most at risk of inflation were stress-tested - All for One (the literal covered-a-mistake question was substituted, with interviewer approval; rating rests on three separate unprompted advocacy instances) and Continuously Improve (the upskill was case-interview prep for another company; rating rests on the deliberate 2-3 month practice method plus pervasive learning signals) - both hold on her own evidence. GWC (assessed on PASS): Gets it - YES-leaning (her mission-drift question - how Taleemabad avoids trading impact for 'titles and awards and numbers' - and next-market question were the most impact-literate candidate questions of the call; model specifics untested); Wants it - PROBE (first question was growth prospects - honest career intentionality, not a flag by itself; recently deep in another company's interview process; Taleemabad-specific motivation untested - debrief probe: why Taleemabad, why growth/BD, why now); Capacity - PROBE (strong execution and stakeholder discipline at AKU - 15-20 concurrent grants, investigator wrangling, finance escalations, training delivery, field-team management - but her track is research administration/grant management in health: no business-development, partnerships, deal-closure, or education-sector work evidenced; the case study and debrief must test the JD pillars - government/institutional partnerships, convenings, storytelling). FLAGS: (1) role-fit not values - weigh the GM case study ('The Story, the Room, and the Deal') heavily on the JD pillars; (2) salary expectations not discussed - collect at next stage; (3) role communicated as remote for Karachi (no Karachi office) - on record; (4) Fathom transcript had attribution flips (parts of her answers credited to the interviewer) - substance reconstructable, nothing scored on a garbled passage. Next: 48-hour GM case study; debrief probes as documented.",
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
           FROM applications a WHERE a.candidate_id = 3075 ORDER BY a.updated_at DESC""")
print("Pre-check (all apps for candidate 3075):")
for r in pre:
    print(" ", r)
assert any(r["id"] == APP_ID and r["job_id"] == JOB_ID and not r["has_sc"] for r in pre), \
    "Guard failed: app 3803 not found empty on job 41 - ABORTING"
most_recent = pre[0]
assert most_recent["id"] == APP_ID, \
    f"Guard failed: most recently updated app for this candidate is {most_recent['id']}, not {APP_ID} - check which record Markaz UI shows"

rows = q("""UPDATE applications
            SET values_scorecard = $1::jsonb,
                values_interview_result = 'pass',
                values_interview_score = 6,
                values_interview_date = '2026-08-10',
                values_interviewer_name = 'Ayesha Khan',
                updated_at = NOW()
            WHERE id = $2 AND job_id = $3 AND values_scorecard IS NULL
            RETURNING id, status, values_interview_result, values_interview_score""",
         [json.dumps(scorecard), APP_ID, JOB_ID])

assert len(rows) == 1, f"Expected exactly 1 row updated, got {len(rows)} - INVESTIGATE"
print("\nSubmitted:", rows[0])

verify = q("SELECT values_scorecard->>'candidateName' AS name, values_scorecard->>'proceedToRightSeat' AS proceed, jsonb_array_length(values_scorecard->'values') AS n_values, status FROM applications WHERE id = $1", [APP_ID])
print("Verify:", verify[0])
