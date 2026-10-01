"""Rendering the joining email into the locked Design 3 layout.

CLAUDE.md Rule 15: Design 3 is the standard for every contract-related email,
and design is not content. The layout comes from the template file; the
wording comes from `joining_email.SITUATIONS` and the skill, and only names,
dates, duration and amount change.

🔴 AN UNFILLED SLOT IS A REFUSAL, NOT A BLANK. The template fails loudly on a
   `{{VARIABLE}}` nobody supplied, because a joining email that renders an
   empty compensation row looks finished and is not.

🔴 BOTH LINKS, ALWAYS, AND THE FORM FOLLOWS THE ENTITY (Ayesha 2026-10-01).
   The buttons are template variables, so a missing one fails here rather than
   reaching an inbox. Both 12 September permanent sends went out with neither.

🔴 NO WEEKDAY IN A DATE, AND THE THINGS THEY ACT ON ARE BOLD. The detail rows
   carry the start date, the compensation and the commitment, and the table
   markup bolds the value column, which is what satisfies the rule rather than
   anybody remembering it.
"""

from __future__ import annotations

import os
import re
from typing import Optional

from . import joining_email as je

SERIF = "Georgia,'Times New Roman',serif"
SANS = "Arial,Helvetica,sans-serif"

LINKEDIN_URL = "https://www.linkedin.com/in/ayesha-raza-khan-386668177/"
PHONE_DISPLAY = "+92 335 4288844"
PHONE_TEL = "+923354288844"

#: The three "what your journey looks like" cards. Fixed copy.
JOURNEY = (
    ("shield", "#e8f4ec", "Make an Impact",
     "Empower educators and shape the future."),
    ("users", "#e9eefb", "Grow Together",
     "Learn, share, and grow with an amazing team."),
    ("heart", "#efecfa", "Do Work That Matters",
     "Every day here creates lasting change."),
)

#: "A Few Important Things to Know". The authenticity clause is locked wording
#: and is never softened; the others vary by situation.
IMPORTANT_AUTHENTICITY = (
    "shield", "Documents must be authentic and verifiable.",
    "Any false information may result in termination or appropriate action.")
IMPORTANT_PROBATION = (
    "probation", "Probation:",
    "This role is subject to a three-month probationary period to assess "
    "performance and suitability.")
IMPORTANT_COMMUTE = (
    "commute", "Commute support:",
    "Home to schools and schools to office will be covered via hub car or a "
    "commute allowance. Office to home will not be covered.")


class RenderError(ValueError):
    """The email cannot be rendered as asked."""


def _rows(details: list[tuple[str, str, str]]) -> str:
    out = []
    for i, (icon, label, value) in enumerate(details):
        border = "" if i == len(details) - 1 else "border-bottom:1px solid #edf0f6;"
        nowrap = "" if label == "Commitment" else "white-space:nowrap;"
        out.append(
            f'<tr><td width="46" valign="middle" style="padding:14px 0;{border}">'
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0">'
            f'<tr><td width="34" height="34" align="center" valign="middle" '
            f'style="background:#eef2fb;border-radius:17px;">'
            f'<img src="cid:ic_{icon}" width="18" height="18" alt="" '
            f'style="display:block;border:0;"></td></tr></table></td>'
            f'<td class="dlabel" valign="middle" style="padding:14px 0;{border}'
            f'font-family:{SANS};font-size:10.5px;letter-spacing:1.1px;'
            f'text-transform:uppercase;color:#7c8aa5;">{label}</td>'
            f'<td class="dval" align="right" valign="middle" style="padding:14px 0;{border}'
            f'font-family:{SANS};font-size:14.5px;color:#111827;font-weight:bold;'
            f'{nowrap}">{value}</td></tr>'
        )
    return "".join(out)


def _journey() -> str:
    out = []
    for i, (icon, bg, title, text) in enumerate(JOURNEY):
        pad = "0" if i == len(JOURNEY) - 1 else "0 0 16px 0"
        out.append(
            f'<tr><td width="42" valign="top" style="padding:{pad};">'
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0">'
            f'<tr><td width="32" height="32" align="center" valign="middle" '
            f'style="background:{bg};border-radius:16px;">'
            f'<img src="cid:ic_{icon}" width="17" height="17" alt="" '
            f'style="display:block;border:0;"></td></tr></table></td>'
            f'<td valign="top" style="padding:{pad};">'
            f'<div style="font-family:{SANS};font-size:13.5px;font-weight:bold;'
            f'color:#111827;margin-bottom:3px;">{title}</div>'
            f'<div style="font-family:{SERIF};font-size:13px;line-height:1.6;'
            f'color:#5b6b7c;">{text}</div></td></tr>'
        )
    return "".join(out)


def _important(items: list[tuple[str, str, str]]) -> str:
    out = []
    for i, (icon, title, text) in enumerate(items):
        pad = "0" if i == len(items) - 1 else "0 0 16px 0"
        out.append(
            f'<tr><td width="34" valign="top" style="padding:{pad};">'
            f'<img src="cid:ic_{icon}" width="18" height="18" alt="" '
            f'style="display:block;border:0;margin-top:2px;"></td>'
            f'<td valign="top" style="padding:{pad};font-family:{SERIF};'
            f'font-size:13px;line-height:1.65;color:#5b6b7c;">'
            f'<b style="color:#111827;">{title}</b> {text}</td></tr>'
        )
    return "".join(out)


def _paragraph(text: str) -> str:
    return (
        f'<p class="just" style="margin:0 0 24px 0;font-family:{SERIF};'
        f'font-size:16px;line-height:1.75;color:#374151;text-align:justify;">'
        f"{text}</p>"
    )


def _sender_contact() -> str:
    bits = [
        f'M: <a href="tel:{PHONE_TEL}" style="color:#2f4fa2;'
        f'text-decoration:none;">{PHONE_DISPLAY}</a>',
        f'<a href="{LINKEDIN_URL}" target="_blank" style="color:#2f4fa2;'
        f'text-decoration:none;font-weight:bold;">LinkedIn</a>',
    ]
    joined = '<span style="color:#c3cbd6;">&nbsp;|&nbsp;</span>'.join(bits)
    return (f'<div style="font-family:{SANS};font-size:13px;color:#6b7280;'
            f'margin-top:7px;">{joined}</div>')


def render(
    *,
    engagement: str,
    entity: str,
    first_name: str,
    role: str,
    start_date: str,
    end_date: Optional[str] = None,
    compensation: Optional[str] = None,
    commitment: str = "Five days &middot; 40 hours per week",
    project_name: Optional[str] = None,
    returning: bool = False,
    sender_name: str = "Ayesha Raza Khan",
    sender_title: str = "Deputy Manager People &amp; Culture",
) -> str:
    """The finished HTML. Raises rather than leaving a slot unfilled."""
    situation = je.situation_for(engagement)
    path = os.path.join(je.TEMPLATE_DIR, situation["template"])
    if not os.path.isfile(path):
        raise RenderError(f"the template {situation['template']} is missing")
    html = open(path, encoding="utf-8").read()

    project = project_name or situation.get("project") or ""
    unpaid = bool(situation.get("no_compensation"))

    details = [("role", "Role", role), ("calendar", "Start date", start_date)]
    if end_date:
        details.append(("calendar_end", "Contract runs to", end_date))
    # 🔴 An unpaid fellowship has no compensation row at all. Printing one with
    #    a blank or a zero reads as a mistake, and printing a figure would be
    #    a promise nobody made.
    if not unpaid:
        if not compensation:
            raise RenderError(
                f"{situation['label']} is a paid engagement and no compensation "
                "was given. A joining email with an empty compensation row "
                "looks finished and is not."
            )
        details.append(("wallet", "Monthly compensation", compensation))
    details.append(("clock", "Commitment", commitment))

    important = [IMPORTANT_AUTHENTICITY, IMPORTANT_PROBATION]
    if project.upper() == "NIETE":
        important.append(IMPORTANT_COMMUTE)

    values = {
        "CANDIDATE_FIRST_NAME": first_name,
        "ROLE": role,
        "PROJECT_NAME": project,
        "PARTNER_NAME": "Orenda",
        "EYEBROW": (project or "Taleemabad").upper(),
        "START_DATE": start_date,
        "CONTRACT_END_DATE": end_date or "",
        "COMPENSATION": compensation or "",
        "COMMITMENT": commitment,
        "SENDER_NAME": sender_name,
        "SENDER_TITLE": sender_title,
        "SENDER_CONTACT": _sender_contact(),
        "DETAIL_ROWS": _rows(details),
        "JOURNEY_ITEMS": _journey(),
        "IMPORTANT_ITEMS": _important(important),
        "ATTACHMENT_NOTE": (
            f'Please find the <b style="color:#111827;">{situation["attachments"]}'
            f"</b> attached to this email."
        ),
        "RETURNING_SENTENCE": _paragraph(
            "We truly value the experience and insight you bring as a returning "
            "team member and are confident that you will continue to make "
            "meaningful contributions to our mission."
        ) if returning else "",
        "WELCOME_EXTRA": "",
        "CLOSING_EXTRA": "",
        "CLOSING_WELCOME": _paragraph(
            "Welcome to the team! We&#39;re excited to have you onboard. If you "
            "have any questions or concerns, please don&#39;t hesitate to reach "
            "out to the People &amp; Culture team."
        ),
        "BUTTONS": "",
    }
    # Both links, with the form chosen by entity. Raises for an entity whose
    # form nobody has given us.
    values.update(je.links_for(entity))

    # Two passes: DETAIL_ROWS itself contains {{ROLE}} and friends.
    for _ in range(2):
        for key, value in values.items():
            html = html.replace("{{" + key + "}}", str(value))

    leftover = sorted(set(re.findall(r"\{\{([A-Z_]+)\}\}", html)))
    if leftover:
        raise RenderError(
            "The template has slots nobody filled: " + ", ".join(leftover)
            + ". An email that renders a blank row looks finished and is not."
        )
    return html
