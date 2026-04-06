"""
Candidate Communication Feedback Widget
========================================
Python port of Noah's feedback-widget.js (tools/gmail-mcp/feedback-widget.js)

For use ONLY on personalised candidate-facing emails:
  - Application feedback (rejection / warm bench / warm hold)
  - Offer letters

DO NOT add to transactional emails (GWC invite, values invite, reminders).

Usage:
    from scripts.utils.feedback_widget import feedback_widget

    html = wrap(hdr() + bdy(build_body(c) + feedback_widget(
        candidate_name = c['full_name'],
        role           = ROLE,
        app_id         = c['app_id'],
        email_type     = 'Application Feedback'
    )))

Responses log silently to: Noah — Candidate Feedback (Google Sheet, Jawwad owns it).
Tagged by role — Coco and Noah responses are separable in the sheet.
"""

from urllib.parse import quote

SCRIPT_URL = (
    "https://script.google.com/a/macros/taleemabad.com/s/"
    "AKfycbzgIVzBfZRLLTHQsuTDHSwQXsaT0ZbHEWL220sBK5Nuy8HwvLZS3FWbdqA4rjtpNFL3/exec"
)


def feedback_widget(candidate_name: str, role: str, app_id, email_type: str) -> str:
    """
    Returns an HTML block to append inside the email body.
    Logs one-tap candidate responses to the shared Google Sheet.

    Parameters
    ----------
    candidate_name : str   — candidate's full name (logged to Sheet)
    role           : str   — role title, e.g. 'Field Coordinator'
    app_id         : int   — Markaz application ID
    email_type     : str   — label for the email type, e.g. 'Application Feedback'
    """

    def enc(s):
        return quote(str(s), safe="")

    base = (
        f"{SCRIPT_URL}"
        f"?candidate={enc(candidate_name)}"
        f"&role={enc(role)}"
        f"&app_id={enc(app_id)}"
        f"&email_type={enc(email_type)}"
    )

    def score_btn(n):
        return (
            f'<a href="{base}&score={n}" target="_blank" '
            f'style="display:inline-block;width:36px;height:36px;line-height:36px;'
            f'text-align:center;background:#ffffff;border:1.5px solid #1565c0;'
            f'border-radius:5px;color:#1565c0;font-family:Georgia,serif;'
            f'font-size:14px;font-weight:bold;text-decoration:none;margin:0 4px;">'
            f"{n}</a>"
        )

    def tag_btn(q, t):
        return (
            f'<a href="{base}&q={enc(q)}&tag={enc(t)}" target="_blank" '
            f'style="display:inline-block;padding:6px 13px;background:#ffffff;'
            f'border:1px solid #dfe6e9;border-radius:14px;color:#636e72;'
            f'font-family:Georgia,serif;font-size:12px;text-decoration:none;margin:4px 3px;">'
            f"{t}</a>"
        )

    divider = '<div style="width:40px;height:1px;background:#e8f0fe;margin:16px auto;"></div>'

    score_btns   = "".join(score_btn(n) for n in range(1, 6))
    personal_btns = "".join(tag_btn("personal", t) for t in ["Yes, personal", "Somewhat", "No, felt generic"])
    useful_btns   = "".join(tag_btn("useful",   t) for t in ["Very useful", "Somewhat", "Not really"])

    return f"""
    <div style="margin-top:36px;padding:24px 28px 22px;background:#f7f9fc;
                border-top:2px solid #e8f0fe;text-align:center;">

      <p style="font-family:Georgia,serif;font-size:12px;font-weight:bold;
                color:#1565c0;margin:0 0 18px;letter-spacing:1px;text-transform:uppercase;">
        Be honest. We can take it.
      </p>

      <!-- Q1 -->
      <p style="font-family:Georgia,serif;font-size:14px;color:#1a1a1a;margin:0 0 10px;">
        How did this land for you?
      </p>
      <div style="margin-bottom:4px;">
        {score_btns}
      </div>
      <p style="font-family:Georgia,serif;font-size:10px;color:#b2bec3;margin:4px 0 0;">
        1 = missed the mark &nbsp;&nbsp; 5 = really landed
      </p>

      {divider}

      <!-- Q2 -->
      <p style="font-family:Georgia,serif;font-size:14px;color:#1a1a1a;margin:0 0 10px;">
        Did it feel written for you specifically?
      </p>
      <div>
        {personal_btns}
      </div>

      {divider}

      <!-- Q3 -->
      <p style="font-family:Georgia,serif;font-size:14px;color:#1a1a1a;margin:0 0 10px;">
        Was the feedback useful?
      </p>
      <div>
        {useful_btns}
      </div>

    </div>"""
