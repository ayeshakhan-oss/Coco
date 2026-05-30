"""
FINAL: Submit Arif Ali's values interview scorecard with proper evidence
Application ID: 3046
Email: alyaref555@gmail.com
Position: Senior Product Manager (Job ID 20)
Date: 2026-05-19
Duration: 32 minutes
Recording: https://fathom.video/share/vaxsNwjAh7ww1KDGE4xUPqHFxt71JAYK

RATINGS:
- Don't Walk Away: +
- All for One and One for All: +/-
- Continuously Improve Our Craft: +
- Have Courageous Conversations: +/-
- Don't Hold On Too Tight: +
- Practice Joy: +/-

LOGIC CHECK:
Minuses: 0 ✓
Plus-Minuses: 3 (= OUT per skill rule: "any minus OR ≥3 plus-minuses")
Result: OUT
GWC Assessment: N/A (only for PASS candidates per skill SOP)
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
    "noteTaker": "Coco",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "Arif demonstrated persistence when handling production crises and complex project rescues. When his tourism-based company released a product with critical NDP data and UI/UX issues, he didn't abandon the project despite severity. He worked through resolving production-level issues affecting both existing and new users, staying engaged until resolution. He also volunteered for a high-risk task: RedConnect integration migration. When facing a $12,000-30,000/month cost burden from a third-party platform, multiple product managers indicated it was 'difficult' with 'lot of issues.' Arif stepped up to own the integration rather than avoid the challenge.",
            "curveBall": "His examples show practical persistence—staying with a problem until resolved—but he frames difficulty more in operational terms (shipping, fixing bugs, managing costs) rather than discussing emotional or interpersonal challenges. The persistence is present but lacks deep reflection on why hard things matter or what he learned about himself.",
            "microCase": "Recently released project: 'I had to drop it. Because we had to release... production level issues and UI and UX issues.' RedConnect: 'Everyone told that this a difficult job... So I have to it.'"
        },
        {
            "name": "All for One and One for All",
            "rating": "+/-",
            "deepDive": "Arif shows team-oriented moments but frames them transactionally rather than with deep mutual investment. When NYC launch crashed due to a senior developer's untested PR, he 'covered it'—stepped in to fix the problem. This is positive but suggests individual heroes solving team problems rather than team members supporting each other proactively. When asked about valued peers, he deflects to 'the whole team' rather than naming specific relationships. He emphasizes one-on-ones as the best way to surface quiet voices—good instinct—but lacks depth. Manages ~40 employees, values giving credit to team, but substance feels process-heavy rather than emotionally connected.",
            "curveBall": "His language around teamwork is process-heavy ('the task is given as a team') but light on emotional resonance or celebration. He talks about team values without demonstrating warmth or genuine investment. The NYC example shows he can problem-solve with others, but not that he actively invests in building team confidence or celebrating wins together.",
            "microCase": "NYC launch: 'A senior developer... was a very basic mistake. Without testing, was a PR merchant in production... production crashed on the launch of the day. So at that time, I covered it.' On peer: 'As a product manager... If direct a team, that would direct a full credit to my [team].'"
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Arif shows genuine appetite for learning new technologies and methodologies. He proactively mentioned learning cloud AI—a cutting-edge technology—and is pursuing certification. He's applying these tools to company development processes and learning 'deep testing' from the QA team. He doesn't learn in isolation; he integrates new knowledge into workflow and teaches others. Willingness to adopt cloud-based automation and AI tools shows he's staying current with industry trends and translating them into practical application. Not passive learning; active upskilling tied to real work.",
            "curveBall": "His learning is genuine but somewhat surface-level. He articulates what he's learning (cloud AI, testing practices) but not deeply why these matter or what specific insights he's gained. Learning appears competent but not reflective—more 'I'm taking a certification' than 'I realized X and now approach Y differently.'",
            "microCase": "'Now, the new thing is cloud AI... are learning AI... are learning about cloud... we use cloud AI tools... I have lot of stuff in cloud. The same thing about our QA team. I have learned that deep team.'"
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Arif participated in high-stakes organizational conversations. During company layoffs, he had meetings with the CEO about firing decisions, then called affected employees to inform them. He explained the business rationale: tourism company, Canada/US operations, needed consolidation. He also received difficult feedback about his process/timing that initially seemed wrong but after reflection, he realized it was valid and adjusted his approach. Shows willingness to participate in difficult business conversations and receptiveness to feedback.",
            "curveBall": "These examples are significant in organizational weight but operational in execution. He can participate in difficult business conversations (layoffs with CEO, policy discussions) and receive feedback gracefully, but responses remained transactional: 'I had to call them and informed them.' He didn't describe how he handled the emotional dimension—employees' shock, grief, pushback. He didn't articulate how he managed his own emotions or used empathy to make the conversation less painful. For Senior PM role where difficult peer conversations (performance feedback, strategy disagreement, accountability) are frequent, his examples lean to 'business conversations' rather than 'people conversations.'",
            "microCase": "Layoffs: 'I called them and started [informing them]... we have our layouts to start... we are able to get from the online industry that we need to have replace together.' Feedback: 'As a product manager... I would say that this should time. So then I realized... I have changed own process.'"
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "Arif demonstrates genuine flexibility and willingness to adopt better approaches from others. At Microsoft, a junior female colleague had superior testing methodology he initially didn't recognize. Rather than defend his approach, he learned from her, adopted her process (mutations, automation, data-based testing), and now recommends it. In current role, he creates roadmaps but hands projects to junior team members for better impact and their development. Shows comfort letting go of ownership when it serves goals better.",
            "curveBall": "His examples are clear and concrete, showing he's not defensive about ideas. However, they're relatively straightforward scenarios (adopting better process, delegating to juniors). The value comes through, but there's no evidence of the emotional maturity of letting go—no examples of releasing a cherished idea, admitting he was wrong about direction, or pivoting strategy based on market feedback. 'Don't Hold On Too Tight' is demonstrated as process flexibility rather than ego flexibility.",
            "microCase": "Microsoft: 'A female staff, colleague... was very impressed with the process... changed the [approach]... I was able to [adopt] script... mutations.' Current role: 'We have three products... then I hand over to [junior PM]... That's right.'"
        },
        {
            "name": "Practice Joy",
            "rating": "+/-",
            "deepDive": "Arif self-describes as a 'smiling emoji'—reasoning: 'Because I think that I'm going [to smile whether I] meet deadlines or miss.' Shows fundamentally positive attitude about work and life. He actively invests in team joy through outings: F9 bowling, Megazone, lunch activities. He realizes that 'having good time together is important—most important part of the team.' He's intentional about creating low-cost but high-impact bonding experiences.",
            "curveBall": "While team engagement activities show thoughtfulness, his personal joy definition is thin. The 'smiling emoji' answer—being happy whether he succeeds or fails—is more stoic acceptance than genuine joy. It's not clear what genuinely brings Arif joy beyond team activities. He doesn't mention hobbies mentioned at session start (hiking, adventures, cricket, football) as sources of sustained joy or energy. Joy practice concentrated in work-related team bonding rather than demonstrating how personal joy fuels work. For a leader, that's a gap: Does he have outlets, practices, or sources of joy that keep him energized and model healthy life balance for team?",
            "microCase": "Self-description: 'Smile. Why? Because I think that I'm going [to be happy whether I] meet deadlines or miss... That's good.' Team joy: 'The best thing is go outing... F9 is the Megazone... have to go bowling and lunch... I realized that I had a lot of time team... that's the most important part the team.'"
        }
    ],
    "finalComments": "OUT — Three plus-minuses (All for One, Courageous Conversations, Practice Joy) with zero minuses. Per pass/out logic: ≥3 plus-minuses = OUT. Arif demonstrates strong operational persistence, learning orientation, and process flexibility. Growth areas—emotional depth in interpersonal conversations, personal joy sources, and team investment—require development before Right Seat Assessment.",
    "proceedToRightSeat": False
}

def main():
    print("[SCORECARD READY FOR SUBMISSION]")
    print(f"Candidate: Arif Ali (App 3046)")
    print(f"Email: alyaref555@gmail.com")
    print(f"Position: Senior Product Manager")
    print(f"Date: 2026-05-19")
    print()
    print("RATINGS:")
    for value in SCORECARD["values"]:
        print(f"  {value['name']}: {value['rating']}")
    print()
    print("LOGIC CHECK:")
    ratings = [v['rating'] for v in SCORECARD["values"]]
    minuses = ratings.count('-')
    plus_minuses = ratings.count('+/-')
    print(f"  Minuses: {minuses}")
    print(f"  Plus-Minuses: {plus_minuses}")
    print(f"  Result: {'OUT' if minuses > 0 or plus_minuses >= 3 else 'PASS'}")
    print()
    print("READY: Ask Ayesha: 'Should I go and submit this on Markaz or not?'")
    print()
    print("[DO NOT SUBMIT WITHOUT APPROVAL]")

if __name__ == "__main__":
    main()
