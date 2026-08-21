"""
v8_template.py — Canonical layout for ALL candidate communication emails
========================================================================
SINGLE SOURCE OF TRUTH for the visual layout of every Skill 01 candidate
communication email: CV rejection, values feedback, warm bench feedback,
GWC rejection, and any future candidate-communication type.

Locked by Ayesha 2026-06-10 (she approved the Syeda Siddiqa Fatima values
feedback email and asked that its exact layout become the standard).

Spec doc: memory/v8_candidate_comms_layout_LOCKED.md
Tone/content rules (separate from layout): memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md

WHAT THIS MODULE OWNS:  font, colors, card, spacing, header, footer, P.S. box.
WHAT IT DOES NOT OWN:   section headings + content rules (these differ per
                        email type and are enforced by the eval harness).

DO NOT redefine H/SUB/P/PS or the card/header/footer inline in a script.
Import them from here so the layout can never drift.

Usage
-----
    from scripts.utils.v8_template import H, SUB, P, PS, wrap, attach_logo, EYEBROW
    from scripts.utils.feedback_widget import feedback_widget

    body = (
        P("Dear ...") +
        H("What We Liked Most About You") + P("...") +
        H("Where We Found Ourselves Sitting With Questions") + SUB("...") + P("...") +
        H("What We Think You Should Do Next") + P("...") +
        PS("<strong>P.S.</strong> ...") +
        feedback_widget(name, role, app_id, "Application Feedback")
    )
    html = wrap(subject_line=SUBJECT, role="CPD Coach",
                eyebrow=EYEBROW["values_feedback"], body_html=body)

    # In the MIMEMultipart("related") message:
    attach_logo(msg)   # embeds assets/logo_taleemabad.png as cid:taleemabad_logo
"""

import os
from email.mime.image import MIMEImage

# ── LOCKED PALETTE ────────────────────────────────────────────────────────────
BLUE       = "#1565c0"   # headings, title, links, header divider
GREEN      = "#1b5e20"   # SUB subheadings + P.S. left border
TEXT       = "#1a1a1a"   # body text
PAGE_BG    = "#f0f4f0"   # canvas behind the card
PS_BG      = "#f1f8e9"   # P.S. box background
SUBTITLE   = "#5c85c7"   # role subtitle under the title

LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "logo_taleemabad.png")

# ── HEADER EYEBROW TEXT (per type) ──────────────────────────────────────────────
# Small uppercase context line under the logo. Candidate-facing: NO internal
# jargon (never "GWC"/"KCD"/"scorecard").
EYEBROW = {
    "cv_rejection":    "People &amp; Culture &nbsp;&bull;&nbsp; Application Update",
    "values_feedback": "People &amp; Culture &nbsp;&bull;&nbsp; Values Interview",
    "warm_bench":      "People &amp; Culture &nbsp;&bull;&nbsp; Application Update",
    "gwc_rejection":   "People &amp; Culture &nbsp;&bull;&nbsp; Application Update",
    "warm_hold":       "People &amp; Culture &nbsp;&bull;&nbsp; Interview Update",
    "case_study_update": "People &amp; Culture &nbsp;&bull;&nbsp; Interview Update",
    # INTERNAL audience (Skill 01 type #7) - staff, not candidates.
    "announcement":    "People &amp; Culture &nbsp;&bull;&nbsp; Internal Announcement",
}

# ── BODY HELPERS (v8 design) ────────────────────────────────────────────────────
H   = lambda t: f'<h2 style="color:{BLUE};font-size:17px;font-weight:bold;margin:36px 0 6px 0;letter-spacing:0.3px;">{t}</h2>'
SUB = lambda t: f'<p style="color:{GREEN};font-weight:bold;margin:0 0 14px 0;font-size:14px;">{t}</p>'
P   = lambda t: f'<p style="margin:0 0 18px 0;text-align:justify;font-family:Georgia,serif;font-size:15px;line-height:1.8;">{t}</p>'
PS  = lambda t: f'<p style="margin:32px 0 0 0;padding:20px 24px;background:{PS_BG};border-left:4px solid {GREEN};font-style:italic;color:#2a2a2a;font-size:14px;line-height:1.7;font-family:Georgia,serif;">{t}</p>'

# Bulleted list. Added 2026-08-20 for the Internal Announcement type (#7), which
# lists criteria and role facts. Same Georgia/leading as P, left-aligned (a
# justified list reads badly). Shared here so no script redefines it inline.
UL  = lambda items: (
    '<ul style="margin:0 0 18px 0;padding-left:22px;font-family:Georgia,serif;'
    'font-size:15px;line-height:1.8;color:' + TEXT + ';">'
    + "".join(f'<li style="margin:0 0 6px 0;">{i}</li>' for i in items)
    + "</ul>"
)

# Left-aligned paragraph (P is justified). For short lines and lead-ins where
# justification would stretch the words apart.
PL  = lambda t: f'<p style="margin:0 0 18px 0;text-align:left;font-family:Georgia,serif;font-size:15px;line-height:1.8;">{t}</p>'

FOOTER = f"""
<table width="100%" cellpadding="0" cellspacing="0"
       style="margin-top:40px;border-top:1px solid #e0e0e0;padding-top:20px;">
  <tr>
    <td style="font-family:Georgia,serif;font-size:13px;color:#555;line-height:1.9;">
      Warm regards,<br>
      <strong style="color:#1a1a1a;">People and Culture Team</strong><br>
      <strong style="color:{BLUE};">Taleemabad</strong><br>
      <a href="mailto:hiring@taleemabad.com"
         style="color:{BLUE};text-decoration:none;">hiring@taleemabad.com</a>
      &nbsp;|&nbsp;
      <a href="http://www.taleemabad.com"
         style="color:{BLUE};text-decoration:none;">www.taleemabad.com</a><br>
    </td>
  </tr>
</table>"""


def header_block(subject_line, role, eyebrow):
    """White header: centered embedded logo, uppercase eyebrow, title, role subtitle, blue divider."""
    return f"""
<table width="100%" cellpadding="0" cellspacing="0"
       style="border-radius:8px 8px 0 0;overflow:hidden;border-bottom:2px solid {BLUE};">
  <tr>
    <td align="center" bgcolor="#ffffff"
        style="background-color:#ffffff;padding:28px 40px 22px 40px;">
      <img src="cid:taleemabad_logo" height="38" alt="Taleemabad"
           style="display:block;margin:0 auto 14px auto;">
      <p style="margin:0;font-family:Georgia,serif;font-size:11px;
                color:{BLUE};letter-spacing:2px;text-transform:uppercase;">
        {eyebrow}
      </p>
      <p style="margin:10px 0 4px 0;font-family:Georgia,serif;font-size:17px;
                font-weight:bold;color:{BLUE};line-height:1.4;">
        {subject_line}
      </p>
      <p style="margin:0;font-family:Georgia,serif;font-size:12px;color:{SUBTITLE};">
        {role}
      </p>
    </td>
  </tr>
</table>"""


def wrap(subject_line, role, eyebrow, body_html):
    """Full HTML document: 620px card on #f0f4f0 canvas, header + body, Georgia serif."""
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background-color:{PAGE_BG};">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background-color:{PAGE_BG};padding:32px 0;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0"
             style="max-width:620px;border-radius:8px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);">
        <tr><td>{header_block(subject_line, role, eyebrow)}</td></tr>
        <tr>
          <td style="background:#ffffff;padding:40px 52px 48px 52px;
                     border-radius:0 0 8px 8px;
                     font-family:Georgia,serif;font-size:15px;
                     line-height:1.8;color:{TEXT};">
            {body_html}
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


def attach_logo(msg, path=None):
    """Embed the Taleemabad logo as cid:taleemabad_logo on a MIMEMultipart('related') message."""
    p = path or LOGO_PATH
    if os.path.exists(p):
        with open(p, "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", "<taleemabad_logo>")
        img.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
        msg.attach(img)
        return True
    return False
