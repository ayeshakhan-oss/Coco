# -*- coding: utf-8 -*-
"""Submit Kanooz Ahmed Siddiqui's values scorecard for Job 42 (Senior Manager Growth).

Verdict: PASS - 4(+) / 2(+/-) / 0(-). Zero In call 2026-08-18 (39 min), host Ayesha Khan.
Approved by Ayesha 2026-08-18 ("submit it on markaz") - card submitted exactly as drafted in chat
(Continuously Improve held at +/-, All for One held at + with the mutuality probe attached).

Record ALREADY EXISTS - no candidate or application insert here:
  candidate 3083 (kanoozay@gmail.com, phone 03172883152, Karachi)
  application 4111 on job 42, status 'shortlisted', applied 2026-08-09
  (she also has app 3811 on job 41 / GM-Karachi, status 'rejected' 2026-07-20 - flagged to Ayesha)

Single guarded UPDATE (values_scorecard IS NULL + row-count assert).
Uses Neon HTTPS SQL API (port 5432 blocked on this network)."""
import os, json
import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

JOB_ID = 42
CAND_ID = 3083
APP_ID = 4111
EMAIL = "kanoozay@gmail.com"


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=120)
    r.raise_for_status()
    return r.json()["rows"]


scorecard = {
    "date": "Aug 18, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "Coco (AI P&C Assistant)",
    "candidateName": "Kanooz Ahmed Siddiqui",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Almost-quit question - the NOWPDP banking-sector donor, a named relationship with real stakes. She inherited unclosed outstanding tasks from her predecessor, which blocked any new request going in, and worked it over roughly three months through a 'hundred plus email chain' while aligning internal teams (audit, sensitisation sessions, persons-with-disabilities account openings) and working around the donor's own app-registration requirement. She named the near-quit honestly: 'almost about to quit, like giving up on this donor because it was this back and forth.' She also held a costing line under pressure - the donor wanted to fund only beneficiary-facing programmatic spend, and she pushed back: 'if you don't pay for these administrative expenses, how can the programs run?' She then invited them onsite, resubmitted the proposal, and reported the outcome: 'they became one of our biggest donors that year.' Persistence, calibrated pushback, stated result.",
            "curveBall": "Ugly-problem probe ('nobody else was pointing to') - lapsed donor accounts, first-ask and genuinely unglamorous. She went back to donors who told her 'we haven't heard from you in a year,' and absorbed the hit without deflecting onto her predecessor: 'yes, you didn't hear back from us, but there is a new team now... this is your report, this is where your partnership was left over.' Her own read on why nobody does it: 'lapsed accounts are not considered in that sense.' She also built the fundraising team from scratch, which is the context in which the unowned work landed on her.",
            "microCase": "Discrimination rather than blanket stubbornness: 'I put a strong foot forward... I think I knew where was the right pushback.' She also credits the counterparty's position - the donor was 'right in their own scenario as well' - which keeps the persistence from curdling into grievance. Rating +: two specific instances, one with a named quit-temptation and its answer, one self-initiated ownership of work no one had assigned, both with outcomes."
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": "Covered-a-mistake-unasked question - the Contour Software partnership (a full cycle: funding for training PLUS employment placement for persons with disabilities, 'so it just not getting the monetary value, but also it becomes an empowerment journey'). Mid-meeting, a programmes teammate told the external partner outright that the partnership could not happen, fearing community backlash because the scope started with physical disabilities only. Kanooz built the middle ground live in the room - begin with physical disabilities, then extend to hearing, speech and visual - and named the stake plainly: 'we could have lost this partnership like within that meeting.' She held the correction for the internal debrief rather than contradicting her colleague in front of the partner ('next time we should be more careful and how we speak to external stakeholders'). She shares credit rather than claiming rescue: 'we were the disability expert in that case and Contour Software with their software... they were expert in that situation.'",
            "curveBall": "Quiet-voices probe - real advocacy with a consequence, not a sentiment. She led six fresh graduates she was teaching fundraising from scratch. After a donor-meeting mix-up, the most vocal member lashed out at a softer-spoken colleague who had in fact tried to make contact, and escalated to 'I'm not going to involve her in the event.' Kanooz blocked it directly: 'that's not true. They did try to reach out to you' and 'the kind of reaction you gave was really harsh.' She then carried it into that person's formal evaluation as development feedback on how they give feedback to others - 'because in the moment, you can be harsh and it could lead to the other person thinking more it was on them.' Follow-through past the moment, in writing.",
            "microCase": "Unprompted collective reframe at the end of the stung-feedback story: 'it didn't become about this me versus the other person... we are all one, you know, at the end of the day, we are representing our organization and it's not about this other team versus my team.' REGISTER CHECK (per the calibration lesson from 2026-08-14): both structured answers have her protecting people who report to her, from a position of authority - solidarity flows downward only, and nothing in 39 minutes shows a peer or senior backing HER up, or her following someone else's lead. That is a real gap in mutuality, carried as a debrief probe. Rating held at + rather than +/- because it does not read as patronage: she credits the partner's expertise, de-centres herself in the 'we are all one' line, and her advocacy cost her something socially with her most vocal report. DEBRIEF PROBE: a time a peer or senior covered for her, or she deferred to a teammate's call."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+/-",
            "deepDive": "Recent-upskill question ('which skill have you recently learned to upscale your professional skills and how did you do it') - she answered adjacent to it, with a lesson in stakeholder perspective rather than a skill. She wrote and won a teacher-training grant carrying a digitising-and-scaling element for schools serving children with disabilities. A year in, schools and parents asked for the training to be extended to parents themselves, because 'a lot of parents pull out their children as soon as they see children with disabilities in the school.' Her admission is the substance: 'initially when I was writing this program and getting the funding and adopting it, we never thought about the parents' perspective first.' Changed practice followed - co-creation with parents and students, 'instead of going with a tunnel vision to something.' Real humility and a named blind spot in her own design work.",
            "curveBall": "Not tested - only one question was asked on this value (interview-design note).",
            "microCase": "Learning appetite is genuine and current, though it sits in leisure: manuscript illumination, learned via a course with a colleague in her own time and described with real animation and philosophical curiosity across Islamic and other traditions; reading a book that morning; 'I like to try out new things in my pastime.' She also describes herself as 'very curious and I ask a lot of questions.' WHY +/- AND NOT +: the value is about deliberately getting better at the craft each day with deep humility. What she evidenced professionally is one retrospective insight, not a mechanism - no feedback-seeking practice, no course, no deliberate skill build in her growth or fundraising craft; the genuinely learned new skill is a leisure art form. This is not a penalty for interviewer phrasing (the question was clear and she moved sideways from it), and personal examples were accepted on merit per SOP. With one question on this value the read is thin either way: if the in-room register was stronger than the transcript shows, this moves to + and the card becomes 5(+)/1(+/-). Flagged to Ayesha as the most adjudicable rating on this card; she reviewed and left it at +/-."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": "Hardest-feedback-given - to her own report, on task prioritisation. A delegated donor and stakeholder report had been pending two weeks after an initial check-in. She scheduled a 1:1 and led with diagnosis rather than verdict - asking what the bottlenecks were, whether data from the programmes team or other stakeholders was holding it up - then made the actual point: a ten-minute letter to a government body should not sit behind a two-week report. 'That task should not be pending because you were working on a report for two weeks.' She also named the resistance she was pushing against: 'a lot of people come in with that mindset that I just need to focus on one task and get it done.'",
            "curveBall": "Two probes, both answered well. (1) The follow-up 'why was it hard for YOU?' produced the most revealing moment of the call - she located the friction in herself rather than in the report: small team, volume arriving from multiple angles, and she could see the effort. 'I could see they're also putting in an effort to do their tasks, but... the pressure is coming on from multiple angles. So I feel like that's where I could empathize with them... but then as a manager, I had to do that.' She also revealed she runs the same prioritisation ritual upward with her own line manager. Candid, not a performance of decisiveness. (2) Feedback-received-that-stung-and-was-true: a high-net-worth-individual visit that went 'terribly wrong.' Another team's member had circulated the full day timeline, so she stayed out of it; her manager challenged her directly on why she had not looked at it, given the visit tied to funding and a proposal would follow. It stung, she sat with it, and landed on the concrete fix - 'I could have just taken out five minutes of my day and did a check-in with this person and made sure everything is aligned' - reframing it away from 'me versus the other person.' Owned without defensiveness or blame-shifting.",
            "microCase": "Instinct for timing and setting: the corrective feedback to the Contour colleague went into the debrief rather than the meeting; the harsh-reaction feedback went both to the person's face and into the written evaluation rather than being let slide. Rating +: both directions evidenced, with specific people, actual words, the discomfort named, and follow-through."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "Handed-off-a-project question (she asked for it to be repeated - see interview feedback). At KDSP she was the only person in the team who knew grant writing, and she handed a grant she was leading to a teammate whose policymaking background suited the provincial disability-policy angle better - 'because they could do it better with their lens... what makes sense to propose' - and stepped back to oversight, 'rather than me doing the entire thing by myself.' She released the exact capability that made her singular on that team. CAVEAT: the story itself is thin - no outcome stated (did the grant land?), no cost or discomfort named, and the sentence trails off.",
            "curveBall": "Not tested - only one question was asked on this value (interview-design note).",
            "microCase": "Three further, independent instances of releasing appear elsewhere in the transcript, and the + rests on the pattern rather than the one story: (1) redesigning her own programme once parent feedback contradicted her original design - letting go of being right about her own work; (2) trading the full-scope Contour partnership for a staged one; (3) resigning her position to redirect toward growth work. She also frames her self-description around movement and re-contexting - Saudi, then the US for macro social work, then here - 'going around to different contexts and people.' DEBRIEF PROBE: a handover that actually cost her something, with its outcome."
        },
        {
            "name": "Practice Joy",
            "rating": "+/-",
            "deepDive": "Silly-ritual question, with food treats explicitly ruled out - she offered silly icebreaker questions in meetings ('if they could eat one food for the rest of their life, what would they do'), and she already runs them rather than inventing one for the interview. Her read on why they work is observant: answers split between 'bohat analytical ho jate hain' and 'kuch ke bohat hee simple hain,' and it becomes a running joke by the end. She has evidence it lands, which is exactly what the question tested - people who attended her Islamabad fundraising sessions later remembered the icebreaker over the content: 'they remember important elements, but they all talked about this icebreaker question you brought in, what was that?' She is also unbothered by the pushback it draws ('why are you even asking this question... I'm like, this is just an icebreaker').",
            "curveBall": "Emoji question - the thinking/pondering face, for curiosity: 'I'm very curious and I ask a lot of questions... even people around me understand that and they see that curiosity.' Honest and consistent with everything else she said about herself (systems thinking, manuscript illumination, asking questions), but it is a cognitive self-image, not a joy or warmth register.",
            "microCase": "Real lightness in the call itself: opened with 'Alhamdulillah,' volunteered that she had woken up and read her book that morning, and lit up describing the illumination course - 'an absolute amazing thing.' No flatness or dread anywhere in 39 minutes. Rating +/-: the value is exhibited but the register is thin and low-invention - an icebreaker question sits close to the traditional category the question tried to exclude, and her own example is (mildly ironically) food-based; asked directly about herself she went to curiosity rather than to fun, energy or warmth; and beyond the icebreaker there is no evidence of her being a source of lightness for a team."
        }
    ],
    "finalComments": "PASS - 4(+) / 2(+/-) / 0(-) (threshold: zero minuses AND <=2 plus-minus; >=3 plus-minus = OUT, not triggered). A well-evidenced interview: every structured probe returned a named incident with stakes, actions and a stated outcome, and she twice named her own blind spot unprompted (the parents' perspective she had not designed for, the visit she assumed was handled). The two +/- ratings are Continuously Improve (answered adjacent to the question - a retrospective insight rather than a deliberate craft-improvement mechanism) and Practice Joy (real but low-invention register; curve-ball moved to curiosity rather than joy). TRANSCRIPT NOTE: speaker labels are flipped in roughly a dozen places (the value definitions appear under her name and vice versa, e.g. 3:40, 17:42, 21:43, 27:34, 35:15) - attribution read by sense per the fairness rule, and nothing scored on ambiguous text. FLAGS: (1) PRIOR REJECTION - she was rejected on Job 41 (Growth Manager - Karachi), application 3811, in the 20 July 2026 batch with NO rejection reason recorded, then reapplied to Job 42 on 9 Aug 2026 and was shortlisted; worth establishing why she was a no there before the debrief (may have been band or seniority rather than substance - Markaz does not say). (2) CURRENTLY BETWEEN ROLES - she resigned recently with nothing named as lined up ('actually, I'm a bit free now'; 'in order to align more with my growth, I actually resigned recently from my current company'); availability is immediate, but the reason for leaving without a next step is worth one question. (3) SALARY EXPECTATION NOT COLLECTED - nothing in this call and questions_answered is empty on her Markaz record; needs collecting before the debrief given where the Job-42 band sits. (4) ALL FOR ONE MUTUALITY GAP - every solidarity story runs downward from her authority; probe a time a peer or senior covered for her, or she deferred to a teammate's call. (5) TWO VALUES CARRY ONLY ONE QUESTION EACH (Continuously Improve, Don't Hold On), so both ratings rest on a single answer plus incidental evidence. (6) SECTOR FIT is in-band for the validated SMG persona - external-facing impact/donor-org partnership hunting (NOWPDP, KDSP) - though her track is disability inclusion rather than edtech B2G, which the case study can test. GWC - ALL THREE PROBE: Gets it PROBE, positive lean (strong sector adjacency: macro social work with an explicit systems lens - 'I really think in systems and how much systems enable us' - plus education and disability inclusion, teacher training at school scale in Pakistan, government-body correspondence, donor and corporate partnerships; but Taleemabad itself never came up once - not our model, not the schools we serve, not what drew her). Wants it PROBE (real behavioural signal: she resigned her role and rewrote her CV for this position - resume file 'Kanooz Siddiqui Resume - Taleemabad_SMG..pdf' - and applied via the career page; against that, no articulated why-Taleemabad, and at the close she had no questions about the role, team or mission, her single question being the timeline for next steps). Capacity PROBE (evidenced: built a fundraising team from scratch, managed and trained six fresh graduates, revived lapsed donor accounts, closed a major banking-sector donor across a three-month grind, wrote and won a teacher-training grant, negotiated a corporate training-to-employment partnership, and can hold a costing negotiation on admin-versus-programmatic spend. NOT evidenced in-call: any deal sizes or revenue figures, institutional/B2G closure at scale, or a growth target she personally owned - the case study must test the SMG pillars). Next step if advancing: SMG case study ('Execution Sprint'), then case study debrief with the hiring manager.",
    "proceedToRightSeat": "Yes"
}

# ---- Guards: confirm the exact candidate + application + position before writing ----
pre = q("""SELECT a.id AS app_id, a.candidate_id, a.job_id, a.status,
                  c.first_name, c.last_name, c.email,
                  j.job_id AS jid, j.title,
                  (a.values_scorecard IS NULL) AS scorecard_empty
           FROM applications a
           JOIN candidates c ON c.id = a.candidate_id
           JOIN jobs j ON j.id = a.job_id
           WHERE a.id = $1""", [APP_ID])
assert len(pre) == 1, f"Guard failed: application {APP_ID} not found - ABORTING"
row = pre[0]
assert row["candidate_id"] == CAND_ID, f"Guard failed: app {APP_ID} belongs to candidate {row['candidate_id']}, expected {CAND_ID} - ABORTING"
assert row["job_id"] == JOB_ID, f"Guard failed: app {APP_ID} is on job {row['job_id']}, expected {JOB_ID} - ABORTING"
assert row["email"] == EMAIL, f"Guard failed: email mismatch {row['email']} != {EMAIL} - ABORTING"
assert row["title"] == "Senior Manager Growth", f"Guard failed: position is {row['title']} - ABORTING"
assert row["scorecard_empty"], f"Guard failed: app {APP_ID} already has a values_scorecard - ABORTING"
print("Guards passed:", json.dumps(row, indent=2))

# ---- Guarded UPDATE ----
rows = q("""UPDATE applications
            SET values_scorecard = $1::jsonb,
                values_interview_result = 'pass',
                values_interview_score = 4,
                values_interview_date = '2026-08-18',
                values_interviewer_name = 'Ayesha Khan',
                updated_at = NOW()
            WHERE id = $2 AND job_id = $3 AND candidate_id = $4 AND values_scorecard IS NULL
            RETURNING id, status, values_interview_result, values_interview_score""",
         [json.dumps(scorecard), APP_ID, JOB_ID, CAND_ID])
assert len(rows) == 1, f"Expected exactly 1 row updated, got {len(rows)} - INVESTIGATE"
print("Scorecard submitted:", rows[0])

# ---- Verify ----
verify = q("""SELECT a.id AS app_id, c.id AS cand_id, c.first_name, c.last_name, c.email,
                     j.job_id AS jid, j.title,
                     a.status, a.values_interview_result, a.values_interview_score,
                     a.values_interview_date::text AS vi_date, a.values_interviewer_name,
                     a.values_scorecard->>'candidateName' AS sc_name,
                     a.values_scorecard->>'host' AS sc_host,
                     a.values_scorecard->>'date' AS sc_date,
                     a.values_scorecard->>'proceedToRightSeat' AS proceed,
                     jsonb_array_length(a.values_scorecard->'values') AS n_values,
                     (SELECT string_agg(v->>'rating', ' ' ORDER BY ord)
                        FROM jsonb_array_elements(a.values_scorecard->'values')
                             WITH ORDINALITY t(v, ord)) AS ratings
              FROM applications a
              JOIN candidates c ON c.id = a.candidate_id
              JOIN jobs j ON j.id = a.job_id
              WHERE a.id = $1""", [APP_ID])
print("Verify:", json.dumps(verify[0], indent=2))
