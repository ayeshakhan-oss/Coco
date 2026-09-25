"""Renders the seven invite types into the LOCKED interview-invite design.

SOURCE OF TRUTH FOR THE DESIGN:
memory/locked_email_template_interview_invites_FINAL_2026_05_13.md, as it is
actually built in scripts/jobs/job39/send_growth_manager_invites_batch.py.
The structure here is a port of that HTML, not a new design.

SOURCE OF TRUTH FOR THE WORDING:
.claude/skills/06_candidate-invites/SKILL.md, which records what Ayesha
approved per type, including the assessment centre (locked verbatim
2026-07-31) and the two types that forbid a call-to-action.

🔒 DESIGN IS 100% LOCKED. ONLY CONTENT CHANGES. Colours, the 775px card, the
   Georgia stack, the 34px CID logo, the 2px #4b67d1 divider and the signature
   block are fixed. `ui-ux-pro-max` does not apply to them (CLAUDE.md Rule 9).

🔴 A MISSING FIELD IS A REFUSAL, NOT A PLACEHOLDER. `render` raises rather than
   emitting "[POSITION]" or an empty href. An invite with a dead booking button
   strands the candidate, and a visible placeholder in a live email is worse
   than no email. Every type declares what it needs in REQUIRED.

⚠️ KNOWN, DELIBERATELY NOT FIXED HERE: the locked shell carries
   `width="775" style="width:775px"` on the card, which CLAUDE.md Rule 16 (from
   2026-08-14, after this design was locked in May) forbids because a phone
   then zooms out instead of reflowing. Changing a locked candidate-facing
   design is Ayesha's call, not this module's, so the port is faithful and the
   conflict is reported rather than silently resolved.
"""

from __future__ import annotations

import html

from .invites import INVITE_TYPES, InviteError

# --------------------------------------------------------------------------
# What each type must be given before it can be rendered
# --------------------------------------------------------------------------

#: Fields every type needs.
_COMMON = ("first_name", "position")

REQUIRED: dict[str, tuple[str, ...]] = {
    "values_interview": _COMMON + ("jd_url", "prep_url", "booking_url"),
    "case_study_debrief": _COMMON + ("booking_url",),
    "exploratory_call": _COMMON + ("booking_url", "context"),
    "warm_bench_opportunity": _COMMON + ("booking_url", "previous_role"),
    "keep_in_touch": _COMMON,
    # Date and time are required and must come from the calendar event or the
    # booking email. The Meet link is optional on purpose: a wrong link
    # strands the candidate, so no verified link means no button.
    "interview_reminder": _COMMON + ("interview_date", "interview_time"),
    # Ayesha supplies the venue and the Maps link per batch. Never sourced here.
    "assessment_center": _COMMON + (
        "activity_date", "start_time", "end_time", "venue", "confirm_by_date",
    ),
}

#: Header label, title and (where there is one) button text, per type.
CHROME = {
    "values_interview": {
        "label": "TALENT ACQUISITION • VALUES INTERVIEW",
        "title": "Invitation for the Values Interview",
        "button": "\U0001f4c5 Book your Interview",
        "subject": "Values Interview for {position} - {full_name}",
    },
    "case_study_debrief": {
        "label": "TALENT ACQUISITION • CASE STUDY DEBRIEF",
        "title": "Invitation for the Case Study Debrief",
        "button": "\U0001f4c5 Schedule Your Debrief",
        "subject": "Case Study Debrief for {position} - {full_name}",
    },
    "exploratory_call": {
        "label": "TALENT ACQUISITION • EXPLORATORY CALL",
        "title": "An Invitation to Talk",
        "button": "\U0001f4c5 Let us Chat",
        "subject": "An exploratory conversation about {position} - {full_name}",
    },
    "warm_bench_opportunity": {
        "label": "TALENT ACQUISITION • NEW OPPORTUNITY",
        "title": "A New Opportunity at Taleemabad",
        "button": "\U0001f4c5 Let us Discuss",
        "subject": "A new opening that made us think of you - {full_name}",
    },
    "keep_in_touch": {
        "label": "TALENT ACQUISITION • A NOTE FROM OUR SIDE",
        "title": "Still Very Much in Our Thinking",
        "button": None,
        "subject": "Still very much in our thinking - {full_name}",
    },
    "interview_reminder": {
        "label": "TALENT ACQUISITION • INTERVIEW REMINDER",
        "title": "Your Interview is Tomorrow",
        "button": "\U0001f3a5 Join your Interview",
        "subject": "Reminder: Your Interview for {position} is Tomorrow",
    },
    "assessment_center": {
        "label": "TALENT ACQUISITION • ASSESSMENT CENTER ACTIVITY",
        "title": "Invitation to Our Assessment Center Activity",
        "button": None,
        "subject": "Invitation to the Assessment Center Activity for {position} - {full_name}",
    },
}

#: The one line every recorded virtual conversation carries. Not on the
#: assessment centre, which is onsite, and not on a keep-in-touch note.
_RECORDING = ("This session will be recorded. By joining, you consent to being "
              "part of the recorded call.")

_IMPACT = "https://impact-microsite.vercel.app/"


def missing_fields(invite_type: str, ctx: dict) -> list[str]:
    if invite_type not in REQUIRED:
        raise InviteError(f"unknown invite type {invite_type!r}")
    return [f for f in REQUIRED[invite_type] if not str(ctx.get(f) or "").strip()]


def subject_for(invite_type: str, ctx: dict) -> str:
    chrome = CHROME[invite_type]
    return chrome["subject"].format(
        position=ctx.get("position", ""),
        full_name=ctx.get("full_name") or ctx.get("first_name", ""),
    ).strip()


# --------------------------------------------------------------------------
# Body content, per type
# --------------------------------------------------------------------------

def _e(value) -> str:
    """Escape anything a person typed before it goes near the HTML.

    A candidate called O'Brien and a role written with an ampersand are both
    ordinary, and neither should be able to break the markup.
    """
    return html.escape(str(value or ""), quote=True)


def _p(text: str, cls: str = "", style: str = "") -> str:
    attrs = (f' class="{cls}"' if cls else "") + (f' style="{style}"' if style else "")
    return f"<p{attrs}>{text}</p>"


def _body(invite_type: str, ctx: dict) -> str:
    """The paragraphs between the divider and the call-to-action."""
    name = _e(ctx.get("first_name"))
    pos = _e(ctx.get("position"))
    out = [_p(f"Hi {name},", style="margin-bottom:30px;")]

    if invite_type == "values_interview":
        out += [
            _p(f"Thank you for your interest in the <strong>{pos}</strong> role "
               "at Taleemabad. We have reviewed your application and would like "
               "to invite you for a <strong>45-minute values conversation</strong> "
               "with our team, to learn more about you and how your persona "
               "aligns with Taleemabad values."),
            _p(f'The JD for this position is <a href="{_e(ctx["jd_url"])}">'
               "available here</a>. You can also explore more about Taleemabad "
               "and our work:"),
            f'<ul><li><a href="{_IMPACT}">10 Years Of Impact - Taleemabad</a></li></ul>',
            _p(f'Please go through the <a href="{_e(ctx["prep_url"])}">interview '
               "prep guide</a> to understand what to expect from this conversation."),
            _p(_RECORDING, cls="callout"),
            _p("Let us know if you have any questions ahead of the interview. We "
               "look forward to speaking with you."),
        ]

    elif invite_type == "case_study_debrief":
        out += [
            _p("Thank you for completing the case study. We have read your "
               f"submission for the <strong>{pos}</strong> role and would like to "
               "invite you for a <strong>30-minute debrief</strong> with our team, "
               "to talk through your approach and the thinking behind it."),
            _p("This is a conversation about your work rather than a test of it. "
               "There is nothing to prepare."),
            _p(_RECORDING, cls="callout"),
            _p("Let us know if you have any questions ahead of the debrief. We "
               "look forward to speaking with you."),
        ]

    elif invite_type == "exploratory_call":
        out += [
            _p(_e(ctx["context"])),
            f'<ul><li><a href="{_IMPACT}">10 Years Of Impact - Taleemabad</a></li></ul>',
            _p("We would like to invite you for a <strong>20-minute exploratory "
               "conversation</strong>. There is no application attached to it and "
               "nothing to prepare. It is a chance for us to hear what you are "
               f"working on, and for you to hear what we are building in {pos}."),
            _p(_RECORDING, cls="callout"),
            _p("If the timing is not right, simply reply and tell us so. We look "
               "forward to speaking with you."),
        ]

    elif invite_type == "warm_bench_opportunity":
        out += [
            _p("We spoke with you earlier about the "
               f"<strong>{_e(ctx['previous_role'])}</strong> role. That process "
               "closed with someone else, and we have kept you in mind since."),
            _p(f"A new opening has come up, <strong>{pos}</strong>, and it aligns "
               "with the strengths we saw in those conversations. We would like "
               "to talk with you about it."),
        ]
        if str(ctx.get("context") or "").strip():
            out.append(_p(_e(ctx["context"])))
        out += [
            _p(_RECORDING, cls="callout"),
            _p("If you are not looking at the moment, simply reply and tell us "
               "so. We would still be glad to know."),
        ]

    elif invite_type == "keep_in_touch":
        # 🔒 NO links, NO booking button, NO promise and NO date. The candidate
        # must have nothing to count on.
        out += [
            _p("Thank you again for the conversation about the "
               f"<strong>{pos}</strong> role. It has stayed with us."),
            _p("We are revisiting how the role is shaped, and that is taking us "
               "longer than we would like. We did not want the quiet to read as "
               "a decision, because it is not one. You are still very much in "
               "our thinking."),
            _p("When we have more clarity, we would genuinely welcome the chance "
               "to be back in touch."),
        ]
        if str(ctx.get("context") or "").strip():
            out.append(_p(_e(ctx["context"])))

    elif invite_type == "interview_reminder":
        out += [
            _p("A short note to remind you that your interview for the "
               f"<strong>{pos}</strong> role is tomorrow."),
            _p(f"{_e(ctx['interview_date'])}, {_e(ctx['interview_time'])}",
               cls="callout"),
            _p(_RECORDING, cls="callout"),
            _p("If anything has come up and the time no longer works, simply "
               "reply to this email and we will find another slot. We look "
               "forward to speaking with you."),
        ]
        # Rule: never fabricate the Meet link. No verified link, no button.
        if not str(ctx.get("meet_url") or "").strip():
            out.append(_p("You can join using the Google Meet link in your "
                          "calendar invitation."))

    elif invite_type == "assessment_center":
        # Wording locked by Ayesha 2026-07-31. Onsite, so no recording line and
        # no Meet link.
        venue = _e(ctx["venue"])
        if str(ctx.get("maps_url") or "").strip():
            venue += (f' &mdash; <a href="{_e(ctx["maps_url"])}">view on Google '
                      "Maps</a>")
        out += [
            _p("Congratulations on making it to the next stage of our recruitment "
               "process! We are excited to invite you to our Assessment Center "
               "Activity."),
            _p("The activity will take place onsite on "
               f"<strong>{_e(ctx['activity_date'])}</strong>, starting promptly at "
               f"<strong>{_e(ctx['start_time'])}</strong> and continuing until "
               f"<strong>{_e(ctx['end_time'])}</strong>. Please plan to arrive on "
               "time so we can begin together."),
            _p(f"<strong>Venue:</strong> {venue}."),
            _p("If you are joining us from outside Islamabad, please let us know "
               "by replying to this email so we can coordinate accordingly."),
            _p("To confirm your attendance, kindly reply to this email with your "
               "acknowledgement. We will send the Google Calendar invitation by "
               f"<strong>{_e(ctx['confirm_by_date'])}</strong> to the candidates "
               "who have confirmed.", cls="callout"),
            _p("We look forward to meeting you and wish you the very best for this "
               "stage of the process. If you have any questions, please feel free "
               "to reach out."),
        ]

    return "\n".join(out)


def _cta(invite_type: str, ctx: dict) -> str:
    """The purple button, where the type has one and the link exists."""
    chrome = CHROME[invite_type]
    if not chrome["button"]:
        return ""
    url = (ctx.get("meet_url") if invite_type == "interview_reminder"
           else ctx.get("booking_url"))
    if not str(url or "").strip():
        return ""
    subtitle = (
        "The link will also be in your calendar invitation."
        if invite_type == "interview_reminder"
        else "Please book a slot at your earliest convenience."
    )
    return (
        '\n                                        <div style="text-align:center; margin:40px 0 28px 0;">\n'
        f'                                            <a href="{_e(url)}" style="background:#5b3fc4; '
        "color:#ffffff; font-size:16px; font-weight:700; "
        "font-family:Georgia,Cambria,'Times New Roman',serif; text-decoration:none; "
        'border-radius:7px; padding:14px 34px; display:inline-block; text-align:center;">'
        f'{chrome["button"]}</a>\n'
        "                                        </div>\n\n"
        f'                                        <p class="button-subtitle">{subtitle}</p>'
    )


def _signature(invite_type: str) -> str:
    """The locked signature, plus Ayesha's block on the assessment centre only."""
    extra = ""
    if invite_type == "assessment_center":
        # Added for this type by Ayesha, 2026-07-31.
        extra = (
            '\n                                        <p style="font-size:16px; line-height:1.7; color:#2f5fc7; margin:0 0 4px 0;">\n'
            '                                            <a href="https://www.linkedin.com/in/ayesha-raza-khan-386668177/" '
            'style="color:#2f5fc7; text-decoration:underline;"><strong>Ayesha Raza Khan</strong></a>\n'
            "                                        </p>\n\n"
            '                                        <p style="font-size:16px; line-height:1.7; color:#5c5c5c; margin:0 0 18px 0;">03354288844</p>'
        )
    return (
        '\n                                        <div style="border-top:1px solid #d9d9d9; margin-top:22px; margin-bottom:28px;"></div>\n\n'
        '                                        <p style="font-size:16px; color:#5c5c5c; line-height:1.7; margin:0 0 10px 0; font-weight:400;">Warm regards,</p>\n\n'
        '                                        <p style="font-size:18px; font-weight:700; color:#111111; line-height:1.6; margin:0 0 6px 0;">People and Culture Team</p>\n\n'
        '                                        <p style="font-size:18px; font-weight:700; color:#2f5fc7; line-height:1.6; margin:0 0 10px 0;">Taleemabad</p>\n\n'
        '                                        <p style="font-size:16px; line-height:1.7; color:#2f5fc7; margin:0 0 18px 0;">\n'
        '                                            <a href="mailto:hiring@taleemabad.com" style="color:#2f5fc7; text-decoration:underline;">hiring@taleemabad.com</a> '
        '<span style="color:#7d7d7d; margin:0 10px;">|</span> '
        '<a href="https://www.taleemabad.com" style="color:#2f5fc7; text-decoration:underline;">www.taleemabad.com</a>\n'
        "                                        </p>" + extra
    )


_SHELL = """<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #f5f5f5;
            font-family: Georgia, Cambria, "Times New Roman", serif;
        }}
        a {{
            color: #3d63c8;
            text-decoration: underline;
        }}
        p {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 17px;
            line-height: 1.85;
            color: #111111;
            font-weight: 400;
            margin: 0 0 26px 0;
        }}
        strong {{
            font-weight: 700;
        }}
        ul {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            margin: 0 0 26px 0;
            padding-left: 50px;
        }}
        li {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 17px;
            line-height: 1.85;
            color: #111111;
        }}
        .callout {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 17px;
            line-height: 1.85;
            font-weight: 700;
            color: #3d63c8;
            margin: 26px 0 26px 0;
        }}
        .button-subtitle {{
            font-family: Georgia, Cambria, "Times New Roman", serif;
            font-size: 16px;
            line-height: 1.6;
            color: #111111;
            text-align: center;
            margin: 18px 0 0 0;
        }}
    </style>
</head>
<body>
    <table width="100%" bgcolor="#f5f5f5" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center">
                <table width="calc(100% - 90px)" bgcolor="#e5e7e2" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
                    <tr>
                        <td align="center" style="padding-top:38px; padding-bottom:38px;">
                            <table width="775" bgcolor="#ffffff" cellpadding="0" cellspacing="0" border="0" style="width:775px; max-width:775px; margin:0 auto;">
                                <!-- Header -->
                                <tr>
                                    <td style="padding:34px 64px 30px 64px; text-align:center;">
                                        <div style="margin-bottom:16px;">
                                            <img src="cid:taleemabad_logo" alt="Taleemabad" width="34" height="34" style="width:34px; height:auto;">
                                        </div>

                                        <div style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:12px; letter-spacing:2.4px; font-weight:500; text-transform:uppercase; color:#3157b7; line-height:1.4; margin:0 0 18px 0;">
                                            {label}
                                        </div>

                                        <h1 style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:24px; line-height:1.2; font-weight:700; color:#3157b7; margin:0 0 10px 0; text-align:center;">
                                            {title}
                                        </h1>

                                        <p style="font-family:Georgia,Cambria,'Times New Roman',serif; font-size:13px; line-height:1.5; color:#5d73b8; text-align:center; margin:0; font-weight:400;">
                                            {position}
                                        </p>
                                    </td>
                                </tr>

                                <!-- Divider -->
                                <tr>
                                    <td style="border-top:2px solid #4b67d1; height:0; padding:0; margin:0;"></td>
                                </tr>

                                <!-- Body Content -->
                                <tr>
                                    <td style="padding:44px 64px 52px 64px; text-align:left;">
                                        {body}
{cta}
                                    </td>
                                </tr>

                                <!-- Signature -->
                                <tr>
                                    <td style="padding:0 64px 52px 64px; text-align:left; font-family:Georgia,Cambria,'Times New Roman',serif;">
{signature}
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""


def render(invite_type: str, ctx: dict) -> str:
    """The full email. Raises InviteError rather than emitting a placeholder."""
    if invite_type not in CHROME:
        raise InviteError(f"unknown invite type {invite_type!r}")

    gaps = missing_fields(invite_type, ctx)
    if gaps:
        label = INVITE_TYPES[invite_type]["label"]
        raise InviteError(
            f"{label} cannot be rendered: missing {', '.join(gaps)}. These are "
            "not optional, and an invite that ships a placeholder or a dead "
            "link is worse than one not sent."
        )

    # A booking link on a type that forbids one would be a design change, not a
    # content one. Refuse rather than quietly dropping it, so the operator
    # learns the type does not work that way.
    if CHROME[invite_type]["button"] is None and str(ctx.get("booking_url") or "").strip():
        raise InviteError(
            f"{INVITE_TYPES[invite_type]['label']} has no booking button by "
            "design, so a booking link cannot be placed in it."
        )

    chrome = CHROME[invite_type]
    return _SHELL.format(
        label=chrome["label"],
        title=chrome["title"],
        position=_e(ctx.get("position")),
        body=_body(invite_type, ctx),
        cta=_cta(invite_type, ctx),
        signature=_signature(invite_type),
    )
