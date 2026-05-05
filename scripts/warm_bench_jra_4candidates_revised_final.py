#!/usr/bin/env python3
"""
WARM BENCH FEEDBACK EMAILS — 4 JRA Candidates (REVISED FINAL - Tone/Structure per Haroon Guide)
Status: READY FOR PILOT (REVISED)

Uses tone from Haroon's guide + Ali/Umair examples:
- Warm opening with genuine appreciation
- Direct clarity on decision (gently)
- "What we genuinely saw in you" — specific strengths via storytelling
- "Where you're still building" — growth areas as natural development
- "What we'd suggest" — forward-looking
- Customized subject lines per candidate story
- Poetic, personal, heartfelt (not generic/scoring)

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
# Subject: "Your resilience showed us something real" or "We saw your grit, Dur E Nayab"
# ============================================

dur_e_nayab_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Dur E Nayab,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Thank you for spending your time with us and engaging so openly in our conversation. We genuinely appreciated the thoughtfulness you brought to our discussion, and we want you to know that your effort and openness mattered to us.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
After careful reflection, we've decided not to move forward with your application for this particular role at this time. We want to be clear about that upfront, because clarity is important. But then we'd like to share what we actually observed about you, because we believe it's valuable feedback as you continue growing your career, and it deserves to be specific rather than generic.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What we genuinely saw in you</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You have a real gift for showing up when things are hard. You led the Sonu Kahani digital project at Amal Academy—a project built entirely around social media, video creation, and public performance—all things that run counter to your natural inclinations. While managing team conflict, your grandmother was on her death bed. You were on calls from the kitchen about video uploads. You didn't step back. Instead, you made a detailed flow chart. Who to deal with how. What your responsibilities were. You channeled your energy constructively. The team won second-best award. That's not just perseverance. That's choosing to lead through personal grief.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We also noticed your generosity. You spent two days with a classmate learning Eviews from YouTube, ChatGPT, and a senior's guidance because your team was behind and weak on the command language. You got the data right. You submitted work in the B+ to A range. You also taught a junior at university Stata—one hour of personal instruction on basics, commands, and how to use AI tools for debugging. She landed jobs using those skills. Most tellingly, when you reviewed Ikra's Excel work at Capacity Analytics and caught her errors so they'd pass your supervisor's standard, you never told Ikra explicitly. "Gestures should be unspoken." You helped quietly, without needing credit.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You also speak up when it matters. During an overnight rules revision at Capacity, when the team was running out of time, you suggested a revised process strategy to your supervisor. She listened. The Karachi Chamber portion was completed on time. And outside of work, you regularly challenge your strict Pashtun father on family decisions. You say a dua before entering his room because of his anger, but you go in anyway. Calmly. The feedback lands. That's courage.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Where we're aligned with you</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
When we talked with you about our mission and our work, it was clear you understand what we're trying to do. You're genuinely energized by the challenge of education in Pakistan. You have the intellectual foundation to engage with research design and data complexity. And you have the capacity to show up on our values daily—that's real.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Where this role didn't advance is something different. It's about the specific shape of this team, the particular blend of experience we're building for right now, the timing. It's not about you or your potential. It's about fit for this moment.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Where you could go</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You have real potential. The way you think about problems—deeply, with attention to impact—that's something that will serve you well in research, policy analysis, or anywhere that requires grit and alignment. Keep building on that. Go deeper into the work that genuinely excites you. Whether that's research design, data analysis, or working with organizations that matter to you, your foundation is strong.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
But here's what we also want to say: we're not closing the door. When roles open that fit your strengths—whether in research, think-tank work, or any function where your grit and values alignment are load-bearing—we'd genuinely welcome your application. You're the kind of person we want to build with. Keep an eye on our careers page (www.taleemabad.com/careers). We hope you'll think of us when opportunities resonate with you.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You have real potential. We believe in you. Keep going.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Warm regards,<br/>
People and Culture Team<br/>
Taleemabad
</p>
"""

# ============================================
# CANDIDATE 2: DANIYAH NOOR
# Subject: "You showed us real advocacy" or "What we saw when you spoke for others"
# ============================================

daniyah_noor_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Daniyah,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Thank you for spending your time with us and engaging so openly in our conversation. We genuinely appreciated the thoughtfulness you brought to our discussion, and we want you to know that your effort and openness mattered to us.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
After careful reflection, we've decided not to move forward with your application for this particular role at this time. We want to be clear about that upfront, because clarity is important. But then we'd like to share what we actually observed about you, because we believe it's valuable feedback as you continue growing your career, and it deserves to be specific rather than generic.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What we genuinely saw in you</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You have a real gift for showing up for people without a voice. You noticed that hostel ayahs—the cleaners—were hired through subcontracting and had lost benefits. Rather than stay silent, you took initiative. "I took initiative in and with other students... we were able to get 200 signatories to end subcontracting in lums." You elevated their voices to senior leadership. You influenced policy change. That petition is still ongoing. You also organized a Hindu religious tolerance event at LUMS during a time of India-Pakistan political division. You created inclusive space when the moment was tense. These weren't small gestures. They were acts of genuine advocacy.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We also saw real resilience in you. You described three months of unemployment after graduation during economic hardship. You carried genuine despair, even suicidal ideation. "Maybe I was struggling with a bit of depression, but I carried on. I kept applying to jobs." Rather than give up on your belief in purpose-driven work, you persevered. "It is just a matter of waiting and finding and just being resilient and not giving up on yourself and what you believe in." You landed your first development sector job and gained clarity. That's not aspirational talk. You lived it.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Your learning narrative is also real. O-levels taught you rote learning; LUMS required critical thinking. Your sophomore year wasn't good academically. "I struggled for 2 years... my sophomore year... academic itna achha nahi kar rahi thi, but that was also a wake up call for me." Junior year you made a deliberate shift. "When I made that shift junior year mein mujhe genuinely feel Hua ke meri genuine inquiries jyaada may... what makes this work, what's the reasoning." This changed how you consume knowledge. And you articulate something important: "Learning isn't something you do just like university tak ya masters tak ya PhD tak. It's a thing that you do throughout your life." Not just growth in a role. A fundamental belief in continuous improvement.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Where we're aligned with you</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
When we talked with you about our mission and our work, it was clear you understand what we're trying to do. You're genuinely energized by education impact. You have the intellectual foundation to engage with research design and methodologies. And you have the capacity to show up on our values daily—that's real.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Where this role didn't advance is something different. It's about the specific shape of this team, the particular blend of experience we're building for right now, the timing. It's not about you or your potential. It's about fit for this moment.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Where you could go</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You have real potential. The way you think about impact—with attention to the voiceless, with a learning mindset, with resilience—that's something that will serve you well in research, program design, or anywhere that requires advocacy and learning agility. Keep building on that. Go deeper into work that genuinely excites you.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
But here's what we also want to say: we're not closing the door. When roles open that fit your strengths—whether in research, program design, or any function where your advocacy instinct and learning mindset are load-bearing—we'd genuinely welcome your application. You're the kind of person we want to build with. Keep an eye on our careers page (www.taleemabad.com/careers). We hope you'll think of us when opportunities resonate with you.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You have real potential. We believe in you. Keep going.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Warm regards,<br/>
People and Culture Team<br/>
Taleemabad
</p>
"""

# ============================================
# CANDIDATE 3: HASSAN ZAFAR
# Subject: "Your grit as a researcher" or "We saw your persistence"
# ============================================

hassan_zafar_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Hassan,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Thank you for spending your time with us and engaging so openly in our conversation. We genuinely appreciated the thoughtfulness you brought to our discussion, and we want you to know that your effort and openness mattered to us.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
After careful reflection, we've decided not to move forward with your application for this particular role at this time. We want to be clear about that upfront, because clarity is important. But then we'd like to share what we actually observed about you, because we believe it's valuable feedback as you continue growing your career, and it deserves to be specific rather than generic.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What we genuinely saw in you</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You have a real gift for persisting through difficult research. You chose a rigorous topic for your Masters—institutional economics. You worked simultaneously at a consultancy firm. You completed your degree in three years while peers took four. Your research paper is still under review in a reputable Q1 journal. You did this with minimal supervisor support. You did not give up. That's not luck. That's grit.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
For your BS field research, you collected sensitive income data in remote rural areas for a women empowerment in agriculture thesis. Building community trust to get data that respondents normally refuse required both cultural intelligence and persistence. You designed indirect questioning methodology to overcome resistance. That shows not just grit, but thoughtfulness about how you work with people.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
We also saw you backing your team, even when it was uncomfortable. When your manager's sampling methodology faced team pushback, you publicly supported her approach even when others called it risky. The methodology held. The interview calls came through. On a co-authored project, your results came out opposite to what was expected—negative impact from remittances on child education. Faced with criticism from supervisors, you stood behind the team and the methodology, which was sound. You accepted the outcome together. That's integrity.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You also speak up when you see a problem. You gave direct feedback to your organization's management: warned against over-reliance on AI for proposal writing (generic output versus specific analysis) and suggested pivoting toward Pakistani tenders versus international ones. Both changes led to measurable improvement in business performance. And when you received feedback from your supervisor, your first instinct was frustration and pushback. But you reflected, apologized, and implemented all feedback. Subsequent proposals showed dramatically improved quality. You acknowledged that your supervisor was protecting his motivation by spacing the feedback. That's growth.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Where we're aligned—and where we're not quite aligned</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
When we talked with you about our mission and our work, it was clear you care deeply about rigorous research. You understand the challenges of working with data in the real world. You have integrity. Those things matter to us.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
But this is where we need to be honest: during our case study conversation and research methodology discussion, we found significant gaps in your approach to applied research design and sampling. When we pressed on these, the responses weren't satisfactory. This role requires a depth in applied research design that we don't believe is present yet. This isn't about your potential or your values. It's about the specific skill match for this role at this moment.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Where you could go</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Right now, you have a strong research foundation and genuine grit. The question is: where do you want to go deeper? If applied research design is something that genuinely excites you, go deeper there. Study methodologies intentionally. Work on projects where you own the entire research arc—from design through analysis. Build that depth. That's how you develop real confidence in your approach.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Alternatively, your strengths in policy analysis, think-tank research, or research coordination are genuine. The direction matters less than committing to it intentionally and building depth.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
But here's what we also want to say: we're not closing the door. When roles open that fit your strengths—whether in research, policy analysis, think-tank work, or any function where your grit and integrity are load-bearing—we'd genuinely welcome your application. You're the kind of person we want to build with. Keep an eye on our careers page (www.taleemabad.com/careers). We hope you'll think of us when opportunities resonate with you.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You have real potential. We believe in you. Keep going.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Warm regards,<br/>
People and Culture Team<br/>
Taleemabad
</p>
"""

# ============================================
# CANDIDATE 4: MAHNOOR HASAN
# Subject: "You showed us real determination" or "What we saw in your persistence"
# ============================================

mahnoor_hasan_body = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Hi Mahnoor,
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Thank you for spending your time with us and engaging so openly in our conversation. We genuinely appreciated the thoughtfulness you brought to our discussion, and we want you to know that your effort and openness mattered to us.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
After careful reflection, we've decided not to move forward with your application for this particular role at this time. We want to be clear about that upfront, because clarity is important. But then we'd like to share what we actually observed about you, because we believe it's valuable feedback as you continue growing your career, and it deserves to be specific rather than generic.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">What we genuinely saw in you</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You have a real gift for showing up when things are hard. You were assigned to teach a C++ lab despite having no prior knowledge in the language—a subject entirely outside your expertise. You didn't say no. You self-studied. You built confidence. You conducted the labs. You received above 80% mid-semester feedback from students. You didn't walk away.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Your persistence shows up in your research as well. For your Masters work on AI for mental health screening, you spent five months with no viable path to data collection. Mental health data is sensitive in Pakistan. Building trust and access is genuinely difficult. Rather than abandon the research, you continued pursuing potential collaborators. Eventually you found a psychiatrist at Benazir Bhutto Hospital willing to help. You did not give up. That's the kind of determination that matters.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You also improve systems, not just work within them. You identified that students in your Data Structures lab lacked MATLAB background—the prerequisite was taught in Python. Rather than work around the gap, you proposed switching the entire course language from MATLAB to Python. You discussed with your reporting teacher, escalated to the HOD who initially resisted, and eventually got the amendment approved. Course performance improved. You don't just adapt to broken systems. You fix them.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You also speak up. At NUST, your PI assigned extra unpaid work—YouTube video editing and workshop assistance. You told him directly these were outside your job description and you would expect compensation if required. The conversation was uncomfortable and ultimately you were still made to do the work, but you raised it. That matters. You also had direct behavioral conversations with troublemaker first-semester students—spoke directly, referenced your own experience going through the same phase, and saw visible behavioral improvement by second semester.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Where we're aligned—and what we noticed</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
When we talked with you about our mission and our work, it was clear you have technical depth and capacity. You understand data science. You have genuine competence. Those things matter to us.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
But here's what we also noticed: your expertise and your passion are clearly in the health sector. Your degree is in Bioinformatics. You have significant expertise in data science and machine learning for health applications. That sector—those problems, that domain—appear more aligned with your longer-term career goals than education sector work.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
This particular role is specialized for education impact research. While you could do this work, we believe you'd find more fulfillment and genuine engagement in a role that sits at the intersection of health, data science, and impact—areas where your passion clearly lies. We'd be a better fit for each other when the role aligns with your deeper strengths and goals.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
<strong style="color:#1565C0;">Where you could go</strong>
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You have real potential in data science. The question is: where do you want to go deeper? If health tech, health data science, or health impact research genuinely excites you, go there. Build projects. Develop expertise in that domain. That's where your foundation is strongest and where you'll find the most fulfillment.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
But here's what we also want to say: we're not closing the door. When roles open that fit your expertise and passions—whether on our data team, in health tech initiatives, or any function where data science and impact intersect—we'd genuinely welcome your application. You're the kind of person we want to build with. Keep an eye on our careers page (www.taleemabad.com/careers). We hope you'll think of us when opportunities resonate with you.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
You have real potential. We believe in you. Keep going.
</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; margin:0 0 20px 0; line-height:1.75; text-align:justify;">
Warm regards,<br/>
People and Culture Team<br/>
Taleemabad
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

    print("[PILOT] Sending 4 warm bench feedback emails (REVISED FINAL)...\n")

    # Email 1: Dur E Nayab
    print("1. Dur E Nayab — Subject: Your resilience showed us something real")
    send_warm_bench_email(
        candidate_name="Dur E Nayab",
        candidate_email="durenayab349@gmail.com",
        position="Junior Research Associate",
        body_html=dur_e_nayab_body,
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    # Email 2: Daniyah Noor
    print("2. Daniyah Noor — Subject: You showed us real advocacy")
    send_warm_bench_email(
        candidate_name="Daniyah Noor",
        candidate_email="daniyahnoor@gmail.com",
        position="Junior Research Associate",
        body_html=daniyah_noor_body,
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    # Email 3: Hassan Zafar
    print("3. Hassan Zafar — Subject: Your grit as a researcher")
    send_warm_bench_email(
        candidate_name="Hassan Zafar",
        candidate_email="hassanzafar8004474@gmail.com",
        position="Junior Research Associate",
        body_html=hassan_zafar_body,
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    # Email 4: Mahnoor Hasan
    print("4. Mahnoor Hasan — Subject: You showed us real determination")
    send_warm_bench_email(
        candidate_name="Mahnoor Hasan",
        candidate_email="mahnoorhasan122@gmail.com",
        position="Junior Research Associate",
        body_html=mahnoor_hasan_body,
        pilot_mode=True,
        pilot_recipients=pilot_recipients
    )

    print("\n[OK] All 4 revised emails sent to pilot recipients for review.")
