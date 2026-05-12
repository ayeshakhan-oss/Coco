"""
Fix Laiba Ahmad values scorecard with correct minimal schema for Markaz
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

# Correct minimal schema (matching reference that works on Markaz UI)
SCORECARD_LAIBA = {
    "date": "May 12, 2026",
    "host": "Ayesha Khan",
    "candidateName": "Laiba Ahmad",
    "noteTaker": "",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Resigned from Invest Innovate to pivot to direct product ownership. Working on compliance AI product - completely new vertical with high complexity. Recently faced major code break after client delivery - wanted to quit. Instead, got team together, identified systematic code review issues, implemented structured reviews and AI regression testing agent. Shows deep persistence and systematic problem-solving.",
            "curveBall": "Earlier: Invest Innovate accelerator had unmet donor targets through 6 rounds. Leadership unhelpful. Created AI diagnostic tool for startups (identifies problems, generates 3-month learning maps), increased program NPS by 30%.",
            "microCase": "Worked with marginalized women entrepreneurs on strict donor deadlines. Tried multiple approaches, none worked. Paused, listened deeply, created custom Urdu e-commerce solution with manual onboarding before automation."
        },
        {
            "name": "All for One and One for All",
            "rating": "+",
            "deepDive": "At Invest Innovate conference, co-lead faced logistics crisis with workshop (space, lights, trainer delay). Laiba suggested they co-lead workshop with existing materials while waiting for trainer. Divided responsibilities, team executed. Result had better feedback than trainer's portion. Shows shared goals, crisis management, and going above and beyond.",
            "curveBall": "Surfacing quiet voices: Associate was brilliant but insecure (new to startup space, uncomfortable with public speaking, camera-shy). Created 6-month structured roadmap: started with 1-on-1s with Laiba, progressed to working groups with founders, built confidence step-by-step. Also mentored another employee at WeCamp - mapped comfort zones (green/yellow/red), created safe progression. Employee now has master's scholarship abroad.",
            "microCase": "Celebrates colleague Saba Kulsoom for confidence, knowing her work boundaries, pushing back against leadership, admitting what she doesn't know. Pattern of lifting teammates evident."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Recently learned product iteration in new compliance/audit space. Built structured learning paths, iterative feedback loops, tight feedback cycles. Ran 6 rounds of accelerator - each round collected feedback and improved incrementally. Result: 4 startups launched in Saudi Arabia, 7-8 raised funding. Philosophy: iteration is a lifelong process.",
            "curveBall": "Teaching while learning: Co-founded social enterprise for women's digital business (not expert herself). Started own tote bag business (DEET) to understand nuances - ran for 2 months, handed off. Teaches women both what worked AND what didn't - emphasizes importance of knowing what not to do.",
            "microCase": "Advises younger sister on career, relationships, parents - always shares what she knows plus what she's still learning. Honest about limitations."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": "New engineer caused major code break. Senior leadership wanted scapegoat. Laiba took stand using concrete examples, changed their minds over 2-3 days that it's systematic, not personal. Then gave difficult feedback to engineer - acknowledged systematic issues, validated work, set clear expectations. Engineer now comfortable admitting mistakes to her.",
            "curveBall": "Performance review feedback on visibility: Initial reaction was frustrated/defensive. Ranted for hour then reflected. Realized truth. Followed up with manager 3 days later, restructured workflows, got involved in senior meetings. Complete turnaround in 2 months.",
            "microCase": "Articulates red flags in leaders: unrealistic timelines without team input, pressure without support, reactive/stress-based decisions. Values leaders who absorb external pressure and translate to doable goals for team."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "Honest: In professional life, has not handed off projects for better impact. Instead, co-creates and gets support while remaining owner. Asian Development Bank project - technical, new to her. Line manager guided her, they brainstormed on paper, she executed, won project.",
            "curveBall": "Open to perspective change from junior staff. Fresh grad associate suggested product scoring rubric variations - added configurables for industry/stage. Much better fit. Recognizes young graduates bring fresh thinking.",
            "microCase": "Values changing perspectives based on junior input."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Pink teddy bear gangster meme - cute fuzzy pink bear dressed as gangster. Relates to being cute inside but acting tough outside. Friends also sent her this meme. Buttercup meme - first 30 mins after waking is unapproachable without coffee.",
            "curveBall": "Silly ritual: Zip Zap Zop game from A-level international camp. Standing in circle, sending energy, people laugh. Fun brain activator, forces eye contact and energy exchange. Mentions trips/physical activities bond teams.",
            "microCase": "Engages warmly with interviewer, relatable personality throughout, brings humor and personality to entire call."
        }
    ],
    "finalComments": "",
    "proceedToRightSeat": "Yes"
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("[FIX] Updating Laiba Ahmad scorecard with correct minimal schema...")
    cur.execute("""
        UPDATE applications
        SET values_scorecard = %s
        WHERE id = 1389
    """, (json.dumps(SCORECARD_LAIBA),))

    print("[OK] Laiba Ahmad scorecard fixed and submitted with correct schema.")
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
