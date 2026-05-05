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

# ── TAIMOOR SAQIB ── App ID 2476, Job 38 (AI Engineer)
taimoor_scorecard = {
    "date": "May 4, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "Coco",
    "candidateName": "Taimoor Saqib",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "CavTek Azure learning: Assigned urgent Azure config task by client despite zero knowledge. Initial hesitation overcome by team lead's 'let's see your learning.' Spent 3+ hours learning load balancing and server configuration, completed successfully. Reflected: 'I should not be hesitant towards learning new things.'",
            "curveBall": "When asked what changed his mind, showed growth mindset: reframed difficulty as opportunity to learn competitive technologies. Viewed challenge as development, not burden.",
            "microCase": "Boring certification completion: Completed very long, boring course over two weeks, going home each day to work through materials. Persisted through tedium without external pressure."
        },
        {
            "name": "All for One, One for All",
            "rating": "+",
            "deepDive": "SQL task support: Proactively took on peer's SQL tasks despite not being asked. Knew he was good at SQL and it would take him 5 minutes vs 15-20 minutes for the peer. Identified where he could add value and lifted teammate's workload.",
            "curveBall": "Honest admission on lifting quieter voices: Acknowledged he hasn't been active in bringing introverted team members into conversations. Interviewer accepted as growth area. Shows self-awareness without defensiveness.",
            "microCase": "Buddy system appreciation: Mentored two junior developers at I2C. Valued their growth and wanted them to succeed beyond what they'd accomplished with him."
        },
        {
            "name": "Continuously Improve",
            "rating": "+",
            "deepDive": "Active learning in AI domain: Pinned two articles on transformer architecture and AI agents in Firefox to read. Not passively consuming—curating and prioritizing domain-relevant content for growth.",
            "curveBall": "Learning transformer architecture with peer: Tackled very difficult architecture that took one week to learn only half. Decided to split learning with peer and study together. Shows willingness to persist through difficult technical material.",
            "microCase": "Observational improvement feedback: Noticed LLM behavior issue in production when searching Wikipedia. Communicated observation to managers. After one week, the issue was fixed."
        },
        {
            "name": "Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Difficult team member feedback at Turing: As team lead, gave harsh feedback to underperforming team member about to be fired due to low throughput/quality. Delivery was via Slack/text, not face-to-face. When asked why not face-to-face: 'I would like to avoid because I don't think I would be the person who is firing someone from the company.'",
            "curveBall": "Excellent feedback reception: Received critical feedback about low throughput due to illness. Initially stunning but then received performance improvement plan with support materials (PDF evaluation criteria). Accepted feedback with humility and used plan to improve.",
            "microCase": "Upward feedback on application: Noticed product issue with LLM/Wikipedia search behavior. Gave observation to managers. Though indirect follow-up, voiced concern about improvement opportunity."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "Handoff of tech learning: Handed off new tech (new language) learning to junior developer so he could focus on core app work. Shows flexibility in letting go of expertise ownership for team goals.",
            "curveBall": "Learning from juniors—strong flexibility: Junior 7-8 months junior introduced him to CTEs (Common Table Expressions) in SQL. Adopted this better approach instead of using joins/sub-queries. Shows willingness to learn from 'below' and let go of being the expert.",
            "microCase": "Tech stack adaptability: Transitioned from AWS to Azure, picked up new Linux commands, adapted to different frameworks. Flexible in technical approaches."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Humor and lightness: Laughing emoji—'I'm good at cracking jokes and making people laugh.' Shows he brings laughter and positivity to teams and employees. Self-aware about wanting to energize others.",
            "curveBall": "Creative team ritual: Non-monetary silly ritual—if anyone leaves laptop on and steps away, they buy ice cream for team. Playful, security-conscious, aligns company values with fun. Shows creativity in team engagement.",
            "microCase": "Warm, engaged interview presence. Personable with Ayesha, asks thoughtful questions about Taleemabad's AI direction. Brings positive energy to interactions."
        }
    ],
    "finalComments": "PASS — Taimoor demonstrates solid values alignment. Strengths: persistence through learning barriers (Azure), proactive peer support (SQL), excellent feedback reception, flexibility in learning from juniors, humor and warmth. Growth areas: lifting quieter voices in group settings, proactive delegation, face-to-face courageous conversations (prefers text-based). Zero minuses. 4 pluses + 2 plus-minuses. Ready for Right Seat interview.",
    "proceedToRightSeat": "Yes"
}

# ── MEER MUNEEB KHAN ── App ID 677, Job 24 (Full Stack Lead)
meer_scorecard = {
    "date": "May 5, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "Coco",
    "candidateName": "Meer Muneeb Khan",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "20-day project with no initial requirements: Started with unclear specs, team made sketch, unclear what client wanted. Then clarified requirements with developer. Completed mobile app within tight 20-day deadline despite initial ambiguity. Interviewer: 'you are both resilient. That's really amazing.'",
            "curveBall": "Shows persistence through ambiguity—didn't quit despite difficulty, accepted challenge as opportunity to deliver.",
            "microCase": "Volunteering for ugly problems: Mentioned startup work where he had to jump in on things nobody else was owning. Shows willingness to step up for difficult tasks."
        },
        {
            "name": "All for One, One for All",
            "rating": "+",
            "deepDive": "Covering teammate's mistake: As group leader, worked on covering for teammate's deadline miss where mistake was made. Proactively covered without being asked, took responsibility for collective outcome.",
            "curveBall": "Advocating for junior: Described situation where junior developer was made to feel bad. 'He made me feel bad, but I fought for him.' Stands up for juniors being mistreated. Interviewer: 'That's nice, most people who have said that they don't hesitate.'",
            "microCase": "Appreciating leadership: Named CTO Usman Mughal as someone he lifts. 'They always stay with us a friend... I would like to them as much possible.' Shows appreciation for humble, team-first leaders."
        },
        {
            "name": "Continuously Improve",
            "rating": "+",
            "deepDive": "Learning new tech stacks: Learned blockchain in recent years. When joining current company, tech stack changed from Node.js to Python/FastAPI. Proactively adapted to new stack and languages required by role.",
            "curveBall": "Shows humility about gaps: 'I have to learn it... Because it's remote job, it's lot easier to learn it.' Acknowledges what he doesn't know and commits to learning.",
            "microCase": "Teaching in group settings: Working with other students, was group leader. Engages in continuous learning contexts."
        },
        {
            "name": "Courageous Conversations",
            "rating": "+",
            "deepDive": "Feedback to CEO on QA/testing: Noticed small things being left untested before shipping. Gave feedback in meeting: 'if you have test, then the mistakes are not... why we QA.' Gave honest feedback to CEO about process gaps, pushed back on shipping untested code.",
            "curveBall": "Feedback to leaders on scope: When requirements kept changing (UI/UX), set boundaries diplomatically: 'I will focus the other task, until you can finalize it.' Set prioritization expectations with leadership.",
            "microCase": "Receiving feedback with reflection: On work-life balance feedback—'at beginning, I tell you no, no... But when you have... Maybe I am too much of a workaholic.' Shows openness to feedback and willingness to reconsider position."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "Handing off new tech learning: Deliberately handed off new language learning to junior developer so he could focus on core app work. Shows flexibility in letting go of expertise ownership for team goals.",
            "curveBall": "Adaptability to remote/changing structures: Remote job made learning easier. Therapieses project with US client required adjustment to different work structures. Shows willingness to adjust to circumstances.",
            "microCase": "Shows openness to evolution and new approaches across projects."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Bringing humor to teams: Laughing emoji—'I'm good at cracking jokes and making people laugh.' Brings laughter and positivity to teams. Philosophy: no point in anything without joy.",
            "curveBall": "Creative team ritual: Introduced gamified card game ritual in breaks. Whoever wins tells everyone 'they got the ones.' Made a trick about who would win. Shows creativity and playfulness in team engagement.",
            "microCase": "Warm, engaged tone throughout interview. Positive presence and energy."
        }
    ],
    "finalComments": "PASS — Meer Muneeb demonstrates solid values alignment. Strengths: persistence through ambiguity (20-day project), strong team support (covers mistakes, advocates for juniors), honest feedback to leadership, proactive learning (blockchain, multiple tech stacks), humor and creative team rituals. Growth area: flexibility/delegation could deepen (one clear handoff example, room for broader ownership release). Zero minuses. 5 pluses + 1 plus-minus. Recommended for Case Study/Assessment stage.",
    "proceedToRightSeat": "No"
}

# ── UPDATE Taimoor ──
cur.execute("""
    UPDATE applications SET
        values_scorecard = %s,
        values_interview_result = %s,
        values_interview_date = %s,
        values_interviewer_name = %s,
        stage = %s
    WHERE id = %s
""", (
    json.dumps(taimoor_scorecard),
    "pass",
    datetime(2026, 5, 4),
    "Ayesha Khan",
    "Right Seat",
    2476
))
print(f"Taimoor Saqib (App 2476): {cur.rowcount} row(s) updated")

# ── UPDATE Meer Muneeb ──
cur.execute("""
    UPDATE applications SET
        values_scorecard = %s,
        values_interview_result = %s,
        values_interview_date = %s,
        values_interviewer_name = %s,
        stage = %s
    WHERE id = %s
""", (
    json.dumps(meer_scorecard),
    "pass",
    datetime(2026, 5, 5),
    "Ayesha Khan",
    "Case Study",
    677
))
print(f"Meer Muneeb Khan (App 677): {cur.rowcount} row(s) updated")

conn.commit()
cur.close()
conn.close()
print("Done. Both scorecards submitted to Markaz.")
