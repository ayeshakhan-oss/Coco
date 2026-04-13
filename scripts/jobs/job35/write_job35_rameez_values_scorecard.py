"""
Write values scorecard for Rameez Wasif (app 1878)
Job 35 — Junior Research Associate, Impact & Policy
Interview conducted: 2026-03-26 by Jawwad Ali
Result: PASS
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

SCORECARD_RAMEEZ = {
    "date": "Mar 26, 2026",
    "host": "Jawwad Ali",
    "candidateName": "Rameez Wasif",
    "noteTaker": "",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "FYP (computer vision model) — sustained effort despite a persistent communication gap with faculty who lacked the technical expertise to properly evaluate the team's work, resulting in consistently average marks. Rather than quitting, Rameez continued because the project was building his own skill set. When asked how he manages emotionally after disappointing evaluations, he described: following up with the instructor at office hours, acting as team lead to re-energise teammates who went quiet for days after bad marks, and scheduling more frequent team meetings to assess progress and plan next steps.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": "Age of Peace international exchange programme (2019–2022) — cross-border dialogue between Pakistani and Indian youth. Rameez noticed that some participants were being talked over or lacked the confidence to contribute. He and another participant shifted their role from active debaters to facilitators: using open-ended questions deliberately directed toward quieter group members to surface their views. Notably, Rameez mentioned he has been on both sides of this dynamic — he himself needed that amplification at an earlier stage — which adds self-awareness to the example.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Volunteer work at STEAM Pakistan (Karachi) — a lean 4–5 person team spending approximately two days manually creating graphs from portal data. End-to-end automation was not feasible because the software team was in Islamabad and there was no API access. Rameez designed a pragmatic Google Apps Script workaround: download portal data, upload to Google Sheets, run the script — graphs generated in one click. He explicitly noted that the simpler solution achieved the same objective faster than chasing the ideal one.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": "Two upward feedback examples: (1) Identified a login-bypass security vulnerability in STEAM Pakistan's portal — exploitable without credentials. Reported it to the team and then wrote a full technical report covering security flaws, speed issues, and system crashes. The report is currently in the approval pipeline via the School Education and Literacy Department of Sindh. (2) In a research project with a university professor, identified that informal settlements in a specific division had been excluded from scope — flagged this, and the professor incorporated them. Additionally, when asked about receiving hard feedback: Rameez disclosed he has a speech impairment and used it as an excuse to avoid public speaking. Someone gave him direct feedback on this. He initially resisted but reflected and acted — began attending internship interviews, speaking more in social settings, and is now doing this interview.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "Spent two years practicing harmonium to earn a place in the university orchestra. Made it in. In final year, recognised the time commitment was pulling too much from career priorities — interviews, applications. Made the deliberate call to step back from performing, but stayed engaged with the subject by taking two music courses (folk music, history of Indian music). The decision-making logic is sound and the pivot is clean. However the example is personal and hobby-context: there is no evidence of this behaviour in a professional, team, or organisational setting. No stakes around releasing something others depended on.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Chose the surfing emoji. Described himself as someone who makes room for things that don't exist yet. Teaching himself to surf independently in Karachi — going into the ocean on a board without formal instruction, using YouTube. Moved from Islamabad to Karachi alone for his studies, against the norm and against obvious logistical challenges — and made a rich experience out of it. Sports enthusiast: football, table tennis, surfing. The answer was energetic and unprompted in its authenticity — he conveyed joy in the process of doing things, not just the outcomes.",
            "curveBall": "",
            "microCase": ""
        }
    ],
    "finalComments": "Rameez cleared all six values. His strongest moments: the STEAM Pakistan Google Apps Script automation (V3), the two-part courageous conversations answer including the speech impairment reflection (V4), and the Age of Peace facilitation example (V2). One +/- on Don't Hold On Too Tight — the example is valid but hobby-context, no evidence of this in a work or team setting. No minuses. Result: PASS. GWC: Gets it YES / Wants it YES / Capacity YES. Advance to case study.",
    "proceedToRightSeat": "Yes"
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        UPDATE applications
        SET values_scorecard = %s,
            values_interview_result = %s,
            values_interview_date = %s,
            values_interviewer_name = %s,
            status = %s
        WHERE id = %s
    """, (
        json.dumps(SCORECARD_RAMEEZ),
        "pass",
        datetime(2026, 3, 26),
        "Jawwad Ali",
        "shortlisted",
        1878
    ))

    conn.commit()
    cur.close()
    conn.close()
    print("Done. App 1878 (Rameez Wasif) — PASS, scorecard written.")

if __name__ == "__main__":
    main()
