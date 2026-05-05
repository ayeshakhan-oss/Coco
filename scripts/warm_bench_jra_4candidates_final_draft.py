#!/usr/bin/env python3
"""
WARM BENCH FEEDBACK EMAILS — 4 JRA Candidates (Final Draft - Pilot)
Status: READY FOR PILOT TO AYESHA + JAWWAD

Candidates:
1. Dur E Nayab (Values PASS + GWC PASS)
2. Daniyah Noor (Values PASS + GWC PASS)
3. Hassan Zafar (Values PASS + GWC NO)
4. Mahnoor Hasan (Values PASS + GWC NO)

All pilot to: ayesha.khan@taleemabad.com, jawwad.ali@taleemabad.com
"""

from scripts.warm_bench_locked import send_warm_bench_email

# ============================================
# CANDIDATE 1: DUR E NAYAB
# ============================================

dur_e_nayab_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Dur E Nayab,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We wanted to reach out to say thank you. Over these past weeks, we've had the privilege of getting to know you through our values conversation, and what struck us most was how you show up when things are hard. You didn't just talk about resilience in the abstract—you lived it. You led a social media project at Amal Academy, a domain that genuinely runs counter to your nature, while your grandmother was on her death bed and you were managing team conflict from the kitchen. Rather than step back, you made a detailed flow chart—who to deal with how, what your responsibilities were—and channeled your energy constructively. That's the kind of person who doesn't walk away.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What We Saw</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Your values conversation showed us real strength across multiple dimensions. When you faced a rigorous Eviews project with a team weak on the command language, you spent 2 days with a classmate—learning from YouTube, ChatGPT, a senior's guidance—until you got the data right and submitted work in the B+ to A range. You didn't accept "we're stuck." You're someone who sees a gap and fills it. You also teach. You gave a junior at university one hour of personal instruction on Stata basics and how to use AI tools effectively for debugging—and she's since landed jobs using those skills. Most importantly, you do this without needing credit. Your colleague Ikra never explicitly knew you reviewed her Excel work and caught her errors so they'd pass Ayesha's standard without drawing attention. You just did it quietly because "gestures should be unspoken."
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You also speak up. At Capacity Analytics, you suggested a revised process strategy to Ayesha during an overnight rules revision when the team was running out of time. She listened. The Karachi Chamber portion was completed on time. And outside of work, you regularly challenge your strict Pashtun father on family decisions—you say a dua before entering his room because of his anger, but you go in anyway, calmly, and the feedback lands.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Your GWC Assessment</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Our GWC conversation showed us that you understand our mission deeply, you're genuinely energized by our work, and you have the capacity to show up on our values daily. You scored a strong Get It (10/10), Want It (9.5/10), and Capacity (9.5/10)—a full Yes across the board. Our hiring manager noted: "Excellent candidate overall. Might need some training with analysis of assessments data but displayed a sound understanding overall. Had a very positive attitude as well as good understanding of on-ground challenges within the education sector in Pakistan. Had a good grasp of the complexities and challenges of handling large datasets." He also recognized your longer-term potential: "Her career plans down the line could diverge towards think-tanks or multilateral agencies but this role will help her get there and she'd be an asset for Taleemabad."
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Where this particular Junior Research Associate role didn't advance isn't about your strengths—it's about the specific composition and needs we're building for this cycle. We were looking for a particular blend of research design experience and available capacity. But make no mistake: your alignment with our mission, your grit, and your ability to lead through ambiguity matter to us deeply.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">The Warm Bench</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's what we want you to know: we're not closing the door. In fact, we're keeping it open deliberately.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Your values alignment and the thoughtfulness you brought to our conversations matter to us. When roles open that fit your strengths and experience—whether in research, data analysis, or any function where grit and alignment are load-bearing—we'd genuinely welcome your application. You're exactly the kind of person we want to build our team with. And if this isn't the right moment, the right role will come. Keep an eye on our careers page (www.taleemabad.com/careers). We hope you'll think of us when opportunities resonate with you, and we'd be delighted to consider your application.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Thank you again for investing your energy in getting to know us. Your thoughtfulness, integrity, and genuine desire to be in service came through in every conversation, and that matters. We're thinking of you as we build.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Warm regards,<br/>
People and Culture Team<br/>
Taleemabad<br/>
hiring@taleemabad.com | www.taleemabad.com<br/>
Sent on behalf of Talent Acquisition Team by Coco
</p>
"""

# ============================================
# CANDIDATE 2: DANIYAH NOOR
# ============================================

daniyah_noor_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Daniyah,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We wanted to reach out to say thank you. Over these past weeks, we've had the privilege of getting to know you through our values conversation, and what struck us most was how you show up for others, often in ways that go unnoticed. You backed hostel ayahs—cleaners hired through subcontracting who'd lost benefits—and rather than stay silent, you took initiative. "I took initiative in and with other students... we were able to get 200 signatories to end subcontracting in lums." You elevated their voices to senior leadership and influenced policy change. That petition is still ongoing. You also organized a Hindu religious tolerance event at a time of India-Pakistan political division, creating inclusive space when the moment was tense. These weren't small gestures. They were acts of advocacy for people without a seat at the table. That's the kind of person you are.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What We Saw</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Your resilience is real. You described 3 months of unemployment post-graduation during economic hardship. You carried genuine despair, even suicidal ideation: "maybe I was struggling with a bit of depression, but I carried on. I kept applying to jobs." Rather than give up on your belief in purpose-driven work, you persevered: "it is just a matter of waiting and finding and just being resilient and not giving up on yourself and what you believe in." You landed your first development sector job and gained clarity. That's not aspirational talk—you lived it.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Your learning narrative is also compelling. O-levels taught you rote learning; LUMS required critical thinking. Sophomore year didn't go well academically: "I struggled for 2 years... my sophomore year... academic itna achha nahi kar rahi thi, but that was also a wake up call for me." Junior year you made a deliberate shift: "when I made that shift junior year mein mujhe genuinely feel Hua ke meri genuine inquiries jyaada may... what makes this work, what's the reasoning." This changed how you consume knowledge. And you articulate learning as lifelong: "learning isn't something you do just like university tak ya masters tak ya PhD tak. It's a thing that you do throughout your life." Not just growth in role, but a fundamental belief in continuous improvement.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Your GWC Assessment</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Our GWC conversation surfaced something clear: you understand our mission deeply, you're genuinely energized by our work, and you have the capacity to show up on our values daily. You scored a full Yes across the board (Get It 9/10, Want It 9/10, Capacity 9/10). Our hiring manager noted: "Excellent overall candidate. Solid analytical skills and good grasp of research design and methodologies." He also observed something important: "The only drawback was that she did not have experience working specifically with student learning data." That's a skill gap we can address through training—your foundation is strong.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Where this particular Junior Research Associate role didn't advance isn't about your fit or your potential—it's about the specific needs and team composition we're building for this cycle. But your values alignment, your advocacy instinct, and your learning mindset are exactly what we're looking for.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">The Warm Bench</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Here's what we want you to know: we're not closing the door. In fact, we're keeping it open deliberately.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Your values alignment and the thoughtfulness you brought to our conversations matter to us. When roles open that fit your strengths and experience—whether in research, program design, or any function where advocacy and learning agility are load-bearing—we'd genuinely welcome your application. You're exactly the kind of person we want to build our team with. And if this isn't the right moment, the right role will come. Keep an eye on our careers page (www.taleemabad.com/careers). We hope you'll think of us when opportunities resonate with you, and we'd be delighted to consider your application.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Thank you again for investing your energy in getting to know us. Your thoughtfulness, integrity, and genuine care for others came through in every conversation, and that matters. We're thinking of you as we build.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Warm regards,<br/>
People and Culture Team<br/>
Taleemabad<br/>
hiring@taleemabad.com | www.taleemabad.com<br/>
Sent on behalf of Talent Acquisition Team by Coco
</p>
"""

# ============================================
# CANDIDATE 3: HASSAN ZAFAR
# ============================================

hassan_zafar_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Hassan,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We wanted to reach out to say thank you. Over these past weeks, we've had the privilege of getting to know you through our values conversation, and what struck us most was your grit. You chose a rigorous topic for your Masters research on institutional economics, worked simultaneously at a consultancy firm, and completed the degree in 3 years while peers took 4. Your research paper is still under review in a reputable Q1 journal. You did not give up despite minimal supervisor support. That kind of persistence matters.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What We Saw</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Your resilience as a researcher is evident across multiple episodes. For your BS field research, you collected sensitive income data in remote rural areas for a women empowerment in agriculture thesis. Building community trust to get data that respondents normally refuse required both cultural intelligence and persistence. You designed indirect questioning methodology to overcome resistance. That shows not just grit, but thoughtfulness.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You're also someone who backs the team, even when it's uncomfortable. At your previous organization, when your manager's sampling methodology faced team pushback, you publicly supported her approach even when others called it risky. The methodology held and the interview calls came through. On a co-authored research project, results came out opposite to expected (negative impact on child education from remittances). Faced with criticism from supervisors, you stood behind the team and the methodology, which was sound. You accepted the outcome together. That's integrity.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You also speak up when you see a problem. You gave direct feedback to your organization's management: warned against over-reliance on AI for proposal writing (generic output versus specific analysis) and suggested pivoting focus toward Pakistani tenders versus international ones. Both changes led to measurable improvement in business performance. And when you received incremental feedback from your supervisor, your first instinct was frustration and pushback. But you reflected, apologized, and implemented all feedback. Subsequent proposals showed dramatically improved quality. You acknowledged that your supervisor was protecting his motivation by spacing the feedback. That's growth.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">On This Particular Role</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We need to be transparent with you. During our GWC conversation and case study review, we found significant gaps in your approach to research methodology, sampling, and research design. When pressed on these during the interview, the responses were not satisfactory. This role requires a certain depth in applied research design that we don't believe is present yet. This is not a reflection on your potential or your values—you clearly have both. It's about the specific skill match for this role at this moment.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">The Warm Bench</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
But here's what we want you to know: your values alignment and your capacity to show up with integrity in your work matter to us. We're not closing the door. In fact, we're keeping it open deliberately.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
When roles open that fit your strengths—whether in research, policy analysis, think-tank work, or any function where grit, integrity, and analytical thinking are load-bearing—we'd genuinely welcome your application. You're exactly the kind of person we want to build with. And if this isn't the right moment, the right role will come. Keep an eye on our careers page (www.taleemabad.com/careers). We hope you'll think of us when opportunities resonate with you, and we'd be delighted to consider your application.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Thank you again for investing your energy in getting to know us. Your grit, integrity, and genuine commitment to rigorous research came through in every conversation, and that matters. We're thinking of you.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Warm regards,<br/>
People and Culture Team<br/>
Taleemabad<br/>
hiring@taleemabad.com | www.taleemabad.com<br/>
Sent on behalf of Talent Acquisition Team by Coco
</p>
"""

# ============================================
# CANDIDATE 4: MAHNOOR HASAN
# ============================================

mahnoor_hasan_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Mahnoor,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We wanted to reach out to say thank you. Over these past weeks, we've had the privilege of getting to know you through our values conversation, and what struck us most was how you show up when things are hard. You were assigned C++ lab instruction despite having no prior knowledge—a subject entirely outside your expertise. Rather than say no, you self-studied, built confidence, and conducted the labs. You received above 80% mid-semester feedback from students. You didn't walk away.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What We Saw</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Your persistence shows up in your research as well. For your Masters work on AI for mental health screening, you spent 5 months with no viable path to data collection. Mental health data is sensitive in Pakistan; building trust and access is difficult. Rather than abandon the research, you continued pursuing potential collaborators. Eventually, you found a psychiatrist at Benazir Bhutto Hospital willing to help. You did not give up.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You also improve systems. You identified that students in your Data Structures lab lacked MATLAB background (the prerequisite was taught in Python). Rather than work around the gap, you proposed switching the entire course language from MATLAB to Python. You discussed with your reporting teacher, escalated to the HOD who initially resisted, and eventually got the amendment approved. Course performance improved. You don't just adapt to broken systems; you fix them.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You also speak up. At NUST, your PI assigned extra unpaid work—YouTube video editing and workshop assistance. You told him directly these were outside your job description and you would expect compensation if required to do them. The conversation was uncomfortable and ultimately you were still made to do the work, but you raised it. That matters. You also had direct behavioral conversations with troublemaker first-semester students, spoke directly, referenced your own recent experience going through the same phase, and saw visible behavioral improvement by second semester.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">On This Particular Role</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We need to be transparent with you. You are an excellent data scientist with significant technical competence. Your GWC assessment confirmed this: Get It (10/10), Want It (8/10), Capacity (9/10). Your hiring manager noted: "She is an excellent data scientist and has significant technical competence." However, we also recognized something important: your expertise and passion lie in the health sector. Your degree is in Bioinformatics and you have significant expertise in data science and machine learning for health applications. That sector and those problems appear more aligned with your longer-term career goals than the education sector.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
This particular Junior Research Associate role is specialized for education impact research. While you could do this work, we believe you'd find more fulfillment and growth in a role that sits at the intersection of health, data science, and impact—areas where your passion clearly lies. We'd be a better fit for each other when the role aligns with your deeper strengths and goals.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">The Warm Bench</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
But here's what we want you to know: we're not closing the door. In fact, we're keeping it open deliberately. Your values alignment, technical excellence, and commitment to showing up even when things are hard matter to us.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
When roles open that fit your expertise and passions—whether on our data team, in health tech initiatives, or any function where data science and impact intersect—we'd genuinely welcome your application. You're exactly the kind of person we want to build with. And if this isn't the right moment, the right role will come. Keep an eye on our careers page (www.taleemabad.com/careers). We hope you'll think of us when opportunities resonate with you, and we'd be delighted to consider your application.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Thank you again for investing your energy in getting to know us. Your technical depth, persistence, and genuine commitment to excellence came through in every conversation, and that matters. We're thinking of you.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Warm regards,<br/>
People and Culture Team<br/>
Taleemabad<br/>
hiring@taleemabad.com | www.taleemabad.com<br/>
Sent on behalf of Talent Acquisition Team by Coco
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

    print("[PILOT] Sending 4 warm bench feedback emails...\n")

    # Email 1: Dur E Nayab
    print("1. Dur E Nayab (Values PASS + GWC PASS)")
    send_warm_bench_email(
        candidate_name="Dur E Nayab",
        candidate_email="durenayab349@gmail.com",
        position="Junior Research Associate",
        body_html=dur_e_nayab_body,
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    # Email 2: Daniyah Noor
    print("2. Daniyah Noor (Values PASS + GWC PASS)")
    send_warm_bench_email(
        candidate_name="Daniyah Noor",
        candidate_email="daniyahnoor@gmail.com",
        position="Junior Research Associate",
        body_html=daniyah_noor_body,
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    # Email 3: Hassan Zafar
    print("3. Hassan Zafar (Values PASS + GWC NO)")
    send_warm_bench_email(
        candidate_name="Hassan Zafar",
        candidate_email="hassanzafar8004474@gmail.com",
        position="Junior Research Associate",
        body_html=hassan_zafar_body,
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    # Email 4: Mahnoor Hasan
    print("4. Mahnoor Hasan (Values PASS + GWC NO)")
    send_warm_bench_email(
        candidate_name="Mahnoor Hasan",
        candidate_email="mahnoorhasan122@gmail.com",
        position="Junior Research Associate",
        body_html=mahnoor_hasan_body,
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    print("\n[OK] All 4 emails sent to pilot recipients for review.")
