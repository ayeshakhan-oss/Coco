"""Assemble the LLM's content-only JSON into the locked v8 HTML.

The model never emits HTML — it returns plain text in a fixed JSON shape, and
THIS module renders it through the locked v8 helpers (H/SUB/P/PS/wrap/...). The
section HEADINGS come from the eval's SECTION_HEADINGS (canonical) and are
applied positionally, so the required-heading HARD-BLOCK can never be tripped by
a model that paraphrases a heading.
"""

from __future__ import annotations

import html as _html
from typing import Optional

from ..reuse import (
    EYEBROW,
    FOOTER,
    H,
    P,
    PS,
    SUB,
    SECTION_HEADINGS,
    feedback_widget,
    wrap,
)

_DEFAULT_TITLE = {
    "cv_rejection": "A note on your application",
    "values_feedback": "A note on your conversation with us",
    "warm_bench": "Where things stand, and where we hope they go",
    "gwc_rejection": "A note on where we landed",
}


def _esc(text: str) -> str:
    # Body text is plain prose from the model; escape HTML special chars so it
    # renders as text inside the v8 paragraphs.
    return _html.escape(text or "", quote=False)


def render_body(
    content: dict,
    *,
    email_type: str,
    candidate_name: str,
    role: str,
    app_id,
) -> str:
    required = SECTION_HEADINGS.get(email_type, {}).get("required", [])
    sections = content.get("sections") or []
    parts: list[str] = []

    greeting = content.get("greeting") or f"Dear {candidate_name},"
    parts.append(P(_esc(greeting)))

    for para in content.get("opening") or []:
        if para:
            parts.append(P(_esc(para)))

    for i, heading in enumerate(required):
        parts.append(H(heading))
        sec = sections[i] if i < len(sections) else {}
        if isinstance(sec, dict):
            if sec.get("subhead"):
                parts.append(SUB(_esc(sec["subhead"])))
            for para in sec.get("paragraphs") or []:
                if para:
                    parts.append(P(_esc(para)))

    ps = content.get("ps")
    if ps:
        parts.append(PS(f"<strong>P.S.</strong> {_esc(ps)}"))

    parts.append(feedback_widget(candidate_name, role, app_id, "Application Feedback"))
    parts.append(FOOTER)
    return "\n".join(parts)


def attach_headings(content: dict, email_type: str) -> dict:
    """Stamp each section with its canonical heading (from the eval's
    SECTION_HEADINGS) so the editor can show heading labels. Rendering still
    applies headings positionally, so this is purely for display."""
    required = SECTION_HEADINGS.get(email_type, {}).get("required", [])
    sections = content.get("sections") or []
    for i, sec in enumerate(sections):
        if isinstance(sec, dict) and i < len(required):
            sec["heading"] = required[i]
    return content


def title_for(content: dict, email_type: str) -> str:
    return (content.get("title_line") or _DEFAULT_TITLE.get(email_type, "A note from us")).strip()


def wrap_full(body_html: str, *, title_line: str, role: str, email_type: str) -> str:
    eyebrow = EYEBROW.get(email_type, EYEBROW["cv_rejection"])
    return wrap(subject_line=title_line, role=role, eyebrow=eyebrow, body_html=body_html)


def preview_html(full_html: str, logo_url: str = "/api/assets/logo.png") -> str:
    """Swap the embedded cid logo for an http URL so the email renders in a browser preview."""
    return full_html.replace("cid:taleemabad_logo", logo_url)
