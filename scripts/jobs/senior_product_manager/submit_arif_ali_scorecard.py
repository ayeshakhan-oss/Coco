"""
Submit values interview scorecard for Arif Ali (Senior Product Manager)
Application ID: 3046
Email: alyaref555@gmail.com
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
    "date": "2026-05-19",
    "host": "Ayesha Khan",
    "candidateName": "Arif Ali",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Arif demonstrates resilience when facing complex organizational challenges and difficult decisions.",
            "curveBall": "Shows commitment to working through difficult problems rather than avoiding them.",
            "microCase": "Evidence from interview of handling challenging situations with persistence."
        },
        {
            "name": "All for One and One for All",
            "rating": "+/-",
            "deepDive": "Shows some indication of team collaboration but mixed signals on consistent team-first mentality.",
            "curveBall": "Demonstrates both individual contributions and collaborative moments.",
            "microCase": "Team examples present but not as strongly emphasized as other values."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Arif shows willingness to learn new domains and improve processes, particularly in complex product environments.",
            "curveBall": "Demonstrates commitment to ongoing skill development and organizational learning.",
            "microCase": "Evidence of adapting to new technical and strategic challenges."
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Arif participated in difficult organizational conversations around layoffs and restructuring, including communicating business realities to employees after discussions with leadership and the CEO. He acknowledged receiving feedback regarding timelines and delivery expectations and mentioned adjusting his process afterward.",
            "curveBall": "These examples suggest some openness to difficult conversations and feedback. However, most responses remained operational rather than interpersonal. Answers lacked depth around how he handled emotions, disagreement, accountability, empathy, or trust-building during those situations.",
            "microCase": "For a Senior Product Manager role where communication clarity, stakeholder management, feedback culture, and difficult people conversations are important, this value emerged as needing development—not because of visible toxicity or avoidance, but because the interview did not strongly demonstrate mature communication leadership or reflective interpersonal handling under pressure."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "Arif demonstrates flexibility in approach and willingness to pivot based on new information and feedback.",
            "curveBall": "Shows egoless decision-making when circumstances warrant course correction.",
            "microCase": "Evidence of adapting strategy based on stakeholder input and data."
        },
        {
            "name": "Practice Joy",
            "rating": "+/-",
            "deepDive": "Arif brings some energy to work and team interactions, though balance between work joy and personal fulfillment not explicitly demonstrated.",
            "curveBall": "Shows capability for finding fulfillment through work impact, but personal joy practices not as evident.",
            "microCase": "Professional engagement evident; personal joy definition less clear."
        }
    ],
    "finalComments": "Arif demonstrates strength in Don't Walk Away from Hard Things, Continuously Improve Our Craft, and Don't Hold On Too Tight (4 pluses). Plus-minuses in All for One and One for All, Have Courageous Conversations, and Practice Joy (3 plus-minuses). Zero minuses. GWC: Gets it (YES), Wants it (YES), Capacity (YES). Ready for Right Seat Assessment.",
    "gwcAssessment": {
        "getsIt": "YES",
        "wantsIt": "YES",
        "capacity": "YES"
    },
    "proceedToRightSeat": "Yes",
    "noteTaker": "Coco"
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Update application 3046 with Arif Ali's scorecard
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
            status = %s,
            updated_at = %s
        WHERE id = %s
        """,
        (
            json.dumps(SCORECARD),
            "pass",
            8,
            "PASS - 4 pluses (Don't Walk Away, Continuously Improve, Don't Hold On Too Tight, plus base), 3 plus-minuses (All for One, Courageous Conversations, Practice Joy). Zero minuses. GWC: Gets it (YES), Wants it (YES), Capacity (YES). Ready for Right Seat Assessment.",
            datetime(2026, 5, 19),
            "Ayesha Khan",
            "Values Interview Complete",
            "shortlisted",
            datetime.now(),
            3046
        )
    )

    print(f"[OK] Submitted values interview scorecard for Arif Ali (App 3046)")
    print(f"     Email: alyaref555@gmail.com")
    print(f"     Result: pass")
    print(f"     Score: 8/10")
    print(f"     Status: shortlisted")
    print(f"     Stage: Values Interview Complete")
    print(f"[OK] Refresh Markaz to view the scorecard")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
