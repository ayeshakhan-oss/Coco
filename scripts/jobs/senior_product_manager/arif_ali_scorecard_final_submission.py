"""
FINAL SCORECARD: Arif Ali (Senior Product Manager)
Application ID: 3046
Email: alyaref555@gmail.com
Date: 2026-05-19
Duration: 32 minutes
Recording: https://fathom.video/share/vaxsNwjAh7ww1KDGE4xUPqHFxt71JAYK

EVIDENCE SOURCED FROM: Expanded transcript analysis (detailed)
RATINGS: 3 Plus + 3 Plus-Minus + 0 Minus
LOGIC: ≥3 plus-minuses = OUT
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
            "deepDive": "Arif demonstrated genuine persistence when facing operational crises. His tourism platform (Canada/US operations, Pakistan-based engineering) released a product with critical NDP data and UI/UX issues affecting both existing and new users. Rather than revert or escalate without resolution, he engaged directly: 'I had to drop it...production level issues and UI/UX issues.' He worked through infrastructure-level fixes rather than abandoning the release. Additionally, when facing a $12,000-30,000/month cost burden from RedConnect (third-party tour platform), every other product manager declined the integration migration due to 'difficult job' and 'lot of issues.' Arif stepped forward to own it: 'Everyone told that this a difficult job...So I have to it, and I have to it.' He volunteered for high-risk consolidation despite team signals to avoid it. The scope was substantial: their entire booking workflow was built on RedConnect's API. A failed migration could lose $12K-30K/month in revenue. He didn't shy away; he committed to the problem.",
            "curveBall": "Arif's examples demonstrate operational persistence—staying with technical or logistical problems until resolved—but lack emotional or interpersonal depth. He describes what happened and that he stayed, but not why these problems mattered or what he learned about himself. Language is transactional: 'I had to drop it,' 'I have to it'—suggesting obligation or process rather than purposeful engagement. For a Group PM, persistence often manifests in team conflict navigation, standing firm on principle when unpopular, or wrestling with ambiguity in strategy. Arif's examples are more operational (bug fixes, technical migrations) than interpersonal or strategic.",
            "microCase": "Production Crisis: 'Recently, we released project...I had to drop it. Because we had to the release, we had to the level issues. So, I had to release of NDP data...We to drop it on the production level issues and UI/UX issues. So, I able do the which is our existing users, or new users.' RedConnect: 'Recently, we work with RedConnect...my company is tourism-based...everyone told that this a difficult job...So I have to it, and I have to it.'"
        },
        {
            "name": "All for One and One for All",
            "rating": "+/-",
            "deepDive": "Arif shows situational teamwork but not pervasive mutual investment. During NYC launch, a senior developer merged an untested PR to production, causing a catastrophic launch-day crash. Arif's response: 'I covered it'—he stepped in to help fix the problem. However, the framing suggests individual rescue ('I covered it') rather than team learning ('We diagnosed it together'). His intervention was necessary, but the narrative emphasizes hero rescue over shared growth. When asked about a valued peer, he deflects to 'the whole team' rather than naming an individual—while this sounds collaborative, real leaders celebrate *specific* individuals within team context. On surfacing concerns from quiet voices: 'One-on-one is the best solution for this kind of stuff'—correct framework but no concrete example of executing it or what he learned from a quiet team member. He manages ~40 employees and frames tasks as 'given as a team,' but execution is process-oriented without evidence of what this approach *produces* (stronger execution, better morale, innovation).",
            "curveBall": "Core issue: Arif shows procedural teamwork (one-on-ones exist, tasks framed as team efforts) but not emotional teamwork (celebrating wins together, lifting individuals, building trust through vulnerability). He has the right processes and language but not the emotional depth where team members feel genuinely valued and supported. Plus-minus because he's not anti-team or toxic, but not the kind of leader who creates deep psychological safety and mutual investment. For a Group PM, this is critical—you model and build team culture. If Arif's team doesn't feel celebrated or deeply connected, it affects morale, retention, and capacity to tackle hard problems together.",
            "microCase": "NYC Launch: 'When we launched in New York City...my developer is a senior developer...was a very basic mistake. Without testing, was a PR merchant in production. So production crashed on the launch of the day. So at that time, I covered it.' Team Credit: 'As a product manager...If direct a team, that would direct a full credit to my [team].' Surfacing Voices: 'One-on-one is the best solution for this kind of...stuff.'"
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Arif demonstrates active, applied learning—not theoretical study, but integrating new knowledge into work and teaching others. He proactively identified cloud AI as critical for his company's future. He's pursuing formal certification, applying cloud AI tools to actual development processes, learning infrastructure integration, and bidirectionally learning from the QA team: 'I have learned that deep team...I'm going to push.' He's not hoarding knowledge; he's identifying best practices and propagating them across the organization. In a distributed platform (Canada/US with Pakistan engineering), cloud infrastructure and AI-driven automation directly impact the product. His learning positions his team to handle modern technical challenges while showing intellectual humility—PM knowledge is insufficient; he actively seeks expertise from other functions (QA). This is learning coupled with action and knowledge-sharing.",
            "curveBall": "While commitment to learning is genuine, articulation of why and what specifically he discovered is surface-level. He tells us what he's learning (cloud AI, certification, testing practices) but not why it matters to the business or what specific insights he's gained. There's no reflection like: 'I realized cloud-native architecture would reduce our dependency on third-party integrations like RedConnect,' or 'Deep testing practices helped me understand the cost of production bugs.' Learning appears competent but not reflective—collecting skills without weaving them into coherent problem-solving strategy. For a Group PM, you need to translate craft improvements into product strategy: not just that cloud AI exists, but when and how to apply it to roadmap and team structure.",
            "microCase": "Cloud AI: 'Now, the new thing is cloud AI. We are learning AI...We are learning about cloud...we use cloud AI tools...I have lot of stuff in cloud.' QA Collaboration: 'The same thing about our QA team. I have learned that deep team. What the same thing I'm going to push.'"
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Arif participated in organizationally significant difficult conversations but executed them in operationally transactional ways. During company layoffs, his company had to reduce headcount (45 people in one week). Arif participated in: CEO meetings to determine affected employees and business rationale (tourism company, Canada/US operations, needed consolidation to survive); calling 45 affected employees to inform them of layoffs. This is courage in not avoiding difficulty, but his description lacks emotional intelligence or reflective handling of the human dimension. He describes mechanics: 'I called them and started [informing them]...we have our layouts to start...we are able to get from the online industry that we need to have replace together.' Missing: How did he prepare for the conversation? How did he handle pushback, shock, anger? What did he learn about communication from delivering devastating news? Did he follow up afterward to help transition? The conversation is treated as business process (inform people, explain rationale) not human conversation (hold space for shock/fear, build trust despite difficulty, demonstrate care). On receiving difficult feedback: 'As a product manager...I would say that this should time. So then I realized...I have changed own process.' Positive: receptive, not defensive, reflected and changed. Missing: How did he process feedback internally? Who gave it? How did the conversation go? What specifically changed? For a Group PM, you need to model how to receive difficult feedback in a way that builds trust—not just that you changed.",
            "curveBall": "Core issue: Arif can participate in difficult business conversations and receive feedback, but interview provides no evidence of difficult interpersonal conversations—common at Group PM level (performance feedback to underperforming PM, peer strategy disagreement, vulnerability about own mistakes, navigating unsupported/unheard situations). His examples are about business realities (layoffs, market changes) not people realities (trust, conflict, accountability, empathy). For Group PM managing other PMs, ability to have emotionally mature, transparent, reflective conversations with direct reports is critical. Arif's examples suggest he can execute operational aspects but may lack interpersonal depth. Framing layoffs as business necessity is correct, but truly courageous conversation also holds space for human impact. Reception of feedback is good, but truly courageous leader would proactively initiate difficult conversations—not just respond to them.",
            "microCase": "Layoffs: 'I would to give an example from AI, we have a layoffs in this company...I called them and started the that we have our layouts to start...we are able to get from the online industry that we need to have replace together.' Feedback: 'As a product manager...I would say that this should time. So then I realized that YP has able to do it. So I have changed own process.'"
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "Arif demonstrates genuine flexibility and egolessness in problem-solving and delegation. At Microsoft, a junior female colleague had superior testing methodology (data-driven mutations, scriptable automation, reusable test foundations). Rather than assuming experience made his approach superior, he learned from her and adopted her methods: 'A female staff, colleague...I was very impressed with the process...I was able to script...I was able to mutations.' He recognized her approach as better and now recommends it—no defensive ego, genuine intellectual humility. In current role, he creates initial roadmaps but hands off ownership to junior PMs for execution and development: 'We have three products...then I hand over to which I make it...That's right.' He doesn't maintain control; he lets go explicitly so junior PMs can develop craft and gain experience. Importantly, he's comfortable with distributed ownership—not a bottleneck but enabling others to grow. At scale, a Group PM who can't delegate and develop others becomes an organizational ceiling.",
            "curveBall": "Examples clearly demonstrate process flexibility and delegation but lack strategic flexibility—ability to pivot cherished strategy when market conditions change. Examples are about adopting better techniques (testing method from colleague) and delegating execution (junior PM's roadmap), not about holding strategic direction strongly then admitting it was wrong when evidence contradicts it. For a Group PM, 'Don't Hold On Too Tight' also means: admitting product hypothesis was wrong, pivoting entire roadmap based on market feedback, changing mind about hire or team structure, letting go of non-working product line. Delegation and technical flexibility are solid, but strategic letting-go isn't demonstrated.",
            "microCase": "Microsoft: 'When I worked for Microsoft...a female staff, colleague...I was very impressed with the process...I was able to script...I was able to [adopt] to the data based...I was able to mutations.' Current: 'We have three products...then the road map, the initial thing, I always make it. And then the product or projects, then I hand over to which I make it. That's right.'"
        },
        {
            "name": "Practice Joy",
            "rating": "+/-",
            "deepDive": "Arif shows fundamental optimism and intentional team bonding but lacks clear sense of personal joy and life balance. When asked what emoji describes him, he chose 'smiling emoji' with reasoning: 'Because I think that I'm going [to smile whether I] meet deadlines or miss...That's good.' This reveals stoic positivity—maintains good attitude regardless of outcomes. Not nothing (emotional stability) but not the same as joy. More 'I don't get upset' than 'This brings me delight.' For leadership, there's a difference between stability and being energizing. On team joy: he actively invests through structured, low-cost outings (F9 bowling, Megazone, lunch activities). He realized 'having good time together is important—most important part of the team.' Not going through motions; intentionally creating moments for team connection outside work pressure. Importantly, emphasizes no financial cost to individuals: creating joy without requiring team member spending. Shows consideration. Earlier in interview, when asked about leisure, he mentioned: hiking, adventures, cricket, football—'very passionate about the mountains and hiking'—genuine personal interests.",
            "curveBall": "Gap: Arif hasn't articulated what personally brings him joy or sustains him emotionally. Earlier mentioned hobbies (hiking, mountains, cricket, football) but never connected them to work life or how they fuel leadership. Why this matters for Group PM: Do you have outlets keeping you energized to show up fully for team? Do you model healthy life balance or work 70 hours expecting sustainable team pace? Are you drawing from genuine joy or burning out while maintaining smile? Can you bring authentic energy to team or performing positivity? Team bonding activities are good but they're group joy, not personal joy. Interview doesn't reveal what fills his cup personally—what makes him come alive. Risk flag for leadership: leaders without personal joy sources often burn out or create teams that mirror depletion. Stoic optimism ('I'll be happy whether I succeed or fail') sounds resilient but could mask lack of genuine joy or connection to purpose.",
            "microCase": "Smiling Emoji: 'Smile. Why? Because I think that I'm going [to smile whether I] meet deadlines or miss...That's good.' Team Bonding: 'The best thing is go outing. Outing is sports. First of F9 is the Megazone. We have to go bowling and lunch...I realized that I had a lot of time team...that's the most important part the team.' Personal Interests: 'I from the past three years...in the hiking and adventures, which I love to very passionate about...And playing cricket, football, and all this stuff.'"
        }
    ],
    "finalComments": "OUT — Three plus-minuses (All for One and One for All, Have Courageous Conversations, Practice Joy) with zero minuses. Per pass/out logic: ≥3 plus-minuses triggers OUT. Arif demonstrates strong operational persistence, learning orientation, and process flexibility. Growth areas—emotional depth in interpersonal conversations, personal joy sources, deep team investment—require development before Right Seat Assessment.",
    "proceedToRightSeat": False
}

def main():
    print("[FINAL SCORECARD — READY FOR SUBMISSION APPROVAL]")
    print()
    print(f"Candidate: Arif Ali (App 3046)")
    print(f"Email: alyaref555@gmail.com")
    print(f"Position: Senior Product Manager (Job ID 20)")
    print(f"Date: 2026-05-19 | Duration: 32 min | Recording: Fathom link")
    print()
    print("=" * 70)
    print("RATINGS & LOGIC CHECK")
    print("=" * 70)
    for value in SCORECARD["values"]:
        print(f"{value['name']:<45} {value['rating']:>5}")
    print()

    ratings = [v['rating'] for v in SCORECARD["values"]]
    minuses = ratings.count('-')
    plus_minuses = ratings.count('+/-')
    pluses = ratings.count('+')

    print(f"Pluses:        {pluses} (Don't Walk Away, Continuously Improve, Don't Hold On Too Tight)")
    print(f"Plus-Minuses:  {plus_minuses} (All for One, Courageous Conversations, Practice Joy)")
    print(f"Minuses:       {minuses}")
    print()
    print(f"Pass Logic:    zero minuses + ≤2 plus-minuses = PASS")
    print(f"Out Logic:     any minus OR ≥3 plus-minuses = OUT")
    print()
    if minuses > 0 or plus_minuses >= 3:
        print(f"RESULT:        OUT (≥3 plus-minuses)")
    else:
        print(f"RESULT:        PASS")
    print()
    print(f"GWC Assessment: N/A (only for PASS candidates)")
    print(f"Proceed to Right Seat: {SCORECARD['proceedToRightSeat']}")
    print()
    print("=" * 70)
    print("READY: Ask Ayesha: 'Should I go and submit this on Markaz or not?'")
    print("=" * 70)

if __name__ == "__main__":
    main()
