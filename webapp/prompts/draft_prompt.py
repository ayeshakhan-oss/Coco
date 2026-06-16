"""Build the per-candidate user prompt from the normalized scorecard.

IMPORTANT: the candidate's name comes from the candidates table (passed in),
NEVER from scorecard.candidateName — some scorecards contain a mismatched name
(confirmed: application 3364).
"""

from __future__ import annotations

from typing import Optional


def _values_evidence(sc: dict) -> str:
    lines = []
    if sc.get("proceed_to_right_seat"):
        lines.append(f"Overall recommendation to proceed: {sc['proceed_to_right_seat']}")
    if sc.get("final_comments"):
        lines.append(f"Interviewer final comments: {sc['final_comments']}")
    lines.append("Per-value observations:")
    for v in sc.get("values", []):
        rating = v.get("rating") or "(no rating)"
        bits = [f"- {v.get('name', '')} [{rating}]"]
        if v.get("deep_dive"):
            bits.append(f"deep dive: {v['deep_dive']}")
        if v.get("curve_ball"):
            bits.append(f"curveball: {v['curve_ball']}")
        if v.get("micro_case"):
            bits.append(f"micro-case: {v['micro_case']}")
        lines.append("  " + " | ".join(bits))
    return "\n".join(lines)


def _gwc_evidence(sc: dict) -> str:
    lines = []
    if sc.get("final_mark"):
        lines.append(f"Final mark: {sc['final_mark']}")
    if sc.get("additional_comments"):
        lines.append(f"Interviewer comments: {sc['additional_comments']}")
    lines.append("Competency scores:")
    for c in sc.get("competencies", []):
        lines.append(f"  - {c.get('name', '')}: score {c.get('score')} (weight {c.get('weight')})")
    return "\n".join(lines)


def build_user_prompt(
    *,
    scorecard: Optional[dict],
    first_name: str,
    role: str,
    email_type: str,
) -> str:
    if scorecard and scorecard.get("kind") == "values":
        evidence = _values_evidence(scorecard)
    elif scorecard and scorecard.get("kind") == "gwc":
        evidence = _gwc_evidence(scorecard)
    else:
        evidence = "(no structured scorecard available; rely only on what is explicitly provided)"

    intent = {
        "cv_rejection": "an application-stage update letting them know we will not be moving forward, with specific, useful reflection",
        "values_feedback": "warm, specific feedback after a values-based interview",
        "warm_bench": "a 'not a yes for now' message that keeps the door open and is honest about the gap",
        "gwc_rejection": "an honest, dignified decision that we will not be moving forward, grounded in the interview",
    }.get(email_type, "candidate communication")

    return f"""Draft {intent}.

Candidate first name (use this EXACTLY for the greeting; ignore any name inside
the scorecard): {first_name}
Role applied for: {role}

Scorecard evidence to ground the email in (do not quote ratings or internal
labels verbatim; translate them into plain, specific observations):

{evidence}

Write the email per the system rules and the output contract. Return JSON only."""
