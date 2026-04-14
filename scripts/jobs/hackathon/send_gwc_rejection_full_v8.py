"""
GWC Stage Rejection Emails - Full v8 Format
Hackathon 2026 Position
PILOT: Ayesha + Jawwad
"""
import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from scripts.utils.safe_send import safe_sendmail
from scripts.utils.feedback_widget import feedback_widget

PILOT_MODE = True
SENDER = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
PILOT_TO = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
ROLE = "Hackathon 2026"

LOGO_PATH = os.path.join(os.path.dirname(__file__), "../../..", "assets", "logo_taleemabad.png")

# ── HTML HELPERS (v8 design) ──────────────────────────────────────────────────

H   = lambda t: f'<h2 style="color:#1565c0;font-size:17px;font-weight:bold;margin:36px 0 6px 0;letter-spacing:0.3px;">{t}</h2>'
SUB = lambda t: f'<p style="color:#1b5e20;font-weight:bold;margin:0 0 14px 0;font-size:14px;">{t}</p>'
P   = lambda t: f'<p style="margin:0 0 18px 0;text-align:justify;font-family:Georgia,serif;font-size:15px;line-height:1.8;">{t}</p>'
PS  = lambda t: f'<p style="margin:32px 0 0 0;padding:20px 24px;background:#f1f8e9;border-left:4px solid #1b5e20;font-style:italic;color:#2a2a2a;font-size:14px;line-height:1.7;font-family:Georgia,serif;">{t}</p>'

FOOTER = """
<table width="100%" cellpadding="0" cellspacing="0"
       style="margin-top:40px;border-top:1px solid #e0e0e0;padding-top:20px;">
  <tr>
    <td style="font-family:Georgia,serif;font-size:13px;color:#555;line-height:1.9;">
      Warm regards,<br>
      <strong style="color:#1a1a1a;">People and Culture Team</strong><br>
      <strong style="color:#1565c0;">Taleemabad</strong><br>
      <a href="mailto:hiring@taleemabad.com"
         style="color:#1565c0;text-decoration:none;">hiring@taleemabad.com</a>
      &nbsp;|&nbsp;
      <a href="http://www.taleemabad.com"
         style="color:#1565c0;text-decoration:none;">www.taleemabad.com</a><br>
      <span style="font-size:12px;color:#aaa;margin-top:4px;display:block;">
        Sent on behalf of Talent Acquisition Team by Coco
      </span>
    </td>
  </tr>
</table>"""

def header_block(subject_line):
    return f"""
<table width="100%" cellpadding="0" cellspacing="0"
       style="border-radius:8px 8px 0 0;overflow:hidden;border-bottom:2px solid #1565c0;">
  <tr>
    <td align="center" bgcolor="#ffffff"
        style="background-color:#ffffff;padding:28px 40px 22px 40px;">
      <img src="cid:taleemabad_logo" height="38" alt="Taleemabad"
           style="display:block;margin:0 auto 14px auto;">
      <p style="margin:0;font-family:Georgia,serif;font-size:11px;
                color:#1565c0;letter-spacing:2px;text-transform:uppercase;">
        People &amp; Culture &nbsp;&bull;&nbsp; GWC Assessment
      </p>
      <p style="margin:10px 0 4px 0;font-family:Georgia,serif;font-size:17px;
                font-weight:bold;color:#1565c0;line-height:1.4;">
        {subject_line}
      </p>
      <p style="margin:0;font-family:Georgia,serif;font-size:12px;color:#5c85c7;">
        {ROLE}
      </p>
    </td>
  </tr>
</table>"""

def wrap(subject_line, body_html):
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background-color:#f0f4f0;">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background-color:#f0f4f0;padding:32px 0;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0"
             style="max-width:620px;border-radius:8px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);">
        <tr><td>{header_block(subject_line)}</td></tr>
        <tr>
          <td style="background:#ffffff;padding:40px 52px 48px 52px;
                     border-radius:0 0 8px 8px;
                     font-family:Georgia,serif;font-size:15px;
                     line-height:1.8;color:#1a1a1a;">
            {body_html}
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""

# ── MOAZ NADEEM (Perfect Pass) ─────────────────────────────────────────────────

MOAZ_SUBJECT = "Your clarity, your commitment, and what we're navigating"

MOAZ_BODY = (
    P("Dear Moaz,") +
    P("We have completed our review of your technical assessment and GWC evaluation for the Hackathon 2026 position. We want to let you know, with directness and care, that we will not be moving you forward at this time. Before you move ahead, we want to reflect back what we saw in you, because this is worth understanding.") +

    H("What We Liked Most About You") +
    P("Your performance across the GWC assessment was exceptional. You demonstrated a crystal-clear understanding of what this role demands. It was not theoretical or surface-level understanding. You showed grasp of the full scope: what success looks like, why it matters, how it connects to broader impact. That depth of understanding came through consistently across every dimension we explored.") +
    P("Beyond understanding, your genuine enthusiasm for this space was unmistakable. You articulated not just what you could do, but why you want to do it. That alignment between capability and motivation is rare, and we value it deeply. Your commitment to the kind of work we are building felt authentic and grounded.") +
    P("Finally, your capacity to execute across multiple dimensions was evident. You showed technical depth, strategic thinking, and the ability to hold complexity without oversimplifying. We could envision you moving quickly and independently in this role, solving problems as they emerge, and growing into greater responsibility over time. The combination of these three elements—genuinely understanding the role, wanting it for the right reasons, and having the capacity to deliver at a high level—is what we look for in candidates. You showed us all three.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We want to be direct, because you deserve honesty.") +
    P("This is not about your readiness. You have demonstrated that you are prepared for this role. The challenge we are sitting with is about us, not about you. We are at a moment where our team structure is still settling. We are building the infrastructure we need, but we are not yet at the place where we can offer you the kind of hands-on mentorship and clarity that you would deserve during your first months here.") +
    P("While your skills and enthusiasm are exactly what we would want in an ideal scenario, we are also aware that bringing someone into a role carries a responsibility on our end. We would need to invest significantly in your onboarding, to create clear pathways for your growth, and to give you the attention you'd need to thrive. Right now, we are concerned we could not give you that in the way that matters.") +
    P("It is an honest assessment of where we are as a team. It is not a reflection of you. We believe you are built for this kind of impact work, and we would rather be transparent about our constraints than bring you in and under-invest in making this work. That would not be fair to you, and it would not be fair to the team.") +

    H("What We Think You Should Do Next") +
    P("Keep doing the work that excites you. Whether that is deepening your technical skills, exploring new problem spaces, or building a portfolio of projects you are genuinely proud of, invest in becoming an even stronger version of yourself. Do not wait for us.") +
    P("In three to six months, as we stabilize our team and create more breathing room, we would genuinely love to revisit this conversation. We would like to keep the door open. If you find yourself drawn back to our mission, and if you are interested in staying loosely connected, reach out then. We will remember this conversation, and we will be excited to talk again.") +
    P("We believe you are going places. And we would like to be part of that story if the timing and fit align down the road.") +

    PS("<strong>P.S.</strong> The clarity you bring to understanding complex problems, the genuine passion you have for creating impact, and the strategic thinking you demonstrated throughout the assessment are genuinely valuable qualities. Organizations will be lucky to work with you. If we can support that journey from a distance, or if the conversation makes sense to revisit later, we are here.") +

    FOOTER
)

MOAZ_HTML = wrap(MOAZ_SUBJECT, MOAZ_BODY)

# ── ALISHBA RAMZAN (Perfect Pass) ──────────────────────────────────────────────

ALISHBA_SUBJECT = "Your understanding, your readiness, and our timing"

ALISHBA_BODY = (
    P("Dear Alishba,") +
    P("We have completed our evaluation of your technical assessment and GWC conversation for the Hackathon 2026 position. We are writing to let you know that we will not be moving you forward at this time. We want to share what we saw in you, because this reflects on your strengths and the reality of where we are as a team.") +

    H("What We Liked Most About You") +
    P("Your understanding of this role is exceptionally clear. You demonstrated grasp of not just what the role does, but what it requires, what it demands, and why it matters. The way you talked about the role suggested someone who has thought deeply about it, who understands the landscape, and who can see how all the pieces fit together.") +
    P("What stood out equally was your genuine enthusiasm. You articulated your interest in this work with authenticity. Your responses were not generic. They reflected real thinking about why this role, why this mission, and what you want to build here. That kind of alignment between what you want from your next move and what we are offering is what we look for.") +
    P("Your capacity to execute is also evident. You showed strong problem-solving ability, strategic thinking, and readiness to work independently. We could see you stepping in and making an impact quickly. The combination of understanding, enthusiasm, and capability is what makes someone truly ready for a role like this. You showed us all three.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("The challenge here is about our readiness, not yours.") +
    P("You are prepared for this role. That is clear. But we are not yet at the place where we can give you what you deserve. Our team is in a phase of significant change and growth. We are building the structure we need, but we are still settling into our rhythm. We are concerned that we do not have the bandwidth right now to give you the mentorship, clarity, and hands-on support that you would need in your first months.") +
    P("Bringing someone in carries responsibility. We would need to invest time in your onboarding, help you understand our culture and approach, and give you regular feedback and growth opportunities. Right now, we cannot make that promise with confidence. We would rather tell you that now than have you discover it three months in.") +
    P("This is not about you. This is about us being honest about what we can offer right now.") +

    H("What We Think You Should Do Next") +
    P("Continue building what you are building. Seek roles where you can move quickly and make an immediate impact. Do not wait for us to get our house in order. Your readiness is now. Go use it.") +
    P("Keep an eye on Taleemabad. In a few months, as our team stabilizes, the conversation might look different. We are not closing a door. We are being honest about timing.") +
    P("Your clarity about what you want, your enthusiasm, and your readiness are all genuine strengths. Organizations will be fortunate to work with you. Go find one that can meet you where you are right now.") +

    PS("<strong>P.S.</strong> The thoughtfulness you bring to understanding impact, and the genuine excitement you have for this kind of work, are real assets. Keep those. And know that if the timing shifts and you want to reconnect, we would genuinely welcome that conversation.") +

    FOOTER
)

ALISHBA_HTML = wrap(ALISHBA_SUBJECT, ALISHBA_BODY)

# ── UMAIR SOLANGI (Low Want It) ────────────────────────────────────────────────

UMAIR_SUBJECT = "Your capability, your hesitation, and what you should pursue"

UMAIR_BODY = (
    P("Dear Umair,") +
    P("We have completed our review of your technical assessment and GWC evaluation for the Hackathon 2026 position. We want to let you know that we will not be moving you forward. We also want to share what we learned from your process, because the insight might be useful as you think about your next move.") +

    H("What We Liked Most About You") +
    P("Your technical foundation is solid. We saw that clearly in how you approached the assessment. You engaged with the problems methodically, asked thoughtful clarifying questions, and showed real hands-on capability. That kind of technical depth is not something we take for granted. You have built something genuine there.") +
    P("Beyond the technical piece, we appreciated your openness throughout the process. You were willing to sit with difficult questions, to reflect on your own thinking, and to engage with feedback. There is maturity and self-awareness in how you showed up. That kind of intellectual honesty is valuable.") +
    P("We also saw someone with genuine energy and ambition. You clearly care about building skills and taking on meaningful work. That drive is a strength, and it is something that will serve you well in whatever you pursue next.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("This is about alignment, not about capability.") +
    P("While you can absolutely do this role technically, something became clear as we moved through the GWC assessment. The alignment between what you want from your next career move and what this position offers was not quite clicking. Specifically, when we explored the 'Want It' dimension—your genuine enthusiasm for this particular space, this particular mission, this particular kind of work—something softened. Your responses suggested hesitation about whether this is where you want to invest your energy right now.") +
    P("That is not a criticism. It is actually important feedback. The truth is, the best professional matches happen when both sides are genuinely excited. If there is even some quietness in your enthusiasm, that is a signal worth paying attention to. We would rather know that now than have you realize six months in that your heart was not fully in it.") +
    P("We respect your instincts about what kind of work lights you up. And we think there is probably a better fit out there for you. A role or organization where the alignment on 'Want It' is as strong as your technical capacity.") +

    H("What We Think You Should Do Next") +
    P("Take time to clarify what you are genuinely excited about moving into. What problems do you want to solve? What kind of impact do you want to create? What team environment brings out your best work? Get clear on those questions, and then seek out opportunities that align with that clarity.") +
    P("You have strong technical skills and good instincts. The key is channeling those toward work that you are genuinely passionate about. Not just technically capable of doing. That is when you will do your best work and build a career you are proud of.") +
    P("If your interests shift toward our mission in the future and you would like to explore again, we are open to that conversation. But for now, we think there is a better fit waiting for you elsewhere. Something that will get you genuinely excited to wake up and work on it.") +

    PS("<strong>P.S.</strong> The technical depth you have built is real. Do not minimize that. But do pay attention to what kind of work lights you up. That clarity is often more important than the technical match. Build your career around what you genuinely want to build, not what you think you should want.") +

    FOOTER
)

UMAIR_HTML = wrap(UMAIR_SUBJECT, UMAIR_BODY)

# ── ALI JAWAD (Mixed Gaps) ─────────────────────────────────────────────────────

ALI_SUBJECT = "Your engagement, your growth, and your next steps"

ALI_BODY = (
    P("Dear Ali,") +
    P("We have completed our evaluation of your technical assessment and GWC conversation for the Hackathon 2026 position. We want to let you know that we will not be moving you forward at this time. We also want to share some reflection on what we learned from your process, because we believe this feedback will be useful as you think about your next move.") +

    H("What We Liked Most About You") +
    P("You brought real thoughtfulness to understanding what this role entails. It was not superficial engagement. You asked good questions and showed genuine curiosity about the work. That kind of intellectual honesty is valuable. You were willing to ask clarifying questions when something was not clear, rather than making assumptions.") +
    P("We also saw solid technical capabilities come through. When we looked at how you approached concrete problems, you showed structure in your thinking and genuine competence. You did not panic when faced with ambiguity. You broke problems down. You thought through implications. That foundation is real, and it is something you can absolutely build on.") +
    P("Finally, we appreciated your flexibility and openness. You were willing to step into an unfamiliar space, try something new, and reflect on the experience. That kind of growth mindset—being willing to stretch and learn—is a genuine strength. Many people are not willing to do that. You were.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We want to be direct about what we found, and why.") +
    P("The GWC assessment revealed something important: while you have real capability, there is still ground to cover across all three dimensions we evaluated. Getting the role—understanding it deeply. Wanting it—having genuine enthusiasm. Capacity to do it—confidence in your ability to deliver at the level we need. All three dimensions need more development for this particular position.") +
    P("It was not that any single dimension was weak in isolation. It is more that all three need additional development for this specific role. You are not quite at the place yet where you can hit the ground running and operate with the kind of independence and clarity this position requires. The combination matters.") +
    P("This is feedback about readiness in this moment, not a statement about your potential. With time and intentional growth, you could absolutely get there. But right now, there is still development work to do, and this role would require us to invest significantly in that journey alongside you. That is a commitment we cannot make right now.") +

    H("What We Think You Should Do Next") +
    P("Seek out opportunities where you can deepen your understanding of how technical work connects to strategy and organizational impact. Work on projects where you can see that connection in action. That is where the clarity develops.") +
    P("At the same time, get clear on your own 'why'. Why are you interested in this kind of work? What impact do you want to create? What kind of environment do you thrive in? That clarity, combined with more direct experience, will strengthen all three dimensions we looked at.") +
    P("Once you have built that foundation, we would be happy to have another conversation. We do not view this as a final no. It is more of a 'not yet'. Keep building. Keep learning. Stay open to the journey. And if the time comes when you feel ready to revisit this, we are open to that.") +

    PS("<strong>P.S.</strong> The willingness you showed to engage with complexity and your openness to learning are genuinely valuable. Do not lose those as you grow. Use them. They are your foundation.") +

    FOOTER
)

ALI_HTML = wrap(ALI_SUBJECT, ALI_BODY)

# ── MARYAM RAFAQAT (Low Understanding) ─────────────────────────────────────────

MARYAM_SUBJECT = "Your enthusiasm, your gaps, and what would help you grow"

MARYAM_BODY = (
    P("Dear Maryam,") +
    P("We have completed our evaluation of your technical assessment and GWC conversation for the Hackathon 2026 position. We are writing to let you know that we will not be moving you forward at this time. We want to be honest about that, and we also want this to feel useful to you. So we are sharing what we learned from your process.") +

    H("What We Liked Most About You") +
    P("You brought real enthusiasm to the conversations. It was clear that you were genuinely interested in exploring this opportunity, and that kind of positive energy matters. You showed up ready to engage. You were willing to step into technical complexity without hesitation. That willingness to try is important.") +
    P("We also saw your capacity to learn and adapt. Throughout the assessment, you demonstrated flexibility and a willingness to think through problems from different angles. That ability to adjust your thinking, to consider new perspectives, is a genuine strength that will serve you in whatever you pursue next.") +
    P("Finally, we appreciated your intellectual honesty. You were willing to reflect on areas where you were not sure, rather than overconfident in areas outside your depth. That kind of self-awareness is something we value, and it shows maturity in how you approach professional growth.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We want to be direct, because clarity is more helpful than softness.") +
    P("The GWC assessment revealed something important about readiness for this specific role. The full complexity of this position—the way it weaves technical execution with strategic thinking and organizational impact—was not quite crystallizing for you yet. Your responses on the 'Get It' dimension suggested that you are still in the learning phase on how this role fits into the broader picture of what we are building.") +
    P("This is not about raw intelligence or capability. It is about domain clarity. This particular position needs someone who can hit the ground understanding the full scope of impact. Not just the technical execution, but how that connects to strategy, to user needs, and to our organizational direction. Right now, it feels like you are still in the learning phase on that front.") +
    P("That is not a criticism. We all start there. But it does mean this role would require us to invest significantly in helping you develop that understanding. And we are not in a position to do that right now. You deserve a role where some of that clarity already exists, where you can absorb it directly from your team as you work.") +

    H("What We Think You Should Do Next") +
    P("Spend intentional time deepening your understanding of how technical work connects to broader strategy and impact. Work on projects where you can see that connection. Read widely in the space. Find mentors or colleagues who can help you understand the full picture of how product, user needs, and engineering come together. That is the foundation that will make your next opportunity much more impactful.") +
    P("Seek opportunities that will build your domain clarity. Whether that is through the projects you work on, the people you learn from, or the communities you engage with, look for contexts where that learning happens naturally.") +
    P("Once you have had time to build that understanding, we would welcome another conversation. For now, we think you will learn and grow fastest in a role where some of that clarity already exists in the environment, and where you can absorb it directly from your team.") +

    PS("<strong>P.S.</strong> The enthusiasm you bring and your willingness to learn are genuine strengths. Do not lose those. Build on them by deepening your understanding of how the pieces connect. That foundation will serve you well.") +

    FOOTER
)

MARYAM_HTML = wrap(MARYAM_SUBJECT, MARYAM_BODY)

# ── SULTAN MUHAMMAD HAMAD SHEHARYAR (Significant Gaps) ───────────────────────

SULTAN_SUBJECT = "Your engagement, the gaps, and what would help"

SULTAN_BODY = (
    P("Dear Sultan,") +
    P("We have completed our evaluation of your technical assessment and GWC conversation for the Hackathon 2026 position. We want to let you know that we will not be moving you forward. We also want to provide feedback that we believe will be useful as you reflect on this process and think about your next moves.") +

    H("What We Liked Most About You") +
    P("You showed genuine willingness to step into a challenging assessment. That kind of openness to try something new, even when it is outside your comfort zone, is a real strength. Not everyone is willing to do that. It speaks to a growth-oriented mindset that we value.") +
    P("We also appreciated your engagement throughout the conversations. You listened carefully to questions. You tried to think through them thoughtfully. You did not dismiss things you did not understand. That kind of attentiveness is valuable in any professional setting.") +
    P("Finally, we recognized that you brought your authentic self to the process. You did not try to be someone you are not. That honesty is something we respect, and it is the foundation of any useful feedback.") +

    H("Where We Found Ourselves Sitting With Questions") +
    SUB("We want to be clear and direct about what we found.") +
    P("The GWC assessment revealed significant gaps across all three dimensions we evaluate. Understanding what this role requires. Genuine enthusiasm for the work. Confidence in your ability to execute. There are gaps on all three fronts.") +
    P("On the 'Get It' dimension, the full scope and complexity of this role did not come through clearly in your responses. You showed effort to understand, but the depth of grasp needed for this position was not there. On 'Want It', your responses suggested this may not be the direction you are genuinely excited about. And on 'Capacity', there were questions about whether this particular role is the right fit for where you are right now in your development.") +
    P("This particular position is a specialized fit. It requires someone who can demonstrate strong understanding of what the role demands, genuine passion for this kind of work, and capability to execute with a degree of independence. Right now, there are gaps on all three fronts that would make it difficult for you to succeed in this position.") +

    H("What We Think You Should Do Next") +
    P("Take time to explore what kind of work genuinely excites you. This role clearly is not it, and that is okay. The best careers come from people finding work that aligns with both their capabilities and their genuine interests. Do not force a fit that does not feel right.") +
    P("Seek opportunities that feel more naturally aligned with where you are right now. Work in those spaces to build deeper understanding and confidence. Get exposure to the technical, strategic, and execution elements at a pace that feels sustainable to you. Over time, that foundation will help you make better choices about your next moves.") +
    P("Growth happens best when you are learning in a context that actually engages you. So the priority right now is finding that context, and building from there.") +

    PS("<strong>P.S.</strong> We wish you well in finding a role that is a better fit. We hope this feedback, while challenging, helps you chart a clearer path forward. Your willingness to engage and be authentic in this process is something to maintain, wherever you go next.") +

    FOOTER
)

SULTAN_HTML = wrap(SULTAN_SUBJECT, SULTAN_BODY)

# ── EMAILS LIST ────────────────────────────────────────────────────────────────

EMAILS = [
    ("Moaz Nadeem", "muazndm128@gmail.com", 1167, MOAZ_HTML),
    ("Alishba Ramzan", "alishbaramzan1@gmail.com", 1152, ALISHBA_HTML),
    ("Umair Solangi", "bscs2112203@szabist.pk", 1149, UMAIR_HTML),
    ("Ali Jawad", "ali.jawad6204@gmail.com", 1114, ALI_HTML),
    ("Maryam Rafaqat", "maryamrafaqat88@gmail.com", 1174, MARYAM_HTML),
    ("Sultan Muhammad Hamad Sheharyar", "pirzadahammadzakori@gmail.com", 1117, SULTAN_HTML),
]

# ── SEND PILOT ──────────────────────────────────────────────────────────────────

print("\n=== SENDING GWC REJECTION EMAILS - PILOT (v8 FORMAT) ===\n")

try:
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER, PASSWORD)
    print("[OK] Connected to Gmail SMTP\n")

    sent_count = 0

    for name, candidate_email, app_id, html_body in EMAILS:
        # Create message
        msg = MIMEMultipart("related")
        msg["Subject"] = f"[PILOT] {name} — We're reflecting on your Hackathon 2026 application"
        msg["From"] = SENDER
        msg["To"] = ", ".join(PILOT_TO)

        # Attach logo as CID
        try:
            with open(LOGO_PATH, "rb") as logo_file:
                logo = MIMEImage(logo_file.read())
                logo.add_header("Content-ID", "<taleemabad_logo>")
                logo.add_header("Content-Disposition", "inline")
                msg.attach(logo)
        except FileNotFoundError:
            print(f"[WARNING] Logo not found at {LOGO_PATH}")

        # Add body with feedback widget
        widget = feedback_widget(name, ROLE, app_id, "Application Feedback")
        full_body = html_body.replace(FOOTER, widget + FOOTER)

        msg_alt = MIMEMultipart("alternative")
        msg.attach(msg_alt)
        msg_alt.attach(MIMEText(full_body, "html"))

        # Send via safe_sendmail
        from scripts.utils.safe_send import safe_sendmail
        safe_sendmail(
            s,
            SENDER,
            PILOT_TO,
            msg.as_string(),
            context=f"GWC_rejection_pilot_{name.replace(' ', '_')}"
        )
        sent_count += 1
        print(f"[OK] Pilot sent for {name}")

    s.quit()

    print(f"\n" + "="*60)
    print(f"Sent {sent_count} pilot emails (v8 format, 800-1100 words each)")
    print(f"PILOT RECIPIENTS: {', '.join(PILOT_TO)}")
    print(f"="*60)

except Exception as e:
    print(f"[FAILED] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
