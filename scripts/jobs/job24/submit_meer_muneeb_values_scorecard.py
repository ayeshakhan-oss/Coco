"""
Submit values scorecard for Meer Muneeb Khan
Job 24 — Full Stack Lead
Interview conducted: 2026-05-05
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

SCORECARD_MEER_MUNEEB = {
    "date": "2026-05-05",
    "host": "Ayesha Khan",
    "candidateName": "Meer Muneeb Khan",
    "noteTaker": "Coco",
    "recordingLink": "https://fathom.video/share/SFEkRND5YX7bix7-acdr7Mth7xYHZYPX",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Started project with unclear requirements. Team didn't know how to proceed. Persisted for 20 days, restructured requirements with team, delivered. 'We made a sketch that gave it to us. We completed the task.'",
            "curveBall": "Given 'impossible' implementation task, initial uncertainty but immediately regrouped: 'Monday, I discussed things with our team... implemented it.' Shows willingness to restart/reframe.",
            "microCase": "Casually mentioned jumping into startup projects with vague requirements. Pattern of ownership evident."
        },
        {
            "name": "All for One and One for All",
            "rating": "+",
            "deepDive": "As group leader, covered teammate's missed deadline. Absorbed work to help the team hit the deadline.",
            "curveBall": "When asked about difficult personalities, immediately defended struggling junior dev: 'He made me feel bad, but I fought for him.' Shows active advocacy for team members.",
            "microCase": "Praised CTO Usman Mughal: 'They always stay with us a friend... I would support them as much possible.' Celebrates leadership and mutual respect."
        },
        {
            "name": "Continue to Improve Our Craft",
            "rating": "+/-",
            "deepDive": "Recently learned blockchain. Switched entire tech stack from Node to Python/FastAPI: 'When I came this company, my tech stack was changed... it's lot easier to learn it.' Shows adaptability.",
            "curveBall": "When asked about teaching, briefly mentioned working with college students but with some hesitation on articulating the learning experience.",
            "microCase": "Mentioned various projects and language shifts but less reflection on why growth matters or on humility about gaps."
        },
        {
            "name": "Courageous Conversations",
            "rating": "+",
            "deepDive": "Gave direct feedback to CEO on QA/testing gaps: 'If you have test, then the mistakes are not... we are going to test this product.' Advocated for better process despite hierarchical concern.",
            "curveBall": "Struggle with receiving feedback question initially, but eventually acknowledged work-life balance feedback after reflection: 'Maybe I am too much of a workaholic... this was actually true.'",
            "microCase": "Feedback to leader on task switching: 'I will focus the other task, until you can finalize it.' Shows ability to push back constructively."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "Handed off new language project to junior dev: 'I was talking the new developer... We wanted to focus on the app. I wanted to share new language... I feel good for my job.' Shows flexibility in letting others own work.",
            "curveBall": "Some transcript confusion on exact details of handover, but direction is clear. Adapted when needs changed.",
            "microCase": "Shifted focus when team needed him elsewhere."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Self-described as laughing emoji: clear association with humor/positivity in team contexts.",
            "curveBall": "When asked about team engagement ritual, described fun card game tradition: 'We played card games in break. We made a trick about who will get ones...' Creative, low-pressure engagement.",
            "microCase": "Consistent warmth and humor throughout interview. Laughing easily, relaxed demeanor."
        }
    ],
    "passingLogic": "0 minuses, 2 plus-minuses = PASS",
    "finalComments": "PASS - Meer Muneeb shows strong alignment with team values (All for One 5/5), solid persistence, and brings joy to team environment. Ready for Right Seat interview.",
    "proceedToRightSeat": True,
    "gwcAssessment": {
        "getsIt": "YES - Demonstrates understanding of teamwork, growth, and resilience.",
        "wantsIt": "YES - Genuine interest in growth and learning. Flexible on tech stack when role required it.",
        "capacity": "YES - Technical maturity (3–4 years FSD), team maturity (group leader experience), bandwidth evident."
    }
}

UPDATE = {
    "application_id": 677,
    "scorecard": SCORECARD_MEER_MUNEEB,
    "result": "pass",
    "interviewer": "Ayesha Khan",
    "status": "shortlisted"
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    interview_date = datetime(2026, 5, 5)

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
