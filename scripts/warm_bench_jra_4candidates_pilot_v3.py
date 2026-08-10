#!/usr/bin/env python3
"""
Warm Bench Feedback Emails — Junior Research Associate (4 candidates)
Dur E Nayab, Daniyah Noor, Hassan Zafar, Mahnoor Hasan
Pilot mode: sends to Ayesha + Jawwad only for review
REDESIGNED: Proper sizing, spacing, readable format + logo via Content ID
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

PILOT_MODE = True
PILOT_RECIPIENTS = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]

def create_email_html(candidate_name, opening_text, section1_title, section1_content, section2_title, section2_content, section3_title, section3_content, section4_title, section4_content):
    """Generate properly formatted warm bench email HTML"""
    return f"""
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Georgia, serif; margin: 0; padding: 0; background-color: #f5f5f5;">

<table width="100%" cellpadding="0" cellspacing="0" style="max-width: 700px; margin: 0 auto; background-color: white;">
<tr><td style="padding: 50px 60px;">

<!-- Logo -->
<div style="text-align: center; margin-bottom: 35px;">
  <img src="cid:logo_taleemabad" alt="Taleemabad" style="height: 75px; display: block;">
</div>

<!-- Small Header -->
<p style="color: #1565c0; font-size: 13px; letter-spacing: 3px; text-transform: uppercase; margin: 0 0 25px 0; font-weight: normal; text-align: center;">PEOPLE &amp; CULTURE • APPLICATION UPDATE</p>

<!-- Main Title -->
<h1 style="color: #1565c0; font-size: 28px; font-weight: bold; margin: 0 0 15px 0; text-align: center; line-height: 1.4;">Your Application for Junior Research Associate</h1>

<!-- Subtitle -->
<p style="color: #1565c0; font-size: 16px; margin: 0 0 30px 0; text-align: center;">Impact &amp; Policy</p>

<!-- Blue Divider -->
<div style="height: 3px; background-color: #1565c0; margin: 30px 0 40px 0;"></div>

<!-- Body Content -->
<div style="font-family: Georgia, serif; font-size: 14px; line-height: 26px; color: #333333;">

<p style="margin: 0 0 20px 0;">{opening_text}</p>

<h2 style="color: #1565c0; font-weight: bold; font-size: 16px; margin: 35px 0 15px 0; border: none; padding: 0;">{section1_title}</h2>
{section1_content}

<h2 style="color: #1565c0; font-weight: bold; font-size: 16px; margin: 35px 0 15px 0; border: none; padding: 0;">{section2_title}</h2>
{section2_content}

<h2 style="color: #1565c0; font-weight: bold; font-size: 16px; margin: 35px 0 15px 0; border: none; padding: 0;">{section3_title}</h2>
{section3_content}

<h2 style="color: #1565c0; font-weight: bold; font-size: 16px; margin: 35px 0 15px 0; border: none; padding: 0;">{section4_title}</h2>
{section4_content}

<p style="margin: 35px 0 0 0;">Warm regards,<br>
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
# DUR E NAYAB
# ====================

DUR_OPENING = "Hi Dur E Nayab,<br><br>I wanted to reach out personally to say thank you. Over the past several weeks, we've had the privilege of getting to know you through our screening and values conversations, and I've been reflecting deeply on what you brought to those exchanges."

DUR_S1_TITLE = "What We Saw in Your Values Interview"
DUR_S1 = """<p style="margin: 0 0 15px 0; text-align: justify;">When you told us about leading the Sonu Kahani digital project at Amal Academy, you spoke with such clarity about something that genuinely terrifies you. Social media, video creation, public performance—these don't come naturally to you. Yet there you were, managing team conflict while your grandmother was on a deathbed and you were taking calls about video uploads from the kitchen. You didn't walk away. Instead, you made a detailed flow chart. You said it plainly: "Who to deal with how. What my responsibilities were." You channeled your discomfort into structure, and your team won second-best award. That's not just persistence. That's showing up with intention when everything inside you wanted to disappear.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">What struck us equally was your reflection on working with Ikra at Capacity Analytics. You reviewed her Excel work quietly, identified errors, and framed corrections in a way that would pass your supervisor Ayesha's standards without drawing attention to Ikra's struggles. You told us: "Gestures should be unspoken." Years later, Ikra mentioned it to her mother. That's All for One and One for All not as a slogan, but as a practice.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Your mastery of Eviews through YouTube tutorials and ChatGPT while sitting with classmates showed us someone who doesn't just solve problems for themselves. You taught Stata to a junior who was drowning in her final year project. One hour of instruction on basics, commands, and how to use AI for debugging. That junior went on to succeed in her job hunt. Continuously Improve isn't about you alone getting better. It's about lifting others.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">And when you challenged your supervisor Ayesha on process strategy during that overnight rules revision at Capacity Analytics, you didn't bulldoze. You proposed. You said: "Kya jyaada se jyaada kya ho gaya ab toh ho gaya." You know something else we heard: you regularly challenge your strict Pashtun father on family decisions. You do it softly, with a calm voice. You say a dua before entering his room because of his anger issues and the lifelong communication gap. That takes far more courage than any boardroom conversation.</p>"""

DUR_S2_TITLE = "Your GWC Assessment"
DUR_S2 = """<p style="margin: 0 0 15px 0; text-align: justify;">Our GWC conversation confirmed what the values interview showed us: you understand our mission deeply. You're genuinely energized by the work of education and equity. You have the capacity to show up on our values daily. Across all three questions—Do you Get It? Do you Want It? Can you do it?—the answer was consistently Yes. Your interviewer noted that despite not having direct experience with student learning data, you displayed sound overall understanding, positive attitude, and real grasp of on-ground challenges within education in Pakistan.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">This particular role didn't move forward not because you lack what it takes. It's because the specific needs of this position and the team we're building right now require a different constellation of immediate technical skills. And even as we made that decision, your interviewer flagged something important: your career plans could diverge toward think-tanks or multilateral agencies down the line, but this role would have helped you get there.</p>"""

DUR_S3_TITLE = "You Belong Here"
DUR_S3 = """<p style="margin: 0 0 15px 0; text-align: justify;">Here's what we want you to know: we're not closing the door. In fact, we're keeping it open deliberately.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Your values alignment and the thoughtfulness you brought to every conversation matter to us. When roles open that fit your strengths and experience, we'd genuinely welcome your application. You're exactly the kind of person we want to build our team with. And if this isn't the right moment, the right role will come.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Keep an eye on our careers page at www.taleemabad.com/careers. We hope you'll think of us when opportunities resonate with you, and we'd be delighted to consider your application.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Thank you again for investing your energy in getting to know us. Your thoughtfulness and integrity came through in every conversation, and that matters.</p>"""

DUR_S4_TITLE = " "
DUR_S4 = ""

DUR_HTML = create_email_html("Dur E Nayab", DUR_OPENING, DUR_S1_TITLE, DUR_S1, DUR_S2_TITLE, DUR_S2, DUR_S3_TITLE, DUR_S3, DUR_S4_TITLE, DUR_S4)

# ====================
# DANIYAH NOOR
# ====================

DANIYAH_OPENING = "Hi Daniyah,<br><br>I wanted to reach out personally and say thank you. The time and energy you invested in getting to know us and helping us understand who you are—that matters to us, and we wanted to acknowledge it directly."

DANIYAH_S1_TITLE = "Your GWC Assessment"
DANIYAH_S1 = """<p style="margin: 0 0 15px 0; text-align: justify;">In our Get It, Want It, Can you do it conversation, something became clear immediately: you understand our mission with real depth. You're genuinely energized by our work in education. And you have the capacity to show up on our values every day. Across all three dimensions—whether you grasp what we're trying to do, whether you're excited about it, and whether you can actually deliver on it—the answer was consistently Yes.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Your interviewer noted your solid analytical skills and your grasp of research design and methodologies. Those are exactly the capabilities this role demands. And they also observed something else: the only drawback was that you hadn't worked specifically with student learning data before. That's not a judgment on your capability. It's simply a gap that this particular role would have required you to close from day one.</p>"""

DANIYAH_S2_TITLE = "Why This Role Didn't Move Forward"
DANIYAH_S2 = """<p style="margin: 0 0 15px 0; text-align: justify;">We made the difficult decision not to move forward with this particular position not because you lack what it takes. It's because the specific timing and immediate needs of this role required someone who could hit the ground running with direct experience in student learning data. That's a constraint of the role, not a reflection of your strength.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">But here's what matters: your alignment with our mission, your analytical rigor, and your genuine interest in the work are exactly what we need. The door isn't closed.</p>"""

DANIYAH_S3_TITLE = "We're Keeping the Door Open"
DANIYAH_S3 = """<p style="margin: 0 0 15px 0; text-align: justify;">Your capability and alignment with our values matter to us. When roles open that fit your skills and experience, we'd genuinely welcome your application. You're the kind of person we want to build our team with.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Keep an eye on our careers page at www.taleemabad.com/careers. We hope you'll think of us when opportunities resonate with you, and we'd be delighted to consider your application. In the meantime, if you come across insights or opportunities that feel relevant to what we're doing, we'd love to hear from you.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Thank you again for investing your time and energy in getting to know us. That matters.</p>"""

DANIYAH_S4_TITLE = " "
DANIYAH_S4 = ""

DANIYAH_HTML = create_email_html("Daniyah Noor", DANIYAH_OPENING, DANIYAH_S1_TITLE, DANIYAH_S1, DANIYAH_S2_TITLE, DANIYAH_S2, DANIYAH_S3_TITLE, DANIYAH_S3, DANIYAH_S4_TITLE, DANIYAH_S4)

# ====================
# HASSAN ZAFAR
# ====================

HASSAN_OPENING = "Hi Hassan,<br><br>I wanted to reach out personally to say thank you. Your values showed us something that matters deeply to us, and I wanted to tell you why, even though this particular role isn't moving forward."

HASSAN_S1_TITLE = "What Your Values Showed Us"
HASSAN_S1 = """<p style="margin: 0 0 15px 0; text-align: justify;">Your values interview revealed someone with genuine grit. You chose a rigorous masters topic on institutional economics while working simultaneously at a consultancy firm. You completed your degree in three years when your peers took four. Your research paper is still under review in a reputable Q1 journal. You didn't give up despite minimal supervisor support. That's "Don't Walk Away from Hard Things" lived out.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">In your bachelor's field research, you collected sensitive income data in remote rural areas for a women empowerment thesis in agriculture. You built community trust to get data that respondents normally refuse. You designed indirect questioning methodology to overcome resistance. You saw a hard problem and you solved it.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">What struck us equally was your commitment to your team. At your previous organization, your manager's sampling methodology faced pushback from colleagues. You backed her publicly, even when others called it risky. Later, when your co-authored research on remittances came out with results opposite to expectations, you faced criticism from supervisors. You stood behind your team and the methodology, which was sound. You accepted the outcome together. That's "All for One and One for All" in practice.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">You transformed proposal writing across six iterations. You went from heavy recurring comments to zero repeating issues. You introduced infographics, citation-linked analysis, and client-relevant framing. Eventually, you started receiving interview calls from clients who had previously ignored submissions. You didn't stay stuck. You improved the craft.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">And recently, after your father passed in January, you learned something about yourself. You dropped the habit of escalating disagreements. You learned that patience and ignoring provocation preserve more relationships than winning arguments. That's real growth. That's "Don't Hold On Too Tight" learned through loss.</p>"""

HASSAN_S2_TITLE = "This Role Isn't the Right Fit"
HASSAN_S2 = """<p style="margin: 0 0 15px 0; text-align: justify;">Your values are clear. We saw that. And your genuine interest in what we do is evident. But in our technical assessment of this particular role, gaps emerged in how you approached the case study work—specifically in research methodology, sampling design, and research design approach. Those gaps matter significantly for this specific position.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">This isn't about your worth or your potential. It's about the particular demands of this role at this moment. The technical foundation we need for this opening requires a different starting point than where you are now.</p>"""

HASSAN_S3_TITLE = "But Your Values Are Clear To Us"
HASSAN_S3 = """<p style="margin: 0 0 15px 0; text-align: justify;">Here's what we want you to know: your strength in the values that matter to us—your grit, your integrity, your willingness to learn—those don't disappear because this role didn't work out. When different roles open that align with your background, we'd genuinely welcome your application. You're exactly the kind of person we want to build with.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Keep an eye on our careers page at www.taleemabad.com/careers. We hope you'll think of us when opportunities resonate with you, and we'd be delighted to reconsider your application for roles that might be a stronger fit.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Thank you for investing your energy in getting to know us. Your integrity came through in every conversation.</p>"""

HASSAN_S4_TITLE = " "
HASSAN_S4 = ""

HASSAN_HTML = create_email_html("Hassan Zafar", HASSAN_OPENING, HASSAN_S1_TITLE, HASSAN_S1, HASSAN_S2_TITLE, HASSAN_S2, HASSAN_S3_TITLE, HASSAN_S3, HASSAN_S4_TITLE, HASSAN_S4)

# ====================
# MAHNOOR HASAN
# ====================

MAHNOOR_OPENING = "Hi Mahnoor,<br><br>I wanted to reach out personally to say thank you. Your values showed us real strength across multiple dimensions, and we wanted to acknowledge that directly, even though this particular role isn't moving forward."

MAHNOOR_S1_TITLE = "What Your Values Showed Us"
MAHNOOR_S1 = """<p style="margin: 0 0 15px 0; text-align: justify;">When you told us about taking on C++ lab instruction with no prior knowledge, you showed us something important. You were assigned a subject completely outside your expertise. Instead of claiming you couldn't do it, you self-studied. You built confidence. You conducted labs. You received above 80 percent mid-semester feedback from students. That's "Don't Walk Away from Hard Things" in action.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Your masters research on AI for mental health screening revealed the same grit. For five months, you had no data collection path. Mental health data in Pakistan carries stigma. Access is difficult. Normal avenues don't work. You didn't abandon the research. You continued pursuing potential collaborators. Eventually you found a psychiatrist at Benazir Bhutto Hospital willing to partner with you. You persisted through the hard thing.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">What struck us equally was your willingness to challenge upward. At your NUST role, your principal investigator assigned extra unpaid work: YouTube video editing and workshop assistance. You told them directly these tasks fell outside your job description and you'd expect compensation if required to do them. The conversation was uncomfortable. The work happened anyway. But you raised it. That's "Have Courageous Conversations" even when the outcome isn't what you hoped for.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">You identified that students in your Data Structures lab lacked MATLAB background because prerequisites were taught in Python. You proposed switching the entire course language from MATLAB to Python. You discussed it with your reporting teacher. You escalated to the Head of Department who initially resisted. You got the amendment approved. Course performance improved. You didn't accept "that's how it's always been done."</p>

<p style="margin: 0 0 15px 0; text-align: justify;">And you demonstrated real self-awareness about your perfectionism. You told us: "I like to do everything on my own. But I have learned that when you are working in a team, you have to keep an open mind." That's genuine reflection. That's "Don't Hold On Too Tight" practiced deliberately.</p>"""

MAHNOOR_S2_TITLE = "Why This Role Didn't Move Forward"
MAHNOOR_S2 = """<p style="margin: 0 0 15px 0; text-align: justify;">Your interviewer noted something important: you are an excellent data scientist with significant technical competence. Your expertise is strong, and the work you've done speaks for itself. But your career trajectory and your deepest expertise lie in the health sector. Your degree is in bioinformatics. Your passion and track record are in health data and machine learning.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">This position sits in education sector work. And while you'd bring real strength to it, your long-term career goals diverge toward health and that domain. We recognized that asking you to commit to education when your heart and expertise point elsewhere wouldn't serve either of us well.</p>"""

MAHNOOR_S3_TITLE = "But Your Values Are Clear To Us"
MAHNOOR_S3 = """<p style="margin: 0 0 15px 0; text-align: justify;">Here's what we want you to know: your strength in the values that matter to us—your grit, your willingness to challenge the status quo, your persistence through hard things—those don't disappear. And if future opportunities open at Taleemabad that align with your expertise and career goals, we'd genuinely welcome your application.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Keep an eye on our careers page at www.taleemabad.com/careers. We hope you'll think of us when opportunities resonate with you, and we'd be delighted to reconsider your application for roles that might be a stronger fit for your trajectory.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Thank you for investing your energy in getting to know us. Your thoughtfulness and integrity came through in every conversation.</p>"""

MAHNOOR_S4_TITLE = " "
MAHNOOR_S4 = ""

MAHNOOR_HTML = create_email_html("Mahnoor Hasan", MAHNOOR_OPENING, MAHNOOR_S1_TITLE, MAHNOOR_S1, MAHNOOR_S2_TITLE, MAHNOOR_S2, MAHNOOR_S3_TITLE, MAHNOOR_S3, MAHNOOR_S4_TITLE, MAHNOOR_S4)

# ====================
# SEND FUNCTION
# ====================

def send_email(to, subject, html_body):
    """Send HTML email via SMTP with embedded logo image"""
    msg = MIMEMultipart('related')
    msg['From'] = EMAIL_USER
    msg['To'] = ', '.join(to) if isinstance(to, list) else to
    msg['Subject'] = subject

    # Attach HTML
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(html_body, 'html', 'utf-8'))

    # Attach logo image with Content ID
    logo_path = r"c:\Agent Coco\assets\logo_taleemabad.png"
    try:
        with open(logo_path, 'rb') as f:
            logo_image = MIMEImage(f.read(), name='logo_taleemabad.png')
            logo_image.add_header('Content-ID', '<logo_taleemabad>')
            logo_image.add_header('Content-Disposition', 'inline', filename='logo_taleemabad.png')
            msg.attach(logo_image)
    except Exception as e:
        print(f"ERROR: Could not attach logo: {e}")
        return False

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
            "html": DUR_HTML
        },
        {
            "name": "Daniyah Noor",
            "candidate_email": "daniyahnoor@gmail.com",
            "html": DANIYAH_HTML
        },
        {
            "name": "Hassan Zafar",
            "candidate_email": "hassanzafar8004474@gmail.com",
            "html": HASSAN_HTML
        },
        {
            "name": "Mahnoor Hasan",
            "candidate_email": "mahnoorhasan122@gmail.com",
            "html": MAHNOOR_HTML
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
            print(f"[LIVE] {candidate['name']} -> {candidate['candidate_email']}")

        success = send_email(recipients, subject, candidate['html'])

        if success:
            print(f"[OK] {candidate['name']} email sent successfully")
        else:
            print(f"[FAIL] {candidate['name']} email FAILED")

    print("\n=== All 4 emails sent (PILOT MODE to Ayesha + Jawwad) ===")
