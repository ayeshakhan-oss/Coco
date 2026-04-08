"""
Write values scorecards for Nain Tara (app 1534) and Muhammad Junaid (app 1592)
Job 35 — Junior Research Associate, Impact & Policy
Also corrects Nain Tara Job 36 (app 1536) → rejected (not qualified for Field Coordinator)
Interviews conducted: 2026-04-06
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

SCORECARD_JUNAID = {
    "date": "Apr 6, 2026",
    "host": "Ayesha Khan",
    "candidateName": "Muhammad Junaid",
    "noteTaker": "",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Junaid described his MPhil second semester — heavy courseload with economic growth and investment theories, teachers who abandoned coursework mid-semester, leaving students entirely to self-study. He was about to quit but chose to stay, working 8am to midnight in the university hostel, combining YouTube learning with peer collaboration to pass all courses.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "All for One & One for All",
            "rating": "+/-",
            "deepDive": "Junaid described a colleague at Aaj Humanitarian Organization who had poor office ethics — not greeting colleagues, lacking basic professional manners. Rather than directly flagging the issue, Junaid used informal conversations and practical examples to guide him. Thoughtful approach, but the answer does not demonstrate covering a mistake or sacrificing his own work for a teammate. The question asked for backup behaviour; he answered with mentoring behaviour.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Strongest answer in the interview. Junaid named specific tools and platforms: MATLAB (learned for thesis optimization via Coursera, not required but self-initiated), World Bank research methodology program, Elsevier journal publication training. Certificates from Coursera. Credible, specific, and proactive — not generic.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Junaid described providing daily feedback to Taleemabad data and impact team leads after field work — post-field WhatsApp debriefs, Zoom meetings, field challenge reports. Also published field observations in Friday Times newspaper. Demonstrates a habit of surfacing issues upward. However the answer stays at the level of reporting problems to managers, not confronting a person directly or navigating resistance. No personal feedback example.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "Junaid described delegating a thematic analysis and conclusion section of an MPhil thesis to a student because he lacked time and the student had relevant expertise. Structurally fits the value. However the example lacks stakes — he was outsourcing freelance work he had taken on, not releasing something he was personally invested in or protective of. No emotional depth or narrative of letting go.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Practice Joy",
            "rating": "-",
            "deepDive": "When asked to describe himself as one emoji, Junaid said thumbs up and praised Taleemabad's office culture as friendly and productive. There is no example of him creating joy for others, no specific action, no story about lifting a teammate. He described the environment, not his role in shaping it. No evidence of initiative around team wellbeing or positivity.",
            "curveBall": "",
            "microCase": ""
        }
    ],
    "finalComments": "Junaid shows genuine commitment to continuous learning and field experience credibility — his MATLAB and World Bank training answers are his strongest moments. However three values came in at +/- and Practice Joy was a clear minus. Result: OUT. 1 minus + 3 +/- exceeds threshold on both counts.",
    "proceedToRightSeat": "No"
}

SCORECARD_NAIN_TARA = {
    "date": "Apr 6, 2026",
    "host": "Ayat Butt",
    "candidateName": "Nain Tara",
    "noteTaker": "",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Two credible examples. First: research internship at WWF Hunza — difficult field conditions, poor office culture, heavy workload alongside studies. Found a fellow intern to partner with, stayed and completed the project well. Second: thesis writing as teaching assistant — repetitive, exhausting, done under tight deadlines set by professor. Stayed because it was building future research capability. Consistent theme: discomfort, finding a path, not leaving.",
            "curveBall": "Scenario (laptop stolen at airport, demo in 3 hours): Analysed the problem, set an objective, leveraged her communication strength to ask a nearby person at the airport to borrow their laptop. Calm and practical under pressure.",
            "microCase": ""
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": "At WWF, a fellow intern had no idea how to write a proposal and was stuck. Nain Tara abandoned her own proposal work entirely to help this colleague structure and write hers. The colleague then presented it to the supervisor successfully. Nain Tara's own proposal was not submitted. Clearest and most specific team backup example in the interview — she explicitly sacrificed her own deliverable.",
            "curveBall": "Bonus pool scenario: Would distribute based on consistency, loyalty, and quality of work (clean and transparent data). Merit-based with named criteria — not uniform, not arbitrary.",
            "microCase": ""
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Erasmus Mundus scholarship failure — was confident she would succeed, got rejected, was heartbroken. Used it to identify gaps and keep building rather than withdrawing. Also described actively returning to YouTube to polish SPSS after a period of disuse during a job. Genuine orientation toward growth through failure rather than despite it.",
            "curveBall": "Asked to design a 1-week crash course: objective-setting first, then key topics, then timeline. Structured and logical if a bit generic. The unlearn/modify question drew a weaker answer — she said she hasn't had to truly unlearn anything, just keeps refreshing skills. Honest but slightly blind to the question's intent.",
            "microCase": ""
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": "Gave harsh feedback to her brother — told him he needs to prioritise himself before giving to others, or people will exploit him. Saw the pattern once, twice, three times before she said it. Framed deliberately and with care. Role-play (confront low-quality colleague): First reviews the work to identify specific segments, names the issue, checks if confidence or skill gap is the root cause, offers guidance on timelines and methods. Frames it as coaching, not confrontation — correct instinct.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "Example: women's empowerment reforestation project in Hunza as forest and social expert — deeply aligned with her personal values. Had to let it go when the contract ended. The example is somewhat forced — the letting go was circumstantial (contract ended), not a deliberate choice. No clear moment of proactively stepping back.",
            "curveBall": "Investor pivot scenario at WWF: apricot harvesting product packaging complete, contract fell through at final stage. Rather than abandoning the project, went back to market to find alternative buyers. Adapted without giving up. Strong adaptive response.",
            "microCase": ""
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Colleague Hussain lost his mother, returned to office grieving after 2-3 weeks. Nain Tara and the whole staff organised a small birthday celebration to rebuild his confidence and bring him back into the team. Specific, emotionally resonant, and real — demonstrates joy as a leadership tool, not just a personal mood.",
            "curveBall": "",
            "microCase": ""
        }
    ],
    "finalComments": "Nain Tara cleared all six values comfortably. Her strongest moments: sacrificing her own proposal to help a fellow intern (V2), the Erasmus Mundus failure story (V3), and the birthday celebration for a grieving colleague (V6). One +/- on Don't Hold On Too Tight — circumstantial rather than deliberate. No minuses. Result: PASS. Advance to case study.",
    "proceedToRightSeat": "Yes"
}

interview_date = datetime(2026, 4, 6)

UPDATES = [
    # Job 35 — Nain Tara PASS
    {
        "application_id": 1534,
        "scorecard": SCORECARD_NAIN_TARA,
        "result": "pass",
        "interviewer": "Ayat Butt",
        "status": "shortlisted"
    },
    # Job 35 — Junaid FAIL
    {
        "application_id": 1592,
        "scorecard": SCORECARD_JUNAID,
        "result": "fail",
        "interviewer": "Ayesha Khan",
        "status": "rejected"
    },
    # Job 36 — Nain Tara correction → rejected (not qualified for Field Coordinator)
    {
        "application_id": 1536,
        "scorecard": None,  # keep existing scorecard, just update status
        "result": "fail",
        "interviewer": None,
        "status": "rejected"
    },
]

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for u in UPDATES:
        if u["scorecard"] is not None:
            cur.execute("""
                UPDATE applications
                SET values_scorecard = %s,
                    values_interview_result = %s,
                    values_interview_date = %s,
                    values_interviewer_name = %s,
                    status = %s
                WHERE id = %s
            """, (
                json.dumps(u["scorecard"]),
                u["result"],
                interview_date,
                u["interviewer"],
                u["status"],
                u["application_id"]
            ))
        else:
            # Just update status + result, preserve existing scorecard
            cur.execute("""
                UPDATE applications
                SET values_interview_result = %s,
                    status = %s
                WHERE id = %s
            """, (
                u["result"],
                u["status"],
                u["application_id"]
            ))
        print(f"Updated app {u['application_id']} | {u['result'].upper()} / {u['status']}")

    conn.commit()
    cur.close()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    main()
