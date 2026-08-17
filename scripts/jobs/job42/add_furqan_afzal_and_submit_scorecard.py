# -*- coding: utf-8 -*-
"""Create Furqan Afzal's Markaz record (Job 42 - Senior Manager Growth) and submit his values
scorecard (PASS 4+/2+-/0-). Approved by Ayesha 2026-08-14 (card confirmed after her adjudication
of All for One from + down to +/-; CV + salary bracket provided same day).

Duplicate check done 2026-08-14 (Irfan lesson - name AND email AND phone): NO existing record
(only Furqans on Markaz are Furqan Jan and Muflah Ul Furqan - different people).
This script:
  1. Inserts the candidate (profile from his CV; resume PDF from Downloads)
     - guards: email not present; phone not present
  2. Inserts the application on job 42, status 'shortlisted' (guard: no existing app)
  3. Fills the values scorecard via guarded UPDATE (values_scorecard IS NULL, row-count assert)
Uses Neon HTTPS SQL API (port 5432 blocked on this network)."""
import os, json, base64
import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

JOB_ID = 42
EMAIL = "fafzal98@gmail.com"
PHONE = "+923135846676"
CV_PATH = r"C:\Users\Dell\Downloads\Furqan_Afzal_-_Growth_Marketing_Manager.pdf"


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
    "candidateName": "Furqan Afzal",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Almost-quit question - a named project with real stakes: the GSMA Climate Adaptation Fund bid at Weather Walay as an INTERN, expected to help win 250,000 pounds on a PKR 14,000 salary, 'working day and night,' with 'C-level executives that were quite toxic undermining my efforts,' family pressure, and deteriorating health. Honest that quitting was live: 'there were many instances in my head where I felt... I was just getting too burnt out.' What kept him in: faith, explicitly ('faith is basically the main reason why I have a high tolerance when it comes to hard trials') plus perspective ('this is not as hard as I faced in previous times'). He also volunteered his boundary unprompted: at a UJAS product launch he was 'pretty much cursed at by internal stakeholders' and left - 'I won't continue a project when it comes to a compromise of self-dignity and self-respect.' Recorded as stated: he distinguishes hard work (stays) from abuse (walks), and named the line himself. CV corroboration: he ultimately SECURED the 250,000-pound GSMA Innovation Fund grant as the sole Pakistani recipient, then led delivery of a 250-station weather monitoring network.",
            "curveBall": "Ugly-problem probe - strong and current: at Pakistan TV Digital (a startup under PTV with NO HR), team members were making 'vulgar remarks' about colleagues including his assistant, and the person doing it was 'very influential... the daughter of a very renowned journalist' with two decades of experience. 'I knew I was going to get fired if I brought it up.' He took it to the editor-in-chief and manager anyway - 'respectful... without any aggression... I was the only one who actually stood up' - and weeks later was appreciated for it. Named risk, named power asymmetry, action taken, outcome.",
            "microCase": "The intro carries the same spine unprompted: only child supporting elderly parents, refused his father's 25-year Schlumberger referral to start 'only from my own efforts... to teach [my kids] about the beauty of trial,' landed at Weather Walay as its sixth employee before graduating, through COVID, health issues, and a university administrative mess. Rating +: two specific instances - one with a named quit-temptation and its answer, one self-initiated ownership of an unowned problem at personal risk with outcome."
        },
        {
            "name": "All for One & One for All",
            "rating": "+/-",
            "deepDive": "Covered-a-mistake question ('without them asking you to'): first response was philosophy, not incident - 'I've done it many times... I'll absorb all the pressure. I'll absorb all the mistakes.' The interviewer had to press directly ('can you quote me any example?') before a concrete one appeared: his assistant, six months into her first digital-marketing job, mismanaged the ads budget while covering his two-month medical absence, and breached a state-broadcaster editorial guideline (the Kashmir terminology rule). His cover: 'she is just six months into her job... we have about 50 years of experience combined. It's very unfair to just throw someone under the bus.' FOR him: once prompted the incident is real and specific, and he described bearing a personal cost for covering her (ridicule, workplace 'accusations... that I have a relationship with my assistant') and kept covering anyway. AGAINST him - three things that hold this at +/-: (1) He himself framed it as duty, three times: 'It is my job. It is my job... that's just a given role for a manager.' The question probes solidarity BEYOND the role; manager accountability for your own trainee is the baseline, and he categorized his own behavior as exactly that baseline. (2) The telling contradicted the claim: to demonstrate protecting his assistant, he itemized her failures at length to an outside interviewer ('she's messed up the overall budget... she has made many critical mistakes') plus her personal context (a 'political background,' a father who 'is always in touch with me'). Shielding someone inside the organization while cataloguing her mistakes and family circumstances outside it is a live counter-signal for a value about making people feel safe and backed. (3) The register across the whole value is one-directional patronage, not unity: I cover, I absorb, I teach - and they thank me, apologize to me, promise to make me proud ('on a daily basis, I'm covering for someone else'; 'I've been told I'm a type four leader'). All-for-one describes peers holding each other up in both directions; every instance offered flows downward from him to a subordinate.",
            "curveBall": "Quiet-voices probe - his strongest advocacy story, first-ask: at a company he deliberately declined to name, female employees facing harassment 'always came to me and just vented out... hearing the stories really boiled my blood.' He 'put up a case against the management,' argued it personally ('how would you feel if someone made comments about your daughter?'), and reported an institutional outcome: harassers removed, 'a few managers let go as well.' FOR: first-ask, real moral stakes, specific and plausible persuasion mechanism, and being the person women trusted is itself a signal. HOLDING IT BACK: every element is anonymized - no company, no people, no timeframe - and the claimed outcome is large with nothing checkable attached; a strong claim told well, softer as evidence than its drama. It also repeats the Question-1 pattern: he is the sole hero of the account.",
            "microCase": "Why +/- and neither + nor -: not a plus because + requires CONSISTENT CLEAR evidence - here one probe produced a duty-framed incident only after prompting whose telling undercut the protective claim, the other a fully anonymized story with an unverifiable outcome, both one-directional (patron to subordinate/victim), neither showing mutual peer-level back-each-other-up. Not a minus because the evidence exists and the care is visibly genuine - the Kashmir incident happened with a real accepted cost, and the harassment advocacy even anonymized is more than nothing. Real but inconsistent/off-center = textbook +/-. ADJUDICATION NOTE: initially rated + on evidence count; revised to +/- after Ayesha's in-room read flagged the register - re-examination confirmed the three counter-signals above. DEBRIEF PROBE inherited: one instance of backing a PEER or a SUPERIOR (solidarity where he was not the patron and had no duty of care), and one instance where someone covered for HIM."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Recent-upskill question - specific, current, applied: learning Claude Code right now, to automate an infographic pipeline for the LinkedIn page 'instead of overburdening my graphic designer,' having studied how other teams built systems around it ('Claude does not have a good reputation when it comes to designing graphics, but there's a way around it'). Beyond that, a deliberate tool-per-department map he is teaching himself despite not being on those teams: 'Higgs Field AI for the video team... Perplexity for research purposes, Claude for creativity, Higgs Field for video generation, and Notion for team collaboration.'",
            "curveBall": "Not separately tested (single-probe value this call; interview-design note).",
            "microCase": "The learning register recurs: self-development named in his leisure time, freelance growth consulting at Teacher Resource Center taken on as a stretch, Executive MBA completed Jan 2026 alongside the PTV role (CV), and in the feedback value he responded to a sting by auditing his own work and asking other managers 'tell me where am I doing wrong so that I can improve myself.' Rating +: named tools, named use case, current, altruistically motivated, corroborated."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": "Hardest-feedback-given - a real conversation with a named dynamic: his assistant kept talking over him; he told her directly 'you have to calm down a bit. I know that outside the office we might be friends, but at the office I am her boss regardless.' She 'felt as if I was trying to put her down,' so he did the repair work: explained the intent ('when I'm absent, I want you to be able to handle everything... advance your career, and in fact even surpass me'), kept giving critical feedback, and described the trust arc honestly - 'the more fair I am to her... the more the trust develops. Now she understands.' Delivery, rupture, repair, outcome.",
            "curveBall": "Feedback-received-that-stung - Weather Walay, age 22-23: a manager told him 'you might think that you're aware of yourself, but you still have a lot to learn and you're not doing good enough' while he was working day and night. Owned his reaction plainly: 'I did react to it... I was very naive back then.' Then a week of processing: audited his own work ('perhaps I'm too slow... perhaps I'm not showing my work'), consulted other managers for corroboration, and landed on a genuine insight - 'I realized I was being too humble. I have to be more vocal about my efforts.' Sting, owned reaction, reflection, named behavior change.",
            "microCase": "The PTV ugly-problem stand (value 1) is itself a courageous conversation held upward against an influential person at stated risk of firing. Rating +: both directions evidenced with specific people, actual words, reception, and change."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "Handed-off-a-project question - three named releases, honestly narrated: after his spine surgery three-four months ago he gave up (1) the website revamp, handed to a news editor 'who doesn't have any experience in web development, but has more news-industry experience than me'; (2) the traditional marketing side (Islamah Talks campaign, vendor/guest/influencer partnerships) to the newly hired partnerships manager; (3) the recruitment he was meant to lead. Named the attachment without airbrushing: 'that stung me as well. I thought I could work from home... and it still stings me a bit to this day.' Outcome witnessed with pride rather than resentment: 'today, as we speak, our new website is being launched by my team member who is no longer part of my team... the results are happening in front of my eyes. That's where I felt I took the right decision.'",
            "curveBall": "Not separately tested (single-probe value this call; interview-design note).",
            "microCase": "The choice inside the constraint was his: colleagues urged him to delegate and he chose FULL handover ('delegate your product to people completely') over clinging via work-from-home, to refocus on his actual mandate (user acquisition) and his health. Rating +: the trigger was circumstance (illness), noted honestly - but the behavior is the value's exact shape: named attachment, complete release, endorsed outcome, ongoing sting acknowledged without reversal."
        },
        {
            "name": "Practice Joy",
            "rating": "+/-",
            "deepDive": "Silly-ritual question (explicitly non-traditional): answered with honest self-knowledge rather than a ritual - 'to be very fair, I'm quite a shy guy when it comes to these traditional team rituals - I've seen people dancing and I don't do that at all. I don't do music as well.' His alternative is real and evidenced: individual and small-group lunches out 'on a random occasion,' one-on-one connection over collective performance - with observed impact he could cite from this week: 'the past three days, I got calls from two to three different members... the way you take care of us, that's more than enough... naturally, my team members are punctual, they update me on the go.' His critique of the samosa-party model was thoughtful: 'everybody wants a human connection... there are different personas that want a one-on-one relation.'",
            "curveBall": "Emoji question: the MELTING SMILEY - and his reason is the most revealing sentence of the interview: 'I'm always fighting with fire, but I'm always smiling and hiding everything... there were many times I felt I was actually melting due to the insane amount of pressure from many different managers, many different expectations, even from my own family as well. And I was just smiling and dropping, dropping, dropping... giving a thumbs up like the Terminator.'",
            "microCase": "Rating +/-: the care-based connection he practices is genuine and demonstrably lands - real positive-environment evidence. But the question asked what joy he would INTRODUCE, and his honest answer is that playful/fun rituals are not him; and the emoji he chose describes concealed strain, not joy. Evidence of warmth: yes. Evidence of infusing fun as this value defines it: not shown."
        }
    ],
    "finalComments": "PASS - 4(+) / 2(+/-) / 0(-) (>=3 plus-minus = OUT, not triggered). A high-evidence interview: nearly every probe returned a named incident with stakes, actions, and outcomes, and he repeatedly named his own costs and flaws unprompted (the reaction to feedback, the sting of letting go, the shyness about rituals). ADJUDICATION RECORD: All for One was initially rated + on evidence count and revised to +/- after Ayesha's in-room read flagged the register; re-examination confirmed three counter-signals (duty-framing, exposing the protected colleague in the telling, one-directional patronage) - full rationale in that value's entry. FLAGS (observed words only, no inference): (1) WELLBEING / SUSTAINABLE-PACE - the melting-emoji answer ('always smiling and hiding everything... melting due to the insane amount of pressure'), said by an only child supporting elderly parents, working six days a week at PTV, four months out from spine surgery, while freelancing on the side; not a values deduction - his candor is to his credit - but if he advances, have a real conversation about workload; he named the exact boundary that burns him: presence-theater ('someone expecting me to work 10-11 hours even though I've completed all my tasks in three'). (2) EVIDENCE CONCENTRATION on one relationship: his assistant features in covered-mistake, hardest-feedback-given, and ugly-problem answers (including his own mention of workplace 'accusations' about the two of them, raised by him as a cost of covering); debrief should probe team-breadth examples beyond this dynamic, plus the peer-solidarity probe from the All-for-One entry. (3) SALARY: expected bracket provided via Ayesha 2026-08-14 - PKR 300,000 (gross) to 400,000 (take-home); sits at/above the top of the Job-42 band (350-400k) on the take-home end - confirm structure (gross vs take-home) at the debrief. (4) CASE-STUDY TIMING pre-agreed: he works Saturdays at PTV and asked to take the case study over a weekend with a fresh mind - accommodated in-call. TRANSCRIPT NOTE: attribution flips at the start and a few garbled stretches - fairness reading applied, nothing scored on garbled text. GWC: Gets it - PROBE, positive lean (probed the role definition proactively - could not find the JD on the website, characterized the role as 'the second guy to the CEO... advisor kind of job'; TRC (Teacher Resource Center) freelance growth-consulting is genuine education-sector exposure; detailed practical questions about timings/remote/overtime/commute show he is seriously imagining working here; mission/B2G engagement untested). Wants it - PROBE (sourced via Ayesha's LinkedIn outreach; why-Taleemabad never articulated; closing questions centered on compensation, perks, and working conditions; real interest signals present - JD hunger, case-study scheduling - motivation direction untested). Capacity - PROBE (evidenced: ground-up startup growth as 6th employee at Weather Walay - scaled a Jazz-partnered app to 3.8M paying subscribers in 2 years at ~PKR 6 CPA, 250,000-pound GSMA grant SECURED as sole Pakistani recipient with 250-station delivery per CV; current PTV Digital lead - 6-person team, PKR 3M/month budget, 0 to 439K social audience in 12 months; education-sector consulting at TRC; Executive MBA FAST-NUCES Jan 2026; strong AI-tooling adoption. NOT evidenced in-call: institutional/B2G deal closure of the NIETE type and long-cycle government partnerships - the case study must test the SMG pillars). Next: SMG case study ('Execution Sprint'), weekend delivery as agreed in-call.",
    "proceedToRightSeat": "Yes"
}


# ---- Step 0: guards ----
dup_email = q("SELECT id FROM candidates WHERE email = $1", [EMAIL])
assert not dup_email, f"Guard failed: email already exists: {dup_email} - ABORTING"
dup_phone = q("SELECT id, first_name, last_name FROM candidates WHERE regexp_replace(phone,'[^0-9]','','g') LIKE '%' || $1", ["3135846676"])
assert not dup_phone, f"Guard failed: phone already exists: {dup_phone} - ABORTING"

with open(CV_PATH, "rb") as f:
    resume_b64 = base64.b64encode(f.read()).decode("ascii")
print(f"CV loaded: {CV_PATH} ({len(resume_b64)} b64 chars)")

# ---- Step 1: candidate insert ----
cand = q("""INSERT INTO candidates
        (first_name, last_name, email, phone, resume_data, resume_file_name, resume_mime_type,
         position, location, current_position, current_company, education, experience, source)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
        RETURNING id, first_name, last_name, email""",
        ["Furqan", "Afzal", EMAIL, PHONE,
         resume_b64, "Furqan_Afzal_-_Growth_Marketing_Manager.pdf", "application/pdf",
         "Senior Manager Growth",
         "Islamabad, Pakistan",
         "Digital Marketing Lead",
         "Pakistan TV Digital",
         "Executive MBA (General Management), FAST-NUCES Islamabad (Aug 2024-Jan 2026, thesis A+); BS Accounting & Finance, NUST (2017-2022)",
         "5+ years in digital growth and marketing. Digital Marketing Lead, Pakistan TV Digital (Aug 2025-date): 6-person team, PKR 3M/month budget, 0 to 439K+ social audience in 12 months, website revamp. Freelance Strategic Marketing & Growth Consultant (Apr 2024-date, incl. Teacher Resource Center). Product & Marketing Specialist, Weather Walay (Nov 2021-Apr 2024): Jazz-partnered app scaled to 3.8M paying subscribers at ~PKR 6 CPA, +25% monthly revenue, GBP 250,000 GSMA Innovation Fund grant secured (sole Pakistani recipient, 250-station weather network delivered). Earlier: AdiFiles content team lead, Mindcob sales & marketing coordinator.",
         "sourced (LinkedIn outreach by Ayesha)"])
CAND_ID = cand[0]["id"]
print("Candidate created:", cand[0])

# ---- Step 2: application insert ----
dup = q("SELECT id FROM applications WHERE candidate_id = $1 AND job_id = $2", [CAND_ID, JOB_ID])
assert not dup, f"Guard failed: candidate {CAND_ID} already has application(s) on job {JOB_ID}: {dup} - ABORTING"

app = q("""INSERT INTO applications (candidate_id, job_id, status, stage, notes)
           VALUES ($1, $2, 'shortlisted', 'Applied',
                   'Sourced candidate; values-invited live 2026-08-07 (no Markaz record at the time). Record created by Coco 2026-08-14 per Ayesha, from CV + Zero In call of 2026-08-14. Expected salary (via Ayesha 2026-08-14): PKR 300,000 gross - 400,000 take-home.')
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

verify = q("""SELECT a.id AS app_id, c.id AS cand_id, c.first_name, c.last_name, c.email, c.phone,
                     length(c.resume_data) AS resume_len, c.resume_file_name,
                     a.status, a.values_interview_result, a.values_interview_score,
                     a.values_scorecard->>'candidateName' AS sc_name,
                     a.values_scorecard->>'proceedToRightSeat' AS proceed,
                     jsonb_array_length(a.values_scorecard->'values') AS n_values
              FROM applications a JOIN candidates c ON c.id = a.candidate_id
              WHERE a.id = $1""", [APP_ID])
print("Verify:", json.dumps(verify[0], indent=2))
