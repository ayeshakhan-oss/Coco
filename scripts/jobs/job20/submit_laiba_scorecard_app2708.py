"""
Submit complete values scorecard for Laiba Ahmad to application 2708
Job 20 — Senior Product Manager
Interview conducted: 2026-05-12
"""

import psycopg2
import json
from datetime import datetime

DB_CONFIG = {
    "host": "ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_kBQ10OASHEmd",
    "sslmode": "require"
}

SCORECARD = {
    "date": "2026-05-12",
    "host": "Ayesha Khan",
    "candidateName": "Laiba Ahmad",
    "noteTaker": "Coco",
    "recordingLink": "https://fathom.video/share/n-_Q9Thxyz5rkisz6ALQ7jBzo5NNdA7r",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Resigned from Invest Innovate to pivot to direct product ownership. Working on compliance AI product - completely new vertical with high complexity. Recently faced major code break after client delivery - wanted to quit. Instead, got team together, identified systematic code review issues, implemented structured reviews and AI regression testing agent.",
            "curveBall": "Earlier: Invest Innovate accelerator had unmet donor targets through 6 rounds. Created AI diagnostic tool for startups (identifies problems, generates 3-month learning maps), increased program NPS by 30%.",
            "microCase": "Worked with marginalized women entrepreneurs on strict donor deadlines. Tried multiple approaches, none worked. Paused, listened deeply, created custom Urdu e-commerce solution with manual onboarding before automation."
        },
        {
            "name": "All for One and One for All",
            "rating": "+",
            "deepDive": "At Invest Innovate conference, co-lead faced logistics crisis with workshop. Laiba suggested they co-lead with existing materials while waiting for trainer. Result had better feedback than trainer's portion. Shows shared goals and going above and beyond.",
            "curveBall": "Surfacing quiet voices: Associate was brilliant but insecure. Created 6-month structured roadmap starting with 1-on-1s, progressing to working groups. Also mentored employee at WeCamp using green/yellow/red zone approach. Employee now has master's scholarship abroad.",
            "microCase": "Celebrates colleague Saba Kulsoom for confidence, knowing her boundaries, pushing back against leadership, admitting what she doesn't know. Pattern of lifting teammates evident."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Recently learned product iteration in new compliance/audit space. Built structured learning paths, iterative feedback loops. Ran 6 rounds of accelerator - each round collected feedback and improved incrementally. Result: 4 startups launched in Saudi Arabia, 7-8 raised funding.",
            "curveBall": "Teaching while learning: Co-founded social enterprise for women's digital business. Started own tote bag business (DEET) to understand nuances - ran for 2 months, handed off. Teaches women both what worked AND what didn't.",
            "microCase": "Advises younger sister on career, relationships, parents - shares what she knows plus what she's still learning. Honest about limitations: These are things I'm also still learning and exploring."
        },
        {
            "name": "Courageous Conversations",
            "rating": "+",
            "deepDive": "New engineer caused major code break. Senior leadership wanted scapegoat. Laiba took stand using concrete examples, changed minds over 2-3 days that it's systematic, not personal. Then gave difficult feedback to engineer - acknowledged systematic issues, validated work, set clear expectations.",
            "curveBall": "Performance review feedback on visibility: Initial reaction was frustrated/defensive. Ranted for hour then reflected. Realized truth. Followed up with manager 3 days later, restructured workflows. Complete turnaround in 2 months.",
            "microCase": "Articulates red flags in leaders: unrealistic timelines without team input, pressure without support, reactive/stress-based decisions. Values leaders who absorb external pressure and translate to doable goals for team."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "Honest answer: In my professional life, I have not handed off projects for better impact. Instead, co-creates and gets support while remaining owner. Asian Development Bank project showed she keeps ownership throughout.",
            "curveBall": "Open to perspective change from junior staff. Fresh grad associate suggested product scoring rubric variations - added configurables for industry/stage. Much better fit. Recognizes young graduates bring fresh thinking.",
            "microCase": "Values changing perspectives based on junior input. Acknowledges: More than senior eyes, junior eyes bring fresh perspective."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Pink teddy bear gangster meme - cute fuzzy pink bear dressed as gangster. Relates to being cute inside but acting tough outside. Friends also sent her this meme. Buttercup meme - first 30 mins after waking is unapproachable without coffee.",
            "curveBall": "Silly ritual: Zip Zap Zop game from A-level international camp. Standing in circle, sending energy, people laugh. Fun brain activator, forces eye contact. Also mentions trips/physical activities bond teams.",
            "microCase": "Engages warmly with interviewer, relatable personality throughout, brings humor and personality to entire call."
        }
    ],
    "finalComments": "PASS - Laiba demonstrates exceptional strength in Don't Walk Away (multiple complex problems solved systematically), All for One (mentoring quiet voices to excellence), Continuously Improve (learning in new fields, teaching while learning), and Courageous Conversations (difficult feedback handled with care and follow-through). One +/- on Don't Hold On Too Tight. Ready for Right Seat interview.",
    "proceedToRightSeat": True,
    "gwcAssessment": {
        "getsIt": "YES - Deeply understands team values. All examples show internalization.",
        "wantsIt": "YES - Career pivots show genuine interest in growth and impact.",
        "capacity": "YES - Leadership experience, product management expertise, proven team development."
    }
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        UPDATE applications
        SET values_scorecard = %s,
            values_interview_result = 'pass',
            values_interview_notes = %s,
            values_interview_date = %s,
            values_interviewer_name = %s,
            stage = %s,
            status = %s
        WHERE id = %s
    """, (
        json.dumps(SCORECARD),
        "PASS - 4 pluses, 2 plus-minuses, 0 minuses. Ready for Right Seat interview.",
        datetime(2026, 5, 12),
        "Ayesha Khan",
        "Right Seat",
        "shortlisted",
        2708
    ))

    print(f"[OK] Submitted complete values scorecard for Laiba Ahmad (App 2708)")
    print(f"     Status: shortlisted | Stage: Right Seat")

    conn.commit()
    cur.close()
    conn.close()
    print("[OK] Scorecard submitted successfully to Markaz.")

if __name__ == "__main__":
    main()
