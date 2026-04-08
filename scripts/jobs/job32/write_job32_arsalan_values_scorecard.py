"""
Job 32 — Fundraising & Partnerships Manager
Write Syed Arsalan Ashraf's values scorecard to Markaz DB
Application ID: 1851
Result: FAIL (OUT) — 3 pluses, 3 +/-, 0 minuses (≥3 +/- = OUT)

NOTE: JSON schema must match Markaz UI format exactly:
{ date, host, candidateName, noteTaker, values: [{name, rating, deepDive, curveBall, microCase}],
  finalComments, proceedToRightSeat }
"""

import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import psycopg2
from dotenv import load_dotenv
from scripts.utils.audit_log import log_db_query

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

APP_ID = 1851

SCORECARD = {
    "date": "Apr 2, 2026",
    "host": "Ayesha Khan",
    "candidateName": "Syed Arsalan Ashraf",
    "noteTaker": "",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": (
                "Flood relief fundraising: raised funds, then discovered 4 months later that implementation "
                "was not meeting donor commitments. Stepped outside his remit, went directly to CEO, "
                "requested access to the implementation side, and personally stepped in. Quote: 'I individually "
                "or personally reach out to the CEO and requested him for an access to the implementation "
                "side as well. And then I personally get into it and did the implementation part as well "
                "because it was very important to ensure that the donors are satisfied.' Strong ownership signal. "
                "Leniency applied — audio conditions during this value (background noise, connectivity issues)."
            ),
            "curveBall": (
                "When redirected to the specific 'almost quit' moment, answer became generic: 'There are a lot "
                "of projects that we initiate but they could not fulfill the requirements... we are bound because "
                "of the partnerships we have created.' Described staying out of obligation rather than a conscious "
                "decision to push through. No specific inflection point named. Inconclusive given audio conditions."
            ),
            "microCase": ""
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": (
                "At Astro Tech Academy, the director was unable to bring in funded projects or training programmes. "
                "Arsalan intervened on his own initiative: raised funds from government and local organisations, "
                "brought in free-of-cost programmes, and created a scholarship stream to solve the director's "
                "student fees problem. Quote: 'I intervened into it or probably saved him from this hassle of "
                "having a low number in classes.' Not asked. Noticed and acted."
            ),
            "curveBall": (
                "Personally monitors deliverables even when delegated: 'I personally look into it because I want "
                "to keep that word with the donor.' When issues go unreported, he investigates and helps. "
                "Attributes this to having been helped himself early in his career. Two strong, consistent examples."
            ),
            "microCase": ""
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+/-",
            "deepDive": (
                "Quote: 'I am not totally into book reading because I used to read books online but later on "
                "there has been a lot of occupancy... there is always a deadline coming up to submit a proposal... "
                "and then I have a family as well. So now I am not into the book reading part.' Honest but shows "
                "limited active investment in personal growth outside work."
            ),
            "curveBall": (
                "Career counselling and mentorship sessions at IBA Karachi and Dow University. British Council "
                "Active Citizens certification on soft skills training. Both examples are institutional and "
                "historical — part of job scope, not personal initiatives. No evidence of actively seeking "
                "new learning in recent months."
            ),
            "microCase": ""
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": (
                "At IBA, proposed creating a corporate leg for an international marketing conference to fund it "
                "locally when no budget existed. Brought in HBL, Gunnebo, GreenStar as partners. Real examples "
                "but framed as proactive suggestions and ideas, not confronting a difficult decision or "
                "delivering a hard truth to someone."
            ),
            "curveBall": (
                "Question about receiving difficult feedback had to be redirected twice. First drifted to positive "
                "feedback. After explicit redirect, described late comings and rationalised: 'When you are working "
                "at night... it is not possible for you to reach early.' He defended against the feedback rather "
                "than sitting with it. Never named a specific piece of feedback that genuinely required honest "
                "reflection. Two redirects, still did not land."
            ),
            "microCase": ""
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": (
                "Flat no on handover question. Quote: 'No, I have been the person who has been assigned different "
                "projects and tasks because it was not doing better in other people. So I think this has not "
                "happened with me as of now.' Framed the reverse — he is always the one brought in to rescue "
                "failing work. Did not try to reframe or find an adjacent example."
            ),
            "curveBall": (
                "A junior hire showed him an AI-based tool for bulk email and WhatsApp messaging. Quote: 'What "
                "we were doing in 2 days, we now been able to do it in 20 minutes.' He adopted the tool and "
                "formally recognised the junior. Open to learning from below, but the core 'let go' instinct "
                "is not yet visible. He is a holder, not a releaser."
            ),
            "microCase": ""
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": (
                "Chose the laugh-cry emoji. Quote: 'I am very loved by these people... whenever I meet them, "
                "it is always a very friendly way of me meeting others.' Describes keeping energy high across "
                "all departments including international teams. Also showed dimension: 'If they are doing it "
                "deliberately, I make sure that they provide those results that are being requested.' "
                "Joy with accountability alongside it. Authentic and warm — not rehearsed."
            ),
            "curveBall": "",
            "microCase": ""
        }
    ],
    "finalComments": (
        "Arsalan is a genuine fundraising professional with a real track record across IBA, Dow University, "
        "Hands Pakistan, flood relief work, and private sector. Functional fit for this role is solid. "
        "Three gaps are consistent with each other: limited active investment in personal growth "
        "(Continuously Improve), difficulty sitting with uncomfortable feedback (Courageous Conversations), "
        "and holding on to ownership rather than releasing it (Don't Hold On Too Tight). Not character "
        "concerns — patterns suggesting someone earlier in their values journey than this role requires. "
        "All for One and Practice Joy are genuine strengths. These gaps are developable. "
        "Result: OUT. 3 pluses, 3 +/-, 0 minuses — triggers the >= 3 +/- threshold. "
        "Note: Values 1-2 evaluated with leniency due to audio conditions (background noise, connectivity issues, "
        "location change mid-call). Values 3-6 evaluated strictly on transcript content."
    ),
    "proceedToRightSeat": "No"
}


def main():
    print(f"Writing values scorecard for Syed Arsalan Ashraf (app_id={APP_ID})...")

    conn = psycopg2.connect(
        host="ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
        dbname="neondb", user="neondb_owner",
        password="npg_kBQ10OASHEmd", sslmode="require"
    )
    cur = conn.cursor()

    cur.execute("""
        UPDATE applications SET
            values_scorecard        = %s,
            values_interview_result = %s,
            values_interview_date   = %s,
            values_interviewer_name = %s,
            values_interview_notes  = %s,
            status                  = %s
        WHERE id = %s
    """, (
        json.dumps(SCORECARD),
        "fail",
        "2026-04-02",
        "Ayesha Khan",
        "OUT — 3 pluses, 3 +/-, 0 minuses. Values: Don't Walk Away (+), All for One (+), "
        "Continuously Improve (+/-), Courageous Conversations (+/-), Don't Hold On Too Tight (+/-), "
        "Practice Joy (+). Audio condition note: Values 1-2 under noisy conditions, leniency applied.",
        "rejected",
        APP_ID,
    ))

    conn.commit()
    rows = cur.rowcount
    cur.close()
    conn.close()

    log_db_query(
        table="applications",
        filters=f"id={APP_ID}",
        rows_returned=rows,
        context="write_job32_arsalan_values_scorecard"
    )

    print(f"Done. {rows} row(s) updated.")
    print(f"  values_interview_result : fail")
    print(f"  values_interview_date   : 2026-04-02")
    print(f"  status                  : values_failed")
    print(f"  scorecard format        : Markaz-compatible")


if __name__ == "__main__":
    main()
