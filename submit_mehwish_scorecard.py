import psycopg2, json

conn = psycopg2.connect(
    host='ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech',
    dbname='neondb',
    user='neondb_owner',
    password='npg_kBQ10OASHEmd',
    sslmode='require'
)
cur = conn.cursor()

scorecard = {
    "date": "Mar 24, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "",
    "candidateName": "Mehwish Hussain",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Ayesha asked: describe a moment you almost quit but chose to stay. A colleague got pregnant and left mid-project. Mehwish had never seen the questionnaire or attended the training, and was handed full data cleaning responsibility with one week remaining. Hundreds of responses arriving daily. Mid-way she uncovered a systemic problem: enumerators had been skipping the NPGP (poverty score) section throughout the survey because they weren't explaining it correctly to respondents. At end-stage she personally called enumerators, supervisors, and field teams to recollect the missing data. She spent multiple nights on the clean-up and pushed it through to completion. Note: she added that she decided to quit the job after completing the project and mentioned a recurring frustration with data quality — worth monitoring.",
            "curveBall": "Ayesha asked: have you ever volunteered for an ugly problem nobody else was owning? In January she voluntarily offered to travel to Kashmir to monitor UNICEF child labour survey teams when nobody else would because of harsh winter weather and poor connectivity. Four-hour drive, arrived at 2pm, had only 2-3 hours to assess teams, write field reports, and simultaneously update German partners on ground conditions. She chose this — it was not assigned.",
            "microCase": ""
        },
        {
            "name": "All for One & One for All",
            "rating": "+/-",
            "deepDive": "Ayesha asked: have you ever covered for someone's mistake without being asked? Mehwish described how enumerators would routinely work on outdated questionnaire versions on their tablets despite being notified of updates. Rather than escalating to her manager, she would catch this on field visits and quietly fix it one-on-one with the teams — coaching them on updating questionnaires. She did this specifically to prevent issues from reaching stakeholders. The spirit of team protection is there but this is largely within her data quality role; not a peer cover-up that required her to absorb personal risk.",
            "curveBall": "Ayesha asked: have you surfaced a quiet voice who couldn't advocate for themselves? A new female colleague was told her dressing (shirt with open buttons) was inappropriate. The colleague was uncomfortable but didn't raise it. Mehwish escalated to HR, HR arranged a meeting, and the outcome was advising the colleague to wear an inner layer. She took action but the route was procedural — escalate to HR rather than personally intervening. The resolution also focused on asking the colleague to adjust rather than addressing the senior's behaviour.",
            "microCase": ""
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Ayesha asked: have you recently taught someone a skill? Mehwish taught interns and probationers the full SurveyCTO workflow — questionnaire design, form deployment to tablets, testing before field launch. Also taught ODK Collect and how to read Stata-generated Excel quality check reports to identify data issues. These are genuinely technical, field-specific skills used daily in research work. She was specific about the why: 'test ke bagair aap survey start nahi kar sakte field mein.' The teaching was structured and purposeful.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Ayesha asked: have you given feedback to upper management that created impact? During a poverty score project, Stata was not flagging income outliers correctly. Mehwish manually downloaded data to Excel, applied filters, identified out-of-range values, and suggested to her Sir to use Excel instead of Stata for this output. He agreed and the donor received the Excel-based poverty score report. This is a technical process improvement — a sensible suggestion to a receptive supervisor with no conflict, no risk, no hard truth delivered. The courageous element the value requires was absent.",
            "curveBall": "Ayesha asked: have you received feedback that initially hurt but turned out to be true? She used ChatGPT to translate a questionnaire from English to Urdu and submitted without thorough review. The AI made literal errors — 'tablet' became 'davai' (medicine), 'dung cake' became 'gobar ka cake.' A colleague caught the errors in review before it reached the field. Mehwish was embarrassed and acknowledged she should have reviewed more carefully. The story is honest and self-aware but the feedback was light — no serious professional consequences — and the lesson was more about AI limitations than a deeper behavioural change.",
            "microCase": ""
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "Ayesha asked: have you dropped an old belief or practice due to new learnings? Mehwish described how she used to take meeting minutes by hand in a diary then retype them per staff member on her laptop. When she discovered AI recording tools, she adopted them — now records meetings, edits the AI output, and submits. She called it moving from hard work to smart work. She gave a complete SBR: old practice identified, new learning adopted, changed approach applied. The value requires not clinging to familiar practices when better ones emerge — this example directly demonstrates that.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Ayesha asked: describe yourself as one emoji. Mehwish chose the laughing/smiling emoji. She said she smiles and laughs even in sad or tense environments, sometimes uncontrollably. She was self-aware enough to acknowledge: 'Pata toh koi serious situation mein aapko nahi hasta chaahiye… at times in jahan se aa jaati hoon' — noting that inappropriate laughter slips out occasionally. Ayesha noted it is something she can work on. The authentic positive energy was consistent throughout the entire call — warm, candid, and easy-going from the first minute.",
            "curveBall": "",
            "microCase": ""
        }
    ],
    "finalComments": "Mehwish has genuine strengths in V1 (pushed through a tough crisis under time pressure, voluntarily took on Kashmir fieldwork in January) and V3 (taught real, technical research tools clearly and purposefully). V2 and V4 both stopped short of the full bar — team protection was procedural rather than solidarity-driven, and the courageous conversation examples were safe suggestions rather than hard truths spoken to power. V5 revised to + after review: she gave a complete SBR demonstrating an old practice let go in favour of a new approach. Note: she mentioned a pattern of wanting to quit her current job due to recurring data quality frustrations — worth probing in the GWC round to understand her resilience thresholds. Proceed to GWC.",
    "proceedToRightSeat": "Yes"
}

cur.execute("""
    UPDATE applications
    SET values_scorecard = %s,
        values_interview_result = %s,
        values_interview_date = %s,
        values_interviewer_name = %s
    WHERE id = %s
""", (
    json.dumps(scorecard),
    'pass',
    '2026-03-24',
    'Ayesha Khan',
    1808
))

print(f'Updated: {cur.rowcount} row(s) affected')
conn.commit()
conn.close()
