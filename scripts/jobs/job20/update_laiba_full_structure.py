"""
Update Laiba Ahmad scorecard with full structure matching Meer Muneeb
"""

import psycopg2
import json

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode": "require"
}

SCORECARD = {
    "date": "May 12, 2026",
    "host": "Ayesha Khan",
    "candidateName": "Laiba Ahmad",
    "noteTaker": "Coco",
    "recordingLink": "https://fathom.video/share/n-_Q9Thxyz5rkisz6ALQ7jBzo5NNdA7r",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Resigned from Invest Innovate to pivot to direct product ownership. Working on compliance AI product - completely new vertical with high complexity. Recently faced major code break after client delivery - wanted to quit. Instead, got team together, identified systematic code review issues, implemented structured reviews and AI regression testing agent.",
            "curveBall": "Invest Innovate accelerator had unmet donor targets through 6 rounds. Created AI diagnostic tool for startups, increased program NPS by 30%.",
            "microCase": "Worked with marginalized women entrepreneurs on strict donor deadlines. Created custom Urdu e-commerce solution."
        },
        {
            "name": "All for One and One for All",
            "rating": "+",
            "deepDive": "At Invest Innovate conference, co-lead faced logistics crisis. Suggested co-leading workshop while waiting for trainer. Divided responsibilities, team executed. Result had better feedback than trainer's portion.",
            "curveBall": "Surfacing quiet voices: Associate was brilliant but insecure. Created 6-month structured roadmap starting with 1-on-1s, progressing to working groups. Employee now has master's scholarship abroad.",
            "microCase": "Celebrates colleague Saba Kulsoom for confidence and pushing back against leadership."
        },
        {
            "name": "Continue to Improve Our Craft",
            "rating": "+",
            "deepDive": "Recently learned product iteration in compliance/audit space. Ran 6 rounds of accelerator with continuous feedback and improvement. Result: 4 startups launched in Saudi Arabia, 7-8 raised funding.",
            "curveBall": "Teaching while learning: Co-founded social enterprise, started own tote bag business (DEET) to understand nuances. Teaches what worked AND what didn't.",
            "microCase": "Advises younger sister on career, sharing what she knows plus what she's still learning."
        },
        {
            "name": "Courageous Conversations",
            "rating": "+",
            "deepDive": "New engineer caused major code break. Senior leadership wanted scapegoat. Took stand using concrete examples, changed their minds that it's systematic, not personal. Gave difficult feedback to engineer with validation and clear expectations.",
            "curveBall": "Performance review feedback on visibility: Initial reaction frustrated/defensive. Ranted then reflected. Followed up with manager 3 days later, restructured workflows. Complete turnaround in 2 months.",
            "microCase": "Articulates red flags in leaders: unrealistic timelines without team input, pressure without support, reactive decisions."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "In professional life, has not handed off projects for better impact. Instead, co-creates and gets support while remaining owner. Asian Development Bank project - technical, new to her. Brainstormed with manager, she executed, won project.",
            "curveBall": "Open to perspective change from junior staff. Fresh grad associate suggested product scoring rubric variations with configurables for industry/stage.",
            "microCase": "Values changing perspectives based on junior input."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Pink teddy bear gangster meme - cute inside but acting tough outside. Buttercup meme - first 30 mins after waking unapproachable without coffee.",
            "curveBall": "Silly ritual: Zip Zap Zop game from A-level camp. Standing in circle, sending energy, people laugh. Fun brain activator. Mentions trips and physical activities bond teams.",
            "microCase": "Engages warmly, relatable personality, brings humor throughout call."
        }
    ],
    "passingLogic": "0 minuses, 1 plus-minus = PASS",
    "finalComments": "PASS - Laiba Ahmad demonstrates exceptional strength in Don't Walk Away (multiple complex problems solved systematically), All for One (mentoring quiet voices to excellence), Continuously Improve (learning in new fields, teaching while learning), and Courageous Conversations (difficult feedback handled with care and follow-through). One +/- on Don't Hold On Too Tight. Strong product leadership orientation, team-focused, willing to absorb pressure and solve messy problems. Ready for Right Seat interview.",
    "gwcAssessment": {
        "getsIt": "YES - Deeply understands team values. All examples show internalization: persistent problem-solving, team lifting, humility in learning, courageous feedback, adaptability.",
        "wantsIt": "YES - Career pivots show genuine interest in growth and impact. Values team environment, takes on hard problems, invests in others' development.",
        "capacity": "YES - Leadership experience (CEO WeCamp, senior program lead Invest Innovate), product management expertise, AI/compliance knowledge, proven team development. Ready to execute on values."
    },
    "proceedToRightSeat": "Yes"
}

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

cur.execute(
    "UPDATE applications SET values_scorecard = %s WHERE id = 1389",
    (json.dumps(SCORECARD),)
)

print("[OK] Laiba Ahmad scorecard updated with full structure matching Meer Muneeb format.")
conn.commit()
cur.close()
conn.close()
