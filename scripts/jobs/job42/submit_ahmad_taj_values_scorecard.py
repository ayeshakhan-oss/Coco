# -*- coding: utf-8 -*-
"""Submit Muhammad Ahmad Taj's values scorecard — Job 42 Senior Manager Growth, app 3971.
Zero In Call 2026-08-17 (52 min, host Ayesha Khan). Verdict PASS 4+ / 2± / 0−.
Approved by Ayesha 2026-08-17 after reviewing the full card in chat.

Duplicate check done 2026-08-17 (Irfan lesson — name AND email AND phone): candidate 3213
is the only Ahmad Taj on Markaz; app 3971 is his only application; values_scorecard IS NULL.
No candidate insert, no application insert — record already exists.

Guarded UPDATE only: values_scorecard IS NULL + candidate/job match + row-count assert.
Uses Neon HTTPS SQL API (port 5432 blocked on this network).
"""
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

JOB_ID = 42
APP_ID = 3971
CAND_ID = 3213


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=120)
    r.raise_for_status()
    return r.json()["rows"]


scorecard = {
    "date": "Aug 17, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "Coco (AI P&C Assistant)",
    "candidateName": "Muhammad Ahmad Taj",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": (
                "Two distinct hard-thing examples, both with mechanism and a number. "
                "(1) Gaming business shutdown: a State Bank of Pakistan blockage killed the "
                "revenue line. He proposed an unconventional structure, carried it through "
                "8-10 iterations against 'a lot of friction, a lot of resistance', secured "
                "approval for a first tranche, onboarded a major international partner, and "
                "moved revenue from ~300K to ~1500K in three to four months - while the team "
                "was being cut. (2) Declining portfolio nobody would take: his manager had "
                "'already asked a few people around and nobody was willing to take that, "
                "because it was on a decline trend'. He took it, sat with the partner to find "
                "the gaps, built an engagement-funnel dashboard to locate the drop-off, changed "
                "a journey design, added a feature in the conversion funnel, and profiled ARPUs "
                "- turning decline into +5% growth in four months."
            ),
            "curveBall": (
                "He chose the second one knowing others had already refused it, and volunteers "
                "the hard version of both stories rather than the flattering one."
            ),
            "microCase": (
                "FLAG for debrief (not a scoring input): he said the solution 'needed to bypass "
                "the policies' and 'did not align with the set structure or the running model'. "
                "It did go to the chief for approval, so not unilateral - but for a role selling "
                "into government and regulated buyers, where he draws the line between creative "
                "structuring and circumventing a rule needs testing."
            ),
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": (
                "Three separate instances. (1) Covered silently: during a PTA regulator exercise "
                "a colleague was making repeated errors in official communications; he rewrote "
                "the drafts and asked the colleague to resend - 'I did not tell him why I am "
                "doing this or helping him out, because I just wanted to cover... I did not want "
                "any consequence... or that colleague would come under fire.' (2) Protected "
                "effort: a team member entered wrong information on a submission form; he "
                "corrected it himself 'so it does not undermine the effort that she put in', "
                "then coached her on reviewing inputs after submission. (3) Spoke for people who "
                "could not: placed in Telenor's Open Mind programme, he carried colleagues' "
                "concerns to management; when his division needed a People Council "
                "representative and nobody volunteered ('I was hoping somebody else would as "
                "well, but nobody did'), he contested and won, then secured fuel cards for job "
                "groups that had none, raised medical allowances and obtained cafe discounts, "
                "using a monthly session with the Chief People Officer as the channel."
            ),
            "curveBall": (
                "Register check: 'help those people who can't voice their opinions' would "
                "normally read as patronage, but he places himself inside the group - 'I'm a "
                "similar type of person. I'm an introvert, sort of' - and was in that programme "
                "himself. He speaks from within, not above. Rating held at + on that basis."
            ),
            "microCase": (
                "PROBE: with the colleague he fixed it and said nothing, so the colleague never "
                "learned; with his own team member he did follow up and coach. Which is his "
                "default when the person is not his report?"
            ),
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+/-",
            "deepDive": (
                "The thinnest answer of the six, noticeably so against the mechanism-rich detail "
                "everywhere else. Asked which skill he had recently learned or polished, he "
                "named people management - a domain, not a skill. Evidence offered was an "
                "outcome (promoted a team member, set their KPIs, team beat targets by over 30%) "
                "plus 'reading about stuff online'. No named course, book, framework, mentor or "
                "specific practice he changed."
            ),
            "curveBall": (
                "Genuine humility is present and unprompted: 'Nobody is a perfect people "
                "manager', 'managing people is the hardest thing I have ever come across in my "
                "career - actually doing the work is very easy now.'"
            ),
            "microCase": (
                "Held at +/- because the humility and the outcome are real but there is no "
                "evidence of DELIBERATE skill acquisition, which is what the value asks. "
                "PROBE: name one specific thing you changed in how you manage in the last six "
                "months, and what prompted it."
            ),
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": (
                "Both directions evidenced. RECEIVING is the stronger half and is genuinely "
                "vulnerable: his manager sat him down for thirty minutes and told him he was not "
                "giving accurate answers, was not fully owning the project, and 'lack[ed] the "
                "skills to lead the team, lead this project'. He repeats that judgement about "
                "himself without softening it and adds 'I would not go into the more harsher "
                "ambits of it'. He did not accept it at first - 'at the time, I did not "
                "comprehend it' - took the weekend, said 'it was not a good weekend', and "
                "concluded 'this guy is only trying to help me, to grow me'. GIVING: told a team "
                "member their presentation and PowerPoint skills were not at C-level standard - "
                "the third time he had raised it - paired with concrete support: a checklist, "
                "guidelines, an offer to switch tools (Canva), and 'take a day off, reflect, come "
                "back fresh'. He names his read honestly: the team member 'was being actually "
                "complacent about it'."
            ),
            "curveBall": (
                "He is candid about the delivery conditions of the feedback he received "
                "('we had 30 minutes') and does not use that as a defence."
            ),
            "microCase": (
                "ROLE-FIT GAP, deliberately NOT scored against this value: his hardest-ever "
                "feedback was downward, to a junior, about slide-making. Nothing in the "
                "transcript shows him challenging a peer or a senior. The SMG is 2IC to the Head "
                "of Growth and the JD requires flagging misalignments early - that ability is "
                "untested. Belongs in the debrief. PROBE: tell me about a time you told someone "
                "more senior than you that they were wrong."
            ),
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": (
                "A clean change-of-behaviour story with a named prior belief. 'I have this knack "
                "of being a perfectionist' - as a new manager he did everything himself for "
                "months rather than delegate. His manager told him to stop. He then handed a "
                "team member complete ownership of the UX and design lead on a platform he had "
                "built from ideation, keeping only legal and financials. The Chief Executive "
                "praised the design directly to the team member and the designers, and it was "
                "rolled out to core products."
            ),
            "curveBall": (
                "The reflection earns the plus: 'in my mind at the time, I thought delegating a "
                "task would be delayed, or it would not be done in a certain way which I want "
                "to. But I actually learned that you need to accept other people as well, how "
                "other people operate.' He also let the credit land on someone else and "
                "described that as the moment he felt proud."
            ),
            "microCase": (
                "Note: the change was prompted by his manager rather than self-initiated. He "
                "acted on it and internalised it, which is what the value asks."
            ),
        },
        {
            "name": "Practice Joy",
            "rating": "+/-",
            "deepDive": (
                "Offered Mafia in a circle, then hiking or paddling with randomised pairings. "
                "The randomisation reasoning is sound - 'if I know a colleague, I would always "
                "choose that colleague... it would still be in a comfort zone' - so he mixes "
                "groups deliberately."
            ),
            "curveBall": (
                "The framing is the problem. His stated reason for Mafia is diagnostic, not "
                "joyful: 'it actually shows a lot about the person. Is the person aggressive? Is "
                "the person calm? Is the person a good liar?' Both activities close on 'so I "
                "could know everyone in a better way'. He turned a joy question into an "
                "assessment exercise - a team game as a read on people rather than as fun."
            ),
            "microCase": (
                "Also, the value is about joy in daily working life; both answers are offsite "
                "events. PROBE: what makes an ordinary Tuesday in your team enjoyable?"
            ),
        },
    ],
    "finalComments": (
        "PASS - 4(+) / 2(+/-) / 0(-). Strong, evidence-dense interview from someone who reaches "
        "for specifics without prompting and attaches numbers to outcomes. The two standout "
        "signals are turning around work other people had refused (a State Bank-blocked revenue "
        "line taken from ~300K to ~1500K in 3-4 months; a declining portfolio nobody would touch "
        "moved to +5% growth in 4 months) and a genuinely non-defensive account of harsh feedback "
        "- he repeats a damaging judgement about himself ('lack the skills to lead this project') "
        "and does not argue with it. All for One is broad and real: covering a colleague's "
        "regulator communications without telling him, protecting a team member's effort, and "
        "winning a People Council seat nobody else wanted then delivering fuel cards and higher "
        "medical allowances. The two +/- are narrow: Continuously Improve is thin on deliberate "
        "learning inputs despite obvious self-awareness, and Practice Joy is answered "
        "instrumentally (team games framed as a way to read people). THE OPEN QUESTION FOR "
        "DEBRIEF IS NOT A VALUE - it is whether he can push back UPWARD. Every example of courage "
        "runs downward to his team or inward on himself; for a 2IC expected to flag misalignments "
        "to a Head of Growth, that is untested. Also probe the 'it needed to bypass the policies' "
        "line from the Hard Things example - it went through the chief for approval, but the "
        "boundary matters in a B2G role. UNCOLLECTED: salary expectation was not discussed on "
        "this call. NOT A FACTOR IN THIS EVALUATION: he disclosed a stammer unprompted at the "
        "outset; he has presented to C-level audiences consistently and led those sessions. It "
        "has no bearing on any rating here and must not appear in any downstream note. EVIDENCE "
        "CAVEAT: the Fathom transcript is poor in places - it renders his name variously as "
        "'Hemant', 'Evan', 'Ahmed' and 'Emil' and several exchanges are garbled; this reading is "
        "grounded in the intact passages. Confidence: Medium-High."
    ),
    "proceedToRightSeat": "Yes",
}

# ---- guards ----
pre = q("""SELECT a.id, a.candidate_id, a.job_id, a.status, a.values_scorecard IS NULL AS empty,
                  c.first_name || ' ' || COALESCE(c.last_name,'') AS name, c.email
           FROM applications a JOIN candidates c ON c.id = a.candidate_id
           WHERE a.id = $1""", [APP_ID])
assert len(pre) == 1, f"app {APP_ID} not found"
assert pre[0]["candidate_id"] == CAND_ID, f"candidate mismatch: {pre[0]}"
assert pre[0]["job_id"] == JOB_ID, f"job mismatch: {pre[0]}"
assert pre[0]["empty"], "values_scorecard already populated - ABORTING (never overwrite)"
print("Pre-check OK:", pre[0])

dup = q("""SELECT id, job_id FROM applications WHERE candidate_id = $1""", [CAND_ID])
assert len(dup) == 1, f"candidate {CAND_ID} has multiple applications {dup} - resolve before writing"
print("Duplicate check OK: single application", dup)

# ---- guarded update ----
rows = q("""UPDATE applications
            SET values_scorecard = $1::jsonb,
                values_interview_result = 'pass',
                values_interview_score = 4,
                values_interview_date = '2026-08-17',
                values_interviewer_name = 'Ayesha Khan',
                updated_at = NOW()
            WHERE id = $2 AND job_id = $3 AND candidate_id = $4 AND values_scorecard IS NULL
            RETURNING id, status, values_interview_result, values_interview_score""",
         [json.dumps(scorecard), APP_ID, JOB_ID, CAND_ID])
assert len(rows) == 1, f"Expected exactly 1 row updated, got {len(rows)} - INVESTIGATE"
print("Scorecard submitted:", rows[0])

verify = q("""SELECT a.id AS app_id, c.first_name, c.last_name, c.email, a.status,
                     a.values_interview_result, a.values_interview_score,
                     a.values_interview_date::text AS values_date, a.values_interviewer_name,
                     a.values_scorecard->>'candidateName' AS sc_name,
                     a.values_scorecard->>'proceedToRightSeat' AS proceed,
                     a.values_scorecard->>'host' AS host,
                     jsonb_array_length(a.values_scorecard->'values') AS n_values
              FROM applications a JOIN candidates c ON c.id = a.candidate_id
              WHERE a.id = $1""", [APP_ID])
print("Verify:", json.dumps(verify[0], indent=2))

ratings = q("""SELECT v->>'name' AS name, v->>'rating' AS rating
               FROM applications a, jsonb_array_elements(a.values_scorecard->'values') v
               WHERE a.id = $1""", [APP_ID])
print("\nRatings:")
for r in ratings:
    print(f"  {r['rating']:4s} {r['name']}")
plus = sum(1 for r in ratings if r["rating"] == "+")
pm = sum(1 for r in ratings if r["rating"] == "+/-")
minus = sum(1 for r in ratings if r["rating"] == "-")
print(f"\nTally: {plus}(+) / {pm}(+/-) / {minus}(-)")
assert (plus, pm, minus) == (4, 2, 0), "tally does not match the approved card"
print("DONE")
