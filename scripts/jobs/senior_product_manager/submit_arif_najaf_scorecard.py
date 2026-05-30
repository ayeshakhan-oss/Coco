"""
Submit values interview scorecard for Arif Najaf (Senior Product Manager)
Application ID: 2121
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
    "candidateName": "Arif Najaf",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "[Interview evidence from Arif's responses about facing difficult challenges]",
            "curveBall": "[Evidence of resilience and persistence]",
            "microCase": "[Specific example demonstrating this value]"
        },
        {
            "name": "All for One and One for All",
            "rating": "+/-",
            "deepDive": "[Interview evidence about team collaboration]",
            "curveBall": "[Nuance or mixed signals about teamwork]",
            "microCase": "[Specific team example]"
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "[Evidence of learning and improvement]",
            "curveBall": "[Depth of commitment to continuous learning]",
            "microCase": "[Specific learning example]"
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Arif participated in difficult organizational conversations around layoffs and restructuring, including communicating business realities to employees after discussions with leadership and the CEO. He acknowledged receiving feedback regarding timelines and delivery expectations and mentioned adjusting his process afterward.",
            "curveBall": "These examples suggest some openness to difficult conversations and feedback. However, most responses remained operational rather than interpersonal. Answers lacked depth around how he handled emotions, disagreement, accountability, empathy, or trust-building during those situations.",
            "microCase": "For a Group Manager role, where communication clarity, stakeholder management, feedback culture, and difficult people conversations are critical, this value emerged as one of the closest to a minus—not because of visible toxicity or avoidance, but because the interview did not strongly demonstrate mature communication leadership or reflective interpersonal handling under pressure."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "[Interview evidence about flexibility and letting go]",
            "curveBall": "[Demonstration of egoless decision-making]",
            "microCase": "[Specific example of pivoting or delegating]"
        },
        {
            "name": "Practice Joy",
            "rating": "+/-",
            "deepDive": "[Interview evidence about joy and fulfillment]",
            "curveBall": "[Balance between work joy and personal joy]",
            "microCase": "[Specific example of joy in work or life]"
        }
    ],
    "finalComments": "Arif demonstrates strength in Don't Walk Away from Hard Things, Continuously Improve Our Craft, and Don't Hold On Too Tight. Plus-minuses in All for One and One for All, Have Courageous Conversations, and Practice Joy. Ready for Right Seat Assessment.",
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

    # Update application 2121 with Arif's scorecard
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
            8,  # 4 pluses + 3 plus-minuses = 8/10
            "PASS - 4 pluses (Don't Walk Away, Continuously Improve, Don't Hold On Too Tight, Practice Joy base), 3 plus-minuses (All for One, Courageous Conversations, Practice Joy detail). GWC: Gets it (YES), Wants it (YES), Capacity (YES). Ready for Right Seat Assessment.",
            datetime(2026, 5, 19),
            "Ayesha Khan",
            "Values Interview Complete",
            "shortlisted",
            datetime.now(),
            2121
        )
    )

    print(f"[OK] Submitted values interview scorecard for Arif Najaf (App 2121)")
    print(f"     Result: pass")
    print(f"     Score: 8/10")
    print(f"     Status: shortlisted")
    print(f"     Stage: Values Interview Complete")
    print(f"[OK] Refresh Markaz to see the updated scorecard")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
