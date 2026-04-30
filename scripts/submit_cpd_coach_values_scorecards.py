import psycopg2
import json
from datetime import datetime

conn = psycopg2.connect(
    host="ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    dbname="neondb",
    user="neondb_owner",
    password="npg_kBQ10OASHEmd",
    sslmode="require"
)
cur = conn.cursor()

# ── IRUM AFZAL ── App ID 1995 | Candidate 489
irum_scorecard = {
    "date": "2026-04-29",
    "host": "Ayesha Khan",
    "candidateName": "Irum Afzal",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Faced pregnancy during critical final months of Teach for Pakistan fellowship. Rather than step back, created summer school program (150 students, 50-60 attended). Introduced remedial classes, maintained constant contact with substitute teacher during maternity leave. Result: 100% passing rate, all students promoted 5th→6th grade. Demonstrates extraordinary resilience through personal, professional, and academic challenges simultaneously."
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": "Recognized quiet back-row students who were putting in effort but not getting noticed. Gave appreciation, observed behavior shift and increased confidence. Also bridged communication gap between veteran teachers (25+ years) and new government teacher hires. Shared resources freely (markers, chart papers), offered mentorship, ensured new teachers felt supported and integrated."
        },
        {
            "name": "Continuously Improving Our Craft",
            "rating": "+",
            "deepDive": "Held MS Word training workshop for 20 government school teachers because they were overloaded (one person doing all paper design/digitization). 8 teachers became fully independent; remaining 12 still learning. Self-aware: 'They were a work in progress.' Demonstrates growth mindset and recognition that improvement is iterative."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": "Received critical feedback from manager: lesson planning effort ≠ classroom delivery quality. Initial defensiveness transformed into deep reflection. Realized: beautiful worksheets alone weren't enough; students needed active engagement during delivery. Adjusted entire approach to increase student participation and responsibility. Clear example of receiving difficult feedback, processing it, and changing behavior."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "N/A",
            "deepDive": "Not assessed in interview structure."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Created daily opening chant ritual with students—a poem that built enthusiasm and readiness for learning. Students memorized it, held her accountable ('We have to chant first'). When lesson plan was long and she wanted to skip it, students reminded her. Energized classroom culture through consistent, joyful ritual."
        }
    ],
    "finalComments": "Irum demonstrates mature reflection, resilience through adversity, and genuine investment in both student and teacher growth. Humility evident in feedback acceptance and continuous learning. Strong team player with natural coaching instincts. 5 values demonstrated (+). PASS.",
    "proceedToRightSeat": "Yes"
}

# ── SYEDA SDDIQA FATIMA ── App ID 308 | Candidate 266
syeda_scorecard = {
    "date": "2026-04-29",
    "host": "Ayesha Khan",
    "candidateName": "Syeda Sddiqa Fatima",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+/-",
            "deepDive": "Science lab construction mentioned; lacks specific challenge details or clear 'almost quit' narrative. Transitioned from teaching → training but no evidence of persisting through explicit difficulty. Response was vague on what the hard thing actually was."
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": "Proactively covered team's training schedule gap without being asked. When colleagues couldn't fill a training slot, she stepped up to help the department avoid conflict. Shows team support instinct."
        },
        {
            "name": "Continuously Improving Our Craft",
            "rating": "+",
            "deepDive": "New to training role; learned training design, manual crafting, lesson planning for adult learners. Self-directed learner. Demonstrates growth orientation and willingness to develop new skills in unfamiliar territory."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Received feedback during Teach for Pakistan classroom observations. Limited reflection on how that feedback changed her behavior or thinking. No evidence of integration or behavioral shift demonstrated."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "Taught chemistry, biology, and computer science (MS in bioinformatics). Recognized expert colleague for CS and handed over responsibility. Acknowledged expertise boundaries and let go of subjects where others were better equipped."
        },
        {
            "name": "Practice Joy",
            "rating": "+/-",
            "deepDive": "Self-describes as 'smiley face emoji' bringing positivity to others. Response feels performative (tactic) rather than grounded in authentic examples. Attempts to be joyful but lacks genuine, embodied examples."
        }
    ],
    "finalComments": "Syeda shows trainer aptitude and some values alignment (team support, delegation). However, responses lack depth and behavioral specificity. 3 values +/-, 3 values +. EXCEEDS 2 +/- LIMIT. FAIL.",
    "proceedToRightSeat": "No"
}

# ── UNZEELA ── App ID 2165 | Candidate 1729
unzeela_scorecard = {
    "date": "2026-04-29",
    "host": "Ayesha Khan",
    "candidateName": "Unzeela",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Witnessed corporal punishment incident from organization's own staff. Difficult position (community & teacher backlash risk). Talked to parents, child, organization. Reported to authorities. Teacher reposted and received empathy training. Initially received backlash but continued effort; after 6 months, teacher improved, students felt safer. Persisted through resistance and adversity."
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": "Team member going through depression, hesitant to speak, caused project miscommunication. Listened, discovered personal struggles, raised her point to team. Shifted group culture—team realized mistakes have reasons, people need support not blame. Advocated for quieter voices."
        },
        {
            "name": "Continuously Improving Our Craft",
            "rating": "+",
            "deepDive": "Taught clumsy student table tennis over 4 months. Made mistakes in front of him to model resilience and normalize struggle. After 4 months, student now wins 8 out of 10 games. Clear growth trajectory and persistence in developing someone else's confidence and skill."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": "CEO publicly discussed female teacher's menstrual leave, causing discomfort. Approached CEO with courage to discuss women-specific leave policy. Result: new organizational menstrual leave policies implemented. Positive cultural shift; women feel understood and heard. Upward feedback with real outcome."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "Lead educator managing grades 1-5 (heavy load Dec-Feb). Identified capable assistant with maths expertise. Pitched to CEO, trained her Feb-Mar. Now teacher handles grades 1-5 maths independently and successfully. Recognized others' strengths and let go of responsibility for greater impact."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Describes self as 'goofy emoji' (googly eyes, tongue out). Lively person who loves speaking. Brings energy; people feel comfortable around her. Authentic, grounded example backed by actual feedback on her personality impact."
        }
    ],
    "finalComments": "Unzeela combines courage, empathy, and continuous growth. She identifies problems, takes interpersonal risks, sustains effort. All 6 values demonstrated (+). STRONG FIT for coaching—demonstrates collaborative, feedback-rich, growth-oriented mindset essential for teacher development work.",
    "proceedToRightSeat": "Yes"
}

# ── HAJRA SAJJAD ── App ID 1061 | Candidate 879
hajra_scorecard = {
    "date": "2026-04-29",
    "host": "Ayesha Khan",
    "candidateName": "Hajra Sajjad",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Principal extremely resistant to 'Bridging Gaps' community partnership project—'no tangible outcomes.' Conducted need assessment, surveys, focus groups with parents, teachers, students. Used data to convince principal. Students' grades improved, created student booklet. Principal's expressions changed when presented results—moved from skepticism to pride. Persisted through institutional resistance."
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": "Kinesthetic learners requested flexible study space (balcony during revision). VP came upstairs, said students should be inside. Hajra defied order, protected student wellbeing. Later told VP testing would happen later. Prioritized student need over hierarchy; unasked advocacy for students."
        },
        {
            "name": "Continuously Improving Our Craft",
            "rating": "+",
            "deepDive": "Recently learned module writing as new cluster lead (Aug 2025). Trained teachers in online workshop for SSC/HSSC pass-out schools. Through teaching others, identified own gaps. Self-review + peer feedback + teacher contextual feedback = continuous improvement. Learned by teaching."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": "Identified problem: SSC/HSSC lesson plan format (from primary) not working. Teachers overwhelmed by multiple activities in 40-45 student classes. Consulted subject specialists. Reached supervisor with data. Proposed 'developmental activities' section (combines input + practice). Supervisor hesitant but agreed. Format proved effective; target achieved. Data-driven upward feedback."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "Curriculum mapping workshop: assigned to deliver technical training. Realized peer team member better equipped for delivery. Collaborative hand-off approach. Recognized strengths in others; willing to share leadership."
        },
        {
            "name": "Practice Joy",
            "rating": "N/A",
            "deepDive": "Interview cut off before Value 6 assessment."
        }
    ],
    "finalComments": "Hajra demonstrates exceptional coaching readiness: data-driven problem-solving, courage to challenge institutional norms, willingness to consult & collaborate, self-awareness of learning gaps. Combines empathy (student wellbeing, teacher constraints) with pragmatism. 5 values demonstrated (+). PASS.",
    "proceedToRightSeat": "Yes"
}

# ── SUBMIT SCORECARDS ──
try:
    # Irum Afzal
    cur.execute("""
        UPDATE applications SET
            values_scorecard = %s,
            values_interview_result = %s,
            values_interview_date = %s,
            values_interviewer_name = %s
        WHERE id = %s
    """, (
        json.dumps(irum_scorecard),
        "pass",
        datetime(2026, 4, 29),
        "Ayesha Khan",
        1995
    ))
    print(f"✓ Irum Afzal (App 1995): {cur.rowcount} row(s) updated")

    # Syeda Sddiqa Fatima
    cur.execute("""
        UPDATE applications SET
            values_scorecard = %s,
            values_interview_result = %s,
            values_interview_date = %s,
            values_interviewer_name = %s
        WHERE id = %s
    """, (
        json.dumps(syeda_scorecard),
        "fail",
        datetime(2026, 4, 29),
        "Ayesha Khan",
        308
    ))
    print(f"✓ Syeda Sddiqa Fatima (App 308): {cur.rowcount} row(s) updated")

    # Unzeela
    cur.execute("""
        UPDATE applications SET
            values_scorecard = %s,
            values_interview_result = %s,
            values_interview_date = %s,
            values_interviewer_name = %s
        WHERE id = %s
    """, (
        json.dumps(unzeela_scorecard),
        "strong_pass",
        datetime(2026, 4, 29),
        "Ayesha Khan",
        2165
    ))
    print(f"✓ Unzeela (App 2165): {cur.rowcount} row(s) updated")

    # Hajra Sajjad
    cur.execute("""
        UPDATE applications SET
            values_scorecard = %s,
            values_interview_result = %s,
            values_interview_date = %s,
            values_interviewer_name = %s
        WHERE id = %s
    """, (
        json.dumps(hajra_scorecard),
        "pass",
        datetime(2026, 4, 29),
        "Ayesha Khan",
        1061
    ))
    print(f"✓ Hajra Sajjad (App 1061): {cur.rowcount} row(s) updated")

    conn.commit()
    print("\n✅ All 4 CPD Coach values scorecards submitted to Markaz successfully.")
    print("\nSUMMARY:")
    print("  1. Irum Afzal .......... PASS (5 values +)")
    print("  2. Syeda Sddiqa Fatima . FAIL (3 +/-, exceeds limit)")
    print("  3. Unzeela ............ STRONG PASS (All 6 values +)")
    print("  4. Hajra Sajjad ....... PASS (5 values +)")

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    cur.close()
    conn.close()
