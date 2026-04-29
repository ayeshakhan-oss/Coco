"""
Template Loader Utility

Loads locked HTML templates from templates/ folder.
Ensures templates are always in sync with code.
"""

import os
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


def load_interview_invite_template():
    """
    Load the locked universal interview invite template.

    Template uses placeholders:
    - {label}: "PEOPLE & CULTURE • [STAGE]"
    - {position}: Position name
    - {subtitle}: Stage subtitle
    - {candidate_name}: Candidate name
    - {body_html}: Main body content (HTML)
    - {booking_link}: Calendar booking link
    - {button_text}: Button text (e.g., "📅 Lock the Calendar")
    - {button_subtext}: Text below button

    Returns:
        str: HTML template with placeholders
    """
    template_path = TEMPLATES_DIR / "interview_invite.html"

    if not template_path.exists():
        raise FileNotFoundError(f"Interview invite template not found: {template_path}")

    return template_path.read_text(encoding='utf-8')


def format_interview_invite(
    candidate_name,
    position,
    label,
    subtitle,
    body_html,
    booking_link,
    button_text="📅 Lock the Calendar",
    button_subtext="Please lock a slot at your earliest convenience."
):
    """
    Format the interview invite template with provided values.

    Args:
        candidate_name: Candidate's first name
        position: Job position name
        label: Header label (e.g., "PEOPLE & CULTURE • WARM BENCH OPPORTUNITY")
        subtitle: Subtitle text (e.g., "A New Role Aligned With Your Expertise")
        body_html: Main body content (HTML)
        booking_link: Google Calendar booking link
        button_text: CTA button text
        button_subtext: Text below button

    Returns:
        str: Formatted HTML ready to send
    """
    template = load_interview_invite_template()

    return template.format(
        label=label,
        position=position,
        subtitle=subtitle,
        candidate_name=candidate_name,
        body_html=body_html,
        booking_link=booking_link,
        button_text=button_text,
        button_subtext=button_subtext
    )


if __name__ == "__main__":
    # Quick test
    print("Testing template loader...")
    template = load_interview_invite_template()
    print(f"[OK] Template loaded: {len(template)} characters")
    print(f"[OK] Template location: {TEMPLATES_DIR / 'interview_invite.html'}")
