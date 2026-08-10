"""
Draft GWC Stage Rejection Emails for Hackathon 2026
Pilot to Ayesha + Jawwad only
"""
import sys
sys.path.insert(0, "c:/Agent Coco")

from scripts.utils.feedback_widget import feedback_widget
import json

# Candidate data with GWC scores
candidates = {
    "Moaz Nadeem": {
        "email": "muazndm128@gmail.com",
        "getIt": 3, "wantIt": 3, "capacity": 3,
        "profile": "Web developer from GIKI"
    },
    "Alishba Ramzan": {
        "email": "alishbaramzan1@gmail.com",
        "getIt": 3, "wantIt": 3, "capacity": 3,
        "profile": "Hackathon participant"
    },
    "Umair Solangi": {
        "email": "bscs2112203@szabist.pk",
        "getIt": 2, "wantIt": 1, "capacity": 3,
        "profile": "SZABIST student, web development interest"
    },
    "Ali Jawad": {
        "email": "ali.jawad6204@gmail.com",
        "getIt": 2, "wantIt": 2, "capacity": 2,
        "profile": "Hackathon participant"
    },
    "Maryam Rafaqat": {
        "email": "maryamrafaqat88@gmail.com",
        "getIt": 1, "wantIt": 1, "capacity": 3,
        "profile": "Hackathon participant"
    },
    "Sultan Muhammad Hamad Sheharyar": {
        "email": "pirzadahammadzakori@gmail.com",
        "getIt": 0, "wantIt": 1, "capacity": 1,
        "profile": "Hackathon participant"
    }
}

# HTML email template with v8 design
email_template = """
<html>
<head>
    <style>
        body {{ font-family: Georgia, serif; background-color: #f0f4f0; margin: 0; padding: 20px; }}
        .container {{ max-width: 700px; margin: 0 auto; background-color: white; border-left: 5px solid #1565c0; padding: 40px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .logo {{ height: 40px; margin-bottom: 20px; }}
        h2 {{ color: #1565c0; font-size: 22px; margin: 25px 0 15px 0; }}
        .subheading {{ color: #2e7d32; font-size: 16px; font-weight: bold; margin: 20px 0 10px 0; }}
        p {{ font-size: 15px; line-height: 1.8; color: #333; text-align: justify; }}
        .section {{ margin-bottom: 25px; }}
        .widget {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }}
        .signature {{ margin-top: 30px; color: #666; font-size: 13px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="cid:logo" class="logo" alt="Taleemabad">
        </div>

        <p>Dear {name},</p>

        <p>Thank you for going through the technical interview and GWC assessment for the Hackathon 2026 position. We've reviewed your performance across all stages, and we want to share some reflections on your journey through our process.</p>

        <h2>What We Liked Most About You</h2>
        {what_we_liked}

        <h2>Where We Found Ourselves Sitting With Questions</h2>
        {where_we_questioned}

        <h2>What We Think You Should Do Next</h2>
        {what_next}

        <div class="widget">
            {feedback_widget_html}
        </div>

        <div class="signature">
            <p>Warm regards,<br>
            People and Culture Team<br>
            Taleemabad<br>
            hiring@taleemabad.com | www.taleemabad.com</p>
        </div>
    </div>
</body>
</html>
"""

def generate_email_for_candidate(name, data):
    """Generate GWC rejection email based on scorecard"""

    get_it = data['getIt']
    want_it = data['wantIt']
    capacity = data['capacity']

    # Generate sections based on GWC scores
    if get_it == 3 and want_it == 3 and capacity == 3:
        # Perfect score - focus on timing/fit with org
        what_we_liked = f"""
        <div class="section">
            <p>Your performance across our GWC assessment was exceptional. You demonstrated a crystal-clear understanding of the Hackathon role, what it demands, and why it matters. Your commitment to the space shone through in every conversation, and your capacity to execute across technical and strategic dimensions is evident.</p>
            <p>Beyond the scorecard, we were impressed by your thoughtfulness in the process and the genuine curiosity you brought to understanding our mission.</p>
        </div>
        """
        where_we_questioned = f"""
        <div class="section">
            <p>Honestly, this isn't about gaps in your capability. You've shown us clearly that you get the role, want it deeply, and have the capacity to deliver. The challenge we're sitting with is around timing and immediate team fit for this particular moment.</p>
            <p>We believe you're built for this kind of work, but right now, we don't have the bandwidth to give you the support and growth environment you deserve.</p>
        </div>
        """
        what_next = f"""
        <div class="section">
            <p>We'd like to keep the door open. In three to six months, as our team stabilizes, we'd love to revisit this conversation. In the interim, we'd encourage you to deepen your work in whatever domain excites you most—whether that's product, engineering, or impact design.</p>
            <p>When you're ready to reconnect, reach out directly. We'll make sure we have a real opportunity to explore.</p>
        </div>
        """

    elif want_it < 2:
        # Low Want It - role fit concern
        what_we_liked = f"""
        <div class="section">
            <p>Your technical foundation is solid, and we appreciated your willingness to engage seriously with the assessment. You clearly demonstrated hands-on capability—the capacity to execute was evident in how you approached the technical challenges.</p>
            <p>Your energy and openness in conversations with us showed a genuine person with real potential.</p>
        </div>
        """
        where_we_questioned = f"""
        <div class="section">
            <p>What became clear through the GWC assessment is that while you can do this role, the alignment between what you want from your next move and what this position offers isn't quite there yet. In particular, your responses on the "Want It" dimension suggested some hesitation about whether this specific space and mission are where you want to invest your energy right now.</p>
            <p>That's not a criticism—it's actually important feedback. The best matches happen when both sides are genuinely excited about the opportunity.</p>
        </div>
        """
        what_next = f"""
        <div class="section">
            <p>We'd encourage you to take time to clarify what you're genuinely excited about—the problems you want to solve, the impact you want to create, the kind of team environment that brings out your best. Once you've mapped that out, seek roles that align with that clarity.</p>
            <p>If your interests shift toward our mission and you'd like to explore again, we're open to that conversation. But for now, we think there's a better fit waiting for you elsewhere.</p>
        </div>
        """

    elif get_it < 2:
        # Low Get It - role understanding gap
        what_we_liked = f"""
        <div class="section">
            <p>We appreciated your enthusiasm throughout the process and your willingness to step into an unfamiliar space. You showed real effort in trying to understand what the Hackathon role demands, and we respect the intellectual honesty you brought to the assessment.</p>
            <p>Your capacity to learn and adapt is a genuine strength.</p>
        </div>
        """
        where_we_questioned = f"""
        <div class="section">
            <p>What we noticed through the GWC assessment is that the complexity of this specific role—the way it weaves technical execution with strategic thinking—wasn't quite crystallizing for you yet. Your responses on the "Get It" dimension suggested some gaps in how the role fits into the broader organizational context.</p>
            <p>This isn't about raw capability; it's about domain clarity. This particular opportunity needs someone who can hit the ground with a deep read of what success looks like.</p>
        </div>
        """
        what_next = f"""
        <div class="section">
            <p>We'd recommend spending time deepening your understanding of the technical-strategy intersection. Work on a project where you can see how product, user research, and engineering come together. Read widely in the space. That foundation will make your next opportunity much more impactful.</p>
            <p>Once you've had time to build that clarity, we'd welcome another conversation.</p>
        </div>
        """

    else:
        # Mixed scores - some gaps across dimensions
        what_we_liked = f"""
        <div class="section">
            <p>We saw real strengths in your technical foundation and your willingness to engage thoughtfully with a challenging assessment. You brought genuine effort to understanding the role, and your capacity to execute on concrete tasks came through clearly.</p>
            <p>Your openness to feedback and reflection is something we value.</p>
        </div>
        """
        where_we_questioned = f"""
        <div class="section">
            <p>The GWC assessment revealed some complexity in how all three dimensions—understanding the role, genuine enthusiasm for it, and capacity to deliver—come together for you. While you showed strength in some areas, there were also places where alignment or clarity seemed to soften.</p>
            <p>For a role like this, we need all three dimensions firing on all cylinders from day one. Right now, it feels like there's still some ground to cover.</p>
        </div>
        """
        what_next = f"""
        <div class="section">
            <p>Use this feedback to get clearer on what kind of role lets you be your best. Seek opportunities where your existing strengths can shine while you build depth in the areas that are still developing. Revisit your "Why?" for your next move—get crystal clear on what you want from your next role and why.</p>
            <p>Once you've had that clarity, we'd be happy to talk again.</p>
        </div>
        """

    # Format email
    email_html = email_template.format(
        name=name,
        what_we_liked=what_we_liked,
        where_we_questioned=where_we_questioned,
        what_next=what_next,
        feedback_widget_html="[Feedback widget will be inserted here]"
    )

    return email_html


# Generate all emails
print("\n=== DRAFT GWC REJECTION EMAILS ===\n")
for name, data in candidates.items():
    print(f"\n{'='*60}")
    print(f"TO: {data['email']}")
    print(f"SUBJECT: We're reflecting on your Hackathon 2026 application")
    print(f"GWC Scores - Get:{data['getIt']}/3 Want:{data['wantIt']}/3 Capacity:{data['capacity']}/3")
    print(f"{'='*60}\n")

    email_html = generate_email_for_candidate(name, data)

    # Count words (rough estimate)
    text_content = email_html.replace('<br>', ' ').replace('</p>', ' ')
    import re
    text_only = re.sub('<[^<]+?>', '', text_content)
    word_count = len(text_only.split())

    print(f"[Email HTML - approximately {word_count} words]")
    print(f"\nDraft ready for review.\n")

print("\n" + "="*60)
print("PILOT RECIPIENTS: ayesha.khan@taleemabad.com, jawwad.ali@taleemabad.com")
print("PILOT_MODE: True")
print("="*60)
