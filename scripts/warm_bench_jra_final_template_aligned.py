#!/usr/bin/env python3
"""
WARM BENCH FEEDBACK EMAILS — 4 JRA Candidates (TEMPLATE-ALIGNED FINAL)
Status: READY FOR PILOT

Following exact template structure from:
1. Amina (Leadership Instincts, Why This Role Wasn't the Fit)
2. Jalal (On-Ground Passion, Why Assessment Foundations Matter First)

Key elements:
- "PEOPLE & CULTURE • APPLICATION UPDATE" header
- Custom title explaining WHY
- Dear [Candidate], opening
- "We will not be moving forward... clarity is most respectful..."
- "We also want to offer you something more than a decision..."
- What We Liked Most About You
- Where We Found Ourselves Sitting With Questions
- What We Think You Should Do Next
- P.S. (memorable moment)
- Feedback survey: "BE HONEST. WE CAN TAKE IT."
- Sign: Jawwad Ali, People and Culture
"""

from scripts.warm_bench_locked import send_warm_bench_email

# ============================================
# CANDIDATE 1: DUR E NAYAB (OFFER)
# ============================================

dur_e_nayab_body = """
<p style="font-family:Georgia,serif; font-size:12px; color:#5B8DBE; letter-spacing:2px; font-weight:bold; margin:0 0 20px 0; text-transform:uppercase;">
PEOPLE &amp; CULTURE • POSITION OFFER
</p>

<p style="font-family:Georgia,serif; font-size:20px; color:#1565C0; font-weight:bold; margin:0 0 20px 0;">
You're Our Junior Research Associate
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Dear Dur E Nayab,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You are our Junior Research Associate. We want to say that directly, because clarity is the most respectful thing we can offer.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We also want to offer you something more than a decision. The grit you showed through personal grief, the way you help without needing credit, the willingness you bring to lead through ambiguity, those things deserve a genuine response. This is ours.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What We Liked Most About You</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You led the Sonu Kahani digital project at Amal Academy—a project built entirely around social media, video creation, and public performance. All things that run counter to your nature. While managing team conflict, your grandmother was on her deathbed. You were on calls from the kitchen about video uploads. You could have rescheduled the interview. You didn't. You showed up. You led. The room went quiet. You didn't walk away from hard things when they mattered.

You also help without needing to be seen. At Capacity Analytics, you reviewed Ikra's Excel work, caught her errors, framed corrections so they'd pass the supervisor's standard without drawing attention. Then you said something that changed how we heard the story: "Gestures should be unspoken." You didn't need credit. You just helped. Most people tell the story differently. You told it with humility.

You challenged your supervisor Ayesha during an overnight rules revision when the team was running out of time. You suggested a more efficient process strategy. She listened. The Karachi Chamber portion was completed on time. You don't just work inside systems. You improve them.

Your hiring manager noted: "Excellent candidate overall. Displayed sound understanding of research design and methodologies. Very positive attitude as well as good understanding of on-ground challenges within the education sector in Pakistan. Good grasp of the complexities and challenges of handling large datasets."
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Where We're Aligned With You</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You understand what we're building in education. You're genuinely energized by the challenge. You have the intellectual foundation to engage with research design and data complexity. You have the capacity to show up on our values daily. Your GWC assessment confirmed this across Get It, Want It, and Capacity to Do It.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What We're Building Together</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You'll learn student learning data analysis with us. That's a skill we'll build together. Your foundation is strong. Your grit is real. Those are what matter. We've worked with people who knew more but cared less. You're the opposite. You care. You persist. You help quietly. Those qualities don't fade. Skills get built.

Jawwad from People & Culture will send formal offer details. But we wanted you to hear from us first.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Warm regards,<br/>
Jawwad Ali<br/>
People and Culture | Taleemabad<br/>
jawwad.ali@taleemabad.com | www.taleemabad.com<br/>
Sent on behalf of Jawwad by Coco, AI Hiring Assistant | People and Culture, Taleemabad
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
P.S. — The thing that will stick with us: "Gestures should be unspoken." You don't lead by being seen. You lead by staying quiet and making the right move. That's exactly who we need.
</p>
"""

# ============================================
# CANDIDATE 2: DANIYAH NOOR (OFFER)
# ============================================

daniyah_noor_body = """
<p style="font-family:Georgia,serif; font-size:12px; color:#5B8DBE; letter-spacing:2px; font-weight:bold; margin:0 0 20px 0; text-transform:uppercase;">
PEOPLE &amp; CULTURE • POSITION OFFER
</p>

<p style="font-family:Georgia,serif; font-size:20px; color:#1565C0; font-weight:bold; margin:0 0 20px 0;">
You're Our Junior Research Associate
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Dear Daniyah,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You are our Junior Research Associate. We want to say that directly, because clarity is the most respectful thing we can offer.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We also want to offer you something more than a decision. The resilience you showed through unemployment and despair, the way you step in when systems are failing, the advocacy instinct you show for voiceless people, those things deserve a genuine response. This is ours.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What We Liked Most About You</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
About 35 minutes into your values conversation, you told us about hostel ayahs—cleaners hired through subcontracting who'd lost benefits. You didn't stay silent. "I took initiative in and with other students. We got 200 signatories to end subcontracting in LUMS." You elevated their voices to senior leadership. You influenced policy change. That petition is still ongoing. The room felt the weight of that commitment.

You also carried a story of three months unemployed after graduation during economic hardship. Genuine despair. Suicidal ideation. You said: "Maybe I was struggling with a bit of depression, but I carried on. I kept applying to jobs." You didn't give up on purpose-driven work. "It is just a matter of waiting and finding and being resilient and not giving up on yourself and what you believe in." You persevered. You landed your first development sector job. You gained clarity. We can't train that kind of grit.

You also transformed how you learn. O-levels taught you rote learning. LUMS required critical thinking. Sophomore year hit hard: "I struggled for 2 years. Academic itna achha nahi kar rahi thi, but that was a wake up call." Junior year you shifted deliberately. "When I made that shift junior year mein mujhe genuinely feel Hua ke meri genuine inquiries jyaada may. What makes this work, what's the reasoning." You articulate something most people don't: "Learning isn't something you do just university tak ya masters tak. It's a thing that you do throughout your life." Not just growth in a role. A fundamental belief in continuous improvement.

Your hiring manager noted: "Excellent overall candidate. Solid analytical skills and good grasp of research design and methodologies."
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Where We're Aligned With You</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You understand what we're building in education. You're genuinely energized by impact. You have the intellectual foundation to engage with research design and methodologies. You have the capacity to show up on our values daily. Your GWC assessment confirmed this across Get It, Want It, and Capacity to Do It.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What We're Building Together</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Student learning data will be new to you. We'll teach you. Your learning mindset is already there—you shifted from rote learning to critical thinking at LUMS. You'll make that shift with us. Your foundation is strong. Your grit is real. Those are what matter.

Jawwad from People & Culture will send formal offer details. But we wanted you to hear from us first.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Warm regards,<br/>
Jawwad Ali<br/>
People and Culture | Taleemabad<br/>
jawwad.ali@taleemabad.com | www.taleemabad.com<br/>
Sent on behalf of Jawwad by Coco, AI Hiring Assistant | People and Culture, Taleemabad
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
P.S. — The thing that will stick with us: you don't just care about systems. You care about the people inside them. You didn't just talk about subcontracting—you got 200 signatures to change it. That's exactly who we need.
</p>
"""

# ============================================
# CANDIDATE 3: HASSAN ZAFAR (KEEP WARM)
# ============================================

hassan_zafar_body = """
<p style="font-family:Georgia,serif; font-size:12px; color:#5B8DBE; letter-spacing:2px; font-weight:bold; margin:0 0 20px 0; text-transform:uppercase;">
PEOPLE &amp; CULTURE • APPLICATION UPDATE
</p>

<p style="font-family:Georgia,serif; font-size:20px; color:#1565C0; font-weight:bold; margin:0 0 20px 0;">
Your Grit, and Why Research Design Matters Now
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Dear Hassan,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We will not be moving forward with your application for the Junior Research Associate role. We want to say that plainly, because clarity is the most respectful thing we can offer.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We also want to offer you something more than a decision. The persistence you showed in your Masters work, the way you back your team under pressure, the integrity you carry through difficult research, those things deserve a genuine response. This is ours.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What We Liked Most About You</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
About 18 minutes in, you told us you completed your Masters in three years while working simultaneously at a consultancy firm. Your research paper is under review in a reputable Q1 journal. You did this with minimal supervisor support. You didn't step back. You persisted. The room wrote it down.

Your BS fieldwork showed real intelligence. You collected sensitive income data in remote rural areas for a women empowerment in agriculture thesis. Building community trust to get data that respondents normally refuse takes both cultural awareness and persistence. You designed indirect questioning methodology to overcome resistance. That's grit and thoughtfulness.

You also back your team publicly. When your manager's sampling methodology faced team pushback, you supported her approach even when others called it risky. The methodology held. When results came out opposite to what was expected—negative impact of remittances on child education—supervisors criticized the findings. You stood beside the team. You stood beside the methodology, which was sound. You accepted the outcome together. That's integrity under pressure.

At about 50 minutes, you gave direct feedback to your organization's management. You warned against over-reliance on AI for proposal writing and suggested pivoting toward Pakistani tenders instead of international ones. Both changes led to measurable improvement in business performance. You don't just work inside systems. You fix them.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Where We Found Ourselves Sitting With Questions</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We share what follows with care, because honest reflection is more useful than softness.

During our GWC conversation and case study review, we found significant gaps in your approach to applied research design, sampling methodology, and research design specifics. When we pressed on these—particularly around methodology rigor and sampling logic—the responses weren't where they needed to be for this role at this moment. This isn't about your potential or your values. It's about the specific skill match for this position right now.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What We Think You Should Do Next</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Your grit and integrity are real. If you go deeper into applied research design—really study it, own a research arc end-to-end, work through real projects with rigorous methodology—that gap closes. The next door opens. We'd like to stay connected. When roles align with your strengths, we'd genuinely welcome talking again. Would you be open to that?
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Warm regards,<br/>
Jawwad Ali<br/>
People and Culture | Taleemabad<br/>
jawwad.ali@taleemabad.com | www.taleemabad.com<br/>
Sent on behalf of Jawwad by Coco, AI Hiring Assistant | People and Culture, Taleemabad
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
P.S. — The Q1 journal work matters. Masters in three years while employed. That's not luck. That's resilience. That will take you far. Build on it.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">BE HONEST. WE CAN TAKE IT.</strong>
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
How did this land for you?<br/>
1 2 3 4 5<br/>
1 = missed the mark    5 = really landed<br/>
<br/>
Did it feel written for you specifically?<br/>
Yes, personal    Somewhat    No, felt generic<br/>
<br/>
Was the feedback useful?<br/>
Very useful    Somewhat    Not really
</p>
"""

# ============================================
# CANDIDATE 4: MAHNOOR HASAN (KEEP WARM)
# ============================================

mahnoor_hasan_body = """
<p style="font-family:Georgia,serif; font-size:12px; color:#5B8DBE; letter-spacing:2px; font-weight:bold; margin:0 0 20px 0; text-transform:uppercase;">
PEOPLE &amp; CULTURE • APPLICATION UPDATE
</p>

<p style="font-family:Georgia,serif; font-size:20px; color:#1565C0; font-weight:bold; margin:0 0 20px 0;">
Your System-Fixing Instincts, and Why Health Tech Is Your Path
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Dear Mahnoor,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We will not be moving forward with your application for the Junior Research Associate role. We want to say that plainly, because clarity is the most respectful thing we can offer.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We also want to offer you something more than a decision. The determination you showed through hardship, the way you fix broken systems, the technical excellence you bring, those things deserve a genuine response. This is ours.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What We Liked Most About You</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
About 10 minutes in, you told us you were assigned to teach C++ lab with zero prior knowledge in the language. A subject entirely outside your expertise. You could have rescheduled. You didn't. You self-studied. You built confidence. You conducted the labs. You received above 80% mid-semester feedback from students. That's grit.

At 25 minutes, you talked about your Masters work on AI for mental health screening. You spent five months with no viable path to data collection. Mental health is sensitive in Pakistan. Building trust and access is difficult. Most people would have given up. You continued pursuing collaborators. Eventually you found a psychiatrist at Benazir Bhutto Hospital willing to help. You didn't abandon the research. That's determination.

But what really showed us something was how you fix systems. You identified that Data Structures lab students lacked MATLAB background—the prerequisite was taught in Python. You didn't just work around the gap. You proposed switching the entire course language from MATLAB to Python. You discussed it with your reporting teacher. You escalated to the HOD who initially resisted. You persisted. You got it approved. Course performance improved. You don't just work inside broken systems. You fix them.

Your hiring manager noted: "She is an excellent data scientist and has significant technical competence."
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Where We Found Ourselves Sitting With Questions</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We share what follows with care, because honest reflection is more useful than softness.

You are an excellent data scientist. Your technical competence is real and strong. But here's what we also noticed: your expertise and your passion lie in the health sector. Your degree is in Bioinformatics. Your expertise is in data science and machine learning for health applications. That sector—those problems, that domain—appear more aligned with your longer-term career goals than education sector work. This role is specialized for education impact research. We'd be a better fit for each other when the role aligns with your deeper strengths and goals.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What We Think You Should Do Next</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Go deep in health data science. That's where your fire is. That's where you belong. If we ever open something in health tech—on our data team or in health initiatives—we'd genuinely welcome talking. You're someone we'd want to build with. Your persistence, your initiative, your system-fixing instincts—those are exactly the qualities we need. We'd like to stay connected. Would you be open to that?
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Warm regards,<br/>
Jawwad Ali<br/>
People and Culture | Taleemabad<br/>
jawwad.ali@taleemabad.com | www.taleemabad.com<br/>
Sent on behalf of Jawwad by Coco, AI Hiring Assistant | People and Culture, Taleemabad
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
P.S. — The MATLAB-to-Python pivot matters. You didn't just adapt. You fixed a broken system. Entire course performance improved because you spoke up. That initiative is rare. Take it to health tech. That's where you'll shine.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">BE HONEST. WE CAN TAKE IT.</strong>
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
How did this land for you?<br/>
1 2 3 4 5<br/>
1 = missed the mark    5 = really landed<br/>
<br/>
Did it feel written for you specifically?<br/>
Yes, personal    Somewhat    No, felt generic<br/>
<br/>
Was the feedback useful?<br/>
Very useful    Somewhat    Not really
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

    print("[PILOT] Sending 4 template-aligned warm bench emails...\n")

    # Email 1: Dur E Nayab
    print("1. Dur E Nayab (OFFER)")
    send_warm_bench_email(
        candidate_name="Dur E Nayab",
        candidate_email="durenayab349@gmail.com",
        position="Junior Research Associate",
        body_html=dur_e_nayab_body,
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    # Email 2: Daniyah Noor
    print("2. Daniyah Noor (OFFER)")
    send_warm_bench_email(
        candidate_name="Daniyah Noor",
        candidate_email="daniyahnoor@gmail.com",
        position="Junior Research Associate",
        body_html=daniyah_noor_body,
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    # Email 3: Hassan Zafar
    print("3. Hassan Zafar (KEEP WARM)")
    send_warm_bench_email(
        candidate_name="Hassan Zafar",
        candidate_email="hassanzafar8004474@gmail.com",
        position="Junior Research Associate",
        body_html=hassan_zafar_body,
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    # Email 4: Mahnoor Hasan
    print("4. Mahnoor Hasan (KEEP WARM)")
    send_warm_bench_email(
        candidate_name="Mahnoor Hasan",
        candidate_email="mahnoorhasan122@gmail.com",
        position="Junior Research Associate",
        body_html=mahnoor_hasan_body,
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    print("\n[OK] All 4 template-aligned emails sent to pilot recipients.")
