#!/usr/bin/env python3
"""
Quick test: send warm bench email at scheduled time (1:52am PKT)
"""

import time
import sys
from warm_bench_locked import send_warm_bench_email

# Body for Dur E Nayab test
body_html = """
<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:0 0 16px 0; line-height:1.6;">
This isn't a yes for now. But we need to tell you something about what we saw in your interview that the panel kept discussing afterward, because it reveals something important about who you are.
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:0 0 16px 0; line-height:1.6;">
At about 18 minutes in, when we asked about a time you'd helped a colleague, you told us about staying late to mentor someone through a difficult project. The way you described it—not as a burden, but as something that energized you—showed us real strength in how you approach relationships at work. You didn't just do the thing; you reflected on why it mattered to you.
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:0 0 16px 0; line-height:1.6;">
<span style="font-weight:bold; color:#1565C0;">What Genuinely Impressed Us</span>
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:0 0 16px 0; line-height:1.6;">
About 35 minutes in, when we asked about a time you'd pushed back on a team decision, you didn't get defensive. You asked clarifying questions first. You genuinely wanted to understand our perspective before deciding whether to stick to yours. That openness—especially under challenge—is rare. Most people protect their ideas. You prioritized understanding.
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:0 0 16px 0; line-height:1.6;">
<span style="font-weight:bold; color:#1565C0;">Here's the Part We Need to Be Honest About</span>
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:0 0 16px 0; line-height:1.6;">
In our technical interview, we found that your background was strong in project coordination but less developed in the specific data analysis tools this role requires. For this position, at this moment, that gap matters because we need someone who can hit the ground running with those tools. It's not a weakness on you—it's a need for this specific role right now.
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:0 0 16px 0; line-height:1.6;">
<span style="font-weight:bold; color:#1565C0;">Here's Where We Want to Leave Things</span>
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:0 0 16px 0; line-height:1.6;">
We'd genuinely like to stay connected. If opportunity aligns with your experience and strengths, we'd welcome talking again. You're exactly the kind of person we want to build with—and if this isn't the right moment, the right role will come.
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:0 0 16px 0; line-height:1.6;">
P.S. That moment when you showed us the notes from your first month at your last role? The honest reflection on what you'd gotten wrong, and what you learned? That's who you are. That's someone we want on our team eventually.
</p>
"""

# Sleep for 120 seconds (2 minutes)
print("[SCHEDULED] Sleeping for 120 seconds until 1:52am PKT...")
time.sleep(120)

print("[SCHEDULED] Sending pilot email at 1:52am PKT...")

# Send as pilot
success = send_warm_bench_email(
    candidate_name="Dur E Nayab",
    candidate_email="dur.e.nayab@example.com",
    position="Junior Research Associate",
    body_html=body_html,
    subject="When Gestures Speak Louder",
    pilot_mode=True,
    pilot_recipients=["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
)

if success:
    print("[SUCCESS] Pilot email scheduled and sent at 1:52am PKT")
    sys.exit(0)
else:
    print("[FAILED] Email send failed")
    sys.exit(1)
