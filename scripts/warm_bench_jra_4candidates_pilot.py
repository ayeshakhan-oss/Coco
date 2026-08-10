#!/usr/bin/env python3
"""
Warm Bench Feedback Emails — Junior Research Associate (4 candidates)
Dur E Nayab, Daniyah Noor, Hassan Zafar, Mahnoor Hasan
Pilot mode: sends to Ayesha + Jawwad only for review
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

PILOT_MODE = True
PILOT_RECIPIENTS = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]

# ====================
# EMAIL TEMPLATES (HTML)
# ====================

DUR_E_NAYAB_HTML = """
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Georgia, serif; margin: 0; padding: 0; background-color: #f5f5f5;">

<table width="100%" cellpadding="0" cellspacing="0" style="max-width: 700px; margin: 0 auto; background-color: white;">
<tr><td style="padding: 50px 60px; text-align: center;">

<!-- Logo -->
<img src="https://drive.google.com/uc?export=view&id=1jM8L0ZX6X1Hj8H9K7L2M3N4O5P6Q7R8S" alt="Taleemabad" style="height: 70px; margin-bottom: 30px;">

<!-- Small Header -->
<p style="color: #1565c0; font-size: 13px; letter-spacing: 3px; text-transform: uppercase; margin: 0 0 25px 0; font-weight: normal;">PEOPLE &amp; CULTURE • APPLICATION UPDATE</p>

<!-- Main Title -->
<h1 style="color: #1565c0; font-size: 28px; font-weight: bold; margin: 0 0 15px 0; text-align: center; line-height: 1.3;">Your Application for Junior Research Associate</h1>

<!-- Subtitle -->
<p style="color: #1565c0; font-size: 16px; margin: 0 0 30px 0; text-align: center;">Impact &amp; Policy</p>

<!-- Blue Divider -->
<hr style="border: none; border-top: 3px solid #1565c0; margin: 30px 0 40px 0; padding: 0;">

<!-- Body Content -->
<div style="font-family: Georgia, serif; font-size: 14px; line-height: 24px; color: #333333; text-align: justify;">

<p style="margin: 0 0 20px 0;">Hi Dur E Nayab,</p>

<p style="margin: 0 0 20px 0;">I wanted to reach out personally to say thank you. Over the past several weeks, we've had the privilege of getting to know you through our screening and values conversations, and I've been reflecting deeply on what you brought to those exchanges.</p>

<p style="color: #1565c0; font-weight: bold; font-size: 16px; margin: 30px 0 15px 0; text-align: left;">What We Saw in Your Values Interview</p>

<p>When you told us about leading the Sonu Kahani digital project at Amal Academy, you spoke with such clarity about something that genuinely terrifies you. Social media, video creation, public performance—these don't come naturally to you. Yet there you were, managing team conflict while your grandmother was on a deathbed and you were taking calls about video uploads from the kitchen. You didn't walk away. Instead, you made a detailed flow chart. You said it plainly: "Who to deal with how. What my responsibilities were." You channeled your discomfort into structure, and your team won second-best award. That's not just persistence. That's showing up with intention when everything inside you wanted to disappear.</p>

<p>What struck us equally was your reflection on working with Ikra at Capacity Analytics. You reviewed her Excel work quietly, identified errors, and framed corrections in a way that would pass your supervisor Ayesha's standards without drawing attention to Ikra's struggles. You told us: "Gestures should be unspoken." Years later, Ikra mentioned it to her mother. That's All for One and One for All not as a slogan, but as a practice.</p>

<p>Your mastery of Eviews through YouTube tutorials and ChatGPT while sitting with classmates showed us someone who doesn't just solve problems for themselves. You taught Stata to a junior who was drowning in her final year project. One hour of instruction on basics, commands, and how to use AI for debugging. That junior went on to succeed in her job hunt. Continuously Improve isn't about you alone getting better. It's about lifting others.</p>

<p>And when you challenged your supervisor Ayesha on process strategy during that overnight rules revision at Capacity Analytics, you didn't bulldoze. You proposed. You said: "Kya jyaada se jyaada kya ho gaya ab toh ho gaya." You know something else we heard: you regularly challenge your strict Pashtun father on family decisions. You do it softly, with a calm voice. You say a dua before entering his room because of his anger issues and the lifelong communication gap. That takes far more courage than any boardroom conversation.</p>

<p style="color: #1565c0; font-weight: bold; font-size: 12px; margin: 20px 0 10px 0; text-align: left;">Your GWC Assessment</p>

<p>Our GWC conversation confirmed what the values interview showed us: you understand our mission deeply. You're genuinely energized by the work of education and equity. You have the capacity to show up on our values daily. Across all three questions—Do you Get It? Do you Want It? Can you do it?—the answer was consistently Yes. Your interviewer noted that despite not having direct experience with student learning data, you displayed sound overall understanding, positive attitude, and real grasp of on-ground challenges within education in Pakistan.</p>

<p>This particular role didn't move forward not because you lack what it takes. It's because the specific needs of this position and the team we're building right now require a different constellation of immediate technical skills. And even as we made that decision, your interviewer flagged something important: your career plans could diverge toward think-tanks or multilateral agencies down the line, but this role would have helped you get there.</p>

<p style="color: #1565c0; font-weight: bold; font-size: 12px; margin: 20px 0 10px 0; text-align: left;">You Belong Here</p>

<p>Here's what we want you to know: we're not closing the door. In fact, we're keeping it open deliberately.</p>

<p>Your values alignment and the thoughtfulness you brought to every conversation matter to us. When roles open that fit your strengths and experience, we'd genuinely welcome your application. You're exactly the kind of person we want to build our team with. And if this isn't the right moment, the right role will come.</p>

<p>Keep an eye on our careers page at www.taleemabad.com/careers. We hope you'll think of us when opportunities resonate with you, and we'd be delighted to consider your application.</p>

<p>Thank you again for investing your energy in getting to know us. Your thoughtfulness and integrity came through in every conversation, and that matters.</p>

<p>Warm regards,<br>
People and Culture Team<br>
Taleemabad<br>
hiring@taleemabad.com | www.taleemabad.com</p>

</div>

</td></tr>
</table>

</body>
</html>
"""

DANIYAH_NOOR_HTML = """
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Georgia, serif; margin: 0; padding: 20px; background-color: #f9f9f9;">

<table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background-color: white; border: 1px solid #e0e0e0;">
<tr><td style="padding: 30px 40px; text-align: center;">

<img src="https://drive.google.com/uc?export=view&id=1jM8L0ZX6X1Hj8H9K7L2M3N4O5P6Q7R8S" alt="Taleemabad" style="height: 50px; margin-bottom: 20px;">

<p style="color: #1565c0; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; margin: 0 0 15px 0; font-weight: normal;">PEOPLE &amp; CULTURE • APPLICATION UPDATE</p>

<h1 style="color: #1565c0; font-size: 18px; font-weight: bold; margin: 0 0 8px 0; text-align: center;">Your Application for Junior Research Associate</h1>

<p style="color: #1565c0; font-size: 12px; margin: 0 0 20px 0; text-align: center;">Impact &amp; Policy</p>

<hr style="border: none; border-top: 2px solid #1565c0; margin: 20px 0; padding: 0;">

<div style="font-family: Georgia, serif; font-size: 11px; line-height: 16px; color: #333333; text-align: justify;">

<p>Hi Daniyah,</p>

<p>I wanted to reach out personally and say thank you. The time and energy you invested in getting to know us and helping us understand who you are—that matters to us, and we wanted to acknowledge it directly.</p>

<p style="color: #1565c0; font-weight: bold; font-size: 12px; margin: 20px 0 10px 0; text-align: left;">Your GWC Assessment</p>

<p>In our Get It, Want It, Can you do it conversation, something became clear immediately: you understand our mission with real depth. You're genuinely energized by our work in education. And you have the capacity to show up on our values every day. Across all three dimensions—whether you grasp what we're trying to do, whether you're excited about it, and whether you can actually deliver on it—the answer was consistently Yes.</p>

<p>Your interviewer noted your solid analytical skills and your grasp of research design and methodologies. Those are exactly the capabilities this role demands. And they also observed something else: the only drawback was that you hadn't worked specifically with student learning data before. That's not a judgment on your capability. It's simply a gap that this particular role would have required you to close from day one.</p>

<p style="color: #1565c0; font-weight: bold; font-size: 12px; margin: 20px 0 10px 0; text-align: left;">Why This Role Didn't Move Forward</p>

<p>We made the difficult decision not to move forward with this particular position not because you lack what it takes. It's because the specific timing and immediate needs of this role required someone who could hit the ground running with direct experience in student learning data. That's a constraint of the role, not a reflection of your strength.</p>

<p>But here's what matters: your alignment with our mission, your analytical rigor, and your genuine interest in the work are exactly what we need. The door isn't closed.</p>

<p style="color: #1565c0; font-weight: bold; font-size: 12px; margin: 20px 0 10px 0; text-align: left;">We're Keeping the Door Open</p>

<p>Your capability and alignment with our values matter to us. When roles open that fit your skills and experience, we'd genuinely welcome your application. You're the kind of person we want to build our team with.</p>

<p>Keep an eye on our careers page at www.taleemabad.com/careers. We hope you'll think of us when opportunities resonate with you, and we'd be delighted to consider your application. In the meantime, if you come across insights or opportunities that feel relevant to what we're doing, we'd love to hear from you.</p>

<p>Thank you again for investing your time and energy in getting to know us. That matters.</p>

<p>Warm regards,<br>
People and Culture Team<br>
Taleemabad<br>
hiring@taleemabad.com | www.taleemabad.com</p>

</div>

</td></tr>
</table>

</body>
</html>
"""

HASSAN_ZAFAR_HTML = """
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Georgia, serif; margin: 0; padding: 20px; background-color: #f9f9f9;">

<table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background-color: white; border: 1px solid #e0e0e0;">
<tr><td style="padding: 30px 40px; text-align: center;">

<img src="https://drive.google.com/uc?export=view&id=1jM8L0ZX6X1Hj8H9K7L2M3N4O5P6Q7R8S" alt="Taleemabad" style="height: 50px; margin-bottom: 20px;">

<p style="color: #1565c0; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; margin: 0 0 15px 0; font-weight: normal;">PEOPLE &amp; CULTURE • APPLICATION UPDATE</p>

<h1 style="color: #1565c0; font-size: 18px; font-weight: bold; margin: 0 0 8px 0; text-align: center;">Your Application for Junior Research Associate</h1>

<p style="color: #1565c0; font-size: 12px; margin: 0 0 20px 0; text-align: center;">Impact &amp; Policy</p>

<hr style="border: none; border-top: 2px solid #1565c0; margin: 20px 0; padding: 0;">

<div style="font-family: Georgia, serif; font-size: 11px; line-height: 16px; color: #333333; text-align: justify;">

<p>Hi Hassan,</p>

<p>I wanted to reach out personally to say thank you. Your values showed us something that matters deeply to us, and I wanted to tell you why, even though this particular role isn't moving forward.</p>

<p style="color: #1565c0; font-weight: bold; font-size: 12px; margin: 20px 0 10px 0; text-align: left;">What Your Values Showed Us</p>

<p>Your values interview revealed someone with genuine grit. You chose a rigorous masters topic on institutional economics while working simultaneously at a consultancy firm. You completed your degree in three years when your peers took four. Your research paper is still under review in a reputable Q1 journal. You didn't give up despite minimal supervisor support. That's "Don't Walk Away from Hard Things" lived out.</p>

<p>In your bachelor's field research, you collected sensitive income data in remote rural areas for a women empowerment thesis in agriculture. You built community trust to get data that respondents normally refuse. You designed indirect questioning methodology to overcome resistance. You saw a hard problem and you solved it.</p>

<p>What struck us equally was your commitment to your team. At your previous organization, your manager's sampling methodology faced pushback from colleagues. You backed her publicly, even when others called it risky. Later, when your co-authored research on remittances came out with results opposite to expectations, you faced criticism from supervisors. You stood behind your team and the methodology, which was sound. You accepted the outcome together. That's "All for One and One for All" in practice.</p>

<p>You transformed proposal writing across six iterations. You went from heavy recurring comments to zero repeating issues. You introduced infographics, citation-linked analysis, and client-relevant framing. Eventually, you started receiving interview calls from clients who had previously ignored submissions. You didn't stay stuck. You improved the craft.</p>

<p>And recently, after your father passed in January, you learned something about yourself. You dropped the habit of escalating disagreements. You learned that patience and ignoring provocation preserve more relationships than winning arguments. That's real growth. That's "Don't Hold On Too Tight" learned through loss.</p>

<p style="color: #1565c0; font-weight: bold; font-size: 12px; margin: 20px 0 10px 0; text-align: left;">This Role Isn't the Right Fit</p>

<p>Your values are clear. We saw that. And your genuine interest in what we do is evident. But in our technical assessment of this particular role, gaps emerged in how you approached the case study work—specifically in research methodology, sampling design, and research design approach. Those gaps matter significantly for this specific position.</p>

<p>This isn't about your worth or your potential. It's about the particular demands of this role at this moment. The technical foundation we need for this opening requires a different starting point than where you are now.</p>

<p style="color: #1565c0; font-weight: bold; font-size: 12px; margin: 20px 0 10px 0; text-align: left;">But Your Values Are Clear To Us</p>

<p>Here's what we want you to know: your strength in the values that matter to us—your grit, your integrity, your willingness to learn—those don't disappear because this role didn't work out. When different roles open that align with your background, we'd genuinely welcome your application. You're exactly the kind of person we want to build with.</p>

<p>Keep an eye on our careers page at www.taleemabad.com/careers. We hope you'll think of us when opportunities resonate with you, and we'd be delighted to reconsider your application for roles that might be a stronger fit.</p>

<p>Thank you for investing your energy in getting to know us. Your integrity came through in every conversation.</p>

<p>Warm regards,<br>
People and Culture Team<br>
Taleemabad<br>
hiring@taleemabad.com | www.taleemabad.com</p>

</div>

</td></tr>
</table>

</body>
</html>
"""

MAHNOOR_HASAN_HTML = """
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Georgia, serif; margin: 0; padding: 20px; background-color: #f9f9f9;">

<table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background-color: white; border: 1px solid #e0e0e0;">
<tr><td style="padding: 30px 40px; text-align: center;">

<img src="https://drive.google.com/uc?export=view&id=1jM8L0ZX6X1Hj8H9K7L2M3N4O5P6Q7R8S" alt="Taleemabad" style="height: 50px; margin-bottom: 20px;">

<p style="color: #1565c0; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; margin: 0 0 15px 0; font-weight: normal;">PEOPLE &amp; CULTURE • APPLICATION UPDATE</p>

<h1 style="color: #1565c0; font-size: 18px; font-weight: bold; margin: 0 0 8px 0; text-align: center;">Your Application for Junior Research Associate</h1>

<p style="color: #1565c0; font-size: 12px; margin: 0 0 20px 0; text-align: center;">Impact &amp; Policy</p>

<hr style="border: none; border-top: 2px solid #1565c0; margin: 20px 0; padding: 0;">

<div style="font-family: Georgia, serif; font-size: 11px; line-height: 16px; color: #333333; text-align: justify;">

<p>Hi Mahnoor,</p>

<p>I wanted to reach out personally to say thank you. Your values showed us real strength across multiple dimensions, and we wanted to acknowledge that directly, even though this particular role isn't moving forward.</p>

<p style="color: #1565c0; font-weight: bold; font-size: 12px; margin: 20px 0 10px 0; text-align: left;">What Your Values Showed Us</p>

<p>When you told us about taking on C++ lab instruction with no prior knowledge, you showed us something important. You were assigned a subject completely outside your expertise. Instead of claiming you couldn't do it, you self-studied. You built confidence. You conducted labs. You received above 80 percent mid-semester feedback from students. That's "Don't Walk Away from Hard Things" in action.</p>

<p>Your masters research on AI for mental health screening revealed the same grit. For five months, you had no data collection path. Mental health data in Pakistan carries stigma. Access is difficult. Normal avenues don't work. You didn't abandon the research. You continued pursuing potential collaborators. Eventually you found a psychiatrist at Benazir Bhutto Hospital willing to partner with you. You persisted through the hard thing.</p>

<p>What struck us equally was your willingness to challenge upward. At your NUST role, your principal investigator assigned extra unpaid work: YouTube video editing and workshop assistance. You told them directly these tasks fell outside your job description and you'd expect compensation if required to do them. The conversation was uncomfortable. The work happened anyway. But you raised it. That's "Have Courageous Conversations" even when the outcome isn't what you hoped for.</p>

<p>You identified that students in your Data Structures lab lacked MATLAB background because prerequisites were taught in Python. You proposed switching the entire course language from MATLAB to Python. You discussed it with your reporting teacher. You escalated to the Head of Department who initially resisted. You got the amendment approved. Course performance improved. You didn't accept "that's how it's always been done."</p>

<p>And you demonstrated real self-awareness about your perfectionism. You told us: "I like to do everything on my own. But I have learned that when you are working in a team, you have to keep an open mind." That's genuine reflection. That's "Don't Hold On Too Tight" practiced deliberately.</p>

<p style="color: #1565c0; font-weight: bold; font-size: 12px; margin: 20px 0 10px 0; text-align: left;">Why This Role Didn't Move Forward</p>

<p>Your interviewer noted something important: you are an excellent data scientist with significant technical competence. Your expertise is strong, and the work you've done speaks for itself. But your career trajectory and your deepest expertise lie in the health sector. Your degree is in bioinformatics. Your passion and track record are in health data and machine learning.</p>

<p>This position sits in education sector work. And while you'd bring real strength to it, your long-term career goals diverge toward health and that domain. We recognized that asking you to commit to education when your heart and expertise point elsewhere wouldn't serve either of us well.</p>

<p style="color: #1565c0; font-weight: bold; font-size: 12px; margin: 20px 0 10px 0; text-align: left;">But Your Values Are Clear To Us</p>

<p>Here's what we want you to know: your strength in the values that matter to us—your grit, your willingness to challenge the status quo, your persistence through hard things—those don't disappear. And if future opportunities open at Taleemabad that align with your expertise and career goals, we'd genuinely welcome your application.</p>

<p>Keep an eye on our careers page at www.taleemabad.com/careers. We hope you'll think of us when opportunities resonate with you, and we'd be delighted to reconsider your application for roles that might be a stronger fit for your trajectory.</p>

<p>Thank you for investing your energy in getting to know us. Your thoughtfulness and integrity came through in every conversation.</p>

<p>Warm regards,<br>
People and Culture Team<br>
Taleemabad<br>
hiring@taleemabad.com | www.taleemabad.com</p>

</div>

</td></tr>
</table>

</body>
</html>
"""

# ====================
# SEND FUNCTION
# ====================

def send_email(to, subject, html_body):
    """Send HTML email via SMTP"""
    msg = MIMEMultipart('alternative')
    msg['From'] = EMAIL_USER
    msg['To'] = ', '.join(to) if isinstance(to, list) else to
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

# ====================
# MAIN
# ====================

if __name__ == "__main__":
    candidates = [
        {
            "name": "Dur E Nayab",
            "candidate_email": "durenayab349@gmail.com",
            "html": DUR_E_NAYAB_HTML
        },
        {
            "name": "Daniyah Noor",
            "candidate_email": "daniyahnoor@gmail.com",
            "html": DANIYAH_NOOR_HTML
        },
        {
            "name": "Hassan Zafar",
            "candidate_email": "hassanzafar8004474@gmail.com",
            "html": HASSAN_ZAFAR_HTML
        },
        {
            "name": "Mahnoor Hasan",
            "candidate_email": "mahnoorhasan122@gmail.com",
            "html": MAHNOOR_HASAN_HTML
        }
    ]

    subject = "Your Application for Junior Research Associate"

    for candidate in candidates:
        # Pilot: send to Ayesha + Jawwad
        if PILOT_MODE:
            recipients = PILOT_RECIPIENTS
            print(f"[PILOT] {candidate['name']} -> {recipients}")
        else:
            recipients = [candidate['candidate_email']]
            print(f"[LIVE] {candidate['name']} → {recipient['candidate_email']}")

        success = send_email(recipients, subject, candidate['html'])

        if success:
            print(f"[OK] {candidate['name']} email sent successfully")
        else:
            print(f"[FAIL] {candidate['name']} email FAILED")

    print("\n=== All 4 emails sent (PILOT MODE to Ayesha + Jawwad) ===")
