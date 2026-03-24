import psycopg2
import json
from datetime import datetime

conn = psycopg2.connect(
    host="ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech",
    dbname="neondb",
    user="neondb_owner",
    password="npg_kBQ10OASHEmd",
    sslmode="require"
)
cur = conn.cursor()

# ── AMINA BATOOL ── App ID 1857
amina_scorecard = {
    "date": "Mar 16, 2026",
    "host": "Ayesha Khan",
    "noteTaker": "",
    "candidateName": "Amina Batool",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+",
            "deepDive": "TFP 2-year commitment (post-Bachelor's, first real job) — 3-hour daily commute each way via local transport through broken roads; physically, mentally, and emotionally draining. Carried the weight of students' struggles and systemic inequity daily — moments of deep doubt ('Will I ever fix this? Am I even making a difference?'). Stayed because of students' daily joy and fellow teachers' 20-30 year resilience. The Suzuki-ditch moment (stranded en route at 9am with teachers who've done this for decades) was a turning point — drew deep strength from their commitment. Strong narrative of showing up every single day despite all three types of challenge.",
            "curveBall": "Volunteered for ethical standards documentation that no stakeholder was taking ownership of — proactively spotted the gap ('later it will create issues for the whole team'), took initiative regardless of whose plate it landed on. Also took sustained ownership of group project quality through university and work: sat with disengaged peers to understand why they'd checked out, motivated them through understanding rather than pressure, ensured the final product reflected everyone's best rather than separating her work from theirs.",
            "microCase": ""
        },
        {
            "name": "All for One & One for All",
            "rating": "+",
            "deepDive": "Covered for teammate's mistake in PFLH Sindh TLM mapping report without blame or 'I told you so.' Errors she had flagged earlier resurfaced via external feedback — rather than highlighting it, quietly helped fix them. Philosophy: 'We all want grace and kindness when we make mistakes.' Chose collective ownership over self-protection repeatedly.",
            "curveBall": "ETech Hub project with foreign team members (Sam Wilson, Alberto Soriano) + Pakistani field team. Proactively built psychological safety — greeted everyone fully by name, made eye contact, acknowledged their time and presence. Field team members shared concerns in her DMs before they felt safe in the group. Elevated intern's ideas publicly in group meetings to build confidence. 'I take personal responsibility for ensuring people can bring their full selves to work.'",
            "microCase": ""
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+/-",
            "deepDive": "Book: Sylvia Plath's 'The Bell Jar' — bleak novel about life choices and depression that she pushed through and finished. Walked away with renewed passion and her core philosophy: 'Not all those who wander are lost.' Applies wandering mindset to work (starts spreadsheets before contracts arrive, works beyond scope out of curiosity) and life (solo group travel to Skardu with strangers). Doing a master's alongside full-time work. Strong curiosity and growth orientation — however, no specific craft improvement system or deliberate daily habit described; the answer was philosophical (life perspective) rather than operational (skills development routine).",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+",
            "deepDive": "Raised team underpayment concern with line manager — a hard upward conversation because she was junior and had full visibility of budget constraints. Debated internally whether to bring it up, then decided: 'Even if nothing changes, the conversation itself matters.' Manager agreed completely and shared the same concern. Outcome: identified budget that could be redirected → significant end-of-project bonuses for all team members. Demonstrates upward feedback that created real, material change for the whole team.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+",
            "deepDive": "PFLH Sindh TLM mapping project: Built the entire foundation of 2 reports solo while teammates were on leave — work she'd poured herself into. At presentation stage, voluntarily split the government presentation with a teammate who had deep prior ownership of one report — chose not to 'hog screen time,' gave the section she was less suited for to the right person. Let go of recognition for the greater outcome. Also flagged: willing to let ideas be taken in new directions and not cling to original plan.",
            "curveBall": "",
            "microCase": ""
        },
        {
            "name": "Practice Joy",
            "rating": "+",
            "deepDive": "Emoji: thinking/curious 🤔. 'There is just no point of anything in life if there's no joy in it.' Described joy as curiosity — working beyond contract scope because she's genuinely excited, starting project spreadsheets before the contract arrives, solo group travel to Skardu with strangers she's never met. Favourite quote: 'Not all those who wander are lost.' Spontaneous, warm, and reflective — joy and exploration are deeply intertwined for her.",
            "curveBall": "",
            "microCase": ""
        }
    ],
    "finalComments": "Amina demonstrated genuine and consistent alignment across all 6 values. Standout moments: TFP resilience story (V1), proactive ethical document ownership (V1 curveball), surfacing quiet voices at ETech Hub (V2), and the team pay conversation with real outcome (V4). Slight gap in V3 — articulated a life philosophy rather than a concrete craft improvement system. Overall: strong cultural fit, authentic, self-aware, high-energy. PASS.",
    "proceedToRightSeat": "Yes"
}

# ── MUHAMMAD OMER KHAN ── App ID 1789
omer_scorecard = {
    "date": "Mar 17, 2026",
    "host": "Ayat Butt",
    "noteTaker": "",
    "candidateName": "Muhammad Omer Khan",
    "values": [
        {
            "name": "Don't Walk Away from Hard Things",
            "rating": "+/-",
            "deepDive": "UNICEF child labour study in Punjab — took over full project management when manager left for a family emergency. Navigated high-risk areas in DG Khan, communicated access constraints proactively to donor, adapted stratified sampling plan. Concrete and specific. However, the follow-up question ('most boring/repetitive task you kept doing') was answered with TADA clearances for field team — extremely thin, administrative paperwork rather than a genuine demonstration of persisting through hard things.",
            "curveBall": "Airport laptop theft scenario: 'Don't panic, check WhatsApp/Zoom/email/mobile for backup, redo presentation, report theft to relevant people.' Procedural checklist with no personality, no creative problem-solving, no sense of urgency or personal resourcefulness. Generic response applicable to anyone.",
            "microCase": ""
        },
        {
            "name": "All for One & One for All",
            "rating": "-",
            "deepDive": "Shared enumerators with colleague Aruba during Punjab data collection when her North Punjab targets were falling behind — sent his male and female enumerators to her districts (Faisalabad, Jhang, Bhakkar). Concrete and specific example of team support.",
            "curveBall": "When asked 'Have you ever put aside personal ambitions or desires for the greater good of the team?' — answered: 'I think it would be a no.' Could not recall a single instance of personal sacrifice for the collective. This is a direct and unambiguous miss on the core spirit of this value.",
            "microCase": "Shared bonus pool distribution scenario: 'Establish clear criteria, reward contribution and impact, maintain fairness and transparency, recognise team collaboration.' Pure buzzword response — no actual method, no numbers, no decision-making framework, no engagement with the tension of unequal contributions."
        },
        {
            "name": "Continuously Improve Our Craft",
            "rating": "+",
            "deepDive": "Entered three successive new domains without prior knowledge: infection prevention and control (Global Fund / Indus Hospital, ~2 years as M&E officer), sexual reproductive health (Embassy of Netherlands, 9 months), now post-abortion care. Measures success by trajectory — 'I started knowing nothing and I can see myself improving.' Concrete shift from paper-based data collection to digital tools (KoboToolbox, Google Forms, Survey CTO) when paper became obsolete.",
            "curveBall": "Structured 5-day crash course outline: Day 1 background/foundations → Day 2 tools and methods → Day 3 case studies and examples → Day 4 role play and feedback → Day 5 assessment and reflection (pre/post test, group work). Organised and logical.",
            "microCase": ""
        },
        {
            "name": "Have Courageous Conversations",
            "rating": "+/-",
            "deepDive": "Confronted a female enumerator directly about data quality issues (skipped sections, logical errors) during Punjab data collection. Told her clearly: corrective measures required, otherwise he would reassign her team or escalate to APSCO. Specific, direct, and outcome-focused.",
            "curveBall": "When asked for an unpopular opinion about a past workplace — answered: 'Mere jan mein toh aisa kuchh nahi aa raha, sab kuchh communicated hota hai.' (Nothing comes to mind, everything gets communicated.) A clear dodge — either lacks critical observation or avoids uncomfortable honesty in this context.",
            "microCase": "Confronting a colleague delivering low-quality work: 'Tell them about their JDs and deliverables, try to motivate them, offer to help together, otherwise escalate to senior management.' Procedural and quick to escalate. No curiosity about root cause, no emotional intelligence or empathy shown."
        },
        {
            "name": "Don't Hold On Too Tight",
            "rating": "+/-",
            "deepDive": "Let go of the Global Fund IPC project (15 districts, Indus Hospital) — but the reason was entirely external: donor pulled funding. Did not demonstrate personal adaptability or a conscious internal choice to let go. The letting go was imposed on him.",
            "curveBall": "Celebrated being wrong: Sehat Sahulat card evaluation in KPK — 'I did not anticipate the change... we were not able to get our targets, we still celebrated the win.' Extremely vague — no specifics on what he was wrong about, what he had expected, why he was happy to be wrong, or what he learned from it.",
            "microCase": "Investor pivot scenario: 'Listen carefully, evaluate impact on operations/cost/timelines/goals, consult team, make evidence-based decision, communicate to investor.' Completely textbook — could be read verbatim from a management textbook. No personal insight, no engagement with the difficulty of the situation."
        },
        {
            "name": "Practice Joy",
            "rating": "-",
            "deepDive": "Lifting team morale during 40-day field assignments: took team to a restaurant to eat, talk about challenges, do bonding exercises and review meetings. Generic — applicable to any team anywhere, no personal creativity or signature.",
            "curveBall": "When asked what fun or quirky ritual he would introduce in his first month: 'Maybe more research-based and evidence-based decisions.' Completely missed the spirit of the question — proposed a work methodology, not a joyful ritual. Shows either a fundamental disconnect with the value of joy or a failure to engage with what was being asked.",
            "microCase": "Meme caption for a failed project launch: Struggled significantly, asked for extended time, landed on 'Education is really important. Please don't fail your exams.' Flat, disconnected from the scenario, not funny, no creativity or playfulness."
        }
    ],
    "finalComments": "Omer demonstrated inconsistent values alignment throughout the interview. Strongest in V3 (genuine domain-hopping and craft development). Clear misses: V2 — explicitly said he has never sacrificed personal ambitions for the team ('I think it would be a no'); V6 — proposed evidence-based decisions as a fun ritual and gave a flat meme. Responses across the interview were predominantly generic and procedural, describing frameworks rather than lived experiences. Generic response pattern was a consistent concern. OUT: 2 minuses (V2, V6) + 3 plus/minus. User decision confirmed.",
    "proceedToRightSeat": "No"
}

# ── UPDATE Amina ──
cur.execute("""
    UPDATE applications SET
        values_scorecard = %s,
        values_interview_result = %s,
        values_interview_date = %s,
        values_interviewer_name = %s
    WHERE id = %s
""", (
    json.dumps(amina_scorecard),
    "pass",
    datetime(2026, 3, 16),
    "Ayesha Khan",
    1857
))
print(f"Amina Batool (App 1857): {cur.rowcount} row(s) updated")

# ── UPDATE Omer ──
cur.execute("""
    UPDATE applications SET
        values_scorecard = %s,
        values_interview_result = %s,
        values_interview_date = %s,
        values_interviewer_name = %s
    WHERE id = %s
""", (
    json.dumps(omer_scorecard),
    "fail",
    datetime(2026, 3, 17),
    "Ayat Butt",
    1789
))
print(f"Muhammad Omer Khan (App 1789): {cur.rowcount} row(s) updated")

conn.commit()
cur.close()
conn.close()
print("Done. Both scorecards submitted to Markaz.")
