"""
Delete problematic application and create fresh one with exact Laiba structure
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

FRESH_SCORECARD = {
    "date": "2026-05-13",
    "host": "Ayesha Khan",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Internship with Odoo: Backend logic and workflow understanding was very difficult initially. Hassan persisted: 'until the task is completed, it doesn't [break me]' — stayed focused and completed despite steep learning curve.",
            "curveBall": "Final year project with simultaneous internship burden: Heavy workload from multiple commitments. Response showed persistence: 'with teamwork, we managed to manage' — persisted through difficulty with team support. Fresher showing strong resilience in learning difficult technologies.",
            "microCase": "When asked about volunteering for ugly problems, acknowledged it's an area to develop: 'didn't have until now' — honest self-awareness. Shows foundation of persistence but room to grow in proactive problem-seeking."
        },
        {
            "name": "All for One and One for All",
            "rating": "+",
            "deepDive": "Cricket background emphasizes collective success: 'Most important thing is the team work... Individual performance, you can't... If someone has bad performance, they can back it so they can improve.' Strong language on group responsibility over individual glory.",
            "curveBall": "Lifting quiet/shy team members: Team had introverted member who was hesitant. Hassan's response: 'We tried [to] give lot [of confidence]... he give lot of opinions... we had a presentation.' Showed intentional mentoring and confidence-building.",
            "microCase": "Consistent language throughout interview emphasizing collective effort, bringing team together, shared responsibility. Natural tendency toward team-first mindset."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+/-",
            "deepDive": "Odoo learning: 'When Odoo launches a new version, changes logic... when we adopt it, we little bit of time, but we manage it. R&D and communication.' Shows willingness to research and learn new platforms.",
            "curveBall": "When asked about difficult courses: Compiler construction course was 'very boring and boring subject.' Some indication of resistance when learning gets abstract or feels disconnected from practical application.",
            "microCase": "Mentions 'workflows and automations, I have seen' — exposure to new systems but minimal evidence of leading learning initiatives or seeking continuous improvement beyond required tasks."
        },
        {
            "name": "Courageous Conversations",
            "rating": "+/-",
            "deepDive": "When directly asked about giving difficult feedback: 'I have not [given difficult] feedback to anyone.' Honest acknowledgment that this is not yet developed — fresher with limited experience in this area.",
            "curveBall": "Teaching experience mentioned but vaguely: 'I had face lot of [challenges]... students' — answer was unclear due to audio distortion, but didn't demonstrate specific examples of courageous conversation skill.",
            "microCase": "Receiving feedback: 'People often told me my communication skills are a little bit less. So, I had to talk the communication level... [improved].' Shows growth mindset and willingness to work on feedback, even if not yet skilled at giving it."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "Student records project: Initially tried to handle front-end himself thinking 'I could do lot,' but realized 'it was a lot of work.' Rather than struggle, he delegated: 'I gave it [to you].' Explicitly shows flexibility and willingness to let go of control.",
            "curveBall": "Handoff maturity: Reflected on learning from delegation: 'So we learned a lot learning, learning, learning about...' Shows growth from letting go of ownership. Willing to trust teammates with responsibility.",
            "microCase": "Pattern of adapting roles, accepting help, sharing responsibility throughout interview. Shows early adaptability and flexibility."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Emoji choice—smiling face: 'Reason: Basically, when we work on a team... if you have a frustration, if you have a task which is difficult, if you have a confusion, then your team will also be...' Hassan sees his role as bringing positive energy to balance team stress.",
            "curveBall": "Silly ritual—team bonding trip: 'When we business, I wanted to a trip to all of us. So, everyone has contributed to gathering... Because the trip, the response came.' Proactively organizes team engagement activities, celebrates collective wins.",
            "microCase": "Consistently warm, collaborative tone throughout interview. Brings lightness to discussion of difficult challenges. Natural joy-bringer."
        }
    ],
    "noteTaker": "Coco",
    "candidateName": "Muhammad Hassan Baig",
    "finalComments": "PASS - Hassan demonstrates strong foundation in All for One (team-first mindset), Don't Hold On Too Tight (delegation & flexibility), and Practice Joy (positive energy). Plus-minuses in Continuously Improve (some resistance to abstract learning) and Courageous Conversations (not yet developed, normal for fresher). As a fresher, Hassan shows exceptional resilience in technical learning (Odoo) and teamwork. Ready for Right Seat interview to assess technical depth and leadership potential.",
    "gwcAssessment": {
        "getsIt": "YES - Understands team values, collective success, flexibility, joy. Clear alignment.",
        "wantsIt": "YES - Genuine enthusiasm about Taleemabad culture: 'friendly environment, communications, team work, flexibility.' Not just seeking employment.",
        "capacity": "YES - Experience with complex systems (Odoo), teaching/mentoring background, accepts feedback, demonstrates growth. Has bandwidth for technical and leadership growth."
    },
    "recordingLink": "https://fathom.video/share/fHzJjsfbtfUseVb1-AwcMXsq8x_hCWSR",
    "proceedToRightSeat": "Yes"
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Delete the old problematic application
    cur.execute("DELETE FROM applications WHERE id = 3185")
    print(f"[OK] Deleted problematic application 3185")

    # Get max ID and create new application with fresh data
    cur.execute(
        "INSERT INTO applications (candidate_id, job_id, status, stage) VALUES (%s, %s, %s, %s) RETURNING id",
        (2561, 34, "new", "Applied")
    )
    new_app_id = cur.fetchone()[0]
    print(f"[OK] Created fresh application (ID: {new_app_id})")

    # Submit with ALL fields populated
    cur.execute(
        """
        UPDATE applications
        SET values_scorecard = %s,
            values_interview_result = %s,
            values_interview_score = %s,
            values_interview_notes = %s,
            values_interview_date = %s,
            values_interviewer_name = %s,
            stage = %s,
            status = %s
        WHERE id = %s
        """,
        (
            json.dumps(FRESH_SCORECARD),
            "pass",
            10,
            "PASS - 4 pluses (All for One, Don't Hold On Too Tight, Practice Joy, Don't Walk Away), 2 plus-minuses (Continuously Improve, Courageous Conversations). Zero minuses. GWC: Gets it (YES), Wants it (YES), Capacity (YES). Ready for Right Seat interview.",
            datetime(2026, 5, 13),
            "Ayesha Khan",
            "Values Interview Complete",
            "shortlisted",
            new_app_id
        )
    )

    print(f"[OK] Submitted fresh scorecard with all fields (App {new_app_id})")
    print(f"[OK] Use App {new_app_id} — refresh Markaz and the form should populate!")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
