"""
GWC Stage Rejection Emails - CLEAN HTML (no broken MIME)
Hackathon 2026 Position
PILOT: Ayesha + Jawwad
"""
import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from scripts.utils.safe_send import safe_sendmail
from scripts.utils.feedback_widget import feedback_widget

SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")
PILOT_TO = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
ROLE = "Hackathon 2026"

# HTML HELPERS
H   = lambda t: f'<h2 style="color:#1565c0;font-size:17px;font-weight:bold;margin:36px 0 6px 0;letter-spacing:0.3px;">{t}</h2>'
SUB = lambda t: f'<p style="color:#1b5e20;font-weight:bold;margin:0 0 14px 0;font-size:14px;">{t}</p>'
P   = lambda t: f'<p style="margin:0 0 18px 0;text-align:justify;font-family:Georgia,serif;font-size:15px;line-height:1.8;">{t}</p>'
PS  = lambda t: f'<p style="margin:32px 0 0 0;padding:20px 24px;background:#f1f8e9;border-left:4px solid #1b5e20;font-style:italic;color:#2a2a2a;font-size:14px;line-height:1.7;font-family:Georgia,serif;">{t}</p>'

FOOTER = """<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:40px;border-top:1px solid #e0e0e0;padding-top:20px;"><tr><td style="font-family:Georgia,serif;font-size:13px;color:#555;line-height:1.9;">Warm regards,<br><strong style="color:#1a1a1a;">People and Culture Team</strong><br><strong style="color:#1565c0;">Taleemabad</strong><br><a href="mailto:hiring@taleemabad.com" style="color:#1565c0;text-decoration:none;">hiring@taleemabad.com</a> &nbsp;|&nbsp; <a href="http://www.taleemabad.com" style="color:#1565c0;text-decoration:none;">www.taleemabad.com</a><br><span style="font-size:12px;color:#aaa;margin-top:4px;display:block;">Sent on behalf of Talent Acquisition Team by Coco</span></td></tr></table>"""

def header_block(subject_line):
    return f"""<table width="100%" cellpadding="0" cellspacing="0" style="border-radius:8px 8px 0 0;overflow:hidden;border-bottom:2px solid #1565c0;"><tr><td align="center" bgcolor="#ffffff" style="background-color:#ffffff;padding:28px 40px 22px 40px;"><p style="margin:0;font-family:Georgia,serif;font-size:11px;color:#1565c0;letter-spacing:2px;text-transform:uppercase;">People &amp; Culture &nbsp;&bull;&nbsp; GWC Assessment</p><p style="margin:10px 0 4px 0;font-family:Georgia,serif;font-size:17px;font-weight:bold;color:#1565c0;line-height:1.4;">{subject_line}</p><p style="margin:0;font-family:Georgia,serif;font-size:12px;color:#5c85c7;">{ROLE}</p></td></tr></table>"""

def wrap(subject_line, body_html):
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body style="margin:0;padding:0;background-color:#f0f4f0;"><table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f4f0;padding:32px 0;"><tr><td align="center"><table width="620" cellpadding="0" cellspacing="0" style="max-width:620px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);"><tr><td>{header_block(subject_line)}</td></tr><tr><td style="background:#ffffff;padding:40px 52px 48px 52px;border-radius:0 0 8px 8px;font-family:Georgia,serif;font-size:15px;line-height:1.8;color:#1a1a1a;">{body_html}</td></tr></table></td></tr></table></body></html>"""

# EMAIL BODIES
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

UMAIR_BODY = (
    P("Dear Umair,") +
    P("We have completed our review of your technical assessment and GWC conversation for the Hackathon 2026 position. We want to let you know that we will not be moving you forward at this time. We also want to share what we learned from your process, because we believe this feedback will be useful as you think about your next move.") +
    H("What We Liked Most About You") +
    P("Your technical foundation is genuinely solid. You graduated with a BSCS in January 2026 and immediately moved into professional work—one year of Laravel experience at Bokala Express, where you built a web application from scratch for a startup incubation center. That kind of hands-on experience in a real business context is valuable. You've also worked on multiple freelance projects using Laravel, which shows you can take ownership of projects and see them through.") +
    P("What stood out most was your problem-solving ability. During your interview, you described a hackathon situation where you needed to generate text for a project. When OpenAI and GPT APIs failed you, you didn't give up. You researched alternatives and found Groq API—which provided free access and better performance. That kind of resourcefulness and ability to pivot quickly when your first approach doesn't work is exactly the kind of thinking we value. It shows you can think independently and find practical solutions under pressure.") +
    P("Your coding task performance was also strong. You were given a character-counting problem in PHP and solved it efficiently using a hash map. Your implementation showed clear understanding of data structures and the ability to write clean, functional code. That kind of technical execution is real.") +
    P("Finally, your willingness to engage directly with technical challenges was evident. You answered questions thoughtfully and didn't shy away from complexity.") +
    H("Where We Found Ourselves Sitting With Questions") +
    SUB("On the \"Get It\" Dimension - Your Full-Stack Understanding:") +
    P("Your backend expertise is clear. Laravel, PHP, SQL, databases—you have built real projects and clearly understand how these pieces fit together. But this position requires full-stack capability, and that's where we encountered a gap.") +
    P("When we asked about your full-stack development experience, you were honest: \"It's not my experience. But I understand HTML, CSS, JavaScript.\" That honesty is good. But the gap is significant. You mentioned you've worked on UI using Streamlit and Gradio, and you're familiar with Bootstrap templates. That's tooling, not deep understanding. There's a difference between using a template library and understanding how to design and build complex frontend systems from first principles.") +
    P("React is a specific skill we need. You mentioned foundational React knowledge but acknowledged no professional projects in React. That's a real constraint. The role requires someone who can move fluidly between backend and frontend, understanding not just how to call APIs but how to build responsive, efficient frontends that consume those APIs thoughtfully.") +
    SUB("On the \"Want It\" Dimension - Your Clarity About This Role:") +
    P("Here's what we noticed: When we described the full-stack nature of this work and the kinds of problems we solve, something softened in your responses. You didn't lean forward. You didn't ask probing questions about the frontend challenges. Instead, your answers suggested you were more energized talking about the Laravel/PHP backend work you've already done.") +
    P("This matters because the best professional matches happen when there's genuine excitement on both sides. Your strength is clearly backend development. Your experience is clearly backend development. And your enthusiasm seemed to be around backend development. That's not criticism—that's actually valuable self-knowledge. But for this particular role, which is genuinely full-stack and values the frontend half equally, we got the sense that part of the work might not engage you the same way.") +
    SUB("On the \"Capacity\" Dimension - The Scope of What You Can Execute:") +
    P("You can definitely execute backend work. You've proven that. But can you execute full-stack with the kind of independence this role requires? We have some questions. Your React knowledge is foundational. Your frontend experience is limited to templates and frameworks like Streamlit. If you were handed a complex React component problem or a difficult CSS layout challenge, we're not confident you'd have the depth to solve it independently.") +
    P("For a role like this, we need someone who can own both sides—who can debug a React performance issue just as confidently as they can optimize a database query. Right now, your capacity is strong on one half and developing on the other.") +
    H("What We Think You Should Do Next") +
    P("Your Laravel skills are valuable. Don't minimize them. But if you want to move into a full-stack role, you need to genuinely deepen your frontend capabilities. Not just frameworks—the fundamentals. Learn React deeply. Learn CSS layout and responsive design. Learn how JavaScript works at a deeper level. Build projects where you're making real frontend decisions, not just wiring together templates.") +
    P("Consider seeking a role that allows you to specialize in backend development for the next year or so. Get more professional experience. Build your portfolio. Deepen your Laravel expertise further. There's nothing wrong with specialization—it's a valid path. Many organizations value backend specialists deeply.") +
    P("If you want to move toward full-stack work, commit to it. Spend real time on React. Build 2-3 substantial projects where you own the entire stack—backend and frontend. Get that experience. Once you have professional React experience and can speak about frontend design decisions with the same confidence you speak about Laravel, you'll be in a much stronger position for roles like this.") +
    P("Most importantly, follow the work that genuinely excites you. If backend is where your energy is, lean into that. If you're genuinely interested in becoming full-stack, invest in that with intention. Either way, you'll be more successful than trying to do both half-heartedly.") +
    P("Your problem-solving ability and your willingness to learn will take you far. Channel those toward deepening expertise in the area that genuinely engages you most.") +
    PS("<strong>P.S.</strong> The resourcefulness you showed with the Groq API is a real strength. That instinct to solve problems creatively will serve you well. Keep that. And know that whether you specialize or go full-stack, the foundation you've built is solid.") +
    FOOTER
)

ALI_BODY = (
    P("Dear Ali,") +
    P("We have completed our review of your technical assessment and GWC conversation for the Hackathon 2026 position. We want to let you know that we will not be moving you forward at this time. We also want to share what we observed during our conversation with you, because the feedback is grounded in what you actually showed us, and deserves to be specific rather than generic.") +
    H("What We Liked Most About You") +
    P("You demonstrated the ability to think across the full scope of a technical project—from data sourcing through implementation to user interface. When you described your cricket analysis and prediction system, you articulated a multi-layered approach that showed systems-level thinking. You discussed multiple data sources: Kaggle datasets, live data from ESPN and Crickinfo through web scraping. More importantly, you showed awareness that different data sources require different integration strategies. That kind of thinking—recognizing that the architecture must adapt to the data—is valuable.") +
    P("You also demonstrated genuine knowledge of ML model selection. You could discuss when to use Random Forest versus XGBoost for different prediction scenarios, and you understood that real-time data ingestion creates fundamentally different technical requirements than batch processing. You weren't just listing tools. You were thinking about trade-offs and constraints.") +
    P("Beyond the technical aspects, you showed awareness of user-facing concerns. You talked about building a dashboard using Streamlit, about styling and layout considerations, about how users would actually interact with the system. You also demonstrated realistic thinking about scope and resources. You acknowledged the challenge of balancing what you want to build with what you have time to deliver. That kind of honest assessment of constraints is something we genuinely value in candidates.") +
    P("Finally, your willingness to stay engaged with difficult technical questions mattered. You stuck with the conversation for 33 minutes and kept trying to explain your thinking, even when the questions were challenging. That persistence is a strength.") +
    H("Where We Found Ourselves Sitting With Questions") +
    SUB("On the \"Get It\" Dimension - Understanding the Technical Depth:") +
    P("When we asked you to walk us through specific implementation details, we noticed the clarity began to soften. For example, when asked directly how you would write a web scraping script, you explained: \"We have to write request on. We have to write HTML and download it. Then we write a parsing. This is a step-by-step process.\" That is a reasonable high-level overview. But when we pressed further about the actual mechanics—how you would handle HTTP requests, parse HTML, deal with errors or changes in the website structure, manage rate limiting from the source—your answers became more fragmented and uncertain.") +
    P("More significantly, when discussing your own role in the implementation, you mentioned that you are relying on Gemini (an AI tool) for much of the code generation. You said: \"I am using it for hard-coded. So I am using for hard-coded.\" And when asked about sharing API keys and integrating Gemini into the system, your response suggested some uncertainty about the mechanics: \"I can. It the do it. But I can.\" This raised a question we had to sit with: How much of the technical execution is genuinely your independent work versus generated by AI? For a role like this, we need to understand what you can do independently, not just what you can prompt an AI tool to generate.") +
    SUB("On the \"Want It\" Dimension - Your Genuine Engagement:") +
    P("During the interview, we noticed something that gave us pause. You started by discussing a cricket prediction dashboard with clear scope—data sources, ML models, real-time ingestion, a Streamlit front-end. You were articulate about the components and the workflow. But then, midway through the conversation, the focus shifted entirely. You moved into discussing a completely different project: a student exam preparation system, with study schedules, weak topic identification, break management, and subject-specific learning paths.") +
    P("This shift raised a deeper question: Are you genuinely excited about either of these problems, or are you working through available tools and concepts without a clear sense of what problem actually engages you? Strong candidates usually have clarity about what they want to solve and why. They can articulate why that problem matters to them personally, why they care about getting it right. In our conversation, we didn't sense that deep engagement. Instead, we sensed someone working through technical concepts and available tools without a clear north star about what they wanted to build and why it mattered.") +
    SUB("On the \"Capacity\" Dimension - Your Ability to Execute:") +
    P("When we explored your ability to execute independently and ship complete work, there were gaps. You spoke openly about your reliance on AI-generated code. You described using hard-coded solutions and leaning on Gemini for both requirements gathering and implementation. When we asked if you were comfortable with the full-stack approach we were discussing—Django backend, React frontend, supporting infrastructure—you hesitated. You said, \"Okay, if I share a video,\" suggesting you wanted to show something rather than articulate your understanding. When we asked directly about your confidence level on independent execution, the answer was tentative.") +
    P("For a position like this, we need to see someone who can take a problem, understand it deeply, think through the technical solution independently, and execute on it without relying on AI tools as the primary mechanism for implementation.") +
    H("What We Think You Should Do Next") +
    P("Before your next opportunity, get clarity on a single problem that genuinely excites you. Don't try to build everything at once. Find one thing—whether it's the cricket analysis system, the exam prep tool, or something else entirely—and own it completely. Spend time with it. Understand not just the architecture, but the problem itself.") +
    P("Work through the full technical implementation yourself. Not just the architecture or the AI-generated parts, but the core logic, the debugging, the edge cases, the problem-solving when things don't work the way you expected. That hands-on depth is what separates understanding a project from actually building one. That is where real confidence comes from, and that is what we're looking for.") +
    P("Before your next conversation like this, be clear and direct about your role in what you've built. If you are using AI tools, be transparent about it. If you are unsure about implementation details, it is better to say so directly than to hope we don't notice. Interviewers appreciate honesty much more than uncertainty disguised as explanation.") +
    P("The ability to think about multiple data sources, system integration challenges, and full-stack architecture is a genuine strength. Build on that by deepening your ability to execute end-to-end, with clarity, independence, and confidence.") +
    PS("<strong>P.S.</strong> The systems thinking you demonstrated—recognizing that data sources have different requirements, that ML models have trade-offs, that real-time and batch processing are fundamentally different—is valuable. Keep developing that. Pair it with hands-on execution depth, and you will be a strong engineer.") +
    FOOTER
)

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

SULTAN_BODY = (
    P("Dear Sultan,") +
    P("We have completed our review of your technical assessment and GWC conversation for the Hackathon 2026 position. We want to let you know that we will not be moving you forward at this time. We also want to share what we observed during our conversation, because the feedback is grounded in what you actually showed us.") +
    H("What We Liked Most About You") +
    P("You have sought out a breadth of experience across different areas of technology. You have worked as a STEM instructor teaching programming to school students, as a Python instructor with Source Code Academia, as a computer vision intern at Access.AI, and as a generative UI intern at AI Tech Fusion. That kind of willingness to explore multiple domains and take on different roles shows initiative and curiosity about how technology works.") +
    P("You also demonstrated awareness of real-world constraints in machine learning projects. When discussing your plant health estimation project using YOLOv8 and Raspberry Pi, you showed understanding that models need to be converted to lightweight formats for edge devices. That kind of practical thinking about deployment is valuable. You also demonstrated some foundational knowledge across multiple areas—you could discuss concepts like binary search trees, linked lists, and different data structures, even if your explanations were incomplete.") +
    P("Finally, your willingness to stay in the conversation and attempt to answer technical questions, even when uncertain, showed persistence.") +
    H("Where We Found Ourselves Sitting With Questions") +
    SUB("On the \"Get It\" Dimension - Understanding Core Concepts:") +
    P("When we began exploring your technical depth, we encountered significant gaps that concerned us. These gaps weren't just in one area—they appeared across multiple fundamental domains.") +
    P("On databases: When asked how you would handle a situation where users might have the same login credentials and you needed to distinguish between them, you explained your approach as creating an ID column for each user. That's a reasonable start. But when we asked if you understood the primary key concept—a fundamental database design principle—your response was simply \"No, sir.\" A primary key is one of the foundational concepts in relational database design. The fact that you haven't yet learned this raised a question: how deeply have you engaged with the fundamentals of the tools you're using?") +
    P("On REST APIs: When we asked about REST API design and HTTP methods, your explanations became confused. You repeated \"FastDP\" several times, but that didn't clarify your understanding. When asked about GET and POST requests, you gave partial answers, but you didn't demonstrate clear understanding of why these distinctions matter or how they're used in practice.") +
    P("On HTML and frontend fundamentals: You mentioned you can \"write HTML,\" but when asked to explain the difference between div and section and span tags, your explanation was unclear. You said \"div and span are one container. Div vs. span different from the div span are one container.\" That fragmented explanation suggests you may have used these tags in frameworks or templates, but don't understand the semantic and structural differences between them. That's concerning because HTML semantics are foundational to frontend development.") +
    P("On data structures and algorithms: When we discussed linked lists, double-linked lists, and binary search trees, your explanations were incomplete. And when we asked you to explain time complexity for an algorithm, your answer was vague: \"we are using one number, we are accessing one and we don't know if we aware of which number is largest.\" That response didn't demonstrate clear understanding of how to analyze algorithmic efficiency.") +
    SUB("On the \"Want It\" Dimension - Your Clarity About Direction:") +
    P("During the interview, we noticed something significant. At the end, when we were discussing the different types of work we do, you asked: \"Is the main work that you do, is AI or the front end?\" This question suggested uncertainty about what kind of work actually interests you or what direction you want to move in.") +
    P("You also said: \"Because I am using AI, so I am saying that. That AI got me, because in full stack, I have not so much work, and in Python, I have done much work.\" This statement—choosing to focus on AI because you haven't done much work in full-stack development—raised a concern: Are you choosing areas based on what genuinely engages you, or based on where you've already had exposure? Strong candidates usually have clarity about what problem domain they want to dive deeper into.") +
    P("Additionally, when asked about your plant health estimation project results and accuracy, you gave vague answers about \"average accuracy is better than\" without finishing the sentence. And when asked if you had reached out to relevant companies like Farmedar—who do very similar work—you said \"No.\" That suggested you may not have thought deeply about what you had built or its potential applications.") +
    SUB("On the \"Capacity\" Dimension - Your Ability to Execute:") +
    P("When we explored your ability to take a concept and execute on it independently, there were concerns. You explicitly said about full-stack development: \"It's not my experience. But I understand...\" That distinction—understanding concepts versus being able to build them—matters significantly. You have done multiple internships and worked on different projects, but when pressed on the details of what you actually built, the answers became vague or deflected.") +
    P("At the end of the interview, you also said: \"this is paid internship, and when you this type of questions, I believe, you have asked HR to answer.\" That response—suggesting HR should answer technical questions rather than engaging with them—raised a question about how you approach technical challenges. In technical roles, you need to be able to articulate what you've built, what you understand, and where your gaps are.") +
    H("What We Think You Should Do Next") +
    P("Before your next opportunity, get clarity on a single domain that genuinely interests you. You have exposure to computer vision, generative AI, full-stack development, and teaching. Pick one. Commit to understanding it deeply—not just the frameworks and tools, but the foundational concepts underneath.") +
    P("If you choose frontend development, learn HTML semantics, CSS layout, and JavaScript fundamentals. Not just how to use Bootstrap or Streamlit, but why semantic HTML matters, how the box model works, why different data types behave differently in JavaScript.") +
    P("If you choose computer vision, go deeper. Understand how YOLOv8 actually works. Know your project results—exact accuracy numbers, what worked, what didn't, and why. Reach out to companies doing similar work. Learn from them.") +
    P("If you choose data science or machine learning, understand the math. Learn how algorithms actually work, not just how to call them. Understand Big O notation and why it matters.") +
    P("Most importantly, become comfortable being honest about what you don't know. In technical interviews, saying \"I haven't learned that yet\" is infinitely better than unclear or deflected answers. It shows self-awareness and a growth mindset.") +
    P("Your willingness to work across different domains is a strength. But right now, that breadth without depth is a gap. Build depth in one area, and you will be significantly stronger.") +
    PS("<strong>P.S.</strong> The fact that you have sought out multiple internships and teaching roles shows you care about growth. Channel that into going deeper—not wider—in the domains that genuinely interest you. That depth is what will make you valuable.") +
    FOOTER
)

EMAILS = [
    ("Moaz Nadeem", 1167, "Your clarity, your commitment, and what we're navigating", MOAZ_BODY),
    ("Alishba Ramzan", 1152, "Your understanding, your readiness, and our timing", ALISHBA_BODY),
    ("Umair Solangi", 1149, "Your capability, your hesitation, and what you should pursue", UMAIR_BODY),
    ("Ali Jawad", 1114, "Your engagement, your growth, and your next steps", ALI_BODY),
    ("Maryam Rafaqat", 1174, "Your enthusiasm, your gaps, and what would help you grow", MARYAM_BODY),
    ("Sultan Muhammad Hamad Sheharyar", 1117, "Your engagement, the gaps, and what would help", SULTAN_BODY),
]

print("\n=== SENDING GWC REJECTION EMAILS - PILOT (CLEAN HTML) ===\n")

try:
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER, PASSWORD)
    print("[OK] Connected to Gmail SMTP\n")

    for name, app_id, subject_line, body_html in EMAILS:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[PILOT] {name} — We're reflecting on your Hackathon 2026 application"
        msg["From"] = SENDER
        msg["To"] = ", ".join(PILOT_TO)

        full_html = wrap(subject_line, body_html)
        msg.attach(MIMEText(full_html, "html"))

        from scripts.utils.safe_send import safe_sendmail
        safe_sendmail(
            s,
            SENDER,
            PILOT_TO,
            msg.as_string(),
            context=f"GWC_rejection_pilot_{name.replace(' ', '_')}"
        )
        print(f"[OK] Sent pilot for {name}")

    s.quit()
    print(f"\n" + "="*60)
    print(f"Sent 6 clean HTML pilots")
    print(f"="*60)

except Exception as e:
    print(f"[FAILED] {e}")
    import traceback
    traceback.print_exc()
