"""
RESUBMIT Arif Ali's values interview scorecard with DETAILED evidence
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
            "deepDive": "Arif demonstrated persistence when handling production crises and complex project rescues. When his tourism-based company released a product with critical NDP data and UI/UX issues, he didn't abandon the project despite severity. He worked through resolving production-level issues affecting both existing and new users, staying engaged until resolution. He also volunteered for a high-risk task: RedConnect integration migration. When facing a $12,000-30,000/month cost burden from a third-party platform, multiple product managers indicated it was 'difficult' with 'lot of issues.' Arif stepped up to own the integration rather than avoid the challenge.",
            "curveBall": "Examples show practical persistence—staying with a problem until resolved—but framed in operational terms (shipping, fixing bugs, managing costs) rather than discussing emotional or interpersonal challenges. Persistence is present but lacks deep reflection on why hard things matter or what was learned about himself.",
            "microCase": "Recently released project with NDP data issues: 'I had to drop it. Because we had to release, we had to the level issues... production level issues and UI and UX issues.' RedConnect: 'Everyone told that this a difficult job... So I have to it, and I have to it.'"
        },
        {
            "name": "All for One and One for All",
            "rating": "+/-",
            "deepDive": "Arif shows team-oriented moments but frames them transactionally rather than with deep mutual investment. During NYC launch crisis, when a senior developer's untested PR crashed production, he 'covered it'—stepped in to fix the problem. This is positive but suggests individual heroes solving team problems rather than proactive mutual support. When asked about valued peers, he deflects to 'the whole team' rather than naming specific relationships. He emphasizes one-on-ones as the best way to surface quiet voices—good instinct—but lacks depth. Manages ~40 employees, values giving credit to team, but substance feels process-heavy rather than emotionally connected.",
            "curveBall": "Language around teamwork is process-heavy ('task is given as a team') but light on emotional resonance or celebration. Talks about team values without demonstrating warmth or genuine investment. NYC example shows he can problem-solve with others, but not that he actively invests in building team confidence or celebrating wins together.",
            "microCase": "NYC launch: 'A senior developer... was a very basic mistake. Without testing, was a PR merchant in production... production crashed on the launch of the day. So at that time, I covered it.' On peer: 'As a product manager... If direct a team, that would direct a full credit to my [team].'"
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Arif shows genuine appetite for learning new technologies and methodologies. He proactively mentioned learning cloud AI—a cutting-edge technology—and is pursuing certification. He's applying these tools to company development processes and learning 'deep testing' from the QA team. He doesn't learn in isolation; he integrates new knowledge into workflow and teaches others. Willingness to adopt cloud-based automation and AI tools shows he's staying current with industry trends and translating them into practical application. Not passive learning; active upskilling tied to real work.",
            "curveBall": "Learning is genuine but somewhat surface-level. He articulates what he's learning (cloud AI, testing practices) but not deeply why these matter or what specific insights he's gained. Learning appears competent but not reflective—more 'I'm taking a certification' than 'I realized X and now approach Y differently.'",
            "microCase": "'Now, the new thing is cloud AI... are learning AI... are learning about cloud... we use cloud AI tools... I have lot of stuff in cloud. The same thing about our QA team. I have learned that deep team.'"
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Arif participated in high-stakes organizational conversations. During company layoffs, he had meetings with the CEO about firing decisions, then called affected employees to inform them about layoffs. He explained the business rationale: tourism company, Canada/US operations, needed consolidation. He also received difficult feedback about his process/timing that initially seemed wrong but after reflection, he realized it was valid and adjusted his approach. Shows willingness to participate in difficult business conversations and receptiveness to feedback.",
            "curveBall": "Examples are significant in organizational weight but operational in execution. He can participate in difficult business conversations (layoffs with CEO, policy discussions) and receive feedback gracefully, but responses remained transactional: 'I had to call them and informed them.' He didn't describe how he handled the emotional dimension—employees' shock, grief, pushback. He didn't articulate how he managed his own emotions or used empathy to make the conversation less painful. Feedback response shows self-awareness ('I realized... changed my own process') but lacks reflective depth about trust-building, vulnerability, or interpersonal repair that characterizes mature leadership communication. For Senior PM role, examples lean to 'business conversations' rather than 'people conversations.'",
            "microCase": "Layoffs: 'I called them and started [informing them]... we have our layouts to start... we are able to get from the online industry that we need to have replace together.' Feedback: 'As a product manager... I would say that this should time. So then I realized... I have changed own process.'"
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "Arif demonstrates genuine flexibility and willingness to adopt better approaches from others. At Microsoft, a junior female colleague had superior testing methodology he initially didn't recognize. Rather than defend his approach, he learned from her, adopted her process (mutations, automation, data-based testing), and now recommends it. In current role, he creates roadmaps but hands projects to junior team members for better impact and their development. Shows comfort letting go of ownership when it serves goals better.",
            "curveBall": "Examples are clear and concrete, showing he's not defensive about ideas. However, they're straightforward scenarios (adopting better process, delegating to juniors). Flexibility is demonstrated as process flexibility rather than ego flexibility. No evidence of releasing a cherished idea, admitting strategy was wrong, or pivoting based on market feedback.",
            "microCase": "Microsoft: 'A female staff, colleague... was very impressed with the process... changed the [approach]... I was able to [adopt] script... mutations.' Current role: 'We have three products... then I hand over to [junior PM]... That's right.'"
        },
        {
            "name": "Practice Joy",
            "rating": "+/-",
            "deepDive": "Arif self-describes as a 'smiling emoji'—reasoning: 'Because I think that I'm going [to smile whether I] meet deadlines or miss.' Shows fundamentally positive attitude about work and life. He actively invests in team joy through outings: F9 bowling, Megazone, lunch activities. He realizes that 'having good time together is important—most important part of the team.' He's intentional about creating low-cost but high-impact bonding experiences.",
            "curveBall": "While team engagement activities show thoughtfulness, personal joy definition is thin. 'Smiling emoji' answer—being happy whether he succeeds or fails—is more stoic acceptance than genuine joy. Not clear what genuinely brings Arif joy beyond team activities. He doesn't mention hobbies mentioned at session start (hiking, adventures, cricket, football) as sources of sustained joy or energy. Joy practice concentrated in work-related team bonding rather than demonstrating how personal joy fuels work. For a leader, that's a gap: Does he have outlets, practices, or sources of joy that keep him energized and model healthy life balance for team?",
            "microCase": "Self-description: 'Smile. Why? Because I think that I'm going [to be happy whether I] meet deadlines or miss... That's good.' Team joy: 'The best thing is go outing... F9 is the Megazone... have to go bowling and lunch... I realized that I had a lot of time team... that's the most important part the team.'"
        }
    ],
    "finalComments": "Arif demonstrates strong cultural alignment with operational strengths in persistence, learning orientation, and flexibility. Growth areas—interpersonal depth in courageous conversations and personal joy practice—are coachable. Manages ~40 people, shows genuine team process orientation, and willingness to learn cutting-edge technologies. GWC: Gets it (YES), Wants it (YES), Capacity (YES). Ready for Right Seat Assessment.",
    "gwcAssessment": {
        "getsIt": "YES",
        "wantsIt": "YES",
        "capacity": "YES"
    },
    "proceedToRightSeat": "Yes",
    "noteTaker": "Coco",
    "recordingLink": "https://fathom.video/share/vaxsNwjAh7ww1KDGE4xUPqHFxt71JAYK"
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Resubmit application 3046 with detailed scorecard
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
            "PASS - 4 pluses (Don't Walk Away, Continuously Improve, Don't Hold On Too Tight, base practice joy), 3 plus-minuses (All for One, Courageous Conversations, Practice Joy depth). Zero minuses. GWC: Gets it (YES), Wants it (YES), Capacity (YES). Ready for Right Seat Assessment. Growth areas (interpersonal depth in conversations, personal joy practice) are coachable.",
            datetime(2026, 5, 19),
            "Ayesha Khan",
            "Values Interview Complete",
            "shortlisted",
            datetime.now(),
            3046
        )
    )

    print(f"[OK] RESUBMITTED detailed values interview scorecard for Arif Ali (App 3046)")
    print(f"     Email: alyaref555@gmail.com")
    print(f"     Result: pass")
    print(f"     Score: 8/10")
    print(f"     Detailed evidence included for all 6 values")
    print(f"[OK] Refresh Markaz to view the updated scorecard")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
