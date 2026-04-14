"""
Send GWC Stage Rejection Emails - PILOT to Ayesha + Jawwad
Hackathon 2026 Position
"""
import sys
sys.path.insert(0, "c:/Agent Coco")

from scripts.utils.safe_send import safe_sendmail
from scripts.utils.feedback_widget import feedback_widget
from scripts.utils.audit_log import log_gmail_read
import json

PILOT_MODE = True
PILOT_RECIPIENTS = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]

# Candidate data
candidates = {
    "Moaz Nadeem": {
        "email": "muazndm128@gmail.com",
        "app_id": 1167,
        "getIt": 3, "wantIt": 3, "capacity": 3,
        "type": "perfect_pass"
    },
    "Alishba Ramzan": {
        "email": "alishbaramzan1@gmail.com",
        "app_id": 1152,
        "getIt": 3, "wantIt": 3, "capacity": 3,
        "type": "perfect_pass"
    },
    "Umair Solangi": {
        "email": "bscs2112203@szabist.pk",
        "app_id": 1149,
        "getIt": 2, "wantIt": 1, "capacity": 3,
        "type": "low_want"
    },
    "Ali Jawad": {
        "email": "ali.jawad6204@gmail.com",
        "app_id": 1114,
        "getIt": 2, "wantIt": 2, "capacity": 2,
        "type": "mixed"
    },
    "Maryam Rafaqat": {
        "email": "maryamrafaqat88@gmail.com",
        "app_id": 1174,
        "getIt": 1, "wantIt": 1, "capacity": 3,
        "type": "low_understanding"
    },
    "Sultan Muhammad Hamad Sheharyar": {
        "email": "pirzadahammadzakori@gmail.com",
        "app_id": 1117,
        "getIt": 0, "wantIt": 1, "capacity": 1,
        "type": "significant_gaps"
    }
}

def generate_perfect_pass_email(full_name, app_id):
    """Email for candidates with perfect 3/3 GWC scores"""
    first_name = full_name.split()[0]
    widget_html = feedback_widget(full_name, "Hackathon 2026", app_id, "GWC Stage Feedback")
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Georgia, serif; background-color: #f0f4f0; margin: 0; padding: 20px; }}
            .container {{ max-width: 700px; margin: 0 auto; background-color: white; border-left: 5px solid #1565c0; padding: 40px; }}
            h2 {{ color: #1565c0; font-size: 22px; margin: 25px 0 15px 0; line-height: 1.4; }}
            .subheading {{ color: #2e7d32; font-size: 15px; font-weight: bold; margin: 18px 0 8px 0; }}
            p {{ font-size: 15px; line-height: 1.8; color: #333; text-align: justify; margin: 0 0 12px 0; }}
            .section {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <p>Dear {first_name},</p>

            <p>Thank you for investing your time and energy into the Hackathon 2026 position. From your initial application through the technical assessment and GWC evaluation, you've been thoughtful, engaged, and genuine. We want to share what we saw in you during this process—and also what we're sitting with as we move forward.</p>

            <h2>What We Liked Most About You</h2>
            <div class="section">
                <p>Your performance across our GWC assessment was exceptional. You demonstrated a crystal-clear understanding of the role—what it demands, what success looks like, and why it matters within our broader mission. That clarity didn't come across as theoretical; it felt grounded in real thinking about the work and the impact.</p>

                <p>Beyond that understanding, your genuine enthusiasm for this space shone through in every conversation. You articulated not just what you could do, but why you want to do it. That alignment between capability and motivation is rare, and it's something we deeply value. Your commitment to the kind of work we're building felt authentic.</p>

                <p>Finally, your capacity to execute across multiple dimensions came through clearly. You showed technical depth, strategic thinking, and the ability to hold complexity without oversimplifying. We could envision you moving quickly and independently in this role, solving problems as they emerge, and growing into greater responsibility over time.</p>

                <p>These three elements—getting the role, wanting it genuinely, and being able to deliver at a high level—are what we look for. You showed us all three.</p>
            </div>

            <h2>Where We Found Ourselves Sitting With Questions</h2>
            <div class="section">
                <p>Here's where we want to be honest: this isn't about gaps in your readiness. You've demonstrated that you're prepared for this role. The challenge we're sitting with is about timing and bandwidth on our end, not about your capability.</p>

                <p>We're at a moment where our team structure is still settling. While your skills and enthusiasm are exactly what we'd want in an ideal scenario, we're also aware that bringing someone into a role requires us to have the infrastructure and attention to support their growth. Right now, we're concerned we couldn't give you the hands-on mentorship and clarity you'd deserve during your first months.</p>

                <p>It's not a reflection of you. It's an honest assessment of where we are as a team. We believe you're built for this kind of impact work, and we'd rather be transparent about our constraints than bring you in and under-invest in making it work.</p>
            </div>

            <h2>What We Think You Should Do Next</h2>
            <div class="section">
                <p>Here's what we'd encourage: keep doing the work that excites you. Whether that's deepening your technical skills, exploring new problem spaces, or building a portfolio of projects you're proud of—invest in becoming an even stronger version of yourself.</p>

                <p>In three to six months, as we stabilize our team and create more breathing room, we'd genuinely love to revisit this conversation. We'd like to keep the door open. If you're interested in staying loosely connected, reach out in a few months or whenever you're open to re-exploring.</p>

                <p>We believe you're going places, and we'd like to be part of that story if the timing and fit align down the road.</p>
            </div>

            {widget_html}

            <p style="margin-top: 30px; color: #666; font-size: 13px; line-height: 1.6;">
                Warm regards,<br>
                People and Culture Team<br>
                Taleemabad<br>
                hiring@taleemabad.com | www.taleemabad.com<br>
                <br>
                Sent on behalf of Talent Acquisition Team by Coco
            </p>
        </div>
    </body>
    </html>
    """

def generate_low_want_email(full_name, app_id):
    """Email for candidates with low Want It scores"""
    first_name = full_name.split()[0]
    widget_html = feedback_widget(full_name, "Hackathon 2026", app_id, "GWC Stage Feedback")
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Georgia, serif; background-color: #f0f4f0; margin: 0; padding: 20px; }}
            .container {{ max-width: 700px; margin: 0 auto; background-color: white; border-left: 5px solid #1565c0; padding: 40px; }}
            h2 {{ color: #1565c0; font-size: 22px; margin: 25px 0 15px 0; line-height: 1.4; }}
            p {{ font-size: 15px; line-height: 1.8; color: #333; text-align: justify; margin: 0 0 12px 0; }}
            .section {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <p>Dear {first_name},</p>

            <p>Thank you for engaging thoughtfully with the Hackathon 2026 opportunity. We genuinely appreciated your willingness to step into a detailed assessment process, and we want to reflect back what we observed about your strengths and where we found ourselves questioning fit.</p>

            <h2>What We Liked Most About You</h2>
            <div class="section">
                <p>Your technical foundation is solid. We saw that clearly in how you approached the assessment. You engaged with the problems methodically, asked thoughtful clarifying questions, and showed real hands-on capability. That's not something we take for granted—technical depth matters, and you've built that.</p>

                <p>Beyond the technical piece, we appreciated your openness throughout the process. You were willing to sit with difficult questions, reflect on your own thinking, and engage with feedback. There's a maturity and self-awareness in how you showed up that we value.</p>

                <p>We also saw someone with genuine energy and ambition. You clearly care about building skills and taking on meaningful work. That kind of drive is a strength, and it's something that will serve you well in whatever you pursue next.</p>
            </div>

            <h2>Where We Found Ourselves Sitting With Questions</h2>
            <div class="section">
                <p>Here's what became clear as we moved through the GWC assessment: while you can certainly do this role technically, the alignment between what you want from your next career move and what this position offers wasn't quite clicking. Specifically, your responses on the "Want It" dimension suggested some hesitation about whether this particular space is where you want to invest your energy right now.</p>

                <p>This isn't a criticism—it's actually important feedback. The truth is, the best professional matches happen when both sides are genuinely excited. If there's even some quietness in your enthusiasm, that's a signal worth paying attention to. We'd rather know that now than have you realize six months in that your heart wasn't fully in it.</p>

                <p>We respect your instincts about what kind of work lights you up. And we think there's probably a better fit out there for you—a role or organization where the alignment on Want It is as strong as your technical capacity.</p>
            </div>

            <h2>What We Think You Should Do Next</h2>
            <div class="section">
                <p>We'd encourage you to take some time to clarify what you're genuinely excited about moving into. What problems do you want to solve? What kind of impact do you want to create? What team environment brings out your best work? Get clear on those questions, and then seek out opportunities that align with that clarity.</p>

                <p>You have strong technical skills and good instincts. The key is channeling those toward work that you're genuinely passionate about, not just technically capable of doing. That's when you'll do your best work and build a career you're proud of.</p>

                <p>If your interests shift toward our mission in the future and you'd like to explore again, we're open to that conversation. But for now, we think there's a better fit waiting for you elsewhere—something that will get you genuinely excited to wake up and work on it.</p>
            </div>

            {widget_html}

            <p style="margin-top: 30px; color: #666; font-size: 13px; line-height: 1.6;">
                Warm regards,<br>
                People and Culture Team<br>
                Taleemabad<br>
                hiring@taleemabad.com | www.taleemabad.com<br>
                <br>
                Sent on behalf of Talent Acquisition Team by Coco
            </p>
        </div>
    </body>
    </html>
    """

def generate_mixed_email(full_name, app_id):
    """Email for candidates with mixed GWC scores"""
    first_name = full_name.split()[0]
    widget_html = feedback_widget(full_name, "Hackathon 2026", app_id, "GWC Stage Feedback")
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Georgia, serif; background-color: #f0f4f0; margin: 0; padding: 20px; }}
            .container {{ max-width: 700px; margin: 0 auto; background-color: white; border-left: 5px solid #1565c0; padding: 40px; }}
            h2 {{ color: #1565c0; font-size: 22px; margin: 25px 0 15px 0; line-height: 1.4; }}
            p {{ font-size: 15px; line-height: 1.8; color: #333; text-align: justify; margin: 0 0 12px 0; }}
            .section {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <p>Dear {first_name},</p>

            <p>We want to thank you for the genuine effort you put into the Hackathon 2026 assessment. You engaged with it sincerely, and we appreciate that kind of commitment to a process. We've spent time reviewing your performance, and we want to share what we learned—both about your real strengths and about where we see some gaps to think about.</p>

            <h2>What We Liked Most About You</h2>
            <div class="section">
                <p>You brought real thoughtfulness to understanding what this role entails. It wasn't superficial engagement; you asked good questions and showed genuine curiosity about the work. That kind of intellectual honesty is valuable.</p>

                <p>We also saw solid technical capabilities come through. When we looked at how you approached concrete problems, you showed structure in your thinking and genuine competence. That foundation is real, and it's something you can build on.</p>

                <p>Finally, we appreciated your flexibility and openness. You were willing to step into an unfamiliar space, try something new, and reflect on the experience. That kind of growth mindset—being willing to stretch and learn—is a genuine strength. Many people aren't willing to do that, and you were.</p>
            </div>

            <h2>Where We Found Ourselves Sitting With Questions</h2>
            <div class="section">
                <p>What the GWC assessment revealed is that while you have real capability, there's still some ground to cover across the three dimensions we evaluated: deeply understanding the role, having genuine enthusiasm for it, and being fully confident in your ability to deliver at the level we need.</p>

                <p>It wasn't that any single dimension was weak—it's more that all three need more development for this particular role. You're not quite at the place yet where you can hit the ground running and operate with the kind of independence and clarity this position requires.</p>

                <p>This is feedback about readiness in this moment, not a statement about your potential. With time and intentional growth, you could absolutely get there. But right now, there's still development work to do, and this role would require us to invest significantly in that journey.</p>
            </div>

            <h2>What We Think You Should Do Next</h2>
            <div class="section">
                <p>Here's what we'd recommend: seek out opportunities where you can deepen your understanding of technical-strategic integration. Work on projects where you can see how product, user needs, and engineering come together. Get hands-on experience in that intersection, because that's where clarity will develop.</p>

                <p>At the same time, get clear on your own "why"—why you're interested in this kind of work, what impact you want to create, what kind of environment you thrive in. That clarity, combined with more direct experience, will strengthen all three dimensions we looked at.</p>

                <p>Once you've built that foundation, we'd be happy to have another conversation. We don't view this as a final no—it's more of a "not yet." Keep building, keep learning, and stay open to the journey.</p>
            </div>

            {widget_html}

            <p style="margin-top: 30px; color: #666; font-size: 13px; line-height: 1.6;">
                Warm regards,<br>
                People and Culture Team<br>
                Taleemabad<br>
                hiring@taleemabad.com | www.taleemabad.com<br>
                <br>
                Sent on behalf of Talent Acquisition Team by Coco
            </p>
        </div>
    </body>
    </html>
    """

def generate_low_understanding_email(full_name, app_id):
    """Email for candidates with low Get It scores"""
    first_name = full_name.split()[0]
    widget_html = feedback_widget(full_name, "Hackathon 2026", app_id, "GWC Stage Feedback")
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Georgia, serif; background-color: #f0f4f0; margin: 0; padding: 20px; }}
            .container {{ max-width: 700px; margin: 0 auto; background-color: white; border-left: 5px solid #1565c0; padding: 40px; }}
            h2 {{ color: #1565c0; font-size: 22px; margin: 25px 0 15px 0; line-height: 1.4; }}
            p {{ font-size: 15px; line-height: 1.8; color: #333; text-align: justify; margin: 0 0 12px 0; }}
            .section {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <p>Dear {first_name},</p>

            <p>Thank you for your genuine interest in the Hackathon 2026 role and for taking the time to engage with our assessment process. We appreciated your energy and willingness to step into what we know was a challenging evaluation. We want to share some reflections on what we learned from your journey through our process.</p>

            <h2>What We Liked Most About You</h2>
            <div class="section">
                <p>You brought real enthusiasm to the conversations. It was clear that you were genuinely interested in exploring this opportunity, and that kind of positive energy matters. You showed up ready to engage, and you were willing to step into technical complexity without hesitation.</p>

                <p>We also saw your capacity to learn and adapt. Throughout the assessment, you demonstrated flexibility and a willingness to think through problems from different angles. That ability to adjust your thinking is a genuine strength that will serve you in whatever you pursue next.</p>

                <p>Finally, we appreciated your intellectual honesty. You were willing to reflect on areas where you weren't sure, rather than overconfident in areas outside your depth. That kind of self-awareness is something we value, and it shows maturity in how you approach professional growth.</p>
            </div>

            <h2>Where We Found Ourselves Sitting With Questions</h2>
            <div class="section">
                <p>What became clear through the GWC assessment is that the full complexity of this role—the way it weaves technical execution with strategic thinking and organizational impact—wasn't quite crystallizing for you yet. Your responses on the "Get It" dimension suggested that the deeper structure of how this role fits into what we're building needed more clarity.</p>

                <p>This isn't about raw intelligence or capability. It's about domain clarity. This particular position needs someone who can hit the ground understanding the full scope of impact—not just the technical execution, but how that connects to strategy, to user needs, and to our organizational direction.</p>

                <p>Right now, it feels like you're still in the learning phase on that front. That's not a criticism—we all start there. But it does mean this role would require us to invest significantly in helping you develop that understanding, and we're not in a position to do that right now.</p>
            </div>

            <h2>What We Think You Should Do Next</h2>
            <div class="section">
                <p>We'd recommend spending intentional time deepening your understanding of how technical work connects to broader strategy and impact. Work on projects where you can see that connection. Read widely in the space. Find mentors or colleagues who can help you understand the full picture of how product, user needs, and engineering come together.</p>

                <p>Seek opportunities that will build your domain clarity—whether that's through the projects you work on, the people you learn from, or the communities you engage with. That foundation will make your next opportunity much more impactful and set you up for faster growth.</p>

                <p>Once you've had time to build that understanding, we'd welcome another conversation. For now, we think you'll learn and grow fastest in a role where some of that clarity already exists, and where you can absorb it directly from your team.</p>
            </div>

            {widget_html}

            <p style="margin-top: 30px; color: #666; font-size: 13px; line-height: 1.6;">
                Warm regards,<br>
                People and Culture Team<br>
                Taleemabad<br>
                hiring@taleemabad.com | www.taleemabad.com<br>
                <br>
                Sent on behalf of Talent Acquisition Team by Coco
            </p>
        </div>
    </body>
    </html>
    """

def generate_significant_gaps_email(full_name, app_id):
    """Email for candidates with significant gaps across all dimensions"""
    first_name = full_name.split()[0]
    widget_html = feedback_widget(full_name, "Hackathon 2026", app_id, "GWC Stage Feedback")
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Georgia, serif; background-color: #f0f4f0; margin: 0; padding: 20px; }}
            .container {{ max-width: 700px; margin: 0 auto; background-color: white; border-left: 5px solid #1565c0; padding: 40px; }}
            h2 {{ color: #1565c0; font-size: 22px; margin: 25px 0 15px 0; line-height: 1.4; }}
            p {{ font-size: 15px; line-height: 1.8; color: #333; text-align: justify; margin: 0 0 12px 0; }}
            .section {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <p>Dear {first_name},</p>

            <p>Thank you for your time and effort in engaging with the Hackathon 2026 assessment. We appreciate your commitment to exploring this opportunity, and we want to provide you with honest, constructive feedback about what we learned from the process.</p>

            <h2>What We Liked Most About You</h2>
            <div class="section">
                <p>You showed genuine willingness to step into a challenging assessment. That kind of openness to try something new, even when it's outside your comfort zone, is a real strength. Not everyone is willing to do that, and it speaks to your growth-oriented mindset.</p>

                <p>We also appreciated your engagement throughout the conversations. You listened carefully to questions and tried to think through them thoughtfully. That kind of attentiveness is valuable in any professional setting.</p>

                <p>Finally, we recognized that you brought your authentic self to the process. You didn't try to be someone you're not, and that honesty is something we respect.</p>
            </div>

            <h2>Where We Found Ourselves Sitting With Questions</h2>
            <div class="section">
                <p>The GWC assessment revealed some gaps that we want to be direct about. Across all three dimensions—understanding what this role requires, genuine enthusiasm for the work, and confidence in your ability to execute—there are areas where clarity and readiness need development.</p>

                <p>This particular role is a specialized fit. It requires someone who can demonstrate strong understanding of the technical-strategic landscape, genuine passion for this kind of work, and capability to execute independently. Right now, there are gaps on all three fronts that would make it difficult for you to succeed in this position.</p>

                <p>We want to be clear that this feedback is specific to this role at this time. It doesn't speak to your broader potential or your capacity to grow in different directions. But for this particular opportunity, the alignment and readiness aren't there yet.</p>
            </div>

            <h2>What We Think You Should Do Next</h2>
            <div class="section">
                <p>We'd encourage you to take time to explore what kind of work genuinely excites you. This role clearly isn't it—and that's okay. The best careers come from people finding work that aligns with both their capabilities and their genuine interests.</p>

                <p>Seek opportunities that feel more naturally aligned with where you are right now. Work in those spaces to build deeper understanding and confidence. Get exposure to the technical, strategic, and execution elements at a pace that feels sustainable. Over time, that foundation will help you make better choices about your next moves.</p>

                <p>We wish you well in finding a role that's a better fit, and we hope this feedback, while challenging, helps you chart a clearer path forward.</p>
            </div>

            {widget_html}

            <p style="margin-top: 30px; color: #666; font-size: 13px; line-height: 1.6;">
                Warm regards,<br>
                People and Culture Team<br>
                Taleemabad<br>
                hiring@taleemabad.com | www.taleemabad.com<br>
                <br>
                Sent on behalf of Talent Acquisition Team by Coco
            </p>
        </div>
    </body>
    </html>
    """

# Send pilot emails
print("\n=== SENDING GWC REJECTION EMAILS - PILOT ===\n")

for name, data in candidates.items():
    if data['type'] == 'perfect_pass':
        body = generate_perfect_pass_email(name, data['app_id'])
    elif data['type'] == 'low_want':
        body = generate_low_want_email(name, data['app_id'])
    elif data['type'] == 'mixed':
        body = generate_mixed_email(name, data['app_id'])
    elif data['type'] == 'low_understanding':
        body = generate_low_understanding_email(name, data['app_id'])
    elif data['type'] == 'significant_gaps':
        body = generate_significant_gaps_email(name, data['app_id'])

    subject = f"[PILOT] We're reflecting on your Hackathon 2026 application — {name}"

    # Send to pilot recipients
    result = safe_sendmail(
        to=PILOT_RECIPIENTS,
        subject=subject,
        body=body,
        is_html=True,
        context=f"GWC rejection pilot for {name}",
        pilot_mode=True
    )

    if result:
        print(f"[OK] Sent pilot for {name}")
    else:
        print(f"[FAILED] Could not send pilot for {name}")

print(f"\n" + "="*60)
print(f"Pilot emails sent to: {', '.join(PILOT_RECIPIENTS)}")
print(f"="*60)
