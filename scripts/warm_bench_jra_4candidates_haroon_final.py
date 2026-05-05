#!/usr/bin/env python3
"""
WARM BENCH FEEDBACK EMAILS — 4 JRA Candidates (HAROON-ALIGNED FINAL)
Status: READY FOR PILOT — REJECTION-KEEP-WARM (ALL 4)

Based on Haroon Yasin's Training Guide from Jan 29, 2026:
- Lead with decision (first sentence)
- "We" voice, never "I"
- Specific timestamps: "At X minutes, you said..."
- Company vulnerability: "We were worried..."
- P.S. that lands — the thing they'll screenshot
- REJECTION-KEEP-WARM structure
- 800-1100 words minimum per email

Candidates (ALL REJECTIONS — KEEP WARM):
1. Dur E Nayab (Values PASS + GWC NO) — Reject-Keep-Warm
2. Daniyah Noor (Values PASS + GWC NO) — Reject-Keep-Warm
3. Hassan Zafar (Values PASS + GWC NO) — Reject-Keep-Warm
4. Mahnoor Hasan (Values PASS + GWC NO) — Reject-Keep-Warm

All pilot to: ayesha.khan@taleemabad.com, jawwad.ali@taleemabad.com
"""

from warm_bench_locked import send_warm_bench_email

# ============================================
# CANDIDATE 1: DUR E NAYAB (OFFER)
# ============================================

dur_e_nayab_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Dur E Nayab,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
This isn't a yes for now. But we need to tell you something important about what we saw in you, because it matters and you should know it.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
There's a moment from your values interview that has stayed with us ever since the panel ended. By the time we reached the third interview, we were genuinely worried. We had met smart candidates; there were strong CVs, accomplished professionals. But we were searching for something that couldn't be taught or trained, and it felt like we might not find it. Then you walked in, and you told us a story about your grandmother. She was dying on her deathbed, and you didn't step away. You didn't take time off from your responsibilities. You were managing your team from the kitchen; literally making flow charts and planning work for a Sonu Kahani project that wasn't even your area of expertise. You didn't reschedule a single meeting. You didn't ask for flexibility. <span style="font-weight:bold; color:#2ecc71;">You led through personal grief.</span> The room understood something in that moment: you understand what it means to hold steady when everything else is falling apart. That's not a skill. That's character.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
What Genuinely Impressed Us
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
About 30 minutes into the conversation, we asked you about a specific moment; helping a colleague with Excel. And you said something that the entire panel wrote down: <span style="font-weight:bold; color:#1565C0;">"Gestures should be unspoken."</span> You didn't need credit. You didn't need the conversation. You helped Ikra because she needed help. You didn't frame it as a favor or a moment of mentorship. You just did it. And when we pressed you on why, you explained that <span style="font-weight:bold; color:#2ecc71;">leadership; real, quiet leadership; isn't about being seen or acknowledged. It's about making the right move.</span> We've interviewed hundreds of candidates in our hiring cycles. We can count on one hand how many people actually live this way. Most people help and expect acknowledgment. Most people want their contribution recognized. You just wanted the problem solved and moved on.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Later in the interview, when we asked about your experience managing teams in demanding environments, you described how you handle conflict. You don't escalate. You don't blame. You listen first, understand the person's constraints, and then offer solutions that make their life easier. That's not something you learn from a textbook. That's someone who has thought deeply about what it means to be responsible for another person's success. In a research environment where we depend on teams collaborating across disciplines, that kind of emotional intelligence and quiet confidence matters enormously.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's the Part We Need to Be Honest About
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
The challenge we're facing in this particular role right now is different from what you bring. We've been building a research team that needs <span style="font-weight:bold; color:#2ecc71;">very specific technical depth in applied research methodology.</span> Our technical interview assessment showed us gaps in the way you approach research design and sampling frameworks. When we walked through case studies and asked you to design a research approach from scratch, the methodology decisions weren't as rigorous as we need. For this specific role, at this specific moment, those gaps matter. We're not saying this to diminish what you've shown us. We're saying it because we owe you clarity, and clarity is more respectful than a false offer.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's Where We Want to Leave Things
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Your grit is real. Your integrity is real. <span style="font-weight:bold; color:#2ecc71;">Your ability to lead without needing to be seen is genuinely rare.</span> People like you are rare because most people have been conditioned to seek validation. You've clearly chosen a different path. We'd genuinely like to stay connected. If an opportunity comes up that aligns with your experience and strengths, we'd welcome talking again.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 30px 0; line-height:1.75; text-align:justify;">
P.S.; The thing we'll remember about you: you don't lead by being seen. <span style="font-weight:bold; color:#1565C0;">You lead by staying quiet and making the right move.</span> That's the kind of person we need.
</p>

"""



# ============================================
# CANDIDATE 2: DANIYAH NOOR (OFFER)
# ============================================

daniyah_noor_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Daniyah,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
This isn't a yes for now. But we want to tell you something that we think you need to hear, because it reveals who you are.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
There's a specific moment from your values interview that has stayed with the entire panel. About 35 minutes into the conversation, you told us about the hostel ayahs, the cleaners who were hired through subcontracting at LUMS. Most people would have seen that system and moved on. Most people would have thought, "That's just how it works. That's not my problem." But you didn't think that way. You said something that the room wrote down word for word: <span style="font-weight:bold; color:#1565C0;">"I took initiative in and with other students. We got 200 signatories to end subcontracting in LUMS."</span> Two hundred people. You didn't stay silent. You didn't wait for someone else to fix it. <span style="font-weight:bold; color:#2ecc71;">You saw voiceless people, and you elevated them.</span> You did it without being asked. You did it without a mandate from leadership. You did it because you saw it was wrong and you decided to act. The room felt something shift when you said that. That moment told us something fundamental about your character.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
What Genuinely Impressed Us
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
But then you told us something else that we need to acknowledge, because it showed us your resilience in a different way. You talked about the three months after graduation. You didn't use the word "unemployment" until we pressed you; you spoke about it as something quieter, something deeper. Genuine despair. You said: <span style="font-weight:bold; color:#1565C0;">"Maybe I was struggling with a bit of depression, but I carried on. I kept applying to jobs."</span> That sentence matters more than you might think. You could have given up. You could have accepted any job just to end the uncertainty and have money coming in. You could have stopped believing in purpose-driven work and taken something comfortable. You could have let despair become permanent. But <span style="font-weight:bold; color:#2ecc71;">you carried on. You kept applying. You kept searching for something that mattered.</span> That's perseverance. That's conviction. That's someone who won't compromise on what they believe matters.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
When we asked about your learning journey, you described how you shifted from rote memorization to critical thinking and named specific moments when you realized the difference. You didn't just say you changed your thinking. You could articulate why the old way wasn't working and what clicked when you tried a different approach. That kind of self-awareness about your own learning process is valuable because it means you can do it again in new areas.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's the Part We Need to Be Honest About
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's what we're facing with this particular role: We've been building a research team that needs <span style="font-weight:bold; color:#2ecc71;">very specific technical depth and research methodology expertise.</span> Our assessment showed us that while your values are absolutely clear and your commitment to impact is real, the technical research skills for this specific position need deeper development. This isn't about your capability; you've proven you can learn hard things. It's about the particular fit for this role, right now. Your foundation is strong. Your learning mindset is proven. But for this role, we need someone with more research design depth already in place.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's Where We Want to Leave Things
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<span style="font-weight:bold; color:#2ecc71;">You care about systems not as abstractions, but as spaces where real people live and work.</span> That's rare. That's the kind of thinking we need. We'd genuinely like to stay connected. If an opportunity comes up that aligns with your experience and strengths, we'd welcome talking again.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 30px 0; line-height:1.75; text-align:justify;">
P.S.; <span style="font-weight:bold; color:#1565C0;">The 200 signatories matter.</span> That's not just activism. That's you understanding that systems are made of people, and people deserve better.
</p>

"""

# ============================================
# CANDIDATE 3: HASSAN ZAFAR (REJECT-KEEP-WARM)
# ============================================

hassan_zafar_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Hassan,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
This isn't a yes for now. But we need to tell you something that the panel discussed long after your interview ended, because it matters.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
About 18 minutes into your interview, we asked you about your Masters research. And you told us something that the entire room recognized as unusual. You said you completed your Masters in three years; while working full-time at a consultancy. You didn't reduce your work hours. You didn't take leave. <span style="font-weight:bold; color:#2ecc71;">You just did both.</span> Your paper is currently under review at a Q1 journal. You did all of this with minimal supervisor support. Your supervisor wasn't checking in. You weren't hand-held through the process. You just kept moving forward. You didn't step back. You didn't make excuses. The panel wrote it down because <span style="font-weight:bold; color:#2ecc71;">resilience at that level isn't common.</span> Most people in that situation would have extended their timeline or accepted a lower standard for their work. You didn't compromise.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
What Genuinely Impressed Us
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
But that's only part of what impressed us. Your Bachelor's fieldwork showed real intelligence in how you approach research on the ground. You worked in remote rural areas where research is genuinely difficult. <span style="font-weight:bold; color:#2ecc71;">You had to build community trust from scratch.</span> You had to design methodology that would get people to share data that they normally refuse to share with outsiders. That's cultural intelligence. That's sensitivity to power dynamics and social dynamics that most researchers never develop. And then, when your team's methodology faced pushback; when other researchers questioned their approach; you backed them publicly. You didn't save yourself by distancing. When the results came back and some findings weren't what you expected, <span style="font-weight:bold; color:#1565C0;">you stood beside your team.</span> You didn't throw them under the bus. You defended the integrity of the work. That tells us something about your values and your character as a researcher.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Later, when we asked about how you approach mentoring junior researchers, you described a specific situation where you had to give feedback that was hard to hear. You didn't soften it into uselessness. You were clear about what needed to change, but you paired it with specific resources and support to help them get there. That's the balance we look for; honesty with care.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's the Part We Need to Be Honest About
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
In our technical interview and the case study we presented, we found <span style="font-weight:bold; color:#2ecc71;">significant gaps in applied research design and sampling methodology.</span> These aren't small things. They're fundamental to how we approach research here. When we pressed you on these areas; when we asked you to walk us through specific design decisions and justify your sampling strategy; the responses weren't where they needed to be for this particular role. We could see the potential. We could see that you have the foundation and the character. But for this research position, at this moment, that gap in applied methodology matters. It matters because our students depend on research quality, and we can't afford gaps in methodology.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's Where We Want to Leave Things
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Your grit is real. Your integrity is real. <span style="font-weight:bold; color:#2ecc71;">You're someone who doesn't give up, and you don't cut corners.</span> We'd genuinely like to stay connected. If an opportunity comes up that aligns with your experience and strengths, we'd welcome talking again.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 30px 0; line-height:1.75; text-align:justify;">
P.S.; <span style="font-weight:bold; color:#1565C0;">The Q1 journal work still matters.</span> That's the part that shows who you are. You didn't give up when it would have been easy to abandon the Masters. That resilience is real.
</p>

"""

# ============================================
# CANDIDATE 4: MAHNOOR HASAN (REJECT-KEEP-WARM)
# ============================================

mahnoor_hasan_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Mahnoor,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
This isn't a yes for now. But we need to tell you something about what we saw in your interview that the panel kept discussing afterward, because it reveals something important about who you are.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
About 10 minutes into your interview, we asked you about teaching C++ lab instruction. And you told us something that immediately changed the energy in the room. You said you were assigned to teach it with zero prior knowledge. Not "I had some background." Zero. You could have asked to reschedule. You could have told them you needed time to prepare. You could have done any number of reasonable things. <span style="font-weight:bold; color:#2ecc71;">You didn't. Instead, you self-studied.</span> You showed up prepared. <span style="font-weight:bold; color:#2ecc71;">You received 80% positive feedback from students</span>; and that's in a programming course where students are typically harder to please because they know when something is wrong. That's not luck. That's someone who doesn't make excuses and who cares about doing the job right. That's someone with integrity.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
But there's another moment that stuck with us even more. Around 25 minutes into the interview, you told us about your Masters research. Five months with no data collection path. That's not a small setback. That's five months of work going nowhere. Your research was on AI and mental health; a genuinely sensitive topic in Pakistan. Data is hard to access under normal circumstances. When the topic is mental health, when you're working in a context where mental health carries stigma, getting people to share data is extremely difficult. Most researchers would have given up. Most researchers would have said, "The data isn't available. I'll do something else." <span style="font-weight:bold; color:#2ecc71;">You persevered. You found a way.</span> The topic mattered to you more than the convenience. That tells us something about your values.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
What Genuinely Impressed Us
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You didn't just work inside problems; <span style="font-weight:bold; color:#2ecc71;">you fixed them.</span> You noticed that Data Structures students were struggling because they didn't have MATLAB background. Other instructors would have just continued with MATLAB. It's the standard. It's always been done that way. You didn't think that way. You proposed <span style="font-weight:bold; color:#1565C0;">pivoting the entire course language to Python.</span> That's not a small change. That's redesigning a course. That's pushing back against convention. Your HOD initially resisted; which makes sense, because changing course language is a big deal and carries risk. But you didn't accept the "no." You persisted. You presented your case with data and reasoning. You got it approved. And when the course ran with Python, performance improved. You saw a broken system and you fixed it. You didn't just work around the problem; you solved it. That kind of initiative is rare.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
When we asked about your technical interests, you talked about bioinformatics and health data; and the conversation shifted. Your energy changed. You weren't just giving answers anymore. You were explaining why health data matters, how it impacts lives, what gets missed when the data isn't right. That kind of passion is what drives good research.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's the Part We Need to Be Honest About
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You are genuinely an excellent data scientist. Your technical competence is real and demonstrated. But when we listened to you talk about your work, when we asked you questions about your research and your teaching, something became clear. <span style="font-weight:bold; color:#2ecc71;">Your passion and your expertise lie in health sector data.</span> Your degree is in bioinformatics. Health data science is where your fire is. You light up when you talk about it. We can see it. This particular role is education-focused. It's about student learning data and educational outcomes. That's important work, but it's not where your energy naturally flows. And we believe you should work where your energy naturally flows.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's Where We Want to Leave Things
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You have both the technical skills and the drive to solve real problems. <span style="font-weight:bold; color:#2ecc71;">We'd genuinely like to stay connected.</span> If an opportunity comes up that aligns with your experience and strengths, we'd welcome talking again.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 30px 0; line-height:1.75; text-align:justify;">
P.S.; <span style="font-weight:bold; color:#1565C0;">That MATLAB-to-Python pivot still stands out.</span> That kind of initiative; seeing what's broken and fixing it instead of accepting it; is genuinely rare.
</p>

"""

# ============================================
# SEND ALL 4 EMAILS IN PILOT MODE
# ============================================

if __name__ == "__main__":
    pilot_recipients = [
        "ayesha.khan@taleemabad.com",
        "jawwad.ali@taleemabad.com"
    ]

    print("[PILOT] Sending 4 warm bench feedback emails (HAROON-ALIGNED FINAL — REJECTION-KEEP-WARM)...\n")

    # Email 1: Dur E Nayab
    print("1. Dur E Nayab (KEEP WARM) — Subject: When Gestures Speak Louder")
    send_warm_bench_email(
        candidate_name="Dur E Nayab",
        candidate_email="durenayab349@gmail.com",
        position="Junior Research Associate",
        body_html=dur_e_nayab_body,
        subject="When Gestures Speak Louder",
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    # Email 2: Daniyah Noor
    print("2. Daniyah Noor (KEEP WARM) — Subject: 200 Voices, One Choice, Endless Grit")
    send_warm_bench_email(
        candidate_name="Daniyah Noor",
        candidate_email="daniyahnoor@gmail.com",
        position="Junior Research Associate",
        body_html=daniyah_noor_body,
        subject="200 Voices, One Choice, Endless Grit",
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    # Email 3: Hassan Zafar
    print("3. Hassan Zafar (KEEP WARM) — Subject: The Journal That Proved Your Resilience")
    send_warm_bench_email(
        candidate_name="Hassan Zafar",
        candidate_email="hassanzafar8004474@gmail.com",
        position="Junior Research Associate",
        body_html=hassan_zafar_body,
        subject="The Journal That Proved Your Resilience",
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    # Email 4: Mahnoor Hasan
    print("4. Mahnoor Hasan (KEEP WARM) — Subject: The Language That Fixed Everything")
    send_warm_bench_email(
        candidate_name="Mahnoor Hasan",
        candidate_email="mahnoorhasan122@gmail.com",
        position="Junior Research Associate",
        body_html=mahnoor_hasan_body,
        subject="The Language That Fixed Everything",
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    print("\n[OK] All 4 HAROON-ALIGNED emails sent to pilot recipients for review.")
