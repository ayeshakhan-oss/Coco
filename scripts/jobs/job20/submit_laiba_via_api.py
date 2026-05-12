"""
Submit Laiba Ahmad's values scorecard via Markaz API
Attempts to POST the complete scorecard data to Markaz backend
"""

import requests
import json

# Markaz API endpoint (trying common patterns)
MARKAZ_BASE_URL = "https://markaz.taleemabad.com"
APPLICATION_ID = 1389

SCORECARD_DATA = {
    "candidateName": "Laiba Ahmad",
    "date": "May 12, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "Coco",
    "recordingLink": "https://fathom.video/share/n-_Q9Thxyz5rkisz6ALQ7jBzo5NNdA7r",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Resigned from Invest Innovate to pivot to direct product ownership. Working on compliance AI product - completely new vertical with high complexity. Recently faced major code break after client delivery - wanted to quit. Instead, got team together, identified systematic code review issues, implemented structured reviews and AI regression testing agent.",
            "curveBall": "Invest Innovate accelerator had unmet donor targets through 6 rounds. Created AI diagnostic tool for startups, increased program NPS by 30%.",
            "microCase": "Worked with marginalized women entrepreneurs on strict donor deadlines. Created custom Urdu e-commerce solution."
        },
        {
            "name": "All for One and One for All",
            "rating": "+",
            "deepDive": "At Invest Innovate conference, co-lead faced logistics crisis. Suggested co-leading workshop while waiting for trainer. Divided responsibilities, team executed. Result had better feedback than trainer's portion.",
            "curveBall": "Surfacing quiet voices: Associate was brilliant but insecure. Created 6-month structured roadmap starting with 1-on-1s, progressing to working groups. Employee now has master's scholarship abroad.",
            "microCase": "Celebrates colleague Saba Kulsoom for confidence and pushing back against leadership."
        },
        {
            "name": "Continue to Improve Our Craft",
            "rating": "+",
            "deepDive": "Recently learned product iteration in compliance/audit space. Ran 6 rounds of accelerator with continuous feedback and improvement. Result: 4 startups launched in Saudi Arabia, 7-8 raised funding.",
            "curveBall": "Teaching while learning: Co-founded social enterprise, started own tote bag business (DEET) to understand nuances. Teaches what worked AND what didn't.",
            "microCase": "Advises younger sister on career, sharing what she knows plus what she's still learning."
        },
        {
            "name": "Courageous Conversations",
            "rating": "+",
            "deepDive": "New engineer caused major code break. Senior leadership wanted scapegoat. Took stand using concrete examples, changed their minds that it's systematic, not personal. Gave difficult feedback to engineer with validation and clear expectations.",
            "curveBall": "Performance review feedback on visibility: Initial reaction frustrated/defensive. Ranted then reflected. Followed up with manager 3 days later, restructured workflows. Complete turnaround in 2 months.",
            "microCase": "Articulates red flags in leaders: unrealistic timelines without team input, pressure without support, reactive decisions."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "In professional life, has not handed off projects for better impact. Instead, co-creates and gets support while remaining owner. Asian Development Bank project - technical, new to her. Brainstormed with manager, she executed, won project.",
            "curveBall": "Open to perspective change from junior staff. Fresh grad associate suggested product scoring rubric variations with configurables for industry/stage.",
            "microCase": "Values changing perspectives based on junior input."
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Pink teddy bear gangster meme - cute inside but acting tough outside. Buttercup meme - first 30 mins after waking unapproachable without coffee.",
            "curveBall": "Silly ritual: Zip Zap Zop game from A-level camp. Standing in circle, sending energy, people laugh. Fun brain activator. Mentions trips and physical activities bond teams.",
            "microCase": "Engages warmly, relatable personality, brings humor throughout call."
        }
    ],
    "passingLogic": "0 minuses, 1 plus-minus = PASS",
    "finalComments": "PASS - Laiba Ahmad demonstrates exceptional strength in Don't Walk Away (multiple complex problems solved systematically), All for One (mentoring quiet voices to excellence), Continuously Improve (learning in new fields, teaching while learning), and Courageous Conversations (difficult feedback handled with care and follow-through). One +/- on Don't Hold On Too Tight. Strong product leadership orientation, team-focused, willing to absorb pressure and solve messy problems. Ready for Right Seat interview.",
    "gwcAssessment": {
        "getsIt": "YES - Deeply understands team values. All examples show internalization: persistent problem-solving, team lifting, humility in learning, courageous feedback, adaptability.",
        "wantsIt": "YES - Career pivots show genuine interest in growth and impact. Values team environment, takes on hard problems, invests in others' development.",
        "capacity": "YES - Leadership experience (CEO WeCamp, senior program lead Invest Innovate), product management expertise, AI/compliance knowledge, proven team development. Ready to execute on values."
    },
    "proceedToRightSeat": "Yes"
}

def submit_via_api():
    endpoints = [
        f"{MARKAZ_BASE_URL}/api/applications/{APPLICATION_ID}/values-scorecard",
        f"{MARKAZ_BASE_URL}/api/applications/{APPLICATION_ID}/submit-values",
        f"{MARKAZ_BASE_URL}/api/values-scorecard",
        f"{MARKAZ_BASE_URL}/api/talent-acquisition/values-scorecard/{APPLICATION_ID}",
    ]

    headers = {
        "Content-Type": "application/json",
    }

    for endpoint in endpoints:
        try:
            print(f"[ATTEMPT] POST {endpoint}")
            response = requests.post(endpoint, json=SCORECARD_DATA, headers=headers, timeout=5)
            print(f"[RESPONSE] Status: {response.status_code}")
            if response.status_code in [200, 201, 202]:
                print(f"[SUCCESS] Scorecard submitted via {endpoint}")
                print(f"Response: {response.text[:200]}")
                return True
            else:
                print(f"[FAIL] {response.status_code}: {response.text[:200]}")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] {endpoint}: {str(e)[:100]}")
            continue

    return False

if __name__ == "__main__":
    print("[INFO] Attempting to submit Laiba's scorecard via Markaz API...")
    success = submit_via_api()
    if not success:
        print("[ERROR] Could not reach Markaz API via standard endpoints.")
        print("[INFO] Markaz may require authentication or use a different API pattern.")
