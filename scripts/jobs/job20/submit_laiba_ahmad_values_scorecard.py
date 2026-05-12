"""
Submit values scorecard for Laiba Ahmad
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

SCORECARD_LAIBA_AHMAD = {
    "date": "2026-05-12",
    "host": "Ayesha Khan",
    "candidateName": "Laiba Ahmad",
    "noteTaker": "Coco",
    "recordingLink": "https://fathom.video/share/n-_Q9Thxyz5rkisz6ALQ7jBzo5NNdA7r",
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
            "name": "Continue to Improve Our Craft",
            "rating": "+",
            "deepDive": "Recently learned product iteration in new compliance/audit space. Built structured learning paths, iterative feedback loops, tight feedback cycles. Ran 6 rounds of accelerator - each round collected feedback and improved incrementally. Result: 4 startups launched in Saudi Arabia, 7-8 raised funding. Philosophy: 'iteration is a lifelong process'.",
            "curveBall": "Teaching while learning: Co-founded social enterprise for women's digital business (not expert herself). Started own tote bag business (DEET) to understand nuances - ran for 2 months, handed off. Teaches women both what worked AND what didn't - emphasizes importance of knowing what not to do.",
            "microCase": "Advises younger sister on career, relationships, parents - always shares what she knows plus what she's still learning. Honest about limitations: 'These are things I'm also still learning and exploring. I don't know what works, but here's what hasn't worked for me.'"
        },
        {
            "name": "Courageous Conversations",
            "rating": "+",
            "deepDive": "New engineer caused major code break. Senior leadership wanted scapegoat. Laiba took stand using concrete examples, changed their minds over 2-3 days that it's systematic, not personal. Then gave difficult feedback to engineer - acknowledged systematic issues, validated work, set clear expectations. Engineer now comfortable admitting mistakes to her. Heavy responsibility but conversation opened dialogue.",
            "curveBall": "Performance review feedback on visibility: Initial reaction was frustrated/defensive - 'I'm doing good work, why isn't it enough?' Ranted for hour then reflected. Realized truth. Followed up with manager 3 days later, restructured workflows, got involved in senior meetings. Complete turnaround in 2 months.",
            "microCase": "Articulates red flags in leaders: unrealistic timelines without team input, pressure without support, reactive/stress-based decisions. Values leaders who absorb external pressure and translate to doable goals for team."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "Honest answer: 'To be very honest, in my professional life, I have not' handed off projects for better impact. Instead, co-creates and gets support while remaining owner. Asian Development Bank project - technical, new to her. Line manager guided her, they brainstormed on paper, she executed, won project. Shows she keeps ownership.",
            "curveBall": "Open to perspective change from junior staff. Fresh grad associate suggested product scoring rubric variations - added configurables for industry/stage. Much better fit. Recognizes young graduates bring fresh thinking, no rules/regulations mentality.",
            "microCase": "Values changing perspectives based on junior input. Acknowledges 'More than senior eyes, junior eyes bring fresh perspective.'"
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Pink teddy bear gangster meme - 'cute fuzzy pink bear dressed as gangster'. Relates to being cute inside but acting tough outside. Friends also sent her this meme - shows shared humor. Buttercup meme - first 30 mins after waking is unapproachable without coffee. Multiple relatable memes.",
            "curveBall": "Silly ritual: Zip Zap Zop game from A-level international camp. Standing in circle, sending energy, people laugh. Fun brain activator, forces eye contact and energy exchange. Also mentions trips/physical activities bond teams. 'I'd love to play it daily.'",
            "microCase": "Engages warmly with interviewer, relatable personality throughout, brings humor and personality to entire call."
        }
    ],
    "passingLogic": "0 minuses, 1 plus-minus = PASS",
    "finalComments": "PASS - Laiba Ahmad demonstrates exceptional strength in Don't Walk Away (multiple complex problems solved systematically), All for One (mentoring quiet voices to excellence), Continuously Improve (learning in new fields, teaching while learning), and Courageous Conversations (difficult feedback handled with care and follow-through). One +/- on Don't Hold On Too Tight (prefers co-creation over delegation, but demonstrates adaptability). Strong product leadership orientation, team-focused, willing to absorb pressure and solve messy problems. Ready for Right Seat interview.",
    "proceedToRightSeat": True,
    "gwcAssessment": {
        "getsIt": "YES - Deeply understands team values. All examples show internalization: persistent problem-solving, team lifting, humility in learning, courageous feedback, adaptability.",
        "wantsIt": "YES - Career pivots show genuine interest in growth and impact. Values team environment, takes on hard problems, invests in others' development.",
        "capacity": "YES - Leadership experience (CEO WeCamp, senior program lead Invest Innovate), product management expertise, AI/compliance knowledge, proven team development. Ready to execute on values."
    }
}

UPDATE = {
    "application_id": 1389,
    "scorecard": SCORECARD_LAIBA_AHMAD,
    "result": "pass",
    "interviewer": "Ayesha Khan",
    "status": "shortlisted"
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    interview_date = datetime(2026, 5, 12)

    cur.execute("""
        UPDATE applications
        SET values_scorecard = %s,
            values_interview_result = %s,
            values_interview_date = %s,
            values_interviewer_name = %s,
            stage = %s,
            status = %s
        WHERE id = %s
    """, (
        json.dumps(UPDATE["scorecard"]),
        UPDATE["result"],
        interview_date,
        UPDATE["interviewer"],
        "Right Seat",
        UPDATE["status"],
        UPDATE["application_id"]
    ))
    print(f"[OK] Submitted values scorecard for {UPDATE['scorecard']['candidateName']} (App {UPDATE['application_id']}) — {UPDATE['result'].upper()}")
    print(f"     Status updated to: {UPDATE['status']} | Stage: Right Seat")

    conn.commit()
    cur.close()
    conn.close()
    print("[OK] Scorecard submitted to Markaz successfully.")

if __name__ == "__main__":
    main()
