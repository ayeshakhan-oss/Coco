#!/usr/bin/env python3
"""
WARM BENCH FEEDBACK EMAILS — 4 JRA Candidates (LIVE SEND)
Status: PRODUCTION SEND TO CANDIDATES
"""

from warm_bench_locked import send_warm_bench_email

# Email bodies (same as pilot version)
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

hassan_zafar_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Hassan,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
This isn't a yes for now. But we need to tell you something about what we saw in your interview, because it matters more than you might realize.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
There's a specific moment from your values interview that stayed with us. About 20 minutes in, you told us about keeping a journal during your first month at your last role. Most people don't reflect that deliberately. Most people move through their first month thinking about tasks, workflows, adjustments. But you wrote things down. You documented what you were learning, what was hard, what surprised you. And when you opened that journal during the interview and read passages from it, the room shifted. You said: <span style="font-weight:bold; color:#1565C0;">"I was completely wrong about how teams work. I thought it was about being right. I learned it's about being useful."</span> That's not something you get from training. <span style="font-weight:bold; color:#2ecc71;">That's someone who actually reflects on their own mistakes and builds from them.</span> You didn't hide what you got wrong. You owned it. You learned from it. You moved forward.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
What Genuinely Impressed Us
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Later, when we asked about handling difficult feedback, you described a moment with a senior colleague who gave you harsh criticism on a project. Instead of defending your work or making excuses, you said something powerful: <span style="font-weight:bold; color:#1565C0;">"I realized they were right. I hadn't actually listened to what they were asking for. I went back, read their feedback three times, and started over."</span> That openness to being wrong—especially in front of authority—is uncommon. Most people get defensive. Most people protect their ego. You prioritize learning over being right.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
When we asked about your approach to research, you explained how you've learned to ask better questions before diving into analysis. You said you used to jump straight to methods, but now you sit with the problem first. You listen to stakeholders. You understand constraints. That maturity in problem-solving—knowing that understanding the problem is half the work—is something we value enormously in research teams.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's the Part We Need to Be Honest About
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
In our technical interview, we found that while your approach to learning is solid, your depth in advanced research methodologies is still developing. We walked through scenarios that required knowledge of specific statistical frameworks and research design patterns, and while you showed good instincts, the technical rigor we need for this role at this moment requires more foundation than you currently have. This isn't a reflection on your potential. You've shown us you can learn hard things. It's about the fit for this role, right now.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's Where We Want to Leave Things
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<span style="font-weight:bold; color:#2ecc71;">Your willingness to be wrong and learn from it is genuinely rare.</span> That trait matters far more than technical knowledge in the long run, because technical knowledge changes and evolves, but the willingness to learn doesn't. We'd genuinely like to stay connected. If an opportunity comes up that aligns with your experience and strengths, we'd welcome talking again.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 30px 0; line-height:1.75; text-align:justify;">
P.S.; The journal entry you read to us—the one about being wrong—that's the thing the room will remember. That's who you are. That's someone we'd want on our team.
</p>
"""

mahnoor_hasan_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Mahnoor,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
This isn't a yes for now. But we need to tell you something about what we discovered in your interview, because it reveals how you think.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
There's a moment about 28 minutes into your values interview that we've discussed multiple times since. You were explaining how you solved a technical problem—something about debugging code that a team member had written. Instead of just telling us you fixed it, you explained the language you used when talking to the colleague. You said: <span style="font-weight:bold; color:#1565C0;">"I didn't say 'you did this wrong.' I said 'I'm seeing this behavior—help me understand what you were trying to do.'"</span> That choice of language matters enormously. <span style="font-weight:bold; color:#2ecc71;">You think about how your words land on another person, especially when giving feedback.</span> You don't just solve the problem; you solve it in a way that protects the other person's dignity. That's emotional intelligence. That's someone who understands that how you say something is as important as what you say.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
What Genuinely Impressed Us
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Later, you described your approach to learning new tools. Rather than just memorizing documentation, you told us you engage with the tool first, break it, figure out what it does, then read the docs. That hands-on, curious approach to technical learning shows self-direction. You don't wait for someone to teach you; you learn by doing.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
When we asked about your role in a collaborative research project, you described how you navigated conflicting perspectives among team members. Instead of trying to get everyone to agree, you said you helped each person articulate what they valued about different approaches, and then you found a path that honored multiple perspectives. That's mature thinking. That's someone who understands that not every problem has a single right answer.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's the Part We Need to Be Honest About
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
In our technical interview, we found that your technical foundation is solid, but it's not yet at the depth we need for this role. You understand concepts well and you learn quickly, but when we asked you to work through complex research design problems under time pressure, the depth of your methodology knowledge became apparent. For this specific role, at this specific moment, we need someone with more research methodology expertise already developed. This isn't about your capability or potential. It's about the fit for where we are right now.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#1565C0; font-weight:bold; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's Where We Want to Leave Things
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<span style="font-weight:bold; color:#2ecc71;">The way you think about language and its impact on people matters.</span> It means you understand that collaboration isn't transactional; it's relational. We'd genuinely like to stay connected. If an opportunity comes up that aligns with your experience and strengths, we'd welcome talking again.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 30px 0; line-height:1.75; text-align:justify;">
P.S.; The thing we'll remember: you think about how your words land. "I'm seeing this behavior" instead of "you did this wrong." That's how people grow. That's who you are.
</p>
"""

# CC list for live send
cc_list = [
    'hiring@taleemabad.com',
    'muzzammil.patel@taleemabad.com',
    'ayesha.khan@taleemabad.com'
]

print("[LIVE] Sending 4 warm bench feedback emails to candidates...")
print(f"CC: {', '.join(cc_list)}\n")

# Send all 4 emails LIVE
send_warm_bench_email(
    candidate_name="Dur E Nayab",
    candidate_email="durenayab349@gmail.com",
    position="Junior Research Associate",
    body_html=dur_e_nayab_body,
    subject="When Gestures Speak Louder",
    pilot_mode=False,
    cc_list=cc_list
)

send_warm_bench_email(
    candidate_name="Daniyah Noor",
    candidate_email="daniyahnoor@gmail.com",
    position="Junior Research Associate",
    body_html=daniyah_noor_body,
    subject="200 Voices, One Choice, Endless Grit",
    pilot_mode=False,
    cc_list=cc_list
)

send_warm_bench_email(
    candidate_name="Hassan Zafar",
    candidate_email="hassanzafar8004474@gmail.com",
    position="Junior Research Associate",
    body_html=hassan_zafar_body,
    subject="The Journal That Proved Your Resilience",
    pilot_mode=False,
    cc_list=cc_list
)

send_warm_bench_email(
    candidate_name="Mahnoor Hasan",
    candidate_email="mahnoorhasan122@gmail.com",
    position="Junior Research Associate",
    body_html=mahnoor_hasan_body,
    subject="The Language That Fixed Everything",
    pilot_mode=False,
    cc_list=cc_list
)

print("\n[OK] All 4 warm bench emails sent LIVE to candidates with proper CC.")
