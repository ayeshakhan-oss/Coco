# -*- coding: utf-8 -*-
"""Submit Yashfeen Zahid's values scorecard (OUT) to Markaz.
Target: application 3799 ONLY (Job 41 - Growth Manager Karachi, candidate 3071).
Approved by Ayesha 2026-08-12 ("I trust you, Coco. Submit her scorecard, the latest one you shared.")
after a leniency stress-test discussion (calibration note included in finalComments).
Guards: exact app id + job id, values_scorecard IS NULL (no overwrite), most-recent-app check, row-count assert.
Values failed -> status 'rejected' (never 'values_failed')."""
import os, json
import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

APP_ID = 3799
JOB_ID = 41
CANDIDATE_ID = 3071

scorecard = {
    "date": "Aug 11, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "Coco (AI P&C Assistant)",
    "candidateName": "Yashfeen Zahid",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+/-",
            "deepDive": "Almost-quit question: the commodity-markets modeling event at Marcus Evans. She had run the same event successfully the prior year; that year 'the commodity markets had collapsed, so we were not really getting a good response.' The 8-12 week timeline stretched to months. Actions named: 'a lot of extra hours,' 'expanding the market... going outside the comfort box,' re-engaging senior decision makers at energy-sector institutions to find out what had changed. Outcome honest and unembellished: delegation numbers recovered enough to run the event, 'not exactly the same as the last one.' Real persistence texture - but the question's core (almost quit, what changed your mind) never appears: the reason for continuing was institutional, not a personal decision point ('we just decided to continue with it because the event had to run. And we don't cancel the event for unnecessary reasons').",
            "curveBall": "Ugly-problem probe: no example produced. After asking what 'ugly problem' meant, the answer stayed entirely at theory level - 'I wouldn't say any problem is too complicated to solve... people just don't want to take ownership of it' - and closed with an explicit refusal of the ask: 'I can't give you a particular example because that's what I've been doing throughout my career.' Claiming the behavior is too constant to instance is a claim, not evidence; the question asked for the LAST time.",
            "microCase": "Laptop-lost-before-pitch scenario: substantively her best answer under this value - material memorized cold ('I know all the basics on my fingertips,' built from 5 years of remote B2B calls), notes on her phone, 'I usually carry a USB in my keys,' deck copies on phone/email/USB, improvise with whiteboard ('go old school, be a teacher'), ask the host site for a computer for visuals. Two deductions: she opened by re-litigating the premise ('you probably shouldn't be relying on your laptop entirely') before giving steps, and it stayed in habitual/hypothetical register rather than a lived recovery. Rating +/-: one solid-but-off-target story, one explicit no-example, one competent hypothetical - inconsistent evidence."
        },
        {
            "name": "All for One & One for All",
            "rating": "+/-",
            "deepDive": "Covered-a-mistake question: no incident, ever. The entire answer is conditional grammar - 'that can happen... if you are the primary stakeholder... your main focus at that moment should be just to deal with the situation rather than shifting blame on others... then later, if you do think it needs to be addressed... you can engage in a one-on-one meeting with that particular colleague.' The framework she describes is actually correct (absorb in front of the client, align internally afterward) - she understands the value's shape - but not one sentence describes a thing that happened: no client, no colleague, no mistake, no moment.",
            "curveBall": "Quiet-voices probe: first response was ~250 words of team-management theory with no example; when asked directly 'can you provide me any example... or you cannot think of one right now?' she answered 'No, I can't think of one, but...' and then found a real one: her Marcus Evans team of 4-5 B2B sales executives - one member who married early, dropped her education, and returned after 16 years ('feels left behind in life,' needs 'to be a little bit more vocal'), another fresh out of university; Yashfeen younger than the returner while managing her. Actions: one-on-ones with everyone; for the member uncomfortable opening up to her, 'I would just direct it to my manager who's more senior... they would maybe feel more comfortable talking to them'; principle stated: 'bring everyone to the table instead of just having a conversation yourself.'",
            "microCase": "The example is real and its team-composition detail credible, but it arrived only on second ask, and the mechanism for the quiet person was routing them to her manager - accommodating communication styles rather than becoming an unheard voice's advocate herself. Rating +/-: one question with zero incident, one with a prompted, partially-fitting example."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Recent-upskill question - the strongest sustained evidence of the call. Deliberate direction with reasoning: from an environmental sciences/sustainability background, building toward 'sustainability systems and climate risk particularly... because it impacts all of us'; she weighed channels (public institutions like World Bank/IFC vs. her corporate-driven path) and chose deliberately. Specific recent study: 'specific courses in the last one year or so' on climate risk and sustainability reporting - 'how European regulations work,' building on 5 years in the European market - and integration into 'Pakistan's climate finance,' citing that 'Pakistan has green banking and ESRM guidelines since 2017, but they're still not implemented.' Self-funded and self-directed, unprompted from her intro: 'Even if an organization is not paying me to do it, I just do it for myself.'",
            "curveBall": "Not separately tested - single structured question for this value this call (interview-design note).",
            "microCase": "Corroborated across the call: took the listening-skills feedback into Marcus Evans' 'very detailed and continuous learning improvement program' and demonstrably improved ('over the time I was able to work better on my listening skills... ask better questions and qualifying'); lifelong reading habit consciously shifted into nonfiction as her career progressed; self-described as 'someone who is very concerned with personal development always.' Rating +: specific, recent, self-initiated, self-funded, tied to a coherent plan, and corroborated by a real feedback-to-training-to-improvement loop. (Direction-of-upskilling flag recorded under GWC Wants-It, not here - role-fit signal, not a values deduction.)"
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Hardest-feedback-given: despite the explicit 'walk me through it,' no single incident was ever narrated. 'There can be like multiple ones... a couple of examples I can pick through' - but she never picks one. The categories: a team member 'who constantly likes to challenge your leadership,' and translating that upward without sounding 'too conflicting or leading towards favoritism.' Her method, abstractly: invite honest feedback, and 'if they're still not willing... you have to redirect them to a senior team member... I would redirect them to my manager.' Her own summary confirms the thinness: 'I wouldn't say it's exactly easy or I've been very successful.'",
            "curveBall": "Feedback-received-that-stung: the best single answer of the interview. Early at Marcus Evans, on voice-only calls across European accents, she was told her listening was the problem - named concretely: 'I would have some trouble in listening to the people... just rushed through the conversation and jumped to my next question without understanding the concern of the next person.' Why it stung, owned honestly: 'difficult for me to accept because I was someone who always thought that my English has been very good... what am I doing wrong? It took me some time.' What she did: worked through the continuous training program over time, improving listening, question quality, and qualification. Specific, self-implicating, complete arc - interviewer acknowledged the vulnerability in-call.",
            "microCase": "In-call micro-signal: politely probed the role's actual goal and structure at the close - engaged, not deferential. Rating +/-: the value has two directions and she evidenced exactly one - receiving is a clear plus, giving is generic to the point of empty and by her own words not a strength."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "Hand-over question, essentially in full: 'Oh, not entirely, I would say, because I think this is the one that's most difficult for me to let go of.' Why, self-diagnosed: 'I'm very conscientious. I feel personally responsible for a project or a task when I start working on it... a little hard for me to not take it personally and just give it to someone else who might be able to do it better.' Workaround: collaborate while keeping input; last resort: 'if it's not working, then I would engage with someone senior... my manager... discuss the best way forward and delegate it to them.' Closing: 'But yeah, I wouldn't let it go so easily.'",
            "curveBall": "Not separately tested (single-probe value this call; interview-design note).",
            "microCase": "The self-awareness is excellent - she named this as her weakest value unprompted and tied it to the eldest-sibling conscientiousness from her intro, rather than manufacturing a story. That honesty is why this is not a minus. But the question asked whether she has EVER done it and the answer is functionally 'not entirely / not easily,' with no instance of release produced; the described behavior (stay involved, keep input, escalate upward when stuck) is managed retention, not letting go. Rating +/-: candor about lacking evidence is not itself evidence."
        },
        {
            "name": "Practice Joy",
            "rating": "+/-",
            "deepDive": "Silly-ritual question (explicitly unique/outside-the-box, no food/chai): she drew on a day-long training attended 'quite a few years ago' (name forgotten). Two rituals: (1) slogan circle - her group 'came up with certain slogans' and before every session 'we would gather around in a circle and shout it at the top of our voices just to keep our energy intact'; (2) generator pull-start mime from a trainer ('she's, I think, from Thailand') - stand, bend to your feet, pretend to yank a generator cord and make the noise. Her reflection lands on-value: 'we would feel silly and stupid doing it... we are all grown adults... I think being an adult and doing silly things is actually something that makes you happy.'",
            "curveBall": "Not asked this call (single-probe value; interview-design note).",
            "microCase": "Both rituals are concrete, vivid, and meet the constraint - the generator mime genuinely outside-the-box - and grounding a hypothetical in lived experience is what the interview asks. What holds it at +/-: both are borrowed (cohort's slogan, trainer's mime) from one event years ago; nothing she has introduced herself appears anywhere in the answer; the 'how would you go about it' half went unaddressed; and the close hands the creative burden back - 'something like that... if you can come up with it.' Evidence of appreciating joy: yes. Evidence of practicing/infusing it for others: not shown."
        }
    ],
    "finalComments": "OUT - 1(+) / 5(+/-) / 0(-) (>=3 plus-minus = OUT). Composed, polite, honest in places - one genuine plus (Continuously Improve) and one excellent vulnerable moment (the listening-skills feedback) - but across five of six values the evidence was generic, hypothetical, or arrived only after prompting, against the interview's own opening ground rule (real-life experiences, not generic definitions). PATTERN (observed behavior only): four first-ask example failures in 40 minutes - ugly problem ('I can't give you a particular example'), covered-a-mistake (purely hypothetical), quiet voices ('No, I can't think of one, but...'), hardest-feedback-given (never narrated) - while her two strong stories prove she CAN narrate concretely, which makes the pattern the meaningful signal. Second pattern: manager-escalation as the default mechanism for hard interpersonal moments, three instances (quiet voices, courageous conversations, letting go) - notable for a remote, largely-solo Karachi role navigating government stakeholders without a senior in the room. CALIBRATION NOTE (leniency stress-test, transparency): every +/- was re-read under a maximally lenient 'human cushion' interpretation at the interviewer's request. Two ratings are acknowledged as flippable to + on a generous read (Don't Walk Away - real multi-month persistence story plus composed scenario answer; Practice Joy - concrete lived rituals grounding a hypothetical). Three hold at +/- even leniently because no incident exists to be generous about (All for One - zero incident on covered-a-mistake; Courageous Conversations - giving side empty by her own assessment 'I wouldn't say I've been very successful'; Don't Hold On - 'I wouldn't let it go so easily,' already cushioned up from a minus for honesty). Lenient ceiling: 3(+)/3(+/-)/0(-) - OUT either way under the >=3 plus-minus rule. Also noted: this was not a couldn't-open-up interview - she was fluent and comfortable for 40 minutes and twice retrieved detailed vulnerable stories instantly; the gap is lived-instance evidence, not expression. GWC (recorded despite OUT): Gets it - MODERATE-TO-GOOD (closing questions were her sharpest stretch: what the role optimizes for - 'are we trying to get funding... or implement programs'; volunteered the Sindh ghost-schools documentary and named Sindh/Balochistan political conditions as practical hurdles; asked about 6-12 month expectations). Wants it - FLAG (unprompted: 'now I want to be specifically transitioning into sustainability systems and climate risk... climate finance' - all her self-funded upskilling points at climate/ESG, not education or B2G growth; why-Taleemabad never articulated; if ever reconsidered, this is the first probe). Capacity - PROBE (evidenced: ~5 years B2B growth at Marcus Evans with senior decision-makers at European financial institutions, led 4-5 sales executives, earlier consultancy TechCellan + teaching assistant METU; not evidenced: government/institutional partnerships, Pakistan-market BD, education sector, long-cycle public-sector deals). FLAGS: (1) salary not discussed - uncollected; (2) role communicated on record as remote-for-Karachi with travel + Islamabad office, hiring-manager expectations deferred to technical call - consistent with the Job 41 script; (3) Fathom transcript has heavy speaker-attribution flips - identity reconstructed from content, fairness reading applied, nothing scored on a garbled passage; flag if the recording is shared with the hiring manager. Next: values feedback email (locked tone, pilot first) on request.",
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
           FROM applications a WHERE a.candidate_id = $1 ORDER BY a.updated_at DESC""", [CANDIDATE_ID])
print("Pre-check (all apps for candidate %d):" % CANDIDATE_ID)
for r in pre:
    print(" ", r)
assert any(r["id"] == APP_ID and r["job_id"] == JOB_ID and not r["has_sc"] for r in pre), \
    "Guard failed: app 3799 not found empty on job 41 - ABORTING"
most_recent = pre[0]
assert most_recent["id"] == APP_ID, \
    f"Guard failed: most recently updated app for this candidate is {most_recent['id']}, not {APP_ID} - check which record Markaz UI shows"

rows = q("""UPDATE applications
            SET values_scorecard = $1::jsonb,
                values_interview_result = 'fail',
                values_interview_score = 1,
                values_interview_date = '2026-08-11',
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
