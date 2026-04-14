"""
Send GWC Stage Rejection Emails - PILOT to Ayesha + Jawwad
Hackathon 2026 Position
"""
import os, sys, smtplib
sys.path.insert(0, "c:/Agent Coco")

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scripts.utils.safe_send import safe_sendmail

load_dotenv(dotenv_path="c:/Agent Coco/.env")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

PILOT_RECIPIENTS = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]

# Candidate data
candidates = {
    "Moaz Nadeem": {
        "email": "muazndm128@gmail.com",
        "app_id": 1167,
        "type": "perfect_pass"
    },
    "Alishba Ramzan": {
        "email": "alishbaramzan1@gmail.com",
        "app_id": 1152,
        "type": "perfect_pass"
    },
    "Umair Solangi": {
        "email": "bscs2112203@szabist.pk",
        "app_id": 1149,
        "type": "low_want"
    },
    "Ali Jawad": {
        "email": "ali.jawad6204@gmail.com",
        "app_id": 1114,
        "type": "mixed"
    },
    "Maryam Rafaqat": {
        "email": "maryamrafaqat88@gmail.com",
        "app_id": 1174,
        "type": "low_understanding"
    },
    "Sultan Muhammad Hamad Sheharyar": {
        "email": "pirzadahammadzakori@gmail.com",
        "app_id": 1117,
        "type": "significant_gaps"
    }
}

# Email bodies by type (simplified for pilot)
email_bodies = {
    "perfect_pass": """
Dear {{first_name}},

Thank you for investing your time and energy into the Hackathon 2026 position. From your initial application through the technical assessment and GWC evaluation, you've been thoughtful, engaged, and genuine.

**What We Liked Most About You**

Your performance across our GWC assessment was exceptional. You demonstrated a crystal-clear understanding of the role, genuine enthusiasm for this space, and strong capacity to execute. These three elements—getting the role, wanting it genuinely, and being able to deliver at a high level—are what we look for, and you showed us all three.

**Where We Found Ourselves Sitting With Questions**

Here's where we want to be honest: this isn't about gaps in your readiness. The challenge we're sitting with is about timing and bandwidth on our end. We're at a moment where our team structure is still settling, and while your skills and enthusiasm are exactly what we'd want, we're concerned we couldn't give you the hands-on mentorship you'd deserve during your first months.

It's an honest assessment of where we are as a team. We believe you're built for this kind of work, and we'd rather be transparent about our constraints than bring you in and under-invest.

**What We Think You Should Do Next**

Keep doing the work that excites you. In three to six months, as we stabilize our team, we'd genuinely love to revisit this conversation. We'd like to keep the door open.

Warm regards,
People and Culture Team
Taleemabad
hiring@taleemabad.com | www.taleemabad.com
""",

    "low_want": """
Dear {{first_name}},

Thank you for engaging thoughtfully with the Hackathon 2026 opportunity. We genuinely appreciated your willingness to step into a detailed assessment process.

**What We Liked Most About You**

Your technical foundation is solid, and we saw that in how you approached the assessment. Beyond the technical piece, we appreciated your openness and the maturity in how you showed up. You clearly care about building skills and taking on meaningful work.

**Where We Found Ourselves Sitting With Questions**

While you can do this role technically, the alignment between what you want from your next career move and what this position offers wasn't quite there. Your responses on the "Want It" dimension suggested some hesitation about whether this particular space is where you want to invest your energy right now.

The best matches happen when both sides are genuinely excited. We respect your instincts about what kind of work lights you up, and we think there's probably a better fit out there for you.

**What We Think You Should Do Next**

Take time to clarify what you're genuinely excited about. What problems do you want to solve? What kind of impact do you want to create? Seek opportunities that align with that clarity.

Warm regards,
People and Culture Team
Taleemabad
hiring@taleemabad.com | www.taleemabad.com
""",

    "mixed": """
Dear {{first_name}},

Thank you for the genuine effort you put into the Hackathon 2026 assessment. We appreciate that kind of commitment to a process.

**What We Liked Most About You**

You brought real thoughtfulness to understanding what this role entails. We saw solid technical capabilities come through, and we appreciated your flexibility and openness. That growth mindset is a genuine strength.

**Where We Found Ourselves Sitting With Questions**

The GWC assessment revealed that while you have real capability, there's still ground to cover across all three dimensions we evaluated: understanding the role deeply, having genuine enthusiasm for it, and being fully confident in your ability to deliver.

This is feedback about readiness in this moment, not a statement about your potential. With time and intentional growth, you could absolutely get there.

**What We Think You Should Do Next**

Seek opportunities where you can deepen your understanding of technical-strategic integration. Work on projects where you can see how product, user needs, and engineering come together. Once you've built that foundation, we'd be happy to have another conversation.

Warm regards,
People and Culture Team
Taleemabad
hiring@taleemabad.com | www.taleemabad.com
""",

    "low_understanding": """
Dear {{first_name}},

Thank you for your genuine interest in the Hackathon 2026 role and for taking the time to engage with our assessment process.

**What We Liked Most About You**

You brought real enthusiasm to the conversations. We also saw your capacity to learn and adapt. Throughout the assessment, you demonstrated flexibility and willingness to think through problems from different angles. We appreciated your intellectual honesty.

**Where We Found Ourselves Sitting With Questions**

The GWC assessment shows that the full complexity of this role—the way it weaves technical execution with strategic thinking and organizational impact—wasn't quite crystallizing for you yet. This isn't about raw intelligence. It's about domain clarity needed for this position.

This role would require us to invest significantly in helping you develop that understanding, and we're not in a position to do that right now.

**What We Think You Should Do Next**

Spend intentional time deepening your understanding of how technical work connects to broader strategy and impact. Work on projects where you can see that connection. Read widely. Find mentors who can help you understand the full picture.

Warm regards,
People and Culture Team
Taleemabad
hiring@taleemabad.com | www.taleemabad.com
""",

    "significant_gaps": """
Dear {{first_name}},

Thank you for your time and effort in engaging with the Hackathon 2026 assessment. We appreciate your commitment to exploring this opportunity.

**What We Liked Most About You**

You showed genuine willingness to step into a challenging assessment. We appreciated your engagement throughout the conversations and that you brought your authentic self to the process.

**Where We Found Ourselves Sitting With Questions**

The GWC assessment revealed gaps across all three dimensions we evaluate. This particular role is a specialized fit requiring strong understanding, genuine passion, and execution capability. There are gaps on all three fronts that would make it difficult to succeed in this position.

This feedback is specific to this role at this time. It doesn't speak to your broader potential, but for this particular opportunity, the alignment and readiness aren't there yet.

**What We Think You Should Do Next**

Take time to explore what kind of work genuinely excites you. Seek opportunities that feel more naturally aligned with where you are right now. Build deeper understanding and confidence over time.

Warm regards,
People and Culture Team
Taleemabad
hiring@taleemabad.com | www.taleemabad.com
"""
}

print("\n=== SENDING GWC REJECTION EMAILS - PILOT ===\n")

try:
    # Connect to Gmail SMTP
    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.starttls()
    s.login(EMAIL_USER, EMAIL_PASSWORD)
    print("[OK] Connected to Gmail SMTP\n")

    sent_count = 0

    for name, data in candidates.items():
        first_name = name.split()[0]
        email_type = data['type']
        body_template = email_bodies[email_type]
        body = body_template.replace("{{first_name}}", first_name)

        subject = f"[PILOT - {email_type}] We're reflecting on your Hackathon 2026 application — {name}"

        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = ", ".join(PILOT_RECIPIENTS)

        msg.attach(MIMEText(body, "plain"))

        # Send via safe_sendmail
        try:
            safe_sendmail(
                s,
                EMAIL_USER,
                PILOT_RECIPIENTS,
                msg.as_string(),
                context=f"GWC_rejection_pilot_{name.replace(' ', '_')}"
            )
            sent_count += 1
            print(f"[OK] Sent pilot for {name}")
        except Exception as e:
            print(f"[ERROR] Failed to send pilot for {name}: {e}")

    s.quit()

    print(f"\n" + "="*60)
    print(f"Sent {sent_count} pilot emails")
    print(f"PILOT RECIPIENTS: {', '.join(PILOT_RECIPIENTS)}")
    print(f"="*60)

except Exception as e:
    print(f"[FAILED] Could not connect to SMTP: {e}")
    sys.exit(1)
